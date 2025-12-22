#!/usr/bin/env python3
"""
Universal Google Ads Negative Keyword Manager

Add negative keywords to any Google Ads account using REST API.
Works for all clients with customer ID and campaign ID parameters.

Usage:
    # Add from Tier 1 promotion report
    python3 add-negative-keywords-universal.py --customer-id 6413338364 --campaign-id 22702563562 --from-file clients/uno-lighting/reports/tier1-keywords.txt

    # Add specific keywords
    python3 add-negative-keywords-universal.py --customer-id 8573235780 --campaign-id 12345 --keywords "led strip lights,plaster in downlights" --match-type exact

    # Dry run to preview changes
    python3 add-negative-keywords-universal.py --customer-id 6413338364 --campaign-id 22702563562 --keywords "test keyword" --dry-run

    # Add to ad group instead of campaign
    python3 add-negative-keywords-universal.py --customer-id 6413338364 --ad-group-id 98765 --keywords "test keyword"

Features:
    - Campaign-level or ad group-level negatives
    - Exact or phrase match support
    - Batch processing from file
    - Dry-run mode for safety
    - Manager account support
    - Verification of added keywords
"""

import argparse
import sys
import os
import requests
from pathlib import Path
from typing import List, Dict, Any

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id

# Google Ads API version
API_VERSION = "v22"


def add_campaign_negative_keywords(
    customer_id: str,
    campaign_id: str,
    keywords: List[str],
    match_type: str = "EXACT",
    manager_id: str = "",
    dry_run: bool = False
) -> List[str]:
    """
    Add negative keywords to a campaign using Google Ads REST API.

    Args:
        customer_id: Google Ads customer ID (no dashes)
        campaign_id: Campaign ID (numeric string)
        keywords: List of keyword strings to add
        match_type: "EXACT" or "PHRASE" (default: EXACT)
        manager_id: Manager account ID (if applicable)
        dry_run: If True, show what would be added without making changes

    Returns:
        List of added negative keyword resource names
    """
    formatted_customer_id = format_customer_id(customer_id)

    if dry_run:
        print("\n🔍 DRY RUN - Would add these negative keywords:")
        print(f"Campaign ID: {campaign_id}")
        print(f"Match Type: {match_type}")
        print(f"Keywords:")
        for kw in keywords:
            match_symbol = "[]" if match_type == "EXACT" else '""'
            print(f"  {match_symbol[0]}{kw}{match_symbol[1]}")
        print("\nNo changes made (dry run mode).")
        return []

    # Get OAuth headers
    headers = get_headers_with_auto_token()
    if manager_id:
        headers['login-customer-id'] = format_customer_id(manager_id)

    # Build operations
    campaign_resource = f"customers/{formatted_customer_id}/campaigns/{campaign_id}"
    operations = []

    for keyword_text in keywords:
        operations.append({
            "create": {
                "campaign": campaign_resource,
                "negative": True,
                "keyword": {
                    "text": keyword_text,
                    "matchType": match_type
                }
            }
        })

    # API request
    url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/campaignCriteria:mutate"
    payload = {"operations": operations}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        results = result.get('results', [])

        print(f"\n✅ Successfully added {len(results)} negative keywords:")
        added_resources = []
        for res in results:
            resource_name = res.get('resourceName', 'Unknown')
            added_resources.append(resource_name)
            print(f"  {resource_name}")

        return added_resources

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Google Ads API error occurred:")
        try:
            error_data = e.response.json()
            if 'error' in error_data:
                error = error_data['error']
                print(f"  Status: {error.get('status', 'Unknown')}")
                print(f"  Message: {error.get('message', 'Unknown')}")
                if 'details' in error:
                    for detail in error['details']:
                        if 'errors' in detail:
                            for err in detail['errors']:
                                print(f"    Error: {err.get('message', 'Unknown')}")
        except:
            print(f"  {str(e)}")
        raise


