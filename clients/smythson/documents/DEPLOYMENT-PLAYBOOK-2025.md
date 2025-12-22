# Smythson Text Asset Deployment Playbook 2025

**Purpose:** Bulletproof deployment process for updating RSA and Performance Max text/image assets across 4 regions (UK, USA, EUR, ROW).

**Last Updated:** 15th December 2025
**Next Deployment:** 24th December 2025 (Christmas Eve - Sale Copy)

---

## Quick Start: What Are You Deploying?

### Decision Tree

```
┌─ RSA Text Updates? ────────────────────────────────────┐
│  New headlines/descriptions for Responsive Search Ads  │
│  → Section 1: RSA Workflow (30-40 mins)                │
└────────────────────────────────────────────────────────┘

┌─ PMax Text Updates? ───────────────────────────────────┐
│  New headlines/descriptions for Performance Max        │
│  → Section 2: PMax Text Workflow (10-15 mins)          │
└────────────────────────────────────────────────────────┘

┌─ PMax Image Updates? ──────────────────────────────────┐
│  New images for Performance Max asset groups           │
│  → Section 3: PMax Image Workflow (60 mins)            │
└────────────────────────────────────────────────────────┘
```

**Deploying All Three?**
- Order: RSAs first → PMax text → PMax images
- Total time: ~2 hours
- Consider staging over 2 days

---

## Section 1: RSA Workflow (Google Ads Editor)

### Overview

**What:** Update Responsive Search Ad headlines and descriptions
**How:** CSV import via Google Ads Editor
**Time:** 30-40 minutes
**Regions:** UK (27 ads), USA (1 ad), EUR (1 ad), ROW (1 ad)

### Google Sheet Source

**Sheet ID:** `189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo`

**Tabs:**
- USA (RSA headlines/descriptions)
- EUR (RSA headlines/descriptions)
- ROW (RSA headlines/descriptions)
- UK (if exists - or uses full sheet)

### Pre-Flight Checklist (Day Before Deployment)

Run on: **23rd December 2025**

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Step 1: Validate existing CSVs meet minimums
python3 verify-rsa-csvs.py

# Expected output:
# ✅ UK: ALL 27 ADS MEET MINIMUM REQUIREMENTS (3 headlines, 2 descriptions)
# ✅ USA: ALL 1 ADS MEET MINIMUM REQUIREMENTS
# ✅ EUR: ALL 1 ADS MEET MINIMUM REQUIREMENTS
# ✅ ROW: ALL 1 ADS MEET MINIMUM REQUIREMENTS

# Step 2: Check CSV files exist
ls -lh ../data/DEPLOY-*.csv

