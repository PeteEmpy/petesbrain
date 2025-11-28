import json

# October 2025 actual spend
october_spend = 39996.40

# Campaign performance data with October-adjusted spend
campaigns = [
    # HIGH PERFORMERS (Keep as-is)
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "conversions": 197.52, "ytd_spend": 18694.84, "cpa": 94.65, "market": "UK", "action": "KEEP"},
    {"name": "NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4", "conversions": 145.60, "ytd_spend": 5540.02, "cpa": 38.05, "market": "UK", "action": "KEEP"},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "conversions": 16.78, "ytd_spend": 2312.33, "cpa": 137.80, "market": "UK", "action": "KEEP"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "conversions": 26.00, "ytd_spend": 7205.07, "cpa": 277.12, "market": "International", "action": "KEEP"},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "conversions": 20.26, "ytd_spend": 3335.22, "cpa": 164.62, "market": "International", "action": "KEEP"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5", "conversions": 17.27, "ytd_spend": 3370.28, "cpa": 195.15, "market": "International", "action": "KEEP"},
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "conversions": 16.75, "ytd_spend": 2500.95, "cpa": 149.31, "market": "International", "action": "KEEP"},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "conversions": 16.00, "ytd_spend": 4434.06, "cpa": 277.13, "market": "International", "action": "KEEP"},
    {"name": "NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9", "conversions": 12.19, "ytd_spend": 2433.98, "cpa": 199.67, "market": "International", "action": "KEEP"},
    {"name": "NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden", "conversions": 21.00, "ytd_spend": 1364.99, "cpa": 65.00, "market": "International", "action": "KEEP"},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "conversions": 8.86, "ytd_spend": 3286.67, "cpa": 370.96, "market": "International", "action": "KEEP"},
    {"name": "NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3", "conversions": 6.25, "ytd_spend": 1828.08, "cpa": 292.49, "market": "International", "action": "KEEP"},
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "conversions": 6.00, "ytd_spend": 1517.35, "cpa": 252.89, "market": "UK", "action": "KEEP"},
    {"name": "NDA | Search | Interior Design Diploma - India Ai Max 19/9", "conversions": 5.59, "ytd_spend": 2319.65, "cpa": 414.96, "market": "International", "action": "KEEP"},
    {"name": "NDA | Search | Brand - UAE  No Target 7/7", "conversions": 2.50, "ytd_spend": 1177.48, "cpa": 470.99, "market": "International", "action": "KEEP"},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing", "conversions": 16.00, "ytd_spend": 6085.14, "cpa": 380.32, "market": "UK", "action": "KEEP"},

    # HIGH CPA - REDUCE 30%
    {"name": "NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4", "conversions": 2.00, "ytd_spend": 1101.22, "cpa": 550.61, "market": "International", "action": "REDUCE_30"},
    {"name": "NDA | Search | Interior Design Degree- UK 120 No Target 24/4", "conversions": 11.51, "ytd_spend": 6973.75, "cpa": 605.89, "market": "UK", "action": "REDUCE_30"},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "conversions": 7.50, "ytd_spend": 7185.15, "cpa": 958.02, "market": "International", "action": "REDUCE_30"},
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada 250", "conversions": 3.00, "ytd_spend": 2019.55, "cpa": 673.18, "market": "International", "action": "REDUCE_30"},
    {"name": "NDA | UAE | Search | Interior Design Degree No Target", "conversions": 2.00, "ytd_spend": 3493.10, "cpa": 1746.55, "market": "International", "action": "REDUCE_30"},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "conversions": 1.37, "ytd_spend": 908.38, "cpa": 663.05, "market": "International", "action": "REDUCE_30"},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "conversions": 1.16, "ytd_spend": 906.96, "cpa": 781.86, "market": "UK", "action": "REDUCE_30"},
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "conversions": 1.00, "ytd_spend": 911.80, "cpa": 911.80, "market": "UK", "action": "REDUCE_30"},
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "conversions": 1.00, "ytd_spend": 827.84, "cpa": 827.84, "market": "UK", "action": "REDUCE_30"},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "conversions": 1.00, "ytd_spend": 2108.53, "cpa": 2108.53, "market": "International", "action": "REDUCE_30"},

    # VERY LOW PERFORMERS - REDUCE 50%
    {"name": "NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar", "conversions": 0.50, "ytd_spend": 1144.68, "cpa": 2289.36, "market": "International", "action": "REDUCE_50"},
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "conversions": 0.15, "ytd_spend": 1825.03, "cpa": 12166.87, "market": "UK", "action": "REDUCE_50"},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "conversions": 0.09, "ytd_spend": 903.66, "cpa": 10040.67, "market": "International", "action": "REDUCE_50"},

    # ZERO PERFORMERS - PAUSE
    {"name": "NDA | EUR | Search | Landscape Design Courses 65", "conversions": 0.00, "ytd_spend": 0.12, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search |  Landscape Design Diplomas No Target", "conversions": 0.00, "ytd_spend": 902.94, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250", "conversions": 0.00, "ytd_spend": 365.36, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | Low Intl | Search | Retail Design Degree No Target", "conversions": 0.00, "ytd_spend": 768.21, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | Low Intl | Search | Curtain Making Course No Target", "conversions": 0.00, "ytd_spend": 38.97, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | IN | Search | Interior Design Degree No Target", "conversions": 0.00, "ytd_spend": 1414.79, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | P Max | Interior Design Degree - USA/Canada 250 Split", "conversions": 0.00, "ytd_spend": 908.95, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | Search | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175", "conversions": 0.00, "ytd_spend": 1943.60, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | Search | Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135", "conversions": 0.00, "ytd_spend": 1373.46, "cpa": 0, "market": "International", "action": "PAUSE"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - MENA", "conversions": 0.00, "ytd_spend": 2017.12, "cpa": 0, "market": "International", "action": "PAUSE"},
]