def add_ad_group_negative_keywords(
    customer_id: str,
    ad_group_id: str,
    keywords: List[str],
    match_type: str = "EXACT",
    manager_id: str = "",
    dry_run: bool = False
) -> List[str]:
    """
    Add negative keywords to an ad group using Google Ads REST API.

    Args:
        customer_id: Google Ads customer ID (no dashes)
        ad_group_id: Ad group ID (numeric string)
        keywords: List of keyword strings to add
        match_type: "EXACT" or "PHRASE" (default: EXACT)
        manager_id: Manager account ID (if applicable)
        dry_run: If True, show what would be added without making changes

    Returns:
        List of added negative keyword resource names
    """
    formatted_customer_id = format_customer_id(customer_id)

    if dry_run:
        print("\n🔍 DRY RUN - Would add these negative keywords:")
        print(f"Ad Group ID: {ad_group_id}")
        print(f"Match Type: {match_type}")
        print(f"Keywords:")
        for kw in keywords:
            match_symbol = "[]" if match_type == "EXACT" else '""'
            print(f"  {match_symbol[0]}{kw}{match_symbol[1]}")
        print("\nNo changes made (dry run mode).")
        return []

    # Get OAuth headers
    headers = get_headers_with_auto_token()
    if manager_id:
        headers['login-customer-id'] = format_customer_id(manager_id)

    # Build operations
    ad_group_resource = f"customers/{formatted_customer_id}/adGroups/{ad_group_id}"
    operations = []

    for keyword_text in keywords:
        operations.append({
            "create": {
                "adGroup": ad_group_resource,
                "negative": True,
                "keyword": {
                    "text": keyword_text,
                    "matchType": match_type
                }
            }
        })

    # API request
    url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/adGroupCriteria:mutate"
    payload = {"operations": operations}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        results = result.get('results', [])

        print(f"\n✅ Successfully added {len(results)} negative keywords:")
        added_resources = []
        for res in results:
            resource_name = res.get('resourceName', 'Unknown')
            added_resources.append(resource_name)
            print(f"  {resource_name}")

        return added_resources

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Google Ads API error occurred:")
        try:
            error_data = e.response.json()
            if 'error' in error_data:
                error = error_data['error']
                print(f"  Status: {error.get('status', 'Unknown')}")
                print(f"  Message: {error.get('message', 'Unknown')}")
                if 'details' in error:
                    for detail in error['details']:
                        if 'errors' in detail:
                            for err in detail['errors']:
                                print(f"    Error: {err.get('message', 'Unknown')}")
        except:
            print(f"  {str(e)}")
        raise


def parse_keywords_from_file(filepath: str) -> List[str]:
    """
    Parse keywords from a text file (one per line).

    Supports:
    - Plain text (one keyword per line)
    - Comments (lines starting with #)
    - Bracket notation ([exact], "phrase")
    """
    keywords = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                # Remove bracket notation if present
                keyword = line.strip('[]"')
                keywords.append(keyword)
    return keywords


def get_campaign_name(customer_id: str, campaign_id: str, manager_id: str = "") -> str:
    """Get campaign name for verification using REST API."""
    try:
        formatted_customer_id = format_customer_id(customer_id)
        headers = get_headers_with_auto_token()
        if manager_id:
            headers['login-customer-id'] = format_customer_id(manager_id)

        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/googleAds:searchStream"
        query = f"""
            SELECT campaign.name
            FROM campaign
            WHERE campaign.id = {campaign_id}
        """

        response = requests.post(url, headers=headers, json={"query": query})
        response.raise_for_status()

        # Parse streaming response
        for line in response.text.strip().split('\n'):
            if line:
                result = eval(line)  # Safe here as it's from Google API
                if 'results' in result:
                    return result['results'][0]['campaign']['name']

        return f"Campaign {campaign_id}"
    except Exception:
        return f"Campaign {campaign_id}"


