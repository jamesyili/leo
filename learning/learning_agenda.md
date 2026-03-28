# Learning Agenda

Personal structured curriculum. Five tracks, each independent. Prioritized for Q2 2026 and beyond.

**Time budget:** ~3 hrs/week dedicated learning + continuous on-the-job learning with Jarvis/Claude Code.

**Companion system:**
- **Concept notes** live in this `learning/` folder as individual `.md` files (e.g., `condition-token.md`, `pretraining-finetuning.md`). Variable granularity — some broad, some very specific. Each focuses on key nuances, what I understand, what I'm still working through.
- **Learning events** are logged in `outputs/session-log.md` (tagged as learning, not a separate journal).

---

## Prioritization

### Tier 1 — Now (Q2 2026)
- **Track 5:** Model Architecture & Transformers — directly supports UPP decisions happening right now
- **Track 2:** Evals modules — PINvestigator Q2 shift to eval-driven development
- **Track 1:** Claude Code hooks, skills, best practices — daily workflow compound gains

### Tier 2 — Next (Q3 2026)
- **Track 3:** ML System Design interview prep — when closer to wanting optionality
- **Track 2:** RL/bandit modules — when Retentive Recs feedback loop work is more active

### Tier 3 — Ongoing
- **Track 4:** Engineering Leadership — practiced in live situations, reflected on in session logs

---

## How to Use Concept Notes

Each concept note in `learning/` follows this shape:

```markdown
# {Concept Name}

## What it is
(My understanding, in my words)

## Key nuances
(The non-obvious stuff — what surprised me, what I got wrong initially, the gotchas)

## What I understand well
(Parts I can explain clearly to someone who doesn't know this)

## What I'm still working through
(Parts where my understanding is fuzzy, incomplete, or I can't yet explain simply)

## How it shows up in my work
(Concrete connections to UPP, Retentive Recs, PINvestigator, Homefeed, etc.)

## Go deeper
- [ ] Suggested exercise, reading, or open question
```

Granularity is intentionally variable. "Two-tower retrieval" and "condition token for user history modeling" can both be notes. They link naturally but don't need to live at the same level.

---

# Track 1: Claude Code & Claude AI Mastery

## Why This Track
Building Jarvis, PINvestigator, and daily workflow all run on Claude Code. This track fills gaps systematically so I stop discovering features by accident and start wielding the full toolkit intentionally.

---

## Module 1.1: Core Concepts & The Agentic Loop

### What to learn
- How Claude Code works under the hood: the agentic loop (model -> tool calls -> results -> model)
- Available tools: Read, Edit, Write, Bash, Glob, Grep, WebFetch, WebSearch, Agent (subagents)
- How the model decides which tools to use and in what order
- Context window management: what happens when context fills up (compaction, summarization)

### Key concepts
- **The agentic loop**: Claude reads prompt -> decides tool calls -> executes -> reads results -> decides next action -> repeats until done
- **Tool selection**: Claude chooses tools based on task; guide it by being specific
- **Context window**: Everything in conversation consumes tokens; long sessions degrade quality
- **Checkpointing**: Claude automatically checkpoints file changes; rewind with `/undo`

### Practice
- Start a session, ask Claude to explain a file, then modify it. Watch the tool sequence.
- Deliberately fill context by exploring a large codebase. Notice when compaction kicks in.
- Use `/undo` to revert a change Claude made.

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| Claude Code Docs | code.claude.com/docs/en/overview | Docs | $0 |
| Claude Code Best Practices | code.claude.com/docs/en/best-practices | Docs | $0 |
| "Building effective agents" | anthropic.com/engineering/ | Blog | $0 |

---

## Module 1.2: CLAUDE.md — Your Most Powerful Lever

### What to learn
- Project-level CLAUDE.md (checked into repo) vs user-level instructions
- How to write effective instructions that shape every response
- `.claude/rules/` directory for granular, path-specific rules
- File imports for composing instructions from multiple files

### Key concepts
- **CLAUDE.md is loaded into every conversation** — always-on context
- **Specificity matters**: "Use pytest, not unittest" > "follow best practices"
- **Rules directory**: `.claude/rules/*.md` files loaded alongside CLAUDE.md
- **Layering**: User-level -> project-level -> directory-level rules; more specific overrides more general

### What I already have
Jarvis CLAUDE.md is thorough — persona, operating principles, AIContext references, session continuity, conventions. Good template for future projects.

### Practice
- Add a `.claude/rules/` directory with a rule specific to ML work
- Try adding a user-level CLAUDE.md for preferences spanning all projects

---

## Module 1.3: Skills, Slash Commands & Subagents

### What to learn
- **Skills**: Reusable prompt templates invoked via `/skill-name`. Project-specific.
- **Slash commands**: Built-in commands (`/help`, `/clear`, `/undo`, `/compact`, `/fast`)
- **Subagents**: Specialized agents via Agent tool (Explore, Plan, general-purpose)
- **Agent teams**: Multiple agents working in parallel on different parts of a task

### Key built-in slash commands
| Command | Purpose |
|---------|---------|
| `/help` | Show help |
| `/clear` | Clear conversation context |
| `/compact` | Force context compaction |
| `/undo` | Revert last file changes |
| `/fast` | Toggle fast mode (same model, faster output) |
| `/review` | Code review |
| `/commit` | Create a git commit |

### Custom skills (what I'm building in Jarvis)
- Located in `.claude/skills/`
- Frontmatter: name, description, trigger conditions, tool access
- User-invocable (slash commands) or auto-triggered
- Current Jarvis skills: `/grill-me`, `/start-session`, `/end-session`, `/thinking-partner`, `/coach-check`, `/session-log`

### Subagent types
- **Explore**: Fast codebase exploration (search, find, understand)
- **Plan**: Architecture planning without making changes
- **general-purpose**: Full capability for complex multi-step tasks
- **claude-code-guide**: Answers questions about Claude Code itself

### Practice
- Create a custom skill for a repetitive task
- Use `/compact` mid-session when context feels bloated
- Ask Claude to use an Explore subagent to map part of the codebase

---

## Module 1.4: Hooks & Automation

### What to learn
- Hooks: Shell commands that execute in response to Claude Code events
- Hook events: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop
- Configuration: Defined in `.claude/settings.json`
- Use cases: Auto-formatting, blocking protected files, audit logging

### Hook types
- **Command-based**: Run a shell command
- **HTTP hooks**: Call a URL
- **Prompt-based**: Inject instructions
- **Agent-based**: Launch an agent
- **Async background**: Run without blocking

### Key events
| Event | When | Use case |
|-------|------|----------|
| `SessionStart` | Session begins | Set up environment |
| `UserPromptSubmit` | Before processing user input | Validate/transform prompts |
| `PreToolUse` | Before a tool executes | Block dangerous operations |
| `PostToolUse` | After a tool executes | Auto-format edited files |
| `Stop` | Session ends | Cleanup |

### Practice
- Set up a PostToolUse hook that runs a formatter after Python file edits
- Set up a PreToolUse hook that warns before modifying protected directories

---

## Module 1.5: Model Context Protocol (MCP)

### What to learn
- MCP = universal standard for connecting AI tools to external services
- Client-server architecture: Claude Code is the client, MCP servers provide tools
- Configuration via `.mcp.json` (project-level) or settings (user-level)
- Supported by Anthropic, OpenAI, Google — the emerging standard

### Key concepts
- **MCP servers expose tools** that Claude can call (database queries, API calls, etc.)
- **Remote servers** (HTTP/SSE): hosted services, no local install needed
- **Local servers** (stdio): run on your machine, communicate via stdin/stdout
- **Scopes**: Local (this machine), Project (shared via `.mcp.json`), User (all projects)

### Practice
- Add an MCP server to a project
- Explore the MCP server ecosystem at modelcontextprotocol.io

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| Intro to MCP (Skilljar) | anthropic.skilljar.com | Course | $0 |
| MCP Advanced Topics (Skilljar) | anthropic.skilljar.com | Course | $0 |
| MCP Docs | modelcontextprotocol.io/introduction | Docs | $0 |

---

## Module 1.6: Permissions, Security & Sandboxing

### What to learn
- Permission modes: which tools require approval vs auto-execute
- Permission rules syntax for fine-grained control
- Filesystem and network sandboxing
- Protecting sensitive files and directories

