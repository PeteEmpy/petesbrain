#!/usr/bin/env python3
"""
Analyse campaign performance Dec 15-21, 2025
Identify top performers for budget increases
"""

# Campaign performance data from Dec 15-21
campaigns = [
    # UK Account
    {"account": "UK", "id": "23194794411", "name": "SMY | UK | P Max | Diaries", "spend": 3328.26, "revenue": 12466.99, "current_budget": 50.00},
    {"account": "UK", "id": "22845468179", "name": "SMY | UK | P Max | H&S", "spend": 3113.47, "revenue": 12681.26, "current_budget": 75.00},
    {"account": "UK", "id": "23021472678", "name": "SMY | UK | P Max | H&S - Men's Briefcases", "spend": 1804.96, "revenue": 5010.35, "current_budget": 100.00},
    {"account": "UK", "id": "23233714033", "name": "SMY | UK | P Max | H&S Christmas Gifting", "spend": 2872.85, "revenue": 10270.07, "current_budget": 75.00},
    {"account": "UK", "id": "13811031042", "name": "SMY | UK | Search | Brand Exact", "spend": 6145.18, "revenue": 48074.92, "current_budget": 37.00},
    {"account": "UK", "id": "13813052579", "name": "SMY | UK | Search | Brand Plus", "spend": 679.51, "revenue": 3739.38, "current_budget": 50.00},
    {"account": "UK", "id": "13813053110", "name": "SMY | UK | Search | Brand Stationery", "spend": 438.12, "revenue": 3183.18, "current_budget": 30.00},
    {"account": "UK", "id": "23215754148", "name": "SMY | UK | Search | Competitor", "spend": 305.90, "revenue": 258.50, "current_budget": 20.00},
    {"account": "UK", "id": "23074901902", "name": "SMY | UK | Search | Generic", "spend": 139.46, "revenue": 686.93, "current_budget": 18.00},
    {"account": "UK", "id": "13810745002", "name": "SMY | UK | Search | Semi Brand - Diaries", "spend": 1057.66, "revenue": 10605.29, "current_budget": 150.00},

    # USA Account
    {"account": "USA", "id": "22796857828", "name": "SMY | US | P Max | Bags", "spend": 629.23, "revenue": 9423.02, "current_budget": 150.00},
    {"account": "USA", "id": "23210838865", "name": "SMY | US | P Max | Diaries", "spend": 907.83, "revenue": 10244.54, "current_budget": 75.00},
    {"account": "USA", "id": "18037696979", "name": "SMY | US | P Max | H&S", "spend": 1511.36, "revenue": 7924.79, "current_budget": 35.00},
    {"account": "USA", "id": "23232558954", "name": "SMY | US | P Max | H&S Christmas Gifting", "spend": 1127.45, "revenue": 7279.30, "current_budget": 40.00},
    {"account": "USA", "id": "22546298306", "name": "SMY | US | PMax | Zombies", "spend": 603.22, "revenue": 3914.79, "current_budget": 100.00},
    {"account": "USA", "id": "1683494533", "name": "SMY | US | Search | Brand Exact", "spend": 3505.92, "revenue": 33461.14, "current_budget": 30.00},
    {"account": "USA", "id": "1602584781", "name": "SMY | US | Search | Brand Plus", "spend": 678.66, "revenue": 7237.31, "current_budget": 30.00},
    {"account": "USA", "id": "1602585081", "name": "SMY | US | Search | Brand Leather", "spend": 411.77, "revenue": 3385.31, "current_budget": 20.00},
    {"account": "USA", "id": "1602584829", "name": "SMY | US | Search | Brand Stationery", "spend": 235.88, "revenue": 1045.73, "current_budget": 20.00},

    # EUR Account
    {"account": "EUR", "id": "23257901431", "name": "SMY | EUR | IT | P Max | Diaries", "spend": 277.54, "revenue": 1355.21, "current_budget": 30.00},
    {"account": "EUR", "id": "23253394509", "name": "SMY | EUR | P Max | Christmas Gifting", "spend": 511.68, "revenue": 464.10, "current_budget": 15.00},
    {"account": "EUR", "id": "23292938044", "name": "SMY | EUR | CH | Search | Brand", "spend": 224.80, "revenue": 1643.36, "current_budget": 10.00},
    {"account": "EUR", "id": "23257639561", "name": "SMY | EUR | DE | P Max | Christmas Gifting", "spend": 92.90, "revenue": 603.60, "current_budget": 9.69},
    {"account": "EUR", "id": "23257761115", "name": "SMY | EUR | DE | P Max | Diaries", "spend": 220.32, "revenue": 117.50, "current_budget": 25.00},
    {"account": "EUR", "id": "691020848", "name": "SMY | EUR | DE | Search | Brand", "spend": 444.35, "revenue": 3513.98, "current_budget": 50.00},
    {"account": "EUR", "id": "23237208923", "name": "SMY | EUR | DE | Search | Competitor", "spend": 83.05, "revenue": 0.00, "current_budget": 6.66},
    {"account": "EUR", "id": "21512797638", "name": "SMY | EUR | DE | Shopping", "spend": 200.99, "revenue": 1695.28, "current_budget": 20.00},
    {"account": "EUR", "id": "23248988334", "name": "SMY | EUR | FR | P Max | Christmas Gifting", "spend": 381.47, "revenue": 1546.25, "current_budget": 39.98},
    {"account": "EUR", "id": "691020884", "name": "SMY | EUR | FR | Search | Brand", "spend": 369.02, "revenue": 203.25, "current_budget": 20.00},
    {"account": "EUR", "id": "23253230592", "name": "SMY | EUR | IT | P Max | Christmas Gifting", "spend": 108.72, "revenue": 88.00, "current_budget": 12.11},
    {"account": "EUR", "id": "1599767262", "name": "SMY | EUR | IT | Search Brand", "spend": 439.47, "revenue": 4639.45, "current_budget": 100.00},
    {"account": "EUR", "id": "23253890345", "name": "SMY | EUR | P Max | Diaries", "spend": 44.54, "revenue": 831.50, "current_budget": 20.00},
    {"account": "EUR", "id": "22440993281", "name": "SMY | EUR | ROEuro | Search | Brand", "spend": 993.47, "revenue": 4968.95, "current_budget": 50.00},
    {"account": "EUR", "id": "1603775949", "name": "SMY | EUR | ROEuro | Search | Brand Diaries", "spend": 72.00, "revenue": 119.00, "current_budget": 12.11},
    {"account": "EUR", "id": "22441297139", "name": "SMY | EUR | RONot | Search | Brand", "spend": 178.73, "revenue": 1701.40, "current_budget": 20.00},

    # ROW Account
    {"account": "ROW", "id": "6551615752", "name": "SMY | ROW | AUS | Search | Brand", "spend": 268.41, "revenue": 1164.09, "current_budget": 5.00},
    {"account": "ROW", "id": "23258454848", "name": "SMY | ROW | P Max | Christmas Gifting", "spend": 614.80, "revenue": 975.46, "current_budget": 10.00},
    {"account": "ROW", "id": "23253385815", "name": "SMY | ROW | P Max | Diaries", "spend": 29.71, "revenue": 0.00, "current_budget": 10.00},
    {"account": "ROW", "id": "22503794801", "name": "SMY | ROW | Search | Brand", "spend": 828.27, "revenue": 6388.46, "current_budget": 60.00},
    {"account": "ROW", "id": "6552020619", "name": "SMY | ROW | Search | Brand Diaries", "spend": 82.57, "revenue": 337.55, "current_budget": 10.00},
    {"account": "ROW", "id": "23241919876", "name": "SMY | ROW | Search | Competitor", "spend": 24.80, "revenue": 230.72, "current_budget": 2.22},
]

