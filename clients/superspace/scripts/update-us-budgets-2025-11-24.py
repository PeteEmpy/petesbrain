#!/usr/bin/env python3
"""
Superspace US Budget Update - 2025-11-24
10% Conversion Reduction Strategy

Updates budgets for 3 campaigns:
- Shopping Branded: $3,669 → $2,935 (-20%)
- P Max Brand Excluded: $3,121 → $2,809 (-10%)
- Shopping Brand Excluded: $2,613 → $2,221 (-15%)
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Add the MCP server path to import OAuth helper
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')
from oauth.google_auth import get_headers_with_auto_token, format_customer_id

load_dotenv('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env')

CUSTOMER_ID = "7482100090"

# Budget changes: budget_id -> new_amount_micros
# $1 = 1,000,000 micros
BUDGET_UPDATES = {
    "14412940053": 2935000000,  # Shopping Branded: $2,935
    "11914791987": 2809000000,  # P Max Brand Excluded: $2,809
    "14021953807": 2221000000,  # Shopping Brand Excluded: $2,221
}

BUDGET_NAMES = {
    "14412940053": "Shopping Branded",
    "11914791987": "P Max Brand Excluded",
    "14021953807": "Shopping Brand Excluded",
}

def update_budget(customer_id: str, budget_id: str, new_amount_micros: int) -> dict:
    """Update a campaign budget amount."""
    formatted_id = format_customer_id(customer_id)
    headers = get_headers_with_auto_token()

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_id}/campaignBudgets:mutate"

    payload = {
        "operations": [
            {
                "update": {
                    "resourceName": f"customers/{formatted_id}/campaignBudgets/{budget_id}",
                    "amountMicros": str(new_amount_micros)
                },
                "updateMask": "amountMicros"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return {"success": True, "response": response.json()}
    else:
        return {"success": False, "error": response.text, "status": response.status_code}

def main():
    print("=" * 60)
    print("Superspace US Budget Update - 2025-11-24")
    print("10% Conversion Reduction Strategy")
    print("=" * 60)
    print()

    results = []

    for budget_id, new_amount_micros in BUDGET_UPDATES.items():
        name = BUDGET_NAMES[budget_id]
        new_amount_dollars = new_amount_micros / 1_000_000

        print(f"Updating {name}...")
        print(f"  Budget ID: {budget_id}")
        print(f"  New Amount: ${new_amount_dollars:,.0f}/day")

        result = update_budget(CUSTOMER_ID, budget_id, new_amount_micros)

        if result["success"]:
            print(f"  ✓ SUCCESS")
            results.append((name, True, new_amount_dollars))
        else:
            print(f"  ✗ FAILED: {result.get('error', 'Unknown error')}")
            results.append((name, False, new_amount_dollars))

        print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    success_count = sum(1 for _, success, _ in results if success)

    for name, success, amount in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}: ${amount:,.0f}/day")

    print()
    print(f"Completed: {success_count}/{len(results)} budgets updated")

    return success_count == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
