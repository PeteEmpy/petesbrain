# Devonshire Hotels - Budget Snapshot

**Date:** 2025-10-30
**Period:** October 2025 (Day 30 of 31)
**Account:** Devonshire Group (5898250490)

---

## Summary

### Dev Properties Budget (Excluding The Hide)

| Metric | Value | Status |
|--------|-------|--------|
| **Monthly Budget** | £9,730.00 | Manual entry |
| **MTD Spend** | £10,265.94 | From Google Ads |
| **Expected Spend** | £9,406.45 | Calculated (30/31 days) |
| **Remaining Budget** | -£535.94 | **⚠️ OVER BUDGET** |
| **Pacing Percentage** | 109.14% | ⚠️ Running 9.14% over |
| **Predicted Month-End** | £10,607.95 | Based on current pace |
| **Yesterday's Spend** | £314.19 | Oct 29 |
| **Req. Daily Budget** | £0.00 | Only 1 day remaining |

**Analysis:** Running £535.94 over the allocated budget for Dev Properties (excluding The Hide). With only 1 day remaining, predicted to finish at £10,607.95 (£877.95 over budget).

### The Hide Budget

| Metric | Value | Status |
|--------|-------|--------|
| **Monthly Budget** | £2,000.00 | Manual entry |
| **MTD Spend** | £1,378.67 | From Google Ads |
| **Expected Spend** | £1,935.48 | Calculated (30/31 days) |
| **Remaining Budget** | £621.33 | ✅ Under budget |
| **Pacing Percentage** | 71.23% | Running 28.77% under |
| **Predicted Month-End** | £1,424.64 | Based on current pace |
| **Yesterday's Spend** | £49.01 | Oct 29 |
| **Req. Daily Budget** | £621.33 | To hit full budget |

**Analysis:** Running £621.33 under budget. Only active since Oct 10 (launch date), so lower spend is expected. Predicted to finish at £1,424.64 (£575.36 under budget).

**Note:** The Hide campaign was launched mid-month (Oct 10), explaining the lower-than-expected pacing.

### Combined Totals (All DEV | Properties)

| Metric | Value |
|--------|-------|
| **Combined Budget** | £11,730.00 |
| **Combined Spend** | £11,644.61 |
| **Combined Remaining** | £85.39 |
| **Combined Pacing** | 105.74% |

**Overall Status:** Slightly over-pacing by 5.74%, but within combined budget. Dev Properties over-spending is partially offset by The Hide under-spend.

---

## Campaign-Level Detail (October 2025)

### Dev Properties Campaigns (13 active)

| Campaign Name | Campaign ID | Type | MTD Spend | Yesterday | % of Total |
|--------------|-------------|------|-----------|-----------|------------|
| **P Max \| All** | 18899261254 | PMax | £2,392.56 | £99.42 | 23.3% |
| **Cavendish** | 21839323410 | Search | £1,239.77 | £27.30 | 12.1% |
| **Devonshire Arms Hotel** | 19577006833 | Search | £1,196.58 | £43.72 | 11.7% |
| **The Beeley Inn** | 22539873565 | Search | £975.45 | £28.34 | 9.5% |
| **Chatsworth Escapes Inns & Hotels** | 2080736142 | Search | £879.26 | £16.99 | 8.6% |
| **Chatsworth Escapes Self Catering** | 19534201089 | Search | £861.04 | £17.67 | 8.4% |
| **The Pilsley Inn** | 19534106385 | Search | £859.01 | £25.45 | 8.4% |
| **The Fell** | 22666031909 | Search | £722.99 | £23.18 | 7.0% |
| **Chatsworth Escapes Locations** | 19654308682 | Search | £488.57 | £15.44 | 4.8% |
| **Bolton Abbey Escapes Locations** | 22720114456 | Search | £482.69 | £5.77 | 4.7% |
| **Bolton Abbey Escapes Self Catering** | 22536922700 | Search | £168.02 | £10.91 | 1.6% |
| **Devonshire Derbyshire Hotels** | 20321507430 | Search | £0.00 | £0.00 | 0.0% |
| **Devonshire Pet Friendly Yorkshire Hotels** | 20330953375 | Search | £0.00 | £0.00 | 0.0% |
| **TOTAL** | | | **£10,265.94** | **£314.19** | **100%** |

**Top 3 Spenders:**
1. P Max All: 23.3% of budget (£2,392.56)
2. Cavendish: 12.1% of budget (£1,239.77)
3. Devonshire Arms Hotel: 11.7% of budget (£1,196.58)

**Inactive Campaigns:** 2 campaigns with £0 spend (Devonshire Derbyshire Hotels, Pet Friendly Yorkshire Hotels)

### The Hide Campaign

| Campaign Name | Campaign ID | Type | MTD Spend | Yesterday | Status |
|--------------|-------------|------|-----------|-----------|--------|
| **The Hide** | 23069490466 | Search | £1,378.67 | £49.01 | Launched Oct 10 |

**Average Daily Spend:** £68.93 (since Oct 10 launch = 20 days active)

---

## Historical Context

### October 2025 Budget Notes

From CONTEXT.md:
- Extra £2K allocated mid-month
- £1K added to monthly budget
- £350 underspend carried forward
- Extra £80/day from Oct 20 = £880
- Portfolio bid strategy increased from 550 to 570 ROAS target on Oct 24 to slow spend

**Current situation aligns with these notes:**
- Main properties slightly over-pacing due to extra budget allocated
- ROAS increase on Oct 24 likely slowed down end-of-month spend
- The Hide under-pacing is expected (mid-month launch)

---

## Recommendations

### For Remaining Day (Oct 31)

**Dev Properties:**
- Currently at £10,265.94 with 1 day remaining
- Expected final spend: ~£10,608
- Already £535.94 over allocated budget
- **Action:** Monitor closely; consider reducing bids if spend accelerates

**The Hide:**
- Currently at £1,378.67 with £621.33 remaining budget
- Expected final spend: ~£1,425
- **Action:** Could increase spend if desired, but new campaign may benefit from gradual ramp

### For November 2025

**Planned Budgets:**
- Dev Properties: £9,000.00
- The Hide: £2,000.00
- Combined: £11,000.00

**Considerations:**
- November budget is £1,730 less than October
- Will need to adjust campaign budgets/bids accordingly
- The Hide will have full month of data

---

## Data Sources

- **Google Ads Account:** 5898250490 (Devonshire Group)
- **Data Pull Date:** 2025-10-30
- **MTD Spend:** Through end of Oct 29, 2025
- **Method:** Google Ads MCP GAQL queries

### GAQL Queries Used

```sql
-- MTD Spend by Campaign
SELECT campaign.id, campaign.name, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND campaign.name LIKE '%DEV | Properties%'
  AND segments.date DURING THIS_MONTH

-- Yesterday's Spend
SELECT campaign.name, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND campaign.name LIKE '%DEV | Properties%'
  AND segments.date = '2025-10-29'
```

---

## How to Update This Data

Simply ask Claude Code:

```
Update the Devonshire budget snapshot
```

Claude Code will:
1. Query Google Ads MCP for latest spend data
2. Calculate current metrics
3. Generate updated snapshot
4. Update Google Sheets if configured

---

**Next Update:** On demand or Nov 1 for month rollover
**Maintained By:** Claude Code via Google Ads MCP
**Contact:** Peter Empson - petere@roksys.co.uk
