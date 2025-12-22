#!/bin/bash
#
# PetesBrain Safety Backup Script
# Creates a quick backup before laptop push operations
# Keeps last 3 safety backups for rollback
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
BACKUP_DIR="$HOME/Documents/PetesBrain-Safety-Backups"

# Create backup directory if needed
mkdir -p "$BACKUP_DIR"

# Generate backup name
BACKUP_NAME="safety-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

echo -e "${YELLOW}→ Creating safety backup before push...${NC}"
echo -e "${YELLOW}  This may take 2-3 minutes...${NC}"

# Create backup (excluding large/unnecessary files)
cd "$PROJECT_DIR/.."
tar -czf "$BACKUP_PATH" \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='.DS_Store' \
    PetesBrain.nosync/

BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
echo -e "${GREEN}✓ Safety backup created: $BACKUP_SIZE${NC}"
echo -e "${GREEN}  Location: $BACKUP_PATH${NC}"

# Clean up old safety backups (keep last 3)
echo -e "${YELLOW}→ Cleaning old safety backups (keeping last 3)...${NC}"
cd "$BACKUP_DIR"
ls -t safety-backup-*.tar.gz 2>/dev/null | tail -n +4 | xargs rm -f 2>/dev/null || true

BACKUP_COUNT=$(ls -1 safety-backup-*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
echo -e "${GREEN}✓ Safety backups maintained: $BACKUP_COUNT${NC}"
echo ""
