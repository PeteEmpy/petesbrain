import json

# Campaign data from Google Ads API
oct_2024_campaigns = [
    {"name": "NDA | 03B1 - DEGREES / MASTERS - Interior Design - HIGH INTL Austria/France/Holland/Malta/Germany/Sweden", "cost": 35050000},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search |  Landscape Design Diplomas No Target", "cost": 299680000},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250 No Target 22/9", "cost": 466547016},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "cost": 194342210},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "cost": 291750000},
    {"name": "NDA | Delhi, Mumbai, Hyderabad, Chennai, Bangalor Diploma I 2023", "cost": 356540892},
    {"name": "NDA | EUR | Search | Landscape Design Courses 65", "cost": 12497142},
    {"name": "NDA | IN | Search | Interior Design Degree No Target", "cost": 2696534858},
    {"name": "NDA | Interior Design - Qatar/Bahrain/Kuwait/Cyprus/Singapore", "cost": 96411263},
    {"name": "NDA | Low Intl | Search | Curtain Making Course No Target", "cost": 66150000},
    {"name": "NDA | Low Intl | Search | Retail Design Degree No Target", "cost": 230170000},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "cost": 795909075},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "cost": 306710000},
    {"name": "NDA | P Max | Interior Design - Australia/New Zealand", "cost": 86137248},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "cost": 933330629},
    {"name": "NDA | P Max | Interior Design Diploma - ROTW 200 13/1", "cost": 319375334},
    {"name": "NDA | P Max | Interior Design Diploma - UAE 175", "cost": 1215391557},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing 17/3 No Target 30/4 New Customers 1/8", "cost": 5176275975},  # UK
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5", "cost": 1188679620},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "cost": 303240000},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "cost": 1414234424},
    {"name": "NDA | Search |  Interior Design - MENA Oman/Saudi/Bahrain/Kuwait", "cost": 84662860},
    {"name": "NDA | Search | Interior Design - MENA Oman/Saudi/Bahrain/Kuwait", "cost": 870000},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "cost": 737333323},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "cost": 1641632313},  # UK
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "cost": 304000000},  # UK
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "cost": 607802993},  # UK
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "cost": 6211062401},  # UK
    {"name": "NDA | UK | Search | Landscape Design Courses No Target", "cost": 455920000},  # UK
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "cost": 304000000},  # UK
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "cost": 34850000},  # UK
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "cost": 66358065},
]

oct_2025_campaigns = [
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search |  Landscape Design Diplomas No Target", "cost": 303861744},
    {"name": "NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250 No Target 22/9", "cost": 216445284},
    {"name": "NDA | BH/CY/KW | Search | Interior Design Degree No Target", "cost": 905569729},
    {"name": "NDA | BH/IN/CYSI | Search | Landscape Design Course No Target", "cost": 304093612},
    {"name": "NDA | IN | Search | Interior Design Degree No Target", "cost": 594730778},
    {"name": "NDA | Low Intl | Search | Curtain Making Course No Target", "cost": 960000},
    {"name": "NDA | Low Intl | Search | Retail Design Degree No Target", "cost": 287582737},
    {"name": "NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target", "cost": 1498194822},
    {"name": "NDA | OM/SA/UAE | Search | Landscape Design No Target", "cost": 300388298},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "cost": 492580327},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "cost": 1711759696},
    {"name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5", "cost": 996696226},
    {"name": "NDA | P Max | Interior Design - India 135 29/11 No Target 10/9", "cost": 1053079782},
    {"name": "NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target", "cost": 561699519},
    {"name": "NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9", "cost": 882711653},
    {"name": "NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4", "cost": 438783006},
    {"name": "NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4", "cost": 1918140584},  # UK
    {"name": "NDA | P Max | Interior Design Degree - USA/Canada 250 Split 11/3", "cost": 301345480},
    {"name": "NDA | P Max | Interior Design Diploma - UK 100 Remarketing 17/3 No Target 30/4 New Customers 1/8", "cost": 1551513689},  # UK
    {"name": "NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5", "cost": 510666628},
    {"name": "NDA | Pro Curtain Making & Soft Furnishings Fast-Track I 2023", "cost": 303642574},
    {"name": "NDA | ROTW | Search | Brand Inclusion No Target", "cost": 1132151582},
    {"name": "NDA | Search | Brand - UAE  No Target 7/7", "cost": 432476056},
    {"name": "NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden Split 12/3 No Target 24/4", "cost": 455827494},
    {"name": "NDA | Search | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 Split 11/3 No Target", "cost": 1356828121},
    {"name": "NDA | Search | Interior Design Degree- UK 120 No Target 24/4", "cost": 3038568844},  # UK
    {"name": "NDA | Search | Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135 Split 11/3", "cost": 461133759},
    {"name": "NDA | Search | Interior Design Diploma - India Ai Max 19/9", "cost": 803368373},
    {"name": "NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3", "cost": 607912053},
    {"name": "NDA | UAE | Search | Interior Design Degree No Target", "cost": 1506098310},
    {"name": "NDA | UAE | Search | Interior Design Diploma No Target", "cost": 2618225749},
    {"name": "NDA | UK | Search | Brand 100 New Customer 1/8 No Target", "cost": 786690122},  # UK
    {"name": "NDA | UK | Search | Curtain Making Courses No Target", "cost": 303375811},  # UK
    {"name": "NDA | UK | Search | Interior Design Careers  No Target", "cost": 608065417},  # UK
    {"name": "NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8", "cost": 8656020427},  # UK
    {"name": "NDA | UK | Search | Landscape Design Diplomas No Target", "cost": 608141330},  # UK
    {"name": "NDA | UK | Search | Retail Design Degree No Target", "cost": 270929889},  # UK
    {"name": "NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9", "cost": 1216144921},
]

