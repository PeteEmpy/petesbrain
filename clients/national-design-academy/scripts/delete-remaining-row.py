#!/usr/bin/env python3
"""
Delete remaining LOW priority row (row 5)
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

def delete_row(service):
    """Delete row 5"""

    print("\nDeleting remaining LOW priority row (row 5)...")

    request = {
        "deleteDimension": {
            "range": {
                "sheetId": 0,
                "dimension": "ROWS",
                "startIndex": 4,  # Row 5 (0-indexed)
                "endIndex": 5
            }
        }
    }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [request]}
        ).execute()
        print(f"✅ Successfully deleted row 5")
        print(f"\nSheet now contains:")
        print(f"  Row 1: Headers")
        print(f"  Rows 2-4: HIGH priority assets ONLY")
        return True
    except Exception as e:
        print(f"❌ Error deleting row: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("DELETING REMAINING LOW PRIORITY ROW")
    print("="*70)

    service = get_service()
    delete_row(service)

    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)