# Calculate ROAS for each campaign
for campaign in campaigns:
    if campaign["spend"] > 0:
        campaign["roas"] = (campaign["revenue"] / campaign["spend"]) * 100
    else:
        campaign["roas"] = 0

# Sort by ROAS descending
campaigns_by_roas = sorted(campaigns, key=lambda x: x["roas"], reverse=True)

# Filter to campaigns with ROAS > 400% (top performers)
top_performers = [c for c in campaigns_by_roas if c["roas"] >= 400]

print("=" * 100)
print("TOP PERFORMING CAMPAIGNS - Dec 15-21, 2025 (ROAS ≥ 400%)")
print("=" * 100)
print()
print(f"{'Account':<6} {'Campaign Name':<50} {'Spend':<10} {'Revenue':<10} {'ROAS':<8} {'Budget':<8}")
print("-" * 100)

for c in top_performers:
    print(f"{c['account']:<6} {c['name'][:48]:<50} £{c['spend']:>8,.0f} £{c['revenue']:>8,.0f} {c['roas']:>6.0f}% £{c['current_budget']:>6,.0f}")

print()
print("=" * 100)
print(f"Total campaigns with ROAS ≥ 400%: {len(top_performers)}")
print("=" * 100)
print()

# Now show recommendations for budget increases
print()
print("=" * 100)
print("BUDGET INCREASE RECOMMENDATIONS (to close £357.23 gap)")
print("=" * 100)
print()

print("Strategy: Increase budgets for campaigns with ROAS > 800%")
print()

ultra_high_performers = [c for c in campaigns_by_roas if c["roas"] >= 800]

print(f"{'Campaign':<50} {'Current':<10} {'Recommended':<12} {'Increase':<10} {'ROAS':<8}")
print("-" * 100)

total_increase = 0
for c in ultra_high_performers[:15]:  # Top 15 ultra-high performers
    # Suggest increasing by 50-100% for campaigns under-budgeted
    if c["current_budget"] < 50:
        increase = c["current_budget"]  # Double the budget
    else:
        increase = c["current_budget"] * 0.5  # Increase by 50%

    new_budget = c["current_budget"] + increase
    total_increase += increase

    print(f"{c['name'][:48]:<50} £{c['current_budget']:>8,.0f} £{new_budget:>10,.0f} +£{increase:>8,.0f} {c['roas']:>6.0f}%")

print("-" * 100)
print(f"{'TOTAL BUDGET INCREASE':<50} {'':<10} {'':<12} +£{total_increase:>8,.2f}")
print()
print(f"Gap to close: £357.23")
print(f"Recommended increase: £{total_increase:.2f}")
if total_increase >= 357.23:
    print(f"✅ This increase covers the gap with £{total_increase - 357.23:.2f} extra")
else:
    print(f"⚠️  Still short by £{357.23 - total_increase:.2f}")
print()
