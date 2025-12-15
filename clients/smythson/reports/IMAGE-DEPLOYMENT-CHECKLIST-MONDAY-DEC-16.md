# Smythson Monday Image Deployment Checklist
**Date**: Monday, 16th December 2025
**Type**: Performance Max Image Asset Replacement
**Script**: `apply-image-assets-from-sheet.py`
**Status**: ✅ Script paths fixed and ready to execute

---

## 🔴 CRITICAL: Pre-Deployment Verification

### 1. Verify Alex Has Updated Image Asset IDs

**Google Sheet**: [Smythson PMax Master Sheet](https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit)

**Check these columns for image asset IDs**:
- **UK ad copy** tab: Columns `BA` through `BU` (21 image columns)
- **US ad copy** tab: Columns `BA` through `BU`
- **EUR ad copy** tab: Columns `BA` through `BU`
- **ROW ad copy** tab: Columns `BA` through `BU`

**What to look for**:
- ✅ Image asset IDs should be numeric (e.g., `1234567890`)
- ✅ Each row (asset group) should have at least:
  - 1 landscape image (1.91:1 aspect ratio)
  - 1 square image (1:1 aspect ratio)
- ⚠️ Empty cells are OK (script will skip them)
- ❌ If columns are empty, **DO NOT PROCEED** - ask Alex first

---

## 📋 Deployment Workflow

### Pre-Deployment: Dry Run Test

**Purpose**: Verify script works and see what changes will be made **WITHOUT** actually applying them.

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Test UK region first
python3 apply-image-assets-from-sheet.py --region uk --dry-run

# If UK looks good, test all regions
python3 apply-image-assets-from-sheet.py --region all --dry-run
```

**What the dry-run output shows**:
- Campaign and asset group names
- Number of image assets to apply per asset group
- Image type distribution (landscape/square/portrait)
- Validation results (passes/fails PMax requirements)

**Expected output example**:
```
[1/X] Finding asset group...
  Campaign: UK | P1 | Category | Brand
  Asset Group: Brand - Collection Name
    ✅ Found unique match: Asset Group 123456 in Campaign 789012
  Asset Group: Brand - Collection Name
    Campaign: UK | P1 | Category | Brand
    Asset Group ID: 123456
    Spreadsheet image assets: 15
    Validating image type requirements...
    ✅ Validation passed - Image distribution:
       Landscape: 8
       Square: 5
       Portrait: 2
    [DRY RUN] Would link 15 image assets
    ✓ Applied successfully
```

**Stop if you see**:
- ❌ "Asset group not found" - Sheet has wrong campaign/asset group names
- ❌ "VALIDATION FAILED: Missing required types" - Need more landscape or square images
- ❌ "AMBIGUOUS: Multiple asset groups match" - Duplicate campaign/asset group names
- ❌ Any Python errors

---

### Deployment: Live Execution

**⚠️ ONLY proceed if dry-run completed successfully**

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Apply to UK region first
python3 apply-image-assets-from-sheet.py --region uk

# If UK succeeds, apply to all regions
python3 apply-image-assets-from-sheet.py --region all
```

**What happens during live execution**:
1. Script reads image asset IDs from Google Sheet
2. For each asset group:
   - Queries current image assets
   - Validates new images meet PMax requirements (1 landscape + 1 square minimum)
   - Queries image dimensions and auto-detects field types
   - Removes old image assets
   - Links new image assets
3. Reports success/failure for each asset group

**Expected duration**: 2-5 minutes per region (depending on number of asset groups)

---

## 🛡️ Safety Features Built Into Script

✅ **Pre-validation** - Checks images meet PMax requirements BEFORE removing any old images
✅ **Auto-type detection** - Queries dimensions and assigns correct field type (landscape/square/portrait)
✅ **20-image limit protection** - Smart removal/addition to never exceed limit
✅ **Unique matching** - Ensures campaign + asset group names match exactly ONE asset group
✅ **OAuth auto-refresh** - Handles token expiry automatically

---

## 📊 What the Script Does (Technical Details)

### Image Field Type Auto-Detection

The script queries image dimensions and determines field type by aspect ratio:

| Aspect Ratio | Field Type | Example Dimensions |
|--------------|------------|-------------------|
| **1.91:1** (landscape) | `MARKETING_IMAGE` | 1200x628, 1600x837 |
| **1:1** (square) | `SQUARE_MARKETING_IMAGE` | 1200x1200, 1000x1000 |
| **4:5** (portrait) | `PORTRAIT_MARKETING_IMAGE` | 960x1200, 800x1000 |

### Smart Removal/Addition Logic

**Scenario 1: Total ≤ 20 images (SAFE)**
1. Add ALL new images first
2. Remove ALL old images
→ No risk of hitting limit or violating minimums

**Scenario 2: Total > 20 images (OVERFLOW)**
1. Remove SOME old images to make room
2. Add ALL new images
3. Remove remaining old images
→ Ensures we never exceed 20-image limit

