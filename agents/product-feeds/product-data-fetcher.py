#!/usr/bin/env python3
"""
Automated Data Fetcher for Product Impact Analyzer

Fetches Google Ads Shopping performance data directly via Google Ads API
without MCP token limits.

Usage:
    python3 fetch_data_automated.py [--client CLIENT_NAME] [--days 30]
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


class AutomatedDataFetcher:
    """Fetches data directly from Google Ads API"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

        # Initialize Google Ads client
        self.client = GoogleAdsClient.load_from_env()

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def fetch_shopping_data(self, customer_id: str, merchant_id: str = None, days_back: int = 30) -> list:
        """Fetch Shopping performance data from Google Ads"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Build WHERE clause
        where_clauses = [
            f"segments.date >= '{start_date}'",
            f"segments.date <= '{end_date}'"
        ]

        # Add merchant filter if provided (critical for multi-brand accounts)
        if merchant_id:
            where_clauses.append(f"segments.product_merchant_id = '{merchant_id}'")

        query = f"""
        SELECT
            segments.product_merchant_id,
            segments.product_item_id,
            segments.product_title,
            segments.date,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM shopping_performance_view
        WHERE {' AND '.join(where_clauses)}
        ORDER BY segments.product_item_id, segments.date
        """

        ga_service = self.client.get_service("GoogleAdsService")

        results = []
        try:
            response = ga_service.search_stream(customer_id=customer_id, query=query)

            for batch in response:
                for row in batch.results:
                    results.append({
                        'segments': {
                            'productMerchantId': row.segments.product_merchant_id,
                            'productItemId': row.segments.product_item_id,
                            'productTitle': row.segments.product_title,
                            'date': row.segments.date
                        },
                        'metrics': {
                            'impressions': row.metrics.impressions,
                            'clicks': row.metrics.clicks,
                            'conversions': row.metrics.conversions,
                            'conversionsValue': row.metrics.conversions_value,
                            'costMicros': row.metrics.cost_micros
                        }
                    })

            return results

        except GoogleAdsException as ex:
            self.log(f"  ❌ Error fetching data: {ex}")
            return []

    def fetch_all_clients(self, client_filter: str = None, days_back: int = 30):
        """Fetch data for all enabled clients"""
        self.log("=" * 80)
        self.log("PRODUCT IMPACT ANALYZER - AUTOMATED DATA FETCHER")
        self.log("=" * 80)
        self.log("")

        for client_config in self.config['clients']:
            if not client_config.get('enabled'):
                continue

            # Skip if no merchant ID (not e-commerce)
            if not client_config.get('merchant_id') or client_config['merchant_id'] == 'UNKNOWN':
                continue

            client_name = client_config['name']

            # Filter if specified
            if client_filter and client_name != client_filter:
                continue

            customer_id = client_config['google_ads_customer_id']
            merchant_id = client_config.get('merchant_id')

            self.log(f"Fetching {client_name} (Customer: {customer_id}, Merchant: {merchant_id})...")

            # Fetch data with merchant filter
            data = self.fetch_shopping_data(customer_id, merchant_id, days_back)

            if data:
                # Save to file
                filename = f"ads_{client_name.replace(' ', '_').lower()}.json"
                filepath = self.data_dir / filename

                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)

                self.log(f"  ✅ Saved {len(data)} rows to {filename}")
            else:
                self.log(f"  ⚠️  No data returned")

        self.log("")
        self.log("=" * 80)
        self.log("FETCH COMPLETE")
        self.log("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Fetch Google Ads data for Product Impact Analyzer')
    parser.add_argument('--client', help='Fetch data for specific client only')
    parser.add_argument('--days', type=int, default=30, help='Days of data to fetch (default: 30)')
    args = parser.parse_args()

    config_path = Path(__file__).parent / 'config.json'
    fetcher = AutomatedDataFetcher(config_path)

    try:
        fetcher.fetch_all_clients(client_filter=args.client, days_back=args.days)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
