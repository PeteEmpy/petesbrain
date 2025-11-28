import json

# Campaign performance data from Google Ads API (YTD Aug-Oct 2025)
campaigns = [
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "conversions": 197.52, "spend": 18694.84, "market": "UK", "type": "Search"},
    {"name": "NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4", "conversions": 145.60, "spend": 5540.02, "market": "UK", "type": "PMax"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "conversions": 26.00, "spend": 7205.07, "market": "International", "type": "PMax"},
    {"name": "NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden Split 12/3 No Target 24/4", "conversions": 21.00, "spend": 1364.99, "market": "International", "type": "Search"},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "conversions": 20.26, "spend": 3335.22, "market": "International", "type": "PMax"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5", "conversions": 17.27, "spend": 3370.28, "market": "International", "type": "PMax"},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "conversions": 16.78, "spend": 2312.33, "market": "UK", "type": "Search"},
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "conversions": 16.75, "spend": 2500.95, "market": "International", "type": "Search"},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "conversions": 16.00, "spend": 4434.06, "market": "International", "type": "Search"},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing 17/3 No Target 30/4 New Customers 1/8", "conversions": 16.00, "spend": 6085.14, "market": "UK", "type": "PMax"},
    {"name": "NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9", "conversions": 12.19, "spend": 2433.98, "market": "International", "type": "PMax"},
    {"name": "NDA | Search | Interior Design Degree- UK 120 No Target 24/4", "conversions": 11.51, "spend": 6973.75, "market": "UK", "type": "Search"},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "conversions": 8.86, "spend": 3286.67, "market": "International", "type": "Search"},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "conversions": 7.50, "spend": 7185.15, "market": "International", "type": "Search"},
    {"name": "NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3", "conversions": 6.25, "spend": 1828.08, "market": "International", "type": "Search"},
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "conversions": 6.00, "spend": 1517.35, "market": "UK", "type": "Search"},
    {"name": "NDA | Search | Interior Design Diploma - India Ai Max 19/9", "conversions": 5.59, "spend": 2319.65, "market": "International", "type": "Search"},
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5", "conversions": 3.00, "spend": 2019.55, "market": "International", "type": "PMax"},
    {"name": "NDA | Search | Brand - UAE  No Target 7/7", "conversions": 2.50, "spend": 1177.48, "market": "International", "type": "Search"},
    {"name": "NDA | UAE | Search | Interior Design Degree No Target", "conversions": 2.00, "spend": 3493.10, "market": "International", "type": "Search"},
    {"name": "NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4", "conversions": 2.00, "spend": 1101.22, "market": "International", "type": "PMax"},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "conversions": 1.37, "spend": 908.38, "market": "International", "type": "Search"},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "conversions": 1.16, "spend": 906.96, "market": "UK", "type": "Search"},
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "conversions": 1.00, "spend": 911.80, "market": "UK", "type": "Search"},
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "conversions": 1.00, "spend": 827.84, "market": "UK", "type": "Search"},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "conversions": 1.00, "spend": 2108.53, "market": "International", "type": "Search"},
    {"name": "NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target", "conversions": 0.50, "spend": 1144.68, "market": "International", "type": "PMax"},
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "conversions": 0.15, "spend": 1825.03, "market": "UK", "type": "Search"},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "conversions": 0.09, "spend": 903.66, "market": "International", "type": "Search"},
    # Zero conversion campaigns (PAUSE THESE)
    {"name": "NDA | EUR | Search | Landscape Design Courses 65", "conversions": 0.00, "spend": 0.12, "market": "International", "type": "Search"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search |  Landscape Design Diplomas No Target", "conversions": 0.00, "spend": 902.94, "market": "International", "type": "Search"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250 No Target 22/9", "conversions": 0.00, "spend": 365.36, "market": "International", "type": "Search"},
    {"name": "NDA | Low Intl | Search | Retail Design Degree No Target", "conversions": 0.00, "spend": 768.21, "market": "International", "type": "Search"},
    {"name": "NDA | Low Intl | Search | Curtain Making Course No Target", "conversions": 0.00, "spend": 38.97, "market": "International", "type": "Search"},
    {"name": "NDA | IN | Search | Interior Design Degree No Target", "conversions": 0.00, "spend": 1414.79, "market": "International", "type": "Search"},
    {"name": "NDA | P Max | Interior Design Degree - USA/Canada 250 Split 11/3", "conversions": 0.00, "spend": 908.95, "market": "International", "type": "PMax"},
    {"name": "NDA | Search | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 Split 11/3 No Target", "conversions": 0.00, "spend": 1943.60, "market": "International", "type": "Search"},
    {"name": "NDA | Search | Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135 Split 11/3", "conversions": 0.00, "spend": 1373.46, "market": "International", "type": "Search"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "conversions": 0.00, "spend": 2017.12, "market": "International", "type": "PMax"},
]

