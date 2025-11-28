# PMax Asset Application Workflow

Complete system for applying text and image assets from Google Spreadsheet to Smythson's Performance Max campaigns.

## Overview

This workflow automates the update of all text and image assets across 4 regional Google Ads accounts (UK, US, EUR, ROW) from a single master Google Spreadsheet.

## Files

### 1. Master Spreadsheet
**ID**: `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`

Contains 4 tabs:
- **UK ad copy** (26 rows)
- **US ad copy** (15 rows)
- **EUR ad copy** (12 rows)
- **ROW ad copy** (3 rows)

**Column Structure**:
- **A**: Campaign Name
- **B**: Asset Group Name
- **C-Q** (columns 3-17): Headlines 1-15 (max 30 chars each)
- **R-V** (columns 18-22): Long Headlines 1-5 (max 90 chars each)
- **W-AA** (columns 23-27): Descriptions 1-5 (max 90 chars each)
- **BA-BU** (columns 53-74): Image Asset IDs 1-21

### 2. Application Scripts

Located in `/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/`

#### apply-text-assets-from-sheet.py
Reads text assets from columns A-AA and applies to Google Ads.

**Usage**:
```bash
# Dry run for single region
python3 apply-text-assets-from-sheet.py --region uk --dry-run

# Live execution for single region
python3 apply-text-assets-from-sheet.py --region uk

# Dry run for all regions
python3 apply-text-assets-from-sheet.py --region all --dry-run
```

**What it does**:
1. Reads spreadsheet data for specified region
2. Finds asset group IDs by matching Campaign Name + Asset Group Name
3. Gets current text assets from Google Ads
4. Creates new text assets via Google Ads API
5. Links new assets to asset groups
6. Removes old asset links

**Requirements**:
- Minimum 3 headlines
- Minimum 1 long headline
- Minimum 2 descriptions
- Maximum 15 headlines, 5 long headlines, 5 descriptions

#### apply-image-assets-from-sheet.py
Reads image asset IDs from columns BA-BU and links to Google Ads.

**Usage**:
```bash
# Dry run for single region
python3 apply-image-assets-from-sheet.py --region uk --dry-run

# Live execution for single region
python3 apply-image-assets-from-sheet.py --region uk
```

**What it does**:
1. Reads campaign/asset group names from columns A-B
2. Reads image asset IDs from columns BA-BU
3. Finds asset group IDs by matching names
4. Removes existing image asset links
5. Links new image assets (as MARKETING_IMAGE type)

**Note**: This script ONLY links existing image assets. It does NOT create new images.

#### apply-all-assets.py
Orchestration script that runs both text and image application in sequence.

**Usage**:
```bash
# Dry run for all regions (recommended first)
python3 apply-all-assets.py --region all --dry-run

# Dry run for single region
python3 apply-all-assets.py --region uk --dry-run

# Live execution for all regions
python3 apply-all-assets.py --region all

# Live execution for single region
python3 apply-all-assets.py --region uk
```

**What it does**:
1. Runs text asset application
2. If text succeeds, runs image asset application
3. Reports overall success/failure

**Safety features**:
- 5-second countdown before live execution
- Skips image application if text fails
- Detailed reporting per region

### 3. Supporting Scripts

#### export-current-assets.py
Exports current text assets from Google Ads to JSON backup files.

**Usage**:
```bash
python3 export-current-assets.py --region uk
python3 export-current-assets.py --region all
```

**Output**: Creates dated JSON files in `data/asset-backups/`:
- `YYYY-MM-DD-uk-assets.json`
- `YYYY-MM-DD-us-assets.json`
- etc.

#### rollback-to-backup.py
Restores text assets from JSON backups to Google Ads.

**Usage**:
```bash
# Dry run
python3 rollback-to-backup.py --region uk --dry-run

# Live execution
python3 rollback-to-backup.py --region uk
```

#### Asset Library Browser
Universal tool for visually browsing and selecting image assets from Google Ads Asset Library.

**Location**: `/Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py`

**Usage**:
```bash
# UK region
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 8573235780 --manager-id 2569949686

# US region
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 7808690871 --manager-id 2569949686

# EUR region
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 7679616761 --manager-id 2569949686

# ROW region
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 5556710725 --manager-id 2569949686
```

