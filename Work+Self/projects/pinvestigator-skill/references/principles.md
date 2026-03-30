# PInvestigator: Key Investigation Principles

These principles form the core reasoning framework for systematic metric investigation. They guide the agent and human investigators through diagnosing homefeed metric movements.

Principles 1–6 are used by the engagement analysis subagent, listed in order of application (Steps 3 → 4 → 5). Principle 7 is used by the holdout analysis subagent. Principle 8 is used by the Slack search subagent and the orchestrator.

-----

## Principle 1: Contextualize Before Concluding

> **Agent inline:** `prompts/engagement-analysis.md` Step 3 (rate decomposition table implements this principle)

**Never investigate a metric in isolation. Always establish the surrounding context first.**

A metric movement only means something relative to what everything else is doing. If all engagement metrics dropped 3%, a 3% repin rate drop isn't a repin-specific problem — it's a broader engagement shift. But if only repin rate dropped while closeups and hides are flat, that's a signal worth isolating.

**What to check:**

- Are all other engagement metrics moving similarly, or just the target metric?
- Is the movement disproportionate on any single breakdown (surface, RTC, country, platform)?
- How has this metric been trending over the past 30 days?
- What was this metric doing in the same 30-day window last year?

**Example:**

```
Investigation: Repin rate dropped 2.5% WoW

Context reveals:
  Repin rate:    -2.5% WoW
  Closeup rate:  -2.3% WoW
  Hide rate:     +0.1% WoW  (flat)
  Imp/DAU:       +0.2% WoW  (flat)

Conclusion: This is NOT a repin-specific problem. Closeup rate
dropped almost identically. This suggests a broad engagement
quality shift (fewer people engaging deeply) rather than anything
specific to the save action. Investigate what's causing BOTH
repin and closeup rates to decline together.

Contrast with:
  Repin rate:    -2.5% WoW
  Closeup rate:  +0.3% WoW  (flat)
  Hide rate:     +0.1% WoW  (flat)

Conclusion: Repin rate is declining INDEPENDENTLY of other
engagement. Something specific to the save action or save-worthy
content is changing. This is a more targeted investigation.
```

**Reasoning:** Without context, you'll waste time chasing a metric-specific root cause when the real cause is systemic, or vice versa. This is always Step 1.

-----

## Principle 2: Decompose Rate Metrics Into Numerator and Denominator

> **Agent inline:** `prompts/engagement-analysis.md` Step 3 (driver classification: NUMERATOR / DENOMINATOR / BOTH)

**A rate investigation is always two separate questions.**

Rate metrics (repin rate, closeup rate, hide rate) are ratios. A rate can drop because the numerator decreased, the denominator increased, or both. In Homefeed, the denominator is almost always **impressions**, so every rate investigation naturally splits into:

1. **How is the numerator (volume metric) moving?** — e.g., are total repins declining?
2. **How are impressions moving?** — e.g., are we serving more impressions per user?

These are fundamentally different problems with different root causes.

**Example:**

```
Investigation: Repin rate dropped 3% WoW

Decomposition:
  Repins (numerator):      -1.0% WoW
  Impressions (denominator): +2.1% WoW

  repin_rate = repins / impressions
  If impressions grew 2.1% but repins only fell 1%, the rate drop
  is PRIMARILY driven by impression inflation, not fewer repins.

Root cause direction: Why are we serving more impressions?
  → Check impressions/DAU (are users seeing more pins per session?)
  → Check DAU itself (did user mix shift?)
  → Check if a launch increased pagination depth

Contrast with:
  Repins (numerator):      -3.2% WoW
  Impressions (denominator): -0.1% WoW (flat)

Root cause direction: This is a genuine repin volume decline.
  → Check repin rate by content type (fresh vs aged)
  → Check repin rate by RTC (which recommendation type?)
  → Check if save-worthy content distribution changed
```

**Reasoning:** Jumping straight to "why did repin rate drop" without this decomposition leads investigators down the wrong path roughly half the time. The fix for "we're serving too many low-quality impressions" is completely different from "users are saving less."

-----

## Principle 3: Distinguish Gradual Decline From Sudden Shift

> **Agent inline:** `prompts/engagement-analysis.md` Step 4 (CLIFF/DRIFT classification)

