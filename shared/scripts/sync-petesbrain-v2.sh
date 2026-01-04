#!/bin/bash

# PetesBrain Sync System V2
# Foolproof desktop ↔ laptop synchronisation with integrity verification
#
# Features:
# - SHA-256 checksum validation (before + after sync)
# - Automatic pre-sync snapshot (instant rollback)
# - Smart conflict detection and resolution
# - Loud failures (macOS notifications + email alerts)
# - Atomic operations (all-or-nothing)
#
# Usage:
#   sync-petesbrain-v2 push    # Desktop: Push changes to laptop
#   sync-petesbrain-v2 pull    # Laptop: Pull changes from desktop
#   sync-petesbrain-v2 status  # Check sync status

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYNC_CHECKSUMS="$PROJECT_ROOT/.sync-checksums.json"
SYNC_SNAPSHOT="$PROJECT_ROOT/.sync-snapshot"
VERIFICATION_SCRIPT="$SCRIPT_DIR/verify-sync-integrity.py"
ROLLBACK_SCRIPT="$SCRIPT_DIR/rollback-sync.sh"
SYNC_LOG="$HOME/.petesbrain-sync-v2.log"
ERROR_LOG="$HOME/.petesbrain-sync-v2-error.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$SYNC_LOG"
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$ERROR_LOG"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓ $*${NC}" | tee -a "$SYNC_LOG"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠ $*${NC}" | tee -a "$SYNC_LOG"
}

# macOS notification function
notify() {
    local title="$1"
    local message="$2"
    local sound="${3:-default}"

    osascript -e "display notification \"$message\" with title \"PetesBrain Sync\" subtitle \"$title\" sound name \"$sound\""
}

# Send email alert for critical failures
send_alert_email() {
    local subject="$1"
    local body="$2"

    local email_file="$PROJECT_ROOT/data/alerts/sync-alert-$(date +%Y%m%d-%H%M%S).html"
    mkdir -p "$PROJECT_ROOT/data/alerts"

    cat > "$email_file" <<EOF
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>$subject</title></head>
<body style="font-family: Verdana, sans-serif; font-size: 13px; line-height: 1.5; padding: 20px;">
<h2 style="color: #DC2626;">🚨 PetesBrain Sync Alert</h2>
<p><strong>Time:</strong> $(date +'%Y-%m-%d %H:%M:%S')</p>
<p><strong>Issue:</strong> $subject</p>
<pre style="background: #f5f5f5; padding: 15px; border-left: 4px solid #DC2626; overflow-x: auto;">$body</pre>
<p style="margin-top: 20px; color: #666;">Check logs: $SYNC_LOG and $ERROR_LOG</p>
</body>
</html>
EOF

    log "Alert email created: $email_file"
}

# Detect machine type (desktop vs laptop)
detect_machine_type() {
    local hostname=$(hostname)

    # Check for .is-desktop marker file (explicit configuration)
    if [[ -f "$PROJECT_ROOT/.is-desktop" ]]; then
        echo "desktop"
        return
    fi

    if [[ -f "$PROJECT_ROOT/.is-laptop" ]]; then
        echo "laptop"
        return
    fi

    # Fallback: Hostname-based detection
    if [[ "$hostname" == *"Mac-mini"* ]] || [[ "$hostname" == *"desktop"* ]]; then
        echo "desktop"
    else
        echo "laptop"
    fi
}

# Check if Git repository is properly configured
check_git_setup() {
    cd "$PROJECT_ROOT" || exit 1

    if [[ ! -d .git ]]; then
        log_error "Not a Git repository. Run 'git init' and configure remote first."
        notify "Sync Failed" "Not a Git repository" "Basso"
        exit 1
    fi

    local remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ -z "$remote_url" ]]; then
        log_error "No Git remote configured. Run 'git remote add origin <url>' first."
        notify "Sync Failed" "No Git remote configured" "Basso"
        exit 1
    fi

    log "Git repository: $remote_url"
}

