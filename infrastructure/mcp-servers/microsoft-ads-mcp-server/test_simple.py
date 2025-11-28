#!/usr/bin/env python3
"""Simple test to check actual accounts by ID"""

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

print("Simple API Test")
print("=" * 50)

try:
    # Set up auth
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=CUSTOMER_ID,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    oauth = OAuthDesktopMobileAuthCodeGrant(client_id=CLIENT_ID)
    oauth.client_secret = CLIENT_SECRET
    oauth.refresh_token = REFRESH_TOKEN

    oauth_tokens = oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)
    authorization_data.authentication = oauth

    print(f"✓ Authenticated as customer: {CUSTOMER_ID}")
    print()

    # Try Campaign Management service to get campaigns
    # This requires an account ID, so let's try one from your screenshot
    # Let's try using Campaign Management to list accounts we have access to

    print("Trying Reporting Service to list accessible accounts...")
    reporting_service = ServiceClient(
        service='ReportingService',
        version=13,
        authorization_data=authorization_data,
    )

    # Try to get account performance report request
    # This would show which accounts we can access
    report_request = reporting_service.factory.create('AccountPerformanceReportRequest')
    print(f"✓ Created report request object")
    print(f"  Available report columns: {dir(report_request)}")

    print("\n" + "=" * 50)
    print("✅ Basic SDK operations work!")
    print("The issue is likely with Customer Management service specifically.")
    print("\nNext step: Try accessing a specific account directly")
    print("Please provide an Account ID from one of your accounts.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
