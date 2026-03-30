# Q2 2026 Roadmap & Structural Plan

> Last updated: 2026-03-27
> Status: Active planning. Bowen departed March 30. EM backfill in progress. 17 direct reports.

---

## Context: The Q2 transition

Bowen Deng (M16 EM, UPP Retrieval) departed Pinterest on March 30, 2026 for OpenAI. This was a management headcount gap, not a technical crisis — Piyush already held retrieval architecture context. James now manages 17 reports directly while hiring an experienced EM.

The Q2 story is about what was built, not who left.

---

## 1. Project Staffing & Priorities

### UPP — Top Priority (Never drop)
- **Staffing:** Piyush (TL), Zihao, Sophia, Devin (indirect via CLR + direct), ATG team, Ryan (from April)
- **Q2 Goal:** At least one surface beyond Homefeed has working UPP integration with measurable results by end of June
- **Strategic context:** Dylan's #1 priority. Centerpiece of Director case. Cross-surface expansion is what makes UPP a platform thesis.

### RecGPT — Strategic Alliance with ATG
- **Staffing:** Bella (TL), Yuke (partial), Hanlin (stays, mid-April checkpoint)
- **Q2 Goal:** One production-quality generative retrieval result + ATG proactively wants to invest more
- **Drop conditions:** Reduce to maintenance if ATG pulls back or technical approach hits fundamental wall

### Retentive Recs / p(UIC) — Andrew's Anticipation Story (Never drop)
- **Staffing:** Yuke (TL), Chuxi (primary, promo vehicle), Yidi
- **Q2 Goal:** p(UIC) model integrated into anticipation flow with measurable retention improvement. Andrew can demo to CTO with real data.
- **Scaling back:** Would reduce personal involvement only if Yuke can own Andrew relationship directly (H2 at earliest)

### CLR — UPP Backbone (Never drop)
- **Staffing:** Devin (TL), Ryan (from April)
- **Q2 Goal:** CLR improvements contribute measurably to UPP cross-surface performance. Devin's leadership is visible.
- **Note:** GULP asks deprioritized with Dylan's air cover.

### LWS — Lightweight Scoring
- **Staffing:** Yali (de facto owner), Hedi, Zili
- **Q2 Goal:** Continued steady gains. Yali feels recognized.
- **Drop conditions:** Would deprioritize if forced to consolidate. Yali's time redirected to UPP or Retentive Recs.

### Real-Time & L1 Utility — JJ's Promo Vehicle (Never drop before promo decision)
- **Staffing:** JJ (TL, absorbs L1 Utility from David in April)
- **Q2 Goal:** JJ promoted to IC16 by end of June.

### PhP / Dynamic Triggering — Conditional
- **Staffing:** Alok (contributor), Mehdi (ATG IC17, conditional), Darren's infra team (conditional)
- **Funding gate:** CTO presentation end of March. All three conditions (presentation lands, Mehdi leads, Darren commits) must be met.
- **Drop conditions:** Immediately if any condition unmet.

### Content Exploration — Low Priority
- **Staffing:** Zihao (~50%), Yidi (fractional)
- **Q2 Goal:** Zihao demonstrates basic project leadership.
- **Drop conditions:** First cannibalization target when UPP needs bandwidth.

### AI (Pinvestigator, Pinsight) — James as TL
- **Staffing:** JJ (Pinvestigator, partial — promo credit), Charlie (under James)
- **Q2 Goal:** Pinvestigator path to production. Pinsight working prototype. Both framed as team capabilities.
- **Drop conditions:** Would not drop Pinvestigator. Scale back Pinsight if cross-team commitment weakens.

