#!/usr/bin/env python3
"""
Analyze P8 performance across all four Smythson accounts (UK, USA, EUR, ROW)
Nov 3-11, 2025 (9 days)
"""

# Raw data from Google Ads API
# UK account: 8573235780
uk_data = [
    # Nov 3-11 data - sum of all campaign rows per day
    {"date": "2025-11-03", "cost": 1208386, "revenue": 9775.98},
    {"date": "2025-11-04", "cost": 1341154, "revenue": 8614.95},
    {"date": "2025-11-05", "cost": 1494236, "revenue": 11656.13},
    {"date": "2025-11-06", "cost": 2089473, "revenue": 11111.53},
    {"date": "2025-11-07", "cost": 2316439, "revenue": 11805.68},
    {"date": "2025-11-08", "cost": 2633404, "revenue": 4830.94},
    {"date": "2025-11-09", "cost": 3059134, "revenue": 4562.74},
    {"date": "2025-11-10", "cost": 2699234, "revenue": 12122.67},
    {"date": "2025-11-11", "cost": 1240267, "revenue": 2815.51},
]

# USA account: 7808690871
usa_data = [
    {"date": "2025-11-03", "cost": 1143970, "revenue": 7745.73},
    {"date": "2025-11-04", "cost": 1229942, "revenue": 11136.09},
    {"date": "2025-11-05", "cost": 1199505, "revenue": 12066.91},
    {"date": "2025-11-06", "cost": 1830147, "revenue": 7901.05},
    {"date": "2025-11-07", "cost": 1986793, "revenue": 10465.85},
    {"date": "2025-11-08", "cost": 2111853, "revenue": 8978.73},
    {"date": "2025-11-09", "cost": 2536298, "revenue": 8465.47},
    {"date": "2025-11-10", "cost": 2598971, "revenue": 6815.38},
    {"date": "2025-11-11", "cost": 802962, "revenue": 1089.00},
]

# EUR account: 7679616761
eur_data = [
    {"date": "2025-11-03", "cost": 278400, "revenue": 1220.01},
    {"date": "2025-11-04", "cost": 294313, "revenue": 952.37},
    {"date": "2025-11-05", "cost": 348370, "revenue": 1725.85},
    {"date": "2025-11-06", "cost": 596025, "revenue": 3055.50},
    {"date": "2025-11-07", "cost": 438021, "revenue": 2068.27},
    {"date": "2025-11-08", "cost": 391495, "revenue": 1030.50},
    {"date": "2025-11-09", "cost": 565459, "revenue": 3746.95},
    {"date": "2025-11-10", "cost": 584846, "revenue": 7987.27},
    {"date": "2025-11-11", "cost": 148594, "revenue": 328.01},
]

# ROW account: 5556710725
row_data = [
    {"date": "2025-11-03", "cost": 90011, "revenue": 1177.18},
    {"date": "2025-11-04", "cost": 156742, "revenue": 1441.38},
    {"date": "2025-11-05", "cost": 171489, "revenue": 1714.18},
    {"date": "2025-11-06", "cost": 306726, "revenue": 707.90},
    {"date": "2025-11-07", "cost": 243176, "revenue": 435.03},
    {"date": "2025-11-08", "cost": 192095, "revenue": 1269.80},
    {"date": "2025-11-09", "cost": 372555, "revenue": 659.54},
    {"date": "2025-11-10", "cost": 233481, "revenue": 430.27},
    {"date": "2025-11-11", "cost": 92959, "revenue": 448.31},
]

