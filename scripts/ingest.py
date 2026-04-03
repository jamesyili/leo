#!/usr/bin/env python3
"""
Knowledge base ingest pipeline for Leo.
Fetches content from curated sources and creates markdown article files.

Usage:
    python ingest.py backfill-aman          # Bulk ingest all Aman.ai content
    python ingest.py backfill-lenny         # Bulk ingest all Lenny's Podcast transcripts (GitHub)
    python ingest.py backfill-substack      # Bulk ingest all Substack sources (Wes Kao, etc.)
    python ingest.py check-rss              # Check RSS feeds for new content
    python ingest.py daily                  # Full daily run (check-aman + check-rss + digest)
    python ingest.py status                 # Show ingest stats
"""

import html
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LEARNING_DIR = BASE_DIR / "learning"
ARTICLES_DIR = LEARNING_DIR / "articles"
DIGEST_DIR = LEARNING_DIR / "digest"
MANIFEST_FILE = LEARNING_DIR / ".ingested_manifest.json"


# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------

RSS_SOURCES = [
    # (slug, feed_url, default_tags)
    ("lilian-weng", "https://lilianweng.github.io/index.xml", ["ml-fundamentals", "deep-learning"]),
    ("sebastian-raschka", "https://magazine.sebastianraschka.com/feed", ["llms", "ml-research"]),
    ("eugene-yan", "https://eugeneyan.com/rss/", ["recsys", "ml-systems"]),
    ("chip-huyen", "https://huyenchip.com/feed.xml", ["ml-systems", "mlops"]),
    ("jay-alammar", "https://jalammar.github.io/feed.xml", ["ml-fundamentals", "visual-explanations"]),
    ("karpathy", "https://karpathy.github.io/feed.xml", ["llms", "deep-learning"]),
    ("cameron-wolfe", "https://cameronrwolfe.substack.com/feed", ["llms", "rlhf", "architectures"]),
    ("nathan-lambert", "https://www.interconnects.ai/feed", ["rlhf", "reinforcement-learning", "llms"]),
    ("simon-willison", "https://simonwillison.net/atom/everything/", ["llm-tooling", "ai-engineering"]),
    ("wes-kao", "https://newsletter.weskao.com/feed", ["managing-up", "exec-comms", "leadership"]),
    ("jefferson-fisher", "https://jeffersonfisher.substack.com/feed", ["communication", "soft-skills"]),
    ("ethan-evans", "https://levelupwithethanevans.substack.com/feed", ["leadership", "career", "managing-up"]),
]

SUBSTACK_BACKFILL_SOURCES = [
    # (slug, base_url, default_tags)
    ("wes-kao", "https://newsletter.weskao.com", ["managing-up", "exec-comms", "leadership"]),
]

LENNY_GITHUB_REPO = "ChatPRD/lennys-podcast-transcripts"
LENNY_DEFAULT_TAGS = ["product-management", "leadership", "growth", "career"]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].rstrip('-')


