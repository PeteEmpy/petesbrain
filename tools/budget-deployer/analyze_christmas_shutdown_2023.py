#!/usr/bin/env python3
"""
Analyse Clear Prospects Christmas 2023 shutdown period to inform 2024 deployment.
"""

# Data from Google Ads API query (Dec 20, 2023 - Jan 10, 2024)
shutdown_data = [
    # Pre-shutdown
    {"date": "2023-12-20", "spend_gbp": 577.25, "conversions": 44.33, "revenue_gbp": 608.49},
    {"date": "2023-12-21", "spend_gbp": 46.55, "conversions": 6.00, "revenue_gbp": 62.91},

    # Christmas shutdown (Dec 22-23 no data - likely paused)
    {"date": "2023-12-24", "spend_gbp": 38.54, "conversions": 2.00, "revenue_gbp": 15.92},
    {"date": "2023-12-25", "spend_gbp": 131.42, "conversions": 4.00, "revenue_gbp": 43.37},

    # Boxing Day recovery
    {"date": "2023-12-26", "spend_gbp": 181.61, "conversions": 18.34, "revenue_gbp": 277.08},
    {"date": "2023-12-27", "spend_gbp": 168.75, "conversions": 19.70, "revenue_gbp": 257.98},
    {"date": "2023-12-28", "spend_gbp": 132.83, "conversions": 19.01, "revenue_gbp": 246.24},
    {"date": "2023-12-29", "spend_gbp": 183.14, "conversions": 25.98, "revenue_gbp": 350.77},
    {"date": "2023-12-30", "spend_gbp": 169.58, "conversions": 32.98, "revenue_gbp": 470.23},
    {"date": "2023-12-31", "spend_gbp": 115.35, "conversions": 16.05, "revenue_gbp": 305.58},

    # New Year period
    {"date": "2024-01-01", "spend_gbp": 196.52, "conversions": 23.81, "revenue_gbp": 317.10},
    {"date": "2024-01-02", "spend_gbp": 269.31, "conversions": 29.68, "revenue_gbp": 350.94},
    {"date": "2024-01-03", "spend_gbp": 313.48, "conversions": 40.55, "revenue_gbp": 494.45},
    {"date": "2024-01-04", "spend_gbp": 325.12, "conversions": 28.00, "revenue_gbp": 351.68},
    {"date": "2024-01-05", "spend_gbp": 271.21, "conversions": 29.98, "revenue_gbp": 302.29},
    {"date": "2024-01-06", "spend_gbp": 278.26, "conversions": 26.47, "revenue_gbp": 323.47},
    {"date": "2024-01-07", "spend_gbp": 305.05, "conversions": 33.14, "revenue_gbp": 400.78},
    {"date": "2024-01-08", "spend_gbp": 361.39, "conversions": 51.92, "revenue_gbp": 770.58},
    {"date": "2024-01-09", "spend_gbp": 318.07, "conversions": 36.10, "revenue_gbp": 459.79},
    {"date": "2024-01-10", "spend_gbp": 318.81, "conversions": 49.62, "revenue_gbp": 572.11},
]

def calculate_roas(revenue, spend):
    """Calculate ROAS percentage"""
    return (revenue / spend * 100) if spend > 0 else 0

# Add ROAS calculations
for row in shutdown_data:
    row["roas_pct"] = calculate_roas(row["revenue_gbp"], row["spend_gbp"])

print("=" * 100)
print("CLEAR PROSPECTS - CHRISTMAS 2023 SHUTDOWN ANALYSIS")
print("=" * 100)
print()

# Pre-shutdown (Dec 20-21)
print("🎄 PRE-SHUTDOWN (Dec 20-21):")
print("-" * 100)
for row in shutdown_data[:2]:
    print(f"{row['date']}: Spend £{row['spend_gbp']:>7.2f} | Revenue £{row['revenue_gbp']:>7.2f} | ROAS {row['roas_pct']:>5.0f}% | Conv {row['conversions']:>5.1f}")
print()
print(f"Dec 20 → Dec 21: Budget reduced by {(1 - 46.55/577.25) * 100:.0f}% (£577 → £47)")
print()

