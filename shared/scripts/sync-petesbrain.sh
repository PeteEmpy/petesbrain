#!/bin/bash
#
# PetesBrain Sync Script
# Syncs PetesBrain between desktop and laptop
#
# Usage: sync-petesbrain [direction] [--force]
#   direction: 'pull' (default), 'push', or 'both'
#   --force: Skip staleness checks on pull
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# Parse arguments
DIRECTION="pull"
FORCE=false

for arg in "$@"; do
    case "$arg" in
        pull|push|both)
            DIRECTION="$arg"
            ;;
        --force|-f)
            FORCE=true
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Load sync configuration if it exists
if [ -f "$PROJECT_DIR/.sync-config" ]; then
    source "$PROJECT_DIR/.sync-config"
fi

# Detect if we're on desktop or laptop
HOSTNAME=$(hostname)
DESKTOP_HOSTNAME="Peters-Mac-mini"  # Desktop Mac Mini hostname
IS_DESKTOP=false

if [[ "$HOSTNAME" == *"$DESKTOP_HOSTNAME"* ]] || [ -f "$PROJECT_DIR/.is-desktop" ]; then
    IS_DESKTOP=true
fi

MACHINE_TYPE=$([ "$IS_DESKTOP" = true ] && echo "Desktop" || echo "Laptop")

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Sync${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Machine:${NC} $HOSTNAME"
echo -e "${YELLOW}Type:${NC} $MACHINE_TYPE"
echo -e "${YELLOW}Direction:${NC} $DIRECTION"
echo -e "${YELLOW}Project:${NC} $PROJECT_DIR"
echo ""

cd "$PROJECT_DIR"

# ============================================================================
# Metadata Functions
# ============================================================================

ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups"
METADATA_FILE="$ICLOUD_BACKUP_DIR/.sync-metadata.json"

write_sync_metadata() {
    # Write metadata about this push
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local unix_timestamp=$(date +%s)
    local machine="$HOSTNAME"
    local user=$(whoami)
    local machine_type="$MACHINE_TYPE"

    # Ensure backup directory exists
    mkdir -p "$ICLOUD_BACKUP_DIR"

    # Write metadata JSON
    cat > "$METADATA_FILE" << EOF
{
    "last_push": {
        "timestamp": "$timestamp",
        "unix_timestamp": $unix_timestamp,
        "machine": "$machine",
        "machine_type": "$machine_type",
        "user": "$user"
    }
}
EOF

    echo -e "${GREEN}✓ Sync metadata written${NC}"
}

check_sync_metadata() {
    # Check metadata before pulling - warn or block if stale

    if [ ! -f "$METADATA_FILE" ]; then
        echo -e "${RED}═══════════════════════════════════════════════════${NC}"
        echo -e "${RED}    ⚠ NO SYNC METADATA FOUND${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}This backup has no metadata - it may be very old or${NC}"
        echo -e "${YELLOW}was created before the metadata system was added.${NC}"
        echo ""

        if [ "$FORCE" = true ]; then
            echo -e "${YELLOW}→ Proceeding anyway (--force flag used)${NC}"
            echo ""
            return 0
        fi

        echo -e "${BOLD}To proceed, run:${NC}"
        echo -e "  sync-petesbrain pull --force"
        echo ""
        echo -e "${BOLD}Or create a fresh backup from the desktop first:${NC}"
        echo -e "  sync-petesbrain push"
        echo ""
        return 1
    fi

    # Read metadata
    local push_timestamp=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['timestamp'])" 2>/dev/null)
    local push_unix=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['unix_timestamp'])" 2>/dev/null)
    local push_machine=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['machine'])" 2>/dev/null)
    local push_machine_type=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['machine_type'])" 2>/dev/null)
    local push_user=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['user'])" 2>/dev/null)

    local now_unix=$(date +%s)
    local age_seconds=$((now_unix - push_unix))
    local age_hours=$((age_seconds / 3600))
    local age_days=$((age_seconds / 86400))

    # Format age for display
    local age_display=""
    if [ $age_days -gt 0 ]; then
        age_display="${age_days} day(s) ago"
    elif [ $age_hours -gt 0 ]; then
        age_display="${age_hours} hour(s) ago"
    else
        local age_mins=$((age_seconds / 60))
        age_display="${age_mins} minute(s) ago"
    fi

    # Display last push info
    echo -e "${BLUE}───────────────────────────────────────────────────${NC}"
    echo -e "${BLUE}    Last Push Information${NC}"
    echo -e "${BLUE}───────────────────────────────────────────────────${NC}"
    echo -e "  ${YELLOW}When:${NC}    $push_timestamp (${BOLD}$age_display${NC})"
    echo -e "  ${YELLOW}From:${NC}    $push_machine ($push_machine_type)"
    echo -e "  ${YELLOW}User:${NC}    $push_user"
    echo -e "${BLUE}───────────────────────────────────────────────────${NC}"
    echo ""

    # Check staleness thresholds
    local WARN_THRESHOLD=$((24 * 3600))   # 24 hours
    local BLOCK_THRESHOLD=$((7 * 86400))  # 7 days

    if [ $age_seconds -gt $BLOCK_THRESHOLD ]; then
        # Very stale - block unless forced
        echo -e "${RED}═══════════════════════════════════════════════════${NC}"
        echo -e "${RED}    ⚠ BACKUP IS VERY STALE (${age_days} days old)${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}This backup is more than 7 days old.${NC}"
        echo -e "${YELLOW}You should create a fresh backup from the desktop first.${NC}"
        echo ""

        if [ "$FORCE" = true ]; then
            echo -e "${YELLOW}→ Proceeding anyway (--force flag used)${NC}"
            echo ""
            return 0
        fi

        echo -e "${BOLD}To proceed anyway, run:${NC}"
        echo -e "  sync-petesbrain pull --force"
        echo ""
        echo -e "${BOLD}Or create a fresh backup from the desktop:${NC}"
        echo -e "  sync-petesbrain push"
        echo ""
        return 1

    elif [ $age_seconds -gt $WARN_THRESHOLD ]; then
        # Stale - warn and ask for confirmation
        echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW}    ⚠ BACKUP IS STALE (${age_display})${NC}"
        echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}This backup is more than 24 hours old.${NC}"
        echo -e "${YELLOW}Consider creating a fresh backup from the desktop.${NC}"
        echo ""

        if [ "$FORCE" = true ]; then
            echo -e "${YELLOW}→ Proceeding anyway (--force flag used)${NC}"
            echo ""
            return 0
        fi

        read -p "Continue with this backup? (y/n) " -n 1 -r
        echo ""

        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo ""
            echo -e "${YELLOW}Aborted. Create a fresh backup from the desktop:${NC}"
            echo -e "  sync-petesbrain push"
            echo ""
            return 1
        fi

        echo ""
    else
        # Fresh backup - good to go
        echo -e "${GREEN}✓ Backup is fresh (${age_display})${NC}"
        echo ""
    fi

    return 0
}

