#!/usr/bin/env python3
"""Fix RSA CSV validation issues - remove -- markers and duplicate headlines"""

import csv
import os
from collections import Counter

base_dir = '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/spreadsheets'

files_to_fix = {
    'UK': 'DEPLOY-MONDAY-rsa-uk-20251216.csv',
    'USA': 'DEPLOY-MONDAY-rsa-usa-20251216.csv',
    'EUR': 'DEPLOY-MONDAY-rsa-eur-20251216.csv',
    'ROW': 'DEPLOY-MONDAY-rsa-row-20251216.csv'
}

print("=" * 80)
print("FIXING RSA CSV VALIDATION ISSUES")
print("=" * 80)

for region, filename in files_to_fix.items():
    filepath = os.path.join(base_dir, filename)

    print(f"\n{'=' * 80}")
    print(f"REGION: {region} - {filename}")
    print(f"{'=' * 80}")

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    fixed_rows = []
    issues_found = 0
    duplicates_removed = 0

    for i, row in enumerate(rows, start=2):
        # Find headline columns
        headline_cols = [col for col in fieldnames if col.startswith('Headline ')]

        # Collect headlines (non-empty, non--)
        headlines = []
        for col in headline_cols:
            value = row[col].strip()
            if value and value != '--':
                headlines.append(value)

        # Check for duplicates
        headline_counts = Counter(headlines)
        duplicates = [h for h, count in headline_counts.items() if count > 1]

        if duplicates:
            print(f"  Row {i}: Found duplicate headlines: {duplicates}")
            issues_found += 1

            # Remove duplicates - keep first occurrence only
            seen = set()
            unique_headlines = []
            for h in headlines:
                if h not in seen:
                    unique_headlines.append(h)
                    seen.add(h)
                else:
                    duplicates_removed += 1

            headlines = unique_headlines

        # Rebuild row with cleaned headlines
        new_row = row.copy()

        # Clear all headline fields first
        for col in headline_cols:
            new_row[col] = ''

        # Fill with unique headlines
        for idx, headline in enumerate(headlines):
            if idx < len(headline_cols):
                col = f'Headline {idx + 1}'
                new_row[col] = headline

        # Do the same for descriptions
        desc_cols = [col for col in fieldnames if col.startswith('Description ')]
        descriptions = []
        for col in desc_cols:
            value = row[col].strip()
            if value and value != '--':
                descriptions.append(value)

        # Clear and rebuild descriptions
        for col in desc_cols:
            new_row[col] = ''
        for idx, desc in enumerate(descriptions):
            if idx < len(desc_cols):
                col = f'Description {idx + 1}'
                new_row[col] = desc

        fixed_rows.append(new_row)

    # Write fixed file
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(fixed_rows)

    if issues_found > 0:
        print(f"\n  ✅ Fixed {issues_found} ads with issues")
        print(f"  ✅ Removed {duplicates_removed} duplicate headlines")
    else:
        print(f"\n  ✅ No issues found - file already clean")

print(f"\n{'=' * 80}")
print(f"ALL FILES FIXED")
print(f"{'=' * 80}")
print(f"\nFiles ready for import:")
for region, filename in files_to_fix.items():
    print(f"  - {filename}")

print(f"\n{'=' * 80}")
