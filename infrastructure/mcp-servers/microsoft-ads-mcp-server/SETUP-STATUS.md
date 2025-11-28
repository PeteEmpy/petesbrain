# Microsoft Ads MCP Server - Setup Status

**Last Updated**: November 21, 2025
**Status**: ✅ **COMPLETE** - Server configured and ready

## Setup Complete

All credentials configured and tested successfully on November 21, 2025.

### Credentials Configured
- **Client ID**: `ed3e808d-85d1-4584-be66-cf8b3814f6d4`
- **Client Secret**: Configured in `.mcp.json`
- **Developer Token**: `017HS0H672339366`
- **Refresh Token**: Configured in `.mcp.json`

### Azure App Registration
- **Name**: Mikerosoft Ads MCP (typo in name, works fine)
- **Tenant**: Default Directory (petere@roksys.co.uk)
- **API Permissions**: `offline_access` (Microsoft Graph)
- **Redirect URI**: `http://localhost:8080`

### What's Ready

- ✅ Server code (`server.py`)
- ✅ Virtual environment with dependencies
- ✅ OAuth authentication working
- ✅ Token refresh tested and working
- ✅ Added to `.mcp.json`

### Available Tools

Once Claude Code is restarted, you'll have access to:

| Tool | Description |
|------|-------------|
| `list_accounts` | List all accessible Microsoft Ads accounts |
| `get_campaigns` | Get campaigns for a customer account |
| `get_campaign_performance` | Get campaign performance metrics with date filtering |
| `get_keywords` | Get keywords for campaigns or ad groups |
| `get_ad_groups` | Get ad groups for campaigns |

### Usage Examples

```
"List all my Microsoft Ads accounts"
"Show me campaigns for Microsoft Ads account 12345678"
"Get campaign performance for account 12345678 for the last 30 days"
```

### To Use

1. **Restart Claude Code** to load the new MCP server
2. The server will be available as `microsoft-ads`
3. Use natural language to query Microsoft Advertising data

### Troubleshooting

If you encounter issues:

1. **Token expired**: Refresh tokens last ~90 days. Re-run OAuth flow if needed
2. **API errors**: Check Developer Token is still valid at https://ads.microsoft.com/ → Settings → Developer Settings
3. **Connection issues**: Verify credentials in `.mcp.json`

---

**Setup completed**: November 21, 2025
