#!/usr/bin/env python3
"""
Superspace US: Profitability Analysis (Stock Depletion Period)
Nov 13 - Dec 13, 2025 (excludes Dec 14 partial day)

Key Question: Are we losing money or just making less profit?
Context: Products show "Sold out for Christmas shipping early January"
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Raw data from Google Ads API (Nov 13 - Dec 13, 2025)
# EXCLUDING Dec 14 to avoid partial day skewing
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
]

# Convert to DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df['spend_gbp'] = df['cost_micros'] / 1_000_000
df['roas'] = (df['value'] / df['spend_gbp']) * 100

# Business metrics (from CONTEXT.md)
GROSS_MARGIN = 0.43  # 43% gross margin
TAX_RATE = 0.06      # 6% US tax
TARGET_ROAS = 600    # 600% target ROAS

# Calculate profitability
df['gross_profit'] = df['value'] * GROSS_MARGIN
df['net_profit'] = df['gross_profit'] - df['spend_gbp']
df['profit_margin'] = (df['net_profit'] / df['spend_gbp']) * 100
df['roi'] = (df['net_profit'] / df['spend_gbp']) * 100

# Calculate 7-day rolling averages
df['spend_7d'] = df['spend_gbp'].rolling(window=7, min_periods=1).mean()
df['roas_7d'] = df['roas'].rolling(window=7, min_periods=1).mean()
df['net_profit_7d'] = df['net_profit'].rolling(window=7, min_periods=1).mean()

# Create comprehensive visualization
fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
fig.suptitle('Superspace US: Profitability Analysis (Nov 13 - Dec 13, 2025)\n"Are We Losing Money or Just Making Less?"',
             fontsize=16, fontweight='bold', y=0.995)

# Key intervention dates
interventions = [
    {"date": "2025-11-13", "label": "Budget Increase\n£12k/day", "color": "green"},
    {"date": "2025-11-17", "label": "ROAS 550%→600%", "color": "orange"},
    {"date": "2025-11-20", "label": "Budget -20%", "color": "red"},
    {"date": "2025-11-21", "label": "Budget -10%", "color": "red"},
    {"date": "2025-11-24", "label": "Budget -10%", "color": "red"},
    {"date": "2025-12-01", "label": "Stock Depletion\nVisible", "color": "purple"},
]

# 1. Daily Net Profit
ax1 = axes[0]
colors = ['green' if x > 0 else 'red' for x in df['net_profit']]
ax1.bar(df['date'], df['net_profit'], color=colors, alpha=0.6, label='Daily Net Profit')
ax1.plot(df['date'], df['net_profit_7d'], '--', color='black', linewidth=2, label='7-Day Average')
ax1.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.3)
ax1.set_ylabel('Net Profit (£)', fontsize=11, fontweight='bold')
ax1.set_title('Daily Net Profit (Revenue × 43% Margin - Ad Spend)', fontsize=12, fontweight='bold', pad=10)
ax1.grid(True, alpha=0.3, axis='y')
ax1.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax1.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)
    if intervention['label'] == "Stock Depletion\nVisible":
        ax1.text(date, ax1.get_ylim()[1] * 0.95, intervention['label'],
                 rotation=90, verticalalignment='top', fontsize=8, color=intervention['color'], fontweight='bold')

# 2. ROAS vs Profitability Threshold
ax2 = axes[1]
ax2.plot(df['date'], df['roas'], 'o-', color='#F18F01', linewidth=2, markersize=4, label='Daily ROAS')
ax2.plot(df['date'], df['roas_7d'], '--', color='#C73E1D', linewidth=2, alpha=0.7, label='7-Day Average')
ax2.axhline(600, color='orange', linestyle=':', linewidth=2, alpha=0.5, label='Target ROAS (600%)')

# Calculate breakeven ROAS (where net profit = 0)
# breakeven: (revenue × margin) - spend = 0
# revenue × margin = spend
# revenue = spend / margin
# ROAS = (revenue / spend) × 100 = (spend / margin / spend) × 100 = 100 / margin
breakeven_roas = (1 / GROSS_MARGIN) * 100
ax2.axhline(breakeven_roas, color='red', linestyle=':', linewidth=2, alpha=0.7, label=f'Breakeven ROAS ({breakeven_roas:.0f}%)')

ax2.set_ylabel('ROAS (%)', fontsize=11, fontweight='bold')
ax2.set_title('ROAS Performance (Breakeven = 233% | Target = 600%)', fontsize=12, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax2.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)

# 3. ROI (Return on Investment)
ax3 = axes[2]
ax3.plot(df['date'], df['roi'], 'o-', color='#06A77D', linewidth=2, markersize=4, label='Daily ROI')
ax3.axhline(0, color='red', linestyle='-', linewidth=2, alpha=0.5, label='Breakeven (0% ROI)')
ax3.axhline(100, color='green', linestyle=':', linewidth=2, alpha=0.5, label='Double Your Money (100% ROI)')
ax3.set_ylabel('ROI (%)', fontsize=11, fontweight='bold')
ax3.set_xlabel('Date', fontsize=11, fontweight='bold')
ax3.set_title('Return on Investment (Net Profit / Ad Spend)', fontsize=12, fontweight='bold', pad=10)
ax3.grid(True, alpha=0.3)
ax3.legend(loc='upper right')

# Add intervention lines
for intervention in interventions:
    date = pd.to_datetime(intervention['date'])
    ax3.axvline(date, color=intervention['color'], linestyle='--', alpha=0.5, linewidth=1.5)

# Format x-axis
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax3.xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('/Users/administrator/Documents/PetesBrain.nosync/clients/superspace/analysis/us-profitability-analysis.png',
            dpi=300, bbox_inches='tight')
print("✅ Chart saved: us-profitability-analysis.png")

# Generate summary statistics
print("\n" + "="*80)
print("💰 SUPERSPACE US: PROFITABILITY ANALYSIS (Nov 13 - Dec 13, 2025)")
print("="*80)
print(f"\nBusiness Assumptions:")
print(f"  • Gross Margin: {GROSS_MARGIN*100:.0f}%")
print(f"  • Breakeven ROAS: {breakeven_roas:.0f}% (any ROAS above this = profit)")
print(f"  • Target ROAS: {TARGET_ROAS:.0f}%")

# Define periods
periods = {
    "Pre-Budget Cuts (Nov 13-19)": ("2025-11-13", "2025-11-19"),
    "Budget Cut Phase (Nov 20-30)": ("2025-11-20", "2025-11-30"),
    "Stock Depletion (Dec 1-13)": ("2025-12-01", "2025-12-13"),
}

for period_name, (start, end) in periods.items():
    period_df = df[(df['date'] >= start) & (df['date'] <= end)]

    total_spend = period_df['spend_gbp'].sum()
    total_revenue = period_df['value'].sum()
    total_gross_profit = period_df['gross_profit'].sum()
    total_net_profit = period_df['net_profit'].sum()
    avg_roas = period_df['roas'].mean()
    avg_roi = period_df['roi'].mean()

    days_count = len(period_df)
    daily_net_profit = total_net_profit / days_count

    print(f"\n{period_name} ({days_count} days)")
    print(f"  • Total Spend: £{total_spend:,.0f}")
    print(f"  • Total Revenue: £{total_revenue:,.0f}")
    print(f"  • Gross Profit (43%): £{total_gross_profit:,.0f}")
    print(f"  • NET PROFIT: £{total_net_profit:,.0f} (£{daily_net_profit:,.0f}/day)")
    print(f"  • Average ROAS: {avg_roas:.0f}%")
    print(f"  • Average ROI: {avg_roi:.0f}%")

    if total_net_profit > 0:
        print(f"  • Status: ✅ PROFITABLE (making £{daily_net_profit:,.0f}/day)")
    else:
        print(f"  • Status: ❌ LOSING MONEY (losing £{abs(daily_net_profit):,.0f}/day)")

# Critical Question: Are we losing money NOW?
print("\n" + "="*80)
print("🚨 CRITICAL QUESTION: Are We Losing Money Now?")
print("="*80)

last_7_days = df.tail(7)
last_7_spend = last_7_days['spend_gbp'].sum()
last_7_revenue = last_7_days['value'].sum()
last_7_net_profit = last_7_days['net_profit'].sum()
last_7_avg_roas = last_7_days['roas'].mean()
last_7_daily_profit = last_7_net_profit / 7

print(f"\nLast 7 Days (Dec 7-13):")
print(f"  • Total Spend: £{last_7_spend:,.0f}")
print(f"  • Total Revenue: £{last_7_revenue:,.0f}")
print(f"  • Net Profit: £{last_7_net_profit:,.0f}")
print(f"  • Daily Net Profit: £{last_7_daily_profit:,.0f}/day")
print(f"  • Average ROAS: {last_7_avg_roas:.0f}%")

if last_7_net_profit > 0:
    print(f"\n✅ ANSWER: NO, we are NOT losing money.")
    print(f"   We are making £{last_7_daily_profit:,.0f}/day net profit.")
    print(f"   ROAS is {last_7_avg_roas:.0f}% (above {breakeven_roas:.0f}% breakeven).")
    print(f"\n   We ARE making LESS profit than ideal:")

    # Calculate what profit SHOULD be at 600% ROAS
    ideal_roas_multiplier = TARGET_ROAS / 100
    ideal_revenue = last_7_spend * ideal_roas_multiplier
    ideal_gross_profit = ideal_revenue * GROSS_MARGIN
    ideal_net_profit = ideal_gross_profit - last_7_spend

    profit_gap = ideal_net_profit - last_7_net_profit
    profit_gap_daily = profit_gap / 7

    print(f"   At 600% target ROAS, we'd make £{ideal_net_profit:,.0f} (£{ideal_net_profit/7:,.0f}/day)")
    print(f"   Current: £{last_7_net_profit:,.0f} (£{last_7_daily_profit:,.0f}/day)")
    print(f"   Gap: £{profit_gap:,.0f} (£{profit_gap_daily:,.0f}/day less than ideal)")
else:
    print(f"\n❌ ANSWER: YES, we are LOSING money.")
    print(f"   We are losing £{abs(last_7_daily_profit):,.0f}/day.")
    print(f"   ROAS is {last_7_avg_roas:.0f}% (below {breakeven_roas:.0f}% breakeven).")

# Conversion lag consideration
print("\n" + "="*80)
print("⏱️  CONVERSION LAG CONSIDERATION")
print("="*80)
print("\nFrom CONTEXT.md: 85% of conversions occur within 1 day of first click.")
print("This means 15% of conversions are attributed 2-7 days after click.")
print("\nImplication for Dec 1-13 performance:")
print("  • Some conversions are from clicks that occurred when stock WAS available")
print("  • These are 'legitimate' conversions (users ordered before stock message appeared)")
print("  • As we move further from stock depletion date, conversion lag effect diminishes")
print("  • By Dec 7-13, most conversions are from clicks AFTER 'Sold Out' message visible")

# Dec 7-13 likely has minimal conversion lag from pre-stock-depletion clicks
print("\nDec 7-13 conversions breakdown (estimated):")
recent_conversions = last_7_days['conversions'].sum()
lag_conversions_estimate = recent_conversions * 0.15  # 15% conversion lag
same_day_conversions = recent_conversions * 0.85

print(f"  • Total conversions: {recent_conversions:.0f}")
print(f"  • Same-day conversions (~85%): {same_day_conversions:.0f}")
print(f"  • Conversion lag (~15%): {lag_conversions_estimate:.0f}")
print(f"\n  If conversion lag is from pre-stock-depletion clicks:")
print(f"    → {lag_conversions_estimate:.0f} conversions are 'real' (ordered before sold out)")
print(f"    → {same_day_conversions:.0f} conversions are questionable (clicked after sold out message)")

# What's happening with those "questionable" conversions?
print("\n  Possible explanations for Dec 7-13 conversions:")
print("    1. Users ordering for January delivery (accepting delay)")
print("    2. Conversion lag from earlier clicks (pre-sold-out)")
print("    3. Other markets (UK/AU) still have stock?")
print("    4. Some US stock still available for certain products?")

# Recommendations
print("\n" + "="*80)
print("📋 RECOMMENDATIONS: What To Do Until January")
print("="*80)

print("\nOption 1: KEEP RUNNING (Craig's likely preference)")
print("  Pros:")
print(f"    ✅ Still profitable (£{last_7_daily_profit:,.0f}/day net profit)")
print(f"    ✅ ROAS {last_7_avg_roas:.0f}% is {last_7_avg_roas - breakeven_roas:.0f}pp above breakeven")
print("    ✅ Maintains campaign momentum for January restock")
print("    ✅ Keeps brand visible during competitive holiday period")
print("  Cons:")
print(f"    ❌ Making £{profit_gap_daily:,.0f}/day LESS than at target ROAS")
print("    ❌ Risk of wasting spend if users can't actually buy")
print("    ❌ Potential negative user experience (ads for unavailable products)")

print("\nOption 2: PAUSE US CAMPAIGNS")
print("  Pros:")
print("    ✅ Zero waste on unavailable products")
print("    ✅ Better user experience (no ads for sold-out items)")
print("    ✅ Save budget for January restock")
print("  Cons:")
print(f"    ❌ Lose £{last_7_daily_profit:,.0f}/day net profit")
print("    ❌ Campaign learning reset (may take 7-14 days to re-optimize)")
print("    ❌ Lose brand visibility during competitive period")

print("\nOption 3: OPTIMIZE FOR STOCK SITUATION (RECOMMENDED)")
print("  Actions:")
print("    1. Check if conversions are JANUARY DELIVERY orders")
print("       → If yes: Keep running, users are intentionally buying for Jan")
print("       → If no: Pause or reduce significantly")
print("")
print("    2. Separate US vs UK/AU performance")
print("       → Query campaign-level data to see if UK/AU still converting well")
print("       → Keep UK/AU running if stock available, pause US only")
print("")
print("    3. Reduce US budgets further (not pause)")
print(f"       → Current: £{last_7_days['spend_gbp'].mean():,.0f}/day")
print(f"       → Reduce to: £3,000-4,000/day (50% reduction)")
print("       → Maintains presence but limits waste")
print("")
print("    4. Switch to BRAND ONLY in US")
print("       → Pause Shopping/PMax (generic product searches)")
print("       → Keep Search Brand running (protect brand searches)")
print("       → Minimizes waste while maintaining brand defence")

print("\n" + "="*80)
print("✅ Analysis complete. Charts saved to clients/superspace/analysis/")
print("="*80)

# Save summary to file
with open('/Users/administrator/Documents/PetesBrain.nosync/clients/superspace/analysis/profitability-summary.txt', 'w') as f:
    f.write("SUPERSPACE US PROFITABILITY ANALYSIS (Nov 13 - Dec 13, 2025)\n")
    f.write("="*80 + "\n\n")
    f.write(f"Last 7 Days (Dec 7-13) Performance:\n")
    f.write(f"  • Total Spend: £{last_7_spend:,.0f}\n")
    f.write(f"  • Total Revenue: £{last_7_revenue:,.0f}\n")
    f.write(f"  • Net Profit: £{last_7_net_profit:,.0f}\n")
    f.write(f"  • Daily Net Profit: £{last_7_daily_profit:,.0f}/day\n")
    f.write(f"  • Average ROAS: {last_7_avg_roas:.0f}%\n\n")

    if last_7_net_profit > 0:
        f.write(f"STATUS: PROFITABLE (but below target)\n")
        f.write(f"Making £{last_7_daily_profit:,.0f}/day net profit\n")
        f.write(f"Gap vs ideal (600% ROAS): £{profit_gap_daily:,.0f}/day less profit\n")
    else:
        f.write(f"STATUS: LOSING MONEY\n")
        f.write(f"Losing £{abs(last_7_daily_profit):,.0f}/day\n")

print("\n💾 Summary saved to: profitability-summary.txt")
