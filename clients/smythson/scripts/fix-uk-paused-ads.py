#!/usr/bin/env python3
"""Fix UK RSA export - remove #original for paused ads and only send actual values"""

import csv

def fix_uk_export():
    """Remove #original markers - only send actual values for paused ads"""

    # Problem lines with PAUSED ads
    paused_lines = [7, 8, 9, 10, 11, 12, 26]

    rows = []

    with open('rsa-uk-export-final-20251215.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Find indices
        h1_idx = header.index('H1')
        d1_idx = header.index('D1')
        final_url_idx = header.index('Final URL')

        # For Google Ads Editor, we'll remove unnecessary columns for cleaner import
        # Keep only filled headlines and descriptions, remove #original
        rows.append(header)

        for i, row in enumerate(reader, start=2):
            if not row:
                continue

            if i in paused_lines:
                # For paused ads, remove all #original markers
                # Google Ads Editor will keep existing values for fields we don't specify
                new_row = []
                for j, val in enumerate(row):
                    if val == '#original':
                        new_row.append('')  # Empty field = keep existing
                    else:
                        new_row.append(val)
                rows.append(new_row)
            else:
                # Keep other rows as-is
                rows.append(row)

    # Write the fixed file
    output_file = 'rsa-uk-export-fixed-paused-20251215.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Created {output_file}")
    print(f"   Fixed lines {paused_lines} - removed #original markers")
    print(f"   Empty fields will keep existing values in Google Ads Editor")

    return output_file

# Alternative approach: Create separate file for paused ads
def create_enable_paused_ads():
    """Create a file to first enable the paused ads"""

    paused_ad_ids = [
        ('784228048465', '13813052579', '137137030741'),  # Line 7
        ('784228048444', '13813052579', '137137030781'),  # Line 8
        ('784228048456', '13813052579', '137137030941'),  # Line 9
        ('784228048459', '13813052579', '121861436342'),  # Line 10
        ('784228048468', '13813052579', '137137031021'),  # Line 11
        ('784228048450', '13813052579', '137137031181'),  # Line 12
        ('784157389885', '23215754148', '191738856607'),  # Line 26
    ]

    with open('rsa-uk-enable-paused-ads-20251215.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Account', 'Action', 'Type', 'Campaign ID', 'Ad Group ID', 'Ad ID', 'Status'])

        for ad_id, campaign_id, ad_group_id in paused_ad_ids:
            writer.writerow(['8573235780', 'Edit', 'Ad', campaign_id, ad_group_id, ad_id, 'Enabled'])

    print("\n✅ Created rsa-uk-enable-paused-ads-20251215.csv")
    print("   This file will ENABLE the 7 paused ads")
    print("\nSuggested import process:")
    print("1. First import: rsa-uk-enable-paused-ads-20251215.csv (enables the paused ads)")
    print("2. Then import: rsa-uk-export-fixed-paused-20251215.csv (updates the text)")

# Run both approaches
print("Fixing UK export for paused ads...\n")
print("Option 1: Removing #original markers")
print("=" * 50)
fix_uk_export()

print("\n" + "=" * 50)
print("Option 2: Creating separate file to enable ads first")
print("=" * 50)
create_enable_paused_ads()

print("\n🎯 Two approaches available:")
print("A) Try rsa-uk-export-fixed-paused-20251215.csv directly")
print("B) First enable ads with rsa-uk-enable-paused-ads-20251215.csv")
print("   Then import rsa-uk-export-fixed-paused-20251215.csv")