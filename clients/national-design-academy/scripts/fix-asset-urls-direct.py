#!/usr/bin/env python3
"""
Direct asset group URL fix using MCP server auth
"""
import sys
import os
from pathlib import Path

# Add MCP server to path
mcp_path = Path(__file__).resolve().parent.parent.parent.parent / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
import requests

CUSTOMER_ID = "1994728449"

ASSET_GROUPS = [
    {"id": "6574590886", "name": "Remarketing UAE (newer)", "campaign": "UAE 175 no target 28/5"},
    {"id": "6553188869", "name": "Remarketing UAE (older)", "campaign": "UAE 175"},
    {"id": "6518747041", "name": "Interior Design Diploma", "campaign": "Australia/NZ"},
]

CORRECT_URL = "https://www.nda.ac.uk/study/courses/diploma-interior-design/"

def update_asset_group_url(asset_group_id: str) -> dict:
    """Update asset group final URL"""
    formatted_customer_id = format_customer_id(CUSTOMER_ID)
    headers = get_headers_with_auto_token()

    resource_name = f"customers/{formatted_customer_id}/assetGroups/{asset_group_id}"
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/assetGroups:mutate"

    payload = {
        "operations": [{
            "update": {
                "resourceName": resource_name,
                "finalUrls": [CORRECT_URL]
            },
            "updateMask": "finalUrls"
        }]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

print("=" * 80)
print("NDA ASSET GROUP URL FIX - DIRECT EXECUTION")
print("=" * 80)
print(f"\nCustomer ID: {CUSTOMER_ID}")
print(f"Correct URL: {CORRECT_URL}")
print(f"\nAsset groups to fix: {len(ASSET_GROUPS)}\n")

for ag in ASSET_GROUPS:
    print(f"- {ag['name']} (ID: {ag['id']})")

print("\n" + "=" * 80)
print("EXECUTING...")
print("=" * 80 + "\n")

results = []
for i, ag in enumerate(ASSET_GROUPS, 1):
    print(f"{i}/{len(ASSET_GROUPS)} Updating {ag['name']} (ID: {ag['id']})...")
    try:
        result = update_asset_group_url(ag['id'])
        print(f"   ✅ SUCCESS")
        results.append({"ag": ag, "success": True, "result": result})
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        results.append({"ag": ag, "success": False, "error": str(e)})

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

successful = sum(1 for r in results if r['success'])
failed = sum(1 for r in results if not r['success'])

print(f"\n✅ Successful: {successful}/{len(ASSET_GROUPS)}")
print(f"❌ Failed: {failed}/{len(ASSET_GROUPS)}")

if successful == len(ASSET_GROUPS):
    print("\n✅ ALL ASSET GROUP URLs FIXED")
    print(f"\nDiploma campaigns now correctly send to:")
    print(f"  {CORRECT_URL}")
else:
    print("\n⚠️  SOME UPDATES FAILED")
    for r in results:
        if not r['success']:
            print(f"  - {r['ag']['name']}: {r['error']}")

print("=" * 80 + "\n")
