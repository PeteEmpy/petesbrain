#!/bin/bash
#
# Critical Files Backup - Tasks Only
# Runs every 6 hours to protect against task data loss
# Much faster than full backup (only tasks.json files)
#

set -e

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks"
BACKUP_NAME="tasks-backup-${TIMESTAMP}.tar.gz"

# Create iCloud directory if needed
mkdir -p "$ICLOUD_DIR"

# Create archive of ONLY tasks.json files
cd /Users/administrator/Documents/PetesBrain.nosync
tar -czf "$ICLOUD_DIR/$BACKUP_NAME" \
    clients/*/tasks.json \
    clients/*/tasks-completed.md \
    roksys/spreadsheets/rok-experiments-client-notes.csv \
    2>/dev/null

# Keep only last 20 critical backups (5 days worth at 6-hour intervals)
ls -1t "$ICLOUD_DIR"/tasks-backup-*.tar.gz 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null || true

echo "[$(date)] ✓ Critical tasks backed up to iCloud: $BACKUP_NAME"
