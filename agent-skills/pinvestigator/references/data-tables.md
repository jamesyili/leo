# PInvestigator Data Tables Reference

All tables are partitioned by `execution_dt`, but for analysis purposes only filter on `dt`. Data range: 2025-01-12 to present.

## Data Availability Constraints

These constraints apply to ALL tables in this skill (engagement, breakdown, freshness, shopping, and holdout).

- **execution_dt retention = 60 days.** Only the most recent 60 days of execution_dt partitions are retained.
- **Each execution_dt covers ~45 days of dt.** When the pipeline runs on execution_dt 2026-03-10, it writes data for approximately the prior 45 days of dt values.
- **Recent dt values may be missing.** Dates close to the execution_dt (e.g., dt = 2026-03-08, 2026-03-09, 2026-03-10) are often not yet available in that execution.
- **Maximum dt lookback ≈ 100 days.** The oldest execution_dt (60 days ago) contains dt values going back ~45 days from that point, giving a theoretical maximum of ~100 days of dt data from the current date.
- **Investigating older dates reduces the available window.** If TARGET_DATE_RANGE ends 60 days ago, only ~45 days of prior dt data may be available. If TARGET_DATE_RANGE is recent, up to ~100 days of prior dt data may be available.

## Valid action_type Values

| action_type | Description |
|-------------|-------------|
| NUM_PIN_IMPRESSION | Total impressions (denominator for most rates) |
| NUM_PIN_REPIN | Repins (saves) |
| NUM_PIN_GRID_CLICK | Closeups |
| NUM_PIN_HIDE | Hides (negative signal) |
| NUM_PIN_REPIN_OUTBOUND_CLICK | Outbound clicks from repins |
| NUM_PIN_SAVE_TO_DEVICE | Save-to-device actions |
| NUM_PIN_SCREENSHOT | Screenshots |
| NUM_PIN_REACT | Reactions |
| NUM_PIN_SHARE_COMPLETED | Shares |
| NUM_VIDEO_V50_WATCH_TIME_MS | Video watch time (ms) |
| NUM_P2P_SESSION_PIN_IMPRESSION | P2P session impressions |
| NUM_P2P_SESSION_PIN_REPIN | P2P session repins |
| NUM_REPIN_FROM_BOARD_CREATE | Repins via board creation |

## Table Schemas

### homefeed.pinvestigator_engagement (main)

All engagement metrics, one row per action_type per day.

| Column | Type | Description |
|--------|------|-------------|
| action_type | varchar | Metric name (see values above) |
| count | bigint | Metric value |
| dt | date | Date of the metric |
| execution_dt | timestamp(6) with time zone | Pipeline run timestamp (partition key) |

### Breakdown Tables (shared schema)

These tables share the same metric columns, each adding one breakdown dimension:

| Table | Breakdown Column | Valid Values |
|-------|-----------------|--------------|
| homefeed.pinvestigator_engagement_by_app | app | IPHONE, ANDROID_MOBILE, IPAD, ANDROID_TABLET, WEB_DENZEL, WEB_MOBILE, null |
| homefeed.pinvestigator_engagement_by_surface | surface | HOME_FEED, RELATED_PIN_FEED, SEARCH_PINS, BOARD_FEED, BOARD_IDEAS_FEED |
| homefeed.pinvestigator_engagement_by_country | country_group | US, UCAN, P6, Global (nested: US ⊂ UCAN ⊂ P6 ⊂ Global) |
| homefeed.pinvestigator_engagement_by_rtc | rtc | ~90 RTC sources (BASEPRIME_GPU, BASEPRIMEEXP, PINNABILITY_*, FRESH_*, P2P_*, etc.) |

Shared metric columns for ALL breakdown tables:

| Column | Type |
|--------|------|
| num_pin_repins | bigint |
| num_pin_impressions | bigint |
| num_outbound_clicks | bigint |
| num_pin_clicks | bigint |
| pin_impression_duration_secs | bigint |
| dt | date |
| execution_dt | timestamp(6) with time zone |

