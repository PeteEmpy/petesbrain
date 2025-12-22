#!/usr/bin/env python3
"""
Simple script to list Microsoft Ads accounts under MCC
"""
import os
from dotenv import load_dotenv
load_dotenv()

from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData

# Get credentials
CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")
CUSTOMER_ID = os.environ.get("MICROSOFT_ADS_CUSTOMER_ID")

# Set up OAuth
oauth = OAuthDesktopMobileAuthCodeGrant(client_id=CLIENT_ID)
oauth.client_secret = CLIENT_SECRET
oauth.refresh_token = REFRESH_TOKEN

# Request access token
oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)

# Create authorization data
authorization_data = AuthorizationData(
    developer_token=DEVELOPER_TOKEN,
    authentication=oauth,
    customer_id=CUSTOMER_ID
)

# Create Customer Management service
customer_service = ServiceClient(
    service='CustomerManagementService',
    version=13,
    authorization_data=authorization_data,
)

print(f"🔍 Searching for accounts under Customer ID: {CUSTOMER_ID}\n")

try:
    # Get accounts info
    accounts = customer_service.GetAccountsInfo()

    if accounts and hasattr(accounts, 'AccountInfo'):
        print(f"✅ Found {len(accounts.AccountInfo)} account(s):\n")

        for i, account in enumerate(accounts.AccountInfo, 1):
            print(f"{i}. {account.Name}")
            print(f"   Account ID: {account.Id}")
            print(f"   Number: {account.Number}")
            print(f"   Status: {account.AccountLifeCycleStatus}")
            print()
    else:
        print("⚠️  No accounts found")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
