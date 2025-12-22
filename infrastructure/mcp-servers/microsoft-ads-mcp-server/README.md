# Microsoft Ads / Bing Ads MCP Server 🚀

**A FastMCP-powered Model Context Protocol server for Microsoft Advertising API integration**

Connect Microsoft Advertising (formerly Bing Ads) API directly to Claude Desktop and other MCP clients with OAuth 2.0 authentication and campaign management capabilities.

**Note:** Microsoft Advertising was formerly known as "Bing Ads" - this server works with both naming conventions.

## ✨ Features

- 🔐 **OAuth 2.0 Authentication** - Secure token-based authentication with automatic token refresh
- 📊 **Campaign Management** - List, create, and manage campaigns (budgets, status)
- 🔍 **Keyword Management** - View, add, and pause keywords with bid management
- 📈 **Performance Reporting** - Get campaign performance metrics with date filtering
- 🔎 **Search Term Analysis** - Analyse search query performance and identify opportunities
- 🎯 **Ad Group Operations** - List and manage ad groups across campaigns
- 🏢 **Account Management** - List and access multiple accounts
- 🔗 **Platform ID Integration** - Retrieve client platform IDs from CONTEXT.md files
- 🚀 **FastMCP Framework** - Built on the modern MCP standard
- 🖥️ **Claude Desktop Ready** - Direct integration with Claude Desktop

## 📋 Available Tools

### Account & Campaign Information

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_accounts` | List all accessible Microsoft Ads accounts | None |
| `get_campaigns` | Get all campaigns for a customer account | `customer_id` |
| `get_campaign_performance` | Get campaign performance metrics | `customer_id`, `campaign_ids` (optional), `start_date`, `end_date` |
| `get_ad_groups` | Get ad groups for campaigns | `customer_id`, `campaign_id` (optional) |
| `get_keywords` | Get keywords for campaigns or ad groups | `customer_id`, `campaign_id` (optional), `ad_group_id` (optional) |
| `get_search_terms` | Get search query performance report | `customer_id`, `start_date` (optional), `end_date` (optional), `campaign_ids` (optional) |
| `get_client_platform_ids` | Get platform IDs from client CONTEXT.md | `client_name` |

### Campaign Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_campaign` | Create a new Microsoft Ads campaign | `customer_id`, `campaign_name`, `daily_budget`, `campaign_type` (optional), `status` (optional) |
| `update_campaign_budget` | Update daily budget for a campaign | `customer_id`, `campaign_id`, `daily_budget` |
| `update_campaign_status` | Update campaign status (Active/Paused/Deleted) | `customer_id`, `campaign_id`, `status` |

### Keyword Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_keywords` | Add keywords to an ad group | `customer_id`, `ad_group_id`, `keywords` (list of dicts) |
| `pause_keywords` | Pause keywords in an ad group | `customer_id`, `ad_group_id`, `keyword_ids` (list) |

## 🚀 Quick Start

### Prerequisites

Before setting up the MCP server, you'll need:
- Python 3.10+ installed
- A Microsoft Advertising account
- Azure App Registration (for OAuth)
- Microsoft Advertising API Developer Token

## 🔧 Step 1: Microsoft Advertising API Setup

### 1.1 Create Azure App Registration

