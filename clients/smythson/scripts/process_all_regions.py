#!/usr/bin/env python3
"""Process USA, EUR, and ROW RSA updates - fetch current state, build updates, generate CSVs"""

import sys
import os
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from oauth.google_auth import execute_gaql
import json

# Account configurations
ACCOUNTS = {
    'USA': {'customer_id': '7808690871', 'manager_id': '2569949686'},
    'EUR': {'customer_id': '7679616761', 'manager_id': '2569949686'},
    'ROW': {'customer_id': '5556710725', 'manager_id': '2569949686'}
}

# Ad IDs from spreadsheet
AD_IDS = {
    'USA': [
        "784198246551", "784523200052", "784539336374", "784539336377", "784448339422",
        "784198246689", "784198246692", "784198246704", "784198246680", "784198246710",
        "784198246554", "784198246701", "784198246557", "784198246707", "784198246683",
        "784198246698", "784198246686", "784198246695", "784326430958", "784326430967",
        "784326430979", "784326430970", "784326430985", "784326430988", "784326430961",
        "784326430982", "784326431000", "784326430991", "784326430973", "784326430994",
        "784326430964", "784523323658", "784326430997", "784326430955", "784326430976",
        "781000775209", "781000644181", "781000644178", "781000644172", "781000644175",
        "781000644169"
    ],
    'EUR': [
        "785121413211", "785121413223", "784327102022", "784941557977", "732880000699",
        "732880000696", "784327102043", "784327102025", "784327102028", "784327102031",
        "784941557980", "773539871911", "784327102034", "775856922188"
    ],
    'ROW': [
        "784326640550", "784326640553", "773497251588", "784326640556"
    ]
}

def fetch_region_rsas(region, customer_id, manager_id, ad_ids):
    """Fetch current state for a region"""
    print(f"\n{'='*80}")
    print(f"Processing {region}")
    print(f"{'='*80}")
    print(f"Fetching {len(ad_ids)} RSAs...")

    ad_ids_str = ",".join(ad_ids)

    query = f"""
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
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

    print(f"✓ Fetched {len(ads)} RSAs")

    # Build current state
    current_state = []
    for ad in ads:
        campaign_name = ad['campaign']['name']
        ad_group_name = ad['adGroup']['name']
        ad_id = ad['adGroupAd']['ad']['id']
        status = ad['adGroupAd']['status']

        rsa = ad['adGroupAd']['ad']['responsiveSearchAd']
        headlines = [h['text'] for h in rsa['headlines']]
        descriptions = [d['text'] for d in rsa['descriptions']]
        final_urls = ad['adGroupAd']['ad']['finalUrls']

        current_state.append({
            'campaign_name': campaign_name,
            'ad_group_name': ad_group_name,
            'ad_id': ad_id,
            'status': status,
            'current_headlines': headlines,
            'current_descriptions': descriptions,
            'final_url': final_urls[0] if final_urls else ''
        })

    return current_state

def build_updates(region, current_state, new_h8_text="Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"):
    """Build update JSON with H8 changes"""
    print(f"\nBuilding updates for {region}...")

    updates = []
    changed_count = 0
    already_has_countdown = 0

    for ad in current_state:
        current_headlines = ad['current_headlines']

        # Build new headlines (replace H8)
        new_headlines = current_headlines.copy()

        # Check if already has countdown
        if len(current_headlines) >= 8 and current_headlines[7] == new_h8_text:
            already_has_countdown += 1
            # Still include it in the CSV but with no actual change
            updates.append({
                'campaign_name': ad['campaign_name'],
                'ad_group_name': ad['ad_group_name'],
                'ad_id': ad['ad_id'],
                'status': ad['status'],
                'current_headlines': current_headlines,
                'new_headlines': current_headlines,  # No change
                'current_descriptions': ad['current_descriptions'],
                'new_descriptions': ad['current_descriptions'],
                'final_url': ad['final_url']
            })
            continue

        # Replace H8 if it exists
        if len(new_headlines) >= 8:
            old_h8 = new_headlines[7]
            new_headlines[7] = new_h8_text
            changed_count += 1
            print(f"  ✓ {ad['ad_id']}: {ad['campaign_name']}")
            print(f"     Old H8: {old_h8}")
            print(f"     New H8: {new_h8_text}")
        else:
            print(f"  ⚠️  {ad['ad_id']} has only {len(new_headlines)} headlines (< 8)")
            continue

        # Build update entry
        updates.append({
            'campaign_name': ad['campaign_name'],
            'ad_group_name': ad['ad_group_name'],
            'ad_id': ad['ad_id'],
            'status': ad['status'],
            'current_headlines': current_headlines,
            'new_headlines': new_headlines,
            'current_descriptions': ad['current_descriptions'],
            'new_descriptions': ad['current_descriptions'],
            'final_url': ad['final_url']
        })

    print(f"\nSummary:")
    print(f"  Total RSAs: {len(current_state)}")
    print(f"  With changes: {changed_count}")
    print(f"  Already have countdown: {already_has_countdown}")

    return updates

# Process each region
for region, config in ACCOUNTS.items():
    ad_ids = AD_IDS[region]

    # Fetch current state
    current_state = fetch_region_rsas(
        region,
        config['customer_id'],
        config['manager_id'],
        ad_ids
    )

    # Save current state
    current_state_path = f'/Users/administrator/Documents/PetesBrain/clients/smythson/data/{region.lower()}_rsa_current_state.json'
    with open(current_state_path, 'w') as f:
        json.dump(current_state, f, indent=2)

    print(f"✓ Saved current state to {current_state_path}")

    # Build updates
    updates = build_updates(region, current_state)

    # Save updates
    updates_path = f'/Users/administrator/Documents/PetesBrain/clients/smythson/data/{region.lower()}_rsa_updates_full.json'
    with open(updates_path, 'w') as f:
        json.dump(updates, f, indent=2)

    print(f"✓ Saved updates to {updates_path}")

print(f"\n{'='*80}")
print(f"ALL REGIONS COMPLETE")
print(f"{'='*80}")
print(f"\nNext steps:")
for region in ['usa', 'eur', 'row']:
    print(f"\npython3 shared/scripts/generate-rsa-update-csv.py \\")
    print(f"  --client smythson \\")
    print(f"  --input clients/smythson/data/{region}_rsa_updates_full.json \\")
    print(f"  --output {region}_rsa_updates.csv")
