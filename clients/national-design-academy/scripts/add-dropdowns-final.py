#!/usr/bin/env python3
"""
Add data validation dropdowns to NDA PMax HIGH priority assets only
- M2, M3, M4 (HIGH priority only)
- Includes "Keep" as first option (default)
- Allows text editing (strict=False)
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
ALTERNATIVES_FILE = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'

# Map HIGH priority cell rows to asset IDs
HIGH_PRIORITY_CELLS = {
    'M2': '6501874539',  # Study Interior Design
    'M3': '6542848540',  # Interior Design Diploma
    'M4': '8680183789',  # Interior Design Courses
}

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

def flatten_alternatives(asset_data):
    """Flatten nested alternatives structure into single list"""
    all_alts = []
    sections = ['Benefits', 'Technical', 'Quirky', 'CTA', 'Brand']
    for section in sections:
        if section in asset_data['section_breakdown']:
            all_alts.extend(asset_data['section_breakdown'][section])
    return all_alts

def clear_non_high_priority_dropdowns(service):
    """Remove data validation from LOW/MEDIUM priority cells"""
    print("\nClearing dropdowns from non-HIGH priority rows...")

    requests = []

    # Cells to clear: M5:M10 (LOW and MEDIUM priority)
    requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 4,      # Row 5 (0-indexed)
                "endRowIndex": 10,       # Row 10
                "startColumnIndex": 12,  # Column M
                "endColumnIndex": 13
            },
            "rule": None  # None removes validation
        }
    })

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": requests}
        ).execute()
        print("✅ Cleared dropdowns from non-HIGH priority rows (M5:M10)")
        return True
    except Exception as e:
        print(f"⚠️  Could not clear non-HIGH rows: {str(e)}")
        return False

def add_dropdown_to_high_priority(service, cell_row, asset_id):
    """Add editable dropdown validation to HIGH priority cell with 'Keep' as default"""

    # Load alternatives data
    with open(ALTERNATIVES_FILE, 'r') as f:
        all_alternatives = json.load(f)

    alternatives = flatten_alternatives(all_alternatives[asset_id])

    # Build list with "Keep" as first option
    dropdown_options = ["Keep"] + alternatives

    # Convert cell reference (M2) to row/column indices
    col_letter = cell_row[0]  # M
    row_num = int(cell_row[1:])  # 2

    col_index = ord(col_letter) - ord('A')
    row_index = row_num - 1

    print(f"\nUpdating dropdown for {cell_row}...")
    print(f"  Asset: {all_alternatives[asset_id]['current']}")
    print(f"  Total options: {len(dropdown_options)} (1 Keep + 15 alternatives)")

    # Build the data validation request with strict=False for editability
    request = {
        "setDataValidation": {
            "range": {
                "sheetId": 0,
                "startRowIndex": row_index,
                "endRowIndex": row_index + 1,
                "startColumnIndex": col_index,
                "endColumnIndex": col_index + 1
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": opt} for opt in dropdown_options]
                },
                "inputMessage": "Select 'Keep' to keep current asset, or choose an alternative",
                "showCustomUi": True,
                "strict": False  # Allow custom text entry
            }
        }
    }

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [request]}
        ).execute()
        print(f"✅ Updated dropdown for {cell_row}")
        return True
    except Exception as e:
        print(f"❌ Error updating {cell_row}: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("UPDATING NDA PMAX DROPDOWNS - HIGH PRIORITY ONLY")
    print("="*70)

    service = get_service()

    # Clear non-HIGH priority cells first
    clear_non_high_priority_dropdowns(service)

    # Update HIGH priority cells with "Keep" + alternatives
    success_count = 0
    for cell_row, asset_id in HIGH_PRIORITY_CELLS.items():
        if add_dropdown_to_high_priority(service, cell_row, asset_id):
            success_count += 1

    print("\n" + "="*70)
    print(f"COMPLETE: {success_count}/3 HIGH priority dropdowns updated")
    print("="*70)
    print("\nDropdown configuration:")
    print("  • 'Keep' is the first option (default - keeps current asset)")
    print("  • 15 alternatives follow")
    print("  • You can edit/type custom text if needed (strict validation disabled)")
    print("  • Non-HIGH priority rows have been cleared")
