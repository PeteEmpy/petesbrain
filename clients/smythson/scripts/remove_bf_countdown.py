#!/usr/bin/env python3
"""
Generate CSV to remove Black Friday countdown from Smythson RSAs

This script reads the existing *_rsa_updates_full.json files (which ADD countdown)
and creates a new CSV that REMOVES the countdown instead.

Used for Dec 2nd post-Black Friday cleanup.
"""

import json
import csv
from pathlib import Path

# Account mappings
ACCOUNTS = {
    'UK': {'customer_id': '8573235780', 'account_id': '857-323-5780', 'account_name': 'Smythson UK'},
    'USA': {'customer_id': '7808690871', 'account_id': '780-869-0871', 'account_name': 'Smythson USA'},
    'EUR': {'customer_id': '7679616761', 'account_id': '767-961-6761', 'account_name': 'Smythson EUR'},
    'ROW': {'customer_id': '5556710725', 'account_id': '555-671-0725', 'account_name': 'Smythson ROW'}
}

# Countdown text pattern to remove
COUNTDOWN_PATTERN = "Black Friday Ends in {COUNTDOWN("

def load_region_updates(region):
    """Load update JSON for a region"""
    data_dir = Path(__file__).parent.parent / 'data'
    input_file = data_dir / f'{region.lower()}_rsa_updates_full.json'

    if not input_file.exists():
        print(f"⚠️  Warning: {input_file} not found, skipping {region}")
        return []

    with open(input_file, 'r') as f:
        return json.load(f)

def remove_countdown_from_headlines(headlines):
    """Remove countdown headline from list"""
    return [h for h in headlines if COUNTDOWN_PATTERN not in h]

def build_csv_row(ad, account_info):
    """Build a CSV row for an ad with countdown removed"""

    # New headlines = current headlines WITHOUT countdown
    new_headlines = remove_countdown_from_headlines(ad['new_headlines'])

    # Current headlines = what's in Google Ads NOW (includes countdown)
    current_headlines = ad['new_headlines']  # This is the current state with countdown

    row = {
        'Account': account_info['account_id'],
        'Action': 'Edit',
        'Campaign': ad['campaign_name'],
        'Ad group': ad['ad_group_name'],
        'Ad ID': ad['ad_id'],
        'Ad type': 'Responsive search ad',
        'Ad status': ad['status'],
    }

    # Add #Original headlines (current state WITH countdown)
    for i in range(1, 16):
        key = f'Headline {i}#Original'
        if i <= len(current_headlines):
            row[key] = current_headlines[i-1]
        else:
            row[key] = ''

    # Add new headlines (WITHOUT countdown)
    for i in range(1, 16):
        key = f'Headline {i}'
        if i <= len(new_headlines):
            row[key] = new_headlines[i-1]
        else:
            row[key] = ''

    # Add #Original descriptions (unchanged)
    for i in range(1, 5):
        key = f'Description {i}#Original'
        if i <= len(ad['current_descriptions']):
            row[key] = ad['current_descriptions'][i-1]
        else:
            row[key] = ''

    # Add new descriptions (unchanged)
    for i in range(1, 5):
        key = f'Description {i}'
        if i <= len(ad['new_descriptions']):
            row[key] = ad['new_descriptions'][i-1]
        else:
            row[key] = ''

    row['Final URL'] = ad['final_url']

    return row

def build_fieldnames():
    """Build CSV fieldnames in Google Ads Editor format"""
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

    return fieldnames

def main():
    print("=" * 80)
    print("Generating Black Friday Countdown Removal CSV")
    print("=" * 80)

    all_rows = []
    totals = {}

    for region in ['UK', 'USA', 'EUR', 'ROW']:
        print(f"\nProcessing {region}...")
        updates = load_region_updates(region)

        if not updates:
            continue

        account_info = ACCOUNTS[region]

        for ad in updates:
            # Only process ads that have countdown
            if any(COUNTDOWN_PATTERN in h for h in ad['new_headlines']):
                row = build_csv_row(ad, account_info)
                all_rows.append(row)

        totals[region] = len([ad for ad in updates if any(COUNTDOWN_PATTERN in h for h in ad['new_headlines'])])
        print(f"  ✓ Added {totals[region]} RSAs with countdown to remove")

    # Write combined CSV
    output_file = Path(__file__).parent.parent / 'data' / 'remove_bf_countdown_all_regions.csv'
    fieldnames = build_fieldnames()

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n{'=' * 80}")
    print(f"COMPLETE")
    print(f"{'=' * 80}")
    print(f"\nCountdown removal CSV created: {output_file}")
    print(f"\nTotals:")
    for region, count in totals.items():
        print(f"  {region}: {count} RSAs")
    print(f"  TOTAL: {sum(totals.values())} RSAs")

    print(f"\n{'=' * 80}")
    print("Import Instructions:")
    print(f"{'=' * 80}")
    print("1. Open Google Ads Editor")
    print(f"2. Load ALL Smythson accounts (UK, USA, EUR, ROW)")
    print("3. Account > Import > From file...")
    print(f"4. Select: {output_file}")
    print(f"5. Review (should show {sum(totals.values())} ads to be EDITED)")
    print("6. Process > Review > Post")
    print("\n⚠️  The Account column will route each ad to the correct account")
    print("⚠️  This will REMOVE the countdown headline while preserving all others")
    print("⚠️  Use this on December 2nd to remove Black Friday countdowns")

if __name__ == '__main__':
    main()
