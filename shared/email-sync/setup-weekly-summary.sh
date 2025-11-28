#!/bin/bash
#
# Setup weekly AI news summary cron job
# Sends email every Monday at 10am
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SUMMARY_SCRIPT="$SCRIPT_DIR/send_summary.py"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python3"

# Create cron job
CRON_JOB="0 10 * * 1 cd $SCRIPT_DIR && $VENV_PYTHON $SUMMARY_SCRIPT >> logs/ai-summary.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "send_summary.py"; then
    echo "⚠️  AI summary cron job already exists. Updating..."
    # Remove old job
    (crontab -l 2>/dev/null | grep -v "send_summary.py") | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Weekly AI news summary scheduled!"
echo ""
echo "Schedule: Every Monday at 10:00 AM"
echo "Email to: petere@roksys.co.uk"
echo "Log file: $SCRIPT_DIR/logs/ai-summary.log"
echo ""
echo "Current cron jobs:"
crontab -l | grep -E "(send_summary|sync-all)"
