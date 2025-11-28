#!/usr/bin/env python3
"""Generate Report 1: Landing Page Statistics (90 days)"""

import os
import sys
import csv
import requests
from collections import defaultdict

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "1994728449"
date_from = "2025-09-01"
date_to = "2025-11-28"

print(f"📊 Generating Report 1: Landing Page Statistics")
print(f"📅 Date Range: {date_from} to {date_to} (90 days)\n")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

# Use landing_page_view resource
query = f"""
    SELECT
        landing_page_view.unexpanded_final_url,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.conversions,
        metrics.conversions_value,
        metrics.cost_micros
    FROM landing_page_view
    WHERE segments.date BETWEEN '{date_from}' AND '{date_to}'
"""

print("Querying landing page data...")
response = requests.post(url, headers=headers, json={'query': query})

if not response.ok:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
results = data.get('results', [])

print(f"✅ Found {len(results)} landing page records\n")

# Aggregate by landing page
landing_pages = defaultdict(lambda: {
    'impressions': 0,
    'clicks': 0,
    'conversions': 0,
    'conv_value': 0,
    'cost': 0
})

for row in results:
    url_path = row['landingPageView']['unexpandedFinalUrl']
    metrics = row['metrics']
    
    landing_pages[url_path]['impressions'] += int(metrics.get('impressions', 0))
    landing_pages[url_path]['clicks'] += int(metrics.get('clicks', 0))
    landing_pages[url_path]['conversions'] += float(metrics.get('conversions', 0))
    landing_pages[url_path]['conv_value'] += float(metrics.get('conversionsValue', 0))
    landing_pages[url_path]['cost'] += int(metrics.get('costMicros', 0)) / 1_000_000

# Write report
print("Writing Report 1...")
report_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report1-landing-page-statistics-90d.csv'

with open(report_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Landing Page URL', 'Impressions', 'Clicks', 'CTR', 'Conversions',
        'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
    ])
    
    # Sort by conversions descending
    sorted_pages = sorted(landing_pages.items(), key=lambda x: x[1]['conversions'], reverse=True)
    
    for url_path, stats in sorted_pages:
        ctr = (stats['clicks'] / stats['impressions'] * 100) if stats['impressions'] > 0 else 0
        conv_rate = (stats['conversions'] / stats['clicks'] * 100) if stats['clicks'] > 0 else 0
        roas = stats['conv_value'] / stats['cost'] if stats['cost'] > 0 else 0
        
        writer.writerow([
            url_path,
            stats['impressions'],
            stats['clicks'],
            f"{ctr:.2f}%",
            stats['conversions'],
            f"{conv_rate:.2f}%",
            f"£{stats['cost']:.2f}",
            f"£{stats['conv_value']:.2f}",
            f"{roas:.2f}"
        ])

print(f"✅ Report 1 saved: {report_path}")
print(f"   {len(landing_pages)} unique landing pages\n")
print("✅ Complete!")
