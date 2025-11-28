#!/usr/bin/env python3
"""
Product Change Detector - Compare product snapshots to detect changes

Compares today's product feed snapshot to yesterday's to identify:
- Price changes (regular and sale prices)
- Availability changes (in/out of stock)
- Title and description changes
- Image changes (main and additional images)
- Product type and category changes
- Item group ID changes (variant grouping)
- Shipping information changes
- Brand, GTIN, MPN, condition changes
- Apparel attributes (age group, color, gender, size)
- Custom label changes
- New products added
- Products removed

Usage:
    python3 product_change_detector.py
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ProductChangeDetector:
    """Detect changes in product feed data"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.history_dir = self.base_dir / 'data' / 'product_feed_history'
        self.changes_dir = self.base_dir / 'data' / 'product_changes'
        self.changes_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def load_snapshot(self, client_name: str, date: str) -> Optional[Dict]:
        """
        Load product snapshot for a specific date

        Args:
            client_name: Name of the client
            date: Date string (YYYY-MM-DD)

        Returns:
            Snapshot dict or None if not found
        """
        client_dir = self.history_dir / client_name
        snapshot_path = client_dir / f"{date}.json"

        if not snapshot_path.exists():
            return None

        try:
            with open(snapshot_path) as f:
                return json.load(f)
        except Exception as e:
            self.log(f"  ❌ Error loading snapshot {snapshot_path}: {e}")
            return None

    def compare_products(self, old_product: Dict, new_product: Dict) -> Dict[str, Tuple[str, str]]:
        """
        Compare two product versions and identify changes

        Args:
            old_product: Product data from previous snapshot
            new_product: Product data from current snapshot

        Returns:
            Dict of changes: {field: (old_value, new_value)}
        """
        changes = {}

        # Fields to compare
        fields_to_check = [
            'price',
            'sale_price',
            'availability',
            'title',
            'description',
            'product_type',
            'link',
            'image_link',
            'additional_image_links',
            'google_product_category',
            'brand',
            'condition',
            'item_group_id',
            'gtin',
            'mpn',
            'age_group',
            'color',
            'gender',
            'size',
            'shipping',
            'custom_label_0',
            'custom_label_1',
            'custom_label_2',
            'custom_label_3',
            'custom_label_4'
        ]

        for field in fields_to_check:
            old_value = old_product.get(field, '')
            new_value = new_product.get(field, '')

            # Handle arrays (additional_image_links, shipping)
            if field in ['additional_image_links', 'shipping']:
                old_list = old_value if isinstance(old_value, list) else []
                new_list = new_value if isinstance(new_value, list) else []
                old_value_norm = json.dumps(sorted(old_list))
                new_value_norm = json.dumps(sorted(new_list))
            else:
                # Normalize for comparison
                old_value_norm = str(old_value).strip()
                new_value_norm = str(new_value).strip()

            if old_value_norm != new_value_norm:
                # For arrays, show count change or simplified diff
                if field in ['additional_image_links', 'shipping']:
                    old_count = len(old_value) if isinstance(old_value, list) else 0
                    new_count = len(new_value) if isinstance(new_value, list) else 0
                    changes[field] = (f"{old_count} items", f"{new_count} items")
                else:
                    changes[field] = (old_value, new_value)

        return changes

    def detect_changes_for_client(self, client_name: str, today: str, yesterday: str) -> Dict:
        """
        Detect all changes for a client between two dates

        Args:
            client_name: Name of the client
            today: Today's date (YYYY-MM-DD)
            yesterday: Yesterday's date (YYYY-MM-DD)

        Returns:
            Dict with change analysis
        """
        self.log(f"Detecting changes for {client_name}...")

        # Load snapshots
        snapshot_yesterday = self.load_snapshot(client_name, yesterday)
        snapshot_today = self.load_snapshot(client_name, today)

        if not snapshot_yesterday:
            self.log(f"  ⚠️  No snapshot for {yesterday}, skipping")
            return {}

        if not snapshot_today:
            self.log(f"  ⚠️  No snapshot for {today}, skipping")
            return {}

        # Build product lookups by product_id
        products_yesterday = {p['product_id']: p for p in snapshot_yesterday['products']}
        products_today = {p['product_id']: p for p in snapshot_today['products']}

        # Track changes
        changed_products = []
        new_products = []
        removed_products = []

        # Check for changes in existing products
        for product_id, today_product in products_today.items():
            if product_id in products_yesterday:
                # Product exists in both - check for changes
                yesterday_product = products_yesterday[product_id]
                changes = self.compare_products(yesterday_product, today_product)

                if changes:
                    changed_products.append({
                        'product_id': product_id,
                        'title': today_product.get('title', ''),
                        'changes': changes
                    })
            else:
                # New product added
                new_products.append({
                    'product_id': product_id,
                    'title': today_product.get('title', ''),
                    'price': today_product.get('price', ''),
                    'availability': today_product.get('availability', '')
                })

        # Check for removed products
        for product_id, yesterday_product in products_yesterday.items():
            if product_id not in products_today:
                removed_products.append({
                    'product_id': product_id,
                    'title': yesterday_product.get('title', ''),
                    'price': yesterday_product.get('price', ''),
                    'availability': yesterday_product.get('availability', '')
                })

        # Categorize changes by type
        price_changes = [p for p in changed_products if 'price' in p['changes']]
        sale_price_changes = [p for p in changed_products if 'sale_price' in p['changes']]
        availability_changes = [p for p in changed_products if 'availability' in p['changes']]
        title_changes = [p for p in changed_products if 'title' in p['changes']]
        description_changes = [p for p in changed_products if 'description' in p['changes']]
        image_changes = [p for p in changed_products if 'image_link' in p['changes'] or 'additional_image_links' in p['changes']]
        item_group_changes = [p for p in changed_products if 'item_group_id' in p['changes']]
        shipping_changes = [p for p in changed_products if 'shipping' in p['changes']]
        label_changes = [p for p in changed_products if any(k.startswith('custom_label') for k in p['changes'].keys())]

        # Log summary
        self.log(f"  Changed products: {len(changed_products)}")
        self.log(f"    Price changes: {len(price_changes)}")
        self.log(f"    Sale price changes: {len(sale_price_changes)}")
        self.log(f"    Availability changes: {len(availability_changes)}")
        self.log(f"    Title changes: {len(title_changes)}")
        self.log(f"    Description changes: {len(description_changes)}")
        self.log(f"    Image changes: {len(image_changes)}")
        self.log(f"    Item group changes: {len(item_group_changes)}")
        self.log(f"    Shipping changes: {len(shipping_changes)}")
        self.log(f"    Label changes: {len(label_changes)}")
        self.log(f"  New products: {len(new_products)}")
        self.log(f"  Removed products: {len(removed_products)}")

        return {
            'date': today,
            'client': client_name,
            'comparison_date': yesterday,
            'total_products_today': len(products_today),
            'total_products_yesterday': len(products_yesterday),
            'summary': {
                'changed_products': len(changed_products),
                'price_changes': len(price_changes),
                'sale_price_changes': len(sale_price_changes),
                'availability_changes': len(availability_changes),
                'title_changes': len(title_changes),
                'description_changes': len(description_changes),
                'image_changes': len(image_changes),
                'item_group_changes': len(item_group_changes),
                'shipping_changes': len(shipping_changes),
                'label_changes': len(label_changes),
                'new_products': len(new_products),
                'removed_products': len(removed_products)
            },
            'changed_products': changed_products,
            'new_products': new_products,
            'removed_products': removed_products,
            'price_changes': price_changes,
            'sale_price_changes': sale_price_changes,
            'availability_changes': availability_changes,
            'title_changes': title_changes,
            'description_changes': description_changes,
            'image_changes': image_changes,
            'item_group_changes': item_group_changes,
            'shipping_changes': shipping_changes,
            'label_changes': label_changes
        }

    def save_changes(self, client_name: str, changes: Dict) -> bool:
        """
        Save detected changes to disk

        Args:
            client_name: Name of the client
            changes: Dict of detected changes

        Returns:
            True if successful
        """
        if not changes:
            return False

        # Create client directory
        client_dir = self.changes_dir / client_name
        client_dir.mkdir(parents=True, exist_ok=True)

        # Save with today's date
        today = changes['date']
        changes_path = client_dir / f"{today}.json"

        try:
            with open(changes_path, 'w') as f:
                json.dump(changes, f, indent=2)

            self.log(f"  ✓ Saved changes to {changes_path}")
            return True

        except Exception as e:
            self.log(f"  ❌ Error saving changes for {client_name}: {e}")
            return False

    def detect_all_clients(self) -> Dict[str, Dict]:
        """
        Detect changes for all enabled clients

        Returns:
            Dict mapping client names to change summaries
        """
        self.log("="*80)
        self.log("PRODUCT CHANGE DETECTOR")
        self.log("="*80)
        self.log("")

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        self.log(f"Comparing {today} to {yesterday}\n")

        results = {}

        for client in self.config['clients']:
            if not client.get('enabled', True):
                continue

            client_name = client['name']

            # Detect changes
            changes = self.detect_changes_for_client(client_name, today, yesterday)

            if changes:
                # Save changes
                self.save_changes(client_name, changes)
                results[client_name] = changes['summary']

            self.log("")

        self.log("="*80)
        self.log("CHANGE DETECTION COMPLETE")
        self.log("="*80)
        self.log(f"\nClients analyzed: {len(results)}")

        # Overall summary
        total_changed = sum(r['changed_products'] for r in results.values())
        total_new = sum(r['new_products'] for r in results.values())
        total_removed = sum(r['removed_products'] for r in results.values())

        self.log(f"\nOverall Changes:")
        self.log(f"  Changed products: {total_changed}")
        self.log(f"  New products: {total_new}")
        self.log(f"  Removed products: {total_removed}")

        return results


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    detector = ProductChangeDetector(config_path)
    detector.detect_all_clients()


if __name__ == "__main__":
    main()
