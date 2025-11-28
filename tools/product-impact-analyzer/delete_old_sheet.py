#!/usr/bin/env python3
"""Delete the old consolidated Daily Performance sheet"""

import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load config
config_path = Path(__file__).parent / 'config.json'
with open(config_path) as f:
    config = json.load(f)
    spreadsheet_id = config['spreadsheet_id']

# Initialize API
credentials = service_account.Credentials.from_service_account_file(
    '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)

# Get sheet ID for "Daily Performance"
sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

sheet_id = None
for sheet in sheet_metadata['sheets']:
    if sheet['properties']['title'] == 'Daily Performance':
        sheet_id = sheet['properties']['sheetId']
        break

if sheet_id is None:
    print("Sheet 'Daily Performance' not found (already deleted?)")
    exit(0)

print(f"Found 'Daily Performance' sheet (ID: {sheet_id})")
print("Deleting...")

# Delete the sheet
service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        'requests': [{
            'deleteSheet': {
                'sheetId': sheet_id
            }
        }]
    }
).execute()

print("✓ Deleted old 'Daily Performance' sheet")
print(f"\nSpreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
