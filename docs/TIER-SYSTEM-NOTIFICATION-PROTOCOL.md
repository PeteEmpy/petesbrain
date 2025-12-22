# Tier System Notification Protocol

**Status:** ✅ Complete and Active
**Date Implemented:** 2025-12-17
**System Version:** Enhanced Weekly Monitor v1.0

---

## 🔔 **How You Get Notified**

### Tier 1 Terms (Immediate Action Required)

**Notification Method:** Daily Briefing Email + Tasks

#### Initial Rollout (One-Time)
✅ **Tasks created for Phase 2 rollout findings:**
- `[Tree2mydoor] Deploy 2 Tier 1 negative keywords` - P1
- `[Smythson] Deploy 51 Tier 1 negative keywords (£24K/year waste)` - P0

These appear in:
- Task Manager UI
- Daily briefing "Personal Tasks" section
- `clients/{client}/tasks.json`

#### Ongoing Detection (Weekly)
📅 **Every Monday after 9 AM:**

Your daily briefing email will include a **"🔴 Negative Keyword Alerts"** section showing:
- NEW Tier 1 terms detected (jumped straight to 30+ clicks)
- Tier 2 terms promoted to Tier 1 (reached threshold after monitoring)
- Projected annual waste
- Direct links to tracker and reports

**Example Alert:**
```
### 🔴 Negative Keyword Alerts

Weekly tier system check: 2 client(s) with new findings

**Smythson:**
- 🆕 3 NEW Tier 1 term(s) detected (immediate action required)
  - Terms: aspinal bags, smyth jewellery, selfridge
- 📈 2 Tier 2 term(s) promoted to Tier 1 (reached 30+ clicks, 0 conv)
  - Terms: smythson sale, luxury diary
- 💰 Est. annual waste: £3,450
- 📊 View tracker

**Tree2mydoor:**
- 🟡 5 NEW Tier 2 term(s) added to monitoring (7-day watch)
```

---

### Tier 2 Terms (Monitoring)

**Notification Method:** Daily Briefing Email (on promotion only)

Tier 2 terms are **silently monitored** weekly. You only see them when:
1. They get promoted to Tier 1 (shown in alert above)
2. You manually check the tracker: `shared/data/tier2_tracker.json`

**No notifications for:**
- New Tier 2 terms added to tracker (too noisy)
- Tier 2 terms still monitoring (no action needed)
- Tier 2 terms that start converting (good news!)

---

## 🤖 **Automated Monitoring System**

### LaunchAgent: `com.petesbrain.tier2-tracker-weekly.plist`

**Schedule:** Every Monday at 9:00 AM
**Script:** `shared/scripts/tier-system-weekly-monitor.py`
**Log:** `~/.petesbrain-tier2-tracker.log`

### What It Does

**Step 1: Check Existing Tier 2 Terms**
- Queries Google Ads API for current stats (last 60 days)
- Flags terms that reached 30+ clicks, 0 conversions
- Marks as 'promoted_tier1' status
- Generates promotion report: `clients/{client}/reports/tier1-promotions-{date}.txt`

**Step 2: Scan for NEW Terms (7-Day Rolling)**
- Runs fresh search term query for last 7 days
- Identifies terms with 10+ clicks not yet in tracker
- Classifies into Tier 1 (30+) or Tier 2 (10-29)
- Auto-adds to tracker with appropriate status

**Step 3: Generate Alert Summary**
- Creates JSON file: `shared/data/state/tier-alerts.json`
- Contains counts, terms, waste projections per client
- Daily briefing reads this file and formats for email

**Step 4: Save Tracker Data**
- Updates `shared/data/tier2_tracker.json`
- Maintains full history of all tracked terms
- Used by weekly runs for promotion detection

---

## 📧 **Daily Briefing Integration**

### File Modified
`agents/daily-intel-report/daily-intel-report.py`

### Function Added
```python
def get_tier_system_alerts():
    """Get negative keyword tier system alerts from weekly monitoring"""
```

