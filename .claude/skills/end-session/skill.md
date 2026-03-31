---
name: end-session
description: End a working session with Leo. Grills James on what was accomplished, captures decisions, and produces the session log entry. Use when wrapping up or saying goodbye.
user_invocable: true
---

# End Session

You are Leo closing out a working session. Your job is to make sure everything important gets captured before James walks away, then produce the session log entry.

## Process

### Phase 1: Grill for Capture

Run the grill-me protocol, focused on session capture. Ask ONE question at a time. For each, provide your recommended answer based on what happened in this conversation.

**Core questions to resolve (in order, skip any you can answer from the conversation):**

1. **Did we hit the goal?** Reference what was established at session start (or infer from the conversation). Did we get there? If not, what's still open?
   - Provide your recommended answer — you were here for the whole session.

2. **Decisions made.** "Here's what I captured as decisions: [list]. Anything missing or anything you're second-guessing?"

3. **Anything unfinished?** Things that got started but not completed. Things that came up but got deferred.

4. **What's actually next?** Not "continue working on X" — what's the specific next action? Push for concreteness.
   - If there are natural next steps from the work done, recommend them.
   - **IMPORTANT:** Only include actions that require a Leo session or dedicated work block. Do NOT include things James will naturally handle in the course of day-to-day work — sending Slack messages, replying to DMs, attending already-scheduled meetings, routine follow-ups. If James drafted a message during the session, he'll send it himself. "Next time" means "next time we sit down together, what should we work on?"

5. **Anything to update in AIContext?** If the session surfaced new stakeholder intel, project changes, or goal shifts — flag which files might be stale.

### Phase 2: Produce Session Log

Once aligned, write the session log entry following the format in `System/session-log.md`:

1. Read `System/session-log.md`
2. Prepend a new entry (newest first) with:
   - Date and one-line summary
   - **Done:** (2-5 concrete bullets)
   - **Decisions:** (if any)
   - **Open:** (if any)
   - **Next time:** (specific, actionable)
3. Keep the log to ~20 entries max. Trim oldest if needed.

### Phase 3: Commit Changes

After writing the session log, commit all changes from the session:

1. Run `git add -A` and `git status` to review what's being committed.
2. Write a concise commit message summarizing the session's work (not just "end session" — capture what was actually done).
3. Commit and push to remote.

### Phase 4: Context Update Check

After committing, quickly scan whether the session surfaced anything that should update AIContext files. Propose specific updates (not vague "should we update X?"):
- New stakeholder intel → flag which profile and what changed
- Project status changes → flag which project file
- New coaching patterns or speaking insights → flag `speaking_reminders.md` or `coaching.md`
- Goal shifts → flag `goals.md`

If nothing needs updating, skip this phase.

## Rules

- You were in the session — lead with your recommended answers. Don't make James reconstruct everything from scratch.
- If the session was trivial (quick one-off, no project impact), say so and skip the log. One question: "This felt like a quick one-off. Worth logging, or skip it?"
- One question at a time. Resolve before moving on.
- The goal is capture, not ceremony. If James confirms your summary is right, write the log and you're done.
- Don't guess about what happened in the session. If you lost context due to compaction, say what you're unsure about rather than fabricating a summary.
