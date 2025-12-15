#!/usr/bin/env python3
"""Test product feed enrichment"""
import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
from analyzer import normalize_product_id

# Load ads data
ads_file = Path('data/ads_brightminds.json')
ads_data = json.load(open(ads_file))
print(f"Loaded {len(ads_data)} ads data records")

# Get unique product IDs from ads data
ads_product_ids = set()
for record in ads_data[:100]:  # Sample first 100
    pid = record.get('segments', {}).get('product_item_id', '')
    if pid:
        normalized = normalize_product_id(pid)
        ads_product_ids.add(normalized)

print(f"\nSample ads product IDs (first 10):")
for pid in list(ads_product_ids)[:10]:
    print(f"  {pid}")

# Load product feed data
feed_file = Path('data/product_feed_history/BrightMinds/2025-12-14.json')
feed_data = json.load(open(feed_file))
products = feed_data['products']
print(f"\nLoaded {len(products)} products from feed")

# Normalize feed product IDs
feed_dict = {}
for product in products:
    pid = product.get('product_id', '')
    normalized = normalize_product_id(pid)
    if normalized:
        feed_dict[normalized] = product

print(f"\nNormalized {len(feed_dict)} feed products")

# Check match rate
matches = 0
for ads_pid in ads_product_ids:
    if ads_pid in feed_dict:
        matches += 1

print(f"\nMatch rate: {matches}/{len(ads_product_ids)} ({matches/len(ads_product_ids)*100:.1f}%)")

# Check out of stock products in feed
avail_counts = Counter([p.get('availability') for p in products])
print(f"\nFeed availability distribution:")
for status, count in avail_counts.items():
    print(f"  {status}: {count}")

# Check if any out-of-stock products are in the ads data
out_of_stock_in_ads = []
for product in products:
    if product.get('availability') == 'out of stock':
        pid = normalize_product_id(product.get('product_id', ''))
        if pid in ads_product_ids:
            out_of_stock_in_ads.append({
                'id': pid,
                'title': product.get('title', '')
            })

print(f"\nOut-of-stock products that appear in ads data (sample of 10):")
for p in out_of_stock_in_ads[:10]:
    print(f"  {p['id']}: {p['title'][:60]}")
