#!/usr/bin/env python3
"""
Clear old data from Daily Performance sheet

Keeps last N days, deletes older rows (in-place, no archive creation)
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--keep-days', type=int, default=30)
    parser.add_argument('--yes', action='store_true')
    args = parser.parse_args()

    print(f"\nClearing data older than {args.keep_days} days from Daily Performance sheet...")
    
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    spreadsheet_id = config['spreadsheet_id']
    
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=credentials)

    # Get all data
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Daily Performance!A:M'
    ).execute()

    all_rows = result.get('values', [])
    if not all_rows:
        print("No data found")
        return

    header = all_rows[0]
    data_rows = all_rows[1:]

    # Calculate cutoff
    cutoff_date = datetime.now() - timedelta(days=args.keep_days)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d")

    # Split data
    keep_rows = []
    delete_count = 0
    
    for row in data_rows:
        if not row:
            continue
        row_date = row[0] if row else ""
        if row_date >= cutoff_str:
            keep_rows.append(row)
        else:
            delete_count += 1

    print(f"Cutoff date: {cutoff_str}")
    print(f"Rows to keep: {len(keep_rows)}")
    print(f"Rows to delete: {delete_count}")
    
    cells_before = len(all_rows) * 26  # 26 columns
    cells_after = (len(keep_rows) + 1) * 26  # +1 for header
    cells_freed = cells_before - cells_after
    
    print(f"\nCells before: {cells_before:,}")
    print(f"Cells after: {cells_after:,}")
    print(f"Cells freed: {cells_freed:,} ({cells_freed/10_000_000*100:.1f}% of limit)")

    if not args.yes:
        response = input("\nContinue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled")
            return

    # Clear sheet
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range='Daily Performance!A:M'
    ).execute()

    # Write header + kept data
    all_data = [header] + keep_rows
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Daily Performance!A1',
        valueInputOption='USER_ENTERED',
        body={'values': all_data}
    ).execute()

    print(f"\n✅ Cleared {delete_count} old rows, kept {len(keep_rows)} recent rows")
    print(f"Freed {cells_freed:,} cells")

if __name__ == "__main__":
    main()
