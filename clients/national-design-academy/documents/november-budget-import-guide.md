# National Design Academy - November Budget Import Guide

**Date Created**: November 5, 2025
**Source File**: `scripts/august_budget_plan_no_pauses.csv`
**Output Files**:
- `spreadsheets/nda_november_budgets_for_google_ads_editor.csv` (new budgets)
- `spreadsheets/nda_october_current_budgets_rollback.csv` (rollback/current budgets)

## Summary

This CSV file converts the monthly budgets from the August baseline plan into **daily budgets** for import into Google Ads Editor.

**Conversion Method**: Monthly budget ÷ 30.44 (average days per month) = Daily budget

## Budget Overview

- **Total Monthly Budget**: £24,201.93
- **Total Daily Budget**: £795.07
- **Number of Campaigns**: 33 (6 UAE campaigns excluded)

**Important Changes**:
- **KEEP campaigns**: Maintain their **current Google Ads budgets** (not August baseline)
- **UAE campaigns**: Removed from this budget import (6 campaigns totaling £62.26/day, £1,895/month)

## Import Instructions for Google Ads Editor

1. **Download the CSV file**:
   - Location: `clients/national-design-academy/spreadsheets/nda_november_budgets_for_google_ads_editor.csv`

2. **Open Google Ads Editor**:
   - Ensure you've downloaded the latest account data
   - Navigate to the NDA account

3. **Import the CSV**:
   - Click **"Import"** → **"Import from file"**
   - Select the CSV file
   - Choose **"Replace existing items"** option
   - Map columns:
     - **Campaign** → Campaign name
     - **Budget** → Daily budget (£)

4. **Review Changes**:
   - Check the changes in Google Ads Editor
   - Verify budget amounts match expectations
   - Review any warnings or errors

5. **Post Changes**:
   - Once satisfied, click **"Post"** to push changes to Google Ads

## Budget Actions Breakdown

| Action | Campaigns | Current Monthly | New Monthly | Daily Budget Range |
|--------|-----------|-----------------|-------------|-------------------|
| **REDUCE_95** | 10 | £3,623.15 | £181.16 | £0.00 - £1.23 |
| **REDUCE_90** | 3 | £1,441.80 | £144.18 | £1.11 - £2.23 |
| **REDUCE_80** | 8 | £6,834.72 | £1,366.94 | £2.02 - £17.57 |
| **REDUCE_50** | 6 | £7,796.05 | £3,898.03 | £6.73 - £42.64 |
| **KEEP** | 12 | ~£18,600 | ~£18,600 | £16.69 - £300.00 |

**Note**: KEEP campaigns use their current Google Ads budgets, not calculated from October spend. This ensures no disruption to top performers.

## Top 5 Budget Campaigns (Daily Spend)

1. **NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8** - £300.00/day (KEEP - unchanged)
2. **NDA | UK | Search | Brand 100 New Customer 1/8 No Target** - £110.00/day (KEEP - unchanged)
3. **NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target** - £50.00/day (KEEP - unchanged)
4. **NDA | Search | Interior Design Degree- UK 120 No Target 24/4** - £42.64/day (REDUCE_50 - was £100/day)
5. **NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9** - £40.00/day (KEEP - unchanged)

## Campaigns with Minimal Budgets (<£1/day)

The following 10 campaigns now have very minimal test budgets (£0.00 - £1.23/day):

- NDA | P Max Reboot | Interior Design Diploma - MENA (£1.23/day)
- NDA | Search | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 (£1.19/day)
- NDA | IN | Search | Interior Design Degree No Target (£0.86/day)
- NDA | Search | Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135 (£0.84/day)
- NDA | P Max | Interior Design Degree - USA/Canada 250 Split (£0.56/day)
- NDA | AT/FR/NL/MA/DE/SW | Search | Landscape Design Diplomas No Target (£0.55/day)
- NDA | Low Intl | Search | Retail Design Degree No Target (£0.47/day)
- NDA | AT/FR/NL/MA/DE/SW | Search | Interior Design Diploma 250 (£0.22/day)
- NDA | Low Intl | Search | Curtain Making Course No Target (£0.02/day)
- NDA | EUR | Search | Landscape Design Courses 65 (£0.00/day)

**Note**: These campaigns had zero conversions YTD and are set to minimal test budgets as per the "Return to August Levels" strategy.

## Excluded UAE Campaigns

The following 6 UAE campaigns are **NOT included** in this budget import CSV and will remain at their current budgets:

1. NDA | UAE | Search | Interior Design Diploma No Target (current: £90/day, planned was: £17.57/day)
2. NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5 (current: £20/day)
3. NDA | UAE | Search | Interior Design Degree No Target (current: £50/day, planned was: £8.54/day)
4. NDA | Search | Brand - UAE No Target 7/7 (current: £15/day, planned was: £7.20/day)
5. NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4 (current: £10/day, planned was: £6.73/day)
6. NDA | OM/SA/UAE | Search | Landscape Design No Target (current: £10/day, planned was: £2.22/day)

**Total UAE budgets excluded**: £195/day (£5,936/month at current levels)

**Note**: If you want to adjust UAE campaign budgets separately, you'll need to do that manually in Google Ads Editor or the UI.

## Expected Impact

- **Monthly Spend**: Reduced from £39,996.40 to £24,201.93 (-40%)
- **Monthly Savings**: £15,794.47
- **Strategy**:
  - KEEP campaigns (11): Maintain current Google Ads budgets (no change)
  - REDUCE campaigns (22): Return to August 2025 baseline levels
  - UAE campaigns (6): Excluded from this import (£1,895/month removed)
  - All remaining campaigns active (no pauses)

## Monitoring Recommendations

1. **Week 1**: Monitor for disapprovals or budget-limited campaigns
2. **Week 2**: Check CPA changes on reduced-budget campaigns
3. **Week 3-4**: Assess overall account performance vs. August baseline
4. **Monthly**: Review conversion volume and efficiency at new budget levels

## Rollback Instructions (If Needed)

If you need to revert to the current configured budgets:

1. **Use the rollback file**: `spreadsheets/nda_october_current_budgets_rollback.csv`
2. **Import process** (same as above):
   - Google Ads Editor → Import → Import from file
   - Select the rollback CSV file
   - Map columns and post changes
3. **Current configured budgets** (pulled from Google Ads API):
   - Total daily: £1,042.00
   - Total monthly: ~£31,718 (estimated at 30.44 days/month)
   - **Source**: Actual campaign_budget.amount_micros from Google Ads (as of Nov 5, 2025)

**Top 5 Current Configured Daily Budgets**:
1. NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8 - £300.00/day
2. NDA | UK | Search | Brand 100 New Customer 1/8 No Target - £110.00/day
3. NDA | Search | Interior Design Degree- UK 120 No Target 24/4 - £100.00/day
4. NDA | UAE | Search | Interior Design Diploma No Target - £90.00/day
5. NDA | UAE | Search | Interior Design Degree No Target - £50.00/day

**Note**: These are the **actual configured daily budgets** in Google Ads, not calculated from spend. This ensures an exact rollback if needed.

## Related Documents

- **Budget Plan Source**: `clients/national-design-academy/scripts/august_budget_plan_no_pauses.csv`
- **Alternative Plan** (with pauses): `clients/national-design-academy/scripts/nda_budget_plan.csv`
- **Original Analysis**: `clients/national-design-academy/documents/budget-reduction-recommendations-2025-11-03.md`
