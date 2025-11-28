#!/usr/bin/env python3
"""
Compare product labels over time to see which converting products
were Zombies and have since been promoted to Heroes/Sidekicks.
"""

import json
import glob
from datetime import datetime, timedelta
from collections import defaultdict

# Get all feed history files
feed_files = sorted(glob.glob('tools/product-impact-analyzer/data/product_feed_history/Go Glean UK/*.json'))

print("=" * 80)
print("LABEL CHANGE ANALYSIS: Go Glean Product Feed History")
print("=" * 80)
print()
print(f"Feed snapshots found: {len(feed_files)}")
for f in feed_files:
    date = f.split('/')[-1].replace('.json', '')
    print(f"  - {date}")
print()

# Load earliest and latest snapshots
earliest_file = feed_files[0]
latest_file = feed_files[-1]

earliest_date = earliest_file.split('/')[-1].replace('.json', '')
latest_date = latest_file.split('/')[-1].replace('.json', '')

print(f"Comparing labels: {earliest_date} → {latest_date}")
print()

with open(earliest_file, 'r') as f:
    earliest_data = json.load(f)

with open(latest_file, 'r') as f:
    latest_data = json.load(f)

# Extract labels from product data
def get_labels(data):
    """Extract product_id -> label mapping from feed data"""
    labels = {}
    if 'products' in data:
        for product in data['products']:
            product_id = product.get('product_id') or product.get('id')
            custom_label = product.get('custom_label_0', '')
            if product_id and custom_label:
                labels[product_id] = custom_label.lower()
    return labels

earliest_labels = get_labels(earliest_data)
latest_labels = get_labels(latest_data)

print(f"Products in {earliest_date}: {len(earliest_labels)}")
print(f"Products in {latest_date}: {len(latest_labels)}")
print()

# Find products that changed labels
label_changes = {}
for product_id in earliest_labels:
    if product_id in latest_labels:
        if earliest_labels[product_id] != latest_labels[product_id]:
            label_changes[product_id] = {
                'from': earliest_labels[product_id],
                'to': latest_labels[product_id]
            }

print("=" * 80)
print(f"LABEL CHANGES: {earliest_date} → {latest_date}")
print("=" * 80)
print()
print(f"Total products with label changes: {len(label_changes)}")
print()

# Group changes by pattern
zombie_to_hero = []
zombie_to_sidekick = []
zombie_to_villain = []
hero_to_zombie = []
other_changes = []

for product_id, change in label_changes.items():
    if 'zombie' in change['from']:
        if 'hero' in change['to']:
            zombie_to_hero.append(product_id)
        elif 'sidekick' in change['to']:
            zombie_to_sidekick.append(product_id)
        elif 'villain' in change['to']:
            zombie_to_villain.append(product_id)
    elif 'hero' in change['from'] and 'zombie' in change['to']:
        hero_to_zombie.append(product_id)
    else:
        other_changes.append((product_id, change['from'], change['to']))

# Now load 30-day conversion data
print("Loading 30-day conversion data...")
with open('tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    ads_data = json.load(f)

# Aggregate conversions by product
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

products = defaultdict(lambda: {
    'item_id': '',
    'title': '',
    'conversions': 0.0,
    'conversions_value': 0.0,
    'spend': 0.0,
    'clicks': 0
})

for row in ads_data:
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
    products[item_id]['conversions'] += float(metrics.get('conversions', 0))
    products[item_id]['conversions_value'] += float(metrics.get('conversionsValue', 0))
    products[item_id]['spend'] += float(metrics.get('costMicros', 0)) / 1_000_000
    products[item_id]['clicks'] += int(metrics.get('clicks', 0))

print()
print("=" * 80)
print("🚨 ANSWER: Products That Were ZOMBIES and Got PROMOTED")
print("=" * 80)
print()

# Check zombie → hero promotions that also converted
zombie_to_hero_converters = []
for product_id in zombie_to_hero:
    if product_id in products and products[product_id]['conversions'] > 0:
        zombie_to_hero_converters.append({
            'id': product_id,
            'title': products[product_id]['title'],
            'conversions': products[product_id]['conversions'],
            'revenue': products[product_id]['conversions_value'],
            'spend': products[product_id]['spend'],
            'clicks': products[product_id]['clicks'],
            'label_change': f"zombie → heroes ({earliest_date} → {latest_date})"
        })

zombie_to_sidekick_converters = []
for product_id in zombie_to_sidekick:
    if product_id in products and products[product_id]['conversions'] > 0:
        zombie_to_sidekick_converters.append({
            'id': product_id,
            'title': products[product_id]['title'],
            'conversions': products[product_id]['conversions'],
            'revenue': products[product_id]['conversions_value'],
            'spend': products[product_id]['spend'],
            'clicks': products[product_id]['clicks'],
            'label_change': f"zombie → sidekicks ({earliest_date} → {latest_date})"
        })

print(f"Zombies → Heroes (that converted in last 30 days): {len(zombie_to_hero_converters)}")
print(f"Zombies → Sidekicks (that converted in last 30 days): {len(zombie_to_sidekick_converters)}")
print()

if zombie_to_hero_converters:
    print("ZOMBIES PROMOTED TO HEROES (with conversions):")
    print("-" * 80)
    for p in zombie_to_hero_converters:
        roas = (p['revenue'] / p['spend'] * 100) if p['spend'] > 0 else 0
        print(f"\n{p['title'][:70]}")
        print(f"  Product ID: {p['id']}")
        print(f"  Label change: {p['label_change']}")
        print(f"  30-day performance: {p['conversions']:.1f} conversions, £{p['revenue']:.2f} revenue, {roas:.0f}% ROAS")
        print(f"  Clicks: {p['clicks']}")

if zombie_to_sidekick_converters:
    print("\n" + "=" * 80)
    print("ZOMBIES PROMOTED TO SIDEKICKS (with conversions):")
    print("-" * 80)
    for p in zombie_to_sidekick_converters:
        roas = (p['revenue'] / p['spend'] * 100) if p['spend'] > 0 else 0
        print(f"\n{p['title'][:70]}")
        print(f"  Product ID: {p['id']}")
        print(f"  Label change: {p['label_change']}")
        print(f"  30-day performance: {p['conversions']:.1f} conversions, £{p['revenue']:.2f} revenue, {roas:.0f}% ROAS")
        print(f"  Clicks: {p['clicks']}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total label changes detected: {len(label_changes)}")
print(f"  - Zombie → Hero: {len(zombie_to_hero)}")
print(f"  - Zombie → Sidekick: {len(zombie_to_sidekick)}")
print(f"  - Zombie → Villain: {len(zombie_to_villain)}")
print(f"  - Hero → Zombie: {len(hero_to_zombie)}")
print(f"  - Other changes: {len(other_changes)}")
print()
print(f"Converting products that were promoted from Zombies:")
print(f"  - To Heroes: {len(zombie_to_hero_converters)}")
print(f"  - To Sidekicks: {len(zombie_to_sidekick_converters)}")
