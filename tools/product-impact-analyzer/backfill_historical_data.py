#!/usr/bin/env python3
"""
Backfill Historical Data to Google Sheets

Fetches 60-90 days of historical shopping performance data for all enabled clients
and writes it to the Daily Performance sheet in Google Sheets.

This is a one-time operation to populate historical baseline data.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import time

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.oauth2 import service_account
from googleapiclient.discovery import build


class HistoricalDataBackfiller:
    """Backfills historical shopping performance data to Google Sheets"""

    def __init__(self, config_path: str, days_back: int = 90):
        """
        Initialize backfiller

        Args:
            config_path: Path to config.json
            days_back: Number of days to fetch (default 90)
        """
        self.config_path = Path(config_path)
        self.days_back = days_back

        # Load config
        with open(self.config_path) as f:
            self.config = json.load(f)

        self.spreadsheet_id = self.config['spreadsheet_id']

        # Initialize Google Ads client
        self.ads_client = GoogleAdsClient.load_from_storage()

        # Initialize Google Sheets client
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")

        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.sheets_service = build('sheets', 'v4', credentials=credentials)

        # Progress tracking
        self.progress_file = Path(__file__).parent / "data" / "backfill_progress.json"
        self.progress_file.parent.mkdir(exist_ok=True)

        self.log("Initialized HistoricalDataBackfiller")
        self.log(f"Will fetch {days_back} days of data")
        self.log(f"Spreadsheet ID: {self.spreadsheet_id}")

    def log(self, message: str):
        """Print timestamped log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}", flush=True)

    def load_progress(self) -> Dict:
        """Load progress from file"""
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                return json.load(f)
        return {"completed_clients": [], "last_date_processed": None}

    def save_progress(self, progress: Dict):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)

    def fetch_client_data(self, customer_id: str, days_back: int) -> Dict[str, List[Dict]]:
        """
        Fetch historical data for a client, grouped by date

        Args:
            customer_id: Google Ads customer ID
            days_back: Number of days to fetch

        Returns:
            Dict mapping date string (YYYY-MM-DD) to list of product dicts
        """
        ga_service = self.ads_client.get_service("GoogleAdsService")

        # Calculate date range
        end_date = datetime.now() - timedelta(days=1)  # Yesterday
        start_date = end_date - timedelta(days=days_back)

        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        self.log(f"  Fetching data from {start_str} to {end_str}")

        query = f"""
        SELECT
            segments.product_item_id,
            segments.product_title,
            segments.date,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM shopping_performance_view
        WHERE segments.date >= '{start_str}'
          AND segments.date <= '{end_str}'
        ORDER BY segments.date, segments.product_item_id
        """

        # Fetch data
        data_by_date = {}

        try:
            stream = ga_service.search_stream(customer_id=customer_id, query=query)

            for batch in stream:
                for row in batch.results:
                    date_str = row.segments.date
                    product_id = row.segments.product_item_id
                    product_title = row.segments.product_title

                    impressions = row.metrics.impressions
                    clicks = row.metrics.clicks
                    conversions = row.metrics.conversions
                    revenue = row.metrics.conversions_value
                    cost = row.metrics.cost_micros / 1_000_000

                    # Calculate derived metrics
                    ctr = (clicks / impressions * 100) if impressions > 0 else 0
                    conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
                    roas = (revenue / cost) if cost > 0 else 0

                    product = {
                        'product_id': product_id,
                        'product_title': product_title,
                        'impressions': impressions,
                        'clicks': clicks,
                        'conversions': conversions,
                        'revenue': revenue,
                        'cost': cost,
                        'ctr': ctr,
                        'conv_rate': conv_rate,
                        'roas': roas,
                        'label': ''  # Labels not available in historical data
                    }

                    if date_str not in data_by_date:
                        data_by_date[date_str] = []

                    data_by_date[date_str].append(product)

            self.log(f"  Fetched {len(data_by_date)} days of data")
            return data_by_date

        except GoogleAdsException as ex:
            self.log(f"  ERROR: Google Ads API error: {ex}")
            return {}

    def write_to_sheets(self, client_name: str, data_by_date: Dict[str, List[Dict]]):
        """
        Write historical data to Daily Performance sheet

        Args:
            client_name: Client name
            data_by_date: Dict mapping date to list of products
        """
        if not data_by_date:
            self.log(f"  No data to write for {client_name}")
            return

        # Prepare rows
        rows = []
        for date_str in sorted(data_by_date.keys()):
            products = data_by_date[date_str]

            for product in products:
                row = [
                    date_str,
                    client_name,
                    str(product['product_id']),
                    product['product_title'],
                    str(product['impressions']),
                    str(product['clicks']),
                    f"{product['conversions']:.2f}",
                    f"{product['revenue']:.2f}",
                    f"{product['cost']:.2f}",
                    f"{product['ctr']:.2f}",
                    f"{product['conv_rate']:.2f}",
                    f"{product['roas']:.2f}",
                    product['label']
                ]
                rows.append(row)

        total_rows = len(rows)
        self.log(f"  Writing {total_rows} rows for {client_name}")

        # Write in batches of 5000 rows to avoid API limits
        batch_size = 5000
        for i in range(0, total_rows, batch_size):
            batch = rows[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total_rows + batch_size - 1) // batch_size

            self.log(f"    Batch {batch_num}/{total_batches} ({len(batch)} rows)")

            try:
                # Append to sheet
                body = {'values': batch}
                self.sheets_service.spreadsheets().values().append(
                    spreadsheetId=self.spreadsheet_id,
                    range='Daily Performance!A2',  # Start after headers
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body=body
                ).execute()

                # Rate limiting: wait 1 second between batches
                if i + batch_size < total_rows:
                    time.sleep(1)

            except Exception as e:
                self.log(f"    ERROR writing batch {batch_num}: {e}")
                raise

        self.log(f"  Successfully wrote {total_rows} rows for {client_name}")

    def backfill_client(self, client: Dict):
        """Backfill data for a single client"""
        client_name = client['name']
        customer_id = client['google_ads_customer_id']

        self.log(f"\n{'='*80}")
        self.log(f"Processing: {client_name}")
        self.log(f"Customer ID: {customer_id}")
        self.log(f"{'='*80}")

        # Fetch data
        data_by_date = self.fetch_client_data(customer_id, self.days_back)

        if not data_by_date:
            self.log(f"No data retrieved for {client_name}")
            return False

        # Write to sheets
        try:
            self.write_to_sheets(client_name, data_by_date)
            return True
        except Exception as e:
            self.log(f"ERROR writing data for {client_name}: {e}")
            return False

    def run(self):
        """Run the backfill process for all enabled clients"""
        self.log("\n" + "="*80)
        self.log("HISTORICAL DATA BACKFILL - START")
        self.log("="*80)
        self.log(f"Days to backfill: {self.days_back}")
        self.log(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit")

        # Load progress
        progress = self.load_progress()
        completed_clients = set(progress.get('completed_clients', []))

        if completed_clients:
            self.log(f"\nResuming from previous run. Already completed: {len(completed_clients)} clients")

        # Get enabled clients with merchant_id
        enabled_clients = [
            c for c in self.config['clients']
            if c.get('enabled', False) and c.get('merchant_id')
        ]

        self.log(f"\nFound {len(enabled_clients)} enabled e-commerce clients")

        # Process each client
        success_count = 0
        error_count = 0

        for client in enabled_clients:
            client_name = client['name']

            # Skip if already completed
            if client_name in completed_clients:
                self.log(f"\n[SKIPPED] {client_name} (already completed)")
                success_count += 1
                continue

            # Backfill client
            success = self.backfill_client(client)

            if success:
                success_count += 1
                completed_clients.add(client_name)

                # Save progress
                progress['completed_clients'] = list(completed_clients)
                progress['last_updated'] = datetime.now().isoformat()
                self.save_progress(progress)
            else:
                error_count += 1

            # Rate limiting between clients
            time.sleep(2)

        # Final summary
        self.log("\n" + "="*80)
        self.log("HISTORICAL DATA BACKFILL - COMPLETE")
        self.log("="*80)
        self.log(f"Total clients: {len(enabled_clients)}")
        self.log(f"Successful: {success_count}")
        self.log(f"Errors: {error_count}")

        if error_count == 0:
            self.log("\n✅ All clients backfilled successfully!")
            self.log(f"View data: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit")

            # Clean up progress file
            if self.progress_file.exists():
                self.progress_file.unlink()
                self.log("Progress file cleaned up")
        else:
            self.log(f"\n⚠️  {error_count} clients had errors. Run again to retry.")

        return error_count == 0


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Backfill historical shopping performance data to Google Sheets"
    )
    parser.add_argument(
        '--days',
        type=int,
        default=90,
        help='Number of days to backfill (default: 90)'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Skip confirmation prompts'
    )

    args = parser.parse_args()
    days_back = args.days

    if not 1 <= days_back <= 120:
        print("ERROR: Days must be between 1 and 120")
        return 1

    print("\n" + "="*80, flush=True)
    print("HISTORICAL DATA BACKFILL TOOL", flush=True)
    print("="*80, flush=True)
    print(flush=True)
    print("This script will backfill 60-90 days of historical product performance data", flush=True)
    print("to the Daily Performance sheet in Google Sheets.", flush=True)
    print(flush=True)
    print("⚠️  WARNING: This is a one-time operation that writes a LOT of data.", flush=True)
    print(flush=True)
    print("Estimated data volume:", flush=True)
    print("  - 13 clients × 90 days × ~700 products/client = ~820,000 rows", flush=True)
    print("  - Google Sheets limit: 10 million cells", flush=True)
    print("  - This backfill: ~10.7 million cells (within limits)", flush=True)
    print(flush=True)
    print("The process includes:", flush=True)
    print("  - API rate limiting (1 second between batches)", flush=True)
    print("  - Progress tracking (can resume if interrupted)", flush=True)
    print("  - Batch writing (5000 rows per API call)", flush=True)
    print(flush=True)
    print(f"Days to backfill: {days_back}", flush=True)
    print(flush=True)

    if not args.yes:
        response = input("Continue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.")
            return 1

    # Run backfill
    config_path = Path(__file__).parent / "config.json"

    try:
        backfiller = HistoricalDataBackfiller(config_path, days_back=days_back)
        success = backfiller.run()
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Progress has been saved.")
        print("Run again to resume from where you left off.")
        return 1

    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
