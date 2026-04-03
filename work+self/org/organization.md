# organization.md
Last Updated: 2026-04-01  
---  
  
# Org & Technical Context (Homefeed Candidate Generation)  
  
## Purpose  
This file is the canonical “what my world is” reference: org structure, scope boundaries, key systems, active workstreams, and the verified outcomes + roadmap themes that matter for reasoning and writing quickly (especially the 2025 Year-in-Review + 2026 priorities).  
  
Tier1 rule: **no raw docs here**. Point to them.  
  
---  
  
## Org / Team Overview  
- **Company:** Pinterest  
- **Org:** Discovery → Homefeed Relevance  
- **Sub-org:** Homefeed Candidate Generation (CG)  
- **CG scope (business framing):** CG determines what enters the Homefeed funnel; impacts **engagement (SSv2)** and **retention (WAU/MAU)**, plus **infra cost/latency**.  
- **CG scope (technical framing):** early-funnel candidate generation + retrieval + preranking + funnel efficiency + personalization foundations.  
  
---  

## Leadership Chain
```
Bill Ready (CEO)
└── Matt Madrigal (CTO)
    └── Jeff Harrell (VP, Engineering - Core)
        ├── Rajat Chaturvedi (VP, Engineering)
        │   ├── Dylan Wang (Sr. Director, ML — Homefeed Relevance) — 132 reports
        │   │   ├── James Li (Sr. Manager, ML — HF Candidate Generation) — 17 reports
        │   │   ├── Dhruvil Deven Badani (Sr. Manager, ML — HF Ranking) — 35 reports
        │   │   │   ├── Rahul Goldam (Manager II, ML)
        │   │   │   └── Dafeng He (Sr. Staff MLE)
        │   │   ├── Yan Li (Sr. Manager, Eng — P13N-Experiences) — 27 reports
        │   │   ├── Tim Leung (Manager II, Eng — Frontend) — 13 reports
        │   │   ├── Francisco Navarrete (Sr. Manager, Eng — Platform/Labeling) — 16 reports
        │   │   └── Olafur Gudmundsson (Sr. Staff MLE — IC)
        │   ├── Kurchi Subhra Hazra (Sr. Director, ML — Search/SSJ) — 114 reports
        │   │   └── Vasil Kasmitski (Manager II, Eng)
        │   ├── Kaanon MacFarlane (Director, Eng) — 34 reports
        │   │   └── (Frontend/backend, no ML. Working with Karina on AI initiative for Rajat)
        │   └── Karina Sobhani (Director, Eng) — 15 reports
        │       └── (Frontend/backend, no ML. Team has shrunk. Working on AI initiative with Kaanon)
        ├── Faisal Farooq (VP, Engineering — Trust & Safety, Signals) — 200 reports
        ├── Shipeng Yu (Sr. Director, ML — Growth) — 122 reports
        ├── Manu Sharma (Sr. Director, Data Science) — 27 reports
        └── Phil Price (Distinguished Engineer)

Other CTO direct reports (outside Jeff's chain):
├── Matthias Zenger (VP, Engineering)
├── Vik Gupta (VP, G&I Monetization)
├── Vicky Gkiza (VP, Product Management)
├── Carmen Maierean (VP, EPD Strat & Ops)
├── Chuck Rosenberg (VP, Engineering)
├── Ken Cushman (CIO)
├── Dana Cho (VP, Design)
├── Andy Steingruebl (CSO)
├── Brittan Bushman (Sr. Director, Corporate Strategy)
└── Kartik Paramasivam (Chief Architect)
```

## Key people / stakeholders (canonical)  
- **James Li:** Sr ML Eng Manager for HF CG    
  - Known for: clarity, decisiveness, technical rigor, operational excellence    
  - Growth edges: communication flexibility, calm under pressure, pre-alignment before escalation  
- **Dylan Wang:** Sr. Director of Homefeed Relevance (132 reports)
  - Style: values accuracy and exec-ready comms; peak trust with James
  - Direct reports: James, Dhruvil, Yan, Tim, Francisco, Olafur
