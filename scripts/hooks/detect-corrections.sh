#!/bin/bash
# Stop hook: Scan the current conversation transcript for correction signals.
# If detected, outputs a prompt for Leo to create/update an instinct.
# Keeps a marker file to avoid re-flagging the same corrections.

PROJECT_DIR="$HOME/.claude/projects/-home-james-src-leo"
MARKER_FILE="/tmp/leo-correction-marker"
INSTINCT_DIR="/home/james/src/leo/system/instincts"

# Find the most recently modified conversation transcript
TRANSCRIPT=$(ls -t "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1)

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  exit 0
fi

# Get the line count we last checked (avoid re-scanning old messages)
LAST_LINE=0
if [ -f "$MARKER_FILE" ]; then
  LAST_LINE=$(cat "$MARKER_FILE")
fi

CURRENT_LINES=$(wc -l < "$TRANSCRIPT")

# Only scan new lines since last check
if [ "$CURRENT_LINES" -le "$LAST_LINE" ]; then
  # Update marker even if no new lines (transcript may have changed files)
  echo "$CURRENT_LINES" > "$MARKER_FILE"
  exit 0
fi

# Extract new user text messages and check for correction patterns
CORRECTIONS=$(tail -n +"$((LAST_LINE + 1))" "$TRANSCRIPT" | python3 -c "
import sys, json, re

correction_patterns = [
    r'\bno[,.]?\s+(not |don.t |stop )',
    r'\bstop (doing|adding|saying)',
    r'\bdon.t (do |add |say |include |summarize|guess)',
    r'\bi told you',
    r'\bi said ',
    r'\bnot like that',
    r'\bwrong\b',
    r'\bthat.s not what',
    r'\bplease don.t',
    r'\bstop\b.*\bing\b',
    r'\byou keep ',
    r'\bagain\b.*\bwrong',
    r'\bi already ',
]

for line in sys.stdin:
    try:
        msg = json.loads(line)
        role = msg.get('message', {}).get('role', msg.get('type', ''))
        content = msg.get('message', {}).get('content', '')
        if role != 'user':
            continue

        text = ''
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get('type') == 'text':
                    text += c['text'] + ' '

        if not text.strip():
            continue

        # Skip system/command messages
        if '<command-name>' in text or '<system-reminder>' in text:
            continue

        text_lower = text.lower()
        for pattern in correction_patterns:
            if re.search(pattern, text_lower):
                # Print the first 200 chars of the correction
                clean = text.strip()[:200]
                print(clean)
                break
    except (json.JSONDecodeError, KeyError):
        continue
" 2>/dev/null)

# Update marker
echo "$CURRENT_LINES" > "$MARKER_FILE"

# If corrections found, output a prompt
if [ -n "$CORRECTIONS" ]; then
  echo "=== CORRECTION SIGNAL DETECTED ==="
  echo "The following user message(s) may contain corrections to Leo's behavior:"
  echo ""
  echo "$CORRECTIONS"
  echo ""
  echo "Consider creating or updating an instinct in system/instincts/."
  echo "Format: id, trigger, behavior, confidence (start at 0.3), evidence."
  echo "If an existing instinct matches, bump its confidence and add evidence."
  echo "=== END CORRECTION SIGNAL ==="
fi
