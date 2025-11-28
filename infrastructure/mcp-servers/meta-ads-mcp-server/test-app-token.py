#!/usr/bin/env python3
"""
Test using App Access Token (App ID + Secret)
This sometimes works for Marketing API if the app has the use case enabled
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('META_APP_ID')
APP_SECRET = os.getenv('META_APP_SECRET')

print("=" * 60)
print("Testing App Access Token")
print("=" * 60)
print()

# Get app access token
app_token = f"{APP_ID}|{APP_SECRET}"
print(f"App Token: {app_token[:20]}...")
print()

# Try to access ad accounts using app token
print("Testing Marketing API access...")
url = "https://graph.facebook.com/v22.0/me/adaccounts"
params = {
    'access_token': app_token,
    'fields': 'account_id,name'
}

response = requests.get(url, params=params)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}...")
print()

if response.ok:
    print("✅ App token works! You can use it.")
else:
    print("❌ App token doesn't have access")
    print()
    print("Next step: We need to get a User Access Token")
    print("Since permissions aren't available yet, you may need to:")
    print("1. Request App Review for ads_read permission")
    print("2. Or wait for test user feature to be re-enabled")
    print("3. Or use the old facebook-ads-mcp-server with manual token")