**What it does**:
1. Queries all image assets from the Google Ads account
2. Gets current usage information for each image
3. Automatically categorizes images by product type (Bags, Notebooks, etc.)
4. Generates standalone HTML file with hierarchical category grouping
5. Auto-opens in browser for immediate viewing

**Output**: Creates HTML files in `/Users/administrator/Documents/PetesBrain/output/`:
- `asset-library-browser-{customer_id}-YYYY-MM-DD.html`

**Features**:
- **Category grouping** - Images organized into collapsible categories (Bags, Notebooks, Wallets, etc.)
- **Expand/Collapse All** buttons for quick navigation
- **Visual thumbnails** of all images
- **Click Asset ID to copy** to clipboard
- **Search** by Asset ID, name, or dimensions
- **Filter** by usage (all/used/unused)
- **Usage tracking** - Shows where each image is currently used
- **Smart categorization** - Automatically detects product types from asset names

**Categories detected**:
- Bags, Notebooks & Diaries, Wallets & Accessories
- Writing Instruments, Home & Office, Tech Accessories
- Men's Products, Women's Products
- Gifts & Seasonal, Black Friday, Seasonal Collections
- Logos & Branding, Other Assets, Unnamed Assets

**Use case**: When populating image asset IDs in columns BA-BU of the activation spreadsheet, use this tool to visually browse and select the images you want. Much faster than navigating the Google Ads UI.

**Workflow**:
1. Generate browser for desired region (see commands above)
2. Browser opens automatically showing all images grouped by category
3. Click category headers to expand/collapse sections
4. Visually browse images by category
5. Click Asset ID to copy it
6. Paste into activation spreadsheet columns BA-BU

**Statistics** (as of 2025-11-26):
- **UK**: 3,700 images (278 currently in use)
- **ROW**: 751 images (168 currently in use)

## Regional Configuration

### UK
- **Customer ID**: 8573235780
- **Asset Groups**: 26
- **Max Images**: 20 per group

### US
- **Customer ID**: 7808690871
- **Asset Groups**: 15
- **Max Images**: 12 per group

### EUR
- **Customer ID**: 7679616761
- **Asset Groups**: 12
- **Max Images**: 20 per group

### ROW (Rest of World)
- **Customer ID**: 5556710725
- **Asset Groups**: 3
- **Max Images**: 3 per group

## Complete Workflow

### Pre-Execution Verification (CRITICAL - Do First)

**Before running any scripts, verify the Google Spreadsheet is correctly set up.**

1. **Read spreadsheet data**:
   ```python
   # Check text assets (columns A-AA)
   mcp__google-sheets__read_cells(
       spreadsheet_id='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g',
       range_name='UK ad copy!A1:AA2'
   )

   # Check image assets (columns BA-BU)
   mcp__google-sheets__read_cells(
       spreadsheet_id='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g',
       range_name='UK ad copy!BA1:BU2'
   )
   ```

2. **Verify campaign and asset group names match Google Ads EXACTLY**:
   - Check for extra spaces
   - Check for case sensitivity
   - Verify campaign names haven't changed

3. **Validate all image asset IDs exist in the target account**:
   ```python
   # Example for UK account
   mcp__google-ads__run_gaql(
       customer_id='8573235780',
       manager_id='2569949686',
       query='''
           SELECT asset.id, asset.name, asset.type
           FROM asset
           WHERE asset.id IN ([list of image IDs from spreadsheet])
               AND asset.type = 'IMAGE'
       '''
   )
   ```

4. **Verify minimum requirements met**:
   - ✅ At least 3 headlines per row
   - ✅ At least 1 long headline per row
   - ✅ At least 2 descriptions per row
   - ✅ All image IDs are valid (if using images)

5. **Check for duplicate asset group names across accounts**:
   - Ensure Campaign + Asset Group combination is unique
   - Watch for similar names across UK/US/EUR/ROW

**If ANY verification fails, STOP and fix the spreadsheet before proceeding.**

---

### Pre-Execution (Tuesday Morning)

1. **Create backup** (CRITICAL):
   ```bash
   cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts
   python3 export-current-assets.py --region all
   ```

