# PInvestigator Architecture

## Quick Context for Development

Read this section first when modifying or extending the skill.

### File Dependencies

| File | Role | Read by | Depends on |
|------|------|---------|------------|
| SKILL.md | Orchestrator prompt | Auto-loaded | References all prompts/, references/report-template.md, references/data-tables.md |
| prompts/engagement-analysis.md | Subagent A prompt | Subagent A | references/data-tables.md |
| prompts/holdout-analysis.md | Subagent B prompt | Subagent B | references/data-tables.md |
| prompts/slack-search.md | Subagent C prompt | Subagent C | — |
| references/data-tables.md | Shared schema reference | Subagent A, Subagent B | — |
| references/rtc-surface-distribution.md | RTC → surface mapping | Subagent A (Step 5 RTC drill-down) | — |
| references/report-template.md | Report format | Orchestrator (Phase 3) | — |
| references/principles.md | Human reference | Not read at runtime | — |
| MCP_SETUP.md | Troubleshooting | Orchestrator (on MCP errors) | — |
| ARCHITECTURE.md | Dev context (this file) | Orchestrator (on dev/design discussions) | — |

### Source of Truth

When modifying a rule, change it in the ground truth file. Other files reference it — do not duplicate.

| Rule | Ground truth | Referenced by |
|------|-------------|---------------|
| Table schemas, column names, valid values | `references/data-tables.md` | engagement-analysis.md, holdout-analysis.md, SKILL.md (Tool Rules, Common Mistakes) |
| Engagement rate formulas (repin_rate, etc.) | `references/data-tables.md` Engagement Rate Formulas | engagement-analysis.md Step 3 |
| Holdout dual-rate formulas | `prompts/holdout-analysis.md` Step 4 | data-tables.md (pointer only) |
| Query rules (no UNION, no DESCRIBE, etc.) | `references/data-tables.md` Query Rules | engagement-analysis.md, holdout-analysis.md |
| Slack channels + IDs | `prompts/slack-search.md` Channels table | ARCHITECTURE.md Slack Channels (verification tracking only) |
| Slack API budget | `prompts/slack-search.md` Budget section | — |
| Baseline variance & z-score | `prompts/engagement-analysis.md` Baseline Variance section | engagement-analysis.md Step 3, Step 5 |
| Investigation principles (inline) | Each prompt file's inline excerpts | references/principles.md has full versions for humans |
| MCP config | `MCP_SETUP.md` | ARCHITECTURE.md MCP Configuration (summary only) |

### Known Limitations

- Full MODE 1 run takes ~10 min wall-clock. Engagement subagent is the bottleneck (~8 min vs ~5 min holdout, ~2 min Slack). Future optimization: split engagement into two subagents (rate decomposition vs dimensional drill-down).
- Slack MCP has no keyword search tool (`search_messages` does not exist). Slack subagent uses `get_channel_history` with timestamp filters as the primary tool. See slack-search.md API Rules.
- Holdout experiment names change quarterly — data-tables.md must be updated each quarter.
- No Statsboard or Helium MCP integration — dimensional cuts beyond the engagement tables require manual dashboard checks.

### How to Test Changes

- **Full smoke test:** Run `/pinvestigator` with a known date or range (e.g., "investigate homefeed repin rate on 2026-03-06" or "investigate repin rate from 03/01 to 03/06") and verify the affected report section.
- **Single subagent test:** Spawn one subagent directly with the Agent tool, passing TARGET_DATE_RANGE, TARGET_METRIC, and SKILL_DIR. No need to run the full MODE 1.
- **Schema changes:** After editing data-tables.md, run a simple Presto query to confirm column names and types match the documentation.
- **Slack changes:** After editing slack-search.md, test with a single `get_channel_history` call to verify channel IDs and timestamp format.

## File Structure

```
pinvestigator/
├── SKILL.md                    [AGENT PROMPT — auto-loaded]     Orchestrator: mode routing, phase execution, synthesis
├── ARCHITECTURE.md             [AGENT+HUMAN — read for dev]     This document: architecture, history, changelog
├── MCP_SETUP.md                [AGENT+HUMAN — read on errors]   MCP config, verification, troubleshooting
├── prompts/
│   ├── engagement-analysis.md  [AGENT PROMPT — Subagent A]      7-table query, rate decomposition, drill-down
│   ├── holdout-analysis.md     [AGENT PROMPT — Subagent B]      Holdout dual-rate, triage, trend detection
│   └── slack-search.md         [AGENT PROMPT — Subagent C]      Broad + targeted Slack search
└── references/
    ├── data-tables.md          [AGENT REF — read by A and B]    Table schemas, column mapping, query rules
    ├── rtc-surface-distribution.md [AGENT REF — read by A]      RTC → surface mapping, impression shares
    ├── principles.md           [HUMAN REF — not read at runtime] 8 principles with full examples
    └── report-template.md      [AGENT REF — read in Phase 3]    Report output format (Sections 1-4)

Report output (separate from skill source):
tools/homefeed/pinvestigator/output/   [GIT-IGNORED]  Generated investigation reports ({start}_{end}_{metric}.md or {date}_{metric}.md)
```

