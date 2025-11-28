#!/usr/bin/env python3
"""Deploy Phase 1 budget changes - simple direct mutation"""

from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import field_mask_pb2
import json
import sys

# Load client
client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')

# Account to deploy
if len(sys.argv) < 3:
    print("Usage: python3 phase1-deploy.py <customer_id> <json_file>")
    sys.exit(1)

customer_id = sys.argv[1]
json_file = sys.argv[2]

# Load changes
with open(json_file, 'r') as f:
    changes = json.load(f)

print(f"\n{'='*120}")
print(f"DEPLOYING PHASE 1 BUDGET CHANGES - Customer ID: {customer_id}")
print(f"{'='*120}\n")

# Get service
service = client.get_service("CampaignBudgetService")

successful = 0
failed = 0

for i, change in enumerate(changes, 1):
    campaign_name = change['campaign_name']
    budget_id = change['budget_id']
    new_budget = change['new_daily_budget']
    new_budget_micros = int(new_budget * 1_000_000)

    print(f"[{i}/{len(changes)}] {campaign_name:<65} → £{new_budget}/day", end="...")

    try:
        # Build resource name
        resource_name = service.campaign_budget_path(customer_id, budget_id)

        # Create operation
        operation = service.mutate_campaign_budgets.metadata.http.request.method_descriptor.options.google.api.http.put  # Get operation type
        # Simpler approach - just send dict
        operation = {
            "update": {
                "resourceName": resource_name,
                "amountMicros": str(new_budget_micros)
            },
            "updateMask": {"paths": ["amountMicros"]}
        }

        # This won't work, need to use proper protobuf. Let me try GAQL UPDATE instead
        # Google Ads doesn't support UPDATE via GAQL, must use mutations

        # Proper mutation approach
        from google.ads.googleads.v22.services.types import campaign_budget_service

        operation = campaign_budget_service.CampaignBudgetOperation()
        operation.update.resource_name = resource_name
        operation.update.amount_micros = new_budget_micros
        operation.update_mask.paths.append("amount_micros")

        response = service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[operation]
        )

        print(" ✅ SUCCESS")
        successful += 1

    except Exception as e:
        print(f" ❌ FAILED: {str(e)[:100]}")
        failed += 1

print(f"\n{'='*120}")
print(f"✅ Successful: {successful}/{len(changes)}")
if failed > 0:
    print(f"❌ Failed: {failed}/{len(changes)}")
print(f"{'='*120}\n")

sys.exit(0 if failed == 0 else 1)
