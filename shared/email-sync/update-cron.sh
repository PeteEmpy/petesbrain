#!/bin/bash
#
# Update cron to use sync-all (auto-label + sync)
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SYNC_ALL="$SCRIPT_DIR/sync-all"

# Remove old cron job
(crontab -l 2>/dev/null | grep -v "sync_emails.py") | crontab -

# Add new cron job that runs sync-all
(crontab -l 2>/dev/null; echo "0 9,12,15,18 * * * cd $SCRIPT_DIR && ./sync-all >> logs/sync.log 2>&1") | crontab -

echo "✓ Cron job updated to use auto-label + sync workflow"
echo ""
echo "New schedule:"
crontab -l | grep sync-all
