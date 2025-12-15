#!/usr/bin/env python3
"""Fix RSA export to use #original for empty fields when updating existing ads"""

import csv

# Read the UK export
filename = 'rsa-uk-export-20251215.csv'
rows = []

with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)

    for i, row in enumerate(reader, start=2):
        if not row:
            continue

        # Find where headlines and descriptions start
        h1_idx = header.index('H1')
        d1_idx = header.index('D1')

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

        # Special handling for known problem lines
        if i == 26:  # Line 26 has empty H2
            print(f"Line {i}: Fixing empty H2")
            row[h1_idx + 1] = '#original'  # H2 position

        # For lines with only 9 headlines filled (lines 10-12)
        if i in [10, 11, 12]:
            print(f"Line {i}: Filling remaining headlines with #original")
            # These have headlines up to H9, so H10-H15 should be #original
            for j in range(h1_idx + 9, h1_idx + 15):
                if j < len(row) and (row[j] == '' or row[j].isspace()):
                    row[j] = '#original'

        rows.append(row)

# Write the fixed file
output_file = 'rsa-uk-export-fixed-20251215.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"✅ Created {output_file} with #original for empty fields")
print("\nProblem lines fixed:")
print("- Lines 7-12: Empty headlines replaced with #original")
print("- Line 26: Empty H2 replaced with #original")
print("\nThis format tells Google Ads Editor to keep existing values for those fields.")