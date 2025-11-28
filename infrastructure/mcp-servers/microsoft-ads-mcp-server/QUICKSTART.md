# Microsoft Ads / Bing Ads MCP Server - Quick Setup Guide

## Overview

This MCP server lets you pull Microsoft Advertising (Bing Ads) campaign data for your clients, just like Google Ads. You can query campaigns, performance metrics, keywords, and ad groups.

## Step 1: Get Azure App Registration Credentials

### 1.1 Create Azure App Registration

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory → App registrations**
3. Click **"New registration"**
4. Configure:
   - **Name**: "Microsoft Ads MCP" (or any name)
   - **Supported account types**: "Accounts in any organizational directory and personal Microsoft accounts"
   - **Redirect URI**: `http://localhost:8080`
5. Click **"Register"**
6. **Copy the Application (client) ID** → This is your `MICROSOFT_ADS_CLIENT_ID`

### 1.2 Create Client Secret

1. In your App Registration, go to **"Certificates & secrets"**
2. Click **"New client secret"**
3. Add description and expiration (recommend 24 months)
4. Click **"Add"**
5. **Copy the secret value immediately** → This is your `MICROSOFT_ADS_CLIENT_SECRET`
   - ⚠️ **You can only see this once!**

### 1.3 Configure API Permissions

1. Go to **"API permissions"**
2. Click **"Add a permission"**
3. Select **"APIs my organization uses"**
4. Search for **"Microsoft Advertising"**
5. Select **"Microsoft Advertising API"**
6. Add permissions:
   - `ads.manage` (Delegated)
   - `offline_access` (Delegated)
7. Click **"Add permissions"**
8. Click **"Grant admin consent"** (if you have admin rights)

## Step 2: Get Developer Token

1. Sign in to [Microsoft Advertising](https://ads.microsoft.com/)
2. Go to **Tools → API Center**
3. **Apply for a Developer Token** (if you don't have one)
   - This may take a few days to approve
4. **Copy your Developer Token** → This is your `MICROSOFT_ADS_DEVELOPER_TOKEN`

## Step 3: Get Refresh Token (OAuth Flow)

### 3.1 Get Authorization Code

Run this Python script (or visit the URL in browser):

```python
import urllib.parse

client_id = "YOUR_CLIENT_ID"
redirect_uri = "http://localhost:8080"
scope = "https://ads.microsoft.com/msads.manage offline_access"

auth_url = (
    f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
    f"client_id={client_id}&"
    f"response_type=code&"
    f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
    f"response_mode=query&"
    f"scope={urllib.parse.quote(scope)}"
)

print("Visit this URL and authorize:")
print(auth_url)
print("\nAfter authorization, copy the 'code' parameter from the redirect URL")
```

### 3.2 Exchange Code for Refresh Token

Once you have the authorization code, run:

```python
import requests

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8080"
code = "AUTHORIZATION_CODE_FROM_STEP_3_1"

token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code',
    'scope': 'https://ads.microsoft.com/msads.manage offline_access'
}

response = requests.post(token_url, data=data)
tokens = response.json()

print("Refresh Token:", tokens.get('refresh_token'))
```

**Save the refresh_token** → This is your `MICROSOFT_ADS_REFRESH_TOKEN`

## Step 4: Configure Environment

Create `.env` file:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/microsoft-ads-mcp-server
cp env.example .env
```

Edit `.env` with your credentials:

```bash
MICROSOFT_ADS_CLIENT_ID=your_client_id_here
MICROSOFT_ADS_CLIENT_SECRET=your_client_secret_here
MICROSOFT_ADS_DEVELOPER_TOKEN=your_developer_token_here
MICROSOFT_ADS_REFRESH_TOKEN=your_refresh_token_here
MICROSOFT_ADS_CUSTOMER_ID=  # Optional: default account ID
```

## Step 5: Update .mcp.json

The server is already added to `.mcp.json`. Just replace the placeholder values:

```json
"microsoft-ads": {
  "env": {
    "MICROSOFT_ADS_CLIENT_ID": "your_actual_client_id",
    "MICROSOFT_ADS_CLIENT_SECRET": "your_actual_client_secret",
    "MICROSOFT_ADS_DEVELOPER_TOKEN": "your_actual_developer_token",
    "MICROSOFT_ADS_REFRESH_TOKEN": "your_actual_refresh_token"
  }
}
```

## Step 6: Restart Claude Desktop

Close and restart Claude Desktop to load the new server.

## Step 7: Find Client Account IDs

Use the helper script to find account IDs for your clients:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/microsoft-ads-mcp-server
source .venv/bin/activate
python3 get_client_ids.py "Client Name"
python3 get_client_ids.py --all  # List all accounts
```

## Usage Examples

Once configured, you can use it just like Google Ads:

### List Accounts
```
"List all my Microsoft Ads accounts"
```

### Get Campaigns
```
"Show me all campaigns for Microsoft Ads account 12345678"
```

### Get Campaign Performance
```
"Get campaign performance for account 12345678 for the last 30 days"

"Show me performance metrics for campaigns 111, 222, 333 in account 12345678"
```

### Get Keywords
```
"Get all keywords for account 12345678"

"Show me keywords for campaign 111 in account 12345678"
```

### Get Ad Groups
```
"List all ad groups for account 12345678"

"Show me ad groups for campaign 111 in account 12345678"
```

## Available Tools

- `list_accounts` - List all accessible Microsoft Ads accounts
- `get_campaigns` - Get campaigns for a customer account
- `get_campaign_performance` - Get campaign performance metrics
- `get_keywords` - Get keywords for campaigns or ad groups
- `get_ad_groups` - Get ad groups for campaigns

## Troubleshooting

**"Invalid client ID/secret"**
- Verify credentials in Azure Portal
- Check `.env` file has correct values

**"Refresh token expired"**
- Re-run OAuth flow to get new refresh token

**"Developer token invalid"**
- Check token in Microsoft Advertising API Center
- Ensure token is approved and active

**"Access denied"**
- Ensure API permissions are granted
- Check admin consent is given

## Next Steps

1. Complete OAuth setup (Steps 1-3)
2. Add credentials to `.mcp.json`
3. Restart Claude Desktop
4. Find client account IDs using `get_client_ids.py`
5. Start querying campaign data!