## Current Architecture: Orchestrator + 3 Parallel Subagents

### Design

The investigation is split into an orchestrator (`SKILL.md`) and 3 parallel subagents, each spawned via Claude Code's `Agent` tool with `subagent_type=general-purpose`:

```
SKILL.md (orchestrator)
  │
  ├── Phase 0: Resolve TARGET_DATE_RANGE, TARGET_METRIC
  │
  ├── Phase 1: Dispatch 3 subagents IN PARALLEL via Agent tool
  │   ├── Subagent A: Engagement Analysis
  │   │     reads prompts/engagement-analysis.md + references/data-tables.md
  │   │     queries 7 Presto tables, rate decomposition, CLIFF/DRIFT, dimensional drill-down
  │   │
  │   ├── Subagent B: Holdout Analysis
  │   │     reads prompts/holdout-analysis.md + references/data-tables.md
  │   │     queries holdout table, dual-rate computation, triage
  │   │
  │   └── Subagent C: Slack Search (Broad)
  │         reads prompts/slack-search.md
  │         searches 4 channels for launches/experiments/alerts
  │
  ├── Phase 2: Synthesis — correlate findings across A + B + C
  │   Optional: targeted Slack re-search if A reveals uncovered signals
  │
  └── Phase 3: Generate report from references/report-template.md
```

### Benefits

| Benefit | Explanation |
|---------|-------------|
| **Focused context** | Each subagent receives ~100-200 lines of instructions instead of 900. Smaller prompts are followed more precisely. |
| **True parallelism** | Engagement queries, holdout queries, and Slack searches run simultaneously. Wall-clock time is bounded by the slowest subagent, not the sum. |
| **Independent tunability** | Editing `prompts/holdout-analysis.md` affects only holdout behavior. No risk of regressing engagement or Slack logic. |
| **Structural blocking** | The orchestrator physically cannot proceed to synthesis until all 3 subagents return. No "skipping Step 5" mistakes. |

## MCP Configuration

See `MCP_SETUP.md` for full configuration details, verification steps, and troubleshooting.

Summary: Presto (`presto-prod`) and Slack (`slack-prod`) on `localhost:9092`. Project permissions in `.claude/settings.local.json` allow `mcp__presto__*` and `mcp__slack__*`.

## Slack Channels

Runtime source of truth is `prompts/slack-search.md`. This table is for verification tracking only — always update slack-search.md first.

| Channel | ID | Verified |
|---------|-----|----------|
| #homefeed-change-logs | C06K41EHY | 2026-03-13 |
| #unity-alerts | C04P24RA277 | 2026-03-13 |
| #p13n-relevance-launches | C0145F4SW9G | 2026-03-13 |
| #browse-product-alerts | C017DHWSW1L | 2026-03-13 |

---

## History

### V2.3 Improvements (2026-03-18)

TARGET_DATE → TARGET_DATE_RANGE migration, report output to file, and data fixes.

**Core change: date range support**
1. **TARGET_DATE → TARGET_DATE_RANGE** — all subagents now accept `[start, end]` instead of a single date. Single-day ranges (`[date, date]`) produce identical behavior to the old single-date flow. Changed across all 7 files (SKILL.md, 3 prompts, 2 references, report-template.md).
2. **Phase 0 range resolution** — 4 input cases: explicit range, single date, "starting X" (auto-resolve end via MAX(dt)), no dates (MAX(dt) single-day).
3. **Range validation** — max 10 days (truncate to `[start, start+9]` with user notification); typo detection (start > end, mixed years) waits for user confirmation.

**Engagement subagent (date range behavior):**
4. **Rate decomposition per-day** — WoW % computed for each date in range, only dates with z-score > 2 shown in table, rest summarized as "stable".
5. **Baseline variance extracted** — z-score computation moved from Step 5 to a standalone section between Step 2 and Step 3, referenced by both steps. Eliminates circular dependency.
6. **Drill-down date selection** — always drill down on the date with highest z-score for TARGET_METRIC (even if z < 2); second date added only if z > 2. Maximum 2 drill-down dates.
7. **CLIFF/DRIFT across range** — pattern classification now operates on the full TARGET_DATE_RANGE time series.
8. **Content mix check** — explicitly uses same drill-down date(s) as Step 5.
9. **Baseline variance weekdays** — fetch trailing pairs for each distinct weekday in the range, not just RANGE_END's weekday.

