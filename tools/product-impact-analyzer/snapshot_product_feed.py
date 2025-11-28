#!/usr/bin/env python3
"""
Product Feed Snapshot System

Fetches product feed data daily from Google Ads Shopping Performance View,
stores snapshots in Google Sheets, and detects changes (price, stock, etc.)

Architecture:
1. Fetch current product data via Google Ads API
2. Store snapshot in "Product Feed History" sheet
3. Compare with previous snapshot
4. Write detected changes to "Price Change Log" sheet
5. Update "Outliers Report" with price change details

Usage:
    python snapshot_product_feed.py

    Or run automatically via LaunchAgent (daily at 6 AM)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import subprocess


def load_config() -> Dict:
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        return json.load(f)


def fetch_product_data_via_mcp(customer_id: str, days_back: int = 1) -> List[Dict]:
    """
    Fetch product-level data from Google Ads via Claude Code MCP integration.

    Returns list of products with current price, title, availability.

    Note: This uses the Google Ads Shopping Performance View which includes:
    - product_item_id
    - product_title
    - product_price_micros (if available)
    - Recent performance metrics
    """

    # Get most recent day's data to capture current product state
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    # We'll use Claude Code's MCP tool to fetch this
    # For now, create a stub that returns the command to run
    query = f"""
    SELECT
        segments.product_item_id,
        segments.product_title,
        segments.product_brand,
        segments.product_condition,
        segments.product_channel,
        metrics.clicks,
        metrics.impressions,
        metrics.cost_micros
    FROM shopping_performance_view
    WHERE segments.date >= '{start_date}'
        AND segments.date <= '{end_date}'
    ORDER BY segments.product_item_id
    """

    print(f"Fetching product data for customer {customer_id}...")
    print(f"Date range: {start_date} to {end_date}")
    print(f"\nGAQL Query:\n{query}\n")

    # In actual use, Claude Code will call this via MCP
    # For manual runs, we need the user to run the query and save results

    # Check if we have cached data from recent MCP call
    cache_path = Path(__file__).parent / "data" / f"snapshot_cache_{customer_id}.json"

    if cache_path.exists():
        # Check if cache is recent (< 1 hour old)
        cache_age = datetime.now().timestamp() - cache_path.stat().st_mtime
        if cache_age < 3600:  # 1 hour
            print(f"Using cached data (age: {cache_age/60:.1f} minutes)")
            with open(cache_path) as f:
                return json.load(f)

    print("\n⚠️  No recent cached data found.")
    print("This script needs to be called via Claude Code MCP to fetch live data.")
    print("\nTo fetch data manually:")
    print(f"1. Run the GAQL query above via mcp__google-ads__run_gaql")
    print(f"2. Save results to: {cache_path}")
    print(f"3. Re-run this script")

    return []


def aggregate_products(raw_data: List[Dict]) -> Dict[str, Dict]:
    """
    Aggregate product data from multiple rows into unique products.

    Shopping Performance View returns one row per date+product, so we need to
    aggregate to get the latest state of each product.
    """
    products = {}

    for row in raw_data:
        try:
            product_id = row['segments']['productItemId']

            # If we haven't seen this product yet, or this is more recent data
            if product_id not in products:
                products[product_id] = {
                    'product_id': product_id,
                    'title': row['segments'].get('productTitle', ''),
                    'brand': row['segments'].get('productBrand', ''),
                    'condition': row['segments'].get('productCondition', ''),
                    'channel': row['segments'].get('productChannel', ''),
                    # Note: price_micros may not be available in shopping_performance_view
                    # We might need to fetch from Merchant Center instead
                    'price_micros': None,
                    'impressions': int(row['metrics'].get('impressions', 0)),
                    'clicks': int(row['metrics'].get('clicks', 0)),
                    'cost_micros': int(row['metrics'].get('costMicros', 0))
                }
            else:
                # Aggregate metrics across dates
                products[product_id]['impressions'] += int(row['metrics'].get('impressions', 0))
                products[product_id]['clicks'] += int(row['metrics'].get('clicks', 0))
                products[product_id]['cost_micros'] += int(row['metrics'].get('costMicros', 0))

        except (KeyError, ValueError) as e:
            print(f"Warning: Error processing row: {e}")
            continue

    return products


def load_previous_snapshot(spreadsheet_id: str, client_name: str) -> Dict[str, Dict]:
    """
    Load most recent snapshot from Product Feed History sheet.

    Sheet structure:
    Snapshot Date | Client | Product ID | Title | Brand | Price Micros | Impressions | Clicks | Cost Micros
    """
    print(f"Loading previous snapshot for {client_name}...")

    # We would use MCP to read from sheet
    # For now, check local cache
    cache_path = Path(__file__).parent / "data" / f"previous_snapshot_{client_name.replace(' ', '_').lower()}.json"

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    print(f"  No previous snapshot found")
    return {}


def detect_changes(current: Dict[str, Dict],
                   previous: Dict[str, Dict],
                   client_name: str) -> List[Dict]:
    """
    Compare current and previous snapshots to detect changes.

    Returns list of changes with type: REMOVED, NEW, MODIFIED, PRICE_CHANGE
    """
    changes = []

    # Detect removed products
    for product_id, prev_data in previous.items():
        if product_id not in current:
            changes.append({
                'client': client_name,
                'product_id': product_id,
                'product_title': prev_data['title'],
                'change_type': 'REMOVED',
                'date_changed': datetime.now().strftime('%d/%m/%Y'),
                'old_price': prev_data.get('price_micros'),
                'new_price': None,
                'old_impressions': prev_data.get('impressions', 0),
                'new_impressions': 0
            })

    # Detect new and modified products
    for product_id, curr_data in current.items():
        if product_id not in previous:
            # New product
            changes.append({
                'client': client_name,
                'product_id': product_id,
                'product_title': curr_data['title'],
                'change_type': 'NEW',
                'date_changed': datetime.now().strftime('%d/%m/%Y'),
                'old_price': None,
                'new_price': curr_data.get('price_micros'),
                'old_impressions': 0,
                'new_impressions': curr_data.get('impressions', 0)
            })
        else:
            # Check for changes
            prev_data = previous[product_id]

            # Price change (if we have price data)
            if (curr_data.get('price_micros') is not None and
                prev_data.get('price_micros') is not None and
                curr_data['price_micros'] != prev_data['price_micros']):

                price_change_pct = (
                    (curr_data['price_micros'] - prev_data['price_micros'])
                    / prev_data['price_micros'] * 100
                )

                changes.append({
                    'client': client_name,
                    'product_id': product_id,
                    'product_title': curr_data['title'],
                    'change_type': 'PRICE_CHANGE',
                    'date_changed': datetime.now().strftime('%d/%m/%Y'),
                    'old_price': prev_data['price_micros'],
                    'new_price': curr_data['price_micros'],
                    'price_change_percent': round(price_change_pct, 2),
                    'old_impressions': prev_data.get('impressions', 0),
                    'new_impressions': curr_data.get('impressions', 0)
                })

            # Title change
            elif curr_data['title'] != prev_data['title']:
                changes.append({
                    'client': client_name,
                    'product_id': product_id,
                    'product_title': curr_data['title'],
                    'change_type': 'MODIFIED',
                    'date_changed': datetime.now().strftime('%d/%m/%Y'),
                    'old_title': prev_data['title'],
                    'new_title': curr_data['title'],
                    'old_price': prev_data.get('price_micros'),
                    'new_price': curr_data.get('price_micros')
                })

    return changes


def save_snapshot_to_sheet(spreadsheet_id: str,
                           client_name: str,
                           products: Dict[str, Dict]):
    """
    Save current snapshot to Product Feed History sheet.

    Appends rows to the sheet with today's date.
    """
    print(f"\nSaving snapshot for {client_name}...")

    snapshot_date = datetime.now().strftime('%Y-%m-%d')

    rows = []
    for product_id, data in products.items():
        rows.append([
            snapshot_date,
            client_name,
            product_id,
            data['title'],
            data.get('brand', ''),
            str(data.get('price_micros', '')),
            str(data.get('impressions', 0)),
            str(data.get('clicks', 0)),
            str(data.get('cost_micros', 0))
        ])

    # For now, save locally
    # Claude Code will write to sheet via MCP
    output_path = Path(__file__).parent / "data" / f"snapshot_{client_name.replace(' ', '_').lower()}_{snapshot_date}.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(products, f, indent=2)

    print(f"  Saved {len(products)} products to {output_path}")

    # Also save as "previous" for next run
    prev_path = Path(__file__).parent / "data" / f"previous_snapshot_{client_name.replace(' ', '_').lower()}.json"
    with open(prev_path, 'w') as f:
        json.dump(products, f, indent=2)

    return rows


def save_changes_to_sheet(spreadsheet_id: str, changes: List[Dict]):
    """
    Save detected changes to Price Change Log sheet.
    """
    if not changes:
        print("\nNo changes detected")
        return

    print(f"\nSaving {len(changes)} changes to Price Change Log...")

    # Save locally for Claude to write to sheet
    output_path = Path(__file__).parent / "data" / "price_changes.json"
    with open(output_path, 'w') as f:
        json.dump(changes, f, indent=2)

    print(f"  Saved changes to {output_path}")

    # Print summary
    by_type = defaultdict(int)
    for change in changes:
        by_type[change['change_type']] += 1

    print("\n  Change Summary:")
    for change_type, count in by_type.items():
        print(f"    {change_type}: {count}")


def update_outliers_report(spreadsheet_id: str, changes: List[Dict]):
    """
    Update Outliers Report with new price change information.

    Adds columns: Old Price, New Price, Price Change %
    """
    # This would be done by Claude Code reading existing report,
    # merging with price change data, and writing back
    pass


def main():
    """Main snapshot workflow"""
    print("=" * 80)
    print("PRODUCT FEED SNAPSHOT SYSTEM")
    print("=" * 80)
    print()

    # Load config
    config = load_config()
    spreadsheet_id = config['spreadsheet_id']

    all_changes = []

    # Process each enabled client
    for client_config in config['clients']:
        if not client_config.get('enabled'):
            continue

        client_name = client_config['name']
        customer_id = client_config['google_ads_customer_id']

        if customer_id == 'UNKNOWN':
            print(f"\nSkipping {client_name} - no customer ID configured")
            continue

        print(f"\n{'='*80}")
        print(f"Processing: {client_name}")
        print(f"{'='*80}")

        # Fetch current product data
        raw_data = fetch_product_data_via_mcp(customer_id)

        if not raw_data:
            print(f"  No data fetched - skipping")
            continue

        current_products = aggregate_products(raw_data)
        print(f"  Found {len(current_products)} unique products")

        # Load previous snapshot
        previous_products = load_previous_snapshot(spreadsheet_id, client_name)

        # Detect changes
        if previous_products:
            changes = detect_changes(current_products, previous_products, client_name)
            all_changes.extend(changes)
        else:
            print("  First snapshot - no previous data to compare")
            changes = []

        # Save current snapshot
        save_snapshot_to_sheet(spreadsheet_id, client_name, current_products)

    # Save all changes
    if all_changes:
        save_changes_to_sheet(spreadsheet_id, all_changes)

    print("\n" + "=" * 80)
    print("SNAPSHOT COMPLETE")
    print("=" * 80)
    print(f"\nTotal changes detected: {len(all_changes)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
