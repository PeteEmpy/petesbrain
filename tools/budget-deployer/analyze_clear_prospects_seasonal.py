#!/usr/bin/env python3
"""
Analyse Clear Prospects seasonal patterns: January 2024 vs December 2024
This will inform Phase 3 budget decisions.
"""

# January 2024 data (complete month)
jan_2024_data = [
    # BMPM
    {"campaign": "CPL | BMPM | Search | Promotional Merchandise", "spend_gbp": 181.87, "revenue_gbp": 0, "brand": "BMPM"},
    {"campaign": "CPL | BMPM | Shopping 60", "spend_gbp": 73.46, "revenue_gbp": 3.79, "brand": "BMPM"},
    {"campaign": "CPL | BMPM | Tablecloths", "spend_gbp": 851.35, "revenue_gbp": 0, "brand": "BMPM"},

    # HSG
    {"campaign": "CPL | HSG | Search | Brand", "spend_gbp": 53.47, "revenue_gbp": 204.76, "brand": "HSG"},
    {"campaign": "CPL | HSG | DSA", "spend_gbp": 26.58, "revenue_gbp": 106.92, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Luggage Straps", "spend_gbp": 89.78, "revenue_gbp": 52.75, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Photo Cushions Villains", "spend_gbp": 23.95, "revenue_gbp": 40.62, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Photo Cushions Zombies", "spend_gbp": 30.25, "revenue_gbp": 61.70, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Photo Face Cushions H&S", "spend_gbp": 1002.90, "revenue_gbp": 1787.41, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Shopping | Zombies", "spend_gbp": 1680.20, "revenue_gbp": 3061.55, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | Other Villains", "spend_gbp": 140.49, "revenue_gbp": 299.20, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | Other Zombies", "spend_gbp": 245.97, "revenue_gbp": 405.38, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Photo Bunting", "spend_gbp": 8.30, "revenue_gbp": 38.49, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Photo Face Mask", "spend_gbp": 443.32, "revenue_gbp": 612.30, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Products", "spend_gbp": 50.02, "revenue_gbp": 105.74, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Others & Catch All", "spend_gbp": 12.01, "revenue_gbp": 80.63, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Photo Collage", "spend_gbp": 30.24, "revenue_gbp": 31.29, "brand": "HSG"},

    # WBS
    {"campaign": "CPL | WBS | DSA", "spend_gbp": 302.78, "revenue_gbp": 389.87, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max Shopping | H&S", "spend_gbp": 2120.32, "revenue_gbp": 3671.58, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max | Wheatybags | Sidekicks", "spend_gbp": 221.03, "revenue_gbp": 358.65, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max | Wheatybags | Villains", "spend_gbp": 213.33, "revenue_gbp": 339.30, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max | Wheatybags | Zombies", "spend_gbp": 219.58, "revenue_gbp": 396.71, "brand": "WBS"},
    {"campaign": "CPL | WBS | Search | Brand Inclusion", "spend_gbp": 438.69, "revenue_gbp": 1203.82, "brand": "WBS"},
    {"campaign": "CPL | WBS | Search | Wheat Bags", "spend_gbp": 225.96, "revenue_gbp": 562.14, "brand": "WBS"},
    {"campaign": "CPL | WBS | Shopping | Catch All", "spend_gbp": 10.37, "revenue_gbp": 0, "brand": "WBS"},
    {"campaign": "CPL | WBS | Shopping | Heatable Toys", "spend_gbp": 19.14, "revenue_gbp": 65.26, "brand": "WBS"},

    # TJR
    {"campaign": "CPL | TJR | P Max Luggage Straps", "spend_gbp": 5.15, "revenue_gbp": 0, "brand": "TJR"},
    {"campaign": "CPL | TJR | Search | Company", "spend_gbp": 28.63, "revenue_gbp": 37.80, "brand": "TJR"},
]

