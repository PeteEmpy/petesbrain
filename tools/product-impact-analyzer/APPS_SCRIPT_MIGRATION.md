# Migrating Existing Apps Script to Track Price Changes

## Overview

Your existing Google Apps Script already does 90% of what we need! It just needs enhancements to track price changes.

**What it currently does:**
- ✅ Fetches products from Google Merchant Center daily
- ✅ Stores current/previous snapshots in Google Sheets
- ✅ Detects REMOVED and NEW products
- ✅ Generates Outliers Report
- ✅ Sends weekly email summaries

**What needs to be added:**
- 💰 Extract price data from GMC API
- 💰 Detect PRICE_CHANGE events
- 💰 Store old/new prices in Changes sheets
- 💰 Show price changes in Outliers Report
- 💰 Include price changes in email summaries

## Key Changes Summary

### 1. Enhanced Product Data Structure

**Before:**
```javascript
{
  id: "01090",
  title: "The Olive Tree Gift",
  status: "active"
}
```

**After:**
```javascript
{
  id: "01090",
  title: "The Olive Tree Gift",
  status: "active",
  price: 24.90,              // NEW
  currency: "GBP",           // NEW
  availability: "in stock"    // NEW
}
```

### 2. Enhanced Change Detection

**Before:**
- REMOVED
- NEW

**After:**
- REMOVED
- NEW
- **PRICE_CHANGE** (new!)
- **TITLE_CHANGE** (new!)
- **AVAILABILITY_CHANGE** (new!)

### 3. Enhanced Sheet Structures

**Current Snapshot sheets:**
- Before: `Product ID | Title | Status | Last Updated`
- **After: `Product ID | Title | Status | Price | Currency | Availability | Last Updated`**

**Changes sheets:**
- Before: `Date | Product ID | Change Type | Title | Status | Notes`
- **After: `Date | Product ID | Change Type | Title | Status | Old Price | New Price | Price Change % | Notes`**

**Outliers Report:**
- Before: `Client | Product ID | Change Type | Date | Title | Days Since | Flag`
- **After: `Client | Product ID | Change Type | Date | Title | Days Since | Old Price | New Price | Price Change % | Flag`**

## Migration Steps

### Step 1: Backup Current Script

1. Go to your Google Sheet
2. Extensions → Apps Script
3. File → Make a copy (save current version)

### Step 2: Replace Script Code

1. Copy the enhanced script from `GMC_Product_Tracker_Enhanced.gs`
2. Paste into Apps Script editor (replace existing code)
3. File → Save

### Step 3: Update Existing Sheet Headers

The script will automatically create new sheets with correct headers, but existing sheets need manual updates:

**For each client's "Current" and "Previous" sheets:**

Current header:
```
Product ID | Title | Status | Last Updated
```

New header (add 3 columns):
```
Product ID | Title | Status | Price | Currency | Availability | Last Updated
```

**For each client's "Changes" sheet:**

Current header:
```
Date Detected | Product ID | Change Type | Product Title | Status | Notes
```

New header (add 3 columns):
```
Date Detected | Product ID | Change Type | Product Title | Status | Old Price | New Price | Price Change % | Notes
```

### Step 4: Test on One Client

1. In Apps Script, run `dailyProductCheck()` manually
2. Check Tree2mydoor sheets to verify:
   - Current sheet now has Price, Currency, Availability columns populated
   - If any products changed price today, they appear in Changes sheet with price data
3. Check logs for errors

### Step 5: Regenerate Outliers Report

1. Run `generateOutliersReport()` manually
2. Verify "Outliers Report" sheet now has price columns
3. Check email report includes price changes

### Step 6: Full Rollout

Once tested successfully:
1. Let daily trigger run automatically
2. Existing daily/weekly triggers will use new script
3. Monitor for 1-2 weeks to ensure data quality

## What the Enhanced Version Does

### Price Change Detection

**Example scenario:**

**Day 1 (Oct 25):**
```
Product 01090: The Olive Tree Gift
Price: £29.90
Status: active
```

**Day 2 (Oct 26):**
```
Product 01090: The Olive Tree Gift
Price: £24.90  ← CHANGED!
Status: active
```

