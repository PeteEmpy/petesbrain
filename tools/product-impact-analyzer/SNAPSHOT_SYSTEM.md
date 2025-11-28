# Product Feed Snapshot System

**Status:** Implemented - Phase 1 (Manual via Claude Code)

## Overview

The Product Feed Snapshot System tracks product-level changes (price, availability, title) over time and correlates them with Google Ads performance impacts.

**Problem it solves:**
- "Why did clicks spike for this product?" → Price dropped 20%
- "Why did revenue drop?" → 50 products removed from feed
- "What's the impact of price testing?" → Track before/after performance

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCT FEED SNAPSHOT SYSTEM                 │
└─────────────────────────────────────────────────────────────────┘

1. DATA COLLECTION (Daily at 6 AM)
   ┌──────────────────┐
   │ Google Ads API   │ → Fetch shopping_performance_view
   │ (via MCP)        │    (product_id, title, brand, metrics)
   └────────┬─────────┘
            │
            ↓
   ┌──────────────────┐
   │ snapshot_product │ → Aggregate by product
   │ _feed.py         │    Store current state
   └────────┬─────────┘
            │
            ↓
2. STORAGE (Google Sheets via MCP)
   ┌──────────────────────────────────────────────────────────────┐
   │ Sheet: "Product Feed History"                                │
   │ Columns: Snapshot Date | Client | Product ID | Title | Brand│
   │          | Price | Impressions | Clicks | Cost                │
   └──────────────────────────────────────────────────────────────┘

3. CHANGE DETECTION
   ┌──────────────────┐
   │ Compare current  │ → New products added?
   │ vs previous      │   Products removed?
   │ snapshot         │   Price changes?
   └────────┬─────────┘    Title changes?
            │
            ↓
   ┌──────────────────────────────────────────────────────────────┐
   │ Sheet: "Price Change Log"                                    │
   │ Columns: Date | Client | Product ID | Change Type            │
   │          | Old Price | New Price | Price Change %            │
   └──────────────────────────────────────────────────────────────┘

4. IMPACT ANALYSIS
   ┌──────────────────┐
   │ analyzer.py      │ → Read changes + performance data
   │                  │   Calculate impact (7 days before/after)
   └────────┬─────────┘   Flag significant impacts
            │
            ↓
   ┌──────────────────────────────────────────────────────────────┐
   │ Output: Impact Analysis Report                               │
   │ - Product removed → Revenue -£500/week                       │
   │ - Price dropped 15% → Clicks +200%, Revenue +£300/week       │
   └──────────────────────────────────────────────────────────────┘
```

## Files

### Core Scripts

**`snapshot_product_feed.py`** - Main snapshot script
- Fetches current product data from Google Ads API
- Compares with previous snapshot
- Detects changes (REMOVED, NEW, PRICE_CHANGE, MODIFIED)
- Saves snapshot to Google Sheets

**`run_snapshot_via_claude.py`** - Claude Code orchestration helper
- Instructions for Claude to fetch data via MCP
- Cache management for API results
- Workflow documentation

**`analyzer.py`** - Impact analysis (updated)
- Now reads price change data from Outliers Report
- Correlates price changes with performance impacts
- Enhanced output with change type and price details

### Setup & Automation

**`setup_daily_snapshot.sh`** - LaunchAgent setup
- Creates LaunchAgent to run snapshots daily at 6 AM
- Configures logging
- Manages virtual environment

**`config.json`** - Configuration
- Client list with merchant_id and customer_id
- Analysis settings (comparison window, thresholds)
- Sheet IDs and names

## Usage

### Phase 1: Manual Snapshots (via Claude Code)

**User command:**
```
"Run the product feed snapshot"
```

**Claude workflow:**

1. Load client configuration from `config.json`

2. For each enabled client, fetch product data:
```python
query = """
SELECT
    segments.product_item_id,
    segments.product_title,
    segments.product_brand,
    segments.date,
    metrics.clicks,
    metrics.impressions,
    metrics.cost_micros
FROM shopping_performance_view
WHERE segments.date = '2025-10-29'
ORDER BY segments.product_item_id
"""

results = mcp__google-ads__run_gaql(
    customer_id=client['google_ads_customer_id'],
    query=query
)
```

3. Cache results locally:
```python
from run_snapshot_via_claude import save_gaql_results
save_gaql_results(customer_id, results['results'])
```

4. Run snapshot script:
```bash
cd tools/product-impact-analyzer
.venv/bin/python snapshot_product_feed.py
```

5. Read output files:
- `data/snapshot_{client}_{date}.json` - Current snapshot
- `data/price_changes.json` - Detected changes

6. Write to Google Sheets via MCP:
```python
# Append to "Product Feed History"
mcp__google-sheets__write_cells(
    spreadsheet_id="1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q",
    range_name="Product Feed History!A:I",
    values=snapshot_rows
)

