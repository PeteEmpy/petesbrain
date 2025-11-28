# Budget Monitoring System Setup Guide

**Created:** October 30, 2025
**Purpose:** Automated daily and weekly budget monitoring for client Google Ads campaigns

---

## Overview

This system provides two levels of budget monitoring:

1. **Daily Budget Monitor** - Sends alerts when budget deviates from target pacing (>5%)
2. **Weekly Budget Status** - Includes budget status in weekly review email

Both systems monitor **Devonshire Hotels** with £11,000 November 2025 budget.

---

## System Architecture

```
┌─────────────────────────────────┐
│   Google Ads (via MCP)          │
│   Account: 5898250490           │
│   Campaigns: DEV | Properties   │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ daily-budget-monitor.py         │
│ • Runs: Daily at 9:00 AM        │
│ • Threshold: ±5% deviation      │
│ • Alerts: Email if triggered    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ weekly-meeting-review.py        │
│ • Runs: Monday at 9:00 AM       │
│ • Includes: Budget status       │
│ • Shows: Pacing, deviation      │
└─────────────────────────────────┘
```

---

## 1. Daily Budget Monitor

### What It Does

- **Runs:** Every day at 9:00 AM
- **Checks:** Devonshire campaign spend vs expected pacing
- **Threshold:** ±5% deviation from target
- **Alerts:** Email sent if threshold exceeded

### Alert Levels

| Deviation | Level | Icon | Action |
|-----------|-------|------|--------|
| < 5% | ✅ On Pace | ✅ | No alert |
| 5-10% | ⚠️ Warning | ⚠️ | Email alert, monitor |
| > 10% | 🚨 Critical | 🚨 | Email alert, immediate action |

### Email Alert Example

**Subject:** 🚨 Budget Alert: Devonshire Hotels OVERPACING - Nov 15

**Content:**
- Days elapsed / remaining
- Expected vs actual spend
- Deviation amount and percentage
- Main Properties vs The Hide breakdown
- Recommendations based on deviation

### Files

- **Script:** `shared/scripts/daily-budget-monitor.py`
- **LaunchAgent:** `shared/scripts/com.petesbrain.budget-monitor.plist`
- **Log:** `~/.petesbrain-budget-monitor.log`

---

## 2. Weekly Budget Status

### What It Does

- **Runs:** Every Monday at 9:00 AM (part of weekly review)
- **Shows:** Budget status for all monitored clients
- **Included:** In weekly review email with meetings/tasks

### Display Format

**Budget Status Section:**
- Client name with status icon (✅⚠️🚨)
- Monthly budget and remaining budget
- Expected vs actual spend
- Deviation amount and percentage
- Days remaining
- Link to budget tracker spreadsheet

### Files

- **Script:** `shared/scripts/weekly-meeting-review.py`
- **Modified:** Added `get_budget_status()` function
- **HTML:** New budget section in email template

---

## Installation & Setup

### Step 1: Install Daily Budget Monitor

```bash
cd /Users/administrator/Documents/PetesBrain

# Copy LaunchAgent plist to LaunchAgents directory
cp shared/scripts/com.petesbrain.budget-monitor.plist \
   ~/Library/LaunchAgents/

# Load the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.petesbrain.budget-monitor.plist

# Verify it's running
launchctl list | grep petesbrain.budget-monitor
```

### Step 2: Test Daily Monitor

```bash
# Test run (dry run, no email sent)
GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
  shared/email-sync/.venv/bin/python3 shared/scripts/daily-budget-monitor.py
```

**Expected output:**
```
================================================================================
📊 Daily Budget Monitor
================================================================================

📅 Date: November 15, 2025
   Days elapsed: 15/30
   Days remaining: 15

🏨 Monitoring: Devonshire Hotels
   Monthly budget: £11,000.00
   Expected spend to date: £5,500.00 (50.0%)

🔍 Fetching current spend from Google Ads...
   ⚠️  NOTE: This requires Google Ads MCP to be called
   For testing, using placeholder data

   ⚠️  No spend data available (using placeholder)
   To get real data, this script needs to call Google Ads MCP

💡 Skipping alert for now - will work once integrated with MCP
```

### Step 3: Weekly Review Already Updated

The weekly review script is already updated and will automatically include budget status when:
- It's November 2025
- After November 3rd (implementation date)
- Budget data is available

No additional setup needed.

---

## Integration with Google Ads MCP

### Current State

Both scripts have **placeholder data** because they can't directly access Google Ads MCP tools.

### Two Options for Real Data

#### Option A: Run via Claude Code (Recommended)

When you need to check budget status:
1. Ask Claude Code: "Check Devonshire budget status"
2. Claude Code will:
   - Query Google Ads MCP for current spend
   - Run the monitoring logic
   - Send email if needed

**Pros:** Simple, uses existing MCP access
**Cons:** Not fully automated (requires Claude Code session)

#### Option B: Standalone MCP Client (Future)

Create a standalone Python client that can call MCP tools directly.

**Pros:** Fully automated
**Cons:** Requires ~2 hours to implement MCP client

