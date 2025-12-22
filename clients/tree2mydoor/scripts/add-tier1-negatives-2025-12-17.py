#!/usr/bin/env python3
"""
Add Tier 1 Negative Keywords - Tree2mydoor
Campaign 598475433 - 2 terms
"""

import sys
from pathlib import Path

# Add MCP server to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
import requests

API_VERSION = "v22"
CUSTOMER_ID = "4941701449"
MANAGER_ID = "2569949686"
CAMPAIGN_ID = "598475433"

KEYWORDS_TO_ADD = [
    "olive trees",
    "tree gifts uk"
]

def add_campaign_negative_keywords():
    """Add negative keywords to campaign"""
    try:
        formatted_customer_id = format_customer_id(CUSTOMER_ID)
        headers = get_headers_with_auto_token()
        headers['login-customer-id'] = format_customer_id(MANAGER_ID)

        campaign_resource = f"customers/{formatted_customer_id}/campaigns/{CAMPAIGN_ID}"
        operations = []

        for keyword_text in KEYWORDS_TO_ADD:
            operations.append({
                "create": {
                    "campaign": campaign_resource,
                    "negative": True,
                    "keyword": {
                        "text": keyword_text,
                        "matchType": "EXACT"
                    }
                }
            })

        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/campaignCriteria:mutate"
        payload = {"operations": operations}

        print(f"Adding {len(KEYWORDS_TO_ADD)} negative keywords to campaign {CAMPAIGN_ID}...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        results = result.get('results', [])

        print(f"✅ Successfully added {len(results)} negative keywords:")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [{KEYWORDS_TO_ADD[i-1]}] as EXACT negative")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = add_campaign_negative_keywords()
    sys.exit(0 if success else 1)
