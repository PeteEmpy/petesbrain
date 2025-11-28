import json

# October 2025 actual spend
october_spend = 39996.40

# Campaign performance data
campaigns = [
    # HIGH PERFORMERS (Keep as-is)
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "conversions": 197.52, "ytd_spend": 18694.84, "cpa": 94.65, "market": "UK", "action": "KEEP", "reason": "Excellent CPA (£95), highest converter"},
    {"name": "NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4", "conversions": 145.60, "ytd_spend": 5540.02, "cpa": 38.05, "market": "UK", "action": "KEEP", "reason": "Best CPA in account (£38)"},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "conversions": 16.78, "ytd_spend": 2312.33, "cpa": 137.80, "market": "UK", "action": "KEEP", "reason": "Good CPA (£138), strong brand campaign"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "conversions": 26.00, "ytd_spend": 7205.07, "cpa": 277.12, "market": "International", "action": "KEEP", "reason": "Reasonable CPA (£277), good volume"},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "conversions": 20.26, "ytd_spend": 3335.22, "cpa": 164.62, "market": "International", "action": "KEEP", "reason": "Good CPA (£165), strong India performance"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5", "conversions": 17.27, "ytd_spend": 3370.28, "cpa": 195.15, "market": "International", "action": "KEEP", "reason": "Good CPA (£195), key UAE market"},
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "conversions": 16.75, "ytd_spend": 2500.95, "cpa": 149.31, "market": "International", "action": "KEEP", "reason": "Good CPA (£149), North America growth"},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "conversions": 16.00, "ytd_spend": 4434.06, "cpa": 277.13, "market": "International", "action": "KEEP", "reason": "Reasonable CPA (£277), MENA presence"},
    {"name": "NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9", "conversions": 12.19, "ytd_spend": 2433.98, "cpa": 199.67, "market": "International", "action": "KEEP", "reason": "Good CPA (£200), global reach"},
    {"name": "NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden", "conversions": 21.00, "ytd_spend": 1364.99, "cpa": 65.00, "market": "International", "action": "KEEP", "reason": "Excellent CPA (£65), Europe performing well"},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "conversions": 8.86, "ytd_spend": 3286.67, "cpa": 370.96, "market": "International", "action": "KEEP", "reason": "Reasonable CPA (£371), brand awareness"},
    {"name": "NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3", "conversions": 6.25, "ytd_spend": 1828.08, "cpa": 292.49, "market": "International", "action": "KEEP", "reason": "Good CPA (£292), North America"},
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "conversions": 6.00, "ytd_spend": 1517.35, "cpa": 252.89, "market": "UK", "action": "KEEP", "reason": "Good CPA (£253), niche product"},
    {"name": "NDA | Search | Interior Design Diploma - India Ai Max 19/9", "conversions": 5.59, "ytd_spend": 2319.65, "cpa": 414.96, "market": "International", "action": "KEEP", "reason": "Acceptable CPA (£415), India growth"},
    {"name": "NDA | Search | Brand - UAE  No Target 7/7", "conversions": 2.50, "ytd_spend": 1177.48, "cpa": 470.99, "market": "International", "action": "KEEP", "reason": "Acceptable CPA (£471), UAE brand"},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing", "conversions": 16.00, "ytd_spend": 6085.14, "cpa": 380.32, "market": "UK", "action": "KEEP", "reason": "Acceptable CPA (£380), remarketing value"},

    # HIGH CPA - REDUCE 30%
    {"name": "NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4", "conversions": 2.00, "ytd_spend": 1101.22, "cpa": 550.61, "market": "International", "action": "REDUCE_30", "reason": "High CPA (£551), test lower spend"},
    {"name": "NDA | Search | Interior Design Degree- UK 120 No Target 24/4", "conversions": 11.51, "ytd_spend": 6973.75, "cpa": 605.89, "market": "UK", "action": "REDUCE_30", "reason": "High CPA (£606), test efficiency at lower budget"},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "conversions": 7.50, "ytd_spend": 7185.15, "cpa": 958.02, "market": "International", "action": "REDUCE_30", "reason": "Very high CPA (£958), reduce spend"},
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada 250", "conversions": 3.00, "ytd_spend": 2019.55, "cpa": 673.18, "market": "International", "action": "REDUCE_30", "reason": "High CPA (£673), test lower budget"},
    {"name": "NDA | UAE | Search | Interior Design Degree No Target", "conversions": 2.00, "ytd_spend": 3493.10, "cpa": 1746.55, "market": "International", "action": "REDUCE_30", "reason": "Extremely high CPA (£1,747), major reduction needed"},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "conversions": 1.37, "ytd_spend": 908.38, "cpa": 663.05, "market": "International", "action": "REDUCE_30", "reason": "High CPA (£663), niche product underperforming"},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "conversions": 1.16, "ytd_spend": 906.96, "cpa": 781.86, "market": "UK", "action": "REDUCE_30", "reason": "High CPA (£782), low demand product"},
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "conversions": 1.00, "ytd_spend": 911.80, "cpa": 911.80, "market": "UK", "action": "REDUCE_30", "reason": "High CPA (£912), niche product"},
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "conversions": 1.00, "ytd_spend": 827.84, "cpa": 827.84, "market": "UK", "action": "REDUCE_30", "reason": "High CPA (£828), low volume product"},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "conversions": 1.00, "ytd_spend": 2108.53, "cpa": 2108.53, "market": "International", "action": "REDUCE_30", "reason": "Extremely high CPA (£2,109), not viable"},

    # VERY LOW PERFORMERS - REDUCE 50%
    {"name": "NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar", "conversions": 0.50, "ytd_spend": 1144.68, "cpa": 2289.36, "market": "International", "action": "REDUCE_50", "reason": "Only 0.5 conv, CPA £2,289, not working"},
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "conversions": 0.15, "ytd_spend": 1825.03, "cpa": 12166.87, "market": "UK", "action": "REDUCE_50", "reason": "Only 0.15 conv, CPA £12,167, completely inefficient"},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "conversions": 0.09, "ytd_spend": 903.66, "cpa": 10040.67, "market": "International", "action": "REDUCE_50", "reason": "Only 0.09 conv, CPA £10,041, not working"},

    # ZERO PERFORMERS - PAUSE
    {"name": "NDA | EUR | Search | Landscape Design Courses 65", "conversions": 0.00, "ytd_spend": 0.12, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions, pure waste"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search |  Landscape Design Diplomas No Target", "conversions": 0.00, "ytd_spend": 902.94, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions over 3 months, pause immediately"},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250", "conversions": 0.00, "ytd_spend": 365.36, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions, no performance"},
    {"name": "NDA | Low Intl | Search | Retail Design Degree No Target", "conversions": 0.00, "ytd_spend": 768.21, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions, wasting budget"},
    {"name": "NDA | Low Intl | Search | Curtain Making Course No Target", "conversions": 0.00, "ytd_spend": 38.97, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions, pause"},
    {"name": "NDA | IN | Search | Interior Design Degree No Target", "conversions": 0.00, "ytd_spend": 1414.79, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions despite £1,415 spend, pause"},
    {"name": "NDA | P Max | Interior Design Degree - USA/Canada 250 Split", "conversions": 0.00, "ytd_spend": 908.95, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions, not performing"},
    {"name": "NDA | Search | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175", "conversions": 0.00, "ytd_spend": 1943.60, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions despite £1,944 spend, major waste"},
    {"name": "NDA | Search | Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135", "conversions": 0.00, "ytd_spend": 1373.46, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions, significant waste"},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - MENA", "conversions": 0.00, "ytd_spend": 2017.12, "cpa": 0, "market": "International", "action": "PAUSE", "reason": "0 conversions despite £2,017 spend, pause immediately"},
]

# Calculate October-adjusted spend
ytd_total = sum(c['ytd_spend'] for c in campaigns)
scale_factor = october_spend / (ytd_total / 3)

for c in campaigns:
    c['oct_spend'] = round((c['ytd_spend'] / 3) * scale_factor, 2)

    if c['action'] == 'KEEP':
        c['new_spend'] = c['oct_spend']
        c['change_pct'] = 0
        c['saving'] = 0
    elif c['action'] == 'REDUCE_30':
        c['new_spend'] = round(c['oct_spend'] * 0.7, 2)
        c['change_pct'] = -30
        c['saving'] = round(c['oct_spend'] - c['new_spend'], 2)
    elif c['action'] == 'REDUCE_50':
        c['new_spend'] = round(c['oct_spend'] * 0.5, 2)
        c['change_pct'] = -50
        c['saving'] = round(c['oct_spend'] - c['new_spend'], 2)
    elif c['action'] == 'PAUSE':
        c['new_spend'] = 0
        c['change_pct'] = -100
        c['saving'] = c['oct_spend']

# Create CSV data
import csv
import sys

writer = csv.writer(sys.stdout)

# Header rows
writer.writerow(['NDA BUDGET REDUCTION PLAN - CAMPAIGN BY CAMPAIGN'])
writer.writerow(['Date:', 'November 3, 2025'])
writer.writerow(['Baseline:', f'£{october_spend:,.2f}/month (October 2025 actual)'])
writer.writerow(['Target:', f'£33,000/month (18% reduction)'])
writer.writerow([])

# Main table header
writer.writerow(['Campaign Name', 'Market', 'YTD Conversions', 'CPA', 'Oct Spend', 'New Budget', 'Change %', 'Monthly Saving', 'Action', 'Rationale'])

# Sort by action, then by spend
action_order = {'PAUSE': 1, 'REDUCE_50': 2, 'REDUCE_30': 3, 'KEEP': 4}
sorted_campaigns = sorted(campaigns, key=lambda x: (action_order[x['action']], -x['oct_spend']))

for c in sorted_campaigns:
    writer.writerow([
        c['name'],
        c['market'],
        f"{c['conversions']:.2f}",
        f"£{c['cpa']:.0f}" if c['cpa'] > 0 else '£0',
        f"£{c['oct_spend']:.2f}",
        f"£{c['new_spend']:.2f}",
        f"{c['change_pct']}%",
        f"£{c['saving']:.2f}",
        c['action'],
        c['reason']
    ])

# Summary section
writer.writerow([])
writer.writerow(['SUMMARY'])
writer.writerow([])

action_groups = {
    'PAUSE': [c for c in campaigns if c['action'] == 'PAUSE'],
    'REDUCE_50': [c for c in campaigns if c['action'] == 'REDUCE_50'],
    'REDUCE_30': [c for c in campaigns if c['action'] == 'REDUCE_30'],
    'KEEP': [c for c in campaigns if c['action'] == 'KEEP']
}

writer.writerow(['Action', 'Campaigns', 'Current Spend', 'New Spend', 'Monthly Saving'])
for action, group in action_groups.items():
    current = sum(c['oct_spend'] for c in group)
    new = sum(c['new_spend'] for c in group)
    saving = current - new
    writer.writerow([
        action,
        len(group),
        f"£{current:,.2f}",
        f"£{new:,.2f}",
        f"£{saving:,.2f}"
    ])

writer.writerow([])
writer.writerow(['TOTAL', len(campaigns), f"£{october_spend:,.2f}", f"£{sum(c['new_spend'] for c in campaigns):,.2f}", f"£{sum(c['saving'] for c in campaigns):,.2f}"])

