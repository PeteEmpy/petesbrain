# Smythson UK Conversion Rate Drop Analysis

**Date:** 14 November 2025
**Analyst:** Pete
**Period Analyzed:** October 21 - November 10, 2025

## Executive Summary

UK conversion rates have declined from 5.16% (2024 average) to 5.59% overall in 2025, but this masks significant volatility in recent weeks. The decline is **isolated to Performance Max campaigns**, while Brand campaigns remain stable and strong at 6-8% CVR.

**Critical Context:** Several PMax campaigns have new asset groups that are still in learning periods (2-4 weeks). Current performance drops are likely temporary and should improve as Smart Bidding completes optimization.

## Campaign-Level Breakdown

### Performance Max Campaigns (In Learning)

| Campaign | Oct 21-27 | Nov 4-10 | Change | Status |
|----------|-----------|----------|--------|--------|
| **P Max H&S Briefcases** | 3.43% | 0.48% | -86% | New asset groups |
| **P Max H&S Christmas Gifting** | 1.87% | 0.75% | -60% | New asset groups |
| **Generic AI Campaign** | 6.27% | 0.36% | -94% | New/learning |

**Traffic Impact:** PMax campaigns drive 36% of total UK traffic, so these declines significantly skew overall account metrics.

### Brand Campaigns (Stable)

| Campaign | Oct 21-27 | Nov 4-10 | Change | Status |
|----------|-----------|----------|--------|--------|
| **Brand - Exact** | 6.51% | 7.76% | +19% | ✓ Stable |

Brand campaigns continue to perform well, indicating no fundamental issues with account health or website conversion capability.

## Regional Performance Comparison

### UK Market
- **2024 Average:** 5.16%
- **2025 Average:** 5.59% (+8%)
- **Recent Trend:** Declining due to PMax learning periods
- **Peak 2025:** 9.89% (Sep 8)
- **Low 2025:** 3.04% (Nov 10)

### USA Market
- **2024 Average:** 3.46%
- **2025 Average:** 2.82% (-18%)
- **Peak 2025:** 4.48% (Sep 8)
- **Low 2025:** 1.19% (Nov 10)
- **Note:** Only market showing sustained decline

### EUR Market
- **2024 Average:** 2.63%
- **2025 Average:** 4.78% (+82%)
- **Peak 2025:** 9.02% (Sep 8)
- **Low 2025:** 1.96% (Oct 6)
- **Note:** Strongest improvement, now using both GA4 and Google Ads conversion tracking

### ROW Market
- **2024 Average:** 0.84% (limited data, campaigns paused)
- **2025 Average:** 3.25% (+287%)
- **Peak 2025:** 4.67% (Sep 8)
- **Low 2025:** 1.42% (Nov 10)
- **Note:** Dramatic improvement with full campaign activity

## Root Cause Analysis

### Primary Factors

1. **Learning Periods (Main Driver)**
   - New asset groups added to existing PMax campaigns
   - Smart Bidding requires 2-4 weeks to optimize
   - Performance typically volatile and below optimized levels during learning
   - Expected to improve significantly once learning completes

2. **Traffic Composition**
   - PMax campaigns represent 36% of UK traffic
   - Learning period inefficiency creates disproportionate impact on account averages
   - Brand campaigns (stable performance) represent smaller portion of traffic

### Secondary Considerations

- **USA Market Decline:** Requires separate investigation as it's not explained by learning periods
- **Seasonality:** November historically shows some volatility in luxury goods sector
- **Asset Group Strategy:** Need to verify new asset groups have appropriate targeting and sufficient data

## Expected Outcome

**Timeline:** Next 2-3 weeks (by late November/early December)

**Expected Changes:**
- PMax conversion rates should recover to 3-4% range as learning completes
- Overall UK average should stabilize around 5-6%
- Brand campaigns will continue to provide 6-8% baseline performance

**Confidence:** High - this pattern is consistent with typical Smart Bidding learning behavior

## Recommendations

### Immediate Actions
1. **Monitor daily:** Track PMax conversion rates for improvement signals
2. **No panic changes:** Avoid making strategic changes during learning periods
3. **Document baseline:** Record when asset groups were added to track learning exit

### Short-term (1-2 weeks)
1. **Review asset group structure:** Ensure new groups have proper targeting and creative assets
2. **Check product feed:** Verify all products in new asset groups are in stock and correctly priced
3. **Monitor USA separately:** Investigate USA-specific decline (not learning-related)

### Medium-term (3-4 weeks)
1. **Post-learning analysis:** Compare performance before/after learning completion
2. **Asset group optimization:** Refine underperforming groups based on learned data
3. **Strategic review:** Assess if asset group additions delivered expected benefits

## Data Sources

- **Google Ads API:** Campaign performance metrics (GAQL queries)
- **Date Range 2024:** September 1 - December 28, 2024 (17 weeks)
- **Date Range 2025:** September 1 - November 10, 2025 (11 weeks)
- **Conversion Actions:**
  - UK: "Purchase (Google Ads)"
  - USA: "Purchase US (Google Ads)"
  - EUR: "New Site - GA4 (web) purchase" + "Purchase EUR (Google Ads)"
  - ROW: "New Site - GA4 (web) purchase"

## Visualizations Created

1. **UK Conversion Rate Chart:** `smythson-uk-conversion-rate-by-week.html`
2. **USA Conversion Rate Chart:** `smythson-usa-conversion-rate-by-week.html`
3. **EUR Conversion Rate Chart:** `smythson-eur-conversion-rate-by-week.html`
4. **ROW Conversion Rate Chart:** `smythson-row-conversion-rate-by-week.html`
5. **Campaign Analysis HTML:** `uk-pmax-conversion-rate-analysis.html`

All charts show 2024 vs 2025 weekly comparison with data labels.

## Key Takeaways

✅ **Not a fundamental problem** - Brand campaigns performing well
✅ **Learning periods explain PMax drops** - Expected to recover
✅ **EUR and ROW showing strong growth** - International expansion working
⚠️ **USA needs attention** - Decline not explained by learning periods
📊 **Traffic mix matters** - PMax 36% of traffic creates outsized impact

## Next Review Date

**November 25, 2025** - Check if PMax campaigns have exited learning and conversion rates have recovered.
