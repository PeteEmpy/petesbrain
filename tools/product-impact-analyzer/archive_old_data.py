#!/usr/bin/env python3
"""
Archive Old Data from Daily Performance Sheet

Moves data older than a specified threshold to a separate archive spreadsheet
to prevent hitting the 10M cell limit.

This should be run every 2-3 months to maintain capacity.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build


class DataArchiver:
    """Archives old Daily Performance data to separate spreadsheet"""

    def __init__(self, config_path: str, keep_days: int = 90):
        """
        Initialize archiver

        Args:
            config_path: Path to config.json
            keep_days: Keep last N days in main sheet (archive older)
        """
        self.config_path = Path(config_path)
        self.keep_days = keep_days

        # Load config
        with open(self.config_path) as f:
            self.config = json.load(f)

        self.spreadsheet_id = self.config['spreadsheet_id']

        # Initialize Google Sheets client
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")

        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )
        self.sheets_service = build('sheets', 'v4', credentials=credentials)
        self.drive_service = build('drive', 'v3', credentials=credentials)

        self.log("Initialized DataArchiver")
        self.log(f"Will archive data older than {keep_days} days")

    def log(self, message: str):
        """Print timestamped log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}", flush=True)

    def get_all_data(self) -> List[List[str]]:
        """Fetch all data from Daily Performance sheet"""
        self.log("Fetching all data from Daily Performance sheet...")

        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Daily Performance!A:M'
        ).execute()

        values = result.get('values', [])
        self.log(f"  Fetched {len(values)} rows")

        return values

    def split_data(self, all_data: List[List[str]]) -> Dict:
        """
        Split data into keep vs archive based on date threshold

        Args:
            all_data: All rows including header

        Returns:
            Dict with 'header', 'keep', 'archive' keys
        """
        if not all_data:
            return {'header': [], 'keep': [], 'archive': []}

        header = all_data[0]
        data_rows = all_data[1:]

        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=self.keep_days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")

        self.log(f"  Cutoff date: {cutoff_str}")
        self.log(f"  Rows dated {cutoff_str} and later will be KEPT")
        self.log(f"  Rows dated before {cutoff_str} will be ARCHIVED")

        keep_rows = []
        archive_rows = []

        for row in data_rows:
            if not row:  # Skip empty rows
                continue

            row_date = row[0] if row else ""

            if row_date >= cutoff_str:
                keep_rows.append(row)
            else:
                archive_rows.append(row)

        self.log(f"  Split complete:")
        self.log(f"    - Keep: {len(keep_rows)} rows")
        self.log(f"    - Archive: {len(archive_rows)} rows")

        return {
            'header': header,
            'keep': keep_rows,
            'archive': archive_rows
        }

    def create_archive_spreadsheet(self, year: int) -> str:
        """
        Create archive spreadsheet for specified year

        Args:
            year: Year for archive (e.g., 2025)

        Returns:
            Spreadsheet ID of created archive
        """
        archive_name = f"Product Impact Analyzer - Archive {year}"

        self.log(f"Creating archive spreadsheet: {archive_name}")

        # Create new spreadsheet
        spreadsheet = {
            'properties': {'title': archive_name},
            'sheets': [
                {
                    'properties': {
                        'title': f'Daily Performance - {year}',
                        'gridProperties': {'frozenRowCount': 1}
                    }
                }
            ]
        }

        result = self.sheets_service.spreadsheets().create(body=spreadsheet).execute()
        archive_id = result['spreadsheetId']

        self.log(f"  Created: https://docs.google.com/spreadsheets/d/{archive_id}/edit")

        return archive_id

    def write_to_archive(self, archive_id: str, header: List[str], data: List[List[str]]):
        """Write archived data to archive spreadsheet"""
        self.log(f"Writing {len(data)} rows to archive...")

        # Determine sheet name (first sheet in archive)
        spreadsheet = self.sheets_service.spreadsheets().get(spreadsheetId=archive_id).execute()
        sheet_name = spreadsheet['sheets'][0]['properties']['title']

        # Write header
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=archive_id,
            range=f'{sheet_name}!A1',
            valueInputOption='USER_ENTERED',
            body={'values': [header]}
        ).execute()

        # Write data in batches
        batch_size = 10000
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(data) + batch_size - 1) // batch_size

            self.log(f"  Batch {batch_num}/{total_batches} ({len(batch)} rows)")

            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=archive_id,
                range=f'{sheet_name}!A2',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': batch}
            ).execute()

        self.log(f"  Successfully wrote {len(data)} rows to archive")

    def clear_and_rewrite_main(self, header: List[str], data: List[List[str]]):
        """Clear Daily Performance sheet and rewrite with kept data"""
        self.log(f"Rewriting main sheet with {len(data)} rows...")

        # Clear sheet
        self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range='Daily Performance!A:M'
        ).execute()

        self.log("  Cleared Daily Performance sheet")

        # Write header + kept data
        all_data = [header] + data

        batch_size = 10000
        for i in range(0, len(all_data), batch_size):
            batch = all_data[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(all_data) + batch_size - 1) // batch_size

            self.log(f"  Batch {batch_num}/{total_batches} ({len(batch)} rows)")

            if i == 0:
                # First batch: update (includes header)
                self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range='Daily Performance!A1',
                    valueInputOption='USER_ENTERED',
                    body={'values': batch}
                ).execute()
            else:
                # Subsequent batches: append
                self.sheets_service.spreadsheets().values().append(
                    spreadsheetId=self.spreadsheet_id,
                    range='Daily Performance!A2',
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body={'values': batch}
                ).execute()

        self.log(f"  Successfully rewrote {len(data)} rows to main sheet")

    def run(self):
        """Run the archival process"""
        self.log("\n" + "="*80)
        self.log("DATA ARCHIVAL PROCESS - START")
        self.log("="*80)

        # Step 1: Fetch all data
        all_data = self.get_all_data()

        if len(all_data) <= 1:
            self.log("\nNo data to archive (sheet is empty or has only header)")
            return True

        # Step 2: Split data
        split = self.split_data(all_data)

        if not split['archive']:
            self.log(f"\nNo data older than {self.keep_days} days. Nothing to archive.")
            return True

        # Step 3: Determine archive year (from oldest archived row)
        oldest_date = split['archive'][0][0] if split['archive'] else ""
        archive_year = int(oldest_date[:4]) if oldest_date else datetime.now().year

        self.log(f"\nArchiving data from year: {archive_year}")

        # Step 4: Create or find archive spreadsheet
        archive_id = self.create_archive_spreadsheet(archive_year)

        # Step 5: Write to archive
        self.write_to_archive(archive_id, split['header'], split['archive'])

        # Step 6: Rewrite main sheet with kept data
        self.clear_and_rewrite_main(split['header'], split['keep'])

        # Summary
        cells_archived = len(split['archive']) * len(split['header'])
        cells_kept = len(split['keep']) * len(split['header'])

        self.log("\n" + "="*80)
        self.log("DATA ARCHIVAL PROCESS - COMPLETE")
        self.log("="*80)
        self.log(f"Archived: {len(split['archive'])} rows ({cells_archived:,} cells)")
        self.log(f"Kept: {len(split['keep'])} rows ({cells_kept:,} cells)")
        self.log(f"\nArchive: https://docs.google.com/spreadsheets/d/{archive_id}/edit")
        self.log(f"Main: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit")

        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Archive old data from Daily Performance sheet"
    )
    parser.add_argument(
        '--keep-days',
        type=int,
        default=90,
        help='Keep last N days in main sheet (default: 90)'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Skip confirmation prompt'
    )

    args = parser.parse_args()

    print("\n" + "="*80, flush=True)
    print("DATA ARCHIVAL TOOL", flush=True)
    print("="*80, flush=True)
    print(flush=True)
    print(f"This script will move data older than {args.keep_days} days from the", flush=True)
    print("Daily Performance sheet to a separate archive spreadsheet.", flush=True)
    print(flush=True)
    print("This frees up space to prevent hitting the 10M cell limit.", flush=True)
    print(flush=True)
    print("⚠️  IMPORTANT:", flush=True)
    print("  - Data is NOT deleted, just moved to archive", flush=True)
    print("  - Archive spreadsheet will be created automatically", flush=True)
    print("  - You can still access archived data anytime", flush=True)
    print(flush=True)

    if not args.yes:
        response = input("Continue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.")
            return 1

    config_path = Path(__file__).parent / "config.json"

    try:
        archiver = DataArchiver(config_path, keep_days=args.keep_days)
        success = archiver.run()
        return 0 if success else 1

    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
