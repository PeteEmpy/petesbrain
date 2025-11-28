# PMAX Asset Swap Tool

## Overview

The PMAX Asset Swap Tool safely replaces Performance Max text assets (headlines, long headlines, descriptions) in Google Ads campaigns. It handles the complete workflow from CSV input to execution with intelligent batching and safety validation.

## Core Functionality

**What it does:**
- Reads swap instructions from CSV files
- Matches assets by exact text
- Removes old assets and adds new ones atomically
- Handles maximum asset limits intelligently
- Provides dry-run mode for validation
- Generates detailed execution reports

**What it doesn't do:**
- Performance analysis (see Asset Text Optimisation Flow)
- AI text generation (see Asset Text Optimisation Flow)
- Campaign creation or structure changes

## File Structure

```
pmax-asset-optimiser/
├── execute_asset_optimisation.py    # Main execution script
├── asset_swap_engine.py              # Core swap logic
├── config.yaml                       # Configuration
├── output/                           # CSV files for review
└── logs/                            # Execution reports
```

## CSV Input Format

Required columns:
- `Original_Text`: Exact text of asset to replace
- `Asset_Type`: "Headline", "Long headline", or "Description"
- `Replacement_Text`: New text (must meet character limits)
- `Action`: "SWAP" (ready to execute) or "REVIEW" (skip)

Optional columns (for context):
- `Impressions`, `CTR`, `Conv_Rate`: Performance metrics
- `Flag_Reason`: Why this asset was flagged
- `Priority`: HIGH, MEDIUM, LOW
- `Char_Count`, `Char_Limit`, `Valid`: Validation info

Example:
```csv
Original_Text,Asset_Type,Replacement_Text,Action
"Black Friday Sale Ends Soon",Headline,"New Collection 2025",SWAP
"30% Off Leather Goods",Headline,"Luxury Leather Craftsmanship",SWAP
```

## Usage

### Step 1: Prepare CSV

Create a CSV with your swap instructions. The tool will:
1. Find the asset group containing each `Original_Text`
2. Remove the old asset
3. Create and link the new `Replacement_Text`

### Step 2: Dry Run (Recommended)

```bash
python3 execute_asset_optimisation.py \
  --customer-id 8573235780 \
  --campaign-id 12345678 \
  --csv output/my-swaps.csv \
  --dry-run
```

This validates:
- All assets can be found
- Character limits are met
- No minimum requirements violated
- Batching strategy is correct

### Step 3: Live Execution

```bash
python3 execute_asset_optimisation.py \
  --customer-id 8573235780 \
  --campaign-id 12345678 \
  --csv output/my-swaps.csv \
  --live
```

**Important:** Only assets with `Action=SWAP` will be processed.

## How It Works

### Asset Matching

The tool searches for assets by **exact text match** across all asset groups in the campaign:

```python
# Finds: "Black Friday Sale Ends Soon"
# Won't find: "Black Friday Sale Ends Soon!"  (extra punctuation)
# Won't find: "Black Friday Sale Ends"         (truncated)
```

### Swap Order Intelligence

The tool automatically selects the correct order based on current asset count:

**Below maximum limit:**
1. CREATE new asset
2. LINK new asset to group
3. REMOVE old asset

**At maximum limit (15 headlines / 5 long headlines / 5 descriptions):**
1. REMOVE old asset first (make room)
2. CREATE new asset
3. LINK new asset to group

This prevents "resource limit exceeded" errors.

### Batching Strategy

**Attempts batch execution when safe:**
- Groups swaps by (asset_group_id, field_type)
- Validates minimum requirements won't be violated
- Falls back to one-by-one if unsafe

**Safety checks:**
- Headlines: Minimum 3 required
- Long Headlines: Minimum 1 required
- Descriptions: Minimum 2 required

If removing all assets in a batch would go below minimum, executes one-by-one instead.

### Error Handling

**If swap fails:**
- Logs detailed error message
- Marks swap as failed in report
- Continues with remaining swaps
- Creates cleanup-needed assets are orphaned

**Common errors:**
- `Asset not found`: Original_Text doesn't match exactly
- `Resource limit exceeded`: Maximum assets reached (shouldn't happen with smart ordering)
- `Character limit exceeded`: Replacement text too long

## Execution Reports

Every run generates a JSON report in `logs/`:

```json
{
  "timestamp": "2025-11-25_12-10-15",
  "mode": "live",
  "customer_id": "8573235780",
  "csv_path": "output/my-swaps.csv",
  "results": {
    "processed": 25,
    "successful": 25,
    "failed": 0,
    "skipped": 0,
    "errors": []
  },
  "engine_log": [...]
}
```

## Character Limits

**Performance Max text asset limits:**
- Headlines: 30 characters maximum
- Long Headlines: 90 characters maximum
- Descriptions: 90 characters maximum

The tool validates these before execution. Invalid assets are skipped.

## Safety Features

1. **Dry-run mode:** Test without making changes
2. **Exact text matching:** Won't accidentally swap wrong asset
3. **Minimum validation:** Never violates Google Ads minimums
4. **Smart ordering:** Handles maximum limits correctly
5. **Detailed logging:** Full audit trail of every operation
6. **Action flag:** Only swaps assets marked `Action=SWAP`

## When Asset Order Changes

**Note:** After swapping, assets may appear in a different order in Google Ads UI. This is normal and doesn't affect performance.

**Why it happens:**
- Google Ads doesn't store a "position" field for assets
- Display order is determined by Google's internal sorting (usually alphabetical or by creation date)
- Performance Max uses machine learning to decide which assets to show - order doesn't matter

**If order matters to client:**
- Explain this is expected API behaviour
- Order can be manually adjusted in Google Ads UI (drag and drop)
- For full asset refreshes, consider manual UI approach instead

## Troubleshooting

### "Asset not found in campaign"

**Cause:** Original_Text doesn't exactly match any asset in the campaign

**Solutions:**
1. Check for extra spaces, punctuation, or capitalization differences
2. Use Google Ads UI to copy exact text
3. Search campaign for partial text to find actual wording

### "Resource limit exceeded"

**Cause:** Trying to link new asset when already at maximum (shouldn't happen with v1.1+)

**Solutions:**
1. This should be prevented by smart ordering - check logs
2. Verify asset counts in campaign
3. Report as bug if smart ordering isn't triggering

### "CSV has no swaps marked SWAP"

**Cause:** All assets in CSV have `Action=REVIEW`

**Solutions:**
1. Change `Action` column to `SWAP` for assets you want to replace
2. Use find/replace in spreadsheet editor
3. Re-export CSV

## Best Practices

1. **Always dry-run first** - catches errors before live execution
2. **Review HTML visualization** - generated alongside CSV for easy review
3. **Start small** - test with 1-2 swaps before bulk operations
4. **Backup current assets** - export via Google Ads before major swaps
5. **Check character counts** - tool validates, but verify in CSV first
6. **Set Action carefully** - only SWAP what you've reviewed

## Advanced: Campaign-Wide Swaps

For swapping across multiple campaigns/asset groups:

1. Create separate CSV per campaign (use `--campaign-id` filter)
2. Or include all in one CSV (tool auto-detects asset groups)
3. Group by asset group for batching efficiency

## Version History

- **v1.1** (2025-11-25): Added smart ordering for maximum limits, fixed REMOVE operation
- **v1.0** (2025-11-25): Initial release with batching and dry-run support
