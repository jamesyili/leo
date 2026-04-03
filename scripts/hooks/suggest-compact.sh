#!/bin/bash
# Stop hook: Track tool calls per session, suggest /compact at logical thresholds.
# Runs after every Claude response. Uses a temp file to persist count across responses.

SESSION_ID="${SESSION_ID:-default}"
COUNTER_FILE="/tmp/leo-toolcount-${SESSION_ID}"

# Initialize counter if it doesn't exist
if [ ! -f "$COUNTER_FILE" ]; then
  echo "0" > "$COUNTER_FILE"
fi

# Increment counter
COUNT=$(cat "$COUNTER_FILE")
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# Suggest compaction at threshold (every 50 tool calls after the first 50)
if [ "$COUNT" -eq 50 ] || [ "$COUNT" -eq 100 ]; then
  echo "=== COMPACTION SUGGESTION ==="
  echo "~${COUNT} tool calls this session. If you're between phases (finished exploring, about to start building, just hit a milestone), now is a good time to suggest /compact to James."
  echo "=== END COMPACTION SUGGESTION ==="
fi
