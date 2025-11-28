# Product Impact Analyzer - ACTUAL Gap Analysis

**Date**: 27 November 2025
**Trigger**: User observation - "I'm looking at that spreadsheet and there's still no labels on it. I'm still not seeing any flagging of issues."
**Status**: CRITICAL - System 80% complete but data invisible to users

---

## The Core Problem

**IMPLEMENTATION-COMPLETE.md claims "All Three Priorities Implemented" (Nov 3, 2025)**

**Reality (Nov 27, 2025)**: Data collection works, but **NO DATA IS VISIBLE IN SPREADSHEETS**

---

## Claimed vs Actual Implementation

| Feature | Docs Claim (Nov 3) | Actual Status (Nov 27) | Evidence |
|---------|-------------------|------------------------|----------|
| **Product change tracking** | ✅ Implemented | ⚠️ DATA ONLY (no visualization) | JSON files exist, sheets empty |
| **Product baselines** | ✅ Implemented | ⚠️ DATA ONLY (no visualization) | Baselines calculated, not in sheets |
| **Product anomaly detection** | ✅ Implemented | ⚠️ CONSOLE ONLY (no sheets) | Runs via monitor.py, doesn't write to sheets |
| **Impact analysis** | ✅ Implemented | ⚠️ TEXT FILES ONLY | Reports in /reports/, not in sheets |
| **Weekly reports** | ✅ Implemented | ⚠️ TEXT FILES ONLY | Generates .txt files, not sheets |
| **Disapproval monitoring** | ✅ Implemented | ⚠️ CONSOLE ONLY | Checks disapprovals, doesn't write to sheets |
| **Product Hero labels** | ✅ Implemented | ⚠️ JSON ONLY | Tracks in JSON, not visible in sheets |

---

## What Files Actually Exist and What They Do

### ✅ Files That Exist

All the scripts that IMPLEMENTATION-COMPLETE.md claims were created DO exist:

1. **product_feed_tracker.py** (10,938 bytes)
   - ✅ Fetches products from Merchant Centre
   - ✅ Saves daily snapshots to JSON
   - ❌ Does NOT write to Google Sheets

2. **product_change_detector.py** (13,296 bytes)
   - ✅ Compares snapshots
   - ✅ Detects changes (price, stock, title, etc.)
   - ✅ Saves to JSON files
   - ❌ Does NOT write to Google Sheets

3. **product_baseline_calculator.py** (320 lines)
   - ✅ Calculates 30-day baselines per product
   - ✅ Saves to `data/product_baselines/[client].json`
   - ❌ Does NOT write to Google Sheets

4. **product_anomaly_detector.py** (390 lines)
   - ✅ Detects product-level performance anomalies
   - ✅ Compares to baselines
   - ⚠️ Sends email alerts only (during business hours)
   - ❌ Does NOT write to Google Sheets

5. **impact_correlator.py** (423 lines)
   - ✅ Analyzes before/after performance
   - ✅ On-demand analysis tool
   - ❌ Does NOT write to Google Sheets

6. **weekly_impact_report.py** (291 lines)
   - ✅ Generates weekly text reports
   - ✅ Saves to `reports/` directory
   - ❌ Does NOT write to Google Sheets

### ❌ The Missing Piece

**NO SPREADSHEET WRITER EXISTS**

The IMPLEMENTATION-COMPLETE.md mentions:

> "Integration with Sheets Writer"
> - Add "Changes Detected" column to daily performance data
> - Flag products that changed on that date
> - Optionally: Separate "Product Changes" sheet in each client's spreadsheet

**This was never built.**

---

## What Data IS Being Collected (But Hidden)

### Just Bin Bags Example

**Location**: `/tools/product-impact-analyzer/`

1. **Product Changes** (`data/product_changes/Just Bin Bags/2025-11-25.json`):
   - 4 availability changes detected
   - Products going in/out of stock tracked
   - Price changes: 0
   - Title changes: 0
   - NEW/REMOVED products: 0

2. **Product Baselines** (`data/product_baselines/just-bin-bags.json`):
   - Baselines for all products calculated
   - 30-day averages for revenue, clicks, conversions
   - Last updated: (need to check)

