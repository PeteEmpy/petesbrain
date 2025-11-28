---
name: google-ads-text-asset-exporter
description: Extracts text assets (headlines, long headlines, descriptions) from Google Ads Performance Max campaigns and exports to a formatted Google Sheet. Use when user asks to "export text assets", "get PMAX assets", "create copy review sheet", or needs to extract ad copy for marketing review.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Read, Write, Bash
---

# Google Ads Text Asset Exporter Skill

## Instructions

When this skill is triggered:

### 1. Gather Requirements

Ask the user to clarify (if not already provided):
- **Client/Account**: Which Google Ads account?
- **Campaigns**: Specific campaign names or IDs (or all PMAX campaigns)
- **Filter**: Any keywords to filter asset groups? (e.g., "gift", "christmas", "brand")
- **Markets**: UK, US, or both?

### 2. Identify Account and Campaigns

```bash
# List available accounts
mcp__google-ads__list_accounts

# Find campaigns matching the criteria
mcp__google-ads__run_gaql with query:
SELECT campaign.name, campaign.id
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
AND campaign.status = 'ENABLED'
```

### 3. Extract Text Assets

Use the extraction script template:

```python
from google.ads.googleads.client import GoogleAdsClient
from collections import defaultdict
import json

client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

customer_id = 'CUSTOMER_ID'
campaign_ids = ['CAMPAIGN_ID_1', 'CAMPAIGN_ID_2']

def get_text_assets(customer_id, campaign_ids):
    # OPTIMIZATION: Use single query with IN clause instead of looping
    # This reduces API calls from N campaigns to 1 call = much faster
    campaign_ids_str = ', '.join(campaign_ids)

    query = f"""
        SELECT
            campaign.name,
            campaign.id,
            asset_group.name,
            asset_group.id,
            asset_group_asset.field_type,
            asset.text_asset.text
        FROM asset_group_asset
        WHERE
            campaign.id IN ({campaign_ids_str})
            AND asset_group.status = 'ENABLED'
            AND asset_group_asset.status = 'ENABLED'
            AND asset.type = 'TEXT'
        ORDER BY campaign.name, asset_group.name, asset_group_asset.field_type
    """

    response = ga_service.search(customer_id=customer_id, query=query)
    all_rows = list(response)

    # Organize by asset group
    asset_groups = defaultdict(lambda: {
        'campaign': '',
        'asset_group': '',
        'headlines': [],
        'long_headlines': [],
        'descriptions': []
    })

    for row in all_rows:
        ag_id = str(row.asset_group.id)
        field_type = row.asset_group_asset.field_type.name
        text = row.asset.text_asset.text

        asset_groups[ag_id]['campaign'] = row.campaign.name
        asset_groups[ag_id]['asset_group'] = row.asset_group.name

        if field_type == 'HEADLINE':
            asset_groups[ag_id]['headlines'].append(text)
        elif field_type == 'LONG_HEADLINE':
            asset_groups[ag_id]['long_headlines'].append(text)
        elif field_type == 'DESCRIPTION':
            asset_groups[ag_id]['descriptions'].append(text)

    return asset_groups

# Extract data
asset_groups = get_text_assets(customer_id, campaign_ids)
```

### 4. Format Data for Google Sheets

Build rows with structure:
- **Market** (UK/US/EUR/etc.)
- **Campaign**
- **Asset Group**
- **Type** (Headline 1, Long Headline 1, Description 1, etc.)
- **Text** (the actual asset text)
- **Approval Status** (dropdown: Approved/Needs Changes/Rejected)
- **Comments** (for reviewer feedback)

Apply filters if specified:
```python
# Example: Filter for gifting-related asset groups
gifting_keywords = ['gift', 'christmas', 'xmas', 'holiday']

filtered_rows = [header_row]
for row in all_rows:
    asset_group_name = row[2].lower()
    campaign_name = row[1].lower()

    is_match = any(keyword in asset_group_name or keyword in campaign_name
                   for keyword in filter_keywords)

    if is_match:
        filtered_rows.append(row)
```

Add blank separator rows between asset groups for clarity.

### 5. Create Google Sheet

Use the Google Drive MCP tool to create the sheet:

```python
import os
os.environ['GOOGLE_DRIVE_OAUTH_CREDENTIALS'] = '/path/to/gcp-oauth.keys.json'

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials and create sheet
# Upload data
# Apply formatting
```

**Formatting requirements:**
- Freeze header row
- Bold header with dark background, white text
- Auto-resize columns
- Add data validation dropdown to "Approval Status" column
- Add blank rows between asset groups

