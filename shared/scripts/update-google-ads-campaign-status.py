#!/usr/bin/env python3
"""
Simple Google Ads Campaign Status Updater
Usage: python3 update-google-ads-campaign-status.py --customer-id XXXXX --campaign "Campaign Name" --status ENABLED
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
    """Find campaign by name pattern."""
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    query = f'''
        SELECT campaign.id, campaign.name, campaign.status
        FROM campaign
        WHERE campaign.name LIKE "%{campaign_name_pattern}%"
    '''

    response = ga_service.search(customer_id=customer_id, query=query)
    results = list(response)

    if not results:
        return None

    row = results[0]
    return {
        'campaign_id': str(row.campaign.id),
        'campaign_name': row.campaign.name,
        'current_status': row.campaign.status.name
    }


def update_campaign_status_http(customer_id: str, campaign_id: str, new_status: str):
    """Update campaign status using HTTP API."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = MANAGER_ID

    formatted_customer_id = customer_id.replace("-", "")
    campaign_resource_name = f"customers/{formatted_customer_id}/campaigns/{campaign_id}"

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/campaigns:mutate"

    payload = {
        'operations': [{
            'updateMask': 'status',
            'update': {
                'resourceName': campaign_resource_name,
                'status': new_status
            }
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        return True, None
    else:
        return False, f"{response.status_code}: {response.text[:100]}"


def main():
    parser = argparse.ArgumentParser(description='Update Google Ads campaign status (pause/enable)')
    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--campaign', help='Campaign name (or partial match)')
    parser.add_argument('--status', choices=['ENABLED', 'PAUSED', 'REMOVED'], help='New status')
    parser.add_argument('--file', help='JSON file with multiple updates')

    args = parser.parse_args()

    # Single campaign update
    if args.campaign and args.status:
        print(f"\nFinding campaign: {args.campaign}")

        campaign = get_campaign_by_name(args.customer_id, args.campaign)

        if not campaign:
            print(f"❌ Campaign not found matching '{args.campaign}'")
            return 1

        print(f"Found: {campaign['campaign_name']}")
        print(f"Current status: {campaign['current_status']}")
        print(f"New status: {args.status}")
        print(f"\nUpdating...", end="")

        success, error = update_campaign_status_http(args.customer_id, campaign['campaign_id'], args.status)

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
            new_status = update['status']

            campaign = get_campaign_by_name(args.customer_id, campaign_pattern)

            if not campaign:
                print(f"❌ Not found: {campaign_pattern}")
                failed += 1
                continue

            status_emoji = "⏸️ " if new_status == "PAUSED" else "▶️ "
            print(f"{status_emoji}{campaign['campaign_name'][:60]:<60} {campaign['current_status']:>10} → {new_status:<10}...", end="")

            success, error = update_campaign_status_http(args.customer_id, campaign['campaign_id'], new_status)

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
