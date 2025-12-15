#!/usr/bin/env python3
"""Convert all RSA exports to proper Google Ads Editor format"""

import csv
import os

def convert_to_editor_format(input_file, output_file):
    """Convert our format to Google Ads Editor's expected format"""

    if not os.path.exists(input_file):
        print(f"⚠️  {input_file} not found")
        return None

    rows = []

    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)

        # Google Ads Editor expects these exact column names
        new_header = [
            'Customer ID',
            'Campaign',
            'Ad group',
            'Ad status',
            'Ad type',
            'Ad ID',
            'Headline 1', 'Headline 2', 'Headline 3', 'Headline 4', 'Headline 5',
            'Headline 6', 'Headline 7', 'Headline 8', 'Headline 9', 'Headline 10',
            'Headline 11', 'Headline 12', 'Headline 13', 'Headline 14', 'Headline 15',
            'Description 1', 'Description 2', 'Description 3', 'Description 4',
            'Final URL'
        ]

        rows.append(new_header)

        for row in reader:
            # Map our columns to Google Ads Editor columns
            new_row = [
                row.get('Account', ''),  # Customer ID
                row.get('Campaign Name', ''),  # Campaign
                row.get('Ad Group Name', ''),  # Ad group
                'Enabled',  # Ad status (always Enabled for RSAs we're updating)
                'Responsive search ad',  # Ad type
                row.get('Ad ID', ''),  # Ad ID
            ]

            # Add headlines (H1-H15 -> Headline 1-15)
            for i in range(1, 16):
                h_val = row.get(f'H{i}', '')
                # Don't include #original in Editor format - use empty instead
                if h_val == '#original':
                    h_val = ''
                new_row.append(h_val)

            # Add descriptions (D1-D4 -> Description 1-4)
            for i in range(1, 5):
                d_val = row.get(f'D{i}', '')
                # Don't include #original in Editor format - use empty instead
                if d_val == '#original':
                    d_val = ''
                new_row.append(d_val)

            # Add Final URL
            new_row.append(row.get('Final URL', ''))

            rows.append(new_row)

    # Write the new format
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Created {output_file}")

    # Count non-empty rows
    data_rows = len(rows) - 1  # Exclude header
    print(f"   {data_rows} RSAs ready for import")

    return output_file

# Convert all regional files
files_to_convert = [
    ('rsa-uk-export-fixed-paused-20251215.csv', 'rsa-uk-editor-format-20251215.csv'),
    ('rsa-usa-export-final-20251215.csv', 'rsa-usa-editor-format-20251215.csv'),
    ('rsa-eur-export-corrected-20251215.csv', 'rsa-eur-editor-format-20251215.csv'),
    ('rsa-row-export-corrected-20251215.csv', 'rsa-row-editor-format-20251215.csv')
]

print("Converting all RSA exports to Google Ads Editor format...")
print("=" * 50)

for input_file, output_file in files_to_convert:
    region = output_file.split('-')[1].upper()
    print(f"\n{region} Export:")
    convert_to_editor_format(input_file, output_file)

print("\n" + "=" * 50)
print("🎯 All files converted to Google Ads Editor format!")
print("\nUSE THESE FILES FOR IMPORT:")
print("  - rsa-uk-editor-format-20251215.csv")
print("  - rsa-usa-editor-format-20251215.csv")
print("  - rsa-eur-editor-format-20251215.csv")
print("  - rsa-row-editor-format-20251215.csv")
print("\nColumn format now matches Google Ads Editor exactly:")
print("  Customer ID | Campaign | Ad group | Ad status | Ad type | Ad ID | Headlines 1-15 | Descriptions 1-4 | Final URL")