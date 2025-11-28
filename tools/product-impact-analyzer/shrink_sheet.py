#!/usr/bin/env python3
"""Shrink Daily Performance sheet to actual data size"""
import json, os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

config_path = Path(__file__).parent / "config.json"
with open(config_path) as f:
    config = json.load(f)

spreadsheet_id = config['spreadsheet_id']

creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(
    creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets']
)

service = build('sheets', 'v4', credentials=credentials)

# Get sheet ID
spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheet_id = None
for sheet in spreadsheet['sheets']:
    if sheet['properties']['title'] == 'Daily Performance':
        sheet_id = sheet['properties']['sheetId']
        break

# Get actual data size
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='Daily Performance!A:M'
).execute()

rows_with_data = len(result.get('values', []))
print(f"Rows with data: {rows_with_data}")

# Resize to data + buffer
new_row_count = rows_with_data + 50000  # 50k buffer for growth
new_col_count = 13  # Only 13 columns needed

print(f"Resizing to {new_row_count} rows × {new_col_count} cols")

service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        'requests': [{
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'rowCount': new_row_count,
                        'columnCount': new_col_count
                    }
                },
                'fields': 'gridProperties(rowCount,columnCount)'
            }
        }]
    }
).execute()

cells_before = 323807 * 26
cells_after = new_row_count * new_col_count
cells_freed = cells_before - cells_after

print(f"✅ Resized Daily Performance sheet")
print(f"Cells before: {cells_before:,}")
print(f"Cells after: {cells_after:,}")
print(f"Cells freed: {cells_freed:,} ({cells_freed/10_000_000*100:.1f}% of limit)")
