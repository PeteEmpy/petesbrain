#!/usr/bin/env python3
"""
Add data validation dropdowns to NDA PMax HIGH priority assets
- Column M: Short headlines (30 chars)
- Column N: Long headlines (90 chars)
- Column O: Descriptions (90 chars)

Updated: Dec 12, 2025 - Added long headlines and descriptions
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
ALTERNATIVES_FILE = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'

# Map rows to asset IDs (from 90-day analysis)
ROW_TO_ASSET = {
    2: '6501874539',   # Study Interior Design (Oman/Saudi Diploma)
    3: '6542848540',   # Interior Design Diploma (Oman/Saudi Diploma)
    4: '8680183789',   # Interior Design Courses (Oman/Saudi Diploma)
    5: '8680183789',   # Interior Design Courses (UAE Diploma)
    6: '6542848540',   # Interior Design Diploma (UAE Diploma)
    7: '8680134790',   # Online Interior Design Degrees (Oman/Saudi Degree)
    8: '6503351051',   # Interior Design Degree (Oman/Saudi Degree)
    9: '10422358209',  # Price-Match Guarantee (USA/Canada Diploma)
    10: '8680183789',  # Interior Design Courses (USA/Canada Diploma)
    11: '182887527317', # Intensive Fast-Track Diplomas (USA/Canada Diploma)
    12: '8680134790',  # Online Interior Design Degrees (USA/Canada Degree)
    13: '8680134790',  # Online Interior Design Degrees (UAE Degree)
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


def flatten_section(asset_data, section_key):
    """Flatten a section into a single list"""
    all_items = []
    sections = ['Benefits', 'Technical', 'Quirky', 'CTA', 'Brand']
    data = asset_data.get(section_key, {})
    for section in sections:
        if section in data:
            all_items.extend(data[section])
    return all_items


def add_dropdown(service, row_num, col_letter, options, input_message):
    """Add dropdown to a specific cell"""
    col_index = ord(col_letter) - ord('A')
    row_index = row_num - 1

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
                    "values": [{"userEnteredValue": opt} for opt in options]
                },
                "inputMessage": input_message,
                "showCustomUi": True,
                "strict": False
            }
        }
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"requests": [request]}
    ).execute()


def add_column_headers(service):
    """Add/update column headers for N and O"""
    # Update headers
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!N1:O1',
        valueInputOption='USER_ENTERED',
        body={'values': [['Long Headline (90 chars)', 'Description (90 chars)']]}
    ).execute()
    print("✅ Added column headers for N (Long Headlines) and O (Descriptions)")


def main():
    print("\n" + "="*70)
    print("UPDATING NDA PMAX DROPDOWNS - ALL ASSET TYPES")
    print("="*70)

    service = get_service()

    # Load alternatives data
    print("\nLoading alternatives data...")
    with open(ALTERNATIVES_FILE, 'r') as f:
        all_alternatives = json.load(f)
    print(f"✅ Loaded alternatives for {len(all_alternatives)} unique asset texts")

    # Add column headers
    add_column_headers(service)

    # Process each row
    success_count = 0
    for row_num, asset_id in ROW_TO_ASSET.items():
        if asset_id not in all_alternatives:
            print(f"⚠️  Row {row_num}: No alternatives found for asset ID {asset_id}")
            continue

        asset_data = all_alternatives[asset_id]
        asset_name = asset_data.get('current', asset_id)

        print(f"\nRow {row_num}: {asset_name}")

        try:
            # Column M: Short headlines (30 chars)
            short_headlines = flatten_section(asset_data, 'section_breakdown')
            if short_headlines:
                options_m = ["Keep"] + short_headlines
                add_dropdown(service, row_num, 'M', options_m, "Short headline (30 chars max)")
                print(f"  ✅ M{row_num}: {len(short_headlines)} short headlines")
            else:
                print(f"  ⚠️  M{row_num}: No short headlines")

            # Column N: Long headlines (90 chars)
            long_headlines = flatten_section(asset_data, 'long_headlines')
            if long_headlines:
                options_n = ["Keep"] + long_headlines
                add_dropdown(service, row_num, 'N', options_n, "Long headline (90 chars max)")
                print(f"  ✅ N{row_num}: {len(long_headlines)} long headlines")
            else:
                print(f"  ⚠️  N{row_num}: No long headlines")

            # Column O: Descriptions (90 chars)
            descriptions = flatten_section(asset_data, 'descriptions')
            if descriptions:
                options_o = ["Keep"] + descriptions
                add_dropdown(service, row_num, 'O', options_o, "Description (90 chars max)")
                print(f"  ✅ O{row_num}: {len(descriptions)} descriptions")
            else:
                print(f"  ⚠️  O{row_num}: No descriptions")

            success_count += 1

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

    print("\n" + "="*70)
    print(f"COMPLETE: {success_count}/{len(ROW_TO_ASSET)} rows updated")
    print("="*70)
    print("\nDropdown columns:")
    print("  • Column M: Short headlines (30 chars) - 'Keep' + alternatives")
    print("  • Column N: Long headlines (90 chars) - 'Keep' + alternatives")
    print("  • Column O: Descriptions (90 chars) - 'Keep' + alternatives")
    print(f"  • Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")


if __name__ == '__main__':
    main()