### Practice
- Review current permission settings
- Add rules that auto-approve reads but require confirmation for writes to certain areas

---

## Module 1.7: Advanced Workflows

### What to learn
- **Plan Mode**: Ask Claude to plan without executing
- **Extended Thinking**: Enable deeper reasoning for complex decisions
- **Git Worktrees**: Run parallel sessions on isolated branches simultaneously
- **Non-interactive mode** (`claude -p`): Use Claude in scripts, CI/CD, automation
- **Session management**: Resume, fork, name sessions

### Practice
- Use Plan Mode to design an approach, review it, then execute
- Run two parallel sessions using git worktrees for independent tasks
- Set up a `claude -p` command in a git pre-commit hook

---

## Module 1.8: Claude API & Agent SDK

### What to learn
- **Messages API**: Programmatic access to Claude models
- **Tool use (function calling)**: Define tools Claude can call in applications
- **Streaming**: Real-time response streaming
- **Agent SDK**: Build standalone agents (Python/TypeScript)
- **Prompt caching**: Reduce costs by caching common system prompts

### Relevance
PINvestigator uses Claude for LLM digest. Understanding the raw API helps debug agent behavior and optimize token usage.

### Practice
- Build a simple Claude API script
- Compare raw API usage vs higher-level wrappers

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| Building with Claude API (Skilljar) | anthropic.skilljar.com | Course | $0 |
| Claude API Docs | docs.anthropic.com | Docs | $0 |
| Agent SDK Docs | platform.claude.com/docs/en/agent-sdk/overview | Docs | $0 |
| Anthropic Cookbook | github.com/anthropics/anthropic-cookbook | Examples | $0 |
| Agent SDK Demos | github.com/anthropics/claude-agent-sdk-demos | Demos | $0 |
| Tool Use Course | github.com/anthropics/courses/tree/master/tool_use | Notebooks | $0 |

---

## Module 1.9: Courses & Certification

### Structured courses
| Course | URL | Hours | Priority |
|--------|-----|-------|----------|
| **Claude Code in Action** | anthropic.skilljar.com/claude-code-in-action | 3-4 | High |
| **Intro to Agent Skills** | anthropic.skilljar.com/introduction-to-agent-skills | 1-2 | High |
| **Prompt Engineering Tutorial** | github.com/anthropics/prompt-eng-interactive-tutorial | 3-4 | Medium |
| **Prompt Evaluations** | github.com/anthropics/courses/tree/master/prompt_evaluations | 2-3 | High (evals) |

### Engineering blog posts (selected)
| Post | Key takeaway |
|------|-------------|
| Building effective agents | Agent design patterns: chaining, routing, parallelization, orchestrator-workers |
| Effective context engineering | Context management, just-in-time retrieval, compaction, sub-agent architectures |
| Demystifying evals for AI agents | Three grader types, pass@k reliability, 8-step eval implementation |
| The "think" tool | Improving Claude's reasoning in complex tool-use scenarios |
| Writing effective tools for agents | Optimizing tool definitions for agent performance |

### Track 1 time estimate: ~29-39 hours total
Spread over 4-6 weeks at ~6-8 hrs/week. Start with Claude Code in Action, then alternate between courses and hands-on building.

---

# Track 2: RL & Evaluation for Rec Systems

## Why This Track
Retentive Recommendations is fundamentally an explore/exploit problem. The Geometric Bandit (Section 6 of the spec) is active design work. PINvestigator needs a proper eval harness for Q2. This track formalizes the RL and eval concepts directly applicable to both.

---

## Module 2.1: Offline Evaluation — Formalizing What You Know

### Core metrics
| Metric | Best for | Key property |
|--------|----------|-------------|
| Precision@K | "Are the top-K items relevant?" | Ignores rank order within K |
| Recall@K | "Did we find all relevant items?" | Captures coverage |
| MAP | Binary relevance, multiple relevant items | Averages precision at each relevant rank |
| MRR | Single "right answer" tasks | Only cares about first relevant item |
| NDCG | Graded relevance, rank-sensitive | Discounts by position; handles non-binary relevance |
| AUC-ROC | Binary classification (click/no-click) | Threshold-independent |

### For Retentive Recs
NDCG is the right primary metric for ranking UIC-conditioned candidates — some candidates are more relevant than others (graded), and position in the feed matters. But the key insight is that **relevance is defined relative to the UIC lifecycle state**: an "Enticement" cluster needs curiosity signals (closeups/clicks) as positive labels, while a "Stabilization" cluster needs commitment signals (repins/saves).

Standard offline eval treats all positive labels equally. Retentive Recs requires **state-dependent evaluation**: the same user action has different relevance depending on which UIC lifecycle state the candidate was served for.

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| Evaluation Metrics — Weaviate | weaviate.io/blog/retrieval-evaluation-metrics | Blog | $0 |
| Evaluating Rec Systems — Shaped | shaped.ai/blog/evaluating-recommendation-systems-map-mmr-ndcg | Blog | $0 |
| Aman.ai: Evaluation Metrics | aman.ai/recsys/metrics/ | Reference | $0 |
| 10 Metrics — Evidently AI | evidentlyai.com/ranking-metrics/evaluating-recommender-systems | Blog | $0 |

---

## Module 2.2: Online Evaluation & Counterfactual Methods

### A/B Testing
Gold standard but slow. Retention is a lagging indicator — A/B tests for Retentive Recs require weeks to reach significance on WAU/MAU.

### Interleaving
Merges recommendations from two models in one list shown to same user. Airbnb reported **50x speedup** over traditional A/B testing. Relevant for comparing UIC-conditioned retrieval vs. baseline CLR candidates within the same feed.

### Multi-Armed Bandits for experimentation
Dynamically allocates traffic to better-performing variants. Thompson Sampling converges fastest in practice.

### Counterfactual / Off-Policy Evaluation
Estimate "what would have happened" from logged data without running live experiments:
- **IPS (Inverse Propensity Scoring)**: Reweight logged interactions by propensity ratio. High variance.
- **SNIPS (Self-Normalized IPS)**: Normalizes weights. More stable, small bias.
- **Doubly Robust**: Combines model estimate with IPS correction. Robust if either is correct.

### For Retentive Recs
Off-policy evaluation lets you ask: **"Would different UIC lifecycle state transitions have improved retention?"** without actually serving different feeds. This is high-leverage because:
- Retention signal is delayed (days/weeks)
- The explore/exploit tradeoff means some users got exploration that didn't pay off — was the exploration well-targeted?
- You can evaluate alternative Geometric Prediction strategies (Vector Transport vs. Sensible Sourcing vs. Graph Completeness) against logged data

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| Counterfactual Evaluation — Eugene Yan | eugeneyan.com/writing/counterfactual-evaluation/ | Blog | $0 |
| KDD 2022 Counterfactual Tutorial | counterfactual-ml.github.io/kdd2022-tutorial/ | Tutorial | $0 |
| RecSys 2021 Off-Policy Tutorial | sites.google.com/cornell.edu/recsys2021tutorial | Tutorial | $0 |
| Beyond A/B Testing — Shaped | shaped.ai/blog/multi-armed-bandits | Blog | $0 |

---

## Module 2.3: Multi-Armed Bandits — The Geometric Bandit

### Classic bandits
- **Epsilon-Greedy**: Explore randomly with prob epsilon. Simple but epsilon needs tuning.
- **UCB (Upper Confidence Bound)**: Pick arm with highest confidence upper bound. "Optimism in the face of uncertainty."
- **Thompson Sampling**: Maintain posterior per arm, sample and pick highest. Best empirically.

### Contextual bandits
Algorithm sees *context* (features) before choosing an arm. This is where personalization enters.
- **LinUCB**: Linear model mapping context -> expected reward per arm.
- **Neural contextual bandits**: Neural net for richer representations.

### For Retentive Recs: The Geometric Bandit (Active Design)
The Retentive Recs system uses Thompson Sampling over **Geometric Hash keys** (LSH of UIC medioids), not Semantic IDs. This is a critical architecture decision:

**Why Geometric Hashing over Semantic IDs:**
- SIDs cause "Signal Bleed" — aliasing distinct user interests into generic categories
- SimHash preserves cosine similarity: similar vectors hash to same key, dissimilar vectors hash differently
- "Glamping" and "Survivalist Camping" are geometrically distant -> different LSH keys -> different Beta distributions
- Reward signal stays clean per-region rather than bleeding across a category label

