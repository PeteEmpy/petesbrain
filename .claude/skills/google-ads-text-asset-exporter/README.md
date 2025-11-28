# Google Ads Text Asset Exporter Skill

## Quick Start

Invoke this skill when you need to export Google Ads text assets (headlines, descriptions) to a Google Sheet for review.

## Usage

```
User: "Export text assets for [client] [campaign/filter]"
User: "Get the asset text for gifting campaigns"
User: "Create a review sheet for PMAX text assets"
```

## What It Does

1. Connects to Google Ads API
2. Extracts text assets from specified campaigns
3. Filters by keywords (optional)
4. Creates formatted Google Sheet with:
   - Organized by market and asset group
   - Blank separators for clarity
   - Approval dropdown column
   - Comments column for feedback

## Parameters You Can Specify

- **Client/Account**: "Smythson", "Uno Lighting", etc.
- **Campaigns**: Campaign names or "all PMAX"
- **Filter**: Keywords like "gift", "christmas", "brand", "hero"
- **Markets**: "UK", "US", "both", "all"

## Output Format

| Market | Campaign | Asset Group | Type | Text | Approval Status | Comments |
|--------|----------|-------------|------|------|----------------|----------|
| UK | Campaign Name | Asset Group | Headline 1 | Text here | [Dropdown] | |
| UK | Campaign Name | Asset Group | Headline 2 | Text here | [Dropdown] | |

## Example Sessions

### Export Gifting Assets
```
You: "Export the text assets for Smythson gifting campaigns"

Creates sheet with:
- UK Christmas Gifting for Him, Her, Heroes & Sidekicks
- US Christmas Gifting for Him, Her, Heroes & Sidekicks
- ~200 text assets total
- Formatted for easy review
```

### Export All Brand Assets
```
You: "Get all text assets from the UK brand campaign"

Creates sheet with:
- All asset groups from brand campaign
- Headlines, long headlines, descriptions
- Ready for marketing team review
```

## Files Created

### Working Scripts
- `export_text_assets_template.py` - Reference implementation
- Can be customized per client in `clients/[name]/scripts/`

### Output
- Google Sheet (shareable link provided)
- Temporary JSON files in `/tmp/` for debugging

## Dependencies

- Google Ads API access (google-ads.yaml configured)
- Google Drive OAuth credentials
- Python packages: google-ads-googleads, google-api-python-client

## Tips

1. **Use filters** to reduce data volume
2. **Specify markets** to separate UK/US reviews
3. **Blank rows** are added automatically between asset groups
4. **Dropdown validation** makes approval faster
5. **Can re-run** anytime to get latest assets

## Troubleshooting

- **"No assets found"**: Check campaign IDs and that asset groups are ENABLED
- **"Permission denied"**: Verify Google Drive OAuth credentials
- **"Too much data"**: Apply stricter filters or split by market

## Related

- Use with `google-ads-text-generator` to create new assets
- Part of Google Ads optimization workflow
- Supports marketing team collaboration