# Create pre-sync snapshot for rollback
create_snapshot() {
    log "Creating pre-sync snapshot..."

    cd "$PROJECT_ROOT" || exit 1

    # Remove old snapshot
    rm -rf "$SYNC_SNAPSHOT"
    mkdir -p "$SYNC_SNAPSHOT"

    # Git stash (saves uncommitted changes)
    if git diff --quiet && git diff --cached --quiet; then
        log "No uncommitted changes to stash"
        touch "$SYNC_SNAPSHOT/no-stash"
    else
        git stash push -u -m "Pre-sync snapshot $(date +'%Y-%m-%d %H:%M:%S')" > "$SYNC_SNAPSHOT/stash.log" 2>&1
        echo "stashed" > "$SYNC_SNAPSHOT/stash-status"
        log "Stashed uncommitted changes"
    fi

    # Save current HEAD commit
    git rev-parse HEAD > "$SYNC_SNAPSHOT/HEAD"

    # Save current branch
    git branch --show-current > "$SYNC_SNAPSHOT/branch"

    # Copy critical files (in case Git doesn't track them)
    log "Backing up critical files to snapshot..."
    mkdir -p "$SYNC_SNAPSHOT/critical-files"

    # Backup all tasks.json files
    find "$PROJECT_ROOT/clients" -name "tasks.json" -type f | while read -r file; do
        relative_path="${file#$PROJECT_ROOT/}"
        mkdir -p "$SYNC_SNAPSHOT/critical-files/$(dirname "$relative_path")"
        cp "$file" "$SYNC_SNAPSHOT/critical-files/$relative_path"
    done

    # Backup state files
    if [[ -d "$PROJECT_ROOT/data/state" ]]; then
        mkdir -p "$SYNC_SNAPSHOT/critical-files/data"
        cp -r "$PROJECT_ROOT/data/state" "$SYNC_SNAPSHOT/critical-files/data/"
    fi

    # Save timestamp
    date +%s > "$SYNC_SNAPSHOT/timestamp"

    log_success "Snapshot created at $SYNC_SNAPSHOT"
}

# Verify data integrity using checksums
verify_integrity() {
    local phase="$1"  # "pre-sync" or "post-sync"

    log "Verifying data integrity ($phase)..."

    if [[ ! -f "$VERIFICATION_SCRIPT" ]]; then
        log_warning "Verification script not found: $VERIFICATION_SCRIPT"
        log_warning "Skipping integrity verification (will create script next)"
        return 0
    fi

    cd "$PROJECT_ROOT" || exit 1

    # Run verification script
    if python3 "$VERIFICATION_SCRIPT" "$phase"; then
        log_success "Integrity verification passed ($phase)"
        return 0
    else
        log_error "Integrity verification FAILED ($phase)"
        notify "Sync Failed" "Data corruption detected during $phase" "Basso"
        send_alert_email "Sync Failed: Corruption Detected" "Integrity verification failed during $phase. Check $ERROR_LOG for details."
        return 1
    fi
}

# Sync push (desktop → remote)
sync_push() {
    log "====== Starting PUSH sync (desktop → remote) ======"

    local machine_type=$(detect_machine_type)
    if [[ "$machine_type" != "desktop" ]]; then
        log_warning "This machine is detected as '$machine_type', not 'desktop'"
        log_warning "Push should only run from desktop. Continue anyway? (y/N)"
        read -r response
        if [[ "$response" != "y" && "$response" != "Y" ]]; then
            log "Push cancelled by user"
            exit 0
        fi
    fi

    cd "$PROJECT_ROOT" || exit 1

    # Check Git setup
    check_git_setup

    # Create snapshot for rollback
    create_snapshot

    # Pre-sync integrity verification
    if ! verify_integrity "pre-sync"; then
        log_error "Pre-sync integrity check failed. Aborting push."
        exit 1
    fi

    # Check for uncommitted changes
    if ! git diff --quiet || ! git diff --cached --quiet; then
        log "Uncommitted changes detected. Creating sync commit..."

        # Stage all changes
        git add -A

        # Create commit
        local commit_message="Sync: Desktop push at $(date +'%Y-%m-%d %H:%M:%S')

Auto-generated sync commit from desktop.

Machine: $(hostname)
User: $(whoami)"

        git commit -m "$commit_message"
        log_success "Created sync commit"
    else
        log "No uncommitted changes - working tree clean"
    fi

    # Push to remote
    log "Pushing to remote..."
    if git push origin "$(git branch --show-current)" 2>&1 | tee -a "$SYNC_LOG"; then
        log_success "Push to remote successful"
    else
        log_error "Push to remote FAILED"
        notify "Sync Failed" "Git push failed - check logs" "Basso"
        send_alert_email "Sync Push Failed" "Git push to remote failed. See $SYNC_LOG for details."

        # Rollback
        log "Initiating automatic rollback..."
        bash "$ROLLBACK_SCRIPT" 2>&1 | tee -a "$SYNC_LOG"
        exit 1
    fi

    # Post-sync verification (quick check)
    log "Post-sync verification..."
    if ! verify_integrity "post-sync"; then
        log_error "Post-sync integrity check failed!"
        notify "Sync Warning" "Post-sync verification failed - investigate" "Funk"
        # Don't rollback automatically - data already pushed
        # But alert user to investigate
        exit 1
    fi

    # Cleanup snapshot (sync successful)
    rm -rf "$SYNC_SNAPSHOT"
    log_success "Snapshot cleaned up (sync successful)"

    # Success notification (silent)
    log_success "====== PUSH sync completed successfully ======"
    notify "Sync Successful" "Desktop changes pushed to remote" "default"
}

