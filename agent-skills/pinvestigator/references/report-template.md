# PInvestigator Report Template

Produce the output in markdown inside a codefence for easy copy-pasting into a Google Doc.

## Report Structure

```markdown
# Investigation Report

**Investigation Metric:** <TARGET_METRIC>
**Investigation Date Range:** <TARGET_DATE_RANGE start> to <TARGET_DATE_RANGE end>

### Data Coverage

| Data Source | Date Range Used | Missing / Gaps |
|-------------|----------------|----------------|
| Engagement (core) | <earliest dt> to <RANGE_END> | <any missing dates or tables that failed> |
| Engagement (YoY) | <YoY window> | <any missing dates> |
| Engagement (baseline variance) | <N weeks of samples used> | <if fewer than 12 weeks, state why> |
| Holdout (core) | <RANGE_START − 10d> to <RANGE_END> | <any missing dates, early-quarter note> |
| Holdout (WoW/MoM) | <dates fetched> | <which comparisons were not possible and why> |
| Slack | <search window per channel> | <any channels that returned no results> |

---

## SECTION 1: What do we know about <TARGET_METRIC> so far?

Snapshot of WoW, MoM, YoY movements of <TARGET_METRIC> across TARGET_DATE_RANGE.
For rate metrics, summarize for both the numerator and denominator.

### Rate Decomposition Table

For multi-day ranges, show one table per date with significant movement (z-score > 2). Summarize stable dates in one line.

| Date | Metric | Volume WoW % | Impressions WoW % | Driver |
|------|--------|-------------|-------------------|--------|
| (each significant date) | (12 action metrics, each paired with impressions) | ... | ... | ... |

Driver: NUMERATOR (volume moved >2x more than impressions), DENOMINATOR (impressions moved >2x more than volume), or BOTH.

### Expectations

- Is this type of movement for <TARGET_METRIC> expected based on movements of other metrics?
- Is this expected due to any holidays around this time?
- Is this a slow drift (DRIFT) or a sudden drop (CLIFF)? If the latter, which date(s) are most important to pay attention to?

---

## SECTION 2a: Breakdowns of <TARGET_METRIC> by different dimensions

For each dimension, generate a table:

| Metric | Dimension | WoW % | MoM % | YoY % | ISOLATED MOVEMENT? (> 2x peers) |
|--------|-----------|-------|-------|-------|----------------------------------|

### by_app
(table)

### by_surface
(table)

### by_country
(table)

### by_rtc
(table — HOME_FEED RTCs only for analysis. Tag each with surface, e.g., "PINNABILITY_MULTI_EMBEDDINGS (HOME_FEED, ~15% share)". Aggregate HOME_FEED RTCs with <1% share into OTHER_HF. Non-HOME_FEED RTCs go in a single "Other Surfaces (reference only)" row with aggregate volume — no isolation analysis.)

---

## SECTION 2b: Holdout Divergence Analysis

⚠️ REQUIRED — DO NOT SKIP

### Date Verification
After each holdout query, compare COUNT(DISTINCT dt) returned against dates requested. If they differ, explain the gap before showing the comparison.

### Presentation Rules
1. All holdout experiments MUST use the same table schema
2. Show full time series tables ONLY for 🔴 findings
3. For 🟡, show a single summary row with range of Δ%
4. For 🟢, group by experiment and state "All metrics flat (<X% Δ)" in one line

### Holdout Table Format

| Experiment | Metric | Eng Rate Δ% (action/imp) | Per-User Rate Δ% (action/users) | Trend |
|------------|--------|--------------------------|----------------------------------|-------|

### Key Holdout Observations (scoped to holdout data ONLY)

- For each 🔴 finding: do the engagement rate and per-user rate tell the same story, or do they diverge?
- Does the holdout divergence pattern align with the TARGET_METRIC anomaly timeline (TARGET_DATE_RANGE)?
- Which holdout experiment(s) show the strongest signal, if any?
- If ALL holdouts show stable deltas → the metric movement is likely NOT caused by a gated launch. State explicitly.
- If a specific holdout diverges → name it and connect it to dimensional findings in Section 2a.

---

## SECTION 2c: Slack Context

Launches, experiments, alerts, and deployments found in Slack that may explain the metric anomaly.

### Summary Table

| # | Channel | Type | Name | Event Date | Confidence | Link |
|---|---------|------|------|------------|------------|------|

### Detailed Findings

For each 🔴/🟡 finding: one paragraph connecting it to the specific anomaly signal (which metric, which dimension, which date — follow Principle 8).

If no relevant context found: state which channels were searched, what window was used, and suggest the user post in #homefeed-metrics with the specific findings from the report.

---

## SECTION 3: Key Findings

Cross-correlated across engagement + holdout + Slack:

3-5 most important key observations synthesizing across all data sources. Connect:
- Dimensional isolation (Section 2a) with Slack events (Section 2c)
- Holdout divergence (Section 2b) with identified launches/experiments (Section 2c)
- CLIFF/DRIFT patterns (Section 1) with event timelines (Section 2c)

---

## SECTION 4: Suggested Next Steps

High-level suggestions following Principle 8 (observation → reasoning → action):

- Should we start a more formal investigation?
- If so, where to go next and why?
- What specific teams, dashboards, or experiments to check?
- **If CLIFF pattern, RTC reallocation, or holdout divergence was found:** suggest a targeted Slack follow-up in MODE 2 with specific channels and keywords (e.g., "Search #homefeed-change-logs for '{experiment_name}' around {RANGE_START}")
- **If Slack search found nothing relevant:** suggest the user post in #homefeed-metrics with the specific findings, or check Helium directly
```