### Summary of People Moves
- Charlie → AI projects (under James's direct TL supervision)
- Hanlin stays on RecGPT (fallback to LWS if Bella escalates, hard mid-April checkpoint)
- Ryan (April) → GULP/CLR with Devin, spare bandwidth to UPP infra

---

## 2. Performance Decisions (Deferred to Mid-Q2)

| Person | Checkpoint | Action if not met |
|--------|-----------|-------------------|
| Charlie | Producing under direct supervision? | Clearest case for action |
| Hanlin | Shipping by mid-April? | Moves to LWS |
| Sophia | Improving under Piyush? | Performance conversation |
| Zili | Monitor via Piyush | Act if Yali flags |

Sequencing: Charlie first. Start the clock so by H2 there are options. Begin after Dylan air cover (Ask #3) and transition stabilization (mid-April).

---

## 3. Team Management Operating Model

### 1:1 Cadence

**Tier 1 — Weekly, 25 min:**

| Person | Slot | Workstream |
|--------|------|-----------|
| Piyush | Tue 3:00pm | UPP |
| Bella | Mon 10:30am | RecGPT |
| Devin | Tue 3:30pm | CLR |
| JJ | Tue 4:00pm | Real-Time, Pinvestigator |
| Yuke | Thu 2:00pm | Retentive Recs |
| Alok | Thu 2:30pm | Real-Time, PhP conditional |
| Chuxi | Wed 4:30pm | Retentive Recs |

**Tier 2 — Biweekly, 25 min:**

| Person | Slot | Workstream |
|--------|------|-----------|
| Zihao | Mon 3:30pm | UPP, Content Exploration |
| Yali | Thu 3:00pm (alternating) | LWS |
| Hedi | Thu 3:00pm (alternating) | LWS |
| Yidi | Wed 4:00pm (alternating) | Retentive Recs |
| David | Wed 4:00pm (alternating) | Departing April |

**Tier 3 — Monthly, 20 min:**

| Person | Slot | Workstream |
|--------|------|-----------|
| Hanlin | Wed 4:00pm monthly | RecGPT |
| Sophia | Fri 3:00pm monthly | UPP |
| Zili | Tue 1:30pm monthly | LWS |
| Charlie | Fri 2:30pm monthly | AI |

**Office Hours:** 1 hr/week, three 20-min slots, Friday 9:30–10:30am.

**Total weekly management time:** ~5.5 hours including office hours.

### Calendar Principles
- Monday mornings protected — white space for thinking, no new 1:1s
- Mornings protected generally — 1:1s batch to afternoons
- Tuesday and Thursday afternoons are primary 1:1 blocks
- 25 minutes means 25 minutes — timer if needed
- Need to reclaim ~2 hours from teal cross-functional meetings to offset new 1:1 load
- Gym and family blocks are non-negotiable

---

## 4. Alternative Org Frameworks (Back Pocket)

**Alternative A — Pod Model** (Emergency fallback if EM hire takes too long)
- 3–4 pods of 4–5 people, each led by TL. James manages TLs only.
- Deploy if no signed EM offer by mid-May.

**Alternative B — Two-Track Org** (Ideal end state for EM hire)
- Production track (UPP, CLR, LWS, Real-Time) goes to new EM.
- Frontier track (RecGPT, Retentive Recs, AI, cross-functional) stays with James.
- This is the Director portfolio. Write the EM JD with this end state in mind.

**Alternative C — Radical Pruning** (H2 preparation)
- Accelerate performance management on Charlie (first) and Zili.
- Start the clock so by H2 there are options.
- Begin after Dylan air cover and transition stabilization (mid-April).

---

## 5. What to Ask Dylan For

1. **EM backfill timeline and ownership (Now):** "I'll draft the JD. Can you get the req opened? Experienced EM, not IC-to-EM. I run the pipeline, bring you in for finals."
2. **GULP protection (Now):** "Ryan covers existing. New asks need your support to push back."
3. **Air cover for performance decisions (Next month):** "I have a few people not at the bar. Can I count on your support for formal performance management?"
4. **Sponsorship into VP-level rooms (Mid-April):** "If there are VP-level conversations about recommendation strategy or UPP expansion, I'd value the chance to be in those rooms."

---

## 6. Risk Mitigation

### Tier 1 — Could Derail Q2

**Must-Win Presentation Doesn't Land**
- UPP expansion to Search/P2P depends on this. Search/P2P ICs explicitly told not to engage until clear guidance.
- Rajat is championing. Monday meeting with Kurchi/Huizhong happened. ICs excited but waiting for permission.
- Mitigation: #1 time investment for next two weeks. Pre-wire Kurchi and Huizhong. Get Piyush into substance day he returns. Frame as what their teams gain.

**JJ's Promo Doesn't Land in June**
- Explicit expectation set. Failure + Bowen departure + AI market = potent combination for JJ to look.
- Mitigation: Start packet in April. Address ML depth gap directly. Understand calibration landscape. Have contingency conversation ready.

**James Burns Out**
- 17 reports, multiple high-visibility workstreams, must-win presentation, AI projects, EM hiring — all simultaneously.
- Burnout signals: patience waning, quiet times filling, evenings and weekends being forced.
- Leading indicators: skipping Monday white space? Walking into 1:1s cold? Canceling gym? Checking Slack after dinner? Sunday evening rumination?
- Emergency lever: activate pod model.

### Tier 2 — Costly but Manageable
- Bowen announcement triggers flight risk conversations (watch Devin in 2–3 week gap before Ryan)
- Alok if PhP deprioritized (keep 20% bandwidth, have alternative scope ready)
- Hanlin continues not shipping (hard mid-April checkpoint, tell Bella it's real)
- Search/P2P ICs blocked by inertia even after presentation (follow up with Kurchi/Huizhong within 48 hours)
- EM backfill takes longer than 6 weeks (mid-May tripwire: design pod model)

### Tier 3 — Monitor
- DaFang leaves (Dylan's problem, have steady message ready)
- Stock continues declining (comp math changes, retention pressure)
- Andrew's anticipation story loses CTO attention (diversify cross-functional visibility)
- Multiple performance situations escalate simultaneously (sequence: Charlie first)

### Monthly Tripwire Calendar

**April 1:** Piyush absorbed UPP? Presentation landed? Ryan onboarding? Team mood? Burnout indicators?

**May 1:** EM offer signed? UPP progress? Hanlin shipping? JJ packet drafted? Alok situation resolved? Burnout check?

**June 1:** UPP results ready to show? JJ packet final? Retentive Recs impact? Performance decisions on Charlie/Sophia? EM onboarding? H2 design started?

---

## 7. Team Resilience & Single Points of Failure

### Current Vulnerabilities
- **Piyush on UPP:** Nobody else has full retrieval architecture context. Zihao transitioning but not there yet.
- **Bella on RecGPT/ATG:** Being hedged through YiPing pairing. Manageable if she leaves.
- **Yuke on Retentive Recs:** Chuxi has context but isn't at TL level yet. James would need to step in personally.
- **Devin on CLR:** Ryan and eventually Yichi provide coverage, but Devin is sole deep model expert currently.
- **JJ on Real-Time:** Essentially solo. No coverage if he left post-promo.

### Approach: Invisible Cross-Training
Don't announce a cross-training initiative. Frame every redundancy move as a growth opportunity for the person stepping up.

Specific moves:
- **Zihao → deeper UPP:** Accelerate architectural understanding by pairing with Piyush on design discussions. Framing to Zihao: "build independent decision-making capability." Framing to Piyush: "Zihao needs more context to be effective."
- **Chuxi on Retentive Recs:** Make sure she's in architectural decision rooms, not just execution. If Yuke leaves, she's been hearing the "why" for months.
- **Yali broadening:** Give her one bounded project outside LWS. Collaboration with a different workstream to build range.
- **JJ and Devin:** Redundancy comes from new hires. Ryan covers CLR with Devin (April). Yichi joins July. Natural solution is time.

**Core Principle:** Make every workstream have at least two people in every design discussion. Not as policy — as habit. Invisible cross-training. Nobody feels threatened, nobody feels like a backup, distributed knowledge in six months.

---

## 8. Bella Retention Assessment

### Current Signals (March 2026)
- Told James directly: been at same place 7 years, thinking about leaving this year
- Thinks Meta/Coupang interviews easy to get but not yet actively pursuing
- Would like pay bump (James said he'd try by end of April)
- Will give at least 3 months notice
- 3-week PTO April 6th
- Bowen separately flagged: Bella kept complaining about stock price when she heard his news

### James's Honest Assessment
- Never really connected with Bella. Low relational investment.
- Doesn't create ideas — needs James to architect, then resists.
- Lacks decisiveness, conviction, communication skills.
- Dylan has also lost trust in Bella over Group MP situation.

### Position
Not retaining, not managing out. Keeping things as they are. Extract value while she's here, don't invest retention capital, let her make her own decision.

**Comp commitment cleanup:** Don't go to Dylan for a bump you don't believe in. Tell Bella honestly: "The environment is tough, I'm working on it, no timeline yet." Don't ghost the commitment, don't spend Dylan's capital.

**Before April 6 PTO:** Get RecGPT momentum locked in. Build direct YiPing working relationship that doesn't depend on Bella. Test RecGPT continuity during 3-week absence.

**If Bella leaves:** RecGPT shifts to ATG-led project. Manageable if YiPing pairing is established. Narrative risk (two IC16+ departures) manageable if timing spans quarters.

---

## 9. Chuxi-Devin-Yuke Dynamics

### The Project
Retentive rec signal integration into CLR training data. Natural cross-workstream collaboration. Chuxi has retentive recs context, Devin owns CLR.

### The Tension
- Devin wants to work with Chuxi (asked for strong collaborators)
- Yuke would see Chuxi working closely with Devin as losing his best IC
- Yuke doesn't get along with Devin
- Chuxi's promo vehicle is Retentive Recs under Yuke

### Additional Context: Yuke Flight Risk
Bowen reported Yuke has been asking interview questions about market pay. Unhappy about promo deferral. Short tenure history. Green card process is primary retention anchor.

James is partially designing this arrangement to hedge against Yuke's potential departure — building Chuxi's independence so she can anchor Retentive Recs if Yuke leaves.

### Decision
Project stays anchored in Retentive Recs. Chuxi is the bridge — works with Yuke on signal design, works with Devin on CLR integration. Yuke and Devin don't need to collaborate directly.

**Framing to Devin:** This is a Retentive Recs project that uses and enhances CLR. Ryan (April) and Yichi (July) will work closely with him.

**Framing to Yuke:** Extends his workstream's reach. Retentive rec signal becoming foundational infrastructure is a scope expansion story. Chuxi is still his IC. This is his win.

**Yuke Promo Timeline:** Not ready by mid-year. Needs p(UIC) successfully built and landed. End of year is right window. Frame as strategy, not deferral.

---

## 10. Bowen Transition Record

### What Happened
- Bowen decided to leave for OpenAI (AI-native company motivation)
- Came to James proactively, released him to inform Dylan
- Final round March 9. Committed to stay through Piyush's return from OOO.
- James handled this well — real growth from previous experience (blowing up at a departing report)
- Bowen shared flight risk intel (DaFang considering leaving; Yuke exploring market pay)

### Dylan's Reaction
Much more casual than anticipated. Key points:
- "Bowen prioritizes himself over the team" — not surprised
- Confident in ICs on James's team
- Has open IC17 role willing to sacrifice for EM backfill
- Full confidence in James expressed explicitly
- Probably would not reach out to Bowen for retention

### Outcome
- Backfill path: EM position. Dylan agreed. Clean.
- James suggested bringing DaFang into UPP — Dylan responded well. Walked in delivering problem, walked out co-solving broader org challenge.
- Last day: March 30, 2026.

### Performance Review Outcome (March 2026)
- **Rating:** Exceeds
- **Comp:** $1.2M equity grant over 3 years (up from $450K last year). Total comp ~$1.35M.
- **Feedback:** Be more aggressive and faster in escalating challenges.
- **Director conversation:** Did not happen in this meeting. Natural window: late March / early April.

---

## Q2 Operating Principles

- Monday mornings are sacred. 1:1s are 25 minutes. One evening per week laptop closes by 7pm.
- UPP expansion, Retentive Recs, and AI are where personal time goes. Everything else delegated.
- Anchor every person to their own growth path. The antidote to "should I leave too?" is "here's something worth staying for."
- Bowen's departure is a management headcount gap, not a technical crisis. The Q2 story is about what was built, not who left.
- When the rumination engine starts: name the pattern, ask what's actually true, ask what you can control, take one concrete action, then stop. Let the gaps be gaps.

## Personal Q2 Success Criteria

- Execution stays strong while leaning into AI
- Trust deepens with Andrew and senior leadership (small, specific relationship deposits)
- Team is stable and transition is a footnote
- The feeling of building real things — side projects becoming production systems
- Growing personal relationships with cross-org leaders, even in small pieces
