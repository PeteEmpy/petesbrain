#!/usr/bin/env python3
"""
Automated Tree2MyDoor CONTEXT.md → Google Doc Sync
Updates Google Doc daily at 7 AM via LaunchAgent
Uses subprocess to call Claude Code with MCP Google Drive tools
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

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
    """Main sync function"""

    log_message("=" * 60)
    log_message("Tree2MyDoor CONTEXT.md → Google Doc Sync")
    log_message("=" * 60)

    # Check if file exists
    if not CONTEXT_FILE.exists():
        log_message(f"ERROR: CONTEXT.md not found at {CONTEXT_FILE}")
        return False

    # Read content
    with open(CONTEXT_FILE, 'r') as f:
        content = f.read()

    log_message(f"Read {len(content)} characters from CONTEXT.md")

    # Prepare the content for the Google Doc
    # Note: We're using the raw content from CONTEXT.md
    # The Google Doc will display it with proper formatting

    log_message(f"Updating Google Doc: {GOOGLE_DOC_ID}")

    # Use npx with the Google Drive MCP server to update the doc
    # Set the required environment variable
    env = os.environ.copy()
    env['GOOGLE_DRIVE_OAUTH_CREDENTIALS'] = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json"

    # Write content to temp file (npx command will read it)
    temp_file = Path("/tmp/tree2mydoor-context-for-gdoc.md")
    with open(temp_file, 'w') as f:
        f.write(content)

    log_message(f"Temp file created: {temp_file}")

    # Build the npx command to use MCP tools
    # Note: This is a placeholder - MCP tools need to be called through Claude Code
    # For now, we'll use the Google Drive API directly via Python client

    try:
        # Import Google API client
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        # Load credentials from the OAuth file
        creds_file = Path("/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json")

        # This approach won't work directly - OAuth credentials need a token file
        # Let's use a simpler approach: call the MCP server via npx

        log_message("ERROR: Direct API access requires OAuth token flow")
        log_message("Falling back to manual update approach")
        log_message(f"Please update Google Doc manually or via Claude Code")
        log_message(f"Content available at: {temp_file}")

        return False

    except ImportError:
        log_message("ERROR: Google API client not installed")
        log_message("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return False
    except Exception as e:
        log_message(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
