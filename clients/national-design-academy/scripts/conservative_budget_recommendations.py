import json

# Campaign performance data
campaigns = [
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "conversions": 197.52, "spend": 18694.84, "market": "UK"},
    {"name": "NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4", "conversions": 145.60, "spend": 5540.02, "market": "UK"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "conversions": 26.00, "spend": 7205.07, "market": "International"},
    {"name": "NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden Split 12/3 No Target 24/4", "conversions": 21.00, "spend": 1364.99, "market": "International"},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "conversions": 20.26, "spend": 3335.22, "market": "International"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5", "conversions": 17.27, "spend": 3370.28, "market": "International"},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "conversions": 16.78, "spend": 2312.33, "market": "UK"},
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "conversions": 16.75, "spend": 2500.95, "market": "International"},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "conversions": 16.00, "spend": 4434.06, "market": "International"},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing 17/3 No Target 30/4 New Customers 1/8", "conversions": 16.00, "spend": 6085.14, "market": "UK"},
    {"name": "NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9", "conversions": 12.19, "spend": 2433.98, "market": "International"},
    {"name": "NDA | Search | Interior Design Degree- UK 120 No Target 24/4", "conversions": 11.51, "spend": 6973.75, "market": "UK"},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "conversions": 8.86, "spend": 3286.67, "market": "International"},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "conversions": 7.50, "spend": 7185.15, "market": "International"},
    {"name": "NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3", "conversions": 6.25, "spend": 1828.08, "market": "International"},
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "conversions": 6.00, "spend": 1517.35, "market": "UK"},
    {"name": "NDA | Search | Interior Design Diploma - India Ai Max 19/9", "conversions": 5.59, "spend": 2319.65, "market": "International"},
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5", "conversions": 3.00, "spend": 2019.55, "market": "International"},
    {"name": "NDA | Search | Brand - UAE  No Target 7/7", "conversions": 2.50, "spend": 1177.48, "market": "International"},
    {"name": "NDA | UAE | Search | Interior Design Degree No Target", "conversions": 2.00, "spend": 3493.10, "market": "International"},
    {"name": "NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4", "conversions": 2.00, "spend": 1101.22, "market": "International"},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "conversions": 1.37, "spend": 908.38, "market": "International"},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "conversions": 1.16, "spend": 906.96, "market": "UK"},
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "conversions": 1.00, "spend": 911.80, "market": "UK"},
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "conversions": 1.00, "spend": 827.84, "market": "UK"},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "conversions": 1.00, "spend": 2108.53, "market": "International"},
    {"name": "NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target", "conversions": 0.50, "spend": 1144.68, "market": "International"},
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "conversions": 0.15, "spend": 1825.03, "market": "UK"},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "conversions": 0.09, "spend": 903.66, "market": "International"},
    # Zero performers
    {"name": "NDA | EUR | Search | Landscape Design Courses 65", "conversions": 0.00, "spend": 0.12, "market": "International"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search |  Landscape Design Diplomas No Target", "conversions": 0.00, "spend": 902.94, "market": "International"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250 No Target 22/9", "conversions": 0.00, "spend": 365.36, "market": "International"},
    {"name": "NDA | Low Intl | Search | Retail Design Degree No Target", "conversions": 0.00, "spend": 768.21, "market": "International"},
    {"name": "NDA | Low Intl | Search | Curtain Making Course No Target", "conversions": 0.00, "spend": 38.97, "market": "International"},
    {"name": "NDA | IN | Search | Interior Design Degree No Target", "conversions": 0.00, "spend": 1414.79, "market": "International"},
    {"name": "NDA | P Max | Interior Design Degree - USA/Canada 250 Split 11/3", "conversions": 0.00, "spend": 908.95, "market": "International"},
    {"name": "NDA | Search | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 Split 11/3 No Target", "conversions": 0.00, "spend": 1943.60, "market": "International"},
    {"name": "NDA | Search | Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135 Split 11/3", "conversions": 0.00, "spend": 1373.46, "market": "International"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "conversions": 0.00, "spend": 2017.12, "market": "International"},
]

# Calculate CPA for each
for c in campaigns:
    c['cpa'] = c['spend'] / c['conversions'] if c['conversions'] > 0 else 9999
    c['monthly_spend'] = c['spend'] / 3

# Current totals
total_spend = sum(c['spend'] for c in campaigns)
total_monthly = total_spend / 3

print("="*90)
print("CONSERVATIVE BUDGET REDUCTION PLAN - NDA")
print("="*90)

print(f"\nCURRENT MONTHLY SPEND: £{total_monthly:,.2f}")

# Identify cuts
zero_conv = [c for c in campaigns if c['conversions'] == 0]
very_low_conv = [c for c in campaigns if 0 < c['conversions'] < 1]
high_cpa = [c for c in campaigns if c['conversions'] > 0 and c['cpa'] > 500]

zero_monthly = sum(c['monthly_spend'] for c in zero_conv)
very_low_monthly = sum(c['monthly_spend'] for c in very_low_conv)
high_cpa_monthly = sum(c['monthly_spend'] for c in high_cpa)

