#!/usr/bin/env python3
"""Test with actual numeric Account ID"""

from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")
CUSTOMER_ID = os.environ.get("MICROSOFT_ADS_CUSTOMER_ID")

# Real numeric Account ID from URL
ACCOUNT_ID = 1673847

print("Testing with real Account ID from URL...")
print(f"Account ID: {ACCOUNT_ID}")
print(f"Customer ID: {CUSTOMER_ID}")
print("=" * 50)

try:
    # Set up auth
    authorization_data = AuthorizationData(
        account_id=ACCOUNT_ID,
        customer_id=CUSTOMER_ID,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    oauth = OAuthDesktopMobileAuthCodeGrant(client_id=CLIENT_ID)
    oauth.client_secret = CLIENT_SECRET
    oauth.refresh_token = REFRESH_TOKEN

    oauth_tokens = oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)
    authorization_data.authentication = oauth

    print("✓ Authenticated with Account ID")
    print()

    # Try Campaign Management service to get campaigns
    print("Fetching campaigns for this account...")
    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
    )

    campaigns_response = campaign_service.GetCampaignsByAccountId(
        AccountId=ACCOUNT_ID,
        CampaignType='Search Shopping DynamicSearchAds'
    )

    if campaigns_response and hasattr(campaigns_response, 'Campaign'):
        campaigns = campaigns_response.Campaign
        print(f"✓ Successfully retrieved {len(campaigns)} campaign(s):\n")
        for campaign in campaigns:
            print(f"  Campaign ID: {campaign.Id}")
            print(f"  Name: {campaign.Name}")
            print(f"  Status: {campaign.Status}")
            print(f"  Budget: {campaign.BudgetType if hasattr(campaign, 'BudgetType') else 'N/A'}")
            print()
    else:
        print("⚠ No campaigns found or unexpected response")
        print(f"Response: {campaigns_response}")

    print("=" * 50)
    print("✅ CAMPAIGN ACCESS SUCCESSFUL!")
    print("\nNow let's try to list ALL accounts accessible to this user...")
    print()

    # Now that we know one account works, try to get all accounts
    # Use Customer Management with the user's customer context
    customer_service = ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
    )

    # Get user's customers
    print("Getting user's customers...")
    user_response = customer_service.GetUser(UserId=1741434)

    print(f"User: {user_response.User.Name}")
    print(f"User Role: {user_response.User.UserLifeCycleStatus}")

    # Get accounts the user can access
    print("\nGetting all accessible accounts...")

    # Try GetAccountsInfo without CustomerID parameter
    accounts_response = customer_service.GetAccountsInfo()

    if accounts_response and hasattr(accounts_response, 'AccountsInfo'):
        account_info_array = accounts_response.AccountsInfo
        if account_info_array and hasattr(account_info_array, 'AccountInfo'):
            accounts = account_info_array.AccountInfo
            print(f"✓ Found {len(accounts)} total account(s):\n")
            for account in accounts:
                print(f"  Account ID: {account.Id}")
                print(f"  Name: {account.Name}")
                print(f"  Number: {account.Number}")
                print()
        else:
            print("⚠ No accounts in AccountsInfo")
    else:
        print("⚠ GetAccountsInfo returned empty or unexpected response")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
