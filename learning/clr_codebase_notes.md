# CLR Codebase Learning Notes

## Quick Reference
- **CLR source code**: `machine-learning/trainer/ppytorch/mlenv/two_tower/conditional_learned_retrieval`
- **P2P LR source code**: `machine-learning/trainer/ppytorch/mlenv/closeup/p2p_learned_retrieval/`
- **Deep technical references**: `AIContext/projects/clr_technical.md`, `AIContext/projects/p2p_lr_technical.md`
- **Learning artifacts go to**: `learning/`

## What is CLR (Conditional Learned Retrieval)?

A **two-tower retrieval model** for Pinterest. It generates embeddings used for fast nearest-neighbor (HNSW) search in the pin index at serving time.

### The Two Towers
1. **Pin Tower** - encodes pins (images/content) into embeddings
2. **Viewer Tower** (user + condition) - encodes a user *conditioned on* a specific context into embeddings

### What is a "condition"?
A condition is the *context* for why we're retrieving pins for a user. Three types:
- **Interest** - user is browsing a topic (e.g., "modern kitchen design")
- **Board** - user is looking at a board
- **Pin** - user is looking at a related pin

The model learns different user embeddings depending on which condition is active. This is what makes it "conditional" - same user gets different embeddings based on context.

### Training Approach
- Trained with **contrastive in-batch negative loss** (similar to how CLIP works)
- Positive pairs: (user+condition, pin the user engaged with)
- Negative pairs: other pins in the same batch

---

## File Map

| File | Role |
|------|------|
| `__init__.py` | Exports `ConditionalTwoTowerModel` and `ConditionalDHENTwoTowerModel` |
| `model.py` | Model classes that override the base two-tower to add conditional logic |
| `modules.py` | The core neural network modules (transformer, condition routing, towers) |
| `agents.md` | Operational docs: how to train, fine-tune, debug |

---

## modules.py - Key Components Walkthrough

### 1. `merge_batches()` (lines 37-75)
- `@torch.jit.script` - compiled to TorchScript for faster execution and deployment
- **Purpose**: Combines multiple batch dicts into one big batch by concatenating tensors
- **Why it exists**: During inference, the model runs multiple conditions (interest, board, pin) separately. Instead of 3 forward passes, merge into one batch, run once, split results. More GPU-efficient.
- **Simple case** (dense features): just concatenates tensors along batch dim
- **Tricky case** (sparse features with `row64` in key name): variable-length data stored as flat values + offset arrays. Offsets must be shifted when merging.
- **Called from**: `extract_conditions_for_inference_batched()` (line 662)

### 2. `ConditionedUserSequenceTransformer` (lines 78-223)
- Takes a user's recent action sequence + condition tokens
- Processes through a standard Transformer encoder
- **Key design choice**: Condition tokens are **appended** to the sequence - they act as learned queries over user history
- **Residual connection**: Raw condition token added back to transformer output to prevent signal washout

### 3. `ConditionTokenGenerator` (lines 246-266)
- Takes raw condition features, concatenates them, produces fixed-dim token
- Two modes: MLP projection (with skip connection) or zero-padding
- Subclassed per condition type (Board/Interest/Pin) - currently identical, structural differentiation for future extension

### 4. `ConditionRouter` (lines 281-351)
- The traffic cop of conditions
- Uses `routing_masks` + `torch.where` to select correct token per example
- Optionally keeps raw concatenated features for DHEN residual connection

### 5. `UserConditionTower` (lines 381-530)
- Main orchestrator for user+condition side
- Sequence: routing masks -> dropout -> stats -> format/embed -> text projection -> condition routing -> sequence transformer

### 6. `ConditionedViewerTower` (lines 533-698)
- Splits batch into unconditioned (regular user features) and conditioned (condition + sequence)
- Runs condition tower, merges outputs, runs DHEN feature crossing
- Inference: creates separate batches per condition, runs all, stacks results

---

## Key Concepts to Remember

### Routing Masks
- Each example in a batch has exactly ONE active condition type
- Priority-based: interest -> board -> pin (first valid condition wins)
- `routing_masks` is a dict of boolean tensors used with `torch.where`

### DHEN Feature Crossing
- `all_cond_feature_combined` has weight **8** in the feature_mix_dict - condition features dominate
- This ensures the final embedding is heavily influenced by retrieval context

### In-Batch Negatives
- Training uses other pins in the same batch as negatives
- **Learnable temperature** parameter controls sharpness
- **Sample probability correction** adjusts for popular items being over-represented

### CLR vs P2P LR: The Fundamental Difference
- **CLR**: User features + explicit condition (interest/board/pin) -> multiple embeddings per condition -> separate ANN lookups
- **P2P LR**: User features + query pin features together in viewer tower -> single embedding per head -> the query pin IS the condition
- P2P has richer loss landscape (SID contrastive, C2C, Q2Q, distillation, hard negatives)
- P2P uses multi-tower parallel DHEN; CLR uses single DHEN with feature_mix_dict weights

---

## What I Understand Well
- The two-tower architecture and why independent encoding is necessary for ANN serving
- Condition routing: priority-based masks, torch.where selection, dummy features for inference
- The training loss (in-batch negatives with sample probability correction)
- Why condition tokens are appended (not prepended) - they act as learned queries
- The DHEN weight of 8 on condition features - the model is designed to be heavily conditional
- How fine-tuning works and the critical feature_stats constraint
- The P2P vs CLR architectural differences and why they exist

## What I'm Still Working Through
- [ ] How does the DHEN EnsembleInteractionLayers work internally?
- [ ] What does the base TwoTowerModel's ViewerTower look like (before conditional extension)?
- [ ] How does the RQ-VAE tokenizer work and what makes cascading fusion effective?
- [ ] The negative transfer detection via gradient cosine similarity - how to interpret and act on it
- [ ] How serving works end-to-end: user request -> viewer tower -> HNSW -> candidate merging -> ranking
- [ ] Cross-surface pretraining mechanics: how is training data from multiple surfaces mixed?

## How This Shows Up in My Work
- **UPP co-design with P2P**: Understanding both CLR and P2P LR architectures is essential for the unified base retriever design. The key tension: CLR uses explicit conditions, P2P uses query pin as implicit condition. The co-design must reconcile these.
- **Piyush's data scaling insight**: Different surfaces use different condition types. Scaling wrong conditions can degrade fine-tuning performance. This is visible in how CLR routing masks work.
- **Cross-surface pretraining**: The UPP thesis is that a shared base model improves all surfaces. Understanding how features and conditions differ between CLR and P2P LR reveals where this gets hard.
- **Wednesday AI demo / technical credibility**: Being able to speak precisely about these architectures in technical forums signals practitioner depth, not just management oversight.
