# RTC Per-Surface Distribution

**RTC** = Reason To Choose, also known as Candidate Generators or Feed Source. This is the algorithm/source that produced a recommendation. RTCs span multiple surfaces — each surface has its own set of candidate generators. There are ~90 RTC sources total across all surfaces.

## Impression Share by Surface (as of 2026-03-14)

**HOME_FEED** (~10.6B daily impressions)

| RTC | Share | Description |
|-----|-------|-------------|
| PINNABILITY_MULTI_EMBEDDINGS | ~15% | Multi-embedding Pinnability recommendations |
| PINNABILITY_CONDITIONAL_PIN_EMBEDDINGS | ~14% | Conditional pin embedding Pinnability |
| PINNABILITY_CONDITIONAL_BOARD_EMBEDDINGS | ~12% | Conditional board embedding Pinnability |
| INSTANT_PFY_NON_MATERIALIZABLE | ~12% | Real-time Pins For You |
| PROMOTED_PIN | ~11% | Ads |
| RECOMMENDED_TOPICS | ~9% | Topic-based recommendations |
| PINNABILITY_CONDITIONAL_UIC_PIN_EMBEDDINGS | ~6% | UIC-conditioned Pinnability |
| NAVBOOST_PFY | ~5% | NavBoost-powered Pins For You |
| FRESH_REPIN_BOARD | ~2% | Fresh content from repin boards |
| REPIN_BOARD | ~2% | Board-based repin recommendations |

**RELATED_PIN_FEED** (~24.9B daily impressions — largest surface)

| RTC | Share | Description |
|-----|-------|-------------|
| P2P_NAVBOOST_CAND | ~42% | NavBoost pin-to-pin candidates |
| P2P_RANDOMWALK_CAND | ~22% | RandomWalk pin-to-pin candidates |
| P2P_TWO_TOWER_EMBEDDING_CAND | ~13% | Two-tower embedding P2P |
| NA | ~12% | Untagged |
| P2P_PINCLIP_CAND | ~4% | PinCLIP visual P2P |
| P2P_TWO_TOWER_MID_FUNNEL_FRESH_EMBEDDING_CAND | ~3% | Two-tower fresh mid-funnel P2P |
| P2P_RECGPT | ~2% | RecGPT-powered P2P |
| P2P_P2B2P_FRESH | ~1% | Pin-to-board-to-pin fresh |

**SEARCH_PINS** (~10.3B daily impressions)

| RTC | Share | Description |
|-----|-------|-------------|
| BASEPRIME_GPU | ~49% | Token Based Retrieval |
| LEARNED_RETRIEVAL | ~14% | Learned retrieval model |
| BASE | ~13% | Base retrieval |
| BASEPRIME_GS | ~11% | BasePrime GraphSage |
| GENERATIVE_RETRIEVAL_RECGPT | ~7% | RecGPT generative retrieval |
| BASEPRIME | ~3% | BasePrime standard |
| FRESH_LR_PIN | ~1% | Fresh learned retrieval |

**BOARD_IDEAS_FEED** (~0.75B) and **BOARD_FEED** (~1.2B) are dominated by NA (untagged). RTC analysis is not meaningful for these surfaces.

## Surface Attribution Rules

When analyzing `homefeed.pinvestigator_engagement_by_rtc`:
- The table mixes RTCs from ALL surfaces. Always tag findings with the surface using the mapping above.
- **Analysis scope: HOME_FEED RTCs only.** Since this skill investigates homefeed anomalies, only HOME_FEED RTCs should be used for uniformity checks and isolation analysis. Non-HOME_FEED RTCs are included for reference only (aggregate them into a single "Other Surfaces" row).
- **HOME_FEED RTCs:** `PINNABILITY_*`, `FRESH_*`, `NAVBOOST_PFY`, `RECOMMENDED_TOPICS`, `INSTANT_PFY_*`, `REPIN_BOARD`. Analyze these for isolation and movements.
- **NON-HOME_FEED RTCs (reference only):**
  - `P2P_*` → RELATED_PIN_FEED
  - `BASEPRIME*`, `BASE*`, `LEARNED_RETRIEVAL`, `GENERATIVE_RETRIEVAL_*` → SEARCH_PINS
- `PROMOTED_PIN` appears primarily in HOME_FEED but can appear in other surfaces at negligible volume. Include in HOME_FEED analysis.
- `NA` appears across multiple surfaces — movements in NA are hard to attribute; flag but do not over-interpret.
