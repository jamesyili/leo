# Closeup (Related Pins) Learned Retrieval - Deep Technical Dive

## Table of Contents
- [1. Overview](#1-overview)
- [2. System Architecture: Two Codebases](#2-system-architecture-two-codebases)
- [3. P2P LWS Two-Tower (Base)](#3-p2p-lws-two-tower-base)
- [4. P2P Learned Retrieval Two-Tower (Production)](#4-p2p-learned-retrieval-two-tower-production)
- [5. Tower Architectures in Detail](#5-tower-architectures-in-detail)
- [6. User Sequence Transformer](#6-user-sequence-transformer)
- [7. Semantic ID (RQ-VAE) Integration](#7-semantic-id-rq-vae-integration)
- [8. Loss Functions](#8-loss-functions)
- [9. Label Extraction and Head Configuration](#9-label-extraction-and-head-configuration)
- [10. Data Pipeline and Filtering](#10-data-pipeline-and-filtering)
- [11. Evaluation and Inference](#11-evaluation-and-inference)
- [12. Training Pipeline](#12-training-pipeline)
- [13. Comparison: Closeup LR vs. HF CLR](#13-comparison-closeup-lr-vs-hf-clr)
- [14. Key File Reference](#14-key-file-reference)

---

## 1. Overview

Closeup (also known as "Related Pins" or P2P / pin-to-pin) is the surface that shows related pins when a user taps on a pin. The **Closeup Learned Retrieval** system uses a two-tower model to retrieve candidate pins that are relevant to a **query pin** in the context of a **viewer** (user).

Unlike Homefeed CLR (which retrieves pins for a user based on interests/boards/pin conditions), Closeup LR retrieves pins related to a **specific source pin**. The query tower sees both user features AND the query pin's features; the candidate tower sees candidate pin features.

There are **two separate two-tower implementations** for closeup:

1. **`closeup/p2p_lws/two_tower/`** - A simpler base model used for LWS (Learned Weighted Sum) and basic retrieval
2. **`closeup/p2p_learned_retrieval/`** - The full production model with DHEN, multi-head, semantic IDs, distillation, and advanced loss functions

---

## 2. System Architecture: Two Codebases

### Why Two Implementations?

The `p2p_lws/two_tower/` codebase is a standalone re-implementation of the base two-tower architecture specifically for closeup. It inherits nothing from the homefeed two-tower code (`mlenv/two_tower/`). The `p2p_learned_retrieval/` builds on this with production-grade features.

```
closeup/
  p2p_lws/two_tower/         <-- Base TT model (simpler, for LWS)
    model.py                      TwoTowerModel, TwoTowerDeployableModel
    modules.py                    PinTower, ViewerTower, UserSequenceTransformerEncoder

  p2p_learned_retrieval/      <-- Production TT model (advanced)
    model.py                      TwoTowerModel (with DHEN, distillation, SID, multi-head)
    modules.py                    PinTowerOrganic, ViewerTowerOrganic, DHENPinTower, DHENViewerTower
    label_extractor.py            P2PLearnedRetrievalLabelExtractor
    filters.py                    Train/eval data filtering
    train.py                      P2PLearnedRetrievalTrainer
    eval_utils.py                 Inference functions
    evaluator.py                  Evaluation pipeline
```

---

## 3. P2P LWS Two-Tower (Base)

Located in `closeup/p2p_lws/two_tower/model.py`.

### 3.1 TwoTowerModel

This is a **single-head** two-tower model. Key characteristics:

- **Query tower** = "viewer tower" (user features + query pin features from `PASSED_IN_DATA`)
- **Candidate tower** = "pin tower" (candidate pin features from `RELATED_PINS_UFR_CAND_PIN_FEATURES`)
- Shared embedding table between towers
- Embedding dimension sizing: `16` if vocab < 465, else `64`
- Single `InBatchNegativeLoss` (not multi-head)

```python
# Feature group assignment
DEFAULT_PIN_FEATURE_GROUP_NAMES = {"RELATED_PINS_UFR_CAND_PIN_FEATURES"}
DEFAULT_VIEWER_FEATURE_GROUP_NAMES = {"PASSED_IN_DATA"}
```

### 3.2 Forward Pass

```
batch
  |
  +-- _get_raw_features() (exclude labels)
  |
  +-- viewer_tower_model(batch) -> viewer_embeddings [B, num_heads, D]
  +-- pin_tower_model(batch)    -> pin_embeddings    [B, D]
  |
  +-- maybe_dedup_negatives()
  +-- InBatchNegativeLoss (per head)
  +-- Logistic loss (BCE with global_bias)
  |
  v
total_loss = ibn_weight * ibn_loss + logistic_weight * log_loss
```

### 3.3 Deployment

The `TwoTowerDeployableModel` subclass adds TorchScript export info (`DEPLOY_INFO`) for both towers. The `build_two_tower_torchscript_converter_fn` creates separate TorchScript models for pin and viewer towers, logged to MLflow.

---

## 4. P2P Learned Retrieval Two-Tower (Production)

Located in `closeup/p2p_learned_retrieval/model.py`.

This is the production-grade model with significantly more features:

### 4.1 Key Differences from Base

| Feature | Base (p2p_lws) | Production (p2p_learned_retrieval) |
|---------|---------------|------------------------------------|
| **Heads** | Single head | Multi-head (closeup, clicks, SRSD, combined) |
| **Loss** | `InBatchNegativeLoss` | `InBatchNegativeLossMultihead` |
| **Feature crossing** | MLP or TransformerMixer | DHEN (EnsembleInteractionLayers) |
| **Embedding tables** | Shared | Separate per tower (optional) |
| **Semantic IDs** | No | RQ-VAE tokenizer + cascading fusion |
| **Distillation** | No | MSE distillation from teacher model |
| **Random negatives** | No | Separate random negative dataloader |
| **Auxiliary losses** | No | SID contrastive, C2C, Q2Q contrastive |
| **Gradient analysis** | No | Per-head gradient cosine similarity tracking |
| **Data loading** | Simple | `StatefulStackLoader` (train + index) |

### 4.2 Model Variants

The model dynamically selects tower implementations:

```python
# Pin tower selection
if is_shopping_lr:       PinTower          (shopping variant)
elif dhen_model_config:  DHENPinTower      (DHEN feature crossing)
else:                    PinTowerOrganic   (standard MLP)

# Viewer tower selection
if is_shopping_lr:       ViewerTower        (shopping variant)
elif dhen_model_config:  DHENViewerTower    (DHEN with parallel sub-towers)
else:                    ViewerTowerOrganic (standard MLP)
```

### 4.3 Forward Pass (Production)

```
batch = {"train": train_batch, "index": random_neg_batch}
  |
  +-- label_extractor.get_labels_weights()   -> head_labels [H, B], head_weights [H, B]
  +-- viewer_tower_model(features)           -> viewer_emb  [B, H, D]
  +-- pin_tower_model(features)              -> pin_emb     [B, D]
  |
  +-- (optional) SID contrastive loss between query/candidate SID embeddings
  |
  +-- AllGatherWithGrad (optional, for multi-GPU negatives)
  +-- maybe_dedup_negatives()
  |
  +-- (optional) random negatives: pin_tower(rand_neg_batch) -> merge with in-batch negatives
  |
  +-- InBatchNegativeLossMultihead(viewer_emb, pin_emb, negatives, ...)
  |
  +-- (optional) logistic loss: BCE(dot(viewer, pin) * exp(temp) + bias, labels)
  +-- (optional) distillation loss: MSE(student_logits, teacher_preds)
  +-- (optional) SID contrastive loss * weight
  +-- (optional) C2C contrastive loss (candidates co-triggered by same query)
  +-- (optional) Q2Q contrastive loss (queries co-triggering same candidate)
  |
  v
total_loss = sum of all weighted losses
```

---

## 5. Tower Architectures in Detail

### 5.1 PinTowerOrganic (Candidate Tower)

`p2p_learned_retrieval/modules.py:506-658`

Processes candidate pin features:

```
Input: candidate pin features (RELATED_PINS_UFR_CAND_PIN_FEATURES)
  |
  +-- nan_to_num(0.0) for all features
  +-- GroupFeatureSelection
  +-- FeatureDropOutInput (optional, prob=pin_feature_dropout_prob)
  +-- FormatFeatureRegistryInput
  +-- representation_layers:
  |     +-- AutoML continuous normalization
  |     +-- Batch dense normalization
  |
  +-- embedding_layer (BatchMergedIdEmbeddingTable) OR sid_embedding_layer
  |     |
  |     +-- (if tokenizer): RQ-VAE encode -> semantic_id_0..7 -> embed -> cascading fusion
  |
  +-- feature_crossing:
  |     +-- MAE assertion (training only, < 10000)
  |     +-- feature_mixer_layers (MLP or TransformerMixer)
  |     +-- (optional) L2 normalize
  |
  v
pin_embedding [B, D]
```

### 5.2 ViewerTowerOrganic (Query Tower)

`p2p_learned_retrieval/modules.py:661-888`

Processes user features AND query pin features together:

```
Input: user features + query pin features (PASSED_IN_DATA)
  |
  +-- nan_to_num(0.0) for all features
  +-- GroupFeatureSelection
  +-- FormatFeatureRegistryInput
  |
  +-- Separate continuous feature processing:
  |     +-- user_representation_layers(user_continuous) -> user_continuous
  |     +-- pin_representation_layers(pin_continuous)   -> pin_continuous
  |
  +-- embedding_layer OR sid_embedding_layer
  |     |
  |     +-- (if tokenizer): RQ-VAE encode -> cascading fusion
  |
  +-- (if enabled) UserSequenceTransformerEncoder
  |
  +-- feature_crossing:
  |     +-- feature_mixer_internal_layers (concat + layernorm)
  |     +-- feature_mixer_output_layer (FC layers)
  |     +-- (optional) L2 normalize
  |
  v
viewer_embedding [B, H*D]  (reshaped to [B, H, D] by model)
```

**Important:** The viewer tower in closeup sees **both** user features and query pin features. This is fundamentally different from homefeed CLR where the viewer tower only sees user features. The query pin's OmniSage embedding, content type, and other features flow through `PASSED_IN_DATA`.

### 5.3 DHENViewerTower (Production DHEN Variant)

`p2p_learned_retrieval/modules.py:973-1000`

Extends `ViewerTowerOrganic` with a **multi-tower parallel DHEN architecture**:

```
feature_crossing:
  |
  +-- Split features by prefix:
  |     user_features  = {k:v for k,v if "user" in k}
  |     pin_features   = {k:v for k,v if "pin" in k}
  |     context_features = {k:v for k,v if "context" in k}
  |
  +-- Parallel processing (torch.jit.fork):
  |     user_future   = DimensionUnifier -> LayerNorm -> DHEN_user
  |     pin_future    = DimensionUnifier -> LayerNorm -> DHEN_pin
  |     context_future = context_MLP
  |
  +-- Collect results (torch.jit.wait)
  |
  +-- Inter-group fusion:
  |     DimensionUnifier({"user":..., "query_pin":..., "context":...})
  |     LayerNorm
  |     final_crossing_DHEN
  |     final_cross_MLP -> [B, H*D]
  |
  v
viewer_embedding [B, H*D]
```

Each sub-tower has its own DHEN config (`dhen_user_config`, `dhen_pin_config`, `dhen_final_crossing_config`), allowing different interaction patterns for user vs pin features.

### 5.4 DHENPinTower

`p2p_learned_retrieval/modules.py:1003-1014`

Simpler than the viewer: a single DHEN pipeline.

```
features -> DimensionUnifier -> LayerNorm -> DHEN -> Linear(D) -> pin_embedding
```

### 5.5 DimensionUnifier / LazyDimensionUnifier

`p2p_learned_retrieval/modules.py:1117-1161`

Projects all feature groups to a uniform dimension before DHEN processing. Special handling for continuous features: they are replicated `continuous_field_num` times (default 4) with separate linear projections, allowing the DHEN to attend to the same continuous features in different representation subspaces.

---

## 6. User Sequence Transformer

### 6.1 Base Version (`p2p_lws/two_tower/modules.py:50-261`)

Encodes user action history using a Transformer encoder.

**Action vocabulary:**
```python
# Action types and their semantic meaning:
# 0 - None (padding)     2 - PIN_REPIN        4 - PIN_CLOSEUP
# 5 - PIN_COMMENT       13 - PIN_CLICK_THROUGH  15 - PIN_HIDE
# 62 - PIN_REACT        70 - STORY_PIN_10S_CLOSEUP
# 71 - STORY_PIN_2S_CLOSEUP  75 - FULL_SCREEN_VIEW_10S
# 76 - FULL_SCREEN_VIEW_2S
```

**Architecture:**
```
Input: action_types [B, 200], seq_embeddings [B, 200, 32], timestamps [B, 200]
  |
  +-- Trim to seq_len (most recent N actions)
  +-- Action vocab lookup -> action_emb [B, seq_len, 32]
  +-- Concat: [action_emb | seq_emb] = [B, seq_len, 64]
  +-- (optional) concat context features (query GSV5, PinnerSage mini) as tokens
  +-- (optional) concat candidate embedding
  |
  +-- Create padding mask (action_type <= 0)
  |
  +-- TransformerEncoder(src, mask)
  |
  +-- Output: max_pool(linear(tfmr_out)) + flatten(latest_n)
  |
  v
batch["seq_emb_ft_name"] = concatenated output
```

**Context features as sequence tokens:** When `concat_context_features=True`, query-level features (GSV5 mini, PinnerSage mini) are projected to the transformer dimension and prepended to the sequence as additional tokens. Each gets a learned "fake action embedding" since they aren't real actions.

### 6.2 Production Version (`p2p_learned_retrieval/modules.py:65-267`)

Extends the base with:

- **Surface embedding** (`use_surface_embedding=True`): Each action has a surface type (which Pinterest surface the action occurred on). Surface vocab includes homepage, search, closeup, etc. Adds 8-D surface embedding to each sequence token.
- **Timestamp embedding** (`use_timestamp_embedding=True`): Time difference between request and action is bucketized into log-spaced buckets (50 buckets spanning 0 to 1 year), then embedded into 16-D. This gives the transformer temporal awareness.
- **Random time window masking**: During training, randomly samples a time window `[0, time_window_ms]` to mask recent actions, preventing the model from relying too heavily on very recent behavior.

**Full token composition:**
```
token = [action_emb(16D) | seq_emb(32D) | surface_emb(8D) | timestamp_emb(16D)]
       = 72D total
```

---

## 7. Semantic ID (RQ-VAE) Integration

The production model optionally integrates **Residual Quantized VAE (RQ-VAE)** semantic IDs to provide a hierarchical discrete representation of pin content.

### 7.1 How It Works

```python
def process_semantic_id_embedding(batch, feature_name, tokenizer, embedding_layer, cascading_fusion_layers):
    # 1. Encode pin's content embedding through frozen RQ-VAE tokenizer
    seq_embs = batch[feature_name]       # [B, 256] content embedding
    semantic_ids = tokenizer.encode(seq_embs)  # [B, n_codebooks] (e.g., [B, 8])

    # 2. Add each codebook level as a separate feature
    for i in range(tokenizer.n_codebooks):
        batch[f"semantic_id_{i}"] = semantic_ids[:, i]  # each is a codebook index

    # 3. Embed through the main embedding layer
    output = embedding_layer(batch)

    # 4. Cascading fusion: hierarchically combine content emb with SID embeddings
    #    MLP[MLP[MLP[content_emb, SID_0], SID_1], SID_2], ...]
    current = output[feature_name]
    for i, fusion_layer in enumerate(cascading_fusion_layers):
        current = fusion_layer(torch.cat([current, output[f"semantic_id_{i}"]], dim=1))
    output['pin_cascading_fusion'] = current
```

**Tokenizer config (default):**
```python
feature_emb_dim = 256
n_codebooks = 8
codebook_size = 2048
hidden_dims = [4096, 2048, 1024, 512, 256]
```

The tokenizer is always **frozen** (no gradient flows through it). SID embeddings learned by the two-tower model provide a learnable interface to the frozen discrete codes.

### 7.2 SID Contrastive Loss

When `enable_sid_contrastive_loss=True`, an additional loss aligns query and candidate SID embeddings:

```python
for each codebook level i:
    similarity = query_sid_i @ candidate_sid_i.T / temperature
    loss_i = (CE(similarity, arange(B)) + CE(similarity.T, arange(B))) / 2
total_sid_loss = sum(loss_i)
```

This is a symmetric InfoNCE loss applied per-codebook level.

---

## 8. Loss Functions

### 8.1 In-Batch Negative Loss (Primary)

`InBatchNegativeLossMultihead` - Same as described in the CLR doc. Multi-head version computes loss across all (head, sample) registers simultaneously.

### 8.2 Logistic Loss (Global Bias)

```python
logits = dot(viewer_emb, pin_emb) * exp(global_temp) + global_bias  # per head
loss = BCEWithLogitsLoss(logits, labels, weights)
```

Both `global_temp` and `global_bias` are learnable per-head parameters.

### 8.3 Distillation Loss

When a teacher model is provided (`teacher_model_path`):

```python
student_logits = dot(viewer_emb, pin_emb) * exp(global_temp_distill) + global_bias_distill
teacher_preds = teacher_model.eval_forward(batch)  # [B, 4] (4 teacher heads)
loss = MSE(student_logits, teacher_preds) * distillation_loss_weight
```

Uses `MultiHeadLRMSEDistillationLoss` from `closeup/modules/loss.py`.

### 8.4 Candidate-to-Candidate (C2C) Contrastive Loss

```python
# If two candidate pins were triggered/shown/clicked by the same query pin,
# their embeddings should be closer
cooccurrence_mask = (query_ids[i] == query_ids[j])  # same query -> positive pair
similarity = candidate_embs @ candidate_embs.T / temperature
loss = -log(sum_pos_exp / (sum_pos_exp + sum_neg_exp))
```

### 8.5 Query-to-Query (Q2Q) Contrastive Loss

```python
# If two queries both triggered the same candidate pin,
# their embeddings should be closer
cooccurrence_mask = (candidate_ids[i] == candidate_ids[j])  # same candidate -> positive pair
similarity = query_embs @ query_embs.T / temperature
loss = -log(sum_pos_exp / (sum_pos_exp + sum_neg_exp))
```

### 8.6 Total Loss

```python
total_loss = (
    in_batch_neg_weight * ibn_loss
    + logistic_weight * logistic_loss.mean()
    + distillation_weight * distill_loss
    + sid_contrastive_weight * sid_contrastive_loss
    + c2c_weight * c2c_loss
    + q2q_weight * q2q_loss
)
```

---

## 9. Label Extraction and Head Configuration

### 9.1 P2PLearnedRetrievalLabelExtractor

`p2p_learned_retrieval/label_extractor.py:31-202`

Responsible for computing labels and weights for each model head. Supports three modes:

**Multi-head mode** (`multi_head=True`):
Each engagement type is a separate head:
- closeup, clickthrough, long_clickthrough, repin, screenshot, save_to_device, react, revisitation_7d

**Combined single-head mode** (`use_combined_head=True`):
- Label = 1 if ANY action is positive
- Weight = max weight across positive actions

**Combined multi-head mode** (`enable_combined_multi_head=True`):
Three merged heads:
- `close_up`: closeup only
- `combined_clicks`: clickthrough OR long_clickthrough
- `combined_srsd`: repin OR screenshot OR save_to_device OR react OR revisitation_7d

### 9.2 Hard Negatives

Certain actions flip positive labels to negative:
```python
HARD_NEGATIVE_ACTIONS = [SHORT_CLICKTHROUGH, HIDE]
NEGATIVE_ACTION_WEIGHTS = {SHORT_CLICKTHROUGH: 3.0, HIDE: 3.0}
```

If a sample has both a positive engagement (e.g., closeup) AND a hard negative (e.g., short click or hide), the label becomes 0 with the hard negative weight (3.0). This trains the model to avoid retrieving pins that lead to quick bounces or hides.

### 9.3 Content Boosting

```python
# Product pins get boosted weight
if tw_product_boost != 0:
    weights = where(content_type == 4, weights * (1 + tw_product_boost), weights)

# Fresh pins get boosted weight
if fresh_boost != 0:
    weights = where(is_fresh, weights * (1 + fresh_boost), weights)
```

---

## 10. Data Pipeline and Filtering

### 10.1 Training Data

Uses `StatefulStackLoader` that combines two data streams:
- **`train`**: Main training data (user + query pin + candidate pin + labels)
- **`index`**: Random negative data (separate corpus for harder negatives)

When random negatives are enabled, the train batch size is halved (e.g., 6000 -> 3000) to make room.

### 10.2 Training Filters

```python
def filter_train_fn(table, label_sampling_rate_map):
    # For each label, keep positive samples always, downsample negatives
    # e.g., {"LABEL/num_repins": 0.9} keeps all repins, drops 90% of non-repins
    # Uses OR logic: if ANY label says keep, the row is kept
```

### 10.3 Eval Filters

```python
EvalFilterType.SAMPLE         # 10% sample by user_id % 100 < 10
EvalFilterType.FRESH_ONLY     # Only fresh candidate pins
EvalFilterType.PRODUCT_ONLY   # Only product candidate pins
EvalFilterType.FRESH_AND_PRODUCT  # Fresh OR product
```

---

## 11. Evaluation and Inference

### 11.1 Inference Function

`eval_utils.py:59-158`

```python
def p2p_learned_retrieval_inference_fn(example, model, ...):
    viewer_embeddings, pin_embeddings = model.eval_forward(example)

    # Normalize for cosine similarity
    norm_viewer = F.normalize(viewer_embeddings)
    norm_pin = F.normalize(pin_embeddings)

    # Multi-head: reshape viewer to [B, H, D], pin to [B, 1, D]
    # normalized_dot_product_score = sum over heads and dims
    # normalized_repin_dot_product_score = last head only (repin head)

    return {
        user_id, entity_id, query_id,
        viewer_embedding, entity_embedding,
        normalized_dot_product_score,
        normalized_repin_dot_product_score,
        # Per-action labels for offline eval:
        w_closeup, w_clicks, w_longclicks, w_repin,
        w_screenshot, w_save_to_device, w_react, w_revisit, w_combined_srsd,
        cand_content_type, is_candidate_pin_fresh,
    }
```

### 11.2 Evaluation Metrics

The eval pipeline writes parquet predictions and computes recall@K metrics. The HPT optimization target is:
```python
OPTIMIZATION_CONFIG = OptimizationConfig(
    objective_name="eval_w_repin/ALL_10",  # repin recall@10
    minimize=False,
)
```

### 11.3 Gradient Transfer Analysis

The production model includes built-in negative transfer detection between heads:

```python
def _compute_negative_transfer_metrics_from_head_losses(self, head_losses, params, head_names):
    # For each pair of heads:
    #   grad_mag_{head}: ||gradient|| magnitude
    #   grad_dot_{head_i}_{head_j}: cosine similarity between gradients
    #
    # Interpretation:
    #   cos > 0: aligned (optimizing one helps the other)
    #   cos ~ 0: orthogonal (independent)
    #   cos < 0: conflicting (negative transfer!)
```

Reports moving averages over the last 10 batches.

---

## 12. Training Pipeline

### 12.1 P2PLearnedRetrievalTrainer

`train.py:108-655`

Extends `CloseupBaseRunner`. Key workflow:

1. **Feature stats**: `load_or_calc_feature_stats()` - auto-calculates if missing
2. **Label extractor**: Configures heads based on `is_p2p_shopping`, `multi_head`, `use_combined_head`
3. **Model creation**: `make_two_tower_deployable_model(locate(model_class_path))(...)` - dynamically loads model class
4. **Optional warm start**: `TwoTowerFaultTolerantSolver.load_pretrain_weights(model, snapshot)`
5. **Optional tower freezing**: `freeze_viewer_tower`, `freeze_pin_tower`
6. **Optimizer**: `FusedAdam(lr, betas=(0.9, 0.999))`
7. **LR schedule**: Constant schedule (no decay)
8. **Solver**: `TwoTowerFaultTolerantSolver` with fault-tolerant checkpointing via `WandbCheckPointManager`
9. **Deployment**: Separate TorchScript export for viewer and pin towers

### 12.2 Tokenizer Loading

```python
def load_tokenizer(self, device):
    tokenizer = RQVAETokenizer(config)  # 256D -> 8 codebooks x 2048 codes
    tokenizer.load_pretrained_weights(snapshot)
    tokenizer.eval()
    for param in tokenizer.parameters():
        param.requires_grad = False  # always frozen
```

### 12.3 Feature Attribution

When `run_attribution=True`, the trainer runs feature attribution at the final evaluation iteration using `two_tower_retrieval_attribution_fn` and `two_tower_retrieval_post_attribution_fn` from the attribution utils.

---

## 13. Comparison: Closeup LR vs. HF CLR

| Aspect | Closeup Learned Retrieval | Homefeed CLR |
|--------|--------------------------|--------------|
| **Surface** | Related Pins (pin-to-pin) | Homefeed (user-to-pin) |
| **Query** | User + query pin features | User features + condition |
| **Conditions** | None (query pin IS the condition) | Interest, Board, Pin |
| **Viewer tower input** | `PASSED_IN_DATA` (user + query pin) | User features only (conditions routed separately) |
| **Pin tower input** | `RELATED_PINS_UFR_CAND_PIN_FEATURES` | `PINNABILITY_PIN_FEATURES` |
| **Multi-output** | Single embedding per head | Multiple embeddings per condition |
| **DHEN variant** | Multi-tower DHEN (user/pin/context sub-towers) | Single DHEN with feature_mix_dict weights |
| **Semantic IDs** | RQ-VAE tokenizer + cascading fusion | Not used |
| **Distillation** | Teacher model MSE | Relevance loss (PinCLIP alignment) |
| **Random negatives** | Separate random negative dataloader | Not used |
| **Auxiliary losses** | SID contrastive, C2C, Q2Q | None |
| **Sequence features** | Action + surface + timestamp embeddings | Action + OmniSage embeddings |
| **Hard negatives** | Short clicks and hides flip labels | Not used |
| **Codebase** | Standalone in closeup/ | Extends mlenv/two_tower/ base classes |

---

## 14. Key File Reference

### Core Model Files

| File | Purpose |
|------|---------|
| `closeup/p2p_lws/two_tower/model.py` | Base TwoTowerModel, TwoTowerDeployableModel, TorchScript export |
| `closeup/p2p_lws/two_tower/modules.py` | Base PinTower, ViewerTower, UserSequenceTransformerEncoder |
| `closeup/p2p_learned_retrieval/model.py` | Production TwoTowerModel with DHEN, multi-head, SID, distillation |
| `closeup/p2p_learned_retrieval/modules.py` | PinTowerOrganic, ViewerTowerOrganic, DHENPinTower, DHENViewerTower, DimensionUnifier, contrastive losses |

### Training and Evaluation

| File | Purpose |
|------|---------|
| `closeup/p2p_learned_retrieval/train.py` | `P2PLearnedRetrievalTrainer` - full training pipeline |
| `closeup/p2p_learned_retrieval/label_extractor.py` | Multi-head label extraction with hard negatives |
| `closeup/p2p_learned_retrieval/filters.py` | Train/eval data filtering functions |
| `closeup/p2p_learned_retrieval/eval_utils.py` | Inference function producing embeddings + scores |
| `closeup/p2p_learned_retrieval/evaluator.py` | Evaluation pipeline |

### Config Files

| File | Purpose |
|------|---------|
| `ml_resources/mlenv/p2p/configs/learned_retrieval_train_config.py` | `P2PLearnedRetrievalAppConfig`, `P2PLearnedRetrievalConfigBundle` |
| `ml_resources/mlenv/p2p/configs/lws_configs.py` | LWS-specific configs, `UserSequenceTransformerConfig` |
| `ml_resources/mlenv/p2p/labels/label_constants.py` | `HeadConfig`, `P2pLabel`, head config lists |
| `ml_resources/mlenv/p2p/features/p2p_learned_retrieval_feature_map.py` | Feature maps, continuous feature lists |
| `ml_resources/mlenv/p2p/features/closeup_feature_map_keys.py` | Closeup feature definitions |

### Shared Modules

| File | Purpose |
|------|---------|
| `closeup/modules/loss.py` | `MultiHeadLRMSEDistillationLoss` |
| `closeup/modules/mmoe.py` | `MMoEModuleLR` (Multi-gate Mixture of Experts) |
| `closeup/modules/user_seq.py` | `GSV5Normalization` |
| `closeup/rqvae/tokenizer.py` | `RQVAETokenizer` for semantic ID generation |
| `trainer/ppytorch/modules/metric_learning.py` | `InBatchNegativeLossMultihead` |

All paths relative to `machine-learning/trainer/ppytorch/mlenv/`.
