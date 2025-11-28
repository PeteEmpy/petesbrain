# Spreadsheet Creation Protocol - Product Impact Analyzer

**Date**: 27 November 2025
**Status**: CRITICAL PROTOCOL - Follow exactly to avoid service account issues

---

## THE ISSUE (27 Nov 2025)

**Incident**: Attempted to programmatically create spreadsheet for Positive Bakes using service account
**Error**: `APIError: [403]: The user's Drive storage quota has been exceeded`
**Root Cause**: Service account attempted to create spreadsheet, triggering storage quota error

---

## THE SOLUTION: Manual Creation Protocol

**NEVER** attempt to create spreadsheets programmatically using the service account.

**ALWAYS** follow this manual process:

### Step 1: Create Spreadsheet (Manual - User Account)

1. **Log in** to Google Sheets with your user account (petere@roksys.co.uk)
2. **Option A - Create from scratch**:
   - Click "Blank spreadsheet"
   - Name it: `{Client Name} - Product Performance`
3. **Option B - Copy existing** (RECOMMENDED):
   - Open an existing client spreadsheet (e.g., Tree2mydoor)
   - File → Make a copy
   - Rename to: `{Client Name} - Product Performance`

### Step 2: Share with Service Account

**CRITICAL**: The service account needs Editor access

1. Click **Share** button
2. Add email: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
3. Set permission: **Editor**
4. Click **Send**

### Step 3: Get Spreadsheet ID

From the URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

Example:
- URL: `https://docs.google.com/spreadsheets/d/1nicOtNeETTbrnl78nrz8AjONNEzKqff8u9mRghPDkLE/edit`
- **Spreadsheet ID**: `1nicOtNeETTbrnl78nrz8AjONNEzKqff8u9mRghPDkLE`

### Step 4: Add to Config

Edit `config.json` and add the `product_performance_spreadsheet_id` field:

```json
{
  "name": "Client Name",
  "merchant_id": "123456789",
  "google_ads_customer_id": "9876543210",
  "enabled": true,
  "product_performance_spreadsheet_id": "PASTE_ID_HERE",
  "monitoring_thresholds": { ... }
}
```

### Step 5: Clear Data (if copied)

