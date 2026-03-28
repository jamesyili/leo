# L1 Utility Project (Homefeed CG Team)

## 1) Why is this important?

### The core problem we’re solving
Homefeed has many candidate generators (CGs) that each retrieve and score their own pools. Historically this created:
- **Fragmented tuning across CGs**: business logic (e.g., diversity, freshness, shopping) often lived inside individual CGs or in inconsistent presort logic, making system-wide optimization difficult.
- **Limited post-merge control**: once candidates from multiple CGs are combined, we need a systematic way to enforce global objectives (quality, diversity, freshness, shopping mix) rather than optimizing CGs in isolation.
- **Redundant compute**: duplicates / near-duplicates (e.g., shared image signatures) can be scored multiple times if not deduped early enough.
- **Latency and timeout risk**: early-funnel surfaces run under strict time budgets, and timeouts can “mask” underlying latency by returning early.

### What L1 Utility establishes
We now have a dedicated **mid-funnel Pre-Ranking layer**—**LWS + L1 Utility**—whose job is **subset selection** (set composition), not final ordering.
- **Subset selection**: choose a candidate set that is diverse, safe, and aligned with business goals.
- **Downstream ranking owns ordering**: later stages (e.g., Pinnability/L2 and L3) decide final ordering and blending; Pre-Ranking ensures downstream rankers receive a better pool.

### Why this is strategically critical
A well-designed L1 Utility layer is one of the most important things we can do for Early/Mid-Funnel Ranking because it:
1. **Unifies global controls across CGs**, enabling consistent tuning and fair competition after merge.
2. **Improves full-funnel alignment** by explicitly optimizing set composition to match downstream needs.
3. **Enables personalized hyperparameters** (user/request-level controls) by centralizing knobs and applying them using model-predicted signals rather than hard-coded heuristics.

---

## 2) How do the goals connect to Pinterest-level goals?

### A) Cost savings
L1 Utility drives cost savings by:
- **Deduping earlier in the funnel** (before expensive scoring and downstream processing), preventing repeated work on the same (or near-duplicate) image signatures.
- **Reducing downstream candidate volume** through intentional subset selection, saving expensive compute (e.g., Pinnability) and reducing overall system work.
- **Avoiding full sorts** by using streaming/heap-based global selection patterns when possible.

### B) Moving towards “AI-first” decision-making
L1 Utility makes the system more AI-driven by:
- Treating **LWS multi-head predictions** as the canonical signals for business controls and quality filtering.
- Expressing objectives (freshness, shopping value, safety, diversity) as **explicit utility functions + constraints** rather than scattered per-CG heuristics.
- Creating a platform where we can **experiment rapidly** with global controls across CGs.

### C) Enabling deeper, more intentional interactions (vs time-spent)
Pinterest value is driven by intentional outcomes (repins/saves, closeups, meaningful clickthrough, shopping clickouts), and a “positive place” experience.
L1 Utility supports this by:
- Optimizing for a controllable set of interaction heads, including negative heads (hide/report) as guardrails.
- Enforcing **set-level composition** to ensure coverage of user interests, including tail/torso interests that support longer-term relevance and discovery.
- Supporting **shopping and fresh controls** as first-class, tunable knobs rather than crude multipliers or per-source hacks.

---

## 3) Technical foundations of the work and opportunities

## 3.1 Where L1 Utility sits in the funnel (mid-funnel)
- **L0 Retrieval**: many CGs retrieve candidates in parallel.
- **LWS (Lightweight Scoring)**: scores candidates (multi-head prediction) and outputs a base pinner-utility-like score.
- **L1 Presort** (per-CG pool shaping): cheap diversity/non-redundancy controls at high volume.
- **L1 Utility** (global selection): cross-CG, constraint-aware selection that produces the final candidate set for L2.
- **L2 Pinnability + L3**: downstream ranking and blending decide final ordering.