- **Rajat C:** VP of Engineering under Jeff
  - Joined from leading Alexa at Amazon
  - Direct reports: Dylan, Kurchi, Kaanon, Karina
- **Jeff Harrell:** VP of Engineering - Core (Rajat's manager)
  - High-I/D profile. Loves demos, “cool work,” and engineering culture modernization.
- **Dhruvil:** Sr EM for Homefeed Ranking (peer under Dylan, 35 reports)
- **Yan Li:** Sr EM for P13N-Experiences (peer under Dylan, 27 reports). New to org post-reorg. Frontend + 6-person ML team. Owns Explore/IB surfaces.
- **Tim Leung:** Manager II under Dylan (13 reports). Frontend team. James mentors him. TL Yu Zhao is one of the best engineers in the org.
- **Francisco Navarrete:** Sr Manager under Dylan (16 reports). Team primarily in Mexico. Labeling + foundational platform work. Stretched by horizontal platform work for all of Core. Good relationship with James.
- **Olafur Gudmundsson:** Sr. Staff MLE under Dylan. IC. Involved in ownership boundary discussions.
- **Kartik Paramasivam:** Chief Architect, reports to CTO. Fan of James's work. Has connected with Dylan about James. Dylan has hinted Kartik's support is important for James's future.
- **Faisal Farooq:** VP Eng under Jeff. Owns T&S + Signals (content understanding, user understanding). Very technical, KDD chair. Open supporter of UPP.
- **Shipeng Yu:** Sr. Director ML (Growth) under Jeff (122 reports). Close to Dylan. Org was pushed into UPP by Jeff — now supportive. Brian Lee and Tingting (Notifications) report to him.
- **Piyush:** IC16 MLE, technical lead for UPP Retrieval. Most performant IC on team. Holds core retrieval architecture context.
- **Cross-org partners (non-exhaustive):** ATG, ML Infra/Core Infra, Notifications ML, Growth/Activation, UU (User Understanding), Blending, Search/Related Pins surfaces

### Notable: Raymond Su
Reports to Tim Leung. Was the previous HF CG manager before James joined above him. Transitioned back to IC unwillingly. Holds resentment toward James. Not an active risk but worth tracking.  
  
### Name normalization (must preserve in outputs)  
- Hong Tao → **Hongtao**  
- Jay Wong / Jay → **Jaewon**  
- RecGBT → **RecGPT** (also known as **PinRec**)  
  
---  
  
## Team structure (2026 — March update)
Following Bowen's departure (March 30, 2026), James is interim manager of all 17 direct reports. Structure is flat pending EM backfill. Team organized by workstream:

### UPP Retrieval
- **TL:** Piyush (IC16)
- **Members:** Zihao, Sophia, Devin (indirect via CLR), Ryan (from April)
- **PM partner:** Matt C

### RecGPT
- **TL:** Bella
- **Members:** Hanlin

### Retentive Recs
- **TL:** Yuke
- **Members:** Chuxi, Yidi
- **PM partner:** Anna K

### CLR (Conditional Learned Retrieval)
- **TL:** Devin
- **Members:** Ryan (from April)

### LWS (Lightweight Scoring)
- **De facto owner:** Yali
- **Members:** Hedi, Zili

### Real-Time / L1 Utility
- **TL:** JJ

### AI (Pinvestigator/Pinsight)
- **Owner:** JJ (partial), Charlie

### Content Exploration
- **Contributors:** Zihao (~50%), Yidi (fractional)

### PhP / Dynamic Triggering
- **Owner:** Alok (conditional)

### Departing
- **David:** April

**EM backfill:** Targeting experienced hire. James running pipeline; Dylan in for finals. Alternative frameworks (pod model, two-track org) documented in `q2_roadmap.md`.  
  
---  
  
## Scope boundaries (explicit)  
  
### In scope  
- **Retrieval / Candidate Generation:** selecting candidate items given user/context and conditioning signals.  
- **Personalization foundations in retrieval:** embeddings, feature retrieval, user interest signals, exploration/exploitation knobs (as they shape candidate sets).  
- **Conditioning / query composition:** building candidate requests/constraints.  
- **Preranking / fast shaping:** lightweight scoring (LWS), early controls, filtering, dedupe, diversification constraints.  
- **Indexing + supply:** candidate coverage/diversity via indexing strategies and retrieval sources.  
- **Serving efficiency:** latency, cost, caching, reliability improvements tied to retrieval/preranking.  
  
### Out of scope (but coordinate tightly)  
- Final ranking model ownership and training pipelines (Ranking org).  
- Full Homefeed blending/business rules (Blending org), unless explicitly delegated.  
- Core infra platform components without clear retrieval ownership (we influence; partner owns).  
- Product UX decisions (we shape via constraints, proof plans, and measured outcomes).  
  
### Shared-ownership zones (where confusion happens)  
- **CG vs Ranking boundary:** CG owns *candidate recall/coverage + fast shaping*; Ranking owns *heavier scoring and ordering*.  
- **Infra vs Modeling:** if it materially changes retrieval behavior, CG leads with Infra partnership and explicit contracts.  
  
---  
  
## Canonical 2025 topline outcomes (numbers that should appear early)  
Use these as canonical headline metrics (repeatable, exec-legible):  
  
- **Product impact:** **+2.1% total SSv2**, **+0.33% WAU** (≈ **+1.1M WAU**)  
- **Company impact:** **~$3M/year annual cost savings** in 2025  
- **NUX / Growth:** critical unblock for NUX Revamp backend; achieved ambitious **1% NUX Growth** goal while enabling the experience  
- **Notifications:** enabled/accelerated Notifications ML with **~6–7 MAU-improving launches** (via platformization + retrieval work)  
  
---  
  
## 2025 narrative arc (high-level story)  
2025 was a **modernize → consolidate → scale** year:  
- **Modernized** CG stack toward learned retrieval + unified components (CLR, multi-embedding, L1 utilities, GPU serving)  
- **Consolidated** away legacy/heuristics with active deprecations (**topics**, **bestpins**, **pinacle2**)  
- **Scaled** impact across Pinterest surfaces (Homefeed first; enabled Notifications and broader **Unified Personalization Platform (UPP)** direction)  
- **Shifted** Retentive Recommendations from product vision → concrete signals + shipping roadmap  
  
---  
  
## 2025 highlights (canonical bullets to reuse)  
  
### A) Team growth & org maturity  
- **New hires + onboarding (2025):** Hanlin Lu, Zili Li, Chuxi Wang, Sophia Zhu, Yidi Wang, Charlie Tian (he/him), Yali Bian *(and other 2025 hires as applicable; keep list current)*  
- **July reorg:** DRP + RCG structure established; Bowen stepped in as EM; TLs stepped up materially across design/execution/ownership  
  
### B) Company contributions (impact summary)  
- Delivered **+2.1% SSv2** and **+0.33% WAU (~+1.1M)** (topline result)  
- Delivered **~$3M/year** annual cost savings (infra + serving + deprecations + migrations)  
- Enabled Growth via **NUX Revamp backend**; hit **1% NUX Growth** goal while unblocking the experience  
- Enabled Notifications ML velocity and MAU impact via platformization + retrieval experimentation (**6–7 launches**)  
  
### C) Technological impact (2025 pillars)  
  
#### Modernized CGs (Engagement / SSv2)  
- **CLR (Conditional Learned Retrieval)** as backbone; upgraded legacy interest/board/pin CGs → better relevance, coverage, flexibility  
- **Multi-Embedding Learned Retrieval (ME LR)** → richer user representation; better diverse/tail interests  
- **Deprecation of legacy services:** **topics**, **bestpins**, **pinacle2** → reduces complexity and frees operational cycles  
  
#### ML advancements (Engagement / Retention)  
- **LLM-based interest generation (PinnerSpark)**  
- **Retentive Recommendations:** grounded in measurable signals + launches; shifted from “vision” to “shipping plan”  
- **Modeling upgrades:** larger ID embeddings; improved losses/activations; more advanced user sequence modeling  
  
#### Funnel / infra efficiency  
- **L1 utility layer** + funnel efficiency improvements (early controls, alignment with downstream ranking, cost/latency optimization)  
- **PhP** and related funnel improvements (internal naming; keep consistent with internal context)  
- **LWS GPU serving:** unblocked model scale with materially better cost/latency profile  
  
#### Research + technical communication  
- **Multi-Embedding KDD paper**  
- Multiple blog posts  
- ML Symposium + ML Day presentation(s) on LWS / CLR / PhP  
- Improved clarity and trust in offline evaluation (faster + more reliable offline experiments)  
  
#### Retentive Recs → concrete shipping plan (status)  
- Took Retentive Recs from product vision → concrete signal + launches:  
  - **Launched in ranking**  
  - **Two additional launches coming** in retrieval and blending  
- Clear roadmap focused on driving retention (WAU/MAU)  
  
#### Cross-surface experimentation  
- Established and started **UPP Retrieval experiment on Notifications** (technical + company impact)  
  
### D) Operational improvements (maturity & leverage)  
- Deprecation program: topics / bestpins / pinacle2; plus active work on **ownership clarity** (“find the right owners for workflows”)  
- Process rigor and runbooks:  
  - HF oncall revamp  
  - “Manas debugging runbooks” and structured debugging practice  
- Wiki improvements: better documentation of funnel numbers + shared understanding of the stack  
  
---  
  
## Technical system overview (high-signal mental model)  
  
### Candidate generation pipeline (conceptual)  
1) **Candidate supply / sources** (multiple retrieval sources; learned + legacy until consolidated)  
2) **Conditioning / query composition** (user state, intent, constraints)  
3) **Retrieval / recall** (broad fetch under latency constraints)  
4) **Fast shaping** (LWS / filtering / dedupe / early controls / diversification constraints)  
5) **Contracts to downstream** (candidate set + features + provenance + constraints → Ranking / Blending)  
  
