# work-leo Setup Guide

One-time setup for Claude Code on James's work laptop.

## 1. Directory Structure

Create the base directory (rename your existing code folder or create new):

```bash
mkdir -p ~/leo-work/context/people
mkdir -p ~/leo-work/context/projects
mkdir -p ~/leo-work/context/org
mkdir -p ~/leo-work/system
```

## 2. Place CLAUDE.md

Copy `CLAUDE.md` from this folder to `~/leo-work/CLAUDE.md`.

## 3. Place work-only goals

Copy `goals.md` from this folder to `~/leo-work/context/goals.md`.

## 4. Copy context files from Leo

These are one-time copies. After setup, work-leo is its own source of truth.

### People (copy all)
```
work+self/people/stakeholders.md     -> ~/leo-work/context/people/stakeholders.md
work+self/people/direct_manager.md   -> ~/leo-work/context/people/direct_manager.md
work+self/people/dylan_1on1_log.md   -> ~/leo-work/context/people/dylan_1on1_log.md
work+self/people/team_members.md     -> ~/leo-work/context/people/team_members.md
```

### Projects (copy all)
```
work+self/projects/pinsight.md                    -> ~/leo-work/context/projects/pinsight.md
work+self/projects/pinvestigator.md               -> ~/leo-work/context/projects/pinvestigator.md
work+self/projects/clr_technical.md               -> ~/leo-work/context/projects/clr_technical.md
work+self/projects/p2p_lr_technical.md            -> ~/leo-work/context/projects/p2p_lr_technical.md
work+self/projects/l1_utility.md                  -> ~/leo-work/context/projects/l1_utility.md
work+self/projects/retentive_recs.md              -> ~/leo-work/context/projects/retentive_recs.md
work+self/projects/upp_must_win_march2026.md      -> ~/leo-work/context/projects/upp_must_win_march2026.md
work+self/projects/learned_dynamic_triggering_elt.md -> ~/leo-work/context/projects/learned_dynamic_triggering_elt.md
```

### Org
```
work+self/org/organization.md  -> ~/leo-work/context/org/organization.md
```

### Communication (direct copy, no changes needed)
```
work+self/communication.md  -> ~/leo-work/context/communication.md
```

### Goals (use the work-only fork, NOT Leo's version)
```
work-leo/goals.md  -> ~/leo-work/context/goals.md
```

## 5. Clone repos

```bash
cd ~/leo-work
git clone <pinboard-repo-url> Pinboard
git clone <optimus-repo-url> Optimus
```

## 6. Initialize session log

Create an empty session log:

```bash
echo "# Session Log" > ~/leo-work/system/session-log.md
echo "" >> ~/leo-work/system/session-log.md
```

## 7. Initialize git (optional)

If you want version control on the context files:

```bash
cd ~/leo-work
git init
# Add context/ system/ CLAUDE.md to git
# Keep Pinboard/ and Optimus/ as separate repos (don't nest)
```

Or use a `.gitignore` to exclude the cloned repos:

```
Pinboard/
Optimus/
```

## 8. NOT included (stays in Leo only)

- `coaching.md` — personal coaching sessions
- `journals_and_growth.md` — personal growth reflections
- `sideprojects/` — Rekko, etc.
- `learning/articles/` — ingested article library
- `notebooklm/` — no external API access on work laptop
- Goal 0 (inner foundation) — personal growth goal
- Bet C (inner resilience) — personal development bet

## 9. What's different from Leo

| Capability | Leo | work-leo |
|-----------|-----|----------|
| NotebookLM | Yes (4 notebooks) | No (no external APIs) |
| Coach supplement | Yes | No |
| Personal growth tracking | Yes | No |
| Codebase navigation | No | Yes (Pinboard + Optimus) |
| AI project building | Partial (skills/scripts) | Yes (in-repo development) |
| Session log | Yes | Yes (independent) |
| Memory system | Yes | Yes (independent) |
| Internal MCP servers | No | Yes (Pinterest internal) |
