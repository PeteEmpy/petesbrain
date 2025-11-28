#!/usr/bin/env python3
"""
Intelligent Threshold Calculator for Product Impact Analyzer

Analyzes each client's actual data to calculate appropriate alert thresholds
based on their revenue patterns, product count, and typical daily fluctuations.

Usage:
    python3 calculate_thresholds.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import statistics


def load_client_data(client_name: str, data_dir: Path) -> List[Dict]:
    """Load Google Ads data for a client"""
    ads_file = data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"

    if not ads_file.exists():
        return None

    with open(ads_file) as f:
        return json.load(f)


def analyze_client_patterns(client_name: str, ads_data: List[Dict]) -> Dict:
    """Analyze a client's revenue patterns to determine thresholds"""

    if not ads_data:
        return None

    # Aggregate revenue by product per day
    daily_revenue_by_product = defaultdict(lambda: defaultdict(float))

    for row in ads_data:
        try:
            product_id = row['segments']['productItemId']
            date = row['segments']['date']
            revenue = float(row['metrics'].get('conversionsValue', 0))

            daily_revenue_by_product[product_id][date] += revenue
        except (KeyError, ValueError):
            continue

    # Calculate daily revenue changes per product
    revenue_changes = []

    for product_id, daily_revenue in daily_revenue_by_product.items():
        dates = sorted(daily_revenue.keys())

        for i in range(1, len(dates)):
            prev_revenue = daily_revenue[dates[i-1]]
            curr_revenue = daily_revenue[dates[i]]
            change = abs(curr_revenue - prev_revenue)

            if prev_revenue > 0:  # Only count products with revenue
                revenue_changes.append(change)

    if not revenue_changes:
        return None

    # Calculate statistics
    mean_change = statistics.mean(revenue_changes)
    median_change = statistics.median(revenue_changes)
    stdev_change = statistics.stdev(revenue_changes) if len(revenue_changes) > 1 else mean_change

    # Calculate total daily revenue across all products
    daily_totals = defaultdict(float)
    for product_data in daily_revenue_by_product.values():
        for date, revenue in product_data.items():
            daily_totals[date] += revenue

    avg_daily_revenue = statistics.mean(daily_totals.values()) if daily_totals else 0

    # Count active products
    active_products = len([p for p in daily_revenue_by_product.keys()
                          if sum(daily_revenue_by_product[p].values()) > 0])

    return {
        'client_name': client_name,
        'active_products': active_products,
        'avg_daily_revenue': avg_daily_revenue,
        'mean_daily_change': mean_change,
        'median_daily_change': median_change,
        'stdev_daily_change': stdev_change,
        'revenue_changes': revenue_changes
    }


def calculate_intelligent_thresholds(analysis: Dict) -> Dict:
    """Calculate intelligent thresholds based on client patterns"""

    if not analysis:
        # Default thresholds if no data
        return {
            'revenue_drop': 500,
            'revenue_spike': 500,
            'click_drop_percent': 50,
            'missing_products': 5,
            'rationale': 'Default - no historical data available'
        }

    # Revenue drop threshold: 2 standard deviations above mean change
    # This captures significant outliers while avoiding noise
    revenue_threshold = analysis['mean_daily_change'] + (2 * analysis['stdev_daily_change'])

    # Minimum threshold based on client size
    if analysis['avg_daily_revenue'] < 1000:
        min_threshold = 100  # Small client
    elif analysis['avg_daily_revenue'] < 5000:
        min_threshold = 250  # Medium client
    else:
        min_threshold = 500  # Large client

    revenue_threshold = max(revenue_threshold, min_threshold)

    # Round to nearest 50
    revenue_threshold = round(revenue_threshold / 50) * 50

    # Missing products threshold: 10% of active products or 5, whichever is larger
    missing_threshold = max(5, int(analysis['active_products'] * 0.1))

    # Click drop: Keep at 50% as it's a good universal metric
    click_drop = 50

    return {
        'revenue_drop': revenue_threshold,
        'revenue_spike': revenue_threshold,
        'click_drop_percent': click_drop,
        'missing_products': missing_threshold,
        'rationale': f"Based on avg daily revenue £{analysis['avg_daily_revenue']:.2f}, {analysis['active_products']} products"
    }


