#!/usr/bin/env python3
"""
Superspace US Budget Drop Effectiveness Analysis
Analyzes performance since Nov 13 budget increases through Dec 14
Focus: Stock depletion impact on conversion rate and ROAS
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Raw data from Google Ads API (Nov 13 - Dec 14, 2025)
data = [
    {"date": "2025-11-13", "cost_micros": 7970763562, "conversions": 397.008049, "value": 124363.493815316},
    {"date": "2025-11-14", "cost_micros": 11860207704, "conversions": 414.568256, "value": 134019.141128333},
    {"date": "2025-11-15", "cost_micros": 17857554918, "conversions": 477.088551, "value": 155446.398456066},
    {"date": "2025-11-16", "cost_micros": 15859706764, "conversions": 532.34093, "value": 169113.636107713},
    {"date": "2025-11-17", "cost_micros": 14968902382, "conversions": 438.276757, "value": 138315.233413735},
    {"date": "2025-11-18", "cost_micros": 11202091989, "conversions": 443.056446, "value": 138301.373694561},
    {"date": "2025-11-19", "cost_micros": 9859565692, "conversions": 421.707519, "value": 136193.269527358},
    {"date": "2025-11-20", "cost_micros": 12338827209, "conversions": 506.414756, "value": 158483.612113797},
    {"date": "2025-11-21", "cost_micros": 12099434700, "conversions": 492.134266, "value": 157586.366186221},
    {"date": "2025-11-22", "cost_micros": 12946121543, "conversions": 515.084584, "value": 166967.836356863},
    {"date": "2025-11-23", "cost_micros": 12789473395, "conversions": 567.628077, "value": 182641.83562896},
    {"date": "2025-11-24", "cost_micros": 12578161582, "conversions": 467.932493, "value": 148092.450875956},
    {"date": "2025-11-25", "cost_micros": 10112717151, "conversions": 431.520214, "value": 137466.46165469},
    {"date": "2025-11-26", "cost_micros": 11207868011, "conversions": 411.456818, "value": 131099.853810067},
    {"date": "2025-11-27", "cost_micros": 11071934828, "conversions": 425.965685, "value": 131904.826523437},
    {"date": "2025-11-28", "cost_micros": 15030480046, "conversions": 949.925421, "value": 297873.106090366},  # Black Friday
    {"date": "2025-11-29", "cost_micros": 15264173761, "conversions": 656.249904, "value": 207806.903692088},  # Black Friday
    {"date": "2025-11-30", "cost_micros": 17489604467, "conversions": 509.045543, "value": 162207.450912632},
    {"date": "2025-12-01", "cost_micros": 22763019594, "conversions": 360.435401, "value": 107615.739620284},  # STOCK DEPLETION VISIBLE
    {"date": "2025-12-02", "cost_micros": 15770532742, "conversions": 216.542647, "value": 66830.093196871},
    {"date": "2025-12-03", "cost_micros": 12518622511, "conversions": 129.897543, "value": 38649.934895682},
    {"date": "2025-12-04", "cost_micros": 10829726273, "conversions": 112.779368, "value": 36652.357977835},
    {"date": "2025-12-05", "cost_micros": 9192642255, "conversions": 117.061217, "value": 35369.558512685},
    {"date": "2025-12-06", "cost_micros": 8342509903, "conversions": 124.579605, "value": 36222.737516784},
    {"date": "2025-12-07", "cost_micros": 7718540524, "conversions": 124.277713, "value": 37241.382396481},
    {"date": "2025-12-08", "cost_micros": 8617256923, "conversions": 110.874652, "value": 32863.192501239},
    {"date": "2025-12-09", "cost_micros": 7765132475, "conversions": 106.380783, "value": 33042.636303477},
    {"date": "2025-12-10", "cost_micros": 6387887664, "conversions": 91.107664, "value": 29789.53409158},
    {"date": "2025-12-11", "cost_micros": 6289400093, "conversions": 83.489229, "value": 25419.822148601},
    {"date": "2025-12-12", "cost_micros": 5950279717, "conversions": 105.873733, "value": 31709.610148101},
    {"date": "2025-12-13", "cost_micros": 5728135318, "conversions": 91.586051, "value": 27966.523811602},
    {"date": "2025-12-14", "cost_micros": 5017035166, "conversions": 49.556508, "value": 14222.334864225},
]

# Convert to DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df['spend_gbp'] = df['cost_micros'] / 1_000_000
df['roas'] = (df['value'] / df['spend_gbp']) * 100
df['cpa_gbp'] = df['spend_gbp'] / df['conversions']

# Calculate 7-day rolling averages
df['spend_7d'] = df['spend_gbp'].rolling(window=7, min_periods=1).mean()
df['roas_7d'] = df['roas'].rolling(window=7, min_periods=1).mean()
df['conversions_7d'] = df['conversions'].rolling(window=7, min_periods=1).mean()

# Key intervention dates
interventions = [
    {"date": "2025-11-13", "label": "Budget Increase\n£12k/day", "color": "green"},
    {"date": "2025-11-17", "label": "ROAS 550%→600%", "color": "orange"},
    {"date": "2025-11-20", "label": "Budget -20%\n£11.6k/day", "color": "red"},
    {"date": "2025-11-21", "label": "Budget -10%\n£10.4k/day", "color": "red"},
    {"date": "2025-11-24", "label": "Budget -10%\n£9.4k/day", "color": "red"},
    {"date": "2025-12-01", "label": "Stock Depletion\nVisible", "color": "purple"},
]

# Create comprehensive visualization
fig, axes = plt.subplots(4, 1, figsize=(16, 14), sharex=True)
fig.suptitle('Superspace US: Budget Drop Effectiveness Analysis (Nov 13 - Dec 14, 2025)',
             fontsize=16, fontweight='bold', y=0.995)

# 1. Daily Spend
ax1 = axes[0]
ax1.plot(df['date'], df['spend_gbp'], 'o-', color='#2E86AB', linewidth=2, markersize=4, label='Daily Spend')
ax1.plot(df['date'], df['spend_7d'], '--', color='#A23B72', linewidth=2, alpha=0.7, label='7-Day Average')
ax1.set_ylabel('Spend (£)', fontsize=11, fontweight='bold')
ax1.set_title('Daily Ad Spend', fontsize=12, fontweight='bold', pad=10)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax1.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)
    ax1.text(date, ax1.get_ylim()[1] * 0.95, intervention['label'],
             rotation=90, verticalalignment='top', fontsize=8, color=intervention['color'], fontweight='bold')

# 2. ROAS Performance
ax2 = axes[1]
ax2.plot(df['date'], df['roas'], 'o-', color='#F18F01', linewidth=2, markersize=4, label='Daily ROAS')
ax2.plot(df['date'], df['roas_7d'], '--', color='#C73E1D', linewidth=2, alpha=0.7, label='7-Day Average')
ax2.axhline(600, color='orange', linestyle=':', linewidth=2, alpha=0.5, label='Target ROAS (600%)')
ax2.set_ylabel('ROAS (%)', fontsize=11, fontweight='bold')
ax2.set_title('Return on Ad Spend (ROAS)', fontsize=12, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax2.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)

# 3. Daily Conversions
ax3 = axes[2]
ax3.plot(df['date'], df['conversions'], 'o-', color='#06A77D', linewidth=2, markersize=4, label='Daily Conversions')
ax3.plot(df['date'], df['conversions_7d'], '--', color='#005F60', linewidth=2, alpha=0.7, label='7-Day Average')
ax3.set_ylabel('Conversions', fontsize=11, fontweight='bold')
ax3.set_title('Daily Conversions (Volume Impact)', fontsize=12, fontweight='bold', pad=10)
ax3.grid(True, alpha=0.3)
ax3.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax3.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)

# 4. Cost Per Acquisition
ax4 = axes[3]
ax4.plot(df['date'], df['cpa_gbp'], 'o-', color='#8B1E3F', linewidth=2, markersize=4, label='Daily CPA')
ax4.axhline(50, color='red', linestyle=':', linewidth=2, alpha=0.5, label='Target CPA (£50)')
ax4.set_ylabel('CPA (£)', fontsize=11, fontweight='bold')
ax4.set_xlabel('Date', fontsize=11, fontweight='bold')
ax4.set_title('Cost Per Acquisition', fontsize=12, fontweight='bold', pad=10)
ax4.grid(True, alpha=0.3)
ax4.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax4.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)

# Format x-axis
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax4.xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('/Users/administrator/Documents/PetesBrain.nosync/clients/superspace/analysis/us-budget-drop-effectiveness.png',
            dpi=300, bbox_inches='tight')
print("✅ Chart saved: us-budget-drop-effectiveness.png")

# Generate summary statistics
print("\n" + "="*80)
print("📊 SUPERSPACE US BUDGET DROP EFFECTIVENESS ANALYSIS")
print("="*80)

# Define periods
periods = {
    "Pre-Budget Cuts (Nov 13-19)": ("2025-11-13", "2025-11-19"),
    "Budget Cut Phase (Nov 20-30)": ("2025-11-20", "2025-11-30"),
    "Stock Depletion (Dec 1-14)": ("2025-12-01", "2025-12-14"),
}

for period_name, (start, end) in periods.items():
    period_df = df[(df['date'] >= start) & (df['date'] <= end)]

    avg_spend = period_df['spend_gbp'].mean()
    avg_roas = period_df['roas'].mean()
    avg_conversions = period_df['conversions'].mean()
    avg_cpa = period_df['cpa_gbp'].mean()
    total_spend = period_df['spend_gbp'].sum()
    total_conversions = period_df['conversions'].sum()
    total_value = period_df['value'].sum()

    print(f"\n{period_name}")
    print(f"  • Daily Spend: £{avg_spend:,.0f} (Total: £{total_spend:,.0f})")
    print(f"  • ROAS: {avg_roas:.0f}%")
    print(f"  • Daily Conversions: {avg_conversions:.0f} (Total: {total_conversions:.0f})")
    print(f"  • CPA: £{avg_cpa:.2f}")
    print(f"  • Total Revenue: £{total_value:,.0f}")

# Calculate effectiveness of budget drops
print("\n" + "="*80)
print("📉 BUDGET DROP EFFECTIVENESS")
print("="*80)

pre_cuts = df[(df['date'] >= "2025-11-13") & (df['date'] <= "2025-11-19")]
post_cuts = df[(df['date'] >= "2025-11-20") & (df['date'] <= "2025-11-30")]
stock_depletion = df[(df['date'] >= "2025-12-01") & (df['date'] <= "2025-12-14")]

spend_reduction = ((pre_cuts['spend_gbp'].mean() - post_cuts['spend_gbp'].mean()) / pre_cuts['spend_gbp'].mean()) * 100
conversions_reduction = ((pre_cuts['conversions'].mean() - post_cuts['conversions'].mean()) / pre_cuts['conversions'].mean()) * 100
roas_change = post_cuts['roas'].mean() - pre_cuts['roas'].mean()

print(f"\nNov 20-30 (Budget Cut Period) vs Nov 13-19 (Pre-Cut):")
print(f"  • Spend Reduction: {spend_reduction:.1f}%")
print(f"  • Conversions Reduction: {conversions_reduction:.1f}%")
print(f"  • ROAS Change: {roas_change:+.0f} percentage points ({post_cuts['roas'].mean():.0f}% vs {pre_cuts['roas'].mean():.0f}%)")

# Stock depletion impact
stock_spend_reduction = ((post_cuts['spend_gbp'].mean() - stock_depletion['spend_gbp'].mean()) / post_cuts['spend_gbp'].mean()) * 100
stock_conversions_reduction = ((post_cuts['conversions'].mean() - stock_depletion['conversions'].mean()) / post_cuts['conversions'].mean()) * 100
stock_roas_change = stock_depletion['roas'].mean() - post_cuts['roas'].mean()

print(f"\nDec 1-14 (Stock Depletion) vs Nov 20-30 (Budget Cut Period):")
print(f"  • Spend Reduction: {stock_spend_reduction:.1f}%")
print(f"  • Conversions Reduction: {stock_conversions_reduction:.1f}%")
print(f"  • ROAS Change: {stock_roas_change:+.0f} percentage points ({stock_depletion['roas'].mean():.0f}% vs {post_cuts['roas'].mean():.0f}%)")

# Critical findings
print("\n" + "="*80)
print("🚨 CRITICAL FINDINGS")
print("="*80)

recent_7d = df.tail(7)
print(f"\nLast 7 Days (Dec 8-14) Performance:")
print(f"  • Average Spend: £{recent_7d['spend_gbp'].mean():,.0f}/day")
print(f"  • Average ROAS: {recent_7d['roas'].mean():.0f}%")
print(f"  • Average Conversions: {recent_7d['conversions'].mean():.0f}/day")
print(f"  • Average CPA: £{recent_7d['cpa_gbp'].mean():.2f}")

# Dec 1 spike analysis
dec1_row = df[df['date'] == "2025-12-01"].iloc[0]
print(f"\nDec 1 Anomaly (Stock Visible But Depleting):")
print(f"  • Spend: £{dec1_row['spend_gbp']:,.0f} (HIGHEST SINGLE DAY)")
print(f"  • ROAS: {dec1_row['roas']:.0f}% (DROPPED BELOW TARGET)")
print(f"  • Conversions: {dec1_row['conversions']:.0f}")
print(f"  • CPA: £{dec1_row['cpa_gbp']:.2f}")

print("\n" + "="*80)
print("✅ Analysis complete. Chart saved to clients/superspace/analysis/")
print("="*80)
