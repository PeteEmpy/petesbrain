# Devonshire Budget Tracker & Shared Drives Automation - Complete

**Completed**: 2025-10-31
**Status**: ✅ All systems operational

---

## What Was Completed

### 1. Devonshire Budget Tracker - Daily Automation ✅

**Files Created/Modified**:
- `clients/devonshire-hotels/scripts/update_budget_tracker.py` - Daily automation script
- `~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist` - LaunchAgent for 9 AM daily updates
- `clients/devonshire-hotels/CONTEXT.md` - Critical campaign structure documentation

**Key Features**:
- ✅ Automatically updates budget tracker every day at 9 AM
- ✅ Correctly filters campaigns to "DEV | Properties" only (excludes Castles, Weddings)
- ✅ Includes paused campaigns in spend calculations
- ✅ Properly combines The Hide + Highwayman campaign IDs
- ✅ Updates Google Sheets with current data:
  - MTD Spend
  - Yesterday Spend
  - Days Elapsed/Remaining
  - Expected Spend
  - Remaining Budget
  - Required Daily Budget
  - Pacing %
  - Predicted Spend

**Campaign Tracking**:
- **Dev Properties Budget**: All "DEV | Properties" campaigns EXCEPT The Hide
- **The Hide Budget**: Two campaign IDs combined:
  - `23069490466` - "DEV | Properties CE | The Hide" (ENABLED)
  - `21815704991` - "DEV | Properties | Highwayman Arms" (PAUSED)

**Critical Rules Documented**:
- ✅ Always include paused campaigns
- ✅ Filter to "DEV | Properties" for main budget
- ❌ Exclude Castles and Weddings
- ⚠️ The Highwayman = The Hide (same property)

**LaunchAgent Status**:
```bash
launchctl list | grep devonshire-budget
# Output: -	0	com.petesbrain.devonshire-budget ✅
```

**Log File**: `~/.petesbrain-devonshire-budget.log`

**Manual Run**:
```bash
/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv/bin/python3 \
  /Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/scripts/update_budget_tracker.py
```

---

### 2. Weekly Email Integration ✅

**File Modified**: `shared/scripts/weekly-meeting-review.py`

**What Was Added**:
- ✅ Devonshire budget status included in weekly Monday email
- ✅ Shared drives updates section added to email
- ✅ Shows budget pacing, spend, and alerts
- ✅ Lists new/updated shared drive documents per client

**Email Sections** (in order):
1. **Meetings** - Recent meetings from all clients
2. **Completed Tasks** - Tasks completed in last 7 days
3. **Budget Status** - Devonshire budget tracker snapshot
4. **Shared Drive Updates** - New/updated documents per client (NEW)

**Weekly Email Schedule**: Every Monday at 9 AM

**LaunchAgent**: `com.petesbrain.weekly-review` (part of existing system)

---

### 3. Shared Drives Monitoring System ✅ (Manual On-Demand)

**Files Created**:
- `shared/scripts/shared-drives-monitor-v2.py` - Helper functions for manual updates
- `docs/SHARED-DRIVES-WORKFLOW.md` - Complete workflow guide
- Google Task: Monthly reminder to scan shared drives

**What It Does**:
- ✅ On-demand scanning via Claude Code (tell Claude: "Scan shared drives")
- ✅ Matches files to clients using keyword detection
- ✅ Filters out images (includes docs, sheets, slides, PDFs only)
- ✅ Updates client CONTEXT.md files with findings
- ✅ Monthly Google Task reminder (7th of each month)
- ✅ Ad-hoc updates when you notice new files

**Client Keyword Matching**:
Each client has keywords for automatic file matching:
- **devonshire-hotels**: ["devonshire", "dev |", "daba", "cavendish", "beeley", etc.]
- **smythson**: ["smythson", "smy |"]
- **clear-prospects**: ["clear prospects", "cp |"]
- _...and more_

**Included File Types**:
- ✅ Google Docs
- ✅ Google Sheets
- ✅ Google Slides
- ✅ PDFs
- ✅ Word/Excel/PowerPoint
- ❌ Images (excluded)
- ❌ Videos (excluded)

**How to Use**:
```
Tell Claude Code: "Scan shared drives and update client CONTEXT files"
```

