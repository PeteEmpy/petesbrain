#!/usr/bin/env python3
"""Test accessing a specific account by number"""

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

# Account number from Crowd Control Company
ACCOUNT_NUMBER = "F10700TZU7"

print("Testing access to specific account...")
print(f"Account Number: {ACCOUNT_NUMBER}")
print(f"Customer ID: {CUSTOMER_ID}")
print("=" * 50)

try:
    # Set up auth
    authorization_data = AuthorizationData(
        account_id=None,  # We'll find this
        customer_id=CUSTOMER_ID,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    oauth = OAuthDesktopMobileAuthCodeGrant(client_id=CLIENT_ID)
    oauth.client_secret = CLIENT_SECRET
    oauth.refresh_token = REFRESH_TOKEN

    oauth_tokens = oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)
    authorization_data.authentication = oauth

    print("✓ Authenticated")
    print()

    # Use Customer Management to find the account ID from the account number
    print("Looking up account ID from account number...")
    customer_service = ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
    )

    # Try SearchAccounts with just paging (no predicates) to get ALL accounts
    paging = customer_service.factory.create('ns5:Paging')
    paging.Index = 0
    paging.Size = 100

    print(f"Searching for all accessible accounts under customer {CUSTOMER_ID}...")
    search_response = customer_service.SearchAccounts(
        Predicates=None,
        Ordering=None,
        PageInfo=paging
    )

    if search_response and hasattr(search_response, 'AdvertiserAccount'):
        accounts = search_response.AdvertiserAccount
        if accounts and len(accounts) > 0:
            print(f"✓ Found {len(accounts)} account(s):\n")
            for account in accounts:
                print(f"  Account ID: {account.Id}")
                print(f"  Account Number: {account.Number}")
                print(f"  Name: {account.Name}")
                print(f"  Customer ID: {account.ParentCustomerId}")
                print()

                # Now try to get campaigns for this account
                print(f"Fetching campaigns for account {account.Id}...")

                # Update authorization with this account ID
                authorization_data.account_id = account.Id

                campaign_service = ServiceClient(
                    service='CampaignManagementService',
                    version=13,
                    authorization_data=authorization_data,
                )

                campaigns_response = campaign_service.GetCampaignsByAccountId(
                    AccountId=account.Id,
                    CampaignType='Search Shopping DynamicSearchAds'
                )

                if campaigns_response and hasattr(campaigns_response, 'Campaign'):
                    campaigns = campaigns_response.Campaign
                    print(f"✓ Found {len(campaigns)} campaign(s):\n")
                    for campaign in campaigns:
                        print(f"    Campaign ID: {campaign.Id}")
                        print(f"    Name: {campaign.Name}")
                        print(f"    Status: {campaign.Status}")
                        print()
                else:
                    print("  No campaigns found or unexpected response")

        else:
            print("⚠ No accounts found matching that number")
    else:
        print("⚠ Unexpected response structure")
        print(f"Response: {search_response}")

    print("=" * 50)
    print("✅ TEST COMPLETE")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
