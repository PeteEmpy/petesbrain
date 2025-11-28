# MCP Server Integrations - Detailed Reference

**Pete's Brain** uses Model Context Protocol (MCP) servers to integrate with external services. These provide Claude Code with direct access to APIs and data sources.

## Google Ads MCP Server

**Location**: `infrastructure/mcp-servers/google-ads-mcp-server/`
**Purpose**: Query Google Ads data using GAQL, run keyword planner, create/modify campaigns
**Configuration**: `.mcp.json` (OAuth2 credentials required)
**Status**: Read operations active since launch, **Write operations added 2025-11-14**

### Tools Available

#### Read Operations (Active since launch)

##### mcp__google-ads__list_accounts
List all accessible Google Ads accounts including nested sub-accounts.

##### mcp__google-ads__run_gaql
Execute GAQL queries using the non-streaming search endpoint for consistent JSON parsing.

**Parameters**:
- `customer_id` (required): The Google Ads customer ID (10 digits, no dashes)
- `query` (required): GAQL query string
- `manager_id` (optional): Manager ID if access type is 'managed'

##### mcp__google-ads__run_keyword_planner
Generate keyword ideas using Google Ads KeywordPlanIdeaService.

**Parameters**:
- `customer_id` (required): The Google Ads customer ID
- `keywords` (required): A list of seed keywords to generate ideas from
- `manager_id` (optional): Manager ID if access type is 'managed'
- `page_url` (optional): Page URL related to your business
- `start_year`, `start_month` (optional): Start date for historical data
- `end_year`, `end_month` (optional): End date for historical data

**Note**: At least one of 'keywords' or 'page_url' must be provided.

##### mcp__google-ads__get_client_platform_ids
Get Google Ads, Merchant Centre, and GA4 IDs for a specific client from CONTEXT.md.

**Parameters**:
- `client_name` (required): Client name (e.g., 'smythson', 'tree2mydoor')

---

#### Write Operations (Added 2025-11-14)

**Purpose**: Enable internal Google Ads campaign automation (alternative to third-party tools like Markifact)
**Documentation**: `/roksys/knowledge-base/ai-strategy/2025-11-14-google-ads-campaign-automation-feasibility.md`

##### mcp__google-ads__create_campaign
Create a new Google Ads campaign with budget and bidding strategy.

**Parameters**:
- `customer_id` (required): Google Ads customer ID (10 digits, no dashes)
- `campaign_name` (required): Name for the new campaign
- `daily_budget_micros` (required): Daily budget in micros (£100 = 100,000,000 micros)
- `target_roas` (optional): Target ROAS for bidding (e.g., 4.0 for 400% ROAS)
- `target_cpa_micros` (optional): Target CPA in micros (£10 = 10,000,000 micros)
- `locations` (optional): List of location constants (defaults to UK: 'geoTargetConstants/2826')
- `campaign_type` (optional): SEARCH, DISPLAY, SHOPPING, VIDEO, PERFORMANCE_MAX (default: SEARCH)
- `status` (optional): PAUSED (default), ENABLED
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: campaign_id, campaign_resource_name, budget_resource_name, Google Ads UI link

**Example**:
```python
mcp__google-ads__create_campaign(
    customer_id="1234567890",
    campaign_name="Brand Search | UK | Main",
    daily_budget_micros=50000000,  # £50/day
    target_roas=4.0,  # 400% ROAS target
    locations=["geoTargetConstants/2826"],
    campaign_type="SEARCH",
    status="PAUSED"
)
```

##### mcp__google-ads__create_ad_group
Create a new ad group in a campaign.

**Parameters**:
- `customer_id` (required): Google Ads customer ID
- `campaign_id` (required): Campaign ID (numeric, e.g., "12345")
- `ad_group_name` (required): Name for the ad group
- `cpc_bid_micros` (optional): Max CPC bid in micros (£2 = 2,000,000 micros)
- `status` (optional): ENABLED (default), PAUSED
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: ad_group_id, ad_group_resource_name

##### mcp__google-ads__create_responsive_search_ad
Create a Responsive Search Ad (RSA) in an ad group.

**Parameters**:
- `customer_id` (required): Google Ads customer ID
- `ad_group_id` (required): Ad group ID (numeric)
- `headlines` (required): List of 3-15 headline strings (max 30 characters each)
- `descriptions` (required): List of 2-4 description strings (max 90 characters each)
- `final_urls` (required): List of final URLs (landing pages)
- `path1` (optional): Display path 1 (max 15 characters)
- `path2` (optional): Display path 2 (max 15 characters)
- `status` (optional): ENABLED (default), PAUSED
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: ad_id, ad_resource_name, headlines_count, descriptions_count

