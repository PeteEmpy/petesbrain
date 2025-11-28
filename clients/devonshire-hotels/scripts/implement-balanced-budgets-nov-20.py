#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Implement Balanced Budget Changes - November 20, 2025

Restores client-approved budgets and deploys remaining budget strategically.
"""

import sys
import os
from datetime import datetime

# Add MCP server path
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server")

# Load environment
env_file = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "5898250490"

# Budget changes (amount in micros: £1 = 1,000,000 micros)
BUDGET_CHANGES = [
    {
        "campaign_id": "18899261254",
        "budget_id": "11945680219",
        "new_budget_micros": 36000000,
        "name": "P Max All",
        "old_daily": 48,
        "new_daily": 36,
        "reason": "Reduce underperformer (397% ROAS)"
    },
    {
        "campaign_id": "19577006833",
        "budget_id": "12288076740",
        "new_budget_micros": 100000000,
        "name": "Dev Arms Hotel",
        "old_daily": 36,
        "new_daily": 100,
        "reason": "Restore £52 approved + £48 additional (850% ROAS top performer)"
    },
    {
        "campaign_id": "21839323410",
        "budget_id": "14032878235",
        "new_budget_micros": 48000000,
        "name": "Cavendish",
        "old_daily": 50,
        "new_daily": 48,
        "reason": "Restore to client-approved budget"
    },
    {
        "campaign_id": "2080736142",
        "budget_id": "6448751751",
        "new_budget_micros": 15000000,
        "name": "Chatsworth Inns",
        "old_daily": 22,
        "new_daily": 15,
        "reason": "Reduce critical underperformer (140% ROAS)"
    },
    {
        "campaign_id": "22666031909",
        "budget_id": "14649374763",
        "new_budget_micros": 26000000,
        "name": "The Fell",
        "old_daily": 22,
        "new_daily": 26,
        "reason": "Restore to client-approved budget"
    },
    {
        "campaign_id": "19654308682",
        "budget_id": "12346612231",
        "new_budget_micros": 25000000,
        "name": "Chatsworth Locations",
        "old_daily": 15,
        "new_daily": 25,
        "reason": "Deploy additional budget (511% ROAS)"
    },
    {
        "campaign_id": "19534201089",
        "budget_id": "12270672141",
        "new_budget_micros": 15000000,
        "name": "Chatsworth SC",
        "old_daily": 18,
        "new_daily": 15,
        "reason": "Reduce underperformer (91% ROAS)"
    },
]


def update_budget(client, customer_id, budget_id, new_amount_micros):
    """Update a campaign budget"""
    campaign_budget_service = client.get_service("CampaignBudgetService")
    operation = client.get_type("CampaignBudgetOperation")

    budget = operation.update
    budget.resource_name = campaign_budget_service.campaign_budget_path(
        customer_id, budget_id
    )
    budget.amount_micros = new_amount_micros

    client.copy_from(
        operation.update_mask,
        client.get_type("FieldMask").from_dict({"paths": ["amount_micros"]})
    )

    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[operation]
    )
    return response


def main():
    print("=" * 80)
    print("BALANCED BUDGET IMPLEMENTATION - NOVEMBER 20, 2025")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Account: {CUSTOMER_ID}")
    print()

    # Initialize Google Ads client
    try:
        client = GoogleAdsClient.load_from_env()
    except Exception as e:
        print(f"ERROR: Failed to initialize Google Ads client: {e}")
        return 1

    print(f"{'Campaign':<25} {'Old Budget':<12} {'New Budget':<12} Status")
    print("-" * 80)

    successful = 0
    failed = 0

    for change in BUDGET_CHANGES:
        try:
            update_budget(
                client,
                CUSTOMER_ID,
                change["budget_id"],
                change["new_budget_micros"]
            )
            status = "✓ SUCCESS"
            successful += 1
        except GoogleAdsException as ex:
            status = f"✗ FAILED: {ex.failure.errors[0].message}"
            failed += 1
        except Exception as ex:
            status = f"✗ ERROR: {str(ex)}"
            failed += 1

        print(f"{change['name']:<25} £{change['old_daily']:>3}/day → £{change['new_daily']:>3}/day   {status}")

    print("-" * 80)
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Successful: {successful}/{len(BUDGET_CHANGES)}")
    print(f"Failed: {failed}/{len(BUDGET_CHANGES)}")

    if successful == len(BUDGET_CHANGES):
        print()
        print("✅ ALL BUDGET CHANGES SUCCESSFULLY IMPLEMENTED")
        print()
        print("CLIENT-APPROVED RESTORATIONS:")
        print("  • The Fell: £22 → £26/day (+£4) ✅")
        print("  • Dev Arms Hotel: £36 → £52 → £100/day (+£16 approved, +£48 additional)")
        print("  • Cavendish: £50 → £48/day (-£2) ✅")
        print()
        print("STRATEGIC REDUCTIONS:")
        print("  • P Max All: £48 → £36/day (-£12)")
        print("  • Chatsworth Inns: £22 → £15/day (-£7)")
        print("  • Chatsworth SC: £18 → £15/day (-£3)")
        print()
        print("ADDITIONAL DEPLOYMENT:")
        print("  • Dev Arms Hotel: +£48/day beyond approved")
        print("  • Chatsworth Locations: £15 → £25/day (+£10)")
        print()
        print("PROJECTION (Nov 21-30):")
        print("  • Current MTD (Day 20): £6,346.29")
        print("  • Additional 10 days @ £316/day: £3,160.00")
        print("  • Projected Month-End: £9,506.29")
        print("  • Budget: £10,261.60")
        print("  • Variance: £+755.31 (92.6% pacing)")
        print()
        print("NEXT STEPS:")
        print("  1. Monitor Dev Arms ROAS at £100/day (next 3 days)")
        print("  2. Audit Chatsworth Inns (140% ROAS - P0 urgent)")
        print("  3. Investigate Cavendish (498% ROAS despite 49% Lost IS - P1)")
        print("  4. Daily budget tracking continues automatically")
        print("  5. Log to experiment tracker for month-end review")
    else:
        print()
        print(f"⚠️  {failed} CHANGES FAILED - Review errors above")

    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