print("\n" + "="*90)
print("STEP 1: PAUSE ZERO-CONVERSION CAMPAIGNS")
print("="*90)
print(f"\n{len(zero_conv)} campaigns with 0 conversions")
print(f"Monthly savings: £{zero_monthly:,.2f}")

for c in zero_conv:
    print(f"  • {c['name'][:70]:<70} £{c['monthly_spend']:>8,.2f}/mo")

print("\n" + "="*90)
print("STEP 2: REDUCE VERY LOW PERFORMERS BY 50%")
print("="*90)
print(f"\n{len(very_low_conv)} campaigns with <1 conversion (reduce by 50%, don't pause)")
print(f"Monthly savings: £{very_low_monthly * 0.5:,.2f}")

for c in very_low_conv:
    print(f"  • {c['name'][:70]:<70} £{c['monthly_spend']:>8,.2f}/mo → £{c['monthly_spend']*0.5:>8,.2f}/mo")

print("\n" + "="*90)
print("STEP 3: REDUCE HIGH CPA CAMPAIGNS (>£500) BY 30%")
print("="*90)
print(f"\n{len(high_cpa)} campaigns with CPA >£500 (still converting, but expensive)")
print(f"Monthly savings: £{high_cpa_monthly * 0.3:,.2f}")

for c in sorted(high_cpa, key=lambda x: x['cpa'], reverse=True):
    if c['conversions'] >= 1:  # Only show those with at least 1 conversion
        print(f"  • {c['name'][:70]:<70} CPA: £{c['cpa']:>6,.0f} | £{c['monthly_spend']:>8,.2f}/mo → £{c['monthly_spend']*0.7:>8,.2f}/mo")

print("\n" + "="*90)
print("STEP 4: KEEP EVERYTHING ELSE AS-IS")
print("="*90)

efficient = [c for c in campaigns if c['conversions'] > 0 and c['cpa'] <= 500 and c['conversions'] >= 1]
print(f"\n{len(efficient)} campaigns with good performance (CPA ≤£500, ≥1 conversion)")
print("These campaigns remain at current budgets - NO CHANGES")

print("\n" + "="*90)
print("BUDGET SUMMARY")
print("="*90)

total_savings = zero_monthly + (very_low_monthly * 0.5) + (high_cpa_monthly * 0.3)
new_monthly = total_monthly - total_savings

print(f"\nCurrent Monthly Spend: £{total_monthly:,.2f}")
print(f"\nSavings Breakdown:")
print(f"  Step 1 (Pause 0-conv):        £{zero_monthly:,.2f}")
print(f"  Step 2 (Reduce <1 conv):      £{very_low_monthly * 0.5:,.2f}")
print(f"  Step 3 (Reduce high CPA):     £{high_cpa_monthly * 0.3:,.2f}")
print(f"  ───────────────────────────────────────")
print(f"  TOTAL MONTHLY SAVINGS:        £{total_savings:,.2f}")

print(f"\nNEW MONTHLY SPEND: £{new_monthly:,.2f}")
print(f"REDUCTION: {(total_savings/total_monthly)*100:.1f}%")

print("\n" + "="*90)
print("EXPECTED IMPACT")
print("="*90)

# Calculate conversion loss
lost_conversions_monthly = (sum(c['conversions'] for c in zero_conv) + sum(c['conversions'] for c in very_low_conv)) / 3
total_conversions_monthly = sum(c['conversions'] for c in campaigns) / 3

print(f"\nCurrent Monthly Conversions: {total_conversions_monthly:.1f}")
print(f"Expected Lost Conversions: {lost_conversions_monthly:.1f} ({(lost_conversions_monthly/total_conversions_monthly)*100:.1f}%)")
print(f"Expected New Conversions: {total_conversions_monthly - lost_conversions_monthly:.1f}")

current_cpa = total_monthly / total_conversions_monthly
new_cpa = new_monthly / (total_conversions_monthly - lost_conversions_monthly)

print(f"\nCurrent CPA: £{current_cpa:.2f}")
print(f"Expected New CPA: £{new_cpa:.2f} ({((new_cpa-current_cpa)/current_cpa)*100:+.1f}%)")

print("\n" + "="*90)
print("RATIONALE")
print("="*90)

print("""
This conservative approach:
✓ Removes pure waste (0 conversions = no value)
✓ Scales back underperformers without killing them entirely
✓ Reduces expensive campaigns by modest 30% (test lower spend)
✓ Leaves efficient campaigns UNTOUCHED (no risk of exhausting volume)
✓ Minimal conversion loss (less than 1% expected)
✓ Allows you to test if high-CPA campaigns can work at lower budgets
✓ No dramatic increases that might hit diminishing returns

Next steps:
1. Monitor performance for 2-3 weeks after cuts
2. IF high performers maintain efficiency, THEN consider small increases
3. IF high-CPA campaigns improve at lower budgets, keep new levels
4. IF high-CPA campaigns worsen, pause them too
""")

print("="*90)

