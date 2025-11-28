#!/usr/bin/env python3
"""
Automated Tree2MyDoor CONTEXT.md Upload to Google Drive

Uses service account for fully unattended operation.
Runs daily at 7 AM via LaunchAgent.
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
    log_message("Tree2MyDoor CONTEXT.md Automated Upload")
    log_message("=" * 60)

    # File paths
    context_file = Path("/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md")
    service_account_file = Path("/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json")

    if not context_file.exists():
        log_message(f"ERROR: CONTEXT.md not found at {context_file}")
        return False

    if not service_account_file.exists():
        log_message(f"ERROR: Service account credentials not found at {service_account_file}")
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
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload

        # Load service account credentials
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = service_account.Credentials.from_service_account_file(
            str(service_account_file),
            scopes=SCOPES
        )

        # Build Drive API service
        service = build('drive', 'v3', credentials=creds)

        # Known file ID (from initial upload)
        file_id = "1M0ZLvTsv8_WDIK8A16IPVYKSv3CEX4sL"

        # Prepare file metadata and content
        file_metadata = {
            'name': filename
        }

        media = MediaInMemoryUpload(
            content.encode('utf-8'),
            mimetype='text/markdown',
            resumable=True
        )

        # Update the file
        log_message(f"Updating file (ID: {file_id})")
        file = service.files().update(
            fileId=file_id,
            body=file_metadata,
            media_body=media,
            fields='id, name, modifiedTime, webViewLink'
        ).execute()

        log_message(f"✓ File updated successfully")
        log_message(f"  File ID: {file.get('id')}")
        log_message(f"  Name: {file.get('name')}")
        log_message(f"  Modified: {file.get('modifiedTime')}")
        if 'webViewLink' in file:
            log_message(f"  View link: {file.get('webViewLink')}")

        log_message("=" * 60)
        return True

    except ImportError as e:
        log_message(f"ERROR: Required Python packages not installed: {e}")
        log_message("Install with: pip install google-auth google-api-python-client")
        return False
    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        import traceback
        log_message(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
