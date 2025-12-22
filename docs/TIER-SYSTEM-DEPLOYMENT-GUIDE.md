# Tier System Consolidated Deployment Guide

**Status:** ✅ Complete and Active
**Date Implemented:** 2025-12-17
**System Version:** Consolidated Batch Workflow v1.0

---

## 🎯 **Overview**

The three-tier negative keyword system now uses a **consolidated batch deployment workflow** instead of creating per-client tasks. This means:

✅ **ONE task every 2 weeks** for Tier 1 deployment (covers all clients)
✅ **ONE task per month** for Tier 2 review (informational)
✅ **Interactive script** for batch or per-term review
✅ **Configurable frequencies** via JSON config file

---

## 📋 **How It Works**

### Weekly Monitoring (Every Monday 9 AM)

The LaunchAgent runs `tier-system-weekly-monitor.py` which:

1. **Checks existing Tier 2 terms** for promotion to Tier 1 (30+ clicks reached)
2. **Scans last 7 days** for NEW terms (10+ clicks, 0 conversions)
3. **Auto-adds new terms** to tracker with appropriate status
4. **Generates alerts** for daily briefing email
5. **Creates tasks** based on bi-weekly/monthly schedule

### Task Creation Schedule

**Configuration:** `shared/scripts/tier-system-config.json`

| Task Type | Frequency | When Created | Priority |
|-----------|-----------|--------------|----------|
| **Tier 1 Deployment** | Bi-weekly | Weeks 1 & 3 of month | P0 (always) |
| **Tier 2 Review** | Monthly | Week 1 of month | P2 (informational) |

**Example Schedule:**
- **Week 1 (1st-7th):** Tier 1 task + Tier 2 task created
- **Week 2 (8th-14th):** No tasks (monitoring only)
- **Week 3 (15th-21st):** Tier 1 task created
- **Week 4 (22nd-28th):** No tasks (monitoring only)

---

## 🚀 **Deployment Workflow**

### When You Receive a Tier 1 Task

**Task Title:** "Deploy Tier 1 Negative Keywords Across Clients"

**Task Contains:**
- Total terms to deploy across all clients
- Projected annual waste
- Client breakdown (e.g., "Smythson: 51 terms")
- Instructions to run interactive script

### Step 1: Run Interactive Script

```bash
cd ~/Documents/PetesBrain.nosync
python3 shared/scripts/deploy-tier1-interactive.py
```

### Step 2: Review Summary

The script shows:
```
SUMMARY: 3 client(s) with Tier 1 terms

  - tree2mydoor: 2 terms (£336/year)
  - smythson: 51 terms (£24,215/year)
  - accessories-for-the-home: 0 terms

TOTAL: 53 terms, £24,551/year projected waste

Press Enter to begin deployment review...
```

### Step 3: Per-Client Review

For each client:
```
================================================================================
CLIENT: TREE2MYDOOR
================================================================================
Customer ID: 4941701449
Tier 1 Terms: 2
Projected Annual Waste: £336

  1. [olive trees] - 50 clicks, £32.47
  2. [tree gifts uk] - 32 clicks, £23.60

Deploy 2 terms to tree2mydoor? (y/n/skip):
```

**Options:**
- `y` = Proceed to deployment
- `n` = Cancel this client
- `skip` = Skip this client, move to next

### Step 4: Choose Deployment Mode

```
Mode: (batch/review):
```

**Batch Mode:**
- Shows list of campaigns
- Select ONE campaign
- Deploys ALL terms to that campaign at once
- Fast for high-confidence terms

**Review Mode:**
- Shows each term individually
- Deploy, skip, or quit for each term
- Select campaign per term
- Slower but more control

### Step 5: Campaign Selection

**Batch Mode:**
```
Available campaigns:
  1. ✅ T2MD | Search | Memorial Gift 150 20/5 140 7/4 (ID: 123456)
  2. ✅ T2MD | Shopping | Catch All 170 150 20/10 (ID: 123457)
  3. ⏸️ T2MD | Search | Roses 152 29/8 140 14/1 (ID: 123458)

Enter campaign number or ID (or 'all' for account-level):
```

