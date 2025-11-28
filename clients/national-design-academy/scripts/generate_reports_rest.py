#!/usr/bin/env python3
"""Generate Landing Page Reports using REST API directly"""

import json
import csv
import requests
import os
import sys

# Add MCP server path
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

# Set env vars
os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "1994728449"
date_from = "2025-09-01"
date_to = "2025-11-28"

print(f"📊 Generating Landing Page Reports for National Design Academy")
print(f"📅 Date Range: {date_from} to {date_to} (90 days)\n")

# Get headers with auth
headers = get_headers_with_auto_token()

# Step 1: Get Performance Max campaigns
print("Step 1: Fetching Performance Max campaigns...")

query_campaigns = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status
    FROM campaign
    WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
      AND campaign.status IN ('ENABLED', 'PAUSED')
"""

url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"
response = requests.post(url, headers=headers, json={'query': query_campaigns})

if not response.ok:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

campaigns_data = response.json()
pmax_campaigns = []

for row in campaigns_data.get('results', []):
    pmax_campaigns.append({
        'id': row['campaign']['id'],
        'name': row['campaign']['name'],
        'status': row['campaign']['status']
    })

print(f"✅ Found {len(pmax_campaigns)} Performance Max campaigns\n")

# Step 2: Get asset groups with metrics for each campaign
print("Step 2: Fetching asset groups with performance data...")
pmax_data = []

for campaign in pmax_campaigns:
    campaign_id = campaign['id']
    campaign_name = campaign['name']
    campaign_status = campaign['status']
    
    print(f"  Querying campaign: {campaign_name}")
    
    query_ag = f"""
        SELECT
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.final_urls,
            asset_group.status,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM asset_group
        WHERE campaign.id = {campaign_id}
          AND segments.date BETWEEN '{date_from}' AND '{date_to}'
    """
    
    response = requests.post(url, headers=headers, json={'query': query_ag})
    
    if not response.ok:
        print(f"    ⚠️  Error: {response.status_code}")
        continue
    
    ag_data = response.json()
    
    for row in ag_data.get('results', []):
        landing_pages = ', '.join(row['assetGroup'].get('finalUrls', [])) or 'N/A'
        
        pmax_data.append({
            'campaign_name': row['campaign']['name'],
            'campaign_status': campaign_status,
            'asset_group_name': row['assetGroup']['name'],
            'asset_group_status': row['assetGroup']['status'],
            'landing_pages': landing_pages,
            'impressions': int(row['metrics'].get('impressions', 0)),
            'clicks': int(row['metrics'].get('clicks', 0)),
            'conversions': float(row['metrics'].get('conversions', 0)),
            'conv_value': float(row['metrics'].get('conversionsValue', 0)),
            'cost': int(row['metrics'].get('costMicros', 0)) / 1_000_000
        })
    
    print(f"    ✓ Found {len(ag_data.get('results', []))} asset groups")

print(f"\n✅ Found {len(pmax_data)} total asset group records\n")

# Step 3: Write Report 2
print("Step 3: Writing Report 2 - Performance Max Landing Pages...")
report2_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report2-pmax-landing-pages-90d.csv'

with open(report2_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Campaign Name', 'Campaign Status', 'Asset Group Name', 'Asset Group Status',
        'Landing Page URL(s)', 'Impressions (90d)', 'Clicks (90d)', 'Conversions (90d)',
        'Conv Value (£)', 'Cost (£)', 'ROAS'
    ])
    
    for row in pmax_data:
        roas = row['conv_value'] / row['cost'] if row['cost'] > 0 else 0
        
        writer.writerow([
            row['campaign_name'],
            row['campaign_status'],
            row['asset_group_name'],
            row['asset_group_status'],
            row['landing_pages'],
            row['impressions'],
            row['clicks'],
            row['conversions'],
            f"£{row['conv_value']:.2f}",
            f"£{row['cost']:.2f}",
            f"{roas:.2f}"
        ])

print(f"✅ Report 2 saved: {report2_path}")
print(f"   {len(pmax_data)} rows written\n")

print("✅ Complete!")
