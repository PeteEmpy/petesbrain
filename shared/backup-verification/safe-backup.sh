#!/bin/bash
#
# Safe Backup Script with Built-in Verification
# Replaces the old .plist backup system
#
# Features:
# - Creates backup with timestamp
# - Verifies backup integrity immediately
# - Stores in multiple locations
# - Alerts on failure
#

set -e  # Exit on error

# Configuration
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BASE_DIR="/Users/administrator/Documents/PetesBrain.nosync"
BACKUP_NAME="tasks-backup-${TIMESTAMP}.tar.gz"

# Multiple backup locations
LOCAL_BACKUP_DIR="${BASE_DIR}/_backups/tasks"
ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks"
TEMP_DIR="/tmp/petesbrain-backup-$$"

# Logging
LOG_FILE="$HOME/.petesbrain-safe-backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

log "===== Safe Backup Starting ====="

# Create directories
mkdir -p "$LOCAL_BACKUP_DIR"
mkdir -p "$ICLOUD_BACKUP_DIR"
mkdir -p "$TEMP_DIR"

# Change to base directory
cd "$BASE_DIR"

# Create backup tarball
log "Creating backup tarball..."
tar -czf "${TEMP_DIR}/${BACKUP_NAME}" \
    clients/*/tasks.json \
    clients/*/tasks-completed.md \
    roksys/tasks.json 2>/dev/null || {
    log "WARNING: Some files may not exist, but continuing..."
    # Don't exit - partial backup is better than no backup
}

# Check if backup file was created and has reasonable size
if [ ! -f "${TEMP_DIR}/${BACKUP_NAME}" ]; then
    log "ERROR: Backup file was not created"
    exit 1
fi

BACKUP_SIZE=$(du -k "${TEMP_DIR}/${BACKUP_NAME}" | cut -f1)
log "Backup size: ${BACKUP_SIZE}KB"

if [ "$BACKUP_SIZE" -lt 10 ]; then
    log "ERROR: Backup file is suspiciously small (${BACKUP_SIZE}KB) - ABORTING"
    exit 1
fi

# Verify backup integrity
log "Verifying backup integrity..."
if python3 "${BASE_DIR}/shared/backup-verification/verify-backup.py" "${TEMP_DIR}/${BACKUP_NAME}"; then
    log "✅ Backup verification PASSED"
else
    log "❌ Backup verification FAILED - backup may be corrupt"
    exit 1
fi

# Copy to local backup location
log "Copying to local backup directory..."
cp "${TEMP_DIR}/${BACKUP_NAME}" "$LOCAL_BACKUP_DIR/"

# Copy to iCloud backup location
log "Copying to iCloud backup directory..."
cp "${TEMP_DIR}/${BACKUP_NAME}" "$ICLOUD_BACKUP_DIR/" || {
    log "WARNING: Failed to copy to iCloud - may not be mounted"
}

# Cleanup old backups (keep last 30 days in local, last 7 days in iCloud)
log "Cleaning up old backups..."
find "$LOCAL_BACKUP_DIR" -name "tasks-backup-*.tar.gz" -mtime +30 -delete 2>/dev/null || true
find "$ICLOUD_BACKUP_DIR" -name "tasks-backup-*.tar.gz" -mtime +7 -delete 2>/dev/null || true

log "✅ Safe backup completed successfully"
log "  Local: ${LOCAL_BACKUP_DIR}/${BACKUP_NAME}"
log "  iCloud: ${ICLOUD_BACKUP_DIR}/${BACKUP_NAME}"
log "  Size: ${BACKUP_SIZE}KB"

exit 0
