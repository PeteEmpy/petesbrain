# Smythson Asset Deployment - Tuesday Dec 2nd Pre-Flight Checklist

**Date Created**: 2025-11-27
**Deployment Date**: 2025-12-02
**Deployment Time**: TBD (recommend 10:00 AM to allow full business day for monitoring)
**Estimated Duration**: 15-20 minutes total execution

---

## Lessons Learned from Today's Devonshire Deployment

### Issues Encountered Today:
1. ❌ **Wrong Google Sheet format** - Created vertical instead of horizontal review format
2. ❌ **Tree2mydoor hardcoded content** - AI generated wrong client's assets
3. ❌ **Scripts ignored --csv parameters** - Used hardcoded paths instead
4. ❌ **Anthropic API key missing** - Module-level client not initialized
5. ❌ **User viewed old Google Sheet** - Multiple test sheets created confusion
6. ⏱️ **Workflow took ~4 hours** - Multiple debugging iterations required

### How Smythson Avoids These:
✅ **No AI generation** - All copy pre-approved in Google Sheet
✅ **No hardcoded client data** - Region-based configuration
✅ **Tested scripts** - Successful dry-run completed 2025-11-26
✅ **Single data source** - One master Google Sheet, no ambiguity
✅ **Shorter execution** - ~15 minutes vs 4 hours

---

## CRITICAL: What Could Go Wrong on Tuesday

### 🔴 **HIGH RISK** - Would Break Deployment

1. **Google Sheets API OAuth token expired**
   - **Symptom**: Script fails with authentication error
   - **Detection**: Run dry-run Monday evening
   - **Fix**: Re-authenticate Google Sheets MCP server
   - **Prevention**: Test OAuth token Monday 5 PM

2. **Google Ads API OAuth token expired**
   - **Symptom**: Script fails with 401 Unauthorized
   - **Detection**: Run dry-run Monday evening
   - **Fix**: Re-authenticate Google Ads MCP server
   - **Prevention**: Test OAuth token Monday 5 PM

3. **Google Sheet has incorrect campaign/asset group names**
   - **Symptom**: Script reports "Asset group not found"
   - **Detection**: Dry-run will catch this
   - **Fix**: Verify exact names match Google Ads UI
   - **Prevention**: Compare sheet to GAQL query results Monday

4. **Spreadsheet ID changed**
   - **Symptom**: Script fails to read data
   - **Detection**: Dry-run will catch this
   - **Fix**: Update SPREADSHEET_ID in scripts
   - **Prevention**: Verify sheet URL unchanged Monday

5. **Not enough text assets (< minimum requirements)**
   - **Symptom**: Script reports "Not enough headlines (X < 3)"
   - **Detection**: Dry-run will catch this
   - **Fix**: Add missing text assets to sheet
   - **Prevention**: Validate sheet meets minimums Monday

### 🟡 **MEDIUM RISK** - Would Cause Delays

6. **Network/API rate limits during bulk deployment**
   - **Symptom**: Script slows down or times out
   - **Detection**: Won't show in dry-run
   - **Fix**: Add retry logic or run regions sequentially
   - **Prevention**: Deploy during low-traffic time (10 AM UK)

7. **Asset group IDs changed since last backup**
   - **Symptom**: Script updates wrong asset group
   - **Detection**: Fresh backup will catch this
   - **Fix**: Use fresh backup from Tuesday morning
   - **Prevention**: Take backup immediately before deployment

8. **Python environment issues**
   - **Symptom**: ModuleNotFoundError or version conflicts
   - **Detection**: Dry-run will catch this
   - **Fix**: Use correct venv path in shebang
   - **Prevention**: Verify venv exists and has dependencies Monday

### 🟢 **LOW RISK** - Minor Issues Only

9. **Character limit violations in sheet data**
   - **Symptom**: Google Ads API rejects asset
   - **Detection**: Dry-run will catch this
   - **Fix**: Trim text assets to limits
   - **Prevention**: Validate sheet data Monday

10. **Extra spaces or formatting in sheet**
    - **Symptom**: Asset group name mismatch
    - **Detection**: Dry-run will catch this
    - **Fix**: Clean up sheet formatting
    - **Prevention**: Use TRIM() function in sheet

---

## Monday Dec 1st - Pre-Flight Tasks (DO THIS DAY BEFORE)

### 3:00 PM - Data Validation