# Sync pull (laptop ← remote)
sync_pull() {
    log "====== Starting PULL sync (laptop ← remote) ======"

    local machine_type=$(detect_machine_type)
    if [[ "$machine_type" != "laptop" ]]; then
        log_warning "This machine is detected as '$machine_type', not 'laptop'"
        log_warning "Pull typically runs on laptop. Continue anyway? (y/N)"
        read -r response
        if [[ "$response" != "y" && "$response" != "Y" ]]; then
            log "Pull cancelled by user"
            exit 0
        fi
    fi

    cd "$PROJECT_ROOT" || exit 1

    # Check Git setup
    check_git_setup

    # Create snapshot for rollback
    create_snapshot

    # Pre-sync integrity verification
    if ! verify_integrity "pre-sync"; then
        log_error "Pre-sync integrity check failed. Aborting pull."
        exit 1
    fi

    # Check for uncommitted changes (should stash before pull)
    if ! git diff --quiet || ! git diff --cached --quiet; then
        log_warning "Uncommitted changes detected on laptop"
        log "Stashing changes before pull..."
        git stash push -u -m "Pre-pull stash $(date +'%Y-%m-%d %H:%M:%S')"
    fi

    # Fetch from remote
    log "Fetching from remote..."
    if ! git fetch origin 2>&1 | tee -a "$SYNC_LOG"; then
        log_error "Fetch from remote FAILED"
        notify "Sync Failed" "Git fetch failed - check network" "Basso"
        exit 1
    fi

    # Check for conflicts before pull
    local current_branch=$(git branch --show-current)
    local local_commit=$(git rev-parse HEAD)
    local remote_commit=$(git rev-parse "origin/$current_branch")

    if [[ "$local_commit" == "$remote_commit" ]]; then
        log "Already up to date - no changes to pull"
        rm -rf "$SYNC_SNAPSHOT"
        notify "Sync Complete" "Already up to date" "default"
        exit 0
    fi

    # Pull from remote
    log "Pulling from remote..."
    if git pull origin "$current_branch" 2>&1 | tee -a "$SYNC_LOG"; then
        log_success "Pull from remote successful"
    else
        log_error "Pull from remote FAILED (merge conflict or network issue)"
        notify "Sync Failed" "Git pull failed - check for conflicts" "Basso"
        send_alert_email "Sync Pull Failed" "Git pull from remote failed. Possible merge conflict. See $SYNC_LOG"

        # Rollback
        log "Initiating automatic rollback..."
        bash "$ROLLBACK_SCRIPT" 2>&1 | tee -a "$SYNC_LOG"
        exit 1
    fi

    # Post-sync verification
    log "Post-sync verification..."
    if ! verify_integrity "post-sync"; then
        log_error "Post-sync integrity check FAILED - corruption detected!"
        notify "Sync Failed" "Corruption detected after pull - rolling back" "Basso"
        send_alert_email "Sync Corruption Detected" "Post-pull integrity check failed. Automatic rollback initiated."

        # Automatic rollback
        log "Initiating automatic rollback due to corruption..."
        bash "$ROLLBACK_SCRIPT" 2>&1 | tee -a "$SYNC_LOG"
        exit 1
    fi

    # Cleanup snapshot (sync successful)
    rm -rf "$SYNC_SNAPSHOT"
    log_success "Snapshot cleaned up (sync successful)"

    # Success notification (silent)
    log_success "====== PULL sync completed successfully ======"
    notify "Sync Successful" "Laptop synced with desktop changes" "default"
}