1. **Go to [Azure Portal](https://portal.azure.com/)**
2. **Navigate to Azure Active Directory → App registrations**
3. **Click "New registration"**
4. **Configure:**
   - Name: "Microsoft Ads MCP"
   - Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
   - Redirect URI: `http://localhost:8080` (for OAuth callback)
5. **Click "Register"**
6. **Note your Application (client) ID** - this is your `MICROSOFT_ADS_CLIENT_ID`

### 1.2 Create Client Secret

1. **In your App Registration, go to "Certificates & secrets"**
2. **Click "New client secret"**
3. **Add description and expiration**
4. **Click "Add"**
5. **Copy the secret value immediately** - this is your `MICROSOFT_ADS_CLIENT_SECRET`
   - ⚠️ **Important:** You can only see this value once!

### 1.3 Configure API Permissions

1. **Go to "API permissions"**
2. **Click "Add a permission"**
3. **Select "APIs my organization uses"**
4. **Search for "Microsoft Advertising"**
5. **Select "Microsoft Advertising API"**
6. **Add permissions:**
   - `ads.manage` (Delegated)
   - `offline_access` (Delegated)
7. **Click "Add permissions"**
8. **Click "Grant admin consent"** (if you have admin rights)

### 1.4 Get Developer Token

1. **Sign in to [Microsoft Advertising](https://ads.microsoft.com/)**
2. **Go to Tools → API Center**
3. **Apply for a Developer Token** (if you don't have one)
4. **Copy your Developer Token** - this is your `MICROSOFT_ADS_DEVELOPER_TOKEN`

## 🔧 Step 2: OAuth Authentication Setup

### 2.1 Get Authorization Code

Run this Python script to get your authorization code:

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

### 2.2 Exchange Code for Refresh Token

Once you have the authorization code, exchange it for a refresh token:

```python
import requests

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8080"
code = "AUTHORIZATION_CODE_FROM_STEP_2_1"

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

Save the `refresh_token` - this is your `MICROSOFT_ADS_REFRESH_TOKEN`.

## 🔧 Step 3: Installation & Setup

### 3.1 Install Dependencies

```bash
cd shared/mcp-servers/microsoft-ads-mcp-server

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3.2 Environment Configuration

Create a `.env` file:

```bash
cp env.example .env
```

Edit `.env` with your credentials:

```bash
MICROSOFT_ADS_CLIENT_ID=your_client_id_here
MICROSOFT_ADS_CLIENT_SECRET=your_client_secret_here
MICROSOFT_ADS_DEVELOPER_TOKEN=your_developer_token_here
MICROSOFT_ADS_REFRESH_TOKEN=your_refresh_token_here
MICROSOFT_ADS_CUSTOMER_ID=your_account_id_here  # Optional
```

## 🖥️ Step 4: Claude Desktop Integration

### 4.1 Add to .mcp.json

Edit `/Users/administrator/Documents/PetesBrain/.mcp.json` and add:

```json
{
  "mcpServers": {
    "microsoft-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/microsoft-ads-mcp-server/.venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/microsoft-ads-mcp-server/server.py"
      ],
      "env": {
        "MICROSOFT_ADS_CLIENT_ID": "your_client_id",
        "MICROSOFT_ADS_CLIENT_SECRET": "your_client_secret",
        "MICROSOFT_ADS_DEVELOPER_TOKEN": "your_developer_token",
        "MICROSOFT_ADS_REFRESH_TOKEN": "your_refresh_token"
      }
    }
  }
}
```

**Important:** 
- Use **absolute paths** for all file locations
- Replace placeholder values with your actual credentials
- Consider using environment variables instead of hardcoding secrets

### 4.2 Restart Claude Desktop

Close and restart Claude Desktop to load the new configuration.

## 📖 Usage Examples

### Account & Campaign Information

**List Accounts**
```
"List all my Microsoft Ads accounts"
```

**Get Campaigns**
```
"Show me all campaigns for account 12345678"
```

**Get Campaign Performance**
```
"Get campaign performance for account 12345678 for the last 30 days"

"Show me performance metrics for campaigns 111, 222, 333 in account 12345678 from 2025-01-01 to 2025-01-31"
```

**Get Ad Groups**
```
"List all ad groups for account 12345678"

"Show me ad groups for campaign 111 in account 12345678"
```

**Get Keywords**
```
"Get all keywords for campaign 111 in account 12345678"

"Show me keywords for ad group 222 in account 12345678"
```

**Get Search Terms**
```
"Get search term report for account 12345678 for the last 30 days"

"Show me search queries for campaigns 111, 222 in account 12345678"
```

**Get Client Platform IDs**
```
"Get Microsoft Ads account ID for Smythson"

"Show me platform IDs for Tree2mydoor"
```

### Campaign Management

**Create Campaign**
```
"Create a new Search campaign called 'Brand - UK' for account 12345678 with £50 daily budget"

"Create a Shopping campaign called 'All Products' for account 12345678 with £100 daily budget, status Active"
```

**Update Campaign Budget**
```
"Update campaign 111 budget to £75 for account 12345678"

"Change daily budget to £150 for campaign 222 in account 12345678"
```

**Update Campaign Status**
```
"Pause campaign 111 in account 12345678"

"Activate campaign 222 in account 12345678"
```

### Keyword Management

**Add Keywords**
```
"Add keywords to ad group 222 in account 12345678:
- luxury leather diary (Exact match, £2.50 bid)
- handcrafted notebook (Phrase match, £1.80 bid)
- premium journal (Broad match)"
```

**Pause Keywords**
```
"Pause keywords 333, 444, 555 in ad group 222, account 12345678"
```

## 🛠️ Troubleshooting

### Authentication Issues

| Issue | Solution |
|-------|----------|
| **Invalid client ID/secret** | Verify credentials in Azure Portal |
| **Refresh token expired** | Re-run OAuth flow to get new refresh token |
| **Access denied** | Ensure API permissions are granted and admin consent is given |

### API Issues

| Issue | Solution |
|-------|----------|
| **Invalid customer ID** | Verify account ID format (usually numeric) |
| **Developer token invalid** | Check token in Microsoft Advertising API Center |
| **Rate limit exceeded** | Wait and retry, or implement rate limiting |

### Configuration Issues

| Issue | Solution |
|-------|----------|
| **Environment variables not set** | Check `.env` file and Claude config `env` section |
| **Module import errors** | Run `pip install -r requirements.txt` |
| **Python path issues** | Use absolute path to Python executable |

## 📊 API Limits

Microsoft Advertising API has rate limits:
- **Standard accounts:** 5,000 calls per day
- **Request rate:** Varies by endpoint

Implement caching and rate limiting as needed.

## 🔒 Security Best Practices

- ✅ **Never commit `.env` file** to version control
- ✅ **Use environment variables** in production
- ✅ **Rotate refresh tokens** periodically
- ✅ **Set secure file permissions:** `chmod 600 .env`
- ✅ **Monitor API usage** in Microsoft Advertising portal

## 📄 License

This project follows the same license as other PetesBrain MCP servers.

---

**Made for PetesBrain**

*Connect your Microsoft Advertising data directly to AI assistants and unlock powerful advertising insights.*