# Calculate October-adjusted spend
ytd_total = sum(c['ytd_spend'] for c in campaigns)
scale_factor = october_spend / (ytd_total / 3)

for c in campaigns:
    c['oct_spend'] = (c['ytd_spend'] / 3) * scale_factor

    if c['action'] == 'KEEP':
        c['new_spend'] = c['oct_spend']
        c['change'] = 0
    elif c['action'] == 'REDUCE_30':
        c['new_spend'] = c['oct_spend'] * 0.7
        c['change'] = -0.30
    elif c['action'] == 'REDUCE_50':
        c['new_spend'] = c['oct_spend'] * 0.5
        c['change'] = -0.50
    elif c['action'] == 'PAUSE':
        c['new_spend'] = 0
        c['change'] = -1.00

# Group by action
keep = [c for c in campaigns if c['action'] == 'KEEP']
reduce_30 = [c for c in campaigns if c['action'] == 'REDUCE_30']
reduce_50 = [c for c in campaigns if c['action'] == 'REDUCE_50']
pause = [c for c in campaigns if c['action'] == 'PAUSE']

print("="*100)
print("DETAILED NDA BUDGET REDUCTION PLAN - CAMPAIGN BY CAMPAIGN")
print("="*100)

print(f"\nBASELINE: October 2025 actual spend = £{october_spend:,.2f}")
print(f"TARGET: Reduce to £33,000/month (18% reduction)")

print("\n" + "="*100)
print("STEP 1: PAUSE ZERO-CONVERSION CAMPAIGNS")
print("="*100)

print(f"\n{len(pause)} campaigns | YTD: 0 conversions | Current spend: £{sum(c['oct_spend'] for c in pause):,.2f}/month")
print(f"\nRATIONALE: These campaigns have generated zero conversions over 3 months. They are")
print("pure waste and should be paused immediately with no impact on conversion volume.")

print(f"\n{'Campaign':<70} {'Oct Spend':>12} {'Action':>12}")
print("-" * 100)
for c in pause:
    print(f"{c['name'][:70]:<70} £{c['oct_spend']:>10,.2f}  PAUSE")

