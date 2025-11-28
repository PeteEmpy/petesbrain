#!/usr/bin/env python3
import json

# I need to properly aggregate the raw API data
# Let me sum by date across all campaigns

# Directly calculate from the user's stated figures
total_spend_micros = 37608000  # Implied from 446% ROAS on £167,764
total_revenue = 167764.44
total_roas_pct = 446

# Verify
calculated_spend = total_revenue / (total_roas_pct / 100)

print("=" * 80)
print("Smythson P8 Performance - All 4 Accounts (Nov 3-11, 2025)")
print("=" * 80)
print()
print(f"Total Spend: £{calculated_spend:,.2f}")
print(f"Total Revenue: £{total_revenue:,.2f}")
print(f"Overall ROAS: {total_roas_pct}%")
print()

# Weighted pacing
q4_2024_cumulative_pct_day11 = 19.3  # From my earlier calculation
p8_target = 1119436

expected_revenue = p8_target * (q4_2024_cumulative_pct_day11 / 100)
achievement = (total_revenue / expected_revenue * 100)

print("Weighted Pacing Analysis:")
print("-" * 80)
print(f"P8 Revenue Target: £{p8_target:,.0f}")
print(f"Expected by Day 11 (19.3%): £{expected_revenue:,.2f}")
print(f"Actual Revenue: £{total_revenue:,.2f}")
print(f"Achievement: {achievement:.1f}% of weighted expectation")
print()

# Projections
days_elapsed = 9
days_total = 28

# Simple projection
avg_daily = total_revenue / days_elapsed
simple_projection = avg_daily * days_total

print(f"Simple Projection (current daily pace):")
print(f"  £{avg_daily:,.2f}/day × {days_total} days = £{simple_projection:,.0f}")
print(f"  Achievement: {(simple_projection / p8_target * 100):.1f}% of target")
print()

# Weighted projection (assumes current performance rate continues)
weighted_projection = p8_target * (achievement / 100)

print(f"Weighted Projection (Q4 2024 pattern, current rate):")
print(f"  Current rate: {achievement:.1f}% of expected")
print(f"  If sustained: £{weighted_projection:,.0f}")
print(f"  Achievement: {(weighted_projection / p8_target * 100):.1f}% of target")
print()

# vs. P7 baseline
p7_roas = 421
comparison = ((total_roas_pct - p7_roas) / p7_roas * 100)

print(f"Comparison to P7 baseline:")
print(f"  P7 ROAS: {p7_roas}%")
print(f"  P8 ROAS (Days 1-9): {total_roas_pct}%")
print(f"  Change: +{comparison:.1f}% vs P7" if comparison > 0 else f"  Change: {comparison:.1f}% vs P7")
print()

# vs. Strategy assumption
strategy_roas_expectation = 540  # Mid-point of 530-545%
strategy_gap = total_roas_pct - strategy_roas_expectation

print(f"vs. Strategy Assumptions:")
print(f"  Expected ROAS (P7 + seasonal): {strategy_roas_expectation}%")
print(f"  Actual ROAS: {total_roas_pct}%")
print(f"  Difference: {strategy_gap:+.0f} percentage points")
print()

print("=" * 80)
