#!/usr/bin/env python3
"""
Smythson - Phase 1 Black Friday Budget Deployment
Deploy budget increases using Google Ads API v22
"""

import requests
import json
import sys

sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')
from oauth.google_auth import get_headers_with_auto_token

def update_budget(customer_id: str, budget_id: str, new_amount_gbp: float, campaign_name: str, manager_id: str = "2569949686") -> dict:
    """Update a campaign budget amount."""
    headers = get_headers_with_auto_token()

    # Add login customer ID header for manager account access
    headers['login-customer-id'] = manager_id

    # Format customer ID (remove dashes if present)
    formatted_customer_id = customer_id.replace("-", "")

    # Construct the budget resource name
    budget_resource_name = f"customers/{formatted_customer_id}/campaignBudgets/{budget_id}"

    # Convert GBP to micros
    amount_micros = int(new_amount_gbp * 1_000_000)

    # API endpoint for budget mutation
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/campaignBudgets:mutate"

    payload = {
        'operations': [{
            'updateMask': 'amountMicros',
            'update': {
                'resourceName': budget_resource_name,
                'amountMicros': str(amount_micros)
            }
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        return {"success": True}
    else:
        return {"success": False, "error": f"{response.status_code}: {response.text}"}

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 deploy-phase1-budgets.py <customer_id> <json_file>")
        sys.exit(1)

    customer_id = sys.argv[1]
    json_file = sys.argv[2]

    # Load changes
    with open(json_file, 'r') as f:
        changes = json.load(f)

    print(f"\n{'='*120}")
    print(f"SMYTHSON PHASE 1 - DEPLOYING BUDGET CHANGES")
    print(f"Customer ID: {customer_id}")
    print(f"Changes: {len(changes)} campaigns")
    print(f"{'='*120}\n")

    successful = 0
    failed = 0
    errors = []

    for i, change in enumerate(changes, 1):
        campaign_name = change['campaign_name']
        budget_id = change['budget_id']
        new_budget = change['new_daily_budget']

        print(f"[{i}/{len(changes)}] {campaign_name[:60]:<60} → £{new_budget:>6.2f}/day...", end="")

        result = update_budget(customer_id, budget_id, new_budget, campaign_name)

        if result["success"]:
            print(" ✅")
            successful += 1
        else:
            print(f" ❌")
            failed += 1
            errors.append((campaign_name, result['error']))

    print(f"\n{'='*120}")
    print("RESULTS")
    print(f"{'='*120}")
    print(f"✅ Successful: {successful}/{len(changes)}")

    if failed > 0:
        print(f"❌ Failed: {failed}/{len(changes)}\n")
        print("Errors:")
        for name, error in errors:
            print(f"  - {name[:50]}: {error[:70]}")
    else:
        print("\n🎉 ALL BUDGET CHANGES SUCCESSFULLY APPLIED!")

    print(f"{'='*120}\n")

    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
