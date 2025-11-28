# Using October actual spend as baseline

# October 2025 actual monthly spend
october_spend = 39996.40

# Campaign performance data (YTD Aug-Oct, so need to adjust to October weighting)
# For simplicity, I'll use the proportions from YTD but apply to October actual spend

campaigns = [
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "conversions": 197.52, "ytd_spend": 18694.84, "market": "UK"},
    {"name": "NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4", "conversions": 145.60, "ytd_spend": 5540.02, "market": "UK"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "conversions": 26.00, "ytd_spend": 7205.07, "market": "International"},
    {"name": "NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden", "conversions": 21.00, "ytd_spend": 1364.99, "market": "International"},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "conversions": 20.26, "ytd_spend": 3335.22, "market": "International"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5", "conversions": 17.27, "ytd_spend": 3370.28, "market": "International"},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "conversions": 16.78, "ytd_spend": 2312.33, "market": "UK"},
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "conversions": 16.75, "ytd_spend": 2500.95, "market": "International"},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "conversions": 16.00, "ytd_spend": 4434.06, "market": "International"},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing", "conversions": 16.00, "ytd_spend": 6085.14, "market": "UK"},
    {"name": "NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9", "conversions": 12.19, "ytd_spend": 2433.98, "market": "International"},
    {"name": "NDA | Search | Interior Design Degree- UK 120 No Target 24/4", "conversions": 11.51, "ytd_spend": 6973.75, "market": "UK"},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "conversions": 8.86, "ytd_spend": 3286.67, "market": "International"},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "conversions": 7.50, "ytd_spend": 7185.15, "market": "International"},
    {"name": "NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3", "conversions": 6.25, "ytd_spend": 1828.08, "market": "International"},
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "conversions": 6.00, "ytd_spend": 1517.35, "market": "UK"},
    {"name": "NDA | Search | Interior Design Diploma - India Ai Max 19/9", "conversions": 5.59, "ytd_spend": 2319.65, "market": "International"},
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada", "conversions": 3.00, "ytd_spend": 2019.55, "market": "International"},
    {"name": "NDA | Search | Brand - UAE  No Target 7/7", "conversions": 2.50, "ytd_spend": 1177.48, "market": "International"},
    {"name": "NDA | UAE | Search | Interior Design Degree No Target", "conversions": 2.00, "ytd_spend": 3493.10, "market": "International"},
    {"name": "NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4", "conversions": 2.00, "ytd_spend": 1101.22, "market": "International"},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "conversions": 1.37, "ytd_spend": 908.38, "market": "International"},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "conversions": 1.16, "ytd_spend": 906.96, "market": "UK"},
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "conversions": 1.00, "ytd_spend": 911.80, "market": "UK"},
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "conversions": 1.00, "ytd_spend": 827.84, "market": "UK"},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "conversions": 1.00, "ytd_spend": 2108.53, "market": "International"},
    {"name": "NDA | P Max | Interior Design Degree - MENA", "conversions": 0.50, "ytd_spend": 1144.68, "market": "International"},
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "conversions": 0.15, "ytd_spend": 1825.03, "market": "UK"},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "conversions": 0.09, "ytd_spend": 903.66, "market": "International"},
    # Zero performers
    {"name": "Zero-conversion campaigns (10 total)", "conversions": 0.00, "ytd_spend": 9733.52, "market": "International"},
]

# Scale YTD spend to October equivalent
ytd_total = sum(c['ytd_spend'] for c in campaigns)
scale_factor = october_spend / (ytd_total / 3)  # YTD is 3 months

for c in campaigns:
    c['oct_spend'] = (c['ytd_spend'] / 3) * scale_factor
    c['cpa'] = c['ytd_spend'] / c['conversions'] if c['conversions'] > 0 else 9999

# Identify action categories
zero_conv = [c for c in campaigns if c['conversions'] == 0]
very_low = [c for c in campaigns if 0 < c['conversions'] < 1]
high_cpa = [c for c in campaigns if c['conversions'] >= 1 and c['cpa'] > 500]

