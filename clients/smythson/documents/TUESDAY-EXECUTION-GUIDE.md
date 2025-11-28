# Smythson Asset Swap - Tuesday Execution Guide
**Date:** December 2nd, 2025
**Task:** Swap Black Friday assets to Christmas/standard messaging
**Regions:** UK, US, EUR, ROW

---

## ⚠️ CRITICAL PRE-FLIGHT CHECKS

**STOP! Before running anything, verify:**

### 1. Spreadsheet Data Validation
Open the master spreadsheet and verify:
- **Spreadsheet ID:** `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`
- **URL:** https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit

**Check each tab (UK, US, EUR, ROW):**
- [ ] Campaign names match Google Ads exactly (no extra spaces)
- [ ] Asset group names match Google Ads exactly (case-sensitive)
- [ ] All image asset IDs are valid (12-digit numbers)
- [ ] No duplicate image IDs in same row
- [ ] Text assets meet character limits (headlines ≤30, descriptions ≤90)

**KNOWN ISSUES TO FIX:**
- **UK Row 5 (Black Friday Travel Bags):** Only has 1 portrait image, needs at least 1 landscape + 1 square
  - Add landscape image ID to column BB (ratio > 1.1, e.g., 1200×628)
  - Add square image ID to column BC (ratio ~1.0, e.g., 1200×1200)
  - Use Asset Library Browser to find suitable images

### 2. Environment Setup
```bash
# Navigate to scripts directory
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

# Verify you're in correct location
pwd
# Should output: /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

# List available scripts
ls -lh *.py
```

### 3. Create Backup (MANDATORY)
```bash
# Export current assets before making ANY changes
python3 export-current-assets.py --region all
```

**Expected output:**
```
Exported UK assets to: data/asset-backups/2025-12-02-uk-assets.json
Exported US assets to: data/asset-backups/2025-12-02-us-assets.json
Exported EUR assets to: data/asset-backups/2025-12-02-eur-assets.json
Exported ROW assets to: data/asset-backups/2025-12-02-row-assets.json
```

**Verify backups created:**
```bash
ls -lh data/asset-backups/2025-12-02-*
```

---

## 🧪 DRY RUN PHASE (MANDATORY)

### Step 1: Text Assets Dry Run
```bash
python3 apply-text-assets-from-sheet.py --region all --dry-run
```

**What to look for:**
- [ ] No errors finding asset groups
- [ ] All campaign/asset group names match
- [ ] Text asset counts look correct (3-15 headlines, 1-5 long headlines, 2-5 descriptions)
- [ ] Should see `[DRY RUN]` prefix on all operations

**Expected output:**
```
Regions processed: 4
Successful: 4 ['uk', 'us', 'eur', 'row']
Failed: 0 []
```

### Step 2: Image Assets Dry Run WITH VALIDATION
```bash
python3 apply-image-assets-from-sheet.py --region all --dry-run
```

**CRITICAL: Review validation output for EVERY asset group**

**✅ PASSING validation looks like:**
```
[5/15] Finding asset group...
  Campaign: SMY | UK | P Max | H&S
  Asset Group: Black Friday Heroes & Sidekicks
    ✅ Found unique match: Asset Group 6598678947

  Asset Group: Black Friday Heroes & Sidekicks
    Campaign: SMY | UK | P Max | H&S
    Asset Group ID: 6598678947
    Spreadsheet image assets: 19
    Validating image type requirements...
    ✅ Validation passed - Image distribution:
       Landscape: 8
       Square: 7
       Portrait: 4
    [DRY RUN] Would link 19 image assets
```

**❌ FAILING validation looks like:**
```
[4/15] Finding asset group...
  Campaign: SMY | UK | P Max | H&S
  Asset Group: Black Friday Travel Bags
    ✅ Found unique match: Asset Group 6625003098

  Asset Group: Black Friday Travel Bags
    Campaign: SMY | UK | P Max | H&S
    Asset Group ID: 6625003098
    Spreadsheet image assets: 1
    Validating image type requirements...
    ❌ VALIDATION FAILED: New images don't meet PMax requirements
    Missing required types: MARKETING_IMAGE, SQUARE_MARKETING_IMAGE
    Current distribution:
      - Landscape (MARKETING_IMAGE): 0
      - Square (SQUARE_MARKETING_IMAGE): 0
      - Portrait (PORTRAIT_MARKETING_IMAGE): 1
    Requirements:
      - At least 1 landscape (MARKETING_IMAGE)
      - At least 1 square (SQUARE_MARKETING_IMAGE)
    Fix: Add missing image types to the spreadsheet before running.
```

