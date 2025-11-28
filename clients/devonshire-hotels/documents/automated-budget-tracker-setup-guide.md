# Devonshire Hotels - Automated Budget Tracker Setup Guide

**Created:** 2025-10-30
**Purpose:** Set up Google Sheets budget tracker with automatic data from Google Ads MCP

## Overview

This guide explains how to set up an automated budget tracking spreadsheet that pulls live data from Google Ads using the Google Ads MCP server, eliminating the need for manual data entry except for budget amounts and notes.

## Spreadsheet Structure

### Two Tracking Sheets Required

1. **Dev Properties Budget** - All main hotel properties and self-catering (excluding The Hide)
2. **The Hide Budget** - Separate £2,000/month budget tracking

### Account Details

- **Google Ads Account ID:** 5898250490
- **Account Name:** Devonshire Group

## Campaigns to Track

### Dev Properties (Excluding The Hide)

All active campaigns with "DEV | Properties" in the name, **excluding**:
- The Hide (campaign ID: 23069490466)
- The Highwayman (paused - was renamed to The Hide)

**Active campaigns as of Oct 30, 2025:**

| Campaign Name | Campaign ID | Type |
|--------------|-------------|------|
| DEV \| Properties \| P Max \| All | 18899261254 | Performance Max |
| DEV \| Properties CE \| Cavendish | 21839323410 | Search |
| DEV \| Properties BE \| Devonshire Arms Hotel | 19577006833 | Search |
| DEV \| Properties CE \| The Beeley Inn | 22539873565 | Search |
| DEV \| Properties CE \| Chatsworth Escapes Inns & Hotels | 2080736142 | Search |
| DEV \| Properties CE \| Chatsworth Escapes Self Catering | 19534201089 | Search |
| DEV \| Properties CE \| The Pilsley Inn | 19534106385 | Search |
| DEV \| Properties BE \| The Fell | 22666031909 | Search |
| DEV \| Properties \| Chatsworth Escapes Locations | 19654308682 | Search |
| DEV \| Properties BE \| Bolton Abbey Escapes Locations | 22720114456 | Search |
| DEV \| Properties BE \| Bolton Abbey Escapes Self Catering | 22536922700 | Search |
| DEV \| Properties \| Devonshire Derbyshire Hotels | 20321507430 | Search |
| DEV \| Properties \| Devonshire Pet Friendly Yorkshire Hotels | 20330953375 | Search |

### The Hide Campaign

| Campaign Name | Campaign ID | Budget |
|--------------|-------------|--------|
| DEV \| Properties \| The Hide | 23069490466 | £2,000/month |

**Note:** The Hide launched on October 10, 2025 (formerly The Highwayman)

## How to Update the Spreadsheet

### On-Demand Updates (Recommended)

Simply ask Claude Code in chat:

```
Update the Devonshire budget tracker
```

Claude Code will:
1. Fetch latest spend data from Google Ads MCP
2. Calculate current month metrics (pacing, remaining budget, etc.)
3. Update both sheets in your budget spreadsheet
4. Provide a summary of key metrics

### What Gets Updated Automatically

- **MTD Spend** - Month-to-date spend from Google Ads
- **Yesterday Spend** - Previous day's spend
- **Days Elapsed** - Current day of month
- **Days Remaining** - Days left in month
- **Expected Spend** - Prorated budget based on days elapsed
- **Remaining Budget** - Budget minus actual spend
- **Required Daily Budget** - What needs to be spent daily to hit budget
- **Pacing %** - Actual spend vs expected spend percentage
- **Predicted Spend** - Projected month-end spend at current pace
- **Last Updated** - Timestamp of data refresh

### What You Update Manually

- **Budget** (Column C) - Enter the planned monthly budget
- **Notes** (Column N) - Add any relevant notes or context

## Sample Current Data (October 2025)

### Dev Properties (Excluding The Hide)