### homefeed.pinvestigator_engagement_freshness (narrow)

| Column | Type |
|--------|------|
| fresh_impressions | bigint |
| fresh_repins_longclicks | bigint |
| dt | date |
| execution_dt | timestamp(6) with time zone |

### homefeed.pinvestigator_engagement_shopping (narrow)

| Column | Type |
|--------|------|
| impressions | bigint |
| longclicks | bigint |
| dt | date |
| execution_dt | timestamp(6) with time zone |

### homefeed.pinvestigator_holdout_metrics (holdout)

Holdout experiment metrics comparing control (holdout) vs enabled (launched) groups.

| Column | Type | Description |
|--------|------|-------------|
| dt | date | Date the metric covers |
| execution_dt | timestamp(6) with time zone | Pipeline run timestamp (partition key) |
| experiment_name | varchar | Name of the holdout |
| metric | varchar | Metric name |
| control_numerator | bigint | Metric numerator for control (holdout) group |
| enabled_numerator | bigint | Metric numerator for enabled (launched) group |
| control_users | bigint | Number of users in control group |
| enabled_users | bigint | Number of users in enabled group |

**Valid experiment_name values (2026 Q1):** home_relevance_holdout_2026_q1, search_quality_quarterly_holdout_26q1, related_pins_quarterly_holdout_2026q1, hfp_longterm_holdout_2026_q1

**Quarterly reset:** Holdout experiments typically start within the first few days of each quarter (not necessarily the 1st). Data for a given experiment_name only exists from that quarter's start date. Early-quarter investigations will have very limited holdout history.

**Note:** Experiment names change every quarter (e.g., `home_relevance_holdout_2026_q1` → `home_relevance_holdout_2026_q2`). If the above names return no data, query current names (exception to the no-SELECT-DISTINCT rule): `SELECT DISTINCT experiment_name FROM homefeed.pinvestigator_holdout_metrics WHERE dt = DATE '{RANGE_END}' LIMIT 10`.

**Valid metric values (9 total):**

| metric | Scope | Description |
|--------|-------|-------------|
| hf_repins | Homefeed | Homefeed repins (saves) |
| hf_clickthroughs | Homefeed | Homefeed closeups |
| hf_long_clickthroughs | Homefeed | Homefeed long clicks (outbound) |
| hf_pin_impressions | Homefeed | Homefeed pin impressions (denominator for HF engagement rates) |
| DAU | Total | Daily active users |
| WAU | Total | Weekly active users |
| overall | Total | Overall engagement composite |
| intent_expression | Total | Intent expression actions |
| srsd | Total | Same-session repin + save-to-device |

**Expected row count:** 36 rows per dt (4 experiments × 9 metrics). If any dt has fewer than 36 rows, flag as a data gap.

## Column Name Mapping (Main ↔ Breakdown)

The main table uses `action_type` (varchar) + `count` (bigint). Breakdown tables use lowercase metric columns. This mapping prevents query errors when switching between tables.

| Main Table `action_type` | Breakdown Table Column | Description |
|--------------------------|----------------------|-------------|
| NUM_PIN_REPIN | num_pin_repins | Repins (saves) |
| NUM_PIN_IMPRESSION | num_pin_impressions | Total impressions |
| NUM_PIN_GRID_CLICK | num_pin_clicks | Closeups |
| NUM_PIN_REPIN_OUTBOUND_CLICK | num_outbound_clicks | Outbound clicks from repins |
| *(no direct mapping)* | pin_impression_duration_secs | Impression duration (breakdown-only) |

Metrics that exist ONLY in the main table (NUM_PIN_HIDE, NUM_VIDEO_V50_WATCH_TIME_MS, etc.) have NO corresponding breakdown table columns.

## Engagement Rate Formulas

Formulas for engagement rate decomposition (used by the engagement subagent). For holdout dual-rate formulas (HF Engagement Rate and Per-User Rate), see `prompts/holdout-analysis.md` Step 4.

