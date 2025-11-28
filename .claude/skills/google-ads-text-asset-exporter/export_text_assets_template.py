#!/usr/bin/env python3
"""
Export Smythson UK and US gifting PMAX text assets to Google Sheet for marketing review
"""

from google.ads.googleads.client import GoogleAdsClient
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json
from collections import defaultdict

# Initialize Google Ads client
ads_client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')
ga_service = ads_client.get_service('GoogleAdsService')

# Target campaigns (gifting-related only)
SMYTHSON_UK_ID = '8573235780'
SMYTHSON_US_ID = '7808690871'

UK_CAMPAIGNS = [
    '22845468179',  # SMY | UK | P Max | H&S
    '23021472678',  # SMY | UK | P Max | H&S - Men's Briefcases
    '23233714033',  # SMY | UK | P Max | H&S Christmas Gifting
]

def get_text_assets(customer_id, campaign_ids):
    """Get text assets for specific campaigns"""
    # OPTIMIZATION: Use single query with IN clause instead of looping
    # This reduces API calls from N campaigns to 1 call = much faster
    campaign_ids_str = ', '.join(campaign_ids)

    query = f"""
        SELECT
            campaign.name,
            campaign.id,
            asset_group.name,
            asset_group.id,
            asset_group_asset.field_type,
            asset.text_asset.text
        FROM asset_group_asset
        WHERE
            campaign.id IN ({campaign_ids_str})
            AND asset_group.status = 'ENABLED'
            AND asset_group_asset.status = 'ENABLED'
            AND asset.type = 'TEXT'
        ORDER BY campaign.name, asset_group.name, asset_group_asset.field_type
    """

    response = ga_service.search(customer_id=customer_id, query=query)
    all_rows = list(response)

    # Organize by asset group
    asset_groups = defaultdict(lambda: {
        'campaign': '',
        'asset_group': '',
        'headlines': [],
        'long_headlines': [],
        'descriptions': []
    })

    for row in all_rows:
        ag_id = str(row.asset_group.id)
        field_type = row.asset_group_asset.field_type.name
        text = row.asset.text_asset.text

        asset_groups[ag_id]['campaign'] = row.campaign.name
        asset_groups[ag_id]['asset_group'] = row.asset_group.name

        if field_type == 'HEADLINE':
            asset_groups[ag_id]['headlines'].append(text)
        elif field_type == 'LONG_HEADLINE':
            asset_groups[ag_id]['long_headlines'].append(text)
        elif field_type == 'DESCRIPTION':
            asset_groups[ag_id]['descriptions'].append(text)

    return asset_groups

print("Fetching UK text assets...")
uk_assets = get_text_assets(SMYTHSON_UK_ID, UK_CAMPAIGNS)

print(f"Found {len(uk_assets)} UK asset groups")

# Get US campaigns
print("\nFetching US campaigns...")
query = """
    SELECT campaign.name, campaign.id
    FROM campaign
    WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
    AND campaign.status = 'ENABLED'
"""
response = ga_service.search(customer_id=SMYTHSON_US_ID, query=query)
us_campaigns = [str(row.campaign.id) for row in response
                if any(term in row.campaign.name.lower() for term in ['gift', 'h&s', 'h & s', 'hero', 'hns', 'christmas'])]

print(f"Found {len(us_campaigns)} US gifting campaigns")

if us_campaigns:
    print("Fetching US text assets...")
    us_assets = get_text_assets(SMYTHSON_US_ID, us_campaigns)
    print(f"Found {len(us_assets)} US asset groups")
else:
    us_assets = {}

# Build Google Sheets data
rows = [['Market', 'Campaign', 'Asset Group', 'Type', 'Text', 'Approval Status', 'Comments']]

# Add UK assets
for ag_id, data in sorted(uk_assets.items(), key=lambda x: (x[1]['campaign'], x[1]['asset_group'])):
    # Headlines
    for i, headline in enumerate(data['headlines'], 1):
        rows.append(['UK', data['campaign'], data['asset_group'], f'Headline {i}', headline, '', ''])

    # Long headlines
    for i, long_headline in enumerate(data['long_headlines'], 1):
        rows.append(['UK', data['campaign'], data['asset_group'], f'Long Headline {i}', long_headline, '', ''])

    # Descriptions
    for i, desc in enumerate(data['descriptions'], 1):
        rows.append(['UK', data['campaign'], data['asset_group'], f'Description {i}', desc, '', ''])

    # Blank row separator
    rows.append(['', '', '', '', '', '', ''])

# Add US assets
for ag_id, data in sorted(us_assets.items(), key=lambda x: (x[1]['campaign'], x[1]['asset_group'])):
    # Headlines
    for i, headline in enumerate(data['headlines'], 1):
        rows.append(['US', data['campaign'], data['asset_group'], f'Headline {i}', headline, '', ''])

    # Long headlines
    for i, long_headline in enumerate(data['long_headlines'], 1):
        rows.append(['US', data['campaign'], data['asset_group'], f'Long Headline {i}', long_headline, '', ''])

    # Descriptions
    for i, desc in enumerate(data['descriptions'], 1):
        rows.append(['US', data['campaign'], data['asset_group'], f'Description {i}', desc, '', ''])

    # Blank row separator
    rows.append(['', '', '', '', '', '', ''])

# Save data to JSON for processing
output_file = '/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/gifting_text_assets_data.json'
output_data = {
    'rows': rows,
    'uk_count': len(uk_assets),
    'us_count': len(us_assets)
}

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"\n✓ Data saved to: {output_file}")
print(f"\nTotal asset groups exported:")
print(f"  UK: {len(uk_assets)}")
print(f"  US: {len(us_assets)}")
print(f"  Total rows: {len(rows)}")
