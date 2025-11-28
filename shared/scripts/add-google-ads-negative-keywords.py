#!/usr/bin/env python3
"""
Simple Google Ads Negative Keyword Adder
Usage: python3 add-google-ads-negative-keywords.py --customer-id XXXXX --campaign "Campaign Name" --keywords "keyword1,keyword2,keyword3"
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


def get_campaign_by_name(customer_id: str, campaign_name_pattern: str):
    """Find campaign by name pattern."""
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    query = f'''
        SELECT campaign.id, campaign.name
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
        'campaign_name': row.campaign.name
    }


def add_negative_keyword_http(customer_id: str, campaign_id: str, keyword_text: str, match_type: str = "EXACT"):
    """Add a negative keyword to a campaign using HTTP API."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = MANAGER_ID

    formatted_customer_id = customer_id.replace("-", "")

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/campaignCriteria:mutate"

    payload = {
        'operations': [{
            'create': {
                'campaign': f"customers/{formatted_customer_id}/campaigns/{campaign_id}",
                'negative': True,
                'keyword': {
                    'text': keyword_text,
                    'matchType': match_type
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
    parser = argparse.ArgumentParser(
        description='Add negative keywords to Google Ads campaigns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Add single keyword
  python3 add-google-ads-negative-keywords.py --customer-id 8573235780 --campaign "Brand Exact" --keywords "cheap,free"

  # Add multiple keywords with specific match type
  python3 add-google-ads-negative-keywords.py --customer-id 8573235780 --campaign "Brand" --keywords "discount,sale" --match-type PHRASE

  # Batch add from JSON file
  python3 add-google-ads-negative-keywords.py --customer-id 8573235780 --file keywords.json

JSON Format:
[
  {
    "campaign": "Brand Exact",
    "keywords": ["cheap", "free", "discount"],
    "match_type": "EXACT"
  }
]
"""
    )

    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--campaign', help='Campaign name (or partial match)')
    parser.add_argument('--keywords', help='Comma-separated keywords to add as negatives')
    parser.add_argument('--match-type', choices=['EXACT', 'PHRASE', 'BROAD'], default='EXACT', help='Match type (default: EXACT)')
    parser.add_argument('--file', help='JSON file with batch keywords')

    args = parser.parse_args()

    # Single campaign operation
    if args.campaign and args.keywords:
        print(f"\nFinding campaign: {args.campaign}")

        campaign = get_campaign_by_name(args.customer_id, args.campaign)

        if not campaign:
            print(f"❌ Campaign not found matching '{args.campaign}'")
            return 1

        print(f"Found: {campaign['campaign_name']}")

        keywords = [k.strip() for k in args.keywords.split(',')]
        print(f"Adding {len(keywords)} negative keywords ({args.match_type} match)\n")

        successful = 0
        failed = 0

        for keyword in keywords:
            print(f"Adding [{keyword}]...", end=" ")
            success, error = add_negative_keyword_http(
                args.customer_id,
                campaign['campaign_id'],
                keyword,
                args.match_type
            )

            if success:
                print("✅")
                successful += 1
            else:
                print(f"❌ {error}")
                failed += 1

        print(f"\n✅ {successful}/{len(keywords)} keywords added successfully")
        if failed > 0:
            print(f"❌ {failed}/{len(keywords)} failed")

        return 0 if failed == 0 else 1

    # Batch operation from file
    elif args.file:
        with open(args.file, 'r') as f:
            batches = json.load(f)

        total_successful = 0
        total_failed = 0

        for batch in batches:
            campaign_pattern = batch.get('campaign_name') or batch.get('campaign')
            keywords = batch['keywords']
            match_type = batch.get('match_type', 'EXACT')

            print(f"\nCampaign: {campaign_pattern}")

            campaign = get_campaign_by_name(args.customer_id, campaign_pattern)

            if not campaign:
                print(f"❌ Not found: {campaign_pattern}")
                total_failed += len(keywords)
                continue

            print(f"Found: {campaign['campaign_name']}")
            print(f"Adding {len(keywords)} keywords ({match_type} match)")

            for keyword in keywords:
                print(f"  [{keyword}]...", end=" ")
                success, error = add_negative_keyword_http(
                    args.customer_id,
                    campaign['campaign_id'],
                    keyword,
                    match_type
                )

                if success:
                    print("✅")
                    total_successful += 1
                else:
                    print(f"❌")
                    total_failed += 1

        print(f"\n✅ {total_successful} keywords added successfully")
        if total_failed > 0:
            print(f"❌ {total_failed} failed")

        return 0 if total_failed == 0 else 1

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
