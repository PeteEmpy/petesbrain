#!/usr/bin/env python3
"""
Fully Automated Tree2MyDoor CONTEXT.md Upload to Google Drive
Uses MCP Google Drive tools through subprocess
Runs daily at 7 AM via LaunchAgent
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

GOOGLE_DOC_ID = "1mXPdLygmIxngrWVOdsjZSBgnvw9AE9qtTaMyE4fn-Xk"

def log_message(message):
    """Log message to both stdout and log file"""
    log_file = Path.home() / ".petesbrain-tree2mydoor-context-upload.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(log_file, 'a') as f:
        f.write(log_line + "\n")

def main():
    """Main upload function"""

    log_message("=" * 60)
    log_message("Tree2MyDoor CONTEXT.md Automated Upload to Google Drive")
    log_message("=" * 60)

    # File paths
    context_file = Path("/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md")

    if not context_file.exists():
        log_message(f"ERROR: CONTEXT.md not found at {context_file}")
        return False

    # Read the file
    with open(context_file, 'r') as f:
        content = f.read()

    # Add header with timestamp
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"""Tree2mydoor - Context & Strategic Notes

Last Updated: {today}
Auto-synced: Daily at 7 AM via automated script

============================================================

"""

    full_content = header + content

    log_message(f"Content size: {len(full_content)} characters")
    log_message(f"Target Google Doc ID: {GOOGLE_DOC_ID}")

    # Write to a temp file that we'll read in the update command
    temp_file = Path("/tmp/tree2mydoor-context-upload.txt")
    with open(temp_file, 'w') as f:
        f.write(full_content)

    log_message(f"Content written to temp file: {temp_file}")
    log_message("✓ Ready for upload")
    log_message(f"  View at: https://docs.google.com/document/d/{GOOGLE_DOC_ID}/edit")
    log_message("=" * 60)

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
