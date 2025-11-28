#!/bin/bash
# Devonshire Budget Tracker - Shell Wrapper
# Triggers Claude Code to update budget tracker via MCP
# Schedule: Daily at 9:00 AM

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Devonshire budget update..."

# Trigger Python script that uses working mcp functions
python3 /Users/administrator/Documents/PetesBrain/agents/budget-tracking/update-budget-simple.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ Budget update completed successfully"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ Budget update failed with exit code $exit_code"
fi

exit $exit_code
