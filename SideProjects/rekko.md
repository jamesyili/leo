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

### Daniel's read (2026-04-02)
- Feels it's too early to pivot — "only done the groundwork"
- Has people signing up and kicking tires, no paying customers
- Wants more time for growth hacking before changing direction
- Full product suite is launched, content/SEO happening

### Strategic assessment (from Daniel's Claude + our Medvi analysis)
- Core problem: product pointed in every direction, no single flywheel spinning
- Three potential bets: (1) shadow trading to prove analysis works, (2) TikTok content-first distribution, (3) API for AI agents via MCP + x402
- Recommended sequence: shadow trading first (cheapest way to validate), then TikTok, then decide
- Medvi comparison: Rekko has far more sophisticated tech but Medvi found a money pipe (GLP-1 demand) and focused entirely on distribution. Rekko needs to find its equivalent demand signal.

## James's ML Tracks

| Track | Status | Notes |
|-------|--------|-------|
| A: Category trading rules | Ready now | Tennis/NCAA mispricing is real and exploitable |
| B: Content ranking | Blocked | Needs engagement data from published videos |
| C: Price movement prediction | Explorable | 1.6M hourly ticks available |
| D: Watchlist (clean data) | Background | Check ~late April for 50+ resolved pairs |
| E: Anomaly detection | Deferred | After A and C |

## Open Questions (for Daniel conversation 2026-04-03)

1. What does TikTok engagement actually look like on published videos?
2. Should they pick ONE bet and go all-in for 30 days?
3. Is the prediction market vertical big enough, or should the content pipeline point at a bigger market (sports betting, stocks, crypto)?
4. What's the Medvi-equivalent demand signal — where is demand massively outstripping supply?

## Conversation framing (2026-04-03)

Goal: talk through how to make money. Not technical gaps — finding traction. Daniel has said James gave him a lot to think about (re: Medvi analysis). Use monetization as the forcing function to focus.
