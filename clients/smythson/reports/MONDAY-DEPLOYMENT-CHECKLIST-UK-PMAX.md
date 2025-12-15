# Smythson UK PMax Text Asset Deployment - Monday Checklist

**Deployment Date**: Monday 16th December 2025
**Region**: UK
**Customer ID**: 8573235780
**Asset Groups**: 14

---

## Pre-Deployment Verification (Do Friday/Weekend)

- [x] JSON deployment file created and verified
- [x] All 14 asset groups validated
- [x] Google Ads OAuth confirmed working
- [x] Dry-run completed successfully
- [ ] **Confirm with Alex**: EUR/ROW still have promotional copy - intentional?

---

## Monday Morning - Pre-Deployment

### Step 1: Final Validation (2 minutes)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
./apply-pmax-from-json.py --json uk-pmax-deployment-2025-12-16.json --validate
```

**Expected output**: "VALIDATION PASSED: Ready for deployment"

If validation fails, check:
- Google Ads OAuth token (may need refresh)
- Network connectivity
- Asset groups haven't been modified

### Step 2: Final Dry-Run (2 minutes)

```bash
./apply-pmax-from-json.py --json uk-pmax-deployment-2025-12-16.json --dry-run
```

Review output to confirm all 14 asset groups will be updated.

---

## Deployment Execution

### Step 3: Execute Deployment (5-10 minutes)

```bash
./apply-pmax-from-json.py --json uk-pmax-deployment-2025-12-16.json
```

**Monitor output for**:
- Backups being saved for each asset group
- "SUCCESS" message for each asset group
- "[VERIFIED]" confirmation after each group

### Step 4: Verify in Google Ads UI

1. Open Google Ads → Customer ID 8573235780
2. Navigate to Performance Max campaigns
3. Check text assets for a few asset groups:
   - Remarketing Heroes & Sidekicks (6598633691)
   - Christmas Gifting (6628451962)
   - Notebooks (6624708659)

**Verify**:
- No "20% off" promotional headlines remain
- New evergreen headlines appear (e.g., "British Luxury Since 1887")

---

## Rollback Procedure (If Needed)

### Backups Location

```
/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/backups/
```

Each backup file contains:
- Complete current state before changes
- Asset IDs and resource names for manual restoration

### To Restore a Single Asset Group

Use the MCP tool or API to:
1. Query the backup file for the asset group
2. Remove current assets
3. Re-create assets from backup data

---

## Post-Deployment

### Verification Queries

```sql
-- Check headlines for an asset group
SELECT
  asset_group.name,
  asset.text_asset.text
FROM asset_group_asset
WHERE asset_group.id = 6598633691
AND asset_group_asset.field_type = 'HEADLINE'
AND asset_group_asset.status != 'REMOVED'
```

### Confirm No Promotional Copy Remains

Search for these terms in any UK PMax asset groups:
- "20% off"
- "Ends Sunday"
- Promotional pricing language

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `data/uk-pmax-deployment-2025-12-16.json` | Deployment data (DO NOT MODIFY) |
| `scripts/apply-pmax-from-json.py` | Deployment script |
| `data/backups/` | Pre-deployment backups |
| `reports/UK-PMAX-TEXT-ASSET-CHANGE-REPORT-2025-12-12.md` | Full change comparison |
| `reports/MULTI-REGION-TEXT-ASSET-CHANGE-REPORT-2025-12-12.md` | All regions analysis |

---

## Emergency Contacts

If deployment fails or issues occur:
1. Check backup files in `data/backups/`
2. Review error logs
3. Do NOT retry without understanding the error
4. Google Sheet version history available as additional fallback

---

## Changes Being Made (Summary)

**Removing** (promotional copy):
- "Enjoy 20% off | Ends Sunday"
- "20% off luxury christmas gifts"
- "20% off bags | Ends Sunday"
- "20% off Notebooks. Ends Sunday"

**Adding** (evergreen copy):
- "British Luxury Since 1887"
- "Quintessential British Luxury"
- "Shop Luxury Christmas Gifts"
- "A Luxurious Christmas"
- "Discover the Art of Gifting"

---

**Prepared**: 2025-12-12
**Prepared by**: PetesBrain