**The Reward Function — Log-Lift:**
$R_t = \log(\frac{CTR_{current} + \epsilon}{CTR_{baseline} + \epsilon})$

This optimizes for **momentum** (is engagement accelerating?) rather than absolute CTR. A stale high-volume interest shouldn't crowd out a growing low-volume one.

**Negative feedback:** Fast Scroll / Hide = explicit penalty (reduces alpha in Beta distribution), collapsing confidence interval immediately.

**The bandit naturally handles explore/exploit:**
- Stabilized clusters: narrow Beta distributions (high confidence) -> sampled less often
- Predicted/new clusters: wide Beta distributions (low confidence) -> sampled more often -> if user engages, mean shifts right; if they ignore, mean shifts left and variance decreases

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| **Bandits for Rec-Sys — Eugene Yan** | eugeneyan.com/writing/bandits/ | Blog | $0 |
| Sutton & Barto Chapter 2 | incompleteideas.net/book/the-book-2nd.html | Textbook | $0 |
| Aman.ai: Multi-Armed Bandits | aman.ai/recsys/multi-armed-bandit/ | Reference | $0 |
| Spotify: Explore, Exploit, Explain | research.atspotify.com | Paper | $0 |

---

## Module 2.4: Full RL for Sequential Recommendation

### Value-based: DQN -> SlateQ
- **DQN for rec-sys**: Learn Q(state, action) = expected cumulative reward
- **SlateQ (Google/YouTube)**: Decomposes slate-level Q-value into per-item LTVs. Solves the combinatorial action space.

### Policy gradient: REINFORCE
- **Top-K Off-Policy Correction (Google, WSDM 2019)**: REINFORCE at YouTube production scale with off-policy correction for logged data. Reported highest single-launch revenue gain at YouTube.

### For Retentive Recs
Full RL maps to the **UIC lifecycle management** problem:
- **State**: Current UIC configuration (set of clusters with lifecycle states, engagement velocities, medioid positions)
- **Action**: Which Geometric Prediction strategy to apply to which cluster (Vector Transport, Sensible Sourcing, Graph Completeness, Synthetic Profiling)
- **Reward**: Long-term retention (WAU), not short-term engagement (CTR)
- **The sequential nature**: Each prediction strategy changes the user's UIC landscape, which changes the state for the next decision. This is genuinely sequential — not a one-shot ranking problem.

**Current scale reality**: The Geometric Bandit (Module 2.3) is the right starting point. Full RL for lifecycle management is Phase 3-4 — when there's enough logged data on strategy outcomes to train a policy.

### Resources
| Resource | URL | Priority |
|----------|-----|----------|
| **Top-K Off-Policy REINFORCE (Chen et al.)** | arxiv.org/abs/1812.02353 | Essential |
| SlateQ (IJCAI 2019) | arxiv.org/abs/1905.12767 | High |
| Deep RL for List-wise Recs | arxiv.org/abs/1801.00209 | Medium |
| Survey on RL for RecSys (Afsar et al.) | arxiv.org/abs/2101.06286 | Reference |

---

## Module 2.5: Reward Design & Delayed Feedback

### The Retentive Recs reward problem
The core tension: **short-term engagement metrics vs. long-term retention**. A feed optimized purely for clicks produces filter bubbles and user fatigue. A feed optimized purely for exploration produces irrelevance and churn. The right reward function balances both — and the signal is delayed.

### Layered reward signals
| Signal | Latency | Weight | Notes |
|--------|---------|--------|-------|
| Closeup/Click | Immediate | Medium | Curiosity signal — high value in Enticement state |
| Repin/Save | Minutes-hours | High | Commitment signal — high value in Stabilization state |
| Board creation | Hours-days | Very High | "Sealing the deal" — strongest new use case signal |
| Session return | Days | High | Short-term retention proxy |
| WAU/MAU | Weeks | Highest | True retention — the north star |

### State-dependent reward weighting
The same action has different reward value depending on UIC lifecycle state:
- **Enticement**: Closeups/clicks weighted high (gauging receptivity)
- **Activation**: Board creation weighted highest (sealing the deal)
- **Stabilization**: Repins/saves weighted high (commitment)
- **Re-evaluation**: Negative signals (fast scroll, hide) weighted high (detect decay faster)

