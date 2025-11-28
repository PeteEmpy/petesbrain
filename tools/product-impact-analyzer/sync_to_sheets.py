#!/usr/bin/env python3
"""
Product Impact Analyzer - Spreadsheet Sync (Universal)

Syncs all product intelligence data from JSON files to client Google Sheets.
This is the visualization layer that makes hidden data visible.

What it syncs:
- Product Changes (price, stock, title changes)
- Merchant Centre Disapprovals
- Product Hero Labels (if enabled)
- Product Baselines (30-day performance averages)
- Performance Anomalies (products deviating from baseline)
- Weekly Summaries (aggregated insights)

Usage:
    # Sync all clients (normal daily run)
    python3 sync_to_sheets.py

    # Sync specific client
    python3 sync_to_sheets.py --client "Tree2mydoor"

    # Backfill historical data
    python3 sync_to_sheets.py --backfill --days 30

    # Dry run (show what would be synced)
    python3 sync_to_sheets.py --dry-run

Schedule: Daily at 8:00 AM (via LaunchAgent after product-tracking completes)
LaunchAgent: com.petesbrain.product-sheets-sync.plist

Author: Pete's Brain
Created: 27 November 2025
"""

import json
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sys
import argparse
import time


class SheetsSync:
    """Universal spreadsheet sync for Product Impact Analyzer"""

    def __init__(self, config_path: Path, credentials_path: str, dry_run: bool = False):
        """
        Initialize sheets sync

        Args:
            config_path: Path to config.json
            credentials_path: Path to service account credentials
            dry_run: If True, show what would be synced without writing
        """
        self.config_path = config_path
        self.credentials_path = credentials_path
        self.dry_run = dry_run
        self.base_dir = config_path.parent

        # Load config
        with open(config_path) as f:
            self.config = json.load(f)

        # Initialize Google Sheets client
        self.log("Initializing Google Sheets client...")
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes
        )
        self.gc = gspread.authorize(creds)

        # Initialize Merchant Centre client for disapprovals
        self.log("Initializing Merchant Centre client...")
        mc_scopes = ['https://www.googleapis.com/auth/content']
        self.mc_creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=mc_scopes
        )

        self.stats = {
            'clients_processed': 0,
            'tabs_created': 0,
            'tabs_updated': 0,
            'rows_written': 0,
            'errors': []
        }

    def log(self, message: str, level: str = 'INFO'):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = "🔍 [DRY RUN]" if self.dry_run else ""
        print(f"[{timestamp}] {prefix} {level}: {message}")

    def get_enabled_clients(self) -> List[Dict]:
        """Get list of enabled clients from config"""
        return [c for c in self.config['clients'] if c.get('enabled', True)]

    def sync_all_clients(self):
        """Sync data for all enabled clients"""
        clients = self.get_enabled_clients()
        self.log(f"Syncing {len(clients)} enabled clients...")

        for client in clients:
            try:
                self.sync_client(client)
                self.stats['clients_processed'] += 1
            except Exception as e:
                error_msg = f"Error syncing {client['name']}: {str(e)}"
                self.log(error_msg, 'ERROR')
                self.stats['errors'].append(error_msg)

        self.print_summary()

    def sync_client(self, client: Dict):
        """
        Sync all data for a specific client

        Args:
            client: Client config dict from config.json
        """
        client_name = client['name']
        spreadsheet_id = client.get('product_performance_spreadsheet_id')

        if not spreadsheet_id:
            self.log(f"No spreadsheet ID for {client_name}, skipping", 'WARNING')
            return

        self.log(f"\n{'='*80}")
        self.log(f"Syncing {client_name}")
        self.log(f"Spreadsheet: {spreadsheet_id}")
        self.log(f"{'='*80}")

        try:
            # Open spreadsheet
            if not self.dry_run:
                sh = self.gc.open_by_key(spreadsheet_id)
            else:
                sh = None
                self.log(f"Would open spreadsheet: {spreadsheet_id}")

            # Sync each data type
            self.sync_product_changes(client, sh)
            self.sync_disapprovals(client, sh)
            self.sync_product_baselines(client, sh)
            self.sync_performance_anomalies(client, sh)

            # Only sync labels if enabled for this client
            if client.get('label_tracking', {}).get('enabled', False):
                self.sync_product_hero_labels(client, sh)

            # Update sync timestamp
            if not self.dry_run and sh:
                self.update_sync_metadata(sh)

            self.log(f"✅ Completed {client_name}")

        except Exception as e:
            raise Exception(f"Failed to sync {client_name}: {str(e)}")

    def sync_product_changes(self, client: Dict, sh: Optional[gspread.Spreadsheet]):
        """Sync product changes to 'Product Changes' tab"""
        client_name = client['name']
        self.log(f"  📝 Syncing product changes...")

        # Load latest product changes
        changes_dir = self.base_dir / 'data' / 'product_changes' / client_name
        if not changes_dir.exists():
            self.log(f"    No changes directory for {client_name}", 'WARNING')
            return

        # Get latest changes file
        change_files = sorted(changes_dir.glob('*.json'), reverse=True)
        if not change_files:
            self.log(f"    No change files found", 'WARNING')
            return

        latest_changes_file = change_files[0]
        with open(latest_changes_file) as f:
            changes_data = json.load(f)

        # Check if there are any changes
        total_changes = changes_data['summary']['changed_products']
        if total_changes == 0:
            self.log(f"    No changes detected in latest file")
            return

        self.log(f"    Found {total_changes} product changes on {changes_data['date']}")

        # Prepare rows for sheet
        rows = self._format_product_changes(changes_data)

        if self.dry_run:
            self.log(f"    Would write {len(rows)} rows to 'Product Changes' tab")
            if rows:
                self.log(f"    Sample row: {rows[0][:5]}...")
            return

        # Get or create 'Product Changes' worksheet
        ws = self._get_or_create_worksheet(sh, 'Product Changes', headers=[
            'Date Detected', 'Product ID', 'Product Title', 'Change Type',
            'Field Changed', 'Old Value', 'New Value', 'Status'
        ])

        # Append new rows (keep last 90 days)
        self._append_and_trim_rows(ws, rows, days_to_keep=90, date_column=0)
        self.stats['rows_written'] += len(rows)
        self.log(f"    ✅ Wrote {len(rows)} rows to Product Changes")

    def sync_disapprovals(self, client: Dict, sh: Optional[gspread.Spreadsheet]):
        """Sync disapprovals to 'Disapprovals' tab"""
        client_name = client['name']
        merchant_id = client['merchant_id']
        self.log(f"  ⚠️  Syncing disapprovals...")

        try:
            # Fetch current disapprovals from Merchant Centre API
            service = build('content', 'v2.1', credentials=self.mc_creds)
            request = service.products().list(merchantId=merchant_id, maxResults=250)
            response = request.execute()

            products = response.get('resources', [])
            self.log(f"    Fetched {len(products)} products from Merchant Centre")

            # Extract disapprovals
            disapprovals = []
            for product in products:
                product_id = product.get('id')
                title = product.get('title', 'N/A')

                item_issues = product.get('itemLevelIssues', [])
                for issue in item_issues:
                    severity = issue.get('severity', 'N/A')
                    if severity == 'disapproved':
                        disapprovals.append({
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'product_id': product_id,
                            'title': title,
                            'code': issue.get('code', 'N/A'),
                            'description': issue.get('description', 'N/A'),
                            'status': 'Active'
                        })

            self.log(f"    Found {len(disapprovals)} disapprovals")

            if len(disapprovals) == 0:
                self.log(f"    No disapprovals - all products approved ✅")
                # Still update the sheet to show "Last Checked" date
                if not self.dry_run:
                    ws = self._get_or_create_worksheet(sh, 'Disapprovals', headers=[
                        'Date First Seen', 'Product ID', 'Product Title',
                        'Issue Code', 'Issue Description', 'Status', 'Last Checked'
                    ])
                    # Add "Last checked" message in first row
                    ws.update('A2', [[f"Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                                     'No disapprovals', 'All products approved ✅', '', '', '', '']])
                return

            # Format rows
            rows = [[
                d['date'], d['product_id'], d['title'], d['code'],
                d['description'], d['status'],
                datetime.now().strftime('%Y-%m-%d %H:%M')
            ] for d in disapprovals]

            if self.dry_run:
                self.log(f"    Would write {len(rows)} disapprovals to 'Disapprovals' tab")
                return

            # Get or create worksheet
            ws = self._get_or_create_worksheet(sh, 'Disapprovals', headers=[
                'Date First Seen', 'Product ID', 'Product Title',
                'Issue Code', 'Issue Description', 'Status', 'Last Checked'
            ])

            # Update disapprovals (merge with existing to track first seen dates)
            self._update_disapprovals_with_history(ws, rows)
            self.stats['rows_written'] += len(rows)
            self.log(f"    ✅ Updated {len(rows)} disapprovals")

        except Exception as e:
            self.log(f"    Error fetching disapprovals: {str(e)}", 'ERROR')
            raise

    def sync_product_hero_labels(self, client: Dict, sh: Optional[gspread.Spreadsheet]):
        """Sync Product Hero labels to 'Product Hero Labels' tab"""
        client_name = client['name']
        self.log(f"  🏆 Syncing Product Hero labels...")

        # Load current labels
        labels_file = self.base_dir / 'history' / 'label-transitions' / \
                     client_name.lower().replace(' ', '-') / 'current-labels.json'

        if not labels_file.exists():
            self.log(f"    No labels file found", 'WARNING')
            return

        with open(labels_file) as f:
            labels_data = json.load(f)

        products = labels_data.get('products', {})
        if not products:
            self.log(f"    No labels data", 'WARNING')
            return

        self.log(f"    Found {len(products)} products with labels")

        # Format rows
        rows = [[
            product_id,
            '',  # Product title (will be joined from performance data)
            label,
            labels_data.get('last_updated', 'N/A')
        ] for product_id, label in products.items()]

        if self.dry_run:
            self.log(f"    Would write {len(rows)} label rows to 'Product Hero Labels' tab")
            return

        # Get or create worksheet
        ws = self._get_or_create_worksheet(sh, 'Product Hero Labels', headers=[
            'Product ID', 'Product Title', 'Current Label', 'Last Updated'
        ])

        # Overwrite with current labels
        ws.clear()
        ws.update('A1', [['Product ID', 'Product Title', 'Current Label', 'Last Updated']] + rows)
        self.stats['rows_written'] += len(rows)
        self.log(f"    ✅ Wrote {len(rows)} label rows")

    def sync_product_baselines(self, client: Dict, sh: Optional[gspread.Spreadsheet]):
        """Sync product baselines to 'Product Baselines' tab"""
        client_name = client['name']
        self.log(f"  📊 Syncing product baselines...")

        # Load baselines
        baselines_file = self.base_dir / 'data' / 'product_baselines' / \
                        f"{client_name.lower().replace(' ', '-')}.json"

        if not baselines_file.exists():
            self.log(f"    No baselines file found", 'WARNING')
            return

        with open(baselines_file) as f:
            baselines_data = json.load(f)

        baselines = baselines_data.get('baselines', {})
        if not baselines:
            self.log(f"    No baseline data", 'WARNING')
            return

        self.log(f"    Found {len(baselines)} product baselines")

        # Format rows
        rows = []
        for product_id, baseline in baselines.items():
            # Extract mean values from nested dicts
            revenue_mean = baseline.get('revenue', {}).get('mean', 0) if isinstance(baseline.get('revenue'), dict) else baseline.get('revenue', 0)
            clicks_mean = baseline.get('clicks', {}).get('mean', 0) if isinstance(baseline.get('clicks'), dict) else baseline.get('clicks', 0)
            conversions_mean = baseline.get('conversions', {}).get('mean', 0) if isinstance(baseline.get('conversions'), dict) else baseline.get('conversions', 0)

            rows.append([
                product_id,
                baseline.get('product_title', ''),
                f"£{revenue_mean:.2f}",
                f"{clicks_mean:.1f}",
                f"{conversions_mean:.1f}",
                '',  # ROAS will be calculated separately if needed
                baselines_data.get('updated', 'N/A')
            ])

        if self.dry_run:
            self.log(f"    Would write {len(rows)} baseline rows to 'Product Baselines' tab")
            return

        # Get or create worksheet
        ws = self._get_or_create_worksheet(sh, 'Product Baselines', headers=[
            'Product ID', 'Product Title', '30d Avg Revenue', '30d Avg Clicks',
            '30d Avg Conversions', 'ROAS', 'Last Updated'
        ])

        # Overwrite with current baselines
        ws.clear()
        ws.update('A1', [['Product ID', 'Product Title', '30d Avg Revenue', '30d Avg Clicks',
                         '30d Avg Conversions', 'ROAS', 'Last Updated']] + rows)
        self.stats['rows_written'] += len(rows)
        self.log(f"    ✅ Wrote {len(rows)} baseline rows")

    def sync_performance_anomalies(self, client: Dict, sh: Optional[gspread.Spreadsheet]):
        """Sync performance anomalies to 'Performance Anomalies' tab"""
        client_name = client['name']
        self.log(f"  🔔 Syncing performance anomalies...")

        # Note: Anomalies are currently only logged/emailed, not saved to JSON
        # For now, create empty tab with headers
        # TODO: Update product_anomaly_detector.py to save anomalies to JSON

        if self.dry_run:
            self.log(f"    Would create 'Performance Anomalies' tab (empty - not yet implemented)")
            return

        # Get or create worksheet
        ws = self._get_or_create_worksheet(sh, 'Performance Anomalies', headers=[
            'Date Detected', 'Product ID', 'Product Title', 'Metric',
            'Baseline Value', 'Actual Value', 'Deviation %', 'Severity'
        ])

        # Add placeholder message
        ws.update('A2', [[
            'Note: Anomaly detection is running, but data not yet archived to sheets.',
            'Email alerts are being sent for significant deviations.',
            'Future update will populate this tab with historical anomalies.',
            '', '', '', '', ''
        ]])
        self.log(f"    ℹ️  Created placeholder tab (feature pending)")

    def update_sync_metadata(self, sh: gspread.Spreadsheet):
        """Update sync metadata in a hidden 'Sync Info' tab"""
        try:
            # Get or create Sync Info tab
            try:
                ws = sh.worksheet('Sync Info')
            except gspread.WorksheetNotFound:
                ws = sh.add_worksheet(title='Sync Info', rows=10, cols=2)
                self.stats['tabs_created'] += 1

            # Update metadata
            ws.update('A1', [
                ['Last Synced', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Sync Script', 'sync_to_sheets.py'],
                ['Version', '1.0.0'],
                ['Data Sources', 'Merchant Centre API, Product Changes JSON, Baselines JSON, Labels JSON']
            ])

        except Exception as e:
            self.log(f"    Warning: Could not update sync metadata: {str(e)}", 'WARNING')

    # ========== Helper Methods ==========

    def _get_or_create_worksheet(self, sh: gspread.Spreadsheet, title: str,
                                 headers: List[str]) -> gspread.Worksheet:
        """Get existing worksheet or create new one with headers"""
        try:
            ws = sh.worksheet(title)
            self.log(f"    Found existing '{title}' tab")
            self.stats['tabs_updated'] += 1
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(title=title, rows=1000, cols=len(headers))
            ws.update('A1', [headers])
            self.log(f"    Created new '{title}' tab")
            self.stats['tabs_created'] += 1

        return ws

    def _format_product_changes(self, changes_data: Dict) -> List[List[str]]:
        """Format product changes data into rows for spreadsheet"""
        rows = []
        date = changes_data['date']

        for product in changes_data['changed_products']:
            product_id = product['product_id']
            title = product['title']

            for field, (old_val, new_val) in product['changes'].items():
                # Determine change type
                if field == 'price':
                    change_type = 'Price'
                elif field == 'availability':
                    change_type = 'Stock'
                elif field == 'title':
                    change_type = 'Title'
                elif field == 'description':
                    change_type = 'Description'
                elif field == 'product_type':
                    change_type = 'Product Type'
                else:
                    change_type = 'Other'

                rows.append([
                    date,
                    product_id,
                    title,
                    change_type,
                    field,
                    str(old_val),
                    str(new_val),
                    'Active'
                ])

        return rows

    def _append_and_trim_rows(self, ws: gspread.Worksheet, new_rows: List[List[Any]],
                              days_to_keep: int = 90, date_column: int = 0):
        """
        Append new rows and trim old rows beyond retention period

        Args:
            ws: Worksheet to update
            new_rows: New rows to append
            days_to_keep: Number of days of data to retain
            date_column: Column index containing date (0-indexed)
        """
        # Get existing data including headers
        all_existing = ws.get_all_values()
        headers = all_existing[0] if all_existing else []
        existing_data = all_existing[1:] if len(all_existing) > 1 else []

        # Calculate cutoff date
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')

        # Filter existing data to keep only recent rows
        recent_data = [row for row in existing_data
                      if len(row) > date_column and row[date_column] >= cutoff_date]

        # Combine and write
        all_data = recent_data + new_rows

        # Clear and rewrite with headers
        ws.clear()
        if headers:
            ws.update('A1', [headers] + all_data)
        else:
            ws.update('A1', all_data)

    def _update_disapprovals_with_history(self, ws: gspread.Worksheet, new_rows: List[List[str]]):
        """
        Update disapprovals tab, merging with existing to track 'Date First Seen'

        Args:
            ws: Disapprovals worksheet
            new_rows: New disapproval rows
        """
        # Get existing data
        existing_data = ws.get_all_values()[1:]  # Skip header

        # Build map of existing disapprovals: (product_id, issue_code) -> row
        existing_map = {}
        for row in existing_data:
            if len(row) >= 4:
                key = (row[1], row[3])  # (Product ID, Issue Code)
                existing_map[key] = row

        # Process new rows
        updated_rows = []
        for new_row in new_rows:
            product_id = new_row[1]
            issue_code = new_row[3]
            key = (product_id, issue_code)

            if key in existing_map:
                # Keep original "Date First Seen"
                existing_row = existing_map[key]
                new_row[0] = existing_row[0]  # Preserve first seen date

            updated_rows.append(new_row)

        # Mark resolved disapprovals
        for key, existing_row in existing_map.items():
            if key not in [(r[1], r[3]) for r in new_rows]:
                # Disapproval no longer exists - mark as resolved
                existing_row[5] = 'Resolved'
                existing_row[6] = datetime.now().strftime('%Y-%m-%d')
                updated_rows.append(existing_row)

        # Write all rows
        ws.clear()
        headers = ['Date First Seen', 'Product ID', 'Product Title',
                  'Issue Code', 'Issue Description', 'Status', 'Date Resolved']
        ws.update('A1', [headers] + updated_rows)

    def print_summary(self):
        """Print sync summary statistics"""
        self.log(f"\n{'='*80}")
        self.log("SYNC SUMMARY")
        self.log(f"{'='*80}")
        self.log(f"Clients processed: {self.stats['clients_processed']}")
        self.log(f"Tabs created: {self.stats['tabs_created']}")
        self.log(f"Tabs updated: {self.stats['tabs_updated']}")
        self.log(f"Total rows written: {self.stats['rows_written']}")

        if self.stats['errors']:
            self.log(f"\nErrors encountered: {len(self.stats['errors'])}", 'ERROR')
            for error in self.stats['errors']:
                self.log(f"  - {error}", 'ERROR')
        else:
            self.log("\n✅ All syncs completed successfully!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Sync Product Impact Analyzer data to Google Sheets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync all clients (daily run)
  python3 sync_to_sheets.py

  # Sync specific client
  python3 sync_to_sheets.py --client "Tree2mydoor"

  # Dry run (show what would be synced)
  python3 sync_to_sheets.py --dry-run

Environment Variables:
  GOOGLE_APPLICATION_CREDENTIALS - Path to service account credentials JSON
        """
    )

    parser.add_argument('--client', help='Sync specific client only')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be synced without writing')
    parser.add_argument('--backfill', action='store_true',
                       help='Backfill historical data (not yet implemented)')
    parser.add_argument('--days', type=int, default=30,
                       help='Days to backfill (with --backfill)')

    args = parser.parse_args()

    # Get credentials path from environment
    import os
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        print("ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        print("Set it to the path of your service account credentials JSON")
        sys.exit(1)

    # Initialize sync
    config_path = Path(__file__).parent / 'config.json'
    sync = SheetsSync(config_path, credentials_path, dry_run=args.dry_run)

    # Run sync
    if args.client:
        # Sync specific client
        clients = sync.get_enabled_clients()
        client = next((c for c in clients if c['name'] == args.client), None)
        if not client:
            sync.log(f"Client '{args.client}' not found in config", 'ERROR')
            sys.exit(1)
        sync.sync_client(client)
    else:
        # Sync all clients
        sync.sync_all_clients()

    # Exit with error code if there were errors
    if sync.stats['errors']:
        sys.exit(1)


if __name__ == '__main__':
    main()
