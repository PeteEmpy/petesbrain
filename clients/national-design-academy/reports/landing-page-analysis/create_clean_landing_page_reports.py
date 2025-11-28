#!/usr/bin/env python3
"""
Generate Clean Landing Page Reports
- Remove URL parameters (utm_*, etc.)
- Filter out paused/removed campaigns
- Aggregate by base URL
"""

import os
import sys
import csv
import requests
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
from datetime import datetime

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

def clean_url(url):
    """Remove query parameters from URL to get base URL."""
    if not url or url == 'N/A':
        return url
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Return just the scheme, netloc, and path (no query parameters)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    # Remove trailing slashes for consistency
    base_url = base_url.rstrip('/')
    
    return base_url

customer_id = "1994728449"
date_from = "2025-09-01"
date_to = "2025-11-28"

print(f"📊 Generating CLEAN Landing Page Reports for National Design Academy")
print(f"📅 Date Range: {date_from} to {date_to} (90 days)")
print(f"🧹 Cleaning: Removing URL parameters, filtering paused/removed\n")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

# =============================================================================
# REPORT 1: Overall Landing Page Statistics (already clean)
# =============================================================================

print("📄 Report 1: Landing Page Statistics")
print("   (This report already aggregates by base URL)")

query1 = f"""
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

response = requests.post(url, headers=headers, json={'query': query1})
data = response.json()
results = data.get('results', [])

# Aggregate by cleaned URL
landing_pages = defaultdict(lambda: {
    'impressions': 0,
    'clicks': 0,
    'conversions': 0,
    'conv_value': 0,
    'cost': 0
})

for row in results:
    raw_url = row['landingPageView']['unexpandedFinalUrl']
    clean_url_str = clean_url(raw_url)
    metrics = row['metrics']
    
    landing_pages[clean_url_str]['impressions'] += int(metrics.get('impressions', 0))
    landing_pages[clean_url_str]['clicks'] += int(metrics.get('clicks', 0))
    landing_pages[clean_url_str]['conversions'] += float(metrics.get('conversions', 0))
    landing_pages[clean_url_str]['conv_value'] += float(metrics.get('conversionsValue', 0))
    landing_pages[clean_url_str]['cost'] += int(metrics.get('costMicros', 0)) / 1_000_000

# Write Report 1
report1_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report1-landing-page-statistics-clean-90d.csv'

with open(report1_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Landing Page URL', 'Impressions', 'Clicks', 'CTR', 'Conversions',
        'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
    ])
    
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

print(f"   ✅ Report 1 saved: {len(landing_pages)} unique base URLs\n")

# =============================================================================
# REPORT 2: Performance Max Landing Pages (ENABLED only, clean URLs)
# =============================================================================

print("📄 Report 2: Performance Max Landing Pages")
print("   Filtering: ENABLED campaigns and asset groups only")

# Get ENABLED PMax campaigns only
query_campaigns = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status
    FROM campaign
    WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
      AND campaign.status = 'ENABLED'
"""

response = requests.post(url, headers=headers, json={'query': query_campaigns})
campaigns_data = response.json()

pmax_campaigns = []
for row in campaigns_data.get('results', []):
    pmax_campaigns.append({
        'id': row['campaign']['id'],
        'name': row['campaign']['name']
    })

print(f"   Found {len(pmax_campaigns)} ENABLED PMax campaigns")

# Get ENABLED asset groups with clean URLs
pmax_data = []

