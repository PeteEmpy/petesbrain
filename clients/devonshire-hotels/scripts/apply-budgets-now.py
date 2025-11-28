#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Devonshire Hotels Budget Changes - November 20, 2025
Simple direct approach using Google Ads API v22
"""

import sys
import os
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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "5898250490"

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

def main():
    print("=" * 80)
    print("DEVONSHIRE HOTELS - BUDGET IMPLEMENTATION")
    print("=" * 80)
    print()

    # Create google-ads.yaml config
    config_dir = Path.home() / '.google-ads'
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / 'google-ads.yaml'

    config_content = f"""developer_token: {os.environ.get('GOOGLE_ADS_DEVELOPER_TOKEN')}
client_id: {os.environ.get('GOOGLE_ADS_CLIENT_ID')}
client_secret: {os.environ.get('GOOGLE_ADS_CLIENT_SECRET')}
refresh_token: {os.environ.get('GOOGLE_ADS_REFRESH_TOKEN')}
use_proto_plus: True
"""

    with open(config_file, 'w') as f:
        f.write(config_content)

    print(f"Created config at: {config_file}")

    # Initialize client
    try:
        client = GoogleAdsClient.load_from_storage(str(config_file))
        print(f"✓ Google Ads client initialized")
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return 1

    print()
    print(f"{'Campaign':<30} {'Old':<10} {'New':<10} Status")
    print("-" * 80)

    successful = 0
    failed = 0

    for budget_id, new_amount, name, old, new in CHANGES:
        try:
            # Get service
            campaign_budget_service = client.get_service("CampaignBudgetService")

            # Create operation
            operation = client.get_type("CampaignBudgetOperation")
            budget = operation.update
            budget.resource_name = campaign_budget_service.campaign_budget_path(
                CUSTOMER_ID, budget_id
            )
            budget.amount_micros = new_amount

            # Set field mask
            client.copy_from(
                operation.update_mask,
                client.get_type("FieldMask")(paths=["amount_micros"])
            )

            # Execute mutation
            response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=CUSTOMER_ID,
                operations=[operation]
            )

            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✓ SUCCESS")
            successful += 1

        except GoogleAdsException as ex:
            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✗ FAILED: {ex.error.message}")
            failed += 1
        except Exception as e:
            print(f"{name:<30} £{old:>3}/day → £{new:>3}/day   ✗ ERROR: {str(e)[:40]}")
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
    sys.exit(main())