# Expected: 4 CSV files (UK, USA, EUR, ROW)
```

**If validation fails:**
1. Check spreadsheet has minimum 3 headlines, 2 descriptions per ad
2. Regenerate CSVs (see "Regenerating CSVs" section below)
3. Re-run validation

### Deployment Day Steps

#### Step 1: Open Google Ads Editor (5 mins)

1. Launch Google Ads Editor
2. **Load all 4 Smythson accounts:**
   - UK: 8573235780
   - USA: 7808690871
   - EUR: 7679616761
   - ROW: 5556710725
3. Click **"Get recent changes"** (sync with live)
4. Wait for sync to complete

#### Step 2: Import UK RSAs (10 mins)

1. In Google Ads Editor: **Account** → **Import** → **From file...**

2. **Select file:**
   ```
   /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-uk-CHANGES-ONLY.csv
   ```

3. **Import type:** Make multiple changes using CSV

4. **CRITICAL CHECKS:**
   - ✅ Account shows: **8573235780** (UK)
   - ✅ Number of ads: **13** (or current count)
   - ✅ Action shows: **"Edit"** (NOT "Add")
   - ✅ Headlines and descriptions look correct

5. Click **"Apply"**

6. Review changes in Editor (should show ads with modified icon)

#### Step 3: Import USA RSAs (5 mins)

1. **Account** → **Import** → **From file...**

2. **Select file:**
   ```
   /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-usa-CHANGES-ONLY.csv
   ```

3. **Verify:**
   - Account: 7808690871 (USA)
   - Ads: 1
   - Action: "Edit"

4. Apply changes

#### Step 4: Import EUR RSAs (5 mins)

1. **Account** → **Import** → **From file...**

2. **Select file:**
   ```
   /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-eur-CHANGES-ONLY.csv
   ```

3. **Verify:**
   - Account: 7679616761 (EUR)
   - Ads: 14 (or current count)
   - Action: "Edit"

4. Apply changes

#### Step 5: Import ROW RSAs (5 mins)

**⚠️ WARNING:** ROW may have pinning issues. If import shows "Add" instead of "Edit", **skip ROW** and manually update in Google Ads UI.

1. **Account** → **Import** → **From file...**

2. **Select file (if available):**
   ```
   /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-row-CHANGES-ONLY.csv
   ```

3. **If no file exists:** ROW has no changes - skip this step

4. **If import shows "Add":** Cancel import - pinning issue detected

5. Apply changes (only if "Edit" shows)

#### Step 6: Post Changes to Google Ads (2 mins)

1. Click **"Post"** button in Google Ads Editor

2. **Select all 4 accounts** (or accounts with changes)

3. **Review post summary:**
   - Confirm number of RSA updates matches expectation
   - Check for errors/warnings

4. Click **"Post changes"**

5. Wait for confirmation: **"Successfully posted"**

#### Step 7: Verify in Google Ads UI (5 mins)

1. Open Google Ads web interface

2. Navigate to: **Campaigns** → **SMY | UK | Search | Brand Exact**

3. Go to: **Ads & assets** → **Ads**

4. **Open one updated RSA** (look for recent "Last modified" date)

5. **Verify:**
   - ✅ Headlines match new copy from spreadsheet
   - ✅ Descriptions match new copy
   - ✅ Status: "Eligible" (may show "Under review" briefly)
   - ✅ Performance history preserved

6. Repeat spot-check for USA/EUR/ROW (1 ad each)

### Troubleshooting RSA Import

#### Error: "Column mapping incorrect"

**Cause:** CSV headers don't match Google Ads Editor format

**Fix:**
1. Check CSV has headers: Account, Action, Campaign, Ad group, Ad ID, Headline 1, Description 1, Final URL
2. Re-export from Google Ads Editor to get correct header format
3. Regenerate CSV with correct headers

#### Error: "Ad not found"

**Cause:** Ad ID doesn't exist in the account

**Fix:**
1. Verify Account ID is correct in CSV
2. Check ad hasn't been deleted in Google Ads
3. Re-export current state and regenerate CSV

#### Error: "Too few headlines/descriptions"

**Cause:** CSV has fewer than 3 headlines or 2 descriptions

**Fix:**
1. Check spreadsheet has minimum requirements
2. Run `verify-rsa-csvs.py` to identify which ads are short
3. Add missing headlines/descriptions to spreadsheet
4. Regenerate CSV

#### Import Shows "Add" Instead of "Edit"

**Cause 1:** Ad has pinned headlines (CSVs don't include pinning info)
**Fix:** Manually update in Google Ads UI (copy/paste text)

**Cause 2:** Ad ID mismatch
**Fix:** Re-export current state, verify Ad IDs match

---

## Section 2: PMax Text Workflow (API)

### Overview

**What:** Update Performance Max text assets (headlines, long headlines, descriptions)
**How:** Python script via Google Ads API
**Time:** 10-15 minutes per region
**Regions:** UK, USA, EUR, ROW (independent deployments)

### Google Sheet Source

**Sheet ID:** `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`

**Tabs:**
- UK PMax Assets
- US PMax Assets
- EUR PMax Assets
- ROW PMax Assets

**Columns:**
- A-B: Campaign ID, Asset Group Name
- C-Q: Headlines 1-15 (max 30 chars each)
- R-V: Long Headlines 1-5 (max 90 chars each)
- W-AA: Descriptions 1-5 (max 90 chars each)

### Pre-Flight Checklist (Day Before Deployment)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Step 1: Create backup of current PMax text assets
python3 export-current-assets.py --region all

# Expected output:
# Exported UK assets to: data/backups/2025-12-23-uk-pmax-text.json
# Exported US assets to: data/backups/2025-12-23-us-pmax-text.json
# Exported EUR assets to: data/backups/2025-12-23-eur-pmax-text.json
# Exported ROW assets to: data/backups/2025-12-23-row-pmax-text.json

# Step 2: Verify backups created
ls -lh ../data/backups/2025-12-23-*

# Step 3: Dry-run deployment (NO changes made)
python3 apply-pmax-text-assets-v2.py --region uk --dry-run

# Check output for:
# ✅ All asset groups found
# ✅ Text assets meet minimums
# ✅ [DRY RUN] prefix on all operations
```