- [ ] **Open master Google Sheet**
  - URL: https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g
  - Confirm URL hasn't changed
  - Confirm 4 tabs exist: UK ad copy, US ad copy, EUR ad copy, ROW ad copy

- [ ] **Validate sheet data quality** (spot-check 5 rows per region):
  - Column A (Campaign Name): No extra spaces, matches Google Ads exactly
  - Column B (Asset Group Name): No extra spaces, matches Google Ads exactly
  - Headlines (C-Q): Max 30 chars each
  - Long Headlines (R-V): Max 90 chars each
  - Descriptions (W-AA): Max 90 chars each
  - No empty required fields

- [ ] **Count rows per region**:
  - UK ad copy: Expected ~26 rows
  - US ad copy: Expected ~15 rows
  - EUR ad copy: Expected ~12 rows
  - ROW ad copy: Expected ~3 rows
  - **Record actual counts** for Tuesday verification

### 4:00 PM - Environment Check

- [ ] **Verify Python environment**:
  ```bash
  cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

  # Check venv exists
  ls -la /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3

  # Test venv works
  /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3 --version
  ```

- [ ] **Test Google Ads API access**:
  ```bash
  # Quick GAQL query to test auth
  # Use MCP tool or direct API call
  ```

- [ ] **Test Google Sheets API access**:
  ```bash
  # Try reading one cell from master sheet
  cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts
  python3 -c "
  from google.oauth2.credentials import Credentials
  from googleapiclient.discovery import build
  import os

  sheets_mcp_path = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server'
  token_path = os.path.join(sheets_mcp_path, 'token.json')

  creds = Credentials.from_authorized_user_file(token_path)
  service = build('sheets', 'v4', credentials=creds)

  result = service.spreadsheets().values().get(
      spreadsheetId='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g',
      range='UK ad copy!A1'
  ).execute()

  print('✅ Google Sheets API working:', result.get('values', []))
  "
  ```

### 5:00 PM - CRITICAL: Full Dry-Run Test

- [ ] **Run complete dry-run for all regions**:
  ```bash
  cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

  python3 apply-all-assets.py --region all --dry-run
  ```

- [ ] **Expected output**:
  ```
  Regions processed: 4
  Successful: 4 ['uk', 'us', 'eur', 'row']
  Failed: 0 []

  ✅ DRY RUN COMPLETE - All checks passed
  🚀 Ready for live execution on Tuesday
  ```

- [ ] **If dry-run FAILS**:
  - ❌ **DO NOT PROCEED** to Tuesday without fixing
  - Document the error
  - Identify root cause (see "High Risk" section above)
  - Fix the issue
  - Re-run dry-run until it passes
  - **Inform client of delay if fix takes > 2 hours**

- [ ] **If dry-run SUCCEEDS**:
  - ✅ Save dry-run output to file
  - ✅ Note any warnings (even if successful)
  - ✅ Proceed to Tuesday deployment

### 5:30 PM - Document Status

- [ ] **Create Monday status note**:
  - Dry-run result: PASS/FAIL
  - Any warnings or concerns
  - OAuth tokens expiry dates
  - Sheet data quality: GOOD/NEEDS FIXES
  - Ready for Tuesday: YES/NO/CONDITIONAL

- [ ] **If NOT ready**:
  - Email client immediately
  - Explain the issue
  - Propose new timeline
  - **DO NOT deploy on Tuesday if dry-run failed**

---

## Tuesday Dec 2nd - Deployment Day

### 9:00 AM - Final Checks

- [ ] **Verify nothing changed overnight**:
  - Open Google Sheet, confirm no surprise edits
  - Check Google Ads UI for any campaign pauses
  - Confirm no client emails requesting delays

- [ ] **Verify RSA countdown removal CSV exists**:
  ```bash
  ls -lh /Users/administrator/Documents/PetesBrain/clients/smythson/data/remove_bf_countdown_all_regions.csv
  ```

  Expected: CSV file dated Nov 26-28, containing 86 RSA updates

  **If missing or needs regeneration:**
  ```bash
  cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts
  python3 remove_bf_countdown.py
  ```

- [ ] **Create fresh backup** (CRITICAL - do this right before deployment):
  ```bash
  cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

  python3 export-current-assets.py --region all
  ```

