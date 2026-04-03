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

> Hi everyone, I'm James — I lead Homefeed Candidate Generation. With me are Sai, who leads Related Pins CG, and Mehdi from ATG. We're presenting together because this work lives at the intersection of surface-specific optimizations and a shared ML solution framework. I'll start with the problem, Sai will show you the vision, and Mehdi will walk through the technology.
>
> I want to show you two problems that initially seem quite different, but converge on a single elegant solution — one that's already saving us nearly a million dollars a year while improving engagement.
>
> This is the funnel architecture we share across Homefeed, BMI, Related Pins, Search, and Notifications. Billions of pins in the corpus, ~20 candidate generators pulling candidates, lightweight scoring, then heavy ranking.
>
> Here's what I want you to notice. Every number highlighted on this slide — 500, 1,000, etc. — these are all hard-coded constants. They don't change based on who the user is, what they're looking for, or what time of day it is. A power shopper and a casual browser get the exact same configuration, every single time.
>
> And tuning these numbers is time-consuming. This is just one surface — multiply it by every surface we run and the complexity is growing faster than our ability to manually optimize.

**Key guidance:**
- BLUF the stakes right after signposting — "$938K saved, engagement up" hooks the room before any technical detail
- Funnel walkthrough compressed to one sentence — the diagram is on the slide, don't narrate every box
- "Here's what I want you to notice" is a verbal spotlight — use it to focus attention on the constants
- Point at the diagram as you reference specific numbers

### Slide 4 — "A rare opportunity to save costs and increase personalization at once"

**Visual:** Bold headline with "save costs" in red and "increase personalization" in red. Lightbulb-highlighted insight about uniform compute. Two-bullet connection to knob problem.

**Talk Track:**

> *(PAUSE. LET THEM READ THE HEADLINE.)*
>
> The second problem: as we scale toward more users, our serving costs scale with it. And here the stakes are significant — our pre-ranking and ranking models alone cost over six and a half million dollars a year, and that cost scales linearly with the number of candidates we send them.
>
> The team surfaced something that seems obvious in hindsight but has big implications: today, we give every user the same compute budget on every request. Same candidate generators fire. Same number of candidates fetched. Same depth of ranking.
>
> Whether you're a power user deep in wedding planning or someone who opens the app once a month — identical.
>
> *(PAUSE BRIEFLY)*
>
> Now, this connects directly to the knob problem I just showed you. The reason we allocate uniformly is that all of these knobs are static. And the reason they're static is that the configuration space is already too complex to tune by hand. Two problems feeding each other: static knobs lead to flat compute allocation, and as we add more knobs, the manual tuning gets even slower.
>
> The team has already proven that a learned system can break this cycle — Sai and Mehdi will walk you through the results. But first, let me show you why we started in Retrieval.

**Key guidance:**
- The headline does its own work — don't narrate it, let silence do the selling
- $6.5M figure moved here from Slide 5 — anchor the stakes before the "identical" line so the audience feels the cost of uniformity
- "Wedding planning vs. once-a-month" is your most memorable line — pause after "identical"
- Don't read the bottom bullets; make the connection verbally
- Bridge to slide 5 should feel purposeful, not like a detour

### Slide 5 — "Retrieval Optimizes for Recall — and that's expensive when it's untargeted"

**Visual:** Two-column layout. Left: Retrieval's job (wide net of ~20 CGs). Right: Currently, the orchestration is static.

**Talk Track:**

> Where in the funnel do these problems matter the most? At the top. Retrieval is the gate to everything downstream.
>
> Retrieval's job is recall — don't miss the right content. It casts a wide net across many candidate generators, each designed for a different purpose. Some are learned and deeply personalized. Some are heuristic-based for diversity. Some are generative — powerful, but expensive. They serve different goals: shopping vs. organic, fresh vs. evergreen, personalized vs. relevant.
>
> But retrieval is pursuing all of these goals, for all users, all of the time. A user who's actively shopping for furniture gets the same CGs firing as someone who just opened the app to browse.
>
> *(PAUSE BRIEFLY)*
>
> If we can right-size that retrieval net — fire fewer CGs when the user doesn't need them, fetch less when the marginal candidate won't help — we're not just saving at retrieval. We're saving everywhere downstream. And we've already observed this working: $938K in annualized savings shipped, with repins up, not down.
>
> So the question becomes: can we learn to right-size that net per request, per user? Sai is going to show you what that looks like.

**Key guidance:**
- Opens with conclusion ("Retrieval is the gate") instead of building to it — no "specific reason why" preamble
- Ends with shipped proof ($938K, repins up) right before Sai handoff — the last thing they hear from you is evidence
- "We've already observed this working" — observation framing is more credible than opinion framing
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

---

## ELT Presentation Outcome (March 30, 2026)

**Result:** Strong success. High excitement, detailed technical questions, cross-org demand.

**CTO (Matt Madrigal):** Pulled into CEO meeting, missed first ~15 minutes. Will watch recording. James's problem framing section was on recording; Sai/Mehdi presented live for most of Q&A.

**James's section:** Landed cleanly. No questions needed — problem framing did its job. Credited Sai and RP results prominently.

**Sai's section:** Handled Q&A well. Answered all questions confidently. Strong showing in front of senior leadership.

**Kurchi:** Gave thumbs up — specifically around RP cost savings and cross-surface results. First positive public signal from her on Dynamic Triggering work.

### Key Engagement (Post-Presentation)

| Person | Title | Signal | Follow-up |
|--------|-------|--------|-----------|
| Kartik Paramasivam | Chief Architect | Wants to join feature review. Asked about feature list adaptability (how system handles new features from engineers). | Reply drafted. Include in next steps. |
| Faisal Farooq | VP Eng, Trust & Safety/Signals | Cold-start concern (new + low-freq + resurrected users). Engaged in DM. | James responded with 3 design considerations. Monitor for follow-up. |
| Ads VP (new to company) | VP Eng, Ads | Detailed technical questions. Interest in Ads surface expansion. | Coordinate with Mehdi for scoping. |
| Ads Principal ML Engineer | Principal ML, Ads | Detailed technical questions alongside Ads VP. | Same — Mehdi drives technical follow-up. |

### Strategic Implications

- **Funding gate cleared.** PhP / Dynamic Triggering moves from conditional to active for Q2.
- **Cross-org demand is inbound (pull, not push):** Ads, T&S/Signals, plus existing RP. Three orgs beyond James's own.
- **Platform thesis validated:** "Not a model, a platform" framing is landing with senior technical leadership.
- **Alok:** Moving to ~50% allocation on Dynamic Triggering. First task: scope Ads surface with Mehdi.
- **Mehdi:** Drives technical roadmap and Ads scoping. James holds exec relationships.
- **Darren (infra):** Funding conversation deferred until infra needs are scoped by Mehdi's technical roadmap.

### Next Steps

1. Reply to Kartik — invite to feature review, offer architecture walkthrough
2. Monitor Faisal thread — offer cold-start data walkthrough if he re-engages
3. Sync with Mehdi this week — align on Ads scoping, sequencing, and roles
4. Message Alok — 50% allocation, first deliverable is Ads scoping support for Mehdi
5. Do NOT respond to Ads interest directly until Mehdi is aligned on approach