### What we optimize (typical tradeoffs)  
- Recall vs precision  
- Freshness vs relevance  
- Diversity/coverage vs short-term engagement  
- Latency/cost vs quality  
- Stability vs iteration speed (trust preservation)  
  
---  
  
## 2026 roadmap priorities (themes to preserve)  
Keep the language close to original intent.  
  
### Themes (core)  
- **Further consolidate the stack**  
  - Unified Personalization Platform direction  
  - CLR to replace heuristic CGs  
- **Achieve ambitious SSv2 goals**  
  - Retrieval/LWS model scaling up  
  - Generative Recommendations (**RecGPT / PinRec**)  
- **Grow retention (WAU, MAU)**  
  - Retentive Recommendations roadmap  
- **Cost savings + user experience**  
  - Business logics in L1 utilities  
  - Personalized budget tunings  
  - Responsiveness & feedback loops  
- **Grow i18n ecosystems and content freshness**
  - Merit-driven distribution
  - Content exploration funnel

### Q2 2026 Focus (updated March 2026)
- **UPP cross-surface expansion:** At least one surface beyond Homefeed with working UPP integration and measurable results by end of June. Must-win presentation March 30.
- **Retentive Recs / p(UIC):** Integrated into anticipation flow with measurable retention improvement. Andrew's CTO demo with real data.
- **RecGPT:** One production-quality generative retrieval result + ATG investment signal.
- **JJ promo to IC16:** Target end of June.
- **EM backfill:** Experienced EM hire; James runs pipeline, Dylan in for finals.
- **Performance decisions:** Charlie, Hanlin, Sophia, Zili checkpoints mid-Q2.

