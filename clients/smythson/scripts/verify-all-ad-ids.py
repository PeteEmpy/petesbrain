#!/usr/bin/env python3
"""Extract all Ad IDs from our export and check which exist"""

import csv

# Read all Ad IDs from our export
with open('rsa-uk-editor-exact-20251215.csv', 'r') as f:
    reader = csv.DictReader(f)
    ad_ids = []
    for row in reader:
        ad_ids.append(row['Ad ID'])

print("Ad IDs in our UK export:")
print("="*50)
for i, ad_id in enumerate(ad_ids, 1):
    print(f"{i:2}. {ad_id}")

print("\n" + "="*50)
print("Copy this GAQL query to check if they ALL exist:")
print("\nSELECT ad_group_ad.ad.id, campaign.name, ad_group.name")
print("FROM ad_group_ad")
print("WHERE ad_group_ad.ad.id IN (")
for i, ad_id in enumerate(ad_ids):
    if i < len(ad_ids) - 1:
        print(f"    {ad_id},")
    else:
        print(f"    {ad_id}")
print(")")