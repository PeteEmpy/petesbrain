# sync_to_sheets.py - Product Impact Analyzer Spreadsheet Sync

**Created**: 27 November 2025
**Purpose**: Universal spreadsheet writer - makes hidden product intelligence data visible
**Status**: Production-ready
**Schedule**: Daily at 8:00 AM via LaunchAgent

---

## OVERVIEW

`sync_to_sheets.py` is the **visualization layer** for the Product Impact Analyzer. It syncs all collected data from JSON files to client Google Sheets, transforming hidden intelligence into actionable dashboards.

### What It Does

Takes data from:
- `data/product_changes/[client]/*.json` → Product changes (price, stock, title)
- `data/product_baselines/[client].json` → 30-day performance baselines
- `history/label-transitions/[client]/current-labels.json` → Product Hero labels
- Merchant Centre API → Current disapprovals
- Future: `data/product_anomalies/[client]/*.json` → Performance anomalies

Writes to Google Sheets:
- **Product Changes** tab → All product modifications with color coding
- **Disapprovals** tab → Merchant Centre issues (highlighted)
- **Product Hero Labels** tab → Hero/Sidekick/Villain/Zombie classification
- **Product Baselines** tab → 30-day performance averages
- **Performance Anomalies** tab → Products deviating from baseline (placeholder)

---

## ARCHITECTURE

### Data Flow

```
Daily Workflow (8:00 AM):
┌─────────────────────────────────────────────────────────────┐
│  7:45 AM - product-tracking LaunchAgent                     │
│    1. product_feed_tracker.py → Fetch from Merchant Centre  │
│    2. product_change_detector.py → Detect changes           │
│    3. Data saved to JSON files                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  8:00 AM - product-sheets-sync LaunchAgent (THIS SCRIPT)    │
│    1. Read latest JSON files                                │
│    2. Query Merchant Centre API for disapprovals            │
│    3. Open each client's spreadsheet                        │
│    4. Create missing tabs                                   │
│    5. Write/update data                                     │
│    6. Apply conditional formatting                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Result: Complete Product Intelligence Dashboard            │
│    ✅ Daily Performance (existing - from other agent)       │
│    ✅ Product Changes (NEW)                                 │
│    ✅ Disapprovals (NEW)                                    │
│    ✅ Product Hero Labels (NEW - if enabled)                │
│    ✅ Product Baselines (NEW)                               │
│    ✅ Performance Anomalies (placeholder - future)          │
└─────────────────────────────────────────────────────────────┘
```

---

## FEATURES

### 1. Universal Client Support

- Works for all 16 clients automatically
- Reads client list from `config.json`
- Only processes enabled clients
- Uses `product_performance_spreadsheet_id` from each client's config

### 2. Intelligent Tab Management

- **Gets or creates** tabs as needed
- Doesn't duplicate tabs
- Updates existing tabs in place
- Tracks metadata in hidden "Sync Info" tab

### 3. Data Retention

- **Product Changes**: Keeps last 90 days
- **Disapprovals**: Tracks "Date First Seen" and "Date Resolved"
- **Product Baselines**: Overwrites with current (updated weekly)
- **Product Hero Labels**: Overwrites with current snapshot

### 4. Smart Disapproval Tracking

- Queries Merchant Centre API directly (always current)
- Merges with existing data to preserve "Date First Seen"
- Marks resolved disapprovals with "Date Resolved"
- Shows "Last Checked" timestamp even when no disapprovals

### 5. Dry Run Mode

- `--dry-run` flag shows what would be synced
- No writes to spreadsheets
- Perfect for testing before rollout

### 6. Per-Client Execution

- `--client "Tree2mydoor"` syncs one client
- Useful for testing or re-syncing specific client

### 7. Error Handling

- Continues processing other clients if one fails
- Logs all errors
- Returns exit code 1 if any errors occurred
- Detailed error messages for debugging

---

## USAGE

### Daily Automated Run (via LaunchAgent)

```bash
# Runs automatically daily at 8:00 AM
# No manual intervention needed
```

**LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist`
**Log file**: `~/.petesbrain-product-sheets-sync.log`

### Manual Runs

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Sync all clients
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \
  .venv/bin/python3 sync_to_sheets.py

# Sync specific client
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \
  .venv/bin/python3 sync_to_sheets.py --client "Tree2mydoor"

# Dry run (test without writing)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \
  .venv/bin/python3 sync_to_sheets.py --dry-run

# Dry run for specific client
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \
  .venv/bin/python3 sync_to_sheets.py --client "Just Bin Bags" --dry-run
```

---

## CONFIGURATION

### Required Environment Variable

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json"
```

This is automatically set in the LaunchAgent plist file.

### Client Configuration

Each client in `config.json` must have:

```json
{
  "name": "Tree2mydoor",
  "merchant_id": "123456789",
  "product_performance_spreadsheet_id": "1ABC...XYZ",
  "enabled": true,
  "label_tracking": {
    "enabled": true,
    "label_field": "custom_label_3"
  }
}
```

**Required fields**:
- `product_performance_spreadsheet_id` - Google Sheets ID where data will be written
- `merchant_id` - For fetching disapprovals from Merchant Centre

**Optional fields**:
- `label_tracking.enabled` - If true, syncs Product Hero labels

---

## SPREADSHEET STRUCTURE

### Tab: Product Changes

**Headers**:
| Date Detected | Product ID | Product Title | Change Type | Field Changed | Old Value | New Value | Status |
|---------------|-----------|---------------|-------------|---------------|-----------|-----------|--------|

**Example Row**:
```
2025-11-25 | 448 | Nitrile Gloves Small | Stock | availability | in stock | out of stock | Active
```

**Data Source**: `data/product_changes/[client]/[date].json`
**Retention**: Last 90 days
**Update Frequency**: Daily

---

### Tab: Disapprovals

**Headers**:
| Date First Seen | Product ID | Product Title | Issue Code | Issue Description | Status | Date Resolved |
|----------------|-----------|---------------|-----------|-------------------|--------|---------------|

**Example Row**:
```
2025-11-18 | 287 | Olive Tree | destination_not_available | Landing page not working | Resolved | 2025-11-27
```

**Data Source**: Merchant Centre API (real-time)
**Special Handling**: Preserves "Date First Seen", tracks resolution
**Update Frequency**: Daily

---

### Tab: Product Hero Labels (only for enabled clients)

**Headers**:
| Product ID | Product Title | Current Label | Last Updated |
|-----------|---------------|---------------|--------------|

**Example Row**:
```
rrbg | Rose Bush Red | heroes | 2025-11-25T07:00:11
```

**Data Source**: `history/label-transitions/[client]/current-labels.json`
**Retention**: Overwritten with current snapshot
**Update Frequency**: Daily

---

### Tab: Product Baselines

**Headers**:
| Product ID | Product Title | 30d Avg Revenue | 30d Avg Clicks | 30d Avg Conversions | 30d Avg ROAS | Last Updated |
|-----------|---------------|-----------------|----------------|---------------------|--------------|--------------|

**Example Row**:
```
287 | Olive Tree Large | £95.50 | 45 | 3.2 | 620% | 2025-11-25
```

**Data Source**: `data/product_baselines/[client].json`
**Retention**: Overwritten with current baselines
**Update Frequency**: Daily (baselines recalculated weekly)

---

### Tab: Performance Anomalies (placeholder - future feature)

**Status**: Tab created with headers, but data not yet populated

**Reason**: `product_anomaly_detector.py` currently sends email alerts only, doesn't save anomalies to JSON files.

**Future Enhancement**: Update `product_anomaly_detector.py` to save daily anomalies to `data/product_anomalies/[client]/[date].json`, then this sync will populate the tab.

---

### Tab: Sync Info (hidden metadata)

**Contains**:
- Last Synced timestamp
- Sync script version
- Data sources

**Purpose**: Troubleshooting and audit trail

---

## LAUNCHAGENT CONFIGURATION

### File Location
```
~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist
```

### Schedule
**Daily at 8:00 AM**

**Why 8:00 AM?**
- product-tracking runs at 7:45 AM
- Gives 15 minutes for product tracking to complete
- Syncs fresh data before business hours (9 AM)

### Log File
```
~/.petesbrain-product-sheets-sync.log
```

**Check logs**:
```bash
tail -f ~/.petesbrain-product-sheets-sync.log
```

### LaunchAgent Commands

```bash
# Load agent
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist

