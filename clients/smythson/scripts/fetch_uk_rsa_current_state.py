#!/usr/bin/env python3
"""Fetch current state of all UK RSAs from Google Ads for #Original columns"""

import sys
import os
import json
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server')

from oauth.google_auth import execute_gaql

customer_id = "8573235780"
manager_id = "2569949686"

# All UK RSA ad IDs from spreadsheet
ad_ids = [
    "784157361259", "784408654524", "784228048462", "784228048447", "784228048453",
    "784228048465", "784228048444", "784228048456", "784228048459", "784228048468",
    "784228048450", "784197388692", "780966363483", "780374687964", "780374687982",
    "780374687985", "780374687991", "780374687979", "780374687976", "780374687967",
    "780374687973", "780374687970", "780374687988", "780374687994", "784157389885",
    "773478848874", "773478848871"
]

print(f"\nFetching current state of {len(ad_ids)} UK RSAs from Google Ads...")

# Build query for all ads
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

print(f"✓ Fetched {len(ads)} RSAs\n")

# Build JSON data
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

    print(f"  {campaign_name} > {ad_group_name}")
    print(f"    Ad ID: {ad_id}, Headlines: {len(headlines)}, Descriptions: {len(descriptions)}")

# Save to JSON
output_path = '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/uk_rsa_current_state.json'
with open(output_path, 'w') as f:
    json.dump(current_state, f, indent=2)

print(f"\n✓ Saved current state to: {output_path}")
print(f"\nNext: Merge with spreadsheet changes to create full update JSON")