**Holdout subagent (date range behavior):**
10. **Core window = `[RANGE_START − 10, RANGE_END]`** — covers pre-anomaly trend + entire anomaly period.
11. **WoW/MoM anchored on RANGE_START** — comparison dates work backward from the anomaly onset, not the end.
12. **Analysis priority updated** — "trend over past 10 days" → "trend from RANGE_START − 10 through RANGE_END".
13. **Example query dates corrected** — WoW dates now match RANGE_START-based computation.

**Slack subagent (date range behavior):**
14. **Window = `[RANGE_START − lookback, RANGE_END]`** — old hard constraint (no scanning past drop_start) removed; window now naturally covers the full anomaly period.
15. **Budget guidance for wider windows** — prioritize messages near RANGE_START for ranges > 5 days.
16. **Confidence assessment updated** — "event within onset ± 2d" → "event within TARGET_DATE_RANGE or RANGE_START ± 2d".
17. **Broad mode date focus** — "RANGE_START ± 2 days" → "near RANGE_START and throughout TARGET_DATE_RANGE".

**Report output:**
18. **Auto-save to file** — Phase 3 writes report to `tools/homefeed/pinvestigator/output/{date}_{metric}.md` (or `{start}_{end}_{metric}.md` for multi-day ranges). Output folder is git-ignored.

**Data fixes:**
19. **BASEPRIME_GPU description corrected** — "GPU-accelerated BasePrime retrieval" → "Token Based Retrieval" in rtc-surface-distribution.md.
20. **RTC analysis scoped to HOME_FEED only** — Surface Attribution Rules in rtc-surface-distribution.md updated: only HOME_FEED RTCs (`PINNABILITY_*`, `FRESH_*`, `NAVBOOST_PFY`, `RECOMMENDED_TOPICS`, `INSTANT_PFY_*`, `REPIN_BOARD`) used for uniformity checks and isolation analysis. Non-HOME_FEED RTCs (`P2P_*` → RELATED_PIN_FEED, `BASEPRIME*`/`BASE*` → SEARCH_PINS) aggregated into "Other Surfaces" for reference only.

### V2.2 Improvements (2026-03-17)

Slack API rewrite, synthesis hardening, and cross-file consistency cleanup.

**Critical fixes:**
1. **`search_messages` removed** — confirmed this tool does not exist in the Slack MCP. Rewrote slack-search.md API Rules around `get_channel_history` as primary tool with timestamp filters. Keywords repurposed as agent-side reading filters, not API parameters.
2. **Slack API budget restructured** — replaced contradictory total cap (6) + per-channel limits with per-channel limits as sole constraint (3 history + 4 thread per channel). `get_message_permalink` excluded from budget.

**Synthesis improvements:**
3. **Contradiction handling rules added** — Phase 2 in SKILL.md now handles 4 contradiction scenarios: holdout flat + Slack experiments, holdout helping + metric declining, CLIFF + no Slack events, broad-based + isolated holdout.
4. **Slack search hard constraint relaxed** — broad mode still blocks post-drop scanning, but thread follow-through and targeted mode (MODE 2) may scan `[drop_start, drop_start + 3d]`.

**Data documentation:**
5. **Holdout metric descriptions** — expanded from one-line list to full table with Scope (Homefeed/Total) and Description per metric in data-tables.md.
6. **`pin_impression_duration_secs` flagged** — moved from BREAKDOWNABLE to "EXISTS BUT NOT USED IN ANALYSIS" with explicit do-not-query instruction.
7. **RTC surface distribution** — new `references/rtc-surface-distribution.md` added (by user), engagement-analysis.md updated to require surface tagging of RTCs.

**Slack API detail fixes:**
8. **Example timestamps corrected** — were 2025 (off by one year), now verified 2026.
9. **`inclusive: true` documented** — prevents missing boundary messages.
10. **Pagination pattern documented** — cursor pass-back explained.
11. **Permalink fallback** — findings no longer dropped on permalink failure; falls back to `#channel @ ts`.
12. **STOP EARLY threshold** — changed from "first 🔴" to "3+ 🔴".

**Cross-file consistency:**
13. **SKILL.md Phase 0 surface names fixed** — matched to data-tables.md valid values.
14. **SKILL.md file index updated** — added rtc-surface-distribution.md.
15. **report-template.md by_rtc** — added surface tag requirement.
16. **ARCHITECTURE.md file tree** — added rtc-surface-distribution.md.
17. **ARCHITECTURE.md test step** — fixed stale search_messages reference.

