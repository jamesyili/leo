# Conditional Learned Retrieval (CLR) - Deep Technical Dive

## Table of Contents
- [1. Overview](#1-overview)
- [2. Motivation: Why Conditional Retrieval?](#2-motivation-why-conditional-retrieval)
- [3. Architecture](#3-architecture)
- [4. The Condition System](#4-the-condition-system)
- [5. Model Components in Detail](#5-model-components-in-detail)
- [6. Training Pipeline](#6-training-pipeline)
- [7. Loss Functions](#7-loss-functions)
- [8. Inference and Deployment](#8-inference-and-deployment)
- [9. Fine-Tuning](#9-fine-tuning)
- [10. Key File Reference](#10-key-file-reference)

---

## 1. Overview

CLR extends the standard **two-tower retrieval model** with a mechanism that produces **different user embeddings depending on the retrieval context** (called a "condition"). Instead of generating a single user embedding for all queries, CLR generates multiple embeddings - one per condition type - allowing the retrieval system to return different candidate sets depending on *why* the user is looking for content.

The core insight: a user searching for "dinner recipes" should retrieve different pins than the same user browsing their "Home Renovation" board, even though the user is the same. Standard two-tower models collapse all user intent into one embedding. CLR keeps them separate.

**Key classes:**
- `ConditionalDHENTwoTowerModel` - the primary production model (DHEN + CLR)
- `ConditionalTwoTowerModel` - simpler variant without DHEN feature crossing

---

## 2. Motivation: Why Conditional Retrieval?

Standard two-tower retrieval works like this:
```
User features  -->  [Viewer Tower]  -->  user_embedding (1 per user)
Pin features   -->  [Pin Tower]     -->  pin_embedding  (1 per pin)

Score = dot_product(user_embedding, pin_embedding)
```

The problem: a single user embedding must simultaneously encode ALL of the user's interests. For HNSW/ANN retrieval, this means the retrieved candidates are a compromise across all possible intents.

CLR solves this by making the user embedding **conditional on the retrieval context**:
```
User features + Condition  -->  [Conditioned Viewer Tower]  -->  user_embedding_for_condition
Pin features               -->  [Pin Tower]                 -->  pin_embedding

Score = dot_product(user_embedding_for_condition, pin_embedding)
```

At inference time, the system generates **one embedding per condition type** for each user, enabling separate ANN lookups per retrieval context.

---

## 3. Architecture

### Class Hierarchy

```
TwoTowerModel (base)
  |
  +-- ConditionalTwoTowerModel
  |     |
  |     +-- ConditionalDHENTwoTowerModel  (production model)
  |
  +-- DHENTwoTowerModel
        |
        +-- ConditionalDHENTwoTowerModel  (via multiple inheritance)
```

### High-Level Data Flow

```
Input Batch
    |
    +-- split_batch() --+
    |                    |
    v                    v
 Unconditioned       Condition Features
 Features            + User Sequence
    |                    |
    |                    v
    |              UserConditionTower
    |                |
    |                +-- create_routing_masks()       (which condition per sample)
    |                +-- _apply_*_dropout()            (training regularization)
    |                +-- format/embed features
    |                +-- ConditionRouter               (generate condition tokens)
    |                +-- ConditionedUserSequenceTransformer  (transformer over seq + condition)
    |                +-- TextEmbeddingModule(s)        (project SearchSage/PinCLIP)
    |                |
    |                v
    |           user_condition_outputs
    |                |
    +---------->  forward_inner()
                    |
                    +-- Regular feature processing
                    +-- Merge condition outputs into feature dict
                    +-- DHEN feature crossing
                    |
                    v
              viewer_embedding [B, H, D]
```

The pin tower is completely unchanged from the base two-tower model. Only the viewer (query) side is conditioned.

---

## 4. The Condition System

### 4.1 Condition Types

Three condition types are defined, each representing a different retrieval context:

| Type | Feature | Dimension | Meaning |
|------|---------|-----------|---------|
| **interest** | `common_pin_source_interest_id` | scalar (vocab ID) | Topical interest taxonomy node |
| **board** | `common_omnisage_v1_board_256d_fp16` | 256-D fp16 | OmniSage board embedding |
| **pin** | `common_omnisage_v1_pin_256d_fp16` | 256-D fp16 | OmniSage pin embedding (more-like-this) |

The **interest** condition also carries text embeddings:
- **SearchSage** (`common_query_search_sage_24_alpha_query_256d_embedding`) - 256-D
- **PinCLIP** (`common_query_pinclip_v1_text_256d_embedding`) - 256-D

These are pretrained text embeddings loaded from S3, not learned end-to-end.

### 4.2 Routing: Which Condition Gets Used?

Routing is determined by `create_routing_masks()` in `feature_names.py:146-156`:

```python
def create_routing_masks(config, batch):
    masks = {}
    cur_mask = torch.zeros(...)  # all False
    for c in config.condition_tags:  # ordered: interest, board, pin
        cond_masks = [is_default_value(f, batch[f]) for f in c.features]
        # A sample uses this condition if ANY feature is non-default AND
        # it hasn't already been claimed by a higher-priority condition
        masks[c.condition_type] = ~torch.stack(cond_masks).all(dim=0) & ~cur_mask
        cur_mask |= masks[c.condition_type]
    return masks
```

This is a **priority-based assignment**: conditions are checked in order (interest -> board -> pin). A sample is assigned to the first condition where it has a valid (non-default) feature value. Samples with no valid conditions get zeros for condition tokens.

### 4.3 Default Values

"No condition" is signaled by sentinel values:
- Interest ID: `-1` (invalid vocab ID)
- Board/Pin/Text embeddings: `torch.zeros(256)` in fp16

The function `is_default_value()` checks whether a feature matches its sentinel. For interest IDs specifically, it uses vocab range bounds (`MIX_P2I_VOCAB` to `MAX_P2I_VOCAB`) to detect invalid values.

### 4.4 Dummy Inference Features

At inference time, the model must produce embeddings for **all** condition types simultaneously from a single forward pass. This is achieved via **dummy features**: multiple copies of each condition feature slot are registered in the feature map.

For example, if the real request has an interest condition, dummy board and pin features are populated with the actual board/pin values. This allows a single batched forward pass to produce embeddings for all conditions.

---

## 5. Model Components in Detail

### 5.1 ConditionTokenGenerator (`modules.py:246-278`)

Converts raw condition features into a fixed-dimensional token that can be injected into the transformer sequence.

```python
class ConditionTokenGenerator(nn.Module):
    def __init__(self, tag_config, output_dim, cond_config):
        # If proj_cond_tokens=True: MLP with skip connection
        #   FullyConnectedLayers(output_size=output_dim, hidden_sizes=[output_dim*2], has_skip=True)
        # If proj_cond_tokens=False: zero-pad to output_dim
        #   MaybeRightPadToDim(output_dim=output_dim)

    def forward(self, batch) -> torch.Tensor:
        # 1. Filter batch to only this condition's features
        # 2. Concatenate them
        # 3. Project/pad to output_dim
        return output[..., :self.output_dim]
```

There are subclasses (`InterestConditionTokenGenerator`, `BoardConditionTokenGenerator`, `PinConditionTokenGenerator`) but they are currently identical - the differentiation is structural, for future extension.

**Output dimension:** `64 * num_condition_tokens` (default: 64 * 1 = 64). This matches the transformer's `d_model`.

### 5.2 ConditionRouter (`modules.py:281-350`)

Orchestrates condition processing across all condition types:

```python
def forward(self, batch, routing_masks):
    # Step 1: Extract ALL condition features from batch
    condition_batch = {f: batch.pop(f) for f in all_features}

    # Optional: keep raw concatenated features for residual connection
    if residual_input_condition_features:
        all_cond_feature_combined = torch.cat(condition_batch.values(), dim=-1)

    # Step 2: Generate tokens per condition type, masked by routing
    out = torch.zeros_like(...)
    for condition_type, token_generator in self.condition_processors.items():
        condition_tokens = token_generator(condition_batch)  # [B, 64]
        out = torch.where(routing_masks[condition_type].unsqueeze(-1),
                          condition_tokens, out)

    batch["condition_tokens"] = out  # [B, 64]
    batch["all_cond_feature_combined"] = all_cond_feature_combined  # for DHEN
    return batch
```

The `torch.where` with routing masks ensures each sample's token comes from the correct condition processor. Samples that match no condition get zero tokens.

### 5.3 ConditionedUserSequenceTransformer (`modules.py:78-223`)

The heart of CLR's sequence modeling. It processes the user's action history alongside condition tokens using a Transformer encoder.

**Architecture:**
```
Input:
  action_type_ids  [B, 500]  -->  action_emb  [B, seq_len, 32]
  sequence_embs    [B, 500, 32]
  condition_tokens [B, num_cond_tokens, 64]

Processing:
  1. Filter sequence by recency (optional, via realtime_seq_days)
  2. Truncate to seq_len (default 100)
  3. Embed action types: [B, seq_len, 32]
  4. Concatenate: [action_emb | seq_emb] = [B, seq_len, 64]
  5. Append condition tokens: [B, seq_len + num_cond_tokens, 64]
  6. Create padding mask (action_type <= 0 means padding; condition tokens never masked)
  7. Linear projection to d_model: [B, seq_len + num_cond_tokens, 64]
  8. Transformer encoder (2 layers, 8 heads, pre-layer-norm)

Output extraction:
  - user_seq: last N positions from sequence portion -> project -> "proj_user_seq"
  - cond_seq: condition token positions -> project -> "proj_condition_seq"
  - Optional: residual add raw condition tokens to cond_seq output
  - Optional: max-pool over sequence positions
```

**Key design choice:** Condition tokens are **appended** to the sequence (not prepended). This means they attend to all sequence positions via self-attention, and the sequence positions attend back to them. The condition tokens effectively act as a learned query over the user's history, filtered by the condition context.

**Residual connection** (`add_cond_tokens_to_tmr_output=True`): The raw condition token is added back to the transformer's output at the condition position. This ensures the condition signal isn't washed out by the transformer.

### 5.4 TextEmbeddingModule (`modules.py:353-378`)

Projects pretrained text embeddings (SearchSage, PinCLIP) through a small MLP before they enter the condition system.

Three projection variants:
1. `skip_text_emb_proj=True`: Identity (pass-through)
2. `text_emb_proj_v2=True` (default): `FullyConnectedLayers(256, [512], has_skip=True)` - MLP with skip connection
3. Legacy: `Linear(256, 512) -> ReLU -> Dropout(0.5) -> Linear(512, 256)`

### 5.5 UserConditionTower (`modules.py:381-530`)

The top-level module that orchestrates all viewer-side condition processing:

```python
def forward(self, batch):
    # 1. Compute routing masks
    routing_masks = create_routing_masks(config, batch)

    # 2. Training-time dropout
    if self.training:
        self._apply_interest_and_text_embedding_dropout(batch)
        self._apply_condition_feature_dropout(batch)

    # 3. Sequence stats (action counts, time aggregates)
    sequence_stats_embedding = self.sequence_stats_module(batch)

    # 4. Standard feature formatting + embedding
    output = format -> group -> embed(batch)

    # 5. Optional layer norm
    if use_layer_norm:
        output = dense_normalization_layer(output)

    # 6. Text embedding projection
    output = text_embedding_module(output)
    output = pinclip_text_embedding_module(output)

    # 7. Route conditions and generate tokens
    output = condition_router(output, routing_masks)

    # 8. Sequence transformer
    output = sequence_transformer_layer(output)

    return output  # Dict of named feature tensors
```

### 5.6 ConditionedViewerTower (`modules.py:533-697`)

Extends the base `ViewerTower` to split the batch and recombine:

```python
def forward(self, batch):
    unconditioned_batch, condition_batch = self.split_batch(batch)
    user_cond_out = self.condition_tower(condition_batch)
    output = self.forward_inner(unconditioned_batch, user_cond_out)
    return self.quantizer(output)
```

`forward_inner` processes unconditioned features normally (representation layers, embeddings, optional UOE/language modules), then **merges** the condition tower outputs into the feature dict before DHEN feature crossing.

### 5.7 Feature Crossing (DHEN)

DHEN (Deep Hierarchical Embedding Network) performs explicit feature interaction. The `feature_mix_dict` controls which feature groups interact and their relative weights:

```python
feature_mix_dict = {
    "continuous": 1,                        # Dense numeric features
    "proj_user_seq": 2,                     # Transformer user sequence output
    "all_cond_feature_combined": 8,         # Raw concatenated condition features (HIGH WEIGHT)
    "proj_cond_seq": 2,                     # Transformer condition token output
    "pinnersage_v3e_static_realtime": 1,    # PinnerSage embedding
    "pinnersage_v3e_static": 1,             # PinnerSage static
}
```

The weight of **8** on `all_cond_feature_combined` is notable - condition features dominate the feature mixing, ensuring the final embedding is heavily influenced by the retrieval context.

---

## 6. Training Pipeline

### 6.1 Training Data

Training samples come with:
- User features (demographics, embeddings, etc.)
- Pin features (the positive candidate)
- A condition context (interest/board/pin that triggered the impression)
- User action sequence (last 500 actions with timestamps and OmniSage embeddings)
- Labels per head (engagement signals: repin, click, etc.)

### 6.2 Dropout as Regularization

CLR uses two specialized dropout strategies during training:

**Condition feature dropout** (`dropout=0.10`):
- For each sample, randomly zero out the entire condition feature with 10% probability
- This forces the model to not over-rely on condition features
- Interest IDs are skipped if text embeddings are present (they have their own dropout)

**Interest/text embedding dropout** (`text_dropout=0.25`):
- Uses a joint scheme: with prob 0.25 drop the interest ID, with prob 0.25 drop the text embedding, with prob 0.50 keep both
- They're never dropped simultaneously (`rnd < 0.25` drops ID, `0.25 <= rnd < 0.50` drops text)
- This teaches the model to use either signal alone

### 6.3 Training Configuration

```
Batch size:     6,000
Iterations:     300,000
Learning rate:  10^(-2.7) ~ 0.002
Warmup steps:   5,000
UID IBN mask:   True (mask same-user negatives)
```

---

## 7. Loss Functions

### 7.1 In-Batch Negative Loss (Primary)

`InBatchNegativeLossMultihead` in `metric_learning.py:525-676`

This is a **softmax cross-entropy over in-batch negatives**, similar to the loss used in CLIP/DPR. For each positive (viewer, pin) pair, all other pins in the batch serve as negatives.

**Step-by-step:**

1. **Positive logit**: `dot(viewer_emb[i], pin_emb[i]) * exp(temperature)`
2. **Negative logits**: `viewer_emb[i] @ all_unique_neg_pin_embs.T * exp(temperature)`
3. **Masking**:
   - Same-item negatives -> `-inf` (a pin can't be its own negative)
   - Same-UID negatives -> `-inf` (if `uid_ibn_mask=True`, other pins from the same user aren't negatives)
4. **Sample probability correction** (if item counter provided):
   ```
   corrected_pos = pos_logit - log(P(positive appears in batch))
   corrected_neg = neg_logits - log(P(negative appears in batch))
   ```
   This adjusts for popular items being over-represented as negatives. The probability is computed as: `P(item in batch) = 1 - (1 - freq/total)^batch_size`
5. **Cross-entropy**: `CE([corrected_pos | corrected_neg], target=0)` where target=0 means the positive is always at index 0

**Temperature** is a **learnable parameter** initialized at `-log(1.0)` and clamped to `max=log(100)`.

**Multi-head handling**: The loss operates over "registers" - (head, sample) pairs where the label is valid. Different heads can have different positive sets. The total loss is averaged across heads.

### 7.2 Relevance Loss (Optional)

Aligns the two-tower similarity with PinCLIP similarity:
```
L_relevance = ||PinCLIP_sim(query, pin) - TT_sim(viewer_emb, pin_emb)||^2 * 200,000
```

This acts as a knowledge distillation signal from PinCLIP into the two-tower space.

### 7.3 Total Loss

```
L_total = ibn_weight * L_in_batch_neg + logistic_weight * L_global_bias + L_relevance
```

Default weights: `ibn_weight=1.0`, `logistic_weight=0.01`

---

## 8. Inference and Deployment

### 8.1 Single-Request Inference Mode

At serving time (`single_request_inference=True`), the model receives one user's features and must produce embeddings for **all** condition types. This is achieved by running multiple forward passes:

```python
def eval_forward(self, batch, deploy=True):
    # 1. Extract conditions: create one batch per condition variant
    unconditioned_batch, condition_batch_list = extract_conditions_for_inference(batch, device)

    # 2. Run forward pass for each condition (parallelized with jit.fork)
    for condition_batch in condition_batch_list:
        future = torch.jit.fork(self.forward, {**unconditioned_batch, **condition_batch})
        futures.append(future)

    # 3. Collect results
    for future in futures:
        emb = torch.jit.wait(future)
        results.append(emb)

    # 4. Stack: [B, num_conditions, D]
    result = torch.stack(results, dim=1)
    return float_to_int8(result)  # quantize for ANN index
```

Each condition type can have multiple "dummy" variants (e.g., multiple interest categories), so the total number of forward passes is `sum(1 + len(dummy_features) for each condition type)`.

### 8.2 Batched GPU Inference

When `enable_gpu_viewer_tower=True`, all conditions are merged into a single large batch:

```python
def extract_conditions_for_inference_batched(self, batch, device):
    unconditioned_batch, condition_batch_list = extract_conditions_for_inference(batch, device)
    conditioned_batch = merge_batches(condition_batch_list)
    unconditioned_repeated = merge_batches([unconditioned_batch] * len(condition_batch_list))
    return unconditioned_repeated, conditioned_batch
```

This produces a batch of size `B * num_conditions`, runs one forward pass, then reshapes:
```python
emb = rearrange(emb, '(c b) (h d) -> b c h d', b=batch_size, h=num_heads)
```

More efficient on GPU but requires more memory.

### 8.3 Deployment Optimizations

- **TorchScript**: Models are exported via `torch.jit.script` for C++ inference
- **Int8 quantization**: Final embeddings are quantized to int8 for compact ANN storage
- **CUDA graphs**: Static shape optimization for GPU inference
- **merge_batches()**: Custom JIT-scripted function that correctly handles variable-length features (with `row64` offset adjustment for sparse features)

### 8.4 How Retrieval Works at Serving Time

```
Offline:
  All pins -> Pin Tower -> pin_embeddings -> HNSW index (one shared index)

Online (per request):
  User + Conditions -> Viewer Tower -> [emb_interest, emb_board, emb_pin, ...]
                                              |            |          |
                                              v            v          v
                                         HNSW lookup  HNSW lookup  HNSW lookup
                                              |            |          |
                                              v            v          v
                                         candidates_1 candidates_2 candidates_3
                                              |
                                              +------> merge & rank downstream
```

Each condition embedding retrieves a different set of candidates from the **same** HNSW index, because the viewer embeddings have been trained to place the user in different regions of the embedding space depending on the condition.

---

## 9. Fine-Tuning

CLR supports fine-tuning the base model for specific surfaces (e.g., notifications):

### 9.1 Snapshot Loading

Patterns control which parameters are reset vs loaded:
```python
reset_parameter_pattern = [
    'viewer_tower_model.feature_mixer_layers',  # DHEN layers (different feature config)
    'viewer_tower_model.condition_tower',        # Condition tower (task-specific)
]

allowed_mismatched_pattern = [
    'norm_modules.51/',     # Different feature sets
    'global_bias',          # Different logistic loss weight
    'feature_mixer_layers.3',  # Different num_heads
    'head_adapter_layer',   # Task-specific head mapping
]
```

### 9.2 Critical Constraint

**Feature stats must match** between base and fine-tuned models. Both must use the same `feature_stats.json` date. Mismatched dates cause embedding table dimension mismatches because the feature vocabulary sizes differ.

### 9.3 Fine-Tuning-Specific Logic

When `is_finetuned_model=True`:
- Board and pin features are forcibly added to `all_features` even if not in the condition tags
- This ensures the DHEN layers see the same feature shape as the pretrained model

---

## 10. Key File Reference

| File | Purpose |
|------|---------|
| `conditional_learned_retrieval/model.py` | `ConditionalTwoTowerModel`, `ConditionalDHENTwoTowerModel` class definitions |
| `conditional_learned_retrieval/modules.py` | All condition-specific modules: `ConditionRouter`, `ConditionTokenGenerator`, `ConditionedUserSequenceTransformer`, `UserConditionTower`, `ConditionedViewerTower` |
| `conditional_learned_retrieval/__init__.py` | Public exports |
| `configs/features/feature_names.py` | Feature IDs, default values, `create_routing_masks()`, `is_default_value()` |
| `configs/base_conditional_lr_config_bundles.py` | Training hyperparameters and model configuration |
| `configs/config_bundle_defs.py` | Config dataclasses: `ConditionalRetrievalConfig`, `ConditionTagConfig`, `ConditionedUserSequenceTransformerConfig` |
| `two_tower/model.py` | Base `TwoTowerModel`, `ViewerTower`, `PinTower` |
| `two_tower/model_zoo/dhen_model.py` | `DHENTwoTowerModel`, `DHENViewerTower` (feature crossing) |
| `modules/metric_learning.py` | `InBatchNegativeLossMultihead` loss function |
| `two_tower/trainer_v2.py` | Training loop infrastructure |

All paths relative to `machine-learning/trainer/ppytorch/mlenv/` or `ml_resources/mlenv/two_tower/`.