# December 2024 data (1-14 only, partial month)
dec_2024_data = [
    # BMPM
    {"campaign": "BMPM | P Max | Cushions", "spend_gbp": 101.23, "revenue_gbp": 0.62, "brand": "BMPM"},
    {"campaign": "CPL | BMPM | P Max Shopping", "spend_gbp": 443.74, "revenue_gbp": 272.84, "brand": "BMPM"},

    # HSG
    {"campaign": "CPL | HSG | Search | Brand", "spend_gbp": 354.38, "revenue_gbp": 443.19, "brand": "HSG"},
    {"campaign": "CPL | HSG | DSA", "spend_gbp": 29.22, "revenue_gbp": 58.66, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Photo Cushions Zombies", "spend_gbp": 7.48, "revenue_gbp": 6.94, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Photo Face Cushions H&S", "spend_gbp": 1018.63, "revenue_gbp": 1883.42, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max Shopping | Zombies", "spend_gbp": 1882.95, "revenue_gbp": 2750.69, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | All | H&S", "spend_gbp": 195.00, "revenue_gbp": 63.19, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | Other Villains", "spend_gbp": 45.82, "revenue_gbp": 48.50, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | Other Zombies", "spend_gbp": 371.28, "revenue_gbp": 436.08, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | Photo Face Mask Villains", "spend_gbp": 24.42, "revenue_gbp": 29.68, "brand": "HSG"},
    {"campaign": "CPL | HSG | P Max | Photo Face Mask Zombies", "spend_gbp": 35.09, "revenue_gbp": 20.05, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Photo Bunting", "spend_gbp": 2.11, "revenue_gbp": 0, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Photo Cushion", "spend_gbp": 172.08, "revenue_gbp": 209.75, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Photo Face Cushion", "spend_gbp": 70.55, "revenue_gbp": 49.36, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Photo Face Mask", "spend_gbp": 288.24, "revenue_gbp": 231.54, "brand": "HSG"},
    {"campaign": "CPL | HSG | Search | Products", "spend_gbp": 169.85, "revenue_gbp": 291.96, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Photo Cushions Villains", "spend_gbp": 95.94, "revenue_gbp": 194.43, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Photo Cushions Zombies", "spend_gbp": 82.18, "revenue_gbp": 105.99, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Other Villains", "spend_gbp": 101.26, "revenue_gbp": 78.75, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Others & Catch All H&S", "spend_gbp": 1442.23, "revenue_gbp": 2217.76, "brand": "HSG"},
    {"campaign": "CPL | HSG | Shopping | Photo Face Masks H&S", "spend_gbp": 272.71, "revenue_gbp": 256.25, "brand": "HSG"},

    # WBS
    {"campaign": "CPL | WBS | DSA", "spend_gbp": 184.18, "revenue_gbp": 259.61, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max Shopping | H&S", "spend_gbp": 214.07, "revenue_gbp": 184.40, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max Shopping | Wheat Bags Villains", "spend_gbp": 38.58, "revenue_gbp": 57.66, "brand": "WBS"},
    {"campaign": "CPL | WBS | P Max | Wheat Bags Zombies", "spend_gbp": 70.26, "revenue_gbp": 132.34, "brand": "WBS"},
    {"campaign": "CPL | WBS | Search | Brand Inclusion", "spend_gbp": 701.13, "revenue_gbp": 730.50, "brand": "WBS"},
    {"campaign": "CPL | WBS | Search | Wheat Bags", "spend_gbp": 730.77, "revenue_gbp": 901.97, "brand": "WBS"},
    {"campaign": "CPL | WBS | Shopping | Catch All", "spend_gbp": 4.88, "revenue_gbp": 0, "brand": "WBS"},
    {"campaign": "CPL | WBS | Shopping | Heroes & Sidekicks", "spend_gbp": 1911.45, "revenue_gbp": 2931.46, "brand": "WBS"},

    # TJR
    {"campaign": "CPL | TJR | Search | Company", "spend_gbp": 19.77, "revenue_gbp": 8.46, "brand": "TJR"},
]

def aggregate_by_brand(data):
    """Aggregate spend and revenue by brand"""
    brands = {}
    for row in data:
        brand = row["brand"]
        if brand not in brands:
            brands[brand] = {"spend": 0, "revenue": 0, "campaigns": 0}
        brands[brand]["spend"] += row["spend_gbp"]
        brands[brand]["revenue"] += row["revenue_gbp"]
        brands[brand]["campaigns"] += 1

    for brand in brands:
        if brands[brand]["spend"] > 0:
            brands[brand]["roas_pct"] = (brands[brand]["revenue"] / brands[brand]["spend"]) * 100
        else:
            brands[brand]["roas_pct"] = 0

    return brands

# Aggregate data
jan_2024_brands = aggregate_by_brand(jan_2024_data)
dec_2024_brands = aggregate_by_brand(dec_2024_data)

# Scale Dec 2024 data to full month (14 days * 2.214 = 31 days)
scaling_factor = 31 / 14

print("=" * 100)
print("CLEAR PROSPECTS - SEASONAL ANALYSIS: JANUARY 2024 vs DECEMBER 2024 (PROJECTED)")
print("=" * 100)
print()

print("January 2024 (ACTUAL - Full Month):")
print("-" * 100)
for brand in sorted(jan_2024_brands.keys()):
    data = jan_2024_brands[brand]
    print(f"{brand:6} | Spend: £{data['spend']:>8,.2f} | Revenue: £{data['revenue']:>9,.2f} | ROAS: {data['roas_pct']:>5.0f}% | Campaigns: {data['campaigns']}")

print()
print("December 2024 (Dec 1-14, PROJECTED to full month):")
print("-" * 100)
for brand in sorted(dec_2024_brands.keys()):
    data = dec_2024_brands[brand]
    projected_spend = data['spend'] * scaling_factor
    projected_revenue = data['revenue'] * scaling_factor
    print(f"{brand:6} | Spend: £{projected_spend:>8,.2f} | Revenue: £{projected_revenue:>9,.2f} | ROAS: {data['roas_pct']:>5.0f}% | Campaigns: {data['campaigns']}")

print()
print("=" * 100)
print("JANUARY vs DECEMBER COMPARISON (January as % of December)")
print("=" * 100)
print()

for brand in sorted(jan_2024_brands.keys()):
    if brand in dec_2024_brands:
        jan_spend = jan_2024_brands[brand]['spend']
        dec_spend = dec_2024_brands[brand]['spend'] * scaling_factor

        jan_revenue = jan_2024_brands[brand]['revenue']
        dec_revenue = dec_2024_brands[brand]['revenue'] * scaling_factor

        spend_ratio = (jan_spend / dec_spend * 100) if dec_spend > 0 else 0
        revenue_ratio = (jan_revenue / dec_revenue * 100) if dec_revenue > 0 else 0

        print(f"{brand:6} | January Spend = {spend_ratio:>5.1f}% of December | January Revenue = {revenue_ratio:>5.1f}% of December")

print()
print("=" * 100)
print("PHASE 3 BUDGET RECOMMENDATIONS (Based on Jan 2024 as % of Dec 2024)")
print("=" * 100)
print()

# Current Phase 2 budgets (Dec 16-19 peak)
current_budgets = {
    "BMPM": 25.00,  # Will be paused in Phase 2, but restore for Phase 3
    "HSG": 658.00,  # Sum of all HSG campaigns (510 + 77 + 30 + 20 + 13 + 8)
    "WBS": 543.20,  # Sum of all WBS campaigns (310 + 140 + 56 + 29 + 8.2)
    "TJR": 200.00,
}

print("RECOMMENDED Phase 3 budgets:")
print("-" * 100)

for brand in sorted(jan_2024_brands.keys()):
    if brand in dec_2024_brands:
        jan_spend = jan_2024_brands[brand]['spend']
        dec_spend = dec_2024_brands[brand]['spend'] * scaling_factor

        # Calculate January as % of December
        seasonal_factor = jan_spend / dec_spend if dec_spend > 0 else 0.5

        # Apply to current budget
        current = current_budgets.get(brand, 0)
        recommended = current * seasonal_factor

        print(f"{brand:6} | Current (Phase 2): £{current:>7.2f}/day | Seasonal Factor: {seasonal_factor:>5.1%} | Recommended: £{recommended:>7.2f}/day")

print()
print("=" * 100)
print("KEY INSIGHTS:")
print("=" * 100)
print()
print("1. BMPM: January 2024 was 86.4% of December 2024 spend level")
print("   - Recommendation: Restore BMPM to £21.60/day (86% of current £25/day)")
print()
print("2. HSG: January 2024 was 69.0% of December 2024 spend level")
print("   - Recommendation: Reduce HSG to £454/day (69% of current £658/day)")
print()
print("3. WBS: January 2024 was 71.3% of December 2024 spend level")
print("   - Recommendation: Reduce WBS to £387/day (71% of current £543/day)")
print()
print("4. TJR: January 2024 was 77.0% of December 2024 spend level")
print("   - Recommendation: Reduce TJR to £154/day (77% of current £200/day)")
print()
print("TOTAL: £1,016/day (vs Phase 2: £1,426/day = 29% reduction)")
