# Rekko

Last updated: 2026-04-02

---

## What It Is

Rekko (rekko.ai, @rekko.ai on TikTok) is an automated prediction market analysis, trading, and content pipeline. Takes a prediction market bet, runs multi-stage AI research/analysis, generates a structured recommendation, optionally trades it, and produces/publishes TikTok videos — end to end.

**Codebase:** `/home/james/src/project_with_daniel/rekko.ai/`

## Team

- **James** — data, ML models, ranking, anomaly detection, personalization. ~5 hrs/week alongside full-time Pinterest job. In it primarily for learning, secondarily for financial upside. Invested $10K in Daniel's previous startup (Salmon.ai).
- **Daniel (Dan)** — built the entire Rekko system solo. Former CTO (Salmon.ai), ex-initialize.ai, strong full-stack/infrastructure engineer. One of James's best friends since college (sophomore year). Near full-time on Rekko with light consulting on the side. Takes the lion's share of any upside given the risk/time asymmetry. James considers him one of the best engineers he's ever known.

### History
- Daniel was CTO at Salmon.ai; his CEO pushed him out (shady circumstances). James had invested $10K — outcome of that investment TBD depending on how Salmon.ai plays out.
- Deep mutual trust despite the investment loss. Daniel has explicitly said he wants James to be part of Rekko's upside.

## Current Status (2026-04-02)

### What's built (extensive)
- 39 API endpoints, 25 MCP tools, 4 auth methods (Unkey + Stripe + RapidAPI + x402 USDC)
- Full self-service billing platform
- Discord bot (10 channels), X/Twitter content pipeline, Remotion video renderer
- Ensemble forecasting, Platt scaling calibration, whale alerts, arbitrage scanning
- Dual TUI (Textual + Ink) with NDJSON bridge
- 364 pipeline runs, 1,029 markets scraped, 302 TikTok scripts generated
- ML: safe bet classifier (concluded — can't beat market price with current data), category-level mispricing finding (tennis/NCAA favorites overpriced)

### What's missing
- **0 paying customers**, 0 trades placed (live or shadow), 0 API keys issued
- Only 9 finished videos on disk despite 302 scripts
- No feedback loop — no engagement data, no validated track record
- No evidence the analysis actually works (364 runs, zero validated against outcomes)

### Daniel conversation debrief (2026-04-03)

**Core question resolved:** What have we built that's truly hard to replicate and has enduring value?

**Answer: The video generation pipeline.** Agreed to bet on building an engine to hyper-produce trending AI videos and farm engagement at scale. Monetization angle TBD — first priority is building up an audience.

**Decisions:**
- P1: AI video engine for trending content. Daniel has an exact recipe for what works. James to put together a plan and share tonight/tomorrow.
- ML models paused for now — too far off from traction.
- James needs to understand Daniel's video generation pipeline before planning next steps.

**P2 ideas (parked, not dead):**
- Whale watching — monitoring large prediction market bets as content/signal
- Automated index fund for prediction markets — passive diversified exposure
- Peptides e-commerce — inspired by Medvi, unregulated niche but growing. Legality questioned; agreed to discuss later.

**Inspiration:** @raycfu (Rui Fu, ex-Meta SWE, 98K followers) — content-first audience building + productized knowledge + done-for-you services. Potential model for monetizing once audience exists.

## James's ML Tracks (paused)

| Track | Status | Notes |
|-------|--------|-------|
| A: Category trading rules | Paused | Tennis/NCAA mispricing is real but deprioritized |
| B: Content ranking | Paused | Needs engagement data from published videos |
| C: Price movement prediction | Paused | 1.6M hourly ticks available |
| D: Watchlist (clean data) | Background | Check ~late April for 50+ resolved pairs |
| E: Anomaly detection | Paused | After A and C |

## Next Steps (James)

1. Understand Daniel's video generation pipeline (codebase review)
2. Put together a plan for the AI video engine bet
3. Share plan with Daniel tonight or tomorrow
4. Follow up on peptides legality question
