# Smythson Q4 Strategy Dashboard - Status

**Created**: 2025-11-03
**Status**: ✅ COMPLETE - Ready to Use

## Final Dashboard

**Spreadsheet ID**: `10vRzZJuUQMX0l86plKcuZfdoiidoexI1LPYnhr6gJlU`
**Link**: https://docs.google.com/spreadsheets/d/10vRzZJuUQMX0l86plKcuZfdoiidoexI1LPYnhr6gJlU/edit

### Layout: Single-Sheet Overview Dashboard

**Design Philosophy**: At-a-glance clarity with traffic light status indicators

### Content Sections

1. **📊 Executive Summary**
   - Q4 period (Oct 29 - Dec 31, 9 weeks)
   - Total budget (£367,014)
   - Revenue target (£780,691)
   - Target ROAS (2.13 blended)

2. **🎯 Regional Overview**
   - UK: £160,752 budget, 3.00 ROAS target
   - USA: $133,960 budget, 1.50 ROAS target
   - EUR: €51,382 budget, 1.50 ROAS target
   - ROW: £20,920 budget, 1.00 ROAS target
   - Each with status indicator and % of target revenue

3. **🚦 Current Status at a Glance**
   - Total Revenue vs Target
   - Total Spend vs Budget
   - Overall ROAS
   - Budget Pacing
   - Active Initiatives count
   - Critical Issues count
   - All with traffic light status (🟢🟡🔴⚪)

4. **📋 Initiative Status (by Phase)**
   - All 13 Q4 milestones organized by phase (1-5)
   - Phase 1: ✅ 3 campaigns launched (UK, EUR, USA)
   - Phase 2: 📋 Nov 15 changes (UK ROAS, ROW launch, review)
   - Phase 3: 📋 Nov 25 Thanksgiving boost
   - Phase 4: 📋 Dec 1 adjustments (all regions)
   - Phase 5: 📋 Dec 15 & 31 assessments
   - Each with date, status, and expected impact

5. **🚨 Active Issues & Recovery Actions**
   - Issue tracking table (currently: no active issues)
   - Date, Issue, Region, Status, Action Taken columns

6. **📌 Status Key**
   - 🟢 Green: On track / No issues
   - 🟡 Amber: Monitoring / Minor issues
   - 🔴 Red: Critical / Requires immediate action
   - ⚪ White: Not started / No data yet
   - ✅ Complete: Initiative completed
   - 📋 Scheduled: Upcoming initiative

### Branding Applied