**The shape of the metric movement tells you what kind of cause to look for.**

There is a critical difference between:

- **Gradual decline**: A slow erosion over days or weeks, where no single day shows a dramatic change but the trend line is clearly negative
- **Sudden shift**: A clear step-change where the metric was stable, then moved sharply on a specific day

Each pattern points to fundamentally different root causes.

**Gradual declines** typically suggest:

- Slow content ecosystem shifts (e.g., gradual change in content mix)
- Accumulating effects of multiple small launches
- Seasonal drift
- User behavior evolution

**Sudden shifts** typically suggest:

- A specific launch or config change on an identifiable date
- An A/B experiment ramping up
- A data pipeline change
- An upstream dependency change

**Important scope note:** These investigations are for *non-obvious* metric movements. Catastrophic drops from component-level failures (e.g., a service going down causing 50%+ drops) trigger real-time SEVs with their own alerting and investigation process. Pinvestigator handles the subtler movements that don't trigger alarms but still need explanation.

**Example:**

```
Gradual decline pattern (past 14 days):
  Day 1:   repin_rate = 3.42%
  Day 2:   repin_rate = 3.41%
  Day 3:   repin_rate = 3.39%
  Day 4:   repin_rate = 3.40%
  Day 5:   repin_rate = 3.38%
  Day 6:   repin_rate = 3.37%
  ...
  Day 14:  repin_rate = 3.28%

  No single day stands out. The trend is slowly negative.
  → Look for: content mix shifts, multiple small launches,
    seasonal patterns, gradual model drift

Sudden shift pattern:
  Day 1:   repin_rate = 3.42%
  Day 2:   repin_rate = 3.41%
  Day 3:   repin_rate = 3.43%
  Day 4:   repin_rate = 2.18%  ← sharp drop
  Day 5:   repin_rate = 2.17%
  Day 6:   repin_rate = 2.19%

  Clear step-change on Day 4. Metric stabilized at a new level.
  → Look for: What launched or changed on Day 4 or Day 3?
  → Check holdout, Helium launches, config changes on that date
```

**Reasoning:** If you don't first classify the shape, you'll waste time looking for a specific launch date during a gradual decline, or searching for ecosystem shifts when there's an obvious step-change to pin down.

-----

## Principle 4: Normalize for Baseline Variance

> **Agent inline:** `prompts/engagement-analysis.md` Step 5 baseline variance pre-check (z-score gate before ISOLATED classification)

**What counts as a "significant" movement depends entirely on how volatile that metric normally is.**

Different metrics have fundamentally different levels of day-to-day noise. A 1% WoW change in impressions might be highly unusual, while a 1% change in hide rate might be completely within normal daily fluctuation. Without understanding each metric's baseline variance, you'll either:

- Chase noise (investigating normal fluctuations)
- Miss real signals (dismissing meaningful shifts as normal)

**How to calibrate:**

- Look at the daily time series for the past 90 days to understand typical variance
- Look at the same 90-day window last year to account for seasonality
- Compute a simple baseline: what's the typical WoW swing for this metric?

**Example:**

```
Two metrics, both showing -2% WoW:

Metric A: Impressions per DAU
  Past 90 days typical WoW range: -0.5% to +0.5%
  A -2% WoW move is 4x the normal variance
  → This is a SIGNIFICANT anomaly. Investigate immediately.

Metric B: Hide rate
  Past 90 days typical WoW range: -3% to +3%
  A -2% WoW move is within normal variance
  → This is NORMAL fluctuation. Do not investigate in isolation.
  → Only flag if the trend persists for multiple consecutive days

Calibration example:
  Metric    | Typical WoW range | -2% WoW is...
  ──────────┼───────────────────┼──────────────────
  Imp/DAU   | ±0.5%             | 🔴 4x normal — investigate
  Repin rate| ±1.0%             | 🟡 2x normal — monitor closely
  Hide rate | ±3.0%             | 🟢 Normal — don't chase
  Closeups  | ±1.5%             | 🟡 1.3x normal — mild flag
```

