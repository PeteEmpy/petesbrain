#!/usr/bin/env python3
"""Fix RSA exports with proper Google Ads Editor column headers"""

import csv

def convert_to_editor_format(input_file, output_file):
    """Convert our format to Google Ads Editor's expected format"""

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
    return output_file

# Convert UK file
print("Converting UK export to Google Ads Editor format...")
uk_file = convert_to_editor_format(
    'rsa-uk-export-fixed-paused-20251215.csv',
    'rsa-uk-editor-format-20251215.csv'
)

# Check first few lines to verify format
print("\nFirst 2 lines of converted file:")
with open(uk_file, 'r') as f:
    for i, line in enumerate(f):
        if i < 2:
            # Show first 100 chars
            print(f"Line {i+1}: {line[:100]}...")
        else:
            break

print("\n🎯 Google Ads Editor format applied:")
print("  - Customer ID (not Account)")
print("  - Campaign (not Campaign Name)")
print("  - Ad group (not Ad Group Name)")
print("  - Headline 1-15 (not H1-H15)")
print("  - Description 1-4 (not D1-D4)")
print("  - Ad status = 'Enabled'")
print("  - Ad type = 'Responsive search ad'")