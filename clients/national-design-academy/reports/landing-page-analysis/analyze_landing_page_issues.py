#!/usr/bin/env python3
"""Analyze landing page mismatches in Search campaigns"""

import csv
from collections import defaultdict

print("🔍 LANDING PAGE MISMATCH ANALYSIS")
print("="*70 + "\n")

# Read the clean report
file_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report3-search-landing-pages-clean-90d.csv'

with open(file_path, 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Define expected landing pages based on campaign type
diploma_page = 'https://www.nda.ac.uk/study/courses/diploma-interior-design'
degree_page = 'https://www.nda.ac.uk/study/courses/degrees-interior-design'

# Analyze mismatches
mismatches = []
diploma_campaigns_using_degree_page = []
degree_campaigns_using_diploma_page = []

for row in data:
    campaign = row['Campaign Name']
    ad_group = row['Ad Group Name']
    landing_page = row['Landing Page URL']
    impressions = int(row['Impressions'])
    cost = float(row['Cost (£)'].replace('£', '').replace(',', ''))
    
    # Check if Diploma campaign using Degree page
    if 'Diploma' in campaign and 'Degree' not in campaign:
        if 'degrees-interior-design' in landing_page or 'interior-design-degrees' in landing_page:
            diploma_campaigns_using_degree_page.append({
                'campaign': campaign,
                'ad_group': ad_group,
                'landing_page': landing_page,
                'impressions': impressions,
                'cost': cost
            })
    
    # Check if Degree campaign using Diploma page
    if 'Degree' in campaign and 'Diploma' not in campaign:
        if 'diploma-interior-design' in landing_page or 'interior-design-courses' in landing_page:
            if 'degrees' not in landing_page:
                degree_campaigns_using_diploma_page.append({
                    'campaign': campaign,
                    'ad_group': ad_group,
                    'landing_page': landing_page,
                    'impressions': impressions,
                    'cost': cost
                })

# Report findings
print("🚨 DIPLOMA CAMPAIGNS USING DEGREE LANDING PAGES")
print("-"*70)

if diploma_campaigns_using_degree_page:
    total_impressions = sum(x['impressions'] for x in diploma_campaigns_using_degree_page)
    total_cost = sum(x['cost'] for x in diploma_campaigns_using_degree_page)
    
    print(f"❌ Found {len(diploma_campaigns_using_degree_page)} ad groups with WRONG landing pages")
    print(f"💰 Total Cost: £{total_cost:,.2f}")
    print(f"👁️  Total Impressions: {total_impressions:,}\n")
    
    for item in diploma_campaigns_using_degree_page:
        print(f"Campaign: {item['campaign']}")
        print(f"  Ad Group: {item['ad_group']}")
        print(f"  ❌ WRONG: {item['landing_page']}")
        print(f"  ✅ SHOULD BE: {diploma_page}")
        print(f"  Cost: £{item['cost']:.2f} | Impressions: {item['impressions']:,}")
        print()
else:
    print("✅ No Diploma campaigns using Degree pages\n")

print("="*70 + "\n")
print("🚨 DEGREE CAMPAIGNS USING DIPLOMA LANDING PAGES")
print("-"*70)

if degree_campaigns_using_diploma_page:
    total_impressions = sum(x['impressions'] for x in degree_campaigns_using_diploma_page)
    total_cost = sum(x['cost'] for x in degree_campaigns_using_diploma_page)
    
    print(f"❌ Found {len(degree_campaigns_using_diploma_page)} ad groups with WRONG landing pages")
    print(f"💰 Total Cost: £{total_cost:,.2f}")
    print(f"👁️  Total Impressions: {total_impressions:,}\n")
    
    for item in degree_campaigns_using_diploma_page:
        print(f"Campaign: {item['campaign']}")
        print(f"  Ad Group: {item['ad_group']}")
        print(f"  ❌ WRONG: {item['landing_page']}")
        print(f"  ✅ SHOULD BE: {degree_page}")
        print(f"  Cost: £{item['cost']:.2f} | Impressions: {item['impressions']:,}")
        print()
else:
    print("✅ No Degree campaigns using Diploma pages\n")

print("="*70)
print("\n📊 SUMMARY")
print(f"Total Diploma→Degree mismatches: {len(diploma_campaigns_using_degree_page)}")
print(f"Total Degree→Diploma mismatches: {len(degree_campaigns_using_diploma_page)}")

if diploma_campaigns_using_degree_page or degree_campaigns_using_diploma_page:
    total_waste = sum(x['cost'] for x in diploma_campaigns_using_degree_page) + sum(x['cost'] for x in degree_campaigns_using_diploma_page)
    print(f"\n💸 Total wasted spend: £{total_waste:,.2f}")
    print("\n⚠️  ACTION REQUIRED: Fix landing page URLs in these ad groups")
else:
    print("\n✅ All landing pages correctly matched!")
