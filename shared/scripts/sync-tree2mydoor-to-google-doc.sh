#!/bin/bash
#
# Tree2MyDoor CONTEXT.md → Google Doc Sync
# Updates both:
#   1. Google Drive .md file (via Google Drive Desktop)
#   2. Google Doc (via MCP - requires manual trigger for now)
# Runs daily at 7 AM via LaunchAgent
#

set -e

CONTEXT_FILE="/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md"
SYNC_DIR="$HOME/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My Drive/PetesBrain-Context"
LOG_FILE="$HOME/.petesbrain-tree2mydoor-context-upload.log"
DATE=$(date +"%Y-%m-%d")
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
GOOGLE_DOC_ID="1mXPdLygmIxngrWVOdsjZSBgnvw9AE9qtTaMyE4fn-Xk"

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

# Part 1: Copy to Google Drive Desktop (for .md file access)
DEST_FILE="$SYNC_DIR/Tree2MyDoor-CONTEXT-$DATE.md"
cp "$CONTEXT_FILE" "$DEST_FILE"

log "✓ Copied to: $DEST_FILE"
log "  File size: $(wc -c < "$DEST_FILE") bytes"

# Also create a "latest" symlink
ln -sf "$DEST_FILE" "$SYNC_DIR/Tree2MyDoor-CONTEXT-LATEST.md"

log "✓ Latest link updated"

# Part 2: Prepare for Google Doc update
# Write to a temp file that can be picked up by a separate process
TEMP_FILE="/tmp/tree2mydoor-context-for-gdoc.txt"
cp "$CONTEXT_FILE" "$TEMP_FILE"

log "✓ Temp file created for Google Doc update: $TEMP_FILE"

# Part 3: Attempt Google Doc update via MCP
# Note: MCP tools only work within Claude Code context
# For automated updates, we'll use a marker file approach

MARKER_FILE="$HOME/.petesbrain-tree2mydoor-needs-doc-update"
echo "$DATE" > "$MARKER_FILE"

log ""
log "NEXT STEPS:"
log "  1. ✓ .md file synced to Google Drive"
log "  2. ⏳ Google Doc update pending (requires Claude Code)"
log "     File: https://docs.google.com/document/d/$GOOGLE_DOC_ID/edit"
log "     Marker: $MARKER_FILE"
log ""
log "To update Google Doc manually, use Claude Code with:"
log "  mcp__google-drive__updateGoogleDoc"
log "  documentId: $GOOGLE_DOC_ID"
log "  content: $(cat $TEMP_FILE | wc -c) bytes from $TEMP_FILE"
log "============================================================"

exit 0
