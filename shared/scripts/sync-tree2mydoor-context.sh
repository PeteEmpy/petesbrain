#!/bin/bash
#
# Tree2MyDoor CONTEXT.md Daily Sync
# Copies CONTEXT.md to a location for easy Google Drive upload
# Runs at 7 AM daily via LaunchAgent
#

set -e

CONTEXT_FILE="/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md"
SYNC_DIR="$HOME/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My Drive/PetesBrain-Context"
LOG_FILE="$HOME/.petesbrain-tree2mydoor-context-upload.log"
DATE=$(date +"%Y-%m-%d")
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "============================================================"
log "Tree2MyDoor CONTEXT.md Daily Sync"
log "============================================================"

# Create sync directory if it doesn't exist
mkdir -p "$SYNC_DIR"

# Check if file exists
if [ ! -f "$CONTEXT_FILE" ]; then
    log "ERROR: CONTEXT.md not found at $CONTEXT_FILE"
    exit 1
fi

# Copy with datestamp
DEST_FILE="$SYNC_DIR/Tree2MyDoor-CONTEXT-$DATE.md"
cp "$CONTEXT_FILE" "$DEST_FILE"

log "✓ Copied to: $DEST_FILE"
log "  File size: $(wc -c < "$DEST_FILE") bytes"

# Also create a "latest" symlink
ln -sf "$DEST_FILE" "$SYNC_DIR/Tree2MyDoor-CONTEXT-LATEST.md"

log "✓ Latest link updated"
log ""
log "NEXT STEP: Upload this file to Google Drive:"
log "  File: $DEST_FILE"
log "  Or use: $SYNC_DIR/Tree2MyDoor-CONTEXT-LATEST.md"
log ""
log "Then share the Google Drive link for use in Claude.ai"
log "============================================================"

exit 0
