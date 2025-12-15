#!/usr/bin/env python3
"""Fix RSA exports by adding Type column after Account column"""

import csv
import os

# Define the files and their account IDs
files = [
    ('rsa-uk-export-20251215.csv', '8573235780'),
    ('rsa-usa-export-20251215.csv', '4941701449'),
    ('rsa-eur-export-20251215.csv', '6266938115'),
    ('rsa-row-export-20251215.csv', '9095901313')
]

for filename, account_id in files:
    if not os.path.exists(filename):
        print(f"⚠️  {filename} not found")
        continue

    # Read the existing data
    rows = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Check if Type column already exists
        if 'Type' in header:
            print(f"✅ {filename} already has Type column")
            continue

        # Create new header with Type column after Account
        new_header = ['Account', 'Type'] + header[1:]  # Skip existing Account column
        rows.append(new_header)

        # Process data rows
        for row in reader:
            if row:  # Skip empty rows
                # Create new row with Account, Type, then rest of data
                new_row = [account_id, 'Responsive search ad'] + row[1:]
                rows.append(new_row)

    # Write back the fixed data
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Fixed {filename} - added Type column")

    # Show first 2 rows to verify
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:2]
        print(f"   Header: {lines[0].strip()}")
        if len(lines) > 1:
            print(f"   First row: {lines[1][:100]}...")

print("\n🎯 All RSA exports now have Account and Type columns for Google Ads Editor import")