**Operational step:** Query the trailing same-day-of-week WoW values for the target metric, defaulting to 12 weeks of samples. If fewer than 12 weeks are available due to data retention constraints, use as many as the data provides and state the sample count. Compute the standard deviation. Express the current WoW change as a z-score (current WoW / std dev). A z-score > 2 warrants investigation; a z-score < 1 is likely noise. This makes Principle 4 actionable rather than purely conceptual.

**Reasoning:** This prevents two costly mistakes: wasting investigation cycles on statistical noise, and failing to escalate genuinely unusual movements because "2% doesn't sound like a lot." Context-dependent thresholds are essential.

-----

## Principle 5: Platform Divergence Signals Client-Side Changes

> **Agent inline:** `prompts/engagement-analysis.md` Step 5 dimensional drill-down (by_app check)

**When a metric moves differently across iOS, Android, and Web, the cause is almost certainly a client-side change.**

Server-side changes (ranking model updates, content policy changes, backend configs) affect all platforms equally because they operate upstream of the client. When you see a metric drop on only one platform (or disproportionately on one), it points to:

- A client-specific app release
- A platform-specific feature launch
- A UI/UX change on one platform
- A client-side bug in a specific app version

**Example:**

```
Investigation: Closeup rate dropped 3% WoW globally

Platform breakdown:
  iOS:      -5.1% WoW  ← disproportionate
  Android:  -0.2% WoW  (flat)
  Web:      +0.1% WoW  (flat)

  Only iOS is affected.
  → This is almost certainly a client-side change on iOS
  → Check: recent iOS app releases, iOS-specific feature flags
  → Check: iOS app version breakdown — is it all versions or
    just the latest release?

Contrast with:
  iOS:      -3.1% WoW
  Android:  -2.8% WoW
  Web:      -3.2% WoW

  All platforms dropped proportionally.
  → This is a server-side or ecosystem-level change
  → Platform-specific investigation is NOT needed
  → Focus on ranking, content, or upstream changes
```

**Reasoning:** This principle lets you immediately narrow the investigation team. If it's iOS-only, you're talking to the iOS client team, not the ranking team. It avoids wasting time on the wrong root cause domain entirely.

-----

## Principle 6: Disproportionate Country Movements Suggest Holidays or Regional Events

> **Agent inline:** `prompts/engagement-analysis.md` Step 5 dimensional drill-down (by_country check)

**When a metric movement is concentrated in specific country groups, ask about holidays first.**

Engagement patterns are heavily influenced by cultural events and holidays. If a metric drops disproportionately in one country group, the most common explanation is a holiday or regional event — not a product change (which would typically affect all countries equally).

During holidays, users typically engage differently: sometimes more browsing (higher impressions) with less purposeful action (lower repins), or sometimes completely reduced activity. The key signal is that **all engagement metrics in that country group tend to move in the same direction.**

**Example:**

```
Investigation: Global repin rate dropped 1.8% WoW

Country breakdown:
  US:          -0.3% WoW  (within normal variance)
  Europe:      -0.2% WoW  (within normal variance)
  Japan:       -7.2% WoW  ← disproportionate
  LatAm:       -0.4% WoW  (within normal variance)
  Rest of World: -0.1% WoW (within normal variance)

Japan deep dive (all metrics):
  Repin rate:    -7.2% WoW
  Closeup rate:  -5.8% WoW
  Hide rate:     -1.2% WoW
  Impressions:   -12.3% WoW
  DAU:           -9.1% WoW

All engagements are down in Japan, including total activity.
→ Check: Is there a major Japanese holiday this week?
→ Answer: Yes — Golden Week. This is expected seasonal behavior.

Contrast with (NOT a holiday pattern):
  Japan repin rate:    -7.2% WoW
  Japan closeup rate:  +0.1% WoW  (flat)
  Japan hide rate:     +0.3% WoW  (flat)
  Japan DAU:           +0.2% WoW  (flat)

Only repin rate dropped in Japan while everything else is stable.
This is NOT a holiday. Something specific changed for Japanese
users' save behavior. Investigate product changes targeting Japan.
```

**Reasoning:** Holiday effects are the single most common false alarm in metric investigations. Checking this early saves significant investigation time and avoids unnecessary escalations.

-----

## Principle 7: Always Cross-Reference the Holdout Time Series

> **Agent inline:** `prompts/holdout-analysis.md` Principle 7 section (full inline of interpretation logic)

