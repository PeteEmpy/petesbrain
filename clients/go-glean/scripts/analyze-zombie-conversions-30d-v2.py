#!/usr/bin/env python3
"""
Analyze Go Glean 30-day product performance (CORRECTED for data structure)
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta

# Load Go Glean product data
with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    data = json.load(f)

print(f"Total rows in data: {len(data)}")

# Filter for last 30 days
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

print(f"Analysis Period: {start_date} to {end_date} (30 days)")
print("=" * 80)

# Group products by item_id and aggregate 30-day performance
products = defaultdict(lambda: {
    'item_id': '',
    'title': '',
    'spend': 0.0,
    'conversions': 0.0,
    'conversions_value': 0.0,
    'clicks': 0,
    'impressions': 0,
    'dates': []
})

rows_in_period = 0
for row in data:
    # Check date is within 30-day window
    segment_date = row.get('segments', {}).get('date', '')
    if segment_date:
        try:
            row_date = datetime.strptime(segment_date, '%Y-%m-%d').date()
            if row_date < start_date or row_date > end_date:
                continue
            rows_in_period += 1
        except:
            continue
    else:
        continue

    item_id = row.get('segments', {}).get('productItemId', '')
    if not item_id:
        continue

    metrics = row.get('metrics', {})

    # Aggregate metrics
    products[item_id]['item_id'] = item_id
    products[item_id]['title'] = row.get('segments', {}).get('productTitle', '')
    products[item_id]['spend'] += float(metrics.get('costMicros', 0)) / 1_000_000
    products[item_id]['conversions'] += float(metrics.get('conversions', 0))
    products[item_id]['conversions_value'] += float(metrics.get('conversionsValue', 0))
    products[item_id]['clicks'] += int(metrics.get('clicks', 0))
    products[item_id]['impressions'] += int(metrics.get('impressions', 0))
    if segment_date not in products[item_id]['dates']:
        products[item_id]['dates'].append(segment_date)

print(f"Rows in 30-day period: {rows_in_period}")
print(f"Unique products in period: {len(products)}")
print()

# Filter for converting products
converting_products = []
for item_id, metrics in products.items():
    if metrics['conversions'] > 0:
        roas_pct = (metrics['conversions_value'] / metrics['spend'] * 100) if metrics['spend'] > 0 else 0
        metrics['roas_pct'] = roas_pct
        converting_products.append(metrics)

# Sort by conversions (descending)
converting_products.sort(key=lambda x: x['conversions'], reverse=True)

print(f"Products with conversions (30 days): {len(converting_products)}")
print()

if converting_products:
    # Check Hero qualification (ROAS ≥195%, Clicks >28)
    hero_qualified = []
    sidekick_qualified = []

    for product in converting_products:
        if product['roas_pct'] >= 195 and product['clicks'] > 28:
            hero_qualified.append(product)
        elif product['roas_pct'] >= 150 and product['clicks'] > 20:
            sidekick_qualified.append(product)

    print("=" * 80)
    print(f"⭐ HERO QUALIFIED: {len(hero_qualified)} products")
    print("=" * 80)
    print("Criteria: ROAS ≥195% AND Clicks >28 (30-day)")
    print()

    if hero_qualified:
        for i, product in enumerate(hero_qualified, 1):
            print(f"{i}. {product['title'][:70]}")
            print(f"   Item ID: {product['item_id']}")
            print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
            print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")
            print(f"   Days active: {len(product['dates'])}")
            print()

    print("=" * 80)
    print(f"🔸 SIDEKICK POTENTIAL: {len(sidekick_qualified)} products")
    print("=" * 80)
    print("Criteria: ROAS ≥150% AND Clicks >20")
    print()

    if sidekick_qualified:
        for i, product in enumerate(sidekick_qualified, 1):
            print(f"{i}. {product['title'][:70]}")
            print(f"   Item ID: {product['item_id']}")
            print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
            print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")
            print(f"   Days active: {len(product['dates'])}")
            print()

    print("=" * 80)
    print("ALL CONVERTING PRODUCTS (Top 30)")
    print("=" * 80)
    print()

    for i, product in enumerate(converting_products[:30], 1):
        print(f"{i}. {product['title'][:70]}")
        print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
        print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")

        # Check qualification
        if product['roas_pct'] >= 195 and product['clicks'] > 28:
            print(f"   ⭐ HERO QUALIFIED")
        elif product['roas_pct'] >= 150 and product['clicks'] > 20:
            print(f"   🔸 SIDEKICK POTENTIAL")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_conv = sum(p['conversions'] for p in converting_products)
    total_spend = sum(p['spend'] for p in converting_products)
    total_revenue = sum(p['conversions_value'] for p in converting_products)
    blended_roas = (total_revenue / total_spend * 100) if total_spend > 0 else 0

    print(f"Total converting products (30d): {len(converting_products)}")
    print(f"Hero qualified: {len(hero_qualified)}")
    print(f"Sidekick potential: {len(sidekick_qualified)}")
    print(f"Total conversions: {total_conv:.1f}")
    print(f"Total spend: £{total_spend:.2f}")
    print(f"Total revenue: £{total_revenue:.2f}")
    print(f"Blended ROAS: {blended_roas:.0f}%")
    print()
    print("NOTE: This data does NOT include custom_label_0 (Product Hero labels).")
    print("      Need to pull that from Merchant Centre feed to see current classifications.")
else:
    print("❌ No converting products found in this data.")
    print()
    print("This could mean:")
    print("1. Data doesn't include recent conversions")
    print("2. Product-level data structure doesn't capture conversions")
    print("3. Need to query Google Ads API directly with product dimension")
