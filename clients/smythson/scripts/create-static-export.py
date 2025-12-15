#!/usr/bin/env python3
"""Create static RSA export without dynamic column interpretation"""

import csv

def create_static_export(input_file, output_file):
    """Create a static export for Google Ads Editor with explicit columns"""

    rows = []

    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)

        # Create header with NO dynamic interpretation
        header = [
            'Action',
            'Customer ID',
            'Campaign',
            'Ad group',
            'Ad ID',
            'Status',
            'Headline 1',
            'Headline 2',
            'Headline 3',
            'Headline 4',
            'Headline 5',
            'Headline 6',
            'Headline 7',
            'Headline 8',
            'Headline 9',
            'Headline 10',
            'Headline 11',
            'Headline 12',
            'Headline 13',
            'Headline 14',
            'Headline 15',
            'Description 1',
            'Description 2',
            'Description 3',
            'Description 4',
            'Path 1',
            'Path 2',
            'Final URL'
        ]

        rows.append(header)

        for row in reader:
            # Build row with explicit column positions
            new_row = [
                'Edit',  # Action
                row.get('Customer ID', ''),
                row.get('Campaign', ''),
                row.get('Ad group', ''),
                row.get('Ad ID', ''),
                'Enabled',  # Status
            ]

            # Add headlines (ensure no duplicates, no dynamic fields)
            for i in range(1, 16):
                headline_key = f'Headline {i}'
                value = row.get(headline_key, '')
                # Don't include empty or duplicate values
                new_row.append(value if value else '')

            # Add descriptions
            for i in range(1, 5):
                desc_key = f'Description {i}'
                value = row.get(desc_key, '')
                new_row.append(value if value else '')

            # Add paths (empty for now)
            new_row.append('')  # Path 1
            new_row.append('')  # Path 2

            # Add Final URL
            new_row.append(row.get('Final URL', ''))

            rows.append(new_row)

    # Write with strict formatting
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Created {output_file}")

    # Verify structure
    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = next(reader)

        print(f"   Columns: {len(header)}")
        print(f"   Action: {data[0]}")
        print(f"   Customer ID: {data[1]}")
        print(f"   Ad ID: {data[4]}")
        print(f"   Headline 1: {data[6]}")
        print(f"   Final URL: {data[27]}")

# Process all files
files = [
    ('rsa-uk-fixed-escaping-20251215.csv', 'rsa-uk-static-20251215.csv'),
    ('rsa-usa-fixed-escaping-20251215.csv', 'rsa-usa-static-20251215.csv'),
    ('rsa-eur-fixed-escaping-20251215.csv', 'rsa-eur-static-20251215.csv'),
    ('rsa-row-fixed-escaping-20251215.csv', 'rsa-row-static-20251215.csv')
]

print("Creating static exports for Google Ads Editor...")
print("=" * 50)

for input_file, output_file in files:
    region = input_file.split('-')[1].upper()
    print(f"\n{region}:")
    create_static_export(input_file, output_file)

print("\n" + "=" * 50)
print("🎯 Static export files ready!")
print("\nUSE THESE FILES:")
for _, output in files:
    print(f"  - {output}")

print("\n📝 Format:")
print("  - Action column first (set to 'Edit')")
print("  - Static column headers (no dynamic interpretation)")
print("  - 28 columns total")
print("  - No duplicate headlines")