**Review Mode:**
```
--- Term 1/2 ---
Search Term: [olive trees]
  Clicks: 50
  Spend: £32.47
  Campaign: T2MD | Shopping | Catch All 170 150

Action: (d)eploy / (s)kip / (q)uit: d

Campaigns:
  1. T2MD | Search | Memorial Gift
  2. T2MD | Shopping | Catch All

Campaign # or ID: 2
```

### Step 6: Deployment Report

After processing all clients:
```
================================================================================
DEPLOYMENT SUMMARY
================================================================================

tree2mydoor:
  ✅ Deployed: 2
  ❌ Failed: 0

smythson:
  ✅ Deployed: 51
  ❌ Failed: 0

================================================================================
TOTAL DEPLOYED: 53
TOTAL FAILED: 0
================================================================================

📄 Report saved: shared/data/state/deployment-report-2025-12-17.json

✅ Deployment complete!
💡 Mark your bi-weekly deployment task as complete in Task Manager
```

### Step 7: Mark Task Complete

In Task Manager, complete the deployment task. The system automatically logs to `roksys/tasks-completed.md`.

---

## 🔧 **Configuration**

### Adjust Frequencies

Edit `shared/scripts/tier-system-config.json`:

```json
{
  "tier1_deployment_frequency": "bi-weekly",  // Change to "monthly" or "weekly"
  "tier2_review_frequency": "monthly",
  "priority_threshold_pounds": 0,
  "always_p0": true,  // Change to false for threshold-based priority
  "deployment_schedule": {
    "tier1_deployment_weeks": [1, 3],  // Which weeks to create tasks
    "tier2_review_week": 1
  }
}
```

**No code changes required** - just edit JSON and save.

### Change Priority Logic

**Current:** Always P0 for Tier 1 tasks

**To change:**
```json
{
  "always_p0": false,
  "priority_threshold_pounds": 5000
}
```

Now:
- Waste > £5,000/year = P0
- Waste < £5,000/year = P1

---

## 📊 **Tracking & Monitoring**

### Tracker Database

**Location:** `shared/data/tier2_tracker.json`

**Structure:**
```json
{
  "clients": {
    "tree2mydoor": {
      "customer_id": "4941701449",
      "terms": [
        {
          "search_term": "olive trees",
          "clicks": 50,
          "cost": 32.47,
          "status": "promoted_tier1",
          "deployed": false,
          "next_review_date": "2025-12-17"
        }
      ]
    }
  }
}
```

