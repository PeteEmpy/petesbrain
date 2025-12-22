#!/usr/bin/env python3
"""
Get intuit_tid from QuickBooks API response headers

This script makes an API call and captures the intuit_tid header
that Intuit support needs for debugging 401 errors.
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from oauth.quickbooks_auth import get_headers_with_auto_token, get_realm_id
import requests


def get_intuit_tid():
    """Make API call and capture intuit_tid from response headers"""

    print("=" * 60)
    print("  QuickBooks API - Get intuit_tid Header")
    print("=" * 60)
    print()

    try:
        # Get authenticated headers
        print("⏳ Getting OAuth token...")
        headers = get_headers_with_auto_token()
        realm_id = get_realm_id()
        print(f"✓ Authenticated for Realm ID: {realm_id}")
        print()

        # Test API call - get company info
        url = f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/companyinfo/{realm_id}"

        print(f"⏳ Making API request to:")
        print(f"   {url}")
        print()

        # Make request
        response = requests.get(url, headers=headers)

        # Display status
        print(f"📊 Response Status: {response.status_code}")
        print()

        # Display all response headers
        print("📋 Response Headers:")
        print("-" * 60)
        for header_name, header_value in response.headers.items():
            print(f"   {header_name}: {header_value}")
        print("-" * 60)
        print()

        # Extract intuit_tid
        intuit_tid = response.headers.get('intuit_tid', 'NOT FOUND')

        print("🎯 Intuit Tracking ID (intuit_tid):")
        print("-" * 60)
        print(f"   {intuit_tid}")
        print("-" * 60)
        print()

        # Show response body (first 500 chars)
        print("📄 Response Body (first 500 chars):")
        print("-" * 60)
        response_text = response.text[:500]
        print(response_text)
        if len(response.text) > 500:
            print("... (truncated)")
        print("-" * 60)
        print()

        # Summary for Intuit support
        print("=" * 60)
        print("  COPY THIS TO INTUIT SUPPORT:")
        print("=" * 60)
        print()
        print(f"Status Code: {response.status_code}")
        print(f"intuit_tid: {intuit_tid}")
        print(f"Realm ID: {realm_id}")
        print(f"Endpoint: GET /v3/company/{realm_id}/companyinfo/{realm_id}")
        print()
        print("Full error response:")
        print(response.text)
        print()
        print("=" * 60)

        return intuit_tid

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    get_intuit_tid()