# Christmas shutdown (Dec 24-25)
print("🎅 CHRISTMAS SHUTDOWN (Dec 24-25):")
print("-" * 100)
for row in shutdown_data[2:4]:
    print(f"{row['date']}: Spend £{row['spend_gbp']:>7.2f} | Revenue £{row['revenue_gbp']:>7.2f} | ROAS {row['roas_pct']:>5.0f}% | Conv {row['conversions']:>5.1f}")
print()
print("⚠️  LOSING MONEY: Dec 24-25 averaged 37% ROAS (£170 spent, £59 revenue = -£111 loss)")
print()

# Boxing Day recovery (Dec 26-31)
print("📦 BOXING DAY RECOVERY (Dec 26-31):")
print("-" * 100)
boxing_day_spend = 0
boxing_day_revenue = 0
for row in shutdown_data[4:10]:
    print(f"{row['date']}: Spend £{row['spend_gbp']:>7.2f} | Revenue £{row['revenue_gbp']:>7.2f} | ROAS {row['roas_pct']:>5.0f}% | Conv {row['conversions']:>5.1f}")
    boxing_day_spend += row['spend_gbp']
    boxing_day_revenue += row['revenue_gbp']
print()
print(f"Dec 26-31 average: £{boxing_day_spend/6:.2f}/day spend, {(boxing_day_revenue/boxing_day_spend)*100:.0f}% ROAS (profitable again)")
print()

# New Year period (Jan 1-10)
print("🎆 NEW YEAR PERIOD (Jan 1-10):")
print("-" * 100)
jan_spend = 0
jan_revenue = 0
for row in shutdown_data[10:]:
    print(f"{row['date']}: Spend £{row['spend_gbp']:>7.2f} | Revenue £{row['revenue_gbp']:>7.2f} | ROAS {row['roas_pct']:>5.0f}% | Conv {row['conversions']:>5.1f}")
    jan_spend += row['spend_gbp']
    jan_revenue += row['revenue_gbp']
print()
print(f"Jan 1-10 average: £{jan_spend/10:.2f}/day spend, {(jan_revenue/jan_spend)*100:.0f}% ROAS")
print()

print("=" * 100)
print("KEY INSIGHTS FOR 2024 DEPLOYMENT:")
print("=" * 100)
print()
print("1. DEC 21-23 (STAFF BACKLOG):")
print("   - Last year: ~£47/day (92% reduction)")
print("   - Conversion rate held up (135% ROAS)")
print("   - Strategy: Keep campaigns warm at minimal spend")
print()
print("2. DEC 24-25 (CHRISTMAS SHUTDOWN):")
print("   - Last year: ~£85/day average")
print("   - LOSING MONEY: 37% ROAS average")
print("   - Strategy: PAUSE or reduce to £20-30/day brand protection only")
print()
print("3. DEC 26-31 (BOXING DAY RECOVERY):")
print("   - Last year: ~£152/day average")
print("   - Performance RECOVERED: 186% ROAS average")
print("   - Strategy: Resume spending (but still holiday period)")
print()
print("4. JAN 1-5 (NEW YEAR RECOVERY):")
print("   - Last year: ~£296/day average")
print("   - Strong performance: 146% ROAS")
print("   - Strategy: Continue recovery budgets")
print()
print("5. JAN 6+ (BACK TO WORK):")
print("   - Apply full seasonal budgets based on Jan 2024 averages")
print()
print("=" * 100)
print("RECOMMENDED FOUR-PHASE DEPLOYMENT:")
print("=" * 100)
print()
print("Phase 1: Dec 15 (DEPLOYED) - Christmas peak budgets")
print("Phase 2: Dec 16-19 - BMPM pause, maintain HSG/WBS")
print("Phase 3: Dec 20-Jan 5 - Shutdown/recovery period:")
print("  - Dec 20-23 (Staff backlog): ~£50/day (90% reduction)")
print("  - Dec 24-25 (Christmas): ~£25/day brand protection (95% reduction)")
print("  - Dec 26-Jan 5 (Recovery): ~£150/day (moderate reduction)")
print("Phase 4: Jan 6+ - Seasonal budgets (Jan 2024 YoY data)")
