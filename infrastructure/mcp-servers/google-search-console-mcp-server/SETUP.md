# Google Search Console MCP Server - Setup Guide

## Quick Start

The Google Search Console MCP server is **already configured and ready to use** in your Claude Code installation!

## Available Tools

You can now use these MCP tools in Claude Code:

```python
# List all verified sites
mcp__google_search_console__list_sites()

# Get search performance data
mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['query']
)

# Inspect a specific URL
mcp__google_search_console__inspect_url(
    site_url='https://www.smythson.com/',
    inspection_url='https://www.smythson.com/gb/leather-goods/diaries.html'
)

# List sitemaps
mcp__google_search_console__list_sitemaps(
    site_url='https://www.smythson.com/'
)

# Get client platform IDs (deprecated - use platform-ids server instead)
mcp__google_search_console__get_client_platform_ids('smythson')
```

## First Time Authentication

The first time you use any Search Console tool, you'll need to authenticate:

1. A browser window will open automatically
2. Sign in with your Google account (peter@roksys.co.uk)
3. Grant Search Console API access
4. Token will be saved for future use

**Note**: This OAuth flow will ONLY happen when you actually call a tool, not when Claude Code starts up (thanks to lazy loading).

## Configuration

The server is configured in `~/.claude.json`:

```json
{
  "mcpServers": {
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
}
```

## Enabling the API

If you haven't already, you'll need to enable the Google Search Console API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Enable these APIs:
   - **Google Search Console API** (webmasters API)
   - **Search Console URL Inspection API** (for URL inspection)
4. Make sure OAuth credentials are configured (Desktop application type)

## Verifying Setup

To verify everything is working:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server
.venv/bin/python -c "import server; print('✅ Server loads successfully')"
```

## Common Use Cases

### Weekly Search Performance Report

```python
# Get last 7 days of top queries
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-12-11',
    end_date='2025-12-18',
    dimensions=['query'],
    row_limit=50
)

# Analyse top queries by clicks
for row in sorted(data['rows'], key=lambda x: x['clicks'], reverse=True)[:10]:
    print(f"{row['keys'][0]}: {row['clicks']} clicks, {row['ctr']:.2%} CTR, pos {row['position']:.1f}")
```

### Compare Desktop vs Mobile Performance

```python
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['device']
)

for row in data['rows']:
    device = row['keys'][0]
    print(f"{device}: {row['clicks']} clicks, {row['impressions']} impressions")
```

### Find Top Landing Pages

```python
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['page'],
    row_limit=20
)

for row in data['rows']:
    print(f"{row['keys'][0]}: {row['clicks']} clicks")
```

### Check URL Indexing Status

```python
result = mcp__google_search_console__inspect_url(
    site_url='https://www.smythson.com/',
    inspection_url='https://www.smythson.com/gb/leather-goods/diaries.html'
)

verdict = result['inspectionResult']['indexStatusResult']['verdict']
print(f"Indexing status: {verdict}")
```

## Client Integration

Each client's `CONTEXT.md` file should include their Search Console property URL:

```markdown
**Search Console URL**: https://www.smythson.com/ (or sc-domain:smythson.com)
```

This allows the platform IDs helper to automatically provide the correct site URL for queries.

## Troubleshooting

### "Permission denied" error

Make sure the site is verified in Google Search Console:
https://search.google.com/search-console

### "Invalid site URL" error

Search Console URLs must be exact:
- **Property prefix**: `https://www.smythson.com/` (with trailing slash)
- **Domain property**: `sc-domain:smythson.com` (no protocol, no www)

Check the exact format in Search Console.

### OAuth token expired

The server will automatically refresh the token. If refresh fails, a new OAuth flow will start automatically.

### Rate limits

Search Console API limits:
- 1,200 queries per minute per project
- 600 queries per minute per user

If you hit limits, wait 60 seconds and retry.

## Next Steps

1. **Test with your sites**: Try listing sites first to verify authentication
2. **Add to client CONTEXT.md files**: Add Search Console URLs to each client's context
3. **Create analysis workflows**: Build regular search performance reports
4. **Monitor indexing**: Set up URL inspection checks for important pages

For full API documentation, see `README.md`.