**Changes sheet entry created:**
```
Date: 2025-10-26
Product ID: 01090
Change Type: PRICE_CHANGE
Title: The Olive Tree Gift
Old Price: 29.90
New Price: 24.90
Price Change %: -16.72
Notes: Price changed from £29.90 to £24.90 (-16.72%)
```

**Outliers Report:**
- Flags this as "💰 Significant Price Change" (±15% or more)
- Ready for performance analysis after 28 days

### New Outliers Report Flags

**Before:**
- 🔴 Recent Change (last 7 days)
- ⚠️ Product Removed
- 📊 Ready to Analyze (28-56 days old)

**After (added):**
- 💰 **Significant Price Change** (±15% or more) - New flag!

### Enhanced Email Report

**Before:**
```
Summary:
🔴 Recent Changes: 5
⚠️ Products Removed: 2
📊 Ready to Analyze: 3
```

**After:**
```
Summary:
🔴 Recent Changes: 5
⚠️ Products Removed: 2
💰 Significant Price Changes (±15%+): 4  ← NEW!
📊 Ready to Analyze: 3
```

Table now includes "Price Change" column showing percentage.

## Example Use Case: Tree2mydoor

**Scenario:** Product 01090 had massive click spike Oct 27-28

**With original script:**
- ✅ Can see product wasn't removed (still in current snapshot)
- ❌ Can't see if price changed

**With enhanced script:**
- ✅ Can see product wasn't removed
- ✅ **Can see price dropped from £29.90 → £24.90 (-16.7%) on Oct 26**
- ✅ **Correlates price drop with click spike timing**
- ✅ **Gets flagged in Outliers Report as "💰 Significant Price Change"**

After 28 days:
- Gets flagged as "📊 Ready to Analyze"
- Performance analysis shows: Price drop → Click increase 1,900% → Revenue +£2,500/week

## Backward Compatibility

The enhanced script is **fully backward compatible**:

- ✅ Existing data in sheets remains intact
- ✅ Existing daily/weekly triggers continue working
- ✅ New columns are added, old columns unchanged
- ✅ Missing price data (old products) shows as blank, doesn't break anything

**Migration is safe and non-destructive!**

## Testing Checklist

Before deploying to production:

- [ ] Backup current script
- [ ] Copy enhanced script to Apps Script editor
- [ ] Update sheet headers manually (or run `createAllTabs()`)
- [ ] Run `dailyProductCheck()` manually on one client
- [ ] Verify price data appears in Current sheet
- [ ] Verify price changes (if any) logged in Changes sheet
- [ ] Run `generateOutliersReport()` manually
- [ ] Check Outliers Report has price columns
- [ ] Receive test email with price change summary
- [ ] Monitor logs for errors
- [ ] Let daily trigger run for 3 days
- [ ] Confirm no issues, deploy to all clients

## Troubleshooting

### "Price column shows blank"

**Cause:** GMC API didn't return price for that product

**Fix:** Check product in Merchant Center - may be missing price data

### "Old price changes show as blank"

**Cause:** Previous snapshot didn't have price data (pre-migration)

**Expected:** Normal during transition period. After first run, all new data will have prices.

### "Script execution exceeded maximum time"

**Cause:** Processing too many clients at once

**Fix:** Split clients into batches, run separately

## Next Steps After Migration

Once the enhanced script is running:

1. **Let it run for 7 days** to build price history
2. **Check Outliers Report weekly** for significant price changes
3. **Wait 28 days** for first "Ready to Analyze" price changes
4. **Use Claude Code** to run performance impact analysis:
   - "Analyze performance impact of price changes in the Outliers Report"
   - Claude will fetch Google Ads data, correlate with price changes
   - Results written back to sheets

## Benefits of This Approach

✅ **No new infrastructure** - Uses existing Apps Script
✅ **Already running daily** - Just enhances existing automation
✅ **Direct GMC API access** - Gets accurate price data from source
✅ **Integrated with existing workflow** - Same sheets, same emails
✅ **Backward compatible** - Safe to deploy
✅ **Low maintenance** - Apps Script handles everything

## Support

Questions about migration?
- Check Apps Script execution logs
- Review function comments in enhanced script
- Test on one client first before full rollout

---

**Ready to migrate?** Follow the steps above and you'll have price tracking running in ~30 minutes!
