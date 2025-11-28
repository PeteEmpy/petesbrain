#!/usr/bin/env python3
"""
Product Feed Tracker - Daily snapshots of Merchant Center product data

Fetches all product attributes from Google Merchant Center via Merchant API
and stores daily snapshots to detect changes over time.

Key attributes tracked:
- Price, Sale price
- Availability (in_stock, out_of_stock)
- Title, Description
- Product type, Google product category
- Link, image link, additional image links
- Brand, GTIN, MPN, Condition
- Item group ID (variant grouping)
- Shipping information
- Age group, Color, Gender, Size (apparel)
- Custom labels (0-4)

Usage:
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json python3 product_feed_tracker.py
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class ProductFeedTracker:
    """Track product feed data from Google Merchant Center"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.history_dir = self.base_dir / 'data' / 'product_feed_history'
        self.history_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Google Content API for Shopping
        # Try OAuth credentials first (for Merchant Center access), then fall back to service account
        oauth_creds_path = self.base_dir / 'oauth_credentials.json'

        if oauth_creds_path.exists():
            # Use OAuth credentials (user authentication)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Using OAuth credentials (user authentication)")
            with open(oauth_creds_path) as f:
                creds_data = json.load(f)

            credentials = Credentials(
                token=creds_data.get('token'),
                refresh_token=creds_data['refresh_token'],
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )
        else:
            # Fall back to service account (won't work for Merchant Center)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️  OAuth credentials not found - using service account (limited access)")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Run 'python3 setup_oauth.py' to set up OAuth authentication")
            credentials_path = os.environ.get(
                'GOOGLE_APPLICATION_CREDENTIALS',
                '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
            )

            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/content']
            )

        self.content_service = build('content', 'v2.1', credentials=credentials)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def fetch_products_for_client(self, client_name: str, merchant_id: str, manager_id: Optional[str] = None) -> List[Dict]:
        """
        Fetch all products for a client from Merchant Center

        Args:
            client_name: Name of the client
            merchant_id: Merchant Center ID
            manager_id: Manager account ID (if applicable)

        Returns:
            List of product dicts with attributes
        """
        self.log(f"Fetching products for {client_name} (merchant: {merchant_id})...")

        products = []
        page_token = None

        try:
            while True:
                # Build request for Content API for Shopping
                request_params = {
                    'merchantId': manager_id if manager_id else merchant_id,
                    'maxResults': 250  # API max per page
                }

                if page_token:
                    request_params['pageToken'] = page_token

                # Fetch products
                result = self.content_service.products().list(**request_params).execute()

                # Process products
                if 'resources' in result:
                    for product in result['resources']:
                        # Extract key attributes
                        product_data = {
                            'product_id': product.get('offerId', ''),
                            'title': product.get('title', ''),
                            'description': product.get('description', ''),
                            'link': product.get('link', ''),
                            'image_link': product.get('imageLink', ''),
                            'additional_image_links': product.get('additionalImageLinks', []),
                            'price': self._extract_price(product.get('price', {})),
                            'sale_price': self._extract_price(product.get('salePrice', {})),
                            'availability': product.get('availability', ''),
                            'product_type': product.get('productType', ''),
                            'google_product_category': product.get('googleProductCategory', ''),
                            'brand': product.get('brand', ''),
                            'gtin': product.get('gtin', ''),
                            'mpn': product.get('mpn', ''),
                            'condition': product.get('condition', ''),
                            'age_group': product.get('ageGroup', ''),
                            'color': product.get('color', ''),
                            'gender': product.get('gender', ''),
                            'item_group_id': product.get('itemGroupId', ''),
                            'size': product.get('size', ''),
                            'shipping': product.get('shipping', []),
                            'custom_label_0': product.get('customLabel0', ''),
                            'custom_label_1': product.get('customLabel1', ''),
                            'custom_label_2': product.get('customLabel2', ''),
                            'custom_label_3': product.get('customLabel3', ''),
                            'custom_label_4': product.get('customLabel4', '')
                        }

                        products.append(product_data)

                # Check for next page
                page_token = result.get('nextPageToken')
                if not page_token:
                    break

            self.log(f"  ✓ Fetched {len(products)} products for {client_name}")
            return products

        except Exception as e:
            self.log(f"  ❌ Error fetching products for {client_name}: {e}")
            return []

    def _extract_price(self, price_obj: Dict) -> str:
        """Extract price value from price object (Content API v2.1 format - deprecated)"""
        if not price_obj:
            return ''

        value = price_obj.get('value', '')
        currency = price_obj.get('currency', '')

        if value and currency:
            return f"{value} {currency}"
        return str(value) if value else ''

    def _extract_price_merchant(self, price_obj: Dict) -> str:
        """Extract price value from price object (Merchant API format)"""
        if not price_obj:
            return ''

        # Merchant API uses 'amountMicros' and 'currencyCode'
        amount_micros = price_obj.get('amountMicros', 0)
        currency = price_obj.get('currencyCode', '')

        if amount_micros and currency:
            # Convert micros to standard units (divide by 1,000,000)
            value = amount_micros / 1000000
            return f"{value} {currency}"
        return ''

    def save_snapshot(self, client_name: str, products: List[Dict]) -> bool:
        """
        Save product snapshot to disk

        Args:
            client_name: Name of the client
            products: List of product dicts

        Returns:
            True if successful
        """
        if not products:
            self.log(f"  ⚠️  No products to save for {client_name}")
            return False

        # Create client directory
        client_dir = self.history_dir / client_name
        client_dir.mkdir(parents=True, exist_ok=True)

        # Save snapshot with today's date
        today = datetime.now().strftime("%Y-%m-%d")
        snapshot_path = client_dir / f"{today}.json"

        try:
            snapshot = {
                'date': today,
                'client': client_name,
                'product_count': len(products),
                'products': products,
                'snapshot_timestamp': datetime.now().isoformat()
            }

            with open(snapshot_path, 'w') as f:
                json.dump(snapshot, f, indent=2)

            self.log(f"  ✓ Saved snapshot to {snapshot_path}")
            return True

        except Exception as e:
            self.log(f"  ❌ Error saving snapshot for {client_name}: {e}")
            return False

    def track_all_clients(self) -> Dict[str, int]:
        """
        Track products for all enabled clients

        Returns:
            Dict mapping client names to product counts
        """
        self.log("="*80)
        self.log("PRODUCT FEED TRACKER")
        self.log("="*80)
        self.log("")

        results = {}

        for client in self.config['clients']:
            if not client.get('enabled', True):
                continue

            client_name = client['name']
            merchant_id = client.get('merchant_id')
            manager_id = client.get('google_ads_manager_id')

            if not merchant_id or merchant_id == 'UNKNOWN':
                self.log(f"⚠️  Skipping {client_name}: No merchant ID")
                continue

            # Fetch products
            products = self.fetch_products_for_client(client_name, merchant_id, manager_id)

            # Save snapshot
            if products:
                success = self.save_snapshot(client_name, products)
                if success:
                    results[client_name] = len(products)

            self.log("")

        self.log("="*80)
        self.log("TRACKING COMPLETE")
        self.log("="*80)
        self.log(f"\nClients tracked: {len(results)}")
        for client_name, count in results.items():
            self.log(f"  {client_name}: {count} products")

        return results


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    tracker = ProductFeedTracker(config_path)
    tracker.track_all_clients()


if __name__ == "__main__":
    main()
