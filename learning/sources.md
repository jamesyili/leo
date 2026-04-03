# Knowledge Base Sources

> Registry of curated content sources for automated ingestion. Used by `scripts/ingest.py` and the `/ingest` skill.

Last updated: 2026-04-02

---

## Tier 1 — Bulk Backfill (one-time, then periodic check)

| Source | Type | URL | Feed/API | Status |
|--------|------|-----|----------|--------|
| **Aman.ai** | Static library | aman.ai | `/search.json` (587 pages, full text) | Pending backfill |
| **Wes Kao** | Substack | newsletter.weskao.com | `/feed` (107 posts, all free) | Pending backfill |
| **Lenny's Podcast** | GitHub transcript repo | github.com/ChatPRD/lennys-podcast-transcripts | GitHub API + raw file fetch (303 transcripts) | Pending backfill |

## Tier 2 — RSS Daily Check

### Technical / ML

| Source | Feed URL | Focus | Cadence |
|--------|----------|-------|---------|
| **Lilian Weng** | `lilianweng.github.io/index.xml` | ML deep dives | ~4-6/year |
| **Sebastian Raschka** | `magazine.sebastianraschka.com/feed` | LLM research | 2-4x/month |
| **Eugene Yan** | `eugeneyan.com/rss/` | RecSys + ML systems | 2-4x/month |
| **Chip Huyen** | `huyenchip.com/feed.xml` | ML systems, MLOps | ~monthly |
| **Jay Alammar** | `jalammar.github.io/feed.xml` | Visual ML explanations | Infrequent |
| **Andrej Karpathy** | `karpathy.github.io/feed.xml` | LLMs, training | Infrequent |
| **Cameron Wolfe** | `cameronrwolfe.substack.com/feed` | LLM architectures, RLHF | 2-4x/month |
| **Nathan Lambert** | `interconnects.ai/feed` | RLHF, RL for LLMs | Weekly |
| **Simon Willison** | `simonwillison.net/atom/everything/` | LLM tooling, AI engineering | Near-daily |

### Leadership / Soft Skills

| Source | Feed URL | Focus | Cadence |
|--------|----------|-------|---------|
| **Jefferson Fisher** | `jeffersonfisher.substack.com/feed` | Communication, persuasion | Weekly (just started Feb 2026) |
| **Ethan Evans** | `levelupwithethanevans.substack.com/feed` | Leadership, career, managing up | 2x/week (~40% free) |

## Parked — Phase 2

| Source | Reason | Notes |
|--------|--------|-------|
| **Shreyas Doshi** | No RSS — Twitter threads | ~50 threads on Thread Reader App + 5-6 LinkedIn articles |
| **RecSys academics** (Ed Chi, Hao Wang, Wenjie Wang) | arXiv papers, not blogs | Track via arXiv author feeds |
| **Jefferson Fisher YouTube** | Requires transcript extraction | Primary content source (hundreds of videos) |
| **Ethan Evans paid** | Paywalled (~60% of content) | ~120 free articles available now |

---

## Output Structure

```
learning/
├── articles/
│   ├── aman-ai/           # One .md per article, full content preserved
│   ├── wes-kao/
│   ├── eugene-yan/
│   ├── lilian-weng/
│   └── ...
└── digest/
    └── YYYY-MM-DD.md      # Daily digest linking to new articles
```

## Article Format

```markdown
# {Original Title}

**Source:** {author} — {URL}
**Ingested:** {date}
**Relevance:** {2-3 sentences — why this matters for James}
**Tags:** {e.g., recsys, transformers, managing-up, eval}

---

{Full original content — preserved as-is, not summarized}
```
