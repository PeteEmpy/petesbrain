#!/usr/bin/env python3
"""Complete landing page mismatch analysis for NDA"""

import csv

print("🔍 NDA LANDING PAGE MISMATCH ANALYSIS")
print("="*80 + "\n")
print("RULE: Diploma campaigns → Diploma pages ONLY")
print("      Degree campaigns → Degree pages ONLY")
print("="*80 + "\n")

file_path = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report3-search-landing-pages-clean-90d.csv'

with open(file_path, 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Define correct pages
diploma_pages = [
    'https://www.nda.ac.uk/study/courses/diploma-interior-design',
    'https://www.nda.ac.uk/study/interior-design-courses'
]

degree_pages = [
    'https://www.nda.ac.uk/study/courses/degrees-interior-design',
    'https://www.nda.ac.uk/study/interior-design-degrees'
]

# Find all mismatches
diploma_campaign_wrong_pages = []
degree_campaign_wrong_pages = []

for row in data:
    campaign = row['Campaign Name']
    ad_group = row['Ad Group Name']
    landing_page = row['Landing Page URL']
    impressions = int(row['Impressions'])
    clicks = int(row['Clicks'])
    cost = float(row['Cost (£)'].replace('£', '').replace(',', ''))
    conversions = float(row['Conversions'])
    
    # Check Diploma campaigns
    if 'Diploma' in campaign and 'Degree' not in campaign:
        # Should ONLY use diploma pages
        if landing_page not in diploma_pages:
            if landing_page in degree_pages:
                diploma_campaign_wrong_pages.append({
                    'campaign': campaign,
                    'ad_group': ad_group,
                    'current_page': landing_page,
                    'should_be': diploma_pages[0],
                    'impressions': impressions,
                    'clicks': clicks,
                    'cost': cost,
                    'conversions': conversions
                })
    
    # Check Degree campaigns
    if 'Degree' in campaign and 'Diploma' not in campaign:
        # Should ONLY use degree pages
        if landing_page not in degree_pages:
            if landing_page in diploma_pages:
                degree_campaign_wrong_pages.append({
                    'campaign': campaign,
                    'ad_group': ad_group,
                    'current_page': landing_page,
                    'should_be': degree_pages[0],
                    'impressions': impressions,
                    'clicks': clicks,
                    'cost': cost,
                    'conversions': conversions
                })

# Report Diploma campaigns with wrong pages
print("🚨 DIPLOMA CAMPAIGNS USING DEGREE PAGES (WRONG)")
print("-"*80)

if diploma_campaign_wrong_pages:
    total_cost = sum(x['cost'] for x in diploma_campaign_wrong_pages)
    total_impressions = sum(x['impressions'] for x in diploma_campaign_wrong_pages)
    total_clicks = sum(x['clicks'] for x in diploma_campaign_wrong_pages)
    total_conversions = sum(x['conversions'] for x in diploma_campaign_wrong_pages)
    
    print(f"❌ Found {len(diploma_campaign_wrong_pages)} ad groups with WRONG landing pages\n")
    
    for i, item in enumerate(diploma_campaign_wrong_pages, 1):
        print(f"{i}. Campaign: {item['campaign']}")
        print(f"   Ad Group: {item['ad_group']}")
        print(f"   ❌ Current: {item['current_page']}")
        print(f"   ✅ Should be: {item['should_be']}")
        print(f"   📊 Stats: £{item['cost']:.2f} | {item['impressions']:,} impr | {item['clicks']} clicks | {item['conversions']:.2f} conv")
        print()
    
    print(f"💰 TOTAL IMPACT:")
    print(f"   Cost: £{total_cost:,.2f}")
    print(f"   Impressions: {total_impressions:,}")
    print(f"   Clicks: {total_clicks:,}")
    print(f"   Conversions: {total_conversions:.2f}")
    print()
else:
    print("✅ No Diploma campaigns using Degree pages\n")

print("="*80 + "\n")

# Report Degree campaigns with wrong pages
print("🚨 DEGREE CAMPAIGNS USING DIPLOMA PAGES (WRONG)")
print("-"*80)

if degree_campaign_wrong_pages:
    total_cost = sum(x['cost'] for x in degree_campaign_wrong_pages)
    total_impressions = sum(x['impressions'] for x in degree_campaign_wrong_pages)
    total_clicks = sum(x['clicks'] for x in degree_campaign_wrong_pages)
    total_conversions = sum(x['conversions'] for x in degree_campaign_wrong_pages)
    
    print(f"❌ Found {len(degree_campaign_wrong_pages)} ad groups with WRONG landing pages\n")
    
    for i, item in enumerate(degree_campaign_wrong_pages, 1):
        print(f"{i}. Campaign: {item['campaign']}")
        print(f"   Ad Group: {item['ad_group']}")
        print(f"   ❌ Current: {item['current_page']}")
        print(f"   ✅ Should be: {item['should_be']}")
        print(f"   📊 Stats: £{item['cost']:.2f} | {item['impressions']:,} impr | {item['clicks']} clicks | {item['conversions']:.2f} conv")
        print()
    
    print(f"💰 TOTAL IMPACT:")
    print(f"   Cost: £{total_cost:,.2f}")
    print(f"   Impressions: {total_impressions:,}")
    print(f"   Clicks: {total_clicks:,}")
    print(f"   Conversions: {total_conversions:.2f}")
    print()
else:
    print("✅ No Degree campaigns using Diploma pages\n")

print("="*80)
print("\n📋 FINAL SUMMARY")
print(f"   Diploma→Degree mismatches: {len(diploma_campaign_wrong_pages)} ad groups")
print(f"   Degree→Diploma mismatches: {len(degree_campaign_wrong_pages)} ad groups")

if diploma_campaign_wrong_pages or degree_campaign_wrong_pages:
    all_wrong = diploma_campaign_wrong_pages + degree_campaign_wrong_pages
    total_waste = sum(x['cost'] for x in all_wrong)
    print(f"\n   💸 Total affected spend: £{total_waste:,.2f}")
    print(f"\n   ⚠️  ACTION REQUIRED: Fix these {len(all_wrong)} ad group landing pages")
else:
    print("\n   ✅ All landing pages correctly matched!")

print("\n" + "="*80)