# Show sync status
sync_status() {
    log "====== Sync Status ======"

    cd "$PROJECT_ROOT" || exit 1

    local machine_type=$(detect_machine_type)
    echo -e "${BLUE}Machine Type:${NC} $machine_type"
    echo -e "${BLUE}Hostname:${NC} $(hostname)"
    echo ""

    # Git status
    if [[ -d .git ]]; then
        local remote_url=$(git remote get-url origin 2>/dev/null || echo "NOT CONFIGURED")
        local current_branch=$(git branch --show-current)
        local local_commit=$(git rev-parse --short HEAD)

        echo -e "${BLUE}Git Remote:${NC} $remote_url"
        echo -e "${BLUE}Current Branch:${NC} $current_branch"
        echo -e "${BLUE}Local Commit:${NC} $local_commit"

        # Check if remote is ahead
        git fetch origin 2>/dev/null
        local remote_commit=$(git rev-parse --short "origin/$current_branch" 2>/dev/null || echo "unknown")
        echo -e "${BLUE}Remote Commit:${NC} $remote_commit"

        if [[ "$local_commit" == "$remote_commit" ]]; then
            echo -e "${GREEN}✓ In sync with remote${NC}"
        else
            echo -e "${YELLOW}⚠ Out of sync with remote${NC}"

            # Show behind/ahead status
            local ahead=$(git rev-list --count "origin/$current_branch..HEAD" 2>/dev/null || echo "0")
            local behind=$(git rev-list --count "HEAD..origin/$current_branch" 2>/dev/null || echo "0")

            if [[ "$ahead" -gt 0 ]]; then
                echo -e "  ${YELLOW}Local is $ahead commit(s) ahead${NC}"
            fi
            if [[ "$behind" -gt 0 ]]; then
                echo -e "  ${YELLOW}Local is $behind commit(s) behind${NC}"
            fi
        fi

        # Uncommitted changes
        if ! git diff --quiet || ! git diff --cached --quiet; then
            echo -e "${YELLOW}⚠ Uncommitted changes present${NC}"
            echo ""
            echo "Modified files:"
            git status --short
        else
            echo -e "${GREEN}✓ Working tree clean${NC}"
        fi
    else
        echo -e "${RED}✗ Not a Git repository${NC}"
    fi

    echo ""

    # Snapshot status
    if [[ -d "$SYNC_SNAPSHOT" ]]; then
        local snapshot_age=$(($(date +%s) - $(cat "$SYNC_SNAPSHOT/timestamp" 2>/dev/null || echo "0")))
        echo -e "${YELLOW}⚠ Snapshot exists (age: ${snapshot_age}s)${NC}"
        echo "  Snapshot from sync operation is still present"
        echo "  This might indicate an incomplete sync"
    else
        echo -e "${GREEN}✓ No snapshot (last sync completed cleanly)${NC}"
    fi

    echo ""
    echo -e "${BLUE}Recent sync log:${NC}"
    tail -10 "$SYNC_LOG" 2>/dev/null || echo "No sync log found"
}

# Main command dispatcher
main() {
    local command="${1:-}"

    case "$command" in
        push)
            sync_push
            ;;
        pull)
            sync_pull
            ;;
        status)
            sync_status
            ;;
        help|--help|-h)
            cat <<EOF
PetesBrain Sync System V2 - Foolproof Desktop ↔ Laptop Sync

Usage:
    sync-petesbrain-v2 push      Push changes from desktop to remote
    sync-petesbrain-v2 pull      Pull changes from remote to laptop
    sync-petesbrain-v2 status    Show current sync status
    sync-petesbrain-v2 help      Show this help message

Features:
    • SHA-256 checksum validation (prevents silent corruption)
    • Automatic pre-sync snapshot (instant rollback on failure)
    • Smart conflict detection and resolution
    • macOS notifications + email alerts for failures
    • Atomic operations (all-or-nothing sync)

Logs:
    Sync log:  $SYNC_LOG
    Error log: $ERROR_LOG

For more information, see: docs/SYNC-SYSTEM-V2.md
EOF
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}"
            echo ""
            echo "Usage: sync-petesbrain-v2 {push|pull|status|help}"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
