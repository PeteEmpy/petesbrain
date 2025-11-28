# Label Tracking Automation Solution

**Status:** ✅ Production-Ready Hybrid Approach
**Date:** October 31, 2025

## The Challenge

LaunchAgents cannot directly execute MCP calls (they require Claude Code with active MCP access). We needed a solution for daily automated label tracking.

## Solution: Hybrid Manual/Automated Approach

### Phase 1: Manual MCP Execution (Current)

**Workflow:**
1. **User**: "Claude, run daily label tracking"
2. **Claude Code**: Executes `fetch_all_labels.py`
3. **System**: Generates pending_label_queries.json
4. **Claude Code**: Executes all MCP queries sequentially
5. **System**: Processes responses, updates current-labels.json files
6. **System**: Detects transitions, saves to monthly files
7. **Complete**: All 8 clients tracked in ~2-3 minutes

**Files Created:**
- `fetch_all_labels.py` - Query generator
- `pending_label_queries.json` - MCP query queue
- `label_tracking_executor.py` - Data processor

**Advantages:**
- ✅ Works today with existing infrastructure
- ✅ No background process complexity
- ✅ User maintains control and visibility
- ✅ Reliable (no silent failures)

**Process:**
```bash
# User runs once daily (or on-demand)
python3 fetch_all_labels.py   # Generates queries
# Claude Code executes MCP queries
# System processes and saves results
```

---

### Phase 2: Scheduled Reminders (Near Future)

**Enhancement:** LaunchAgent sends email reminder

**LaunchAgent Purpose:**
- Runs daily at 10:00 AM
- Sends email to petere@roksys.co.uk
- Subject: "⏰ Daily Label Tracking Reminder"
- Body: "Time to run daily label tracking. Ask Claude Code: 'Run daily label tracking'"

**Implementation:**
```xml
<!-- ~/Library/LaunchAgents/com.petesbrain.label-tracker-reminder.plist -->
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.label-tracker-reminder</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/mail</string>
        <string>-s</string>
        <string>⏰ Daily Label Tracking Reminder</string>
        <string>petere@roksys.co.uk</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

**Advantages:**
- ✅ Never forget to run tracking
- ✅ Consistent daily schedule
- ✅ Simple, reliable
- ✅ No complex background processes

---

### Phase 3: Full Automation (Future - Optional)

**Potential Solutions** (if full automation becomes critical):

#### Option A: MCP Background Server
- Run MCP server as background process
- Python script calls MCP API directly
- Requires: MCP server authentication, process management

#### Option B: Google Ads API Direct
- Bypass MCP, use Google Ads Python client directly
- Requires: Service account setup, API quotas
- More complex but fully automated

#### Option C: Cloud Function
- Deploy to Google Cloud Functions
- Triggered by Cloud Scheduler (cron)
- Stores results in Cloud Storage or sends to webhook
- Requires: GCP setup, monthly costs (~$5-10)

**Current Decision:** Phase 1 (Manual) + Phase 2 (Reminders) sufficient for current needs

---

## Current Status (Phase 1)

### ✅ Completed Components

1. **Query Generator** (`fetch_all_labels.py`)
   - Generates GAQL queries for all 8 enabled clients
   - Handles partial coverage for large accounts (LIMIT 500)
   - Outputs pending_label_queries.json

2. **Data Processor** (`label_tracking_executor.py`)
   - Parses MCP responses
   - Detects label transitions
   - Updates current-labels.json snapshots
   - Saves transitions to monthly files

3. **Report Integration** (`label_validation_report.py`)
   - Generates HTML sections for weekly reports
   - Shows label distribution and recent transitions
   - Integrated into run_automated_analysis.py

### 📊 Tracking Coverage

**Full Coverage (LIMIT 10000):**
- Tree2mydoor (272 products tracked)
- Grain Guard
- Crowd Control
- HappySnapGifts
- WheatyBags
- BMPM

**Partial Coverage (LIMIT 500):**
- Accessories for the Home (~500 of ~1000 products)
- Uno Lights (~500 of ~1000 products)

---

## Usage Instructions

### Daily Label Tracking (Manual)

**User asks Claude Code:**
> "Run daily label tracking for all clients"

**Claude Code executes:**
1. Runs `fetch_all_labels.py` to generate queries
2. Loads `pending_label_queries.json`
3. For each client:
   - Executes `mcp__google-ads__run_gaql()` with query
   - Passes response to `track_client_labels(config, response)`
4. Reports summary (transitions detected, files updated)

**Expected output:**
```
======================================================================
🏷️  Product Hero Label Tracker
======================================================================
Date: 2025-10-31

