#!/usr/bin/env python3
"""Rename ad group in Google Ads"""

import os
import sys
import requests

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "1994728449"

print("🔍 Finding 'Interior Design University' ad group...")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

# Find the ad group
query = """
    SELECT
        ad_group.id,
        ad_group.name,
        campaign.id,
        campaign.name
    FROM ad_group
    WHERE ad_group.name = 'interior design university'
      AND campaign.name = 'NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8'
"""

response = requests.post(url, headers=headers, json={'query': query})

if not response.ok:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
results = data.get('results', [])

if not results:
    print("❌ Ad group 'interior design university' not found")
    exit(1)

ad_group = results[0]
ad_group_id = ad_group['adGroup']['id']
ad_group_name = ad_group['adGroup']['name']
campaign_name = ad_group['campaign']['name']

print(f"✓ Found ad group:")
print(f"  ID: {ad_group_id}")
print(f"  Current Name: {ad_group_name}")
print(f"  Campaign: {campaign_name}")
print()

# Rename the ad group
print("✏️  Renaming to 'Interior Design University Degree'...")

mutation_url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/adGroups:mutate"

payload = {
    "operations": [{
        "update": {
            "resourceName": f"customers/{customer_id}/adGroups/{ad_group_id}",
            "name": "Interior Design University Degree"
        },
        "updateMask": "name"
    }]
}

response = requests.post(mutation_url, headers=headers, json=payload)

if not response.ok:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    exit(1)

result = response.json()
print("✅ Ad group renamed successfully!")
print(f"   Old Name: interior design university")
print(f"   New Name: Interior Design University Degree")
print()