- [ ] **Verify backups created**:
  ```bash
  ls -lh /Users/administrator/Documents/PetesBrain/clients/smythson/data/2025-12-02-*-assets.json
  ```

  Expected files:
  - `2025-12-02-uk-assets.json`
  - `2025-12-02-us-assets.json`
  - `2025-12-02-eur-assets.json`
  - `2025-12-02-row-assets.json`
  - `2025-12-02-all-assets.json`

- [ ] **Record backup file sizes** (for verification):
  - UK: ~XXX KB
  - US: ~XXX KB
  - EUR: ~XXX KB
  - ROW: ~XXX KB

### 9:30 AM - Single Asset Group Test (CRITICAL)

**DO NOT skip this step. This is your last safety check.**

- [ ] **Pick test asset group**: ROW region, "Diaries AW25 - All" (low traffic)

- [ ] **Run single-group test**:
  ```bash
  # Test text assets only first
  python3 apply-text-assets-from-sheet.py --region row --dry-run

  # If dry-run passes, run live on ROW only (smallest region)
  python3 apply-text-assets-from-sheet.py --region row
  ```

- [ ] **Immediately verify in Google Ads UI**:
  - Navigate to ROW account (5556710725)
  - Find "Diaries AW25 - All" asset group
  - Check Assets tab
  - Confirm new text assets are showing
  - Confirm old text assets are removed
  - Check for any errors/warnings

- [ ] **Verify in API**:
  ```bash
  # Quick GAQL query to confirm asset count
  SELECT asset_group.name, asset_group_asset.field_type, COUNT(*)
  FROM asset_group_asset
  WHERE asset_group.id = [ROW_ASSET_GROUP_ID]
  AND asset_group_asset.field_type IN ('HEADLINE', 'LONG_HEADLINE', 'DESCRIPTION')
  GROUP BY asset_group.name, asset_group_asset.field_type
  ```

- [ ] **If test FAILS**:
  - ❌ **STOP IMMEDIATELY**
  - Roll back test asset group: `python3 rollback-to-backup.py --region row`
  - Document the error
  - Inform client of delay
  - Debug the issue
  - **DO NOT proceed to bulk deployment**

- [ ] **If test SUCCEEDS**:
  - ✅ **Proceed to bulk deployment below**
  - Screenshot successful result for documentation

### 10:00 AM - Bulk Deployment (Only if test passed)

**PHASE 1: Remove RSA Countdowns (Do this FIRST)**

- [ ] **Open Google Ads Editor**
- [ ] **Load ALL Smythson accounts** (UK: 857-323-5780, USA: 780-869-0871, EUR: 767-961-6761, ROW: 555-671-0725)
- [ ] **Import countdown removal CSV**:
  - Account > Import > From file...
  - Select: `/Users/administrator/Documents/PetesBrain/clients/smythson/data/remove_bf_countdown_all_regions.csv`
  - Review: Should show 86 RSAs to be EDITED (not added)
  - Process > Review > Post

- [ ] **Verify RSA updates**:
  - UK: 27 RSAs updated ✅
  - USA: 41 RSAs updated ✅
  - EUR: 14 RSAs updated ✅
  - ROW: 4 RSAs updated ✅
  - Total: 86 RSAs ✅

- [ ] **Spot-check in Google Ads UI**:
  - Pick 2 RSAs from UK account
  - Confirm countdown headline removed
  - Confirm other headlines intact

**Duration:** ~5 minutes

**If import fails:** See "Troubleshooting" section in TUESDAY-EXECUTION-GUIDE.md

---

**PHASE 2: Deploy PMAX Assets (After RSA countdowns removed)**

**Deploy in order: ROW → EUR → US → UK (smallest to largest)**

#### Region 1: ROW (Rest of World)

- [ ] **Deploy ROW** (already partially done from test):
  ```bash
  python3 apply-all-assets.py --region row
  ```

- [ ] **Expected output**:
  ```
  ROW: ✅ SUCCESS
    Text assets: ✅
    Image assets: ✅
  ```

- [ ] **If ROW fails**: STOP, roll back ROW, investigate

#### Region 2: EUR (Europe)

- [ ] **Deploy EUR**:
  ```bash
  python3 apply-all-assets.py --region eur
  ```

- [ ] **Expected output**:
  ```
  EUR: ✅ SUCCESS
    Text assets: ✅
    Image assets: ✅
  ```

- [ ] **If EUR fails**: STOP, roll back EUR, investigate

#### Region 3: US (United States)

- [ ] **Deploy US**:
  ```bash
  python3 apply-all-assets.py --region us
  ```

