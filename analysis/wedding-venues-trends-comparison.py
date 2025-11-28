#!/usr/bin/env python3
"""
Wedding Venues Google Trends Comparison
Comparing Nov 2024 - Nov 2025 vs Nov 2023 - Nov 2024
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Data from Google Trends
current_year = [
    ("2024-11-24", 47), ("2024-12-01", 45), ("2024-12-08", 49), ("2024-12-15", 53),
    ("2024-12-22", 71), ("2024-12-29", 100), ("2025-01-05", 88), ("2025-01-12", 77),
    ("2025-01-19", 76), ("2025-01-26", 74), ("2025-02-02", 69), ("2025-02-09", 66),
    ("2025-02-16", 75), ("2025-02-23", 68), ("2025-03-02", 60), ("2025-03-09", 66),
    ("2025-03-16", 63), ("2025-03-23", 62), ("2025-03-30", 62), ("2025-04-06", 63),
    ("2025-04-13", 70), ("2025-04-20", 79), ("2025-04-27", 63), ("2025-05-04", 70),
    ("2025-05-11", 72), ("2025-05-18", 69), ("2025-05-25", 83), ("2025-06-01", 78),
    ("2025-06-08", 81), ("2025-06-15", 75), ("2025-06-22", 75), ("2025-06-29", 77),
    ("2025-07-06", 74), ("2025-07-13", 76), ("2025-07-20", 79), ("2025-07-27", 89),
    ("2025-08-03", 94), ("2025-08-10", 79), ("2025-08-17", 90), ("2025-08-24", 96),
    ("2025-08-31", 80), ("2025-09-07", 81), ("2025-09-14", 74), ("2025-09-21", 77),
    ("2025-09-28", 74), ("2025-10-05", 71), ("2025-10-12", 70), ("2025-10-19", 68),
    ("2025-10-26", 69), ("2025-11-02", 59), ("2025-11-09", 56), ("2025-11-16", 53),
    ("2025-11-23", 55)
]

previous_year = [
    ("2023-11-19", 51), ("2023-11-26", 45), ("2023-12-03", 51), ("2023-12-10", 48),
    ("2023-12-17", 49), ("2023-12-24", 81), ("2023-12-31", 100), ("2024-01-07", 90),
    ("2024-01-14", 90), ("2024-01-21", 81), ("2024-01-28", 79), ("2024-02-04", 73),
    ("2024-02-11", 78), ("2024-02-18", 69), ("2024-02-25", 71), ("2024-03-03", 64),
    ("2024-03-10", 66), ("2024-03-17", 66), ("2024-03-24", 68), ("2024-03-31", 77),
    ("2024-04-07", 73), ("2024-04-14", 66), ("2024-04-21", 71), ("2024-04-28", 67),
    ("2024-05-05", 71), ("2024-05-12", 69), ("2024-05-19", 74), ("2024-05-26", 95),
    ("2024-06-02", 77), ("2024-06-09", 77), ("2024-06-16", 72), ("2024-06-23", 76),
    ("2024-06-30", 74), ("2024-07-07", 89), ("2024-07-14", 78), ("2024-07-21", 89),
    ("2024-07-28", 83), ("2024-08-04", 84), ("2024-08-11", 95), ("2024-08-18", 95),
    ("2024-08-25", 93), ("2024-09-01", 80), ("2024-09-08", 83), ("2024-09-15", 81),
    ("2024-09-22", 78), ("2024-09-29", 77), ("2024-10-06", 78), ("2024-10-13", 74),
    ("2024-10-20", 75), ("2024-10-27", 72), ("2024-11-03", 62), ("2024-11-10", 57),
    ("2024-11-17", 51), ("2024-11-24", 50)
]

# Create DataFrames
df_current = pd.DataFrame(current_year, columns=['date', 'interest'])
df_previous = pd.DataFrame(previous_year, columns=['date', 'interest'])

df_current['date'] = pd.to_datetime(df_current['date'])
df_previous['date'] = pd.to_datetime(df_previous['date'])

# Normalize dates to compare same periods (shift previous year by 1 year)
df_previous['normalized_date'] = df_previous['date'] + pd.DateOffset(years=1)

# Create the figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

# Plot 1: Overlay comparison
ax1.plot(df_current['date'], df_current['interest'],
         linewidth=2.5, color='#2E86AB', marker='o', markersize=4,
         label='Nov 2024 - Nov 2025', alpha=0.8)
ax1.plot(df_previous['normalized_date'], df_previous['interest'],
         linewidth=2.5, color='#E63946', marker='s', markersize=4,
         label='Nov 2023 - Nov 2024 (shifted)', alpha=0.6, linestyle='--')

ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
ax1.set_ylabel('Search Interest (0-100)', fontsize=12, fontweight='bold')
ax1.set_title('Wedding Venues Search Trends: Year-over-Year Comparison (GB)',
              fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
ax1.legend(loc='upper left', fontsize=11)

# Add peak annotations
ax1.axhline(y=100, color='gray', linestyle=':', alpha=0.3)
ax1.text(df_current['date'].iloc[5], 102, 'Peak: New Year (100)',
         fontsize=9, ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

# Plot 2: Month-by-month comparison
months = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
current_monthly = []
previous_monthly = []

# Calculate monthly averages
for i in range(12):
    start_idx = i * 4
    end_idx = start_idx + 4
    if end_idx <= len(df_current):
        current_monthly.append(df_current['interest'].iloc[start_idx:end_idx].mean())
        previous_monthly.append(df_previous['interest'].iloc[start_idx:end_idx].mean())

x = range(len(months))
width = 0.35

bars1 = ax2.bar([i - width/2 for i in x], current_monthly, width,
                label='2024-2025', color='#2E86AB', alpha=0.8)
bars2 = ax2.bar([i + width/2 for i in x], previous_monthly, width,
                label='2023-2024', color='#E63946', alpha=0.6)

ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
ax2.set_ylabel('Average Search Interest', fontsize=12, fontweight='bold')
ax2.set_title('Monthly Average Comparison', fontsize=13, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(months)
ax2.legend(loc='upper left', fontsize=11)
ax2.grid(True, alpha=0.3, linestyle=':', linewidth=0.5, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# Save
output_path = '/Users/administrator/Documents/PetesBrain/analysis/wedding-venues-trends-comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Chart saved to: {output_path}")

# Statistics
print("\n" + "="*70)
print("WEDDING VENUES SEARCH TRENDS - YEAR-OVER-YEAR ANALYSIS (GB)")
print("="*70)

print("\nCurrent Year (Nov 2024 - Nov 2025):")
print(f"  Average interest: {df_current['interest'].mean():.1f}")
print(f"  Peak: {df_current['interest'].max()} (New Year period)")
print(f"  Low: {df_current['interest'].min()} (Dec 2024)")
print(f"  Current (Nov 2025): {df_current['interest'].iloc[-1]}")

print("\nPrevious Year (Nov 2023 - Nov 2024):")
print(f"  Average interest: {df_previous['interest'].mean():.1f}")
print(f"  Peak: {df_previous['interest'].max()} (New Year period)")
print(f"  Low: {df_previous['interest'].min()} (Nov 2023)")
print(f"  End (Nov 2024): {df_previous['interest'].iloc[-1]}")

print("\nYear-over-Year Change:")
print(f"  Average: {((df_current['interest'].mean() / df_previous['interest'].mean()) - 1) * 100:+.1f}%")
print(f"  Nov 2025 vs Nov 2024: {df_current['interest'].iloc[-1]} vs {df_previous['interest'].iloc[-1]} ({df_current['interest'].iloc[-1] - df_previous['interest'].iloc[-1]:+d})")

print("\n" + "="*70)
print("KEY INSIGHTS")
print("="*70)
print("• Peak season: New Year (Dec-Jan) - 100 search interest")
print("• Wedding planning season: Late summer (Aug) - 94-96 interest")
print("• Low season: November - 50-55 interest")
print("• Trends are remarkably consistent year-over-year")

plt.show()
