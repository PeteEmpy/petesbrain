#!/usr/bin/env python3
"""
Fetch Asset Performance Data via Google Ads API

Pulls Performance Max asset performance data with full campaign/asset group hierarchy.
Outputs CSV in same format as manual export but with added Campaign ID, Campaign Name,
Asset Group ID, and Asset Group Name columns.

Usage:
    python3 fetch_asset_performance_api.py --customer-id 4941701449 --days 90

Author: PetesBrain
Created: 2025-11-26
"""

import os
import sys
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Add MCP server path for Google Ads imports
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configuration
GOOGLE_ADS_YAML = os.path.expanduser("~/google-ads.yaml")
OUTPUT_DIR = Path(__file__).parent / 'output'


class AssetPerformanceFetcher:
    """Fetches PMAX asset performance data with campaign/asset group hierarchy"""

    def __init__(self, customer_id: str, days: int = 90):
        """
        Initialise fetcher

        Args:
            customer_id: Google Ads customer ID (10 digits)
            days: Number of days of performance data to fetch
        """
        self.customer_id = customer_id
        self.days = days
        self.client = None
        self.data = []

    def initialise_client(self) -> bool:
        """Initialise Google Ads API client"""
        try:
            self.client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
            print(f"✅ Google Ads client initialised for customer {self.customer_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to initialise Google Ads client: {e}")
            return False

    def fetch_asset_performance(self) -> bool:
        """
        Fetch asset performance data from Google Ads API

        Returns:
            True if successful, False otherwise
        """
        try:
            ga_service = self.client.get_service("GoogleAdsService")

            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.days)
            date_range = f"{start_date.strftime('%Y-%m-%d')},{end_date.strftime('%Y-%m-%d')}"

            # Build GAQL query
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    asset_group.id,
                    asset_group.name,
                    asset_group.status,
                    asset_group.final_urls,
                    asset.id,
                    asset.name,
                    asset.text_asset.text,
                    asset.type,
                    asset_group_asset.field_type,
                    asset_group_asset.status,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.ctr,
                    metrics.conversions,
                    metrics.conversions_value,
                    metrics.cost_micros,
                    metrics.average_cpc
                FROM asset_group_asset
                WHERE
                    campaign.advertising_channel_type = 'PERFORMANCE_MAX'
                    AND segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
                    AND asset.type = 'TEXT'
                    AND asset_group_asset.status = 'ENABLED'
                ORDER BY campaign.name, asset_group.name, asset_group_asset.field_type
            """

            print(f"🔍 Querying Google Ads API...")
            print(f"   Customer ID: {self.customer_id}")
            print(f"   Date range: Last {self.days} days")
            print()

            # Execute query
            response = ga_service.search(customer_id=self.customer_id, query=query)

            # Process results
            asset_map = {}  # Group by asset to aggregate metrics

            for row in response:
                # Extract data
                campaign_id = str(row.campaign.id)
                campaign_name = row.campaign.name
                campaign_status = row.campaign.status.name

                asset_group_id = str(row.asset_group.id)
                asset_group_name = row.asset_group.name
                asset_group_status = row.asset_group.status.name
                asset_group_url = list(row.asset_group.final_urls)[0] if row.asset_group.final_urls else ''

                asset_id = str(row.asset.id)
                asset_text = row.asset.text_asset.text
                asset_type = row.asset_group_asset.field_type.name
                asset_status = row.asset_group_asset.status.name

                # Metrics
                impressions = row.metrics.impressions
                clicks = row.metrics.clicks
                ctr = row.metrics.ctr
                conversions = row.metrics.conversions
                conv_value = row.metrics.conversions_value
                cost_micros = row.metrics.cost_micros
                avg_cpc = row.metrics.average_cpc

                # Create unique key for each asset instance (asset + campaign + asset group + type)
                key = (campaign_id, campaign_name, asset_group_id, asset_group_name,
                       asset_id, asset_text, asset_type)

                # Aggregate metrics if this asset appears multiple times
                if key not in asset_map:
                    asset_map[key] = {
                        'campaign_id': campaign_id,
                        'campaign_name': campaign_name,
                        'campaign_status': campaign_status,
                        'asset_group_id': asset_group_id,
                        'asset_group_name': asset_group_name,
                        'asset_group_status': asset_group_status,
                        'asset_group_url': asset_group_url,
                        'asset_id': asset_id,
                        'asset_text': asset_text,
                        'asset_type': asset_type,
                        'asset_status': asset_status,
                        'impressions': 0,
                        'clicks': 0,
                        'conversions': 0.0,
                        'conv_value': 0.0,
                        'cost_micros': 0
                    }

                # Aggregate metrics
                asset_map[key]['impressions'] += impressions
                asset_map[key]['clicks'] += clicks
                asset_map[key]['conversions'] += conversions
                asset_map[key]['conv_value'] += conv_value
                asset_map[key]['cost_micros'] += cost_micros

            # Convert to list
            self.data = list(asset_map.values())

            # Calculate derived metrics
            for asset in self.data:
                # CTR
                if asset['impressions'] > 0:
                    asset['ctr'] = (asset['clicks'] / asset['impressions']) * 100
                else:
                    asset['ctr'] = 0.0

                # Conv rate
                if asset['clicks'] > 0:
                    asset['conv_rate'] = (asset['conversions'] / asset['clicks']) * 100
                else:
                    asset['conv_rate'] = 0.0

                # Cost per conversion
                if asset['conversions'] > 0:
                    asset['cost_per_conv'] = (asset['cost_micros'] / 1_000_000) / asset['conversions']
                else:
                    asset['cost_per_conv'] = 0.0

                # Average CPC
                if asset['clicks'] > 0:
                    asset['avg_cpc'] = (asset['cost_micros'] / 1_000_000) / asset['clicks']
                else:
                    asset['avg_cpc'] = 0.0

                # Cost in currency
                asset['cost'] = asset['cost_micros'] / 1_000_000

            print(f"✅ Fetched {len(self.data)} asset performance records")
            print()

            # Summary by campaign
            campaigns = defaultdict(int)
            asset_groups = defaultdict(int)
            for asset in self.data:
                campaigns[asset['campaign_name']] += 1
                asset_groups[f"{asset['campaign_name']} → {asset['asset_group_name']}"] += 1

            print(f"📊 Summary:")
            print(f"   Campaigns: {len(campaigns)}")
            print(f"   Asset Groups: {len(asset_groups)}")
            print()

            for campaign, count in sorted(campaigns.items()):
                print(f"   📁 {campaign}: {count} assets")

            print()

            return True

        except GoogleAdsException as ex:
            print(f"❌ Google Ads API error: {ex}")
            for error in ex.failure.errors:
                print(f"   Error: {error.message}")
            return False
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return False

    def export_to_csv(self, output_path: Path) -> bool:
        """
        Export data to CSV in Google Ads Asset Performance Report format

        Args:
            output_path: Path to output CSV file

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.data:
                print("❌ No data to export")
                return False

            # Map asset types to match CSV export format
            type_map = {
                'HEADLINE': 'Headline',
                'LONG_HEADLINE': 'Long headline',
                'DESCRIPTION': 'Description'
            }

            print(f"💾 Exporting to CSV...")

            # Create output with CSV header matching Google Ads export format
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)

                # Write header rows (matching Google Ads format)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=self.days)

                writer.writerow(['Asset performance report'])
                writer.writerow([f'{start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")}'])

                # Column headers - NEW: Added Campaign ID, Campaign Name, Asset Group ID, Asset Group Name, Asset Group URL
                writer.writerow([
                    'Campaign ID',
                    'Campaign',
                    'Asset Group ID',
                    'Asset Group',
                    'Asset Group URL',
                    'Asset',
                    'Asset type',
                    'Status',
                    'Impr.',
                    'Clicks',
                    'CTR',
                    'Conversions',
                    'Conv. rate',
                    'Currency code',
                    'Cost',
                    'Cost / conv.',
                    'Conv. value',
                    'Avg. CPC'
                ])

                # Write data rows
                for asset in self.data:
                    writer.writerow([
                        asset['campaign_id'],
                        asset['campaign_name'],
                        asset['asset_group_id'],
                        asset['asset_group_name'],
                        asset['asset_group_url'],
                        asset['asset_text'],
                        type_map.get(asset['asset_type'], asset['asset_type']),
                        asset['asset_status'],
                        f"{asset['impressions']:,}",  # Format with commas
                        asset['clicks'],
                        f"{asset['ctr']:.2f}%",
                        f"{asset['conversions']:.2f}",
                        f"{asset['conv_rate']:.2f}%",
                        'GBP',  # Assuming GBP - could be made configurable
                        f"{asset['cost']:.2f}",
                        f"{asset['cost_per_conv']:.2f}" if asset['cost_per_conv'] > 0 else "0",
                        f"{asset['conv_value']:.2f}",
                        f"{asset['avg_cpc']:.2f}"
                    ])

            print(f"✅ Exported to: {output_path}")
            print()

            return True

        except Exception as e:
            print(f"❌ Error exporting CSV: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Fetch PMAX asset performance data via Google Ads API'
    )
    parser.add_argument(
        '--customer-id',
        required=True,
        help='Google Ads customer ID (10 digits, no dashes)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=90,
        help='Number of days of performance data (default: 90)'
    )
    parser.add_argument(
        '--output',
        help='Output CSV path (default: output/{client}-asset-performance-{date}.csv)'
    )

    args = parser.parse_args()

    print("=" * 80)
    print("FETCH PMAX ASSET PERFORMANCE VIA API")
    print("=" * 80)
    print()

    # Initialise fetcher
    fetcher = AssetPerformanceFetcher(
        customer_id=args.customer_id,
        days=args.days
    )

    # Initialise Google Ads client
    if not fetcher.initialise_client():
        sys.exit(1)

    # Fetch data
    if not fetcher.fetch_asset_performance():
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Auto-generate filename
        today = datetime.now().strftime('%Y-%m-%d')
        # Try to infer client name from customer ID
        # For now, use generic name
        output_path = OUTPUT_DIR / f'asset-performance-{args.customer_id}-{today}.csv'

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export to CSV
    if not fetcher.export_to_csv(output_path):
        sys.exit(1)

    print("=" * 80)
    print("✅ SUCCESS")
    print("=" * 80)
    print()
    print(f"Next step: Run analyse_asset_performance.py with this CSV")
    print(f"  python3 analyse_asset_performance.py")
    print()


if __name__ == "__main__":
    main()
