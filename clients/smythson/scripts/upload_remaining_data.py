#!/usr/bin/env python3
"""Upload remaining data to Google Sheet"""

import json
import os
os.environ['GOOGLE_DRIVE_OAUTH_CREDENTIALS'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json'

import sys
sys.path.insert(0, '/Users/administrator/.config/google-drive-mcp')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load OAuth tokens
token_path = '/Users/administrator/.config/google-drive-mcp/tokens.json'
with open(token_path, 'r') as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data['access_token'],
    refresh_token=token_data.get('refresh_token'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=token_data['client_id'],
    client_secret=token_data['client_secret']
)

sheets_service = build('sheets', 'v4', credentials=creds)

# Load all data
with open('/tmp/smythson_sheet_data.json', 'r') as f:
    all_rows = json.load(f)

spreadsheet_id = '1FE5TM3oYZ9dM-EJcT-gTlTrmD4kIEfqCtdt9BonzKA0'

print(f"Uploading {len(all_rows)} total rows...")
print(f"First 10 rows already uploaded, adding remaining {len(all_rows) - 10} rows...")

# Upload remaining data in chunks starting from row 11
chunk_size = 500
start_row = 11  # Row 11 in the sheet (10 already uploaded)
data_index = 10  # Index in the array

while data_index < len(all_rows):
    chunk = all_rows[data_index:data_index + chunk_size]
    end_row = start_row + len(chunk) - 1
    range_name = f'A{start_row}:G{end_row}'

    try:
        sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': chunk}
        ).execute()

        print(f"✓ Uploaded rows {start_row}-{end_row} ({len(chunk)} rows)")

        start_row += len(chunk)
        data_index += len(chunk)
    except Exception as e:
        print(f"Error uploading chunk: {e}")
        break

print(f"\n✅ Upload complete!")
print(f"Total rows in sheet: {start_row - 1}")
print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
