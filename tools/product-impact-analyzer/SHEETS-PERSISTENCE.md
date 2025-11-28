# Google Sheets Historical Persistence

**Status**: ✅ Code complete, ready for execution
**Date**: November 2, 2025

## Problem Solved

Previously, the Product Impact Analyzer only stored **30 days of data in local JSON files** with no long-term historical accumulation. This made it impossible to:
- Track product performance trends beyond 30 days
- Compare current performance to historical baselines
- Identify seasonal patterns or long-term product lifecycle stages
- Build predictive models from historical data

## Solution Overview

The system now writes **daily performance snapshots** and **weekly impact analysis results** to Google Sheets for permanent historical tracking.

## Architecture

### Data Flow

```
Daily (10 AM) - monitor.py
    ↓
Fetch yesterday's Google Ads data (last 24 hours)
    ↓
Aggregate metrics by product
    ↓
Append to "Daily Performance" sheet (accumulating historical data)
    ↓
Check for alerts and send emails if needed

Weekly (Tuesday 9 AM) - run_automated_analysis.py
    ↓
Fetch Outliers Report (product changes)
    ↓
Analyze impact of changes on performance
    ↓
Append to "Impact Analysis" sheet (accumulating historical data)
    ↓
Generate and send HTML email report
```

### Google Sheets Structure

The configured spreadsheet (`1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q`) will have three new sheets:

#### 1. **Daily Performance** (Accumulating)

**Purpose**: Historical daily performance for every product across all clients

**Columns**:
| Date | Client | Product ID | Product Title | Impressions | Clicks | Conversions | Revenue (£) | Cost (£) | CTR (%) | Conv Rate (%) | ROAS | Label |