def strip_html(text):
    """Strip HTML tags and decode entities. Preserves line breaks."""
    if not text:
        return ""
    # Convert common block elements to newlines
    text = re.sub(r'<br\s*/?\s*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?(p|div|h[1-6]|li|tr|blockquote)[^>]*>', '\n', text, flags=re.IGNORECASE)
    # Convert links to markdown
    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE)
    # Convert bold/italic
    text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text, flags=re.IGNORECASE)
    text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text, flags=re.IGNORECASE)
    # Convert code
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.IGNORECASE)
    # Convert images to markdown
    text = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', text, flags=re.IGNORECASE)
    text = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*/?>', r'![](\1)', text, flags=re.IGNORECASE)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def fetch_url(url, timeout=60):
    """Fetch a URL and return the response body as string."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; LeoKnowledgeBot/1.0)',
        'Accept': 'application/json, application/xml, text/xml, */*',
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', errors='replace')


# ---------------------------------------------------------------------------
# Manifest (tracks what's been ingested)
# ---------------------------------------------------------------------------

def load_manifest():
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE) as f:
            return json.load(f)
    return {"ingested_urls": [], "last_synced": {}}


def save_manifest(manifest):
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2, default=str)


# ---------------------------------------------------------------------------
# Article creation
# ---------------------------------------------------------------------------

def create_article_md(title, source_slug, url, content, tags=None):
    """Create a markdown article file. Returns (filepath, was_created)."""
    source_dir = ARTICLES_DIR / source_slug
    source_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(title)
    if not slug:
        # Fallback: derive from URL
        path_part = url.rstrip('/').split('/')[-1]
        slug = slugify(path_part) or "untitled"

    filepath = source_dir / f"{slug}.md"

    # Don't overwrite existing files
    if filepath.exists():
        return filepath, False

    tags_str = ", ".join(tags) if tags else "untagged"

    md = f"""# {title}

**Source:** {url}
**Ingested:** {date.today().isoformat()}
**Tags:** {tags_str}

---

