---
title: Pinsight M1 — HF Request Debugger
date: 2026-04-04
status: ready-for-implementation
goal: Given an employee user ID + time range, fetch their Homefeed request, let the human identify problematic pins, then diagnose why those pins were shown using funnel data and LLM reasoning.
constraints: Claude Code skill on work-leo (~/leo-work/), Presto MCP for data access, single-agent sequential flow, ~10 hours build time, must be demoable to Jeff and Dylan.
---

# Pinsight M1 — HF Request Debugger Implementation Spec

## Overview

Pinsight M1 is a Claude Code skill that answers "Why was this pin shown to me?" for Pinterest Homefeed. Given an employee's user ID and a date/time range, it queries the `bi.core_daily_homefeed_backend_funnel_candidate_evaluation` table, presents the final-chunk pins to a human for selection, then performs deep analysis on selected pins — tracing their CG source, scores, and ranking signals. It produces a markdown report with per-pin traces and an LLM-synthesized diagnosis, and writes a structured trace to a local SQLite database for systematic eval/improvement.

This is a separate skill from PINvestigator. They share the same MCP setup (Presto on localhost:9092) but have different use cases: PINvestigator investigates metric anomalies; Pinsight debugs individual requests.

## Folder Structure

```
~/leo-work/pinboard/agent-skills/pinsight/
├── SKILL.md                          # Agent prompt — auto-loaded when skill is invoked
├── MCP_SETUP.md                      # Reference to ../pinvestigator/MCP_SETUP.md
├── references/
│   └── data-tables.md                # Schema for bi.core_daily_homefeed_backend_funnel_candidate_evaluation
├── output/                           # Generated reports (git-ignored)
│   └── {dt}_{user_id}.md
└── traces/
    ├── db.py                         # SQLite helper script
    └── pinsight_traces.db            # SQLite database for session traces (git-ignored)
```

## Data Model

### Source Table

**`bi.core_daily_homefeed_backend_funnel_candidate_evaluation`**

Flattened table. One row per candidate at its furthest stage. Daily `dt` partition. 100% employee requests, 1% public.

**Primary key (logical):** `request_id + candidate_source + candidate_furthest_stage + candidate_pin_id`

#### Request-level columns

| Column | Type | Description |
|--------|------|-------------|
| `dt` | string | Partition date (YYYY-MM-DD) |
| `request_id` | string | Unique request identifier |
| `user_id` | bigint | Pinterest user ID |
| `user_country` | string | User country code |
| `request_timestamp` | timestamp | When the request was made |
| `request_params` | map<string,string> | Request parameters |
| `homefeed_tab` | string | Which homefeed tab (e.g., "FOR_YOU") |
| `sizer_values` | map<string,double> | Sizer configuration values |
| `resource_signals` | map<string,string> | Resource-level signals |

#### Candidate-level columns

| Column | Type | Description |
|--------|------|-------------|
| `candidate_pin_id` | bigint | Pin ID |
| `candidate_pin_image_signature` | string | Image signature for pin lookup |
| `candidate_source` | string | CG source attribution (e.g., "PINNABILITY_PROD") |
| `candidate_content_type` | string | Content type (e.g., "image", "video") |
| `candidate_furthest_stage` | string | Furthest funnel stage this candidate reached |
| `candidate_drop_stage` | string | Stage where candidate was dropped (NULL if served) |
| `candidate_drop_reason` | string | Why candidate was dropped (NULL if served) |

#### Scoring columns

| Column | Type | Description |
|--------|------|-------------|
| `candidate_lws_scores` | map<string,double> | Per-head LWS (lightweight scoring) scores |
| `candidate_lws_score_aggregate` | double | Aggregated LWS score |
| `candidate_lws_rank` | int | Rank after LWS |
| `candidate_l1_utility_score` | double | L1 utility score |
| `candidate_ranking_scores` | map<string,double> | Per-head ranking scores |
| `candidate_ranking_score_aggregate` | double | Aggregated ranking score |
| `candidate_ranking_rank` | int | Rank after full ranking |
| `candidate_ssd_score` | double | SSD (same-source diversity) score |
| `candidate_presorting_utility` | double | Pre-sorting utility score |

#### Output columns

