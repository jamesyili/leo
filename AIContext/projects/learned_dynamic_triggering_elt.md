# Learned Dynamic Triggering — ELT Presentation

**Date:** March 31, 2026 (early Monday morning)
**Audience:** CTO (Matt Madrigal) + VPs
**Slot:** 20–30 minutes
**Presenters:** James Li (slides 1–5, problem framing), Sai Xiao (slides 6–10, vision + results), Mehdi Ben Ayed (slides 11–17, solution + technology)

## James's Role

Opens the presentation. Sets the tone. Sells the problem space — knob proliferation, flat compute allocation, and why retrieval is the highest-leverage place to solve both. ~4–5 minutes speaking time.

## Narrative Arc (James's Section)

### Core thesis
Two problems that initially seem disparate — (1) knob proliferation / engineering velocity ceiling, and (2) flat compute allocation / cost inefficiency — converge on a single elegant solution: a learned system that makes per-request retrieval decisions.

### Slide Flow

| Slide | Title | Purpose | Time |
|-------|-------|---------|------|
| 1 | Learned Dynamic Triggering (title) | Intro, acknowledge cross-org team | ~15 sec |
| 2 | Problem (section divider) | Transition — skip quickly | ~3 sec |
| 3 | Average-User Tuning & Knob Proliferation | Orient audience on funnel. Establish Problem 1: static knobs, growing complexity | ~60–75 sec |
| 4 | A rare opportunity to save costs and increase personalization at once | Establish Problem 2: flat compute allocation. Connect the two problems | ~60–75 sec |
| 5 | Retrieval Optimizes for Recall — and that's expensive when it's untargeted | Why retrieval is the highest-leverage intervention point. Bridge to Sai | ~60–75 sec |

## Slide-by-Slide Talk Tracks

### Slide 3 — "Average-User Tuning & Knob Proliferation"

**Visual:** Funnel diagram showing Corpus → ~20 CGs (with hardcoded fetch counts) → ~10k pins → Ranking (LWS → Pinnability) → ~2k pins → Blending → ~200 pins → Feed.

**Talk Track:**

> Hi everyone, my name is James and I lead the Homefeed Candidate Generation teams. I'll start by framing two problems that initially seem quite different, but turn out to share an elegant common solution.
>
> Let me first quickly orient everyone on how we serve recommendations today. This is the funnel architecture that we share across Homefeed, Related Pins, Search, and Notifications.
>
> We start with billions of pins in the corpus, and each of our ~20 candidate generators pulls a fixed number of candidates. CG1 always fetches 500, CG2 always 1,000, and so on. These then go through lightweight scoring, and 2,000 candidates are fed into the heavy ranker scoring.
>
> Here's what I want you to notice. Every highlighted number on this slide — 500, 1,000, etc. — these are all hard-coded constants. They don't change based on who the user is, what they're looking for, or what time of the day it is. A power shopper and a casual browser get the exact same configuration, every single time.
>
> And tuning these numbers is time-consuming. This is just one surface — multiply it by every surface we run and you see that complexity is growing faster than our ability to manually optimize, which slows down iteration speed.

**Key guidance:**
- Point at the diagram as you reference specific numbers
- "Here's what I want you to notice" is a verbal spotlight — use it to focus attention
- Don't narrate every box in the funnel; skim the flow, land on the constants

### Slide 4 — "A rare opportunity to save costs and increase personalization at once"

**Visual:** Bold headline with "save costs" in red and "increase personalization" in red. Lightbulb-highlighted insight about uniform compute. Two-bullet connection to knob problem.

**Talk Track:**

> *(PAUSE. Let them read the headline.)*
>
> The second problem: as we scale toward more users, our serving costs scale with it. The question we asked ourselves is: does it have to be linear? Can we bend that curve without degrading the experience?
>
> And the team surfaced something that seems obvious in hindsight but has big implications: today, we give every user the same compute budget on every request. Same candidate generators fire. Same number of candidates fetched. Same depth of ranking.
>
> Whether you're a power user deep in wedding planning or someone who opens the app once a month — identical.
>
> *(PAUSE)*
>
> Now, this connects directly to the knob problem I mentioned a moment ago. The reason we allocate uniformly is that all of these knobs are static. And the reason they're static is that the configuration space is already too complex to tune by hand. So we end up with two problems feeding each other: static knobs lead to flat compute allocation, and as we add more knobs, the manual tuning gets even slower.
>
> These two problems converge on a single solution. But before we get there, I want to show you why retrieval specifically is the highest-leverage place to solve it.

**Key guidance:**
- The headline does its own work — don't narrate it, let silence do the selling
- "Wedding planning vs. once-a-month" is your most memorable line — pause after "identical"
- Don't read the bottom bullets; make the connection verbally
- The bridge to slide 5 should feel purposeful, not like a detour

### Slide 5 — "Retrieval Optimizes for Recall — and that's expensive when it's untargeted"

**Visual:** Two-column layout. Left: Retrieval's job (wide net of ~20 CGs). Right: Currently, the orchestration is static.

**Talk Track:**

> So where in the recommendation funnel do these problems matter the most? At the top. And there's a specific reason why.
>
> Retrieval's job is recall — don't miss the right content. It does this by casting a wide net across many candidate generators, each designed for a different purpose. Some are learned and deeply personalized. Some are heuristic-based for diversity. Some are generative — powerful, but expensive. They also all serve different goals: shopping vs. organic, fresh vs. evergreen, personalized vs. relevant.
>
> But here's the thing — retrieval is pursuing all of these goals, for all users, all of the time. A user who's actively shopping for furniture gets the same CGs firing as someone who just opened the app to browse.
>
> *(PAUSE)*
>
> And this matters because retrieval is the gate to everything downstream. Pre-ranking and ranking are our most expensive models — over six million dollars a year combined — and their cost scales linearly with the number of candidates we send them. If we can right-size the retrieval net — fire fewer CGs when the user doesn't need them, fetch less when the marginal candidate won't help — we're not just saving at retrieval. We're saving everywhere downstream.
>
> So that's the opportunity. The question becomes: can we learn to right-size that net per request, per user? Sai is going to show you what that looks like.

