# Dylan 1:1 Log

> Rolling log of 1:1 conversations with Dylan. Captures key decisions, signals, and action items for cross-session continuity.

---

## 2026-04-03 (Thursday) — Dylan 1:1 Debrief

**Outcome: Strong.** AI momentum confirmed. Dylan actively shielding James. PM tone feedback delivered.

### What happened

**AI / PINvestigator:**
- Dylan pushed a PINvestigator PR at 11:30pm the night before, chased James + JJ to land it next morning. Senior Director writing code — extraordinary signal.
- Majority of 1:1 spent on AI. Dylan is genuinely excited.
- Dylan wants to shield James from unproductive cross-org conversations (e.g., ELT/Ads Dynamic Triggering with Kartik). "Let Mehdi drive, you focus on AI." This is active portfolio curation — Director-level treatment.
- Dylan said her other directs aren't stepping up on AI the way James has. She's going to try to get them to do the same. **Clear peer differentiation signal.**
- "Run things by me" — she wants to co-own the AI narrative. Feed her first looks on ideas.
- Showed James asking her for code paths/pointers to model codebases — she's learning from him. Guide relationship solidifying.
- Logging work (Alok/CSI for Cupcake) = what Roberto built for Search, but for Homefeed. Dylan very supportive. Extend to BMI/GULP.
- Reflex: very supportive. Darren willing to fund Evals help. All of this is foundation for Reflex vision.

**Yan / Ownership:**
- Yan stepping up is a friendly gesture — good for James since team is stretched.
- Agreed to showcase Yan's proposal to tech leads for technical comments, then go from there. Collaborative approach.

**PM tone feedback:**
- Some newer PMs (Akshanta, Lili Li) have told Dylan that James's tone could be better when they approach him with asks.
- Dylan delivered softly. Specifically flagged Akshanta as someone she thinks is good — meaning the source is credible.
- James committed to watching his tone with newer PMs.
- Root cause: two incidents — (1) James told Lili to back off from pinging engineers for mundane tasks (in front of TPMs, came off strong), (2) Slack to Akshanta routing her through Crystal instead of pinging engineers directly (text-only, no warmth).
- Action: James will send a warm DM to Akshanta opening a door. Lighter touch with Lili — just be warmer in future interactions.

**EM Hiring:**
- Started sourcing, intake last week, working with Daniel McCray again.
- Leadership round interviewers: Dylan, Jiajing, Bo (will ping), Krishna.

**Health:**
- Dylan told James to take more time off for kidney stone recovery as needed. James is determined to be present.

