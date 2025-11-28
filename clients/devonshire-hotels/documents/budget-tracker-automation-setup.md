# Devonshire Budget Tracker Automation - Setup Complete

**Date:** 2025-10-31
**Status:** ✅ Active & Running

---

## What Was Set Up

The Devonshire budget tracker now has **three levels of automation**:

### 1. ✅ On-Demand Updates (Already Working)
**Status:** Active since Oct 30, 2025
**Usage:** Ask Claude Code "Update Devonshire budget tracker"

### 2. ✅ Daily Automated Updates (NEW - Oct 31, 2025)
**Status:** Active, runs daily at 9:00 AM
**Script:** `clients/devonshire-hotels/scripts/update_budget_tracker.py`
**LaunchAgent:** `~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist`
**Log File:** `~/.petesbrain-devonshire-budget.log`

**What it does:**
- Fetches current month spend from Google Ads API (all campaigns)
- Fetches yesterday's spend
- Separates Dev Properties from The Hide campaign
- Calculates pacing metrics (expected spend, remaining budget, etc.)
- Updates both automated sheets in Google Sheets
- Logs results and alerts if pacing is significantly off (>110% or <90%)

### 3. ✅ Weekly Summary Email (NEW - Oct 31, 2025)
**Status:** Active, included in Monday 9 AM weekly review email
**Integration:** `shared/scripts/weekly-meeting-review.py`

**What it includes:**
- Current month budget vs actual spend
- Pacing percentage
- Days remaining
- Budget status (on-pace, warning, or critical)
- Link to budget tracker spreadsheet

---

## How It Works

### Data Flow

```
Google Ads Account (5898250490)
         ↓
Daily Script (9:00 AM)
         ↓
Google Sheets Budget Tracker
         ↓
Weekly Email (Mondays 9:00 AM)
         ↓
Your Inbox (petere@roksys.co.uk)
```

### Budget Tracking Sheets

**Spreadsheet ID:** `1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc`

**Two Automated Sheets:**
1. **"Dev Properties Auto"** - Main campaigns (excludes The Hide)
2. **"The Hide Properties Auto"** - The Hide campaign only

**Updated Fields (columns E-M):**
- Days Elapsed
- Days Remaining
- Spend (MTD)
- Expected Spend
- Remaining Budget
- Required Daily Budget
- Pacing %
- Predicted Spend
- Yesterday Spend

**Manual Fields (you control):**
- Column C: Monthly Budget (update at start of each month)
- Column N: Notes

---

## Monthly Budgets (Pre-Configured)

The script already has budgets defined through March 2026:

| Month | Dev Properties | The Hide | Total |
|-------|---------------|----------|-------|
| Oct 2025 | £11,730 | £2,000 | £13,730 |
| Nov 2025 | £9,000 | £2,000 | £11,000 |
| Dec 2025 | £7,750 | £2,000 | £9,750 |
| Jan 2026 | £6,750 | £2,000 | £8,750 |
| Feb 2026 | £6,500 | £2,000 | £8,500 |
| Mar 2026 | £8,000 | £2,000 | £10,000 |

**To update for future months:**
Edit `clients/devonshire-hotels/scripts/update_budget_tracker.py` and add entries to the `MONTHLY_BUDGETS` dictionary.

---

## Checking Status

### View Daily Update Logs
```bash
cat ~/.petesbrain-devonshire-budget.log
```

### Check LaunchAgent Status
```bash
launchctl list | grep devonshire
```

### Manual Run (for testing)
```bash
python3 /Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/scripts/update_budget_tracker.py
```

### View Current Data
Open the spreadsheet: https://docs.google.com/spreadsheets/d/1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc/

---

## How to Use

### Start of Each Month
1. **Update budgets** in the script (if needed for future months)
2. **Manually enter budget** in Column C of both sheets
3. Script will auto-populate all other columns from day 1

### During the Month
- **Daily:** Script runs automatically at 9 AM, updates sheets
- **Monday:** Receive weekly email with budget status
- **Anytime:** Ask Claude Code for current status

### End of Month
- Review final spend vs budget
- Check variance
- Note any underspend/overspend for next month

---

## Alert Thresholds

The system alerts when pacing is off-target:

| Status | Pacing % | Meaning |
|--------|----------|---------|
| ✅ On-Pace | 90-110% | Spending as expected |
| ⚠️ Warning | 85-90% or 110-115% | Slightly off-pace |
| 🚨 Critical | <85% or >115% | Significantly off-pace |

---

## Troubleshooting

### Script Not Running
```bash
# Check if LaunchAgent is loaded
launchctl list | grep devonshire

# If not loaded, reload it
launchctl unload ~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist
```

### Google Ads Connection Issues
- Requires OAuth token from Google Ads MCP server
- Token stored in: `shared/mcp-servers/google-ads-mcp-server/`
- If expired, MCP will trigger re-auth flow

### Google Sheets Connection Issues
- Requires service account credentials
- Path: `shared/mcp-servers/google-sheets-mcp-server/credentials.json`
- Check LaunchAgent has correct `GOOGLE_APPLICATION_CREDENTIALS` path

### "No budget defined for [month]" Error
- Add the month to `MONTHLY_BUDGETS` in the script
- Format: `"YYYY-MM": {"dev": X, "hide": Y}`

---

## Files Created/Modified

### New Files
- ✅ `clients/devonshire-hotels/scripts/update_budget_tracker.py` - Daily update script
- ✅ `~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist` - LaunchAgent config
- ✅ `clients/devonshire-hotels/documents/budget-tracker-automation-setup.md` - This file

### Modified Files
- ✅ `shared/scripts/weekly-meeting-review.py` - Added `get_devonshire_budget_status()` function

### Google Sheets
- ✅ Updated "Dev Properties Auto" sheet with Oct 31 data
- ✅ Updated "The Hide Properties Auto" sheet with Oct 31 data

---

## Next Steps

### For November 1, 2025
1. Script will automatically start tracking November spend
2. Manually update Column C (Budget) in both sheets to November budgets:
   - Dev Properties Auto: £9,000
   - The Hide Properties Auto: £2,000
3. Add row 7 for November in "Dev Properties Auto" sheet
4. Add row 8 for November in "The Hide Properties Auto" sheet

### Future Enhancements (Optional)
- 📧 **Budget alerts via email** - Send email when >110% or <90% pacing
- 📊 **Visualizations** - Add charts to sheets
- 🤖 **Auto-adjust daily budgets** - Recommend budget changes in Google Ads
- 📈 **Trend analysis** - Week-over-week spending patterns
- 🔮 **Forecasting** - Predict end-of-month spend with confidence intervals

---

## Support

**For budget questions:**
Peter Empson - petere@roksys.co.uk

**For technical issues:**
Ask Claude Code in PetesBrain workspace

**Documentation:**
- Setup guide: `clients/devonshire-hotels/documents/automated-budget-tracker-setup-guide.md`
- Workflow: `clients/devonshire-hotels/documents/budget-tracker-workflow.md`
- This file: `clients/devonshire-hotels/documents/budget-tracker-automation-setup.md`

---

**Last Updated:** 2025-10-31
**Setup By:** Claude Code
**Status:** ✅ Fully Operational
