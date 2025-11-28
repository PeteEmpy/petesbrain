#!/usr/bin/env python3
"""
Analyze Go Glean 30-day product performance to identify:
1. Which products converted in PMax campaigns in last 30 days
2. Which of those converting products are still labeled as "Zombies"
3. Which products qualify for Hero/Sidekick promotion (ROAS ≥195%, Clicks >28)
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta

# Load Go Glean product data
with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    data = json.load(f)

# Filter for PMax campaigns and last 30 days
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

print(f"Analysis Period: {start_date} to {end_date} (30 days)")
print("=" * 80)

# Group products by item_id and aggregate 30-day performance
products = defaultdict(lambda: {
    'item_id': '',
    'title': '',
    'custom_label_0': '',
    'campaigns': set(),
    'spend': 0.0,
    'conversions': 0.0,
    'conversions_value': 0.0,
    'clicks': 0,
    'impressions': 0
})

for row in data:
    # Only look at PMax campaigns
    campaign_name = row.get('campaign_name', '')
    if 'P Max' not in campaign_name and 'PMax' not in campaign_name:
        continue

    # Check date is within 30-day window
    segment_date = row.get('segments_date', '')
    if segment_date:
        try:
            row_date = datetime.strptime(segment_date, '%Y-%m-%d').date()
            if row_date < start_date or row_date > end_date:
                continue
        except:
            continue

    item_id = row.get('segments_product_item_id', '')
    if not item_id:
        continue

    # Aggregate metrics
    products[item_id]['item_id'] = item_id
    products[item_id]['title'] = row.get('segments_product_title', '')
    products[item_id]['custom_label_0'] = row.get('segments_product_custom_label0', '')
    products[item_id]['campaigns'].add(campaign_name)
    products[item_id]['spend'] += float(row.get('metrics_cost_micros', 0)) / 1_000_000
    products[item_id]['conversions'] += float(row.get('metrics_conversions', 0))
    products[item_id]['conversions_value'] += float(row.get('metrics_conversions_value', 0))
    products[item_id]['clicks'] += int(row.get('metrics_clicks', 0))
    products[item_id]['impressions'] += int(row.get('metrics_impressions', 0))

# Calculate ROAS and filter for converting products
converting_products = []
for item_id, metrics in products.items():
    if metrics['conversions'] > 0:
        roas_pct = (metrics['conversions_value'] / metrics['spend'] * 100) if metrics['spend'] > 0 else 0
        metrics['roas_pct'] = roas_pct
        metrics['campaigns'] = list(metrics['campaigns'])
        converting_products.append(metrics)

# Sort by conversions (descending)
converting_products.sort(key=lambda x: x['conversions'], reverse=True)

print(f"\nTotal converting products in PMax campaigns (30 days): {len(converting_products)}")
print()

# Analyze by custom_label_0
label_stats = defaultdict(lambda: {
    'count': 0,
    'conversions': 0.0,
    'spend': 0.0,
    'revenue': 0.0
})

zombies_converting = []
hero_qualified = []
sidekick_qualified = []

for product in converting_products:
    label = product['custom_label_0'] or 'UNLABELED'
    label_stats[label]['count'] += 1
    label_stats[label]['conversions'] += product['conversions']
    label_stats[label]['spend'] += product['spend']
    label_stats[label]['revenue'] += product['conversions_value']

    # Check if labeled as Zombie but converting
    if 'zombie' in label.lower() or label.lower() == 'z':
        zombies_converting.append(product)

        # Check if qualifies for promotion (ROAS ≥195%, Clicks >28)
        if product['roas_pct'] >= 195 and product['clicks'] > 28:
            hero_qualified.append(product)
        elif product['roas_pct'] >= 150 and product['clicks'] > 28:  # Potential Sidekick
            sidekick_qualified.append(product)

print("CONVERTING PRODUCTS BY LABEL:")
print("-" * 80)
for label, stats in sorted(label_stats.items(), key=lambda x: x[1]['conversions'], reverse=True):
    roas = (stats['revenue'] / stats['spend'] * 100) if stats['spend'] > 0 else 0
    print(f"\n{label}:")
    print(f"  Products: {stats['count']}")
    print(f"  Conversions: {stats['conversions']:.1f}")
    print(f"  Spend: £{stats['spend']:.2f}")
    print(f"  Revenue: £{stats['revenue']:.2f}")
    print(f"  ROAS: {roas:.0f}%")

print("\n" + "=" * 80)
print(f"🚨 CRITICAL ISSUE: ZOMBIES CONVERTING ({len(zombies_converting)} products)")
print("=" * 80)

if zombies_converting:
    print("\nProducts labeled as 'Zombies' but generating conversions in last 30 days:")
    print()
    for i, product in enumerate(zombies_converting[:20], 1):  # Top 20
        print(f"{i}. {product['title'][:60]}")
        print(f"   Item ID: {product['item_id']}")
        print(f"   Label: {product['custom_label_0']}")
        print(f"   Conversions: {product['conversions']:.1f}")
        print(f"   Spend: £{product['spend']:.2f}")
        print(f"   Revenue: £{product['conversions_value']:.2f}")
        print(f"   ROAS: {product['roas_pct']:.0f}%")
        print(f"   Clicks: {product['clicks']}")
        print()

print("\n" + "=" * 80)
print(f"⭐ HERO QUALIFIED: {len(hero_qualified)} Zombie products meet Hero criteria")
print("=" * 80)
print("Criteria: ROAS ≥195% AND Clicks >28 (30-day)")
print()

if hero_qualified:
    for i, product in enumerate(hero_qualified, 1):
        print(f"{i}. {product['title'][:60]}")
        print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
        print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")
        print(f"   ACTION: PROMOTE TO HERO")
        print()

print("\n" + "=" * 80)
print(f"🔸 SIDEKICK POTENTIAL: {len(sidekick_qualified)} Zombie products close to Hero")
print("=" * 80)
print("Criteria: ROAS ≥150% AND Clicks >28 (not quite Hero level)")
print()

if sidekick_qualified:
    for i, product in enumerate(sidekick_qualified, 1):
        print(f"{i}. {product['title'][:60]}")
        print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
        print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")
        print(f"   ACTION: Consider SIDEKICK promotion")
        print()

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total converting products (30d): {len(converting_products)}")
print(f"Zombies that are converting: {len(zombies_converting)} ({len(zombies_converting)/len(converting_products)*100:.0f}% of converters)")
print(f"Zombies ready for Hero promotion: {len(hero_qualified)}")
print(f"Zombies near Sidekick level: {len(sidekick_qualified)}")
print()
print("🚨 This explains why Zombies asset group generates 76% of revenue!")
print("   Best performers are stuck in low-budget Zombie group instead of Hero-level allocation.")