| Column | Type | Description |
|--------|------|-------------|
| `candidate_final_position` | int | Final position in served feed (NULL if not served) |

### SQLite Trace Schema

**File:** `~/leo-work/pinboard/agent-skills/pinsight/traces/pinsight_traces.db`

```sql
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    dt TEXT NOT NULL,
    request_id TEXT,
    num_requests INTEGER,
    num_final_chunk_pins INTEGER,
    num_selected_pins INTEGER,
    selected_pin_ids TEXT,              -- JSON array
    started_at TEXT NOT NULL,           -- ISO 8601
    completed_at TEXT,
    report_path TEXT,
    outcome TEXT                        -- success, error, abandoned
);

CREATE TABLE IF NOT EXISTS phases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    phase INTEGER NOT NULL,
    phase_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,               -- success, error, skipped
    error_message TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    phase INTEGER NOT NULL,
    sql_text TEXT NOT NULL,
    row_count INTEGER,
    execution_time_ms INTEGER,
    error TEXT,
    executed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pin_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    pin_id INTEGER NOT NULL,
    candidate_source TEXT,
    candidate_content_type TEXT,
    candidate_furthest_stage TEXT,
    candidate_drop_stage TEXT,
    candidate_drop_reason TEXT,
    lws_score_aggregate REAL,
    lws_rank INTEGER,
    l1_utility_score REAL,
    ranking_score_aggregate REAL,
    ranking_rank INTEGER,
    ssd_score REAL,
    presorting_utility REAL,
    final_position INTEGER,
    lws_scores_json TEXT,               -- JSON serialization of map
    ranking_scores_json TEXT,           -- JSON serialization of map
    diagnosis TEXT                       -- LLM-generated per-pin diagnosis
);

CREATE TABLE IF NOT EXISTS diagnosis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    cg_distribution_json TEXT,
    score_pattern_summary TEXT,
    content_type_summary TEXT,
    overall_diagnosis TEXT,
    key_findings TEXT                   -- JSON array
);
```

## Tasks

### T-1: Scaffold Skill Directory

**Description:** Create the Pinsight skill directory structure, SKILL.md stub, and reference files.

**Files:**
- `pinboard/agent-skills/pinsight/SKILL.md`
- `pinboard/agent-skills/pinsight/references/data-tables.md`
- `pinboard/agent-skills/pinsight/MCP_SETUP.md`
- `pinboard/agent-skills/pinsight/.gitignore`

**Acceptance criteria:**
- [ ] Directory structure matches folder structure above
- [ ] `.gitignore` excludes `output/` and `traces/*.db`
- [ ] `MCP_SETUP.md` references PINvestigator's MCP_SETUP.md for Presto config
- [ ] `references/data-tables.md` contains the full schema + query rules

**Dependencies:** None

**Implementation notes:**

`.gitignore`:
```
output/
traces/*.db
```

`references/data-tables.md` query rules:
1. Always filter on `dt` (string, format 'YYYY-MM-DD') — NOT `DATE 'YYYY-MM-DD'`
2. Always filter on `user_id` (bigint)
3. Use `candidate_furthest_stage = 'FINAL_CHUNK'` to get served pins
4. Map columns queried with bracket notation: `candidate_lws_scores['repin']`
5. Do NOT use DESCRIBE, SHOW, DDL, or UNION
6. Discover map keys dynamically from a sample row before using them

---

### T-2: SQLite Trace Database Script

**Description:** Create the Python helper that initializes the SQLite DB and provides write functions.

**Files:**
- `pinboard/agent-skills/pinsight/traces/db.py`

**Acceptance criteria:**
- [ ] `python3 db.py init` creates the SQLite database with all tables (idempotent)
- [ ] Exposes: `create_session()`, `log_phase()`, `log_query()`, `log_pin_analysis()`, `log_diagnosis()`, `complete_session()`
- [ ] `create_session` generates UUID, returns it
- [ ] DB path resolved relative to script directory (not cwd)
- [ ] All functions accept keyword arguments matching schema columns

**Dependencies:** None

**Implementation notes:**