---

## Usage

### Check Budget Manually (via Claude Code)

```
You: "Check Devonshire budget status for today"
```

Claude Code will:
1. Query Google Ads for current MTD spend
2. Calculate expected spend
3. Check deviation
4. Send alert email if needed
5. Report status

### View Logs

```bash
# Daily monitor log
tail -f ~/.petesbrain-budget-monitor.log

# Weekly review log
# (Included in weekly review output)
```

### Modify Threshold

Edit `shared/scripts/daily-budget-monitor.py`:

```python
# Line ~650
threshold = 5.0  # Change to desired percentage (e.g., 3.0 for 3%)
```

### Add New Client Monitoring

1. **Edit `daily-budget-monitor.py`:**
   - Add new client budget data in `main()`
   - Add to monitoring loop

2. **Edit `weekly-meeting-review.py`:**
   - Update `get_budget_status()` function
   - Add client check with budget amounts

Example:
```python
def get_budget_status():
    # Existing Devonshire check...

    # Add new client
    if today.month == 12 and today.year == 2025:  # December
        # Smythson monitoring
        result.append({
            'client': 'Smythson',
            'monthly_budget': 120000.0,
            # ... rest of data
        })

    return result
```

---

## Monitoring Schedule

| Time | Day | Action | Script |
|------|-----|--------|--------|
| 9:00 AM | Daily | Check budget, send alert if needed | `daily-budget-monitor.py` |
| 9:00 AM | Monday | Weekly review with budget status | `weekly-meeting-review.py` |

---

## Troubleshooting

### LaunchAgent Not Running

```bash
# Check status
launchctl list | grep budget-monitor

# Reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.budget-monitor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.budget-monitor.plist
```

### No Email Alerts Sent

1. **Check Gmail token:**
   ```bash
   ls -la shared/email-sync/token.json
   ```

2. **Test Gmail auth:**
   ```bash
   shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
   ```

3. **Check threshold:** Alert only sent if deviation > 5%

### No Budget Data in Weekly Email

- Budget status only shows if:
  - Current month is November 2025
  - Date is >= November 3rd
  - Actual spend data > 0 (requires MCP integration)

### Wrong Budget Amounts

Edit the budget constants in both scripts:

**`daily-budget-monitor.py` (line ~640):**
```python
monthly_budget = 11000.0
main_budget = 9000.0
hide_budget = 2000.0
```

**`weekly-meeting-review.py` (line ~207):**
```python
monthly_budget = 11000.0
```

---

## Configuration Files

### Daily Monitor LaunchAgent

**File:** `~/Library/LaunchAgents/com.petesbrain.budget-monitor.plist`

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>  <!-- Change run time here -->
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

### Email Recipients

**Daily alerts:**
```python
# daily-budget-monitor.py line ~680
send_email(gmail_service, 'petere@roksys.co.uk', subject, html_content)
```

**Weekly review:**
```python
# weekly-meeting-review.py line ~730
message = create_message(
    to='petere@roksys.co.uk',
    ...
)
```

---

## Example Alert Scenarios

### Scenario 1: Overpacing (Day 15 of 30)

**Expected:** £5,500 (50% of £11,000)
**Actual:** £6,200
**Deviation:** +£700 (+12.7%)
**Alert Level:** 🚨 Critical
**Recommendation:** Reduce daily budgets by 15%, review high spenders

### Scenario 2: Underpacing (Day 20 of 30)

**Expected:** £7,333 (66.7% of £11,000)
**Actual:** £6,800
**Deviation:** -£533 (-7.3%)
**Alert Level:** ⚠️ Warning
**Recommendation:** Increase budgets by 10% or lower ROAS targets

### Scenario 3: On Pace (Day 10 of 30)

**Expected:** £3,667 (33.3% of £11,000)
**Actual:** £3,550
**Deviation:** -£117 (-3.2%)
**Alert Level:** ✅ On Pace
**Action:** No alert sent (< 5% threshold)

---

## Future Enhancements

### Phase 1 (Current)
- ✅ Daily monitoring script
- ✅ Weekly budget status in review email
- ✅ LaunchAgent automation
- ⏳ MCP integration (requires Claude Code)

### Phase 2 (Future)
- ⬜ Standalone MCP client for full automation
- ⬜ Multi-client monitoring (Smythson, Tree2mydoor, etc.)
- ⬜ Budget forecast predictions
- ⬜ Automatic budget adjustment suggestions
- ⬜ Dashboard view (web interface)

---

## Related Documentation

- **Budget tracker spreadsheet:** [Link](https://docs.google.com/spreadsheets/d/1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc/)
- **November budget changes:** `clients/devonshire-hotels/documents/november-2025-budget-changes.md`
- **Weekly review automation:** Already documented in CLAUDE.md
- **Google Ads MCP:** `.mcp.json` configuration

---

## Questions?

**Contact:** Peter Empson - petere@roksys.co.uk
**Created:** 2025-10-30
**Last Updated:** 2025-10-30
