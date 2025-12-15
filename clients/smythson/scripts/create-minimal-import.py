#!/usr/bin/env python3
"""Create minimal import file with only essential columns for RSA updates"""

import csv

def create_minimal_import():
    """Create minimal file with only columns needed to update RSAs"""

    # Read our data
    with open('rsa-uk-editor-exact-20251215.csv', 'r') as f:
        reader = csv.DictReader(f)

        rows = []

        # Minimal header - ONLY what's needed to identify and update RSAs
        header = [
            'Customer ID',
            'Ad ID',
            'Headline 1',
            'Headline 2',
            'Headline 3',
            'Description 1',
            'Description 2'
        ]

        rows.append(header)

        # Process first 5 ads as test
        for i, row in enumerate(reader):
            if i >= 5:
                break

            new_row = [
                row['Customer ID'],
                row['Ad ID'],
                'Smythson of Bond Street™',  # Simple static text for testing
                'British heritage since 1887',
                'Shop luxury leather pieces',
                'Make the ordinary extraordinary',
                'Discover the perfect gift'
            ]

            rows.append(new_row)

    # Write minimal file
    with open('test-minimal-import.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ Created test-minimal-import.csv")
    print("\nMinimal format with:")
    print("  - Customer ID")
    print("  - Ad ID")
    print("  - 3 Headlines")
    print("  - 2 Descriptions")
    print("  - NO campaign/ad group names")
    print("  - NO status/type columns")
    print("  - NO Final URL")
    print("\nTesting with first 5 ads only")

create_minimal_import()

print("\n" + "="*50)
print("If this minimal import works, we know Editor can find the ads.")
print("We can then add columns back one by one to find the problem.")