2. **Verify backups created**:
   ```bash
   ls -lh data/asset-backups/2025-*
   ```

3. **Final dry-run check with validation**:
   ```bash
   python3 apply-all-assets.py --region all --dry-run
   ```

   Expected output:
   ```
   Regions processed: 4
   Successful: 4 ['uk', 'us', 'eur', 'row']
   Failed: 0 []
   ```

4. **Review validation output for each asset group**:
   - Check that each asset group shows "✅ Validation passed"
   - Look for any "❌ VALIDATION FAILED" messages
   - Verify image distribution (landscape/square/portrait counts)

   Example passing validation:
   ```
   Validating image type requirements...
   ✅ Validation passed - Image distribution:
      Landscape: 2
      Square: 3
      Portrait: 4
   ```

   Example failing validation:
   ```
   ❌ VALIDATION FAILED: New images don't meet PMax requirements
   Missing required types: MARKETING_IMAGE, SQUARE_MARKETING_IMAGE
   Current distribution:
     - Landscape (MARKETING_IMAGE): 0
     - Square (SQUARE_MARKETING_IMAGE): 0
     - Portrait (PORTRAIT_MARKETING_IMAGE): 1
   Fix: Add missing image types to the spreadsheet before running.
   ```

5. **Fix any validation failures**:
   - Open spreadsheet and locate the failing asset group
   - Add missing image types (landscape or square)
   - Use Asset Library Browser to find suitable images
   - Re-run dry-run until all validations pass

### Live Execution (Tuesday)

1. **Execute application**:
   ```bash
   python3 apply-all-assets.py --region all
   ```

2. **Monitor progress**:
   - Watch for "✅ SUCCESS" per region
   - Check for any errors or failures

3. **Verify in Google Ads UI**:
   - Spot-check a few asset groups
   - Confirm text assets updated
   - Confirm image assets linked

### Post-Execution Verification

1. **Check asset counts** in Google Ads UI
2. **Verify campaign performance** doesn't drop significantly
3. **Keep backups** for at least 7 days

### Emergency Rollback

If something goes wrong:

```bash
# Rollback single region
python3 rollback-to-backup.py --region uk --dry-run
python3 rollback-to-backup.py --region uk

# Rollback all regions
python3 rollback-to-backup.py --region all
```

## Common Issues and Fixes

### Issue: Asset group not found

**Symptom**: Script reports "✗ Asset group not found in Google Ads"

**Cause**: Campaign Name or Asset Group Name in spreadsheet doesn't match Google Ads exactly

**Fix**:
1. Run GAQL query to get exact names:
   ```python
   SELECT campaign.name, asset_group.name
   FROM asset_group
   WHERE campaign.id = CAMPAIGN_ID
   ```
2. Update spreadsheet column A or B with exact match
3. Watch for:
   - Extra spaces (e.g., "ROW  |" vs "ROW |")
   - Missing prefixes (e.g., "Travel Bags" vs "Black Friday Travel Bags")
   - Ampersands vs "and"

### Issue: Not enough headlines/descriptions

**Symptom**: Script reports "ERROR: Not enough headlines (X < 3)"

**Cause**: Spreadsheet has fewer than minimum required assets

**Fix**: Add more text assets to meet minimums:
- Headlines: minimum 3
- Long Headlines: minimum 1
- Descriptions: minimum 2

### Issue: Too many assets

**Symptom**: Script reports "WARNING: Too many headlines (X > 15), truncating"

**Cause**: Spreadsheet has more than maximum allowed assets

**Fix**: Script automatically truncates to maximums. Review which assets are being truncated.

### Issue: Python module not found

**Symptom**: `ModuleNotFoundError: No module named 'dotenv'`

**Cause**: Scripts must run using Google Ads MCP server venv Python

**Fix**: Scripts now have correct shebang:
```python
#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
```

Make executable: `chmod +x *.py`

## Data Quality Checks

Before execution, verify spreadsheet data:

1. **Campaign names** match Google Ads exactly
2. **Asset group names** match Google Ads exactly
3. **No extra spaces** in names
4. **Image asset IDs** are valid (12-digit numbers)
5. **Text assets** meet character limits:
   - Headlines: 1-30 chars
   - Long Headlines: 1-90 chars
   - Descriptions: 1-90 chars

