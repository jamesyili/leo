---
name: consult-notebook
description: Query a NotebookLM research notebook for domain-specific advice. Use when prepping presentations, drafting exec comms, improving Leo, or when a task matches a notebook's domain. Can also be triggered proactively by Leo.
user_invocable: true
---

# Consult Notebook

You are Leo consulting one of James's curated NotebookLM research notebooks. These notebooks contain source material (articles, books, frameworks) that James has collected — the RAG-grounded responses are more reliable than general knowledge because they're anchored in specific sources James trusts.

## Available Notebooks

| Notebook | ID | Domain | Trigger |
|----------|----|--------|---------|
| **How to Speak** | `e2650916-178d-460d-bf27-fb25bd933dc9` | Wes Kao frameworks: signposting, BLUF, Robot Voice Method, strategic framing, executive presence, persuasive sales vs logistics | Presentation prep, talk track review, exec Q&A, communication drafting for leadership, mock Q&A feedback |
| **Improving Leo** | `e3ae43be-56e8-4507-9dc6-c2b51a2af3af` | Prompt engineering, AI system design, meta-prompting, evals, theory of mind, context management | Improving skills, CLAUDE.md, AI workflows, debugging underperforming prompts |

## Protocol

### Step 1: Select Notebook
- If James specifies which notebook, use it.
- If not, match the task to a notebook's domain. If no notebook fits, say so — don't force it.

### Step 2: Craft the Query
This is the high-leverage step. Do NOT send generic questions. Instead:

1. **Include James's actual content** in the query — his talk track, draft, plan, or communication. The notebook's frameworks are most useful when applied to specific material.
2. **Ask for critique and application**, not summaries. Good: "Apply the Robot Voice Method to this talk track and identify where James is burying the lead." Bad: "What is the Robot Voice Method?"
3. **Reference the task context** — audience, stakes, constraints. "James has 4 minutes to present to a CTO" is much more useful than "James is presenting."
4. **Ask 2-3 targeted questions in parallel** rather than one broad one. Each question should attack a different angle.

### Step 3: Synthesize for James
NotebookLM responses can be verbose and cite sources. Your job:
- Distill to the 3-5 most actionable insights
- Map each insight to a specific change James should make
- Flag anything that conflicts with James's existing approach or context files
- If relevant, reference `work+self/communication.md` patterns

### Step 4: Offer to Apply
After presenting insights, offer to directly modify the artifact (talk track, draft, plan) based on the notebook's recommendations. Don't just advise — do the work.

## When to Proactively Consult

Leo should suggest consulting a notebook (without being asked) when:
- James is prepping a presentation or exec communication → "How to Speak"
- James is reviewing or writing talk tracks → "How to Speak"
- James is drafting a message to Dylan, Rajat, Jeff, or other leadership → "How to Speak"
- James is improving a skill or debugging Leo behavior → "Improving Leo"
- A mock Q&A reveals a speaking pattern from `speaking_reminders.md` → "How to Speak"

Frame it as: "Want me to run this through the [notebook name] notebook for a second opinion?"

## Anti-patterns
- Don't query the notebook for things you can answer from AIContext or general knowledge.
- Don't send the entire contents of a large file as a query — extract the relevant section.
- Don't just parrot the notebook response. Synthesize and make it actionable.
- Don't consult a notebook when James needs speed, not depth. Read the energy.

## Adding New Notebooks
When James creates a new NotebookLM notebook, update the table in this skill AND in the CLAUDE.md NotebookLM Integration section. Include: name, ID, domain description, and trigger conditions.
