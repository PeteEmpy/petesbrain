#!/usr/bin/env python3
"""
Product Price Tracker

Fetches product prices from Google Merchant Center API and tracks changes over time.
Integrates with Product Impact Analyzer to correlate price changes with performance impact.

Usage:
    python3 price_tracker.py                    # Track all enabled clients
    python3 price_tracker.py --client "Tree2mydoor"  # Track specific client
    python3 price_tracker.py --report           # Generate price change report
"""

import json
import os
import sys
import argparse
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from googleapiclient.errors import HttpError
import socket
import ssl

# Import Merchant Center tracker
from merchant_center_tracker import MerchantCenterTracker


class PriceTracker:
    """Track product prices and detect changes"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize price tracker"""
        self.config = self._load_config(config_path)
        self.base_dir = Path(__file__).parent
        self.price_dir = self.base_dir / "monitoring" / "prices"
        self.price_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Merchant Center tracker
        self.mc_tracker = MerchantCenterTracker(config_path)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def get_client_config(self, client_name: str) -> Optional[Dict]:
        """Get configuration for a specific client"""
        for client in self.config.get('clients', []):
            if client['name'].lower() == client_name.lower():
                return client
        return None

    def fetch_current_prices(self, merchant_id: str, max_retries: int = 3) -> Dict[str, Dict]:
        """
        Fetch current prices for all products from Merchant Center with retry logic.

        Args:
            merchant_id: Merchant Center ID
            max_retries: Maximum retry attempts per request

        Returns:
            Dict mapping product_id to price data:
            {
                'product_id': 'HSG123',
                'title': 'Product Name',
                'price': 24.99,
                'sale_price': 19.99,  # None if no sale
                'currency': 'GBP',
                'availability': 'in stock',
                'timestamp': '2025-11-12T12:00:00'
            }
        """
        products = {}
        page_token = None
        page_count = 0

        while True:
            retry_count = 0
            success = False

            while retry_count < max_retries and not success:
                try:
                    # Get products from Merchant Center
                    response = self.mc_tracker.service.products().list(
                        merchantId=merchant_id,
                        pageToken=page_token,
                        maxResults=250
                    ).execute()

                    # Process products
                    for item in response.get('resources', []):
                        product_id = item.get('offerId', item.get('id'))

                        # Extract price data
                        price_obj = item.get('price', {})
                        sale_price_obj = item.get('salePrice', {})
                        sale_effective_date = item.get('salePriceEffectiveDate', '')

                        products[product_id] = {
                            'product_id': product_id,
                            'title': item.get('title', 'Unknown'),
                            'price': float(price_obj.get('value', 0)) if price_obj.get('value') else None,
                            'sale_price': float(sale_price_obj.get('value', 0)) if sale_price_obj.get('value') else None,
                            'sale_effective_date': sale_effective_date,
                            'currency': price_obj.get('currency', 'GBP'),
                            'availability': item.get('availability', 'unknown'),
                            'timestamp': datetime.now().isoformat()
                        }

                    # Check for next page
                    page_token = response.get('nextPageToken')
                    page_count += 1
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
                            wait_time = (2 ** retry_count)  # Exponential backoff: 2s, 4s, 8s
                            print(f"  Rate limit/server error (HTTP {e.resp.status}), retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                            time.sleep(wait_time)
                        else:
                            print(f"  Failed after {max_retries} retries: HTTP {e.resp.status}")
                            return products  # Return partial results
                    else:
                        print(f"  HTTP error {e.resp.status}: {str(e)}")
                        return products

                except (socket.timeout, socket.error) as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = (2 ** retry_count)
                        print(f"  Network timeout, retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        print(f"  Network timeout after {max_retries} retries")
                        return products

                except ssl.SSLError as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = (2 ** retry_count)
                        print(f"  SSL error, retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        print(f"  SSL error after {max_retries} retries")
                        return products

                except Exception as e:
                    print(f"  Unexpected error fetching prices for merchant {merchant_id}: {str(e)}")
                    return products

            if not success:
                break

        return products

    def load_previous_snapshot(self, client_name: str) -> Optional[Dict]:
        """Load most recent price snapshot for a client"""
        snapshot_files = sorted(
            self.price_dir.glob(f"prices_{client_name.replace(' ', '_').lower()}_*.json")
        )

        if not snapshot_files:
            return None

        # Get most recent
        latest = snapshot_files[-1]
        with open(latest) as f:
            return json.load(f)

    def save_snapshot(self, client_name: str, prices: Dict[str, Dict]):
        """Save current price snapshot"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = self.price_dir / f"prices_{client_name.replace(' ', '_').lower()}_{timestamp}.json"

        snapshot = {
            'client': client_name,
            'timestamp': datetime.now().isoformat(),
            'product_count': len(prices),
            'products': prices
        }

        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"  Saved snapshot: {len(prices)} products")
        return filename

    def _price_hash(self, product: Dict) -> str:
        """
        Generate hash of price-relevant fields for quick comparison.

        This allows us to skip detailed comparison for products where nothing changed,
        significantly improving performance when few prices change.
        """
        # Create hash from price, sale_price, and sale_effective_date
        price = str(product.get('price', ''))
        sale_price = str(product.get('sale_price', ''))
        sale_dates = product.get('sale_effective_date', '')

        key = f"{price}|{sale_price}|{sale_dates}"
        return hashlib.md5(key.encode()).hexdigest()

    def detect_price_changes(
        self,
        current: Dict[str, Dict],
        previous: Dict[str, Dict],
        client_name: str
    ) -> List[Dict]:
        """
        Compare current and previous price snapshots to detect changes.

        Returns list of price change events with type:
        - PRICE_INCREASE
        - PRICE_DECREASE
        - SALE_STARTED
        - SALE_ENDED
        - PRICE_AND_SALE_CHANGED

        Uses hash-based optimization to skip unchanged products.
        """
        changes = []
        skipped = 0  # Track how many products were skipped

        for product_id, curr in current.items():
            # Skip if product didn't exist before (new product)
            if product_id not in previous:
                continue

            prev = previous[product_id]

            # OPTIMIZATION: Quick hash check - skip if nothing changed
            curr_hash = self._price_hash(curr)
            prev_hash = self._price_hash(prev)

            if curr_hash == prev_hash:
                skipped += 1
                continue  # Nothing changed, skip detailed comparison

            # Get current effective price (sale price if available, else regular price)
            curr_effective = curr['sale_price'] if curr['sale_price'] else curr['price']
            prev_effective = prev['sale_price'] if prev['sale_price'] else prev['price']

            # Skip if no price data
            if curr_effective is None or prev_effective is None:
                continue

            # Detect price change
            price_changed = False
            sale_changed = False
            change_type = None
            change_percent = 0

            # Check if effective price changed
            if abs(curr_effective - prev_effective) > 0.01:  # More than 1 cent change
                price_changed = True
                change_percent = ((curr_effective - prev_effective) / prev_effective) * 100

                # Determine change type
                if change_percent > 0:
                    change_type = 'PRICE_INCREASE'
                else:
                    change_type = 'PRICE_DECREASE'

            # Check if sale status changed
            prev_had_sale = prev['sale_price'] is not None
            curr_has_sale = curr['sale_price'] is not None

            if prev_had_sale != curr_has_sale:
                sale_changed = True
                if curr_has_sale:
                    change_type = 'SALE_STARTED'
                else:
                    change_type = 'SALE_ENDED'

            # Check if sale effective dates changed
            prev_sale_dates = prev.get('sale_effective_date', '')
            curr_sale_dates = curr.get('sale_effective_date', '')
            sale_dates_changed = prev_sale_dates != curr_sale_dates

            # Check if both price and sale changed
            if price_changed and sale_changed:
                change_type = 'PRICE_AND_SALE_CHANGED'

            # Only record if something changed
            if price_changed or sale_changed or sale_dates_changed:
                change = {
                    'client': client_name,
                    'product_id': product_id,
                    'product_title': curr['title'],
                    'change_type': change_type,
                    'date_changed': datetime.now().strftime('%Y-%m-%d'),
                    'old_price': prev['price'],
                    'new_price': curr['price'],
                    'old_sale_price': prev['sale_price'],
                    'new_sale_price': curr['sale_price'],
                    'old_sale_effective_date': prev_sale_dates,
                    'new_sale_effective_date': curr_sale_dates,
                    'old_effective_price': prev_effective,
                    'new_effective_price': curr_effective,
                    'price_change_percent': round(change_percent, 2),
                    'currency': curr['currency'],
                    'availability': curr['availability']
                }

                changes.append(change)

        # Print efficiency stats
        total_compared = len([p for p in current.keys() if p in previous])
        if total_compared > 0:
            efficiency = (skipped / total_compared) * 100
            print(f"  Comparison efficiency: {skipped}/{total_compared} products unchanged ({efficiency:.1f}%)")

        return changes

    def log_price_changes(self, changes: List[Dict]):
        """Save price changes to monthly log file"""
        if not changes:
            return

        month = datetime.now().strftime("%Y-%m")
        log_file = self.price_dir / f"price_changes_{month}.json"

        # Load existing log or create new
        if log_file.exists():
            with open(log_file) as f:
                log_data = json.load(f)
        else:
            log_data = {
                'month': month,
                'changes': []
            }

        # Append new changes
        log_data['changes'].extend(changes)

        # Save
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

        print(f"\n  Logged {len(changes)} price changes to {log_file.name}")

    def generate_summary(self, changes: List[Dict]) -> Dict:
        """Generate summary statistics for price changes"""
        if not changes:
            return {}

        by_type = defaultdict(int)
        by_client = defaultdict(int)
        total_products_affected = len(set(c['product_id'] for c in changes))

        price_increases = []
        price_decreases = []

        for change in changes:
            by_type[change['change_type']] += 1
            by_client[change['client']] += 1

            if change['change_type'] in ['PRICE_INCREASE', 'PRICE_DECREASE']:
                if change['price_change_percent'] > 0:
                    price_increases.append(change['price_change_percent'])
                else:
                    price_decreases.append(abs(change['price_change_percent']))

        return {
            'total_changes': len(changes),
            'products_affected': total_products_affected,
            'by_type': dict(by_type),
            'by_client': dict(by_client),
            'avg_price_increase': round(sum(price_increases) / len(price_increases), 2) if price_increases else 0,
            'avg_price_decrease': round(sum(price_decreases) / len(price_decreases), 2) if price_decreases else 0,
            'largest_increase': max(price_increases) if price_increases else 0,
            'largest_decrease': max(price_decreases) if price_decreases else 0
        }

    def track_client(self, client_name: str) -> List[Dict]:
        """Track prices for a single client"""
        client_config = self.get_client_config(client_name)
        if not client_config:
            print(f"Client '{client_name}' not found in config")
            return []

        merchant_id = client_config.get('merchant_id')
        if not merchant_id or merchant_id == 'UNKNOWN':
            print(f"No merchant ID configured for {client_name}")
            return []

        print(f"\n{'='*80}")
        print(f"Tracking prices: {client_name}")
        print(f"{'='*80}")

        # Fetch current prices
        print(f"Fetching prices from Merchant Center (ID: {merchant_id})...")
        current_prices = self.fetch_current_prices(merchant_id)

        if not current_prices:
            print("  No products found")
            return []

        print(f"  Found {len(current_prices)} products with price data")

        # Load previous snapshot
        previous_snapshot = self.load_previous_snapshot(client_name)

        # Detect changes
        changes = []
        if previous_snapshot:
            previous_prices = previous_snapshot.get('products', {})
            changes = self.detect_price_changes(current_prices, previous_prices, client_name)

            if changes:
                print(f"\n  Detected {len(changes)} price changes:")
                by_type = defaultdict(int)
                for change in changes:
                    by_type[change['change_type']] += 1

                for change_type, count in by_type.items():
                    print(f"    {change_type}: {count}")
            else:
                print("  No price changes detected")
        else:
            print("  First snapshot - no previous data to compare")

        # Save current snapshot
        self.save_snapshot(client_name, current_prices)

        # Log changes
        if changes:
            self.log_price_changes(changes)

        return changes

    def track_all_clients(self) -> Dict[str, List[Dict]]:
        """Track prices for all enabled clients (SEQUENTIAL with rate limiting)"""

        # Get list of enabled clients with valid merchant IDs
        enabled_clients = []
        for client_config in self.config.get('clients', []):
            if not client_config.get('enabled'):
                continue

            merchant_id = client_config.get('merchant_id')
            if not merchant_id or merchant_id == 'UNKNOWN':
                continue

            enabled_clients.append(client_config['name'])

        if not enabled_clients:
            return {}

        print(f"\nProcessing {len(enabled_clients)} clients sequentially to avoid rate limits...")

        all_changes = {}

        # Process clients sequentially to avoid rate limiting
        for i, client_name in enumerate(enabled_clients, 1):
            try:
                print(f"\n[{i}/{len(enabled_clients)}] Processing {client_name}...")
                changes = self.track_client(client_name)
                all_changes[client_name] = changes

                # Add delay between clients to respect rate limits
                if i < len(enabled_clients):
                    print(f"  Waiting 2s before next client...")
                    time.sleep(2)

            except Exception as e:
                print(f"\n  Error tracking {client_name}: {str(e)}")
                all_changes[client_name] = []

        return all_changes

    def generate_report(self, client_name: Optional[str] = None):
        """Generate price change report"""
        print("\n" + "="*80)
        print("PRICE CHANGE REPORT")
        print("="*80)

        # Load recent price changes (last 30 days)
        month = datetime.now().strftime("%Y-%m")
        log_file = self.price_dir / f"price_changes_{month}.json"

        if not log_file.exists():
            print("\nNo price changes recorded this month")
            return

        with open(log_file) as f:
            log_data = json.load(f)

        changes = log_data.get('changes', [])

        # Filter by client if specified
        if client_name:
            changes = [c for c in changes if c['client'].lower() == client_name.lower()]

        if not changes:
            if client_name:
                print(f"\nNo price changes for {client_name} this month")
            else:
                print("\nNo price changes this month")
            return

        # Generate summary
        summary = self.generate_summary(changes)

        print(f"\nSummary:")
        print(f"  Total changes: {summary['total_changes']}")
        print(f"  Products affected: {summary['products_affected']}")
        print(f"  Average increase: +{summary['avg_price_increase']}%")
        print(f"  Average decrease: -{summary['avg_price_decrease']}%")
        print(f"  Largest increase: +{summary['largest_increase']}%")
        print(f"  Largest decrease: -{summary['largest_decrease']}%")

        print(f"\nBy type:")
        for change_type, count in summary['by_type'].items():
            print(f"  {change_type}: {count}")

        if not client_name:
            print(f"\nBy client:")
            for client, count in summary['by_client'].items():
                print(f"  {client}: {count}")

        # Show recent significant changes (>10% or sale changes)
        significant = [
            c for c in changes
            if abs(c.get('price_change_percent', 0)) > 10
            or c['change_type'] in ['SALE_STARTED', 'SALE_ENDED']
        ]

        if significant:
            print(f"\n\nSignificant changes (>{10}% or sale changes):")
            print("-" * 80)

            for change in significant[-10:]:  # Last 10
                print(f"\n{change['change_type']}: {change['product_title'][:60]}")
                print(f"  Product ID: {change['product_id']}")
                print(f"  Date: {change['date_changed']}")

                if change['change_type'] == 'SALE_STARTED':
                    print(f"  Price: {change['currency']} {change['new_price']:.2f}")
                    print(f"  Sale price: {change['currency']} {change['new_sale_price']:.2f} ({change['price_change_percent']:+.1f}%)")
                elif change['change_type'] == 'SALE_ENDED':
                    print(f"  Was: {change['currency']} {change['old_sale_price']:.2f}")
                    print(f"  Now: {change['currency']} {change['new_price']:.2f} ({change['price_change_percent']:+.1f}%)")
                else:
                    print(f"  Old: {change['currency']} {change['old_effective_price']:.2f}")
                    print(f"  New: {change['currency']} {change['new_effective_price']:.2f} ({change['price_change_percent']:+.1f}%)")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Track product prices from Merchant Center')
    parser.add_argument('--client', help='Track specific client only')
    parser.add_argument('--report', action='store_true', help='Generate price change report')
    args = parser.parse_args()

    tracker = PriceTracker()

    if args.report:
        tracker.generate_report(args.client)
    elif args.client:
        changes = tracker.track_client(args.client)
        if changes:
            tracker.generate_report(args.client)
    else:
        all_changes = tracker.track_all_clients()

        # Print summary
        total_changes = sum(len(changes) for changes in all_changes.values())
        print("\n" + "="*80)
        print("PRICE TRACKING COMPLETE")
        print("="*80)
        print(f"\nTotal price changes detected: {total_changes}")

        if total_changes > 0:
            for client_name, changes in all_changes.items():
                if changes:
                    print(f"  {client_name}: {len(changes)} changes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
