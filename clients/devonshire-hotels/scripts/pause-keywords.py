#!/usr/bin/env python3
"""
Pause 16 wastage keywords identified in keyword analysis.
User approved on 2025-11-18.

This script pauses keywords via Google Ads API v22 using direct HTTP requests.
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Add MCP server oauth directory to path for authentication
mcp_oauth_path = Path(__file__).parent.parent.parent.parent / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server' / 'oauth'
sys.path.insert(0, str(mcp_oauth_path))

from google_auth import get_headers_with_auto_token, format_customer_id

# Customer ID
CUSTOMER_ID = "5898250490"

# All 16 keywords to pause (with criterion IDs and ad group IDs from GAQL queries)
KEYWORDS_TO_PAUSE = [
    {
        "ad_group_id": "166550831202",
        "criterion_id": "306651029886",
        "text": "luxurious cottage",
        "match_type": "BROAD",
        "campaign": "Chatsworth Escapes Self Catering",
        "ad_group": "Search - Peak District Cottages"
    },
    {
        "ad_group_id": "166550831202",
        "criterion_id": "10962031",
        "text": "peak district holiday cottages",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Self Catering",
        "ad_group": "Search - Peak District Cottages"
    },
    {
        "ad_group_id": "145260755676",
        "criterion_id": "1373505721161",
        "text": "chatsworth cottages dog friendly",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Self Catering",
        "ad_group": "Search - Chatsworth Self Catering"
    },
    {
        "ad_group_id": "145260755676",
        "criterion_id": "915155350989",
        "text": "chatsworth estate cottages to rent",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Self Catering",
        "ad_group": "Search - Chatsworth Self Catering"
    },
    {
        "ad_group_id": "145260755676",
        "criterion_id": "413933579267",
        "text": "chatsworth estate holiday cottages",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Self Catering",
        "ad_group": "Search - Chatsworth Estate Cottages"
    },
    {
        "ad_group_id": "170844309513",
        "criterion_id": "11704571560",
        "text": "bed and breakfast baslow",
        "match_type": "EXACT",
        "campaign": "Cavendish",
        "ad_group": "Search - Cavendish Hotel Baslow"
    },
    {
        "ad_group_id": "170844309513",
        "criterion_id": "98402665",
        "text": "country hotels uk",
        "match_type": "EXACT",
        "campaign": "Cavendish",
        "ad_group": "Search - Cavendish Hotel Baslow"
    },
    {
        "ad_group_id": "170844309513",
        "criterion_id": "2276232358722",
        "text": "cavendish house derbyshire",
        "match_type": "EXACT",
        "campaign": "Cavendish",
        "ad_group": "Search - Cavendish Hotel Baslow"
    },
    {
        "ad_group_id": "145493058603",
        "criterion_id": "304623178555",
        "text": "luxury hotels peak district",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Locations",
        "ad_group": "Search - Peak District Hotels"
    },
    {
        "ad_group_id": "145493058603",
        "criterion_id": "140059516",
        "text": "hotel peak district",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Locations",
        "ad_group": "Search - Peak District Hotels"
    },
    {
        "ad_group_id": "145493059123",
        "criterion_id": "315415980638",
        "text": "holidays in derbyshire peak district",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Locations",
        "ad_group": "Search - North Peak District Hotels"
    },
    {
        "ad_group_id": "145493059123",
        "criterion_id": "37326869740",
        "text": "peak district getaways",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Locations",
        "ad_group": "Search - North Peak District Hotels"
    },
    {
        "ad_group_id": "142451973337",
        "criterion_id": "303753752522",
        "text": "chatsworth pubs with rooms",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Inns & Hotels",
        "ad_group": "Search - Chatsworth Estate Pubs"
    },
    {
        "ad_group_id": "142451973337",
        "criterion_id": "13955850421",
        "text": "accommodation near chatsworth house",
        "match_type": "EXACT",
        "campaign": "Chatsworth Escapes Inns & Hotels",
        "ad_group": "Search - Chatsworth Estate Pubs"
    },
    {
        "ad_group_id": "180093078420",
        "criterion_id": "13880867634",
        "text": "hotels in beeley",
        "match_type": "EXACT",
        "campaign": "The Beeley Inn",
        "ad_group": "Search - Beeley Hotel"
    },
    {
        "ad_group_id": "147580845240",
        "criterion_id": "1631697467752",
        "text": "pilsley pubs",
        "match_type": "EXACT",
        "campaign": "The Pilsley Inn",
        "ad_group": "Search - Pilsley Hotels"
    }
]

def pause_keywords():
    """Pause all 16 identified wastage keywords."""

    print(f"\n{'='*80}")
    print(f"DEVONSHIRE HOTELS - KEYWORD PAUSE OPERATION")
    print(f"{'='*80}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Customer ID: {CUSTOMER_ID}")
    print(f"Keywords to pause: {len(KEYWORDS_TO_PAUSE)}")
    print(f"{'='*80}\n")

    # Get OAuth headers
    print("Getting OAuth credentials...")
    try:
        headers = get_headers_with_auto_token()
    except Exception as e:
        print(f"❌ Failed to get OAuth credentials: {e}")
        return False

    formatted_customer_id = format_customer_id(CUSTOMER_ID)

    # Build operations for each keyword
    operations = []
    for idx, kw in enumerate(KEYWORDS_TO_PAUSE, 1):
        resource_name = f"customers/{formatted_customer_id}/adGroupCriteria/{kw['ad_group_id']}~{kw['criterion_id']}"

        operations.append({
            'update': {
                'resourceName': resource_name,
                'status': 'PAUSED'
            },
            'updateMask': 'status'
        })

        print(f"{idx:2d}. {kw['text']:<45} [{kw['match_type']}]")
        print(f"    Campaign: {kw['campaign']}")
        print(f"    Ad Group: {kw['ad_group']}")
        print(f"    Resource: {resource_name}")
        print()

    # Execute pause operations
    print(f"\n{'='*80}")
    print("EXECUTING API REQUEST...")
    print(f"{'='*80}\n")

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/adGroupCriteria:mutate"
    payload = {
        'operations': operations,
        'partialFailure': True  # Allow partial success
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if not response.ok:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}\n")
            # Even with partial failure, we might get a 400 if all operations failed
            # Try to extract any useful info
            try:
                error_data = response.json()
                if 'error' in error_data:
                    print(f"Error details: {json.dumps(error_data['error'], indent=2)}\n")
            except:
                pass
            return False

        result = response.json()

        # Count successes and failures
        success_count = 0
        failure_count = 0

        # Check for partial failure status
        partial_failure = result.get('partialFailureError')
        if partial_failure:
            print(f"⚠️  PARTIAL SUCCESS - Some operations failed\n")

        # Log results
        results = []
        for idx, api_result in enumerate(result['results'], 1):
            kw = KEYWORDS_TO_PAUSE[idx - 1]

            # Check if this operation succeeded (has resourceName) or failed (empty/null)
            if 'resourceName' in api_result and api_result['resourceName']:
                success_count += 1
                result_data = {
                    "timestamp": datetime.now().isoformat(),
                    "action": "PAUSE",
                    "customer_id": CUSTOMER_ID,
                    "ad_group_id": kw['ad_group_id'],
                    "criterion_id": kw['criterion_id'],
                    "keyword_text": kw['text'],
                    "match_type": kw['match_type'],
                    "campaign": kw['campaign'],
                    "ad_group": kw['ad_group'],
                    "resource_name": api_result['resourceName'],
                    "status": "SUCCESS"
                }
                results.append(result_data)

                print(f"{idx:2d}. ✅ {kw['text']}")
                print(f"    Resource: {api_result['resourceName']}")
            else:
                failure_count += 1
                # This operation failed - extract error from partial failure
                error_msg = "Unknown error"
                if partial_failure:
                    try:
                        # Parse partial failure errors (they're in a specific format)
                        import re
                        pf_msg = partial_failure.get('message', '')
                        # Try to find relevant error for this operation
                        if 'negative' in pf_msg.lower():
                            error_msg = "Negative keyword (cannot pause, must remove)"
                        elif 'removed' in pf_msg.lower():
                            error_msg = "Ad group has been removed"
                        else:
                            error_msg = pf_msg[:100]
                    except:
                        error_msg = "Operation failed (see partial failure details)"

                result_data = {
                    "timestamp": datetime.now().isoformat(),
                    "action": "PAUSE",
                    "customer_id": CUSTOMER_ID,
                    "ad_group_id": kw['ad_group_id'],
                    "criterion_id": kw['criterion_id'],
                    "keyword_text": kw['text'],
                    "match_type": kw['match_type'],
                    "campaign": kw['campaign'],
                    "ad_group": kw['ad_group'],
                    "resource_name": "N/A",
                    "status": "FAILED",
                    "error": error_msg
                }
                results.append(result_data)

                print(f"{idx:2d}. ❌ {kw['text']}")
                print(f"    Error: {error_msg}")

        print(f"\n{'='*80}")
        print(f"SUMMARY: {success_count} succeeded, {failure_count} failed")
        print(f"{'='*80}\n")

        # Save API log
        log_file = Path(__file__).parent.parent / "api-changes-log.json"

        if log_file.exists():
            with open(log_file, 'r') as f:
                existing_log = json.load(f)
        else:
            existing_log = []

        existing_log.extend(results)

        with open(log_file, 'w') as f:
            json.dump(existing_log, f, indent=2)

        print(f"\n{'='*80}")
        print(f"✅ API CHANGES LOG UPDATED: {log_file}")
        print(f"{'='*80}\n")

        # Return success if at least some keywords were paused
        return success_count > 0

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")

        # Log error
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "action": "PAUSE_KEYWORDS",
            "customer_id": CUSTOMER_ID,
            "status": "FAILED",
            "error": str(e),
            "keywords_attempted": len(KEYWORDS_TO_PAUSE)
        }

        log_file = Path(__file__).parent.parent / "api-changes-log.json"

        if log_file.exists():
            with open(log_file, 'r') as f:
                existing_log = json.load(f)
        else:
            existing_log = []

        existing_log.append(error_data)

        with open(log_file, 'w') as f:
            json.dump(existing_log, f, indent=2)

        return False

if __name__ == "__main__":
    success = pause_keywords()
    sys.exit(0 if success else 1)
