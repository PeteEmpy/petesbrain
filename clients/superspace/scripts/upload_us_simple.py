#!/usr/bin/env python3
import os
import csv
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
DEST_SPREADSHEET_ID = '138tHMTm16uwBMfbJv9UNPYoVb3gX7geEuDgvVY8_pOo'

# Read US data
with open('us-data-new.csv', 'r') as f:
    reader = csv.reader(f)
    us_data = list(reader)

print(f"Loaded {len(us_data)} rows")

# Authenticate
creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Just try to write - don't clear first
print("Uploading US data...")
body = {'values': us_data}
result = service.spreadsheets().values().update(
    spreadsheetId=DEST_SPREADSHEET_ID,
    range='US!A1',
    valueInputOption='RAW',
    body=body
).execute()

print(f"✓ {result.get('updatedCells')} cells updated")
