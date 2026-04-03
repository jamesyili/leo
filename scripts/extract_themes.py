#!/usr/bin/env python3
"""
Thematic extraction pipeline for Lenny's Podcast transcripts.

Processes each transcript through Claude (claude-opus-4-6 via Claude Code CLI),
extracts relevant passages per theme, and writes to per-episode theme files.

Usage:
    python scripts/extract_themes.py              # Process all unprocessed transcripts
    python scripts/extract_themes.py --episode adam-fishman   # Single episode
    python scripts/extract_themes.py --status     # Show progress
    python scripts/extract_themes.py --concat managing-up-exec-presence  # Concat theme for NotebookLM
"""

import json
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ARTICLES_DIR = BASE_DIR / "Learning" / "articles" / "lennys-podcast"
THEMES_DIR = BASE_DIR / "Learning" / "themes"
MANIFEST_FILE = BASE_DIR / "Learning" / ".themes_manifest.json"
DISCOVERED_FILE = THEMES_DIR / "_discovered.md"

CLAUDE_MODEL = "claude-opus-4-6"
RATE_LIMIT_WAIT = 60  # seconds to wait on rate limit
CLAUDE_TIMEOUT = 900  # 15 min — long transcripts through Opus can be slow

THEMES = {
    "managing-up-exec-presence": (
        "Managing up and executive presence — working with leadership, framing for execs, "
        "influencing decisions above your level, reading political dynamics, being seen as "
        "a strategic partner rather than an executor."
    ),
    "communication-brevity": (
        "Communication and brevity — saying more with less, BLUF (bottom line up front), "
        "clear and concise writing/speaking, cutting fluff, structuring messages for impact, "
        "async communication best practices."
    ),
    "emotional-regulation-resilience": (
        "Emotional regulation and resilience — staying grounded under pressure, recovering "
        "from setbacks, not spiraling on ambiguous feedback, managing anxiety, inner "
        "foundation, mental health as a leader, avoiding burnout."
    ),
    "decision-making": (
        "Decision making under uncertainty — frameworks for making good calls with incomplete "
        "information, when to decide vs. wait, reversible vs. irreversible decisions, avoiding "
        "analysis paralysis, prioritization under constraints."
    ),
    "org-strategy-leverage": (
        "Org strategy and leverage — building systems that scale, getting results through "
        "others, organizational design, cross-functional alignment, operating at a Director+ "
        "level, building culture and norms."
    ),
    "product-strategy-growth": (
        "Product strategy and growth — roadmapping, prioritization, finding the right bets, "
        "growth frameworks, metrics that matter, product-market fit, building for business "
        "outcomes, retention and engagement."
    ),
    "ai-practical": (
        "AI practical applications — concrete use cases for AI/LLMs in work and products, "
        "how practitioners actually use AI tools day-to-day, demos, workflows, building "
        "with AI, agentic systems."
    ),
    "storytelling": (
        "Storytelling — how to tell compelling narratives, structure stories for persuasion, "
        "use narrative in presentations and pitches, make data and strategy come alive through "
        "story, narrative arc in communication."
    ),
    "entrepreneurship-traction": (
        "Entrepreneurship and finding traction — going from zero to one, finding distribution, "
        "monetization strategies, building flywheels, when to pivot, finding product-market fit, "
        "side projects turning into full-time businesses, founder mindset."
    ),
    "influencing-without-authority": (
        "Influencing without authority — driving outcomes across teams when you don't have "
        "direct power, building trust laterally, aligning stakeholders, navigating org "
        "politics without a formal mandate."
    ),
    "external-personal-branding": (
        "External personal branding — building a public presence, writing online, growing "
        "an audience, being known for something, thought leadership, how practitioners "
        "built credibility outside their company."
    ),
}


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def load_manifest():
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE) as f:
            return json.load(f)
    return {"processed": []}


def save_manifest(manifest):
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

