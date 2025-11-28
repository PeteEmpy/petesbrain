#!/usr/bin/env python3
"""
Load organized search terms data to destination spreadsheet.
"""

import os
import csv
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
DEST_SPREADSHEET_ID = '138tHMTm16uwBMfbJv9UNPYoVb3gX7geEuDgvVY8_pOo'

def load_csv_to_sheet(service, spreadsheet_id, sheet_name, csv_file):
    """Load CSV data to a specific sheet."""
    # Read CSV
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    print(f"Loading {len(data)} rows to {sheet_name}...")

    # Clear existing data first
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:Z"
    ).execute()

    # Upload new data
    body = {
        'values': data
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"  ✓ {result.get('updatedCells')} cells updated in {sheet_name}")
    return result

def main():
    # Authenticate
    creds = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    # Load each file to its corresponding sheet
    print("Loading data to destination spreadsheet...")
    print(f"Spreadsheet ID: {DEST_SPREADSHEET_ID}")
    print()

    load_csv_to_sheet(service, DEST_SPREADSHEET_ID, 'US', 'us-data-new.csv')
    load_csv_to_sheet(service, DEST_SPREADSHEET_ID, 'UK', 'uk-data-new.csv')
    load_csv_to_sheet(service, DEST_SPREADSHEET_ID, 'AUS', 'aus-data-new.csv')

    print()
    print("✓ All data loaded successfully!")
    print()
    print("View the spreadsheet at:")
    print(f"https://docs.google.com/spreadsheets/d/{DEST_SPREADSHEET_ID}/")

if __name__ == "__main__":
    main()
