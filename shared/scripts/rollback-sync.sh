#!/bin/bash

# PetesBrain Sync Rollback System
# Emergency recovery script to restore pre-sync state
#
# Usage:
#   rollback-sync.sh          # Interactive rollback (confirms with user)
#   rollback-sync.sh --force  # Automatic rollback (no confirmation)
#
# What it does:
# 1. Restores Git state to pre-sync commit
# 2. Restores critical files from snapshot
# 3. Cleans up snapshot directory
# 4. Logs rollback operation

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYNC_SNAPSHOT="$PROJECT_ROOT/.sync-snapshot"
ROLLBACK_LOG="$HOME/.petesbrain-sync-rollback.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$ROLLBACK_LOG"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*${NC}" | tee -a "$ROLLBACK_LOG"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓ $*${NC}" | tee -a "$ROLLBACK_LOG"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠ $*${NC}" | tee -a "$ROLLBACK_LOG"
}

# macOS notification
notify() {
    local title="$1"
    local message="$2"
    local sound="${3:-default}"

    osascript -e "display notification \"$message\" with title \"PetesBrain Sync Rollback\" subtitle \"$title\" sound name \"$sound\""
}

# Check if snapshot exists
check_snapshot() {
    if [[ ! -d "$SYNC_SNAPSHOT" ]]; then
        log_error "No snapshot found at $SYNC_SNAPSHOT"
        log_error "Cannot rollback - no previous state saved"
        notify "Rollback Failed" "No snapshot found" "Basso"
        exit 1
    fi

    if [[ ! -f "$SYNC_SNAPSHOT/timestamp" ]]; then
        log_error "Snapshot exists but timestamp missing - corrupted snapshot"
        exit 1
    fi

    local snapshot_timestamp=$(cat "$SYNC_SNAPSHOT/timestamp")
    local snapshot_age=$(($(date +%s) - snapshot_timestamp))

    log "Snapshot found:"
    log "  Location: $SYNC_SNAPSHOT"
    log "  Age: ${snapshot_age} seconds ($(($snapshot_age / 60)) minutes)"

    if [[ -f "$SYNC_SNAPSHOT/HEAD" ]]; then
        local snapshot_commit=$(cat "$SYNC_SNAPSHOT/HEAD")
        log "  Git commit: $snapshot_commit"
    fi

    if [[ -f "$SYNC_SNAPSHOT/branch" ]]; then
        local snapshot_branch=$(cat "$SYNC_SNAPSHOT/branch")
        log "  Git branch: $snapshot_branch"
    fi
}

# Restore Git state
restore_git_state() {
    log "Restoring Git state..."

    cd "$PROJECT_ROOT" || exit 1

    # Check if stash exists
    if [[ -f "$SYNC_SNAPSHOT/stash-status" ]]; then
        local stash_status=$(cat "$SYNC_SNAPSHOT/stash-status")

        if [[ "$stash_status" == "stashed" ]]; then
            log "  Restoring stashed changes..."

            # Find the sync stash
            local stash_ref=$(git stash list | grep "Pre-sync snapshot" | head -1 | cut -d: -f1)

            if [[ -n "$stash_ref" ]]; then
                git stash pop "$stash_ref" 2>&1 | tee -a "$ROLLBACK_LOG"
                log_success "Stashed changes restored"
            else
                log_warning "Could not find pre-sync stash - may have been cleared"
            fi
        else
            log "  No stashed changes to restore"
        fi
    fi

    # Reset to snapshot commit (if needed)
    if [[ -f "$SYNC_SNAPSHOT/HEAD" ]]; then
        local snapshot_commit=$(cat "$SYNC_SNAPSHOT/HEAD")
        local current_commit=$(git rev-parse HEAD)

        if [[ "$snapshot_commit" != "$current_commit" ]]; then
            log "  Resetting Git to snapshot commit: $snapshot_commit"

            # Hard reset to snapshot commit
            git reset --hard "$snapshot_commit" 2>&1 | tee -a "$ROLLBACK_LOG"

            log_success "Git state reset to snapshot commit"
        else
            log "  Git already at snapshot commit (no reset needed)"
        fi
    fi

    log_success "Git state restored"
}

# Restore critical files from snapshot
restore_critical_files() {
    log "Restoring critical files from snapshot..."

    local snapshot_files="$SYNC_SNAPSHOT/critical-files"

    if [[ ! -d "$snapshot_files" ]]; then
        log_warning "No critical files in snapshot (snapshot may be empty)"
        return
    fi

    # Count files to restore
    local file_count=$(find "$snapshot_files" -type f | wc -l | tr -d ' ')
    log "  Found $file_count file(s) in snapshot"

    # Restore files
    local restored=0
    find "$snapshot_files" -type f | while read -r snapshot_file; do
        # Calculate relative path
        local relative_path="${snapshot_file#$snapshot_files/}"
        local target_file="$PROJECT_ROOT/$relative_path"

        # Create parent directory if needed
        mkdir -p "$(dirname "$target_file")"

        # Restore file
        cp "$snapshot_file" "$target_file"

        echo "    ✓ Restored: $relative_path" | tee -a "$ROLLBACK_LOG"
        ((restored++))
    done

    log_success "Critical files restored ($restored files)"
}

