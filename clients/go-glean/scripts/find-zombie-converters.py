#!/usr/bin/env python3
"""
Cross-reference converting products with Product Hero labels
to identify which Zombies are actually converting
"""

import json
from datetime import datetime, timedelta

# Load current labels
with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/history/label-transitions/go-glean-uk/current-labels.json', 'r') as f:
    labels_data = json.load(f)
    labels = labels_data['products']

print(f"Current label distribution:")
print(f"  Heroes: {labels_data['distribution']['heroes']}")
print(f"  Sidekicks: {labels_data['distribution']['sidekicks']}")
print(f"  Villains: {labels_data['distribution']['villains']}")
print(f"  Zombies: {labels_data['distribution']['zombies']}")
print(f"  Last updated: {labels_data['last_updated']}")
print()

# Load 30-day product performance
with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    data = json.load(f)

# Aggregate 30-day performance
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

from collections import defaultdict
products = defaultdict(lambda: {
    'item_id': '',
    'title': '',
    'spend': 0.0,
    'conversions': 0.0,
    'conversions_value': 0.0,
    'clicks': 0,
})

for row in data:
    segment_date = row.get('segments', {}).get('date', '')
    if segment_date:
        try:
            row_date = datetime.strptime(segment_date, '%Y-%m-%d').date()
            if row_date < start_date or row_date > end_date:
                continue
        except:
            continue
    else:
        continue

    item_id = row.get('segments', {}).get('productItemId', '')
    if not item_id:
        continue

    metrics = row.get('metrics', {})
    products[item_id]['item_id'] = item_id
    products[item_id]['title'] = row.get('segments', {}).get('productTitle', '')
    products[item_id]['spend'] += float(metrics.get('costMicros', 0)) / 1_000_000
    products[item_id]['conversions'] += float(metrics.get('conversions', 0))
    products[item_id]['conversions_value'] += float(metrics.get('conversionsValue', 0))
    products[item_id]['clicks'] += int(metrics.get('clicks', 0))

# Analyze converting products by label
converting_by_label = {
    'heroes': [],
    'sidekicks': [],
    'villains': [],
    'zombies': [],
    'unlabeled': []
}

for item_id, metrics in products.items():
    if metrics['conversions'] > 0:
        roas_pct = (metrics['conversions_value'] / metrics['spend'] * 100) if metrics['spend'] > 0 else 0
        metrics['roas_pct'] = roas_pct

        # Get label
        label = labels.get(item_id, 'unlabeled')
        metrics['label'] = label

        # Check if qualifies for Hero promotion (ROAS ≥195%, Clicks >28)
        metrics['hero_qualified'] = (roas_pct >= 195 and metrics['clicks'] > 28)
        metrics['sidekick_potential'] = (roas_pct >= 150 and metrics['clicks'] > 20 and not metrics['hero_qualified'])

        converting_by_label[label].append(metrics)

# Sort each category by conversions
for label in converting_by_label:
    converting_by_label[label].sort(key=lambda x: x['conversions'], reverse=True)

print("=" * 80)
print("🚨 CRITICAL FINDING: ZOMBIES THAT ARE CONVERTING")
print("=" * 80)
print()

zombies_converting = converting_by_label['zombies']
zombies_hero_qualified = [p for p in zombies_converting if p['hero_qualified']]
zombies_sidekick_potential = [p for p in zombies_converting if p['sidekick_potential']]

print(f"Total Zombies converting: {len(zombies_converting)} products")
print(f"Zombies qualified for HERO promotion: {len(zombies_hero_qualified)} products")
print(f"Zombies with Sidekick potential: {len(zombies_sidekick_potential)} products")
print()

if zombies_hero_qualified:
    print("⭐ ZOMBIES READY FOR HERO PROMOTION (ROAS ≥195%, Clicks >28):")
    print("-" * 80)
    for i, product in enumerate(zombies_hero_qualified, 1):
        print(f"\n{i}. {product['title'][:70]}")
        print(f"   Item ID: {product['item_id']}")
        print(f"   Current Label: {product['label'].upper()}")
        print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
        print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")
        print(f"   ✅ MEETS HERO CRITERIA - PROMOTE NOW")

if zombies_sidekick_potential:
    print("\n" + "=" * 80)
    print("🔸 ZOMBIES WITH SIDEKICK POTENTIAL (ROAS ≥150%, Clicks >20):")
    print("-" * 80)
    for i, product in enumerate(zombies_sidekick_potential, 1):
        print(f"\n{i}. {product['title'][:70]}")
        print(f"   Item ID: {product['item_id']}")
        print(f"   Current Label: {product['label'].upper()}")
        print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
        print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")
        print(f"   ⚠️ CLOSE TO HERO - Consider Sidekick promotion")

# Show all converting Zombies even if don't meet criteria
other_zombies = [p for p in zombies_converting if not p['hero_qualified'] and not p['sidekick_potential']]
if other_zombies:
    print("\n" + "=" * 80)
    print("OTHER CONVERTING ZOMBIES (Don't yet meet Hero/Sidekick criteria):")
    print("-" * 80)
    for i, product in enumerate(other_zombies, 1):
        print(f"\n{i}. {product['title'][:70]}")
        print(f"   ROAS: {product['roas_pct']:.0f}% | Clicks: {product['clicks']} | Conversions: {product['conversions']:.1f}")
        print(f"   Revenue: £{product['conversions_value']:.2f} | Spend: £{product['spend']:.2f}")

# Now show breakdown by all labels
print("\n" + "=" * 80)
print("CONVERSION PERFORMANCE BY CURRENT LABEL:")
print("=" * 80)

for label_name, products_list in converting_by_label.items():
    if products_list:
        total_conv = sum(p['conversions'] for p in products_list)
        total_spend = sum(p['spend'] for p in products_list)
        total_revenue = sum(p['conversions_value'] for p in products_list)
        blended_roas = (total_revenue / total_spend * 100) if total_spend > 0 else 0

        print(f"\n{label_name.upper()}:")
        print(f"  Converting products: {len(products_list)}")
        print(f"  Total conversions: {total_conv:.1f}")
        print(f"  Total spend: £{total_spend:.2f}")
        print(f"  Total revenue: £{total_revenue:.2f}")
        print(f"  Blended ROAS: {blended_roas:.0f}%")

# Summary
print("\n" + "=" * 80)
print("SUMMARY & NEXT ACTIONS")
print("=" * 80)

total_converting = sum(len(products_list) for products_list in converting_by_label.values())
print(f"\nTotal converting products (30 days): {total_converting}")
print(f"  - Heroes: {len(converting_by_label['heroes'])} converting")
print(f"  - Sidekicks: {len(converting_by_label['sidekicks'])} converting")
print(f"  - Villains: {len(converting_by_label['villains'])} converting")
print(f"  - Zombies: {len(zombies_converting)} converting ⚠️")
print(f"  - Unlabeled: {len(converting_by_label['unlabeled'])} converting")
print()
print(f"🚨 URGENT ACTION REQUIRED:")
print(f"   {len(zombies_hero_qualified)} Zombies meet Hero criteria and should be promoted")
print(f"   {len(zombies_sidekick_potential)} Zombies close to Hero level (Sidekick potential)")
print()
print(f"📅 Label data last updated: {labels_data['last_updated']}")
print(f"   Current date: {datetime.now().isoformat()}")
print()
print(f"✅ NEXT STEP:")
print(f"   Update Merchant Centre feed custom_label_0 for these {len(zombies_hero_qualified) + len(zombies_sidekick_potential)} products")
print(f"   to promote them from 'zombies' → 'heroes' or 'sidekicks'")
