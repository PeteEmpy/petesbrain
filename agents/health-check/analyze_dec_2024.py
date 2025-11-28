import json
from collections import defaultdict
from datetime import datetime

# Load the data
with open('dec_2024_data.json', 'r') as f:
    data = json.load(f)

results = data['results']

# Aggregate by date
daily_totals = defaultdict(lambda: {'revenue': 0, 'spend': 0, 'conversions': 0})

for row in results:
    date = row['segments']['date']
    revenue = float(row['metrics']['conversionsValue'])
    spend = int(row['metrics']['costMicros']) / 1_000_000  # Convert micros to pounds
    conversions = float(row['metrics']['conversions'])

    daily_totals[date]['revenue'] += revenue
    daily_totals[date]['spend'] += spend
    daily_totals[date]['conversions'] += conversions

# Sort by date and calculate metrics
print("\nDecember 2024 Daily Performance (UK Account Only)\n")
print("Date       | Revenue   | Spend    | ROAS  | Conversions | Day")
print("-" * 80)

dates = sorted(daily_totals.keys())
for date in dates:
    dt = datetime.strptime(date, '%Y-%m-%d')
    day_name = dt.strftime('%a')
    d = daily_totals[date]
    roas = (d['revenue'] / d['spend'] * 100) if d['spend'] > 0 else 0
    print(f"{date} | £{d['revenue']:>8,.0f} | £{d['spend']:>7,.0f} | {roas:>4.0f}% | {d['conversions']:>11.1f} | {day_name}")

# Calculate period averages
def calc_avg(start, end):
    period_dates = [d for d in dates if start <= d <= end]
    total_rev = sum(daily_totals[d]['revenue'] for d in period_dates)
    total_spend = sum(daily_totals[d]['spend'] for d in period_dates)
    total_conv = sum(daily_totals[d]['conversions'] for d in period_dates)
    days = len(period_dates)
    return {
        'avg_rev': total_rev / days if days > 0 else 0,
        'avg_spend': total_spend / days if days > 0 else 0,
        'avg_conv': total_conv / days if days > 0 else 0,
        'days': days
    }

pre_xmas = calc_avg('2024-12-01', '2024-12-20')  # Strong shopping period
post_xmas = calc_avg('2024-12-21', '2024-12-31')  # Post-delivery cutoff

print("\n" + "=" * 80)
print("\nPeriod Analysis:")
print(f"\nDec 1-20 (Pre-Christmas): {pre_xmas['days']} days")
print(f"  Avg Daily Revenue: £{pre_xmas['avg_rev']:,.0f}")
print(f"  Avg Daily Spend: £{pre_xmas['avg_spend']:,.0f}")
print(f"  Avg Daily Conversions: {pre_xmas['avg_conv']:.1f}")

print(f"\nDec 21-31 (Post-Cutoff): {post_xmas['days']} days")
print(f"  Avg Daily Revenue: £{post_xmas['avg_rev']:,.0f}")
print(f"  Avg Daily Spend: £{post_xmas['avg_spend']:,.0f}")
print(f"  Avg Daily Conversions: {post_xmas['avg_conv']:.1f}")

# Calculate drop-off percentage
rev_drop = ((post_xmas['avg_rev'] - pre_xmas['avg_rev']) / pre_xmas['avg_rev'] * 100) if pre_xmas['avg_rev'] > 0 else 0
conv_drop = ((post_xmas['avg_conv'] - pre_xmas['avg_conv']) / pre_xmas['avg_conv'] * 100) if pre_xmas['avg_conv'] > 0 else 0

print(f"\nDrop-off Analysis:")
print(f"  Revenue: {rev_drop:+.1f}% (post-cutoff vs pre-Christmas)")
print(f"  Conversions: {conv_drop:+.1f}% (post-cutoff vs pre-Christmas)")

# Calculate weighting factor for budget allocation
# If post-Christmas is X% of pre-Christmas performance, we should weight budget accordingly
weight_factor = post_xmas['avg_rev'] / pre_xmas['avg_rev'] if pre_xmas['avg_rev'] > 0 else 0

print(f"\nWeighting Factor for Budget Allocation:")
print(f"  Post-Christmas period performs at {weight_factor:.1%} of pre-Christmas levels")
print(f"  Suggested: Weight Dec 1-20 as 1.0x, Dec 21-31 as {weight_factor:.2f}x")

# Calculate "effective days" for December
effective_days_pre = 20 * 1.0  # Dec 1-20 at full weight
effective_days_post = 11 * weight_factor  # Dec 21-31 at reduced weight
total_effective = effective_days_pre + effective_days_post

print(f"\nEffective Days Calculation for December 2025:")
print(f"  Dec 1-20: 20 days × 1.00 = {effective_days_pre:.1f} effective days")
print(f"  Dec 21-31: 11 days × {weight_factor:.2f} = {effective_days_post:.1f} effective days")
print(f"  Total: {total_effective:.1f} effective days (not 21, not 31)")

# Now calculate budget allocation based on this
daily_budget = 5838  # £5,838/day from dashboard
total_budget = daily_budget * total_effective

print(f"\nBudget Calculation for December 2025:")
print(f"  Daily Budget (all regions): £{daily_budget:,.0f}")
print(f"  Effective Days: {total_effective:.1f}")
print(f"  Total December Budget: £{total_budget:,.0f}")
print(f"\nThis should replace the current '£183,929 (21 days effective)' in cell B35")
