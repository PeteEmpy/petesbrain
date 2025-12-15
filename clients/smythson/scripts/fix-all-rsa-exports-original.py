#!/usr/bin/env python3
"""Fix all RSA exports to use #original for empty fields when updating existing ads"""

import csv
import os

# Define all files to process
files = [
    ('rsa-usa-export-20251215.csv', 'rsa-usa-export-fixed-20251215.csv'),
    ('rsa-eur-export-20251215.csv', 'rsa-eur-export-fixed-20251215.csv'),
    ('rsa-row-export-20251215.csv', 'rsa-row-export-fixed-20251215.csv')
]

for input_file, output_file in files:
    if not os.path.exists(input_file):
        print(f"⚠️  {input_file} not found, skipping")
        continue

    rows = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        # Find column indices
        try:
            h1_idx = header.index('H1')
            d1_idx = header.index('D1')
            final_url_idx = header.index('Final URL')
        except ValueError as e:
            print(f"⚠️  Error finding columns in {input_file}: {e}")
            continue

        for i, row in enumerate(reader, start=2):
            if not row:
                continue

            # Ensure row has enough columns
            while len(row) <= final_url_idx:
                row.append('')

            # Process headlines (H1-H15)
            for j in range(h1_idx, h1_idx + 15):
                if j < len(row):
                    # Replace empty headlines with #original
                    if row[j] == '' or row[j].isspace():
                        row[j] = '#original'
                else:
                    # Add #original for missing columns
                    row.append('#original')

            # Process descriptions (D1-D4)
            for j in range(d1_idx, d1_idx + 4):
                if j < len(row):
                    # Replace empty descriptions with #original
                    if row[j] == '' or row[j].isspace():
                        row[j] = '#original'
                else:
                    # Add #original for missing columns
                    row.append('#original')

            rows.append(row)

    # Write the fixed file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Created {output_file}")

    # Show sample of what was changed
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) > 1:
            # Count #original occurrences in first data row
            first_data = lines[1]
            original_count = first_data.count('#original')
            if original_count > 0:
                print(f"   - Added {original_count} #original markers for unchanged fields")
            else:
                print(f"   - All fields have values (no #original needed)")

print("\n🎯 All regional RSA exports now have #original for empty fields")
print("Files ready for Google Ads Editor import:")
print("- rsa-uk-export-fixed-20251215.csv (already created)")
print("- rsa-usa-export-fixed-20251215.csv")
print("- rsa-eur-export-fixed-20251215.csv")
print("- rsa-row-export-fixed-20251215.csv")