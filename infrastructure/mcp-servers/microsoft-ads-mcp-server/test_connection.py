#!/usr/bin/env python3
"""Test connection to Microsoft Ads API using official Bing Ads SDK"""

from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials
CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")
CUSTOMER_ID = os.environ.get("MICROSOFT_ADS_CUSTOMER_ID")

print("Testing Microsoft Ads API connection...")
print(f"Client ID: {CLIENT_ID[:10]}...")
print(f"Developer Token: {DEVELOPER_TOKEN}")
print(f"Customer ID: {CUSTOMER_ID}")
print()

try:
    # Set up OAuth authorization with Customer ID
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=CUSTOMER_ID,  # Manager/MCC Customer ID
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    # Create OAuth object with credentials
    oauth = OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID
    )

    # Set client secret and refresh token as properties
    oauth.client_secret = CLIENT_SECRET
    oauth.refresh_token = REFRESH_TOKEN

    # Request access token
    print("Requesting access token...")
    oauth_tokens = oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)
    print(f"✓ Access token obtained: {oauth_tokens.access_token[:20]}...")
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

    # Get user information first
    print("Fetching user information...")
    user_response = customer_service.GetUser()
    print(f"✓ User ID: {user_response.User.Id}")
    print(f"  User Name: {user_response.User.Name}")
    print()

    # Try using SearchAccounts which works better for manager accounts
    print("Searching for accessible accounts...")

    try:
        # SearchAccounts with no predicates returns all accessible accounts
        search_response = customer_service.SearchAccounts()

        if search_response and hasattr(search_response, 'AdvertiserAccount'):
            accounts = search_response.AdvertiserAccount
            print(f"✓ Successfully retrieved {len(accounts)} account(s):\n")

            for account in accounts:
                print(f"  Account ID: {account.Id}")
                print(f"  Name: {account.Name}")
                print(f"  Number: {account.Number}")
                if hasattr(account, 'AccountLifeCycleStatus'):
                    print(f"  Status: {account.AccountLifeCycleStatus}")
                print()
        else:
            print(f"⚠ Unexpected response structure")
            print(f"Response: {search_response}")

    except Exception as e:
        print(f"⚠ SearchAccounts failed: {e}")
        print("\nLet me check the exact SOAP fault details...")
        import traceback
        traceback.print_exc()

    print("✅ CONNECTION TEST SUCCESSFUL!")

except Exception as e:
    print(f"❌ CONNECTION TEST FAILED:")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
