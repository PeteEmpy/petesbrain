---
name: smythson-strategy-dashboard
description: Manages and updates the Smythson Q4 2025 Strategy Control Dashboard including budget targets, ROAS expectations, revenue projections, and weighted pacing calculations. Use when updating Smythson dashboard, adjusting Q4 targets, or managing Smythson strategy metrics.
allowed-tools: Bash, Read, Write, mcp__google-ads__run_gaql
---

# Smythson Strategy Dashboard Skill

---

## Overview

This skill handles all updates and adjustments to the Smythson Q4 Strategy Control Dashboard, including budget targets, ROAS expectations, revenue projections, and weighted pacing calculations based on Q4 2024 historical data.

---

## Key Resources

### Google Sheet Dashboard
- **Spreadsheet ID**: `10vRzZJuUQMX0l86plKcuZfdoiidoexI1LPYnhr6gJlU`
- **Name**: Smythson Q4 2025 Strategy Control Dashboard
- **URL**: https://docs.google.com/spreadsheets/d/10vRzZJuUQMX0l86plKcuZfdoiidoexI1LPYnhr6gJlU/edit

### Python Scripts
- **Main script**: `clients/smythson/scripts/update-q4-dashboard.py`
- **Revenue analysis**: `clients/smythson/scripts/calculate-q4-2024-revenue-distribution.py`
- **Historical data**: `clients/smythson/scripts/q4-2024-revenue-distribution.json`

### Documentation
- **CONTEXT.md**: `clients/smythson/CONTEXT.md` (Document History rows 616-618)
- **Update summary**: `clients/smythson/DASHBOARD-UPDATE-SUMMARY.md`
- **Corrected targets**: `clients/smythson/DASHBOARD-UPDATE-CORRECTED.md`
- **Pacing integration**: `clients/smythson/WEIGHTED-PACING-INTEGRATION-COMPLETE.md`

---

## Current Configuration (Nov 7, 2025)

### Budget & Revenue Targets
```python
TOTAL_BUDGET = 570252  # £570,252 total Q4
TOTAL_REVENUE_TARGET = 2380000  # £2,380,000 client target
```

**Budget Breakdown:**
- P7 (Sep 29 - Nov 2): £132,519 (completed, £113,970 actual spend)
- P8 (Nov 3-30): £218,653
- P9 (Dec 1-28): £219,080

### Regional Revenue Targets

**November (P8):**
- UK: £577,167 (6.0 ROAS)
- USA: £354,227 (4.5 ROAS)
- EUR: £122,446 (4.0 ROAS)
- ROW: £65,596 (5.0 ROAS)

**December (P9):**
- UK: £578,451 (6.0 ROAS)
- USA: £354,834 (4.5 ROAS)
- EUR: £122,685 (4.0 ROAS)
- ROW: £65,724 (5.0 ROAS)

### Weighted Pacing Data

**November 2024 Actual Distribution:**
- Total revenue: £608,165
- Average daily: £20,272
- Black Friday (Nov 23): 2.39x multiplier
- Cyber Monday (Nov 29): 2.65x multiplier
- Black Friday week (Nov 22-30): 53% of month

**December 2024:** Not yet integrated (using fallback multipliers)

---

## Common Adjustment Tasks

### 1. Update Budget Targets

**When**: Client approves budget changes, period budget adjustments

**Steps**:
1. Read `update-q4-dashboard.py` (lines 70-107)
2. Update `TOTAL_BUDGET`, `NOVEMBER_REVENUE_TARGETS`, `DECEMBER_REVENUE_TARGETS`
3. Recalculate regional splits (44% UK, 36% USA, 14% EUR, 6% ROW)
4. Update Google Sheet cells: B9 (budget), B10 (revenue target), J19-J22 (Nov targets), J31-J34 (Dec targets)
5. Test script: `python3 update-q4-dashboard.py`
6. Update CONTEXT.md Document History with changes

**Example prompt**: "Update Smythson dashboard budget to £600k total Q4"

### 2. Adjust ROAS Targets

**When**: Performance exceeds/underperforms expectations, strategic shifts

**Steps**:
1. Read `update-q4-dashboard.py` (lines 83-107)
2. Update regional ROAS multipliers in calculations
3. Recalculate `NOVEMBER_REVENUE_TARGETS` and `DECEMBER_REVENUE_TARGETS`
4. Update Google Sheet cells with new targets
5. Update email template (lines 561-563) with new ROAS targets
6. Update CONTEXT.md Document History

**Example prompt**: "Adjust UK ROAS target to 7.0 based on P8 performance"

### 3. Add December 2024 Weighted Pacing

**When**: December data becomes available for analysis

**Steps**:
1. Modify `calculate-q4-2024-revenue-distribution.py`:
   - Change date range to December 2024
   - Query: `SELECT segments.date, metrics.conversions_value FROM campaign WHERE segments.date BETWEEN '2024-12-01' AND '2024-12-31'`
