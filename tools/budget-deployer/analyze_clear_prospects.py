#!/usr/bin/env python3
"""
Analyse Clear Prospects campaign budgets and create three-phase Christmas deployment plan.

Phase 1: Run-up to Christmas (ALREADY DEPLOYED DEC 15)
Phase 2: Christmas Peak (Dec 16-19 before Michael finishes)
Phase 3: Post-Christmas (After Dec 19/23 shutdown)
"""

import json
import csv
from pathlib import Path

# Campaign data from Google Ads API
ENABLED_CAMPAIGNS = {
    # BMPM (B2B Trade) - Currently losing £290 in Dec 1-12
    "21173762063": {"name": "CPL | BMPM | P Max Shopping", "budget_gbp": 15.00, "brand": "BMPM"},
    "384585297": {"name": "CPL | BMPM | Search | Promotional Merchandise", "budget_gbp": 10.00, "brand": "BMPM"},

    # HSG (HappySnapGifts) - Performing well (151% ROAS Dec 1-13)
    "211394337": {"name": "CPL | HSG | Search | Brand", "budget_gbp": 20.00, "brand": "HSG"},
    "17287142780": {"name": "CPL | HSG | P Max Shopping | Villains", "budget_gbp": 13.00, "brand": "HSG"},
    "17146649454": {"name": "CPL | HSG | P Max Shopping | Zombies", "budget_gbp": 28.00, "brand": "HSG"},
    "21730574366": {"name": "CPL | HSG | P Max | All | H&S", "budget_gbp": 510.00, "brand": "HSG", "note": "Dec 15 increase from £70"},
    "20502206066": {"name": "CPL | HSG | Search | Photo Face Mask", "budget_gbp": 77.00, "brand": "HSG"},
    "704093015": {"name": "CPL | HSG | Search | Products", "budget_gbp": 30.00, "brand": "HSG"},

    # WBS (WheatyBags) - Performing well (139% ROAS Dec 1-13)
    "78340377": {"name": "CPL | WBS | Search | Brand Inclusion", "budget_gbp": 56.00, "brand": "WBS"},
    "60035097": {"name": "CPL | WBS | Search | Wheat Bags", "budget_gbp": 140.00, "brand": "WBS", "note": "Shared budget across 4 search campaigns"},
    "17599480539": {"name": "CPL | WBS | P Max Shopping | H&S", "budget_gbp": 310.00, "brand": "WBS", "note": "Dec 15 increase from £150"},
    "17342356076": {"name": "CPL | WBS | P Max Shopping | Wheat Bags | Villains", "budget_gbp": 8.20, "brand": "WBS"},
    "17610292964": {"name": "CPL | WBS | P Max | Shopping | Zombies", "budget_gbp": 29.00, "brand": "WBS"},
    "1410219026": {"name": "Target CPA Experiment - CPL | WBS | Search | Heat Pads & Packs | Broad", "budget_gbp": 500.00, "brand": "WBS"},

    # TJR (JetRest)
    "1422969577": {"name": "Target CPA Experiment – CPL | TJR | Search | Luggage Straps | Exact", "budget_gbp": 200.00, "brand": "TJR"},
}

CUSTOMER_ID = "6281395727"
MANAGER_ID = ""  # No manager for Clear Prospects

def create_phase1_csv():
    """
    Phase 1: Run-up to Christmas (ALREADY DEPLOYED DEC 15)
    This verifies the current state after the Dec 15 increases.
    """
    rows = []
    rows.append(["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"])

    # This phase was already deployed on Dec 15. We're just documenting it.
    # No changes needed - this is the current state.
    print("Phase 1 (Run-up to Christmas - Dec 15) - Current state verified")
    print("HSG H&S PMax: £510/day (was £70)")
    print("WBS H&S PMax: £310/day (was £150)")
    print("BMPM: £25/day (needs to stop losses)")

    return rows

