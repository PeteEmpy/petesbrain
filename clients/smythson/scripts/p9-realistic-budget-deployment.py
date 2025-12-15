#!/usr/bin/env python3
"""
Smythson P9 Realistic Budget Deployment
Max 20% increases, respecting last order date windows
"""

# Current budgets (as of Dec 14)
campaigns = {
    'EUR': {
        'Brand Search': 78.37,
        'Brand Shopping': 169.68,
        'Generic Search': 157.11,
        'Generic Shopping': 177.85,
        'Performance Max': 304.60,
        'Performance Max Brand': 60.64,
        'active_days': 3  # Dec 15-17 (last order Dec 17)
    },
    'USA': {
        'Brand Search': 100.00,
        'Generic Search': 100.00,
        'Performance Max': 300.00,
        'Generic Shopping': 4.00,
        'active_days': 2  # Dec 15-16 (last order Dec 16)
    },
    'UK': {
        'Brand Search': 323.48,
        'Generic Search': 261.97,
        'Performance Max': 455.81,
        'Performance Max Brand': 60.64,
        'active_days': 7  # Dec 15-21 (DHL last order Dec 21)
    },
    'ROW': {
        'active_days': 2  # Dec 15-16 then pause
    }
}

print("\n" + "=" * 80)
print("SMYTHSON P9 REALISTIC BUDGET DEPLOYMENT")
print("Max 20% increases | Respecting last order windows")
print("=" * 80)

total_current_daily = 0
total_new_daily = 0
total_spend_projection = 0

for region, data in campaigns.items():
    if region == 'ROW':
        print(f"\n{region} Account - PAUSE (last order Dec 16, minimal opportunity)")
        continue

    print(f"\n{region} Account - {data['active_days']} active days (Dec 15 - last order)")
    print("-" * 80)

    region_current = 0
    region_new = 0

    for campaign, current_budget in data.items():
        if campaign == 'active_days':
            continue

        # Apply 20% increase
        increase_pct = 20
        new_budget = current_budget * 1.20
        increase = new_budget - current_budget

        region_current += current_budget
        region_new += new_budget

        print(f"  {campaign:25} £{current_budget:>7.2f} → £{new_budget:>7.2f} (+{increase_pct}% = +£{increase:.2f})")

    region_spend = region_new * data['active_days']
    total_current_daily += region_current
    total_new_daily += region_new
    total_spend_projection += region_spend

    print(f"\n  Region daily total:        £{region_current:>7.2f} → £{region_new:>7.2f}")
    print(f"  {data['active_days']}-day spend projection:   £{region_spend:>7,.2f}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Current total daily budget:  £{total_current_daily:>7,.2f}")
print(f"New total daily budget:      £{total_new_daily:>7,.2f}")
print(f"Daily increase:              +£{total_new_daily - total_current_daily:>7,.2f} (+{((total_new_daily - total_current_daily)/total_current_daily)*100:.1f}%)")
print(f"\nActive window spend:         £{total_spend_projection:>7,.2f}")
print(f"Remaining P9 budget:         £80,474")
print(f"Budget utilization:          {(total_spend_projection/80474)*100:.1f}%")
print("=" * 80)

# Calculate what happens after last order dates
print("\n" + "=" * 80)
print("POST LAST-ORDER PERIOD (Dec 18-28)")
print("=" * 80)
print("Only UK Click & Collect available (minimal volume expected)")
print("Projected daily: £500-1,000/day")
print("Days remaining: 11 days (Dec 18-28)")
print("Additional spend: ~£7,500")
print(f"\nTotal P9 deployment projection: £{total_spend_projection + 7500:,.0f}")
print(f"Remaining unspent: £{80474 - total_spend_projection - 7500:,.0f}")
print("=" * 80)
