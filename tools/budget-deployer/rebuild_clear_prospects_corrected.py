#!/usr/bin/env python3
"""
Rebuild Clear Prospects deployment CSVs with ONLY active campaigns (end_date >= today).
Excludes past experiment campaigns (TJR, WBS Heat Pads, etc.).
"""

import csv
from pathlib import Path

CUSTOMER_ID = "6281395727"
MANAGER_ID = ""

# ONLY campaigns with end_date >= 2025-12-16 (from Google Ads API query)
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

# Seasonal factors from year-on-year analysis (Jan 2024 vs Dec 2024)
SEASONAL_FACTORS = {
    "BMPM": 0.917,  # 91.7% - B2B trade, minimal seasonality
    "HSG": 0.260,   # 26.0% - Gift business, massive Christmas peak
    "WBS": 0.442,   # 44.2% - Gift business, also highly seasonal
}

def create_phase2_csv():
    """
    Phase 2: Christmas Peak (Dec 16-19)
    - BMPM: PAUSE (stop losses over Christmas)
    - HSG/WBS: Maintain at peak levels
    """
    rows = []
    rows.append(["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"])

    # BMPM - PAUSE to stop losses
    rows.append([CUSTOMER_ID, MANAGER_ID, "21173762063", "CPL | BMPM | P Max Shopping", "15.00", "0.00", "PAUSE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "384585297", "CPL | BMPM | Search | Promotional Merchandise", "10.00", "0.00", "PAUSE"])

    print("Phase 2 (Christmas Peak - Dec 16-19):")
    print("  BMPM: 2 campaigns PAUSED")
    print("  HSG/WBS: Maintained at current levels")
    print("  Total changes: 2 campaigns")

    return rows

def create_phase3_csv():
    """
    Phase 3: Post-Christmas (January)
    DATA-DRIVEN seasonal reductions based on Jan 2024 vs Dec 2024.
    """
    rows = []
    rows.append(["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"])

    # Apply seasonal factors to ALL active campaigns
    for campaign_id, data in ACTIVE_CAMPAIGNS.items():
        brand = data["brand"]
        current_budget = data["budget_gbp"]
        seasonal_factor = SEASONAL_FACTORS.get(brand, 1.0)  # Default to 1.0 if brand not found
        new_budget = current_budget * seasonal_factor

        rows.append([
            CUSTOMER_ID,
            MANAGER_ID,
            campaign_id,
            data["name"],
            f"{current_budget:.2f}",
            f"{new_budget:.2f}",
            "BUDGET_CHANGE"
        ])

    # Calculate totals by brand
    bmpm_total = sum(ACTIVE_CAMPAIGNS[cid]["budget_gbp"] * SEASONAL_FACTORS["BMPM"]
                     for cid in ACTIVE_CAMPAIGNS if ACTIVE_CAMPAIGNS[cid]["brand"] == "BMPM")
    hsg_total = sum(ACTIVE_CAMPAIGNS[cid]["budget_gbp"] * SEASONAL_FACTORS["HSG"]
                    for cid in ACTIVE_CAMPAIGNS if ACTIVE_CAMPAIGNS[cid]["brand"] == "HSG")
    wbs_total = sum(ACTIVE_CAMPAIGNS[cid]["budget_gbp"] * SEASONAL_FACTORS["WBS"]
                    for cid in ACTIVE_CAMPAIGNS if ACTIVE_CAMPAIGNS[cid]["brand"] == "WBS")
    total = bmpm_total + hsg_total + wbs_total

    print("\nPhase 3 (Post-Christmas - January) - DATA-DRIVEN:")
    print(f"  BMPM: £{bmpm_total:.2f}/day (91.7% seasonal factor - RESTORED)")
    print(f"  HSG: £{hsg_total:.2f}/day (26.0% seasonal factor)")
    print(f"  WBS: £{wbs_total:.2f}/day (44.2% seasonal factor)")
    print(f"  Total: £{total:.2f}/day")
    print(f"  Total changes: {len(ACTIVE_CAMPAIGNS)} campaigns")

    return rows

def save_csv(rows, filename):
    """Save CSV file"""
    filepath = Path(f"/Users/administrator/Documents/PetesBrain.nosync/clients/clear-prospects/spreadsheets/{filename}")
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"  Saved: {filepath}")
    return filepath

if __name__ == "__main__":
    print("=" * 80)
    print("CLEAR PROSPECTS - CORRECTED DEPLOYMENT (Active Campaigns Only)")
    print("=" * 80)
    print(f"Total active campaigns: {len(ACTIVE_CAMPAIGNS)}")
    print(f"  BMPM: 2 campaigns")
    print(f"  HSG: 6 campaigns")
    print(f"  WBS: 5 campaigns")
    print(f"  TJR: 0 campaigns (experiment ended)")
    print()

    # Phase 2
    print("=" * 80)
    phase2_rows = create_phase2_csv()
    phase2_file = save_csv(phase2_rows, "phase2-christmas-peak-dec16.csv")

    # Phase 3
    print("\n" + "=" * 80)
    phase3_rows = create_phase3_csv()
    phase3_file = save_csv(phase3_rows, "phase3-post-christmas-dec20.csv")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("✓ Excluded 6 past experiment campaigns")
    print("✓ Phase 2: 2 campaigns (BMPM pause only)")
    print("✓ Phase 3: 13 campaigns (seasonal adjustments)")
    print(f"\nPhase 2 CSV: {phase2_file}")
    print(f"Phase 3 CSV: {phase3_file}")