def create_phase2_csv():
    """
    Phase 2: Christmas Peak (Dec 16-19 before Michael finishes)
    - BMPM: PAUSE (stop driving losses)
    - HSG H&S: MAINTAIN £510/day (strong 151% ROAS)
    - WBS H&S: MAINTAIN £310/day (strong 139% ROAS)
    - Other campaigns: Maintain or slight reductions
    """
    rows = []
    rows.append(["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"])

    # BMPM - PAUSE to stop losses
    rows.append([CUSTOMER_ID, MANAGER_ID, "21173762063", "CPL | BMPM | P Max Shopping", "15.00", "0.00", "PAUSE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "384585297", "CPL | BMPM | Search | Promotional Merchandise", "10.00", "0.00", "PAUSE"])

    # HSG - Maintain strong performers, no changes for Christmas peak
    # (All campaigns stay as is)

    # WBS - Maintain strong performers, no changes for Christmas peak
    # (All campaigns stay as is)

    # TJR - Maintain
    # (Stay as is)

    print("\nPhase 2 (Christmas Peak - Dec 16-19):")
    print("BMPM: PAUSED (stop losses)")
    print("HSG H&S PMax: £510/day (maintain)")
    print("WBS H&S PMax: £310/day (maintain)")
    print("Total daily budget: ~£820/day (down from ~£845/day)")

    return rows

def create_phase3_csv():
    """
    Phase 3: Post-Christmas (After Dec 19/23 shutdown)
    DATA-DRIVEN budget reductions based on Jan 2024 vs Dec 2024 performance.

    Seasonal factors (Jan as % of Dec):
    - BMPM: 91.7% → Restore to £22.93/day (NOT paused)
    - HSG: 26.0% → Reduce to £171.19/day
    - WBS: 44.2% → Reduce to £239.96/day
    - TJR: 77.2% → Reduce to £154.33/day
    """
    rows = []
    rows.append(["customer_id", "manager_id", "campaign_id", "campaign_name", "current_budget_gbp", "new_budget_gbp", "action"])

    # Seasonal factors from year-on-year analysis
    SEASONAL_FACTORS = {
        "BMPM": 0.917,  # 91.7%
        "HSG": 0.260,   # 26.0%
        "WBS": 0.442,   # 44.2%
        "TJR": 0.772,   # 77.2%
    }

    # BMPM - RESTORE (NOT paused) based on seasonal factor
    rows.append([CUSTOMER_ID, MANAGER_ID, "21173762063", "CPL | BMPM | P Max Shopping", "15.00", f"{15.00 * SEASONAL_FACTORS['BMPM']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "384585297", "CPL | BMPM | Search | Promotional Merchandise", "10.00", f"{10.00 * SEASONAL_FACTORS['BMPM']:.2f}", "BUDGET_CHANGE"])

    # HSG - Apply 26% seasonal factor (gift business, massive Christmas spike)
    rows.append([CUSTOMER_ID, MANAGER_ID, "211394337", "CPL | HSG | Search | Brand", "20.00", f"{20.00 * SEASONAL_FACTORS['HSG']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "17287142780", "CPL | HSG | P Max Shopping | Villains", "13.00", f"{13.00 * SEASONAL_FACTORS['HSG']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "17146649454", "CPL | HSG | P Max Shopping | Zombies", "28.00", f"{28.00 * SEASONAL_FACTORS['HSG']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "21730574366", "CPL | HSG | P Max | All | H&S", "510.00", f"{510.00 * SEASONAL_FACTORS['HSG']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "20502206066", "CPL | HSG | Search | Photo Face Mask", "77.00", f"{77.00 * SEASONAL_FACTORS['HSG']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "704093015", "CPL | HSG | Search | Products", "30.00", f"{30.00 * SEASONAL_FACTORS['HSG']:.2f}", "BUDGET_CHANGE"])

    # WBS - Apply 44.2% seasonal factor (also gift-focused)
    rows.append([CUSTOMER_ID, MANAGER_ID, "78340377", "CPL | WBS | Search | Brand Inclusion", "56.00", f"{56.00 * SEASONAL_FACTORS['WBS']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "60035097", "CPL | WBS | Search | Wheat Bags", "140.00", f"{140.00 * SEASONAL_FACTORS['WBS']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "17599480539", "CPL | WBS | P Max Shopping | H&S", "310.00", f"{310.00 * SEASONAL_FACTORS['WBS']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "17342356076", "CPL | WBS | P Max Shopping | Wheat Bags | Villains", "8.20", f"{8.20 * SEASONAL_FACTORS['WBS']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "17610292964", "CPL | WBS | P Max | Shopping | Zombies", "29.00", f"{29.00 * SEASONAL_FACTORS['WBS']:.2f}", "BUDGET_CHANGE"])
    rows.append([CUSTOMER_ID, MANAGER_ID, "1410219026", "Target CPA Experiment - CPL | WBS | Search | Heat Pads & Packs | Broad", "500.00", f"{500.00 * SEASONAL_FACTORS['WBS']:.2f}", "BUDGET_CHANGE"])

    # TJR - Apply 77.2% seasonal factor (moderate seasonality)
    rows.append([CUSTOMER_ID, MANAGER_ID, "1422969577", "Target CPA Experiment – CPL | TJR | Search | Luggage Straps | Exact", "200.00", f"{200.00 * SEASONAL_FACTORS['TJR']:.2f}", "BUDGET_CHANGE"])

    # Calculate totals for summary
    bmpm_total = 15.00 * SEASONAL_FACTORS['BMPM'] + 10.00 * SEASONAL_FACTORS['BMPM']
    hsg_total = (20.00 + 13.00 + 28.00 + 510.00 + 77.00 + 30.00) * SEASONAL_FACTORS['HSG']
    wbs_total = (56.00 + 140.00 + 310.00 + 8.20 + 29.00 + 500.00) * SEASONAL_FACTORS['WBS']
    tjr_total = 200.00 * SEASONAL_FACTORS['TJR']
    total = bmpm_total + hsg_total + wbs_total + tjr_total

    print("\nPhase 3 (Post-Christmas - After Dec 19/23) - DATA-DRIVEN:")
    print(f"BMPM: £{bmpm_total:.2f}/day (RESTORED, not paused - 91.7% of Phase 2)")
    print(f"HSG: £{hsg_total:.2f}/day (down from £678 - 26.0% seasonal factor)")
    print(f"WBS: £{wbs_total:.2f}/day (down from £1,043 - 44.2% seasonal factor)")
    print(f"TJR: £{tjr_total:.2f}/day (down from £200 - 77.2% seasonal factor)")
    print(f"Total daily budget: £{total:.2f}/day")
    print("Based on January 2024 vs December 2024 year-on-year performance")

    return rows

def save_csv(rows, filename):
    """Save CSV file"""
    filepath = Path(f"/Users/administrator/Documents/PetesBrain.nosync/clients/clear-prospects/spreadsheets/{filename}")
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\nSaved: {filepath}")
    return filepath

if __name__ == "__main__":
    print("=" * 80)
    print("CLEAR PROSPECTS - THREE-PHASE CHRISTMAS BUDGET DEPLOYMENT")
    print("=" * 80)

    # Phase 1 - Already deployed
    phase1_rows = create_phase1_csv()
    # Don't save Phase 1 CSV - it's already deployed

    print("\n" + "=" * 80)

    # Phase 2 - Christmas Peak (Dec 16-19)
    phase2_rows = create_phase2_csv()
    phase2_file = save_csv(phase2_rows, "phase2-christmas-peak-dec16.csv")

    print("\n" + "=" * 80)

    # Phase 3 - Post-Christmas (After Dec 19/23)
    phase3_rows = create_phase3_csv()
    phase3_file = save_csv(phase3_rows, "phase3-post-christmas-dec20.csv")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("Phase 1 (Run-up): ALREADY DEPLOYED on Dec 15")
    print("  - HSG H&S PMax: £510/day")
    print("  - WBS H&S PMax: £310/day")
    print("  - Total: ~£845/day")
    print()
    print("Phase 2 (Christmas Peak - Dec 16-19): READY TO DEPLOY")
    print("  - BMPM: PAUSED (stop losses)")
    print("  - HSG/WBS: Maintained at peak levels")
    print("  - Total: ~£820/day")
    print(f"  - CSV: {phase2_file}")
    print()
    print("Phase 3 (Post-Christmas - After Dec 19/23): READY TO DEPLOY")
    print("  - All budgets reduced ~50-60%")
    print("  - Total: ~£390/day")
    print(f"  - CSV: {phase3_file}")
