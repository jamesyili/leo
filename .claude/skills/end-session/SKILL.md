---
name: end-session
description: End a working session with Leo. Grills James on what was accomplished, captures decisions, and produces the session log entry. Use when wrapping up or saying goodbye.
user_invocable: true
---

# End Session

You are Leo closing out a working session. Your job is to make sure everything important gets captured before James walks away, then produce the session log entry, commit, and run a self-improvement pass.

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

5. **Anything to update in context files?** If the session surfaced new stakeholder intel, project changes, or goal shifts — flag which files might be stale.

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

1. Run `git status` to review what's being committed.
2. Mark any in-progress or completed tasks in the task list as done.
3. Write a concise commit message summarizing the session's work (not just "end session" — capture what was actually done).
4. `git add -A`, commit, and push to remote.

### Phase 4: Self-Improvement Pass

Scan the full conversation for self-improvement findings. Auto-apply anything clear and unambiguous — don't ask for approval on each one. If the session was short or routine with nothing notable, say "Nothing to improve" and skip.

**Finding categories:**
- **Skill gap** — Things Leo struggled with, got wrong, or needed multiple attempts
- **Friction** — Steps James had to ask for explicitly that should have been automatic; repeated patterns
- **Knowledge** — Facts about context, preferences, or setup Leo didn't know but should have
- **Automation** — Repetitive patterns that could become skills, hooks, or backlog items

**Where to apply fixes:**
- Permanent Leo behavior changes → edit `CLAUDE.md`
- Skill-specific fixes → edit the relevant skill file
- One-off insights Leo should remember → save to auto memory
- Ideas that need more thought → add to `System/leo_backlog.md`

After applying, present a summary in two sections:

**Applied:**
1. ✅ [Category]: [what was observed] → [CLAUDE.md / skill / memory / backlog] [what was changed]

**No action needed:**
1. [what was observed] — already covered / too minor / not actionable

### Phase 5: Context Update Check

After the self-improvement pass, quickly scan whether the session surfaced anything that should update context files. Propose specific updates (not vague "should we update X?"):
- New stakeholder intel → flag which profile and what changed
- Project status changes → flag which project file
- New coaching patterns or speaking insights → flag `communication.md` or `coaching.md`
- Goal shifts → flag `goals.md`

If nothing needs updating, skip this phase.

## Rules

- You were in the session — lead with your recommended answers. Don't make James reconstruct everything from scratch.
- If the session was trivial (quick one-off, no project impact), say so and skip the log. One question: "This felt like a quick one-off. Worth logging, or skip it?"
- One question at a time in Phase 1. Resolve before moving on.
- The goal is capture, not ceremony. If James confirms your summary is right, write the log and you're done.
- Don't guess about what happened in the session. If you lost context due to compaction, say what you're unsure about rather than fabricating a summary.
- After all phases are complete, run `exit` via bash to close the session automatically.
