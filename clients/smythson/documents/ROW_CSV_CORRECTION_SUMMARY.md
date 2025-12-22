# ROW RSA CSV Correction Summary

## Problem Identified

The original ROW CSV (`row_rsa_updates_from_sheet.csv`) created a **duplicate ad** in the "Diaries and Organisers Diaries" campaign because:

1. **Included a REMOVED ad**: The spreadsheet contained 4 ads, but ad `784326640550` was REMOVED in Google Ads
2. **Missing proper #Original columns**: The processing script used spreadsheet data for BOTH current and new values, not actual Google Ads current state
3. **Result**: Google Ads Editor couldn't match the #Original columns and created a NEW ad instead of updating the existing one

## Root Cause

The original ROW processing script (`process_row_from_sheet_data.py`) had this logic:

```python
# WRONG - uses spreadsheet as both current and new
updates.append({
    'current_headlines': parsed['headlines'],  # From spreadsheet
    'new_headlines': parsed['headlines'],       # From spreadsheet
    ...
})
```

This meant the #Original columns in the CSV didn't match the actual current state in Google Ads.

## Solution

1. **Fetched actual current state** from Google Ads API for the 3 active ROW ads
2. **Created `row_rsa_current_state.json`** with real current headlines/descriptions from Google Ads
3. **Rebuilt the ROW update JSON** using proper comparison (current state vs spreadsheet)
4. **Regenerated the CSV** with correct #Original columns

## Corrected CSV Details

**File**: `/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/row_rsa_updates_from_sheet.csv`

**Account ID**: `5556710725` (ROW)

**Ads included** (3 active ads only):
- `784326640553` - SMY | ROW | Search | Brand Ai
- `773497251588` - SMY | ROW | Search | Brand Diaries and Organisers (the one that got duplicated)
- `784326640556` - SMY | ROW | Search | Competitor | Ai

**Excluded** (1 REMOVED ad):
- `784326640550` - SMY | AUS | Search | Brand Ai (REMOVED status in Google Ads)

**Verification results**:
- ✓ 3 ads in CSV (not 4)
- ✓ 19 #Original columns present
- ✓ Headlines clean (no description text in headline columns)
- ✓ Descriptions in correct columns
- ✓ Current = New for all ads (no changes needed, verification CSV)

## What Changed

| Aspect | Before | After |
|--------|--------|-------|
| **Ads in CSV** | 4 (including REMOVED ad) | 3 (active ads only) |
| **#Original columns** | ❌ Didn't match Google Ads | ✓ Match actual current state |
| **Current state source** | Spreadsheet (wrong) | Google Ads API (correct) |
| **Result when importing** | Creates duplicate ads | Updates existing ads |

## Next Steps

The corrected CSV is ready for import into Google Ads Editor. When you import it:

1. **Expected result**: Google Ads Editor should show "3 ads to be EDITED" (not created)
2. **No changes will be applied** because current = new (verification CSV)
3. **Purpose**: Verify the CSV structure is correct and won't create duplicates

## Cleanup Required

**In Google Ads Editor**, you need to:
1. Find and **delete the duplicate ad** that was created in "SMY | ROW | Search | Brand Diaries and Organisers" campaign
2. Verify there's only ONE ad with ID `773497251588` in that campaign after deletion

## Files Created/Updated

1. `/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/row_rsa_current_state.json` - Current state from Google Ads API (3 active ads)
2. `/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts/rebuild_row_rsa_from_current_state.py` - Corrected rebuild script
3. `/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/row_rsa_updates_from_sheet.json` - Corrected update JSON (3 ads)
4. `/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/row_rsa_updates_from_sheet.csv` - Corrected CSV (3 ads with #Original columns)

---

**Date**: 2025-12-15
**Issue**: ROW CSV created duplicate ad due to REMOVED ad inclusion and missing #Original columns
**Status**: ✓ RESOLVED