```python
#!/usr/bin/env python3
"""Pinsight trace database utilities."""

import sqlite3, uuid, json, os
from datetime import datetime, timezone

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "pinsight_traces.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""...""")  # All CREATE TABLE IF NOT EXISTS from schema
    conn.close()

def create_session(user_id: int, dt: str, **kwargs) -> str:
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn = get_connection()
    conn.execute("INSERT INTO sessions (session_id, user_id, dt, started_at) VALUES (?, ?, ?, ?)",
                 (session_id, user_id, dt, now))
    conn.commit(); conn.close()
    return session_id

def log_phase(session_id, phase, phase_name, status, **kwargs): ...
def log_query(session_id, phase, sql_text, **kwargs): ...
def log_pin_analysis(session_id, pin_id, **kwargs): ...
def log_diagnosis(session_id, **kwargs): ...
def complete_session(session_id, outcome, **kwargs): ...

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        init_db()
        print(f"Database initialized at {DB_PATH}")
```

Agent calls via Bash: `python3 -c "import sys; sys.path.insert(0, '{SKILL_DIR}/traces'); from db import create_session; print(create_session(user_id=12345, dt='2026-04-01'))"`

---

### T-3: SKILL.md — Main Agent Prompt

**Description:** Write the full SKILL.md orchestrator implementing all 6 phases.

**Files:**
- `pinboard/agent-skills/pinsight/SKILL.md`

**Acceptance criteria:**
- [ ] Frontmatter: `name: pinsight`, description matches M1 use case
- [ ] Defines `SKILL_DIR` path
- [ ] Implements Phases 0-5 sequentially
- [ ] Phase 1 output: compact markdown table (pin_id, source, content_type, ranking_score, position)
- [ ] Phase 2: explicit PAUSE — agent MUST stop and wait for human input
- [ ] Phase 3: exact queries for comparative analysis specified
- [ ] Phase 4: structured LLM diagnosis (CG source, score drivers, unusual signals, hypothesis)
- [ ] Phase 5: report output + SQLite trace
- [ ] MCP error handling included
- [ ] Common mistakes section included

**Dependencies:** T-1, T-2

**Implementation notes:**

#### Phase 0: Resolve User + Time Range
- Required: `USER_ID` (bigint) + `DT` (string YYYY-MM-DD)
- Validation query: count distinct request_ids for user/date
- 0 results → report no data
- Multiple requests → present table (request_id, timestamp, num_pins), ask user to choose
- Single request → auto-select
- Init SQLite session

#### Phase 1: Fetch and Present FINAL_CHUNK Pins
```sql
SELECT candidate_pin_id, candidate_source, candidate_content_type,
       candidate_ranking_score_aggregate, candidate_final_position
FROM bi.core_daily_homefeed_backend_funnel_candidate_evaluation
WHERE dt = '{DT}' AND user_id = {USER_ID} AND request_id = '{REQUEST_ID}'
  AND candidate_furthest_stage = 'FINAL_CHUNK'
ORDER BY candidate_final_position ASC
```
Present as numbered markdown table. If >75 pins, show first 40 + last 10 with truncation notice.

#### Phase 2: PAUSE
**CRITICAL: STOP. Do NOT proceed until human responds with pin selection.**
Accept: row numbers ("3, 7, 15") or pin_ids (large numbers).

#### Phase 3: Deep Analysis
- **3a:** Full data pull for selected pins (all columns + map columns)
- **3b:** Comparative context — aggregate stats for ALL FINAL_CHUNK pins:
  - CG distribution: `GROUP BY candidate_source` → count, avg scores
  - Content type distribution: `GROUP BY candidate_content_type`
  - Score percentiles: `APPROX_PERCENTILE(..., ARRAY[0.25, 0.5, 0.75, 0.9])`
- **3c:** Pattern analysis:
  1. CG concentration — are selected pins all from one source?
  2. Score anomalies — above/below median/75th percentile?
  3. Multihead drivers — which heads are unusually high? (discover keys dynamically)
  4. Content type concentration vs distribution
  5. Position vs score — any SSD reranking effects?

Multihead analysis requires discovering map keys first:
```sql
SELECT candidate_lws_scores, candidate_ranking_scores
FROM bi.core_daily_homefeed_backend_funnel_candidate_evaluation
WHERE dt = '{DT}' AND user_id = {USER_ID} AND request_id = '{REQUEST_ID}'
  AND candidate_furthest_stage = 'FINAL_CHUNK'
LIMIT 1
```
Then build per-head median queries dynamically.