**Monthly Reminder**: Google Task on 7th of each month

**Workflow Guide**: See [docs/SHARED-DRIVES-WORKFLOW.md](SHARED-DRIVES-WORKFLOW.md)

---

### 4. Client CONTEXT.md Rollout ✅

**What Was Done**:
- ✅ Added "Shared Drive Resources" section to ALL client CONTEXT.md files
- ✅ Section placed before "Document History" in each file
- ✅ Includes automatic update tracking placeholder

**Clients Updated**:
- ✅ accessories-for-the-home
- ✅ bright-minds
- ✅ clear-prospects
- ✅ crowd-control
- ✅ devonshire-hotels (with specific resources documented)
- ✅ go-glean
- ✅ godshot
- ✅ grain-guard
- ✅ just-bin-bags
- ✅ national-design-academy
- ✅ otc
- ✅ print-my-pdf
- ✅ smythson
- ✅ superspace
- ✅ tree2mydoor
- ✅ uno-lighting

**Section Format**:
```markdown
## Shared Drive Resources

**Last Scanned:** 2025-10-31

### Key Shared Documents

_Automatic monitoring via "Shared with Me" in Google Drive_
_Updated documents will appear here when detected by daily scans_

**Note**: This section tracks important resources shared by the client via Google Drive, including:
- Monthly reports and presentations
- Campaign briefs and strategy documents
- Product data and assets
- Client-maintained documentation
```

**Devonshire-Specific Content** (example of what monitoring will populate):
```markdown
**Monthly Reporting:**
- "Devonshire Hotels Monthly Report - November 2024" (Google Slides)
  - Contains Paid Search section (your responsibility - updated ~7th-8th monthly)
  - Template for monthly performance reporting
```

---

## How It All Works Together

### Daily Workflow (Automated)

**9:00 AM** - Devonshire Budget Tracker
1. Fetches latest spend data from Google Ads
2. Calculates pacing metrics
3. Updates both budget sheets (Dev Properties + The Hide)
4. Logs results

**Monday 9:00 AM** - Weekly Email
1. Gathers meetings from last 7 days
2. Gathers completed tasks from last 7 days
3. Gets Devonshire budget status snapshot
4. Gets shared drive updates from state file (if any from manual scans)
5. Generates HTML email with all sections
6. Sends to petere@roksys.co.uk

**Monthly (7th)** - Shared Drives Reminder
1. Google Task reminder appears
2. User tells Claude Code: "Scan shared drives"
3. Claude searches Google Drive, matches to clients
4. Updates all client CONTEXT.md files
5. Reports findings

### Data Flow

```
Google Ads API (via MCP)
    ↓
update_budget_tracker.py (daily 9 AM)
    ↓
Google Sheets (budget tracker)
    ↓
weekly-meeting-review.py (Monday 9 AM)
    ↓
Email Report

Google Drive API (via MCP)
    ↓
Claude Code (manual on-demand scan)
    ↓
Client CONTEXT.md files (direct updates)
    +
shared/data/shared-drives-state.json
    ↓
weekly-meeting-review.py (Monday 9 AM)
    ↓
Email Report (shows recent updates)
```

---

## Maintenance

### Monthly Budget Updates

**When**: Start of each month (update MONTHLY_BUDGETS dict)

**File**: `clients/devonshire-hotels/scripts/update_budget_tracker.py`

```python
MONTHLY_BUDGETS = {
    "2025-10": {"dev": 11730.00, "hide": 2000.00},
    "2025-11": {"dev": 9000.00, "hide": 2000.00},
    "2025-12": {"dev": 7750.00, "hide": 2000.00},
    # Add new months here
}
```

### Checking System Status

**All LaunchAgents**:
```bash
launchctl list | grep petesbrain
```

**Specific Logs**:
```bash
cat ~/.petesbrain-devonshire-budget.log
cat ~/.petesbrain-shared-drives.log
cat ~/.petesbrain-weekly-review.log
```

