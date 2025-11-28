#!/usr/bin/env python3
"""Combine USA, EUR, and ROW RSA updates into one CSV with Account column"""

import json
import csv

# Account mappings
ACCOUNTS = {
    'USA': {'customer_id': '7808690871', 'account_id': '780-869-0871', 'account_name': 'Smythson USA'},
    'EUR': {'customer_id': '7679616761', 'account_id': '767-961-6761', 'account_name': 'Smythson EUR'},
    'ROW': {'customer_id': '5556710725', 'account_id': '555-671-0725', 'account_name': 'Smythson ROW'}
}

def load_region_updates(region):
    """Load update JSON for a region"""
    input_file = f'/Users/administrator/Documents/PetesBrain/clients/smythson/data/{region.lower()}_rsa_updates_full.json'
    with open(input_file, 'r') as f:
        return json.load(f)

def build_csv_row(ad, account_info):
    """Build a CSV row for an ad"""
    row = {
        'Account': account_info['account_id'],
        'Action': 'Edit',
        'Campaign': ad['campaign_name'],
        'Ad group': ad['ad_group_name'],
        'Ad ID': ad['ad_id'],
        'Ad type': 'Responsive search ad',
        'Ad status': ad['status'],
    }

    # Add #Original headlines (current state)
    for i in range(1, 16):
        key = f'Headline {i}#Original'
        if i <= len(ad['current_headlines']):
            row[key] = ad['current_headlines'][i-1]
        else:
            row[key] = ''

    # Add new headlines
    for i in range(1, 16):
        key = f'Headline {i}'
        if i <= len(ad['new_headlines']):
            row[key] = ad['new_headlines'][i-1]
        else:
            row[key] = ''

    # Add #Original descriptions
    for i in range(1, 5):
        key = f'Description {i}#Original'
        if i <= len(ad['current_descriptions']):
            row[key] = ad['current_descriptions'][i-1]
        else:
            row[key] = ''

    # Add new descriptions
    for i in range(1, 5):
        key = f'Description {i}'
        if i <= len(ad['new_descriptions']):
            row[key] = ad['new_descriptions'][i-1]
        else:
            row[key] = ''

    row['Final URL'] = ad['final_url']

    return row

# Define CSV fieldnames
fieldnames = ['Account', 'Action', 'Campaign', 'Ad group', 'Ad ID', 'Ad type', 'Ad status']

# Headlines - #Original
for i in range(1, 16):
    fieldnames.append(f'Headline {i}#Original')

# Headlines - New
for i in range(1, 16):
    fieldnames.append(f'Headline {i}')

# Descriptions - #Original
for i in range(1, 5):
    fieldnames.append(f'Description {i}#Original')

# Descriptions - New
for i in range(1, 5):
    fieldnames.append(f'Description {i}')

fieldnames.append('Final URL')

# Process all regions
print("="*80)
print("Combining all regions into single CSV")
print("="*80)

all_rows = []
totals = {}

for region in ['USA', 'EUR', 'ROW']:
    print(f"\nProcessing {region}...")
    updates = load_region_updates(region)
    account_info = ACCOUNTS[region]

    for ad in updates:
        row = build_csv_row(ad, account_info)
        all_rows.append(row)

    totals[region] = len(updates)
    print(f"  ✓ Added {len(updates)} RSAs")

# Write combined CSV
output_file = '/Users/administrator/Documents/PetesBrain/clients/smythson/data/all_regions_rsa_updates.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\n{'='*80}")
print(f"COMPLETE")
print(f"{'='*80}")
print(f"\nCombined CSV created: {output_file}")
print(f"\nTotals:")
for region, count in totals.items():
    print(f"  {region}: {count} RSAs")
print(f"  TOTAL: {sum(totals.values())} RSAs")

print(f"\n{'='*80}")
print("Import Instructions:")
print(f"{'='*80}")
print("1. Open Google Ads Editor")
print("2. Load ALL Smythson accounts (USA, EUR, ROW)")
print("3. Account > Import > From file...")
print(f"4. Select: {output_file}")
print(f"5. Review (should show {sum(totals.values())} ads to be EDITED across all accounts)")
print("6. Process > Review > Post")
print("\n⚠️  The Account column will route each ad to the correct account")
print("⚠️  The #Original columns ensure ads are UPDATED, not duplicated")
