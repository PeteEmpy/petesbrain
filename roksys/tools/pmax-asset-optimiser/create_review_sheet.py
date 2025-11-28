#!/usr/bin/env python3
"""
Reformat replacement candidates into review sheet format
Matches Devonshire Hotels format: one row per asset with 3 options side-by-side
"""

import csv
from pathlib import Path
from collections import defaultdict

base_dir = Path(__file__).parent

# Input and output paths
input_csv = base_dir / 'output' / 'replacement-candidates.csv'
output_csv = base_dir / 'output' / 'tree2mydoor-review-sheet.csv'

def main():
    print("=" * 80)
    print("CREATING REVIEW SHEET")
    print("=" * 80)
    print()

    # Read all replacements
    print(f"📄 Reading: {input_csv.name}")
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        replacements = list(reader)

    print(f"✅ Loaded {len(replacements)} replacement rows")

    # Group by original asset (3 options per asset)
    assets = defaultdict(list)
    for row in replacements:
        key = (
            row.get('Campaign_ID', ''),
            row.get('Campaign', ''),
            row.get('Asset_Group_ID', ''),
            row.get('Asset_Group', ''),
            row['Original_Text'],
            row['Asset_Type'],
            row['Impressions'],
            row['CTR'],
            row['Conv_Rate'],
            row['Flag_Reason'],
            row['Priority']
        )
        assets[key].append(row['Replacement_Text'])

    print(f"✅ Grouped into {len(assets)} unique assets")
    print()

    # Create review sheet format
    print(f"📝 Creating review sheet format...")
    review_rows = []

    for (campaign_id, campaign, asset_group_id, asset_group, orig_text, asset_type, impressions, ctr, conv_rate, flag_reason, priority), options in assets.items():
        # Ensure we have exactly 3 options (pad with empty if needed)
        while len(options) < 3:
            options.append("")

        review_row = {
            'Campaign': campaign,
            'Asset Group': asset_group,
            'Priority': priority,
            'Asset Type': asset_type,
            'Current Text': orig_text,
            'Impressions': impressions,
            'CTR': ctr,
            'Conv Rate': conv_rate,
            'Issue': flag_reason,
            'Option 1': options[0] if len(options) > 0 else '',
            'Option 2': options[1] if len(options) > 1 else '',
            'Option 3': options[2] if len(options) > 2 else '',
            'Selected Option (1/2/3 or blank to skip)': '',  # User fills this in
            'Notes': ''  # User fills this in
        }
        review_rows.append(review_row)

    # Sort by priority (HIGH first)
    review_rows.sort(key=lambda x: (0 if x['Priority'] == 'HIGH' else 1, -int(x['Impressions'].replace(',', ''))))

    print(f"✅ Created {len(review_rows)} review rows")

    # Write output
    print(f"💾 Writing: {output_csv.name}")
    fieldnames = [
        'Campaign', 'Asset Group', 'Priority', 'Asset Type', 'Current Text', 'Impressions', 'CTR', 'Conv Rate', 'Issue',
        'Option 1', 'Option 2', 'Option 3', 'Selected Option (1/2/3 or blank to skip)', 'Notes'
    ]

    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(review_rows)

    print()
    print("=" * 80)
    print("✅ REVIEW SHEET CREATED")
    print("=" * 80)
    print()
    print(f"📊 Summary:")
    print(f"   - Total assets: {len(review_rows)}")
    print(f"   - HIGH priority: {sum(1 for r in review_rows if r['Priority'] == 'HIGH')}")
    print(f"   - MEDIUM priority: {sum(1 for r in review_rows if r['Priority'] == 'MEDIUM')}")
    print()
    print(f"📍 Output: {output_csv}")
    print()
    print("Next step: Upload to Google Sheets using automated_sheets_upload.py")
    print()

if __name__ == "__main__":
    main()