# Unload agent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist

# Check status
launchctl list | grep product-sheets-sync

# View recent logs
tail -50 ~/.petesbrain-product-sheets-sync.log

# Test manually (trigger immediate run)
launchctl start com.petesbrain.product-sheets-sync
```

---

## DEPENDENCIES

### Python Packages

Required in `.venv`:
- `gspread` - Google Sheets API client
- `google-auth` - Authentication
- `google-api-python-client` - Google APIs

All already installed in the existing venv.

### Service Account Credentials

**File**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json`

**Required Scopes**:
- `https://www.googleapis.com/auth/spreadsheets` - Read/write sheets
- `https://www.googleapis.com/auth/content` - Read Merchant Centre products

---

## ERROR HANDLING

### Common Errors

**1. Spreadsheet ID not found**
```
ERROR: Spreadsheet not found for [Client Name]
```
**Fix**: Add `product_performance_spreadsheet_id` to client config

**2. Permission denied**
```
ERROR: Service account doesn't have access to spreadsheet
```
**Fix**: Share spreadsheet with service account email (from credentials.json)

**3. API quota exceeded**
```
ERROR: Quota exceeded for Merchant Centre API
```
**Fix**: Rare - retry later, or increase quota in Google Cloud Console

**4. Client data missing**
```
WARNING: No changes directory for [Client Name]
```
**Fix**: Normal if client hasn't run product-tracking yet, will populate next run

### Exit Codes

- `0` - Success (all clients synced)
- `1` - Errors occurred (check logs)

---

## TESTING

### Test Plan (Before First Production Run)

#### 1. Dry Run All Clients (5 mins)
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 sync_to_sheets.py --dry-run
```

**Expected output**:
```
[2025-11-27 12:00:00] 🔍 [DRY RUN] INFO: Syncing 16 enabled clients...
[2025-11-27 12:00:01] 🔍 [DRY RUN] INFO: Syncing Tree2mydoor
[2025-11-27 12:00:01] 🔍 [DRY RUN] INFO: Would write 12 rows to 'Product Changes' tab
...
```

#### 2. Test Single Client (Tree2mydoor) (10 mins)
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 sync_to_sheets.py --client "Tree2mydoor"
```

**Verify**:
- Open Tree2mydoor spreadsheet
- Check new tabs exist: Product Changes, Disapprovals, Product Hero Labels, Product Baselines
- Verify data looks correct
- Check "Sync Info" tab shows last sync timestamp

#### 3. Test Just Bin Bags (No Labels) (5 mins)
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 sync_to_sheets.py --client "Just Bin Bags"
```

**Verify**:
- New tabs: Product Changes, Disapprovals, Product Baselines (NO Product Hero Labels)
- Disapprovals tab shows "No disapprovals - all products approved"
- Product Changes shows 4 availability changes from 25 Nov

#### 4. Full Production Run (30 mins)
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 sync_to_sheets.py
```

**Monitor**:
- Watch log output for errors
- Check summary at end shows all clients processed
- Verify exit code is 0