## 3.2 Current production status (as of 2026)
- **GPU serving for LWS is fully up-ramped in production**, unblocking model scale-up and richer context usage.
- **Coverage gap**: the only CGs not yet covered by LWS + L1 Utility are:
  - shopping-based CGs
  - some freshness-based CGs

## 3.3 Key system constraints and numbers (typical operating regime)
- LWS-covered traffic is a majority of impressions; LWS can score thousands of candidates per request and returns a reduced set.
- CGs can overfetch (e.g., ~x5 relative to their budget) to allow post-LWS filtering and diversity shaping.
- Time budgets exist at multiple points (e.g., L0, L0+L1, end-to-end). Timeouts can mask real latency; latency and timeout rate must be actively controlled.

## 3.4 Utility design primitives (configurable, head-based)
All probabilities are from LWS: `p(interaction | user, img_sig)`.

### Baseline: L1 pinner utility
- Define **pinner utility prime** as a weighted sum over heads:
  - `U_pinner' = Σ_i w_i * p_i` (can include negative weights for negative outcomes)
- Define **pinner utility** with non-negativity:
  - `U_pinner = max(U_pinner', 0)`

### Shopping utility (primary business knob)
- Define a shopping-specific utility using only shopping-relevant positive heads:
  - `U_shop = Σ_j wS_j * p_shop_j`
- Motivation: capture differentiated value (e.g., clickout/long-clickout) rather than applying a simplistic global multiplier.

### Freshness (“net-new”) utility (primary business knob)
- Net-new is effectively **freshness** in this context.
- Define a freshness-specific utility using positive heads appropriate for discovery and early intent:
  - `U_fresh = Σ_k wF_k * p_fresh_k`

### Safety / quality filtering using negative heads (aggressive)
- Use thresholds `t_hide`, `t_report`.
- If `p(hide) > t_hide` OR `p(report) > t_report`, apply aggressive removal/penalization to filter early.

### Total utility for selection
- `U_total = U_pinner + U_shop + U_fresh` (with diversity controls applied via constraints/penalties/caps)

## 3.5 Diversity control: evolving from attribution signals → content & user-coverage signals

### Why “throughId” is problematic as a global diversity signal
- throughId is retrieval attribution, not content similarity.
- throughId distributions differ across CGs; penalties based on throughId can break cross-CG score comparability after merge.

### Content-grounded diversity: SID (Semantic ID)
- SID is a discrete multi-token semantic code derived from multimodal embeddings (image+text).
- SID supports **multi-granularity** controls:
  - coarse prefixes (coverage control)
  - fine prefixes / full SID (strong near-dup / “too similar” control)

### User-personalized diversity: UIC (User Interest Cluster)
- UIC aims to control **personalized interest coverage**: which of the user’s interest regions a candidate belongs to.
- UIC assignment can be expensive (per-pin similarity computations), so it should be applied **later** than cheap signals.

### “Cheap signals early, expensive signals late”
- Presort (high-volume, large cutoffs): prefer stable, low-regret caps based on cheap content signals (e.g., SID); keep throughId only as a guardrail if needed.
- Utility (lower-volume, global stage): apply user-personalized constraints like UIC, where cost is more manageable and global selection benefits more.

## 3.6 Streaming constrained selection (latency-oriented)
Rather than fully sorting all merged candidates:
- Generate a globally “best-next” stream via **k-way merge** using a max-heap over per-CG lists.
- Apply selection constraints as accept/reject gates (global dedup → SID caps → UIC caps).
- This is both latency-friendly and naturally extensible to new business constraints.

### Example accept/reject logic (conceptual)
For each candidate in descending-ish score order:
1. If global dedup fails → skip
2. If fine SID cap fails → skip
3. If coarse SID cap fails → skip (or apply light penalty update)
4. Compute UIC bucket (on-demand)
5. If UIC cap fails → skip
6. Accept and update counters
Stop when we reach final L2 input size.

## 3.7 Opportunities (2026+)
### A) Bring remaining CGs into LWS + L1 Utility
- Integrate shopping-based CGs and remaining freshness-based CGs into the unified mid-funnel control plane.

