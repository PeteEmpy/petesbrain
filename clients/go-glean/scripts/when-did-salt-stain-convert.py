#!/usr/bin/env python3
"""
Check when Salt Stain 5L actually got its conversions and clicks
to see if it recently crossed the >28 clicks threshold
"""

import json
from datetime import datetime
from collections import defaultdict

# Load 30-day data
with open('tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    data = json.load(f)

# Salt Stain 5L product ID
target_id = 'shopify_gb_8399314354453_45692891857173'

# Group by date
by_date = defaultdict(lambda: {
    'clicks': 0,
    'conversions': 0.0,
    'spend': 0.0,
    'revenue': 0.0
})

for row in data:
    item_id = row.get('segments', {}).get('productItemId', '')
    if item_id != target_id:
        continue

    date = row.get('segments', {}).get('date', '')
    if not date:
        continue

    metrics = row.get('metrics', {})
    by_date[date]['clicks'] += int(metrics.get('clicks', 0))
    by_date[date]['conversions'] += float(metrics.get('conversions', 0))
    by_date[date]['spend'] += float(metrics.get('costMicros', 0)) / 1_000_000
    by_date[date]['revenue'] += float(metrics.get('conversionsValue', 0))

print("=" * 80)
print("Salt Stain & White Efflorescence Remover 5L - Daily Performance")
print("=" * 80)
print()

dates_sorted = sorted(by_date.keys())
cumulative_clicks = 0
cumulative_conversions = 0.0
cumulative_spend = 0.0
cumulative_revenue = 0.0

print(f"{'Date':<12} {'Clicks':>8} {'Conv':>6} {'Spend':>8} {'Revenue':>8} | {'Cum Clicks':>10} {'Cum Conv':>8} {'ROAS':>6}")
print("-" * 80)

for date in dates_sorted:
    day = by_date[date]
    cumulative_clicks += day['clicks']
    cumulative_conversions += day['conversions']
    cumulative_spend += day['spend']
    cumulative_revenue += day['revenue']

    roas = (cumulative_revenue / cumulative_spend * 100) if cumulative_spend > 0 else 0

    threshold_marker = "✓" if cumulative_clicks > 28 else " "

    print(f"{date:<12} {day['clicks']:>8} {day['conversions']:>6.1f} £{day['spend']:>6.2f} £{day['revenue']:>6.2f} | {cumulative_clicks:>10} {cumulative_conversions:>8.1f} {roas:>5.0f}% {threshold_marker}")

print()
print("=" * 80)
print("ANALYSIS")
print("=" * 80)
print()
print(f"Total 30-day performance:")
print(f"  Clicks: {cumulative_clicks}")
print(f"  Conversions: {cumulative_conversions:.1f}")
print(f"  ROAS: {roas:.0f}%")
print()

# Find when it crossed >28 threshold
threshold_date = None
for date in dates_sorted:
    cumulative = sum(by_date[d]['clicks'] for d in dates_sorted if d <= date)
    if cumulative > 28 and threshold_date is None:
        threshold_date = date
        break

if threshold_date:
    print(f"✅ Crossed >28 clicks threshold on: {threshold_date}")

    # Calculate days since threshold
    threshold_dt = datetime.strptime(threshold_date, '%Y-%m-%d')
    today = datetime.now()
    days_since = (today - threshold_dt).days

    print(f"   Days since crossing threshold: {days_since} days")
    print()
    print("INTERPRETATION:")
    print(f"  - Product has only been Hero-eligible for {days_since} days")
    print(f"  - Product Hero may run weekly/bi-weekly label updates")
    print(f"  - If last update was before {threshold_date}, product wouldn't have been promoted yet")
else:
    print("❌ Has not crossed >28 clicks threshold yet (currently at {cumulative_clicks})")
    print()
    print("INTERPRETATION:")
    print("  - Product does NOT meet Hero criteria (needs >28 clicks)")
    print("  - Should remain as Zombie until it crosses threshold")
