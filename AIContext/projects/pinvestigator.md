# PINvestigator

LLM-powered metrics investigation tool for the Homefeed Relevance team.

## What It Does

Python Notebook launched during metric investigations. Built-in functions that:

1. **High-dimensional time-series analysis** — pulls all metrics (repins, closeups, etc.) with breakdowns (Discovery surface, fresh, shopping, etc.) and YoY/WoW/MoM patterns
2. **Metric similarity** — compares and finds closest metrics given a target metric of investigation
3. **Anomaly detection & visualization** — basic anomaly detection, cross-surface analysis
4. **Breakdowns** — by RTC, countries, platforms
5. **LLM digest** — digests all data points and suggests what to look for next
6. **Slack + internal systems integration** — checks relevant launch and/or incident timing
7. **Historical context** — loads past analyses, LLM digests all context and proposes next investigation steps

## Architecture: Thin Orchestrator + 3 Parallel Subagents

Built as a Claude Code skill (`agent-skills/pinvestigator/`).

```
SKILL.md (orchestrator, ~236 lines, auto-loaded)
  │
  ├── Phase 0:  Resolve TARGET_DATE + TARGET_METRIC
  ├── Phase 1:  Dispatch 3 subagents IN PARALLEL
  │   ├── Subagent A (engagement-analysis.md + data-tables.md) → 7 Presto tables
  │   ├── Subagent B (holdout-analysis.md + data-tables.md)    → 1 holdout table
  │   └── Subagent C (slack-search.md)                         → 4 Slack channels
  ├── Phase 1b: Validate subagent results (handle partial failures)
  ├── Phase 2:  Cross-correlate findings across A + B + C
  └── Phase 3:  Generate report (report-template.md)
```

## File Organization: 10 Files, 3 Categories

```
pinvestigator/
├── SKILL.md                    [AGENT PROMPT — auto-loaded]
├── ARCHITECTURE.md             [AGENT+HUMAN — read for dev context]
├── MCP_SETUP.md                [AGENT+HUMAN — read on MCP errors]
├── prompts/
│   ├── engagement-analysis.md  [AGENT PROMPT — Subagent A]
│   ├── holdout-analysis.md     [AGENT PROMPT — Subagent B]
│   └── slack-search.md         [AGENT PROMPT — Subagent C]
└── references/
    ├── data-tables.md          [AGENT REF — read by A and B]
    ├── principles.md           [HUMAN REF — not read at runtime]
    └── report-template.md      [AGENT REF — read in Phase 3]
```

Every file has an explicit role tag. At runtime, the agent reads only the files it needs for the current phase.

## Design Principles

1. **Minimal context loading** — SKILL.md (~236 lines) is the only file auto-loaded. Table schemas, SQL patterns, Slack channel lists load only when a subagent needs them. Each subagent loads ~290 lines total (its prompt + data-tables.md) vs. ~900 lines monolithic.

2. **Parallel subagents** — three independent data sources (engagement tables, holdout table, Slack) queried simultaneously. Wall-clock time drops from ~28 min sequential to ~20 min (bounded by engagement subagent). Orchestrator blocks until all three return.

3. **One subagent per data source** — clean ownership. Editing holdout-analysis.md can't regress engagement analysis. Each prompt testable in isolation. Failures contained (Slack MCP down → other two still produce valid results).

4. **Synthesis in orchestrator** — cross-correlation (holdout divergence + iOS isolation + Slack deploy on same date) requires all three outputs. Phase 2 runs after all subagents return. No subagent knows about the others.

5. **Shared reference files** — data-tables.md is single source of truth for table schemas, column names, valid values, query rules. Both Subagent A and B read it.

6. **Layered context loading** — developers modifying the skill read ARCHITECTURE.md. MCP errors trigger MCP_SETUP.md. Default context stays clean.

7. **Human reference files don't consume agent context** — principles.md (~400 lines, full examples) is for human investigators. Subagents use compact inline excerpts instead.

## Interview Positioning (March 2026)

PINvestigator is James's hands-on agentic AI case study — he's acting as tech lead, building it himself with Claude Code. This is complementary to the UPP case study (Director-scale oversight):

- **UPP**: Shows James operates at Director scale (oversight, architecture, cross-org stakeholder management)
- **PINvestigator**: Shows James can go deep and build (hands-on, novel agentic architecture, eval-driven)

Key differentiators for interviews:
1. **Parallel subagent architecture** — most candidates can't talk about building agent systems from scratch
2. **Eval harness** (Q2 focus) — demonstrates the "hard part" of agent engineering that separates real systems from demos
3. **Three-level evaluation**: black-box (report quality), glass-box (trajectory), white-box (per-step)
4. **Failure handling as architecture** — one subagent per data source means failures are contained, partial results are useful
