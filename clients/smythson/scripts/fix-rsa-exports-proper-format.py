#!/usr/bin/env python3
"""Fix RSA exports with proper Google Ads Editor format"""

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

        # Find where the actual data columns start (after Type column currently)
        type_idx = header.index('Type') if 'Type' in header else -1

        # Create new header with proper columns for Google Ads Editor
        # Account, Action, Type, Ad type, then the rest of the columns
        if type_idx >= 0:
            # Skip Account and Type columns, start from Campaign ID
            data_columns = header[type_idx+1:]
        else:
            # If Type not found, start from Campaign ID (index 1)
            data_columns = header[1:]

        new_header = ['Account', 'Action', 'Type', 'Ad type'] + data_columns
        rows.append(new_header)

        # Process data rows
        for row in reader:
            if row:  # Skip empty rows
                # Extract data columns (skip current Account and Type if present)
                if type_idx >= 0:
                    data_values = row[type_idx+1:]
                else:
                    data_values = row[1:]

                # Create new row with proper format
                new_row = [account_id, 'Edit', 'Ad', 'Responsive search ad'] + data_values
                rows.append(new_row)

    # Write back the fixed data
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Fixed {filename} - proper Google Ads Editor format")

    # Show first 2 rows to verify
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:2]
        print(f"   Header: {lines[0][:150]}...")
        if len(lines) > 1:
            print(f"   First row: {lines[1][:150]}...")

print("\n🎯 All RSA exports now have proper format for Google Ads Editor import:")
print("   - Type = 'Ad'")
print("   - Ad type = 'Responsive search ad'")
print("   - Action = 'Edit' (for updating existing ads)")