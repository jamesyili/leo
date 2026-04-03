# Search — Knowledge Base Query

Search across all Leo context files and ingested knowledge base articles.

## When to Use
- When James asks to find information across the knowledge base
- When you need to locate relevant context before answering a question
- When connecting concepts across different sources

## Process

### 1. Understand the query

Parse what James is looking for. It could be:
- A specific concept (e.g., "NDCG", "transformer attention")
- A topic area (e.g., "managing up", "candidate generation")
- A person or project reference
- A framework or technique

### 2. Search across all knowledge

Search these locations in parallel:

**Context files** (highest priority):
```
Work+Self/          # Goals, coaching, communication, stakeholders
Learning/           # Learning agenda, concept notes
System/             # Session log, backlog
```

**Ingested articles:**
```
Learning/articles/  # All ingested content, organized by source
```

Use Grep with the query terms across all `.md` files. Search for:
- Exact term matches
- Related terms and synonyms
- Partial matches for compound concepts

### 3. Present results

Format results as:
```
## Search: "{query}"

### Context Files
- **{file}** (line {N}): {relevant snippet}

### Knowledge Base Articles
- **{source}/{article}**: {relevant snippet}
```

Rank by relevance:
1. Exact matches in titles
2. Exact matches in content
3. Related/partial matches
4. Tag matches

### 4. Synthesize if asked

If James asks a question (not just searching), synthesize across the matched sources:
- Combine insights from multiple articles
- Connect to James's work context (projects, goals)
- Flag any contradictions between sources
