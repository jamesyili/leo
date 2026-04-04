## 2026-04-04 (afternoon) — ECC deep-dive continued, custom subagents research, weekend plan

**Done:**
- Reviewed full backlog across Leo, Rekko, and personal items — consolidated prioritized view
- Marked org chart refresh as done in leo_backlog.md (James completed it independently)
- Continued ECC deep-dive: audited hooks (4 built, remaining recipes are incremental)
- Researched custom subagents — new capability: `.claude/agents/` with YAML frontmatter, scoped tools/models/permissions per agent. Daniel already uses one in Rekko (critic.md)
- Scoped 4 high-value subagents for Leo: researcher, notebook-consultant, context-auditor, writer

**Decisions:**
- Custom subagents are higher value than Context Modes (#5) — context isolation is the big win
- Weekend plan: subagents → rules directory → mgrep skill → memory improvements → evals/trace → hook validation → Rekko video pipeline

**Open:**
- Rekko: video pipeline review + 30-day plan still pending (committed to Daniel)
- Evals system still not built (carried forward)
- Hook validation not yet done

**Next time:**
- Build Leo subagents (researcher, notebook-consultant, context-auditor, writer)
- ~~Explore rules directory pattern~~ *(deprioritized)*
- ~~Build mgrep skill~~ *(deprioritized)*
- Dig deeper into Affaan's ECC thread: https://x.com/affaanmustafa/status/2014040193557471352
- Memory persistence improvements across sessions
- Evals + trace system
- Validate hooks fire correctly in fresh session
- Rekko: review Daniel's video pipeline codebase, draft 30-day plan
