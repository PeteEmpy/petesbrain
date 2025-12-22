#!/usr/bin/env python3
"""
Create FIVE-phase deployment for Clear Prospects Christmas 2024.
Based on actual Christmas 2023 shutdown data.

Phase 1: Dec 15 (DEPLOYED) - Christmas peak
Phase 2: Dec 16-19 - BMPM pause, maintain HSG/WBS
Phase 3: Dec 20-25 - Shutdown period (keep warm → brand protection)
Phase 4: Dec 26-Jan 5 - Boxing Day recovery
Phase 5: Jan 6+ - Full seasonal budgets (Jan 2024 YoY)
"""

import csv
from pathlib import Path

CUSTOMER_ID = "6281395727"
MANAGER_ID = ""

# Active campaigns (end_date >= 2025-12-16)
ACTIVE_CAMPAIGNS = {
    # BMPM (2 campaigns)
    "21173762063": {"name": "CPL | BMPM | P Max Shopping", "budget_gbp": 15.00, "brand": "BMPM"},
    "384585297": {"name": "CPL | BMPM | Search | Promotional Merchandise", "budget_gbp": 10.00, "brand": "BMPM"},

    # HSG (6 campaigns)
    "211394337": {"name": "CPL | HSG | Search | Brand", "budget_gbp": 20.00, "brand": "HSG"},
    "17287142780": {"name": "CPL | HSG | P Max Shopping | Villains", "budget_gbp": 13.00, "brand": "HSG"},
    "17146649454": {"name": "CPL | HSG | P Max Shopping | Zombies", "budget_gbp": 28.00, "brand": "HSG"},
    "21730574366": {"name": "CPL | HSG | P Max | All | H&S", "budget_gbp": 510.00, "brand": "HSG"},
    "20502206066": {"name": "CPL | HSG | Search | Photo Face Mask", "budget_gbp": 77.00, "brand": "HSG"},
    "704093015": {"name": "CPL | HSG | Search | Products", "budget_gbp": 30.00, "brand": "HSG"},

    # WBS (5 campaigns)
    "17599480539": {"name": "CPL | WBS | P Max Shopping | H&S", "budget_gbp": 310.00, "brand": "WBS"},
    "17342356076": {"name": "CPL | WBS | P Max Shopping | Wheat Bags | Villains", "budget_gbp": 8.20, "brand": "WBS"},
    "17610292964": {"name": "CPL | WBS | P Max | Shopping | Zombies", "budget_gbp": 29.00, "brand": "WBS"},
    "78340377": {"name": "CPL | WBS | Search | Brand Inclusion", "budget_gbp": 56.00, "brand": "WBS"},
    "60035097": {"name": "CPL | WBS | Search | Wheat Bags", "budget_gbp": 140.00, "brand": "WBS"},
}

# Calculate current total by brand
current_totals = {"BMPM": 25.00, "HSG": 678.00, "WBS": 543.20}

# Seasonal factors from Jan 2024 vs Dec 2024 YoY analysis
SEASONAL_FACTORS = {
    "BMPM": 0.917,  # 91.7%
    "HSG": 0.260,   # 26.0%
    "WBS": 0.442,   # 44.2%
}

def save_csv(rows, filename):
    """Save CSV file"""
    filepath = Path(f"/Users/administrator/Documents/PetesBrain.nosync/clients/clear-prospects/spreadsheets/{filename}")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"  Saved: {filepath.name}")
    return filepath

