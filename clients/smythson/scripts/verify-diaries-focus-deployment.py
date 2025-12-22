#!/usr/bin/env python3
"""
Verify the Diaries-focused budget deployment
Calculate new total daily budget after increases
"""

print("=" * 80)
print("DIARIES-FOCUSED BUDGET DEPLOYMENT VERIFICATION")
print("=" * 80)
print()

# Current spending budgets (from actual spend Dec 15-21)
current_total = 1642.77

# Proposed increases from CSV
increases = {
    "UK": [
        {"name": "Semi Brand - Diaries", "from": 150, "to": 250, "increase": 100},
        {"name": "Brand Exact", "from": 37, "to": 67, "increase": 30},
    ],
    "USA": [
        {"name": "P Max | Diaries", "from": 75, "to": 150, "increase": 75},
        {"name": "Brand Exact", "from": 30, "to": 60, "increase": 30},
        {"name": "Brand Plus", "from": 30, "to": 60, "increase": 30},
    ],
    "EUR": [
        {"name": "P Max | Diaries", "from": 20, "to": 50, "increase": 30},
        {"name": "IT | P Max | Diaries", "from": 30, "to": 50, "increase": 20},
        {"name": "IT | Search Brand", "from": 100, "to": 150, "increase": 50},
        {"name": "RONot | Search | Brand", "from": 20, "to": 30, "increase": 10},
    ],
    "ROW": [
        {"name": "Brand Diaries", "from": 10, "to": 20, "increase": 10},
        {"name": "Competitor", "from": 2.22, "to": 5, "increase": 2.78},
    ],
}

print("INCREASES BY ACCOUNT:")
print("-" * 80)
print()

total_increase = 0

for account, campaigns in increases.items():
    account_increase = sum(c["increase"] for c in campaigns)
    total_increase += account_increase

    print(f"{account} Account: +£{account_increase:.2f}")
    for c in campaigns:
        print(f"  {c['name']:<40} £{c['from']:>6.2f} → £{c['to']:>6.2f} (+£{c['increase']:.2f})")
    print()

print("=" * 80)
print(f"Current daily budget (Dec 15-21 actual):    £{current_total:,.2f}")
print(f"Total budget increase:                      +£{total_increase:,.2f}")
print(f"New daily budget:                            £{current_total + total_increase:,.2f}")
print("=" * 80)
print()
print(f"Target:                                      £2,000.00")
print(f"Difference from target:                      £{(current_total + total_increase) - 2000:+,.2f}")
print()

if (current_total + total_increase) > 2000:
    overage = (current_total + total_increase) - 2000
    print(f"✅ OVER target by £{overage:.2f}")
elif (current_total + total_increase) < 2000:
    shortfall = 2000 - (current_total + total_increase)
    print(f"⚠️  SHORT of target by £{shortfall:.2f}")
else:
    print(f"✅ EXACTLY on target")

print()
print("=" * 80)
print("DIARIES CAMPAIGNS PRIORITISED:")
print("=" * 80)
diaries_campaigns = [
    "UK: Semi Brand - Diaries (+£100)",
    "USA: P Max | Diaries (+£75)",
    "EUR: P Max | Diaries (+£30)",
    "EUR: IT | P Max | Diaries (+£20)",
    "ROW: Brand Diaries (+£10)",
]
for d in diaries_campaigns:
    print(f"  ✓ {d}")

print()
print("Total Diaries increase: £235.00")
print("Other strong performers: £152.78")
print()
