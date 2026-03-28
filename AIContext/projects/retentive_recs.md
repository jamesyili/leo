# System Context: Retentive Recommendations & The Prediction Engine
**Current Status: January 2026 (updated March 2026 with James's framing of key innovations)**

## 1. Core Objective: Solving the "Serendipity" Problem
**Transitioning from Reactive Exploitation to Proactive Prediction.**

Historically, the industry has struggled with the "Explore / Exploit" dilemma. "Exploit" algorithms are efficient but lead to boredom and decay, while "Explore" algorithms often fail because they rely on random "undirected leaps" or generic popularity, which users perceive as irrelevant noise. The "Holy Grail" is **Serendipity**: showing the user something they didn't know they wanted, but which feels immediately relevant.

The **Retentive Recommendations** program solves this by operationalizing **User Interest Clusters (UIC)**. By moving from simple pattern matching to **Geometric Prediction** and **LLM-Based Reasoning**, we engineer serendipity—delivering exploration that is "sensible," personalized, and structurally aligned with the user's real life.

### **January 2026 Status Update: Validation**
As of January 2026, we have successfully validated the core thesis. By leveraging UICs as a superior form of user representation in our ranking stack, **we have achieved statistically significant lifts in both engagement and retention metrics.**

Moving retention via ranking experiments is historically rare and difficult, as retention is typically a lagging indicator driven by product market fit rather than algorithm tuning. Achieving this lift confirms that **UIC is the correct atomic unit for long-term pinner value**, validating our move to the next phase: **Prediction**.

---

## 2. The Data Foundation: User Interest Clusters (UIC)
The atomic unit of this system is the **User Interest Cluster (UIC)**. It replaces rigid taxonomy with dynamic "Use Case Clouds" located in a universal embedding space.

### 2.1. The OmniSage Representation
The power of the UIC is derived from its underlying embedding space, **OmniSage**, which uniquely fuses three distinct signal layers:
1.  **Visual & Semantic (CLIP):** Encodes the raw "meaning" of content (e.g., a hiking boot looks like a shoe).
2.  **Interaction Graph (Engagement):** Encodes user preference by clustering items that are co-engaged by the same user.
3.  **Social Graph (Pin-Board Topology):** Encodes "utility" by clustering items that are curated together on the same boards by the community.

**Result:** In OmniSage, "closeness" represents **functional utility**, not just visual similarity. A *hiking boot* and a *granola bar* are neighbors because the Graph connects them via "Hiking Trip" boards. This allows us to represent nuanced, unlabeled behaviors (e.g., "Minimalist Apartment Gardening") without needing explicit taxonomy labels.

### 2.2. UIC Signal Composition
A UIC is an **externalized feature** stored in the GSS Feature Store, enabling low-latency access across the stack.
* **Centroid/Medioid:** The coordinate center of the cluster in OmniSage space.
* **Action Counts:** Aggregated interactions (Repins, Closeups, Clicks, Search) associated with the cluster.
* **Cluster Variance:** Statistical measures (Min, Max, P50, Std Dev) of cosine similarity within the cluster, indicating "tightness" or "focus".
* **Temporal Distribution:** Time buckets to track interaction velocity (e.g., is this cluster accelerating or decaying?).

### 2.3. Stateful Lifecycle Management
Unlike static profiles, UICs carry state metadata that dictates system behavior:
* **Enticement:** High exploration, low efficiency threshold. Focus on gauging receptivity.
* **Activation:** Refinement of scope. Success metric = Board Creation ("Sealing the deal").
* **Stabilization:** Exploitative reinforcement. Success metric = Efficiency/Repins.
* **Re-evaluation:** Managed decline. Success metric = Proactive pivoting to new use cases via extinction or re-introduction.

---

## 3. Geometric Prediction Strategies
Leveraging the continuous nature of the OmniSage embedding space, we employ **Geometric Prediction** to navigate users to their next interest.

### Strategy A: Vector Transport (Trajectory Prediction)
We treat user evolution as a physics problem involving drift through the embedding space.
* **Concept:** Users do not jump randomly; they flow through adjacent concepts (e.g., *Apartment* $\rightarrow$ *Balcony* $\rightarrow$ *Gardening*).
* **Mechanism:** By analyzing the historical paths of the "Golden Cohort" (retained users), we calculate **velocity vectors** for any given coordinate.
* **Application:** If a user is at Coordinate $A$, we apply the population-level velocity vector $\vec{v}$ to predict their arrival at Coordinate $B$, seeding content from $B$ before they explicitly search for it.

### Strategy B: Graph Completeness (Topological Prediction)
We leverage the "Pin-Board Graph" structure to identify missing functional components of a Use Case.
* **Concept:** A complete Use Case (e.g., "Camping") has a specific graph topology connecting *Gear*, *Locations*, and *Food*.
* **Mechanism:** The system scans the user's current UIC. If the user has dense nodes for *Gear* and *Locations* but a "structural void" where *Food* normally exists in the OmniSage graph, the system predicts *Food* as the next high-utility node.
* **Application:** Recommending items that "complete the set" based on graph topology rather than generic popularity.

### Strategy C: Sensible Sourcing (Cluster Collision)
We solve the "Cold Start" and "Undirected Leap" exploration problems by calculating the geometric intersection of existing clusters.
* **Concept:** "Serendipity" is finding the logical bridge between known interests.
* **Mechanism:** If User has $UIC_1$ (Vegan Cooking) and $UIC_2$ (Budget Travel), we query the embedding space for the **Centroid** between $UIC_1$ and $UIC_2$.
* **Application:** The system recommends "Vegan Camping Food"—a niche located mathematically between the two existing clusters, ensuring exploration feels personalized and safe.

### Strategy D: Synthetic Profiling
* **Concept:** Low-signal users are volatile due to sparse data.
* **Mechanism:** We match a low-signal user's fragment (e.g., 2 clicks) to a mature "Synthetic Cluster" aggregated from thousands of similar users.
* **Application:** We "spoof" a robust profile to immediately provide depth and diversity, bypassing the "training wheels" phase.

---

## 4. The Reasoning Engine (LLM/VLM Integration)
The UIC acts as the bridge between raw behavioral data and high-level reasoning capabilities.

* **The Problem:** Traditional recommenders match patterns ("bought hammer" $\rightarrow$ "buy nails"). They do not understand *intent*.
* **The Solution:** We treat the UIC as a **Dynamic Prompt** for LLMs and VLMs.
* **Workflow:**
    1.  **Input:** The VLM ingests the visual/semantic tokens of the pins within a UIC (e.g., images of wood, blueprints, saws).
    2.  **Reasoning:** The Model deduces the real-world objective: *"The user is building a deck."*
    3.  **Generation:** The Model generates a "Next Best Action" plan: *"After building, they will need staining and furniture."*
    4.  **Output:** The system queries OmniSage for "Wood Staining" and "Outdoor Furniture" clusters, effectively recommending a **future timeline** rather than just a similar product.

---

## 5. Operational Architecture
The UIC signal is integrated into the entire Homefeed stack via the **User Feature Representation (UFR) Node**.

### 5.1. Candidate Generation (CG)
* **Conditioning:** UICs serve as the "condition" input for Conditional Learned Retrieval models.
* **Retrieval:** We fetch candidates that are chemically close to the UIC medioid, or "predicted" coordinates based on Geometric Strategy.

### 5.2. Utility & Ranking (L1/L2)
* **Weight Tuning:** We create specific utility weights based on the UIC's lifecycle state.
    * *Enticement State:* Higher weight on **Closeups/Clicks** (signaling curiosity).
    * *Stabilization State:* Higher weight on **Repins/Saves** (signaling utility).
    * *Re-evaluation State:* Down-weighting of engagement signals to allow for decay and replacement.

### 5.3. Diversity (SSD)
* **Logic:** We enforce diversity *between* UICs (broadening) and *within* UICs (deepening).
* **Mechanism:** The diversity scorer ensures the feed isn't dominated by a single "Stabilized" cluster, explicitly reserving slots for "Enticement" clusters derived from Geometric Prediction.

---

## 6. Strategic Imperatives
This architecture serves as the "Operating System" for Pinterest’s key strategic bets:

1.  **Retention (MAU $\rightarrow$ WAU):** By predicting UIC decay and proactively seeding the next use case, we create a continuous chain of value, preventing the "empty feed" experience that leads to churn.
2.  **AI Forward (Agents):** AI Agents require context to be useful. The UIC provides a portable, pre-computed "Theory of Mind" for the user, allowing agents to understand *who* they are helping instantly (e.g., "I know you are a vegan budget traveler").
3.  **Explore (Use Case Expansion):** Moving Explore from "Random Popularity" to "Sensible Sourcing" allows us to safely expand users into new verticals, driving the multi-use-case depth that correlates with long-term retention.

---

## 7. Strategic Alignment: Powering the "Anticipation" Vision
Retentive Recommendations is not a siloed ranking project; it is the **technical engine** that makes the company-wide **"Anticipation"** vision  possible.

### 7.1 The "Brain" of Anticipation
The "Anticipation" strategy centers on moving users from *reactive matching* to *predictive journeys*.
* **The "What":** The company vision calls for "Journey Jumps" (predicting the s'mores bar after the firepit).
* **The "How":** Retentive Recommendations provides the **Geometric Prediction** capabilities (Vector Transport, Graph Completeness) required to execute these jumps reliably. Without the UIC's ability to model trajectory in embedding space, "Anticipation" remains an abstract concept without a delivery mechanism.

### 7.2 Enabling "Downstream Rewards"
A key pillar of Anticipation is shifting incentives from short-term clicks to long-term value.
* **The Mechanism:** Our work on **UIC Lifecycle Management** (detecting decay in "Stabilized" clusters and injecting "Enticement" clusters) is the operational implementation of Downstream Rewards. We are building the system that explicitly trades short-term efficiency for long-term retention health.

### 7.3 The Portable Signal for "Cross-Surface Action"
Anticipation requires a coherent experience across Homefeed, Search, and Notifications.
* **The Enabler:** The UIC is designed as an externalized feature in the GSS Feature Store, making it a portable "User State" that can be accessed by the **Unified P13N Platform (UPP)**.
* **The Impact:** When Homefeed predicts a "Camping" journey via UIC, that same signal is instantly available to Notifications (for "Camping Gear" alerts) and Search (for personalized query suggestions), ensuring the "Anticipation" effect is felt ubiquitously.

# Technical Specification: Retentive Recommendations & The Prediction Engine
**Version:** 2.0 (January 2026)
**Domain:** Homefeed Discovery / Personalization
**Status:** Validated / Scaling Phase

---

## 1. Executive Summary: The Engineering of Serendipity
Traditional recommendation systems face the **"Explore/Exploit" dilemma**: "Exploit" algorithms drive short-term efficiency but cause long-term churn through boredom; "Explore" algorithms often fail due to relevance noise. 

**Retentive Recommendations** solves this by shifting the paradigm from **Reactive Matching** (logging history → finding lookalikes) to **Geometric Prediction** (mapping trajectory → anticipating future state).

The core thesis—now validated by statistically significant retention lifts—is that **User Interest Clusters (UIC)** represent the correct atomic unit for modeling long-term user value. By leveraging UICs within an **OmniSage** embedding space, we can engineer "serendipity": exploration that is mathematically adjacent to confirmed utility rather than randomly sourced.

---

## 2. Core Abstraction: User Interest Clusters (UIC)
The UIC replaces rigid taxonomy with dynamic "Use Case Clouds" rooted in a high-dimensional vector space.

### 2.1 The OmniSage Embedding Space
UICs do not exist in isolation; they are coordinates within **OmniSage**, a fused latent space that encodes three distinct signal layers[cite: 1644, 2266]:
1.  **Visual/Semantic Layer (CLIP):** Encodes raw pixel/text meaning (e.g., *Hiking Boot* $\approx$ *Running Shoe*).
2.  **Interaction Graph:** Encodes user preference via co-engagement (e.g., Users who click *Hiking Boot* also click *Granola Bar*).
3.  **Topology Graph (Pin-Board):** Encodes functional utility via curation (e.g., *Hiking Boot* and *Tent* coexist on "Camping" boards).

**Technical Definition:** A UIC is a tuple defined as $C_i = \{ \vec{\mu}_i, \Sigma_i, T_i, A_i \}$, where:
* $\vec{\mu}_i$: The **Medioid vector** representing the cluster center in OmniSage space.
* $\Sigma_i$: **Cluster Variance** (Min, Max, P50, Std Dev of internal cosine similarity), representing "focus."
* $T_i$: **Temporal Distribution**, modeling the velocity/decay of the interest.
* $A_i$: **Action Vectors**, aggregated interaction counts (Repins, Closeups, Clicks, Search)[cite: 1645].

### 2.2 Signal Construction (L500 Sequence)
The UIC signal is constructed in real-time from the user's **L500 sequence** (last 500 actions).
* **Clustering Algorithm:** Complete-link hierarchical clustering is performed on the sequence.
* **Merge Criteria:** Events merge only if similarity exceeds a threshold $\theta$ relative to *all* events in the target cluster, ensuring high coherence[cite: 2583].
* **Externalization:** Computed UICs are stored in the **GSS Feature Store**, enabling low-latency access across CG, Ranking, and Diversity stages without re-computation[cite: 2938].

#### Clustering Parameters (v2)
The clustering logic is governed by the following configuration. The *underlined* parameters are primary candidates for experimentation.

```json
clusterParamString = {
    "viewName": "ssuliman_testing",
    "version": "CLUSTERED_OMNISAGE_V1_EMBEDDING",
    "eventCountThreshold": 1000,
    "clusterLimit": 25,                 // Max clusters per user
    "dimension": 32,                    // Embedding dimension
    "similarityThreshold": 0.5,         // Threshold for merging events into cluster
    "maxLandmarks": 30,                 // Max landmark images per cluster
    "actionTypesForClustering": ["PIN_REPIN", "PIN_CLOSEUP"],
    "customizedActionWeights": {
        "PIN_REPIN": 2.0,               // Repins weighted 2x vs Closeups
        "PIN_CLOSEUP": 1.0
    },
    "sampleMethod": "NONE",
    "queryRewardFunc": "REPIN_CLICK",
    "actionTypesForBackfilling": [],
    "useMedoidAggregator": True,
    "actionTypeCount": Map<ActionType, Integer>,
    "skipLshTermGeneration": True,
    "appendStats": True,
    "computeClusterWeight": True
}
---

## 3. The Prediction Engine: Geometric Strategy
*Status: Heuristic MVP Phase*

We reject generic "diversity" heuristics (e.g., random noise). True prediction requires modeling **Momentum** and **Composition**. We employ two deterministic geometric strategies to generate "Predicted UICs" that serve as seed queries for the Candidate Generator (CLR).

### 3.1 Strategy A: Time-Vector Extrapolation (Momentum)
We treat user interest not as a static point, but as a vector with velocity. We assume the user's interest is drifting *away* from the center of the cluster towards their most recent interactions.

* **Logic:** $Trajectory = \text{Recent} - \text{History}$
* **Calculation:**
    1.  Identify the **Cluster Medoid** ($\vec{\mu}_{UIC}$): The geometric center of the cluster (The "Average").
    2.  Identify the **Temporal Edge** ($\vec{p}_{latest}$): The embedding of the most recent interaction *assigned* to this cluster.
    3.  Compute the **Drift Vector**: $\vec{v} = \vec{p}_{latest} - \vec{\mu}_{UIC}$.
    4.  **Prediction:** $\vec{target} = \vec{p}_{latest} + \lambda \vec{v}$ (where $\lambda$ is a scalar, typ. 0.5 - 1.0).
* **Outcome:** If a user moves from *Basic Baking* $\rightarrow$ *Sourdough*, the vector points toward *Fermentation*. We retrieve from *Fermentation* before the user searches for it.

### 3.2 Strategy B: Geometric Mixups (Sensible Sourcing)
We solve the "Cold Start" exploration problem by calculating the geometric intersection of existing clusters. This mimics "compositional reasoning" in the embedding space.

* **Logic:** Serendipity is often the bridge between two known interests.
* **Calculation:**
    1.  Select Top 2 strongest UICs: $UIC_A$ and $UIC_B$.
    2.  **Topology Check:** Verify $UIC_A$ and $UIC_B$ have non-zero co-occurrence in the global Pin-Board graph (prevents "Frankenstein" merges like *Motorcycles* + *Cupcakes*).
    3.  **Prediction:** $\vec{target} = \text{Slerp}(\vec{\mu}_A, \vec{\mu}_B, 0.5)$.
* **Outcome:** User has `Mid-Century Modern` and `Cats`. The midpoint vector retrieves `Mid-Century Cat Furniture`.

### 3.3 Strategy C: Graph Completeness (Topological Prediction)
We leverage the "Pin-Board Graph" to identify **structural voids** in a use case.
* **Mechanism:** A complete use case (e.g., "Camping") has a known topological structure connecting nodes like *Gear*, *Location*, and *Food*.
* **Execution:** The system scans the user’s UIC. If nodes for *Gear* and *Location* are dense but *Food* is sparse/absent, the system identifies the "missing centroid" required to complete the graph topology and boosts those candidates.

### 3.4 Strategy D: Cluster Collision (Sensible Sourcing)
We solve the "Cold Start" exploration problem by calculating geometric intersections.
* **Mechanism:** If User has $UIC_A$ (Vegan Cooking) and $UIC_B$ (Budget Travel), we query OmniSage for the **Geometric Median** between $\vec{\mu}_A$ and $\vec{\mu}_B$.
* **Execution:** The system retrieves "Vegan Camping Food"—a niche located mathematically between existing clusters, ensuring exploration is "safe" and personalized.

### 3.5 Strategy E: Synthetic Profiling
We mitigate volatility in low-signal users (LSU) via "Synthetic Clusters."
* **Mechanism:** LSUs lack sufficient data for stable clustering. We match LSU fragments (e.g., 2 clicks) to mature "Synthetic Clusters" aggregated from thousands of high-signal users with similar initial trajectories.
* **Execution:** We "spoof" a robust profile for the LSU, immediately enabling depth and diversity recommendations.

---

## 4. The Reasoning Layer: LLM Integration
We treat the UIC as a **Dynamic Prompt** for Large Language/Vision Models.
* **Input:** VLM ingests visual tokens from pins within a UIC (e.g., *wood, blueprints, saw*).
* **Inference:** The model deduces intent ("Building a deck") and generates a "Next Best Action" plan ("Needs staining").
* **Output:** The system queries OmniSage for the "Wood Staining" cluster, essentially recommending a **future timeline**.

---

## 5. Operational Architecture
The architecture is federated across the entire Homefeed stack via the **User Feature Representation (UFR) Node**.

### 5.1 Candidate Generation (CG)
* **Conditional Learned Retrieval (CLR):** We deprecate the "Followed Interests" logic. Instead, the CLR two-tower model accepts the **UIC Medioid** $\vec{\mu}_i$ directly as a "condition" input.
* **Efficiency:** This reduces "overfetch" ratios (fetching candidates irrelevant to the current user state), generating significant infra cost savings (approx. 322k/year projected).

### 5.2 Ranking (Pinnability) & Utility
* **Composite Labeling:** Instead of adding new heads (which increases latency), we use **Curriculum Learning** via composite labels.
    * *Standard Label:* `repin`
    * *Composite Label:* `repin` + `new_use_case` (where `new_use_case` is defined by distance > threshold $\delta$ from existing UICs).
    * **Weighting:** Composite positives are weighted $2\alpha$ vs standard $\alpha$, forcing the model to learn "exploration" as a high-value trait.
* **State-Dependent Utility:**
    * *Enticement Phase:* Utility function boosts **Closeups/Clicks** (curiosity signals).
    * *Stabilization Phase:* Utility function boosts **Repins/Saves** (commitment signals).

### 5.3 Diversity & Blending
* **Inter-Cluster vs. Intra-Cluster:** The diversity scorer explicitly allocates slots to distinct UICs to prevent feed collapse.
* **Mechanism:** We reserve slots specifically for "Enticement" clusters (derived from Prediction Strategies) to ensure the feed is never 100% "Stabilization" content.

---

## 6. Feedback & Reinforcement: The Geometric Bandit (New)
*Status: Design Phase*

To prevent "Zombie Clusters" (interests that persist despite disengagement) and "Infinite Exploration" (randomly showing new topics forever), we implement a **Thompson Sampling Bandit**.

**CRITICAL ARCHITECTURE DECISION:** We explicitly **DEPRECATE Semantic IDs (SIDs)** for reward tracking. SIDs cause "Signal Bleed" (aliasing distinct user interests into generic categories). We instead use **Geometric Hashing**.

### 6.1 The Geometric Key (LSH)
We track rewards based on the specific region of the embedding space the user is interacting with.

* **Key Generation:** `LSH_Key = SimHash(UIC.medioid, bits=16)`
    * *SimHash* preserves cosine similarity. Similar vectors hash to the same key; dissimilar vectors hash differently.
* **Storage:** `Map<User_ID + LSH_Key, Beta_Distribution_Params>`
* **Advantage:** "Glamping" and "Survivalist Camping" are geometrically distant. They generate different LSH keys, ensuring the user's dislike of one does not penalize the other.

### 6.2 The Reward Function: Log-Lift
We optimize for **Momentum**, not absolute Click-Through Rate (CTR). High-volume, stale interests should not crowd out low-volume, growing interests.

* **Formula:** $R_t = \log(\frac{CTR_{current} + \epsilon}{CTR_{baseline} + \epsilon})$
    * $CTR_{current}$: Engagement in the current session/window.
    * $CTR_{baseline}$: The user's historical average for this LSH key (or global average if new).
* **Negative Feedback:** "Fast Scroll" or "Hide" actions are treated as explicit penalties (reducing the $\alpha$ parameter in the Beta distribution), forcing the confidence interval to collapse immediately.

### 6.3 Sampling Logic (Thompson)
At serving time, we do not rank clusters by their raw score. We sample from their Beta distributions.
* **Stabilized Clusters:** Have narrow distributions (High confidence).
* **Predicted/New Clusters:** Have wide distributions (Low confidence).
* **Result:** The bandit naturally "explores" the wide distributions occasionally. If the user engages (Log-Lift), the mean shifts right. If they ignore, the mean shifts left and variance decreases (stopping exploration).

---

## 7. Strategic Alignment: "Anticipation"
This architecture is the technical engine for the company-wide **Anticipation** vision.

* **Journey Jumps:** By implementing **Vector Transport**, we move from "reactive matching" to "predictive jumps" (e.g., Firepit $\rightarrow$ S'mores).
* **Downstream Rewards:** By managing **Lifecycle States**, we explicitly trade short-term CTR for long-term retention (WAU), optimizing for the "Golden Cohort" trajectory rather than the "Clickbait" trajectory.
* **Cross-Surface Portability:** Because UICs are externalized in GSS, the "Predicted Next Interest" is available instantly to **Search** (query suggestions) and **Notifications** (alerting), creating a unified "Theory of Mind" for the user across the platform.

---

## 8. James's Framing: The Three Key Innovations (March 2026)

This section captures how James frames the core innovations of Retentive Recommendations — useful for interview prep, stakeholder comms, and learning agenda alignment.

### Innovation 1: Personalized Interest Representation
We moved beyond a global interest definition into a personalized one. We don't cluster over all possible pins, but rather cluster over only the pins the user has engaged with. This makes a much easier problem and a much more accurate representation. Improvements:
- Longer history (L500 sequence instead of shorter windows)
- Dynamic cluster count (not fixed categories — users with diverse interests have more clusters)
- Complete-link hierarchical clustering ensures high coherence within each UIC

### Innovation 2: Embedding-Space Prediction at the Interest Level
We are predicting a point in space in the embedding space where the user is likely to engage, using what they have historically already engaged with. This is fundamentally different from pin-level prediction. This is "use case" or "interest level" prediction personalized to the user. The Geometric Prediction strategies (Vector Transport, Sensible Sourcing, Graph Completeness) all operate at this level — predicting where in the embedding space the user is heading, not which specific pin they'll click.

### Innovation 3: The RL Feedback Loop
How we build an actual feedback loop to do reinforcement learning for explore-exploit, to make sure we thoroughly and effectively explore the different regions of the embedding space for each user. The Geometric Bandit (Thompson Sampling over LSH keys with Log-Lift reward) is the mechanism. This is novel because:
- Exploration is systematic and trackable (per-region Beta distributions)
- Reward measures momentum (Log-Lift) not absolute engagement
- Negative feedback collapses exploration immediately (no zombie clusters)
- The bandit handles the explore/exploit tradeoff automatically through posterior width