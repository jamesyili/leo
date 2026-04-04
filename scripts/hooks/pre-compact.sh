#!/bin/bash
# PreCompact hook: Fires before context compaction.
# 1. Logs the compaction event for tracking
# 2. Outputs a recovery instruction that survives compaction

COMPACT_LOG="/home/james/src/leo/system/compaction-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log the compaction event
if [ ! -f "$COMPACT_LOG" ]; then
  echo "# Compaction Log" > "$COMPACT_LOG"
  echo "" >> "$COMPACT_LOG"
  echo "Tracks context compaction events for debugging context loss." >> "$COMPACT_LOG"
  echo "" >> "$COMPACT_LOG"
fi

echo "- $TIMESTAMP — compaction triggered" >> "$COMPACT_LOG"

# Output recovery instruction (survives into post-compaction context)
cat <<'EOF'
=== CONTEXT COMPACTION OCCURRED ===
Context was just compacted. To recover session state:
1. Re-read the latest file in system/session-logs/ for context
2. If mid-task, re-read any active context files relevant to the current work
3. Ask James to re-state the current goal if unclear
=== END COMPACTION NOTICE ===
EOF
