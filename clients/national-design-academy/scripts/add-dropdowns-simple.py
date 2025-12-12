#!/usr/bin/env python3
"""
Add data validation dropdowns to NDA PMax Asset Performance Analysis sheet
Uses existing OAuth tokens from google-drive-mcp
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
ALTERNATIVES_FILE = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'

# Map cell rows to asset IDs
CELL_TO_ASSET = {
    'M2': '6501874539',  # Study Interior Design
    'M3': '6542848540',  # Interior Design Diploma
    'M4': '8680183789',  # Interior Design Courses
}

def get_service():
    """Load credentials from existing token file and build service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    # Create credentials from token data
    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    # Refresh if needed
    if creds.expired:
        creds.refresh(Request())

    return build('sheets', 'v4', credentials=creds)

def flatten_alternatives(asset_data):
    """Flatten nested alternatives structure into single list"""
    all_alts = []
    sections = ['Benefits', 'Technical', 'Quirky', 'CTA', 'Brand']
    for section in sections:
        if section in asset_data['section_breakdown']:
            all_alts.extend(asset_data['section_breakdown'][section])
    return all_alts

def add_dropdown_to_cell(service, cell_row):
    """Add dropdown validation to a specific cell"""

    # Get the alternative for this cell
    asset_id = CELL_TO_ASSET[cell_row]

    # Load alternatives data
    with open(ALTERNATIVES_FILE, 'r') as f:
        all_alternatives = json.load(f)

    alternatives = flatten_alternatives(all_alternatives[asset_id])

    # Convert cell reference (M2) to row/column indices
    col_letter = cell_row[0]  # M
    row_num = int(cell_row[1:])  # 2

    # Convert column letter to index (A=0, B=1, ..., M=12)
    col_index = ord(col_letter) - ord('A')
    row_index = row_num - 1  # 0-indexed

    print(f"\nAdding dropdown to {cell_row}...")
    print(f"  Asset: {all_alternatives[asset_id]['current']}")
    print(f"  Alternatives: {len(alternatives)}")

    # Build the data validation request
    request = {
        "setDataValidation": {
            "range": {
                "sheetId": 0,  # First sheet
                "startRowIndex": row_index,
                "endRowIndex": row_index + 1,
                "startColumnIndex": col_index,
                "endColumnIndex": col_index + 1
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": alt} for alt in alternatives]
                },
                "inputMessage": "Select an alternative headline",
                "strict": True,
                "showCustomUi": True
            }
        }
    }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [request]}
        ).execute()
        print(f"✅ Successfully added dropdown to {cell_row}")
        return True
    except Exception as e:
        print(f"❌ Error adding dropdown to {cell_row}: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("ADDING DATA VALIDATION DROPDOWNS TO NDA PMAX SHEET")
    print("="*70)

    service = get_service()

    success_count = 0
    for cell_row in ['M2', 'M3', 'M4']:
        if add_dropdown_to_cell(service, cell_row):
            success_count += 1

    print("\n" + "="*70)
    print(f"COMPLETE: {success_count}/3 dropdowns added successfully")
    print("="*70)
    print("\nYou can now click on cells M2, M3, or M4 to select alternatives")
    print("from the dropdown lists in the original Google Sheet.")