**If dry-run fails:**
1. Check spreadsheet campaign/asset group names match Google Ads exactly
2. Verify text meets character limits (H: 30, LH: 90, D: 90)
3. Check minimum requirements: 3+ headlines, 1+ long headline, 2+ descriptions

### Deployment Day Steps

#### Step 1: UK PMax Text Deployment (10 mins)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Final dry-run check
python3 apply-pmax-text-assets-v2.py --region uk --dry-run

# If dry-run passes, execute live
python3 apply-pmax-text-assets-v2.py --region uk
```

**Monitor output:**
- Look for: `✓ Applied successfully` for each asset group
- Check for: `[BACKUP]` confirmation (backup saved)
- Look for: `[VERIFIED]` checks (API queries confirm changes)

**Expected duration:** 5-10 minutes for UK (largest region)

#### Step 2: USA/EUR/ROW PMax Text (Optional)

**Only deploy if Alex has updated those regions in the spreadsheet.**

```bash
# USA
python3 apply-pmax-text-assets-v2.py --region us

# EUR
python3 apply-pmax-text-assets-v2.py --region eur

# ROW
python3 apply-pmax-text-assets-v2.py --region row
```

#### Step 3: Verify in Google Ads UI (5 mins)

1. Open Google Ads web interface

2. Navigate to: **Campaigns** → **Performance Max campaigns**

3. Select: **SMY | UK | P Max | Bags** (or any UK PMax campaign)

4. Click: **Asset groups** tab

5. **Open one asset group** (e.g., "Bags - High Earners")

6. **Verify:**
   - ✅ Headlines section shows new text
   - ✅ Descriptions section shows new text
   - ✅ Asset group status: "Eligible"
   - ✅ Campaign still serving

### Troubleshooting PMax Text

#### Error: "Asset group not found"

**Cause:** Campaign or Asset Group name in spreadsheet doesn't match Google Ads

**Fix:**
1. Open Google Ads UI → Navigate to Performance Max campaign
2. Copy EXACT campaign name (with spaces, capitalization, punctuation)
3. Copy EXACT asset group name
4. Update spreadsheet with exact names
5. Re-run deployment

#### Error: "Text asset too long"

**Cause:** Headline >30 chars, Long Headline >90 chars, or Description >90 chars

**Fix:**
1. Check spreadsheet columns C-AA for character counts
2. Shorten text to meet limits
3. Re-run deployment

#### Error: "NOT_ENOUGH_TEXT_ASSET"

**Cause:** Asset group needs minimum: 3 headlines, 1 long headline, 2 descriptions

**Fix:**
1. Check spreadsheet row has minimum requirements
2. Add missing text assets
3. Re-run deployment

---

## Section 3: PMax Image Workflow (API)

### Overview

**What:** Update Performance Max image assets
**How:** Python script reads image IDs from spreadsheet, links via API
**Time:** 60 minutes (includes Alex selecting images)
**Complexity:** High (requires Alex to populate spreadsheet with Asset IDs)

### Google Sheet Source

**Sheet ID:** `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`

**Columns AW-BT** (21 image columns):
- Landscape images (1.91:1 aspect ratio)
- Square images (1:1 aspect ratio)
- Portrait images (4:5 aspect ratio)
- Logo images

### Pre-Requisite: Alex Must Select Images

**Before deployment, Alex needs to:**
1. Run Asset Library Browser (see "HOW-TO-SELECT-IMAGES-FOR-ALEX.md")
2. Browse images by category
3. Copy Asset IDs
4. Paste into spreadsheet columns AW-BT

**Minimum Requirements:**
- At least 1 landscape image (MARKETING_IMAGE)
- At least 1 square image (SQUARE_MARKETING_IMAGE)

### Pre-Flight Checklist (Day Before Deployment)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Step 1: Verify Alex populated image columns
# Open spreadsheet and check columns AW-BT have Asset IDs

# Step 2: Dry-run image deployment (NO changes made)
python3 apply-image-assets-from-sheet.py --region uk --dry-run

# Check output for:
# ✅ All asset groups found
# ✅ Validation passed - Image distribution (1+ landscape, 1+ square)
# ❌ VALIDATION FAILED: Missing required types (if this shows, need more images)

# Step 3: If validation passes for UK, test all regions
python3 apply-image-assets-from-sheet.py --region all --dry-run
```

