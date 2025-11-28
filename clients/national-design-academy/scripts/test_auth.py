import os
import sys
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

headers = get_headers_with_auto_token()

print("Headers generated successfully:")
print(f"  Authorization: {headers['Authorization'][:30]}...")
print(f"  Developer-Token: {headers['Developer-Token'][:10]}...")
print(f"  Content-Type: {headers['Content-Type']}")

# Test with a simple query
import requests

customer_id = "7511832413"
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

query = "SELECT customer.id, customer.descriptive_name FROM customer"

print(f"\nTesting API call to: {url}")
response = requests.post(url, headers=headers, json={'query': query})

print(f"Status: {response.status_code}")
if response.ok:
    print("✅ SUCCESS!")
    print(response.json())
else:
    print("❌ FAILED!")
    print(response.text)