#### 5. Load LaunchAgent (1 min)
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist
```

**Verify**:
```bash
launchctl list | grep product-sheets-sync
# Should show agent loaded with PID or 0
```

#### 6. Wait for Next Scheduled Run (8:00 AM next day)

**Check**:
```bash
tail -100 ~/.petesbrain-product-sheets-sync.log
```

Should show successful sync at 8:00 AM.

---

## MAINTENANCE

### Weekly Checks

1. **Check logs for errors**:
   ```bash
   grep ERROR ~/.petesbrain-product-sheets-sync.log
   ```

2. **Verify last sync timestamp**:
   - Open any client spreadsheet
   - Check "Sync Info" tab
   - Verify "Last Synced" is today

3. **Spot check data**:
   - Open 2-3 random client spreadsheets
   - Verify tabs exist and have recent data
   - Check disapprovals are current

### Monthly Maintenance

1. **Review retention periods** - Adjust `days_to_keep` if needed
2. **Check API quotas** - Ensure not approaching limits
3. **Update documentation** - If features added/changed

---

## FUTURE ENHANCEMENTS

### Priority 1: Performance Anomalies Data

**Current state**: Tab created but empty (placeholder)

**Required**:
1. Update `product_anomaly_detector.py` to save anomalies to JSON:
   - `data/product_anomalies/[client]/[date].json`
2. Update `sync_to_sheets.py` to read and sync anomaly data

**Benefit**: Historical record of all performance anomalies, not just email alerts

---

### Priority 2: Conditional Formatting

**Current state**: Data written, but no color coding

**Add**:
- 🔴 Red: Active disapprovals, out of stock products
- 🟢 Green: Resolved disapprovals, back in stock
- 🟠 Orange: Price increases >10%
- 🟡 Yellow: Products with >3 changes in 7 days
- 🏆 Gold: Hero products
- 💀 Black: Villain products

**Implementation**: Use gspread's `format()` method after writing data

---

### Priority 3: Weekly Summary Tab

**Current state**: Weekly reports generated as text files only

**Add**:
- "Weekly Summary" tab to each spreadsheet
- Append weekly summaries (keep last 12 weeks)
- Aggregated insights, recommendations

**Implementation**: Update `weekly_impact_report.py` to save JSON output, sync reads it

---

### Priority 4: Backfill Historical Data

**Current state**: Only syncs latest data

**Add**:
- `--backfill --days 30` mode
- Reads last N days of JSON files
- Populates historical data in tabs

**Use case**: First-time setup, or recovering from extended downtime

---

## TROUBLESHOOTING

### Agent Not Running

**Symptom**: Data not updating in spreadsheets

**Check**:
```bash
launchctl list | grep product-sheets-sync
```

**Fix**:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-sheets-sync.plist
```

---

### Data Missing for Specific Client

**Symptom**: One client's spreadsheet not updating

**Check**:
1. Is client enabled in config.json?
2. Does client have `product_performance_spreadsheet_id`?
3. Does service account have access to that spreadsheet?
4. Check logs for specific error

**Manual test**:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json \
  .venv/bin/python3 sync_to_sheets.py --client "[Client Name]"
```

---

### Permission Errors

**Symptom**: `Permission denied` errors in logs

**Fix**:
1. Open the spreadsheet in browser
2. Click "Share"
3. Add service account email (from credentials.json)
4. Give "Editor" access

---

## MONITORING

### Success Indicators

✅ **Daily check**: Last sync timestamp in "Sync Info" tab is today
✅ **Weekly check**: All client spreadsheets have recent data
✅ **Monthly check**: No errors in log file

### Alert Triggers

🚨 **Immediate**: Sync fails for 2+ consecutive days
⚠️ **Warning**: Sync fails for 1 day (check logs)
ℹ️ **Info**: Individual client fails (may be expected)

---

## SUPPORT

### Log Analysis

```bash
# View recent activity
tail -100 ~/.petesbrain-product-sheets-sync.log

# Search for errors
grep ERROR ~/.petesbrain-product-sheets-sync.log

# Check specific client
grep "Syncing Tree2mydoor" ~/.petesbrain-product-sheets-sync.log
```

### Common Questions

**Q: Why are some tabs empty?**
A: Normal if data hasn't been collected yet. Product Changes requires product-tracking to have run at least once.

**Q: Why don't I see Product Hero Labels tab for all clients?**
A: Only created for clients with `label_tracking.enabled: true` in config.

**Q: Can I run sync more frequently than daily?**
A: Yes, change `StartCalendarInterval` in plist, but daily is recommended (data only updates daily).

---

## VERSION HISTORY

### v1.0.0 - 27 November 2025 (Initial Release)

**Features**:
- Universal client support (all 16 clients)
- Product Changes sync
- Disapprovals sync (real-time from API)
- Product Hero Labels sync (for enabled clients)
- Product Baselines sync
- Performance Anomalies tab (placeholder)
- Dry run mode
- Per-client execution
- LaunchAgent automation

**Known Limitations**:
- Performance Anomalies tab is placeholder (data not yet saved by anomaly detector)
- No conditional formatting (coming in v1.1)
- No backfill mode (coming in v1.2)

---

**Status**: ✅ PRODUCTION READY
**Next Review**: 4 December 2025 (1 week after deployment)
**Maintainer**: Pete's Brain Product Impact Analyzer System
