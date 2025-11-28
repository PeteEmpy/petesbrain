#!/usr/bin/env python3
"""
Universal RSA Update CSV Generator for Google Ads Editor

Generates CSV files using the #Original column method to UPDATE existing RSAs
while preserving their performance history.

Usage:
    python3 generate-rsa-update-csv.py --client smythson --input spreadsheet_data.json --output rsa_updates.csv

The input JSON should contain RSA data with current and new headline/description values.
Output CSV will be saved to the client's data/ folder.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

def generate_rsa_update_csv(client_name, input_file, output_file):
    """
    Generate Google Ads Editor CSV for RSA updates

    Args:
        client_name: Client folder name (e.g., 'smythson')
        input_file: Path to JSON file with RSA update data
        output_file: Name of output CSV file
    """

    # Determine client folder
    base_path = Path(__file__).parent.parent.parent
    client_path = base_path / "clients" / client_name / "data"

    if not client_path.exists():
        print(f"✗ Client folder not found: {client_path}")
        sys.exit(1)

    # Load input data
    with open(input_file, 'r') as f:
        data = json.load(f)

    output_path = client_path / output_file

    print(f"\n{'='*80}")
    print(f"Google Ads Editor RSA Update CSV Generator")
    print(f"{'='*80}")
    print(f"\nClient: {client_name}")
    print(f"Input: {input_file}")
    print(f"Output: {output_path}")
    print(f"RSAs to update: {len(data)}")

    # CSV columns for Google Ads Editor RSA import
    fieldnames = [
        'Action',
        'Campaign',
        'Ad group',
        'Ad ID',
        'Ad type',
        'Ad status',
        # Headlines - #Original columns for matching
        'Headline 1#Original', 'Headline 2#Original', 'Headline 3#Original',
        'Headline 4#Original', 'Headline 5#Original', 'Headline 6#Original',
        'Headline 7#Original', 'Headline 8#Original', 'Headline 9#Original',
        'Headline 10#Original', 'Headline 11#Original', 'Headline 12#Original',
        'Headline 13#Original', 'Headline 14#Original', 'Headline 15#Original',
        # Headlines - New values
        'Headline 1', 'Headline 2', 'Headline 3', 'Headline 4', 'Headline 5',
        'Headline 6', 'Headline 7', 'Headline 8', 'Headline 9', 'Headline 10',
        'Headline 11', 'Headline 12', 'Headline 13', 'Headline 14', 'Headline 15',
        # Descriptions - #Original columns
        'Description 1#Original', 'Description 2#Original',
        'Description 3#Original', 'Description 4#Original',
        # Descriptions - New values
        'Description 1', 'Description 2', 'Description 3', 'Description 4',
        # URL
        'Final URL'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rsa in data:
            row = {
                'Action': 'Edit',
                'Campaign': rsa['campaign_name'],
                'Ad group': rsa['ad_group_name'],
                'Ad ID': rsa['ad_id'],
                'Ad type': 'Responsive search ad',
                'Ad status': rsa.get('status', 'Enabled'),
                'Final URL': rsa.get('final_url', '')
            }

            # Add original headlines (for matching)
            for i, headline in enumerate(rsa['current_headlines'], 1):
                row[f'Headline {i}#Original'] = headline

            # Add new headlines (for update)
            for i, headline in enumerate(rsa['new_headlines'], 1):
                row[f'Headline {i}'] = headline

            # Add original descriptions (for matching)
            for i, desc in enumerate(rsa.get('current_descriptions', []), 1):
                row[f'Description {i}#Original'] = desc

            # Add new descriptions (for update)
            for i, desc in enumerate(rsa.get('new_descriptions', []), 1):
                row[f'Description {i}'] = desc

            writer.writerow(row)

    print(f"\n✓ CSV generated successfully")
    print(f"\n{'='*80}")
    print(f"Import Instructions:")
    print(f"{'='*80}")
    print(f"1. Open Google Ads Editor")
    print(f"2. Load the {client_name} account")
    print(f"3. Account > Import > From file...")
    print(f"4. Select: {output_path}")
    print(f"5. Review (should show {len(data)} ads to be EDITED)")
    print(f"6. Process > Review > Post")
    print(f"\n⚠️  The #Original columns ensure existing ads are UPDATED, not duplicated")

def main():
    parser = argparse.ArgumentParser(
        description='Generate RSA update CSV for Google Ads Editor'
    )
    parser.add_argument(
        '--client',
        required=True,
        help='Client name (e.g., smythson)'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input JSON file with RSA update data'
    )
    parser.add_argument(
        '--output',
        default='rsa_updates.csv',
        help='Output CSV filename (default: rsa_updates.csv)'
    )

    args = parser.parse_args()

    generate_rsa_update_csv(args.client, args.input, args.output)

if __name__ == "__main__":
    main()