**The holdout is your best signal for whether a relevance or product launch caused the movement.**

Relevance changes and product launches at Pinterest are typically gated behind the holdout experiment. The holdout group does NOT receive these changes. Therefore:

- If the metric dropped in the **main population** but is **stable in the holdout**, the cause is very likely a recent launch that's in the holdout
- If the metric dropped in **both the main population AND the holdout**, the cause is something external to launches — ecosystem change, seasonality, upstream dependency, etc.

**Example:**

```
Investigation: Repin rate dropped 2% WoW starting Tuesday

Holdout check:
  Main population repin rate:  -2.0% WoW  (dropped Tuesday)
  Holdout repin rate:          -0.1% WoW  (flat, normal variance)

  The holdout DIVERGED from main population on Tuesday.
  → Strong signal: a launch gated by the holdout caused this
  → Check Helium for what ramped or launched on Monday/Tuesday
  → Cross-reference with holdout metric deltas

Contrast with:
  Main population repin rate:  -2.0% WoW  (dropped Tuesday)
  Holdout repin rate:          -1.8% WoW  (also dropped Tuesday)

  Both dropped nearly identically.
  → The holdout can't protect against this — it's NOT a launch
  → Look for: external factors, upstream changes, content
    ecosystem shifts, holiday effects, data pipeline changes
```

**Reasoning:** The holdout is the closest thing to a controlled experiment for the entire product. It's the fastest way to bifurcate the investigation into "caused by a launch" vs. "caused by something else," which dramatically narrows the search space.

-----

## Principle 8: Always Provide Rationale for Suggestions

> **Agent inline:** `prompts/slack-search.md` output format + `references/report-template.md` Section 3/4

**Never suggest a next step, hypothesis, or conclusion without explaining the specific data or reasoning that led to it.**

Metric investigations are high-stakes — they influence decisions about whether to roll back launches, escalate to teams, or ignore a movement. An unsupported suggestion ("check the ranking model") is worse than no suggestion at all, because it sends investigators on potentially expensive wild goose chases with no way to evaluate whether the direction is sound.

Every suggestion must be a chain: **observation → reasoning → suggestion**. The investigator needs to see the chain to decide whether to follow it, modify it, or reject it.

This applies to:

- Hypothesized root causes
- Suggested next investigation steps
- Recommendations to escalate or dismiss
- Comparisons to past investigations
- Any claim about what's "normal" or "anomalous"

**Example — Good (rationale for every suggestion):**

```
Finding: Repin rate dropped 2.3% WoW.

Observation 1: The drop is concentrated on a single day (Thursday),
  not a gradual decline. This suggests a discrete change, not a
  slow ecosystem shift.
  → Suggestion: Look for launches or config changes on Wednesday
    or Thursday specifically.

Observation 2: Closeup rate is flat (+0.1% WoW), meaning users
  are still tapping into pins at the same rate but saving less.
  This rules out a general engagement decline.
  → Suggestion: Focus on what changed about save-worthy content
    or the save action itself, not engagement broadly.

Observation 3: The holdout shows repin rate is stable (-0.1% WoW),
  while the main population dropped 2.3%. The divergence started
  Thursday.
  → Suggestion: This is very likely caused by a launch gated
    behind the holdout. Check Helium for experiments that ramped
    on Wednesday/Thursday. The holdout divergence is strong
    evidence — prioritize this over other angles.
```

**Anti-patterns to avoid:**

```
❌ "You might want to check X"
   → WHY might I want to check X? What data suggests this?

❌ "This could be caused by A, B, C, or D"
   → Listing every possible cause without ranking or evidence
     is not helpful. Which is MOST likely given the data?

✅ "The drop started Thursday and the holdout diverged on the
   same day (main: -2.3%, holdout: -0.1%). This pattern
   strongly suggests a gated launch caused the movement.
   Check Helium for experiments that ramped Wednesday/Thursday."
   → Observation, reasoning, and specific action — all connected.
```

**Reasoning:** This principle exists because an investigation tool without rationale is just an automation of gut instinct. The entire value of Pinvestigator is that it can process more data dimensions than a human can hold in their head simultaneously — but that value is destroyed if the agent doesn't show how those dimensions connect to its suggestions.
