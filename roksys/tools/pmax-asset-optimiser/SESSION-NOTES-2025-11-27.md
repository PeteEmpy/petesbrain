# PMAX Asset Optimiser Session Notes - 27 November 2025

## Session Summary

**P0 TASK COMPLETED**: Tree2mydoor URL-Based Review Sheet Upload

Successfully regenerated and uploaded the complete URL-based PMAX asset review sheet with all 154 underperforming assets (up from 92 in the previous version).

## What Was Accomplished

### 1. Identified the Issue
- **Previous upload (26 Nov)**: Only 92 assets in Google Sheets
- **Root cause**: Script was reading from old file `replacement-candidates-with-hierarchy.csv`
- **New data available**: 154 underperformers with URL-based product context

### 2. Fixed the Script
**File Modified**: `create_review_sheet.py`
- **Line 14**: Changed input from `replacement-candidates-with-hierarchy.csv` → `replacement-candidates.csv`
- **Result**: Now reads the latest URL-based data (462 rows = 154 assets × 3 options)

### 3. Regenerated Review Sheet
**Output**: `output/tree2mydoor-review-sheet.csv`
- **Rows**: 155 (1 header + 154 data rows)
- **Format**: Devonshire format - one row per asset with 3 options side-by-side
- **Breakdown**:
  - HIGH priority: 95 assets (62%)
  - MEDIUM priority: 59 assets (38%)
  - Total: 154 assets

### 4. Uploaded to Google Sheets
**Spreadsheet ID**: `1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI`
- **Sheet**: "Replacement Candidates"
- **Cells updated**: 2,170 cells (155 rows × 14 columns)
- **Upload time**: 27 Nov 2025
- **Status**: ✅ SUCCESSFUL

## Key Improvements Over Previous Version

### More Assets (92 → 154)
The original 92-asset version was incomplete. The new version includes all underperforming assets identified by the performance analysis.

### URL-Based Product Context
Each replacement is generated with the correct product context extracted from the landing page URL:
- Olive tree assets → Olive tree copy (Mediterranean, patio, peace symbolism)
- Lemon tree assets → Citrus tree copy (conservatory, fresh lemons)
- Memorial roses → Sympathy/remembrance copy
- Anniversary roses → Milestone celebration copy

**Previously**: AI was sometimes generating lemon tree copy for olive tree assets, or Christmas tree copy for memorial roses.

**Now**: Product context is explicitly passed to AI via landing page URL, ensuring accurate, product-specific replacements.

## Google Sheet Details

**URL**: https://docs.google.com/spreadsheets/d/1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI/edit

**Columns**:
1. Campaign - Campaign name
2. Asset Group - Asset group name
3. Priority - HIGH/MEDIUM
4. Asset Type - Headline/Long headline/Description
5. Current Text - Underperforming text
6. Impressions - Total impressions
7. CTR - Click-through rate
8. Conv Rate - Conversion rate
9. Issue - Why it's underperforming (Low CTR, Low Conv Rate, High Cost/Conv)
10. Option 1 - First replacement suggestion
11. Option 2 - Second replacement suggestion
12. Option 3 - Third replacement suggestion
13. Selected Option (1/2/3 or blank to skip) - **USER FILLS THIS IN**
14. Notes - Optional user notes

## Next Steps for Client (Gareth)

1. **Open the sheet**: https://docs.google.com/spreadsheets/d/1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI/edit
2. **Review each row**: Look at the 3 replacement options
3. **Select preferred option**: In column "Selected Option (1/2/3 or blank to skip)", enter:
   - `1` = Use Option 1
   - `2` = Use Option 2
   - `3` = Use Option 3
   - Leave blank = Skip this asset (don't change)
4. **Add notes** (optional): Any specific feedback in "Notes" column
5. **Notify when complete**: Let me know when ready to execute the asset swaps

## Execution Plan (After Client Review)

Once Gareth has made selections:

```bash
cd /Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser

# Download reviewed sheet from Google Sheets as CSV
# Save as: output/tree2mydoor-reviewed-selections.csv

# Execute swaps (dry-run first)
python3 execute_asset_optimisation.py --dry-run

# If dry-run looks good, execute live
python3 execute_asset_optimisation.py --live
```

## Files Generated

```
/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/output/
├── asset-performance-4941701449-2025-11-26.csv      # API fetch with URLs (560 assets)
├── underperforming-assets.csv                        # 154 underperformers with URLs
├── replacement-candidates.csv                        # 462 alternatives (URL-based)
└── tree2mydoor-review-sheet.csv                     # 154 assets in review format
```

## Technical Details

### URL-Based Product Extraction
The `generate_replacement_text.py` script extracts product context from landing page URLs:

- `/collections/olive-trees` → "olive trees (Mediterranean olive varieties for patios)"
- `/collections/lemon-trees` → "lemon trees (citrus trees for patios and conservatories)"
- `/collections/anniversary-gifts` → "anniversary tree and plant gifts"
- `/collections/memorial-rose-bushes` → "rose bushes (memorial and sympathy roses)"

This ensures AI generates product-appropriate copy for each asset.

### Batching for Performance
Assets are batched by `(Asset Group URL, Asset Type)` to avoid duplicate AI calls:
- 154 underperformers → 23 batched AI calls
- **6x performance improvement** vs individual calls
- Processing time: ~2 minutes

## Customer IDs
- **Tree2mydoor**: 4941701449
- **Campaign**: T2MD | P Max | HP&P 150 5/9 140 23/10 (ID: 15820346778)

## Task Status
✅ **P0 Task Complete** - Tree2mydoor PMAX Asset Optimiser URL-Based Review Sheet Upload

## Session End Time
27 November 2025, ~10:30
