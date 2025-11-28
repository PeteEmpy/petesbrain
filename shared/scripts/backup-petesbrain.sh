#!/bin/bash
#
# PetesBrain Backup Script
# Automated backup system for PetesBrain project
# Creates timestamped backups on both local SSD and iCloud Drive
#

set -e  # Exit on error

# Configuration
PROJECT_DIR="/Users/administrator/Documents/PetesBrain"
LOCAL_BACKUP_DIR="/Users/administrator/Documents"
ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="PetesBrain-backup-${TIMESTAMP}.tar.gz"
MAX_LOCAL_BACKUPS=5  # Keep last 5 backups locally
MAX_ICLOUD_BACKUPS=10  # Keep last 10 backups in iCloud

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Backup System${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Timestamp:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}✗ Error: Project directory not found: $PROJECT_DIR${NC}"
    exit 1
fi

# Create iCloud backup directory if it doesn't exist
if [ ! -d "$ICLOUD_BACKUP_DIR" ]; then
    echo -e "${YELLOW}→ Creating iCloud backup directory...${NC}"
    mkdir -p "$ICLOUD_BACKUP_DIR"
fi

# Step 1: Create local backup
echo -e "${YELLOW}→ Creating backup archive...${NC}"
cd "$(dirname "$PROJECT_DIR")"

# Exclude large dependency folders that can be rebuilt
# - venv, .venv: Python virtual environments
# - node_modules: Node.js dependencies
# - __pycache__: Python bytecode cache
# This reduces backup size from ~4GB to ~700MB and prevents stuck backups
if tar -czf "${LOCAL_BACKUP_DIR}/${BACKUP_NAME}" \
    --exclude='*/venv/*' \
    --exclude='*/node_modules/*' \
    --exclude='*/.venv/*' \
    --exclude='*/__pycache__/*' \
    "$(basename "$PROJECT_DIR")" 2>/dev/null; then
    BACKUP_SIZE=$(du -h "${LOCAL_BACKUP_DIR}/${BACKUP_NAME}" | cut -f1)
    echo -e "${GREEN}✓ Local backup created: ${BACKUP_SIZE}${NC}"
    echo -e "  Location: ${LOCAL_BACKUP_DIR}/${BACKUP_NAME}"
    echo -e "  ${YELLOW}Note: Excludes venv, node_modules (can be rebuilt)${NC}"
else
    echo -e "${RED}✗ Error: Failed to create backup archive${NC}"
    exit 1
fi

# Step 2: Copy to iCloud
echo ""
echo -e "${YELLOW}→ Copying backup to iCloud Drive...${NC}"
if cp "${LOCAL_BACKUP_DIR}/${BACKUP_NAME}" "$ICLOUD_BACKUP_DIR/"; then
    echo -e "${GREEN}✓ iCloud backup created${NC}"
    echo -e "  Location: ${ICLOUD_BACKUP_DIR}/${BACKUP_NAME}"
else
    echo -e "${RED}✗ Warning: Failed to copy to iCloud (local backup still exists)${NC}"
fi

# Step 3: Clean up old local backups
echo ""
echo -e "${YELLOW}→ Cleaning up old backups...${NC}"

# Count and remove old local backups
LOCAL_COUNT=$(ls -1 "${LOCAL_BACKUP_DIR}"/PetesBrain-backup-*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
if [ "$LOCAL_COUNT" -gt "$MAX_LOCAL_BACKUPS" ]; then
    REMOVE_COUNT=$((LOCAL_COUNT - MAX_LOCAL_BACKUPS))
    ls -1t "${LOCAL_BACKUP_DIR}"/PetesBrain-backup-*.tar.gz | tail -n "$REMOVE_COUNT" | while read -r old_backup; do
        rm -f "$old_backup"
        echo -e "${YELLOW}  Removed old local backup: $(basename "$old_backup")${NC}"
    done
fi

# Count and remove old iCloud backups
if [ -d "$ICLOUD_BACKUP_DIR" ]; then
    ICLOUD_COUNT=$(ls -1 "${ICLOUD_BACKUP_DIR}"/PetesBrain-backup-*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
    if [ "$ICLOUD_COUNT" -gt "$MAX_ICLOUD_BACKUPS" ]; then
        REMOVE_COUNT=$((ICLOUD_COUNT - MAX_ICLOUD_BACKUPS))
        ls -1t "${ICLOUD_BACKUP_DIR}"/PetesBrain-backup-*.tar.gz | tail -n "$REMOVE_COUNT" | while read -r old_backup; do
            rm -f "$old_backup"
            echo -e "${YELLOW}  Removed old iCloud backup: $(basename "$old_backup")${NC}"
        done
    fi
fi

# Step 4: Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Backup Complete${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Local Backups:${NC}"
ls -lht "${LOCAL_BACKUP_DIR}"/PetesBrain-backup-*.tar.gz 2>/dev/null | head -n "$MAX_LOCAL_BACKUPS" | awk '{printf "  %s  %s\n", $9, $5}' | xargs -I {} basename {}
echo ""
echo -e "${YELLOW}iCloud Backups:${NC}"
ls -lht "${ICLOUD_BACKUP_DIR}"/PetesBrain-backup-*.tar.gz 2>/dev/null | head -n "$MAX_ICLOUD_BACKUPS" | awk '{printf "  %s  %s\n", $9, $5}' | xargs -I {} basename {}
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Log to file
LOG_FILE="$PROJECT_DIR/shared/data/backup-log.txt"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup completed: ${BACKUP_NAME} (${BACKUP_SIZE})" >> "$LOG_FILE"