**Behavior:**
- Reads `shared/data/state/tier-alerts.json`
- Only shows alerts from last 7 days (freshness check)
- Returns empty string if no alerts (section doesn't appear)
- Formats with client names, counts, terms, waste projections

### Integration Point
**Phase 3 - Data Collection:**
```python
logger.info("  🔴 Checking tier system alerts...")
tier_alerts_section = get_tier_system_alerts()
```

**Phase 4 - Briefing Assembly:**
```markdown
## ⚠️ Client Alerts (2-Day Lag)
{anomalies_section}
---
{tier_alerts_section}  # ← Tier system alerts inserted here
---
## 📊 Performance Overview
```

---

## 📁 **File Locations**

### Scripts
- **Enhanced Monitor:** `shared/scripts/tier-system-weekly-monitor.py`
- **Tier 2 Tracker:** `shared/scripts/tier2_tracker.py` (library)
- **Deployment Tool:** `shared/scripts/add-negative-keywords-universal.py`

### Data Files
- **Tracker Database:** `shared/data/tier2_tracker.json`
- **Alert Notifications:** `shared/data/state/tier-alerts.json`
- **Client Reports:** `clients/{client}/reports/tier1-promotions-{date}.txt`

### Configuration
- **LaunchAgent:** `~/Library/LaunchAgents/com.petesbrain.tier2-tracker-weekly.plist`
- **Log File:** `~/.petesbrain-tier2-tracker.log`

---

## 🎯 **What You Should Do**

### Every Morning
1. ✅ **Read daily briefing email** (arrives at 7 AM)
2. 🔴 **Check "Negative Keyword Alerts" section** (if present)
3. 📝 **Note which clients have Tier 1 terms**

### When Alerts Appear
1. **For NEW Tier 1 terms:**
   - Review terms in alert (shows first 3)
   - Click tracker link to see full list
   - Add as [exact match] negatives using deployment script

2. **For Tier 2 promotions:**
   - These were already monitored for 7 days
   - High confidence - deploy immediately
   - Use the generated `tier1-promotions-{date}.txt` report

### Deployment Process
```bash
# Review the terms first
cat clients/{client}/reports/tier1-promotions-{date}.txt

# Deploy using universal script
python3 shared/scripts/add-negative-keywords-universal.py \
  --customer-id {CUSTOMER_ID} \
  --campaign-id {CAMPAIGN_ID} \
  --keywords "term1,term2,term3" \
  --match-type exact
```

---

## 🚨 **If You Don't See Alerts**

### Possible Reasons

1. **No new Tier 1/Tier 2 terms this week** - Good news!
2. **Monitor hasn't run yet** - Check log: `tail -f ~/.petesbrain-tier2-tracker.log`
3. **Alert file is stale** - File older than 7 days is ignored
4. **LaunchAgent not loaded** - Run: `launchctl list | grep tier2-tracker`

### Manual Check
```bash
# Check if LaunchAgent is loaded
launchctl list | grep tier2-tracker

# View recent log
tail -50 ~/.petesbrain-tier2-tracker.log

# Check alert file
cat shared/data/state/tier-alerts.json

# Run monitor manually (for testing)
python3 shared/scripts/tier-system-weekly-monitor.py
```

---

## 📊 **Monitoring the Monitor**

### Weekly Checks (Every Monday)
- ✅ Check daily briefing for tier alerts section
- ✅ Verify LaunchAgent ran: `grep "WEEKLY MONITOR COMPLETE" ~/.petesbrain-tier2-tracker.log`
- ✅ Review tracker growth: `wc -l shared/data/tier2_tracker.json`

### Monthly Checks
- ✅ Review deployed Tier 1 negatives (did waste decrease?)
- ✅ Check for false positives (terms blocking converting queries?)
- ✅ Verify LaunchAgent still loaded: `launchctl list | grep tier2-tracker`

---

## 🔧 **Troubleshooting**

### "LaunchAgent not running"
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.tier2-tracker-weekly.plist
```

### "No alerts even though I know there are new terms"
1. Check alert file timestamp: `ls -l shared/data/state/tier-alerts.json`
2. Check daily briefing ran: `ls -lrt briefing/ | tail -1`
3. Run monitor manually: `python3 shared/scripts/tier-system-weekly-monitor.py`

### "Alerts showing wrong data"
- Alert file might be stale
- Daily briefing only shows alerts from last 7 days
- Delete alert file to reset: `rm shared/data/state/tier-alerts.json`
- Wait for next Monday run

---

## 📈 **Success Metrics**

### What to Track
- **Tier 1 deployment rate:** % of Tier 1 terms deployed within 1 week
- **Waste reduction:** Month-over-month decrease in non-converting spend
- **Tier 2 promotion rate:** % of Tier 2 terms that reach Tier 1
- **False positive rate:** % of deployed negatives that blocked converting queries

### Expected Results
- **Immediate:** £24K/year waste identified (Phase 2 rollout)
- **Week 1:** 10-20% of Tier 1 terms deployed
- **Month 1:** 50-70% of Tier 1 terms deployed
- **Month 3:** Measurable spend decrease on non-converting terms

---

## 🎓 **Summary**

**You get notified through:**
1. ✅ **Tasks** (for initial Phase 2 rollout findings)
2. ✅ **Daily briefing email** (for ongoing weekly detections)

**When notifications appear:**
- 🔴 **NEW Tier 1 terms** (jumped to 30+ clicks in 7 days)
- 📈 **Tier 2 promotions** (reached 30+ clicks after monitoring)

**What to do:**
- Review terms in alert
- Deploy as [exact match] negatives
- Track waste reduction

**Automation level:** 100%
- Weekly monitoring runs automatically
- Daily briefing includes alerts automatically
- No manual checks required (unless troubleshooting)

---

**Questions? Check:**
- System docs: `docs/NEGATIVE-KEYWORD-TIER-SYSTEM.md`
- Rollout results: `docs/NEGATIVE-KEYWORD-TIER-SYSTEM-PHASE-2-ROLLOUT.md`
- LaunchAgent logs: `~/.petesbrain-tier2-tracker.log`