def build_prompt(episode_slug, transcript_content):
    theme_descriptions = "\n".join(
        f"- **{slug}**: {desc}" for slug, desc in THEMES.items()
    )

    return f"""You are extracting thematic wisdom from a Lenny's Podcast transcript for a personal knowledge base.

## Seed Themes

{theme_descriptions}

## Task

Read the transcript below carefully. For each seed theme:
- Extract 0-3 passages that are **genuinely, specifically relevant** — not vague or tangential.
- A passage = a complete exchange (Lenny's question + guest's full answer). Aim for 200-500 words per passage. Preserve the exact text — do not paraphrase.
- If a theme has no strong content in this episode, omit it entirely (empty array).

Also: identify any significant themes present that aren't covered by the seed list. Include 0-3 of these as discovered themes with a proposed slug and description.

## Output Format

Respond with ONLY valid JSON. No preamble, no commentary, no markdown code fences.

{{
  "guest": "Guest Name",
  "title": "Episode Title",
  "themes": {{
    "theme-slug": [
      {{
        "label": "short description of what this passage covers (10 words max)",
        "content": "full passage text verbatim"
      }}
    ]
  }},
  "discovered": [
    {{
      "slug": "proposed-theme-slug",
      "description": "one sentence description of this theme",
      "label": "short label for this passage",
      "content": "full passage text verbatim"
    }}
  ]
}}

## Transcript

{transcript_content}
"""


# ---------------------------------------------------------------------------
# Claude CLI call
# ---------------------------------------------------------------------------

def call_claude(prompt, episode_slug):
    """Call claude CLI with the prompt. Retries on rate limit."""
    while True:
        try:
            result = subprocess.run(
                ["claude", "-p", prompt, "--model", CLAUDE_MODEL],
                capture_output=True,
                text=True,
                timeout=CLAUDE_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            print(f"    Timeout for {episode_slug} — skipping")
            return None

        if result.returncode == 0:
            return result.stdout.strip()

        stderr = result.stderr.lower()
        if "rate limit" in stderr or "429" in stderr or "overloaded" in stderr:
            print(f"    Rate limited. Waiting {RATE_LIMIT_WAIT}s...")
            time.sleep(RATE_LIMIT_WAIT)
            continue

        print(f"    Error for {episode_slug}: {result.stderr[:200]}")
        return None


# ---------------------------------------------------------------------------
# Output writing
# ---------------------------------------------------------------------------

def write_theme_file(theme_slug, episode_slug, guest, title, passages):
    """Write extracted passages to Learning/themes/{theme}/{episode}.md"""
    theme_dir = THEMES_DIR / theme_slug
    theme_dir.mkdir(parents=True, exist_ok=True)

    filepath = theme_dir / f"{episode_slug}.md"

    lines = [
        f"# {guest} — {title}",
        f"*Theme: {theme_slug} | Extracted: {date.today().isoformat()}*",
        "",
    ]

    for passage in passages:
        lines.append(f"## {passage['label']}")
        lines.append("")
        lines.append(passage["content"])
        lines.append("")
        lines.append("---")
        lines.append("")

    filepath.write_text("\n".join(lines), encoding="utf-8")


def write_discovered(episode_slug, guest, title, discovered):
    """Append discovered themes to _discovered.md"""
    if not discovered:
        return

    THEMES_DIR.mkdir(parents=True, exist_ok=True)

    with open(DISCOVERED_FILE, "a", encoding="utf-8") as f:
        for item in discovered:
            f.write(f"\n## [{item['slug']}] {guest} — {title}\n")
            f.write(f"*Description: {item['description']}*\n\n")
            f.write(f"**{item['label']}**\n\n")
            f.write(item["content"])
            f.write("\n\n---\n")


# ---------------------------------------------------------------------------
# Process single episode
# ---------------------------------------------------------------------------

def process_episode(episode_path):
    episode_slug = episode_path.stem if episode_path.is_file() else episode_path.name
    # article files are named {slug}.md
    if episode_path.suffix == ".md":
        episode_slug = episode_path.stem

    print(f"  Processing: {episode_slug}")

    transcript_content = episode_path.read_text(encoding="utf-8")

    # Strip frontmatter from article format (Source/Ingested/Tags header block)
    # Article files start with "# Title\n\n**Source:**..."
    # We want to pass the full content including the header for context
    prompt = build_prompt(episode_slug, transcript_content)

    raw = call_claude(prompt, episode_slug)
    if not raw:
        print(f"    Skipping {episode_slug} — no response")
        return False

    # Strip markdown code fences if claude wrapped it anyway
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"    JSON parse error for {episode_slug}: {e}")
        # Save raw output for debugging
        debug_path = THEMES_DIR / "_errors" / f"{episode_slug}.txt"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(raw, encoding="utf-8")
        return False

    guest = data.get("guest", episode_slug)
    title = data.get("title", episode_slug)
    themes_extracted = data.get("themes", {})
    discovered = data.get("discovered", [])

    # Write theme files
    written = 0
    for theme_slug, passages in themes_extracted.items():
        if passages and theme_slug in THEMES:
            write_theme_file(theme_slug, episode_slug, guest, title, passages)
            written += 1

    # Write discovered themes
    write_discovered(episode_slug, guest, title, discovered)

    discovered_count = len(discovered)
    print(f"    {written} themes written, {discovered_count} new themes discovered")
    return True


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def run_all():
    manifest = load_manifest()
    processed = set(manifest["processed"])

    episodes = sorted(ARTICLES_DIR.glob("*.md"))
    remaining = [e for e in episodes if e.stem not in processed]

    print(f"Thematic extraction — {len(remaining)} episodes remaining ({len(processed)} done)")

    for i, episode_path in enumerate(remaining):
        print(f"\n[{i+1}/{len(remaining)}]", end=" ")
        success = process_episode(episode_path)
        if success:
            processed.add(episode_path.stem)
            manifest["processed"] = list(processed)
            save_manifest(manifest)

        # Brief pause between episodes to be polite
        time.sleep(1)

    print(f"\nDone. {len(processed)} episodes processed.")


