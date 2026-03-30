# NotebookLM Query Log

> Rolling log of queries sent to NotebookLM notebooks and their outcomes. Helps James see what Leo is consulting, evaluate response quality, and improve query patterns over time.

---

## 2026-03-29 — How to Speak + ELT Presentation

**Notebook:** How to Speak
**Context:** ELT presentation talk tracks (slides 3-5) for CTO + VPs, March 31

**Query 1:** Review talk tracks for "project management narration" vs "visionary leader framing" — apply signposting and strategic framing principles
- **Key insight:** Slide 3 funnel walkthrough is "backstory scope creep." Compress to 1 sentence, let diagram work.
- **Action:** Rewrote slide 3 opening to BLUF the $938K savings in the first 30 seconds

**Query 2:** Apply Robot Voice Method — where is James burying the lead or over-explaining?
- **Key insight:** $6.5M figure buried in slide 5. Leading with logistics instead of selling.
- **Action:** Moved $6.5M to slide 4, restructured slide 5 to open with conclusion

**Query 3:** How should James structure exec Q&A answers? Senior engineer vs executive framing.
- **Key insight:** 3A Pyramid (Answer → Arguments → Add-ons). "I've observed" > "I think" (40% more credible). Don't validate negative frames.
- **Action:** Added Q&A structure to speaking reminders, integrated into communication.md

---

## 2026-03-29 — Improving Leo + System Design

**Notebook:** Improving Leo
**Context:** Evaluating Leo system architecture for improvements

**Query 1:** Highest-leverage improvements for Leo given current structure
- **Key insights:** Context indexing (CLAUDE.md as index), escape hatches, automate context updates in end-session, reverse elicitation pattern
- **Action:** Added escape hatches to CLAUDE.md + skills, enhanced end-session with Phase 4

**Query 2:** What would a practical eval system look like for a personal AI?
- **Key insights:** SOPs/rubrics per task type, test suite of edge cases, human baseline, track escape hatch usage
- **Action:** Added to leo_backlog.md for future implementation

**Query 3:** Meta-prompting workflow for improving CLAUDE.md and skills
- **Key insights:** Prompt folding (feed failures back), end-of-session "what did you learn" debrief, interview technique for building new skills
- **Action:** Added to leo_backlog.md for future implementation
