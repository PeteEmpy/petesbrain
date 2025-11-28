# MCP Servers Setup Guide

This directory contains MCP (Model Context Protocol) servers that integrate external services with Claude Code:

## Installed Servers

1. **Google Analytics 4** - Analyze GA4 data and website traffic
2. **Google Ads** - Query Google Ads performance with GAQL, keyword research
3. **Google Sheets** - Read/write spreadsheet data, automated exports
4. **Google Tasks** - Manage tasks, create action items from meetings
5. **Facebook/Meta Ads** - Access Meta advertising account data

## Installation Status

✅ All servers installed with dependencies

### Server Locations

- `google-analytics-mcp-server/` - GA4 data and reports
- `google-ads-mcp-server/` - Google Ads queries and keyword planner
- `google-sheets-mcp-server/` - Google Sheets integration
- `google-tasks-mcp-server/` - Google Tasks management
- `facebook-ads-mcp-server/` - Meta Ads data

## Next Steps: OAuth Credentials Setup

Before you can use these servers, you need to obtain OAuth credentials from Google Cloud and Meta:

### Google Analytics & Google Ads Setup

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing

2. **Enable APIs**
   - Enable "Google Analytics Data API" (for Analytics)
   - Enable "Google Ads API" (for Ads)

3. **Create OAuth 2.0 Credentials**
   - Go to APIs & Services → Credentials
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: "Desktop application"
   - Download the JSON file

4. **For Google Ads: Get Developer Token**
   - Go to [Google Ads API Center](https://ads.google.com/aw/apicenter)
   - Request a developer token
   - Save the token

5. **Configure Environment Variables**

   For **Google Analytics**:
   ```bash
   cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-analytics-mcp-server
   cat > .env << EOF
   GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH=/full/path/to/client_secret.json
   EOF
   ```

   For **Google Ads**:
   ```bash
   cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server
   cat > .env << EOF
   GOOGLE_ADS_DEVELOPER_TOKEN=your-developer-token-here
   GOOGLE_ADS_OAUTH_CONFIG_PATH=/full/path/to/client_secret.json
   EOF
   ```

### Google Sheets Setup

**Option 1: Service Account (Recommended for automation)**

1. **Create Service Account**
   - Go to Google Cloud Console → IAM & Admin → Service Accounts
   - Create new service account
   - Download JSON key file

2. **Enable Google Sheets API**
   - Go to APIs & Services → Library
   - Search for "Google Sheets API"
   - Enable it

3. **Configure**
   ```bash
   cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server
   # Copy your service account JSON to credentials.json
   cp /path/to/downloaded-key.json credentials.json
   ```

4. **Share Spreadsheets**
   - For each spreadsheet you want to access, share it with the service account email
   - Email format: `service-account-name@project-id.iam.gserviceaccount.com`

**Option 2: OAuth (For user-specific access)**
   - Follow same OAuth setup as Google Analytics above
   - Enable "Google Sheets API" instead

### Google Tasks Setup

1. **Enable API**
   - Go to Google Cloud Console → APIs & Services
   - Enable "Google Tasks API"

2. **Run Setup Script**
   ```bash
   cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server
   ./setup.sh
   ```

3. **First Use Authentication**
   - On first use, browser will open for OAuth
   - Grant permission to manage tasks
   - Token stored in `token.json` for future use

### Facebook/Meta Ads Setup

1. **Create Meta App**
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Create a new app or use existing
   - Add "Marketing API" product

2. **Get Access Token**
   - Generate a User Access Token with `ads_read` permission
   - Save the token

3. **Configure Environment**
   ```bash
   cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/facebook-ads-mcp-server
   cat > .env << EOF
   FACEBOOK_ACCESS_TOKEN=your-access-token-here
   EOF
   ```

## Configuring in Claude Code

Once you have credentials set up, add the servers to Claude Code:

### Option 1: Using `.mcp.json` (Project-level)

Create `/Users/administrator/Documents/PetesBrain/.mcp.json`:

```json
{
  "mcpServers": {
    "google-analytics": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-analytics-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-analytics-mcp-server/server.py"]
    },
    "google-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/server.py"]
    },
    "facebook-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/facebook-ads-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/facebook-ads-mcp-server/server.py"]
    }
  }
}
```

### Option 2: Using CLI Commands

```bash
cd /Users/administrator/Documents/PetesBrain

# Add Google Analytics
claude mcp add --transport stdio --scope project google-analytics \
  -- /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-analytics-mcp-server/.venv/bin/python \
  /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-analytics-mcp-server/server.py

# Add Google Ads
claude mcp add --transport stdio --scope project google-ads \
  -- /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv/bin/python \
  /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/server.py

# Add Facebook Ads
claude mcp add --transport stdio --scope project facebook-ads \
  -- /Users/administrator/Documents/PetesBrain/shared/mcp-servers/facebook-ads-mcp-server/.venv/bin/python \
  /Users/administrator/Documents/PetesBrain/shared/mcp-servers/facebook-ads-mcp-server/server.py
```

## First-Time Authentication

When you first use each server in Claude Code:

1. **Google Services**: A browser window will open automatically for OAuth
2. **Facebook**: Uses the access token from .env file

Tokens are stored locally and refreshed automatically.

## Verification

To verify the servers are configured:
```bash
claude mcp list
```

## Usage in Claude Code

Once configured, you can ask Claude Code to:

**Google Ads:**
- "Analyze Google Ads performance for client X"
- "Run keyword research for 'luxury notebooks'"
- "Query campaign data with GAQL"

**Google Analytics:**
- "Pull GA4 data for the last 30 days"
- "Show me traffic sources for client Y"
- "Compare page views month over month"

**Google Sheets:**
- "Read data from ROK Experiments sheet"
- "Export campaign data to Google Sheets"
- "Update client budget spreadsheet"

**Google Tasks:**
- "Create a task for following up with Smythson"
- "Show my tasks for this week"
- "Mark the client report task as complete"

**Facebook/Meta Ads:**
- "Show me Facebook Ads metrics for campaign Y"
- "Compare Meta ad performance across accounts"

## Troubleshooting

- **Server not found**: Check paths in `.mcp.json` are absolute
- **Auth errors**: Verify OAuth credentials are correct and APIs are enabled
- **Permission errors**: Ensure .venv/bin/python is executable

## Next Steps

1. Set up OAuth credentials (see above)
2. Configure servers in Claude Code
3. Start analyzing client data!