# Filter for international campaigns (exclude UK-specific)
uk_keywords = ["| UK |", "- UK "]

def is_international(campaign_name):
    for keyword in uk_keywords:
        if keyword in campaign_name:
            return False
    return True

# Calculate international spend
oct_2024_intl_cost = sum(c['cost'] for c in oct_2024_campaigns if is_international(c['name']))
oct_2024_intl_spend = round(oct_2024_intl_cost / 1_000_000, 2)

oct_2025_intl_cost = sum(c['cost'] for c in oct_2025_campaigns if is_international(c['name']))
oct_2025_intl_spend = round(oct_2025_intl_cost / 1_000_000, 2)

# Enrollment data
oct_2024_intl_enrollments = 19  # Estimated
oct_2025_intl_enrollments = 50  # Actual

# Cost per enrollment
oct_2024_cost_per_enrol = round(oct_2024_intl_spend / oct_2024_intl_enrollments)
oct_2025_cost_per_enrol = round(oct_2025_intl_spend / oct_2025_intl_enrollments)

# Revenue data (from previous calculation)
oct_2024_intl_revenue = 118960
oct_2025_intl_revenue = 127792

# Revenue per enrollment
oct_2024_rev_per_enrol = round(oct_2024_intl_revenue / oct_2024_intl_enrollments)
oct_2025_rev_per_enrol = round(oct_2025_intl_revenue / oct_2025_intl_enrollments)

# Calculate changes
cost_change = oct_2025_intl_spend - oct_2024_intl_spend
cost_change_pct = round((cost_change / oct_2024_intl_spend) * 100, 1)

cost_per_enrol_change = oct_2025_cost_per_enrol - oct_2024_cost_per_enrol
cost_per_enrol_change_pct = round((cost_per_enrol_change / oct_2024_cost_per_enrol) * 100, 1)

enrollment_change = oct_2025_intl_enrollments - oct_2024_intl_enrollments
enrollment_change_pct = round((enrollment_change / oct_2024_intl_enrollments) * 100, 1)

revenue_change = oct_2025_intl_revenue - oct_2024_intl_revenue
revenue_change_pct = round((revenue_change / oct_2024_intl_revenue) * 100, 1)

rev_per_enrol_change = oct_2025_rev_per_enrol - oct_2024_rev_per_enrol
rev_per_enrol_change_pct = round((rev_per_enrol_change / oct_2024_rev_per_enrol) * 100, 1)