**UPP Retrieval Strategy (FYI from notes):**
- 5-prong approach: Scale HF/Base CLR (GPU serving), Cross-surface Training (Zihao driving, Piyush/Hongtao/Jaewon supporting), ReDesign CLR with P2P (Piyush), Notif & Finetuning (Hongtao's major Q2 project), Finetuning models for HF+BMI (junior end-to-end opportunity).
- ELT presentation → Kartik asked to connect with Ads on Dynamic Triggering. Mehdi Ben Ayed will drive. Dylan shielding James from this.
- Cost asks (Adaptive and GPU) are fine.

### Signals summary
| Signal | Meaning |
|--------|---------|
| PR at 11:30pm + morning chase | Dylan is personally invested in PINvestigator, not just supportive |
| "Shield you from unproductive convos" | Active portfolio curation — she's managing the environment around James |
| "Other directs not stepping up on AI" | James is differentiated among peers on this dimension |
| "Run things by me" | She wants to co-own the AI narrative — managing-up opportunity |
| PM tone feedback (delivered softly) | Real but not severe — she's doing him a favor by surfacing it early |

---

## 2026-04-03 (Thursday) — PREP NOTES (pre-meeting)

**Context:** MW and ELT presentations landed well (March 30). Bowen departed March 26. James recovering from kidney stone surgery (post-op checkup Thursday morning). PINvestigator had a breakthrough day on April 1 — Dylan personally ran the tool, spent ~5 hours engaging with it, called the investigation doc "great," proactively suggested sharing with Karim/PADS, and wants James to show her skills in the 1:1. The AI/IC concern is effectively dead — Dylan is now pulling James in as her AI guide. Dylan moved the 1:1 to BEFORE the group sync.

**Operating frame:** Three-beat managing up (share what's hard → show how you're crushing it → enlist her help). Reduce her cognitive load. Don't pitch; plant seeds. The AI seed is already planted — today watered it.

### Priority Stack (1:1)

---

**1. AI / PINvestigator (she'll likely bring this up — ride the momentum)**

*Strategy:* Dylan wants a live walkthrough of skills/CC setup ("I will ask some question in 1:1"). Let her lead. This is a relationship-building moment disguised as a tech question. Be the guide, not the pitcher.

**If she asks for a CC walkthrough:**
> Show her what she asked for. Help with MCP setup issues. This is time well spent — she's investing in the tooling your team built.

**Natural bridge to Reflex (only if the conversation flows there):**
> "By the way, this investigation capability — diagnosing funnel issues with LLM-powered analysis — is exactly what Andrew's Reflex vision is about. He's invited me to co-own the sensing layer. Darren's contributing eval support. Worth leaning into, or are there landmines I'm not seeing?"

**If she asks about time investment:** "Pinsight v0 is a 10-hour timebox, then handing off to Alok. The architecture builds on the UPP data logging the team already built."

**If she probes on IC direction:** "This is management capability — building the tooling layer that makes the team's debugging faster and connecting it to Andrew's cross-functional vision. I'm architecting, not coding full-time."

**Key:** Don't over-narrate the PINvestigator win. She experienced it firsthand. She doesn't need you to explain the value — she felt it. If anything, use the moment to show you're thinking about scale: "JJ's already connecting with PADS. The question is how we make this available beyond just our team."

---

**2. Yan / Ownership — Pre-Sync Alignment (she may want to align with you before the group meeting)**

*Strategy:* Dylan moved the 1:1 to before the sync. She may want to hear your position privately first — either to pre-align or to test your posture before putting everyone in a room. Be ready for both.

**TL feedback (collected):**

| Person | Key input |
|--------|-----------|
| **Devin** | Contain CG scope. GULP CG scope = HFContextualGraphBuilder only. Everything outside (how request reaches the file, etc.) should be Experience or CSI. |
| **Bella** | Separate maintenance vs development. Development can be owned by Curation (Yan's team). Backend resourcing hard to justify from CG. CG can provide extensive onboarding/guidance at first. Same GULP scoping as Devin. |

**Synthesis — James's position:**
- CG scope should be contained to what's core: HFContextualGraphBuilder for GULP, and retrieval/ML-specific services
- The "how the request reaches the file" layer — routing, explore seeds, surface-specific glue — should move to Experience (Yan) or CSI
- Separate maintenance (keep the lights on) from development (new features). CG can maintain what we've built, but new development for Explore/IB surfaces should be Yan's team
- CG offers onboarding/guidance through the transition — generous, time-bounded, same posture as before

**If Dylan asks "what's your read before we go in?":**
> "My team's feedback is consistent — we should contain CG scope to the ML/retrieval core. The routing layer, explore seeds, surface glue code — that's a natural fit for Yan's team since they own the surfaces. We're happy to support the transition with onboarding. The main thing I'd push for in the meeting is separating maintenance from development — we can keep things running, but new surface work should be resourced from Yan's team."

**If Dylan asks about friction/collaboration:**
> "The IC-level friction is a symptom of the ambiguity, not a people problem. Devin and Dhruvil's team have equally blurry boundaries but zero conflict — the difference is working relationship density. Once we clarify ownership and get Yan's engineers into the code alongside ours, the collaboration follows."

**What NOT to raise in the 1:1:**
- AJ specifically (save for Yan 1:1)
- Yan's operating style or doc quality
- Anything that sounds like territory defense

---

**3. UPP Next Moves (forward-looking, not MW debrief)**

*Strategy:* MW landed. Don't debrief — use it as a launchpad. Show the four active workstreams with owners and momentum.

> "MW landed well. On the retrieval side, here's where we are and where we're going."

**Four active workstreams:**

| Stream | Owner(s) | Status | What's next |
|--------|----------|--------|-------------|
| Cross-surface training | Zihao leading, Piyu guiding, Pengtao + Jaewong supporting | Ongoing | Continued execution — this is the platform proof point |
| Base CLR scale-up | Devin | In progress | GPU serving — scaling the foundation |
| Foundation Model in CLR | Sujie + Hongtao | Strong offline gains | Needs to go online. Working closely with them. |
| P2P co-design (Piyush + Jiaqing) | Piyush + Jiaqing | Design doc phase | Incorporating P2P semantic relevance + query pin best practices into CLR. Jinfeng and Sai are bought in since Monday's conversation. |

**On the P2P co-design (if she probes):**
> "Piyush has been out and Jiaqing's team wanted to know if we're taking P2P input seriously — semantic relevance, query pin handling, all the best practices from their side. I told them absolutely, this only works if they feel like co-owners. Jinfeng and Sai are a lot more collaborative since that conversation."

**The one ask (if appropriate):**
> "Anything I should know about Kurchi's read post-MW? I want to make sure the design review this week goes smoothly."

---

**4. EM Hire (FYI — two sentences)**

> "EM hire is moving — intake is done, recruiter is engaged, pipeline is building. Nothing I need from you right now. I'll flag it if I hit a blocker."

---

**5. Team Pulse (status report — end with "nothing I need from you")**

> "Team is stable post-Bowen. Three things I'm watching:
> - Bella OOO for 3 weeks starting April 6. RecGPT coordinated through YiPing directly.
> - Piyush is back and already engaging on UPP. First 1:1 Monday.
> - Handling Yuke's EB1 sponsorship — that's his main retention anchor.
> Nothing I need from you on any of this."

---

### Read-the-Room Guide

| If Dylan seems... | Adjust by... |
|-------------------|-------------|
| Excited about PINvestigator / AI | Ride it. Spend time on the walkthrough. Plant the Reflex seed. Save UPP for async. |
| Focused on Yan pre-alignment | Give her your position cleanly. She's preparing for the group sync — make her job easy. |
| Rushed / low energy | Quick Yan pre-align + EM FYI only. Everything else can wait. |
| Engaged / strategic | Go deep on UPP workstreams. Bridge AI → Reflex → platform story. |
| Probing on health/sustainability | Be honest, brief, forward-looking: "I'm good. The team held while I was out — that's the signal that the system works." |

---

## 2026-04-03 (Thursday) — Group Sync: Unity-HF Ownership Proposal (after 1:1)

**Room:** Dylan (decision-maker), Dhruvil (GULP owner), Yan (doc author), James

**Dylan's intent:** She convened this to resolve ambiguity. She'll have heard James's position in the 1:1 already. The group sync is for alignment, not discovery.

### James's Posture: Collaborative Senior Partner

Tone is already set from Slack. James is the most tenured EM in the room. The Director-altitude move is elevating from ownership lines to org capability.

### Talking Points (in order of priority)

**1. Open supportive**
> "I think this doc is a great starting point — Yan's team taking more ownership here is the right direction. I've talked to Devin and Bella and the high-level alignment feels close."

**2. Anchor on what the org needs (the elevation move)**
> "The Cupcake fire this week showed that no team has deep expertise in the routing/explore-seeds path. My team stepped in because we were adjacent. The bigger question is: how do we build real expertise in this area? That benefits everyone."

**3. Propose the maintenance vs development split**
> "One framing that came up from my TLs: separate maintenance from development. CG can maintain what we've built — keep the lights on. But new development for Explore and IB surfaces should be resourced from the team that owns those surfaces. We can provide onboarding and guidance through the transition."

**4. Contain CG scope clearly**
> "For GULP specifically, CG scope is HFContextualGraphBuilder. The routing layer, how requests reach the file, explore seeds — that's a natural fit for Experience since they own the surfaces."

**5. Pin down the label**
> "'Relevance-side Unity-HF owners' appears throughout as primary owner. Can we map that to a specific team so scope doesn't land somewhere by default?"

### What NOT to Do
- Don't bring up AJ/Devin friction — that's a Yan 1:1 topic
- Don't re-litigate things Dylan already resolved in the 1:1
- Don't over-talk. Make your points, let Dylan drive.
- Don't propose what Dhruvil's team should own — let him speak for himself

### Watch For
- **Dylan's energy** — did the 1:1 already resolve her questions? If so, the group sync may be quick.
- **Dhruvil's position** — is he trying to shed scope, claim scope, or stay neutral?
- **Yan's response to the maintenance/development split** — does he accept development ownership or push back on resourcing?

---
