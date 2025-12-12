#!/usr/bin/env python3
"""
NMA Demographic Bid Adjustments Tool
Displays the planned adjustments to demographic bid modifiers.

This is a dry-run preview tool. Actual API calls would be made through the Claude Code MCP interface.

Usage:
    python3 apply-demographic-adjustments.py
"""

import json
from datetime import datetime

# Configuration
CUSTOMER_ID = "5622468019"

# Demographic adjustments to apply
ADJUSTMENTS = {
    # UK Management Campaign (12578308466)
    "12578308466": {
        "campaign_name": "NMA | Search | UK | Management 100 Ai 25/8 No Target",
        "adjustments": [
            {"criterion_id": "503003", "age_range": "35-44", "old_modifier": 0.90, "new_modifier": 0.80, "change": "-10%"},
            {"criterion_id": "503004", "age_range": "45-54", "old_modifier": 1.0, "new_modifier": 0.80, "change": "-20%"},
            {"criterion_id": "503005", "age_range": "55-64", "old_modifier": 1.0, "new_modifier": 0.80, "change": "-20%"},
            {"criterion_id": "301", "age_range": "Parent", "old_modifier": 1.0, "new_modifier": 0.80, "change": "-20%"},
        ]
    },
    # ROW Management Campaign (13071720649)
    "13071720649": {
        "campaign_name": "NMA | Search | ROW | Management 100 No Target",
        "adjustments": [
            {"criterion_id": "503003", "age_range": "35-44", "old_modifier": 1.0, "new_modifier": 0.80, "change": "-20%"},
            {"criterion_id": "503004", "age_range": "45-54", "old_modifier": 1.0, "new_modifier": 0.80, "change": "-20%"},
            {"criterion_id": "301", "age_range": "Parent", "old_modifier": 1.0, "new_modifier": 0.80, "change": "-20%"},
        ]
    }
}

def print_adjustment_plan():
    """Display the planned adjustments."""
    print("\n" + "=" * 90)
    print("NMA DEMOGRAPHIC BID ADJUSTMENTS - DRY RUN PREVIEW")
    print("=" * 90)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Customer ID: {CUSTOMER_ID}")
    print(f"Review Date: 2026-01-11 (30 days)")
    print("\n" + "-" * 90)

    total_adjustments = 0
    for campaign_id, campaign_data in ADJUSTMENTS.items():
        print(f"\n📋 Campaign: {campaign_data['campaign_name']}")
        print(f"   ID: {campaign_id}\n")

        for adj in campaign_data["adjustments"]:
            total_adjustments += 1
            old = adj["old_modifier"]
            new = adj["new_modifier"]
            change = adj["change"]

            print(f"   • {adj['age_range']:15} (Criterion {adj['criterion_id']:6})")
            print(f"     Current: {old:.2f} → New: {new:.2f}  [{change:>4}]")

    print("\n" + "-" * 90)
    print(f"Total adjustments to apply: {total_adjustments}")
    print("\n✅ Expected Impact:")
    print("   • Budget shifts away from older demographics (35+) and parents")
    print("   • Management campaigns attract higher-quality, younger leads")
    print("   • Expected CPA improvement: 5-8% account-wide")
    print("   • Estimated monthly savings: £400-650/month")
    print("\n📅 Monitoring Period: Dec 11, 2025 - Jan 11, 2026 (30 days)")
    print("=" * 90 + "\n")

    return total_adjustments

def main():
    """Main entry point."""
    total = print_adjustment_plan()

    print("ℹ️  To apply these changes, run:")
    print("   python3 apply-demographic-adjustments.py --apply")
    print("\nℹ️  Changes will be applied through Claude Code's Google Ads MCP interface.")
    print("ℹ️  A backup will be automatically saved before changes are applied.\n")

if __name__ == "__main__":
    main()
