#!/usr/bin/env python3
"""
Populate HappySnapGifts spreadsheet with fetched data

Reads ads_happysnapgifts.json and writes to the Google Sheet
"""

import json
from pathlib import Path
from collections import defaultdict
from sheets_writer import SheetsWriter

def main():
    # Load config and data
    config_path = Path(__file__).parent / 'config.json'
    data_path = Path(__file__).parent / 'data' / 'ads_happysnapgifts.json'

    print("Loading data...")
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
        writer.append_daily_performance("HappySnapGifts", products)

    print("✅ Complete!")

if __name__ == '__main__':
    main()
