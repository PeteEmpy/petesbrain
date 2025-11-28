# Google Ads Asset Library Browser

Universal tool for visually browsing and selecting image assets from any Google Ads account.

## Overview

The Asset Library Browser creates an interactive HTML page that displays all image assets from a Google Ads account, organized by automatically detected categories. This makes it easy to visually browse and select asset IDs without navigating through the Google Ads UI.

## Location

```
/Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py
```

## Features

### Visual Browsing
- **Image thumbnails** - See actual images, not just names and IDs
- **Category grouping** - Images automatically organized by product type
- **Collapsible sections** - Expand/collapse categories for easier navigation
- **Grid layout** - View multiple images at once

### Search & Filter
- **Text search** - Filter by Asset ID, name, or dimensions
- **Usage filter** - Show all images, only used, or only unused
- **Real-time filtering** - Results update as you type
- **Category counts** - See how many images match in each category

### Asset Information
- **Asset ID** - Click to copy to clipboard
- **Asset name** - From Google Ads Asset Library
- **Dimensions** - Width × Height in pixels
- **Usage tracking** - Shows where each image is currently used
- **Usage count** - Visual badge showing number of uses

### Categories Detected

The tool automatically categorizes images based on their names:

| Category | Detected Keywords |
|----------|------------------|
| Bags | bag, bags, tote, clutch, briefcase, backpack, handbag |
| Notebooks & Diaries | notebook, notebooks, diary, diaries, journal, planner |
| Wallets & Accessories | wallet, cardholder, purse, passport |
| Writing Instruments | pen, pencil, writing |
| Home & Office | home, desk, office |
| Tech Accessories | tech, ipad, iphone, airpod, device, laptop, tablet |
| Plants & Nature | plant, tree, flower, garden, seed |
| Food & Beverage | food, coffee, drink, beverage |
| Men's Products | mens, men's, male |
| Women's Products | womens, women's, female, ladies |
| Gifts & Seasonal | gift, stocking, xmas, christmas, holiday |
| Black Friday | black friday, bf_, blackfriday, bfcm |
| Seasonal Collections | ss20, ss21, ss22, aw20, aw21, aw22, etc. |
| Logos & Branding | logo, brand, icon |
| Other Assets | Named assets not matching above categories |
| Unnamed Assets | Assets without names |

## Usage

### Basic Usage

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 1234567890
```

### With Manager Account

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 1234567890 \
    --manager-id 9876543210
```

### Custom Output Directory

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 1234567890 \
    --output-dir /path/to/output
```

## Client Examples

### Smythson

```bash
# UK (3,700 images)
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 8573235780 --manager-id 2569949686

# US
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 7808690871 --manager-id 2569949686

# EUR
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 7679616761 --manager-id 2569949686

# ROW (751 images)
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 5556710725 --manager-id 2569949686
```

### Tree2MyDoor

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 4941701449
```

## Output

The tool creates an HTML file in the output directory:

**Default location**: `/Users/administrator/Documents/PetesBrain/output/`

**Filename format**: `asset-library-browser-{customer_id}-{date}.html`

**Example**: `asset-library-browser-8573235780-2025-11-26.html`

The HTML file:
- Is fully self-contained (no external dependencies)
- Opens automatically in your default browser
- Can be saved and shared
- Works offline after generation

## How It Works

### Step 1: Query Assets

Uses Google Ads API v22 to query all image assets:

```sql
SELECT
    asset.id,
    asset.name,
    asset.image_asset.full_size.url,
    asset.image_asset.full_size.width_pixels,
    asset.image_asset.full_size.height_pixels,
    asset.image_asset.mime_type
FROM asset
WHERE asset.type = 'IMAGE'
```

### Step 2: Query Usage

Finds where each asset is currently used in Performance Max campaigns:

```sql
SELECT
    asset.id,
    campaign.name,
    asset_group.name,
    asset_group_asset.field_type
FROM asset_group_asset
WHERE asset_group_asset.field_type IN ('MARKETING_IMAGE',
    'SQUARE_MARKETING_IMAGE', 'PORTRAIT_MARKETING_IMAGE', 'LOGO')
AND asset_group_asset.status = 'ENABLED'
AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

### Step 3: Categorize

Analyzes asset names using keyword matching to assign categories.

### Step 4: Generate HTML

Creates a responsive HTML page with:
- Embedded CSS for styling
- Embedded JavaScript for interactivity
- Image URLs from Google's CDN
- Lazy loading for performance

## Use Cases

### 1. Performance Max Asset Selection

**Scenario**: Populating image asset IDs in a spreadsheet for bulk asset updates

**Workflow**:
1. Generate browser for the account
2. Browse images by category
3. Click Asset ID to copy
4. Paste into spreadsheet

### 2. Asset Audit

**Scenario**: Review which images are used vs. unused

**Workflow**:
1. Generate browser
2. Filter by "Not used"
3. Review unused assets for potential removal or activation

### 3. Client Asset Review

**Scenario**: Show client which images are in their account

**Workflow**:
1. Generate browser
2. Share HTML file with client
3. Client can browse and provide feedback

### 4. Asset Naming Analysis

**Scenario**: Identify assets that need better naming

**Workflow**:
1. Generate browser
2. Check "Unnamed Assets" category
3. Identify assets to rename in Google Ads UI

## Technical Details

### Authentication

Uses OAuth 2.0 via Google Ads MCP server:
- Path: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server`
- Credentials automatically loaded from `.env` file

### API Version

Google Ads API v22

### Dependencies

- Python 3.x
- `requests` library
- `python-dotenv` library
- Google Ads MCP server OAuth module

All dependencies are included in the Google Ads MCP server virtual environment.

### Performance

Typical execution times:
- Query 750 assets: ~2 seconds
- Query 3,700 assets: ~2 seconds
- HTML generation: <1 second
- Total: 2-3 seconds for most accounts

### Browser Compatibility

The generated HTML works in:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Any modern browser with JavaScript enabled

## Limitations

### Known Limitations

1. **Folder structure not available** - Google Ads API does not expose Asset Library folder organization
2. **Labels not available** - Asset labels are UI-only, not accessible via API
3. **Images must exist** - Tool only browses existing assets, cannot create new ones
4. **Performance Max focus** - Usage tracking only covers Performance Max campaigns

### Workarounds

**For folder organization**: The automatic categorization provides similar functionality by grouping based on naming patterns.

**For labels**: Use consistent naming conventions that the categorization can detect.

## Troubleshooting

### Images Not Loading

**Problem**: Some images show "Image unavailable"

**Cause**: Google Ads may restrict access to certain image URLs

**Solution**: This is expected for a small percentage of images; the Asset ID is still available to copy

### Authentication Errors

**Problem**: Script fails with OAuth error

**Cause**: Google Ads API credentials need refreshing

**Solution**: Run the OAuth refresh process for the Google Ads MCP server

### Category Detection Issues

**Problem**: Images categorized incorrectly

**Cause**: Asset names don't contain recognizable keywords

**Solution**:
1. Use the search function to find images by other attributes
2. Consider renaming assets in Google Ads UI for better categorization
3. Images will appear in "Other Assets" or "Unnamed Assets" categories

## Future Enhancements

Potential improvements:
- Add download functionality for images
- Export selected Asset IDs to CSV
- Support for video assets
- Custom category definitions via config file
- Multi-account comparison view

## Related Tools

- **Google Ads Text Asset Exporter** - Export text assets from Performance Max campaigns
- **Google Ads Asset Group Manager** - Bulk update asset groups
- **PMax Asset Application Scripts** - Apply assets from spreadsheet to campaigns

## Support

For issues or questions:
1. Check this documentation
2. Review script output for specific errors
3. Verify Google Ads API credentials are valid
4. Test with a smaller account first

## Version History

- **2025-11-26** - Initial universal version created
  - Client-independent functionality
  - Automatic categorization
  - Hierarchical grouping
  - Usage tracking
  - Search and filter capabilities