for campaign in pmax_campaigns:
    campaign_id = campaign['id']
    
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
          AND asset_group.status = 'ENABLED'
          AND segments.date BETWEEN '{date_from}' AND '{date_to}'
    """
    
    response = requests.post(url, headers=headers, json={'query': query_ag})
    ag_data = response.json()
    
    for row in ag_data.get('results', []):
        # Clean URLs
        raw_urls = row['assetGroup'].get('finalUrls', [])
        cleaned_urls = [clean_url(u) for u in raw_urls]
        landing_pages_str = ', '.join(cleaned_urls) if cleaned_urls else 'N/A'
        
        pmax_data.append({
            'campaign_name': row['campaign']['name'],
            'asset_group_name': row['assetGroup']['name'],
            'landing_pages': landing_pages_str,
            'impressions': int(row['metrics'].get('impressions', 0)),
            'clicks': int(row['metrics'].get('clicks', 0)),
            'conversions': float(row['metrics'].get('conversions', 0)),
            'conv_value': float(row['metrics'].get('conversionsValue', 0)),
            'cost': int(row['metrics'].get('costMicros', 0)) / 1_000_000
        })

# Write Report 2
report2_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report2-pmax-landing-pages-clean-90d.csv'

with open(report2_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Campaign Name', 'Asset Group Name', 'Landing Page URL(s)',
        'Impressions', 'Clicks', 'Conversions', 'Conv Value (£)', 'Cost (£)', 'ROAS'
    ])
    
    for row in pmax_data:
        roas = row['conv_value'] / row['cost'] if row['cost'] > 0 else 0
        
        writer.writerow([
            row['campaign_name'],
            row['asset_group_name'],
            row['landing_pages'],
            row['impressions'],
            row['clicks'],
            row['conversions'],
            f"£{row['conv_value']:.2f}",
            f"£{row['cost']:.2f}",
            f"{roas:.2f}"
        ])

print(f"   ✅ Report 2 saved: {len(pmax_data)} ENABLED asset groups\n")

# =============================================================================
# REPORT 3: Search Campaign Landing Pages (ENABLED only, clean URLs)
# =============================================================================

print("📄 Report 3: Search Campaign Landing Pages")
print("   Filtering: ENABLED campaigns only, clean URLs")

query3 = f"""
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
      AND campaign.status = 'ENABLED'
      AND segments.date BETWEEN '{date_from}' AND '{date_to}'
"""

response = requests.post(url, headers=headers, json={'query': query3})
data = response.json()
results = data.get('results', [])

print(f"   Found {len(results)} ENABLED ads")

# Aggregate by campaign + ad group + clean URL
search_aggregated = defaultdict(lambda: {
    'impressions': 0,
    'clicks': 0,
    'conversions': 0,
    'conv_value': 0,
    'cost': 0
})

for row in results:
    campaign_name = row['campaign']['name']
    ad_group_name = row['adGroup']['name']
    
    final_urls = row.get('adGroupAd', {}).get('ad', {}).get('finalUrls', [])
    raw_url = final_urls[0] if final_urls else 'N/A'
    clean_url_str = clean_url(raw_url)
    
    # Create unique key for aggregation
    key = (campaign_name, ad_group_name, clean_url_str)
    
    metrics = row['metrics']
    search_aggregated[key]['impressions'] += int(metrics.get('impressions', 0))
    search_aggregated[key]['clicks'] += int(metrics.get('clicks', 0))
    search_aggregated[key]['conversions'] += float(metrics.get('conversions', 0))
    search_aggregated[key]['conv_value'] += float(metrics.get('conversionsValue', 0))
    search_aggregated[key]['cost'] += int(metrics.get('costMicros', 0)) / 1_000_000

# Write Report 3
report3_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report3-search-landing-pages-clean-90d.csv'

with open(report3_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Campaign Name', 'Ad Group Name', 'Landing Page URL', 'Impressions',
        'Clicks', 'CTR', 'Conversions', 'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
    ])
    
    for (campaign_name, ad_group_name, landing_page), stats in search_aggregated.items():
        ctr = (stats['clicks'] / stats['impressions'] * 100) if stats['impressions'] > 0 else 0
        conv_rate = (stats['conversions'] / stats['clicks'] * 100) if stats['clicks'] > 0 else 0
        roas = stats['conv_value'] / stats['cost'] if stats['cost'] > 0 else 0
        
        writer.writerow([
            campaign_name,
            ad_group_name,
            landing_page,
            stats['impressions'],
            stats['clicks'],
            f"{ctr:.2f}%",
            stats['conversions'],
            f"{conv_rate:.2f}%",
            f"£{stats['cost']:.2f}",
            f"£{stats['conv_value']:.2f}",
            f"{roas:.2f}"
        ])

print(f"   ✅ Report 3 saved: {len(search_aggregated)} aggregated ad group URLs\n")

print("="*70)
print("✅ All CLEAN reports generated!")
print("\n📊 Reports saved:")
print(f"   1. {report1_path}")
print(f"   2. {report2_path}")
print(f"   3. {report3_path}")
print("\n🧹 Cleaning applied:")
print("   ✓ URL parameters removed (utm_*, etc.)")
print("   ✓ Only ENABLED campaigns/asset groups/ads included")
print("   ✓ Aggregated by base URL")
print("="*70 + "\n")
