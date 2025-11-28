#!/usr/bin/env python3
"""Generate Report 3: Search Campaign Landing Page Performance"""

import os
import sys
import csv
import requests

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "1994728449"
date_from = "2025-09-01"
date_to = "2025-11-28"

print(f"📊 Generating Report 3: Search Campaign Landing Pages")
print(f"📅 Date Range: {date_from} to {date_to} (90 days)\n")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

# Query for Search campaigns only
query = f"""
    SELECT
        campaign.name,
        ad_group.name,
        ad_group_ad.ad.final_urls,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.conversions,
        metrics.conversions_value,
        metrics.cost_micros
    FROM ad_group_ad
    WHERE campaign.advertising_channel_type = 'SEARCH'
      AND ad_group_ad.status = 'ENABLED'
      AND ad_group.status = 'ENABLED'
      AND campaign.status IN ('ENABLED', 'PAUSED')
      AND segments.date BETWEEN '{date_from}' AND '{date_to}'
"""

print("Querying Search campaign data...")
response = requests.post(url, headers=headers, json={'query': query})

if not response.ok:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
results = data.get('results', [])

print(f"✅ Found {len(results)} ad records from Search campaigns\n")

# Write report
print("Writing Report 3...")
report_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report3-search-landing-pages-90d.csv'

with open(report_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Campaign Name', 'Ad Group Name', 'Landing Page URL', 'Impressions',
        'Clicks', 'CTR', 'Conversions', 'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
    ])
    
    for row in results:
        campaign_name = row['campaign']['name']
        ad_group_name = row['adGroup']['name']
        
        # Get final URLs (may be multiple)
        final_urls = row.get('adGroupAd', {}).get('ad', {}).get('finalUrls', [])
        landing_page = final_urls[0] if final_urls else 'N/A'
        
        metrics = row['metrics']
        impressions = int(metrics.get('impressions', 0))
        clicks = int(metrics.get('clicks', 0))
        conversions = float(metrics.get('conversions', 0))
        conv_value = float(metrics.get('conversionsValue', 0))
        cost = int(metrics.get('costMicros', 0)) / 1_000_000
        
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
        roas = conv_value / cost if cost > 0 else 0
        
        writer.writerow([
            campaign_name,
            ad_group_name,
            landing_page,
            impressions,
            clicks,
            f"{ctr:.2f}%",
            conversions,
            f"{conv_rate:.2f}%",
            f"£{cost:.2f}",
            f"£{conv_value:.2f}",
            f"{roas:.2f}"
        ])

print(f"✅ Report 3 saved: {report_path}")
print(f"   {len(results)} rows written\n")
print("✅ Complete!")