✅ Tree2mydoor: 272 products, 0 transitions
✅ AFH: 500 products, 3 transitions (2 upgrades, 1 downgrade)
✅ Uno Lights: 500 products, 0 transitions
... (all clients)

📊 Summary:
- 8 clients tracked
- 2,500+ products monitored
- 5 total transitions detected
- Files updated in history/label-transitions/

Transitions saved to 2025-10.json files.
```

**Frequency:** Daily (recommended 10:00 AM)

**Time required:** 2-3 minutes

---

### Weekly Report Generation (Automated)

**Automatic Integration:**
- LaunchAgent runs `run_automated_analysis.py` every Tuesday
- Label validation sections auto-included for each client
- No manual intervention needed

**Report includes:**
- Current label distribution (Heroes, Sidekicks, Villains, Zombies)
- Transitions in last 7 days
- Recommendations based on changes

---

## Data Storage Structure

```
tools/product-impact-analyzer/
├── history/
│   └── label-transitions/
│       ├── tree2mydoor/
│       │   ├── current-labels.json       # Latest snapshot
│       │   ├── 2025-10.json             # October transitions
│       │   └── 2025-11.json             # November transitions
│       ├── accessories-for-the-home/
│       ├── uno-lights/
│       └── ... (all clients)
│
├── pending_label_queries.json            # MCP query queue
├── fetch_all_labels.py                   # Query generator
├── label_tracking_executor.py            # Data processor
└── label_validation_report.py            # Report generator
```

---

## Monitoring & Maintenance

### Daily Checks
- Run label tracking (manual via Claude Code)
- Review transition summary
- Investigate unexpected downgrades (Heroes → Villains)

### Weekly Checks
- Review weekly report email (automated)
- Verify label distributions look reasonable
- Check for structural misalignments (products in wrong campaigns)

### Monthly Checks
- Review monthly transition files
- Analyze patterns (seasonality, product lifecycle)
- Identify optimization opportunities

---

## Future Enhancements

### Immediate (This Week)
- [x] Option B: Weekly report integration ✅
- [x] Option C: Automation solution ✅
- [ ] Option A: Historical backfill (October 2025)

### Short Term (Next 2 Weeks)
- [ ] LaunchAgent email reminder (Phase 2)
- [ ] Email alerts for significant transitions
- [ ] Sampled tracking for full coverage of large accounts

### Medium Term (Next Month)
- [ ] Trend analysis (label stability over time)
- [ ] Campaign structure validation
- [ ] Automated restructuring recommendations

### Long Term (Optional)
- [ ] Full background automation (if needed)
- [ ] Real-time monitoring dashboard
- [ ] Predictive label transitions

---

## Conclusion

**Current Solution (Phase 1):**
- ✅ Production-ready
- ✅ Simple and reliable
- ✅ User maintains control
- ✅ 2-3 minutes daily effort

**Upgrade Path (Phase 2):**
- Add email reminders for consistency
- Still manual execution
- Minimal additional complexity

**Future (Phase 3 - Optional):**
- Full automation if business case justifies
- Multiple technical approaches available
- Would require infrastructure investment

**Recommendation:** Stay with Phase 1 for now. The manual approach provides good visibility and control while requiring minimal time investment. Add Phase 2 reminders if tracking is occasionally forgotten.

---

**Last Updated:** October 31, 2025
**Status:** ✅ Production Ready
**Maintained By:** Claude Code + Pete Ewbank