**Example**:
```python
mcp__google-ads__create_responsive_search_ad(
    customer_id="1234567890",
    ad_group_id="54321",
    headlines=[
        "Luxury leather diaries",
        "Handcrafted in London",
        "Free UK delivery"
    ],
    descriptions=[
        "Shop our collection of premium leather diaries. Made in England.",
        "Personalisation available. Next day delivery on all orders."
    ],
    final_urls=["https://example.com/diaries"],
    path1="diaries",
    path2="luxury"
)
```

##### mcp__google-ads__add_keywords
Add keywords to an ad group.

**Parameters**:
- `customer_id` (required): Google Ads customer ID
- `ad_group_id` (required): Ad group ID (numeric)
- `keywords` (required): List of keyword dictionaries with 'text' and 'match_type'
  - Match types: EXACT, PHRASE, BROAD
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: keywords_added count, keyword_resource_names

**Example**:
```python
mcp__google-ads__add_keywords(
    customer_id="1234567890",
    ad_group_id="54321",
    keywords=[
        {"text": "leather diary", "match_type": "EXACT"},
        {"text": "luxury diary", "match_type": "PHRASE"},
        {"text": "notebook", "match_type": "BROAD"}
    ]
)
```

##### mcp__google-ads__add_sitelinks
Add sitelink extensions to a campaign.

**Parameters**:
- `customer_id` (required): Google Ads customer ID
- `campaign_id` (required): Campaign ID (numeric)
- `sitelinks` (required): List of sitelink dictionaries with 'text', 'url', optional 'description1', 'description2'
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: sitelinks_added count, asset_resource_names

**Example**:
```python
mcp__google-ads__add_sitelinks(
    customer_id="1234567890",
    campaign_id="98765",
    sitelinks=[
        {
            "text": "Shop Diaries",
            "url": "https://example.com/diaries",
            "description1": "Premium leather",
            "description2": "Made in England"
        },
        {
            "text": "Free Delivery",
            "url": "https://example.com/delivery",
            "description1": "Next day shipping",
            "description2": "On all orders"
        }
    ]
)
```

##### mcp__google-ads__add_callouts
Add callout extensions to a campaign.

**Parameters**:
- `customer_id` (required): Google Ads customer ID
- `campaign_id` (required): Campaign ID (numeric)
- `callouts` (required): List of callout text strings (max 25 characters each)
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: callouts_added count, asset_resource_names

**Example**:
```python
mcp__google-ads__add_callouts(
    customer_id="1234567890",
    campaign_id="98765",
    callouts=[
        "Free UK delivery",
        "Made in England",
        "Premium leather",
        "Personalisation available",
        "Next day shipping",
        "Gift wrapping"
    ]
)
```

##### mcp__google-ads__create_asset_group
Create an asset group for a Performance Max campaign (text assets only). Use this to add asset groups to existing Performance Max campaigns.

**Parameters**:
- `customer_id` (required): Google Ads customer ID
- `campaign_id` (required): Performance Max campaign ID (numeric) - can be existing or newly created
- `asset_group_name` (required): Name for the asset group
- `final_urls` (required): List of landing page URLs (at least 1)
- `headlines` (required): List of 3-5 headlines (max 30 characters each)
- `long_headlines` (required): List of 1-5 long headlines (max 90 characters each)
- `descriptions` (required): List of 2-5 descriptions (max 90 characters each)
- `business_name` (required): Business name (max 25 characters)
- `call_to_action` (optional): LEARN_MORE (default), SHOP_NOW, SIGN_UP, etc.
- `path1` (optional): Display path 1 (max 15 characters)
- `path2` (optional): Display path 2 (max 15 characters)
- `status` (optional): ENABLED (default), PAUSED
- `manager_id` (optional): Manager account ID if using managed access

**Returns**: asset_group_id, asset_group_resource_name, text_assets_summary, Google Ads UI link

