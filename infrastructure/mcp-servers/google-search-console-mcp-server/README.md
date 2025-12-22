# Google Search Console MCP Server

MCP server providing Google Search Console API integration for PetesBrain.

## Features

### Available Tools

1. **list_sites** - List all verified sites/properties in Search Console
2. **get_performance_data** - Query Search Analytics data (clicks, impressions, CTR, position)
3. **inspect_url** - Inspect specific URLs for indexing status and issues
4. **list_sitemaps** - List all sitemaps for a site
5. **get_client_platform_ids** - Look up client platform IDs from CONTEXT.md (deprecated - use platform-ids MCP server)

## Setup

### 1. Install Dependencies

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure OAuth Credentials

You need OAuth credentials for Google Search Console API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable "Google Search Console API"
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the JSON file
6. Save to `/Users/administrator/Downloads/google-oauth-config.json`

### 3. Configure Environment

Create `.env` file:

```bash
# OAuth Configuration Path
GOOGLE_SEARCH_CONSOLE_OAUTH_CONFIG_PATH=/Users/administrator/Downloads/google-oauth-config.json

# Optional: Platform IDs Helper
PLATFORM_IDS_HELPER=/Users/administrator/Documents/PetesBrain.nosync/shared/platform_ids.py
CLIENT_IDS_PATH=/Users/administrator/Documents/PetesBrain.nosync/clients
```

### 4. Add to Claude Code

```bash
claude mcp add -s user google-search-console \
  "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server/.venv/bin/python" \
  "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server/server.py"
```

Or manually add to `.mcp.json`:

```json
{
  "mcpServers": {
    "google-search-console": {
      "command": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server/.venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-search-console-mcp-server/server.py"
      ],
      "env": {
        "GOOGLE_SEARCH_CONSOLE_OAUTH_CONFIG_PATH": "/Users/administrator/Downloads/google-oauth-config.json",
        "PLATFORM_IDS_HELPER": "/Users/administrator/Documents/PetesBrain.nosync/shared/platform_ids.py",
        "CLIENT_IDS_PATH": "/Users/administrator/Documents/PetesBrain.nosync/clients"
      }
    }
  }
}
```

## Usage Examples

### List All Verified Sites

```python
# Get all sites you have access to
sites = mcp__google_search_console__list_sites()
print(f"Found {sites['count']} sites")
for site in sites['sites']:
    print(f"- {site['siteUrl']} ({site['permissionLevel']})")
```

### Get Performance Data

```python
# Get query performance for last 30 days
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['query'],
    row_limit=100
)

for row in data['rows']:
    print(f"Query: {row['keys'][0]}")
    print(f"  Clicks: {row['clicks']}")
    print(f"  Impressions: {row['impressions']}")
    print(f"  CTR: {row['ctr']:.2%}")
    print(f"  Position: {row['position']:.1f}")
```

### Get Performance by Page

```python
# Get page performance
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['page'],
    row_limit=50
)
```

### Get Performance by Device

```python
# Compare desktop vs mobile
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['device']
)
```

### Multiple Dimensions

```python
# Get queries by device
data = mcp__google_search_console__get_performance_data(
    site_url='https://www.smythson.com/',
    start_date='2025-11-18',
    end_date='2025-12-18',
    dimensions=['query', 'device'],
    row_limit=100
)
```

### Inspect URL

```python
# Check if URL is indexed
result = mcp__google_search_console__inspect_url(
    site_url='https://www.smythson.com/',
    inspection_url='https://www.smythson.com/gb/leather-goods/diaries.html'
)

# Check indexing status
index_status = result['inspectionResult']['indexStatusResult']
print(f"Verdict: {index_status['verdict']}")
print(f"Coverage state: {index_status['coverageState']}")
if 'crawledAs' in index_status:
    print(f"Crawled as: {index_status['crawledAs']}")
```

### List Sitemaps

```python
# Get all sitemaps for a site
sitemaps = mcp__google_search_console__list_sitemaps(
    site_url='https://www.smythson.com/'
)

for sitemap in sitemaps['sitemaps']:
    print(f"Sitemap: {sitemap['path']}")
    print(f"  Type: {sitemap.get('type', 'unknown')}")
    print(f"  Last submitted: {sitemap.get('lastSubmitted', 'never')}")
    print(f"  Status: {sitemap.get('isPending', False)}")
```

## Available Dimensions

For `get_performance_data`, you can use the following dimensions:

- **query** - Search queries
- **page** - Landing pages
- **country** - Countries (ISO codes)
- **device** - Device types (DESKTOP, MOBILE, TABLET)
- **searchAppearance** - How the result appeared (e.g., VIDEO, IMAGE)
- **date** - Date (YYYY-MM-DD)

You can combine up to 3 dimensions in a single query.

## Authentication

The server uses OAuth 2.0 with lazy loading to prevent startup popups:

1. First API call triggers OAuth flow if needed
2. Browser opens for Google authentication
3. Token saved to `token.json` in server directory
4. Subsequent calls use cached token
5. Token auto-refreshes when expired

## Troubleshooting

### OAuth popup appears

This is normal on first use. Just authenticate in the browser. The token will be cached for future use.

### "Permission denied" errors

Make sure you've verified ownership of the site in Google Search Console first. Go to:
https://search.google.com/search-console

### API quota exceeded

Search Console API has rate limits:
- 1,200 queries per minute per project
- 600 queries per minute per user

If you hit limits, wait a minute and try again.

### Token expired

The server automatically refreshes expired tokens. If refresh fails, it will trigger a new OAuth flow.

## API Documentation

- [Search Console API Overview](https://developers.google.com/webmaster-tools/search-console-api-original)
- [Search Analytics API](https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics)
- [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [Sitemaps API](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sitemaps)

## Notes

- Date ranges are limited to 16 months of data
- Row limits: 1-25,000 rows per request
- Use pagination (start_row) for large result sets
- Performance data may have a 2-3 day delay
- URL inspection checks live index status (real-time)