{content}
"""

    filepath.write_text(md, encoding='utf-8')
    return filepath, True


# ---------------------------------------------------------------------------
# Aman.ai
# ---------------------------------------------------------------------------

def derive_aman_tags(url):
    """Derive tags from Aman.ai URL path."""
    tag_map = {
        '/primers/ai/': 'ml-fundamentals',
        '/recsys/': 'recsys',
        '/sysdes/': 'system-design',
        '/mlsysdes/': 'ml-system-design',
        '/cs229/': 'ml-theory',
        '/cs231n/': 'computer-vision',
        '/cs230/': 'deep-learning',
        '/cs224n/': 'nlp',
        '/code/': 'algorithms',
        '/tnt/': 'python',
        '/infra/': 'infrastructure',
    }
    tags = []
    for prefix, tag in tag_map.items():
        if prefix in url:
            tags.append(tag)

    url_lower = url.lower()
    keyword_tags = {
        'transformer': 'transformers',
        'llm': 'llms',
        'language-model': 'llms',
        'attention': 'attention',
        'embedding': 'embeddings',
        'reinforcement': 'reinforcement-learning',
        'eval': 'evaluation',
        'retrieval': 'retrieval',
        'ranking': 'ranking',
        'gnn': 'graph-neural-networks',
        'graph': 'graph-neural-networks',
        'bert': 'transformers',
        'gpt': 'llms',
        'diffusion': 'generative-models',
        'gan': 'generative-models',
        'cnn': 'computer-vision',
        'rnn': 'sequence-models',
        'lstm': 'sequence-models',
        'fine-tun': 'fine-tuning',
        'pretrain': 'pretraining',
        'rlhf': 'rlhf',
        'recommend': 'recsys',
        'cold-start': 'recsys',
        'candidate': 'candidate-generation',
        'collaborative-filter': 'collaborative-filtering',
    }
    for keyword, tag in keyword_tags.items():
        if keyword in url_lower:
            tags.append(tag)

    return list(set(tags)) if tags else ['ml-fundamentals']


def ingest_aman(check_only=False):
    """Fetch content from Aman.ai and create article files."""
    action = "Checking" if check_only else "Backfilling"
    print(f"{action} Aman.ai...")

    data = json.loads(fetch_url("https://aman.ai/search.json"))
    print(f"  Found {len(data)} entries in search.json")

    manifest = load_manifest()
    ingested = set(manifest["ingested_urls"])

    created_articles = []  # (title, filepath) for digest
    skipped = 0

    for entry in data:
        entry_url = entry.get('url', '')
        if not entry_url:
            continue

        if entry_url.startswith('/'):
            entry_url = f"https://aman.ai{entry_url}"

        if entry_url in ingested:
            skipped += 1
            continue

        title = entry.get('title', '').strip()
        content = entry.get('content', '').strip()

        if not title or not content or len(content) < 200:
            skipped += 1
            continue

        tags = derive_aman_tags(entry_url)
        category = entry.get('category', '').strip()
        if category:
            cat_tag = slugify(category)
            if cat_tag and cat_tag not in tags:
                tags.append(cat_tag)

        filepath, was_created = create_article_md(
            title=title,
            source_slug="aman-ai",
            url=entry_url,
            content=content,
            tags=tags,
        )

        if was_created:
            created_articles.append((title, filepath))
            ingested.add(entry_url)
        else:
            skipped += 1

    manifest["ingested_urls"] = list(ingested)
    manifest["last_synced"]["aman-ai"] = datetime.now().isoformat()
    save_manifest(manifest)

    print(f"  {len(created_articles)} articles created, {skipped} skipped")
    return created_articles


# ---------------------------------------------------------------------------
# RSS feeds
# ---------------------------------------------------------------------------

def parse_feed(xml_text):
    """Parse RSS or Atom feed XML. Returns list of (title, url, content, pub_date)."""
    root = ET.fromstring(xml_text)
    entries = []

    # Atom feeds
    atom_ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('.//atom:entry', atom_ns):
        title = (entry.findtext('atom:title', '', atom_ns) or '').strip()
        link_elem = entry.find('atom:link[@rel="alternate"]', atom_ns)
        if link_elem is None:
            link_elem = entry.find('atom:link', atom_ns)
        link = link_elem.get('href', '') if link_elem is not None else ''
        content = (entry.findtext('atom:content', '', atom_ns)
                   or entry.findtext('atom:summary', '', atom_ns) or '')
        pub_date = (entry.findtext('atom:published', '', atom_ns)
                    or entry.findtext('atom:updated', '', atom_ns) or '')
        if title and link:
            entries.append((title, link, content.strip(), pub_date))

    # RSS feeds (only if no Atom entries found)
    if not entries:
        content_ns = '{http://purl.org/rss/1.0/modules/content/}'
        for item in root.findall('.//item'):
            title = (item.findtext('title') or '').strip()
            link = (item.findtext('link') or '').strip()
            content = (item.findtext(f'{content_ns}encoded')
                       or item.findtext('description') or '').strip()
            pub_date = (item.findtext('pubDate') or '').strip()
            if title and link:
                entries.append((title, link, content, pub_date))

    return entries


def check_rss_sources(sources=None):
    """Check RSS sources for new content."""
    if sources is None:
        sources = RSS_SOURCES

    manifest = load_manifest()
    ingested = set(manifest["ingested_urls"])
    all_created = {}  # source_slug -> [(title, filepath)]

    for source_slug, feed_url, default_tags in sources:
        print(f"  Checking {source_slug}...")
        try:
            xml_text = fetch_url(feed_url, timeout=30)
            entries = parse_feed(xml_text)
        except Exception as e:
            print(f"    Error: {e}")
            continue

        created = []
        for title, url, content, pub_date in entries:
            if url in ingested:
                continue

            # Convert HTML content to markdown-ish text
            if content and ('<' in content):
                content = strip_html(content)

            if not content:
                content = f"*Full content not available in feed. Visit the source URL.*\n\nPublished: {pub_date}"

            filepath, was_created = create_article_md(
                title=title,
                source_slug=source_slug,
                url=url,
                content=content,
                tags=list(default_tags),
            )

            if was_created:
                created.append((title, filepath))
                ingested.add(url)

        if created:
            all_created[source_slug] = created
        print(f"    {len(created)} new articles")
        manifest["last_synced"][source_slug] = datetime.now().isoformat()

        # Be polite to servers
        time.sleep(0.5)

    manifest["ingested_urls"] = list(ingested)
    save_manifest(manifest)

    total = sum(len(v) for v in all_created.values())
    print(f"  Total: {total} new articles from RSS")
    return all_created


# ---------------------------------------------------------------------------
# Substack backfill (paginated API)
# ---------------------------------------------------------------------------

def backfill_substack():
    """Bulk ingest all posts from Substack sources using their API."""
    manifest = load_manifest()
    ingested = set(manifest["ingested_urls"])
    all_created = {}

    for source_slug, base_url, default_tags in SUBSTACK_BACKFILL_SOURCES:
        print(f"  Backfilling {source_slug} from {base_url}...")
        created = []
        offset = 0
        batch_size = 12

        while True:
            api_url = f"{base_url}/api/v1/archive?sort=new&limit={batch_size}&offset={offset}"
            try:
                data = json.loads(fetch_url(api_url))
            except Exception as e:
                print(f"    Error at offset {offset}: {e}")
                break

            if not data:
                break

            for post in data:
                url = post.get('canonical_url', '') or f"{base_url}/p/{post.get('slug', '')}"
                title = post.get('title', '').strip()

                if url in ingested or not title:
                    continue

                # Get full post content — try body_html first, fall back to subtitle
                content = post.get('body_html', '') or post.get('body_text', '')
                if content and '<' in content:
                    content = strip_html(content)
                if not content:
                    subtitle = post.get('subtitle', '')
                    content = subtitle if subtitle else '*Content not available via API.*'

                post_date = post.get('post_date', '')[:10] if post.get('post_date') else ''

                filepath, was_created = create_article_md(
                    title=title,
                    source_slug=source_slug,
                    url=url,
                    content=content,
                    tags=list(default_tags),
                )

                if was_created:
                    created.append((title, filepath))
                    ingested.add(url)

            offset += batch_size
            print(f"    Processed offset {offset} ({len(created)} created so far)")
            time.sleep(1)  # Rate limiting

        if created:
            all_created[source_slug] = created
        manifest["last_synced"][source_slug] = datetime.now().isoformat()
        print(f"    {source_slug}: {len(created)} articles created")

    manifest["ingested_urls"] = list(ingested)
    save_manifest(manifest)
    return all_created


# ---------------------------------------------------------------------------
# Lenny's Podcast (GitHub transcript repo)
# ---------------------------------------------------------------------------

def backfill_lenny():
    """Bulk ingest all episode transcripts from the Lenny's Podcast GitHub repo."""
    print(f"Backfilling Lenny's Podcast transcripts from GitHub...")

    # List all transcript files via GitHub API
    tree_url = f"https://api.github.com/repos/{LENNY_GITHUB_REPO}/git/trees/main?recursive=1"
    tree_data = json.loads(fetch_url(tree_url))
    episode_paths = [
        f["path"] for f in tree_data.get("tree", [])
        if f["type"] == "blob" and f["path"].startswith("episodes/") and f["path"].endswith("/transcript.md")
    ]
    print(f"  Found {len(episode_paths)} episode transcripts")

    manifest = load_manifest()
    ingested = set(manifest["ingested_urls"])

    created_articles = []
    skipped = 0

    for path in episode_paths:
        raw_url = f"https://raw.githubusercontent.com/{LENNY_GITHUB_REPO}/main/{path}"

        if raw_url in ingested:
            skipped += 1
            continue

        try:
            encoded_path = urllib.parse.quote(path, safe='/')
            raw_url = f"https://raw.githubusercontent.com/{LENNY_GITHUB_REPO}/main/{encoded_path}"
            content = fetch_url(raw_url, timeout=30)
        except Exception as e:
            print(f"    Error fetching {path}: {e}")
            continue

        # Parse frontmatter for title, date, keywords
        title = ""
        tags = list(LENNY_DEFAULT_TAGS)
        lines = content.splitlines()
        in_frontmatter = False
        frontmatter_done = False
        body_start = 0

        for i, line in enumerate(lines):
            if i == 0 and line.strip() == "---":
                in_frontmatter = True
                continue
            if in_frontmatter and line.strip() == "---":
                frontmatter_done = True
                body_start = i + 1
                break
            if in_frontmatter:
                if line.startswith("title:"):
                    raw_title = line[len("title:"):].strip().strip("'\"")
                    title = raw_title
                elif line.startswith("- ") and not frontmatter_done:
                    # keyword list items
                    kw = slugify(line[2:].strip())
                    if kw and kw not in tags:
                        tags.append(kw)

        if not title:
            # Derive from path slug
            title = path.split("/")[1].replace("-", " ").title()

        body = "\n".join(lines[body_start:]).strip() if frontmatter_done else content

        filepath, was_created = create_article_md(
            title=title,
            source_slug="lennys-podcast",
            url=raw_url,
            content=body,
            tags=tags,
        )

        if was_created:
            created_articles.append((title, filepath))
            ingested.add(raw_url)
        else:
            skipped += 1

        time.sleep(0.1)  # Be polite to GitHub

    manifest["ingested_urls"] = list(ingested)
    manifest["last_synced"]["lennys-podcast"] = datetime.now().isoformat()
    save_manifest(manifest)

    print(f"  {len(created_articles)} transcripts created, {skipped} skipped")
    return created_articles