### 6. Report Results

Provide the user with:
- ✅ Google Sheet URL
- 📊 Summary: Number of asset groups, total rows, markets covered
- 📋 List of asset groups included
- 🎯 Any filters applied

## Example Usage

### Example 1: Export Gifting Assets
```
User: "Export the text assets for Smythson's gifting campaigns"

Assistant (using skill):
1. Asks: "Would you like UK, US, or both markets?"
2. Finds: SMY | UK | P Max | H&S Christmas Gifting campaign
3. Extracts: All text assets from active asset groups
4. Filters: Only asset groups containing "gift" or "christmas"
5. Creates: Google Sheet with 204 rows (6 asset groups)
6. Reports: "Created sheet with 3 UK + 3 US gifting asset groups"
```

### Example 2: Export Brand Campaign Assets
```
User: "Get all text assets from the UK brand campaign for review"

Assistant (using skill):
1. Finds: SMY | UK | P Max | Brand campaign
2. Extracts: All asset groups with their text assets
3. Creates: Formatted Google Sheet
4. Reports: "Exported 15 asset groups with 500+ text assets"
```

### Example 3: Export with Multiple Filters
```
User: "Export PMAX assets for Uno Lighting, filter for 'hero' asset groups only"

Assistant (using skill):
1. Identifies: Uno Lighting account
2. Finds: All PMAX campaigns
3. Filters: Asset groups containing "hero"
4. Creates: Sheet with filtered results
5. Reports: "Found 4 hero asset groups across 2 campaigns"
```

## File Locations

### Scripts
Create standalone script that can be reused:
```
clients/[client-name]/scripts/export_text_assets.py
```

### Temporary Data
```
/tmp/text_assets_data.json          # Raw extracted data
/tmp/text_assets_filtered.json      # After applying filters
```

### Google Sheet Output
Sheet is created in Google Drive with sharing enabled for the client's team.

## Error Handling

### Common Issues

1. **No campaigns found**
   - Verify customer ID is correct
   - Check that campaigns are ENABLED
   - Confirm PMAX channel type

2. **No text assets found**
   - Verify asset groups are ENABLED
   - Check campaigns have text assets added
   - Confirm correct campaign IDs

3. **Google Sheet creation fails**
   - Check OAuth credentials are valid
   - Verify Google Drive API is enabled
   - Ensure sufficient permissions

4. **Too much data (>1000 rows)**
   - Apply stricter filters
   - Export one market at a time
   - Split into multiple sheets

## Best Practices

1. **Use single query with IN clause** - Query all campaigns at once instead of looping (much faster)
2. **Always filter when possible** - Reduces clutter and makes review easier
3. **Add blank separator rows** - Improves visual clarity between asset groups
4. **Use descriptive sheet names** - Include client, date, and scope
5. **Enable dropdown validation** - Makes approval process faster
6. **Auto-resize columns** - Ensures all text is visible

## Integration Points

### Google Ads API
- Uses Google Ads GAQL queries
- Requires `google-ads.yaml` configuration
- Customer ID must have appropriate access level

### Google Drive/Sheets API
- Uses OAuth credentials from google-drive-mcp-server
- Creates spreadsheets with formatting
- Applies data validation rules

### Client Workflows
- Export assets → Marketing review → Feedback → Implementation
- Can be scheduled (e.g., weekly asset audits)
- Supports approval workflows

## Future Enhancements

- **Compare versions**: Show what changed between exports
- **Bulk upload**: Import approved changes back to Google Ads
- **Performance overlay**: Add CTR/conversion data per asset
- **AI suggestions**: Automatically flag weak copy
- **Multi-language**: Support for multiple markets simultaneously

## Related Skills

- `google-ads-text-generator`: Generate new text assets
- `google-ads-campaign-audit`: Broader campaign analysis
- `google-ads-keyword-audit`: Keyword-level review

## Performance Optimization Reference

See [google-ads-query-optimization-patterns.md](../google-ads-query-optimization-patterns.md) for reusable Google Ads API query optimization patterns. This skill implements:
- **Pattern 1**: IN clause for multiple campaigns (3-5x faster)
- **Pattern 3**: Minimal field selection
- **Pattern 7**: Asset status filtering (critical for accuracy)

## Notes

- Text assets include: Headlines (max 30 chars), Long Headlines (max 90 chars), Descriptions (max 90 chars)
- PMAX campaigns can have multiple asset groups
- Each asset group can have different combinations of text assets
- Google Ads allows up to 15 headlines, 5 long headlines, 4 descriptions per asset group
- The skill creates a review-ready format, not a bulk upload format
