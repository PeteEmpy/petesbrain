#!/usr/bin/env python3
"""
Generate Landing Page Performance Reports for National Design Academy
Using individual campaign queries instead of bulk queries
"""

import os
import sys
import csv
from datetime import datetime, timedelta

# Add MCP server path for imports
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

# Set environment variables BEFORE import
os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import execute_gaql, format_customer_id

customer_id = "7511832413"

# Date range: Last 90 days (Sept 1 - Nov 28, 2025)
date_to = "2025-11-28"
date_from = "2025-09-01"

print(f"📊 Generating Landing Page Reports for National Design Academy")
print(f"📅 Date Range: {date_from} to {date_to} (90 days)")
print(f"🔑 Customer ID: {customer_id}\n")

# Step 1: Get all Performance Max campaigns
print("Step 1: Fetching Performance Max campaigns...")
query_campaigns = """
    SELECT
        campaign.id,
        campaign.name
    FROM campaign
    WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
      AND campaign.status IN ('ENABLED', 'PAUSED')
"""

response_campaigns = execute_gaql(customer_id, query_campaigns)

pmax_campaigns = []
for row in response_campaigns['results']:
    pmax_campaigns.append({
        'id': row['campaign']['id'],
        'name': row['campaign']['name']
    })

print(f"✅ Found {len(pmax_campaigns)} Performance Max campaigns\n")

# Step 2: For each campaign, get asset groups with metrics
print("Step 2: Fetching asset groups with performance data...")
pmax_data = []

for campaign in pmax_campaigns:
    campaign_id = campaign['id']
    campaign_name = campaign['name']
    
    print(f"  Querying campaign: {campaign_name} (ID: {campaign_id})")
    
    # Query asset groups for this specific campaign
    query_ag = f"""
        SELECT
            campaign.id,
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
    
    try:
        response_ag = execute_gaql(customer_id, query_ag)

        for row in response_ag['results']:
            # Get landing pages
            landing_pages = ', '.join(row['assetGroup']['finalUrls']) if 'finalUrls' in row['assetGroup'] else 'N/A'

            pmax_data.append({
                'campaign_name': row['campaign']['name'],
                'campaign_status': 'ENABLED',  # We can add status tracking if needed
                'asset_group_name': row['assetGroup']['name'],
                'asset_group_status': row['assetGroup']['status'],
                'landing_pages': landing_pages,
                'impressions': row['metrics']['impressions'],
                'clicks': row['metrics']['clicks'],
                'conversions': row['metrics']['conversions'],
                'conv_value': row['metrics']['conversionsValue'],
                'cost': int(row['metrics']['costMicros']) / 1_000_000
            })

    except Exception as ex:
        print(f"    ⚠️  Error querying campaign {campaign_name}: {str(ex)}")
        continue

print(f"✅ Found {len(pmax_data)} asset group records with metrics\n")

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
