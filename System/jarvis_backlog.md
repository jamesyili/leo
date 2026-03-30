# Leo Improvement Backlog

> Running backlog of ideas, improvements, and experiments for making Leo better. Prioritize ruthlessly — not everything here needs to happen.

Last updated: 2026-03-29

---

## Rename: Jarvis → Leo

- [ ] **Complete rename across all remaining files** — CLAUDE.md and key skills updated. Remaining: scan all context files, memory files, and remaining skills for "Jarvis" references and update to "Leo". Low priority but should be cleaned up.

## Skills to Build

- [ ] **`/prep`** — Pre-meeting preparation skill. Reads stakeholder profiles, recent context, generates talking points and watch-fors. Highest-leverage unbuilt skill. *(carried over 3 sessions)*
- [ ] **`/debrief`** — Post-meeting debrief. Captures signals, decisions, follow-ups. Pair with `/prep`. *(carried over 3 sessions)*
- [ ] **`/1pager`** — Generate a structured one-pager (problem, proposal, alternatives, ask) from a grill session or raw notes
- [ ] **`/decision`** — Decision doc generator with options, tradeoffs, and recommendation
- [ ] **`/retro`** — Retrospective facilitator for projects or incidents
- [ ] **`/context-update`** — Guided update of AIContext files when things change (reorg, new stakeholder, project pivot)

## Jarvis System Improvements

- [ ] **Evals system** — Build rubrics for common Jarvis tasks (presentation prep, stakeholder analysis, communication drafting). Track quality over time instead of judging by feel. Start simple: after each task, rate output 1-5 on a few dimensions. Log to a file. Look for trends.
- [ ] **Meta-prompting workflow** — When a skill underperforms, feed the failed output + original skill prompt into Claude and ask it to rewrite the skill. Systematic prompt improvement instead of manual tweaking.
- [ ] **Mid-session process notes** — Before context compaction hits, Jarvis writes a checkpoint file summarizing decisions, open threads, and session state. Reads it back after compaction to maintain continuity.
- [ ] **End-session auto-propose context updates** — Phase 4 of end-session skill. Already added to the skill definition, needs to be tested and refined in practice.
- [ ] **Better context structure** — Audit and restructure `AIContext/` for optimal loading. Questions to answer: Which files are loaded too often? Which are too large? Should CLAUDE.md be an index that points to context files loaded on-demand rather than describing everything inline? How to minimize context window waste while keeping Jarvis well-informed.

## Automation & Proactive Jarvis

- [ ] **Cron job: web scouring for James** — Set up a scheduled agent that periodically searches the web for content relevant to James's interests and work. Could monitor: new papers on retrieval/recommendation systems, Pinterest engineering blog posts, agentic AI developments, leadership/management content matching James's growth edges. Deliver a digest (daily or weekly) with links + one-line summaries. Filter aggressively — only surface things James would actually read.
- [ ] **Self-improving Jarvis** — Explore how Jarvis can improve automatically without human intervention. Ideas: after each session, Jarvis reviews its own performance against the session log and proposes skill/prompt improvements. Automated A/B testing of skill prompt variants. Use the Jork framework (https://github.com/hirodefi/Jork) as reference for self-improving agent patterns. Key constraint: changes should be proposed and logged, not silently applied — James needs to trust the system.

## Monetization & Side Projects

- [ ] **How Jarvis can help James make money** — Brainstorm session on leveraging Jarvis + James's expertise for income. Potential angles: AI consulting for rec-sys teams, productizing Pinvestigator-like tools, content creation (blog/newsletter on AI-assisted engineering management), building and selling Claude Code skill packs, tutoring/coaching other EMs on AI workflows, side projects that compound James's ML + agentic AI skills into something sellable. Run a `/grill-me` session to pressure-test which ideas have real potential vs. distraction.

## Learning & Craft Projects

- [ ] **Recommendation system codebase from scratch** — Create a dedicated folder where James and Jarvis collaboratively build a recommendation system from the ground up. Purpose: deepen James's hands-on ML craft, create interview-ready artifacts, and serve as a teaching tool. Could follow the CLR/P2P architecture James already understands but implement from first principles. Structure: `projects/recsys-from-scratch/` with progressive modules (embeddings → two-tower → training loop → eval → serving). Jarvis acts as pair programmer and teacher.
- [ ] **NotebookLM notebook expansion** — Create notebooks for other domains James is learning: recommendation systems, agentic AI patterns, engineering leadership. Feed curated sources. Use `/consult-notebook` to query during relevant work.
