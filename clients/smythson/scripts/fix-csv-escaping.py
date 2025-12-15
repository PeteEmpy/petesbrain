#!/usr/bin/env python3
"""Fix CSV escaping issues for Google Ads Editor"""

import csv

def fix_csv_escaping(input_file, output_file):
    """Re-write CSV with proper escaping and no #original markers"""

    rows = []

    with open(input_file, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            # Replace #original with empty string
            cleaned_row = []
            for cell in row:
                if cell == '#original':
                    cleaned_row.append('')
                else:
                    # Remove any line breaks and extra spaces
                    cleaned = cell.replace('\n', ' ').replace('\r', ' ')
                    # Ensure no double spaces
                    cleaned = ' '.join(cleaned.split())
                    cleaned_row.append(cleaned)

            rows.append(cleaned_row)

    # Write with Excel dialect (more strict escaping)
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerows(rows)

    print(f"✅ Created {output_file} with proper escaping")

    # Verify column count
    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data_row = next(reader)
        print(f"   Header: {len(header)} columns")
        print(f"   Data: {len(data_row)} columns")
        print(f"   Final URL: {data_row[25] if len(data_row) > 25 else 'MISSING'}")

# Process all editor format files
files = [
    ('rsa-uk-editor-format-20251215.csv', 'rsa-uk-fixed-escaping-20251215.csv'),
    ('rsa-usa-editor-format-20251215.csv', 'rsa-usa-fixed-escaping-20251215.csv'),
    ('rsa-eur-editor-format-20251215.csv', 'rsa-eur-fixed-escaping-20251215.csv'),
    ('rsa-row-editor-format-20251215.csv', 'rsa-row-fixed-escaping-20251215.csv')
]

print("Fixing CSV escaping for Google Ads Editor...")
print("=" * 50)

for input_file, output_file in files:
    region = input_file.split('-')[1].upper()
    print(f"\n{region}:")
    fix_csv_escaping(input_file, output_file)

print("\n" + "=" * 50)
print("🎯 Fixed files ready for import!")
print("\nUSE THESE FILES:")
for _, output in files:
    print(f"  - {output}")

print("\n📝 Changes made:")
print("  - Removed all #original markers")
print("  - Fixed line breaks and escaping")
print("  - Used Excel CSV dialect for compatibility")