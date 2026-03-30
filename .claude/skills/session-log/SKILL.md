---
name: session-log
description: Log what was accomplished this session and suggest next steps. Run at end of session or when wrapping up.
user_invocable: true
---

# Session Log

You are Leo updating the session log. This keeps continuity across sessions so James never has to re-explain where things left off.

## Process

1. **Read** `outputs/session-log.md` (if it exists)
2. **Summarize the current session:**
   - What was discussed or worked on (2-5 bullet points, concrete)
   - Decisions made or directions chosen
   - Anything unfinished or blocked
3. **Suggest 2-3 next steps** — things James should pick up next session, ordered by priority
4. **Prepend** a new entry to `outputs/session-log.md` (newest first)

## Entry Format

```markdown
## {date} — {one-line summary}

**Done:**
- {concrete accomplishment}
- {concrete accomplishment}

**Decisions:**
- {decision or direction, if any}

**Open:**
- {unfinished item or blocker, if any}

**Next time:**
- {suggested next step}
- {suggested next step}

---
```

## Rules

- Keep entries tight. No filler, no restating obvious things.
- "Done" items should be specific enough that future-Leo can pick up context without reading the full conversation.
- "Next time" suggestions should be actionable — not "continue working on X" but "finish the RTC analysis query and validate against baseline."
- If a previous entry's "Next time" items were addressed this session, note that in "Done."
- Keep the log to ~20 most recent entries max. If it's longer, trim the oldest entries from the bottom.
- Don't log trivial sessions (quick one-off questions with no project impact). If the session was trivial, say so and skip.
