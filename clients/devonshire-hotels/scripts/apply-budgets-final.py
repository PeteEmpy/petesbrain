#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Devonshire Hotels Budget Changes - November 20, 2025
Using MCP server's OAuth authentication infrastructure
"""

import sys
import os
import requests
from pathlib import Path

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

from oauth.google_auth import get_headers_with_auto_token, format_customer_id

CUSTOMER_ID = "5898250490"
API_VERSION = "v22"

# Budget changes (budget_id, new_amount_micros, name, old, new)
CHANGES = [
    ("11945680219", 36000000, "P Max All", 48, 36),
    ("12288076740", 100000000, "Dev Arms Hotel", 36, 100),
    ("14032878235", 48000000, "Cavendish", 50, 48),
    ("6448751751", 15000000, "Chatsworth Inns", 22, 15),
    ("14649374763", 26000000, "The Fell", 22, 26),
    ("12346612231", 25000000, "Chatsworth Locations", 15, 25),
    ("12270672141", 15000000, "Chatsworth SC", 18, 15),
]

def update_budget(customer_id, budget_id, new_amount_micros):
    """Update a campaign budget using REST API"""
    headers = get_headers_with_auto_token()
    formatted_customer_id = format_customer_id(customer_id)

    url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/campaignBudgets:mutate"

    payload = {
        "operations": [{
            "update": {
                "resourceName": f"customers/{formatted_customer_id}/campaignBudgets/{budget_id}",
                "amountMicros": new_amount_micros
            },
            "updateMask": "amountMicros"
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if not response.ok:
        raise Exception(f"{response.status_code}: {response.text}")

    return response.json()

def main():
    print("=" * 80)
    print("DEVONSHIRE HOTELS - BUDGET IMPLEMENTATION")
    print("=" * 80)
    print()
    print(f"{'Campaign':<30} {'Old':<10} {'New':<10} Status")
    print("-" * 80)

    successful = 0
    failed = 0

    for budget_id, new_amount, name, old, new in CHANGES:
        try:
            update_budget(CUSTOMER_ID, budget_id, new_amount)
            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✓ SUCCESS")
            successful += 1
        except Exception as e:
            error_msg = str(e)[:50]
            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✗ FAILED: {error_msg}")
            failed += 1

    print("-" * 80)
    print()
    print(f"Successful: {successful}/{len(CHANGES)}")
    print(f"Failed: {failed}/{len(CHANGES)}")

    if successful == len(CHANGES):
        print()
        print("✅ ALL CHANGES APPLIED SUCCESSFULLY")
        print()

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