# ============================================================================
# Sync Logic
# ============================================================================

# Check if Git is configured (but only use it if SYNC_METHOD isn't already set)
if [ -d ".git" ] && [ -z "${SYNC_METHOD:-}" ]; then
    REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

    if [ -n "$REMOTE" ]; then
        echo -e "${YELLOW}→ Using Git sync...${NC}"

        # Check for uncommitted changes
        if [ -n "$(git status --porcelain)" ]; then
            echo -e "${YELLOW}⚠ Uncommitted changes detected${NC}"
            git status --short
            echo ""
            read -p "Commit changes before syncing? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git add -A
                git commit -m "Sync: $(date '+%Y-%m-%d %H:%M:%S')"
            fi
        fi

        case "$DIRECTION" in
            pull)
                echo -e "${YELLOW}→ Pulling latest changes...${NC}"
                git fetch origin
                git pull origin main || git pull origin master
                echo -e "${GREEN}✓ Pulled latest changes${NC}"
                ;;

            push)
                echo -e "${YELLOW}→ Pushing changes...${NC}"
                CURRENT_BRANCH=$(git branch --show-current)
                git push origin "$CURRENT_BRANCH"
                echo -e "${GREEN}✓ Pushed changes${NC}"
                ;;

            both)
                echo -e "${YELLOW}→ Pulling latest changes...${NC}"
                git fetch origin
                git pull origin main || git pull origin master
                echo -e "${GREEN}✓ Pulled latest changes${NC}"

                echo ""
                echo -e "${YELLOW}→ Pushing local changes...${NC}"
                CURRENT_BRANCH=$(git branch --show-current)
                git push origin "$CURRENT_BRANCH"
                echo -e "${GREEN}✓ Pushed changes${NC}"
                ;;
        esac

    else
        echo -e "${YELLOW}⚠ Git repository found but no remote configured${NC}"
        echo "Setting up iCloud Drive sync instead..."
        SYNC_METHOD="icloud"
    fi
else
    echo -e "${YELLOW}⚠ Not a Git repository${NC}"

    # Check if we have rsync configured
    if [ "${SYNC_METHOD:-}" = "rsync" ]; then
        echo "Using rsync sync method..."
    else
        echo "Setting up iCloud Drive sync instead..."
        SYNC_METHOD="icloud"
    fi
fi