# Calculate metrics for each campaign
for c in campaigns:
    c['cpa'] = c['spend'] / c['conversions'] if c['conversions'] > 0 else 9999
    c['efficiency_score'] = c['conversions'] / c['spend'] * 1000 if c['spend'] > 0 else 0  # Conversions per £1000 spend

# Separate into tiers
high_performers = [c for c in campaigns if c['conversions'] >= 10]
medium_performers = [c for c in campaigns if 1 <= c['conversions'] < 10]
low_performers = [c for c in campaigns if 0 < c['conversions'] < 1]
zero_performers = [c for c in campaigns if c['conversions'] == 0]

print("="*90)
print("NDA CAMPAIGN BUDGET RECOMMENDATIONS - YTD PERFORMANCE ANALYSIS")
print("="*90)

total_spend = sum(c['spend'] for c in campaigns)
total_conversions = sum(c['conversions'] for c in campaigns)
overall_cpa = total_spend / total_conversions

print(f"\nCURRENT PERFORMANCE (Aug-Oct 2025):")
print(f"  Total Spend: £{total_spend:,.2f}")
print(f"  Total Conversions: {total_conversions:.1f}")
print(f"  Overall CPA: £{overall_cpa:,.2f}")

uk_spend = sum(c['spend'] for c in campaigns if c['market'] == 'UK')
intl_spend = sum(c['spend'] for c in campaigns if c['market'] == 'International')
uk_conversions = sum(c['conversions'] for c in campaigns if c['market'] == 'UK')
intl_conversions = sum(c['conversions'] for c in campaigns if c['market'] == 'International')

print(f"\n  UK: £{uk_spend:,.2f} ({uk_spend/total_spend*100:.1f}%) | {uk_conversions:.0f} conversions | £{uk_spend/uk_conversions:.2f} CPA")
print(f"  International: £{intl_spend:,.2f} ({intl_spend/total_spend*100:.1f}%) | {intl_conversions:.0f} conversions | £{intl_spend/intl_conversions:.2f} CPA")

print("\n" + "="*90)
print("HIGH PERFORMERS (10+ conversions) - INVEST MORE")
print("="*90)
print(f"{'Campaign':<75} {'Convs':>8} {'Spend':>12} {'CPA':>10}")
print("-" * 90)

high_uk_spend = 0
high_intl_spend = 0

for c in sorted(high_performers, key=lambda x: x['conversions'], reverse=True):
    print(f"{c['name'][:75]:<75} {c['conversions']:>8.1f} £{c['spend']:>10,.2f} £{c['cpa']:>8,.2f}")
    if c['market'] == 'UK':
        high_uk_spend += c['spend']
    else:
        high_intl_spend += c['spend']

print(f"\nSubtotal: {len(high_performers)} campaigns | {sum(c['conversions'] for c in high_performers):.0f} conversions | £{sum(c['spend'] for c in high_performers):,.2f}")
print(f"UK: £{high_uk_spend:,.2f} | International: £{high_intl_spend:,.2f}")

print("\n" + "="*90)
print("MEDIUM PERFORMERS (1-9 conversions) - MAINTAIN OR TEST")
print("="*90)
print(f"{'Campaign':<75} {'Convs':>8} {'Spend':>12} {'CPA':>10}")
print("-" * 90)

for c in sorted(medium_performers, key=lambda x: x['conversions'], reverse=True):
    print(f"{c['name'][:75]:<75} {c['conversions']:>8.1f} £{c['spend']:>10,.2f} £{c['cpa']:>8,.2f}")

print(f"\nSubtotal: {len(medium_performers)} campaigns | {sum(c['conversions'] for c in medium_performers):.0f} conversions | £{sum(c['spend'] for c in medium_performers):,.2f}")

print("\n" + "="*90)
print("LOW PERFORMERS (<1 conversion) - PAUSE OR REDUCE DRASTICALLY")
print("="*90)
print(f"{'Campaign':<75} {'Convs':>8} {'Spend':>12} {'CPA':>10}")
print("-" * 90)

for c in low_performers:
    print(f"{c['name'][:75]:<75} {c['conversions']:>8.2f} £{c['spend']:>10,.2f} £{c['cpa']:>8,.2f}")