- [ ] **Expected output**:
  ```
  US: ✅ SUCCESS
    Text assets: ✅
    Image assets: ✅
  ```

- [ ] **If US fails**: STOP, roll back US, investigate

#### Region 4: UK (United Kingdom)

- [ ] **Deploy UK** (largest - do last):
  ```bash
  python3 apply-all-assets.py --region uk
  ```

- [ ] **Expected output**:
  ```
  UK: ✅ SUCCESS
    Text assets: ✅
    Image assets: ✅
  ```

- [ ] **If UK fails**: STOP, roll back UK, investigate

### 10:20 AM - Post-Deployment Verification

- [ ] **Spot-check 2-3 asset groups per region in Google Ads UI**:
  - UK: Check 3 asset groups (1 Black Friday, 1 standard, 1 Christmas)
  - US: Check 2 asset groups
  - EUR: Check 1 asset group
  - ROW: Already checked during test

- [ ] **Verify asset counts via GAQL** (quick check):
  ```sql
  SELECT
    campaign.name,
    asset_group.name,
    asset_group_asset.field_type,
    COUNT(*) as asset_count
  FROM asset_group_asset
  WHERE campaign.status != 'REMOVED'
  AND asset_group.status != 'REMOVED'
  AND asset_group_asset.field_type IN ('HEADLINE', 'LONG_HEADLINE', 'DESCRIPTION', 'MARKETING_IMAGE')
  GROUP BY campaign.name, asset_group.name, asset_group_asset.field_type
  ORDER BY campaign.name, asset_group.name
  ```

- [ ] **Expected results**:
  - Headlines: 3-15 per group
  - Long Headlines: 1-5 per group
  - Descriptions: 2-5 per group
  - Marketing Images: varies per group

- [ ] **Check for campaign performance drops**:
  - Monitor impressions for next 2 hours
  - Expect small learning period dip (normal)
  - If impressions drop >50%: Investigate immediately

### 10:30 AM - Documentation & Communication

- [ ] **Log to tasks-completed.md**:
  ```markdown
  ### [Smythson] ✅ Completed: Deploy post-Black Friday asset refresh
  **Completed**: 2025-12-02 10:30

  Deployed Christmas/standard copy to 56 asset groups across 4 regional accounts:
  - UK: 26 asset groups ✅
  - US: 15 asset groups ✅
  - EUR: 12 asset groups ✅
  - ROW: 3 asset groups ✅

  Removed Black Friday messaging and replaced with evergreen luxury copy.
  Backups created and verified before deployment.
  All regions deployed successfully with no errors.

  Verification complete: Text and image assets updated in all regions.
  ```

- [ ] **Email client** (Lauryn/Alex):
  - Subject: "Smythson PMax Assets Updated - Black Friday → Christmas Copy"
  - Brief: All 4 regions updated successfully
  - Note: Small learning period expected (24-48 hours)
  - Attach: Screenshot of successful deployment output

- [ ] **Monitor for next 24 hours**:
  - Check campaign performance at 5 PM Tuesday
  - Check again Wednesday morning
  - Alert client if any issues

---

## Emergency Rollback Procedure

**If deployment goes wrong, follow these steps immediately:**

### Quick Rollback (Preferred Method)

```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

# Rollback single region
python3 rollback-to-backup.py --region uk --dry-run  # Test first
python3 rollback-to-backup.py --region uk            # Execute

# Rollback all regions
python3 rollback-to-backup.py --region all --dry-run
python3 rollback-to-backup.py --region all
```

### Rollback Source Files

Use today's backups (created in Step "9:00 AM - Final Checks"):
- `/clients/smythson/data/2025-12-02-uk-assets.json`
- `/clients/smythson/data/2025-12-02-us-assets.json`
- `/clients/smythson/data/2025-12-02-eur-assets.json`
- `/clients/smythson/data/2025-12-02-row-assets.json`

### Manual Rollback (If Script Fails)

1. Open backup JSON file for the region
2. Navigate to affected asset group in Google Ads UI
3. Go to Assets tab
4. Remove new assets
5. Re-add old assets from JSON file (copy text from `"text"` fields)

---

## Communication Templates

### If Deployment Delayed

```
Subject: Smythson Asset Deployment - Postponed to [New Date]

Hi [Client],

During our pre-flight checks yesterday, we identified [issue description].

To ensure a smooth deployment without risk to campaign performance,
I recommend postponing to [new date] to resolve this properly.

What we found: [technical details]
Risk if we proceed: [potential impact]
Fix required: [what needs to be done]
New timeline: [proposed schedule]

Please confirm if this works for you, or if you'd prefer to proceed
with the original date accepting the risk.

Best,
Pete
```