**Term Statuses:**
- `monitoring` = Tier 2 (10-29 clicks, waiting for 30+)
- `promoted_tier1` = Ready for deployment
- `deployed` flag = Already deployed (won't show in interactive script)

### Alert Notifications

**Location:** `shared/data/state/tier-alerts.json`

**Used by:** Daily briefing email to show summary

**Format:**
```json
{
  "timestamp": "2025-12-17T09:00:00",
  "alerts": [
    {
      "client": "tree2mydoor",
      "tier2_promoted_count": 2,
      "new_tier1_count": 0,
      "new_tier2_count": 18,
      "total_waste_projection": 336
    }
  ]
}
```

### Deployment Reports

**Location:** `shared/data/state/deployment-report-YYYY-MM-DD.json`

**Contains:**
- Timestamp
- Total deployed/failed
- Per-client breakdown
- Campaign IDs used

---

## 🔍 **Troubleshooting**

### "No Tier 1 terms pending deployment"

**Cause:** All Tier 1 terms already deployed, or no terms promoted yet

**Solution:** Normal - wait for next weekly run to detect new terms

### Task not created on schedule

**Check 1:** Is LaunchAgent running?
```bash
launchctl list | grep tier2-tracker
```

**Check 2:** Is it the right week?
```bash
python3 -c "from datetime import datetime; print(f'Week {((datetime.now().day - 1) // 7) + 1}')"
```

**Check 3:** Check logs
```bash
tail -50 ~/.petesbrain-tier2-tracker.log
```

### Interactive script shows wrong clients

**Check:** Tracker database might be out of date
```bash
cat shared/data/tier2_tracker.json | grep -c "promoted_tier1"
```

If 0, no Tier 1 terms are ready. Wait for weekly monitor to run.

### Campaign deployment failed

**Check 1:** OAuth token expired?
```bash
ls -l ~/.google-ads/
```

**Check 2:** Campaign ID correct?
- Script shows campaign names and IDs
- Can enter either number (from list) or direct ID

**Check 3:** API permissions
- Manager account 2569949686 needs edit access
- Customer ID must be correct

---

## 📈 **Expected Timeline**

### Week 1 (Initial Rollout)
- ✅ Phase 2 completed: 53 Tier 1 terms identified
- ✅ Tasks created for Tree2mydoor (P1) and Smythson (P0)
- ⏳ Deploy using interactive script manually (Phase 2 findings)

### Week 2-3 (First Cycle)
- 📊 Weekly monitor runs, checks Tier 2 terms for promotion
- 📊 Scans for NEW terms in last 7 days
- 🔔 Creates consolidated task if Week 1 or 3

### Week 4-8 (Steady State)
- 🔄 Bi-weekly deployments become routine
- 📉 Waste reduction becomes measurable
- 🎯 Adjust frequencies based on volume

### Month 3 (Optimization)
- 📊 Review false positive rate
- 🔧 Consider changing to monthly if volume low
- 🎯 Consider threshold-based priority if waste decreases

---

## 🎓 **Quick Reference**

### File Locations

| File | Purpose |
|------|---------|
| `shared/scripts/deploy-tier1-interactive.py` | Interactive deployment script |
| `shared/scripts/tier-system-config.json` | Configuration (frequencies, priority) |
| `shared/scripts/tier-system-weekly-monitor.py` | Weekly monitoring + task creation |
| `shared/data/tier2_tracker.json` | Term tracking database |
| `shared/data/state/tier-alerts.json` | Alerts for daily briefing |
| `shared/data/state/deployment-report-*.json` | Deployment history |

### Commands

```bash
# Run interactive deployment
python3 shared/scripts/deploy-tier1-interactive.py

# Run weekly monitor manually (testing)
python3 shared/scripts/tier-system-weekly-monitor.py

# Check tracker status
cat shared/data/tier2_tracker.json | jq '.clients | to_entries[] | {client: .key, terms: (.value.terms | length)}'

# Check what week it is
python3 -c "from datetime import datetime; print(f'Week {((datetime.now().day - 1) // 7) + 1}')"

# View LaunchAgent status
launchctl list | grep tier2-tracker

# View logs
tail -f ~/.petesbrain-tier2-tracker.log
```

### Task Workflow

1. **Task appears** in Task Manager (Week 1 or 3)
2. **Run script:** `python3 shared/scripts/deploy-tier1-interactive.py`
3. **Review summary** showing all clients
4. **Per-client decision:** Deploy, skip, or cancel
5. **Choose mode:** Batch (fast) or Review (detailed)
6. **Select campaigns** for negative keywords
7. **Review report** showing deployed/failed counts
8. **Mark task complete** in Task Manager

---

## 📚 **Related Documentation**

- **System Design:** `docs/NEGATIVE-KEYWORD-TIER-SYSTEM.md`
- **Phase 2 Results:** `docs/NEGATIVE-KEYWORD-TIER-SYSTEM-PHASE-2-ROLLOUT.md`
- **Notification Protocol:** `docs/TIER-SYSTEM-NOTIFICATION-PROTOCOL.md`
- **LaunchAgent Logs:** `~/.petesbrain-tier2-tracker.log`

---

## ✨ **Benefits of Consolidated Workflow**

**Before (Per-Client Tasks):**
- ❌ 10-20 tasks per week (overwhelming)
- ❌ Context switching between clients
- ❌ No batch processing capability
- ❌ Hard to see total impact

**After (Consolidated Workflow):**
- ✅ ONE task every 2 weeks (manageable)
- ✅ Process all clients in single session
- ✅ Batch mode for efficiency
- ✅ Clear total waste projection
- ✅ Configurable frequencies
- ✅ Review mode for careful analysis

**Time Savings:**
- Batch mode: ~2-3 minutes per client
- Review mode: ~5-10 minutes per client
- Total session: 30-60 minutes every 2 weeks
- vs. 5-10 minutes per task × 20 tasks = 100-200 minutes

---

**Questions? Check:**
- LaunchAgent logs: `~/.petesbrain-tier2-tracker.log`
- Tracker database: `shared/data/tier2_tracker.json`
- Configuration: `shared/scripts/tier-system-config.json`
