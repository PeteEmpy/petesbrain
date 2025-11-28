#!/usr/bin/env python3
"""Test connection to Microsoft Ads API using official Bing Ads SDK"""

from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData
from bingads.v13.customer_management import CustomerManagementService
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials
CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")

print("Testing Microsoft Ads API connection...")
print(f"Client ID: {CLIENT_ID[:10]}...")
print(f"Developer Token: {DEVELOPER_TOKEN}")
print()

try:
    # Set up OAuth authorization
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    # Create OAuth object with credentials
    oauth = OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirection_uri="http://localhost:8080"
    )

    # Set refresh token
    oauth.refresh_token = REFRESH_TOKEN

    # Request access token
    print("Requesting access token...")
    oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)
    print(f"✓ Access token obtained: {oauth.access_token[:20]}...")
    print()

    # Set authentication
    authorization_data.authentication = oauth

    # Create Customer Management service client
    print("Creating Customer Management service client...")
    customer_service = ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
    )
    print("✓ Service client created")
    print()

    # Get accounts
    print("Fetching accounts...")
    accounts_info = customer_service.GetAccountsInfo()

    if accounts_info and accounts_info.AccountInfo:
        print(f"✓ Successfully retrieved {len(accounts_info.AccountInfo)} account(s):\n")
        for account in accounts_info.AccountInfo:
            print(f"  Account ID: {account.Id}")
            print(f"  Name: {account.Name}")
            print(f"  Status: {account.AccountLifeCycleStatus}")
            print()
    else:
        print("⚠ No accounts found")

    print("✅ CONNECTION TEST SUCCESSFUL!")

except Exception as e:
    print(f"❌ CONNECTION TEST FAILED:")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
