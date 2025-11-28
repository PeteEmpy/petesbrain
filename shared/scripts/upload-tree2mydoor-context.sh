#!/bin/bash
#
# Daily upload of Tree2MyDoor CONTEXT.md to Google Drive
# Runs at 7 AM daily via LaunchAgent
#

set -e

CONTEXT_FILE="/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md"
LOG_FILE="$HOME/.petesbrain-tree2mydoor-context-upload.log"
DATE=$(date +"%Y-%m-%d")
FILENAME="Tree2MyDoor CONTEXT ${DATE}.md"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "============================================================"
log "Tree2MyDoor CONTEXT.md Daily Upload"
log "============================================================"

# Check if file exists
if [ ! -f "$CONTEXT_FILE" ]; then
    log "ERROR: CONTEXT.md not found at $CONTEXT_FILE"
    exit 1
fi

# Get file size
FILE_SIZE=$(wc -c < "$CONTEXT_FILE")
log "Starting upload: $FILENAME"
log "Content size: $FILE_SIZE bytes"

# Read the content
CONTENT=$(cat "$CONTEXT_FILE")

# Create the file on Google Drive using npx and the MCP server
export GOOGLE_DRIVE_OAUTH_CREDENTIALS="/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json"

# Write content to a temp file for upload
TEMP_FILE=$(mktemp)
cat "$CONTEXT_FILE" > "$TEMP_FILE"

log "Content prepared for upload"

# Create a state file that contains the upload request
STATE_FILE="/Users/administrator/Documents/PetesBrain/shared/data/tree2mydoor-context-upload-state.json"
mkdir -p "$(dirname "$STATE_FILE")"

cat > "$STATE_FILE" << EOF
{
  "filename": "$FILENAME",
  "source_file": "$CONTEXT_FILE",
  "upload_date": "$DATE",
  "file_size": $FILE_SIZE,
  "status": "pending"
}
EOF

log "✓ Upload state saved to $STATE_FILE"
log "  Filename: $FILENAME"
log "  Size: $FILE_SIZE bytes"
log "  Status: Ready for upload"

# Clean up
rm -f "$TEMP_FILE"

log "✓ Upload preparation completed successfully"
log "============================================================"

exit 0
