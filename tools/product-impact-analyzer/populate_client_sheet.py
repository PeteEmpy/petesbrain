#!/usr/bin/env python3
"""
Populate client spreadsheet with fetched data

Usage: python3 populate_client_sheet.py <client_name>
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from sheets_writer import SheetsWriter

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 populate_client_sheet.py <client_name>")
        sys.exit(1)

    client_name = sys.argv[1]

    # Load config and data
    config_path = Path(__file__).parent / 'config.json'
    data_filename = f"ads_{client_name.replace(' ', '_').lower()}.json"
    data_path = Path(__file__).parent / 'data' / data_filename

    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        sys.exit(1)

    print(f"Loading data for {client_name}...")
    with open(data_path) as f:
        raw_data = json.load(f)

    print(f"Loaded {len(raw_data)} rows")

    # Group by date
    by_date = defaultdict(list)
    for row in raw_data:
        date = row['segments']['date']
        by_date[date].append(row)

    print(f"Found data for {len(by_date)} dates")

    # Initialize sheets writer
    writer = SheetsWriter(config_path)

    # Process each date
    for date in sorted(by_date.keys()):
        rows = by_date[date]

        # Convert to expected format
        products = []
        for row in rows:
            products.append({
                'product_id': row['segments']['productItemId'],
                'product_title': row['segments']['productTitle'],
                'impressions': int(row['metrics']['impressions']),
                'clicks': int(row['metrics']['clicks']),
                'conversions': float(row['metrics']['conversions']),
                'revenue': float(row['metrics']['conversionsValue']),
                'cost': float(row['metrics']['costMicros']) / 1_000_000,
                'date': date,
                'label': ''  # Labels come from separate API call
            })

        print(f"Writing {len(products)} products for {date}...")
        writer.append_daily_performance(client_name, products)

    print(f"✅ Complete! Populated {client_name} spreadsheet")

if __name__ == '__main__':
    main()