### If Deployment Successful

```
Subject: Smythson PMax Assets Updated - Black Friday → Christmas Copy

Hi [Client],

All Smythson Performance Max assets have been successfully updated across
all 4 regional accounts:

✅ UK: 26 asset groups
✅ US: 15 asset groups
✅ EUR: 12 asset groups
✅ ROW: 3 asset groups

Black Friday messaging has been removed and replaced with Christmas/evergreen
luxury copy as planned.

You may see a small learning period over the next 24-48 hours as Google's
algorithm adjusts to the new creative, which is completely normal.

I'll monitor performance closely and let you know if I see anything unexpected.

Best,
Pete
```

### If Rollback Required

```
Subject: Smythson Asset Deployment - Rolled Back [Reason]

Hi [Client],

During today's asset deployment, we encountered [issue description].

As a precaution, I've rolled back all changes to restore the previous
Black Friday copy while we investigate.

What happened: [technical details]
Action taken: Full rollback to previous assets
Current status: Campaigns running normally with Black Friday copy
Next steps: [investigation plan]
New timeline: [proposed schedule]

No campaign performance was impacted - the rollback was completed within
[X minutes] of detecting the issue.

I'll follow up with a revised deployment plan once we've identified
and resolved the root cause.

Best,
Pete
```

---

## Success Criteria

**Deployment is considered SUCCESSFUL if:**

1. ✅ All 56 asset groups updated without errors
2. ✅ Spot-checks confirm new copy is live
3. ✅ No warnings or policy violations in Google Ads UI
4. ✅ Campaign impressions continue (no >50% drop in first 2 hours)
5. ✅ Backups exist and are verified
6. ✅ Client notified of successful completion

**Deployment is considered FAILED if:**

1. ❌ Any region fails to update completely
2. ❌ Asset groups show errors or warnings
3. ❌ Campaign impressions drop >50% in first 2 hours
4. ❌ Cannot verify changes in Google Ads UI
5. ❌ Rollback script doesn't work when tested

---

## Key Contacts

- **Primary**: Peter Empson (petere@roksys.co.uk, 07932 454652)
- **Client**: Lauryn/Alex at Smythson
- **Google Ads Rep**: [Name if applicable]

---

## File Locations Quick Reference

**Master Google Sheet**:
`https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`

**Deployment Scripts**:
```
/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/
├── apply-all-assets.py           # Main orchestration
├── apply-text-assets-from-sheet.py
├── apply-image-assets-from-sheet.py
├── export-current-assets.py      # Backup creation
├── rollback-to-backup.py         # Emergency rollback
```

**Data & Backups**:
```
/Users/administrator/Documents/PetesBrain/clients/smythson/data/
├── 2025-11-24-*-assets.json     # Previous backup (fallback)
├── 2025-12-02-*-assets.json     # Fresh backup (use this)
```

**Documentation**:
```
/Users/administrator/Documents/PetesBrain/clients/smythson/documents/
├── pmax-asset-application-workflow.md    # Technical reference
├── 2025-12-02-asset-revert-plan.md       # Original plan
├── TUESDAY-DEC-2-PREFLIGHT-CHECKLIST.md  # This file
```

---

## Estimated Timeline

| Time | Task | Duration |
|------|------|----------|
| 9:00 AM | Final checks & fresh backup | 15 mins |
| 9:30 AM | Single asset group test | 10 mins |
| 10:00 AM | **Remove RSA countdowns (Editor CSV import)** | **5 mins** |
| 10:05 AM | ROW PMAX deployment | 2 mins |
| 10:07 AM | EUR PMAX deployment | 3 mins |
| 10:10 AM | US PMAX deployment | 3 mins |
| 10:13 AM | UK PMAX deployment | 5 mins |
| 10:18 AM | Verification | 7 mins |
| 10:25 AM | Documentation & email | 10 mins |
| **10:35 AM** | **COMPLETE** | **35 mins total** |

**Note**: Times assume no errors. Add 15-30 minutes if any issues require investigation.

---

**Last Updated**: 2025-11-27
**Status**: READY FOR MONDAY PRE-FLIGHT CHECKS
**Next Review**: Monday Dec 1st, 3:00 PM
