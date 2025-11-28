# Pete's Brain MCP Servers - Setup Checklist

## ✅ Fully Configured & Ready

These MCP servers are configured and ready to use:

- [x] **Google Analytics** - OAuth configured, ready to query GA4 data
- [x] **Google Sheets** - Service account configured, automated exports working
- [x] **Google Tasks** - OAuth configured, task management integrated
- [x] **WooCommerce** - API credentials configured for Godshot

## 🎯 Newly Added - Awaiting Setup

### Google Drive MCP Server ⏳

**Status**: Configuration ready, awaiting OAuth credentials

**Purpose**: Bulletproof Google Docs/Drive integration for importing documents to client folders

**Setup required**:
1. Complete Google Cloud OAuth setup (15 min)
2. Run authentication (5 min)
3. Test import workflow (5 min)

**Full guide**: `shared/mcp-servers/google-drive-mcp-server/SETUP_CHECKLIST.md`

**Quick start**:
```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server
# Follow SETUP_CHECKLIST.md for Google Cloud setup
# Then run:
npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json
```

**What it enables**:
- Import Google Docs to client folders (auto-converted to Markdown)
- Import Google Sheets (auto-converted to CSV)
- Search entire Google Drive
- Read/write Google Workspace files
- Folder management and navigation

## 📋 Pending Credentials

These servers are configured but awaiting API credentials:

### 1. Google Ads - Needs Developer Token

**Time required:** 5-10 minutes (+ approval wait, can be instant or take days)

**Steps:**
1. Go to: https://ads.google.com/aw/apicenter
2. Sign in with your Google Ads account
3. Request developer token
4. Wait for approval
5. Add to `.env` file

**Configuration file**: `shared/mcp-servers/google-ads-mcp-server/.env`

### 2. Facebook Ads - Needs Access Token

**Time required:** 10-15 minutes

**Steps:**
1. Go to: https://developers.facebook.com/
2. Create app → Add Marketing API
3. Generate long-lived access token (60 day expiry)
4. Add to `.env` file

**Configuration file**: `shared/mcp-servers/facebook-ads-mcp-server/.env`

## 🧪 Testing Configured Services

### Google Analytics
```
"Show me GA4 traffic data for the last 30 days"
"What are the top pages by traffic?"
```

### Google Sheets
```
"Read the ROK Experiments sheet"
"Export client list to CSV"
```

### Google Tasks
```
"List my tasks for this week"
"Create task: Follow up with Smythson on Q4 strategy"
```

### Google Drive (after setup)
```
"Add this Google Doc to Devonshire: [URL]"
"Import all docs from this folder to clients/smythson/documents/"
```

### WooCommerce (Godshot)
```
"List products from Godshot store"
"Show me recent orders"
```

## 📚 Documentation

Each MCP server has its own documentation:

- **Google Drive**: `shared/mcp-servers/google-drive-mcp-server/README.md`
- **Google Sheets**: `shared/mcp-servers/google-sheets-mcp-server/README.md`
- **Google Tasks**: `shared/mcp-servers/google-tasks-mcp-server/README.md`
- **Google Analytics**: See `.mcp.json` configuration
- **Google Ads**: `shared/mcp-servers/google-ads-mcp-server/`
- **Facebook Ads**: `shared/mcp-servers/facebook-ads-mcp-server/`
- **WooCommerce**: `shared/mcp-servers/woocommerce-mcp-server/`

## 🔐 Security Notes

All credentials are:
- ✅ Excluded from git (`.gitignore` configured)
- ✅ Stored locally only
- ✅ OAuth tokens auto-refresh
- ✅ Scoped to minimum required permissions

**Credential locations**:
- OAuth tokens: `~/.config/[service-name]/tokens.json`
- Service account keys: `shared/mcp-servers/*/credentials.json`
- API keys: `shared/mcp-servers/*/.env`

## 🚀 Next Steps

1. **Complete Google Drive setup** (highest priority - enables document imports)
   - Follow: `shared/mcp-servers/google-drive-mcp-server/SETUP_CHECKLIST.md`

2. **Get Google Ads developer token** (when needed for campaign analysis)

3. **Get Facebook Ads access token** (when needed for Meta campaigns)

## 📞 Need Help?

- **Google Cloud APIs**: https://console.cloud.google.com/
- **Google Ads API**: https://developers.google.com/google-ads/api/docs/start
- **Meta Marketing API**: https://developers.facebook.com/docs/marketing-apis/
- **MCP Specification**: https://modelcontextprotocol.io/

## 🔄 Automated Workflows Using MCP Servers

These automated workflows use MCP server integrations:

- **ROK Experiments Export** (Google Sheets) - Every 6 hours
- **Weekly Meeting Review** (Google Tasks) - Every Monday 9 AM
- **Tasks Monitor** (Google Tasks) - Every 6 hours
- **Knowledge Base Summary** (Email → Files) - Every Monday 9 AM