✅ Rok Systems Green (#6CC24A) main header with white text
✅ Professional gray section headers
✅ "Prepared by Rok Systems (roksys.co.uk)" attribution
✅ Bold section titles
✅ Clear emoji status indicators throughout

### How to Use

**Weekly Update Process:**
1. Update "Current Status at a Glance" section with latest numbers
2. Update Regional Overview with actual ROAS and % of target
3. Change initiative status from 📋 Scheduled → 🟢 Complete as milestones are hit
4. Add any issues to "Active Issues" section with 🔴 Red or 🟡 Amber status
5. Update "Last Updated" date in Executive Summary

**Traffic Light Rules:**
- 🟢 Green: Performance on or above target
- 🟡 Amber: Performance 5-15% below target (monitoring)
- 🔴 Red: Performance >15% below target (action required)
- ⚪ White: No data yet or not started

**What to Track:**
- Regional ROAS vs targets (UK: 3.0, USA: 1.5, EUR: 1.5, ROW: 1.0)
- Budget pacing (should be ~11% per week over 9 weeks)
- Revenue progress (should be ~11% per week toward £780,691)
- Initiative completion on schedule

### Why This Layout Works

**Single-sheet simplicity**: Everything visible without tab-switching
**Traffic lights prominent**: Instant status understanding at a glance
**Organized by importance**: Executive summary first, details below
**Clear sections**: Visual dividers between each section
**Emoji status**: Universal, colorful, instantly recognizable
**Action-oriented**: Issues section prompts corrective actions

### Automation Setup ✅

**Daily Updates**: Configured to run every morning at 7:00 AM
- Script: `clients/smythson/scripts/update-q4-dashboard.py`
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.smythson-dashboard.plist`
- Logs: `~/.petesbrain-smythson-dashboard.log`

**Status**: ✅ **FULLY OPERATIONAL** (as of 2025-11-10)

**Recent Fix** (2025-11-10):
- Fixed Google Sheets API quota exceeded error (reduced 78 API calls → 1 batch call)
- Installed missing `cryptography` dependency
- Tested and verified working
- See [dashboard-automation-fix-2025-11-10.md](dashboard-automation-fix-2025-11-10.md) for full details

**Email Integration**:
- ✅ **Included in weekly summary email** (Mondays 8:30 AM)
- No separate daily emails (reduces inbox noise)
- Q4 dashboard section appears in weekly business summary

**What it does**:
1. Fetches latest Google Ads performance data for all 4 regions via API
2. Updates dashboard with current metrics and traffic lights using **single batch API call**
3. Saves data to JSON for weekly summary email integration
4. Runs automatically every morning at 7 AM
5. **Performance**: 99% API quota reduction (78 calls → 1 call per run)

**Manual run**:
```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts
.venv/bin/python3 update-q4-dashboard.py
```

**Verify automation is working**:
```bash
# Check last run log
tail -20 ~/.petesbrain-smythson-dashboard.log

# Should show:
# Dashboard updated successfully
# Total API calls: 1 (batch update with 78 cells)
# Email sent successfully to petere@roksys.co.uk
```

### Revenue Performance Tracking ✅

**Status**: Complete (2025-11-04)

**What's included**:
- Target revenue columns for November and December
- Traffic light status for revenue performance vs strategy projections
- **Weighted pacing model** accounts for multiple factors:
  - **Learning period** (Days 1-10): 0.4x → 0.6x → 0.8x → 1.0x
  - **Black Friday/Cyber Monday** (Nov 25-30): 1.5x multiplier
  - **Pre-Christmas peak** (Dec 15-23): 1.3x multiplier
  - **Post-Christmas** (Dec 26-31): 0.9x multiplier
  - **Phase transitions** (Nov 15, 25, Dec 1): 0.85x for 3 days (Smart Bidding re-learning)

**Why weighted pacing?**
Simple day-counting assumes linear revenue distribution, but Q4 is heavily weighted toward Black Friday and pre-Christmas periods. The weighted model prevents false "underperforming" alerts before peak shopping dates.

**Dashboard columns**:
- **F**: Actual Revenue (from Google Ads API)
- **G**: Expected Revenue (what we should have by now, based on weighted pacing)
- **H**: Rev Status (🟢🟡🔴 comparing actual vs expected)
- **I**: Spend
- **J**: Target Revenue (full monthly target from final strategy)

**Traffic light thresholds** (more lenient than ROAS):
- 🟢 Green: Actual ≥ 85% of weighted expected
- 🟡 Amber: Actual ≥ 70% of weighted expected
- 🔴 Red: Actual < 70% of weighted expected

**Documentation**: See [revenue-pacing-model.md](revenue-pacing-model.md) for detailed explanation of weighted pacing calculation

### Next Steps

1. ✅ Daily automation configured
2. ✅ Revenue traffic lighting implemented with weighted pacing
3. Add Alex and Lauryn to email recipients when ready
4. Monitor first few automated runs (especially Black Friday performance)
5. Use dashboard for weekly status check-ins and client reporting

### Optional Enhancements (If Desired)

If you want to add more visual polish manually:
- Add borders around tables
- Add more background colors to sections
- Widen columns for better readability
- Add conditional formatting for automatic color changes
- Freeze top rows for scrolling

But it's perfectly usable as-is for tracking Q4 strategy.

---

**Result**: Clean, clear dashboard ready for Q4 tracking with prominent traffic lights showing exactly what's happening at any time.