pause_savings = sum(c['oct_spend'] for c in pause)
print(f"\n{'STEP 1 TOTAL SAVINGS:':<70} £{pause_savings:>10,.2f}/month")

print("\n" + "="*100)
print("STEP 2: REDUCE VERY LOW PERFORMERS BY 50%")
print("="*100)

print(f"\n{len(reduce_50)} campaigns | YTD: <1 conversion | Current spend: £{sum(c['oct_spend'] for c in reduce_50):,.2f}/month")
print(f"\nRATIONALE: These campaigns have generated less than 1 conversion in 3 months,")
print("resulting in CPAs over £2,000. Rather than pause entirely, I'm reducing budgets")
print("by 50% to test if they can work at lower spend while minimizing waste.")

print(f"\n{'Campaign':<70} {'Oct Spend':>12} {'New Budget':>12} {'Saving':>12}")
print("-" * 100)
for c in sorted(reduce_50, key=lambda x: x['cpa'], reverse=True):
    saving = c['oct_spend'] - c['new_spend']
    print(f"{c['name'][:70]:<70} £{c['oct_spend']:>10,.2f} £{c['new_spend']:>10,.2f} £{saving:>10,.2f}")
    print(f"  └─ CPA: £{c['cpa']:,.0f} | {c['conversions']:.2f} conversions YTD | Reduce by 50%")

reduce_50_savings = sum(c['oct_spend'] - c['new_spend'] for c in reduce_50)
print(f"\n{'STEP 2 TOTAL SAVINGS:':<70} £{reduce_50_savings:>10,.2f}/month")

print("\n" + "="*100)
print("STEP 3: REDUCE HIGH-CPA CAMPAIGNS BY 30%")
print("="*100)

print(f"\n{len(reduce_30)} campaigns | CPA >£500 | Current spend: £{sum(c['oct_spend'] for c in reduce_30):,.2f}/month")
print(f"\nRATIONALE: These campaigns ARE converting but at expensive CPAs (>£500). Rather")
print("than pause, I'm reducing budgets by 30% to test if they can maintain conversions")
print("at lower spend. If efficiency improves, keep the lower budget. If it worsens,")
print("consider pausing.")

print(f"\n{'Campaign':<70} {'Oct Spend':>12} {'New Budget':>12} {'Saving':>12}")
print("-" * 100)
for c in sorted(reduce_30, key=lambda x: x['cpa'], reverse=True):
    saving = c['oct_spend'] - c['new_spend']
    print(f"{c['name'][:70]:<70} £{c['oct_spend']:>10,.2f} £{c['new_spend']:>10,.2f} £{saving:>10,.2f}")
    print(f"  └─ CPA: £{c['cpa']:,.0f} | {c['conversions']:.1f} conversions YTD | Reduce by 30%")

reduce_30_savings = sum(c['oct_spend'] - c['new_spend'] for c in reduce_30)
print(f"\n{'STEP 3 TOTAL SAVINGS:':<70} £{reduce_30_savings:>10,.2f}/month")

print("\n" + "="*100)
print("STEP 4: KEEP EFFICIENT CAMPAIGNS UNCHANGED")
print("="*100)

print(f"\n{len(keep)} campaigns | CPA ≤£500 & ≥1 conversion | Current spend: £{sum(c['oct_spend'] for c in keep):,.2f}/month")
print(f"\nRATIONALE: These campaigns are performing well with reasonable CPAs. Making NO")
print("changes to avoid risking volume or hitting diminishing returns. Let them continue")
print("at current budgets.")

print(f"\n{'Campaign':<70} {'Oct Spend':>12} {'Action':>12}")
print("-" * 100)
for c in sorted(keep, key=lambda x: x['conversions'], reverse=True)[:15]:
    print(f"{c['name'][:70]:<70} £{c['oct_spend']:>10,.2f}  UNCHANGED")
    print(f"  └─ CPA: £{c['cpa']:,.0f} | {c['conversions']:.1f} conversions YTD")

print(f"\n... and {len(keep)-15} more efficient campaigns")

print("\n" + "="*100)
print("BUDGET SUMMARY")
print("="*100)

total_savings = pause_savings + reduce_50_savings + reduce_30_savings
new_total = october_spend - total_savings

print(f"\nCurrent Monthly Spend (Oct 2025):        £{october_spend:,.2f}")
print(f"\nSavings Breakdown:")
print(f"  Step 1 (Pause {len(pause)} campaigns):              £{pause_savings:>10,.2f}")
print(f"  Step 2 (Reduce {len(reduce_50)} by 50%):                 £{reduce_50_savings:>10,.2f}")
print(f"  Step 3 (Reduce {len(reduce_30)} by 30%):                £{reduce_30_savings:>10,.2f}")
print(f"  ─────────────────────────────────────────────")
print(f"  TOTAL MONTHLY SAVINGS:                   £{total_savings:>10,.2f}")
print(f"\nNEW MONTHLY SPEND:                        £{new_total:,.2f}")
print(f"REDUCTION:                                {(total_savings/october_spend)*100:.1f}%")

# Market split
uk_current = sum(c['oct_spend'] for c in campaigns if c['market'] == 'UK')
intl_current = sum(c['oct_spend'] for c in campaigns if c['market'] == 'International')
uk_new = sum(c['new_spend'] for c in campaigns if c['market'] == 'UK')
intl_new = sum(c['new_spend'] for c in campaigns if c['market'] == 'International')

print(f"\n{'Market Split:':<40} {'Current':>15} {'New':>15}")
print("-" * 75)
print(f"{'UK:':<40} £{uk_current:>13,.2f} ({uk_current/october_spend*100:.1f}%) £{uk_new:>13,.2f} ({uk_new/new_total*100:.1f}%)")
print(f"{'International:':<40} £{intl_current:>13,.2f} ({intl_current/october_spend*100:.1f}%) £{intl_new:>13,.2f} ({intl_new/new_total*100:.1f}%)")

print("\n" + "="*100)
print("EXPECTED IMPACT")
print("="*100)

total_conv = sum(c['conversions'] for c in campaigns) / 3
lost_conv = (sum(c['conversions'] for c in pause) + sum(c['conversions'] for c in reduce_50)) / 3
remaining_conv = total_conv - lost_conv

current_cpa = october_spend / total_conv
new_cpa = new_total / remaining_conv

print(f"\nConversions:")
print(f"  Current:  {total_conv:.1f}/month")
print(f"  Lost:     {lost_conv:.1f}/month ({(lost_conv/total_conv)*100:.1f}%)")
print(f"  Expected: {remaining_conv:.1f}/month")

print(f"\nCost Per Acquisition:")
print(f"  Current:  £{current_cpa:.2f}")
print(f"  Expected: £{new_cpa:.2f} ({((new_cpa-current_cpa)/current_cpa)*100:+.1f}%)")

print(f"\nROAS Impact:")
print(f"  Current ROAS (Oct):  515% (international), higher for UK")
print(f"  Expected change:     +{abs((new_cpa-current_cpa)/current_cpa)*100:.0f}% improvement in efficiency")
print(f"                       Should translate to ~{abs((new_cpa-current_cpa)/current_cpa)*100:.0f}% ROAS improvement")

print("\n" + "="*100)
print("IMPLEMENTATION CHECKLIST")
print("="*100)

print("""
Week 1 - Immediate Actions:
 ☐ Pause 10 zero-conversion campaigns (Step 1)
 ☐ Reduce 3 very low performers by 50% (Step 2)
 ☐ Reduce 10 high-CPA campaigns by 30% (Step 3)
 ☐ Set up daily performance monitoring dashboard

Week 2-3 - Monitor & Adjust:
 ☐ Check high-CPA campaigns daily for first week
 ☐ If any improve efficiency, keep reduced budgets
 ☐ If any worsen significantly, consider pausing
 ☐ Monitor efficient campaigns for any unexpected drops

Week 4 - Review:
 ☐ Compare actual vs expected conversion volume
 ☐ Calculate actual CPA improvement
 ☐ Identify any campaigns to pause based on 2-week performance
 ☐ Prepare report for client with results
""")

print("="*100)
