#!/usr/bin/env python3
"""Update EUR and ROW RSA exports with real Ad IDs from Google Ads"""

import csv

# EUR: Found Ad ID 732987221519 from campaign "SMY | EUR | AT | Search | Brand..."
# in ad group "AT_Brand_Exact"
eur_updates = {
    'account': '7679616761',  # Correct EUR account ID
    'campaign_id': '22228334811',
    'campaign_name': 'SMY | EUR | AT | Search | Brand Max Conv Value No Target Port 16/6',
    'ad_group_id': '175399205416',
    'ad_group_name': 'AT_Brand_Exact',
    'ad_id': '732987221519'  # Real Ad ID from Google Ads
}

# ROW: Found Ad ID 652080574559 from campaign "ROW - AE - brand"
# in ad group "ROW - Brand - Of Bond Street"
row_updates = {
    'account': '5556710725',  # Correct ROW account ID
    'campaign_id': '19865545148',
    'campaign_name': 'ROW - AE - brand',
    'ad_group_id': '146504794999',
    'ad_group_name': 'ROW - Brand - Of Bond Street',
    'ad_id': '652080574559'  # Real Ad ID from Google Ads
}

def update_file(input_file, output_file, updates):
    """Update RSA export with real IDs"""

    rows = []

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        # Find column indices
        account_idx = header.index('Account')
        action_idx = header.index('Action')
        campaign_id_idx = header.index('Campaign ID')
        campaign_name_idx = header.index('Campaign Name')
        ad_group_id_idx = header.index('Ad Group ID')
        ad_group_name_idx = header.index('Ad Group Name')
        ad_id_idx = header.index('Ad ID')

        for row in reader:
            if not row:
                continue

            # Update with real IDs
            row[account_idx] = updates['account']
            row[action_idx] = 'Edit'  # Now we can edit because these are real ads
            row[campaign_id_idx] = updates['campaign_id']
            row[campaign_name_idx] = updates['campaign_name']
            row[ad_group_id_idx] = updates['ad_group_id']
            row[ad_group_name_idx] = updates['ad_group_name']
            row[ad_id_idx] = updates['ad_id']

            # Replace empty values with #original (for Edit action)
            for i, val in enumerate(row):
                if val == '' and i > ad_id_idx:
                    row[i] = '#original'

            rows.append(row)

    # Write the fixed file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Updated {output_file}")
    print(f"   Account: {updates['account']}")
    print(f"   Campaign: {updates['campaign_name']} ({updates['campaign_id']})")
    print(f"   Ad Group: {updates['ad_group_name']} ({updates['ad_group_id']})")
    print(f"   Ad ID: {updates['ad_id']}")
    print(f"   Action: Edit (updating existing ad)")

# Update EUR export
print("Updating EUR export with real Ad ID:")
update_file(
    'rsa-eur-export-final-20251215.csv',
    'rsa-eur-export-corrected-20251215.csv',
    eur_updates
)

print("\nUpdating ROW export with real Ad ID:")
update_file(
    'rsa-row-export-final-20251215.csv',
    'rsa-row-export-corrected-20251215.csv',
    row_updates
)

print("\n🎯 Both EUR and ROW exports now have real Ad IDs for EDITING existing ads")
print("Files ready for import:")
print("  - rsa-eur-export-corrected-20251215.csv")
print("  - rsa-row-export-corrected-20251215.csv")