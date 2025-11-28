#!/usr/bin/env python3
"""
Devonshire Hotels - Revenue-Proportional Budget Reductions
Update campaign budgets via Google Ads API

Date: 2025-11-18
Reason: Reduce overspend - property campaigns only, proportional to revenue
"""

import os
import sys
import json
from datetime import datetime

# Add Google Ads MCP path
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server")

# Load environment variables
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
from google.protobuf import field_mask_pb2

# Configuration
CUSTOMER_ID = "5898250490"

# Budget changes (budget_id, old_amount, new_amount, campaign_name)
BUDGET_UPDATES = [
    {
        "budget_id": "11945680219",
        "campaign_name": "P Max All",
        "old_budget": 66000000,
        "new_budget": 48000000,
        "old_daily": "£66",
        "new_daily": "£48",
        "reason": "Revenue 29.11% of total, proportional reduction"
    },
    {
        "budget_id": "12288076740",
        "campaign_name": "Dev Arms Hotel",
        "old_budget": 52000000,
        "new_budget": 36000000,
        "old_daily": "£52",
        "new_daily": "£36",
        "reason": "Revenue 25.96% of total, proportional reduction"
    },
    {
        "budget_id": "14032878235",
        "campaign_name": "Cavendish",
        "old_budget": 59000000,
        "new_budget": 50000000,
        "old_daily": "£59",
        "new_daily": "£50",
        "reason": "Revenue 14.19% of total, proportional reduction (still £2 above original £48 for test)"
    },
    {
        "budget_id": "14556539992",
        "campaign_name": "Beeley Inn",
        "old_budget": 29000000,
        "new_budget": 22000000,
        "old_daily": "£29",
        "new_daily": "£22",
        "reason": "Revenue 12.13% of total, proportional reduction"
    },
    {
        "budget_id": "14649374763",
        "campaign_name": "The Fell",
        "old_budget": 26000000,
        "new_budget": 22000000,
        "old_daily": "£26",
        "new_daily": "£22",
        "reason": "Revenue 6.56% of total, proportional reduction"
    },
    {
        "budget_id": "12266218514",
        "campaign_name": "Pilsley Inn",
        "old_budget": 24000000,
        "new_budget": 20000000,
        "old_daily": "£24",
        "new_daily": "£20",
        "reason": "Revenue 6.20% of total, proportional reduction"
    },
    {
        "budget_id": "6448751751",
        "campaign_name": "Chatsworth Inns",
        "old_budget": 25000000,
        "new_budget": 22000000,
        "old_daily": "£25",
        "new_daily": "£22",
        "reason": "Revenue 4.25% of total, proportional reduction"
    },
    {
        "budget_id": "12346612231",
        "campaign_name": "Chatsworth Locations",
        "old_budget": 16000000,
        "new_budget": 15000000,
        "old_daily": "£16",
        "new_daily": "£15",
        "reason": "Revenue 2.29% of total, proportional reduction"
    }
]


def update_campaign_budget(client, customer_id, budget_id, new_amount_micros):
    """Update a campaign budget amount"""
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")

    budget_resource_name = campaign_budget_service.campaign_budget_path(customer_id, budget_id)
    campaign_budget = campaign_budget_operation.update
    campaign_budget.resource_name = budget_resource_name
    campaign_budget.amount_micros = new_amount_micros

    field_mask = field_mask_pb2.FieldMask(paths=["amount_micros"])
    campaign_budget_operation.update_mask = field_mask

    try:
        response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[campaign_budget_operation]
        )
        return {
            "success": True,
            "resource_name": response.results[0].resource_name
        }
    except GoogleAdsException as ex:
        return {
            "success": False,
            "error": ex.failure.errors[0].message if ex.failure.errors else str(ex)
        }


def log_changes(changes):
    """Log API changes to JSON file"""
    log_file = "/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/api-changes-log.json"

    # Load existing log
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = []

    # Add new change entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "BUDGET_UPDATE_REVENUE_PROPORTIONAL",
        "customer_id": CUSTOMER_ID,
        "reason": "November overspend reduction - property campaigns only, proportional to revenue contribution",
        "total_reduction": "£61/day",
        "changes": changes
    }
    log_data.append(log_entry)

    # Save log
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)

    print(f"\n✅ Changes logged to: {log_file}")


def main():
    """Main execution"""
    print("=" * 70)
    print("Devonshire Hotels - Revenue-Proportional Budget Reductions")
    print("=" * 70)
    print("\n📊 Strategy: Property campaigns only, cuts proportional to revenue")
    print("🎯 Goal: Reduce daily spend from £315 to £253 (-£61/day)")
    print("📅 Effective: Nov 19-30 (12 days remaining)")
    print("\n" + "=" * 70)

    # Initialize client
    try:
        client = GoogleAdsClient.load_from_storage()
    except Exception as e:
        print(f"\n❌ Error loading Google Ads client: {e}")
        sys.exit(1)

    changes = []
    total_old = 0
    total_new = 0

    # Process each budget update
    for update in BUDGET_UPDATES:
        print(f"\n📋 Updating: {update['campaign_name']}")
        print(f"   Current: {update['old_daily']}/day ({update['old_budget']:,} micros)")
        print(f"   New: {update['new_daily']}/day ({update['new_budget']:,} micros)")
        print(f"   Reason: {update['reason']}")

        result = update_campaign_budget(
            client,
            CUSTOMER_ID,
            update['budget_id'],
            update['new_budget']
        )

        change_record = {
            "budget_id": update['budget_id'],
            "campaign_name": update['campaign_name'],
            "old_budget_micros": update['old_budget'],
            "new_budget_micros": update['new_budget'],
            "old_daily": update['old_daily'],
            "new_daily": update['new_daily'],
            "reduction": f"{(update['old_budget'] - update['new_budget']) / 1000000:.0f}",
            "reason": update['reason'],
            "result": result
        }
        changes.append(change_record)

        if result["success"]:
            print(f"   ✅ SUCCESS")
            total_old += update['old_budget']
            total_new += update['new_budget']
        else:
            print(f"   ❌ FAILED: {result['error']}")

    # Log all changes
    log_changes(changes)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    success_count = sum(1 for c in changes if c["result"]["success"])
    total_count = len(changes)

    print(f"\n✅ Successfully updated: {success_count}/{total_count} budgets")

    if success_count > 0:
        total_reduction = (total_old - total_new) / 1000000
        print(f"\n💰 Budget Changes:")
        print(f"   Previous total: £{total_old / 1000000:.0f}/day")
        print(f"   New total: £{total_new / 1000000:.0f}/day")
        print(f"   Total reduction: £{total_reduction:.0f}/day")

    if success_count == total_count:
        print("\n🎉 All budget updates completed successfully!")
        print("\n📊 Expected Impact (Nov 19-30):")
        print("   - Daily spend: £253/day (down from £315/day)")
        print("   - Remaining 12 days: £3,036 projected spend")
        print("   - Month-end total: £8,980 (hits £9,000 target)")
        print("\n📝 Next Steps:")
        print("   1. Monitor daily spend for next 3 days")
        print("   2. Verify campaigns hitting new budget levels")
        print("   3. Review Cavendish test performance (£50/day, still £2 above baseline)")
        print("\n📄 Documentation:")
        print("   - Analysis: clients/devonshire-hotels/documents/nov-18-revenue-proportional-cuts.md")
        print("   - API Log: clients/devonshire-hotels/api-changes-log.json")
    else:
        print("\n⚠️ Some updates failed. Please review errors above.")

    print("=" * 70)


if __name__ == "__main__":
    main()
