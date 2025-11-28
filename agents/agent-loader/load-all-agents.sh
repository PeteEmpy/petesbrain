#!/bin/bash
#
# PetesBrain Agent Loader
#
# Loads all PetesBrain LaunchAgents at login to ensure they start reliably.
# This is more reliable than depending on RunAtLoad which can fail silently.
#
# Usage: Run at login via LaunchAgent or Login Items
#

LOG_FILE="$HOME/.petesbrain-agent-loader.log"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "============================================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Agent Loader Starting" >> "$LOG_FILE"
echo "============================================================" >> "$LOG_FILE"

# Wait a few seconds for system to stabilize after login
sleep 5

# Count loaded before
LOADED_BEFORE=$(launchctl list | grep -c "com.petesbrain" || echo 0)
echo "Agents already loaded: $LOADED_BEFORE" >> "$LOG_FILE"

# Load all PetesBrain agents
LOADED_COUNT=0
FAILED_COUNT=0
ALREADY_LOADED=0

for plist in "$LAUNCH_AGENTS_DIR"/com.petesbrain.*.plist; do
    if [ -f "$plist" ]; then
        LABEL=$(basename "$plist" .plist)

        # Check if already loaded
        if launchctl list "$LABEL" &>/dev/null; then
            ((ALREADY_LOADED++))
            continue
        fi

        # Try to load
        if launchctl load "$plist" 2>/dev/null; then
            echo "✓ Loaded: $LABEL" >> "$LOG_FILE"
            ((LOADED_COUNT++))
        else
            echo "✗ Failed: $LABEL" >> "$LOG_FILE"
            ((FAILED_COUNT++))
        fi
    fi
done

# Summary
echo "" >> "$LOG_FILE"
echo "Summary:" >> "$LOG_FILE"
echo "  Already loaded: $ALREADY_LOADED" >> "$LOG_FILE"
echo "  Newly loaded: $LOADED_COUNT" >> "$LOG_FILE"
echo "  Failed: $FAILED_COUNT" >> "$LOG_FILE"

# Count loaded after
LOADED_AFTER=$(launchctl list | grep -c "com.petesbrain" || echo 0)
echo "  Total now loaded: $LOADED_AFTER" >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Agent Loader Complete" >> "$LOG_FILE"
echo "============================================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# If there were failures, exit with error code (for health check to detect)
if [ $FAILED_COUNT -gt 0 ]; then
    exit 1
fi

exit 0
