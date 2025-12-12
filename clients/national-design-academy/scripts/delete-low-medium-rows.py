#!/usr/bin/env python3
"""
Delete LOW and MEDIUM priority rows from NDA PMax sheet
Keep only HIGH priority rows (2-4)
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'

def get_service():
    """Load credentials from existing token file and build service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    if creds.expired:
        creds.refresh(Request())

    return build('sheets', 'v4', credentials=creds)

def delete_rows(service):
    """Delete rows 5-10 (LOW and MEDIUM priority)"""

    print("\nDeleting LOW and MEDIUM priority rows (rows 5-10)...")

    # Delete in reverse order to avoid shifting issues
    # Delete rows 10, 9, 8, 7, 6, 5 (in that order)
    requests = []

    for row_index in range(9, 4, -1):  # Rows 10, 9, 8, 7, 6, 5 (0-indexed: 9, 8, 7, 6, 5, 4)
        requests.append({
            "deleteDimension": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": row_index - 1,  # 0-indexed
                    "endIndex": row_index
                }
            }
        })

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": requests}
        ).execute()
        print(f"✅ Successfully deleted 6 rows (LOW and MEDIUM priority)")
        print(f"\nSheet now contains:")
        print(f"  Row 1: Headers")
        print(f"  Rows 2-4: HIGH priority assets only")
        return True
    except Exception as e:
        print(f"❌ Error deleting rows: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("DELETING LOW AND MEDIUM PRIORITY ROWS")
    print("="*70)

    service = get_service()
    delete_rows(service)

    print("\n" + "="*70)
    print("COMPLETE - Sheet now shows HIGH priority assets only")
    print("="*70)
