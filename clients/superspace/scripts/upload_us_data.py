#!/usr/bin/env python3
"""
Upload US data to destination spreadsheet using OAuth credentials.
This script uses the Google Drive MCP server's token to authenticate.
"""

import json
import csv
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Google Drive MCP server OAuth token location
TOKEN_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/token.json'
SPREADSHEET_ID = '138tHMTm16uwBMfbJv9UNPYoVb3gX7geEuDgvVY8_pOo'

def load_us_data():
    """Load US data from CSV."""
    with open('us-data-new.csv', 'r') as f:
        reader = csv.reader(f)
        return list(reader)

def upload_to_sheet(data):
    """Upload data to Google Sheets using OAuth."""
    # Load OAuth token
    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    # Build service
    service = build('sheets', 'v4', credentials=creds)

    # Clear existing data
    print("Clearing existing US data...")
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range='US!A:Z'
    ).execute()

    # Upload new data
    print(f"Uploading {len(data)} rows...")
    body = {'values': data}

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='US!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"✓ {result.get('updatedCells')} cells updated")
    return result

def main():
    print("Loading US data...")
    us_data = load_us_data()
    print(f"Loaded {len(us_data)} rows")

    print("\nUploading to spreadsheet...")
    upload_to_sheet(us_data)

    print("\n✓ US data uploaded successfully!")
    print(f"\nView at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/")

if __name__ == "__main__":
    main()