def get_client_tier_defaults(client_name: str) -> Dict:
    """Get intelligent defaults based on known client characteristics"""

    # Client tiers based on business knowledge
    # (These would ideally come from a client database or config)

    tier_thresholds = {
        # High-value luxury brands
        'smythson': {
            'revenue_drop': 1000,
            'revenue_spike': 1000,
            'click_drop_percent': 40,
            'missing_products': 10,
            'rationale': 'Luxury brand - higher value products, lower volume'
        },

        # Medium e-commerce
        'tree2mydoor': {
            'revenue_drop': 500,
            'revenue_spike': 500,
            'click_drop_percent': 50,
            'missing_products': 10,
            'rationale': 'Seasonal products - moderate volume, variable pricing'
        },

        'superspace': {
            'revenue_drop': 300,
            'revenue_spike': 300,
            'click_drop_percent': 50,
            'missing_products': 15,
            'rationale': 'Furniture - large catalog, moderate prices'
        },

        'brightminds': {
            'revenue_drop': 400,
            'revenue_spike': 400,
            'click_drop_percent': 50,
            'missing_products': 20,
            'rationale': 'Educational toys - large catalog, moderate prices'
        },

        # Lower-volume clients
        'accessories_for_the_home': {
            'revenue_drop': 250,
            'revenue_spike': 250,
            'click_drop_percent': 50,
            'missing_products': 10,
            'rationale': 'Home accessories - smaller catalog'
        },

        'go_glean': {
            'revenue_drop': 300,
            'revenue_spike': 300,
            'click_drop_percent': 50,
            'missing_products': 10,
            'rationale': 'Cleaning products - moderate volume'
        },

        'uno_lights': {
            'revenue_drop': 400,
            'revenue_spike': 400,
            'click_drop_percent': 50,
            'missing_products': 15,
            'rationale': 'Lighting - moderate to high ticket items'
        }
    }

    # Normalize client name for lookup
    lookup_name = client_name.lower().replace(' ', '_')

    if lookup_name in tier_thresholds:
        return tier_thresholds[lookup_name]

    # Default for unknown clients
    return {
        'revenue_drop': 500,
        'revenue_spike': 500,
        'click_drop_percent': 50,
        'missing_products': 5,
        'rationale': 'Default thresholds - client tier unknown'
    }


def main():
    """Calculate and display intelligent thresholds for all clients"""

    print("="*80)
    print("INTELLIGENT THRESHOLD CALCULATOR")
    print("="*80)
    print()

    # Load config
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    data_dir = Path(__file__).parent / "data"

    results = {}

    print("Analyzing clients...\n")

    for client_config in config['clients']:
        if not client_config.get('enabled'):
            continue

        client_name = client_config['name']
        print(f"📊 {client_name}")
        print("-" * 80)

        # Try to load and analyze actual data
        ads_data = load_client_data(client_name, data_dir)

        if ads_data:
            print(f"  ✓ Found {len(ads_data)} data rows")
            analysis = analyze_client_patterns(client_name, ads_data)

            if analysis:
                print(f"  ✓ Analysis complete:")
                print(f"    - Active products: {analysis['active_products']}")
                print(f"    - Avg daily revenue: £{analysis['avg_daily_revenue']:.2f}")
                print(f"    - Mean daily change: £{analysis['mean_daily_change']:.2f}")

                thresholds = calculate_intelligent_thresholds(analysis)
            else:
                print(f"  ⚠ No revenue data - using tier defaults")
                thresholds = get_client_tier_defaults(client_name)
        else:
            print(f"  ⚠ No data file - using tier defaults")
            thresholds = get_client_tier_defaults(client_name)

        print(f"\n  📍 Recommended Thresholds:")
        print(f"    - Revenue drop alert:    £{thresholds['revenue_drop']}")
        print(f"    - Revenue spike alert:   £{thresholds['revenue_spike']}")
        print(f"    - Click drop alert:      {thresholds['click_drop_percent']}%")
        print(f"    - Missing products:      {thresholds['missing_products']}+ products")
        print(f"    - Rationale: {thresholds['rationale']}")
        print()

        results[client_name] = thresholds

    # Generate updated config structure
    print("="*80)
    print("RECOMMENDED CONFIG.JSON UPDATE")
    print("="*80)
    print()
    print("Replace the 'clients' array in config.json with this:")
    print()
    print('"clients": [')

    for i, client_config in enumerate(config['clients']):
        if not client_config.get('enabled'):
            continue

        client_name = client_config['name']
        thresholds = results.get(client_name, get_client_tier_defaults(client_name))

        print('  {')
        print(f'    "name": "{client_name}",')
        print(f'    "merchant_id": "{client_config["merchant_id"]}",')
        print(f'    "google_ads_customer_id": "{client_config["google_ads_customer_id"]}",')
        print(f'    "enabled": {str(client_config["enabled"]).lower()},')
        print(f'    "monitoring_thresholds": {{')
        print(f'      "revenue_drop": {thresholds["revenue_drop"]},')
        print(f'      "revenue_spike": {thresholds["revenue_spike"]},')
        print(f'      "click_drop_percent": {thresholds["click_drop_percent"]},')
        print(f'      "missing_products": {thresholds["missing_products"]},')
        print(f'      "rationale": "{thresholds["rationale"]}"')
        print(f'    }}')

        # Check if this is the last enabled client
        remaining = [c for c in config['clients'][i+1:] if c.get('enabled')]
        if remaining or not client_config.get('enabled'):
            print('  },')
        else:
            print('  }')

    print(']')
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
