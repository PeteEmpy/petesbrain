#!/usr/bin/env python3
"""Test accessing child customer directly"""

from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")

# Try using the child customer ID instead
# Remove the 'F' prefix and '0' padding - convert F10700TZU7 to numeric
# Actually, let's try the raw value first
CHILD_CUSTOMER_ID = "10700"  # Trying just the numeric part

print("Testing with child customer ID...")
print(f"Customer ID: {CHILD_CUSTOMER_ID}")
print("=" * 50)

try:
    # Set up auth with child customer
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=CHILD_CUSTOMER_ID,
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

    customer_service = ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
    )

    # Try GetAccountsInfo for this customer
    print(f"Getting accounts for customer {CHILD_CUSTOMER_ID}...")
    response = customer_service.GetAccountsInfo(
        CustomerId=CHILD_CUSTOMER_ID
    )

    if response and hasattr(response, 'AccountsInfo'):
        account_info = response.AccountsInfo
        if account_info and hasattr(account_info, 'AccountInfo'):
            accounts = account_info.AccountInfo
            print(f"✓ Found {len(accounts)} account(s):\n")
            for account in accounts:
                print(f"  Account ID: {account.Id}")
                print(f"  Name: {account.Name}")
                print(f"  Number: {account.Number}")
                print()
        else:
            print("⚠ No accounts in response")
    else:
        print(f"⚠ Unexpected response: {response}")

    print("=" * 50)
    print("✅ SUCCESS!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying different customer ID formats...")

    # Maybe it's the full number without prefix?
    for test_id in ["10700TZU7", "107000", "536777922"]:
        print(f"\nTrying customer ID: {test_id}")
        try:
            auth = AuthorizationData(
                account_id=None,
                customer_id=test_id,
                developer_token=DEVELOPER_TOKEN,
                authentication=oauth,
            )

            svc = ServiceClient(
                service='CustomerManagementService',
                version=13,
                authorization_data=auth,
            )

            resp = svc.GetAccountsInfo(CustomerId=test_id)
            print(f"  ✓ GetAccountsInfo succeeded for {test_id}!")
            if resp and hasattr(resp, 'AccountsInfo'):
                print(f"  Response: {resp.AccountsInfo}")
            break
        except Exception as e2:
            print(f"  ✗ Failed: {str(e2)[:80]}")
