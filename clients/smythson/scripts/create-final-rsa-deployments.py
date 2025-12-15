#!/usr/bin/env python3
"""Create final clean RSA CSV files for Monday deployment"""

import csv
import shutil
from datetime import datetime

base_dir = '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/spreadsheets'

# Source files (verified working)
source_files = {
    'UK': f'{base_dir}/rsa-uk-proven-format-20251215.csv',
    'USA': f'{base_dir}/rsa-usa-proven-format-20251215.csv',
    'EUR': f'{base_dir}/rsa-eur-proven-format-20251215.csv',
    'ROW': f'{base_dir}/rsa-row-proven-format-20251215.csv'
}

# Destination files (clean names for deployment)
dest_files = {
    'UK': f'{base_dir}/DEPLOY-MONDAY-rsa-uk-20251216.csv',
    'USA': f'{base_dir}/DEPLOY-MONDAY-rsa-usa-20251216.csv',
    'EUR': f'{base_dir}/DEPLOY-MONDAY-rsa-eur-20251216.csv',
    'ROW': f'{base_dir}/DEPLOY-MONDAY-rsa-row-20251216.csv'
}

print("=" * 80)
print("CREATING FINAL RSA DEPLOYMENT FILES")
print("=" * 80)

total_ads = 0

for region in ['UK', 'USA', 'EUR', 'ROW']:
    source = source_files[region]
    dest = dest_files[region]

    # Copy file
    shutil.copy2(source, dest)

    # Count ads
    with open(dest) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        ads = len(list(reader))
        total_ads += ads

    print(f"\n✅ {region}:")
    print(f"   Source: {source.split('/')[-1]}")
    print(f"   Output: {dest.split('/')[-1]}")
    print(f"   Ads: {ads}")

print(f"\n{'=' * 80}")
print(f"DEPLOYMENT FILES CREATED")
print(f"{'=' * 80}")
print(f"\nTotal ads across all regions: {total_ads}")
print("\nFiles ready for import into Google Ads Editor:")
for region, path in dest_files.items():
    print(f"  - {path.split('/')[-1]}")

print("\n" + "=" * 80)
