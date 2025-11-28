#!/usr/bin/env python3
"""
Merchant Center Product Status Tracker

Tracks Google Merchant Center product approval status and disapproval reasons.
Integrates with Product Impact Analyzer to identify why products disappeared.

Uses Google Content API for Shopping (Merchant Center API).
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import socket
import ssl


class MerchantCenterTracker:
    """Track product status and disapprovals in Google Merchant Center"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize with configuration"""
        self.config = self._load_config(config_path)
        self.service = None
        self._initialize_service()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def _initialize_service(self):
        """Initialize Google Content API service with timeout configuration"""
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        if not credentials_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

        # Scopes for Content API for Shopping
        scopes = ['https://www.googleapis.com/auth/content']

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes
        )

        # Build service with timeout configuration
        # Set socket timeout to 60 seconds globally
        socket.setdefaulttimeout(60)

        self.service = build('content', 'v2.1', credentials=credentials)

    def get_product_status(self, merchant_id: str, product_id: str) -> Optional[Dict]:
        """
        Get status for a specific product

        Args:
            merchant_id: Merchant Center ID
            product_id: Product ID (e.g., "online:en:GB:287")

        Returns:
            Dict with product status information or None if not found
        """
        try:
            response = self.service.productstatuses().get(
                merchantId=merchant_id,
                productId=product_id
            ).execute()

            return self._parse_product_status(response)

        except Exception as e:
            print(f"Error fetching product {product_id}: {str(e)}")
            return None

    def get_all_product_statuses(self, merchant_id: str, max_retries: int = 3) -> List[Dict]:
        """
        Get status for all products in a merchant account with retry logic

        Args:
            merchant_id: Merchant Center ID
            max_retries: Maximum number of retry attempts per request

        Returns:
            List of product status dictionaries
        """
        all_statuses = []
        page_token = None

        while True:
            retry_count = 0
            success = False

            while retry_count < max_retries and not success:
                try:
                    request = self.service.productstatuses().list(
                        merchantId=merchant_id,
                        pageToken=page_token,
                        maxResults=250  # Max allowed by API
                    )

                    response = request.execute()

                    # Parse each product status
                    for item in response.get('resources', []):
                        status = self._parse_product_status(item)
                        if status:
                            all_statuses.append(status)

                    # Check for next page
                    page_token = response.get('nextPageToken')
                    success = True

                    # Rate limiting: Small delay between pages
                    if page_token:
                        time.sleep(0.5)

                    if not page_token:
                        break

                except HttpError as e:
                    retry_count += 1
                    if e.resp.status in [429, 500, 503]:  # Rate limit or server error
                        if retry_count < max_retries:
                            wait_time = (2 ** retry_count)  # Exponential backoff
                            print(f"  Rate limit/server error (HTTP {e.resp.status}), retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                            time.sleep(wait_time)
                        else:
                            print(f"  Failed after {max_retries} retries: HTTP {e.resp.status}")
                            return all_statuses
                    else:
                        print(f"  HTTP error {e.resp.status}: {str(e)}")
                        return all_statuses

                except (socket.timeout, socket.error) as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = (2 ** retry_count)
                        print(f"  Network timeout, retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        print(f"  Network timeout after {max_retries} retries: {str(e)}")
                        return all_statuses

                except ssl.SSLError as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = (2 ** retry_count)
                        print(f"  SSL error, retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        print(f"  SSL error after {max_retries} retries: {str(e)}")
                        return all_statuses

                except Exception as e:
                    print(f"  Unexpected error listing products for merchant {merchant_id}: {str(e)}")
                    return all_statuses

            if not success:
                break

        return all_statuses

    def _parse_product_status(self, api_response: Dict) -> Dict:
        """
        Parse API response into simplified status dictionary

        Returns:
            {
                'product_id': str,
                'title': str,
                'status': 'approved' | 'disapproved' | 'pending',
                'destination_statuses': {
                    'Shopping': {
                        'status': str,
                        'disapproved_countries': [str],
                        'pending_countries': [str],
                        'approved_countries': [str]
                    }
                },
                'item_level_issues': [
                    {
                        'code': str,
                        'servability': str,
                        'resolution': str,
                        'description': str,
                        'detail': str,
                        'documentation': str,
                        'affected_countries': [str]
                    }
                ]
            }
        """
        product_id = api_response.get('productId', 'unknown')
        title = api_response.get('title', 'Unknown Product')

        # Determine overall status
        destination_statuses = api_response.get('destinationStatuses', [])
        overall_status = 'approved'  # Default

        # Build destination status map
        dest_status_map = {}

        for dest in destination_statuses:
            dest_name = dest.get('destination', 'Unknown')
            status = dest.get('status', 'unknown')

            # Track countries by status
            approved_countries = dest.get('approvedCountries', [])
            pending_countries = dest.get('pendingCountries', [])
            disapproved_countries = dest.get('disapprovedCountries', [])

            dest_status_map[dest_name] = {
                'status': status,
                'approved_countries': approved_countries,
                'pending_countries': pending_countries,
                'disapproved_countries': disapproved_countries
            }

            # Update overall status based on worst case
            if disapproved_countries:
                overall_status = 'disapproved'
            elif pending_countries and overall_status == 'approved':
                overall_status = 'pending'

        # Parse item-level issues (disapproval reasons)
        issues = []
        for issue in api_response.get('itemLevelIssues', []):
            issues.append({
                'code': issue.get('code', 'unknown'),
                'servability': issue.get('servability', 'unknown'),
                'resolution': issue.get('resolution', 'unknown'),
                'description': issue.get('description', ''),
                'detail': issue.get('detail', ''),
                'documentation': issue.get('documentation', ''),
                'affected_countries': issue.get('applicableCountries', [])
            })

        return {
            'product_id': product_id,
            'title': title,
            'status': overall_status,
            'destination_statuses': dest_status_map,
            'item_level_issues': issues,
            'last_checked': datetime.now().isoformat()
        }

    def check_all_clients(self) -> Dict[str, List[Dict]]:
        """
        Check product status for all enabled clients

        Returns:
            Dict mapping client names to their product status lists
        """
        results = {}

        for client in self.config.get('clients', []):
            if not client.get('enabled', False):
                continue

            client_name = client['name']
            merchant_id = client.get('merchant_id')

            if not merchant_id or merchant_id == "UNKNOWN":
                print(f"⚠️  Skipping {client_name}: No merchant ID configured")
                continue

            print(f"Checking {client_name} (Merchant ID: {merchant_id})...")

            statuses = self.get_all_product_statuses(merchant_id)
            results[client_name] = statuses

            # Print summary
            total = len(statuses)
            disapproved = len([s for s in statuses if s['status'] == 'disapproved'])
            pending = len([s for s in statuses if s['status'] == 'pending'])
            approved = total - disapproved - pending

            print(f"  ✓ {total} products: {approved} approved, {pending} pending, {disapproved} disapproved")

        return results

    def identify_disapprovals(self, statuses: List[Dict]) -> List[Dict]:
        """
        Filter to only disapproved products with detailed reasons

        Args:
            statuses: List of product statuses from get_all_product_statuses()

        Returns:
            List of disapproved products with reasons
        """
        disapproved = []

        for status in statuses:
            if status['status'] == 'disapproved':
                disapproved.append(status)

        return disapproved

    def save_snapshot(self, results: Dict[str, List[Dict]], output_path: str = "data/merchant_center_snapshot.json"):
        """
        Save product status snapshot to file

        Args:
            results: Results from check_all_clients()
            output_path: Where to save the snapshot
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'clients': results
        }

        with open(output_path, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"\n✓ Snapshot saved to {output_path}")

    def generate_disapproval_report(self, results: Dict[str, List[Dict]]) -> str:
        """
        Generate human-readable disapproval report

        Args:
            results: Results from check_all_clients()

        Returns:
            Formatted text report
        """
        report_lines = [
            "=" * 80,
            "MERCHANT CENTER DISAPPROVAL REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 80,
            ""
        ]

        total_disapproved = 0

        for client_name, statuses in results.items():
            disapproved = self.identify_disapprovals(statuses)
            total_disapproved += len(disapproved)

            if not disapproved:
                continue

            report_lines.append(f"\n{'─' * 80}")
            report_lines.append(f"{client_name}: {len(disapproved)} Disapproved Products")
            report_lines.append(f"{'─' * 80}\n")

            for product in disapproved:
                product_id = product['product_id'].split(':')[-1]  # Extract just the ID
                title = product['title']

                report_lines.append(f"🚫 Product {product_id}: {title}")

                # Show destination statuses
                for dest, dest_info in product['destination_statuses'].items():
                    if dest_info['disapproved_countries']:
                        countries = ', '.join(dest_info['disapproved_countries'])
                        report_lines.append(f"   Destination: {dest} (Disapproved in: {countries})")

                # Show issues
                for issue in product['item_level_issues']:
                    code = issue['code']
                    description = issue['description']
                    servability = issue['servability']

                    report_lines.append(f"   Issue: {code} ({servability})")
                    if description:
                        report_lines.append(f"      {description}")
                    if issue['resolution']:
                        report_lines.append(f"      Resolution: {issue['resolution']}")

                report_lines.append("")

        if total_disapproved == 0:
            report_lines.append("✅ No disapproved products found!")
        else:
            report_lines.append(f"\n{'=' * 80}")
            report_lines.append(f"TOTAL DISAPPROVED: {total_disapproved} products")
            report_lines.append(f"{'=' * 80}")

        return '\n'.join(report_lines)


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Track Merchant Center product disapprovals')
    parser.add_argument('--client', help='Check specific client only')
    parser.add_argument('--report', action='store_true', help='Generate disapproval report')
    parser.add_argument('--save', action='store_true', help='Save snapshot to file')

    args = parser.parse_args()

    tracker = MerchantCenterTracker()

    if args.client:
        # Check specific client
        client_config = next(
            (c for c in tracker.config['clients'] if c['name'].lower() == args.client.lower()),
            None
        )

        if not client_config:
            print(f"❌ Client '{args.client}' not found in config")
            return

        merchant_id = client_config.get('merchant_id')
        if not merchant_id or merchant_id == "UNKNOWN":
            print(f"❌ No merchant ID configured for {args.client}")
            return

        print(f"Checking {args.client} (Merchant ID: {merchant_id})...\n")
        statuses = tracker.get_all_product_statuses(merchant_id)
        results = {args.client: statuses}
    else:
        # Check all clients
        results = tracker.check_all_clients()

    if args.report:
        # Generate and print disapproval report
        report = tracker.generate_disapproval_report(results)
        print(f"\n{report}")

    if args.save:
        # Save snapshot
        tracker.save_snapshot(results)


if __name__ == '__main__':
    main()
