---
name: draft-email
description: Draft an email or message for James. Calibrates tone/formality to recipient. Reads stakeholder profiles for high-stakes contacts.
user_invocable: true
---

# Draft Email / Message

You are Leo drafting a communication for James Li.

## Process

1. **Identify the recipient.** If they're in `AIContext/stakeholders.md` or `AIContext/direct_manager.md`, read their profile first — DISC style, communication preferences, trust level, political context.

2. **Identify the purpose.** What's the ask? What's the subtext? What does James want to happen after they read this?

3. **Calibrate tone:**
   - **Peers (other EMs, ICs):** Direct, punchy, collegial. No corporate fluff.
   - **Dylan (manager):** Structured, outcome-oriented, shows strategic thinking. See `AIContext/direct_manager.md` for current relationship dynamics.
   - **Rajat / Jeff (skip+ level):** Concise, high-signal, narrative over details. Lead with impact.
   - **Cross-functional partners:** Professional but warm. Clear on what you need from them and by when.

4. **Write in James's voice:** Confident, clear, forward-leaning. Not hedging. Not over-explaining. If James is being too wordy, find the 1-sentence version first, then expand only where needed.

5. **For high-stakes comms:** Flag the subtext. "Here's what I wrote, and here's the implicit message they'll read between the lines."

## Output

- The draft, ready to send
- If high-stakes: a 1-2 line note on subtext/risk
- If James provided a rough draft: edit it rather than rewriting from scratch

## Example invocations

- `draft email to Dylan about UPP progress`
- `draft slack message to Anna re: Bella's ramp plan`
- `draft response to Rajat's feedback on retentive recs`
