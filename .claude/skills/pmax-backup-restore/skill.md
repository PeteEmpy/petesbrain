# PMax Backup & Restore Skill

**Type:** Execution
**Priority:** P0
**Effort:** 2-3 hours (create universal scripts)
**Use:** Backup and restore Performance Max asset groups (text + images)

---

## What This Skill Does

Creates complete backups of Performance Max asset groups and provides emergency rollback capability. Backs up:
- Headlines, long headlines, descriptions (text assets)
- Marketing images with field types (landscape/square/portrait)
- Campaign and asset group metadata

---

## When to Use

User says:
- "Backup [client] assets"
- "Create backup before changes"
- "Rollback [client] to backup"
- "Emergency restore for [client]"
- "Revert [client] assets"

---

## Operations

### Backup Operation

**Creates snapshot of current state:**
1. Query all PMax campaigns and asset groups
2. Export text assets (headlines, long headlines, descriptions)
3. Export image assets (IDs, field types, dimensions)
4. Save to JSON backup file with timestamp

**Output:** `{client}/data/asset-backups/{date}-{account}-assets.json`

### Restore Operation

**Reverts to backup state:**
1. Read backup JSON file
2. For each asset group:
   - Remove current text assets
   - Create and link backup text assets
   - Remove current image links
   - Re-link backup images with correct field types
3. Report success/failure per asset group

---

## Inputs Required

**For Backup:**
- Client name
- Account/region (optional, defaults to all)

**For Restore:**
- Client name
- Backup date (optional, uses most recent)
- Account/region (optional, defaults to all)
- Dry-run flag (optional, preview changes)

---

## Safety Features

**Add-Before-Remove Strategy:**
- Never leaves asset groups empty
- Adds new assets first, then removes old ones
- Prevents "NOT_ENOUGH_X_ASSET" errors

**Dry-Run Mode:**
- Preview what would be restored
- Shows before/after counts
- No changes made until confirmed

**Backup Validation:**
- Verifies backup file exists
- Checks JSON structure is valid
- Reports missing campaigns/asset groups

---

## What Gets Created

**Backup Files:**
```
clients/{client}/data/asset-backups/
├── 2025-12-02-uk-assets.json
├── 2025-12-02-us-assets.json
├── 2025-12-02-eur-assets.json
└── 2025-12-02-row-assets.json
```

**Backup Structure:**
```json
{
  "region": "UK",
  "customer_id": "8573235780",
  "export_date": "2025-12-02T09:00:00",
  "campaigns": {
    "SMY | UK | P Max | Bags": {
      "campaign_id": "12345",
      "asset_groups": {
        "Bags - High Earners": {
          "asset_group_id": "67890",
          "headlines": [
            {"text": "Luxury Leather Bags", "asset_id": "111"}
          ],
          "long_headlines": [...],
          "descriptions": [...],
          "images": [
            {
              "asset_id": "11781430013",
              "field_type": "MARKETING_IMAGE",
              "name": "bag-lifestyle.jpg",
              "width": "2400",
              "height": "1256"
            }
          ]
        }
      }
    }
  }
}
```

---

## Technical Implementation

**Universal Scripts to Create:**

1. **`/shared/scripts/google-ads-pmax-backup.py`**
   - Universal backup script (any client, any account)
   - Parameters: `--customer-id`, `--manager-id`, `--output-file`
   - Queries all PMax campaigns and exports text + images

2. **`/shared/scripts/google-ads-pmax-restore.py`**
   - Universal restore script
   - Parameters: `--customer-id`, `--manager-id`, `--backup-file`, `--dry-run`
   - Restores text and image assets from backup JSON

**Extracted from Smythson:**
- `/clients/smythson/scripts/export-current-assets.py` → Universal backup
- `/clients/smythson/scripts/rollback-to-backup.py` → Universal restore

**Key Functions to Extract:**
- `get_asset_groups()` - Query PMax campaigns
- `get_text_assets_for_asset_group()` - Export text
- `get_image_assets_for_asset_group()` - Export images
- `rollback_asset_group()` - Restore single asset group
- `link_image_assets()` - Re-link images with field types

---

## Example Usage

### Backup Before Changes

**User:** "Backup Smythson assets before Black Friday changes"

**Skill Actions:**
1. Read Smythson CONTEXT.md for account IDs
2. For each account (UK, US, EUR, ROW):
   - Run `google-ads-pmax-backup.py --customer-id X --manager-id Y --output-file {date}-{region}-assets.json`
3. Report: "Backed up 56 asset groups across 4 regions to `clients/smythson/data/asset-backups/`"

### Emergency Rollback

**User:** "Rollback Smythson UK to backup"

**Skill Actions:**
1. Find most recent UK backup in `clients/smythson/data/asset-backups/`
2. Run dry-run: `google-ads-pmax-restore.py --customer-id 8573235780 --backup-file 2025-12-02-uk-assets.json --dry-run`
3. Show preview of changes
4. Ask for confirmation
5. Execute: `google-ads-pmax-restore.py --customer-id 8573235780 --backup-file 2025-12-02-uk-assets.json`
6. Report: "Restored 26 asset groups from backup (2025-12-02 09:00)"

---

## Error Handling

**Backup Errors:**
- API authentication failures → Guide user through OAuth refresh
- No PMax campaigns found → Inform user (nothing to backup)
- Permission issues → Check manager account access

**Restore Errors:**
- Backup file not found → List available backups
- Asset group not found → Skip with warning (may have been deleted)
- API errors → Report and continue with remaining asset groups

---

## Benefits

**Complete Disaster Recovery:**
- Full restoration of text AND images
- Exact field type preservation (landscape/square/portrait)
- Campaign state snapshot

**Confidence:**
- Safe to make bulk changes knowing you can revert
- Dry-run preview before restoration
- Automatic atomic operations

**Speed:**
- Automated vs manual UI work
- Batch operations across all asset groups
- Parallel region processing

**Audit Trail:**
- Timestamped backups
- JSON format for manual inspection
- Before/after comparison

---

## Related Tools

- **Asset Library Browser** - Find Asset IDs for manual updates
- **Text Asset Exporter** - Export text only (no images)
- **Spreadsheet Application** - Apply new assets from Google Sheets

---

## Implementation Checklist

- [ ] Create `/shared/scripts/google-ads-pmax-backup.py`
- [ ] Create `/shared/scripts/google-ads-pmax-restore.py`
- [ ] Extract functions from Smythson scripts
- [ ] Make scripts client-agnostic (parameter-driven)
- [ ] Add comprehensive error handling
- [ ] Test with Smythson accounts
- [ ] Test with Tree2MyDoor accounts
- [ ] Document in skill.md
- [ ] Add usage examples
- [ ] Update .claude/skills/README.md

---

## Testing Plan

1. **Backup Test:**
   - Run backup on test account
   - Verify JSON structure
   - Check text and images captured

2. **Restore Test (Dry-Run):**
   - Run dry-run on test account
   - Verify preview output accurate
   - Confirm no changes made

3. **Restore Test (Live):**
   - Make manual change to test asset group
   - Restore from backup
   - Verify exact restoration

4. **Multi-Account Test:**
   - Backup all 4 Smythson regions
   - Verify all backups created
   - Test selective restore (UK only)
