#!/usr/bin/env python3
"""Create export in EXACT Google Ads Editor format for RSA updates"""

import csv

def create_editor_exact_format():
    """Create a file that exactly matches Google Ads Editor's expected format"""

    # Read our current data
    with open('rsa-uk-fixed-escaping-20251215.csv', 'r') as f:
        reader = csv.DictReader(f)

        # Google Ads Editor EXACT format for RSA updates
        rows = []

        # Header - EXACT order and naming Google Ads Editor expects
        header = [
            'Customer ID',
            'Campaign',
            'Ad group',
            'Ad ID',
            'Status',
            'Ad type',
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
            'Final URL'
        ]

        rows.append(header)

        for row in reader:
            new_row = [
                row['Customer ID'],
                row['Campaign'],
                row['Ad group'],
                row['Ad ID'],
                'Enabled',  # Status
                'Responsive search ad',  # Ad type
            ]

            # Add headlines
            for i in range(1, 16):
                headline = row.get(f'Headline {i}', '')
                new_row.append(headline if headline else '')

            # Add descriptions
            for i in range(1, 5):
                desc = row.get(f'Description {i}', '')
                new_row.append(desc if desc else '')

            # Add Final URL
            new_row.append(row['Final URL'])

            rows.append(new_row)

    # Write the file
    with open('rsa-uk-editor-exact-20251215.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ Created rsa-uk-editor-exact-20251215.csv")
    print("\nFormat matches Google Ads Editor exactly:")
    print("  - Customer ID (not Account)")
    print("  - Campaign, Ad group, Ad ID")
    print("  - Status = Enabled")
    print("  - Ad type = Responsive search ad")
    print("  - Headlines 1-15, Descriptions 1-4, Final URL")
    print("  - No Action column (let Editor determine)")
    print("  - No extra columns")

    # Show first few ads for verification
    print("\nFirst 5 ads in file:")
    for i in range(1, min(6, len(rows))):
        print(f"  {i}. Ad {rows[i][3]} in {rows[i][1][:30]}")

create_editor_exact_format()

# Also create for other regions
print("\n" + "="*50)
print("Creating for other regions...")

for region, customer_id, input_file in [
    ('USA', '4941701449', 'rsa-usa-fixed-escaping-20251215.csv'),
    ('EUR', '7679616761', 'rsa-eur-fixed-escaping-20251215.csv'),
    ('ROW', '5556710725', 'rsa-row-fixed-escaping-20251215.csv')
]:
    try:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            row = next(reader)

            # Create single-row file for each region
            output = f'rsa-{region.lower()}-editor-exact-20251215.csv'
            with open(output, 'w', newline='', encoding='utf-8') as out:
                writer = csv.writer(out)

                # Header
                writer.writerow([
                    'Customer ID', 'Campaign', 'Ad group', 'Ad ID', 'Status', 'Ad type',
                    'Headline 1', 'Headline 2', 'Headline 3', 'Headline 4', 'Headline 5',
                    'Headline 6', 'Headline 7', 'Headline 8', 'Headline 9', 'Headline 10',
                    'Headline 11', 'Headline 12', 'Headline 13', 'Headline 14', 'Headline 15',
                    'Description 1', 'Description 2', 'Description 3', 'Description 4',
                    'Final URL'
                ])

                # Data row
                data = [
                    row['Customer ID'], row['Campaign'], row['Ad group'],
                    row['Ad ID'], 'Enabled', 'Responsive search ad'
                ]

                for i in range(1, 16):
                    data.append(row.get(f'Headline {i}', ''))

                for i in range(1, 5):
                    data.append(row.get(f'Description {i}', ''))

                data.append(row['Final URL'])

                writer.writerow(data)

            print(f"✅ {region}: {output}")
    except Exception as e:
        print(f"❌ {region}: {e}")

print("\n" + "="*50)
print("🎯 Use these EXACT format files:")
print("  - rsa-uk-editor-exact-20251215.csv")
print("  - rsa-usa-editor-exact-20251215.csv")
print("  - rsa-eur-editor-exact-20251215.csv")
print("  - rsa-row-editor-exact-20251215.csv")