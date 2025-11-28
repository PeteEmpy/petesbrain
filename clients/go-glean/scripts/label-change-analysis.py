#!/usr/bin/env python3
"""
Answer the question: When these products converted in the last 30 days,
were they ALREADY Heroes/Sidekicks, or were they Zombies that have since been promoted?
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict

# Load current labels (Nov 17, 2025)
with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/history/label-transitions/go-glean-uk/current-labels.json', 'r') as f:
    current_labels_data = json.load(f)
    current_labels = current_labels_data['products']

print("=" * 80)
print("LABEL CHANGE ANALYSIS: Go Glean Product Hero Classification")
print("=" * 80)
print()
print(f"Current labels captured: {current_labels_data['last_updated']}")
print(f"30-day analysis period: Oct 21 - Nov 20, 2025")
print()

# Load 30-day performance data
with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    data = json.load(f)

# Aggregate 30-day performance
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

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

# Get converting products
converting_products = []
for item_id, metrics in products.items():
    if metrics['conversions'] > 0:
        roas_pct = (metrics['conversions_value'] / metrics['spend'] * 100) if metrics['spend'] > 0 else 0
        metrics['roas_pct'] = roas_pct
        metrics['current_label'] = current_labels.get(item_id, 'UNLABELED')
        converting_products.append(metrics)

converting_products.sort(key=lambda x: x['conversions'], reverse=True)

print("=" * 80)
print("KEY FINDING: ALL CURRENT LABELS ARE FROM NOV 17")
print("=" * 80)
print()
print("The label transition history only has ONE snapshot: Nov 17, 2025")
print("This means:")
print("  - We DON'T have historical label data from earlier in the 30-day period")
print("  - We CAN'T determine if products were promoted DURING the 30-day window")
print("  - We CAN ONLY see what labels they have NOW (as of Nov 17)")
print()
print("To answer your question 'were they zombies when they converted', we would need:")
print("  - Label snapshots from Oct 21 (start of 30-day period)")
print("  - Or daily label transition logs showing when products changed categories")
print()

print("=" * 80)
print("WHAT WE CAN SAY:")
print("=" * 80)
print()
print("Based on current labels (Nov 17), here's how converting products are classified:")
print()

# Group by current label
by_label = defaultdict(list)
for product in converting_products:
    by_label[product['current_label']].append(product)

for label_name in ['heroes', 'sidekicks', 'villains', 'zombies', 'UNLABELED']:
    products_list = by_label.get(label_name, [])
    if products_list:
        total_conv = sum(p['conversions'] for p in products_list)
        print(f"\n{label_name.upper()}: {len(products_list)} converting products, {total_conv:.1f} conversions")
        print("-" * 80)
        for p in products_list[:5]:  # Top 5
            print(f"  {p['title'][:65]}")
            print(f"    ROAS: {p['roas_pct']:.0f}% | Clicks: {p['clicks']} | Conv: {p['conversions']:.1f}")

print("\n" + "=" * 80)
print("INTERPRETATION:")
print("=" * 80)
print()
print("Since we only have labels from Nov 17, there are TWO possibilities:")
print()
print("1. **Labels are STATIC** (not updated during 30-day period):")
print("   - Products had SAME label throughout Oct 21 - Nov 20")
print("   - Heroes were Heroes when they converted")
print("   - Zombies were Zombies when they converted")
print()
print("2. **Labels were UPDATED** sometime before Nov 17:")
print("   - Some products may have been Zombies earlier in the period")
print("   - Then promoted to Heroes/Sidekicks before Nov 17")
print("   - We can't tell which without earlier snapshots")
print()
print("🔍 TO DEFINITIVELY ANSWER YOUR QUESTION:")
print("   Need to implement daily label snapshot tracking to capture label changes over time")
print("   OR check Merchant Centre feed upload history to see when custom_label_0 was last updated")
