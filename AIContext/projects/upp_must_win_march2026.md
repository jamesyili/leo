# UPP Must-Win: Full Strategic Coaching & Preparation Log

**James Li • March 2026 • Exported from Claude conversation**

---

## Table of Contents

1. [Strategic Context & Key Documents](#1-strategic-context--key-documents)
2. [Initial Strategic Assessment](#2-initial-strategic-assessment)
3. [Monday Meeting Strategy (Rajat Alignment)](#3-monday-meeting-strategy-rajat-alignment)
4. [James's Unique Position in Senior Rooms](#4-jamess-unique-position-in-senior-rooms)
5. [The CFM vs UPP Framing Challenge](#5-the-cfm-vs-upp-framing-challenge)
6. [The Two Key Points to Land](#6-the-two-key-points-to-land)
7. [Rajat Meeting Outcome (Week of 3/16)](#7-rajat-meeting-outcome-week-of-316)
8. [Follow-Up to Kurchi's Team](#8-follow-up-to-kurchis-team)
9. [P2P Retrieval Scoping (Week of 3/16–3/23)](#9-p2p-retrieval-scoping-week-of-316323)
10. [Strategic Escalation: Option 1 vs Option 2](#10-strategic-escalation-option-1-vs-option-2)
11. [Jinfeng's Pushback & Resolution](#11-jinfengs-pushback--resolution)
12. [Wednesday Co-Design Alignment](#12-wednesday-co-design-alignment)
13. [Must-Win Talking Points (March 30)](#13-must-win-talking-points-march-30)
14. [Key Learnings & Strategic Insights](#14-key-learnings--strategic-insights)

---

## 1. Strategic Context & Key Documents

### What UPP Is

UPP (Unified Personalization Platform) is the cross-surface retrieval platform owned by James's team. Currently live on Homefeed and Notifications, with Q2 mandate to expand to Search and P2P. CLR (Conditional Learned Retrieval) is the backbone model.

UPP is Dylan's #1 priority and the centerpiece of the team's Director case. Cross-surface expansion is what makes UPP a platform thesis rather than a Homefeed optimization.

### Key Stakeholders

| Person | Role | Disposition |
|--------|------|-------------|
| Jeff | VP of Core | Decision-maker. Huge proponent of UPP since inception. Both orgs report to him. |
| Vicky | Product VP | Co-audience with Jeff. Likely supportive if pitch shows clear ROI. |
| Rajat | VP of Eng | Strong supporter. Pushed for Option 1 (unified base retriever). Forced alignment. |
| Kurchi | Search Sr. Dir | Key skeptic. Wants data before committing. Concerned about semantic relevance. |
| Huizhong | P2P Director | Making things difficult. Her ICs were blocked from engaging until leadership aligned. |
| Dylan | James's Dir | Internal champion. Leading the charge. Pre-aligned with Jeff. |
| Jinfeng | P2P ML Lead | Pushed for P2P LR as base. Now co-designing UPP CLR after Dylan/Rajat alignment. |

### Key Documents Referenced

- **UPP High-Level Architecture Doc** — Three-tier model hierarchy: Foundation Model → Base Models (Ranking + Retrieval) → Surface-Specific Models
- **Must-Win Retrieval Draft** — Variations for wins, learns, motivation, levers, risks sections
- **Must-Win Strategic Synthesis** — 8-section preparation guide covering goals, stakeholders, objections, talking points
- **UPP Context Summary** — Organizational context for presentation prep

### The Three-Tier UPP Hierarchy

```
            [Foundation Model (FM)]
            Pretrained, user-level next-token prediction
                        │
                   fine-tune
              ┌─────────┴─────────┐
              ▼                   ▼
    [Base Ranking Model]   [Base Retrieval Model]
    (CFM is one option       (Base CLR)
     for this layer)         Dual-tower architecture
              │                   │
         fine-tune           fine-tune
         ┌───┴───┐         ┌─────┴─────┐
         ▼       ▼         ▼           ▼
     [Surface  [Surface  [Surface    [Surface
      Ranker    Ranker    Retriever   Retriever
      - HF]     - Notif]  - HF]       - Notif]
```

### Key Shipped Results (Retrieval)

| Launch | Status | Impact | Details |
|--------|--------|--------|---------|
| Notif CLR Architecture Replication | Launched | +156k WAU | Replicated HF CLR architecture on Notif retrieval |
| Pretrained HF → Notif FT + DHEN Scaling | In-flight | +130k WAU | Pretrained HF base, fine-tuned for Notif, scaled via DHEN |

Total retrieval impact on Notifications: ~286k WAU (launched + in-flight). These are the only shipped online wins in all of UPP.

---

## 2. Initial Strategic Assessment

### The Core Strategic Frame

The presentation is not a technical demo. It's a resource commitment decision. Jeff and Vicky need to believe that allocating their teams' ICs to UPP integration will pay off FOR THEIR TEAMS. The frame must be: what does Search/P2P gain from UPP, not what does UPP need from Search/P2P.

### Key Risk

If the must-win doesn't land, Search and P2P ICs stay blocked. The Q2 goal of a working cross-surface integration becomes impossible.

### Initial Directions Identified

- Structuring the Monday alignment meeting with Rajat, Kurchi, and Huizhong
- Building the must-win presentation narrative arc for Jeff and Vicky
- Thinking through the Huizhong/Kurchi dynamic given the IC engagement blockage
- Pressure-testing the staffing story given Piyush returns March 25

---

## 3. Monday Meeting Strategy (Rajat Alignment)

### Key Insight: Monday Is Pre-Alignment, Not the Must-Win

The goal isn't to win the argument — it's to surface objections, make Kurchi and Huizhong feel heard, and ensure there are no surprises in the Jeff/Vicky room. If you "win" Monday but Kurchi feels steamrolled, she sandbags the must-win. If you "lose" Monday but learn exactly what she'll object to, you can pre-wire Jeff accordingly.

### Top Message Options Considered

**Option A**: "We're proposing a learning agenda, not a takeover." Matt Chun's framing. Disarms autonomy concern. Risk: too soft for Rajat.

**Option B**: "UPP covers both retrieval AND ranking — the alternative covers only half the stack." Sharpest differentiation. SSJ's parallel path is ranking-only. Risk: can feel like an attack on Kurchi's CFM proposal.

**Option C**: "Here's what P2P and Search get from this — for free." Pure value-to-them framing. Risk: sounds too good to be true.

**Recommendation**: Lead with A (collaborative), pivot to C (value), hold B in reserve. Let Dylan or Rajat make the "your proposal is incomplete" argument if possible.

### Countering Kurchi and Huizhong

**Kurchi's likely moves:**
- "We're already evaluating CFM for P2P ranking" → Reframe: CFM is a great ranking base model option within UPP's learning agenda
- Autonomy concerns → Point to Notifs model: they own fine-tuning, launch decisions, feature choices
- Goes quiet/noncommittal → Most dangerous. Ask directly: "What would need to be true for Search to see this as valuable?"

**Huizhong's likely moves:**
- Defer to Kurchi or raise practical blockers ("can't staff this") → Counter with sequencing: P2P proposed first because architecturally closer to HF/Notif
- Don't try to win her over directly. Real audience is Rajat.

---

## 4. James's Unique Position in Senior Rooms

### The Fundamental Constraint

In a 30-minute room of senior directors, James is a senior manager. Speaking power comes from one thing nobody else has: being the person who actually did it. Not strategic arguments (Dylan's job), not org-level framing (Rajat's job) — lived operational experience.

### What James Is Uniquely Positioned to Say

1. **The retrieval gap in SSJ's proposal** — As the retrieval lead, flagging "what's being discussed is ranking-only; retrieval is where our shipped wins are" is a factual observation from the subject matter expert. It's his lane.
2. **The access ask** — Reframes from "person advocating for UPP" to "person trying to do the work who needs help." Asking senior directors to unblock cross-team collaboration is asking them to do their job.
3. **Operational feasibility** — When someone asks "how hard is this, really?" — "We went through this with Notifs. The playbook exists, the infra is built, and the second time is faster."

### The Moment to Listen For

Any variant of "what's the timeline," "how much eng cost," "is this realistic," or feasibility concerns. That's the cue for one calm, specific, experience-based answer. Then stop talking.

---

## 5. The CFM vs UPP Framing Challenge

### The Risk: Terminological Confusion Is the Weapon

If the UPP team needed a multi-day Slack thread to align on how CFM fits into UPP's three-tier hierarchy, imagine what happens when Jinfeng says "we're going to do CFM for P2P" in a room full of non-technical senior directors. To Jeff and Vicky, that sounds like a plan. To James, it sounds like ranking-only base model work outside the UPP framework that ignores retrieval.

The danger isn't that Jinfeng is wrong — it's that "do CFM" sounds complete and simple, while "do UPP" sounds complex and cross-org.

### Internal Alignment (From Slack Thread)

The team aligned that:
- CFM sits at the base model layer (Layer 2 in UPP hierarchy)
- Base ranker = ranking CFM, base retriever = retrieval CFM (architecturally adapted)
- CFM wouldn't co-exist with another Base Retriever or Base Ranker — that fragments the system
- Long-term: base ranker = ranking CFM, base retriever = retrieval CFM
- Preferred approach: 2b (augment base CLR with CFM-style training) over 2a (separate models)
- Bowen suggested merging CFM/FM terminology for simplicity; James pushed for real alignment first

### The 30-Second Clarification (If Needed)

"UPP has three layers. Foundation model at the bottom, base models in the middle — that's where CFM lives — and surface-specific models on top. CFM is a great option for the base ranking model, and we're aligned on that. But there's also a base retrieval model, and that's where our shipped wins came from. If we only do CFM for ranking, we're covering one of the two base model slots."

---

## 6. The Two Key Points to Land

### Point 1: The Retrieval Gap (Domain Expertise)

"I want to flag that what's being discussed right now is ranking-only. Retrieval is where our shipped wins are, and it's not part of the current scoping."

This is a factual observation from the subject matter expert. It's James's lane. Nobody else in the room can make that point with the same authority.

### Point 2: The Access Ask (The Concrete Request)

"To give you a real answer on what P2P retrieval onboarding looks like — timeline, eng cost, what's hard, what's not — my team needs to get into the technical details with the P2P retrieval engineers. Right now we haven't been able to do that scoping. If we can get that access, we can come back with a concrete plan instead of estimates."

Why this works:
- It's humble — "I don't have the answer yet because I haven't been able to do the work"
- It's practical — asking for something specific and actionable
- It puts the ball in Kurchi's/Huizhong's court without calling them out
- It gives Rajat exactly the opening to say "let's make that happen"

The two points connect: "The current proposal covers ranking but not retrieval. We'd like to scope retrieval for P2P, and to do that well, we need to work directly with the P2P team on the technical details." Factual gap → concrete ask. Then done.

---

## 7. Rajat Meeting Outcome (Week of 3/16)

### What James Landed in the Room

- Flagged that the current proposals cover ranking only — retrieval (where shipped wins are) isn't part of the scoping
- Made the concrete ask: "We need access to the P2P team and prioritization to do the scoping."
- Rajat agreed and decided that Kurchi and Huizhong would unblock IC access for scoping before the must-win

### Key Outcome

Kurchi was genuinely surprised retrieval was on the table. Dylan vocally supported doing both ranking and retrieval. Rajat decided to open access for scoping. The ask was heard clearly.

### Kurchi's Specific Concerns Raised

1. Even scoping has costs — prioritization decisions needed about what to drop
2. Wanted more details about the retrieval plan — asked if the idea is to replace learned retrieval models
3. Search and P2P have a strong semantic relevance component that UPP hasn't solved for yet

### On the Semantic Relevance Point

Jaewon argued it's just a question of goals — UPP can optimize for engagement or relevance labels, no real trade-off, just a question of whether it's been tried. Rajat wasn't as confident. This became a key scoping question.

### Assessment: Being Direct Worked

James's bluntness about asking for access and prioritization was effective, not excessive. The outcome speaks for itself: Rajat made the decision needed, and it was framed as a request, not a demand.

---

## 8. Follow-Up to Kurchi's Team

### The Message Sent

Brief follow-up pointing to technical design docs with three highlights:
1. Shipped Notif retrieval wins: +156k WAU (launched) and +130k WAU (in-flight)
2. Base CLR supports surface-specific fine-tuning — surfaces own features, heads, and launch decisions
3. On semantic relevance: framework supports multi-head objectives (relevance loss added for Notif), but not yet validated on a relevance-heavy surface — key thing to dig into during scoping

### The Relevance Doc Sent to Kurchi

Detailed the BMI CLR relevance work:
- CLR model possesses ability to incorporate relevance loss, already in production for Notifications
- Notif fine-tuned model maintains relevance loss, and UPP v1 launched on Notif without relevance regressions
- CLR with relevance loss showed visual semantic relevance improvement (but with engagement regressions on HF/BMI)
- Architecture can be extended to do relevance loss in base training for surfaces with higher relevance importance

---

## 9. P2P Retrieval Scoping (Week of 3/16–3/23)

### Initial Scoping Meeting with Jinfeng/Sai

Alignment on joint ownership: P2P drives fine-tuning, co-ownership at pretraining layer. Two options emerged:

**Option 1**: One unified base retriever across all surfaces (jointly designed)
**Option 2**: Two separate base models — one for HF/Notif, one for SSJ surfaces

Jinfeng/Sai leaned toward Option 2 (SSJ-first unification using P2P LR). Both options require cross-surface training data, which is unsolved and difficult.

### James and Jaewon's Position

One base model is the right long-term structure, consistent with UPP's thesis and the wins seen from CFM cross-surface pretraining on ranking. Two base models adds maintenance cost and fragments the very thing being unified. But the base model doesn't have to be the current CLR — P2P should be co-owners of the design, not adopters.

### From James and Jaewon's Side Conversation

**Jaewon**: "I hope that we don't view UPP×P2P retrieval as a competition between P2P LR vs CLR. Since the goal is to build a better unified model in the future, I feel it is pointless to debate which one is better today."

**James**: "I wonder if it might be more helpful to discuss in terms experiment priority? ... I don't know if there's much of a point to even debating whether or not this is UPP. It is UPP imo. Just a matter of which experiments to try first."

**Jaewon**: "I agree. This is UPP, and SSJ wants to do cross surface pretraining. So the only question for P2P finetuning is the base ranker design: (1) whether we use the current P2P LR as a base ranker merging SSJ only, or (2) whether we use a unified base retriever merging 4 surfaces. What I really don't want to see is that we choose (1) because we couldn't agree on the design for the unified retriever."

### Strategic Insight: The Cross-Surface Data Play

Both options need cross-surface training data, nobody's solved it, and it's naturally UPP-scoped work. Leading the cross-surface data effort means the architecture question starts to answer itself — because building cross-surface training infrastructure for two separate base models is strictly more work than building it for one. You don't need to argue against Option 2; you just need to make the shared infrastructure so obviously one-base-model-shaped that Option 2 becomes the harder path.

---

## 10. Strategic Escalation: Option 1 vs Option 2

### James Surfaced the Question to Dylan, Matt, Andrew

Message outlined the two options, Jinfeng/Sai's preference for Option 2, and asked for guidance on how to prepare.

### Rapid Alignment Triggered

**Dylan**: "Rajat just called me regarding this area. He wants to go with 1, he doesn't want people to go with option 2. He will call an alignment meeting between me and Kurchi and put his step on option 1."

**Andrew**: "Rajat told me he senses there is no full buy-in on the SSJ side yet (which is where the alternative option 2 is coming from) and thus he plans to make them 'disagree & commit.'"

**Dhruvil's observation**: "It's not clear how much of Yihong's time we will have, and for how long. We want to treat it as a 'serious try with few iterations to make it work' whereas P2P seems to be thinking of it more as 'one off experiment to see if it works.'"

**Dylan's "One Moving Variable" Reframe**: "There are two moving variables: (1) Surfaces: HF, notif, BMI, P2P, SR; (2) Model architecture: P2P based, or CLR based. I suggest we only have one moving variable. Now that CLR is on 3 surfaces, let's try make it work for P2P, and start design next gen base (combination of P2P and CLR). Once we are having all surfaces using the same base, it's much easier to iterate and upgrade architecture."

### Dylan's Meeting with Rajat and Kurchi (1 hour)

Outcome:
- Full execution focus on making Option 1 (CLR) work for P2P
- No execution resource for Option 2
- Jinfeng can do joint design on next-gen retriever as continuation of Option 1 succeeding (not alternative)
- Firm date/milestone for go/no-go decision on CLR results for P2P

### Assessment

James surfaced the right questions to the right people at the right time and let them act. That's effective escalation. The message created the forcing function that got Rajat to call Dylan, which got Dylan to reframe for Jinfeng, which got the alignment meeting with Kurchi. None of that happens if James just tries to negotiate with Jinfeng directly.

---

## 11. Jinfeng's Pushback & Resolution

### The Misalignment

After the decision, Jinfeng told the Slack channel he'd agreed with Dylan/Kurchi to start with P2P LR as the backbone — contradicting Dylan's actual directive. His proposed sequencing:
1. Start with today's CLR base model and fine-tune on P2P data (quick test)
2. Re-design P2P LR for cross-surface context model (real investment)
3. Run online experiments on P2P first, then adopt on other surfaces

The pattern: Step 1 is set up to produce underwhelming results with low investment. Step 2 is where real engineering goes — into P2P LR, not CLR. This is Option 2 relabeled as a roadmap.

### Jaewon's Counter

"Shouldn't we also try re-designing today's CLR base model?" — diplomatically calling out that Jinfeng's sequence only invests in improving P2P LR.

### Escalation to Dylan

James flagged the discrepancy to Dylan directly. Dylan confirmed: "That's not what I agreed." Dylan and Kurchi were added to the thread to clarify.

### The Thread Resolution

Kurchi proposed: A design review of both approaches — (1) CLR base model, what it takes to make it more contextual; (2) P2P base model, what it takes to generalize it. Then discuss as a group.

**Kurchi's key concern**: "My ask is to do what is going to help us easily maintain semantic relevance on contextual surfaces — and not go for a design that makes it super hard." Also: "It's hard to do anything without some offline evals — I am not sure where you all are getting confidence from without data."

**Dylan pushed for focus**: "Kurchi, we would like to focus. After reviewing both tomorrow, can we align on committing to one approach?"

**Kurchi pushed back**: "That seems like not the right call to me as well — given our VPs are not experts either. Again, I don't know how anyone can decide without data. Let's discuss tomorrow and see where we land as a group."

### Assessment of Kurchi

She's being reasonable, not political. "I don't know how anyone can decide without data" is fair. She's not blocking; she's saying don't force a premature commitment.

---

## 12. Wednesday Co-Design Alignment

### Meeting Occurred While James Was Out (Kidney Stone Operation)

James missed the Wednesday meeting but received updates from Dylan, Krystal, and Zihao.

### Key Decisions Made

1. Skip CLR vs. P2P LR evaluation — not apples to apples
2. Co-design a unified base retriever: CLR extended with P2P's context tower strengths ("UPP CLR")
3. POCs named: Jaewon (ATG), Jinfeng (P2P), Piyush (P13N), Hongtao (ATG), plus a P2P engineer TBD
4. Success criteria: No regression on semantic relevance, flexibility in fine-tuning
5. Same group to reconvene next week to review co-designed artifact, then determine milestones

### Zihao's Terminology (Important Anchor)

- **Base CLR**: Current HF CLR model
- **UPP CLR**: After co-design, a CLR model that incorporates P2P LR's context pin tower design on top of the Base CLR
- **Rationale**: Building on Base CLR preserves the cross-surface foundation (HF, BMI, Notif) and generalizes more naturally when expanding to P2P and other surfaces

### Cross-Surface Work in Parallel

Cross-surface dataloader deep dive scheduled (Alekhya benchmarking Option A vs B) to help unblock cross-surface training.

### Assessment

This is an excellent outcome:
- Skipped the CLR vs. P2P LR evaluation entirely
- Went straight to co-design with CLR as the base
- Jinfeng gets co-ownership (named POC on redesign) — addresses pride-of-authorship concern
- Framing shifted from "whose model wins" to "what do we build together"
- Team (Zihao, Krystal) owned the room without James present — reflects well on leadership

### Post-Meeting Watch Items

- **Krystal's warning**: "Let's see if we don't re-litigate next week." The co-design review is where Jinfeng could steer architecture back toward P2P LR with CLR elements rather than CLR with P2P elements.
- **Dhruvil's observation**: P2P may treat this as "one-off experiment" rather than "serious try." Yihong's bandwidth is the real execution risk.
- **The go/no-go milestone cuts both ways.** Set it far enough out that P2P's IC has time to make it a fair test. Notifs took ~4 months from skeptic to believer.
- **Ranking already landed on one base model** (CFM cross-surface). If Retrieval ends up with two, that's an inconsistency in the UPP thesis that Jeff will notice.

---

## 13. Must-Win Talking Points (March 30)

### Operating Principles for the Room
- **Role:** Practitioner with shipped results. Not the advocate, not the strategist — that's Dylan and Rajat.
- **Airtime:** 1-2 chances max. If past sentence four, past your window.
- **Posture:** Collaborative framing in every line. Credit SSJ people by name. Frame all work as joint.
- **Discipline:** Speak on execution/feasibility questions (your lane). Stay quiet on product, political, and director-level alignment questions (not your lane).
- **Intel collection:** Even when silent, watch Jeff's body language on UPP, Kurchi's engagement level (quiet = dangerous), what Rajat emphasizes, and any new objections from Vicky.

### Top 5 Lines (Collaborative Framing, Priority Order)

**#1. Co-design update (PROACTIVE — seek one moment for this)**
> "Jaewon and Jinfeng's teams are co-designing the unified base retriever together — building on our cross-surface foundation and incorporating P2P's context modeling strengths. First review is next week."

Lead with their names. Not "we aligned" or "my team."

**#2. If asked about confidence / "is this real?" (REACTIVE — short version)**
> "On the retrieval side — we've already proven this works. We shipped cross-surface retrieval on Notifications with strong WAU wins, and the same pre-train and fine-tune approach applies to P2P. Jinfeng and Jaewon are co-designing the base retriever to make sure relevance is built in from the start. First review is next week."

Extended version if someone pulls the thread — add: scaling the base model to GPU serving (strong offline results), relevance co-design with Jinfeng's team, and enabling cross-surface training on retrieval for the first time (borrowing from CFM ranking wins).

**#3. If relevance comes up (REACTIVE)**
> "Relevance is a key part of the co-design — Jinfeng's team is co-owning that piece. We already support relevance loss in production on Notifs without regressions, so the foundation is there, but getting it right for Search and P2P is exactly what the joint design work is focused on."

Lead with Jinfeng's ownership. Acknowledge "getting it right" is real work — don't dismiss Kurchi's concern.

**#4. If asked about timeline or risk (REACTIVE)**
> "We're running due diligence in parallel with the co-design. We'll have a clearer picture after next week's joint review — the right milestone structure will come from that."

"Joint review" and "come from that" — defer to the co-design process. Respects Kurchi's "I need data" stance.

**#5. If staffing dependency / "what if P2P can't staff this?" comes up (REACTIVE — don't take the bait)**
> "I can speak to the retrieval side — the co-design of the base retriever is a relatively scoped exercise and is already underway with Jaewon, Jinfeng, and Piyush. First draft next week. The fine-tuning work should ideally be driven by the surface team, so that's where this group should decide."

De-risk without blaming. Don't throw Kurchi's team under the bus even if Jeff is offering the opening.

### What NOT to Do

- Don't relitigate Option 1 vs. Option 2
- Don't mention Jinfeng's earlier pushback or the misrepresentation incident
- Don't get into CLR vs. P2P LR architecture details
- Don't overclaim on timeline — Kurchi's "I need data" stance was reasonable
- Don't answer product questions (Vicky) — that's Dylan/Andrew/Krystal
- Don't comment on director-level alignment questions — thumbs up, let Dylan and Kurchi handle it
- Don't speak just to be heard — silence is fine, it preserves your shot

### The Meta-Point

Retrieval is the only part of UPP with shipped online wins AND active cross-org co-design in progress. Ranking has promising offline signal. Retrieval has production results and a joint team already working. If Dylan needs a proof point that UPP's collaboration model works, James's side of the house is it. Let Dylan use that — James doesn't need to say it himself.

### Mock Q&A Insights (March 29 prep session)
- **Best instinct:** Knowing when NOT to speak. Letting Dylan handle Kurchi's process question. Thumbs-up on alignment check.
- **Key coaching point:** When speaking, lead with conviction + evidence, not technical mechanics. Have short (4-sentence) and extended versions ready. Read Jeff's energy to decide which to deploy.
- **Collaborative framing works:** Every line names SSJ people positively, frames work as joint, positions James as practitioner reporting on collaborative progress.

---

## 14. Key Learnings & Strategic Insights

### On James's Position in Senior Rooms

- Speaking power comes from being the practitioner, not the strategist. Let Dylan/Rajat handle org politics.
- One calm, specific, experience-based answer is worth more than multiple strategic arguments.
- The moment to listen for: any variant of "what's the timeline," "how much eng cost," or feasibility concerns. That's the cue.

### On the CFM vs. UPP Framing

- CFM is an option within UPP (the base ranking model layer), not an alternative to UPP.
- The UPP three-tier hierarchy: Foundation Model → Base Models (Ranking + Retrieval) → Surface-Specific Models.
- SSJ's competing proposal was ranking-only. Retrieval — where the shipped wins are — was the blind spot.

### On Managing Cross-Org Resistance

- Surface teams fear consolidation → layoffs. Never address directly. Reinforce: "UPP unlocks surface teams to do higher-value work."
- Jinfeng's pushback was about pride of ownership and technical preference, not bad faith. Co-design gave him a role.
- Dylan's "one moving variable" reframe was the breakthrough: add a surface (P2P) on the existing base, then iterate on architecture.
- Cross-surface training data is the shared work that sidesteps the architecture debate — both options need it.

### On Escalation

- James surfaced the right questions to the right people at the right time and let them act. That's effective escalation.
- Flagging Jinfeng's misalignment to Dylan was factual, not emotional — and it worked.
- The message to Dylan/Matt/Andrew created the forcing function for Rajat's intervention. None of that happens if James negotiates with Jinfeng directly.

### On Kurchi

- She's reasonable AND political — both are true simultaneously. "I don't know how anyone can decide without data" is fair AND maintains her optionality over architecture decisions.
- Political veteran who has survived multiple VPs of Discovery. Has leverage beyond Rajat's chain (likely directly with Jeff). Can push back on Rajat and make it stick (moved Search from monthly milestones to H2).
- Her core motivation: be the originator of technical strategy, not the adopter. Relevance is her differentiator — the one area where SSJ leads and personalization hasn't solved it.
- Uses reasonableness as her primary tool — process requests, data demands, design reviews. These are simultaneously fair and strategic.
- Jinfeng is her champion in technical debates. His positions reflect her strategic interests.
- She will not overtly block UPP (Jeff/Rajat too strong), but she will condition, slow-play, and steer toward SSJ ownership of the technical direction.
- James's meta-goal with Kurchi: shift from "Rajat's battering ram" to "the practitioner who made SSJ's surfaces better."
- Krishna (her most trusted lieutenant) is a strong trust channel — James has good direct rapport with him.
- The relevance doc addressing her BMI/Notif questions was the right move — evidence, not promises.

### On Timing and Staffing

- Piyush returns March 25, must-win is March 30. Five days of overlap. Tight but manageable.
- Notifs took ~4 months from skeptic to believer. The go/no-go milestone for P2P needs to account for a similar ramp.
- If the milestone is set too early and results are underwhelming due to underinvestment, Option 2 advocates get their evidence.

---

## Appendix: Full Stakeholder Map

### Internal Team (P13N / UPP)

| Person | Role | Notes |
|--------|------|-------|
| James Li | Sr. EM, Retrieval Lead | Owns UPP Retrieval. Only person with shipped cross-surface retrieval wins. |
| Dylan Wang | Director of Eng | James's manager. UPP internal champion. Pre-aligned with Jeff. |
| Piyush Maheshwari | TL, Technical Anchor | Returning from OOO ~March 25. Key for must-win technical depth. |
| Zihao | IC, transitioning in | Delivered strong meeting summary. Anchored "UPP CLR" terminology. |
| Dhruvil | Ranking counterpart | Observed P2P treating this as "one-off experiment." Valuable strategic eye. |
| Bowen | UPP context source | Suggested merging CFM/FM terminology for simplicity. |

### Cross-Org (SSJ / P2P / Search)

| Person | Role | Notes |
|--------|------|-------|
| Rajat | VP of Eng | Strong supporter. Forced "disagree and commit" on Option 1. |
| Kurchi | Search Sr. Dir | Key skeptic but reasonable. Wants data. Concerned about semantic relevance. |
| Huizhong | P2P Director | Making things difficult. Shut down pre-wiring attempts. |
| Jinfeng | P2P ML Lead | Pushed for P2P LR as base. Misrepresented alignment. Now co-designing UPP CLR. |
| Sai | P2P IC | Silent throughout. Following Jinfeng's lead. |

### ATG (External Support)

| Person | Role | Notes |
|--------|------|-------|
| Jaewon Yang | ATG ML Lead | Key ally. Technically credible with both sides. |
| Hongtao | ATG IC | Named POC for UPP CLR co-design implementation. |
| Matt Lawhon | ATG | Clarified CFM/CLR technical distinctions in Slack thread. |

### Exec / Leadership

| Person | Role | Notes |
|--------|------|-------|
| Jeff | VP of Core | Decision-maker. Both orgs report to him. Kingmaker. |
| Vicky | Product VP | Co-audience with Jeff. Needs clear ROI. |
| Andrew Yaroshevsky | Sr. Dir Product | Dylan's counterpart. "We've seen this rodeo before." |
| Matt Chun | Product | "Learning agenda" framing. Long-term: base ranker = ranking CFM, base retriever = retrieval CFM. |
| Krystal Benitez | PM | Drove action items in Wednesday meeting. "Let's see if we don't re-litigate." |

---

## Appendix: Key Slack Conversations

### Internal UPP Technical Alignment (CFM/FM/CLR Terminology)

James posted the three-tier hierarchy to align the team:
1. Foundation Model: user-level next token prediction
2. Base Ranker / Retriever: cross-surface base models (CFM is one option for this layer)
3. Surface-level Rankers and Retrievers

**Piyush** confirmed: "yes CFM is 2."

**Jaewon** clarified: base models can take CFM's transformer output instead of FM outputs.

**Matt Lawhon**: "The most obvious path forward here is there is only one base model per category (ranking or retrieval) and the pretraining is sufficiently general that no other base models are required in the category."

**Matt Chun** summarized: "In the long run: base ranker = ranking CFM, base retriever = retrieval CFM."

**James's preference**: "I would prefer 2b first (augment base CLR with CFM-style training), and if that doesn't work, then consider 2a (separate models). Main rationale would be less model maintenance and better dev velocity as per our UPP goals."

### Jinfeng's Pushback Sequence

**Jinfeng** (in channel): "I chatted with Dylan and Kurchi, and we agreed that starting with the P2P LR model as the backbone for the unified base retriever."

**Dylan** (to James, privately): "This is confusing." → "That's not what I agreed."

**James**: "At this point, for tomorrow's meeting it's best if you're there instead of me."

Dylan and Kurchi added to the thread → Kurchi proposed design review of both approaches → Dylan pushed for focus and committing to one approach → Kurchi pushed back wanting data → Agreed to discuss in Wednesday meeting.

### Resolution: Co-Design (Wednesday Meeting)

**Krystal's summary of decisions:**
- Skip CLR vs. P2P LR evaluation (not apples to apples)
- Co-design UPP CLR (CLR + P2P context tower)
- POCs: Jaewon, Jinfeng, Piyush, Hongtao, plus P2P engineer TBD
- Success criteria: no regression on semantic relevance, flexibility in fine-tuning
- Reconvene next week to review co-designed artifact