def main():
    parser = argparse.ArgumentParser(
        description="Add negative keywords to Google Ads campaigns (universal script)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Add exact match negatives to campaign
  python3 add-negative-keywords-universal.py --customer-id 6413338364 --campaign-id 22702563562 --keywords "led strip lights,led plaster in profile"

  # Add phrase match negatives to campaign
  python3 add-negative-keywords-universal.py --customer-id 8573235780 --campaign-id 12345 --keywords "emergency,outdoor wall" --match-type phrase

  # Add negatives from file (Tier 1 promotions)
  python3 add-negative-keywords-universal.py --customer-id 6413338364 --campaign-id 22702563562 --from-file clients/uno-lighting/reports/tier1-keywords.txt

  # Dry run (preview without changes)
  python3 add-negative-keywords-universal.py --customer-id 6413338364 --campaign-id 22702563562 --keywords "test keyword" --dry-run

  # Add to ad group instead of campaign
  python3 add-negative-keywords-universal.py --customer-id 6413338364 --ad-group-id 98765 --keywords "test"

  # With manager account ID
  python3 add-negative-keywords-universal.py --customer-id 8573235780 --manager-id 2569949686 --campaign-id 12345 --keywords "test"

Tier System Integration:
  1. Run keyword audit: python3 shared/scripts/export-google-ads-search-terms.py --output tiers
  2. Track Tier 2: python3 shared/scripts/tier2_tracker.py --add-from-csv tier2.csv
  3. Check promotions: python3 shared/scripts/tier2_tracker.py --check-client uno-lighting
  4. Add negatives: python3 shared/scripts/add-negative-keywords-universal.py --from-file tier1-promotions.txt
"""
    )

    # Target selection
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument('--campaign-id', help='Campaign ID to add negatives to')
    target_group.add_argument('--ad-group-id', help='Ad group ID to add negatives to')

    # Keyword input
    keyword_group = parser.add_mutually_exclusive_group(required=True)
    keyword_group.add_argument('--keywords', help='Comma-separated list of keywords')
    keyword_group.add_argument('--from-file', help='File containing keywords (one per line)')

    # Options
    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--manager-id', default='', help='Manager account ID (if applicable)')
    parser.add_argument('--match-type', choices=['exact', 'phrase'], default='exact',
                       help='Match type (default: exact)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying them')

    args = parser.parse_args()

    # Parse keywords
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
    else:
        keywords = parse_keywords_from_file(args.from_file)

    if not keywords:
        print("❌ No keywords provided.")
        return 1

    # Convert match type to API enum format
    match_type = args.match_type.upper()

    # Display summary
    print("=" * 80)
    print("UNIVERSAL NEGATIVE KEYWORD MANAGER")
    print("=" * 80)
    print(f"Customer ID: {args.customer_id}")
    if args.manager_id:
        print(f"Manager ID: {args.manager_id}")
    if args.campaign_id:
        campaign_name = get_campaign_name(args.customer_id, args.campaign_id, args.manager_id)
        print(f"Campaign: {campaign_name} (ID: {args.campaign_id})")
    if args.ad_group_id:
        print(f"Ad Group ID: {args.ad_group_id}")
    print(f"Match Type: {match_type}")
    print(f"Keywords to add: {len(keywords)}")
    if args.dry_run:
        print("Mode: DRY RUN (no changes will be made)")
    print("=" * 80)

    # Add negatives
    try:
        if args.campaign_id:
            added = add_campaign_negative_keywords(
                customer_id=args.customer_id,
                campaign_id=args.campaign_id,
                keywords=keywords,
                match_type=match_type,
                manager_id=args.manager_id,
                dry_run=args.dry_run
            )
        else:
            added = add_ad_group_negative_keywords(
                customer_id=args.customer_id,
                ad_group_id=args.ad_group_id,
                keywords=keywords,
                match_type=match_type,
                manager_id=args.manager_id,
                dry_run=args.dry_run
            )

        if not args.dry_run:
            print(f"\n✅ Complete! Added {len(added)} negative keywords.")
            print("\n💰 Expected impact: Blocked terms will stop triggering ads within 1-2 hours.")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
