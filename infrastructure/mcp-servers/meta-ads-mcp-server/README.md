# Meta (Facebook) Ads MCP Server 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-v2.8.0-green.svg)](https://github.com/jlowin/fastmcp)

**A FastMCP-powered Model Context Protocol server for Meta Marketing API integration with automatic OAuth 2.0 authentication**

Connect Meta (Facebook/Instagram) Ads directly to Claude Desktop and other MCP clients with seamless OAuth 2.0 authentication, automatic token management, and comprehensive ad performance insights.

Built for **PetesBrain** - Part of the integrated digital marketing intelligence system.

## ✨ Features

- 🔐 **Automatic OAuth 2.0** - One-time browser authentication with long-lived tokens (60 days)
- 🔄 **Smart Token Management** - Automatic token refresh and validation
- 📊 **Comprehensive Insights** - Campaign, ad set, and ad-level performance data
- 🎯 **Audience Analysis** - Delivery estimates and targeting insights
- 🏢 **Multi-Account Support** - Manage multiple ad accounts seamlessly
- 🔍 **Custom Queries** - Flexible insights API with breakdowns and filtering
- 🚀 **FastMCP Framework** - Built on the modern MCP standard
- 🖥️ **Claude Desktop Ready** - Direct integration with Claude Desktop
- 🛡️ **Secure Local Storage** - Tokens stored locally, never exposed

## 📋 Available Tools

### Account Management
| Tool | Description | Example Usage |
|------|-------------|---------------|
| `list_ad_accounts` | List all accessible ad accounts | "Show me all my Meta ad accounts" |
| `get_account_details` | Get detailed info about an account | "Get details for account act_123456789" |

### Campaign Operations
| Tool | Description | Example Usage |
|------|-------------|---------------|
| `get_campaigns` | List campaigns for an account | "Show me all campaigns for account act_123456789" |
| `get_campaign_insights` | Get campaign performance data | "Get campaign performance for campaign 123456789" |

### Ad Set Operations
| Tool | Description | Example Usage |
|------|-------------|---------------|
| `get_adsets` | List ad sets for a campaign | "Show me ad sets for campaign 123456789" |
| `get_adset_insights` | Get ad set performance data | "Get ad set insights for adset 123456789" |

### Ad Operations
| Tool | Description | Example Usage |
|------|-------------|---------------|
| `get_ads` | List ads for an ad set | "Show me ads in ad set 123456789" |
| `get_ad_insights` | Get individual ad performance | "Get performance for ad 123456789" |

### Advanced Insights
| Tool | Description | Example Usage |
|------|-------------|---------------|
| `get_account_insights` | Account-level insights with aggregation | "Get account insights by campaign for act_123456789" |
| `run_custom_insights_query` | Run custom insights with full control | "Query impressions and spend by age and gender" |
| `get_audience_insights` | Get audience delivery estimates | "Estimate reach for 25-34 year olds in New York" |

**Note:** All tools automatically handle authentication - no token parameters required!

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ installed
- A Meta Business account with ad account access
- Meta for Developers app credentials

## 🔧 Step 1: Meta for Developers Setup

### 1.1 Create Meta App