# ---------------------------------------------------------------------------
# Daily digest
# ---------------------------------------------------------------------------

def create_digest(articles_by_source):
    """Create a daily digest file linking to new articles."""
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    digest_path = DIGEST_DIR / f"{today}.md"

    total = sum(len(arts) for arts in articles_by_source.values())

    if total == 0:
        print("  No new articles — skipping digest")
        return None

    lines = [f"# Daily Digest — {today}\n"]
    lines.append(f"**{total} new articles ingested**\n")

    for source_slug in sorted(articles_by_source.keys()):
        articles = articles_by_source[source_slug]
        if articles:
            lines.append(f"\n## {source_slug}\n")
            for title, filepath in articles:
                rel_path = os.path.relpath(filepath, DIGEST_DIR)
                lines.append(f"- [{title}]({rel_path})")

    digest_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"  Digest written: {digest_path}")
    return digest_path


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status():
    """Show ingest stats."""
    manifest = load_manifest()
    print(f"Total ingested URLs: {len(manifest['ingested_urls'])}")
    print(f"\nLast synced:")
    for source, ts in sorted(manifest.get("last_synced", {}).items()):
        print(f"  {source}: {ts}")

    print(f"\nArticle directories:")
    if ARTICLES_DIR.exists():
        for d in sorted(ARTICLES_DIR.iterdir()):
            if d.is_dir():
                count = len(list(d.glob("*.md")))
                print(f"  {d.name}: {count} articles")

    print(f"\nDigests:")
    if DIGEST_DIR.exists():
        digests = sorted(DIGEST_DIR.glob("*.md"))
        print(f"  {len(digests)} digest files")
        if digests:
            print(f"  Latest: {digests[-1].name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    # Ensure directories exist
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)

    if command == "backfill-aman":
        ingest_aman(check_only=False)

    elif command == "backfill-lenny":
        backfill_lenny()

    elif command == "backfill-substack":
        backfill_substack()

    elif command == "check-rss":
        check_rss_sources()

    elif command == "daily":
        print("=== Daily ingest run ===")
        all_articles = {}

        print("\n[1/3] Checking Aman.ai for updates...")
        aman_articles = ingest_aman(check_only=True)
        if aman_articles:
            all_articles["aman-ai"] = aman_articles

        print("\n[2/3] Checking RSS feeds...")
        rss_articles = check_rss_sources()
        all_articles.update(rss_articles)

        print("\n[3/3] Creating digest...")
        create_digest(all_articles)

        total = sum(len(v) for v in all_articles.values())
        print(f"\n=== Done: {total} new articles ===")

    elif command == "status":
        show_status()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