### Engagement feedback loops — the traps
- **Popularity bias**: Stabilized clusters get more exposure -> more data -> appear more "optimal" -> crowd out Enticement clusters
- **Filter bubbles**: Users only see content from their strongest clusters -> no new use case discovery
- **Zombie clusters**: Interests that persist in the system despite user disengagement (the bandit's negative feedback handles this)
- **Mitigation**: Diversity injection between UICs, exploration budgets via Thompson Sampling, Log-Lift reward (momentum over absolute CTR)

### Resources
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| ROLeR: Reward Shaping in Offline RL (2024) | arxiv.org/html/2407.13163 | Paper | $0 |
| Handling Feedback Loops: Deep Bayesian Bandits | towardsdatascience.com | Blog | $0 |

---

## Module 2.6: Production Systems & Industry Practice

### Company approaches
| Company | Approach | Key insight |
|---------|----------|-------------|
| YouTube | REINFORCE + off-policy correction; SlateQ | Policy gradient scales to millions; off-policy is essential |
| Spotify | In-context exploration-exploitation | Coordinated exploration across recommender surfaces |
| Netflix | Contextual bandits for artwork personalization | Start bandits on a narrow surface, expand later |
| **Pinterest** | PinRec: outcome-conditioned generative retrieval (2025) | Moving beyond RL toward generative retrieval |
| DoorDash | Thompson Sampling with Beta distributions | Simple bandits, highly effective for categorical |
| Alibaba | LinUCB with positional bias correction | Contextual bandits with domain-specific corrections |

### Safe exploration in production
- **Conservative policy updates**: Constrain KL-divergence between old and new policies
- **Shadow mode**: Run new policy in shadow, evaluate with IPS/SNIPS, promote when confident
- **Exploration budgets**: Reserve slots for underexplored clusters (Retentive Recs does this by reserving Enticement slots in diversity scoring)

### Resources
| Resource | URL | Priority |
|----------|-----|----------|
| **PinRec (Pinterest, 2025)** | arxiv.org/html/2504.10507v1 | High — your day job |
| RL for Recommendations — Eugene Yan | eugeneyan.com/writing/reinforcement-learning-for-recsys-and-search/ | High |
| RL for Long-term Engagement (KDD 2019) | dl.acm.org/doi/10.1145/3292500.3330668 | Medium |

---

## Module 2.7: Evaluating AI Agents (PINvestigator Focus)

### Why this module
PINvestigator is shifting to eval-driven development in Q2. The agent has 3 parallel subagents (engagement analysis, holdout analysis, Slack search) — evaluating multi-step agentic behavior is fundamentally different from evaluating a single model call.

### Three evaluation levels
1. **Black-box (final output)**: Does the investigation report correctly identify the root cause? Compare against human-generated golden set investigations.
2. **Glass-box (trajectory)**: Did each subagent query the right tables? Did the orchestrator cross-correlate correctly? Compare tool call sequences against expected patterns.
3. **White-box (per-step)**: Unit-test individual subagent outputs. Did Subagent A correctly compute WoW deltas? Did Subagent C find the relevant Slack deploy messages?

### Key eval dimensions for PINvestigator
| Dimension | What to measure | How |
|-----------|----------------|-----|
| **Tool correctness** | Did the agent call the right Presto tables with valid queries? | Regex match on SQL, validate column names |
| **Tool efficiency** | Did the agent use optimal query patterns (not over-fetching)? | Count queries, measure token usage |
| **Cross-correlation quality** | Did Phase 2 correctly connect signals across subagents? | Golden set of known incidents with expected cross-correlations |
| **Report quality** | Is the final report actionable and accurate? | LLM-as-judge against human expert reports |
| **Failure handling** | When one subagent fails (e.g., Slack MCP down), does the system degrade gracefully? | Inject failures, verify partial report quality |

### Implementation roadmap
1. **Start with 20-50 real failure cases** — past investigations where PINvestigator got it wrong or missed something. This is the golden set.
2. **Build per-subagent unit evals** — can each subagent independently produce correct analysis for known scenarios?
3. **Build trajectory evals** — for a given metric anomaly, does the full system produce the right investigation sequence?
4. **Add LLM-as-judge** — have Claude evaluate report quality using binary pass/fail with detailed critiques (Hamel's approach)
5. **Run pass@k** — PINvestigator is non-deterministic. Run each eval case 3-5 times. Report pass@3 (succeeds in at least 1 of 3 runs) and pass^3 (succeeds in all 3 runs).

### Resources — Foundational
| Resource | URL | Format | Cost |
|----------|-----|--------|------|
| **Demystifying evals for AI agents** (Anthropic) | anthropic.com/engineering/demystifying-evals-for-ai-agents | Blog | $0 |
| **Your AI Product Needs Evals** (Hamel) | hamel.dev/blog/posts/evals/ | Blog | $0 |
| **LLM-as-a-Judge Guide** (Hamel) | hamel.dev/blog/posts/llm-judge/ | Blog | $0 |
| **LLM Evals FAQ** (Hamel & Shreya) | hamel.dev/blog/posts/evals-faq/ | Reference | $0 |
| **Task-Specific LLM Evals** (Eugene Yan) | eugeneyan.com/writing/evals/ | Blog | $0 |
| **A Field Guide to Improving AI Products** (Hamel) | hamel.dev/blog/posts/field-guide/ | Blog | $0 |

### Resources — Frameworks & Platforms
| Platform | URL | Best for | Cost |
|----------|-----|----------|------|
| **Inspect AI** (UK AISI) | inspect.aisi.org.uk | Most comprehensive open-source eval framework | $0 |
| **DeepEval** | deepeval.com | Easiest to start; pytest integration | $0 |
| **Langfuse** | langfuse.com | Open-source observability + eval | $0 self-hosted |
| **Promptfoo** | promptfoo.dev | Red-teaming and security eval | $0 |

### Resources — Papers & Benchmarks
| Resource | URL | Relevance |
|----------|-----|-----------|
| TRACE: Trajectory-Aware Eval | arxiv.org/html/2602.21230 | Trajectory eval theory |
| KDD 2025: LLM Agent Eval Survey | arxiv.org/html/2507.21504v1 | Comprehensive taxonomy |
| AgentRewardBench | arxiv.org/abs/2504.08942 | LLM judges for agent trajectories |
| Langfuse Agent Eval Cookbook | langfuse.com/guides/cookbook/ | Hands-on PydanticAI eval |

### Module 2.7 time estimate: ~22-30 hours
Read Anthropic + Hamel blog posts first (Week 1). Then hands-on: build evals with Inspect or DeepEval (Weeks 2-4). Papers last.

---

## Track 2 Textbooks & Courses
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| Sutton & Barto Ch. 2 (Bandits) | incompleteideas.net/book/the-book-2nd.html | 3-4 | High |
| Sutton & Barto Ch. 6 (TD Learning) | " | 2-3 | Medium |
| Sutton & Barto Ch. 13 (Policy Gradient) | " | 2-3 | Medium |
| David Silver Lectures 1-3 | davidstarsilver.wordpress.com/teaching/ | 3 | High |
| David Silver Lectures 6-7 | " | 2 | Medium |
| OpenAI Spinning Up (VPG, DQN) | spinningup.openai.com | 4-6 | Medium |

## Track 2 Frameworks
| Framework | URL | Best for |
|-----------|-----|----------|
| Vowpal Wabbit | vowpalwabbit.org | Production contextual bandits |
| Mab2Rec | github.com/fidelity/mab2rec | Bandit-based recommenders |
| d3rlpy | github.com/takuseno/d3rlpy | Offline deep RL |
| Ray RLlib | docs.ray.io/en/latest/rllib | Scalable distributed RL |

---

# Track 3: ML System Design Interviews

## Why This Track
Two rare assets: (1) UPP — a production-scale cross-surface ML platform I'm overseeing with 17+ engineers, and (2) PINvestigator — an agentic AI system I'm building hands-on. Most candidates describe systems they maintained or contributed to. I can describe one I designed at scale (UPP) AND one I built from scratch (PINvestigator). Breadth AND depth.

---

## Module 3.1: The ML System Design Interview Framework

### What interviewers evaluate
1. **Problem framing**: Translate business goals into ML objectives
2. **System architecture**: Design end-to-end, not just the model
3. **Data strategy**: How do you get, clean, store, and serve features?
4. **Model selection**: Why this approach over alternatives? Tradeoffs?
5. **Evaluation**: How do you know it's working? Offline -> online -> business metrics.
6. **Iteration**: How do you improve the system over time?
7. **Scale considerations**: What breaks at 10x, 100x, 1000x?
8. **Edge cases & failure modes**: What goes wrong and how do you handle it?

### The RESHAPES framework
1. **R**equirements: Clarify functional and non-functional
2. **E**stimation: Scale numbers (DAU, QPS, storage, latency)
3. **S**ervice architecture: High-level components and data flow
4. **H**igh-level design: API design, key abstractions
5. **A**rticulate data model: Schema, storage, access patterns
6. **P**erformance: Caching, indexing, optimization
7. **E**xtend: Edge cases, scale challenges, monitoring
8. **S**ecurity: Auth, rate limiting, data protection

---

## Module 3.2: Mapping UPP to System Design Dimensions

### The Story
UPP (Unified Personalization Platform) eliminates fragmentation where Homefeed, Notifications, Search, and P2P maintain parallel, independently-evolving ranking and retrieval models. The solution: a pretraining/fine-tuning framework where a shared base model gets continuously improved, and surface teams fine-tune on top.

**Why this is a strong interview case study:**
- Director-scale oversight: 17+ engineers, cross-org stakeholder management
- Rich model architecture: three-tier hierarchy (Foundation Model -> Base Models -> Surface-Specific Models)
- Live cross-org dynamics: Jinfeng's pushback, Kurchi's skepticism, co-design resolution
- Shipped results: +286k WAU on Notifications (only shipped online wins in all of UPP)

### Dimension 1: Problem Framing
**Interview hook**: "I lead the retrieval platform for Pinterest's Unified Personalization Platform — eliminating the fragmentation where four surfaces each maintain independent ranking and retrieval models."

**Key talking points:**
- Business metric: WAU (retention), not just engagement (clicks)
- ML objective: A shared base retriever that, when fine-tuned per surface, matches or beats standalone surface-specific models
- The non-obvious constraint: surface teams must own fine-tuning, features, and launch decisions — otherwise they won't adopt

### Dimension 2: System Architecture
**The Three-Tier Hierarchy:**
```
        [Foundation Model]
        User-level next-token prediction
                    |
               fine-tune
          +--------+--------+
          v                 v
  [Base Ranking Model]  [Base Retrieval Model (CLR)]
  (CFM option)           Dual-tower architecture
          |                 |
     fine-tune         fine-tune
     +----+----+      +-----+-----+
     v    v    v      v     v     v
   [HF] [Notif] [P2P] [HF] [Notif] [Search]
   Surface-Specific Models
```

**What interviewers love:**
- Clear separation between foundation, base, and surface-specific layers
- The pretraining/fine-tuning paradigm mirrors how frontier AI labs think about model platforms
- Co-equal platform pillars: Retrieval (James) and Ranking (Dhruvil)

### Dimension 3: Data Strategy
**The cross-surface data challenge** (great interview narrative):
1. "Each surface has different training data distributions — Homefeed is engagement-heavy, Search is relevance-heavy, P2P has contextual pins."
2. "The key unsolved problem: how do you build a cross-surface training dataloader that doesn't dilute surface-specific signal?"
3. "We evaluated two dataloader architectures (Options A vs B) and benchmarked them."
4. "The deeper insight: cross-surface training data is the shared infrastructure that makes a unified base model viable. If you can't solve the data, the model architecture doesn't matter."

**Feature engineering:**
- UIC medioids as condition inputs for CLR (replacing deprecated "Followed Interests" logic)
- OmniSage embedding space fusing Visual/Semantic (CLIP) + Interaction Graph + Topology Graph
- Surface-specific features owned by surface teams (fine-tuning layer)

### Dimension 4: Model Selection & Tradeoffs
**The UPP CLR architecture:**
- Dual-tower model: User Context Tower + Condition Tower (UIC medioid) + surface-specific Surface Towers
- Shared base pretrained on HF data, fine-tuned per surface
- Key design decision: CLR extended with P2P's context tower strengths ("UPP CLR") rather than separate base models per surface family

**The architecture debate (great interview material):**
- Option 1: One unified base retriever across all surfaces (chosen)
- Option 2: Two separate base models — one for HF/Notif, one for SSJ surfaces
- Why Option 1 won: Dylan's "one moving variable" reframe — add surfaces on existing base, then iterate architecture. Two base models fragments the thesis and doubles maintenance.
- How we got there: co-design process with P2P's ML lead, not a top-down mandate

**Evolution story:**
- v0: Standalone surface-specific CLRs (fragmented, each team builds independently)
- v1: HF CLR architecture replicated to Notif (+156k WAU)
- v2: Pretrained HF base, fine-tuned for Notif + DHEN scaling (+130k WAU)
- v3 (current): UPP CLR co-designed with P2P context tower, expanding to Search

### Dimension 5: Evaluation
**Offline:** Surface-specific metrics per fine-tuned model. Semantic relevance is the key concern for Search/P2P (engagement-optimized base may sacrifice relevance).

**The relevance challenge:**
- CLR supports multi-head objectives (relevance loss added for Notif, validated in production)
- But not yet validated on a relevance-heavy surface (Search)
- Kurchi's "I need data" was the right pushback — solved by scoping relevance loss experiments in co-design

**Online:** WAU impact per surface. Notif fine-tune matches standalone Notif CLR = proof point that pretraining/fine-tuning paradigm works for retrieval.

### Dimension 6: Iteration & Feedback
**The pretraining/fine-tuning flywheel:**
- Base model improves continuously with more surfaces and data
- Each surface team benefits from base improvements without retraining
- Surface teams can independently iterate on fine-tuning without affecting base

### Dimension 7: Scale
| Scale | Challenge | Solution |
|-------|-----------|----------|
| More surfaces | Cross-surface data distribution shifts | Surface-specific feature alignment (Zihao's documentation work) |
| Larger base model | Training cost, serving latency | DHEN scaling, GPU serving via CSI |
| Real-time features | Feature logging across surfaces | Cross-team infra dependencies (Notif feature logging) |

### Dimension 8: Edge Cases & Failure Modes
| Failure mode | Mitigation |
|-------------|------------|
| Base model regresses a surface | Surface teams own launch decisions; go/no-go milestone |
| Relevance degradation on semantic surfaces | Multi-head objectives with relevance loss |
| Cross-surface data dilution | Surface-specific dataloader weighting |
| Political resistance to platform adoption | Co-design model — surface teams are co-owners, not adopters |

---

## Module 3.3: Mapping PINvestigator to System Design Dimensions

### The Story
PINvestigator is an LLM-powered metrics investigation tool for the Homefeed Relevance team. Built as a Claude Code skill with parallel subagent architecture. James is building this hands-on as a tech lead.

**Why this is a differentiating interview case study:**
- Novel agentic AI architecture — most candidates can't talk about building agent systems from scratch
- Parallel subagent design with independent failure domains
- Real production use case (metrics investigation), not a toy demo
- Eval harness design (Q2 focus) — demonstrates the "hard part" of agent engineering

### Dimension 1: Problem Framing
**Interview hook**: "I built an LLM-powered metrics investigation agent that parallelizes across three independent data sources — engagement tables, holdout data, and Slack deploy history — then cross-correlates findings to identify root causes."

**Key framing:**
- Business problem: metric investigations take hours of manual SQL + Slack searching. Agents can do 80% of the rote work.
- ML objective: correctly identify root cause of metric movements with high recall (don't miss real issues) and reasonable precision (minimize false alarms)
- The hard part isn't the LLM — it's the orchestration, failure handling, and evaluation

### Dimension 2: Architecture — Thin Orchestrator + 3 Parallel Subagents
```
SKILL.md (orchestrator)
  |
  +-- Phase 0: Resolve target date + metric
  +-- Phase 1: Dispatch 3 subagents IN PARALLEL
  |   +-- Subagent A (engagement) -> 7 Presto tables
  |   +-- Subagent B (holdout)     -> 1 holdout table
  |   +-- Subagent C (Slack)       -> 4 Slack channels
  +-- Phase 1b: Validate results (handle partial failures)
  +-- Phase 2: Cross-correlate findings across A + B + C
  +-- Phase 3: Generate report
```

**Design principles:**
- Minimal context loading — only load schemas when a subagent needs them (~290 lines vs. ~900 monolithic)
- One subagent per data source — clean ownership, failures contained
- Synthesis in orchestrator — cross-correlation requires all outputs, runs after all subagents return
- Shared reference files — data-tables.md as single source of truth for schemas

### Dimension 5: Evaluation (Key Differentiator)
This is where the interview gets interesting — most candidates can't talk about evaluating agents.
- Three-level eval: black-box (report quality), glass-box (trajectory), white-box (per-step)
- pass@k for non-determinism (agents don't produce identical output each run)
- Golden set built from 20-50 real past investigations where the system got it wrong
- LLM-as-judge for report quality using binary pass/fail with critiques

### Dimension 8: Failure Modes
| Failure mode | Mitigation |
|-------------|------------|
| Slack MCP down | Subagent C fails gracefully; report generated from A + B only |
| Wrong SQL generated | Schema validation + query result sanity checks |
| LLM hallucination in cross-correlation | Ground all findings in specific data points from subagent outputs |
| Context window exhaustion | Layered context loading — only load what's needed per phase |

---

## Module 3.4: Common Interview Questions -> Your Answers

### "Design a recommendation system"
**Hook**: "I lead the retrieval platform for Pinterest's Unified Personalization Platform, which unifies recommendation models across four surfaces."
**Walk through**: Three-tier hierarchy (FM -> Base Models -> Surface-Specific). Emphasize the pretraining/fine-tuning paradigm, cross-surface data challenge, and the co-design process.

### "Design a recommendation system with exploration"
**Hook**: "We built a system called Retentive Recommendations that engineers serendipity — using Geometric Prediction in embedding space rather than random exploration."
**Walk through**: UIC representation, three prediction strategies (Vector Transport, Sensible Sourcing, Graph Completeness), Thompson Sampling Geometric Bandit with LSH keys and Log-Lift reward.

### "How would you evaluate an ML model in production?"
**Hook**: "We use layered evaluation because our key metric — retention — is a lagging indicator that takes weeks to measure."
**Walk through**: Offline (NDCG with state-dependent labels) -> Counterfactual (IPS/SNIPS on logged data) -> Online (A/B with WAU) -> Business (retention curves).

### "Design an anomaly detection / investigation system"
**Hook**: "I built an LLM-powered metrics investigation agent with parallel subagent architecture."
**Walk through**: Thin orchestrator + 3 parallel subagents, cross-correlation in Phase 2, eval harness with golden sets and pass@k. Emphasize failure handling and eval — that's what separates real agents from demos.

### "How do you handle cross-org resistance to platform adoption?"
**Hook**: "UPP expansion to Search and P2P faced real resistance. Here's how we navigated it."
**Walk through**: Co-design model (surface teams are co-owners, not adopters), "one moving variable" reframe, escalation pattern (surface right questions to right people, let them act), evidence over promises (ship wins on Notif first, then expand).

### The "why not just..." rebuttals
- **"Why not separate models per surface?"** -> "We tried that. It fragments the platform, doubles maintenance, and each surface misses cross-surface signal. The pretraining/fine-tuning paradigm is strictly better — and we proved it on Notif."
- **"Why not just use one model for everything?"** -> "Surface teams need to own fine-tuning. A monolithic model removes their agency and makes them adopters instead of co-owners. The three-tier hierarchy preserves ownership at the right level."
- **"Why Thompson Sampling over UCB?"** -> "Thompson Sampling handles the non-stationary reward landscape better — user interests evolve, so the Beta distributions need to adapt. Also, it naturally handles the exploration budget without a tuning parameter."
- **"Why LSH keys instead of Semantic IDs?"** -> "Signal bleed. Semantic IDs alias distinct interests into categories. Geometric hashing preserves the structure of the embedding space — similar interests hash together, dissimilar ones don't."

---

## Module 3.5: Technical Depth Drills

For each topic, practice explaining in 2 minutes:

### Two-tower retrieval (your Pinterest expertise)
- Query tower: user features -> embedding
- Item tower: item features -> embedding
- ANN for fast retrieval
- **UPP application**: CLR is a dual-tower model. User Context Tower + Condition Tower (UIC medioid) -> retrieve candidates close to the conditioned query point.

### Pretraining/fine-tuning for retrieval models
- Base model pretrained on cross-surface data (HF + BMI + Notif)
- Surface-specific fine-tuning preserves base representations while adapting to surface distribution
- **UPP application**: The core thesis. Pretrained HF base fine-tuned for Notif = +130k WAU. Same paradigm extending to P2P and Search.

### Cross-surface representation learning
- Challenge: different surfaces have different label distributions (engagement vs. relevance)
- Solution: multi-head objectives (engagement loss + relevance loss)
- **UPP application**: CLR with relevance loss already in production on Notif. Key open question: does it transfer to relevance-heavy surfaces (Search)?

### Feature engineering for embedding spaces
- OmniSage: fused Visual/Semantic (CLIP) + Interaction Graph + Topology Graph
- UIC construction: complete-link hierarchical clustering on L500 sequence
- **Retentive Recs application**: UICs as externalized features in GSS Feature Store — portable across CG, Ranking, and Diversity stages

### Agentic AI architecture patterns
- Thin orchestrator + parallel subagents (PINvestigator)
- Minimal context loading (only load schemas when needed)
- Layered failure handling (partial results > no results)
- Eval as first-class concern (golden sets, pass@k, LLM-as-judge)

---

## Module 3.6: Practice Schedule

### Week 1-2: Framework Mastery
- Memorize RESHAPES framework
- Practice drawing the UPP three-tier hierarchy in 60 seconds
- Practice drawing PINvestigator's subagent architecture in 60 seconds
- Prepare the "cross-surface data challenge" narrative (2 minutes)

### Week 3-4: Dimension Deep Dives
- Practice explaining each of the 8 dimensions using UPP
- Practice PINvestigator's eval story (the differentiator)
- Record yourself answering "Design a recommendation system" (aim for 35 minutes)

### Week 5-6: Common Questions
- Work through Module 3.4 questions, one per session
- Practice transitioning from generic answer -> UPP/PINvestigator-specific example
- Time yourself: 5 min clarification -> 20 min design -> 10 min deep dive

### Week 7-8: Technical Depth + Mocks
- Work through Module 3.5 drills (2 min each)
- Practice the "go deeper" follow-ups
- Mock interview with someone who can push back on tradeoffs

### Ongoing
Every time something evolves in UPP or PINvestigator, draft:
1. The 2-sentence interview description of what changed
2. The tradeoff considered and why this approach was chosen
3. The evolution story — "we started with X, learned Y, evolved to Z"

---

## Track 3 Resources
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| **ML System Design Interview** (Xu & Aminian) | amazon.com/dp/1736049127 | 10-12 | High |
| **Designing ML Systems** (Chip Huyen) | amazon.com/dp/1098107969 | 8-10 | Medium |
| System Design for Recs — Eugene Yan | eugeneyan.com/writing/system-design-for-discovery/ | 1.5 | High |
| Patterns for Personalization — Eugene Yan | eugeneyan.com/writing/patterns-for-personalization/ | 1 | Medium |
| Aman.ai: ML System Design Framework | aman.ai/mlsysdes/framework/ | 3-4 | High |
| Aman.ai: ML System Design Questions | aman.ai/mlsysdes/ | 3-4 | High |
| khangich/machine-learning-interview | github.com/khangich/machine-learning-interview | 2-3 | Medium |
| Grokking the ML Interview (Educative) | educative.io | 4-6 | Medium |

---

# Track 4: Engineering Leadership

## Why This Track
The soft skills are load-bearing for everything else. Strategic thinking shapes how UPP and Retentive Recs get prioritized. Delegation determines whether I can invest in Goal 2 (Agentic AI craft) without sacrificing Goal 1 (business outcomes). Emotional regulation is Goal 0 — the inner foundation.

This track is qualitatively different: it's practiced in live situations and reflected on, not studied in blocks.

---

## Module 4.1: Strategic Thinking

### What it means for an EM at Director trajectory
Strategic thinking at this level is not "having a vision." It's the ability to:
- See the system of incentives, constraints, and stakeholder motivations around a problem
- Identify the highest-leverage intervention point (not the most obvious one)
- Frame problems in ways that create alignment rather than resistance
- Hold multiple timescales simultaneously (this quarter's delivery AND the 18-month platform thesis)

### Key nuances I'm working through
- **The difference between being strategic and sounding strategic.** Real strategy is choosing what NOT to do. "We're going to do X, Y, and Z" is a plan, not a strategy. "We're going to do X because it's the only thing that unblocks Y and Z" is strategic.
- **Strategic framing as a political tool.** Dylan's "one moving variable" reframe solved the Option 1 vs. Option 2 impasse not by arguing either side but by changing the frame entirely. This is a learnable skill.
- **When to be strategic vs. when to be operational.** In senior rooms, my speaking power comes from being the practitioner (operational), not the strategist (Dylan's job). Strategic thinking informs *what I choose to say*, but the delivery should sound like lived experience.

### Applied practice (live situations)
- **UPP expansion**: How to frame the retrieval platform narrative for Rajat in a way that makes it co-equal with Dhruvil's ranking platform — not competing, complementary
- **Retentive Recs**: Framing as "the technical engine for Anticipation" (strategic alignment with company vision) rather than "a ranking optimization" (tactical)
- **Resource allocation**: Making the case for what to drop when adding scope — not "we need more people" but "here's the tradeoff we're making and why"

### Frameworks
- **"What game are we playing?"** — Finite (deliver this feature) vs. infinite (build a platform that compounds). Director-caliber leaders play infinite games.
- **The DACI for strategic decisions**: Driver, Approver, Contributors, Informed. Forces clarity on who actually decides.
- **Pre-alignment before broadcast**: Raise flags in small forums first, especially for contentious cross-team topics.

### Suggested reading
| Resource | What you learn |
|----------|---------------|
| **Good Strategy / Bad Strategy** (Rumelt) | The kernel of strategy: diagnosis, guiding policy, coherent actions. Most "strategies" are just goals. |
| **The Art of Action** (Bungay) | Bridging the gap between plans and execution. Directed opportunism. |
| **Playing to Win** (Lafley & Martin) | Strategy as an integrated set of choices: Where to Play and How to Win. |
| **An Elegant Puzzle** (Larson) | Engineering management strategy — sizing teams, managing technical debt, organizational design. |

---

## Module 4.2: Delegation & Coaching TLs

### The core challenge
Director-readiness is leverage. But delegation without capability scaffolding produces one of two failure modes:
1. **Under-delegation**: I stay in the critical path for everything. Can't take a week off without escalation debt. (Current risk.)
2. **Over-delegation**: TLs don't have the judgment yet, decisions go sideways, I end up cleaning up. (Historical pattern.)

### Key nuances
- **"Barbell delegation"**: Delegate ownership while retaining 2-3 key review gates. Not micromanaging, but not abdication.
- **The narrative gap**: TLs can own execution but often can't own the narrative. If Piyush delivers the technical work but I'm not present for the exec framing, the story gets lost or captured.
- **Coaching TLs who aren't performing to standard**: The instinct is to take it back. The Director move is to invest in their growth with clear feedback, explicit expectations, and a deadline for improvement.
- **Scaling through Bowen's departure**: 17 direct reports is not sustainable. The EM hire and pod model activation (if no signed offer by mid-May) are structural interventions, not just backfill.

### Applied practice
- **Piyush**: Owns UPP CLR technical architecture. My job: narrative ownership with Rajat, cross-org unblocking, not technical oversight.
- **TL operating system**: Weekly TL sync, decision review rubric, artifact templates. The goal: TLs proactively write decision docs and pre-align stakeholders without prompting.
- **Explicit leader scoreboard**: Are my TLs spending more time on strategy and system design than on unblocking tickets?

### Frameworks
- **Situational Leadership II**: Match leadership style (directing, coaching, supporting, delegating) to follower development level per task
- **The Coaching Habit** (Bungay Stanier): 7 questions that shift from advice-giving to coaching. "What's the real challenge here for you?"
- **Intent-based leadership** (Marquet, "Turn the Ship Around"): Push authority to where the information lives. "I intend to..." instead of "permission to..."

### Suggested reading
| Resource | What you learn |
|----------|---------------|
| **Turn the Ship Around** (Marquet) | Leader-leader model. Push decision authority down. |
| **The Coaching Habit** (Bungay Stanier) | 7 essential coaching questions. Stop giving advice, start asking. |
| **High Output Management** (Grove) | The classic on leverage, meetings, and organizational output. |
| **Radical Candor** (Scott) | Care personally + challenge directly. The framework for hard feedback. |

---

## Module 4.3: Emotional Regulation & Executive Presence

### The pattern (from coaching with David & Rodney)
Under pressure, the Di profile intensifies:
- **High D spike**: Overly demanding, blunt, pushing agenda without inviting input
- **High i spike**: Overselling, optimistic promises to preserve momentum
- **Speed bias**: Steamrolling methodical thinkers, dismissing legitimate concerns
- **Rumination**: Uncertainty converts to analysis. The analysis feels productive but is avoidance.

### The Tai Chi base
Not passivity — a practice of returning to base. When something hits (reorg, lukewarm response, peer's success), the question is not "what does this mean about me?" It's "where is my base, and how quickly can I return to it?"

### Key practices
- **Intent labeling**: Before disagreeing or pushing for speed, state intent. "My intent here is to unblock us for Friday, so I'm pushing hard on X. Thoughts?" Prevents directness from reading as aggression.
- **Pre-meeting reset**: 2 minutes before high-stakes meetings. Story -> facts -> ask. Visualize the Tai Chi base.
- **Post-meeting debrief**: What did I feel? What story am I telling? What are the facts? Did I say what was true and useful before asking "how did I land?"
- **Naming the pattern**: "I'm reading tea leaves again." "I'm converting uncertainty to analysis." The act of naming interrupts the spiral.
- **Boring Consistency**: Low Heat, Steady Light. Metric: zero instances of defensiveness or litigating the point. "I am not the owner of the truth; I am the mechanic fixing the car."

### The UPP training ground
The SSJ/Kurchi/Jinfeng dynamic is a live case for all three skills:
- **Strategic thinking**: Framing UPP retrieval as co-equal with Ranking, not competing
- **Delegation**: Letting Dylan and Rajat handle the political escalation; staying in the practitioner lane
- **Emotional regulation**: When Jinfeng misrepresented alignment, flagging it factually, not emotionally. When Kurchi pushed back ("I need data"), recognizing it as reasonable, not adversarial.

### Applied practice
- **Weekly check**: Am I leaving high-stakes meetings asking "did I say what was true and useful?" before "how did I land?"
- **Recovery tracking**: Rumination episodes getting shorter? Returning to base faster after triggering events?
- **The internal scoreboard**: Is PINvestigator better this week? Is my team energized? Am I learning? Am I recovering faster? Do *I* think I did good work?

### Suggested reading
| Resource | What you learn |
|----------|---------------|
| **Leadership and Self-Deception** (Arbinger Institute) | How self-betrayal creates organizational dysfunction. The "box." |
| **Crucial Conversations** (Patterson et al.) | High-stakes dialogue when opinions differ and emotions run hot. |
| **Nonviolent Communication** (Rosenberg) | Observation, feeling, need, request framework. Reduces reactivity. |
| **The Inner Game of Tennis** (Gallwey) | Self 1 (conscious) vs Self 2 (unconscious). Quiet the inner critic. |

---

# Track 5: Model Architecture & Transformers

## Why This Track
UPP decisions happen at the architecture level — pretraining, fine-tuning, tower design, cross-surface representation learning. Being able to engage credibly at the technical review level (not just the strategy level) is what separates a strong EM from one who's just "above the fray."

---

## Module 5.1: Transformer Fundamentals

### What to learn
- Self-attention mechanism: queries, keys, values, attention weights
- Multi-head attention: why multiple heads capture different relationship types
- Positional encoding: how transformers handle sequence order
- Layer normalization, residual connections, feed-forward layers
- The encoder-decoder architecture vs. decoder-only (GPT-style) vs. encoder-only (BERT-style)

### Key nuances for UPP
- **Foundation Model layer** uses next-token prediction (decoder-style) — why? Because it's learning sequential user behavior patterns.
- **CLR** uses a dual-tower encoder architecture — why? Because retrieval needs independent encoding of queries and items for ANN serving.
- The relationship between these two layers is a pretraining/fine-tuning paradigm, not a single architecture.

### Resources
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| **3Blue1Brown: Attention in Transformers** | youtube.com (Visualizing attention) | 0.5 | High (intuition) |
| **Jay Alammar: The Illustrated Transformer** | jalammar.github.io/illustrated-transformer/ | 1-2 | High |
| **Attention Is All You Need** (Vaswani et al.) | arxiv.org/abs/1706.03762 | 2-3 | High |
| **Stanford CS224N** (selected lectures) | web.stanford.edu/class/cs224n/ | 3-4 | Medium |

---

## Module 5.2: Two-Tower Architectures for Retrieval

### What to learn
- The fundamental constraint: at serving time, you can't run a cross-attention model over billions of items
- Solution: encode queries and items independently, use ANN for retrieval
- Query tower: user features + context -> query embedding
- Item tower: item features -> item embedding
- Training: contrastive loss (positive pairs close, negative pairs far)
- Serving: item tower pre-computed and indexed; query tower runs at request time

### Key nuances for UPP CLR
- **Condition Tower**: The UIC medioid is a condition input — it tells the query tower *what aspect of the user* to retrieve for. This is different from a standard query tower that encodes a single user representation.
- **Surface-specific Surface Towers**: Each surface can add its own tower elements on top of the shared base. This is the fine-tuning layer.
- **Cross-surface pretraining**: The base CLR is trained on data from multiple surfaces. The hypothesis: cross-surface signal improves each surface's retrieval because user behavior on one surface is informative for another.
- **The semantic relevance challenge**: Standard CLR optimizes for engagement. Search needs relevance. Multi-head objectives (engagement loss + relevance loss) are the solution, but balancing the heads is non-trivial.

### Resources
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| Google: Recommendation Systems (two-tower section) | developers.google.com/machine-learning/recommendation | 1-2 | High |
| Aman.ai: Candidate Generation | aman.ai/recsys/candidate-gen/ | 2 | High |
| YouTube: Deep Neural Networks for Recommendations | arxiv.org/abs/1606.07792 | 2 | Medium |
| **PinRec (Pinterest, 2025)** | arxiv.org/html/2504.10507v1 | 2-3 | High |

---

## Module 5.3: Pretraining & Fine-Tuning Paradigms

### What to learn
- **Pretraining**: Train a large model on broad data (self-supervised or multi-task)
- **Fine-tuning**: Adapt the pretrained model to a specific task/surface with task-specific data
- **Why it works**: Pretrained representations capture general patterns; fine-tuning specializes without losing them
- **Key design decisions**: What to freeze vs. unfreeze, learning rate scheduling, how much fine-tuning data is enough

### Key nuances for UPP
- **The UPP thesis**: A shared base model pretrained on cross-surface data should produce better surface-specific models than surface-specific training from scratch. Validated on Notif (+130k WAU with pretrained HF -> Notif fine-tune).
- **What the base model learns**: Cross-surface user behavior patterns that no single surface could learn in isolation. Users who engage with hiking content on Homefeed also click camping notifications — that cross-surface signal improves both.
- **The risk**: Pretraining on a dominant surface (HF) may bias the base model toward that surface's distribution. Fine-tuning may not fully overcome this bias for surfaces with very different distributions (Search, P2P).
- **DHEN scaling**: Deep Hierarchical Expert Networks — scaling the model capacity at the fine-tuning layer. Used in the Notif win.

### The evolution story (strong interview material)
1. **Status quo**: Each surface builds and maintains its own retrieval model independently
2. **Insight**: Cross-surface pretraining on ranking (CFM) showed wins. Does the same work for retrieval?
3. **Proof point**: HF CLR architecture replicated to Notif = +156k WAU. Pretrained HF, fine-tuned for Notif = +130k WAU.
4. **Scaling**: Co-design UPP CLR incorporating P2P context tower strengths. Expand to Search.
5. **Future**: Foundation Model -> Base Retriever -> Surface-Specific Retrievers as the permanent architecture

### Resources
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| **Designing ML Systems** Ch. 9 (Chip Huyen) | amazon.com/dp/1098107969 | 2-3 | High |
| Transfer Learning survey | ruder.io/transfer-learning/ | 1-2 | Medium |
| BERT: Pre-training of Deep Bidirectional Transformers | arxiv.org/abs/1810.04805 | 2 | Medium |

---

## Module 5.4: Cross-Surface Representation Learning

### What to learn
- **Multi-task learning**: Training one model on multiple tasks/surfaces simultaneously
- **Shared vs. task-specific parameters**: Which layers are shared (base) vs. surface-specific
- **Label distribution mismatch**: Engagement-heavy surfaces (HF) vs. relevance-heavy surfaces (Search)
- **Multi-head objectives**: Multiple loss functions (engagement + relevance) weighted per surface
- **Negative transfer**: When cross-surface training hurts rather than helps a specific surface

### Key nuances for UPP
- **The cross-surface dataloader challenge**: How to sample and weight training data from surfaces with wildly different distributions. This is the unsolved infrastructure problem that gates everything.
- **Relevance loss in production**: Already deployed on Notif (no relevance regression). Key open question: does it transfer to Search where relevance is the primary concern, not a secondary constraint?
- **The condition tower as the bridge**: UIC medioids encode personalized user state across surfaces. The same UIC can condition retrieval on HF (engagement-oriented) and Search (relevance-oriented) — the surface tower adapts the base representation.
- **Feature alignment across surfaces**: Different surfaces log different features. Zihao's surface documentation work maps which features exist on which surfaces and identifies gaps that must be filled before cross-surface training.

### Resources
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| Multi-Task Learning in Rec Systems — Aman.ai | aman.ai/sysdes/sys-design/ | 2 | High |
| Aman.ai: RecSys Architectures | aman.ai/recsys/architectures/ | 2 | Medium |
| Eugene Yan: Real-time ML for Recs | eugeneyan.com/writing/real-time-recommendations/ | 1 | Medium |

---

## Module 5.5: Embedding Spaces & Representation Quality

### What to learn
- **Embedding space geometry**: What "closeness" means (cosine similarity, euclidean distance)
- **Embedding fusion**: Combining multiple signal layers into one space (OmniSage approach)
- **Clustering in embedding space**: How to identify coherent groups (hierarchical, k-means, HDBSCAN)
- **Evaluation of embedding quality**: Retrieval benchmarks, alignment metrics, downstream task performance

### Key nuances for Retentive Recs
- **OmniSage fuses three signal layers**: Visual/Semantic (CLIP) + Interaction Graph + Topology Graph (Pin-Board). In OmniSage, "closeness" = functional utility, not just visual similarity. A hiking boot and a granola bar are neighbors because users curate them on the same "Hiking Trip" boards.
- **UIC construction**: Complete-link hierarchical clustering on the user's L500 sequence (last 500 actions). Merge criterion: similarity must exceed threshold relative to ALL events in target cluster (ensuring high coherence).
- **Dynamic cluster count**: The number of UICs per user is not fixed — users with diverse interests have more clusters. This is a key innovation over fixed-category approaches.
- **Geometric operations in embedding space**: Vector Transport, Slerp interpolation, centroid computation — these are meaningful operations because OmniSage is structured so that geometric proximity = functional utility.

### Resources
| Resource | URL | Hours | Priority |
|----------|-----|-------|----------|
| Jay Alammar: Illustrated Word2Vec | jalammar.github.io/illustrated-word2vec/ | 1 | High (intuition) |
| Stanford CS246: Dimensionality Reduction | web.stanford.edu/class/cs246/ | 2-3 | Medium |
| Google: Embeddings overview | developers.google.com/machine-learning/crash-course/embeddings | 1 | Medium |

---

## Track 5 time estimate: ~20-30 hours
Prioritize Modules 5.1-5.3 (T1). Modules 5.4-5.5 deepen as UPP work demands.

---

# Appendix A: Master Resource List

## Newsletters (subscribe to 4-5 max)
| Newsletter | Author | URL | Focus |
|------------|--------|-----|-------|
| **Latent Space** | swyx & Alessio | latent.space | AI engineering (most technically relevant) |
| **ByteByteGo** | Alex Xu | blog.bytebytego.com | System design (clear diagrams) |
| **Eugene Yan's Blog** | Eugene Yan | eugeneyan.com/writing/ | Rec-sys + LLM intersection |
| **The Batch** | Andrew Ng | deeplearning.ai/the-batch/ | Broad AI news |
| **Ahead of AI** | Sebastian Raschka | magazine.sebastianraschka.com | Deep technical dives, paper roundups |

## Podcasts
| Podcast | Suggested episodes | Hours |
|---------|--------------------|-------|
| Lenny's Podcast | AI evals (Hamel & Shreya), LinkedIn full-stack builders | 5-6 |
| Latent Space | Agents, evals, rec-sys episodes | 3-4 |
| Behind the Craft | AI product episodes | 2-3 |

## Key Papers (priority order)
| Paper | URL | Priority |
|-------|-----|----------|
| **Top-K Off-Policy REINFORCE** (Chen et al.) | arxiv.org/abs/1812.02353 | Essential |
| **PinRec (Pinterest, 2025)** | arxiv.org/html/2504.10507v1 | High (your day job) |
| SlateQ (IJCAI 2019) | arxiv.org/abs/1905.12767 | High |
| Attention Is All You Need | arxiv.org/abs/1706.03762 | High |
| BERT | arxiv.org/abs/1810.04805 | Medium |
| ROLeR: Reward Shaping (2024) | arxiv.org/html/2407.13163 | Medium |
| TRACE: Trajectory-Aware Eval | arxiv.org/html/2602.21230 | Medium |

---

# Appendix B: Time Estimates

| Track | Hours (Range) | Priority Tier |
|-------|--------------|---------------|
| 1. Claude Code & Claude AI Mastery | 29-39 | T1 (selected modules) |
| 2. RL & Evaluation for Rec Systems | 45-60 | T1 (evals), T2 (RL) |
| 3. ML System Design Interviews | 42-58 | T2 |
| 4. Engineering Leadership | Ongoing | T3 |
| 5. Model Architecture & Transformers | 20-30 | T1 |
| **TOTAL** | **~136-187 hrs** | |

### Realistic timeline
| Pace | Hours/Week | Duration |
|------|-----------|----------|
| **Normal** (alongside work) | 3-4 | 8-12 months |
| **Moderate** (dedicated learning time) | 6-8 | 4-6 months |
| **Intensive** (interview prep) | 10-15 | 3-4 months |

### If time-constrained (100 hours)
1. Xu/Aminian ML System Design book (12 hrs, whiteboard)
2. Claude Code in Action + 2-3 Anthropic courses (10 hrs)
3. Eugene Yan: Bandits + Counterfactual Eval + System Design (5 hrs)
4. YouTube REINFORCE + PinRec papers (6 hrs)
5. Hamel eval blog posts + hands-on eval building (8 hrs)
6. Transformer fundamentals + two-tower deep dive (8 hrs)
7. UPP case study prep — write interview answers (10 hrs)
8. PINvestigator case study prep — write interview answers (8 hrs)
9. Mock interviews (20 hrs)
10. Leadership reading (1-2 books) (13 hrs)

### If time-constrained (50 hours)
1. Xu/Aminian ML System Design book (12 hrs)
2. Claude Code in Action (4 hrs)
3. Eugene Yan: Bandits + System Design for Recs (3 hrs)
4. YouTube REINFORCE paper (4 hrs)
5. Hamel evals blog posts (3 hrs)
6. Write UPP + PINvestigator interview answers (8 hrs)
7. Mock interviews (16 hrs)

---

# Appendix C: Study Mode Reference

| Mode | When to Use | Retention |
|------|-------------|-----------|
| **Read** | Concepts, surveys, blog posts, docs | ~20% after 1 week |
| **Watch** | Lectures, demos, walkthroughs | ~30% after 1 week |
| **Build** | Code, experiment, integrate into your project | ~75% after 1 week |
| **Whiteboard** | Draw diagrams, practice explaining, mock interviews | ~60% after 1 week |
| **Discuss** | Teach someone, explain to a peer, rubber-duck to Jarvis | ~90% after 1 week |

Best approach: Read -> Whiteboard -> Discuss for conceptual material. Watch -> Build for tools/code. The concept notes in `learning/` are the "Discuss" artifact — writing forces understanding.