**Update Frequency**: Daily at 10 AM (appends previous day's metrics)

**Data Retention**: Permanent (accumulates indefinitely)

**Sample Row**:
```
2025-11-02 | Tree2mydoor | 287 | Olive Tree Large | 1,245 | 52 | 4.5 | £245.00 | £98.50 | 4.18% | 8.65% | 2.49 | hero
```

#### 2. **Impact Analysis** (Accumulating)

**Purpose**: Historical record of product change impacts analyzed weekly

**Columns**:
| Analysis Date | Client | Product ID | Product Title | Change Type | Date Changed | Days Since | Before Clicks | After Clicks | Click Change % | Before Revenue | After Revenue | Revenue Change £ | Revenue Change % | Impact Flag | Label |

**Update Frequency**: Weekly on Tuesday at 9 AM (appends latest analysis)

**Data Retention**: Permanent (accumulates indefinitely)

**Sample Row**:
```
2025-11-02 | Tree2mydoor | 287 | Olive Tree Large | PRICE_CHANGE | 2025-10-26 | 7 | 422 | 301 | -28.7% | £680.00 | £500.00 | -£180.00 | -26.5% | 📉 | hero
```

#### 3. **Product Summary** (Overwritten)

**Purpose**: Current snapshot of all active products (refreshed weekly)

**Columns**:
| Client | Product ID | Product Title | Current Label | Last 7D Clicks | Last 7D Revenue | Last 30D Clicks | Last 30D Revenue | ROAS | Status |

**Update Frequency**: Weekly on Tuesday at 9 AM (overwrites previous data)

**Data Retention**: Only current week (not historical)

**Sample Row**:
```
Tree2mydoor | 287 | Olive Tree Large | hero | 218 | £425.00 | 892 | £1,680.00 | 2.45 | active
```

## Implementation

### Code Changes

1. **✅ Created `sheets_writer.py`**
   - `SheetsWriter` class with methods for each sheet type
   - Generates write requests as JSON files for Claude Code to execute
   - Validates data before writing

2. **✅ Integrated into `monitor.py`**
   - Daily monitor now calls `sheets_writer.append_daily_performance()`
   - Writes yesterday's metrics for all products across all clients
   - Appends to existing data (does not overwrite)

3. **✅ Integrated into `run_automated_analysis.py`**
   - Weekly analyzer now calls `sheets_writer.write_impact_analysis()`
   - Writes analysis results for all product changes detected
   - Appends to existing data (does not overwrite)

### Execution Process

The `sheets_writer.py` module generates **write request JSON files** in `data/sheets_write_*.json`. These files must be executed by Claude Code using the MCP Google Sheets server.

**Why this approach?**
- The LaunchAgent-triggered automated scripts run without Claude Code present
- Direct MCP integration requires Python MCP client library (not yet integrated)
- Temporary bridge: Scripts generate write requests, Claude Code executes them periodically

**Workflow**:
1. Automated scripts run (daily monitor, weekly analyzer)
2. Scripts generate `data/sheets_write_*.json` files
3. Claude Code periodically checks for pending writes
4. Claude Code executes MCP calls to write to Google Sheets
5. Claude Code deletes executed request files

## Manual Setup (One-Time)

### Step 1: Create New Sheets

The Google Sheets spreadsheet needs three new sheets added:

1. **Daily Performance** - Create blank sheet with this name
2. **Impact Analysis** - Create blank sheet with this name
3. **Product Summary** - Create blank sheet with this name

You can create these manually in Google Sheets or ask Claude Code to do it.

### Step 2: Write Headers

Each sheet needs a header row:

**Daily Performance (Row 1)**:
```
Date | Client | Product ID | Product Title | Impressions | Clicks | Conversions | Revenue (£) | Cost (£) | CTR (%) | Conv Rate (%) | ROAS | Label
```

**Impact Analysis (Row 1)**:
```
Analysis Date | Client | Product ID | Product Title | Change Type | Date Changed | Days Since | Before Clicks | After Clicks | Click Change % | Before Revenue | After Revenue | Revenue Change £ | Revenue Change % | Impact Flag | Label
```

**Product Summary (Row 1)**:
```
Client | Product ID | Product Title | Current Label | Last 7D Clicks | Last 7D Revenue | Last 30D Clicks | Last 30D Revenue | ROAS | Status
```

### Step 3: Test Data Flow

Run a manual test to verify the pipeline:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Test sheets writer
.venv/bin/python3 sheets_writer.py

# This will generate: data/sheets_write_daily_performance.json

# Then Claude Code executes the pending write
```

## Ongoing Maintenance

### Daily (Automated)

- 9:30 AM: `fetch_data_automated.py` fetches last 30 days from Google Ads API
- 10:00 AM: `monitor.py` runs, appends yesterday to "Daily Performance" sheet

### Weekly (Automated)

- Tuesday 9:00 AM: `run_automated_analysis.py` runs, appends analysis to "Impact Analysis" sheet

### Periodic (Manual - Until Direct MCP Integration)

Claude Code should periodically execute pending Sheets writes:

```python
# Check for pending writes
sheets_writer = SheetsWriter(config_path)
sheets_writer.execute_pending_writes()

# Execute each pending write via MCP
# Then delete the request JSON files
```

## Benefits

### 1. **Trend Analysis**
- Track product performance week-over-week, month-over-month
- Identify improving vs declining products
- Detect seasonality patterns
- Validate Product Hero label assignments over time

### 2. **Historical Context**
- Compare current performance to 30/60/90 day averages
- Understand product lifecycle stages
- Identify one-time anomalies vs persistent changes

### 3. **Reporting**
- Export historical data for client reports
- Create charts and visualizations in Google Sheets
- Share specific date ranges or product subsets

### 4. **Predictive Modeling** (Future)
- Use historical data to train ML models
- Predict impact of product changes before they happen
- Optimize Product Hero label transitions

### 5. **Audit Trail**
- Permanent record of all product changes and their impacts
- Track what was tried and what worked
- Document experiments and their outcomes

## Data Volume Estimate

### Daily Performance Sheet

**Rows per day**: ~9,276 products (across 13 clients)
**Rows per year**: ~3.4 million rows
**Columns**: 13 columns
**Google Sheets limit**: 10 million cells per sheet

**Capacity**: ~3 years of daily data before hitting Google Sheets limits
**Solution for scaling**: Archive older data to BigQuery or separate spreadsheet annually

### Impact Analysis Sheet

**Rows per week**: ~50-200 product changes (varies by week)
**Rows per year**: ~5,000 rows
**Columns**: 16 columns

**Capacity**: Decades of data before limits

## Alternative Architecture (Future Phase 3)

For larger scale (beyond 3 years of data), consider:

### BigQuery Integration
- Store raw daily metrics in BigQuery tables
- Query historical data via SQL
- Use Google Sheets as a **view** layer (Data Studio/Looker Studio)
- Unlimited storage, fast queries

### Database Backend
- PostgreSQL or MySQL database
- Store all historical data
- Google Sheets imports summaries via Apps Script
- More complex setup, better for enterprise scale

### Hybrid Approach
- Keep Google Sheets for current month + last 12 months
- Archive older data to BigQuery/CSV exports
- Fetch historical data on-demand when needed for analysis

## Testing Checklist

- [x] `sheets_writer.py` module created
- [x] Test mode generates valid write requests
- [x] `monitor.py` integrated with daily performance writing
- [x] `run_automated_analysis.py` integrated with impact analysis writing
- [ ] Manual test: Create "Daily Performance" sheet
- [ ] Manual test: Write header row to "Daily Performance"
- [ ] Manual test: Execute pending write request via Claude Code
- [ ] Manual test: Verify data appears correctly in sheet
- [ ] Manual test: Run monitor.py and verify append works
- [ ] Manual test: Run weekly analysis and verify impact data writes
- [ ] Production test: Let daily monitor run for 7 days, verify accumulation
- [ ] Production test: Let weekly analysis run for 3 weeks, verify accumulation

## Next Steps

1. **Create the three new sheets** in the Google Sheets spreadsheet
2. **Write header rows** to each sheet
3. **Execute first test write** to verify end-to-end flow
4. **Monitor for 1 week** to ensure daily accumulation works
5. **Review data quality** after 1 week to validate metrics
6. **Phase 3**: Integrate direct MCP client library to eliminate manual execution step

## Support

For issues:
- Check logs: `~/.petesbrain-product-monitor.log`
- Check pending writes: `ls -la tools/product-impact-analyzer/data/sheets_write_*.json`
- Test sheets writer: `python3 sheets_writer.py`
- Verify spreadsheet ID: Check `config.json` matches actual spreadsheet

---

**Generated**: November 2, 2025
**Version**: 1.0
**Status**: Implementation complete, testing in progress
