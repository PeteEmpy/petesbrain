#!/usr/bin/env python3
"""
Upload Devonshire Hotels asset performance data to Google Sheets
"""

import csv
import sys
import os

# Add the Google Sheets MCP path if needed
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server')

def read_csv_data(csv_file):
    """Read CSV and convert to 2D array for Google Sheets"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

def main():
    csv_file = 'output/devonshire-asset-performance-api-2025-11-27.csv'

    print("=" * 80)
    print("UPLOADING DEVONSHIRE HOTELS DATA TO GOOGLE SHEETS")
    print("=" * 80)
    print()

    # Read CSV data
    data = read_csv_data(csv_file)
    print(f"✓ Read {len(data)} rows from CSV")
    print()

    # The data is now ready for Google Sheets API
    # Format: [
    #   ["Performance Max campaigns"],
    #   ["Campaign", "Asset group", "Asset", ...],
    #   ["DEV | Core...", "The Cavendish Hotel", "The Cavendish Hotel", ...]
    # ]

    print("Data structure:")
    print(f"  - Title row: {data[0]}")
    print(f"  - Header row: {data[1]}")
    print(f"  - Data rows: {len(data) - 2}")
    print()
    print("Ready to upload to Google Sheets via MCP")

    return data

if __name__ == "__main__":
    data = main()
