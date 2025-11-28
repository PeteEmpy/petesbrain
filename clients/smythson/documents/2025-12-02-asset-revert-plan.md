# Smythson Asset Text Revert - December 2nd, 2025

**Date Created:** 2025-11-24
**Scheduled Execution:** 2025-12-02
**Status:** PREPARED - Scripts ready, awaiting execution date

---

## Overview

Remove Black Friday messaging from PMax text assets and replace with Christmas/standard copy across all 4 Smythson Google Ads accounts.

---

## Data Sources

**Google Sheet (replacement copy):**
`https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`

**Local CSV backups:**
- `data/replacement-copy/uk-replacement-copy.csv` (34 rows)
- `data/replacement-copy/us-replacement-copy.csv` (15 rows)
- `data/replacement-copy/eur-replacement-copy.csv` (12 rows)
- `data/replacement-copy/row-replacement-copy.csv` (3 rows)

**Current asset backup (2025-11-24):**
- `data/asset-backups/2025-11-24-uk-assets.json`
- `data/asset-backups/2025-11-24-us-assets.json`
- `data/asset-backups/2025-11-24-eur-assets.json`
- `data/asset-backups/2025-11-24-row-assets.json`
- `data/asset-backups/2025-11-24-all-assets.json` (combined)

---

## Accounts & Scope

| Region | Customer ID | Manager ID | Asset Groups | Black Friday Groups |
|--------|-------------|------------|--------------|---------------------|
| UK | 8573235780 | 2569949686 | 15 | 9 (Black Friday*) |
| US | 7808690871 | 2569949686 | 17 | 11 (Black Friday*) |
| EUR | 7679616761 | 2569949686 | 16 | 0 (Christmas Gifting) |
| ROW | 5556710725 | 2569949686 | 4 | 0 (Christmas Gifting) |

**Total: 52 asset groups across 4 accounts**

---

## Current Black Friday Asset Groups (UK)

From the 2025-11-24 export:
- Black Friday Card Holders
- Black Friday Competitors H&S
- Black Friday Heroes & Sidekicks
- Black Friday Jewellery Boxes and Rolls
- Black Friday Leopard Collection
- Black Friday Notebooks
- Black Friday Remarketing Heroes & Sidekicks
- Black Friday Travel Bags

---

## Text Assets to Update Per Group

| Asset Type | Count | Max Chars |
|------------|-------|-----------|
| Headlines | Up to 15 | 30 |
| Long Headlines | Up to 5 | 90 |
| Descriptions | Up to 5 | 90 |

---

## Scripts Created

1. **`scripts/export-current-assets.py`** - Creates backup of current assets (DONE)
2. **`scripts/download-sheet-data.py`** - Downloads Google Sheet to local CSV (DONE)
3. **`scripts/smythson-asset-revert-dec2.py`** - Main implementation script (TO CREATE)

---

## Execution Plan (Dec 2nd)

### Pre-Flight Checks
1. Verify Google Sheet has latest copy
2. Re-run `export-current-assets.py` for fresh backup (creates new dated backup)
3. Confirm no active campaigns need Black Friday messaging

### Step 1: Test on ONE Asset Group First

**CRITICAL: Do not proceed to bulk update until this test passes.**

1. Pick a low-traffic asset group from ROW account (smallest account)
   - Suggested: "Diaries AW25 - All" (ID: 6631187342) - non-Black Friday group

2. Run the update script for ONLY this asset group:
   ```bash
   # Script will have --asset-group-id parameter for single group testing
   ```

3. **Verify in Google Ads UI:**
   - [ ] Asset group still exists with same ID
   - [ ] Performance history is intact (check Insights tab)
   - [ ] Text assets show the new Christmas copy
   - [ ] No errors or warnings on the asset group

4. **If test FAILS:** Stop immediately. Use rollback script or manual revert.

5. **If test PASSES:** Proceed to bulk execution below.

### Step 2: Bulk Execution (only after test passes)

1. Run implementation script for ROW account (remaining groups)
2. Verify changes via GAQL query
3. Run for EUR account
4. Run for US account
5. Run for UK account (largest - do last)
6. Update "Christmas phase 2" checklist in Google Sheet

### Post-Execution
1. Spot-check 2-3 asset groups in UI across different accounts
2. Log to `tasks-completed.md`
3. Send confirmation to Lauryn/Alex

---

## Rollback Procedure

If issues arise, restore from the 2025-11-24 backups using the rollback script:

### Quick Rollback Command
```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson

# Use the Google Ads MCP server venv
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3 scripts/rollback-to-backup.py --region uk

# Or run for all regions
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3 scripts/rollback-to-backup.py --region all

# Dry run first to verify
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3 scripts/rollback-to-backup.py --region uk --dry-run
```

### Backup Files Location
```
data/asset-backups/2025-11-24-uk-assets.json   (15 asset groups)
data/asset-backups/2025-11-24-us-assets.json   (17 asset groups)
data/asset-backups/2025-11-24-eur-assets.json  (16 asset groups)
data/asset-backups/2025-11-24-row-assets.json  (4 asset groups)
```

### What Gets Restored
- All Headlines (up to 15 per group)
- All Long Headlines (up to 5 per group)
- All Descriptions (up to 5 per group)

### Manual Rollback (if script fails)
1. Open backup JSON file for the region
2. Use Google Ads UI to manually update text assets
3. Match by Asset Group name → Asset ID

---

## Notes

- EUR and ROW accounts already have "Christmas Gifting" asset groups (not Black Friday)
- UK and US have explicit "Black Friday" named asset groups
- Sheet copy matches asset group names - mapping by Campaign + Asset Group name
- Some sheet rows reference campaigns that may not exist (old campaigns)

---

## Document History

- **2025-11-24:** Plan created, scripts prepared, backups taken
- **2025-12-02:** [Scheduled] Execute asset revert

---

**Questions?** Contact Peter Empson (petere@roksys.co.uk)