#### Phase 4: LLM Diagnosis
Structured output:
1. **CG Source Analysis** — what generated these pins and why
2. **Score Drivers** — which multihead scores pushed them to the top
3. **Unusual Signals** — anything anomalous
4. **Hypothesis** — 2-3 sentence plain-language explanation (non-technical audience)

#### Phase 5: Report + Trace
- Report format: per-pin traces first → diagnosis → request context → CG distribution → raw data appendix
- Save to `{SKILL_DIR}/output/{DT}_{USER_ID}.md` (numeric suffix if exists)
- Complete SQLite session, write pin_analyses and diagnosis rows

---

### T-4: Smoke Test

**Description:** Run end-to-end with a known employee user ID and date.

**Acceptance criteria:**
- [ ] Phase 0 resolves user/date, finds request(s)
- [ ] Phase 1 presents pin table correctly
- [ ] Phase 2 pauses and waits
- [ ] Phase 3 queries succeed, computes comparisons
- [ ] Phase 4 produces coherent diagnosis
- [ ] Report written to `output/`
- [ ] Trace queryable: `sqlite3 traces/pinsight_traces.db "SELECT * FROM sessions"`
- [ ] Total wall-clock < 5 minutes for 3-5 pins

**Dependencies:** T-3

---

### T-5: Context File Updates

**Description:** Update pinsight.md with M1 built status and skill pointer.

**Files:**
- `~/leo-work/context/projects/pinsight.md`

**Acceptance criteria:**
- [ ] M1 status = "built", pointer to `pinboard/agent-skills/pinsight/`
- [ ] Note SQLite trace system

**Dependencies:** T-4

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|------------------|
| No data for user/date | Phase 0 reports "no data found", suggests checking employee status |
| >10 requests on the date | Phase 0 shows all sorted by time, asks user to pick |
| >100 FINAL_CHUNK pins | Phase 1 shows first 40 + last 10 with truncation notice |
| <3 FINAL_CHUNK pins | Show all, ask user to select from what's available |
| User selects invalid pin IDs | Report which IDs weren't found, ask to re-select |
| Map columns are NULL | Show "N/A" in report, note the gap |
| Presto connection fails | Log error, report what was collected, suggest retry |
| SQLite write fails | Log to console, continue with report — tracing is best-effort |
| `dt` filtered with DATE literal | 0 rows — data-tables.md warns about this |
| User provides pin_id instead of row number | Handle both — match against pin_id if input is large numbers |

## Testing Plan

| Test | Type | What it validates |
|------|------|------------------|
| SQLite init idempotency | Unit | `db.py init` twice without error |
| SQLite write/read round-trip | Unit | All tables writable and readable |
| Phase 0 validation query | Integration | Presto returns expected schema for known user |
| Phase 1 pin table formatting | Integration | Sorted, correct columns, truncation works |
| Phase 2 pause enforcement | Manual | Agent stops after Phase 1 |
| Phase 3 map key discovery | Integration | Discovers keys, builds per-head queries |
| Full end-to-end (T-4) | E2E | Complete flow: invocation → report + trace |
| Trace queryability | Integration | `sqlite3` queries return structured data |

## Out of Scope

- **VLM-powered pin identification** — backlog. M1 requires human pin selection.
- **Reverse trace ("why NOT shown")** — forward trace only in M1.
- **Request-level summary view** — M1 is pin-level analysis first.
- **Multi-agent parallel analysis** — single-agent sequential for M1.
- **candidate_batch_id** — excluded from table schema.
- **Scale analysis (M3)** — running Pinsight across many users.
- **User understanding (M2)** — VLM-powered interest profiling.
- **Cross-request analysis** — comparing same pin across requests.
- **Automatic anomaly detection** — human identifies problematic pins.
- **Dashboard / web UI** — markdown + SQLite, no frontend.

## Backlog (Future Capabilities)

- VLM-powered pin identification from screenshots/video (high-priority backlog)
- Reverse trace: "Why am I NOT seeing X?"
- Request-level summary before pin drill-down
- Multi-agent parallel analysis for performance
- Automatic anomaly detection in served pins
- Cross-request analysis (same user, different times)
- Integration with PINvestigator for metric→request drill-down
