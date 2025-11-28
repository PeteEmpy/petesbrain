#!/usr/bin/env python3
"""
Automatically Update Tree2MyDoor Google Doc
This script is called by automated workflows to update the Google Doc
when new content is available (indicated by marker file)

NOTE: This script requires Claude Code MCP context to run
It's meant to be triggered by you (the AI) when checking for pending updates
"""

import os
import sys
from datetime import datetime
from pathlib import Path

MARKER_FILE = Path.home() / ".petesbrain-tree2mydoor-needs-doc-update"
TEMP_FILE = Path("/tmp/tree2mydoor-context-for-gdoc.txt")
CONTEXT_FILE = Path("/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md")
GOOGLE_DOC_ID = "1mXPdLygmIxngrWVOdsjZSBgnvw9AE9qtTaMyE4fn-Xk"
LOG_FILE = Path.home() / ".petesbrain-tree2mydoor-google-doc.log"

def log_message(message):
    """Log message to both stdout and log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + "\n")

def main():
    """Main function - outputs JSON for Claude Code to parse"""

    # Check if update is needed
    if not MARKER_FILE.exists():
        print('{"status": "no_update_needed", "message": "No pending updates"}')
        return True

    # Get update date
    with open(MARKER_FILE, 'r') as f:
        date_requested = f.read().strip()

    # Check content file
    if TEMP_FILE.exists():
        content_source = TEMP_FILE
    elif CONTEXT_FILE.exists():
        content_source = CONTEXT_FILE
    else:
        print('{"status": "error", "message": "No content file found"}')
        return False

    # Read content
    with open(content_source, 'r') as f:
        content = f.read()

    # Output JSON for Claude Code to parse
    result = {
        "status": "update_ready",
        "date_requested": date_requested,
        "doc_id": GOOGLE_DOC_ID,
        "content_length": len(content),
        "content_file": str(content_source),
        "marker_file": str(MARKER_FILE),
        "message": "Update ready - call mcp__google-drive__updateGoogleDoc"
    }

    import json
    print(json.dumps(result, indent=2))

    log_message("=" * 60)
    log_message("Google Doc Update Ready")
    log_message(f"  Date requested: {date_requested}")
    log_message(f"  Content: {len(content)} characters")
    log_message(f"  Doc ID: {GOOGLE_DOC_ID}")
    log_message("=" * 60)

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