**If validation fails:**
1. Check which asset groups failed (shown in output)
2. Ask Alex to add missing image types (landscape or square)
3. Re-run dry-run

### Deployment Day Steps

#### Step 1: Final Verification (5 mins)

1. **Open spreadsheet:**
   ```
   https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit
   ```

2. **Check UK PMax Assets tab, columns AW-BT:**
   - ✅ All rows (asset groups) have image Asset IDs
   - ✅ Each row has at least 1 landscape + 1 square
   - ✅ Asset IDs are numeric (12-digit numbers)

#### Step 2: UK Image Deployment (20 mins)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Final dry-run
python3 apply-image-assets-from-sheet.py --region uk --dry-run

# If dry-run passes, execute live
python3 apply-image-assets-from-sheet.py --region uk
```

**Monitor output:**
- Look for: `✓ Applied successfully` for each asset group
- Check for: `✅ Validation passed - Image distribution`
- Watch for errors: `❌ VALIDATION FAILED`

**Expected duration:** 10-20 minutes for UK

#### Step 3: Verify in Google Ads UI (10 mins)

1. Open Google Ads web interface

2. Navigate to: **Campaigns** → **Performance Max** → **SMY | UK | P Max | Bags**

3. Click: **Asset groups** → Select one asset group

4. Scroll to: **Images** section

5. **Verify:**
   - ✅ New images appear
   - ✅ At least 1 landscape + 1 square present
   - ✅ No more than 20 total images
   - ✅ Asset group status: "Eligible"

#### Step 4: Deploy to Other Regions (Optional)

**Only if Alex has populated image IDs for those regions.**

```bash
# USA
python3 apply-image-assets-from-sheet.py --region us

# EUR
python3 apply-image-assets-from-sheet.py --region eur

# ROW
python3 apply-image-assets-from-sheet.py --region row
```

### Troubleshooting PMax Images

#### Error: "Asset group not found"

**Fix:** Same as PMax Text - verify campaign/asset group names match exactly

#### Error: "VALIDATION FAILED: Missing required types"

**Cause:** Asset group doesn't have at least 1 landscape + 1 square image

**Fix:**
1. Check spreadsheet row - which image types are missing?
2. Ask Alex to add missing image type
3. Re-run deployment

#### Error: "Image asset not found"

**Cause:** Asset ID doesn't exist in the account

**Fix:**
1. Verify Asset ID is correct (12-digit number)
2. Check Asset ID exists in Asset Library Browser
3. Replace with correct Asset ID

---

## Emergency Rollback Procedures

### When to Rollback

**Rollback if:**
- ✅ Campaigns stop serving (check status in Google Ads)
- ✅ Significant performance drop (>50% impressions lost)
- ✅ Policy violations / disapprovals
- ✅ Wrong text/images deployed

**Wait it out if:**
- Minor performance fluctuations (<20% change)
- Ads show "Under review" (normal, clears in 1-2 hours)
- Learning period reset message (expected for major changes)

### RSA Rollback (Google Ads Editor)

**Not easily reversible** - Google Ads Editor doesn't have built-in rollback.

**Options:**
1. **Manual revert in Google Ads UI** (5-10 mins per ad)
   - Open each updated RSA
   - Manually type old text back
   - Save changes

2. **Create new CSV with old text** (20 mins)
   - Find backup of previous CSV (if exists)
   - Import previous CSV via Google Ads Editor
   - Post changes

### PMax Text Rollback (Automated)

**Script:** `rollback-to-backup.py`

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# List available backups
ls -lt ../data/backups/2025-*-pmax-text.json

# Rollback UK to most recent backup (DRY RUN first)
python3 rollback-to-backup.py --region uk --dry-run

# If dry-run looks correct, execute live
python3 rollback-to-backup.py --region uk
```