If you copied an existing spreadsheet, clear the old data:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 -c "
import gspread
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file(
    '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
gc = gspread.authorize(creds)

sh = gc.open_by_key('PASTE_SPREADSHEET_ID_HERE')

for ws in sh.worksheets():
    if ws.title != 'Sheet1':
        ws.clear()
        print(f'Cleared: {ws.title}')
"
```

### Step 6: Sync Data

```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \
.venv/bin/python3 sync_to_sheets.py --client "Client Name"
```

---

## WHY THIS HAPPENS

### Service Account Limitations

**Service accounts** are special Google accounts used by applications, not humans. They have different restrictions:

1. **Limited Drive Storage**: Service accounts may have storage quotas
2. **No Google Workspace**: Service accounts aren't part of your Google Workspace
3. **API-only access**: Designed for reading/writing existing resources, not creating new ones

### Correct Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ User Account (petere@roksys.co.uk)                          │
│                                                               │
│ - Creates spreadsheets                                       │
│ - Owns spreadsheets                                          │
│ - Shares with service account                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Shares with Editor access
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Service Account (mcp-sheets-reader@...)                     │
│                                                               │
│ - Reads existing spreadsheets                                │
│ - Writes data to spreadsheets                               │
│ - NEVER creates new spreadsheets                            │
└─────────────────────────────────────────────────────────────┘
```

---

## CHECKLIST FOR NEW CLIENT SETUP

When adding a new e-commerce client to Product Impact Analyzer:

- [ ] Client has Merchant Centre account
- [ ] Client has Google Ads account with Shopping/PMAX campaigns
- [ ] **User creates** spreadsheet manually
- [ ] Spreadsheet named: `{Client Name} - Product Performance`
- [ ] Spreadsheet shared with: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com` (Editor)
- [ ] Spreadsheet ID copied from URL
- [ ] Spreadsheet ID added to `config.json` under client
- [ ] Old data cleared (if copied from template)
- [ ] Test sync: `sync_to_sheets.py --client "Client Name"`
- [ ] Verify tabs created: Product Changes, Disapprovals, Baselines, Labels, Anomalies
- [ ] Verify daily sync working at 8:00 AM

---

## REAL-WORLD EXAMPLE: Positive Bakes (27 Nov 2025)

### Situation
- Client: Positive Bakes
- Merchant ID: 395496688
- Running P-Max and Shopping campaigns
- No spreadsheet configured

### What Happened
1. Attempted to create spreadsheet programmatically
2. Got error: "Drive storage quota exceeded"
3. Realized service account shouldn't create spreadsheets

### Resolution
1. **User (petere@roksys.co.uk)** copied Tree2mydoor spreadsheet
2. Renamed to: "Positive Bakes - Product Performance"
3. Confirmed it was already shared with service account (inherited from copy)
4. Extracted spreadsheet ID: `1nicOtNeETTbrnl78nrz8AjONNEzKqff8u9mRghPDkLE`
5. Cleared old Tree2mydoor data from copied tabs
6. Added ID to config.json line 158
7. Ran sync: `sync_to_sheets.py --client "Positive Bakes"`
8. Success: ✅ 17 rows of product changes, 0 disapprovals, tabs created

### Time to Resolution
- Problem identified: 11:52
- Spreadsheet created: 11:55
- Data synced: 11:59
- **Total: 7 minutes**

---

## TROUBLESHOOTING

### "APIError: [403]: Drive storage quota exceeded"

**Cause**: Attempting to create spreadsheet with service account

**Fix**: Follow manual creation protocol above (user creates, not service account)

### "No spreadsheet ID for {Client}"

**Cause**: `product_performance_spreadsheet_id` missing from config.json

**Fix**:
1. Create spreadsheet manually
2. Add ID to config.json
3. Re-run sync

### "Unable to open spreadsheet"

**Cause**: Service account doesn't have access

**Fix**:
1. Open spreadsheet in browser
2. Click Share
3. Add: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
4. Permission: Editor
5. Re-run sync

### "Spreadsheet has old client data"

**Cause**: Copied existing spreadsheet without clearing

**Fix**: Run clear script (Step 5 above)

---

## AUTOMATION STATUS

### What's Automated ✅
- Daily data sync at 8:00 AM (product-sheets-sync LaunchAgent)
- Product changes detection
- Disapproval monitoring
- Label tracking
- Baseline calculations
- Writing data to tabs

### What's Manual ❌
- **Creating new client spreadsheets** (MUST be manual - see protocol above)
- Initial spreadsheet sharing
- Adding spreadsheet IDs to config

---

## RELATED DOCUMENTATION

- **sync_to_sheets.py**: Main sync script
- **SYNC-TO-SHEETS-DOCUMENTATION.md**: Operational guide
- **IMPLEMENTATION-COMPLETE-ACTUALLY-2025-11-27.md**: System overview
- **config.json**: Client configuration including spreadsheet IDs

---

## SERVICE ACCOUNT DETAILS

**Email**: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
**Project**: petesbrain-emailsync
**Credentials**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json`

**Permissions Required**:
- Google Sheets API: Read/Write
- Google Drive API: Read metadata (for opening by ID)
- Merchant Centre Content API: Read products

**What it CAN do**:
- ✅ Open spreadsheets by ID
- ✅ Read spreadsheet data
- ✅ Write data to spreadsheets
- ✅ Create/delete tabs
- ✅ Format cells

**What it CANNOT do**:
- ❌ Create new spreadsheets
- ❌ List user's spreadsheets
- ❌ Access Drive storage beyond shared files

---

## CONCLUSION

**The service account is for automation, not resource creation.**

Think of it like this:
- **User**: Architect (designs and creates the building)
- **Service Account**: Maintenance worker (maintains and updates the building)

Follow the manual creation protocol above for all new client spreadsheets. This is not a limitation, it's the correct architecture.

---

**Last Updated**: 27 November 2025
**Next Review**: When adding next new client
**Status**: ✅ Protocol established and documented
