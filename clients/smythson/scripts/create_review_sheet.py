#!/usr/bin/env python3
"""Create Google Sheet from extracted data"""

import json
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/.venv/lib/python3.13/site-packages')

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Load data
with open('/tmp/smythson_sheet_data.json', 'r') as f:
    rows = json.load(f)

print(f"Loaded {len(rows)} rows")

# Load credentials
token_path = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/token.json'
creds = Credentials.from_authorized_user_file(token_path, [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
])

sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# Create new spreadsheet
spreadsheet = {
    'properties': {
        'title': 'Smythson PMAX Gifting Text Assets - Marketing Review'
    }
}

spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
spreadsheet_id = spreadsheet.get('spreadsheetId')

print(f"Created spreadsheet: {spreadsheet_id}")

# Write data in chunks (Google Sheets has limits)
chunk_size = 1000
for i in range(0, len(rows), chunk_size):
    chunk = rows[i:i+chunk_size]
    range_name = f'A{i+1}:G{i+len(chunk)}'

    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body={'values': chunk}
    ).execute()

    print(f"Wrote rows {i+1} to {i+len(chunk)}")

# Format header row
requests = [
    {
        'repeatCell': {
            'range': {
                'sheetId': 0,
                'startRowIndex': 0,
                'endRowIndex': 1
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
                    'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True}
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
        }
    },
    {
        'updateSheetProperties': {
            'properties': {
                'sheetId': 0,
                'gridProperties': {
                    'frozenRowCount': 1
                }
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    },
    {
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': 0,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': 5
            }
        }
    }
]

sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': requests}
).execute()

print(f"\n✓ Spreadsheet created successfully!")
print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
