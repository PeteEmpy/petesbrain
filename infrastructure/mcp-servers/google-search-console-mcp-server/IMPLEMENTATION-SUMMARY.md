# Google Search Console MCP Server - Implementation Summary

**Date**: 18 December 2025
**Status**: ✅ Complete and Ready to Use

## What Was Built

A fully functional MCP server providing Google Search Console API integration for PetesBrain.

### Core Components

1. **server.py** - Main FastMCP server with 5 tools:
   - `list_sites` - List all verified Search Console properties
   - `get_performance_data` - Query Search Analytics data (clicks, impressions, CTR, position)
   - `inspect_url` - Check URL indexing status and issues
   - `list_sitemaps` - List sitemaps for a site
   - `get_client_platform_ids` - Legacy tool for platform ID lookup (deprecated)

2. **oauth/google_auth.py** - OAuth 2.0 authentication with lazy loading
   - Prevents startup OAuth popups (loads only when tools are called)
   - Automatic token refresh
   - Browser-based OAuth flow with console fallback
   - Token persistence in server directory

3. **oauth/__init__.py** - Module exports

4. **requirements.txt** - Dependencies:
   - fastmcp>=0.8.0
   - requests>=2.31.0
   - python-dotenv>=1.0.0
   - google-auth>=2.23.0
   - google-auth-oauthlib>=1.1.0
   - google-auth-httplib2>=0.1.1

5. **README.md** - Comprehensive documentation (190+ lines)
   - Feature overview
   - Setup instructions
   - Usage examples for all tools
   - API reference
   - Troubleshooting guide

6. **SETUP.md** - Quick start guide
   - Common use cases with code examples
   - Client integration instructions
   - Configuration reference
   - Troubleshooting tips

7. **.env.example** - Environment variable template

8. **.env** - Actual configuration (already existed, verified correct)

## Configuration

### MCP Server Registration

Added to `~/.claude.json`:

```json
{
  "google-search-console": {
    "command": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server/.venv/bin/python",
    "args": [
      "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server/server.py"
    ],
    "env": {
      "GOOGLE_SEARCH_CONSOLE_OAUTH_CONFIG_PATH": "/Users/administrator/Downloads/credentials.json",
      "PLATFORM_IDS_HELPER": "/Users/administrator/Documents/PetesBrain.nosync/shared/platform_ids.py",
      "CLIENT_IDS_PATH": "/Users/administrator/Documents/PetesBrain.nosync/clients"
    }
  }
}
```

### Virtual Environment

- Pre-existing venv with Python 3.12
- All dependencies already installed
- Verified working with import test

## Available MCP Tools

### 1. mcp__google_search_console__list_sites()

Returns all verified sites/properties with permission levels.

**Example Response**:
```json
{
  "sites": [
    {
      "siteUrl": "https://www.smythson.com/",
      "permissionLevel": "siteOwner"
    }
  ],
  "count": 1
}
```

### 2. mcp__google_search_console__get_performance_data()

Query Search Analytics data with flexible dimensions.

**Parameters**:
- `site_url` (required): Property URL
- `start_date` (required): YYYY-MM-DD
- `end_date` (required): YYYY-MM-DD
- `dimensions` (optional): query, page, country, device, searchAppearance, date
- `row_limit` (optional): 1-25000, default 1000
- `start_row` (optional): Pagination offset

**Example Usage**:
```python
# Top queries by clicks
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['query'],
    row_limit=50
)

# Device comparison
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-12-11',
    end_date='2025-12-18',
    dimensions=['device']
)

# Query performance by device
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-12-11',
    end_date='2025-12-18',
    dimensions=['query', 'device'],
    row_limit=100
)
```

### 3. mcp__google_search_console__inspect_url()

Check live indexing status for specific URLs.

**Parameters**:
- `site_url` (required): Property URL
- `inspection_url` (required): URL to inspect (must be under site_url)

**Example**:
```python
result = mcp__google_search_console__inspect_url(
    site_url='https://www.smythson.com/',
    inspection_url='https://www.smythson.com/gb/leather-goods/diaries.html'
)

# Check verdict
verdict = result['inspectionResult']['indexStatusResult']['verdict']
# Possible values: PASS, PARTIAL, FAIL, NEUTRAL
```

### 4. mcp__google_search_console__list_sitemaps()

List all submitted sitemaps and their status.

**Parameters**:
- `site_url` (required): Property URL

**Example**:
```python
sitemaps = mcp__google_search_console__list_sitemaps(
    site_url='https://www.smythson.com/'
)

for sitemap in sitemaps['sitemaps']:
    print(f"{sitemap['path']}: {sitemap.get('isPending', False)}")
```

### 5. mcp__google_search_console__get_client_platform_ids()

⚠️ **Deprecated**: Use `mcp__platform-ids__get_client_platform_ids()` instead.

Legacy tool for looking up platform IDs from client CONTEXT.md files.