### Minimum Requirements (PMax API)

Per Google Ads API, each asset group MUST have:
- ✅ At least 1 `MARKETING_IMAGE` (landscape)
- ✅ At least 1 `SQUARE_MARKETING_IMAGE` (square)

Script validates BEFORE making any changes.

---

## 🚨 Troubleshooting

### Error: "Google Sheets OAuth token not found"

**Cause**: Missing or expired Google Sheets OAuth token

**Fix**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server
ls -la token.json  # Check if file exists
```

If missing, regenerate OAuth token via MCP server setup.

---

### Error: "Asset group not found"

**Cause**: Campaign or asset group name in spreadsheet doesn't match Google Ads

**Fix**:
1. Open Google Ads UI
2. Navigate to Performance Max campaigns
3. Copy EXACT campaign name and asset group name
4. Update spreadsheet with exact names (including spaces, capitalization, punctuation)

---

### Error: "VALIDATION FAILED: Missing required types"

**Cause**: New images don't meet PMax minimum requirements (1 landscape + 1 square)

**Fix**:
1. Check image asset IDs in spreadsheet
2. Verify at least 1 landscape (1.91:1) and 1 square (1:1) image included
3. Add missing image types to spreadsheet
4. Re-run dry-run to verify

---

### Error: "AMBIGUOUS: Multiple asset groups match"

**Cause**: Same campaign + asset group name exists multiple times in Google Ads

**Fix**:
1. Add asset group IDs to spreadsheet (requires script modification)
2. OR rename duplicate asset groups in Google Ads
3. OR process manually via Google Ads UI

---

## 📝 Post-Deployment Verification

### Check Image Asset Counts

**Via Google Ads UI**:
1. Navigate to: Campaigns → Performance Max → [Campaign] → Asset groups
2. Click each asset group
3. Verify images section shows:
   - ✅ New image assets (check by image file names)
   - ✅ At least 1 landscape + 1 square
   - ✅ No more than 20 total images

**Via Script** (optional):
```bash
# Re-run dry-run to see current state
python3 apply-image-assets-from-sheet.py --region uk --dry-run
```

---

## 🔄 Rollback Plan (If Issues Occur)

**If deployment causes issues** (e.g., campaigns stop serving, wrong images applied):

### Option 1: Re-run Script with Previous Image IDs

1. Check if you have backup of previous Google Sheet state
2. Restore old image asset IDs to spreadsheet
3. Re-run script with old IDs: `python3 apply-image-assets-from-sheet.py --region uk`

### Option 2: Manual Rollback via Google Ads UI

1. Navigate to: Campaigns → Performance Max → [Campaign] → Asset groups → [Asset group]
2. Go to Images section
3. Click "Remove" on incorrect images
4. Click "Add images" → Select from asset library → Choose correct images

### Option 3: Contact Google Ads Support

If campaigns stop serving due to image policy violations:
1. Check "Assets" tab for disapproval reasons
2. Remove disapproved images
3. Add compliant images
4. Wait 24-48 hours for review

---

## 📅 Timeline

**Monday, 16th December 2025**

| Time | Action | Duration |
|------|--------|----------|
| 09:00 | Verify Alex has updated image IDs in Google Sheet | 5 mins |
| 09:05 | Run dry-run test (UK region) | 2 mins |
| 09:07 | Review dry-run output, verify validation passes | 5 mins |
| 09:12 | Run live deployment (UK region) | 2 mins |
| 09:14 | Verify UK deployment via Google Ads UI | 10 mins |
| 09:24 | Run dry-run test (all regions) | 5 mins |
| 09:29 | Run live deployment (all regions) | 10 mins |
| 09:39 | Verify all regions via Google Ads UI | 20 mins |
| 09:59 | **COMPLETE** | |

**Total estimated time**: 1 hour

---

## ✅ Success Criteria

- ✅ Dry-run completes without errors for all regions
- ✅ Validation passes for all asset groups (1 landscape + 1 square minimum)
- ✅ Live execution reports "Applied successfully" for all asset groups
- ✅ Google Ads UI shows new images in asset groups
- ✅ Campaigns continue serving (check 2-4 hours after deployment)
- ✅ No image policy disapprovals (check "Assets" tab)

---

## 📞 Escalation

**If script fails or campaigns stop serving:**
1. Document exact error message and timestamp
2. Take screenshots of Google Ads UI (campaigns, asset groups, images)
3. Check if images are disapproved (policy violations)
4. If urgent, manually rollback via Google Ads UI
5. Report to Alex with error details for investigation

---

## 📄 Related Documentation

- **Script location**: `clients/smythson/scripts/apply-image-assets-from-sheet.py`
- **Google Sheet**: [Smythson PMax Master Sheet](https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit)
- **PMax workflow docs**: `clients/smythson/documents/pmax-asset-application-workflow.md`

---

**Generated**: 2025-12-15 by Claude Code
**Last updated**: 2025-12-15 (Paths fixed for .nosync directory)
