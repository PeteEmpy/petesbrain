#!/usr/bin/env python3
"""Create ASCII-only version removing special characters"""

import csv
import unicodedata

def clean_text(text):
    """Remove or replace non-ASCII characters"""
    if not text:
        return text

    # Replace known special characters
    text = text.replace('™', '')  # Remove trademark
    text = text.replace('£', 'GBP ')  # Replace pound symbol
    text = text.replace('–', '-')  # Replace en-dash
    text = text.replace('—', '-')  # Replace em-dash
    text = text.replace(''', "'")  # Replace smart quote
    text = text.replace(''', "'")  # Replace smart quote
    text = text.replace('"', '"')  # Replace smart quote
    text = text.replace('"', '"')  # Replace smart quote

    # Remove any remaining non-ASCII
    cleaned = ''.join(char if ord(char) < 128 else '' for char in text)

    return cleaned

def create_ascii_only():
    """Create ASCII-only version of the export"""

    with open('rsa-uk-clean-20251215.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        rows = []

        for row in reader:
            clean_row = [clean_text(cell) for cell in row]
            rows.append(clean_row)

    # Write ASCII-only version
    with open('rsa-uk-ascii-20251215.csv', 'w', newline='', encoding='ascii') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ Created rsa-uk-ascii-20251215.csv")

    # Verify it's ASCII-only
    with open('rsa-uk-ascii-20251215.csv', 'rb') as f:
        content = f.read()
        non_ascii = [b for b in content if b > 127]

        if non_ascii:
            print(f"⚠️  Still has {len(non_ascii)} non-ASCII bytes")
        else:
            print("✅ Confirmed: 100% ASCII")
            print(f"   File size: {len(content)} bytes")

create_ascii_only()

# Create for other regions
print("\n" + "="*50)
print("Creating ASCII versions for other regions...")

for region in ['usa', 'eur', 'row']:
    input_file = f'rsa-{region}-clean-20251215.csv'
    output_file = f'rsa-{region}-ascii-20251215.csv'

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            rows = []
            for row in reader:
                clean_row = [clean_text(cell) for cell in row]
                rows.append(clean_row)

        with open(output_file, 'w', newline='', encoding='ascii') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"✅ {region.upper()}: {output_file}")
    except Exception as e:
        print(f"❌ {region.upper()}: {e}")

print("\n" + "="*50)
print("🎯 ASCII-ONLY FILES (should not hang Editor):")
print("  - rsa-uk-ascii-20251215.csv")
print("  - rsa-usa-ascii-20251215.csv")
print("  - rsa-eur-ascii-20251215.csv")
print("  - rsa-row-ascii-20251215.csv")
print("\nChanges made:")
print("  - Removed ™ symbol from 'Smythson of Bond Street'")
print("  - Replaced £ with 'GBP'")
print("  - Removed all other non-ASCII characters")