#!/usr/bin/env python3
"""
Simple Google Ads Keyword Status Updater (Pause/Enable)
Usage: python3 update-google-ads-keyword-status.py --customer-id XXXXX --campaign "Campaign Name" --keyword "exact keyword text" --status PAUSED
       OR provide keywords via JSON file
"""

import sys
import json
import argparse
from pathlib import Path

# Add MCP server to path
mcp_path = Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google.ads.googleads.client import GoogleAdsClient
import requests
from oauth.google_auth import get_headers_with_auto_token

MANAGER_ID = "2569949686"  # Rok Systems MCC


def find_keyword(customer_id: str, campaign_name_pattern: str, keyword_text: str):
    """Find keyword by campaign name and keyword text."""
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    query = f'''
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group_criterion.criterion_id,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            campaign.name,
            campaign.id
        FROM ad_group_criterion
        WHERE campaign.name LIKE "%{campaign_name_pattern}%"
        AND ad_group_criterion.keyword.text LIKE "%{keyword_text}%"
        AND ad_group_criterion.type = KEYWORD
    '''

    response = ga_service.search(customer_id=customer_id, query=query)
    results = list(response)

    if not results:
        return None

    row = results[0]
    return {
        'ad_group_id': str(row.ad_group.id),
        'ad_group_name': row.ad_group.name,
        'criterion_id': str(row.ad_group_criterion.criterion_id),
        'keyword_text': row.ad_group_criterion.keyword.text,
        'match_type': row.ad_group_criterion.keyword.match_type.name,
        'current_status': row.ad_group_criterion.status.name,
        'campaign_name': row.campaign.name
    }


def update_keyword_status_http(customer_id: str, ad_group_id: str, criterion_id: str, new_status: str):
    """Update keyword status using HTTP API."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = MANAGER_ID

    formatted_customer_id = customer_id.replace("-", "")
    criterion_resource_name = f"customers/{formatted_customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}"

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/adGroupCriteria:mutate"

    payload = {
        'operations': [{
            'updateMask': 'status',
            'update': {
                'resourceName': criterion_resource_name,
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
    parser = argparse.ArgumentParser(
        description='Update Google Ads keyword status (pause/enable)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Pause single keyword
  python3 update-google-ads-keyword-status.py --customer-id 8573235780 --campaign "Brand Exact" --keyword "smythson" --status PAUSED

  # Enable keyword
  python3 update-google-ads-keyword-status.py --customer-id 8573235780 --campaign "Brand" --keyword "luxury stationery" --status ENABLED

  # Batch update from JSON file
  python3 update-google-ads-keyword-status.py --customer-id 8573235780 --file keywords.json

JSON Format:
[
  {
    "campaign": "Brand Exact",
    "keyword": "smythson",
    "status": "PAUSED"
  },
  {
    "campaign": "Shopping",
    "keyword": "luxury notebooks",
    "status": "ENABLED"
  }
]
"""
    )

    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--campaign', help='Campaign name (or partial match)')
    parser.add_argument('--keyword', help='Keyword text to find')
    parser.add_argument('--status', choices=['ENABLED', 'PAUSED', 'REMOVED'], help='New status')
    parser.add_argument('--file', help='JSON file with batch updates')

    args = parser.parse_args()

    # Single keyword update
    if args.campaign and args.keyword and args.status:
        print(f"\nFinding keyword in campaign: {args.campaign}")
        print(f"Keyword: {args.keyword}")

        keyword = find_keyword(args.customer_id, args.campaign, args.keyword)

        if not keyword:
            print(f"❌ Keyword not found matching '{args.keyword}' in campaign '{args.campaign}'")
            return 1

        print(f"\nFound:")
        print(f"  Campaign: {keyword['campaign_name']}")
        print(f"  Ad Group: {keyword['ad_group_name']}")
        print(f"  Keyword: {keyword['keyword_text']} [{keyword['match_type']}]")
        print(f"  Current status: {keyword['current_status']}")
        print(f"  New status: {args.status}")
        print(f"\nUpdating...", end=" ")

        success, error = update_keyword_status_http(
            args.customer_id,
            keyword['ad_group_id'],
            keyword['criterion_id'],
            args.status
        )

        if success:
            print("✅ SUCCESS")
            return 0
        else:
            print(f"❌ FAILED\n{error}")
            return 1

    # Batch update from file
    elif args.file:
        with open(args.file, 'r') as f:
            updates = json.load(f)

        print(f"\nUpdating {len(updates)} keywords...\n")

        successful = 0
        failed = 0

        for update in updates:
            campaign_pattern = update.get('campaign_name') or update.get('campaign')
            keyword_text = update['keyword']
            new_status = update['status']

            keyword = find_keyword(args.customer_id, campaign_pattern, keyword_text)

            if not keyword:
                print(f"❌ Not found: {keyword_text} in {campaign_pattern}")
                failed += 1
                continue

            status_emoji = "⏸️ " if new_status == "PAUSED" else "▶️ "
            print(f"{status_emoji}{keyword['keyword_text'][:50]:<50} [{keyword['match_type']}] {keyword['current_status']:>10} → {new_status:<10}...", end=" ")

            success, error = update_keyword_status_http(
                args.customer_id,
                keyword['ad_group_id'],
                keyword['criterion_id'],
                new_status
            )

            if success:
                print("✅")
                successful += 1
            else:
                print("❌")
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
