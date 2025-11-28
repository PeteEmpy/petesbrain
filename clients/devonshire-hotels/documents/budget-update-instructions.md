# Devonshire Budget Tracker - Update Instructions

**Date:** 2025-10-30
**Purpose:** How to update automated sheets without losing manual budget entries

---

## The Problem

When the automated budget sheets are updated with fresh Google Ads data, the update process can accidentally overwrite manual budget entries you've made in Column C.

## The Solution

### What's AUTOMATED (Updated by Claude Code):

These columns get fresh data from Google Ads every time you ask for an update:

- **Column D:** Total Days (calculated)
- **Column E:** Days Elapsed (calculated from current date/time)
- **Column F:** Days Remaining (calculated)
- **Column G:** Spend (from Google Ads)
- **Column H:** Expected Spend (calculated)
- **Column I:** Remaining Budget (calculated)
- **Column J:** Req Daily Budget (calculated)
- **Column K:** Pacing % (calculated)
- **Column L:** Predicted Spend (calculated)
- **Column M:** Yesterday Spend (from Google Ads)
- **Column O:** Data Date (timestamp)

### What's MANUAL (You Control):

These columns should NEVER be overwritten by updates:

- **Column C:** Budget (💡 YOU ENTER THIS)
- **Column N:** Notes (💡 YOU ENTER THIS)

---

## How to Update Without Losing Your Data

### For You (User):

Simply ask Claude Code:
```
Update Devonshire budget tracker
```

**Your manual entries in Column C (Budget) and Column N (Notes) will be preserved.**

### For Claude Code:

When updating, follow this process:

**Step 1:** Read existing budgets from Column C
```
Read Dev Properties Auto!C14:C18 (future months)
Read The Hide Properties Auto!C9:C13 (future months)
```

**Step 2:** Fetch fresh data from Google Ads
```
Run GAQL queries for current month spend
Calculate pacing metrics
```

**Step 3:** Write data CAREFULLY
```
Only update automated columns (D-M, O)
PRESERVE Column C (budgets) by writing back what was read
PRESERVE Column N (notes) by writing back what was read
```

---

## Current Budget Allocations

As of Oct 30, 2025:

### Dev Properties (Main hotels/properties)

| Month | Budget | Status |
|-------|--------|--------|
| October 2025 | £9,730.00 | Active - overspending |
| November 2025 | £9,000.00 | Manual entry |
| December 2025 | **£11,730.00** | ⚠️ Updated Oct 30 |
| January 2026 | £6,750.00 | Manual entry |
| February 2026 | £6,500.00 | Manual entry |
| March 2026 | £8,000.00 | Manual entry |

### The Hide

| Month | Budget | Status |
|-------|--------|--------|
| October 2025 | £2,000.00 | Active - underspending |
| November 2025 | £2,000.00 | First full month |
| December 2025 | £2,000.00 | Manual entry |
| January 2026 | £2,000.00 | Manual entry |
| February 2026 | £2,000.00 | Manual entry |
| March 2026 | £2,000.00 | Manual entry |

### Combined Totals

| Month | Combined Budget |
|-------|-----------------|
| October 2025 | £11,730.00 |
| November 2025 | £11,000.00 |
| December 2025 | **£13,730.00** (Main: £11,730 + Hide: £2,000) |
| January 2026 | £8,750.00 |
| February 2026 | £8,500.00 |
| March 2026 | £10,000.00 |

---

## Visual Indicators in Sheets

Both automated sheets now have:

⚠️ **Warning banner in Row 3/4:**
> "COLUMN C (BUDGET) IS MANUAL ENTRY - YOUR CHANGES WILL BE PRESERVED"

This reminds anyone updating the sheets that Column C must be handled carefully.

---

## What Changed (Oct 30, 2025)

1. **December Dev Properties budget** updated from £7,750 → **£11,730**
2. **Added warning banners** to both sheets
3. **Created this documentation** to prevent future overwrites

---

## If Your Budget Gets Reset Accidentally

If an update accidentally overwrites your budget:

1. **Don't panic** - just re-enter the correct amount in Column C
2. **Tell Claude Code:**
   ```
   The December budget should be £11,730, not £7,750. Please fix and make sure it doesn't reset again.
   ```
3. Claude Code will fix it and update the process to prevent future resets

---

## Technical Notes

### Why This Happens

The Google Sheets MCP writes entire ranges of cells at once. If we're not careful, it can overwrite cells that should be left alone.

### The Fix

When updating, Claude Code must:
1. Read the current state of manual columns (C and N)
2. Fetch fresh automated data
3. Merge the two datasets
4. Write back only what's changed (or write everything but preserve manual entries)

### Future Enhancement

Ideally, we'd protect Column C and N at the Google Sheets level (cell protection), but that requires direct Google Sheets API access beyond what MCP provides.

---

## Quick Reference

**✅ Safe to update automatically:**
- Spend data (Column G)
- Days elapsed/remaining (E, F)
- Pacing calculations (K, L)
- Yesterday's spend (M)
- All metrics derived from Google Ads

**⚠️ NEVER automatically update:**
- Budget amounts (Column C)
- Notes (Column N)

---

## Contact

If budgets keep resetting or you notice other issues:
- **Tell Claude Code in chat** - "The budget keeps resetting"
- **Check this document** for current budget allocations
- **Manual fix:** Just re-enter the budget in Column C (it won't break anything)

---

**Last Updated:** 2025-10-30
**Maintained By:** Claude Code
**Sheet ID:** 1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc
