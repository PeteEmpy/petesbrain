#!/usr/bin/env python3
"""
Add data validation dropdowns to NDA PMax HIGH priority assets
- M2:M13 (12 HIGH priority assets)
- Includes "Keep" as first option (default)
- Allows text editing (strict=False)

Updated: Dec 12, 2025 - Extended to 12 HIGH priority rows from 90-day analysis
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
ALTERNATIVES_FILE = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'

# Map HIGH priority cell rows to asset IDs (from 90-day analysis)
# Same asset text can appear in multiple campaigns - use same alternatives
HIGH_PRIORITY_CELLS = {
    'M2': '6501874539',   # Study Interior Design (Oman/Saudi Diploma)
    'M3': '6542848540',   # Interior Design Diploma (Oman/Saudi Diploma)
    'M4': '8680183789',   # Interior Design Courses (Oman/Saudi Diploma)
    'M5': '8680183789',   # Interior Design Courses (UAE Diploma)
    'M6': '6542848540',   # Interior Design Diploma (UAE Diploma)
    'M7': '8680134790',   # Online Interior Design Degrees (Oman/Saudi Degree)
    'M8': '6503351051',   # Interior Design Degree (Oman/Saudi Degree)
    'M9': '10422358209',  # Price-Match Guarantee (USA/Canada Diploma)
    'M10': '8680183789',  # Interior Design Courses (USA/Canada Diploma)
    'M11': '182887527317', # Intensive Fast-Track Diplomas (USA/Canada Diploma)
    'M12': '8680134790',  # Online Interior Design Degrees (USA/Canada Degree)
    'M13': '8680134790',  # Online Interior Design Degrees (UAE Degree)
}

def get_service():
    """Load credentials from existing token file and build service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get('access_token') or token_data.get('token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
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

def add_dropdown_to_high_priority(service, cell_row, asset_id, all_alternatives):
    """Add editable dropdown validation to HIGH priority cell with 'Keep' as default"""

    if asset_id not in all_alternatives:
        print(f"⚠️  No alternatives found for asset ID {asset_id}")
        return False

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
    print(f"  Total options: {len(dropdown_options)} (1 Keep + {len(alternatives)} alternatives)")

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
    print("UPDATING NDA PMAX DROPDOWNS - 12 HIGH PRIORITY ASSETS")
    print("="*70)

    service = get_service()

    # Load alternatives data once
    print("\nLoading alternatives data...")
    with open(ALTERNATIVES_FILE, 'r') as f:
        all_alternatives = json.load(f)
    print(f"✅ Loaded alternatives for {len(all_alternatives)} unique asset texts")

    # Update HIGH priority cells with "Keep" + alternatives
    success_count = 0
    for cell_row, asset_id in HIGH_PRIORITY_CELLS.items():
        if add_dropdown_to_high_priority(service, cell_row, asset_id, all_alternatives):
            success_count += 1

    print("\n" + "="*70)
    print(f"COMPLETE: {success_count}/{len(HIGH_PRIORITY_CELLS)} HIGH priority dropdowns updated")
    print("="*70)
    print("\nDropdown configuration:")
    print("  • 'Keep' is the first option (default - keeps current asset)")
    print("  • 15 alternatives follow (organised by Benefits, Technical, Quirky, CTA, Brand)")
    print("  • You can edit/type custom text if needed (strict validation disabled)")
    print(f"  • Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
