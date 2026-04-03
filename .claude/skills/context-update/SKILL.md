---
name: context-update
description: Guided update of context files when information changes. Proposes updates based on conversation, then probes for gaps. Triggered manually, at end-of-session, or proactively when context is rich.
user_invocable: true
---

# Context Update

Guided update of context files. I identify what's stale, propose changes, make the edits, and probe for gaps I might have missed.

## Triggers

1. **End-of-session** — runs automatically as part of `/end-session` after the session log is written.
2. **Manual** — James invokes `/context-update` directly after a context dump or when things have changed.
3. **Proactive** — I suggest it mid-session when the conversation has surfaced substantial new context (new stakeholder intel, project pivots, org changes, coaching insights) and I sense we might lose it to context compaction if we don't capture it now.

## Process

### Step 1: Load the Index

Read `system/file_index.md` to understand what files exist, what they cover, and when they were last updated.

### Step 2: Scan and Propose

Scan the current conversation for signals that context files are stale or missing information. Look for:

- **Stakeholder intel** — new people, changed relationships, trust shifts, political dynamics
- **Project status changes** — milestones hit, scope changes, new workstreams, blockers resolved
- **Org changes** — reorgs, new reports, role changes, reporting line shifts
- **Coaching/growth insights** — new patterns, tools, journal-worthy moments
- **Goal shifts** — priorities changed, new bets, goals achieved or deprioritized
- **Communication insights** — new audience playbooks, speaking patterns, feedback received
- **New files needed** — a new project, person, or domain that doesn't have a file yet

Present proposed updates as a concrete list:

```
**Proposed updates:**
1. `stakeholders.md` — Add profile for [person]: [one-line reason]
2. `pinsight.md` — Update M1 status: [what changed]
3. `goals.md` — [specific change]: [why]
4. NEW FILE: `projects/[name].md` — [why it's needed]
```

If nothing needs updating, say so and skip to Step 4.

### Step 3: Execute Updates

After James confirms (or adjusts), make the edits. Update `system/file_index.md` timestamps for any files touched.

### Step 4: Probe for Gaps

This is the part most update systems miss. Ask 2-3 targeted questions about context that *could* be useful but wasn't surfaced in the conversation:

- "You mentioned [person] — is there anything about their current situation that would be useful for me to know next time?"
- "The last time [file] was updated was [date]. Has anything shifted since then?"
- "[Topic] came up but we didn't go deep. Is there context there I should have?"
- "Is there anything happening this week — meetings, decisions, deadlines — that I should know about for next session?"

Don't ask generic questions. Ask specific ones based on what was discussed and what's in the index. If the conversation was thorough and I can't identify gaps, say so and skip.

### Step 5: Capture Gap Responses

If James shares new context from the probing questions, update the relevant files immediately. Update index timestamps.

## Rules

- **Be specific.** "Update stakeholders.md" is useless. "Add Kartik profile to stakeholders.md — Chief Architect, CTO direct report, publicly supportive of James's work" is useful.
- **Don't propose updates for things that were already updated during the session.** Check what was actually edited before proposing.
- **Keep it fast.** This isn't a full audit. It's a targeted sweep based on what happened in the conversation.
- **When running at end-of-session:** Keep it tight. James is wrapping up. Propose, confirm, execute. Save the deep probing for manual invocations.
- **When proactively suggesting mid-session:** Be brief. "We've covered a lot of ground on [topic] — want me to run a quick context update before we move on?" One sentence, not a pitch.
- **New files:** Only propose a new file if there's enough substance to justify it. A one-paragraph note can go in an existing file.
- **Index maintenance:** Always update `system/file_index.md` timestamps when editing files. If a new file is created, add it to the index.