def analyze_all_accounts():
    """Aggregate and analyze all four accounts"""

    # Aggregate by date
    totals_by_date = {}

    for account_data in [uk_data, usa_data, eur_data, row_data]:
        for day in account_data:
            date = day["date"]
            if date not in totals_by_date:
                totals_by_date[date] = {"cost": 0, "revenue": 0}

            # Convert micros to pounds
            totals_by_date[date]["cost"] += day["cost"] / 1_000_000
            totals_by_date[date]["revenue"] += day["revenue"]

    # Calculate daily ROAS and print
    print("=" * 80)
    print("Smythson P8 Performance - All Accounts Combined (Nov 3-11, 2025)")
    print("=" * 80)
    print()
    print(f"{'Date':<12} {'Spend (£)':<15} {'Revenue (£)':<15} {'ROAS':<10} {'Day'}")
    print("-" * 80)

    total_cost = 0
    total_revenue = 0

    for i, date in enumerate(sorted(totals_by_date.keys()), 1):
        data = totals_by_date[date]
        cost = data["cost"]
        revenue = data["revenue"]
        roas = (revenue / cost * 100) if cost > 0 else 0

        total_cost += cost
        total_revenue += revenue

        print(f"{date:<12} £{cost:>13,.2f} £{revenue:>13,.2f} {roas:>8,.0f}% Day {i}")

    print("-" * 80)
    overall_roas = (total_revenue / total_cost * 100) if total_cost > 0 else 0
    print(f"{'TOTAL':<12} £{total_cost:>13,.2f} £{total_revenue:>13,.2f} {overall_roas:>8,.0f}%")
    print("=" * 80)
    print()

    # Calculate weighted pacing
    print("Weighted Pacing Analysis")
    print("-" * 80)

    # Q4 2024 daily percentages for Nov 1-11
    q4_2024_percentages = {
        1: 1.36, 2: 1.13, 3: 1.59, 4: 1.69, 5: 1.49,
        6: 1.84, 7: 1.86, 8: 2.20, 9: 1.32, 10: 2.20, 11: 2.60
    }

    cumulative_expected_pct = sum([q4_2024_percentages[i] for i in range(1, 12)])  # Days 1-11
    print(f"Days 1-11 expected share of monthly revenue (Q4 2024): {cumulative_expected_pct:.1f}%")
    print()

    # P8 targets from P8/P9 analysis document
    p8_revenue_target = 1119436  # £1.119M

    expected_revenue = p8_revenue_target * (cumulative_expected_pct / 100)
    achievement_pct = (total_revenue / expected_revenue * 100) if expected_revenue > 0 else 0

    print(f"P8 Revenue Target: £{p8_revenue_target:,.0f}")
    print(f"Expected by Day 11: £{expected_revenue:,.2f} ({cumulative_expected_pct:.1f}% of target)")
    print(f"Actual Revenue: £{total_revenue:,.2f}")
    print(f"Achievement: {achievement_pct:.1f}% of weighted expectation")
    print()

    # Projection to end of P8
    if total_revenue > 0:
        days_elapsed = 9
        days_remaining = 19  # 28 - 9

        # Simple extrapolation (not weighted - conservative)
        avg_daily_revenue = total_revenue / days_elapsed
        projected_revenue_simple = total_revenue + (avg_daily_revenue * days_remaining)

        print(f"Simple Projection (current pace):")
        print(f"  £{avg_daily_revenue:,.2f}/day × {days_remaining} days = £{projected_revenue_simple:,.0f} total")
        print(f"  Achievement: {(projected_revenue_simple / p8_revenue_target * 100):.1f}% of target")
        print()

        # Weighted projection (accounts for Black Friday week)
        # Days 1-11 = 17.9% of month
        # Days 12-21 = 29.1% of month
        # Days 22-28 = 53.0% of month (Black Friday week)

        remaining_nov_expected_pct = 100 - cumulative_expected_pct  # 82.1%

        # We've achieved X% of the first 17.9%
        # Assume we'll achieve the same % of the remaining 82.1%
        performance_rate = achievement_pct / 100  # e.g., 0.925 if we're at 92.5%

        projected_revenue_weighted = p8_revenue_target * performance_rate

        print(f"Weighted Projection (Q4 2024 pattern, current performance rate):")
        print(f"  Current rate: {achievement_pct:.1f}% of weighted expectation")
        print(f"  If sustained: £{projected_revenue_weighted:,.0f} total")
        print(f"  Achievement: {(projected_revenue_weighted / p8_revenue_target * 100):.1f}% of target")
        print()

    # Regional breakdown
    print("Regional Performance (Nov 3-11)")
    print("-" * 80)

    regions = [
        ("UK", uk_data),
        ("USA", usa_data),
        ("EUR", eur_data),
        ("ROW", row_data)
    ]

    for region_name, region_data in regions:
        region_cost = sum([d["cost"] for d in region_data]) / 1_000_000
        region_revenue = sum([d["revenue"] for d in region_data])
        region_roas = (region_revenue / region_cost * 100) if region_cost > 0 else 0
        share_of_revenue = (region_revenue / total_revenue * 100) if total_revenue > 0 else 0

        print(f"{region_name:>4}: £{region_cost:>10,.2f} spend → £{region_revenue:>10,.2f} revenue ({region_roas:>5.0f}% ROAS) [{share_of_revenue:>4.1f}% of total]")

    print("=" * 80)

if __name__ == "__main__":
    analyze_all_accounts()