### V2.1 Improvements (2026-03-16)

Data window redesign, cross-file consistency cleanup, and developer ergonomics.

**Critical fixes (would have caused incorrect analysis):**
1. **Baseline variance data window fixed** — changed from requiring 28 weeks (196 days, physically impossible given ~100-day retention) to defaulting to 12 weeks with graceful fallback; agent must state sample count used
2. **Holdout query window fixed** — changed from 8 days (couldn't compute MoM) to layered fetching: 10-day core + up to 12 WoW + 3 MoM discrete dates
3. **Engagement query window restructured** — layered fetching: 45-day core + YoY window + up to 6 additional same-day-of-week pairs for baseline variance via `dt IN (...)`

**Data documentation:**
4. **Data Availability Constraints** — new section in data-tables.md documenting execution_dt 60-day retention, ~45-day dt coverage per execution, ~100-day max lookback, and how investigating older dates reduces the available window
5. **Holdout quarterly reset** — documented that holdout experiments start in the first few days of each quarter, limiting early-quarter data availability
6. **Holdout analysis priorities** — defined explicit priority order: 10-day trend (primary) > WoW (up to 12) > MoM (up to 3)

**Dead logic and consistency cleanup:**
7. **Phase 0 dead logic removed** — WoW/MoM/YoY comparison date computation was never passed to subagents; deleted
8. **Instruction File Index fixed** — "Phase 1/2/3" renamed to "Subagent A/B/C" to match actual parallel dispatch
9. **WoW formula disambiguated** — changed from natural language to `value[D] − value[D−7]` notation
10. **principles.md synced** — updated baseline variance from "trailing 28" to "12 weeks" to match engagement-analysis.md

**Report and template improvements:**
11. **Data Coverage table added** — new section in report-template.md showing actual date ranges used and gaps per data source (engagement, holdout, Slack)
12. **Internal file reference removed** — driver classification definition inlined in report-template.md instead of referencing `prompts/engagement-analysis.md`

**Operational file cleanup:**
13. **MCP_SETUP.md: stale verification step removed** — deleted "Spawn a Task agent" subagent inheritance check (bug fixed in v2.1.30, documented in History)
14. **ARCHITECTURE.md: file dependency corrected** — report-template.md no longer depends on engagement-analysis.md
15. **Data Availability Constraints scoped** — explicitly stated constraints apply to all tables (engagement, breakdown, freshness, shopping, holdout)

### V2 Improvements (2026-03-13)

Key changes from the initial skill build:

1. **Slack tool preference fixed** — `search_messages` preferred over `get_channel_history` *(Note: search_messages later confirmed non-existent; reverted in V2.2)*
2. **Column name mapping** — main table ↔ breakdown table mapping in data-tables.md
3. **Engagement rate formulas** — all derived rate formulas documented
4. **Content mix analysis** — Step 5b: freshness/shopping engagement rates
5. **Baseline variance** — Principle 4 operationalized with z-score computation
6. **Enhanced synthesis** — holdout divergence × dimensional isolation cross-correlation
7. **MCP error handling** — connection errors, empty results, troubleshooting
8. **Holdout trend detection** — widening/narrowing: slope > 0.3%/day over 5+ days
9. **MODE 3 checklists** — specific info requirements per follow-up type

### MCP Session Issue (Resolved in Claude Code v2.1.30+)

In earlier versions of Claude Code, subagents spawned via the `Agent` tool ran as independent child processes that did not inherit MCP server sessions. Both Presto and Slack MCP servers require valid HTTP session IDs, so subagent MCP calls failed with `"Bad Request: No valid session ID provided"`.

**Claude Code v2.1.30** fixed this. Subagents now inherit MCP tools from the parent session. Verified on Claude Code v2.1.75 (2026-03-13).

### V1 (Helix) vs V2 (Claude Code)

PInvestigator was migrated from a monolithic 900-line Helix system prompt (`v005.md`) to a decomposed Claude Code skill.

| Aspect | V1 (Helix) | V2 (Claude Code) |
|--------|-----------|-------------------|
| Prompt | Single 900-line monolith | 8 focused files (~100-200 lines each) |
| Execution | Sequential, single agent | 3 parallel subagents |
| Data access | MCP via Helix platform | MCP via Claude Code (localhost:9092) |
| Iteration | Edit one massive file | Edit individual subagent/reference files |
| Slack search | MODE 2 only (follow-up) | MODE 1 (proactive) + MODE 2 (targeted) |
| Holdout analysis | Step 5 gating in monolith | Dedicated subagent with explicit trend detection |

Historical Helix system prompts (v000–v005) are archived in `tools/homefeed/pinvestigator/system_prompts/`.
