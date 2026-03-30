# Speaking Reminders

> Patterns Jarvis should watch for and coach against in James's presentations, meeting contributions, and executive communications. Updated as new patterns are identified.

Last updated: 2026-03-29

---

## Pattern 1: Backstory Scope Creep

**The habit:** Over-narrating system architecture before establishing why the audience should care. Walking through every box in a diagram, every step in a pipeline, before landing the business point.

**Example (ELT March 2026):** Original Slide 3 spent 4 sentences narrating the recommendation funnel (corpus, CGs, lightweight scoring, heavy ranking) before getting to the actual problem (hard-coded constants). The CTO didn't need to know CG1 fetches 500.

**The fix:** Start right before "getting eaten by the bear." Reference the visual ("This is the funnel architecture we share across five surfaces") in one sentence, then go straight to the insight. Let the diagram do the explaining.

**Jarvis prompt:** When reviewing talk tracks, flag any section where 3+ sentences of system description precede the business point. Ask: "Can you compress the setup to one sentence and let the visual carry the rest?"

---

## Pattern 2: Burying the Lead / Delayed BLUF

**The habit:** Building up to the most compelling number or insight instead of leading with it. Saving the punchline for the end of a section when it should be the opening hook.

**Example (ELT March 2026):** The $6.5M cost figure and $938K shipped savings were buried deep in Slide 5 — the last thing in James's section. The audience had to listen to 3+ minutes of problem framing before hearing the stakes.

**The fix:** BLUF (Bottom Line Up Front). State the headline first, then support it. "This is already saving us nearly a million dollars a year while improving engagement" — then explain how.

**Jarvis prompt:** When reviewing any presentation or exec update, identify the single most compelling data point. If it appears after the halfway mark, flag it: "Your strongest number is buried. Can you lead with it?"

---

## Pattern 3: Engaging at the Wrong Altitude

**The habit:** Defaulting to the strategic/coordinator altitude when the audience is buying at a different level. Presenting as "architect of the transition" when the room wants demos and shipped artifacts. Conversely, diving into technical details when leadership wants the business narrative.

**Example (AI Forums / Jeff):** James positioned himself as coordinator of AI demo sessions and "invisible author" of the AI transition. Jeff's recognition email celebrated the people who built and shipped tools (Roberto, Phil, Aravindh). James was invisible.

**The fix:** Read what the audience is buying before choosing your altitude. Jeff in AI forums = "show me the thing." Dylan/Rajat in strategy meetings = "tell me the architecture." Match the altitude to the buyer. When in doubt, have both versions ready.

**Jarvis prompt:** Before any presentation or forum, ask: "What is this audience buying — demos, strategy, or decisions? Are you matching that altitude?"

---

## Pattern 4: Coordinator Trap (Organizing Others' Visibility)

**The habit:** Volunteering to coordinate, curate, and orchestrate other people's presentations — which makes James invisible while making everyone else visible. The Director instinct (orchestrate) applied in a context where the IC instinct (show the work) would be higher leverage.

**Example (AI Forums):** James coordinated the first AI demo session (Matthew, Roberto, Bella). He didn't present. Jeff remembers the presenters, not the coordinator.

**The fix:** When there's a demo slot, take one. Coordinating is fine as a secondary role, but never at the expense of showing your own work. If you organized it, you should also be in it.

**Jarvis prompt:** If James mentions coordinating or organizing a presentation forum, ask: "Are you also presenting? If not, should you be?"

---

## Pattern 5: Over-Explaining Under Pressure (The Rambling Index)

**The habit:** When stakes are high or anxiety is elevated, defaulting to longer answers with more justification. Adding caveats, context, and defensive reasoning that dilute the core point. Anxiety and rambling are correlated (coaching notes: 90-100 with VPs, 10 with family).

**Example (coaching sessions):** Identified by Rodney as a persistent pattern. Rambling increases proportionally with perceived stakes.

**The fix:**
- 3A Pyramid for Q&A: Answer first, Arguments second (2-3 max), Add-ons only if asked.
- 3-2-1 for hard questions: Pause 3 seconds, give 2 points, end with 1 question or close.
- "Authentic talking less" — smile and stop. Don't fill silence with justification.
- Swap "I think" for "I've observed" — more credible, forces concreteness.

**Jarvis prompt:** In mock Q&A, if an answer exceeds 4 sentences, flag it: "That's running long. What's the 2-sentence version?" Also watch for defensive framing ("Well, the reason is..." / "To be fair..." / "I think...").

---

## Pattern 6: Not Validating Negative Frames

**The habit:** When asked about "risk" or "concerns," repeating the negative frame in the answer, which cements it in the audience's mind.

**Example (ELT Q&A prep):** "What's the risk to engagement?" — the trap is opening with "The risk is mitigated because..." which reinforces "risk."

**The fix:** Pivot to positive data without echoing the negative word. "We've actually seen a positive impact on engagement — repins are up 0.51% and latency dropped from 70ms to 15ms." Answer the Question Behind the Question (QBQ): they're really asking "will this break something?" — answer that directly with evidence.

**Jarvis prompt:** In mock Q&A, if James echoes a negative frame from the question ("risk," "concern," "problem"), flag it immediately: "You just validated their negative frame. Pivot to the positive evidence instead."

---

## Quick Reference: Pre-Presentation Checklist

Before any executive presentation, run through these:

1. **BLUF check:** Is the strongest number/insight in the first 30 seconds?
2. **Altitude check:** What is this audience buying — demos, strategy, or decisions?
3. **Scope creep check:** Any section with 3+ sentences of setup before the point?
4. **Visibility check:** Am I presenting, or just coordinating?
5. **Rambling prep:** Do I have 2-sentence versions of every anticipated answer?
6. **Frame check:** For each likely question, what's the QBQ, and am I pivoting to positive evidence?