3. **Weekly Reports** (`reports/`):
   - Text files with weekly summaries
   - Change aggregations
   - Impact assessments
   - NOT visible in spreadsheets

4. **Product Hero Labels**:
   - Status: Disabled for JBB ("Limited Product Hero labels detected")
   - If enabled, would track in JSON only (not sheets)

### What You Can See (Only 1 Thing)

**Just Bin Bags Spreadsheet**: `1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA`

**Visible Tab:**
- "Sheet1" (should be "Daily Performance")
- Columns: Date, Client, Product ID, Product Title, Impressions, Clicks, Conversions, etc.
- Last updated: 24 Nov 08:45 (before system broke)
- Source: `product-data-fetcher` agent

**Missing Tabs:**
1. ❌ "Product Changes" - Prices, stock, titles that changed
2. ❌ "Disapprovals" - Merchant Centre issues
3. ❌ "Product Baselines" - 30-day performance averages
4. ❌ "Anomalies" - Products deviating from baseline
5. ❌ "Product Hero Labels" - Hero/Sidekick/Villain/Zombie classification
6. ❌ "Weekly Summary" - Aggregated insights

---

## Why This Happened

### Theory 1: Scope Creep After Documentation

- Nov 3: IMPLEMENTATION-COMPLETE.md written (optimistic assessment)
- Nov 3-27: Scripts were built and tested locally
- LaunchAgents configured to run data collection
- **NOBODY BUILT THE SPREADSHEET WRITER**

### Theory 2: Documentation Aspirational

- IMPLEMENTATION-COMPLETE.md was a plan, not a status report
- "Implementation Complete" meant "code complete" not "feature complete"
- Spreadsheet integration was assumed to be trivial
- Never actually tested from user perspective

### Theory 3: Gradual Feature Removal

- Spreadsheet writer was built
- Something broke it
- System continued running data collection
- Nobody noticed sheets were empty

---

## The Automation Reality Check

### What's Running (LaunchAgents)

1. **product-data-fetcher** (every 6 hours)
   - ✅ Writes to Google Sheets (Daily Performance tab)
   - ✅ Working perfectly

2. **product-monitor** (every 6 hours)
   - ⚠️ Runs anomaly detection
   - ⚠️ Sends email alerts only
   - ❌ Doesn't write to sheets

3. **product-tracking** (daily 7:45 AM)
   - ✅ Runs product_feed_tracker.py
   - ✅ Runs product_change_detector.py
   - ❌ Doesn't run sheets writer (doesn't exist)

4. **product-impact-analyzer** (Tuesday 9:00 AM)
   - ⚠️ Purpose unclear (LaunchAgent exists but unclear what it runs)
   - ❌ Doesn't write to sheets

5. **weekly-impact-report** (Monday 9:15 AM)
   - ✅ Runs weekly_impact_report.py
   - ✅ Generates text files in `/reports/`
   - ❌ Doesn't write to sheets

---

## What SHOULD Be in the Spreadsheets

### Tab 1: Daily Performance (✅ EXISTS)
**Current state**: Working
- Date, Product ID, Product Title, Impressions, Clicks, Conversions, Revenue, Cost, CTR, Conv Rate, ROAS

### Tab 2: Product Changes (❌ MISSING)
**Should contain**:
- Date Detected
- Product ID
- Product Title
- Change Type (Price, Stock, Title, Description, Type)
- Old Value
- New Value
- Current ROAS (from performance data)
- 30-Day Avg ROAS (from baselines)

### Tab 3: Disapprovals (❌ MISSING)
**Should contain**:
- Date First Seen
- Product ID
- Product Title
- Issue Code
- Issue Description
- Status (Active/Resolved)
- Date Resolved

### Tab 4: Product Baselines (❌ MISSING)
**Should contain**:
- Product ID
- Product Title
- Product Hero Label (if enabled)
- 30-Day Avg Revenue
- 30-Day Avg Clicks
- 30-Day Avg Conversions
- 30-Day Avg ROAS
- Last Updated

### Tab 5: Performance Anomalies (❌ MISSING)
**Should contain**:
- Date Detected
- Product ID
- Product Title
- Metric (Revenue, Clicks, Conversions)
- Baseline Value
- Actual Value
- Deviation %
- Severity (High/Medium/Low)
- Correlated Change (if any)

