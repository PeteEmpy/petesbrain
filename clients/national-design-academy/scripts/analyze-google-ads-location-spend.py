#!/usr/bin/env python3
"""
Analyze NDA Google Ads Location Report to determine actual spend by geography
Compare against enrollment data analysis
"""

import csv
from collections import defaultdict

# Read the location report
print("📊 Reading Google Ads Location Report...")
print("=" * 70)

location_spend = defaultdict(float)
campaign_location_spend = {}

with open('/Users/administrator/Downloads/Location report.csv', 'r') as f:
    # Skip first 2 rows (title and date range)
    next(f)
    next(f)
    reader = csv.DictReader(f)

    for row in reader:
        location = row['Location']
        campaign = row['Campaign']
        cost_str = row['Cost']

        # Skip Google Ads summary rows (e.g., "Total: Account", "Total: Locations")
        if location.startswith('Total:'):
            continue

        # Parse cost (remove commas)
        try:
            cost = float(cost_str.replace(',', ''))
        except (ValueError, AttributeError):
            cost = 0.0

        if cost > 0:
            location_spend[location] += cost

            # Track by campaign + location
            key = f"{campaign}|{location}"
            campaign_location_spend[key] = cost

# Categorize locations into regions matching NDA campaign structure
print("\n🌍 SPEND BY LOCATION (Sept 1 - Dec 16, 2025)")
print("=" * 70)

uk_spend = 0
india_spend = 0
uae_spend = 0
gcc_spend = 0  # Oman, Saudi Arabia, Bahrain, Kuwait, Qatar
europe_spend = 0
us_canada_spend = 0
rotw_spend = 0

# Europe countries
europe_countries = [
    'Austria', 'France', 'Netherlands', 'Malta', 'Germany', 'Sweden',
    'Switzerland', 'Belgium', 'Italy', 'Spain', 'Denmark', 'Norway',
    'Poland', 'Ireland', 'Hungary', 'Romania', 'Serbia', 'Cyprus'
]

# GCC countries
gcc_countries = ['Oman', 'Saudi Arabia', 'Bahrain', 'Kuwait', 'Qatar']

# Print top locations by spend
sorted_locations = sorted(location_spend.items(), key=lambda x: x[1], reverse=True)

print("\n📍 Top 30 Locations by Spend:")
print(f"{'Location':<40} {'Spend':>12}")
print("-" * 54)

for i, (location, spend) in enumerate(sorted_locations[:30], 1):
    print(f"{i:2}. {location:<37} £{spend:>10,.2f}")

    # Categorize
    if 'United Kingdom' in location or location == 'United Kingdom':
        uk_spend += spend
    elif 'India' in location or location == 'India':
        india_spend += spend
    elif 'United Arab Emirates' in location or location == 'United Arab Emirates' or 'UAE' in location or 'Abu Dhabi' in location or 'Dubai' in location:
        uae_spend += spend
    elif any(gcc in location for gcc in gcc_countries):
        gcc_spend += spend
    elif any(euro in location for euro in europe_countries):
        europe_spend += spend
    elif 'United States' in location or location == 'United States' or 'Canada' in location or location == 'Canada':
        us_canada_spend += spend
    else:
        rotw_spend += spend

# Process remaining locations (below top 30)
for location, spend in sorted_locations[30:]:
    if 'United Kingdom' in location or location == 'United Kingdom':
        uk_spend += spend
    elif 'India' in location or location == 'India':
        india_spend += spend
    elif 'United Arab Emirates' in location or location == 'United Arab Emirates' or 'UAE' in location or 'Abu Dhabi' in location or 'Dubai' in location:
        uae_spend += spend
    elif any(gcc in location for gcc in gcc_countries):
        gcc_spend += spend
    elif any(euro in location for euro in europe_countries):
        europe_spend += spend
    elif 'United States' in location or location == 'United States' or 'Canada' in location or location == 'Canada':
        us_canada_spend += spend
    else:
        rotw_spend += spend

total_spend = sum(location_spend.values())
international_spend = total_spend - uk_spend

print("\n" + "=" * 70)
print("📊 SPEND BY REGIONAL GROUPING")
print("=" * 70)

regions = [
    ('UK', uk_spend),
    ('UAE', uae_spend),
    ('GCC (Oman/SA/BH/KW/QA)', gcc_spend),
    ('Europe', europe_spend),
    ('India', india_spend),
    ('US/Canada', us_canada_spend),
    ('ROTW (Other)', rotw_spend)
]

print(f"\n{'Region':<30} {'Spend':>12} {'% of Total':>10} {'% of Intl':>10}")
print("-" * 64)

for region, spend in sorted(regions, key=lambda x: x[1], reverse=True):
    pct_total = (spend / total_spend * 100) if total_spend > 0 else 0
    pct_intl = (spend / international_spend * 100) if international_spend > 0 and region != 'UK' else 0

    if region == 'UK':
        print(f"{region:<30} £{spend:>10,.2f}  {pct_total:>8.1f}%  {'N/A':>9}")
    else:
        print(f"{region:<30} £{spend:>10,.2f}  {pct_total:>8.1f}%  {pct_intl:>8.1f}%")

print("-" * 64)
print(f"{'TOTAL':<30} £{total_spend:>10,.2f}  {'100.0%':>9}  {'-':>9}")
print(f"{'UK':<30} £{uk_spend:>10,.2f}  {(uk_spend/total_spend*100):>8.1f}%  {'-':>9}")
print(f"{'International':<30} £{international_spend:>10,.2f}  {(international_spend/total_spend*100):>8.1f}%  {'100.0%':>9}")

print("\n" + "=" * 70)
print("🔍 COMPARISON: Google Ads Location Data vs Campaign-Level Analysis")
print("=" * 70)

print("\n📌 Original Analysis (Campaign-Level Aggregation):")
print("   UK:         £57,917  (46.6%)")
print("   India:      £7,394   (5.9%)")
print("   UAE:        £20,311  (16.3%)")
print("   GCC:        £14,801  (11.9%)")
print("   Europe:     £2,690   (2.2%)")
print("   US/Canada:  £8,428   (6.8%)")
print("   ROTW:       £12,051  (9.7%)")
print("   International: £66,345 (53.4%)")
print("   TOTAL:      £124,262")

print("\n📌 Location Report Analysis (User-Level Geography):")
print(f"   UK:         £{uk_spend:,.0f}  ({uk_spend/total_spend*100:.1f}%)")
print(f"   India:      £{india_spend:,.0f}   ({india_spend/total_spend*100:.1f}%)")
print(f"   UAE:        £{uae_spend:,.0f}  ({uae_spend/total_spend*100:.1f}%)")
print(f"   GCC:        £{gcc_spend:,.0f}  ({gcc_spend/total_spend*100:.1f}%)")
print(f"   Europe:     £{europe_spend:,.0f}   ({europe_spend/total_spend*100:.1f}%)")
print(f"   US/Canada:  £{us_canada_spend:,.0f}   ({us_canada_spend/total_spend*100:.1f}%)")
print(f"   ROTW:       £{rotw_spend:,.0f}  ({rotw_spend/total_spend*100:.1f}%)")
print(f"   International: £{international_spend:,.0f} ({international_spend/total_spend*100:.1f}%)")
print(f"   TOTAL:      £{total_spend:,.0f}")

print("\n" + "=" * 70)
print("✅ Analysis complete - data saved for comparison")
print("=" * 70)
