#!/usr/bin/env python3
"""Debug the Final URL issue"""

import csv

# Check the UK file
input_file = 'rsa-uk-export-fixed-paused-20251215.csv'

with open(input_file, 'r') as f:
    reader = csv.DictReader(f)

    print("Column headers found:")
    print(reader.fieldnames)
    print("\n" + "="*50 + "\n")

    # Read first row
    first_row = next(reader)

    print("First row data:")
    print(f"Campaign: {first_row.get('Campaign Name', 'NOT FOUND')}")
    print(f"Ad Group: {first_row.get('Ad Group Name', 'NOT FOUND')}")
    print(f"Ad ID: {first_row.get('Ad ID', 'NOT FOUND')}")
    print(f"H1: {first_row.get('H1', 'NOT FOUND')}")
    print(f"D1: {first_row.get('D1', 'NOT FOUND')}")
    print(f"D2: {first_row.get('D2', 'NOT FOUND')}")
    print(f"D3: {first_row.get('D3', 'NOT FOUND')}")
    print(f"D4: {first_row.get('D4', 'NOT FOUND')}")
    print(f"Final URL: {first_row.get('Final URL', 'NOT FOUND')}")

    print("\n" + "="*50 + "\n")
    print("All keys in row:")
    for key in first_row.keys():
        print(f"  '{key}': '{first_row[key][:50] if first_row[key] else '(empty)'}'...")