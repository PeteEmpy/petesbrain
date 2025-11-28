#!/usr/bin/env python3
"""Deploy Phase 1 budget changes using Google Ads Python client"""

from google.ads.googleads.client import GoogleAdsClient
import json
import sys

# Load client
client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')

# Account to deploy
if len(sys.argv) < 3:
    print("Usage: python3 phase1-deploy-budgets.py <customer_id> <json_file>")
    sys.exit(1)

customer_id = sys.argv[1]
json_file = sys.argv[2]

# Load changes
with open(json_file, 'r') as f:
    changes = json.load(f)

print(f"\n{'='*120}")
print(f"DEPLOYING PHASE 1 BUDGET CHANGES - Customer ID: {customer_id}")
print(f"{'='*120}\n")

# Get services
campaign_budget_service = client.get_service("CampaignBudgetService")

successful = 0
failed = 0

for i, change in enumerate(changes, 1):
    campaign_name = change['campaign_name']
    budget_id = change['budget_id']
    new_budget = change['new_daily_budget']
    new_budget_micros = int(new_budget * 1_000_000)

    print(f"[{i}/{len(changes)}] {campaign_name:<65} → £{new_budget}/day", end="...")

    try:
        # Create budget operation
        budget_operation = client.get_type("CampaignBudgetOperation")
        budget = budget_operation.update
        budget.resource_name = campaign_budget_service.campaign_budget_path(customer_id, budget_id)
        budget.amount_micros = new_budget_micros

        # Set field mask
        client.copy_from(
            budget_operation.update_mask,
            client.get_type("FieldMask", version="v17"),
        )
        budget_operation.update_mask.paths.append("amount_micros")

        # Execute mutation
        response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[budget_operation]
        )

        print(" ✅ SUCCESS")
        successful += 1

    except Exception as e:
        print(f" ❌ FAILED: {str(e)[:80]}")
        failed += 1

print(f"\n{'='*120}")
print("RESULTS")
print(f"{'='*120}")
print(f"Successful: {successful}/{len(changes)}")
print(f"Failed: {failed}/{len(changes)}")

if successful == len(changes):
    print("\n✅ ALL BUDGET CHANGES SUCCESSFULLY APPLIED")
else:
    print(f"\n⚠️  {failed} CHANGES FAILED")

print(f"{'='*120}\n")

sys.exit(0 if failed == 0 else 1)
