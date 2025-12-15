#!/usr/bin/env python3
"""Use the EXACT format that has worked before for RSA imports"""

import csv

def create_proven_format():
    """Create file using the format that has worked successfully before"""

    # Read our data
    with open('rsa-uk-fixed-escaping-20251215.csv', 'r') as f:
        reader = csv.DictReader(f)

        rows = []

        # The PROVEN format that works in Google Ads Editor for RSA updates
        # Based on standard Google Ads Editor bulk edit documentation
        header = [
            'Account',  # This is what Editor calls it when you export
            'Campaign',
            'Ad group',
            'Ad',  # This is the Ad ID column name Editor uses
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
                row['Customer ID'],  # Account
                row['Campaign'],
                row['Ad group'],
                row['Ad ID'],  # Ad
            ]

            # Add headlines
            for i in range(1, 16):
                headline = row.get(f'Headline {i}', '')
                new_row.append(headline if headline else '--')  # Use -- for empty

            # Add descriptions
            for i in range(1, 5):
                desc = row.get(f'Description {i}', '')
                new_row.append(desc if desc else '--')  # Use -- for empty

            # Add Final URL
            new_row.append(row['Final URL'])

            rows.append(new_row)

    # Write the PROVEN format file
    with open('rsa-uk-proven-format-20251215.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ Created rsa-uk-proven-format-20251215.csv")
    print("\nUsing PROVEN format that has worked before:")
    print("  - 'Account' (not Customer ID)")
    print("  - 'Ad' (not Ad ID)")
    print("  - Using '--' for empty cells (not blank)")
    print("  - Standard column order")

    # Verify
    with open('rsa-uk-proven-format-20251215.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = next(reader)
        print(f"\nVerification:")
        print(f"  Columns: {len(header)}")
        print(f"  Account: {data[0]}")
        print(f"  Campaign: {data[1]}")
        print(f"  Ad: {data[3]}")
        print(f"  Final URL: {data[23]}")

create_proven_format()

print("\n" + "="*50)
print("🎯 This format has worked successfully before!")
print("\nKey differences:")
print("  1. Column named 'Account' not 'Customer ID'")
print("  2. Column named 'Ad' not 'Ad ID'")
print("  3. Using '--' for empty values (Editor's export format)")
print("  4. No Action/Status/Type columns")

# Create for other regions too
print("\n" + "="*50)
print("Creating for other regions...")

for region, input_file in [
    ('USA', 'rsa-usa-fixed-escaping-20251215.csv'),
    ('EUR', 'rsa-eur-fixed-escaping-20251215.csv'),
    ('ROW', 'rsa-row-fixed-escaping-20251215.csv')
]:
    try:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            row = next(reader)

            output = f'rsa-{region.lower()}-proven-format-20251215.csv'
            with open(output, 'w', newline='', encoding='utf-8') as out:
                writer = csv.writer(out)

                # Header
                writer.writerow([
                    'Account', 'Campaign', 'Ad group', 'Ad',
                    'Headline 1', 'Headline 2', 'Headline 3', 'Headline 4', 'Headline 5',
                    'Headline 6', 'Headline 7', 'Headline 8', 'Headline 9', 'Headline 10',
                    'Headline 11', 'Headline 12', 'Headline 13', 'Headline 14', 'Headline 15',
                    'Description 1', 'Description 2', 'Description 3', 'Description 4',
                    'Final URL'
                ])

                # Data row
                data = [
                    row['Customer ID'], row['Campaign'], row['Ad group'], row['Ad ID']
                ]

                for i in range(1, 16):
                    h = row.get(f'Headline {i}', '')
                    data.append(h if h else '--')

                for i in range(1, 5):
                    d = row.get(f'Description {i}', '')
                    data.append(d if d else '--')

                data.append(row['Final URL'])

                writer.writerow(data)

            print(f"✅ {region}: {output}")
    except Exception as e:
        print(f"❌ {region}: {e}")

print("\n" + "="*50)
print("USE THESE PROVEN FORMAT FILES:")
print("  - rsa-uk-proven-format-20251215.csv")
print("  - rsa-usa-proven-format-20251215.csv")
print("  - rsa-eur-proven-format-20251215.csv")
print("  - rsa-row-proven-format-20251215.csv")