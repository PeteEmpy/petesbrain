#!/usr/bin/env python3
"""
Budget increase for AFH PMax H&S campaign
Date: 2025-11-18 21:44
Change: £1,600/day → £1,800/day (+£200)
"""

import os
import sys
from datetime import datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import json

# Set credentials
os.environ['GOOGLE_ADS_CONFIGURATION_FILE_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/google-ads.yaml'

# Initialize client
client = GoogleAdsClient.load_from_storage()
customer_id = "7972994730"
budget_resource_name = "customers/7972994730/campaignBudgets/12692019746"

# New budget
new_budget_micros = 1800000000  # £1,800/day
old_budget_micros = 1600000000  # £1,600/day

print(f"Updating AFH PMax H&S budget...")
print(f"Old: £{old_budget_micros/1000000:.2f}/day")
print(f"New: £{new_budget_micros/1000000:.2f}/day")
print(f"Increase: £{(new_budget_micros - old_budget_micros)/1000000:.2f}/day")

# Create budget operation
campaign_budget_service = client.get_service("CampaignBudgetService")
campaign_budget_operation = client.get_type("CampaignBudgetOperation")

campaign_budget = campaign_budget_operation.update
campaign_budget.resource_name = budget_resource_name
campaign_budget.amount_micros = new_budget_micros

field_mask = client.get_type("FieldMask")
field_mask.paths.append("amount_micros")
campaign_budget_operation.update_mask.CopyFrom(field_mask)

# Execute update
try:
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[campaign_budget_operation]
    )

    print(f"\n✅ Budget updated successfully!")
    print(f"Resource: {response.results[0].resource_name}")

    # Log to api-changes-log.json
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "budget_update",
        "customer_id": customer_id,
        "campaign_id": "20276730131",
        "campaign_name": "AFH | P Max | H&S Zombies Furniture",
        "budget_resource_name": budget_resource_name,
        "old_value_micros": old_budget_micros,
        "new_value_micros": new_budget_micros,
        "old_value_pounds": old_budget_micros / 1000000,
        "new_value_pounds": new_budget_micros / 1000000,
        "change_pounds": (new_budget_micros - old_budget_micros) / 1000000,
        "status": "SUCCESS",
        "method": "Google Ads API",
        "script": "budget-increase-nov18.py"
    }

    log_file = "/Users/administrator/Documents/PetesBrain/clients/accessories-for-the-home/api-changes-log.json"

    # Read existing log
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    # Append new entry
    logs.append(log_entry)

    # Write back
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"\n✅ Logged to api-changes-log.json")

except GoogleAdsException as ex:
    print(f"\n❌ Request failed with status {ex.error.code().name}")
    for error in ex.failure.errors:
        print(f"\tError: {error.message}")
    sys.exit(1)
