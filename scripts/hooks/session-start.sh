#!/bin/bash
# SessionStart hook: Auto-load the most recent session log entry into context.
# stdout is injected as a system message at session start.

SESSION_LOG="/home/james/src/leo/system/session-log.md"

if [ ! -f "$SESSION_LOG" ]; then
  exit 0
fi

# Extract the most recent entry: from the first "## " heading to the first "---" separator
echo "=== LAST SESSION CONTEXT (auto-loaded by SessionStart hook) ==="
awk '
  /^## / { if (found) exit; found=1 }
  found { print }
' "$SESSION_LOG"
echo "=== END LAST SESSION CONTEXT ==="
