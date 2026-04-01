# Pinsight

LLM-powered deep analysis tool for Homefeed recommendation systems — user understanding, request debugging, and aggregate insight generation.

Last Updated: 2026-03-31

---

## What It Does

Pinsight equips Homefeed (and eventually other surfaces) with automated, deep analysis of recommendation systems using LLMs/VLMs. Three capability layers:

1. **HF Request Debugger (M1)** — Given an employee ID + timestamp, fetch and diagnose a full Homefeed request across all 14 funnel stages. "What happened to this candidate at every step?"
2. **User Understanding Summary (M2)** — Given a user ID, generate a rich interest/intent profile using VLM analysis of engagement history. Evaluates how well the system understands the user.
3. **Scale Analysis (M3)** — Run Pinsight at scale (hundreds of thousands of queries) to surface systematic patterns: relevance gaps by segment, content supply gaps, training data staleness, cross-surface quality differences.

## Strategic Context

### Reflex Connection
Pinsight is the **sensing and diagnosis layer** of Andrew Yaroshevsky's (Sr. Director, Product) Reflex vision — a self-healing discovery stack. Reflex's pipeline:
1. **Detect** where experience is failing → PINvestigator + Pinsight M3
2. **Diagnose** likely causes → Pinsight M1 + M2
3. Design interventions → (future)
4. Verify → (future)
5. Experiment → (future)
6. Explain results → Pinsight + PINvestigator reporting
7. Roll out → (future)

James is co-owning the Detect + Diagnose layers with Andrew. Andrew is pitching Reflex to the CTO and Kartik (Chief Architect).

### Roberto / Search Dynamic
Roberto (Sr. EM, Search) built a similar funnel debugging tool on Search logs using Claude Code. Jeff highlighted it to the entire org. Key distinctions:
- Roberto's tool = funnel debugging on Search logs. Does NOT do LLM-powered user understanding.
- Pinsight M1 = parity for Homefeed (~10 hours to build)
- Pinsight M2 + M3 = differentiated. No one else is doing this.
- Strategy: ship M1 for parity, then differentiate. Connect with Roberto as peers after M1 ships.

## Data Substrate

### Full Funnel Logging (14 stages)
James's team built comprehensive request tracing for HF. Alok completing by April 4, 2026.

| Stage | What's Logged |
|-------|--------------|
| AT_REQUEST_ENTRY | User context, request params |
| AFTER_SIZER_CALCULATION | Sizer values |
| AFTER_RESOURCE_FETCHING | Signal values |
| AFTER_CANDIDATE_GENERATION | Candidates + metadata |
| AFTER_PRERANKING_FILTERING | Surviving candidates + LWS signals |
| AFTER_LWS | Per-head LWS scores |
| AFTER_L1_UTILITY | L1 utility scores |
| AFTER_RANKING_BATCHING | Batch size/metadata + ranking signals |
| AFTER_RANKING | Per-head ranking scores |
| AFTER_POST_RANKING_FILTERING | Candidates + filter attribution |
| AFTER_PRESORTING | Utility scores + SSD signals |
| AFTER_SSD | SSD scores + metadata |
| FINAL_CHUNK | Final candidate set returned |

**Gap:** More Ideas surface not included in logging. Extension needed if relevance fire continues.

## Q2 2026 Milestones

### M1: HF Request Debugger (Target: mid-April 2026)
- **What:** Employee ID + timestamp → full funnel trace + LLM-powered diagnosis
- **Why first:** Quick win (~10 hours), Roberto parity, immediately demoable, execs love it
- **Demo to Jeff:** After PINvestigator demo (PINvestigator goes first)
- **Owner:** James builds v0, Alok extends

### M2: User Understanding Summary (Target: late Q2)
- **What:** User ID → VLM-powered interest/intent profile from engagement history
- **Why it matters:**
  - Evaluates UIC model for Retentive Recs (Goal 1 tie-in)
  - Tests VLM capabilities for understanding user history
  - Differentiated — no one else building this
- **Owner:** James architects, handoff TBD

### M3: Scale Analysis (Target: late Q2 / stretch)
- **What:** Run Pinsight hundreds of thousands of times, aggregate for systematic insights
- **Use cases:**
  - Systematic relevance gaps by user segment
  - Content supply gaps for high-intent users
  - Training data staleness signals
  - Cross-surface quality comparison
  - UIC validation at scale (does the model see what the LLM sees?)
- **Owner:** TBD
- **Constraint:** Cost management for LLM calls at scale

## Origin

Summer 2025 hackathon prototype. Original team included Alok (motivated, still invested). Vision: LLM-powered understanding of users and recommendations — going beyond internal data to incorporate "world knowledge" for richer insights.

Original Pinsight vision included:
- Helix-powered user understanding using LLMs for semantic/world knowledge
- User journey mapping (enticed → activated → stabilized → retired)
- Future external data integration (e.g., Gmail with consent)
- Smart efficiency via representative sampling for LLM analysis

## Staffing

| Person | Role | Notes |
|--------|------|-------|
| James | Architect / v0 builder | Timeboxed. Exit criteria TBD after M1 ships. |
| Alok | Logging (done Friday) → DT → extends Pinsight later | Original hackathon team. Motivated. |
| Darren's eval DS | Eval framework | Via partnership with Darren's infra team |

## Partnerships

| Partner | What they bring | Play |
|---------|----------------|------|
| **Darren Regers** (Sr. EM, Infra) | Eval DS, willing to invest resources | Go deep. Primary partnership. Give milestones, get DS committed. |
| **Brian Lee** (Activation/Growth) | Weekly AI forum, front-end tooling | Use forum for visibility/demos. Don't force engineering collab. |
| **Kent** (Core Serving Infra) | System log debugging | Pass. Different domain, manager may leave. |
| **Roberto** (Sr. EM, Search) | Search equivalent tool, Jeff's attention | Wait until M1 ships, then peer-to-peer shared platform conversation. |

## Positioning

### With Dylan (Friday 1:1)
"Andrew shared his Reflex vision and invited me to co-own the sensing layer — Detect and Diagnose. It maps directly to PINvestigator and Pinsight, and ties into Retentive Recs through UIC evaluation. Darren's team is contributing eval support. I'd love your take — any landmines? And I want to keep you in the loop given your AI interest."

### With Jeff
PINvestigator demo first (next bi-weekly). Pinsight M1 demo next. Each builds the story incrementally.

### With Andrew
Name added to Reflex doc. Co-owning Detect + Diagnose layers. Wait for his CTO pitch outcome, then align on next steps with Kartik.

## Success Criteria (End of Q2)
- Pinsight M1 shipped and used for real HF debugging
- Pinsight M2 working prototype tied to UIC eval
- Darren's eval DS actively contributing
- Andrew has pitched CTO on Reflex; James named on Detect + Diagnose
- Dylan sees AI work as strategic, not a side project

## Open Items
- Handoff criteria for Pinsight — when does James stop being TL? (Resolve after M1 ships)
- More Ideas logging gap — extend if relevance fire continues
- Scope out Roberto's code to inform M1 build
- Alok's milestone doc — compare with James's milestones and align
