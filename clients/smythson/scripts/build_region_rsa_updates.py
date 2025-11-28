#!/usr/bin/env python3
"""Build RSA updates by comparing Google Ads current state with spreadsheet desired state"""

import sys
import os
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from oauth.google_auth import execute_gaql
import json

# Account configurations with spreadsheet data
ACCOUNTS = {
    'USA': {
        'customer_id': '7808690871',
        'manager_id': '2569949686',
        'spreadsheet_file': '/Users/administrator/Documents/PetesBrain/clients/smythson/data/usa_spreadsheet_data.json'
    },
    'EUR': {
        'customer_id': '7679616761',
        'manager_id': '2569949686',
        'spreadsheet_file': '/Users/administrator/Documents/PetesBrain/clients/smythson/data/eur_spreadsheet_data.json'
    },
    'ROW': {
        'customer_id': '5556710725',
        'manager_id': '2569949686',
        'spreadsheet_file': '/Users/administrator/Documents/PetesBrain/clients/smythson/data/row_spreadsheet_data.json'
    }
}

def fetch_spreadsheet_data(spreadsheet_file):
    """Load spreadsheet data from JSON file"""
    print(f"  Loading spreadsheet data from {spreadsheet_file}...")

    with open(spreadsheet_file, 'r') as f:
        rows = json.load(f)

    # Parse into structured data
    spreadsheet_rsas = {}
    for row in rows:
        if len(row) < 5:
            continue

        ad_id = row[4]  # Column E

        # Extract headlines (columns F-T = H1-H15)
        headlines = []
        for i in range(5, 20):  # Columns 5-19 (F-T)
            if i < len(row) and row[i].strip():
                headlines.append(row[i].strip())

        # Extract descriptions (columns U-X = D1-D4)
        descriptions = []
        for i in range(20, 24):  # Columns 20-23 (U-X)
            if i < len(row) and row[i].strip():
                descriptions.append(row[i].strip())

        # Final URL (column Y)
        final_url = row[24].strip() if len(row) > 24 else ''

        spreadsheet_rsas[ad_id] = {
            'headlines': headlines,
            'descriptions': descriptions,
            'final_url': final_url
        }

    print(f"  ✓ Found {len(spreadsheet_rsas)} RSAs in spreadsheet")
    return spreadsheet_rsas

def fetch_google_ads_state(region, customer_id, manager_id, ad_ids):
    """Fetch current state from Google Ads"""
    print(f"  Fetching current state from Google Ads...")

    ad_ids_str = ",".join(ad_ids)

    query = f"""
    SELECT
        campaign.name,
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.status,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions,
        ad_group_ad.ad.final_urls
    FROM ad_group_ad
    WHERE
        ad_group_ad.ad.id IN ({ad_ids_str})
        AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
    ORDER BY campaign.name, ad_group.name
    """

    result = execute_gaql(customer_id, query, manager_id)
    ads = result.get('results', [])

    print(f"  ✓ Fetched {len(ads)} RSAs from Google Ads")

    # Build current state lookup
    current_state = {}
    for ad in ads:
        ad_id = ad['adGroupAd']['ad']['id']
        rsa = ad['adGroupAd']['ad']['responsiveSearchAd']

        current_state[ad_id] = {
            'campaign_name': ad['campaign']['name'],
            'ad_group_name': ad['adGroup']['name'],
            'status': ad['adGroupAd']['status'],
            'headlines': [h['text'] for h in rsa['headlines']],
            'descriptions': [d['text'] for d in rsa['descriptions']],
            'final_url': ad['adGroupAd']['ad']['finalUrls'][0] if ad['adGroupAd']['ad']['finalUrls'] else ''
        }

    return current_state

def compare_and_build_updates(region, current_state, spreadsheet_data):
    """Compare current vs desired state and build updates"""
    print(f"\n  Comparing current state vs spreadsheet...")

    updates = []
    changed_count = 0
    no_change_count = 0
    not_in_spreadsheet = 0

    for ad_id, current in current_state.items():
        if ad_id not in spreadsheet_data:
            print(f"  ⚠️  {ad_id} not in spreadsheet - skipping")
            not_in_spreadsheet += 1
            continue

        desired = spreadsheet_data[ad_id]

        # Check for differences
        headlines_changed = current['headlines'] != desired['headlines']
        descriptions_changed = current['descriptions'] != desired['descriptions']
        url_changed = current['final_url'] != desired['final_url']

        if headlines_changed or descriptions_changed or url_changed:
            changed_count += 1
            print(f"\n  ✓ {ad_id}: {current['campaign_name']}")

            if headlines_changed:
                # Find which headlines changed
                for i, (curr_h, new_h) in enumerate(zip(current['headlines'], desired['headlines']), 1):
                    if curr_h != new_h:
                        print(f"     H{i}: '{curr_h}' → '{new_h}'")

            if descriptions_changed:
                print(f"     Descriptions changed")

            if url_changed:
                print(f"     URL: '{current['final_url']}' → '{desired['final_url']}'")

            updates.append({
                'campaign_name': current['campaign_name'],
                'ad_group_name': current['ad_group_name'],
                'ad_id': ad_id,
                'status': current['status'],
                'current_headlines': current['headlines'],
                'new_headlines': desired['headlines'],
                'current_descriptions': current['descriptions'],
                'new_descriptions': desired['descriptions'],
                'final_url': desired['final_url']
            })
        else:
            no_change_count += 1

    print(f"\n  Summary:")
    print(f"    Total RSAs: {len(current_state)}")
    print(f"    With changes: {changed_count}")
    print(f"    No changes: {no_change_count}")
    print(f"    Not in spreadsheet: {not_in_spreadsheet}")

    return updates

# Process each region
print("="*80)
print("Building RSA updates from spreadsheet data")
print("="*80)

for region, config in ACCOUNTS.items():
    print(f"\n{'='*80}")
    print(f"Processing {region}")
    print(f"{'='*80}")

    # Fetch spreadsheet data
    spreadsheet_data = fetch_spreadsheet_data(config['sheet_name'])

    # Get ad IDs from spreadsheet
    ad_ids = list(spreadsheet_data.keys())

    # Fetch current Google Ads state
    current_state = fetch_google_ads_state(
        region,
        config['customer_id'],
        config['manager_id'],
        ad_ids
    )

    # Save current state
    current_state_list = [
        {
            'ad_id': ad_id,
            **data
        }
        for ad_id, data in current_state.items()
    ]

    current_state_path = f'/Users/administrator/Documents/PetesBrain/clients/smythson/data/{region.lower()}_rsa_current_state.json'
    with open(current_state_path, 'w') as f:
        json.dump(current_state_list, f, indent=2)

    print(f"\n  ✓ Saved current state to {current_state_path}")

    # Compare and build updates
    updates = compare_and_build_updates(region, current_state, spreadsheet_data)

    # Save updates
    updates_path = f'/Users/administrator/Documents/PetesBrain/clients/smythson/data/{region.lower()}_rsa_updates_full.json'
    with open(updates_path, 'w') as f:
        json.dump(updates, f, indent=2)

    print(f"  ✓ Saved {len(updates)} updates to {updates_path}")

print(f"\n{'='*80}")
print(f"ALL REGIONS COMPLETE")
print(f"{'='*80}")
print(f"\nNext steps:")
for region in ['usa', 'eur', 'row']:
    print(f"\npython3 shared/scripts/generate-rsa-update-csv.py \\")
    print(f"  --client smythson \\")
    print(f"  --input clients/smythson/data/{region}_rsa_updates_full.json \\")
    print(f"  --output {region}_rsa_updates.csv")