**Key guidance:**
- Left side takes ~20 seconds (context-setting), right side takes ~40–50 seconds (the argument)
- The $6M+ figure makes "linearly" feel expensive rather than abstract — anchor it
- Bridge to Sai is one sentence. Clean, confident handoff. Don't linger.

## Anticipated Executive Questions

### Tier 1: Likely Questions

**Q: "What's the total cost savings opportunity?"**
- Behind it: "Is this worth my attention, or is this a science project?"
- Prep: $6.5M+ in ranking cost exposure. ~$938K already saved from shopping optimization alone (HF $258K + RP $680K). Frame as floor, not ceiling.

**Q: "What's the risk to engagement / pinner experience?"**
- Behind it: "Are you going to break something to save money?"
- Prep: Shopping case study — reduced shopping load 8% while repins UP 0.51% and GPS neutral. "Not a cost-vs-quality tradeoff."

**Q: "How does this interact with ranking improvements?"**
- Behind it: "Does this team understand the full system?"
- Prep: Not jointly modeling retrieval and ranking today — open area. Cost asymmetry means retrieval-side optimization has higher ROI even without joint modeling. Framework is extensible.

**Q: "Why RL? Why not simpler?"**
- Behind it: Legitimacy check.
- Prep: Mehdi's territory. Started simple (offline replay, value model) — those already shipped. RL next because action space is combinatorial (150+ configs). Frame as progression.

**Q: "What's the latency impact?"**
- Prep: ~70ms without parallelization → ~15ms with Dynamic Sizer running async. Launching together.

**Q: "How does this scale to other surfaces?"**
- Prep: Surface-agnostic decisioning framework. Already proven on HF + RP independently. Search and Ads next.

### Tier 2: Unspoken Questions

- "Who owns this?" → Joint workstream, clear ownership per layer
- "What's the team investment?" → Frame as leverage: X engineers, $Y savings, applies everywhere
- "Is this the same as what [other team] is doing?" → Blending personalizes utility weights at end of funnel; we personalize what enters the funnel. Complementary.
- "What do you need from us?" → Have ask ready. Continued investment, potential GPU optimization support from MLP teams if ranking budget tuning scales up.

## Prepared Answers (Full)

**Cost savings:**
> Already proven — 20% reduction on Shopping CGs. $260K annual HF savings shipped, engagement up. Applying same framework across all HF stages (CG, LWS, Ranking) at conservative 10% floor = additional $850K off $8.5M base. ~$1.1M total on HF alone, before Search/Ads/Notif expansion. Not cost-vs-quality — 1–2% repin gains alongside cost reduction.

**What do you need from us?**
> In a good place. Dynamic Sizer integration with CSI complete. Watching: as we expand into LWS and Ranking optimization with higher candidate counts, may need GPU optimizations from MLP teams for parallelism. Not an ask today, will flag early if it materializes.

**Latency:**
> Anticipated from day one — invested in Dynamic Sizer with CSI before shipping. Without parallelization: ~70ms. With async RPCs: ~15ms incremental. Launching together, mitigation baked in from start.

**Engagement risk:**
> Not trading engagement for cost — smarter allocation. Shopping load tuning proof: reduced shopping load for disinterested users, replaced with engaging organic content. Repins +0.51%, GPS neutral. Giving each user more of what they want, spending less on what they'd scroll past. Personalized compute is an engagement lever that also saves money.

**Ranking interaction:**
> Tuning stages independently today. Designed for robustness: 95/5 explore/exploit framework. 5% random policy → training data for next auto-retrained model. Gives adaptability (catches ranking model changes), avoids feedback loops, enables continuous learning.

## Key Numbers

- Pinnability model: ~$5M/yr
- LWS model: ~$1.5M/yr
- Combined ranking exposure: ~$6.5M/yr
- Shipped savings: ~$938K/yr (HF $258K + RP $680K)
- Shopping load reduction: 8% (HF), with repins +0.51%
- Dynamic Sizer latency mitigation: 70ms → 15ms

## Strategic Principles

- Two problems, one solution (knob proliferation + flat compute → learned per-request decisions)
- Retrieval is the leverage point (controls what flows downstream)
- Cost asymmetry (retrieval fetch = sub-linear cost; ranking score = linear cost)
- Frame as floor, not ceiling ($938K from one knob on two surfaces)
- It's a platform, not a model (the decisioning framework is the strategic asset)

## Cross-Org Teams

- Personalization CG: Alok Malik, Piyush Maheshwari, Bowen Deng, James Li
- SSJ CG: Ryan Hou, Sai Xiao
- ATG: Mehdi Ben Ayed, Jiajing Xu
- Infra (CSI): Kent Jiang, Darren Regger

## Presentation Dos and Don'ts

**Do:**
- Let slide 4 headline work on its own — pause
- Use concrete examples (wedding planner, furniture shopper, casual browser)
- Anchor with dollar figures ($6.5M exposure, $938K saved)
- Frame every ELT question as a buying signal
- Have a clear ask ready

**Don't:**
- Read the slides
- Get into RL details (Mehdi's job)
- Claim identical treatment for all users — say "largely uniform"
- Get defensive on questions
- Linger on Sai handoff
