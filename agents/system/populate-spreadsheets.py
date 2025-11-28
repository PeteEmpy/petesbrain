#!/usr/bin/env python3
"""
Populate all client Product Performance spreadsheets with daily data.

Reads from ads_*.json files (fetched by fetch_data_automated.py)
and writes daily snapshots to each client's dedicated spreadsheet.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from sheets_writer import SheetsWriter
from collections import defaultdict

def log(message: str):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    """Main execution"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'
    data_dir = script_dir / 'data'

    log("=" * 80)
    log("POPULATE ALL CLIENT SPREADSHEETS")
    log("=" * 80)

    # Initialize sheets writer
    writer = SheetsWriter(config_path)

    # Load config to get client list
    with open(config_path) as f:
        config = json.load(f)

    # Process each client
    total_updated = 0
    total_skipped = 0

    for client in config['clients']:
        if not client.get('enabled'):
            continue

        client_name = client['name']
        merchant_id = client.get('merchant_id')

        if not merchant_id or merchant_id == 'UNKNOWN':
            log(f"⚠️  {client_name}: No merchant ID, skipping")
            total_skipped += 1
            continue

        # Check if spreadsheet ID exists
        spreadsheet_id = client.get('product_performance_spreadsheet_id')
        if not spreadsheet_id:
            log(f"⚠️  {client_name}: No spreadsheet ID in config, skipping")
            total_skipped += 1
            continue

        # Build filename from client name
        filename_base = client_name.lower().replace(' ', '_').replace('(', '').replace(')', '')
        ads_file = data_dir / f'ads_{filename_base}.json'

        if not ads_file.exists():
            log(f"⚠️  {client_name}: No data file {ads_file.name}, skipping")
            total_skipped += 1
            continue

        log(f"\nProcessing {client_name}...")
        log(f"  Data file: {ads_file.name}")
        log(f"  Spreadsheet ID: {spreadsheet_id}")

        # Load ads data
        try:
            with open(ads_file) as f:
                ads_data = json.load(f)
        except Exception as e:
            log(f"  ❌ Error loading data: {e}")
            total_skipped += 1
            continue

        log(f"  Loaded {len(ads_data):,} rows")

        # Group by date
        products_by_date = defaultdict(list)
        for row in ads_data:
            # Date is in segments.date
            date = row.get('segments', {}).get('date')
            if date:
                products_by_date[date].append(row)

        if not products_by_date:
            log(f"  ⚠️  No dated data found")
            total_skipped += 1
            continue

        log(f"  Found data for {len(products_by_date)} dates")

        # Write most recent date only (today's snapshot)
        # Sort dates and get the most recent
        latest_date = max(products_by_date.keys())
        products = products_by_date[latest_date]

        log(f"  Writing {len(products)} products for {latest_date}...")

        success = writer.append_daily_performance(client_name, products)

        if success:
            log(f"  ✅ Updated spreadsheet for {client_name}")
            total_updated += 1
        else:
            log(f"  ❌ Failed to update spreadsheet for {client_name}")
            total_skipped += 1

    log("\n" + "=" * 80)
    log("COMPLETE")
    log("=" * 80)
    log(f"\n✅ Updated: {total_updated} clients")
    log(f"⚠️  Skipped: {total_skipped} clients")

    if total_updated == 0 and total_skipped > 0:
        log("\n⚠️  WARNING: No spreadsheets were updated!")
        sys.exit(1)

if __name__ == '__main__':
    main()
