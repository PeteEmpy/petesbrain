#!/usr/bin/env python3
"""
Apply Pending Google Doc Updates
Checks for marker files indicating pending doc updates and applies them
Can be run manually or via automation
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Marker file created by sync script
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
    """Check for pending updates and provide instructions"""

    log_message("=" * 60)
    log_message("Checking for Pending Google Doc Updates")
    log_message("=" * 60)

    # Check if marker file exists
    if not MARKER_FILE.exists():
        log_message("No pending updates")
        return True

    # Read marker file to see when update was requested
    with open(MARKER_FILE, 'r') as f:
        date_requested = f.read().strip()

    log_message(f"Update requested: {date_requested}")

    # Check if temp file exists
    if not TEMP_FILE.exists():
        log_message(f"ERROR: Temp file not found: {TEMP_FILE}")
        log_message("Re-running sync script to regenerate")
        return False

    # Read content
    with open(TEMP_FILE, 'r') as f:
        content = f.read()

    log_message(f"Content ready: {len(content)} characters")
    log_message(f"Target Google Doc: {GOOGLE_DOC_ID}")
    log_message("")
    log_message("=" * 60)
    log_message("TO APPLY THIS UPDATE:")
    log_message("=" * 60)
    log_message("")
    log_message("Run this command in Claude Code:")
    log_message("")
    log_message("  Update Tree2MyDoor Google Doc with latest CONTEXT.md")
    log_message("")
    log_message("Or use MCP tool directly:")
    log_message(f"  mcp__google-drive__updateGoogleDoc(")
    log_message(f"    documentId=\"{GOOGLE_DOC_ID}\",")
    log_message(f"    content=<content from {TEMP_FILE}>")
    log_message(f"  )")
    log_message("")
    log_message(f"View Doc: https://docs.google.com/document/d/{GOOGLE_DOC_ID}/edit")
    log_message("=" * 60)

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