- **Budget:** £9,730.00 (manual entry)
- **MTD Spend:** £10,265.94 (from Google Ads)
- **Yesterday Spend:** £314.19 (from Google Ads)
- **Pacing:** 109.14% (calculated)
- **Days Elapsed:** 30 of 31

**Top Spending Campaigns:**
1. P Max All: £2,392.56
2. Cavendish: £1,239.77
3. Devonshire Arms Hotel: £1,196.58

### The Hide

- **Budget:** £2,000.00 (manual entry)
- **MTD Spend:** £1,378.67 (from Google Ads)
- **Yesterday Spend:** £49.01 (from Google Ads)
- **Pacing:** 71.23% (calculated)
- **Note:** Only active since Oct 10 (launch date)

### Combined Totals

- **Combined Budget:** £11,730.00
- **Combined Spend:** £11,644.61
- **Combined Pacing:** 105.74%

## Automation Options

### Option 1: Daily Scheduled Update (Future Enhancement)

A LaunchAgent could be configured to run daily at 9 AM:

```bash
~/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist
```

This would automatically update the spreadsheet every morning.

### Option 2: Weekly Summary Email

Include budget snapshot in the weekly meeting review email showing:
- Current month pacing for both budgets
- Week-over-week spend trends
- Alerts if pacing exceeds thresholds (e.g., >110% or <90%)

## GAQL Queries Used

### Get Month-to-Date Spend by Campaign

```sql
SELECT
  campaign.id,
  campaign.name,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND campaign.name LIKE '%DEV | Properties%'
  AND segments.date DURING THIS_MONTH
```

### Get Yesterday's Spend by Campaign

```sql
SELECT
  campaign.name,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND campaign.name LIKE '%DEV | Properties%'
  AND segments.date = 'YYYY-MM-DD'
```

**Note:** cost_micros must be divided by 1,000,000 to get GBP amount

## Formulas for Calculated Fields

### Expected Spend
```
= (Budget / Total Days) * Days Elapsed
```

### Remaining Budget
```
= Budget - Actual Spend
```

### Required Daily Budget
```
= Remaining Budget / Days Remaining
```

### Pacing Percentage
```
= (Actual Spend / Expected Spend) * 100
```

### Predicted Spend
```
= (Actual Spend / Days Elapsed) * Total Days
```

## Benefits of Automation

✅ **No manual data entry** - Spend data pulled directly from Google Ads
✅ **Real-time accuracy** - Always shows current data
✅ **Automatic calculations** - Pacing, predictions, and budgets calculated instantly
✅ **Historical tracking** - Keep monthly records without manual logging
✅ **Separate visibility** - Track The Hide independently from main properties
✅ **On-demand updates** - Refresh anytime by asking Claude Code

## Maintenance

### When Campaigns Change

If new campaigns are added or removed:
1. Update the campaign list in this document
2. Ask Claude Code to refresh the campaign list in the spreadsheet
3. Verify new campaigns appear in the breakdown section

### When Budget Changes

Simply update the Budget column (Column C) in the spreadsheet - all calculations will automatically adjust.

### Monthly Rollover

At the start of each new month:
1. Ask Claude Code to update the spreadsheet
2. New month's row will populate with current spend
3. Previous month's data remains as historical record

## Troubleshooting

### Data Not Updating

1. Check Google Ads MCP connection: `mcp__google-ads__list_accounts`
2. Verify account ID is correct: 5898250490
3. Check if campaigns have been renamed or paused

### Pacing Seems Wrong

- Verify the Budget column has the correct monthly amount
- Check if any mid-month budget changes occurred
- Ensure days elapsed calculation is correct

### Missing Campaigns

- Confirm campaign is ENABLED in Google Ads
- Check campaign name contains "DEV | Properties"
- Verify campaign wasn't recently paused or removed

## Contact

For questions or issues:
- **Account Manager:** Peter Empson - petere@roksys.co.uk
- **Technical Support:** Claude Code in PetesBrain workspace

---

**Last Updated:** 2025-10-30
**Spreadsheet ID:** 1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc (original tracker)
