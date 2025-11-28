#!/usr/bin/env python3
import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load config
config_path = Path("config.json")
with open(config_path) as f:
    config = json.load(f)

spreadsheet_id = config['spreadsheet_id']

# Get credentials
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(
    creds_path,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

service = build('sheets', 'v4', credentials=credentials)

# Clear Daily Performance (keep headers)
print("Clearing Daily Performance sheet...")
service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range='Daily Performance!A2:M'
).execute()

print("✅ Cleared all data rows (headers preserved)")
