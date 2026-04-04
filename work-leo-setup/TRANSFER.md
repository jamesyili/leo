# work-leo Transfer Guide

Porting new Leo capabilities to an already-deployed work-leo instance.
Created: 2026-04-04

## What to Transfer

### Agents (`.claude/agents/`)

Copy these directly to `~/leo-work/.claude/agents/`:

| File | Copy? | Notes |
|------|-------|-------|
| `karen.md` | YES | No external deps. Challenges blind spots on work decisions. |
| `code-planner.md` | YES | Generic implementation architect. Great for Pinvestigator/Pinsight. |
| `consult.md` | NO | Depends on NotebookLM — no external APIs on work laptop. |

```bash
mkdir -p ~/leo-work/.claude/agents
scp james@home:~/src/leo/.claude/agents/karen.md ~/leo-work/.claude/agents/
scp james@home:~/src/leo/.claude/agents/code-planner.md ~/leo-work/.claude/agents/
```

### Skills (`.claude/skills/`)

Copy entire skill directories to `~/leo-work/.claude/skills/`:

| Skill | Copy? | Notes |
|-------|-------|-------|
| `start-session` | YES | Updated for individual session log files |
| `end-session` | YES | Updated for session-logs/ dir + memory extraction |
| `session-log` | YES | Updated for new structure |
| `pulse` | YES | No external deps |
| `prep` | YES | Reads stakeholder profiles — works with context/people/ |
| `draft-email` | YES | Audience-calibrated drafting |
| `thinking-partner` | YES | Generic |
| `grill-me` | YES | Generic |
| `context-update` | YES | Works with any context file structure |
| `debrief` | YES | Generic session debrief |
| `coach-check` | NO | Depends on coaching.md (excluded from work-leo) |
| `consult-notebook` | NO | Depends on NotebookLM |
| `weekly-review` | NO | Depends on journals/coaching files |
| `ingest` | NO | Article library stays on Leo |
| `search` | NO | Article library stays on Leo |

```bash
mkdir -p ~/leo-work/.claude/skills
for skill in start-session end-session session-log pulse prep draft-email thinking-partner grill-me context-update debrief; do
  scp -r james@home:~/src/leo/.claude/skills/$skill ~/leo-work/.claude/skills/
done
```

### Hooks (`scripts/hooks/`)

All 4 hooks are generic but have **hardcoded paths** that need updating.

```bash
mkdir -p ~/leo-work/scripts/hooks
scp james@home:~/src/leo/scripts/hooks/*.sh ~/leo-work/scripts/hooks/
```

**After copying, update paths in each file:**

| File | Change | From | To |
|------|--------|------|----|
| `session-start.sh` | `SESSION_DIR` | `/home/james/src/leo/system/session-logs` | `$HOME/leo-work/system/session-logs` |
| `pre-compact.sh` | `COMPACT_LOG` | `/home/james/src/leo/system/compaction-log.md` | `$HOME/leo-work/system/compaction-log.md` |
| `detect-corrections.sh` | `PROJECT_DIR` | `$HOME/.claude/projects/-home-james-src-leo` | Update to work-leo's project hash |
| `detect-corrections.sh` | `MEMORY_DIR` | `$HOME/.claude/projects/-home-james-src-leo/memory` | Update to work-leo's project hash |
| `suggest-compact.sh` | No changes needed | (uses /tmp, no hardcoded paths) | — |

To find work-leo's project hash: `ls ~/.claude/projects/ | grep leo-work`

### Settings (`.claude/settings.local.json`)

Create or update `~/leo-work/.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(~/leo-work/scripts/hooks/session-start.sh)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/leo-work/scripts/hooks/session-start.sh"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/leo-work/scripts/hooks/pre-compact.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/leo-work/scripts/hooks/suggest-compact.sh"
          },
          {
            "type": "command",
            "command": "~/leo-work/scripts/hooks/detect-corrections.sh"
          }
        ]
      }
    ]
  }
}
```

### Session Log Migration

Migrate from single file to individual files:

```bash
mkdir -p ~/leo-work/system/session-logs

# If session-log.md has entries, you can either:
# 1. Keep the old file as a backup and start fresh with individual files
# 2. Split it manually into individual files (YYYY-MM-DD.md)

mv ~/leo-work/system/session-log.md ~/leo-work/system/session-log.md.bak
```

### CLAUDE.md Updates

The work-leo CLAUDE.md needs these additions:

1. **Subagent dispatch section** — Add Karen + Code Planner dispatch rules (copy from Leo's CLAUDE.md, remove Consult references)
2. **Session log restructure** — Update "Session Continuity" section to reference `system/session-logs/` instead of `system/session-log.md`
3. **Memory system** — Already mentioned but may need the same behavioral rules as Leo's

### Memory System

Create the memory directory if it doesn't exist:

```bash
# Find work-leo's project directory
PROJECT_HASH=$(ls ~/.claude/projects/ | grep leo-work)
mkdir -p ~/.claude/projects/$PROJECT_HASH/memory
echo "" > ~/.claude/projects/$PROJECT_HASH/memory/MEMORY.md
```

## What NOT to Transfer

- `consult.md` agent (NotebookLM dependency)
- `consult-notebook` skill (NotebookLM dependency)
- `coach-check` skill (no coaching.md on work-leo)
- `weekly-review` skill (no journals/coaching files)
- `ingest` / `search` skills (article library stays on Leo)
- `notebooklm/` directory
- `system/karen_observations.md` (Karen creates her own on work-leo)
- Leo-specific permissions in settings.local.json (curl commands, ingest/search skill copies)

## Post-Transfer Checklist

- [ ] Verify hooks fire: start a new session and confirm SessionStart loads session context
- [ ] Test Karen: she should fire at ~20% context window
- [ ] Test `/start-session` and `/end-session` with new session-logs/ structure
- [ ] Confirm memory system works: save a test memory, verify it persists
- [ ] Update work-leo CLAUDE.md with subagent dispatch + session log changes
