#!/usr/bin/env python3
"""
Automated Tree2MyDoor CONTEXT.md Upload to Google Docs

Fully automated - uses service account for unattended operation.
Runs daily at 7 AM via LaunchAgent.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Google Doc ID where we'll upload the content
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

    log_message(f"Content size: {len(content)} characters ({len(content.encode('utf-8'))} bytes)")

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        # Load service account credentials
        SCOPES = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive.file'
        ]
        creds = service_account.Credentials.from_service_account_file(
            str(service_account_file),
            scopes=SCOPES
        )

        # Build Docs API service
        docs_service = build('docs', 'v1', credentials=creds)

        # Get current document content to clear it
        log_message(f"Updating Google Doc (ID: {GOOGLE_DOC_ID})")

        # First, get the document to know its length
        doc = docs_service.documents().get(documentId=GOOGLE_DOC_ID).execute()
        doc_content = doc.get('body').get('content')
        end_index = doc_content[-1].get('endIndex') if doc_content else 1

        # Delete all content except the first character (index 1 is required)
        if end_index > 1:
            requests = [{
                'deleteContentRange': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': end_index - 1
                    }
                }
            }]
            docs_service.documents().batchUpdate(
                documentId=GOOGLE_DOC_ID,
                body={'requests': requests}
            ).execute()

        # Insert new content
        # Add header with last updated date
        header = f"Tree2mydoor - Context & Strategic Notes\n\n"
        header += f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"Auto-synced daily at 7 AM\n\n"
        header += "=" * 60 + "\n\n"

        full_content = header + content

        requests = [{
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': full_content
            }
        }]

        docs_service.documents().batchUpdate(
            documentId=GOOGLE_DOC_ID,
            body={'requests': requests}
        ).execute()

        log_message(f"✓ Google Doc updated successfully")
        log_message(f"  View at: https://docs.google.com/document/d/{GOOGLE_DOC_ID}/edit")
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
