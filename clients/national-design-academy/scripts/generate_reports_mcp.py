#!/usr/bin/env python3
"""Generate Landing Page Reports using MCP tools directly"""

import json
import csv
import subprocess

customer_id = "7511832413"
date_from = "2025-09-01"
date_to = "2025-11-28"

print(f"📊 Generating Landing Page Reports for National Design Academy")
print(f"📅 Date Range: {date_from} to {date_to} (90 days)\n")

# Step 1: Get all Performance Max campaigns
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

# Use MCP tool via subprocess
result = subprocess.run(
    ['claude', 'mcp', 'call', 'google-ads', 'run_gaql', '--', 
     json.dumps({
         'customer_id': customer_id,
         'query': query_campaigns
     })],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"❌ Error: {result.stderr}")
    exit(1)

response = json.loads(result.stdout)
campaigns_data = json.loads(response['content'][0]['text'])

pmax_campaigns = []
for row in campaigns_data['results']:
    pmax_campaigns.append({
        'id': row['campaign']['id'],
        'name': row['campaign']['name'],
        'status': row['campaign']['status']
    })

print(f"✅ Found {len(pmax_campaigns)} Performance Max campaigns\n")

# Step 2: For each campaign, get asset groups with metrics
print("Step 2: Fetching asset groups with performance data...")
pmax_data = []

for campaign in pmax_campaigns:
    campaign_id = campaign['id']
    campaign_name = campaign['name']
    campaign_status = campaign['status']
    
    print(f"  Querying campaign: {campaign_name} (ID: {campaign_id})")
    
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
    
    result = subprocess.run(
        ['claude', 'mcp', 'call', 'google-ads', 'run_gaql', '--',
         json.dumps({
             'customer_id': customer_id,
             'query': query_ag
         })],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"    ⚠️  Error querying campaign: {result.stderr}")
        continue
    
    try:
        ag_response = json.loads(result.stdout)
        ag_data = json.loads(ag_response['content'][0]['text'])
        
        for row in ag_data['results']:
            landing_pages = ', '.join(row['assetGroup']['finalUrls']) if 'finalUrls' in row['assetGroup'] else 'N/A'
            
            pmax_data.append({
                'campaign_name': row['campaign']['name'],
                'campaign_status': campaign_status,
                'asset_group_name': row['assetGroup']['name'],
                'asset_group_status': row['assetGroup']['status'],
                'landing_pages': landing_pages,
                'impressions': int(row['metrics']['impressions']),
                'clicks': int(row['metrics']['clicks']),
                'conversions': float(row['metrics']['conversions']),
                'conv_value': float(row['metrics']['conversionsValue']),
                'cost': int(row['metrics']['costMicros']) / 1_000_000
            })
            
        print(f"    ✓ Found {len(ag_data['results'])} asset groups")
    except Exception as e:
        print(f"    ⚠️  Error parsing response: {str(e)}")
        continue

print(f"\n✅ Found {len(pmax_data)} total asset group records with metrics\n")

# Step 3: Write Report 2 - Performance Max Landing Pages
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
