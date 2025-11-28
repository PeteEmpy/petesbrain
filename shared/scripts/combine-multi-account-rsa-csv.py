#!/usr/bin/env python3
"""
Universal multi-account RSA CSV combiner

Combines multiple region/account RSA update JSONs into a single CSV
with Account column for Google Ads Editor import.

Usage:
    python3 combine-multi-account-rsa-csv.py \\
        --config account_config.json \\
        --inputs usa_updates.json eur_updates.json row_updates.json \\
        --output all_regions_rsa_updates.csv

Account config format:
{
    "USA": {"customer_id": "7808690871", "account_id": "780-869-0871", "account_name": "Client USA"},
    "EUR": {"customer_id": "7679616761", "account_id": "767-961-6761", "account_name": "Client EUR"}
}

Input JSON format (from RSA update builder):
[
    {
        "campaign_name": "Campaign Name",
        "ad_group_name": "Ad Group Name",
        "ad_id": "123456789",
        "status": "ENABLED",
        "current_headlines": ["H1", "H2", ...],
        "new_headlines": ["H1", "H2", ..., "New H12"],
        "current_descriptions": ["D1", "D2", "D3", "D4"],
        "new_descriptions": ["D1", "D2", "D3", "D4"],
        "final_url": "https://example.com"
    }
]
"""

import json
import csv
import argparse
import sys
from pathlib import Path

# Add utils to path for account ID formatter
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))
from google_ads_formatters import format_customer_id_with_dashes, validate_customer_id


def load_account_config(config_path):
    """Load account configuration from JSON file"""
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Validate and format account IDs
    for region, info in config.items():
        if 'customer_id' not in info:
            raise ValueError(f"Missing customer_id for {region}")

        # Validate customer ID
        if not validate_customer_id(info['customer_id']):
            raise ValueError(f"Invalid customer_id for {region}: {info['customer_id']}")

        # Generate account_id if not provided
        if 'account_id' not in info:
            info['account_id'] = format_customer_id_with_dashes(info['customer_id'])

    return config


def load_region_updates(json_path):
    """Load update JSON for a region"""
    with open(json_path, 'r') as f:
        return json.load(f)


def build_csv_row(ad, account_info):
    """Build a CSV row for an ad with #Original columns"""
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
    parser = argparse.ArgumentParser(description='Combine multi-account RSA updates into single CSV')
    parser.add_argument('--config', required=True, help='Account configuration JSON file')
    parser.add_argument('--inputs', nargs='+', required=True, help='Input JSON files (one per region/account)')
    parser.add_argument('--output', required=True, help='Output CSV file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Load account config
    if args.verbose:
        print("Loading account configuration...")
    config = load_account_config(args.config)

    # Detect region labels from input filenames
    # e.g., "usa_rsa_updates.json" → "USA"
    region_mapping = {}
    for input_path in args.inputs:
        filename = Path(input_path).stem.lower()
        for region in config.keys():
            if region.lower() in filename:
                region_mapping[input_path] = region
                break
        if input_path not in region_mapping:
            print(f"Warning: Could not detect region for {input_path}, skipping...")

    if not region_mapping:
        print("Error: No input files matched configured regions")
        sys.exit(1)

    # Process all regions
    print("=" * 80)
    print("Combining RSA updates into single multi-account CSV")
    print("=" * 80)

    all_rows = []
    totals = {}

    for input_path, region in region_mapping.items():
        if args.verbose:
            print(f"\nProcessing {region} ({input_path})...")

        updates = load_region_updates(input_path)
        account_info = config[region]

        for ad in updates:
            row = build_csv_row(ad, account_info)
            all_rows.append(row)

        totals[region] = len(updates)
        print(f"  ✓ {region}: {len(updates)} RSAs ({account_info['account_id']})")

    # Write combined CSV
    fieldnames = build_fieldnames()

    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n{'=' * 80}")
    print(f"COMPLETE")
    print(f"{'=' * 80}")
    print(f"\nCombined CSV created: {args.output}")
    print(f"\nTotals:")
    for region, count in totals.items():
        print(f"  {region}: {count} RSAs")
    print(f"  TOTAL: {sum(totals.values())} RSAs")

    print(f"\n{'=' * 80}")
    print("Import Instructions:")
    print(f"{'=' * 80}")
    print("1. Open Google Ads Editor")
    print(f"2. Load ALL accounts: {', '.join(config.keys())}")
    print("3. Account > Import > From file...")
    print(f"4. Select: {args.output}")
    print(f"5. Review (should show {sum(totals.values())} ads to be EDITED across all accounts)")
    print("6. Process > Review > Post")
    print("\n⚠️  The Account column will route each ad to the correct account")
    print("⚠️  The #Original columns ensure ads are UPDATED, not duplicated")
    print("⚠️  Test on 1-2 ads first to verify format")


if __name__ == '__main__':
    main()