print("="*90)
print("NDA BUDGET REDUCTION - BASED ON OCTOBER ACTUAL SPEND")
print("="*90)

print(f"\nOCTOBER 2025 ACTUAL SPEND: £{october_spend:,.2f}")
print(f"\nThis is £{october_spend - (ytd_total/3):,.2f} higher than the Aug-Oct average (£{ytd_total/3:,.2f})")

print("\n" + "="*90)
print("CONSERVATIVE REDUCTION PLAN")
print("="*90)

# Calculate savings
zero_savings = sum(c['oct_spend'] for c in zero_conv)
very_low_savings = sum(c['oct_spend'] for c in very_low) * 0.5
high_cpa_savings = sum(c['oct_spend'] for c in high_cpa) * 0.3

total_savings = zero_savings + very_low_savings + high_cpa_savings
new_spend = october_spend - total_savings

print(f"\nSTEP 1: Pause {len(zero_conv)} zero-conversion campaigns")
print(f"  Savings: £{zero_savings:,.2f}/month")

print(f"\nSTEP 2: Reduce {len(very_low)} very low performers (<1 conv) by 50%")
print(f"  Savings: £{very_low_savings:,.2f}/month")

print(f"\nSTEP 3: Reduce {len(high_cpa)} high-CPA campaigns (>£500) by 30%")
print(f"  Savings: £{high_cpa_savings:,.2f}/month")

print(f"\nSTEP 4: Keep efficient campaigns unchanged")

print("\n" + "="*90)
print("BUDGET SUMMARY")
print("="*90)

print(f"\nCurrent Monthly Spend (Oct actual):  £{october_spend:,.2f}")
print(f"Total Monthly Savings:               £{total_savings:,.2f}")
print(f"New Monthly Spend:                   £{new_spend:,.2f}")
print(f"\nReduction: {(total_savings/october_spend)*100:.1f}%")

# Expected impact
total_conv = sum(c['conversions'] for c in campaigns) / 3  # Monthly average
lost_conv = (sum(c['conversions'] for c in zero_conv) + sum(c['conversions'] for c in very_low)) / 3

print("\n" + "="*90)
print("EXPECTED IMPACT")
print("="*90)

print(f"\nCurrent Monthly Conversions: {total_conv:.1f}")
print(f"Expected Lost Conversions: {lost_conv:.1f} ({(lost_conv/total_conv)*100:.1f}%)")
print(f"Expected Remaining: {total_conv - lost_conv:.1f}")

current_cpa = october_spend / total_conv
new_cpa = new_spend / (total_conv - lost_conv)

print(f"\nCurrent CPA: £{current_cpa:.2f}")
print(f"Expected CPA: £{new_cpa:.2f} ({((new_cpa-current_cpa)/current_cpa)*100:+.1f}%)")

print("\n" + "="*90)
print("KEY CAMPAIGNS TO REDUCE (High CPA >£500)")
print("="*90)

for c in sorted(high_cpa, key=lambda x: x['cpa'], reverse=True)[:10]:
    reduction = c['oct_spend'] * 0.3
    print(f"  {c['name'][:60]:<60} CPA: £{c['cpa']:>6,.0f}")
    print(f"    £{c['oct_spend']:>8,.2f} → £{c['oct_spend']*0.7:>8,.2f}  (save £{reduction:,.2f}/mo)")

print("\n" + "="*90)
print("RECOMMENDATION")
print("="*90)

print(f"""
Target Monthly Spend: £{new_spend:,.0f} (rounded to £{round(new_spend/1000)*1000:,.0f})

This represents a {(total_savings/october_spend)*100:.1f}% reduction from October's actual spend,
achieved by:
- Eliminating waste (0-conversion campaigns)
- Scaling back underperformers
- Testing if high-CPA campaigns can work more efficiently

Expected outcome: Virtually same conversion volume at {((new_cpa-current_cpa)/current_cpa)*100:+.1f}% better CPA.
""")

print("="*90)

