#!/usr/bin/env python3
"""
Simple test to verify Tree2MyDoor account access
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

# Try different account ID formats
ACCOUNT_IDS_TO_TRY = ["X1658737", "1658737", "01658737"]

print("🔍 Testing Tree2MyDoor account access...\n")

for account_id in ACCOUNT_IDS_TO_TRY:
    print(f"Trying Account ID: {account_id}")
    print("-" * 50)

    try:
        # Set up OAuth
        oauth = OAuthDesktopMobileAuthCodeGrant(client_id=CLIENT_ID)
        oauth.client_secret = CLIENT_SECRET
        oauth.refresh_token = REFRESH_TOKEN
        oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)

        # Create authorization data with just account ID
        authorization_data = AuthorizationData(
            account_id=account_id,
            customer_id=None,
            developer_token=DEVELOPER_TOKEN,
            authentication=oauth,
        )

        # Try to fetch campaigns
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        campaigns_response = campaign_service.GetCampaignsByAccountId(
            AccountId=account_id,
            CampaignType='Search Shopping DynamicSearchAds'
        )

        if campaigns_response and hasattr(campaigns_response, 'Campaign'):
            print(f"✅ SUCCESS with Account ID: {account_id}")
            print(f"   Found {len(campaigns_response.Campaign)} campaigns:")
            for campaign in campaigns_response.Campaign:
                print(f"   • {campaign.Name} (ID: {campaign.Id}, Status: {campaign.Status})")
            print()
            break
        else:
            print(f"⚠️  No campaigns found with this ID\n")

    except Exception as e:
        error_msg = str(e)
        if "Invalid client data" in error_msg:
            print(f"❌ Invalid client data - account ID format may be wrong\n")
        elif "not authorized" in error_msg.lower():
            print(f"❌ Not authorized for this account\n")
        else:
            print(f"❌ Error: {error_msg}\n")

print("=" * 50)
print("If all attempts failed, the account might need to be added")
print("to your Microsoft Ads access list, or the ID format is different.")