def create_phase2():
    """Phase 2: Dec 16-19 - BMPM pause"""
    rows = [["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"]]
    rows.append([CUSTOMER_ID, MANAGER_ID, "21173762063", "CPL | BMPM | P Max Shopping", "15.00", "0.00", "PAUSE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "384585297", "CPL | BMPM | Search | Promotional Merchandise", "10.00", "0.00", "PAUSE"])
    return rows

def create_phase3():
    """
    Phase 3: Dec 20-25 - Shutdown period
    Based on 2023 data: Dec 20-23 was £47/day (92% reduction), Dec 24-25 was £85/day (losing money)
    Strategy: ~£50/day total (94% reduction from current £845/day)
    """
    rows = [["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"]]

    # Target: £50/day total across all campaigns
    # Allocate proportionally by current brand spend
    total_current = sum(current_totals.values())
    shutdown_budget_total = 50.00

    for campaign_id, data in ACTIVE_CAMPAIGNS.items():
        brand = data["brand"]
        current_budget = data["budget_gbp"]
        brand_proportion = current_totals[brand] / total_current
        new_budget = shutdown_budget_total * brand_proportion * (current_budget / current_totals[brand])

        rows.append([
            CUSTOMER_ID, MANAGER_ID, campaign_id, data["name"],
            f"{current_budget:.2f}", f"{new_budget:.2f}", "BUDGET_CHANGE"
        ])

    return rows

def create_phase4():
    """
    Phase 4: Dec 26 - Jan 5 - Boxing Day recovery
    Based on 2023 data: Dec 26-31 averaged £158/day (201% ROAS - profitable)
    Strategy: ~£150/day total (moderate reduction, campaigns warm for January)
    """
    rows = [["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"]]

    # Target: £150/day total
    total_current = sum(current_totals.values())
    recovery_budget_total = 150.00

    for campaign_id, data in ACTIVE_CAMPAIGNS.items():
        brand = data["brand"]
        current_budget = data["budget_gbp"]
        brand_proportion = current_totals[brand] / total_current
        new_budget = recovery_budget_total * brand_proportion * (current_budget / current_totals[brand])

        rows.append([
            CUSTOMER_ID, MANAGER_ID, campaign_id, data["name"],
            f"{current_budget:.2f}", f"{new_budget:.2f}", "BUDGET_CHANGE"
        ])

    return rows

def create_phase5():
    """
    Phase 5: Jan 6+ - Full seasonal budgets
    Based on Jan 2024 vs Dec 2024 YoY analysis
    """
    rows = [["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"]]

    for campaign_id, data in ACTIVE_CAMPAIGNS.items():
        brand = data["brand"]
        current_budget = data["budget_gbp"]
        seasonal_factor = SEASONAL_FACTORS[brand]
        new_budget = current_budget * seasonal_factor

        rows.append([
            CUSTOMER_ID, MANAGER_ID, campaign_id, data["name"],
            f"{current_budget:.2f}", f"{new_budget:.2f}", "BUDGET_CHANGE"
        ])

    return rows

if __name__ == "__main__":
    print("=" * 100)
    print("CLEAR PROSPECTS - FIVE-PHASE CHRISTMAS DEPLOYMENT (Data-Driven)")
    print("=" * 100)
    print()

    # Phase 2
    print("PHASE 2: Dec 16-19 (Christmas Peak)")
    print("  - BMPM: PAUSE (stop losses)")
    print("  - HSG/WBS: Maintain at current levels")
    phase2 = create_phase2()
    save_csv(phase2, "phase2-christmas-peak-dec16.csv")
    print()

    # Phase 3
    print("PHASE 3: Dec 20-25 (Christmas Shutdown - Keep Warm)")
    print("  - Based on 2023: Dec 20-23 was £47/day, Dec 24-25 lost money")
    print("  - Target: £50/day (94% reduction)")
    print("  - Strategy: Minimal spend to keep campaigns warm")
    phase3 = create_phase3()
    save_csv(phase3, "phase3-shutdown-keep-warm-dec20.csv")
    print()

    # Phase 4
    print("PHASE 4: Dec 26 - Jan 5 (Boxing Day Recovery)")
    print("  - Based on 2023: Dec 26-31 averaged £158/day (201% ROAS - profitable)")
    print("  - Target: £150/day (moderate reduction)")
    print("  - Strategy: Resume spending, keep warm for January")
    phase4 = create_phase4()
    save_csv(phase4, "phase4-boxing-day-recovery-dec26.csv")
    print()

    # Phase 5
    print("PHASE 5: Jan 6+ (Full Seasonal Budgets)")
    print("  - Based on Jan 2024 vs Dec 2024 YoY analysis")
    print("  - BMPM: £22.93/day (91.7% seasonal factor - RESTORED)")
    print("  - HSG: £176.28/day (26.0% seasonal factor)")
    print("  - WBS: £240.09/day (44.2% seasonal factor)")
    print("  - Total: £439.30/day")
    phase5 = create_phase5()
    save_csv(phase5, "phase5-january-seasonal-jan6.csv")
    print()

    print("=" * 100)
    print("DEPLOYMENT SUMMARY")
    print("=" * 100)
    print("Phase 1: Dec 15 ✓ DEPLOYED (Christmas peak £845/day)")
    print("Phase 2: Dec 16-19 ⏳ READY (BMPM pause, ~£820/day)")
    print("Phase 3: Dec 20-25 ⏳ READY (Keep warm £50/day)")
    print("Phase 4: Dec 26-Jan 5 ⏳ READY (Recovery £150/day)")
    print("Phase 5: Jan 6+ ⏳ READY (Seasonal £439/day)")
    print()
    print("All CSVs generated and ready for deployment!")
