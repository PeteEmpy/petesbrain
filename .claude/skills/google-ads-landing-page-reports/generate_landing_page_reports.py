#!/usr/bin/env python3
"""
Universal Landing Page Reports Generator for Google Ads
Generates 3 comprehensive reports for any client account
"""

import os
import sys
import csv
import requests
from collections import defaultdict
from datetime import datetime, timedelta
import argparse

# Add MCP server to path for OAuth helper
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

# Set environment variables for OAuth
os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate Google Ads landing page reports')
    parser.add_argument('customer_id', help='Google Ads Customer ID (10 digits, no dashes)')
    parser.add_argument('client_slug', help='Client folder name (e.g., smythson, national-design-academy)')
    parser.add_argument('--date-from', help='Start date (YYYY-MM-DD). Default: 90 days ago')
    parser.add_argument('--date-to', help='End date (YYYY-MM-DD). Default: today')
    parser.add_argument('--days', type=int, default=90, help='Number of days to look back. Default: 90')
    parser.add_argument('--manager-id', help='Manager account ID if this is a managed account')

    return parser.parse_args()

def calculate_dates(date_from, date_to, days):
    """Calculate date range."""
    if date_to:
        end_date = date_to
    else:
        end_date = datetime.now().strftime('%Y-%m-%d')

    if date_from:
        start_date = date_from
    else:
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    return start_date, end_date

def get_headers(manager_id=None):
    """Get API headers with authentication."""
    headers = get_headers_with_auto_token()

    if manager_id:
        headers['login-customer-id'] = manager_id

    return headers

def generate_report1_landing_page_stats(customer_id, date_from, date_to, output_path, headers):
    """Generate Report 1: Overall Landing Page Statistics."""
    print(f"\n📊 Generating Report 1: Landing Page Statistics")
    print(f"📅 Date Range: {date_from} to {date_to}")

    url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

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

    print("  Querying landing page data...")
    response = requests.post(url, headers=headers, json={'query': query})

    if not response.ok:
        print(f"  ❌ Error: {response.status_code} - {response.text}")
        return False

    data = response.json()
    results = data.get('results', [])

    print(f"  ✓ Found {len(results)} landing page records")

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

    # Write CSV
    with open(output_path, 'w', newline='') as f:
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

    print(f"  ✅ Report 1 saved: {len(landing_pages)} unique landing pages")
    return True

def generate_report2_pmax_landing_pages(customer_id, date_from, date_to, output_path, headers):
    """Generate Report 2: Performance Max Landing Pages by Asset Group."""
    print(f"\n📊 Generating Report 2: Performance Max Landing Pages")

    url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

    # Step 1: Get all PMax campaigns
    query_campaigns = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND campaign.status IN ('ENABLED', 'PAUSED')
    """

    print("  Fetching Performance Max campaigns...")
    response = requests.post(url, headers=headers, json={'query': query_campaigns})

    if not response.ok:
        print(f"  ❌ Error: {response.status_code} - {response.text}")
        return False

    campaigns_data = response.json()

    pmax_campaigns = []
    for row in campaigns_data.get('results', []):
        pmax_campaigns.append({
            'id': row['campaign']['id'],
            'name': row['campaign']['name'],
            'status': row['campaign']['status']
        })

    print(f"  ✓ Found {len(pmax_campaigns)} Performance Max campaigns")

    # Step 2: Query asset groups for each campaign
    print("  Fetching asset group data...")
    pmax_data = []

    for campaign in pmax_campaigns:
        campaign_id = campaign['id']
        campaign_name = campaign['name']
        campaign_status = campaign['status']

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

    print(f"  ✓ Found {len(pmax_data)} asset group records")

    # Write CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Campaign Name', 'Campaign Status', 'Asset Group Name', 'Asset Group Status',
            'Landing Page URL(s)', 'Impressions', 'Clicks', 'Conversions',
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

    print(f"  ✅ Report 2 saved: {len(pmax_data)} asset group records")
    return True

def generate_report3_search_landing_pages(customer_id, date_from, date_to, output_path, headers):
    """Generate Report 3: Search Campaign Landing Pages."""
    print(f"\n📊 Generating Report 3: Search Campaign Landing Pages")

    url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

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

    print("  Querying Search campaign data...")
    response = requests.post(url, headers=headers, json={'query': query})

    if not response.ok:
        print(f"  ❌ Error: {response.status_code} - {response.text}")
        return False

    data = response.json()
    results = data.get('results', [])

    print(f"  ✓ Found {len(results)} ad records from Search campaigns")

    # Write CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Campaign Name', 'Ad Group Name', 'Landing Page URL', 'Impressions',
            'Clicks', 'CTR', 'Conversions', 'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
        ])

        for row in results:
            campaign_name = row['campaign']['name']
            ad_group_name = row['adGroup']['name']

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

    print(f"  ✅ Report 3 saved: {len(results)} ad records")
    return True

def main():
    """Main execution function."""
    args = parse_arguments()

    # Calculate dates
    date_from, date_to = calculate_dates(args.date_from, args.date_to, args.days)

    # Setup
    print(f"🚀 Google Ads Landing Page Reports Generator")
    print(f"📁 Client: {args.client_slug}")
    print(f"🔑 Customer ID: {args.customer_id}")
    print(f"📅 Date Range: {date_from} to {date_to}")

    if args.manager_id:
        print(f"🏢 Manager Account: {args.manager_id}")

    # Get OAuth headers
    print(f"\n🔐 Authenticating...")
    headers = get_headers(args.manager_id)
    print(f"  ✓ Authentication successful")

    # Create output directory
    output_dir = f'/Users/administrator/Documents/PetesBrain/clients/{args.client_slug}/reports/landing-page-analysis'
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n📂 Output Directory: {output_dir}")

    # Generate reports
    date_label = f"{args.days}d" if not args.date_from else f"{date_from}_to_{date_to}"

    report1_path = f"{output_dir}/report1-landing-page-statistics-{date_label}.csv"
    report2_path = f"{output_dir}/report2-pmax-landing-pages-{date_label}.csv"
    report3_path = f"{output_dir}/report3-search-landing-pages-{date_label}.csv"

    success = True

    # Report 1
    if not generate_report1_landing_page_stats(args.customer_id, date_from, date_to, report1_path, headers):
        success = False

    # Report 2
    if not generate_report2_pmax_landing_pages(args.customer_id, date_from, date_to, report2_path, headers):
        success = False

    # Report 3
    if not generate_report3_search_landing_pages(args.customer_id, date_from, date_to, report3_path, headers):
        success = False

    # Summary
    print(f"\n{'='*60}")
    if success:
        print(f"✅ All reports generated successfully!")
    else:
        print(f"⚠️  Some reports had errors - check output above")

    print(f"\n📊 Report Files:")
    print(f"  1. {report1_path}")
    print(f"  2. {report2_path}")
    print(f"  3. {report3_path}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
