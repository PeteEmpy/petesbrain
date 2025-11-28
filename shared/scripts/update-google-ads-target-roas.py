#!/usr/bin/env python3
"""
Simple Google Ads Target ROAS Updater
Usage: python3 update-google-ads-target-roas.py --customer-id XXXXX --campaign "Campaign Name" --target-roas 3.0
       OR provide multiple campaigns via JSON file
"""

import sys
import json
import argparse
from pathlib import Path

# Add MCP server to path for OAuth
mcp_path = Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google.ads.googleads.client import GoogleAdsClient
import requests
from oauth.google_auth import get_headers_with_auto_token

MANAGER_ID = "2569949686"  # Rok Systems MCC


def get_campaign_by_name(customer_id: str, campaign_name_pattern: str):
    """Find campaign by name pattern and get current target ROAS."""
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    query = f'''
        SELECT
            campaign.id,
            campaign.name,
            campaign.target_roas.target_roas,
            campaign.bidding_strategy_type
        FROM campaign
        WHERE campaign.status = "ENABLED"
        AND campaign.name LIKE "%{campaign_name_pattern}%"
    '''

    response = ga_service.search(customer_id=customer_id, query=query)
    results = list(response)

    if not results:
        return None

    row = results[0]

    # Get current target ROAS if it exists
    current_roas = None
    if hasattr(row.campaign, 'target_roas') and hasattr(row.campaign.target_roas, 'target_roas'):
        current_roas = row.campaign.target_roas.target_roas

    return {
        'campaign_id': str(row.campaign.id),
        'campaign_name': row.campaign.name,
        'current_target_roas': current_roas,
        'bidding_strategy': row.campaign.bidding_strategy_type.name
    }


def update_target_roas_http(customer_id: str, campaign_id: str, target_roas: float):
    """Update target ROAS using HTTP API."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = MANAGER_ID

    formatted_customer_id = customer_id.replace("-", "")
    campaign_resource_name = f"customers/{formatted_customer_id}/campaigns/{campaign_id}"

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/campaigns:mutate"

    payload = {
        'operations': [{
            'updateMask': 'target_roas.target_roas',
            'update': {
                'resourceName': campaign_resource_name,
                'targetRoas': {
                    'targetRoas': target_roas
                }
            }
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        return True, None
    else:
        return False, f"{response.status_code}: {response.text[:100]}"


def main():
    parser = argparse.ArgumentParser(description='Update Google Ads campaign target ROAS')
    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--campaign', help='Campaign name (or partial match)')
    parser.add_argument('--target-roas', type=float, help='New target ROAS (e.g., 3.0 for 300%%)')
    parser.add_argument('--file', help='JSON file with multiple updates')

    args = parser.parse_args()

    # Single campaign update
    if args.campaign and args.target_roas:
        print(f"\nFinding campaign: {args.campaign}")

        campaign = get_campaign_by_name(args.customer_id, args.campaign)

        if not campaign:
            print(f"❌ Campaign not found matching '{args.campaign}'")
            return 1

        print(f"Found: {campaign['campaign_name']}")
        print(f"Bidding strategy: {campaign['bidding_strategy']}")

        if campaign['current_target_roas']:
            print(f"Current target ROAS: {campaign['current_target_roas']:.2f} ({campaign['current_target_roas']*100:.0f}%)")
        else:
            print(f"Current target ROAS: Not set")

        print(f"New target ROAS: {args.target_roas:.2f} ({args.target_roas*100:.0f}%)")

        if campaign['bidding_strategy'] != 'TARGET_ROAS':
            print(f"\n⚠️  Warning: Campaign bidding strategy is '{campaign['bidding_strategy']}', not 'TARGET_ROAS'")
            print(f"   This will change the bidding strategy to Target ROAS.")
            response = input("Continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Cancelled.")
                return 0

        print(f"\nUpdating...", end="")

        success, error = update_target_roas_http(args.customer_id, campaign['campaign_id'], args.target_roas)

        if success:
            print(" ✅ SUCCESS")
            return 0
        else:
            print(f" ❌ FAILED\n{error}")
            return 1

    # Batch update from file
    elif args.file:
        with open(args.file, 'r') as f:
            updates = json.load(f)

        print(f"\nUpdating {len(updates)} campaigns...\n")

        successful = 0
        failed = 0

        for update in updates:
            campaign_pattern = update.get('campaign_name') or update.get('campaign')
            new_roas = update['target_roas']

            campaign = get_campaign_by_name(args.customer_id, campaign_pattern)

            if not campaign:
                print(f"❌ Not found: {campaign_pattern}")
                failed += 1
                continue

            current_display = f"{campaign['current_target_roas']:.2f}" if campaign['current_target_roas'] else "None"
            print(f"{campaign['campaign_name'][:50]:<50} {current_display:>6} → {new_roas:<6.2f}...", end="")

            success, error = update_target_roas_http(args.customer_id, campaign['campaign_id'], new_roas)

            if success:
                print(" ✅")
                successful += 1
            else:
                print(f" ❌")
                failed += 1

        print(f"\n✅ {successful}/{len(updates)} successful")
        if failed > 0:
            print(f"❌ {failed}/{len(updates)} failed")

        return 0 if failed == 0 else 1

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
