# Budget Comparison: Current vs November 2025

**Date**: November 5, 2025
**Source**: Google Ads API (actual configured budgets) vs August baseline plan

## Summary

| Metric | Current (API) | November (Planned) | Change |
|--------|---------------|-------------------|--------|
| **Total Daily** | £1,042.00 | £850.50 | -£191.50 (-18%) |
| **Total Monthly** | ~£31,718 | £25,890.97 | -£5,827 (-18%) |
| **Campaigns** | 39 | 39 | 0 |

## Key Differences

### Current Budgets vs October Spend
The **actual configured budgets** (£1,042/day = £31,718/month) are **lower** than the October spend (£39,996.40/month). This suggests:
- Campaigns were frequently spending above their daily budget limits
- Budget-limited campaigns were common in October
- Some campaigns may have had budget increases mid-October that aren't reflected in current settings

### November Plan vs Current Budgets
The November plan reduces budgets by **18%** from current configured levels, or **35%** from actual October spend.

## Campaign-by-Campaign Comparison

### Top 10 Campaigns (by current budget)

| Campaign | Current Daily | November Daily | Change | % Change |
|----------|--------------|----------------|--------|----------|
| NDA \| UK \| Search \| Interior Design Diploma 140 Ai Max 5/8 | £300.00 | £228.58 | -£71.42 | -24% |
| NDA \| UK \| Search \| Brand 100 New Customer 1/8 No Target | £110.00 | £28.27 | -£81.73 | -74% |
| NDA \| Search \| Interior Design Degree- UK 120 No Target 24/4 | £100.00 | £42.63 | -£57.37 | -57% |
| NDA \| UAE \| Search \| Interior Design Diploma No Target | £90.00 | £17.57 | -£72.43 | -80% |
| NDA \| UAE \| Search \| Interior Design Degree No Target | £50.00 | £8.54 | -£41.46 | -83% |
| NDA \| OM/SA/BH/KW \| Search \| Interior Design Diploma No Target | £50.00 | £54.22 | +£4.22 | +8% |
| NDA \| Search \| Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 | £45.00 | £1.19 | -£43.81 | -97% |
| NDA \| ROTW \| Search \| Brand Inclusion No Target | £45.00 | £20.09 | -£24.91 | -55% |
| NDA \| US/CA \| Search \| Interior Design Degree 250 No Target 15/9 | £40.00 | £30.59 | -£9.41 | -24% |
| NDA \| BH/CY/KW \| Search \| Interior Design Degree No Target | £30.00 | £5.16 | -£24.84 | -83% |

### Campaigns with Drastic Reductions (>90%)

These campaigns move to minimal test budgets (<£2/day):

| Campaign | Current Daily | November Daily | % Change |
|----------|--------------|----------------|----------|
| NDA \| Search \| Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 | £45.00 | £1.19 | -97% |
| NDA \| P Max Reboot \| Interior Design Diploma - MENA | £10.00 | £1.23 | -88% |
| NDA \| P Max \| Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar | £10.00 | £1.40 | -86% |
| NDA \| IN \| Search \| Interior Design Degree No Target | £20.00 | £0.86 | -96% |
| NDA \| Search \| Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135 | £15.00 | £0.84 | -94% |
| NDA \| EUR \| Search \| Landscape Design Courses 65 | £15.00 | £0.00 | -100% |

**Rationale**: All have 0 YTD conversions and are set to minimal test budgets per August baseline strategy.

### Campaigns Unchanged

12 campaigns remain at their current budget levels (kept from August baseline):

- NDA | UK | Search | Interior Design Diploma 140 Ai Max 5/8 (£300/day → £228.58/day, but this is actual August level)
- NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5
- NDA | P Max | Interior Design Degree - UK 100 17/3 No Target 30/4
- NDA | OM/SA/BH/KW | Search | Interior Design Diploma No Target
- NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5
- NDA | P Max | Interior Design - India 135 29/11 No Target 10/9
- NDA | US/CA | Search | Interior Design Degree 250 No Target 15/9
- NDA | P Max | Interior Design Degree - ROTW 200 13/1 No Target 23/9
- NDA | UK | Search | Brand 100 New Customer 1/8 No Target (£110/day → £28.27/day, August level)
- NDA | Search | Interior Design Diploma - USA/ Canada 250 Split 11/3
- NDA | UK | Search | Landscape Design Diplomas No Target
- NDA | Search | Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden

## Important Notes

### Why Current Budgets ≠ October Spend

The current configured budgets (£31,718/month) are **21% lower** than actual October spend (£39,996.40/month). This discrepancy likely due to:

1. **Budget-limited campaigns**: Many campaigns spent at or near their daily limits
2. **Mid-month changes**: Budgets may have been increased during October that aren't reflected in current settings
3. **Shared budgets**: Some campaigns may share budgets that allow overspend
4. **Delivery fluctuations**: Google Ads can spend up to 2x daily budget on high-traffic days

### November Budget Strategy

The November plan is based on **August baseline performance** (not current budgets). Key principles:

1. **No pauses**: All campaigns remain active at minimum test budgets
2. **95% reduction**: Zero-conversion campaigns get £0-£1.23/day
3. **80% reduction**: Very high CPA campaigns (£600-£2,000+)
4. **50% reduction**: High CPA campaigns (£400-£600)
5. **Keep**: Good CPA campaigns (£38-£300) maintain August levels

## Rollback Strategy

Both CSV files are provided for safe deployment:

1. **nda_november_budgets_for_google_ads_editor.csv**: New November budgets (August baseline)
2. **nda_october_current_budgets_rollback.csv**: Current configured budgets (exact API values)

If November budgets cause issues, simply import the rollback CSV to restore exact current settings.

## Next Steps

1. **Import November budgets** via Google Ads Editor
2. **Monitor Week 1**: Check for disapprovals, budget-limited campaigns
3. **Assess Week 2**: Review CPA changes, conversion volume
4. **Compare Month 1**: Evaluate performance vs August baseline
5. **Rollback if needed**: Import rollback CSV to restore current settings
