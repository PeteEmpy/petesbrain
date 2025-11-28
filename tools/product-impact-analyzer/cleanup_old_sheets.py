#!/usr/bin/env python3
"""
Cleanup Old Format Sheets

Deletes the old per-client sheets (Current/Previous/Changes) to free up space
for the new consolidated Daily Performance historical data.
"""

import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build


def main():
    print("\n" + "="*80)
    print("CLEANUP OLD FORMAT SHEETS")
    print("="*80)
    print()
    print("This script will DELETE the old per-client sheets to free up space")
    print("for the new consolidated historical data format.")
    print()
    print("Sheets to delete:")
    print("  - All '*- Current' sheets (10 sheets)")
    print("  - All '*- Previous' sheets (11 sheets)")
    print("  - All '*- Changes' sheets (10 sheets)")
    print()
    print("Total: 31 old format sheets will be deleted")
    print()
    print("Sheets to KEEP:")
    print("  - Dashboard")
    print("  - Outliers Report")
    print("  - Daily Performance (new)")
    print("  - Impact Analysis (new)")
    print("  - Product Summary (new)")
    print()
    print("⚠️  WARNING: This action cannot be undone!")
    print()

    response = input("Continue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Cancelled.")
        return 1

    # Load config
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    spreadsheet_id = config['spreadsheet_id']

    # Get credentials
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        print("\n❌ ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        return 1

    print(f"\nUsing credentials: {creds_path}")
    print(f"Spreadsheet ID: {spreadsheet_id}")

    # Authenticate
    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=credentials)

    # Get all sheets
    print("\nFetching sheet list...")
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])

    # Identify sheets to delete (old format)
    sheets_to_delete = []
    sheets_to_keep = ['Dashboard', 'Outliers Report', 'Daily Performance', 'Impact Analysis', 'Product Summary']

    for sheet in sheets:
        sheet_title = sheet['properties']['title']
        sheet_id = sheet['properties']['sheetId']

        # Delete if it matches old format pattern
        if sheet_title not in sheets_to_keep:
            if any(suffix in sheet_title for suffix in [' - Current', ' - Previous', ' - Changes', '- Current', '- Previous']):
                sheets_to_delete.append({
                    'title': sheet_title,
                    'id': sheet_id
                })

    print(f"\nFound {len(sheets_to_delete)} old format sheets to delete:")
    for sheet in sheets_to_delete:
        print(f"  - {sheet['title']}")

    if not sheets_to_delete:
        print("\nNo old sheets found. Nothing to delete.")
        return 0

    print(f"\nDeleting {len(sheets_to_delete)} sheets...")

    # Build batch delete request
    requests = []
    for sheet in sheets_to_delete:
        requests.append({
            'deleteSheet': {
                'sheetId': sheet['id']
            }
        })

    body = {'requests': requests}

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()

        print(f"\n✅ Successfully deleted {len(sheets_to_delete)} old format sheets!")
        print(f"\nFreed up approximately {len(sheets_to_delete) * 300000} cells (~{len(sheets_to_delete) * 300000 / 1000000:.1f}M cells)")
        print("\nRemaining sheets:")
        for keeper in sheets_to_keep:
            print(f"  ✓ {keeper}")

        print(f"\nView spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
        print("\nYou can now re-run the backfill script to populate historical data:")
        print("  GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\")
        print("    .venv/bin/python3 backfill_historical_data.py --yes --days 90")

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