## Design Patterns Used

### Lazy OAuth Loading

OAuth modules imported inside tool functions (not at module level) to prevent startup popups:

```python
@mcp.tool
def list_sites(ctx: Context = None):
    # Import ONLY when tool is called
    from oauth.google_auth import get_headers_with_auto_token
    headers = get_headers_with_auto_token()
    # ... rest of function
```

This follows the pattern established in the December 16, 2025 OAuth popup fix.

### Platform IDs Integration

Optional integration with PetesBrain's centralised platform IDs system:
- Reads `PLATFORM_IDS_HELPER` and `CLIENT_IDS_PATH` from environment
- Dynamically imports `shared.platform_ids` helper if available
- Gracefully degrades if helper not found

### Error Handling

- Descriptive error messages for API failures
- Status code and response text included in exceptions
- Logging via Python logging module
- Context-aware messages via FastMCP Context object

### Pagination Support

`get_performance_data` supports pagination with `row_limit` and `start_row` parameters for large datasets (max 25,000 rows per request).

## Testing Status

✅ **Module Import**: Server loads successfully
✅ **FastMCP Registration**: All 5 tools registered
✅ **Configuration**: Added to ~/.claude.json with env vars
✅ **Dependencies**: All packages installed in venv
⏸️ **OAuth Flow**: Requires manual testing (will trigger on first API call)
⏸️ **API Calls**: Requires OAuth authentication to test live

## Next Steps for Testing

1. **First Use Authentication**:
   - Call `mcp__google_search_console__list_sites()` in Claude Code
   - OAuth flow will open browser
   - Authenticate with peter@roksys.co.uk
   - Verify token saved to server directory

2. **API Verification**:
   - Test `list_sites()` returns expected properties
   - Test `get_performance_data()` with recent date range
   - Test `inspect_url()` with known URL
   - Test `list_sitemaps()` returns sitemaps

3. **Client Integration**:
   - Add Search Console URLs to client CONTEXT.md files
   - Test platform IDs integration
   - Create example weekly search report workflow

## API Requirements

To use this server, you need:

1. **Google Cloud Project** with these APIs enabled:
   - Google Search Console API (webmasters)
   - Search Console URL Inspection API

2. **OAuth 2.0 Credentials**:
   - Type: Desktop application
   - Saved to: `/Users/administrator/Downloads/credentials.json`

3. **Site Verification**:
   - Sites must be verified in Google Search Console
   - User must have at least "Full" permission level

## Files Created

```
infrastructure/mcp-servers/google-search-console-mcp-server/
├── server.py                          # Main MCP server (430 lines)
├── oauth/
│   ├── __init__.py                    # Module exports
│   └── google_auth.py                 # OAuth authentication (145 lines)
├── requirements.txt                   # Dependencies
├── README.md                          # Full documentation (329 lines)
├── SETUP.md                           # Quick start guide (240 lines)
├── .env.example                       # Environment template
├── .env                               # Configuration (already existed)
├── .venv/                             # Virtual environment (already existed)
└── IMPLEMENTATION-SUMMARY.md          # This file
```

## Architecture Benefits

1. **No Startup Delays**: Lazy OAuth loading prevents authentication popups at Claude Code startup
2. **Token Persistence**: OAuth tokens cached in server directory for subsequent uses
3. **Automatic Refresh**: Expired tokens refreshed automatically
4. **Graceful Degradation**: Works without platform IDs helper
5. **Comprehensive Error Messages**: Clear debugging information
6. **Flexible Queries**: Support for multiple dimensions and pagination
7. **Real-time Data**: URL inspection checks live index status

## Integration with PetesBrain

The server follows PetesBrain conventions:

- **British English**: All documentation and comments use UK spelling
- **Platform IDs**: Integrates with centralised platform_ids.py helper
- **Client Context**: Designed to read Search Console URLs from CONTEXT.md
- **MCP Pattern**: Follows same structure as other Google MCP servers (Analytics, Ads)
- **OAuth Pattern**: Uses same OAuth implementation as Analytics server
- **Lazy Loading**: Prevents startup OAuth popups (critical requirement)

## Performance Considerations

- **API Rate Limits**: 1,200 queries/minute per project, 600/minute per user
- **Data Freshness**: Search performance data has 2-3 day delay
- **Date Range**: Limited to 16 months of historical data
- **Row Limits**: Max 25,000 rows per request (use pagination for larger datasets)
- **URL Inspection**: Real-time checks (no delay)

## Security

- OAuth tokens stored in server directory with restrictive permissions
- Credentials file referenced from Downloads folder (not in repository)
- Environment variables used for sensitive paths
- No API keys or secrets in code

## Status

**✅ READY TO USE**

The Google Search Console MCP server is fully implemented, configured, and ready for use. It will be available in Claude Code after restart or when MCP servers reconnect.

First API call will trigger OAuth authentication flow. All subsequent calls will use cached token.
