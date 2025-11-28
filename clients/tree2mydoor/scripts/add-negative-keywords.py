#!/usr/bin/env python3
"""
Add negative keywords to Tree2MyDoor Search Campaign
Campaign ID: 598475433
Customer ID: 4941701449

Based on 120-day search term audit (2025-11-24)
"""

import os
import sys

# Add the MCP server path to use shared auth
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from dotenv import load_dotenv
load_dotenv('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env')

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
import requests
import json

# Configuration
CUSTOMER_ID = "4941701449"
CAMPAIGN_ID = "598475433"

# Negative keywords to add (exact match)
NEGATIVE_KEYWORDS = [
    "olive trees in pots",
    "lemon tree",
    "lemon trees for sale",
    "small olive tree in pot",
    "twisted olive tree",
    "bay trees for sale",
    "olive trees for sale uk",
    "the present tree olive tree",
]

def add_negative_keyword(customer_id: str, campaign_id: str, keyword_text: str, match_type: str = "EXACT"):
    """Add a single negative keyword to a campaign."""

    formatted_id = format_customer_id(customer_id)
    headers = get_headers_with_auto_token()

    url = f"https://googleads.googleapis.com/v19/customers/{formatted_id}/campaignCriteria:mutate"

    # Build the operation
    operation = {
        "operations": [{
            "create": {
                "campaign": f"customers/{formatted_id}/campaigns/{campaign_id}",
                "negative": True,
                "keyword": {
                    "text": keyword_text,
                    "matchType": match_type
                }
            }
        }]
    }

    response = requests.post(url, headers=headers, json=operation)

    if response.status_code == 200:
        result = response.json()
        return {"success": True, "keyword": keyword_text, "result": result}
    else:
        return {"success": False, "keyword": keyword_text, "error": response.text, "status": response.status_code}


def main():
    print(f"Adding {len(NEGATIVE_KEYWORDS)} negative keywords to campaign {CAMPAIGN_ID}")
    print(f"Customer ID: {CUSTOMER_ID}")
    print("-" * 50)

    results = []
    for keyword in NEGATIVE_KEYWORDS:
        print(f"Adding: [{keyword}]... ", end="")
        result = add_negative_keyword(CUSTOMER_ID, CAMPAIGN_ID, keyword)
        if result["success"]:
            print("OK")
        else:
            print(f"FAILED: {result.get('error', 'Unknown error')}")
        results.append(result)

    print("-" * 50)
    success_count = sum(1 for r in results if r["success"])
    print(f"Complete: {success_count}/{len(NEGATIVE_KEYWORDS)} keywords added successfully")

    # Print any failures
    failures = [r for r in results if not r["success"]]
    if failures:
        print("\nFailed keywords:")
        for f in failures:
            print(f"  - {f['keyword']}: {f.get('error', 'Unknown')}")

    return results


if __name__ == "__main__":
    main()