## Technical Details

### Authentication
Uses OAuth 2.0 via Google Ads MCP server:
- **Path**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server`
- **Manager ID**: 2569949686

### Google Ads API Version
**v22**

### API Endpoints Used
1. **googleAds:search** - Query campaigns, asset groups, assets
2. **assets:mutate** - Create new text assets
3. **assetGroupAssets:mutate** - Link/unlink assets to/from asset groups

### Google Sheets API
Uses Google Sheets MCP server OAuth credentials:
- **Path**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server`

## Dry Run Test Results (2025-11-26)

Final dry-run test completed successfully:

```
Regions processed: 4
Successful: 4 ['uk', 'us', 'eur', 'row']
Failed: 0 []
```

**UK**: 26/26 asset groups ✅
**US**: 15/15 asset groups ✅
**EUR**: 12/12 asset groups ✅
**ROW**: 3/3 asset groups ✅

**Total**: 56/56 asset groups ready for live execution ✅

## Execution Order

When using `--region all`, regions process in this order:
1. UK (largest, 26 groups)
2. US (15 groups)
3. EUR (12 groups)
4. ROW (smallest, 3 groups)

This ensures any issues surface early with the largest region.

## Performance

Typical execution times (dry-run):
- **ROW**: ~6 seconds (3 groups)
- **EUR**: ~13 seconds (12 groups)
- **US**: ~9 seconds (15 groups)
- **UK**: ~13 seconds (26 groups)
- **All regions**: ~42 seconds total

Live execution adds ~2-3 seconds per group for API calls.

## Key Features (Added 2025-11-28)

### Image Validation System
**Pre-execution validation prevents failures before making changes:**

1. **Automatic field type detection** - Queries image dimensions and assigns correct PMax field type:
   - Landscape (MARKETING_IMAGE): ratio > 1.1
   - Square (SQUARE_MARKETING_IMAGE): ratio 0.9-1.1
   - Portrait (PORTRAIT_MARKETING_IMAGE): ratio 0.7-0.9

2. **Type requirement validation** - Checks each asset group has:
   - At least 1 landscape image (required)
   - At least 1 square image (required)
   - Portrait is optional

3. **Clear error messages** - Shows exactly what's missing:
   ```
   ❌ VALIDATION FAILED: New images don't meet PMax requirements
   Missing required types: MARKETING_IMAGE, SQUARE_MARKETING_IMAGE
   Current distribution:
     - Landscape (MARKETING_IMAGE): 0
     - Square (SQUARE_MARKETING_IMAGE): 0
     - Portrait (PORTRAIT_MARKETING_IMAGE): 1
   Fix: Add missing image types to the spreadsheet before running.
   ```

4. **Deduplication** - Automatically removes duplicate image IDs within same asset group
   - Prevents DUPLICATE_RESOURCE API errors
   - Example: 9 IDs in spreadsheet with 1 duplicate → 8 unique images applied

5. **Overflow protection** - Handles cases where current + new images > 20 limit
   - Smart batch removal: removes just enough old images first
   - Adds all new images
   - Removes remaining old images

### Safety Features

1. **Add-before-remove strategy** - Never leaves asset group empty
2. **Validation gates** - Stops execution if requirements not met
3. **Dry-run validation** - Catches issues before live execution
4. **Idempotent operations** - Safe to re-run if interrupted

## Tuesday Execution Guide

**For step-by-step instructions on running the December 2nd asset swap, see:**

📋 **[TUESDAY-EXECUTION-GUIDE.md](./TUESDAY-EXECUTION-GUIDE.md)**

Quick start:
```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

# 1. Create backups
python3 export-current-assets.py --region all

# 2. Dry run with validation
python3 apply-all-assets.py --region all --dry-run

# 3. Fix any validation failures in spreadsheet

# 4. Live execution (when ready)
python3 apply-all-assets.py --region all
```

## Contact

For issues or questions:
- Check TUESDAY-EXECUTION-GUIDE.md for execution steps
- Review this documentation for technical details
- Review script output for specific errors
- Use dry-run mode to test changes safely
