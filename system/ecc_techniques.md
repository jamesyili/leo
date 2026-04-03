# Techniques from everything-claude-code

> Source: https://github.com/affaan-m/everything-claude-code
> Extracted: 2026-04-03
> Status: Research log. Items marked with priority will be built; others are reference.

---

## 1. Automatic Session Persistence via Hooks [PRIORITY — BUILD FIRST]

**What:** Use Claude Code hooks to automatically persist and reload session context, eliminating reliance on manual `/start-session` and `/end-session` invocation.

**How it works in ECC:**
- `SessionStart` hook: On every new session, auto-loads the most recent session summary. Matches sessions to the current project by checking worktree/project fields, falls back to most-recent.
- `Stop` hook: Runs after every Claude response. Parses the JSONL transcript to extract user messages, tools used, and files modified. Writes/updates a session summary file.
- Together, these create a rolling breadcrumb trail that survives session boundaries.

**How to adapt for Leo:**
- `SessionStart` hook: Auto-read `system/session-log.md` and inject the last entry's "Open" and "Next time" items into context. Could also auto-read `work+self/goals.md` for orientation.
- `Stop` hook: Lightweight breadcrumb capture after each response — not full session logging (that's still `/end-session`'s job), but enough to recover context if the session dies unexpectedly.
- Keep `/start-session` and `/end-session` as the high-quality semantic layer. Hooks are the safety net.

**Tradeoff:** Hook-based persistence is mechanical (transcript parsing). Leo's skill-based approach is semantic (grilling James for decisions, open items). We should do both.

---

## 2. PreCompact Hook — Catch Invisible Context Loss [PRIORITY — BUILD FIRST]

**What:** Before Claude compacts context (which loses detail), hook fires to preserve key state.

**How it works in ECC:**
- `PreCompact` hook timestamps the compaction event in a log file
- Annotates the active session file with what was lost
- Creates a record of context compaction events

**How to adapt for Leo:**
- Write a checkpoint to a temp file: current session goals, active decisions, open threads
- After compaction, this checkpoint gets re-read to maintain continuity
- Aligns with existing backlog item "Mid-session process notes" — this is the automated version

---

## 3. The "Instinct" System for Self-Improvement [DESIGN LATER]

**What:** Instead of free-form backlog items, capture atomic learned behaviors ("instincts") with confidence scoring that strengthens over time.

**How it works in ECC:**
- Observation hooks capture every tool use (PreToolUse + PostToolUse) to JSONL
- Instincts start at confidence 0.3 (tentative), can reach 0.9 (near-certain)
- Confidence grows from: repeated observation, user corrections, error resolutions
- Project scoping: instincts tied to projects by git remote hash, promotable to global
- Evolution pipeline (`/evolve`): clustered instincts get promoted into full skills, commands, or agents
- 5-layer anti-recursion to prevent the observer from observing itself

**How to adapt for Leo:**
- Primary signal: **user corrections**. When James says "no, not like that" or "stop doing X," that's the strongest instinct trigger.
- Secondary signal: **confirmed approaches**. When James says "yes, exactly" or accepts a non-obvious choice.
- These already map to the memory system's `feedback` type — the instinct model adds structure (confidence scores, triggers, evidence count) on top.
- Could evolve high-confidence instincts into CLAUDE.md operating principles or skill modifications.

**Key insight:** The memory system already captures corrections. The gap is: no confidence scoring, no clustering, no promotion pipeline. The instinct model is the memory system with a growth engine on top.

---

## 4. Strategic Compaction Suggestions [LOW EFFORT]

**What:** Track tool call count per session and suggest `/compact` at logical phase transitions rather than letting auto-compact fire at arbitrary points.

**How it works in ECC:**
- `suggest-compact.js` hook counts tool calls
- At ~50 tool calls, suggests manual `/compact`
- Philosophy: compact after exploration before execution, after completing a milestone before starting the next

**How to adapt for Leo:**
- A Stop hook that counts tool calls and emits a reminder at ~50
- Or simpler: just a note in CLAUDE.md about when to suggest compaction to James
- Low priority — useful but not transformative

---

## 5. Context Modes [DESIGN LATER]

**What:** Lightweight mode files that shift Claude's behavior without rewriting CLAUDE.md. Activated per-task.

**How it works in ECC:**
- `contexts/` directory with mode-specific files: dev.md, review.md, research.md
- Each sets posture/priorities for that mode
- Example: dev.md says "Write code first, explain after. Prefer working solutions over perfect."

**How to adapt for Leo:**
- Leo already has implicit modes (thinking partner, writer, coach, builder) defined in CLAUDE.md
- Could make these explicit as activatable context files: `system/modes/meeting-prep.md`, `system/modes/deep-work.md`, `system/modes/coaching.md`
- Each mode would specify: which context files to load, what tone to use, what to prioritize
- The Context Loading Guide table in CLAUDE.md is a static version of this — modes would make it dynamic

---

## 6. Hook Recipes Worth Considering [REFERENCE]

From ECC's hook library, these are relevant to Leo:

| Hook | Type | What it does | Leo relevance |
|------|------|-------------|---------------|
| Block files >800 lines | PreToolUse (Write) | Forces modular design | Could apply to context files — warn if they get too large |
| Config protection | PreToolUse (Write/Edit) | Blocks modifications to specific config files | Protect CLAUDE.md from accidental edits by hooks/agents |
| Batch format+typecheck at Stop | Stop | Accumulates edited files, runs checks once at end of response | Could batch context file validation |
| Desktop notifications | Stop | Notifies when Claude finishes a long task | Nice QoL if James walks away during long operations |

---

## 7. MCP Context Budget Warning [REFERENCE]

**Key finding:** Each MCP tool description consumes tokens from the context window. Too many MCPs can shrink effective context to ~70k (from 200k).

**Recommendation:** Keep under 10 MCPs enabled and under 80 tools active. Disable unused MCPs per-project.

**Leo relevance:** As we add more skills and tools, monitor context budget. Currently not a problem, but worth watching.

---

## 8. Layered CLAUDE.md Architecture [REFERENCE]

**How ECC structures it:**
- User-level (`~/.claude/CLAUDE.md`): Personal preferences, universal rules
- Project-level (project root `CLAUDE.md`): Project-specific stack, patterns, commands
- Rules directory (`~/.claude/rules/`): Broken into `common/` + language-specific dirs

**Leo already does this well.** Our CLAUDE.md is more sophisticated for a personal OS use case. The one pattern we're not using: **rules directory** — breaking operating principles into separate modular files. Could reduce CLAUDE.md size and make rules more maintainable.

---

## 9. Session File Matching [REFERENCE]

**What:** SessionStart hook doesn't just load the most recent session — it matches by worktree path first, then project name, then recency.

**Leo relevance:** Currently single-project (leo repo), so not needed. Would matter if Leo expanded to manage multiple repos/contexts.