**If ANY validation failures:**
1. **STOP** - Do not proceed to live execution
2. Open spreadsheet and find the failing asset group
3. Add missing image types (landscape or square)
4. Use Asset Library Browser to find suitable images:
   ```bash
   # UK region
   python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
       --customer-id 8573235780 --manager-id 2569949686
   ```
5. Re-run dry-run until ALL validations pass
6. Expected final output:
   ```
   Regions processed: 4
   Successful: 4 ['uk', 'us', 'eur', 'row']
   Failed: 0 []
   ```

### Step 3: Combined Dry Run (Text + Images)
```bash
python3 apply-all-assets.py --region all --dry-run
```

**Expected output:**
```
============================================================
TEXT ASSETS - UK
============================================================
[Shows text asset operations...]

============================================================
IMAGE ASSETS - UK
============================================================
[Shows image validation and operations for each asset group...]

✅ UK: Text and image assets applied successfully

[Repeats for US, EUR, ROW...]

============================================================
SUMMARY
============================================================
Regions processed: 4
Successful: 4 ['uk', 'us', 'eur', 'row']
Failed: 0 []
```

**CHECKPOINT:**
- [ ] All dry runs completed successfully
- [ ] No validation failures
- [ ] All asset groups found and matched
- [ ] Image distributions look correct
- [ ] Backups created

**IF ANY ISSUES:** Fix them now before proceeding!

---

## 🚀 LIVE EXECUTION PHASE

### ⚠️ FINAL CONFIRMATION
Before running live, confirm:
- [ ] Backups created and verified
- [ ] All dry runs passed with 0 failures
- [ ] All image validations passed
- [ ] Spreadsheet data is correct and complete
- [ ] You're ready to update LIVE campaigns

**Once you run this, changes will be IMMEDIATELY applied to live Google Ads campaigns.**

### Phase 1: Remove Black Friday Countdown from RSAs

**IMPORTANT: Do this FIRST before PMAX asset updates**

The RSAs currently have Black Friday countdown timers (added on Nov 26) that need to be removed:
- UK: 27 RSAs with countdown
- USA: 41 RSAs with countdown
- EUR: 14 RSAs with countdown
- ROW: 4 RSAs with countdown
- Total: 86 RSAs across 4 accounts

**Steps:**

1. **Import pre-generated CSV to Google Ads Editor:**
   ```
   Location: /Users/administrator/Documents/PetesBrain/clients/smythson/data/remove_bf_countdown_all_regions.csv
   ```

2. **Import instructions:**
   - Open Google Ads Editor
   - Load ALL Smythson accounts (UK, USA, EUR, ROW)
   - Account > Import > From file...
   - Select: `/clients/smythson/data/remove_bf_countdown_all_regions.csv`
   - Review (should show 86 ads to be EDITED across all accounts)
   - Process > Review > Post

3. **Verification:**
   - [ ] 86 RSAs updated (27 UK + 41 USA + 14 EUR + 4 ROW)
   - [ ] Import shows "Edit" not "Add"
   - [ ] No errors or warnings
   - [ ] Spot-check 2-3 RSAs in Google Ads UI to confirm countdown removed

**Duration:** ~5 minutes

**If CSV doesn't exist or needs regeneration:**
```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

# Regenerate the removal CSV
python3 remove_bf_countdown.py
```

**Troubleshooting:**
- **"Invalid account specified"**: Ensure all 4 accounts loaded in Editor (UK, USA, EUR, ROW)
- **Import shows "Add" instead of "Edit"**: CSV out of sync, regenerate fresh CSV
- **"Asset group not found"**: Campaign names changed, regenerate CSV from current state

---

### Phase 2: Update PMAX Assets

**After RSA countdowns removed, proceed with PMAX asset swap:**

```bash
python3 apply-all-assets.py --region all
```

**The script will:**
1. Show a 5-second countdown
2. Process each region in order: UK → US → EUR → ROW
3. For each asset group:
   - Validate image types BEFORE making changes
   - Apply text assets (create new, link, remove old)
   - Apply image assets (validate, link new, remove old)
4. Report success/failure per region

**Monitor output for:**
- [ ] Each asset group shows "✓ Applied successfully"
- [ ] Image validation passes for each asset group
- [ ] No API errors (400, 401, 403, 500)
- [ ] Final summary shows 0 failures

**Expected duration:** ~5-10 minutes for all regions

---

## ✅ POST-EXECUTION VERIFICATION

### Step 1: Verify in Google Ads UI
Open Google Ads and spot-check a few asset groups:

