#!/usr/bin/env python3
"""
Create new sheets in Google Sheets spreadsheet

Uses Google Sheets API directly to add new sheet tabs.
"""

import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    print("\n" + "="*80)
    print("CREATING NEW SHEETS IN GOOGLE SPREADSHEET")
    print("="*80)

    # Load config
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    spreadsheet_id = config['spreadsheet_id']

    # Get credentials
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        print("\n❌ ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        print("Set it to the path of your service account JSON file")
        return 1

    print(f"\nUsing credentials: {creds_path}")
    print(f"Spreadsheet ID: {spreadsheet_id}")

    # Authenticate
    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=credentials)

    # Define new sheets to create
    new_sheets = [
        "Daily Performance",
        "Impact Analysis",
        "Product Summary"
    ]

    print("\nCreating sheets...")

    # Create batch update request
    requests = []
    for sheet_name in new_sheets:
        requests.append({
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        })

    body = {
        'requests': requests
    }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()

        print(f"\n✅ Successfully created {len(new_sheets)} sheets:")
        for sheet_name in new_sheets:
            print(f"   - {sheet_name}")

        print("\n" + "="*80)
        print("SHEETS CREATED SUCCESSFULLY")
        print("="*80)

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        if "already exists" in str(e).lower():
            print("\nSheets may already exist. This is okay - continuing with setup...")
            return 0
        return 1

if __name__ == "__main__":
    exit(main())