1. **Go to [Meta for Developers](https://developers.facebook.com/)**
2. **Click "My Apps" → "Create App"**
3. **Select "Business" as app type**
4. **Fill in app details:**
   - Display name: "Meta Ads MCP"
   - App contact email: Your email
   - Business account: Select your business
5. **Click "Create App"**

### 1.2 Configure App Settings

1. **In your app dashboard, go to "Settings" → "Basic"**
2. **Copy your App ID and App Secret** (you'll need these)
3. **Add a platform:**
   - Click "Add Platform"
   - Select "Website"
   - Site URL: `http://localhost:8080/`
4. **Save changes**

### 1.3 Enable Marketing API

1. **In app dashboard, click "Add Product"**
2. **Find "Marketing API" and click "Set Up"**
3. **Grant necessary permissions:**
   - `ads_read` - Read ad account data
   - `ads_management` - Manage ads
   - `business_management` - Access business info

### 1.4 Go Live

1. **Switch app mode from "Development" to "Live"**
   - Top of dashboard toggle
   - Required for accessing production ad accounts

## 🔧 Step 2: Installation & Setup

### 2.1 Navigate to Project Directory

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server
```

### 2.2 Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Environment Configuration

Create a `.env` file in the project directory:

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` with your credentials:

```bash
# Required: Meta App ID from Meta for Developers
META_APP_ID=1234567890123456

# Required: Meta App Secret from Meta for Developers
META_APP_SECRET=your_app_secret_here

# Optional: Custom path to store OAuth token
# META_TOKEN_PATH=/custom/path/to/meta_ads_token.json
```

## 🖥️ Step 3: Claude Desktop Integration

### 3.1 Locate Claude Configuration

Find your Claude Desktop configuration file:

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

### 3.2 Add MCP Server Configuration

Edit the configuration file and add your Meta Ads MCP server:

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server/venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server/server.py"
      ]
    }
  }
}
```

**Important:** 
- Use **absolute paths** for all file locations
- Replace paths with your actual installation directory
- On Windows, use forward slashes `/` or double backslashes `\\`

### 3.3 Restart Claude Desktop

Close and restart Claude Desktop to load the new configuration.

## 🔐 Step 4: First-Time Authentication

### 4.1 Trigger OAuth Flow

1. **Open Claude Desktop**
2. **Try any Meta Ads command**, for example:
   ```
   "List all my Meta ad accounts"
   ```

### 4.2 Complete Authentication

1. **Browser opens automatically** to Facebook login
2. **Sign in** with your Facebook account (the one with ad account access)
3. **Grant permissions** by clicking "Continue"
4. **Browser shows success page** - "✅ Authentication Successful!"
5. **Return to Claude** - your command will complete automatically!

### 4.3 Verify Setup

After authentication, you should see:
- A `meta_ads_token.json` file created in your project directory
- Your Meta ad accounts listed in Claude's response

## 📖 Usage Examples

### Basic Account Operations

```
"List all my Meta ad accounts"

"Show me details for account act_123456789"

"Which accounts have active campaigns?"
```

### Campaign Analysis

```
"Show me all campaigns for account act_123456789"

"Get campaign performance for the last 30 days"

"Which campaigns have the highest spend?"

"Show me campaign insights with device breakdown"
```

### Ad Set Performance

```
"Get ad sets for campaign 123456789"

"Show me ad set performance for the last 7 days"

"Compare ad set performance by age and gender"
```

### Ad-Level Insights

```
"Show me all ads in ad set 123456789"

"Get ad performance for ad 987654321"

"Which ads have the best click-through rate?"
```

### Custom Insights Queries

```
"Get account insights by campaign for the last 30 days"

"Show me impressions and spend broken down by age for campaign 123456789"

"Query all active campaigns with spend over $100"
```

### Audience Insights

```
"Estimate reach for targeting 25-34 year olds interested in technology"