See `q2_roadmap.md` for full structural plan, risk mitigation, and team operating model.

### Start / Stop framing (2026)  
  
#### Things to START  
- **Reliability + debuggability as first-class investment**  
  - Build **agentic workflows** for end-to-end tracing across the HF stack (faster root-cause, fewer regressions)  
  - Reduce “whack-a-mole” debugging time  
- **Explore Page**  
  - Dedicated Explore backend to reliably surface new ideas/use cases; drive more active days, WAU, retention  
- **VLM & LLM integrations**  
  - Domain moving rapidly; invest to adopt advancements continuously  
  
#### Things to STOP  
- **Duplicative improvements across individual models**  
  - Consolidate user sequence modeling iterations  
- **Heuristic-based CG iterations**  
  - High maintenance / limited upside; prioritize scalable model-based approaches  
  
---  
  
## Unified document strategy (single doc serving 3 audiences)  
Primary artifact: one document with layered readability.  
  
### Layer 1 — Exec skim summary (top; ~1/3 page)  
Must include:  
- **+2.1% SSv2**  
- **+0.33% WAU (~+1.1M)**  
- **~$3M/yr savings**  
- **NUX unblock + 1% NUX Growth goal**  
- **Notifications: 6–7 launches**  
Format requirement:  
- **3–5 bullets**, crisp, no paragraphs  
  