**What it does:**
1. Reads backup JSON file
2. Removes current text assets
3. Recreates old text assets
4. Links old assets to asset groups
5. Verifies changes applied

**Duration:** 5-10 minutes per region

### PMax Image Rollback (Automated)

**Same as PMax Text** - uses `rollback-to-backup.py`

**Note:** Image backups are only created if `export-current-assets.py` was run with `--include-images` flag.

---

## Regenerating CSVs (If Needed)

### RSA CSVs

If spreadsheet changes or validation fails, regenerate CSVs:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Step 1: Fetch current RSA state from Google Ads API
python3 fetch_uk_rsa_current_state.py
python3 fetch_row_current_state.py
# (USA/EUR scripts may exist - check scripts/ folder)

# Step 2: Read spreadsheet and compare with current state
python3 rebuild_rsa_updates_from_spreadsheet.py

# Step 3: Generate CSVs from comparison JSON
python3 build_uk_from_full_sheet.py
python3 build_usa_from_sheet.py
python3 build_eur_updates_simple.py

# Step 4: Validate CSVs
python3 verify-rsa-csvs.py

# Step 5: Copy to clean deployment names
python3 create-final-rsa-deployments.py
```

**Output:** New CSV files in `/clients/smythson/data/`

---

## Account IDs Reference

| Region | Customer ID | Manager ID | Notes |
|--------|-------------|------------|-------|
| UK | 8573235780 | 2569949686 | Largest account |
| USA | 7808690871 | 2569949686 | Second largest |
| EUR | 7679616761 | 2569949686 | Multiple languages |
| ROW | 5556710725 | 2569949686 | Rest of world |

---

## Key File Locations

### Scripts
```
/clients/smythson/scripts/
├── apply-pmax-text-assets-v2.py (PMax text deployment)
├── apply-image-assets-from-sheet.py (PMax image deployment)
├── export-current-assets.py (Create backups)
├── rollback-to-backup.py (Emergency rollback)
├── verify-rsa-csvs.py (RSA validation)
└── rebuild_rsa_updates_from_spreadsheet.py (RSA CSV generation)
```

### Data Files
```
/clients/smythson/data/
├── DEPLOY-rsa-uk-CHANGES-ONLY.csv (UK RSA deployment)
├── DEPLOY-rsa-usa-CHANGES-ONLY.csv (USA RSA deployment)
├── DEPLOY-rsa-eur-CHANGES-ONLY.csv (EUR RSA deployment)
└── backups/ (PMax text/image backups)
```

### Documentation
```
/clients/smythson/
├── DEPLOYMENT-PLAYBOOK-2025.md (This file)
├── HOW-TO-SELECT-IMAGES-FOR-ALEX.md (Image selection guide)
├── MASTER-INDEX.md (Links to all docs)
├── documents/pmax-asset-application-workflow.md (Detailed PMax workflow)
└── reports/ (Deployment checklists and reports)
```

---

## Contact & Support

**If issues on Dec 24th:**
1. Check this playbook first
2. Check HOW-TO-SELECT-IMAGES-FOR-ALEX.md for image issues
3. Check MASTER-INDEX.md for links to detailed docs
4. Emergency contact: [Add contact info]

---

## Version History

| Date | Changes | Author |
|------|---------|--------|
| 15 Dec 2025 | Initial creation | PetesBrain |

---

**Last updated:** 15th December 2025
**Next review:** After 24th December 2025 deployment
