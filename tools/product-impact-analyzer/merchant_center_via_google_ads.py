#!/usr/bin/env python3
"""
Merchant Center Product Status Tracker - Google Ads API Method

Uses Google Ads API (shopping_performance_view) to check product approval status.
This method uses the EXISTING OAuth credentials from google-ads-mcp-server,
avoiding the need to grant service account access to 16+ Merchant Center accounts.

Requires: google-ads.yaml with OAuth refresh token (already configured)
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


class MerchantCenterViaGoogleAds:
    """Track product status via Google Ads API (shopping_performance_view)"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize with configuration"""
        self.config = self._load_config(config_path)

        # Google Ads YAML config path
        self.google_ads_yaml = os.path.expanduser("~/google-ads.yaml")
        if not os.path.exists(self.google_ads_yaml):
            raise ValueError(f"google-ads.yaml not found at {self.google_ads_yaml}")

        self.client = GoogleAdsClient.load_from_storage(self.google_ads_yaml)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def get_product_issues_for_client(self, customer_id: str, manager_id: Optional[str] = None) -> List[Dict]:
        """
        Get products with issues using Google Ads API

        Args:
            customer_id: Google Ads customer ID (e.g., "6281395727")
            manager_id: Optional manager ID for sub-accounts

        Returns:
            List of products with issue details
        """
        # Use manager ID if provided, otherwise use customer ID
        login_customer_id = manager_id if manager_id else customer_id

        ga_service = self.client.get_service("GoogleAdsService")

        # Query shopping_performance_view for product issues
        # Segments contain product details, metrics show performance
        query = """
            SELECT
                segments.product_item_id,
                segments.product_title,
                segments.product_brand,
                segments.product_category_level1,
                segments.product_country,
                segments.product_language,
                metrics.clicks,
                metrics.impressions
            FROM shopping_performance_view
            WHERE segments.date DURING LAST_30_DAYS
            LIMIT 500
        """

        products_with_issues = []

        try:
            search_request = self.client.get_type("SearchGoogleAdsRequest")
            search_request.customer_id = customer_id
            search_request.query = query

            # Note: login_customer_id is set at client level, not request level
            # If manager access is needed, reinitialize client with login_customer_id

            response = ga_service.search(request=search_request)

            for row in response:
                segments = row.segments
                metrics = row.metrics

                # Products with 0 impressions in 30 days likely have issues
                if metrics.impressions == 0 and metrics.clicks == 0:
                    products_with_issues.append({
                        'product_id': segments.product_item_id,
                        'title': segments.product_title,
                        'brand': segments.product_brand,
                        'category': segments.product_category_level1,
                        'country': segments.product_country,
                        'language': segments.product_language,
                        'impressions': metrics.impressions,
                        'clicks': metrics.clicks,
                        'status': 'potential_issue',
                        'reason': 'No impressions/clicks in last 30 days - possible disapproval or low bid',
                        'last_checked': datetime.now().isoformat()
                    })

        except GoogleAdsException as ex:
            print(f"❌ Error querying Google Ads API for customer {customer_id}:")
            for error in ex.failure.errors:
                print(f"   {error.message}")
            return []

        return products_with_issues

    def check_all_clients(self) -> Dict[str, List[Dict]]:
        """
        Check product status for all enabled clients using Google Ads API

        Returns:
            Dict mapping client names to their product issue lists
        """
        results = {}

        for client in self.config.get('clients', []):
            if not client.get('enabled', False):
                continue

            client_name = client['name']
            customer_id = client.get('google_ads_customer_id')
            manager_id = client.get('label_tracking', {}).get('manager_id')

            if not customer_id or customer_id == "UNKNOWN":
                print(f"⚠️  Skipping {client_name}: No Google Ads customer ID configured")
                continue

            print(f"Checking {client_name} (Customer ID: {customer_id})...")

            issues = self.get_product_issues_for_client(customer_id, manager_id)
            results[client_name] = issues

            print(f"  ⚠️  {len(issues)} products with potential issues (0 impressions in 30 days)")

        return results

    def generate_report(self, results: Dict[str, List[Dict]]) -> str:
        """
        Generate human-readable report of products with issues

        Args:
            results: Results from check_all_clients()

        Returns:
            Formatted text report
        """
        report_lines = [
            "=" * 80,
            "MERCHANT CENTER PRODUCT ISSUES REPORT (via Google Ads API)",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 80,
            "",
            "NOTE: This shows products with 0 impressions in last 30 days.",
            "Possible causes: Merchant Center disapproval, low bids, or seasonal.",
            ""
        ]

        total_issues = 0

        for client_name, issues in results.items():
            total_issues += len(issues)

            if not issues:
                continue

            report_lines.append(f"\n{'─' * 80}")
            report_lines.append(f"{client_name}: {len(issues)} Products with Potential Issues")
            report_lines.append(f"{'─' * 80}\n")

            for product in issues[:10]:  # Show first 10
                product_id = product['product_id']
                title = product['title']

                report_lines.append(f"⚠️  Product {product_id}: {title}")
                report_lines.append(f"   Brand: {product.get('brand', 'N/A')}")
                report_lines.append(f"   Category: {product.get('category', 'N/A')}")
                report_lines.append(f"   Reason: {product['reason']}")
                report_lines.append("")

            if len(issues) > 10:
                report_lines.append(f"   ... and {len(issues) - 10} more products with issues\n")

        if total_issues == 0:
            report_lines.append("✅ No products with zero impressions found!")
        else:
            report_lines.append(f"\n{'=' * 80}")
            report_lines.append(f"TOTAL PRODUCTS WITH ISSUES: {total_issues}")
            report_lines.append(f"{'=' * 80}")
            report_lines.append("")
            report_lines.append("ACTION: Review these products in Merchant Center for disapprovals")

        return '\n'.join(report_lines)

    def save_snapshot(self, results: Dict[str, List[Dict]], output_path: str = "data/merchant_center_snapshot_via_ads.json"):
        """
        Save product issue snapshot to file

        Args:
            results: Results from check_all_clients()
            output_path: Where to save the snapshot
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'method': 'google_ads_api',
            'note': 'Products with 0 impressions in last 30 days - potential disapprovals',
            'clients': results
        }

        with open(output_path, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"\n✓ Snapshot saved to {output_path}")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Track Merchant Center product issues via Google Ads API'
    )
    parser.add_argument('--client', help='Check specific client only')
    parser.add_argument('--report', action='store_true', help='Generate issue report')
    parser.add_argument('--save', action='store_true', help='Save snapshot to file')

    args = parser.parse_args()

    try:
        tracker = MerchantCenterViaGoogleAds()
    except Exception as e:
        print(f"❌ Error initializing tracker: {e}")
        print("\nMake sure google-ads.yaml exists at ~/google-ads.yaml")
        sys.exit(1)

    if args.client:
        # Check specific client
        client_config = next(
            (c for c in tracker.config['clients']
             if c['name'].lower() == args.client.lower()),
            None
        )

        if not client_config:
            print(f"❌ Client '{args.client}' not found in config")
            return

        customer_id = client_config.get('google_ads_customer_id')
        if not customer_id or customer_id == "UNKNOWN":
            print(f"❌ No Google Ads customer ID configured for {args.client}")
            return

        print(f"Checking {args.client} (Customer ID: {customer_id})...\n")
        manager_id = client_config.get('label_tracking', {}).get('manager_id')
        issues = tracker.get_product_issues_for_client(customer_id, manager_id)
        results = {args.client: issues}
    else:
        # Check all clients
        results = tracker.check_all_clients()

    if args.report:
        # Generate and print report
        report = tracker.generate_report(results)
        print(f"\n{report}")

    if args.save:
        # Save snapshot
        tracker.save_snapshot(results)


if __name__ == '__main__':
    main()
