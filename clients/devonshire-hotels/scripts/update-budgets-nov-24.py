#!/usr/bin/env python3
"""
Devonshire Hotels - Budget Update Script
November 24, 2025

Updates campaign budgets to close the predicted underspend gap.
"""

import requests
import json
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from oauth.google_auth import get_headers_with_auto_token

CUSTOMER_ID = "5898250490"

# Budget changes: campaign_name, budget_resource_id, current_budget_gbp, new_budget_gbp
BUDGET_CHANGES = [
    ("The Beeley Inn", "14556539992", 22, 45),
    ("Devonshire Arms Hotel", "12288076740", 100, 150),
    ("Cavendish", "14032878235", 48, 70),
    ("P Max All", "11945680219", 36, 75),
    ("The Pilsley Inn", "12266218514", 20, 35),
]

def update_budget(budget_id: str, new_amount_gbp: float) -> dict:
    """Update a campaign budget amount."""
    headers = get_headers_with_auto_token()

    # Format customer ID (remove dashes if present)
    formatted_customer_id = CUSTOMER_ID.replace("-", "")

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
        return {"success": True, "response": response.json()}
    else:
        return {"success": False, "error": f"{response.status_code}: {response.text}"}

def main():
    print("=" * 70)
    print("DEVONSHIRE HOTELS - BUDGET UPDATE")
    print("Date: November 24, 2025")
    print("=" * 70)
    print()

    results = []

    for campaign_name, budget_id, current, new in BUDGET_CHANGES:
        print(f"Updating {campaign_name}: £{current}/day → £{new}/day...")

        result = update_budget(budget_id, new)

        if result["success"]:
            print(f"  ✅ SUCCESS")
            results.append((campaign_name, True, None))
        else:
            print(f"  ❌ FAILED: {result['error']}")
            results.append((campaign_name, False, result['error']))

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    successes = [r for r in results if r[1]]
    failures = [r for r in results if not r[1]]

    print(f"Successful updates: {len(successes)}")
    print(f"Failed updates: {len(failures)}")

    if failures:
        print("\nFailed campaigns:")
        for name, _, error in failures:
            print(f"  - {name}: {error}")

    total_daily_increase = sum(new - current for _, _, current, new in BUDGET_CHANGES)
    print(f"\nTotal daily budget increase: +£{total_daily_increase}")
    print(f"6-day impact: +£{total_daily_increase * 6}")

if __name__ == "__main__":
    main()
