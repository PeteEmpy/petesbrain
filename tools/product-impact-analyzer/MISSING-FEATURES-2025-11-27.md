# Product Impact Analyzer - Missing Features Report

**Date**: 27 November 2025
**Reporter**: User observation
**Issue**: "I'm looking at that spreadsheet and there's still no labels on it. I'm still not seeing any flagging of issues. You said there was potentially more than one sheet that should have been in there and there isn't."

---

## What You Expected to See

Based on the system name "Product Impact Analyzer" and the configuration showing `product_performance_spreadsheet_id` for each client, you expected:

1. **Multiple tabs** in each client spreadsheet:
   - Daily Performance (Google Ads metrics) ✅ EXISTS
   - Product Changes (price, title, availability changes) ❌ MISSING
   - Disapprovals (Merchant Centre issues) ❌ MISSING
   - Product Labels (custom_label tracking) ❌ MISSING

2. **Flagging of issues** - Visual indicators showing:
   - Products with disapprovals
   - Products with landing page errors
   - Products that changed price
   - Products that went out of stock
   - Products with performance drops

---

## What Actually Exists

### Just Bin Bags Spreadsheet: `1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA`

**Current State:**
- **Only 1 tab**: "Sheet1" (should be named "Daily Performance")
- **Contents**: Google Ads performance data (impressions, clicks, conversions, revenue) by product and date
- **Last updated**: 24 Nov 08:45 (before system broke)
- **Data source**: `product-data-fetcher` agent

**Missing Tabs:**
1. ❌ Product Changes
2. ❌ Disapprovals
3. ❌ Product Labels

---

## What Data IS Being Collected (But Not Displayed)

### 1. Product Changes ✅ Collected, ❌ Not in Spreadsheet

**Location**: `/tools/product-impact-analyzer/data/product_changes/Just Bin Bags/2025-11-25.json`

**Data Collected**:
- 4 availability changes detected on 25 Nov:
  - Nitrile Gloves Small: in stock → out of stock
  - Documents Enclosed Wallets: out of stock → in stock
  - Coloured Bin Bags: out of stock → in stock
  - Blue Vinyl Gloves Large: in stock → out of stock

**Also tracks**:
- Price changes
- Sale price changes
- Title changes
- Description changes
- Image changes
- Product type changes
- Brand/GTIN/MPN changes
- Custom label changes
- New products added
- Products removed

**Problem**: `product_change_detector.py` saves to JSON files but **never writes to Google Sheets**

---

### 2. Disapprovals ✅ Can Be Collected, ❌ Not in Spreadsheet

**Source**: Google Merchant Centre Content API v2.1

**Current Status** (checked 27 Nov):
- Just Bin Bags: 0 disapprovals
- 121 products, all approved

**Historical Status**:
- 18 Nov: 6 landing page errors (task created)
- Between 18-27 Nov: Unknown (system was broken)
- 27 Nov: 0 errors (confirmed via API)

**Problem**: No script exists to write disapproval data to spreadsheets. The `merchant_center_tracker.py` script fetches data but only logs to console, doesn't update sheets.

---

### 3. Product Labels ⚠️ Partially Implemented

**Configuration** (from config.json):
```json
"label_tracking": {
  "enabled": false,
  "label_field": "custom_label_0",
  "notes": "Limited Product Hero labels detected"
}
```

**Status for Just Bin Bags**: Disabled (limited labels in feed)

**Problem**: Even when enabled, label changes are tracked in JSON but not written to spreadsheets.

---

## The Architecture Gap

### What Exists (4 Automated Agents)

1. **product-data-fetcher** (every 6 hours)
   - ✅ Fetches Google Ads performance data
   - ✅ Writes to Google Sheets (Sheet1 / "Daily Performance")
   - ✅ Working perfectly

2. **product-monitor** (every 6 hours)
   - ✅ Compares current performance vs 30-day baseline
   - ✅ Detects revenue drops, revenue spikes, click drops
   - ✅ Writes alerts to Google Sheets
   - ✅ Working perfectly

3. **product-tracking** (daily 7:45 AM)
   - ✅ Fetches products from Merchant Centre API
   - ✅ Saves snapshots to JSON files
   - ✅ Runs `product_change_detector.py` to compare snapshots
   - ❌ **NEVER WRITES TO GOOGLE SHEETS**

4. **product-impact-analyzer** (Tuesday 9:00 AM)
   - ✅ Generates weekly impact analysis reports
   - ✅ Correlates product changes with performance shifts
   - ❌ **NEVER WRITES TO GOOGLE SHEETS**

### What's Missing

**No "Spreadsheet Writer" component** - There's no script that takes the JSON data from product changes and disapprovals and writes it to the per-client spreadsheets.

---

## Why This Happened

Looking at the LaunchAgent configuration:

```xml
<string>cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer &amp;&amp;
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json
.venv/bin/python3 product_feed_tracker.py &amp;&amp;
sleep 60 &amp;&amp;
.venv/bin/python3 product_change_detector.py</string>
```

This runs:
1. `product_feed_tracker.py` - Fetches from Merchant Centre, saves to JSON
2. `product_change_detector.py` - Compares snapshots, saves to JSON

**Missing step**:
3. `product_changes_to_sheets.py` - **DOESN'T EXIST**

---

## What Needs to Be Built

### Option 1: Build Complete Spreadsheet Writer

Create `product_changes_to_sheets.py` that:

1. **Creates missing tabs** in each client spreadsheet:
   - "Product Changes" tab
   - "Disapprovals" tab
   - "Product Labels" tab (if enabled)

2. **Writes product changes** from JSON to "Product Changes" tab:
   - Headers: Date | Product ID | Product Title | Change Type | Old Value | New Value
   - One row per change
   - Color coding: Red for out of stock, green for back in stock, orange for price increases

3. **Writes disapprovals** from Merchant Centre to "Disapprovals" tab:
   - Headers: Date First Seen | Product ID | Product Title | Issue Code | Issue Description | Status
   - Updates status when issue resolves
   - Highlights landing page errors in red

4. **Writes label changes** (if enabled) to "Product Labels" tab:
   - Headers: Date | Product ID | Product Title | Label Field | Old Label | New Label

### Option 2: Extend Existing Scripts

Modify `product_change_detector.py` to:
- Accept optional `--write-to-sheets` flag
- Read `product_performance_spreadsheet_id` from config
- Create tabs if they don't exist
- Write changes to appropriate tabs

### Option 3: Create Separate "Sync to Sheets" Agent

Create new LaunchAgent that runs after product-tracking:
- Reads all JSON files from `data/product_changes/` and `data/product_feed_history/`
- Syncs to Google Sheets
- Runs independently so failures don't block data collection

---

## Impact Assessment

### For Just Bin Bags

**What you're missing**:
- 4 availability changes on 25 Nov (not visible in spreadsheet)
- Historical product changes from Nov 18-25 (stored in JSON but not displayed)
- Disapproval history (would have shown when the 6 landing page errors were fixed)

**What you can still do**:
- See daily performance data (impressions, clicks, revenue) ✅
- Detect performance anomalies (revenue drops, spikes) ✅
- Query JSON files manually for product changes ⚠️

### For All 16 Clients

All clients have the same issue:
- Performance data visible ✅
- Product changes invisible ❌
- Disapprovals invisible ❌

---

## Recommended Solution

### Phase 1: Quick Fix (1-2 hours)

Create simple script `sync_changes_to_sheets.py`:

```python
# Read latest product changes JSON for each client
# For each client:
#   - Open spreadsheet by ID
#   - Create "Product Changes" tab if doesn't exist
#   - Write changes from JSON to sheet
#   - Create "Disapprovals" tab if doesn't exist
#   - Fetch current disapprovals from Merchant Centre
#   - Write to sheet
```

Add to LaunchAgent after `product_change_detector.py`:
```xml
.venv/bin/python3 sync_changes_to_sheets.py
```

### Phase 2: Historical Backfill (30 mins)

Run once to populate historical data:
- Read all JSON files from Nov 18-27
- Write to spreadsheets
- Gives you full 10-day history

### Phase 3: Visual Enhancements (1 hour)

Add conditional formatting:
- Red: Products with disapprovals or out of stock
- Orange: Price increases
- Green: Products back in stock
- Yellow: Products with >3 changes in 7 days

---

## Current Workaround

Until spreadsheet writer is built, you can:

1. **Check disapprovals manually** (what we just did):
```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json .venv/bin/python3 -c "
# [Script to check Merchant Centre for disapprovals]
"
```

2. **Read product changes from JSON**:
```bash
cat data/product_changes/"Just Bin Bags"/2025-11-25.json | jq '.summary'
```

3. **Query specific change types**:
```bash
cat data/product_changes/"Just Bin Bags"/2025-11-25.json | jq '.availability_changes'
```

---

## Conclusion

**You were right to be confused** - the system name "Product Impact Analyzer" and the presence of `product_performance_spreadsheet_id` in the config strongly implies that product changes and disapprovals would be visible in the spreadsheet.

**What actually happened**:
- The data collection part was built (agents fetch data, save to JSON)
- The data visualization part was never built (no spreadsheet writer)
- You can see performance data because `product-data-fetcher` was built to write to sheets
- You can't see product changes or disapprovals because no one built the writer for those

**Next steps**:
1. Build `sync_changes_to_sheets.py` to populate missing tabs
2. Update LaunchAgent to run it automatically
3. Backfill historical data from JSON files
4. Add conditional formatting for visual alerts

**Estimated effort**: 2-3 hours total