### Layer 2 — Peer/system-level narrative (next ~1–1.5 pages)  
- DRP vs RCG missions and ownership boundaries  
- Platformization interfaces and where CG creates leverage for other teams  
- 2026 priorities and cross-org asks/enablement  
  
### Layer 3 — Internal team narrative + details (remaining 3–6 pages)  
- People growth + reorg story  
- Technical pillars + major launches + deprecations  
- Operational maturation  
- 2026 vision and how engineers plug in  
  
---  
  
## Voice / style requirements (for Year-in-Review outputs)  
- Executive presence: crisp, direct, high-signal; minimal fluff  
- Prefer bullets and strong verbs; avoid generic praise  
- Concrete nouns: systems, launches, deprecations, savings, outcomes  
- If placeholders are needed, label them explicitly (topline 2025 metrics above are **not** placeholders)  
  
---  
  
## Known constraints & realities  
- Tier1 must stay compact (Helix upload limits); keep raw detail outside Tier1 and link it.  
- Leadership expectation: **accuracy and trust** in exec-facing responses are non-negotiable.  
- Team maturity dictates bandwidth: independence → more outward/platform leverage; instability → more internal foundation work.  
  
---  
  
## Pointers to raw material (outside Tier1)  
> Add raw docs here instead of pasting them into Tier1.  
  
- **Pointer:** Unified “2025 Year in Review” doc (exec skim + deeper layers)    
  **Location:** Pinterest Context/<outside Tier1 path>    
  **Why it matters:** canonical narrative + verified numbers + reusable bullets    
  **Extracted state:** encoded above in topline metrics + 2025 arc + 2026 themes  
  
- **Pointer:** 2026 planning slides / roadmap source deck    
  **Location:** Pinterest Context/<outside Tier1 path>    
  **Why it matters:** preserves exact language of priorities + start/stop framing    
  **Extracted state:** encoded above in 2026 priorities + start/stop  
  
---  
  
## Open questions (stateful)
- Where are the crispest ownership boundaries between CG / Ranking / Blending for upcoming launches (especially Retentive Recs + RecGPT)?
- What is the highest-leverage “agentic debugging/tracing” workflow to build first (end-to-end HF tracing, regression triage, launch validation)?
- Explore Page: who is the single-threaded owner across backend/UX, and what success metrics define “worth it” in 2026?
- What is the right EM JD framing to target the Two-Track Org end state (Production track vs Frontier track)?
- How to sequence performance management for Charlie and Zili with Dylan's air cover?  
  
---  
  
## Review cadence
- Last Updated: 2026-04-01
- Next Review: monthly  