**UK Account (8573235780):**
- Campaign: SMY | UK | P Max | Bags
- Asset Group: Bags - High Earners
- Check: Text assets updated, images updated

**US Account (7808690871):**
- Campaign: SMY | US | P Max | H&S
- Asset Group: (any asset group)
- Check: Text and images match spreadsheet

### Step 2: Monitor Performance
For the next 24-48 hours:
- [ ] Check campaign performance hasn't dropped significantly
- [ ] Verify ads are serving with new creative
- [ ] Look for any disapprovals or policy issues

### Step 3: Keep Backups
**DO NOT DELETE backups for at least 7 days.**

Backup location: `/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/data/asset-backups/`

---

## 🚨 EMERGENCY ROLLBACK

If something goes wrong and you need to revert:

### Rollback Single Region
```bash
# Dry run first to see what will be restored
python3 rollback-to-backup.py --region uk --dry-run

# Execute rollback
python3 rollback-to-backup.py --region uk
```

### Rollback All Regions
```bash
python3 rollback-to-backup.py --region all
```

**This will:**
1. Read the most recent backup file (2025-12-02-{region}-assets.json)
2. Restore all text assets to their previous state
3. **Restore all image assets to their previous state** (NEW!)
4. Complete automatic recovery - no manual work needed

---

## 📋 Quick Reference Commands

### Asset Library Browser (Find Image IDs)
```bash
# UK
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 8573235780 --manager-id 2569949686

# US
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 7808690871 --manager-id 2569949686

# EUR
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 7679616761 --manager-id 2569949686

# ROW
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py \
    --customer-id 5556710725 --manager-id 2569949686
```

### View Current Assets (Before Changes)
```bash
# Export without applying
python3 export-current-assets.py --region uk
```

### Test Single Region First
```bash
# If nervous, test UK only first
python3 apply-all-assets.py --region uk --dry-run
python3 apply-all-assets.py --region uk

# Then do remaining regions
python3 apply-all-assets.py --region us
python3 apply-all-assets.py --region eur
python3 apply-all-assets.py --region row
```

---

## 🎯 Success Criteria

**Execution is successful when:**
- [ ] All 4 regions processed with 0 failures
- [ ] All asset groups show validation passed
- [ ] Text assets updated in Google Ads UI
- [ ] Images updated in Google Ads UI
- [ ] No API errors or warnings
- [ ] Campaign performance stable after 24 hours
- [ ] Backups safely stored

---

## 📞 Troubleshooting

### "Asset group not found"
**Problem:** Campaign or Asset Group name in spreadsheet doesn't match Google Ads
**Fix:** Compare spreadsheet names with Google Ads UI, watch for extra spaces

### "VALIDATION FAILED: Missing required types"
**Problem:** Asset group needs at least 1 landscape AND 1 square image
**Fix:** Add missing image types to spreadsheet, use Asset Library Browser

### "DUPLICATE_RESOURCE"
**Problem:** Same image ID listed multiple times in spreadsheet
**Fix:** Script should auto-deduplicate, but check spreadsheet for duplicates

### "NOT_ENOUGH_MARKETING_IMAGE_ASSET"
**Problem:** Removing images left asset group without required type
**Fix:** This shouldn't happen with new validation, but rollback if it does

### Script hangs or times out
**Problem:** Network issue or API rate limit
**Fix:** Wait 5 minutes, re-run from where it stopped (idempotent)

---

## 📊 Regional Summary

| Region | Customer ID | Asset Groups | Notes |
|--------|-------------|--------------|-------|
| UK | 8573235780 | 26 | Largest region, test first |
| US | 7808690871 | 15 | Standard configuration |
| EUR | 7679616761 | 12 | Standard configuration |
| ROW | 5556710725 | 3 | Smallest region |

**Total:** 56 asset groups across 4 regions

---

## 📝 Checklist Summary

**Pre-Flight:**
- [ ] Fix Travel Bags spreadsheet data (add landscape + square)
- [ ] Navigate to scripts directory
- [ ] Create backups (export-current-assets.py --region all)
- [ ] Verify backups created

**Dry Run:**
- [ ] Text dry run passed (--region all --dry-run)
- [ ] Image dry run passed with ALL validations ✅
- [ ] Combined dry run passed (apply-all-assets.py)

**Live:**
- [ ] Final confirmation before execution
- [ ] Run: python3 apply-all-assets.py --region all
- [ ] Monitor output for errors
- [ ] Verify in Google Ads UI

**Post:**
- [ ] Spot-check campaigns in UI
- [ ] Monitor performance for 24-48 hours
- [ ] Keep backups for 7 days

---

**Good luck! 🚀**
