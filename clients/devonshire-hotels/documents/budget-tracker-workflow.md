# Devonshire Budget Tracker - Automated Workflow

**Created:** 2025-10-30
**Purpose:** How to update budget tracking using Claude Code and Google Ads MCP

---

## Quick Start

### To Update Budget Data

Simply say to Claude Code:

```
Update Devonshire budget tracker
```

Or more specifically:

```
Get current month spend for Devonshire campaigns
```

```
Show me The Hide campaign performance
```

Claude Code will fetch live data from Google Ads and provide:
- Current month-to-date spend
- Yesterday's spend
- Campaign-level breakdown
- Pacing calculations
- Budget recommendations

---

## What You Get

### Automated Data (From Google Ads MCP)

✅ **Real-time spend data** - Always current
✅ **Campaign breakdowns** - Individual campaign performance
✅ **Yesterday's metrics** - Daily spend tracking
✅ **MTD totals** - Month-to-date cumulative spend
✅ **Automatic calculations** - Pacing, predictions, remaining budget

### Manual Inputs (You Control)

📝 **Monthly budgets** - Set budget amounts for each month
📝 **Notes** - Add context about budget changes, strategies, etc.
📝 **Future planning** - Budget allocations for upcoming months

---

## Setup: Create Your Tracking Sheets

### Option 1: Use Existing Spreadsheet (Recommended)

Your current budget tracker: [spreadsheet_id: 1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc]

**Step 1:** Add two new sheets to this workbook:
1. "Dev Properties Auto"
2. "The Hide Auto"

**Step 2:** Copy the template structure from `automated-budget-tracker-setup-guide.md`

**Step 3:** Ask Claude Code to populate the data:
```
Populate the Dev Properties Auto sheet with current data
```

### Option 2: Create New Spreadsheet

**Step 1:** Create a new Google Sheet named "Devonshire Budget Tracker (Automated)"

**Step 2:** Create two sheets:
1. "Dev Properties"
2. "The Hide"

**Step 3:** Set up the column headers (see template below)

**Step 4:** Share the spreadsheet with the service account:
- Email: [your-service-account]@[project-id].iam.gserviceaccount.com
- Permission: Editor

**Step 5:** Give Claude Code the spreadsheet ID and ask to populate

---

## Sheet Templates

### Dev Properties Sheet Structure

```
Row 1: [HEADER] Devonshire Hotels - Dev Properties Budget Tracker
Row 2: Last Updated: [DATE] | Account: 5898250490
Row 3: [BLANK]
Row 4: [COLUMN HEADERS]
       A: Start Date
       B: End Date
       C: Budget (MANUAL)
       D: Total Days
       E: Days Elapsed
       F: Days Remaining
       G: Spend
       H: Expected Spend
       I: Remaining Budget
       J: Req Daily Budget
       K: Pacing %
       L: Predicted Spend
       M: Yesterday Spend
       N: Notes (MANUAL)
Row 5+: Monthly data rows
```

### The Hide Sheet Structure

Same structure as Dev Properties, but tracking only The Hide campaign (£2,000/month budget)

---

## Update Frequency Options

### 1. On-Demand (Recommended for Now)

**Pros:**
- Update whenever you need current data
- No setup required
- Flexible timing

**How:**
Just ask Claude Code in chat

### 2. Daily Automated

**Pros:**
- Always up-to-date
- No manual requests needed
- Morning reports ready

**How:**
Set up LaunchAgent (similar to other automated scripts):

```bash
~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist
```

**Schedule:** Daily at 9:00 AM

**Script:** `clients/devonshire-hotels/spreadsheets/update_budget_tracker.py`

### 3. Weekly Summary

**Pros:**
- Less frequent updates
- Included in weekly meeting review email
- Highlights key changes

**How:**
Integrate with existing weekly review automation

---

## Example Queries

### Get Current Month Status

```
What's the Devonshire budget status for October?
```

**Response will include:**
- MTD spend vs budget
- Pacing percentage
- Days remaining
- Predicted month-end spend
- Separate totals for Dev Properties and The Hide

### Get Campaign Breakdown

```
Show me the top spending Devonshire campaigns this month
```

**Response will include:**
- List of campaigns by spend
- Individual campaign totals
- Percentage of total budget
- Yesterday's spend per campaign

### Get Yesterday's Performance

```
How much did Devonshire spend yesterday?
```

**Response will include:**
- Total spend Oct 29
- Campaign-level breakdown
- Comparison to average daily spend

### Check Pacing