"What's the audience size for New York City residents?"
```

## 🔍 Advanced Usage

### Date Ranges

**Using Date Presets:**
```
get_campaign_insights(
    campaign_id="123456789",
    date_preset="last_30d"
)
```

Available presets: `today`, `yesterday`, `last_7d`, `last_14d`, `last_30d`, `last_90d`, `this_month`, `last_month`, `this_quarter`, `last_quarter`, `maximum`

**Using Custom Time Ranges:**
```
get_campaign_insights(
    campaign_id="123456789",
    time_range={"since": "2025-01-01", "until": "2025-01-31"}
)
```

### Breakdowns

Get insights broken down by dimensions:

```
get_campaign_insights(
    campaign_id="123456789",
    date_preset="last_30d",
    breakdowns=["age", "gender", "device_platform"]
)
```

Common breakdowns:
- **Demographics:** `age`, `gender`
- **Platform:** `device_platform`, `publisher_platform`, `platform_position`
- **Time:** `hourly_stats_aggregated_by_advertiser_time_zone`

### Filtering

Filter results with custom conditions:

```
run_custom_insights_query(
    object_id="act_123456789",
    fields=["impressions", "clicks", "spend", "campaign_name"],
    date_preset="last_30d",
    level="campaign",
    filtering=[{
        "field": "campaign.delivery_info",
        "operator": "IN",
        "value": ["active"]
    }]
)
```

### Status Filtering

Filter by object status:

```
get_campaigns(
    account_id="act_123456789",
    status_filter=["ACTIVE", "PAUSED"]
)
```

## 📁 Project Structure

```
meta-ads-mcp-server/
├── server.py                    # Main MCP server
├── oauth/
│   ├── __init__.py             # Package initialization
│   └── meta_auth.py            # OAuth authentication logic
├── meta_ads_token.json         # Auto-generated token storage (gitignored)
├── .env                        # Environment variables (gitignored)
├── env.example                 # Environment template
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── venv/                       # Virtual environment (gitignored)
├── README.md                   # This file
├── SETUP.md                    # Detailed setup guide
└── QUICKSTART.md               # PetesBrain integration guide
```

## 🔒 Security & Best Practices

### File Security
- ✅ **Credential files are gitignored** - Never committed to version control
- ✅ **Local token storage** - Tokens stored in `meta_ads_token.json` locally
- ✅ **Environment variables** - Sensitive data in `.env` file
- ✅ **Long-lived tokens** - 60-day token validity reduces re-auth frequency

### Recommended File Permissions
```bash
# Set secure permissions for sensitive files
chmod 600 .env
chmod 600 meta_ads_token.json
```

### Production Considerations
1. **Use environment variables** instead of `.env` files in production
2. **Implement rate limiting** to respect API quotas
3. **Monitor API usage** in Meta for Developers dashboard
4. **Secure token storage** with proper access controls
5. **Regular security audits** of access permissions

## 🛠️ Troubleshooting

### Authentication Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **No tokens found** | "Starting OAuth flow" message | ✅ Normal for first-time setup - complete browser authentication |
| **Permission denied** | "Access denied" in browser | Ensure Facebook account has ad account access |
| **Invalid app credentials** | "Invalid app ID or secret" | Verify META_APP_ID and META_APP_SECRET in .env |
| **Token expired** | "Invalid OAuth access token" | Delete `meta_ads_token.json` and re-authenticate |

### Configuration Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Environment variables missing** | "Environment variable not set" | Check `.env` file exists and has correct values |
| **File not found** | "FileNotFoundError" | Verify absolute paths in Claude config |
| **Module import errors** | "ModuleNotFoundError" | Run `pip install -r requirements.txt` in venv |
| **Python path issues** | "Command not found" | Use absolute path to Python in venv |

### API Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Invalid account ID** | "Account not found" | Use format: `act_123456789` (with `act_` prefix) |
| **Permissions error** | "Insufficient permissions" | Verify app has required permissions in Meta for Developers |
| **Rate limit exceeded** | "Rate limit exceeded" | Wait for quota reset or reduce request frequency |
| **App not live** | "App must be live" | Switch app mode to "Live" in Meta for Developers |

### Debug Mode

Enable detailed logging for troubleshooting:

```python
# Add to server.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Advanced Configuration

### HTTP Transport Mode

For web deployment or remote access:

```bash
# Start server in HTTP mode
python3 server.py --http
```

**Claude Desktop config for HTTP:**
```json
{
  "mcpServers": {
    "meta-ads": {
      "url": "http://127.0.0.1:8001/mcp"
    }
  }
}
```

### Custom Token Storage

Modify token storage location in `.env`:

```bash
META_TOKEN_PATH=/custom/secure/path/meta_ads_token.json
```

## 📊 API Metrics & Insights

### Common Metrics Available

**Performance Metrics:**
- `impressions` - Ad views
- `clicks` - Click count
- `spend` - Amount spent
- `reach` - Unique people reached
- `frequency` - Avg impressions per person

**Cost Metrics:**
- `cpc` - Cost per click
- `cpm` - Cost per 1000 impressions
- `cpp` - Cost per 1000 people reached
- `ctr` - Click-through rate

**Conversion Metrics:**
- `actions` - All actions (likes, shares, conversions)
- `action_values` - Values of actions
- `conversions` - Total conversions
- `conversion_values` - Revenue from conversions
- `cost_per_action_type` - Cost per action type
- `cost_per_conversion` - Cost per conversion

**Video Metrics (for video ads):**
- `video_thruplay_watched_actions` - 15s+ views
- `video_p100_watched_actions` - 100% completion

## 🔗 Integration with PetesBrain

This MCP server integrates with the PetesBrain system for:

- **Cross-Platform Analytics** - Combine with Google Ads MCP for unified reporting
- **Client Management** - Works with Superspace and other clients running Meta ads
- **Automated Reporting** - Data feeds into monthly report generators
- **Performance Monitoring** - Daily performance alerts and tracking

See `QUICKSTART.md` for PetesBrain-specific integration details.

## 📄 License

This project is licensed under the MIT License.

```
Copyright (c) 2025 PetesBrain Meta Ads MCP Server

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Built with ❤️ for PetesBrain**

*Connecting Meta Ads data directly to AI assistants for powerful advertising insights through natural language conversations.*

