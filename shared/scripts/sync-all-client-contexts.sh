#!/bin/bash
#
# Sync All Client CONTEXT.md Files to Google Docs
# Runs daily at 7 AM via LaunchAgent
# Updates both Google Drive .md files and Google Docs
#

set -e

CLIENTS_DIR="/Users/administrator/Documents/PetesBrain/clients"
SYNC_DIR="$HOME/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My Drive/PetesBrain-Context"
REGISTRY="/Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json"
LOG_FILE="$HOME/.petesbrain-all-clients-sync.log"
DATE=$(date +"%Y-%m-%d")
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "============================================================"
log "All Clients CONTEXT.md Daily Sync"
log "============================================================"

# Create sync directory if it doesn't exist
mkdir -p "$SYNC_DIR"

# Check if registry exists
if [ ! -f "$REGISTRY" ]; then
    log "ERROR: Registry not found at $REGISTRY"
    exit 1
fi

# Counter for stats
TOTAL=0
SYNCED=0
SKIPPED=0
PENDING_DOCS=0

# Read all clients from registry
CLIENTS=$(python3 -c "import json; data=json.load(open('$REGISTRY')); print(' '.join(data.keys()))")

for client in $CLIENTS; do
    TOTAL=$((TOTAL + 1))
    CONTEXT_FILE="$CLIENTS_DIR/$client/CONTEXT.md"

    # Check if CONTEXT.md exists
    if [ ! -f "$CONTEXT_FILE" ]; then
        log "⚠️  $client: No CONTEXT.md found"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Get display name from registry
    DISPLAY_NAME=$(python3 -c "import json; data=json.load(open('$REGISTRY')); print(data['$client']['display_name'])")

    # Part 1: Copy to Google Drive Desktop (for .md file access)
    DEST_FILE="$SYNC_DIR/$DISPLAY_NAME-CONTEXT-$DATE.md"
    cp "$CONTEXT_FILE" "$DEST_FILE"

    # Create "latest" symlink
    ln -sf "$DEST_FILE" "$SYNC_DIR/$DISPLAY_NAME-CONTEXT-LATEST.md"

    FILE_SIZE=$(wc -c < "$CONTEXT_FILE")
    log "✓ $client: Synced ($FILE_SIZE bytes)"

    # Part 2: Prepare for Google Doc update
    TEMP_FILE="/tmp/${client}-context-for-gdoc.txt"
    cp "$CONTEXT_FILE" "$TEMP_FILE"

    # Create marker file for this client
    MARKER_FILE="$HOME/.petesbrain-${client}-needs-doc-update"
    echo "$DATE" > "$MARKER_FILE"

    SYNCED=$((SYNCED + 1))
    PENDING_DOCS=$((PENDING_DOCS + 1))
done

log ""
log "============================================================"
log "Summary:"
log "  Total clients: $TOTAL"
log "  Synced: $SYNCED"
log "  Skipped: $SKIPPED"
log "  Google Docs pending update: $PENDING_DOCS"
log ""
log ".md files synced to: $SYNC_DIR"
log "Google Doc updates require Claude Code (marker files created)"
log "============================================================"

exit 0
