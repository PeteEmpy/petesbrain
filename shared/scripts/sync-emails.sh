#!/bin/bash
#
# Email Sync - Manual Command
# Convenience script to run the complete email sync workflow
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EMAIL_SYNC_DIR="$SCRIPT_DIR/../email-sync"

# Check Gmail OAuth scopes BEFORE running sync
echo "🔍 Checking Gmail OAuth scopes..."
bash "$EMAIL_SYNC_DIR/check-gmail-scopes.sh" || exit 1
echo ""

# Check if email sync directory exists
if [ ! -d "$EMAIL_SYNC_DIR" ]; then
    echo "❌ Error: Email sync directory not found: $EMAIL_SYNC_DIR"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$EMAIL_SYNC_DIR/.venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run: cd $EMAIL_SYNC_DIR && ./setup-cron.sh"
    exit 1
fi

# Run the workflow
cd "$EMAIL_SYNC_DIR"
"$EMAIL_SYNC_DIR/.venv/bin/python3" "$EMAIL_SYNC_DIR/email_sync_workflow.py" "$@"