### B) Scale LWS on GPU (now unblocked)
With GPU serving fully ramped:
- Increase model capacity and context length (e.g., long user sequences on the order of ~16k).
- Apply proven model scaling and inference techniques that have worked in other stages (e.g., Pinnability-style optimizations).

### C) Improve training data foundations
- Iceberg migrations for reproducible, versioned datasets and feature views.
- Ray adoption for scalable multi-source ingestion.
- Stronger offline evaluation alignment with online metrics (e.g., SSv2, retention proxies, safety guardrails) to reduce iteration risk.

### D) Business knobs as first-class controls
- Fresh control (“net-new” / freshness rate and quality composition)
- Shopping control (shopping proportionality and value-aware selection)
Both should be:
- globally applied post-merge
- tunable, ideally personalized per user/request
- latency-safe by design

---

## 4) Main innovations the team is excited about

### 4.1 L1 Utility as a durable platform for global controls
- A single layer to implement and iterate on global business logic across CGs (instead of duplicating logic within each CG).
- Enables cross-CG fairness, better monitoring, and easier funnel debugging.

### 4.2 Early merge + dedupe to cut cost and latency
- Deduping earlier in the funnel prevents repeated scoring and downstream processing of near-duplicates.
- This directly improves unit economics and tail latency.

### 4.3 From “single scalar penalty scores” → constraint-aware selection
- Diversity and business controls are naturally set-dependent (“no more than X from group Y”), which is better represented as constraints/caps than as stacked multiplicative penalties.
- Cap-based approaches are more stable, interpretable, and extensible.

### 4.4 SID + UIC diversity controls (content similarity + personalized coverage)
- SID controls “this looks too similar / repetitive” at multiple granularities.
- UIC controls user-personalized interest coverage and supports long-term relevance.
- Combined signals act as partially orthogonal facets for diversification.

### 4.5 GPU-enabled LWS scale-up
- With GPU serving fully ramped, we can increase model scale and context length cost-effectively.
- This unlocks a new regime for mid-funnel: richer user modeling, better multi-objective prediction heads, and tighter alignment to downstream ranking.

---

## 5) Timeline (past ~2 years)

### 2024: Foundations, experimentation, and key learnings
- Ran a series of early-funnel diversity and freshness experiments (coterie/embedding/heuristics).
- Observed: higher latency correlates with lower engagement; timeouts can mask real latency.
- Observed: removing diversity hurts engagement; excessive diversity can also hurt → tuning and better signals are required.
- Identified limitations of greedy, per-CG penalty re-ranking (can cause CG dominance and distribution shifts).
- Built initial technical direction: centralized controls in L1; move expensive steps to after L1 when it reduces total work.

### 2025: Major platform step-function
- Established the L1 Utility layer in the mid-funnel while saving latency.
- Significantly improved the LWS model.
- Enabled GPU serving for LWS, setting up cost-effective model scaling.
- Result: recent launches delivered improvements in engagement and retention as measured by SSv2 and retention metrics, with minimal trade-offs in latency and cost.

### Late 2025–2026: Diversity design maturation and wins
- Shipped / recommended diversity control using UIC + SID signals in L1 Utility, improving impression diversity and driving gains in SSv2 and retention, with minimal trade-offs in latency and cost.
- Converged on design direction:
  - Replace throughId-based global diversity in L1 Utility with SID/UIC-based controls for cross-CG comparability.
  - Use cap-based constraints and streaming selection for stability and extensibility.

### 2026: Next focus areas
- Expand L1 Utility business controls with two primary knobs:
  - Fresh control (net-new/freshness)
  - Shopping control (value-aware proportionality)
- Bring remaining shopping-based and some freshness-based CGs into LWS + L1 Utility coverage.
- Leverage GPU serving to scale LWS model capacity (e.g., longer user sequences ~16k) cost-effectively.
- Upgrade training-data foundations (Iceberg, Ray) and improve offline↔online alignment.
