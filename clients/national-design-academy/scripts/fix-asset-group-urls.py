#!/usr/bin/env python3
"""
Fix Asset Group URLs - NDA Landing Page Issue
Corrects 3 Diploma asset groups sending traffic to Degree page.

Issue: Diploma campaigns accidentally using /courses/degrees-interior-design/
Fix: Change to correct diploma page /courses/diploma-interior-design/

Run with: python3 fix-asset-group-urls.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for shared imports
parent_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(parent_dir / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
import requests

# NDA Customer ID
CUSTOMER_ID = "1994728449"

# Asset groups to fix
ASSET_GROUPS_TO_FIX = [
    {
        "asset_group_id": "6574590886",
        "campaign_name": "NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5",
        "asset_group_name": "Remarketing UAE",
        "description": "UAE Diploma - Remarketing (newer campaign)"
    },
    {
        "asset_group_id": "6553188869",
        "campaign_name": "NDA | P Max | Interior Design Diploma - UAE 175",
        "asset_group_name": "Remarketing UAE",
        "description": "UAE Diploma - Remarketing (older campaign)"
    },
    {
        "asset_group_id": "6518747041",
        "campaign_name": "NDA | P Max | Interior Design - Australia/New Zealand",
        "asset_group_name": "Interior Design Diploma",
        "description": "Australia/NZ Diploma"
    }
]

# URLs
WRONG_URL = "https://www.nda.ac.uk/study/courses/degrees-interior-design/"
CORRECT_URL = "https://www.nda.ac.uk/study/courses/diploma-interior-design/"

def update_asset_group_url(customer_id: str, asset_group_id: str, new_url: str) -> dict:
    """
    Update the finalUrls for an asset group.

    Args:
        customer_id: Google Ads customer ID
        asset_group_id: Asset group ID to update
        new_url: New landing page URL

    Returns:
        Response from API
    """
    formatted_customer_id = format_customer_id(customer_id)
    headers = get_headers_with_auto_token()

    asset_group_resource_name = f"customers/{formatted_customer_id}/assetGroups/{asset_group_id}"

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/assetGroups:mutate"

    payload = {
        "operations": [{
            "update": {
                "resourceName": asset_group_resource_name,
                "finalUrls": [new_url]
            },
            "updateMask": "finalUrls"
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if not response.ok:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    return response.json()

def main():
    """Fix all 3 asset group URLs."""
    print("=" * 80)
    print("NDA ASSET GROUP URL FIX")
    print("=" * 80)
    print(f"\nCustomer ID: {CUSTOMER_ID}")
    print(f"Wrong URL: {WRONG_URL}")
    print(f"Correct URL: {CORRECT_URL}")
    print(f"\nAsset groups to fix: {len(ASSET_GROUPS_TO_FIX)}")
    print("=" * 80)

    # Show what will be updated
    print("\nREVIEW BEFORE PROCEEDING:")
    for i, ag in enumerate(ASSET_GROUPS_TO_FIX, 1):
        print(f"\n{i}. {ag['description']}")
        print(f"   Campaign: {ag['campaign_name']}")
        print(f"   Asset Group: {ag['asset_group_name']}")
        print(f"   Asset Group ID: {ag['asset_group_id']}")

    # Confirm before proceeding
    print("\n" + "=" * 80)
    response = input("Proceed with URL updates? (yes/no): ").strip().lower()

    if response != 'yes':
        print("\n❌ Cancelled. No changes made.")
        return

    print("\n" + "=" * 80)
    print("UPDATING ASSET GROUPS...")
    print("=" * 80)

    results = []

    for i, ag in enumerate(ASSET_GROUPS_TO_FIX, 1):
        print(f"\n{i}/{len(ASSET_GROUPS_TO_FIX)} Updating {ag['description']}...")
        print(f"   Asset Group ID: {ag['asset_group_id']}")

        try:
            result = update_asset_group_url(
                customer_id=CUSTOMER_ID,
                asset_group_id=ag['asset_group_id'],
                new_url=CORRECT_URL
            )
            print(f"   ✅ SUCCESS - URL updated to diploma page")
            results.append({
                'asset_group': ag,
                'success': True,
                'result': result
            })
        except Exception as e:
            print(f"   ❌ FAILED - {str(e)}")
            results.append({
                'asset_group': ag,
                'success': False,
                'error': str(e)
            })

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    successful = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])

    print(f"\n✅ Successful: {successful}/{len(ASSET_GROUPS_TO_FIX)}")
    print(f"❌ Failed: {failed}/{len(ASSET_GROUPS_TO_FIX)}")

    if failed > 0:
        print("\nFailed asset groups:")
        for r in results:
            if not r['success']:
                print(f"  - {r['asset_group']['description']}: {r['error']}")

    print("\n" + "=" * 80)

    if successful == len(ASSET_GROUPS_TO_FIX):
        print("✅ ALL ASSET GROUP URLs FIXED")
        print("\nDiploma campaigns now correctly send to:")
        print(f"  {CORRECT_URL}")
    else:
        print("⚠️  SOME UPDATES FAILED - Review errors above")

    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
