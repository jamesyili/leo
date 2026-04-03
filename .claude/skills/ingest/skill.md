# Ingest — Knowledge Base Content Pipeline

Ingest content from curated sources into the Leo knowledge base.

## When to Use
- Daily cron job (6am PT)
- Ad-hoc when James wants to pull new content
- After adding a new source to the registry

## Process

### 1. Run the ingest script

The main script is at `scripts/ingest.py`. Choose the right command based on context:

```bash
# Daily run (default for cron) — checks all sources for new content + creates digest
python scripts/ingest.py daily

# Bulk backfill Aman.ai (first-time only)
python scripts/ingest.py backfill-aman

# Bulk backfill Substack sources (first-time only)
python scripts/ingest.py backfill-substack

# Check only RSS feeds
python scripts/ingest.py check-rss

# Show current stats
python scripts/ingest.py status
```

### 2. Review output

After the script runs:
1. Check how many articles were created
2. If this is a daily run, read the digest at `Learning/digest/YYYY-MM-DD.md`
3. Spot-check 2-3 articles for format quality

### 3. Add relevance tags (daily run only)

For new articles ingested during daily runs (typically 1-10 articles):
1. Read each new article
2. Add a **Relevance:** line after the Tags line with 2-3 sentences on why it matters for James
3. Cross-reference with `Learning/learning_agenda.md` and `Work+Self/goals.md` for relevance

Skip relevance tagging for bulk backfills — those get tagged lazily when accessed.

### 4. Commit and push

```bash
git add Learning/articles/ Learning/digest/ Learning/.ingested_manifest.json
git commit -m "Daily knowledge ingest — {date}"
git push
```

## Adding New Sources

1. If it has an RSS/Atom feed, add it to `RSS_SOURCES` in `scripts/ingest.py`
2. If it's a Substack, also add to `SUBSTACK_BACKFILL_SOURCES` for initial bulk ingest
3. Update `Learning/sources.md` with the new source details
4. Run `python scripts/ingest.py check-rss` to pull initial content

## Source Registry

See `Learning/sources.md` for the full list of curated sources, their feeds, and sync status.

## Output Structure

```
Learning/
├── articles/{source-slug}/{article-slug}.md   # Full content, permanent
└── digest/YYYY-MM-DD.md                        # Daily summary, links to articles
```
