#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Devonshire Hotels Budget Changes - November 20, 2025
Simplified approach using MCP server's infrastructure
"""

import sys
import os
from datetime import datetime
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

from oauth.google_auth import execute_mutation

CUSTOMER_ID = "5898250490"

# Budget changes
CHANGES = [
    ("11945680219", 36000000, "P Max All", 48, 36),
    ("12288076740", 100000000, "Dev Arms Hotel", 36, 100),
    ("14032878235", 48000000, "Cavendish", 50, 48),
    ("6448751751", 15000000, "Chatsworth Inns", 22, 15),
    ("14649374763", 26000000, "The Fell", 22, 26),
    ("12346612231", 25000000, "Chatsworth Locations", 15, 25),
    ("12270672141", 15000000, "Chatsworth SC", 18, 15),
]

def main():
    print("=" * 80)
    print("DEVONSHIRE HOTELS - BUDGET IMPLEMENTATION")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print(f"{'Campaign':<30} {'Old':<10} {'New':<10} Status")
    print("-" * 80)

    successful = 0
    failed = 0

    for budget_id, new_amount, name, old, new in CHANGES:
        mutation = f"""
        mutation {{
          mutateCampaignBudgets(
            customerId: "{CUSTOMER_ID}"
            operations: [{{
              update: {{
                resourceName: "customers/{CUSTOMER_ID}/campaignBudgets/{budget_id}"
                amountMicros: {new_amount}
              }}
              updateMask: "amountMicros"
            }}]
          ) {{
            results {{
              resourceName
            }}
          }}
        }}
        """

        try:
            result = execute_mutation(CUSTOMER_ID, mutation)
            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✓ SUCCESS")
            successful += 1
        except Exception as e:
            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✗ FAILED: {str(e)[:30]}")
            failed += 1

    print("-" * 80)
    print(f"\nSuccessful: {successful}/{len(CHANGES)}")
    print(f"Failed: {failed}/{len(CHANGES)}")

    if successful == len(CHANGES):
        print("\n✅ ALL CHANGES APPLIED SUCCESSFULLY\n")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