2. Run script to generate December multipliers
3. Update `q4-2024-revenue-distribution.json` with December data
4. Remove fallback_december_multipliers from `update-q4-dashboard.py` (lines 224-234)
5. Update Google Sheet methodology notes (rows 91-95)
6. Update CONTEXT.md Document History

**Example prompt**: "Add December 2024 weighted pacing data to Smythson dashboard"

### 4. Update Phase Transition Dates

**When**: Timeline changes, phases shift

**Steps**:
1. Read `update-q4-dashboard.py` (lines 240-246)
2. Update `phase_transitions` list with new dates
3. Update Google Sheet "INITIATIVE STATUS" section with new timeline
4. Update CONTEXT.md Important Dates section
5. Test weighted pacing calculations with new dates

**Example prompt**: "Move Phase 3 to November 28 due to timeline shift"

### 5. Add New Regional Account

**When**: New market launches (e.g., Asia-Pacific)

**Steps**:
1. Update `REGIONAL_ACCOUNTS` dictionary (lines 46-60)
2. Add to `NOVEMBER_REVENUE_TARGETS` and `DECEMBER_REVENUE_TARGETS`
3. Update regional split percentages (ensure total = 100%)
4. Add new rows to Google Sheet regional tables
5. Update email template with new region
6. Update CONTEXT.md with new account structure

**Example prompt**: "Add Asia-Pacific account to Smythson dashboard with 5% budget allocation"

---

## Google Sheet Structure

### Key Cells to Update

**Executive Summary:**
- B8: Q4 Period dates
- B9: Total Budget
- B10: Revenue Target
- B11: Target ROAS (blended)
- B12: Last Updated timestamp
- A13: Revenue pacing note

**November Regional Targets:**
- J19: UK target
- J20: USA target
- J21: EUR target
- J22: ROW target
- J23: November total

**December Regional Targets:**
- J31: UK target
- J32: USA target
- J33: EUR target
- J34: ROW target
- J35: December total

**Status Section:**
- B42-B47: Various status metrics

**Methodology Section:**
- A78-B95: Revenue pacing methodology notes

---

## Testing & Validation

### After Any Changes

1. **Dry run script**:
   ```bash
   cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts
   source .venv/bin/activate
   python3 update-q4-dashboard.py
   ```

2. **Check calculations**:
   - Regional targets sum to monthly total
   - Monthly totals sum to Q4 total
   - ROAS multipliers match documentation
   - Weighted pacing loads Q4 2024 data

3. **Verify Google Sheet**:
   - All cells populated correctly
   - No #REF! or #VALUE! errors
   - Traffic lights displaying properly
   - Methodology notes accurate

4. **Update documentation**:
   - CONTEXT.md Document History entry
   - Create/update status document if major change
   - Note changes in dashboard update log

---

## Automation

**LaunchAgent**: Daily updates at 7:00 AM
**Script location**: `clients/smythson/scripts/update-q4-dashboard.py`
**Log file**: Check stdout/stderr in script execution

**Email summary**: Sent to petere@roksys.co.uk after each update

---

## Troubleshooting

### Google Sheets API Quota Exceeded
**Error**: `APIError: [429]: Quota exceeded`
**Cause**: Too many write operations (60/minute limit)
**Fix**: Script will work on next run after quota resets (1 hour)

### Q4 2024 Data Not Loading
**Error**: "Warning: Could not load Q4 2024 data"
**Cause**: `q4-2024-revenue-distribution.json` missing or invalid
**Fix**:
- Check file exists: `ls clients/smythson/scripts/q4-2024-revenue-distribution.json`
- Re-run: `python3 calculate-q4-2024-revenue-distribution.py`

### Regional Targets Don't Sum Correctly
**Cause**: Rounding errors or incorrect percentages
**Fix**:
- Verify regional splits: 44% + 36% + 14% + 6% = 100%
- Recalculate: `budget × regional_pct × ROAS`

---

## Version History

| Date | Change | Notes |
|------|--------|-------|
| 2025-11-07 | Initial skill creation | After weighted pacing integration |
| 2025-11-07 | Budget corrections #1 & #2 | £367k→£570k→£2.38M targets |
| 2025-11-07 | Q4 2024 pacing integration | November actual data, December pending |

---

## Related Skills

- **Smythson Account Management** - General account strategy and optimizations
- **Google Ads Performance Analysis** - Performance deep dives and reporting
- **Budget Management** - Period-based budget tracking and pacing

---

## Notes

- Always read CONTEXT.md before making dashboard changes
- Document all changes in CONTEXT.md Document History
- Test changes before committing
- Keep methodology notes in Google Sheet up-to-date
- Dashboard is client-facing - changes should be carefully considered