**Example**:
```python
mcp__google-ads__create_asset_group(
    customer_id="1234567890",
    campaign_id="98765",  # Existing Performance Max campaign
    asset_group_name="Leather Diaries",
    final_urls=["https://example.com/diaries"],
    headlines=[
        "Luxury leather diaries",
        "Handcrafted in London",
        "Free UK delivery"
    ],
    long_headlines=[
        "Shop our collection of luxury leather diaries"
    ],
    descriptions=[
        "Premium leather diaries handcrafted in London. Free UK delivery on all orders.",
        "Personalisation available. Next day delivery. Shop now."
    ],
    business_name="Example Leather",
    call_to_action="SHOP_NOW",
    path1="diaries",
    path2="luxury"
)
```

**Note**: Images and videos must be added manually via Google Ads UI after creation. This tool creates the text-only foundation.

**Common use case**: Add multiple asset groups to a single Performance Max campaign, each targeting different product categories or landing pages.

---

## Google Analytics MCP Server

**Location**: Configured in `.mcp.json`
**Purpose**: Query GA4 properties for traffic and conversion data
**Configuration**: `.mcp.json` (OAuth2 credentials required)

**⚠️ IMPORTANT**: The `GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH` environment variable MUST be set in `.mcp.json` to prevent OAuth popup on every startup. See [Troubleshooting docs](TROUBLESHOOTING.md#oauth-popup-on-every-claude-code-startup) for details.

### Tools Available

#### mcp__google-analytics__list_properties
List all Google Analytics 4 accounts with their associated properties in a hierarchical structure.

**Parameters**:
- `account_id` (optional): Specific GA account ID to list properties for

#### mcp__google-analytics__get_page_views
Get page view metrics for a specific date range.

**Parameters**:
- `property_id` (required): GA4 property ID (numeric, e.g., "123456789")
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `dimensions` (optional): List of dimensions to group by (defaults to ["pagePath"])

#### mcp__google-analytics__get_active_users
Get active users metrics for a specific date range.

**Parameters**:
- `property_id` (required): GA4 property ID
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `dimensions` (optional): List of dimensions to group by (defaults to ["date"])

#### mcp__google-analytics__get_events
Get event metrics for a specific date range.

**Parameters**:
- `property_id` (required): GA4 property ID
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `dimensions` (optional): List of dimensions to group by (defaults to ["eventName"])

#### mcp__google-analytics__get_traffic_sources
Get traffic source metrics for a specific date range.

**Parameters**:
- `property_id` (required): GA4 property ID
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `dimensions` (optional): List of dimensions to group by (defaults to ["source", "medium"])

#### mcp__google-analytics__get_device_metrics
Get device metrics for a specific date range.

**Parameters**:
- `property_id` (required): GA4 property ID
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `dimensions` (optional): List of dimensions to group by (defaults to ["deviceCategory"])

#### mcp__google-analytics__run_report
Execute a comprehensive GA4 report with full customization capabilities.

**Parameters**:
- `property_id` (required): GA4 property ID (numeric)
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `metrics` (required): Array of metric names as STRINGS (e.g., ["sessions", "totalUsers"])
- `dimensions` (optional): Array of dimension names as STRINGS
- `limit` (optional): Maximum number of rows (default: 100)
- `offset` (optional): Number of rows to skip (default: 0)
- `order_bys` (optional): Sorting configuration
- `dimension_filter` (optional): Filter for dimensions
- `metric_filter` (optional): Filter for metrics
- `keep_empty_rows` (optional): Include empty rows

**Valid GA4 Metrics**: sessions, totalUsers, activeUsers, newUsers, screenPageViews, pageviews, bounceRate, engagementRate, averageSessionDuration, userEngagementDuration, engagedSessions, conversions, totalRevenue, purchaseRevenue, eventCount, eventsPerSession

**Valid GA4 Dimensions**: country, city, region, continent, deviceCategory, operatingSystem, browser, source, medium, campaignName, sessionDefaultChannelGroup, pagePath, pageTitle, landingPage, date, month, year, hour, dayOfWeek, sessionSource, sessionMedium, sessionCampaignName

---

## Google Sheets MCP Server

**Location**: `shared/mcp-servers/google-sheets-mcp-server/`
**Purpose**: Read/write Google Sheets data, automated exports
**Configuration**: Service account credentials in `credentials.json`

### Tools Available

#### mcp__google-sheets__list_sheets
Lists all sheets (tabs) in a specific Google Spreadsheet.

**Parameters**:
- `spreadsheet_id` (required): The spreadsheet ID from the URL

#### mcp__google-sheets__read_cells
Reads data from a specified range in a Google Sheet.

**Parameters**:
- `spreadsheet_id` (required): The spreadsheet ID
- `range_name` (required): Range in A1 notation (e.g., "Sheet1!A1:D10")

#### mcp__google-sheets__write_cells
Writes data to a specified range in a Google Sheet.

**Parameters**:
- `spreadsheet_id` (required): The spreadsheet ID
- `range_name` (required): Range in A1 notation
- `values` (required): 2D array of values to write

### Automated Exports

The Google Sheets MCP server includes automated exports:

- **What**: Exports ROK Experiments sheet every 6 hours
- **Output**: `roksys/spreadsheets/*.csv` files
- **Script**: `shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.googlesheets.export.plist`
- **Files generated**:
  - `rok-experiments-client-notes.csv` - Timestamped experiment log
  - `rok-experiments-client-list.csv` - Simple list of all ROK clients

---

## Google Tasks MCP Server

**Location**: `shared/mcp-servers/google-tasks-mcp-server/`
**Purpose**: Manage Google Tasks lists and tasks
**Configuration**: OAuth2 credentials (prompts on first use)
**Setup**: Run `./setup.sh` to install dependencies and configure

### Tools Available

#### mcp__google-tasks__list_task_lists
Lists all task lists in Google Tasks.

#### mcp__google-tasks__create_task_list
Creates a new task list.

**Parameters**:
- `title` (required): Task list title

#### mcp__google-tasks__list_tasks
Lists all tasks in a specific task list.

**Parameters**:
- `tasklist_id` (required): Task list ID
- `show_completed` (optional): Show completed tasks (default: false)

#### mcp__google-tasks__create_task
Creates a new task in Google Tasks.

**Parameters**:
- `tasklist_id` (required): Task list ID
- `title` (required): Task title
- `notes` (optional): Task notes/description
- `due` (optional): Due date in ISO format

#### mcp__google-tasks__update_task
Updates an existing task.

**Parameters**:
- `tasklist_id` (required): Task list ID
- `task_id` (required): Task ID
- `title` (optional): New task title
- `notes` (optional): New task notes
- `due` (optional): New due date
- `status` (optional): Task status

#### mcp__google-tasks__complete_task
Marks a task as completed.

**Parameters**:
- `tasklist_id` (required): Task list ID
- `task_id` (required): Task ID

#### mcp__google-tasks__delete_task
Deletes a task.

**Parameters**:
- `tasklist_id` (required): Task list ID
- `task_id` (required): Task ID

### Use Cases
- Create action items from meeting notes
- Track client deliverables and deadlines
- Manage project tasks and follow-ups

---

## Google Drive MCP Server

**Location**: `shared/mcp-servers/google-drive-mcp-server/`
**Purpose**: Bulletproof Google Docs/Drive integration for importing documents to client folders
**Configuration**: `.mcp.json` (OAuth2 credentials required, NPX-based)
**Status**: ⏳ Configured, awaiting OAuth setup
**Setup Guide**: `shared/mcp-servers/google-drive-mcp-server/SETUP_CHECKLIST.md`

### Tools Available

#### File Management
- `mcp__google-drive__search` - Search files across entire Drive
- `mcp__google-drive__listFolder` - Browse folder contents
- `mcp__google-drive__createTextFile` - Create new text/markdown files
- `mcp__google-drive__updateTextFile` - Update existing files
- `mcp__google-drive__createFolder` - Create folders
- `mcp__google-drive__deleteItem` - Delete files/folders (moves to trash)
- `mcp__google-drive__renameItem` - Rename items
- `mcp__google-drive__moveItem` - Move to different folder

#### Google Docs
- `mcp__google-drive__createGoogleDoc` - Create new Google Doc
- `mcp__google-drive__updateGoogleDoc` - Update Google Doc content
- `mcp__google-drive__getGoogleDocContent` - Get content with text indices for formatting
- `mcp__google-drive__formatGoogleDocText` - Apply text formatting (bold, italic, colors, etc.)
- `mcp__google-drive__formatGoogleDocParagraph` - Apply paragraph formatting (alignment, spacing, styles)

#### Google Sheets
- `mcp__google-drive__createGoogleSheet` - Create new Sheet
- `mcp__google-drive__updateGoogleSheet` - Update Sheet data
- `mcp__google-drive__getGoogleSheetContent` - Get content with cell information
- `mcp__google-drive__formatGoogleSheetCells` - Format cells (background, borders, alignment)
- `mcp__google-drive__formatGoogleSheetText` - Apply text formatting
- `mcp__google-drive__formatGoogleSheetNumbers` - Apply number formatting
- `mcp__google-drive__setGoogleSheetBorders` - Set borders for cells
- `mcp__google-drive__mergeGoogleSheetCells` - Merge cells
- `mcp__google-drive__addGoogleSheetConditionalFormat` - Add conditional formatting

#### Google Slides
- `mcp__google-drive__createGoogleSlides` - Create presentation
- `mcp__google-drive__updateGoogleSlides` - Update existing presentation
- `mcp__google-drive__getGoogleSlidesContent` - Get content with element IDs
- `mcp__google-drive__formatGoogleSlidesText` - Apply text formatting
- `mcp__google-drive__formatGoogleSlidesParagraph` - Apply paragraph formatting
- `mcp__google-drive__styleGoogleSlidesShape` - Style shapes
- `mcp__google-drive__setGoogleSlidesBackground` - Set background color
- `mcp__google-drive__createGoogleSlidesTextBox` - Create text box
- `mcp__google-drive__createGoogleSlidesShape` - Create shape

### File Conversions (automatic)
- Google Docs → Markdown
- Google Sheets → CSV
- Google Slides → Plain text
- PDFs → Text extraction

### Common Workflows

**Import Single Google Doc**:
```
User: "Add this Google Doc to [client-name]: [Google Docs URL]"
```

Claude Code will:
- Fetch document (auto-converted to Markdown)
- Save to `clients/[client-name]/documents/[filename].md`
- Add YAML frontmatter with metadata (source URL, date, etc.)

**Import Multiple Docs from Folder**:
```
User: "Import all Google Docs from this folder to Smythson: [folder URL]"
```

Claude Code will:
- List all files in folder
- Filter for Google Docs
- Import each to `clients/smythson/documents/`

**Search and Import**:
```
User: "Find Google Docs about 'Q4 strategy' and import relevant ones to clients/"
```

### Setup Required (one-time, ~25 minutes)

1. Google Cloud Console setup (create OAuth credentials)
2. Enable APIs: Drive, Docs, Sheets, Slides
3. Run authentication: `npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json`
4. Restart Claude Code

**Documentation**:
- Setup guide: `shared/mcp-servers/google-drive-mcp-server/SETUP.md`
- Checklist: `shared/mcp-servers/google-drive-mcp-server/SETUP_CHECKLIST.md`
- Upstream repo: https://github.com/piotr-agier/google-drive-mcp

---

## Google Photos MCP Server

**Location**: `shared/mcp-servers/google-photos-mcp-server/`
**Purpose**: Access Google Photos library for album browsing, photo search, metadata extraction, and downloads
**Configuration**: `.mcp.json` (OAuth2 credentials required)
**Status**: ✅ Fully implemented, ready for setup

### Tools Available

#### mcp__google-photos__list_albums
List all albums in your Google Photos library.

**Parameters**:
- `page_size` (integer, optional): Number of albums to return (default: 50, max: 50)
- `page_token` (string, optional): Token for pagination (from previous response)

**Returns**:
```json
{
  "albums": [
    {
      "id": "album-id-123",
      "title": "Vacation 2024",
      "productUrl": "https://photos.google.com/album/...",
      "mediaItemsCount": "42",
      "coverPhotoBaseUrl": "https://..."
    }
  ],
  "nextPageToken": "token-for-next-page"
}
```

#### mcp__google-photos__get_album
Get details for a specific album.

**Parameters**:
- `album_id` (string, required): Album ID

#### mcp__google-photos__list_album_contents
List all media items (photos/videos) in a specific album.

**Parameters**:
- `album_id` (string, required): Album ID
- `page_size` (integer, optional): Number of items to return (default: 100, max: 100)
- `page_token` (string, optional): Token for pagination

**Returns**:
```json
{
  "mediaItems": [
    {
      "id": "media-id-456",
      "filename": "IMG_1234.jpg",
      "mimeType": "image/jpeg",
      "productUrl": "https://photos.google.com/photo/...",
      "baseUrl": "https://lh3.googleusercontent.com/...",
      "creationTime": "2024-06-15T14:30:00Z",
      "width": "4032",
      "height": "3024",
      "photo": {
        "cameraMake": "Apple",
        "cameraModel": "iPhone 14 Pro",
        "focalLength": 6.86,
        "apertureFNumber": 1.78,
        "isoEquivalent": 64
      }
    }
  ],
  "nextPageToken": null
}
```

#### mcp__google-photos__search_media
Search for media items with optional filters (date range, media type, album).

**Parameters**:
- `album_id` (string, optional): Filter by album ID
- `start_date` (string, optional): Start date in YYYY-MM-DD format
- `end_date` (string, optional): End date in YYYY-MM-DD format
- `media_types` (array, optional): Filter by type - `["PHOTO"]`, `["VIDEO"]`, or `["ALL_MEDIA"]`
- `page_size` (integer, optional): Number of items to return (default: 100, max: 100)
- `page_token` (string, optional): Token for pagination

**Example**:
```python
# Find photos from July 2024
mcp__google-photos__search_media(
    start_date="2024-07-01",
    end_date="2024-07-31",
    media_types=["PHOTO"]
)
```

#### mcp__google-photos__get_media_item
Get full details for a specific media item (photo or video).

**Parameters**:
- `media_item_id` (string, required): Media item ID

**Returns**: Complete metadata including EXIF data (camera, ISO, aperture, etc.), dimensions, timestamps, URLs

#### mcp__google-photos__download_media
Generate time-limited download URL for a media item with optional resizing.

**Parameters**:
- `media_item_id` (string, required): Media item ID
- `width` (integer, optional): Resize width (max 16383)
- `height` (integer, optional): Resize height (max 16383)

**Returns**:
```json
{
  "mediaItem": { ... },
  "downloadUrl": "https://lh3.googleusercontent.com/...=d",
  "instructions": "Use this URL to download the media item. URL expires after 60 minutes."
}
```

**Note**: Download URLs expire after 60 minutes. Generate new URL if needed.

### Common Use Cases

**Browse photo library**:
```
List all my Google Photos albums
```

**Search by date**:
```
Find photos I took in October 2024
```

**Get album contents**:
```
Show me all photos in my "Vacation 2024" album
```

**Extract EXIF metadata**:
```
What camera was used for photo [photo-id]?
```

**Download photos**:
```
Get download URLs for all photos in album [album-name]
```

### API Limits

- **Free tier**: 10,000 requests per day
- **Rate limit**: 10 requests per second per user
- **Download URLs**: Expire after 60 minutes (regenerate as needed)
- **Pagination**: Albums (50 per page), Media items (100 per page)

### Setup Required (one-time, ~10 minutes)

1. **GCP Setup**: Create OAuth credentials and enable Google Photos Library API
2. **Run setup**: `./setup-oauth.sh` (creates venv, installs dependencies, runs OAuth flow)
3. **Add to .mcp.json**: Configure server in Claude Code
4. **Restart Claude Code**

**Documentation**:
- Quick start: `shared/mcp-servers/google-photos-mcp-server/QUICKSTART.md`
- Complete guide: `shared/mcp-servers/google-photos-mcp-server/README.md`
- GCP setup: `shared/mcp-servers/google-photos-mcp-server/GCP-SETUP-GUIDE.md`
- Installation complete: `shared/mcp-servers/google-photos-mcp-server/INSTALLATION-COMPLETE.md`

### Features

- ✅ **OAuth 2.0** authentication with automatic token refresh
- ✅ **Read-only access** - Cannot modify or delete photos (safe)
- ✅ **Pagination support** for large libraries
- ✅ **EXIF metadata** extraction (camera, settings, location)
- ✅ **Album management** - List, browse, search albums
- ✅ **Date filtering** - Find photos by date range
- ✅ **Media type filtering** - Photos vs videos
- ✅ **Download URLs** - Time-limited, optionally resized
- ✅ **Comprehensive error handling** with helpful messages
- ✅ **Complete documentation** with examples

---

## WooCommerce MCP Server

**Location**: `shared/mcp-servers/woocommerce-mcp-server/`
**Purpose**: Query WooCommerce product data and manage e-commerce operations
**Configuration**: `.mcp.json` (Node.js based, requires API credentials)

### Environment Variables

- `WORDPRESS_SITE_URL` - WooCommerce site URL
- `WOOCOMMERCE_CONSUMER_KEY` - WooCommerce API consumer key
- `WOOCOMMERCE_CONSUMER_SECRET` - WooCommerce API consumer secret

### Use Cases

- Product data analysis for Google Shopping campaigns
- Inventory tracking for campaign optimization
- Product feed generation