print(f"\nSubtotal: {len(low_performers)} campaigns | {sum(c['conversions'] for c in low_performers):.1f} conversions | £{sum(c['spend'] for c in low_performers):,.2f}")

print("\n" + "="*90)
print("ZERO PERFORMERS (0 conversions) - PAUSE IMMEDIATELY ❌")
print("="*90)
print(f"{'Campaign':<75} {'Convs':>8} {'Spend':>12}")
print("-" * 90)

for c in zero_performers:
    print(f"{c['name'][:75]:<75} {c['conversions']:>8.0f} £{c['spend']:>10,.2f}")

print(f"\nSubtotal: {len(zero_performers)} campaigns | {sum(c['spend'] for c in zero_performers):,.2f} WASTED")

print("\n" + "="*90)

# Calculate recommended budget
print("\nBUDGET RECOMMENDATION STRATEGY:")
print("="*90)

# Target: 60% UK, 40% International (maintaining UK bias but allocating based on performance)
target_monthly_budget = 30000  # Example target (current is £36k/month)

print(f"\nTARGET MONTHLY BUDGET: £{target_monthly_budget:,}")
print(f"  UK allocation: 60% = £{target_monthly_budget * 0.6:,.2f}")
print(f"  International allocation: 40% = £{target_monthly_budget * 0.4:,.2f}")

# Allocate based on conversion share within each market
uk_high_performers = [c for c in high_performers if c['market'] == 'UK']
intl_high_performers = [c for c in high_performers if c['market'] == 'International']

uk_high_conversions = sum(c['conversions'] for c in uk_high_performers)
intl_high_conversions = sum(c['conversions'] for c in intl_high_performers)

print("\n" + "="*90)
print("RECOMMENDED MONTHLY BUDGETS BY CAMPAIGN (High Performers Only)")
print("="*90)
print(f"{'Campaign':<75} {'Current':>12} {'Recommended':>12}")
print("-" * 90)

uk_budget_pool = target_monthly_budget * 0.6
intl_budget_pool = target_monthly_budget * 0.4

print("\nUK CAMPAIGNS:")
for c in sorted(uk_high_performers, key=lambda x: x['conversions'], reverse=True):
    current_monthly = c['spend'] / 3  # YTD is 3 months
    conversion_share = c['conversions'] / uk_high_conversions if uk_high_conversions > 0 else 0
    recommended_monthly = uk_budget_pool * conversion_share
    change_pct = ((recommended_monthly - current_monthly) / current_monthly * 100) if current_monthly > 0 else 0
    
    print(f"{c['name'][:75]:<75} £{current_monthly:>10,.0f} £{recommended_monthly:>10,.0f} ({change_pct:+.0f}%)")

print("\nINTERNATIONAL CAMPAIGNS:")
for c in sorted(intl_high_performers, key=lambda x: x['conversions'], reverse=True):
    current_monthly = c['spend'] / 3
    conversion_share = c['conversions'] / intl_high_conversions if intl_high_conversions > 0 else 0
    recommended_monthly = intl_budget_pool * conversion_share
    change_pct = ((recommended_monthly - current_monthly) / current_monthly * 100) if current_monthly > 0 else 0
    
    print(f"{c['name'][:75]:<75} £{current_monthly:>10,.0f} £{recommended_monthly:>10,.0f} ({change_pct:+.0f}%)")

print("\n" + "="*90)
print("IMMEDIATE ACTIONS:")
print("="*90)

print(f"\n1. PAUSE {len(zero_performers)} campaigns with 0 conversions:")
print(f"   Saving: £{sum(c['spend'] for c in zero_performers)/3:,.2f}/month")

print(f"\n2. REDUCE low performers (<1 conversion) by 75%:")
print(f"   Current: £{sum(c['spend'] for c in low_performers)/3:,.2f}/month")
print(f"   Saving: £{sum(c['spend'] for c in low_performers)/3 * 0.75:,.2f}/month")

print(f"\n3. REALLOCATE budget to high performers (10+ conversions)")

total_savings = (sum(c['spend'] for c in zero_performers) + sum(c['spend'] for c in low_performers) * 0.75) / 3

print(f"\nTOTAL MONTHLY SAVINGS: £{total_savings:,.2f}")
print(f"NEW MONTHLY SPEND: £{total_spend/3 - total_savings:,.2f} (from £{total_spend/3:,.2f})")
print(f"REDUCTION: {total_savings/(total_spend/3)*100:.1f}%")

print("\n" + "="*90)