# rsync direct sync (when configured)
if [ "${SYNC_METHOD:-git}" = "rsync" ]; then
    echo ""
    echo -e "${YELLOW}→ Using rsync direct sync...${NC}"

    if [ "$IS_DESKTOP" = true ]; then
        # On desktop - only push is supported (no laptop to pull from configured)
        case "$DIRECTION" in
            pull)
                echo -e "${RED}✗ Pull not supported on desktop${NC}"
                echo -e "${YELLOW}Desktop is the source. Use 'push' to backup, or pull from laptop.${NC}"
                exit 1
                ;;

            push)
                echo -e "${YELLOW}→ Desktop detected - nothing to push${NC}"
                echo -e "${YELLOW}(Laptop will pull from this machine)${NC}"
                echo -e "${GREEN}✓ Desktop is up to date${NC}"
                ;;

            both)
                echo -e "${YELLOW}→ Desktop detected - nothing to sync${NC}"
                echo -e "${YELLOW}(Laptop will pull from this machine)${NC}"
                echo -e "${GREEN}✓ Desktop is up to date${NC}"
                ;;
        esac
    else
        # On laptop - can pull from desktop
        case "$DIRECTION" in
            pull)
                if [ -z "${DESKTOP_HOST:-}" ]; then
                    echo -e "${RED}✗ DESKTOP_HOST not configured${NC}"
                    echo -e "${YELLOW}Edit $PROJECT_DIR/.sync-config and set DESKTOP_HOST${NC}"
                    exit 1
                fi

                echo -e "${YELLOW}→ Syncing from desktop: $DESKTOP_USER@$DESKTOP_HOST${NC}"
                echo ""

                rsync -avz --progress \
                    --exclude='.git' \
                    --exclude='venv' \
                    --exclude='__pycache__' \
                    --exclude='.DS_Store' \
                    --exclude='.venv' \
                    --exclude='node_modules' \
                    --exclude='.config/venv' \
                    "$DESKTOP_USER@$DESKTOP_HOST:$DESKTOP_PATH/" "$PROJECT_DIR/"

                echo ""
                echo -e "${GREEN}✓ Pulled from desktop${NC}"
                ;;

            push)
                if [ -z "${DESKTOP_HOST:-}" ]; then
                    echo -e "${RED}✗ DESKTOP_HOST not configured${NC}"
                    echo -e "${YELLOW}Edit $PROJECT_DIR/.sync-config and set DESKTOP_HOST${NC}"
                    exit 1
                fi

                echo -e "${YELLOW}→ Syncing to desktop: $DESKTOP_USER@$DESKTOP_HOST${NC}"
                echo ""

                rsync -avz --progress \
                    --exclude='.git' \
                    --exclude='venv' \
                    --exclude='__pycache__' \
                    --exclude='.DS_Store' \
                    --exclude='.venv' \
                    --exclude='node_modules' \
                    --exclude='.config/venv' \
                    "$PROJECT_DIR/" "$DESKTOP_USER@$DESKTOP_HOST:$DESKTOP_PATH/"

                echo ""
                echo -e "${GREEN}✓ Pushed to desktop${NC}"
                ;;

            both)
                "$0" pull
                echo ""
                "$0" push
                ;;
        esac
    fi

# Fallback to iCloud Drive sync if Git not available
elif [ "${SYNC_METHOD:-git}" = "icloud" ]; then
    echo ""
    echo -e "${YELLOW}→ Using iCloud Drive sync...${NC}"

    if [ ! -d "$ICLOUD_BACKUP_DIR" ]; then
        mkdir -p "$ICLOUD_BACKUP_DIR"
    fi

    case "$DIRECTION" in
        pull)
            # Check metadata before pulling
            if ! check_sync_metadata; then
                exit 1
            fi

            # Find latest backup
            LATEST_BACKUP=$(ls -t "$ICLOUD_BACKUP_DIR"/PetesBrain-backup-*.tar.gz 2>/dev/null | head -1)

            if [ -z "$LATEST_BACKUP" ]; then
                echo -e "${RED}✗ No backups found in iCloud Drive${NC}"
                echo ""
                echo -e "${YELLOW}Create a backup from the desktop first:${NC}"
                echo -e "  sync-petesbrain push"
                exit 1
            fi

            echo -e "${YELLOW}→ Found backup: $(basename "$LATEST_BACKUP")${NC}"
            echo -e "${YELLOW}→ Extracting to temporary location...${NC}"

            TEMP_DIR=$(mktemp -d)
            cd "$TEMP_DIR"
            tar -xzf "$LATEST_BACKUP"

            echo -e "${YELLOW}→ Syncing files...${NC}"
            rsync -av --delete \
                --exclude='.git' \
                --exclude='venv' \
                --exclude='__pycache__' \
                --exclude='.DS_Store' \
                --exclude='.venv' \
                PetesBrain/ "$PROJECT_DIR/"

            rm -rf "$TEMP_DIR"
            echo -e "${GREEN}✓ Synced from iCloud backup${NC}"
            ;;

        push)
            echo -e "${YELLOW}→ Creating backup...${NC}"
            if [ -f "$PROJECT_DIR/shared/scripts/backup-petesbrain.sh" ]; then
                "$PROJECT_DIR/shared/scripts/backup-petesbrain.sh"

                # Write metadata after successful push
                write_sync_metadata

                echo -e "${GREEN}✓ Backup created in iCloud Drive${NC}"
            else
                echo -e "${RED}✗ Backup script not found${NC}"
                exit 1
            fi
            ;;

        both)
            echo -e "${YELLOW}→ Pulling from iCloud...${NC}"
            "$0" pull $([ "$FORCE" = true ] && echo "--force")

            echo ""
            echo -e "${YELLOW}→ Pushing to iCloud...${NC}"
            "$0" push
            ;;
    esac
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    Sync Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