# Append to "Price Change Log"
mcp__google-sheets__write_cells(
    spreadsheet_id="1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q",
    range_name="Price Change Log!A:J",
    values=change_rows
)
```

7. Report summary to user

### Phase 2: Automated Snapshots (Future)

**Setup:**
```bash
cd tools/product-impact-analyzer
./setup_daily_snapshot.sh
```

**Runs:** Daily at 6:00 AM automatically

**Logs:** `~/.petesbrain-product-snapshot.log`

**Note:** Phase 2 requires building an automated data fetching mechanism (API wrapper or separate service).

## Google Sheets Structure

### Sheet: "Product Feed History"

Stores daily product snapshots.

| Snapshot Date | Client | Product ID | Title | Brand | Price Micros | Impressions | Clicks | Cost Micros |
|---------------|--------|------------|-------|-------|--------------|-------------|--------|-------------|
| 2025-10-29 | Tree2mydoor | 01090 | The Olive Tree... | Tree2mydoor | 2490000 | 349187 | 1465 | 17534000 |

**Purpose:** Historical record of product state over time

### Sheet: "Price Change Log"

Stores detected changes.

| Date | Client | Product ID | Title | Change Type | Old Price | New Price | Price Change % | Old Impressions | New Impressions |
|------|--------|------------|-------|-------------|-----------|-----------|----------------|-----------------|-----------------|
| 29/10/2025 | Tree2mydoor | 01090 | The Olive... | PRICE_CHANGE | 2990000 | 2490000 | -16.72 | 2500 | 349187 |

**Change Types:**
- `REMOVED` - Product no longer in feed
- `NEW` - Product added to feed
- `PRICE_CHANGE` - Price changed
- `MODIFIED` - Title or other metadata changed

### Sheet: "Outliers Report" (Enhanced)

Existing sheet now includes price columns:

| Client | Product ID | Change Type | Date Changed | Product Title | Days Since | Flag | Old Price | New Price | Price Change % |
|--------|------------|-------------|--------------|---------------|------------|------|-----------|-----------|----------------|

## Example Scenarios

### Scenario 1: Price Drop Analysis

**Question:** "Why did Product 01090 get 1,465 clicks on Oct 28?"

**Snapshot system detects:**
- Oct 26: Price changed from £29.90 → £24.90 (-16.7%)
- Oct 28: Clicks spiked 1,900%

**Impact analysis shows:**
- Before price change (Oct 19-25): 10 clicks/day avg
- After price change (Oct 26-Nov 1): 500 clicks/day avg
- Revenue impact: +£2,500/week despite lower price

**Conclusion:** Price drop made product more competitive in auctions

### Scenario 2: Product Removal Impact

**Question:** "Why did campaign revenue drop 20%?"

**Snapshot system detects:**
- Oct 26: 98 products removed from feed

**Impact analysis shows:**
- Removed products generated £500/week revenue
- Most were seasonal (Christmas products) or low-performing
- Net impact: -£500/week revenue, +2% ROAS (removed unprofitable SKUs)

**Conclusion:** Strategic product removal improved profitability

### Scenario 3: New Product Launch

**Question:** "How is the new product performing?"

**Snapshot system detects:**
- Oct 20: Product 05678 added to feed (price: £49.90)

**Impact analysis shows:**
- Oct 20-27: 50 clicks, £25 revenue (ROAS 0.50x) - Learning phase
- Oct 28-Nov 3: 200 clicks, £300 revenue (ROAS 3.00x) - Optimized

**Conclusion:** Product performing well after learning phase

## Data Sources

### Google Ads API (Shopping Performance View)

**Advantages:**
- Easy access via existing MCP integration
- Historical data available
- Includes performance metrics alongside product data

**Limitations:**
- `product_price_micros` may not be available in all reports
- Depends on Google Ads having accurate product data
- Only shows products with impressions (won't catch removed products immediately)

### Google Merchant Center API (Future Enhancement)

**Advantages:**
- Direct access to product feed data
- Includes price, availability, stock status
- Shows all products, even those with 0 impressions

**Limitations:**
- Requires Merchant Center API setup
- Separate authentication from Google Ads

**Implementation priority:** Medium - Add if Shopping Performance View doesn't include prices

## Troubleshooting

### "No recent cached data found"

**Cause:** `snapshot_cache_{customer_id}.json` doesn't exist or is > 1 hour old

**Fix:** Run data fetch via Claude Code MCP first, then run snapshot script

### "No previous snapshot found"

**Cause:** First run - no historical data to compare

**Expected:** This is normal. Run snapshot daily to build history.

### "Warning: Skipping invalid row"

**Cause:** Google Ads API returned unexpected data structure

**Fix:** Check GAQL query and API response format. Update `aggregate_products()` if needed.

### LaunchAgent not running

**Check status:**
```bash
launchctl list | grep product-snapshot
```

**View logs:**
```bash
tail -f ~/.petesbrain-product-snapshot.log
tail -f ~/.petesbrain-product-snapshot-error.log
```

**Reload:**
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-snapshot.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-snapshot.plist
```

## Roadmap

### Phase 1: Manual via Claude Code (Current)
- ✅ Snapshot script implemented
- ✅ Change detection working
- ✅ Analyzer updated to read price data
- ⏳ Need to create Google Sheets tabs
- ⏳ Test end-to-end workflow

### Phase 2: Automated Daily Snapshots
- ⏳ Build API wrapper for automated data fetching
- ⏳ Set up LaunchAgent
- ⏳ Configure error alerting

### Phase 3: Advanced Features
- ⏳ Merchant Center API integration
- ⏳ Stock availability tracking
- ⏳ Competitor price tracking
- ⏳ Automated price change recommendations
- ⏳ Dashboard/visualization of price history

## Related Documentation

- **`TOOL_CLAUDE.md`** - Product Impact Analyzer architecture
- **`QUICKSTART.md`** - Setup and first run instructions
- **`README.md`** - High-level overview
- **`config.json`** - Configuration reference

## Support

**Questions or issues?**
- Check logs: `~/.petesbrain-product-snapshot.log`
- Review this document for troubleshooting steps
- Ask Claude Code for help interpreting results
