#!/usr/bin/env python3
"""
Daily upload of Tree2MyDoor CONTEXT.md to Google Drive

Simple script that reads the CONTEXT.md file and uploads it to Google Drive
using the Google Drive API with OAuth credentials.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

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
    log_message("Tree2MyDoor CONTEXT.md Daily Upload")
    log_message("=" * 60)

    # File paths
    context_file = Path("/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md")

    if not context_file.exists():
        log_message(f"ERROR: CONTEXT.md not found at {context_file}")
        return False

    # Read the file
    with open(context_file, 'r') as f:
        content = f.read()

    # Generate filename
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"Tree2MyDoor CONTEXT {today}.md"

    log_message(f"File to upload: {filename}")
    log_message(f"Content size: {len(content)} characters ({len(content.encode('utf-8'))} bytes)")

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload
        import json

        # Load OAuth credentials
        creds_file = Path("/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json")
        token_file = Path("/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/token.json")

        if not creds_file.exists():
            log_message(f"ERROR: OAuth credentials not found at {creds_file}")
            return False

        # Load credentials
        if token_file.exists():
            with open(token_file, 'r') as f:
                token_data = json.load(f)
                creds = Credentials.from_authorized_user_info(token_data)
        else:
            log_message("ERROR: token.json not found. Run OAuth setup first.")
            return False

        # Refresh if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed token
            with open(token_file, 'w') as f:
                f.write(creds.to_json())

        # Build Drive API service
        service = build('drive', 'v3', credentials=creds)

        # Search for existing file with today's date
        query = f"name='{filename}' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        # Prepare file metadata and content
        file_metadata = {
            'name': filename,
            'mimeType': 'text/markdown'
        }

        media = MediaInMemoryUpload(
            content.encode('utf-8'),
            mimetype='text/markdown',
            resumable=True
        )

        if files:
            # Update existing file
            file_id = files[0]['id']
            log_message(f"Updating existing file (ID: {file_id})")
            file = service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            log_message(f"✓ File updated successfully")
        else:
            # Create new file
            log_message(f"Creating new file")
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            log_message(f"✓ File created successfully")

        log_message(f"  File ID: {file.get('id')}")
        if 'webViewLink' in file:
            log_message(f"  View link: {file.get('webViewLink')}")

        log_message("=" * 60)
        return True

    except ImportError as e:
        log_message(f"ERROR: Required Python packages not installed: {e}")
        log_message("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return False
    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        import traceback
        log_message(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