| Rate Metric | Formula | Source Tables |
|-------------|---------|---------------|
| repin_rate | NUM_PIN_REPIN / NUM_PIN_IMPRESSION | main or breakdown (num_pin_repins / num_pin_impressions) |
| closeup_rate | NUM_PIN_GRID_CLICK / NUM_PIN_IMPRESSION | main or breakdown (num_pin_clicks / num_pin_impressions) |
| hide_rate | NUM_PIN_HIDE / NUM_PIN_IMPRESSION | main ONLY (hide is overall-only) |
| outbound_click_rate | NUM_PIN_REPIN_OUTBOUND_CLICK / NUM_PIN_IMPRESSION | main or breakdown (num_outbound_clicks / num_pin_impressions) |
| fresh_engagement_rate | fresh_repins_longclicks / fresh_impressions | freshness table ONLY |
| shopping_engagement_rate | longclicks / impressions | shopping table ONLY |
| fresh_impression_share | fresh_impressions / NUM_PIN_IMPRESSION | CROSS-TABLE (freshness ÷ main) |

## RTC Definition

**RTC** = Reason To Choose, also known as Candidate Generators or Feed Source. This is the algorithm/source that produced a recommendation. RTCs span multiple surfaces (HOME_FEED, RELATED_PIN_FEED, SEARCH_PINS, etc.) — each surface has its own set of candidate generators. There are ~90 RTC sources total.

For per-surface RTC distribution, impression shares, and surface attribution rules, see `references/rtc-surface-distribution.md`. The engagement subagent must read that file during Step 5 (RTC drill-down).

## Metric Availability

**BREAKDOWNABLE** (exist in app/surface/country/rtc tables):
num_pin_repins, num_pin_impressions, num_outbound_clicks, num_pin_clicks

**EXISTS BUT NOT USED IN ANALYSIS:**
pin_impression_duration_secs — present in breakdown tables but not used by any rate formula or drill-down step. Do not query or analyze this column.

**OVERALL-ONLY** (exist ONLY in pinvestigator_engagement):
NUM_PIN_HIDE, NUM_VIDEO_V50_WATCH_TIME_MS, NUM_PIN_SAVE_TO_DEVICE, NUM_PIN_SCREENSHOT, NUM_PIN_REACT, NUM_PIN_SHARE_COMPLETED, NUM_P2P_SESSION_PIN_IMPRESSION, NUM_P2P_SESSION_PIN_REPIN, NUM_REPIN_FROM_BOARD_CREATE

**HOLDOUT METRICS** (exist ONLY in pinvestigator_holdout_metrics):
DAU, WAU, overall, intent_expression, srsd, hf_pin_impressions, hf_repins, hf_clickthroughs, hf_long_clickthroughs
These are NOT joinable 1:1 with the engagement tables — they use different metric naming and granularity. Analyze independently.

**NARROW BREAKDOWNS ONLY:**
- freshness: fresh_impressions, fresh_repins_longclicks
- shopping: impressions, longclicks

**RULE:** Do NOT query a breakdown table for a metric it doesn't have. If a flagged metric is overall-only, state so and recommend the relevant Statsboard dashboard for dimensional cuts.

## Query Rules

All Presto queries in this skill must follow these rules:

- ⛔ Only single SELECT statements. No UNION, UNION ALL, or multi-statement queries.
- Do NOT run DESCRIBE, SHOW TABLES, or SELECT DISTINCT. All schemas and valid values are documented above.
- Run independent queries in parallel when possible.
- After receiving results, verify data makes sense (row counts, nulls, zeros).
- If a query returns unexpected results, flag the data issue rather than building on bad data.

## Date Partitioning Rules

All tables are partitioned by `execution_dt` but for analysis, only filter on `dt`:
- All tables: `execution_dt` is `timestamp(6) with time zone`, `dt` is date.
- Holdout-specific: does NOT have YoY data (experiments are quarterly). Each dt should have only one execution; if duplicates exist, use the latest `execution_dt`. Verify each dt has 36 rows (4 experiments × 9 metrics).
