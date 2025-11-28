#!/usr/bin/env python3
"""
Quick test script for Meta Ads OAuth authentication
"""

import sys
from oauth.meta_auth import get_oauth_credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("Meta Ads MCP Server - Authentication Test")
print("=" * 60)
print()
print("🚀 Starting OAuth flow...")
print("📱 Your browser should open automatically...")
print()

try:
    # Get OAuth token
    token = get_oauth_credentials()
    
    print()
    print("✅ SUCCESS! Authentication completed!")
    print(f"✅ Token obtained: {token[:30]}...")
    print()
    
    # Test API access by listing ad accounts
    print("Testing API access - fetching ad accounts...")
    
    import requests
    headers = {'Content-Type': 'application/json'}
    url = f"https://graph.facebook.com/v22.0/me/adaccounts"
    params = {
        'access_token': token,
        'fields': 'account_id,name,account_status'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.ok:
        data = response.json()
        accounts = data.get('data', [])
        
        print()
        print(f"✅ Found {len(accounts)} ad account(s)!")
        print()
        
        for account in accounts:
            print(f"  📊 {account.get('name', 'Unnamed')}")
            print(f"     ID: {account.get('account_id')}")
            print(f"     Status: {account.get('account_status')}")
            print()
        
        print("=" * 60)
        print("✅ Meta Ads MCP Server is ready to use!")
        print("=" * 60)
        
    else:
        print(f"⚠️  API call succeeded but returned: {response.status_code}")
        print(f"Response: {response.text}")
        
except KeyboardInterrupt:
    print()
    print("⚠️  Test cancelled by user")
    sys.exit(1)
    
except Exception as e:
    print()
    print(f"❌ Error: {e}")
    print()
    print("Check:")
    print("  1. Ad account is added to the app")
    print("  2. OAuth redirect URI is correct")
    print("  3. App has 'ads_read' permission")
    sys.exit(1)