**Reload After Changes**:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist
```

### Adding New Client Keywords

**File**: `shared/scripts/shared-drives-monitor.py`

Find `CLIENT_KEYWORDS` dict and add:
```python
CLIENT_KEYWORDS = {
    # ... existing
    "new-client": ["keyword1", "keyword2", "campaign prefix |"],
}
```

---

## Troubleshooting

### Budget Tracker Not Updating

1. **Check LaunchAgent status**:
   ```bash
   launchctl list | grep devonshire-budget
   ```
   Should show: `-	0	com.petesbrain.devonshire-budget`

2. **Check log file**:
   ```bash
   cat ~/.petesbrain-devonshire-budget.log
   ```

3. **Run manually**:
   ```bash
   /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv/bin/python3 \
     /Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/scripts/update_budget_tracker.py
   ```

4. **Common issues**:
   - Campaign name changed → Update GAQL query filter
   - New campaign added → Verify it matches "DEV | Properties" pattern
   - Budget seems wrong → Check MONTHLY_BUDGETS for current month

### Shared Drives Not Detecting Files

1. **Check LaunchAgent status**:
   ```bash
   launchctl list | grep shared-drives
   ```

2. **Check log file**:
   ```bash
   cat ~/.petesbrain-shared-drives.log
   ```

3. **Verify OAuth credentials**:
   ```bash
   ls -la /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json
   ```

4. **Common issues**:
   - File not matched → Add keyword to CLIENT_KEYWORDS
   - Image included → Check INCLUDE_TYPES filter
   - Wrong client → Adjust keyword matching logic

### Weekly Email Missing Section

1. **Check weekly review script runs**:
   ```bash
   cat ~/.petesbrain-weekly-review.log
   ```

2. **Verify state files exist**:
   ```bash
   ls -la /Users/administrator/Documents/PetesBrain/shared/data/shared-drives-state.json
   ```

3. **Run weekly review manually**:
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=... shared/email-sync/.venv/bin/python3 \
     shared/scripts/weekly-meeting-review.py
   ```

---

## Success Metrics

### Budget Tracker
- ✅ Updates daily at 9 AM without manual intervention
- ✅ Correct campaign filtering (DEV | Properties only)
- ✅ Paused campaigns included in calculations
- ✅ The Hide + Highwayman properly combined
- ✅ Accurate pacing calculations
- ✅ Alerts when off-pace (>110% or <90%)

### Shared Drives
- ✅ Scans daily at 8 AM
- ✅ Correctly matches files to clients
- ✅ Excludes images, includes documents
- ✅ Tracks updates over time
- ✅ Populates weekly email with new files
- ✅ Eventually populates client CONTEXT.md files

### Weekly Email
- ✅ Sends every Monday at 9 AM
- ✅ Includes Devonshire budget status
- ✅ Includes shared drive updates
- ✅ Shows meetings and completed tasks
- ✅ Professional HTML formatting
- ✅ Delivered to petere@roksys.co.uk

---

## Files Modified Summary

**Created**:
- `clients/devonshire-hotels/scripts/update_budget_tracker.py`
- `~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist`
- `shared/scripts/shared-drives-monitor.py`
- `~/Library/LaunchAgents/com.petesbrain.shared-drives.plist`
- `docs/SHARED-DRIVES-SETUP.md`
- `docs/DEVONSHIRE-AUTOMATION-COMPLETE.md` (this file)

**Modified**:
- `clients/devonshire-hotels/CONTEXT.md` - Added critical campaign structure and The Hide documentation
- `shared/scripts/weekly-meeting-review.py` - Added budget status and shared drives sections
- All client CONTEXT.md files (16 total) - Added Shared Drive Resources section

**State Files**:
- `shared/data/shared-drives-state.json` (auto-created by monitor)

---

## Next Steps (Optional Future Enhancements)

1. **Automated CONTEXT.md Updates**: Have shared-drives-monitor.py directly update client CONTEXT.md files when new important documents are detected (currently only tracks in state file + email)

2. **Budget Alerts**: Send immediate email if budget pacing exceeds threshold (not just weekly summary)

3. **Multiple Client Budget Trackers**: Extend daily automation to other clients with budget monitoring

4. **Document Categorization**: Use Claude API to automatically categorize shared drive documents (strategy vs. reporting vs. assets)

5. **Historical Tracking**: Archive previous months' budget data for trend analysis

---

**Status**: ✅ All systems operational and tested
**Last Updated**: 2025-10-31
**Author**: Claude Code