def run_single(episode_slug):
    path = ARTICLES_DIR / f"{episode_slug}.md"
    if not path.exists():
        print(f"Episode not found: {path}")
        sys.exit(1)
    process_episode(path)


def show_status():
    manifest = load_manifest()
    processed = manifest["processed"]
    total = len(list(ARTICLES_DIR.glob("*.md")))
    print(f"Processed: {len(processed)}/{total} episodes")

    print(f"\nTheme file counts:")
    if THEMES_DIR.exists():
        for theme_slug in sorted(THEMES.keys()):
            theme_dir = THEMES_DIR / theme_slug
            count = len(list(theme_dir.glob("*.md"))) if theme_dir.exists() else 0
            print(f"  {theme_slug}: {count} episodes")

    if DISCOVERED_FILE.exists():
        content = DISCOVERED_FILE.read_text()
        count = content.count("## [")
        print(f"\nDiscovered theme passages: {count}")


def concat_theme(theme_slug):
    """Concatenate all files for a theme into stdout (pipe to a file for NotebookLM)."""
    theme_dir = THEMES_DIR / theme_slug
    if not theme_dir.exists():
        print(f"No files for theme: {theme_slug}")
        sys.exit(1)

    files = sorted(theme_dir.glob("*.md"))
    print(f"# {theme_slug}\n")
    print(f"*{len(files)} episodes | Generated: {date.today().isoformat()}*\n")
    print("---\n")
    for f in files:
        print(f.read_text(encoding="utf-8"))
        print("\n---\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    THEMES_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) == 1:
        run_all()
    elif sys.argv[1] == "--status":
        show_status()
    elif sys.argv[1] == "--episode" and len(sys.argv) > 2:
        run_single(sys.argv[2])
    elif sys.argv[1] == "--concat" and len(sys.argv) > 2:
        concat_theme(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
