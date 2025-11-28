#!/usr/bin/env python3
"""Check the structure of Go Glean data"""

import json

with open('/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/data/ads_go_glean_uk.json', 'r') as f:
    data = json.load(f)

print(f"Total rows: {len(data)}")
print()
print("First row keys:")
if data:
    for key in sorted(data[0].keys()):
        print(f"  {key}: {data[0][key]}")

    print("\n" + "="*80)
    print("Sample campaigns in data:")
    campaigns = set()
    for row in data[:1000]:  # Check first 1000 rows
        campaigns.add(row.get('campaign_name', ''))
    for campaign in sorted(campaigns):
        print(f"  {campaign}")

    print("\n" + "="*80)
    print("Sample custom_label_0 values:")
    labels = set()
    for row in data[:1000]:
        label = row.get('segments_product_custom_label0', '')
        if label:
            labels.add(label)
    for label in sorted(labels):
        print(f"  {label}")

    print("\n" + "="*80)
    print("Check for conversions:")
    conv_count = 0
    for row in data[:1000]:
        if float(row.get('metrics_conversions', 0)) > 0:
            conv_count += 1
    print(f"  Rows with conversions (first 1000): {conv_count}")