### Tab 6: Product Hero Labels (❌ MISSING - if enabled)
**Should contain**:
- Product ID
- Product Title
- Current Label
- Previous Label
- Date Changed
- Days in Current Label
- Label History

---

## Impact on User Experience

### What You Expected

"Product Impact Analyzer" - A complete system where:
- You open a client's spreadsheet
- You see daily performance (✅)
- You see product changes (❌)
- You see disapprovals highlighted (❌)
- You see which products are underperforming (❌)
- You see Product Hero label transitions (❌)
- You get a complete picture of product health

### What You Actually Get

- One tab with raw performance data
- No context on what changed
- No alerts or flags
- No baselines for comparison
- No disapproval visibility
- Must check JSON files manually
- Must read LaunchAgent logs for alerts
- Must open text files in /reports/ for insights

---

## The "Complete System" That Isn't

From COMPLETE-SYSTEM.md:

> "The Product Impact Analyzer automatically tracks product changes, analyzes their impact on performance, and provides actionable insights through daily monitoring and weekly reports."

**Reality**:
- ✅ Tracks product changes (JSON only)
- ✅ Analyzes impact (text files only)
- ⚠️ Daily monitoring (email alerts only, not in sheets)
- ⚠️ Weekly reports (text files only, not in sheets)
- ❌ NO VISIBILITY IN SPREADSHEETS

---

## What Needs to Be Built (For Real This Time)

### Priority 1: Spreadsheet Writer Core Module

**File**: `sync_to_sheets.py`

**Responsibilities**:
1. Read latest product changes from JSON
2. Read current disapprovals from Merchant Centre API
3. Read product baselines from JSON
4. Read performance anomalies from product_anomaly_detector output
5. For each client:
   - Open spreadsheet by ID (from config.json)
   - Create missing tabs if they don't exist
   - Write data to appropriate tabs
   - Apply conditional formatting (red for issues, green for resolved)
   - Update "Last Synced" timestamp

**Estimated Size**: 400-500 lines

### Priority 2: LaunchAgent Integration

Add to `product-tracking` LaunchAgent after `product_change_detector.py`:

```xml
<string>cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer &amp;&amp;
GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json
.venv/bin/python3 product_feed_tracker.py &amp;&amp;
sleep 60 &amp;&amp;
.venv/bin/python3 product_change_detector.py &amp;&amp;
sleep 30 &amp;&amp;
.venv/bin/python3 sync_to_sheets.py
</string>
```

### Priority 3: Historical Backfill

Run once to populate historical data:

```bash
.venv/bin/python3 sync_to_sheets.py --backfill --start-date 2025-11-18 --end-date 2025-11-27
```

### Priority 4: Conditional Formatting

Add to sync_to_sheets.py:
- Red: Products with disapprovals
- Orange: Products out of stock
- Yellow: Products with >20% performance drop
- Green: Products that improved
- Blue: Products back in stock

---

## Conclusion

**IMPLEMENTATION-COMPLETE.md was WRONG.**

The system is **80% complete**:
- ✅ Data collection (product changes, baselines, anomalies, impact analysis)
- ✅ Automation (LaunchAgents running daily/weekly)
- ✅ Analysis (text reports, email alerts)
- ❌ **VISUALIZATION (spreadsheet integration)**

**The missing 20% is the MOST IMPORTANT 20%** - it's what makes the system usable.

Without spreadsheet integration, the system is like a car with no dashboard - the engine works, you're collecting data, but you can't see where you're going.

---

## Recommended Next Steps

1. **Acknowledge the gap** - IMPLEMENTATION-COMPLETE.md was optimistic
2. **Build sync_to_sheets.py** - The missing visualization layer
3. **Update LaunchAgents** - Integrate sheets writer into automation
4. **Backfill historical data** - Show last 10 days of changes
5. **Test with one client** - Verify all tabs appear correctly
6. **Roll out to all clients** - Complete the system

**Estimated Time**: 4-6 hours to build + test + deploy

---

**Status**: CRITICAL GAP IDENTIFIED
**Date**: 27 November 2025
**Next Action**: Build sync_to_sheets.py to make data visible