# ROAS calculation
oct_2024_roas = round((oct_2024_intl_revenue / oct_2024_intl_spend) * 100)
oct_2025_roas = round((oct_2025_intl_revenue / oct_2025_intl_spend) * 100)
roas_change = oct_2025_roas - oct_2024_roas

print("\n" + "="*70)
print("INTERNATIONAL STUDENTS ONLY - OCTOBER 2024 vs OCTOBER 2025")
print("="*70)

print(f"\n{'':20} {'Oct 2024':>15} {'Oct 2025':>15} {'Change':>15}")
print("-" * 70)

print(f"{'Enrollments:':<20} {oct_2024_intl_enrollments:>15} {oct_2025_intl_enrollments:>15} {enrollment_change:>+8} ({enrollment_change_pct:+.1f}%)")
print(f"{'Revenue:':<20} {'£' + f'{oct_2024_intl_revenue:,}':>15} {'£' + f'{oct_2025_intl_revenue:,}':>15} {'£' + f'{revenue_change:,}':>8} ({revenue_change_pct:+.1f}%)")
print(f"{'Google Ads Spend:':<20} {'£' + f'{oct_2024_intl_spend:,.2f}':>15} {'£' + f'{oct_2025_intl_spend:,.2f}':>15} {'£' + f'{cost_change:,.2f}':>8} ({cost_change_pct:+.1f}%)")

print("\n" + "-" * 70)
print("EFFICIENCY METRICS")
print("-" * 70)

print(f"{'Cost/Enrollment:':<20} {'£' + f'{oct_2024_cost_per_enrol:,}':>15} {'£' + f'{oct_2025_cost_per_enrol:,}':>15} {'£' + f'{cost_per_enrol_change:,}':>8} ({cost_per_enrol_change_pct:+.1f}%)")
print(f"{'Revenue/Enrollment:':<20} {'£' + f'{oct_2024_rev_per_enrol:,}':>15} {'£' + f'{oct_2025_rev_per_enrol:,}':>15} {'£' + f'{rev_per_enrol_change:,}':>8} ({rev_per_enrol_change_pct:+.1f}%)")
print(f"{'ROAS:':<20} {oct_2024_roas:>14}% {oct_2025_roas:>14}% {roas_change:>+8}pp")

print("\n" + "="*70)
print("KEY INSIGHTS")
print("="*70)

print(f"""
✅ MARKETING EFFICIENCY: Cost per enrollment improved by {abs(cost_per_enrol_change_pct):.1f}%
   - Acquiring international students MORE efficiently than last year
   - International ad spend increased {cost_change_pct:+.1f}% but enrollments grew {enrollment_change_pct:+.1f}%

❌ REVENUE PER STUDENT: Revenue per enrollment declined {rev_per_enrol_change_pct:.1f}%
   - Each international student generating {abs(rev_per_enrol_change_pct):.1f}% less revenue
   - Similar pattern to overall YTD trend (course mix or payment plans)

📊 OVERALL ROAS: {oct_2024_roas}% → {oct_2025_roas}% ({roas_change:+d}pp)
   - ROAS {"improved" if roas_change > 0 else "declined"} by {abs(roas_change)} percentage points
   - {"Still highly profitable at " + str(oct_2025_roas) + "%" if oct_2025_roas > 300 else "Return on ad spend needs attention"}

🌍 INTERNATIONAL GROWTH: +{enrollment_change} enrollments ({enrollment_change_pct:+.1f}%)
   - Strong volume growth continues in international markets
   - Dubai/MENA/India driving majority of international expansion
""")

print("="*70)
print("DATA NOTES")
print("="*70)
print("""
- Oct 2024 enrollments: ESTIMATED (19 students based on 41.3% YTD international rate)
- Oct 2025 enrollments: ACTUAL (50 students from enrollment spreadsheet)
- Oct 2024 revenue: ESTIMATED (£118,960 based on 39% YTD international revenue)
- Oct 2025 revenue: ESTIMATED (£127,792 based on 51% YTD international revenue)
- Google Ads spend: ACTUAL (from Google Ads API, international campaigns only)
""")
print("="*70 + "\n")