# Cleanup snapshot
cleanup_snapshot() {
    log "Cleaning up snapshot..."

    if [[ -d "$SYNC_SNAPSHOT" ]]; then
        rm -rf "$SYNC_SNAPSHOT"
        log_success "Snapshot cleaned up"
    else
        log "  No snapshot to clean up"
    fi
}

# Main rollback function
perform_rollback() {
    local force="${1:-false}"

    log "====== ROLLBACK INITIATED ======"

    # Check snapshot exists
    check_snapshot

    # Confirm with user (unless --force)
    if [[ "$force" != "true" ]]; then
        echo ""
        echo -e "${YELLOW}⚠  WARNING: This will restore your repository to pre-sync state${NC}"
        echo -e "${YELLOW}   All changes since the last sync will be lost${NC}"
        echo ""
        read -p "Continue with rollback? (yes/no): " response

        if [[ "$response" != "yes" ]]; then
            log "Rollback cancelled by user"
            exit 0
        fi
    fi

    # Start rollback timer
    local start_time=$(date +%s)

    # Step 1: Restore critical files FIRST (most important)
    restore_critical_files

    # Step 2: Restore Git state
    restore_git_state

    # Step 3: Cleanup snapshot
    cleanup_snapshot

    # Calculate elapsed time
    local end_time=$(date +%s)
    local elapsed=$((end_time - start_time))

    log_success "====== ROLLBACK COMPLETED ======"
    log "  Elapsed time: ${elapsed} seconds"
    notify "Rollback Complete" "Repository restored to pre-sync state (${elapsed}s)" "Glass"

    echo ""
    echo -e "${GREEN}✅ Rollback successful${NC}"
    echo -e "   Repository restored to pre-sync state"
    echo -e "   Time taken: ${elapsed} seconds"
    echo ""
}

# Check rollback status (for diagnostics)
rollback_status() {
    echo -e "${BLUE}====== Rollback Status ======${NC}"
    echo ""

    if [[ -d "$SYNC_SNAPSHOT" ]]; then
        echo -e "${YELLOW}⚠ Snapshot exists${NC}"
        echo "  Location: $SYNC_SNAPSHOT"

        if [[ -f "$SYNC_SNAPSHOT/timestamp" ]]; then
            local snapshot_timestamp=$(cat "$SYNC_SNAPSHOT/timestamp")
            local snapshot_age=$(($(date +%s) - snapshot_timestamp))
            echo "  Age: ${snapshot_age}s ($(($snapshot_age / 60)) minutes)"
        fi

        if [[ -f "$SYNC_SNAPSHOT/HEAD" ]]; then
            echo "  Git commit: $(cat "$SYNC_SNAPSHOT/HEAD")"
        fi

        if [[ -f "$SYNC_SNAPSHOT/branch" ]]; then
            echo "  Git branch: $(cat "$SYNC_SNAPSHOT/branch")"
        fi

        local file_count=$(find "$SYNC_SNAPSHOT/critical-files" -type f 2>/dev/null | wc -l | tr -d ' ')
        echo "  Critical files: $file_count"

        echo ""
        echo -e "${YELLOW}A rollback can be performed to restore this snapshot${NC}"
    else
        echo -e "${GREEN}✓ No snapshot present${NC}"
        echo "  Last sync completed cleanly"
    fi

    echo ""
    echo -e "${BLUE}Recent rollback log:${NC}"
    if [[ -f "$ROLLBACK_LOG" ]]; then
        tail -10 "$ROLLBACK_LOG"
    else
        echo "  No rollback log found"
    fi
}

# Main command dispatcher
main() {
    local command="${1:-rollback}"

    case "$command" in
        --force)
            perform_rollback true
            ;;
        status)
            rollback_status
            ;;
        help|--help|-h)
            cat <<EOF
PetesBrain Sync Rollback System

Usage:
    rollback-sync.sh          Interactive rollback (confirms with user)
    rollback-sync.sh --force  Automatic rollback (no confirmation)
    rollback-sync.sh status   Show rollback status
    rollback-sync.sh help     Show this help message

What it does:
    1. Restores Git state to pre-sync commit
    2. Restores critical files from snapshot (.sync-snapshot/)
    3. Cleans up snapshot directory
    4. Completes in <30 seconds

Logs:
    Rollback log: $ROLLBACK_LOG

For more information, see: docs/SYNC-SYSTEM-V2.md
EOF
            ;;
        rollback)
            perform_rollback false
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}"
            echo ""
            echo "Usage: rollback-sync.sh {rollback|--force|status|help}"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
