#!/usr/bin/env python3
"""
Calculate Q4 2024 daily revenue distribution for Smythson UK
This creates weighted pacing factors based on actual Q4 2024 performance
"""

import json
from collections import defaultdict

# Q4 2024 UK revenue data from Google Ads (Nov 2024 shown, add Oct/Dec later)
nov_2024_data = {
    "2024-11-01": 8294.177,
    "2024-11-02": 6855.888,
    "2024-11-03": 9642.235,
    "2024-11-04": 10286.548,
    "2024-11-05": 9071.688,
    "2024-11-06": 11190.147,
    "2024-11-07": 11289.401,
    "2024-11-08": 13369.078,
    "2024-11-09": 7999.820,
    "2024-11-10": 13388.185,
    "2024-11-11": 15783.670,
    "2024-11-12": 15964.831,
    "2024-11-13": 17768.161,
    "2024-11-14": 8288.421,
    "2024-11-15": 11385.386,
    "2024-11-16": 11563.905,
    "2024-11-17": 14000.447,
    "2024-11-18": 24798.695,
    "2024-11-19": 20836.905,
    "2024-11-20": 23915.099,
    "2024-11-21": 19193.097,
    "2024-11-22": 35716.983,
    "2024-11-23": 48542.893,  # Black Friday - MASSIVE spike
    "2024-11-24": 26549.229,
    "2024-11-25": 26636.985,
    "2024-11-26": 35568.250,
    "2024-11-27": 31338.072,
    "2024-11-28": 32856.335,
    "2024-11-29": 53710.193,  # Cyber Monday - MASSIVE spike
    "2024-11-30": 32359.912
}

# Aggregate by day (sum across campaigns - already done above)
# Calculate total month revenue
total_nov = sum(nov_2024_data.values())
print(f"Total November 2024 UK Revenue: £{total_nov:,.2f}")
print()

# Calculate daily percentages
daily_percentages = {}
cumulative_pct = 0

print("Daily Revenue Distribution (Nov 2024):")
print("=" * 70)
print(f"{'Date':<12} {'Revenue':>15} {'% of Month':>12} {'Cumulative':>12}")
print("=" * 70)

for date, revenue in sorted(nov_2024_data.items()):
    day_pct = (revenue / total_nov) * 100
    cumulative_pct += day_pct
    daily_percentages[date] = day_pct

    day_num = int(date.split('-')[2])
    marker = ""
    if day_pct > 7:  # Highlight big days
        marker = " ⭐ PEAK"
    elif day_pct > 4:
        marker = " 🔥"

    print(f"{date:<12} £{revenue:>13,.0f} {day_pct:>11.2f}% {cumulative_pct:>11.1f}%{marker}")

print("=" * 70)
print()

# Calculate average daily revenue
avg_daily = total_nov / 30
print(f"Average Daily Revenue: £{avg_daily:,.0f}")
print()

# Calculate multipliers vs average
print("Daily Multipliers vs Average:")
print("=" * 70)
print(f"{'Date':<12} {'Multiplier':>12} {'Description'}")
print("=" * 70)

daily_multipliers = {}
for date, revenue in sorted(nov_2024_data.items()):
    multiplier = revenue / avg_daily
    daily_multipliers[date] = multiplier

    day_num = int(date.split('-')[2])

    if multiplier >= 3.0:
        desc = "MASSIVE PEAK"
    elif multiplier >= 2.0:
        desc = "Major Peak"
    elif multiplier >= 1.5:
        desc = "Peak Day"
    elif multiplier >= 1.2:
        desc = "Above Average"
    elif multiplier >= 0.8:
        desc = "Normal"
    else:
        desc = "Below Average"

    print(f"{date:<12} {multiplier:>11.2f}x {desc}")

print("=" * 70)
print()

# Key insights
print("KEY INSIGHTS:")
print("-" * 70)
print(f"Black Friday (Nov 23): {daily_multipliers['2024-11-23']:.2f}x average (£{nov_2024_data['2024-11-23']:,.0f})")
print(f"Cyber Monday (Nov 29): {daily_multipliers['2024-11-29']:.2f}x average (£{nov_2024_data['2024-11-29']:,.0f})")
print()

# Black Friday weekend (Nov 22-25)
bf_weekend = sum([nov_2024_data[f'2024-11-{d}'] for d in range(22, 26)])
bf_pct = (bf_weekend / total_nov) * 100
print(f"Black Friday Weekend (Nov 22-25): £{bf_weekend:,.0f} ({bf_pct:.1f}% of month)")
print()

# Full week including Cyber Monday (Nov 22-30)
bf_week = sum([nov_2024_data[f'2024-11-{d:02d}'] for d in range(22, 31)])
bf_week_pct = (bf_week / total_nov) * 100
print(f"Black Friday Week (Nov 22-30): £{bf_week:,.0f} ({bf_week_pct:.1f}% of month)")
print()

# First half vs second half
first_half = sum([nov_2024_data[f'2024-11-{d:02d}'] for d in range(1, 16)])
second_half = sum([nov_2024_data[f'2024-11-{d:02d}'] for d in range(16, 31)])
print(f"First Half (Nov 1-15): £{first_half:,.0f} ({(first_half/total_nov)*100:.1f}%)")
print(f"Second Half (Nov 16-30): £{second_half:,.0f} ({(second_half/total_nov)*100:.1f}%)")
print()

# Save multipliers for use in dashboard
output = {
    "month": "2024-11",
    "total_revenue": total_nov,
    "avg_daily_revenue": avg_daily,
    "daily_multipliers": daily_multipliers,
    "daily_percentages": daily_percentages
}

with open('q4-2024-revenue-distribution.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Multipliers saved to: q4-2024-revenue-distribution.json")
print()
print("Use these multipliers in dashboard's calculate_weighted_pacing() function")
