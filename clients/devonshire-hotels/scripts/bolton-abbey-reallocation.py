#!/usr/bin/env python3
"""
Devonshire Hotels - Bolton Abbey Budget Reallocation
Pause Bolton Abbey Locations and increase Cavendish budget

Date: 2025-11-18
Test: Budget reallocation to justify additional Cavendish spend
"""

import os
import sys
import json
from datetime import datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configuration
CUSTOMER_ID = "5898250490"
BOLTON_ABBEY_CAMPAIGN_ID = "22720114456"
CAVENDISH_CAMPAIGN_ID = "21839323410"
CAVENDISH_BUDGET_ID = "14032878235"  # From GAQL query

# New budget: £59/day = 59,000,000 micros
NEW_BUDGET_MICROS = 59000000

def pause_campaign(client, customer_id, campaign_id):
    """Pause a campaign"""
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")

    campaign_resource_name = campaign_service.campaign_path(customer_id, campaign_id)
    campaign = campaign_operation.update
    campaign.resource_name = campaign_resource_name
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    campaign_operation.update_mask = client.get_type("FieldMask").get_field_mask(campaign)

    try:
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation]
        )
        return {
            "success": True,
            "resource_name": response.results[0].resource_name,
            "message": f"Campaign {campaign_id} paused successfully"
        }
    except GoogleAdsException as ex:
        return {
            "success": False,
            "error": ex.failure.errors[0].message if ex.failure.errors else str(ex)
        }

def update_campaign_budget(client, customer_id, budget_id, new_amount_micros):
    """Update campaign budget amount"""
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")

    budget_resource_name = campaign_budget_service.campaign_budget_path(customer_id, budget_id)
    campaign_budget = campaign_budget_operation.update
    campaign_budget.resource_name = budget_resource_name
    campaign_budget.amount_micros = new_amount_micros

    campaign_budget_operation.update_mask = client.get_type("FieldMask").get_field_mask(campaign_budget)

    try:
        response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[campaign_budget_operation]
        )
        return {
            "success": True,
            "resource_name": response.results[0].resource_name,
            "message": f"Budget {budget_id} updated to {new_amount_micros} micros (£{new_amount_micros/1000000:.2f}/day)"
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
        log_data = {"changes": []}

    # Add new changes
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": "bolton_abbey_budget_reallocation",
        "changes": changes
    }
    log_data["changes"].append(log_entry)

    # Save log
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)

    print(f"\n✅ Changes logged to: {log_file}")

def main():
    """Main execution"""
    print("=" * 70)
    print("Devonshire Hotels - Bolton Abbey Budget Reallocation")
    print("=" * 70)
    print("\nChanges to be made:")
    print(f"1. Pause Bolton Abbey Locations (Campaign ID: {BOLTON_ABBEY_CAMPAIGN_ID})")
    print(f"2. Increase Cavendish budget to £59/day (Campaign ID: {CAVENDISH_CAMPAIGN_ID})")
    print("\nThis is a TEST to justify the additional budget increase.")
    print("=" * 70)

    # Initialize client
    try:
        client = GoogleAdsClient.load_from_storage()
    except Exception as e:
        print(f"\n❌ Error loading Google Ads client: {e}")
        print("\nMake sure google-ads.yaml is configured correctly.")
        sys.exit(1)

    changes = []

    # Step 1: Pause Bolton Abbey
    print("\n📋 Step 1: Pausing Bolton Abbey Locations campaign...")
    bolton_result = pause_campaign(client, CUSTOMER_ID, BOLTON_ABBEY_CAMPAIGN_ID)
    changes.append({
        "campaign_id": BOLTON_ABBEY_CAMPAIGN_ID,
        "campaign_name": "DEV | Properties BE | Bolton Abbey Escapes Locations",
        "action": "pause_campaign",
        "result": bolton_result
    })

    if bolton_result["success"]:
        print(f"   ✅ {bolton_result['message']}")
    else:
        print(f"   ❌ Failed: {bolton_result['error']}")

    # Step 2: Update Cavendish budget
    print("\n📋 Step 2: Updating Cavendish campaign budget to £59/day...")
    cavendish_result = update_campaign_budget(client, CUSTOMER_ID, CAVENDISH_BUDGET_ID, NEW_BUDGET_MICROS)
    changes.append({
        "campaign_id": CAVENDISH_CAMPAIGN_ID,
        "budget_id": CAVENDISH_BUDGET_ID,
        "campaign_name": "DEV | Properties CE | Cavendish",
        "action": "update_budget",
        "old_budget_micros": 48000000,
        "new_budget_micros": NEW_BUDGET_MICROS,
        "old_budget_daily": "£48",
        "new_budget_daily": "£59",
        "result": cavendish_result
    })

    if cavendish_result["success"]:
        print(f"   ✅ {cavendish_result['message']}")
    else:
        print(f"   ❌ Failed: {cavendish_result['error']}")

    # Log changes
    log_changes(changes)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    success_count = sum(1 for c in changes if c["result"]["success"])
    total_count = len(changes)

    print(f"\n✅ Successfully completed: {success_count}/{total_count} operations")

    if success_count == total_count:
        print("\n🎉 All changes applied successfully!")
        print("\nNext steps:")
        print("1. Monitor Cavendish daily spend (should increase to ~£59/day)")
        print("2. Track budget lost impression share (should reduce from 49%)")
        print("3. Review end of November in monthly report")
        print("4. Justify continued higher budget to client")
        print("\nBaseline snapshot: clients/devonshire-hotels/documents/cavendish-budget-increase-baseline-nov-18.md")
        print("Experiment log: roksys/spreadsheets/rok-experiments-client-notes.csv (18/11/2025 entry)")
    else:
        print("\n⚠️ Some operations failed. Please review errors above.")

    print("=" * 70)

if __name__ == "__main__":
    main()