```
Is Devonshire on track for budget this month?
```

**Response will include:**
- Current pacing percentage
- Expected vs actual spend
- Predicted month-end total
- Recommendations for adjustments

---

## Data Sources

### Account Information

- **Google Ads Account ID:** 5898250490
- **Account Name:** Devonshire Group
- **Access Method:** Google Ads MCP

### Campaigns Tracked

#### Dev Properties (13 campaigns)
- All campaigns with "DEV | Properties" in name
- **Excludes:** The Hide, The Highwayman (paused)
- See full list in `automated-budget-tracker-setup-guide.md`

#### The Hide (1 campaign)
- Campaign ID: 23069490466
- Launched: Oct 10, 2025
- Budget: £2,000/month

---

## Calculations Reference

### Expected Spend
```
(Budget / Total Days in Month) × Days Elapsed
```

### Pacing Percentage
```
(Actual Spend / Expected Spend) × 100
```

### Remaining Budget
```
Budget - Actual Spend
```

### Required Daily Budget
```
Remaining Budget / Days Remaining
```

### Predicted Month-End Spend
```
(Actual Spend / Days Elapsed) × Total Days in Month
```

---

## Troubleshooting

### "No data returned"

**Possible causes:**
- Google Ads MCP not connected
- Account ID incorrect
- Date range issue

**Solution:**
```
Check Google Ads connection for Devonshire account
```

### "Campaigns missing"

**Possible causes:**
- Campaign was paused or removed
- Campaign renamed
- Filter criteria changed

**Solution:**
```
List all active Devonshire campaigns
```

### "Spend seems low/high"

**Possible causes:**
- Data freshness (might be 1-2 hours delayed)
- Time zone differences
- Recent budget/bid changes

**Solution:**
```
When was Devonshire data last updated?
```

---

## Monthly Workflow

### Beginning of Month (e.g., Nov 1)

1. **Review previous month:**
   ```
   Generate October budget summary for Devonshire
   ```

2. **Update budget allocations:**
   - Manually enter November budget in spreadsheet
   - Dev Properties: £9,000
   - The Hide: £2,000

3. **Set new month row:**
   Ask Claude Code to initialize November tracking

### Mid-Month Check (e.g., Nov 15)

```
Check Devonshire mid-month pacing
```

Claude Code will alert if significantly off-pace (>110% or <90%)

### End of Month (e.g., Nov 30)

```
Generate end-of-month Devonshire budget report
```

Includes:
- Final spend vs budget
- Variance analysis
- Carry-forward calculations
- Recommendations for next month

---

## Benefits vs. Old Manual Method

| Aspect | Old Method | New Automated Method |
|--------|-----------|---------------------|
| **Data Entry** | Manual copy/paste from Google Ads | Automatic via MCP |
| **Accuracy** | Prone to typos | Always accurate |
| **Freshness** | Updated when you remember | Real-time on demand |
| **Calculations** | Manual formulas | Automatic |
| **Pacing Alerts** | Need to check manually | Proactive alerts |
| **Campaign Detail** | Not included | Full breakdown |
| **Time Required** | 15-30 minutes | 30 seconds |
| **Historical Data** | Sometimes lost | Always preserved |

---

## Future Enhancements

### Coming Soon

🔮 **Automated daily updates** - Wake up to refreshed data
🔮 **Budget alerts** - Email notifications when >110% or <90% pacing
🔮 **Week-over-week trends** - See spending patterns
🔮 **Anomaly detection** - Alert on unusual daily spend
🔮 **Multi-month forecasting** - Predict Q1, Q2 budgets
🔮 **Campaign performance** - Integrate ROAS, conversion data
🔮 **Visualizations** - Charts and graphs in sheets

### Already Available

✅ On-demand updates via Claude Code
✅ Real-time Google Ads integration
✅ Automatic calculations
✅ Campaign-level detail
✅ Separate Hide tracking

---

## Support

### For Budget Questions
**Account Manager:** Peter Empson - petere@roksys.co.uk

### For Technical Issues
**Claude Code:** In PetesBrain workspace
```
Help with Devonshire budget tracker
```

### Documentation
- **Setup Guide:** `automated-budget-tracker-setup-guide.md`
- **Current Snapshot:** `current-budget-snapshot-2025-10-30.md`
- **This Workflow:** `budget-tracker-workflow.md`

---

**Last Updated:** 2025-10-30
**Status:** Ready to use - just ask Claude Code!
**Next Step:** Choose a setup option above and get started
