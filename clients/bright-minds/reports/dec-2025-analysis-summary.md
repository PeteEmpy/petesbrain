# Bright Minds - December 2025 Performance Analysis

**Analysis Date**: 15th December 2025  
**Data Range**: 1st-15th December 2025  
**Customer ID**: 1404868570

---

## Executive Summary

December 2025 performance shows **significant YoY decline** compared to December 2024, with revenue down 70% and ROAS down 60%. While spend has remained relatively stable (+0.8% daily average), the account is generating substantially fewer conversions at a much higher cost per acquisition.

### Key Metrics (Dec 1-15)

| Metric | Dec 2024 | Dec 2025 | YoY Change |
|--------|----------|----------|------------|
| **Spend** | £12,279.18 | £9,284.43 | -24.4% |
| **Revenue** | £128,085.50 | £38,429.22 | -70.0% |
| **Conversions** | 11,103.04 | 1,096.91 | -90.1% |
| **ROAS** | 10.43 | 4.14 | -60.3% |
| **Conversion Rate** | 35.06% | 3.54% | -89.9% |
| **CPA** | £1.11 | £8.46 | +665.3% |

---

## Critical Issues

### 1. Conversion Tracking Crisis
**The 90% drop in conversions suggests a conversion tracking issue rather than genuine performance decline.**

**Evidence**:
- Conversion rate dropped from 35.06% to 3.54% (-89.9%)
- Conversions dropped from 11,103 to 1,097 (-90.1%)
- CPA increased from £1.11 to £8.46 (+665%)
- Click volume only down 2.2% (31,665 → 30,959)

**Likely Cause**: 
- Conversion tracking implementation changed between Dec 2024 and Dec 2025
- Different conversion actions being tracked
- Possible tracking tag removal or configuration change

**Immediate Action Required**:
1. Verify conversion tracking implementation in Google Ads
2. Check conversion actions currently active vs. Dec 2024
3. Verify Google Tag Manager / GA4 implementation
4. Check if conversion goals have been modified

### 2. Revenue Quality Concern

Even accounting for potential tracking issues, the **70% revenue decline** is severe.

**Possible Explanations**:
- Different conversion value tracking methodology
- Product mix shift (lower-value products/services)
- Pricing changes
- Market demand shift

**Action Required**:
- Review conversion value tracking setup
- Compare product/service mix Dec 2024 vs 2025
- Verify revenue attribution model hasn't changed

---

## Campaign Structure (Dec 2025)

### Active Campaigns

1. **BMI | P Max | Generic** (ID: 21064167535)
   - Status: ENABLED
   - Primary campaign driving traffic
   - Budget adjustments throughout period (shown in name)

2. **BMI | Search | Brand** (ID: 2083618047)
   - Status: ENABLED
   - Brand protection campaign
   - Budget: £550 (from 20th November)

---

## Daily Performance Trends

**Notable Pattern**: Spend has been relatively consistent (£550-£730/day) through 14th December, with a significant drop on 15th December (£180 - partial day data).

**Strongest Days** (by spend):
- 12th Dec: £729.91 (7.9% of total)
- 14th Dec: £718.41 (7.7%)
- 11th Dec: £707.17 (7.6%)

**No outlier days detected** - spend distribution is healthy (largest day <30% of total).

---

## Projections

### Full Month Forecast (if current pace continues)

| Metric | Projected Dec 2025 (31 days) |
|--------|------------------------------|
| Spend | £19,187.81 |
| Revenue | £79,420.38 |
| Conversions | 2,267 |
| ROAS | 4.14 |

### Remaining Period (16th-31st Dec)

At current daily averages:
- Additional spend: £9,903.39
- Additional revenue: £40,991.16
- Additional conversions: 1,170

---

## Strategic Recommendations

### Priority 1: URGENT - Fix Conversion Tracking

**Timeline**: Today (15th December)

**Actions**:
1. Audit conversion tracking setup in Google Ads
2. Compare conversion actions: Dec 2024 vs Dec 2025
3. Verify Google Analytics 4 / Tag Manager implementation
4. Check for any website changes that might have removed tracking tags
5. Test conversion tracking on live site

**Why Urgent**: Cannot optimize effectively with 90% conversion drop - this masks all other insights.

### Priority 2: Investigate Revenue Attribution

**Timeline**: 16th-17th December

**Actions**:
1. Review conversion value setup (fixed values vs. dynamic)
2. Check if attribution model changed
3. Verify product catalogue pricing
4. Compare average order value Dec 2024 vs 2025

### Priority 3: Budget Optimization (Post-Tracking Fix)

**Timeline**: 18th-20th December (after tracking verified)

**Actions**:
1. Review Performance Max asset performance
2. Analyze Search term report for brand campaign
3. Consider budget reallocation based on fixed tracking data
4. Test increased budgets if ROAS improves post-fix

### Priority 4: Pre-Christmas Push (If Tracking Fixed)

**Timeline**: 21st-24th December

**Actions**:
1. Increase budgets for final shopping days
2. Monitor hourly for rapid optimization
3. Ensure ad scheduling optimized for peak hours
4. Review audience signals in Performance Max

---

## Data Quality Verification

✅ **Data verified from Google Ads API**:
- Queried ALL campaigns (including paused) with spend
- 2 campaigns found in period
- 0 paused campaigns with spend
- Revenue distribution: largest day = 7.9% of total (2025-12-12)
- No outlier days detected (largest <30% of total)
- Daily data complete (15 days covered)

**Verification saved to**: 
- `/Users/administrator/Documents/PetesBrain.nosync/clients/bright-minds/reports/dec-2025-performance-verification.txt`

**Raw data saved to**:
- `/Users/administrator/Documents/PetesBrain.nosync/clients/bright-minds/reports/dec-2025-daily-performance.csv`

**Comparison saved to**:
- `/Users/administrator/Documents/PetesBrain.nosync/clients/bright-minds/reports/dec-2024-vs-2025-comparison.txt`

---

## Next Steps

1. **Immediate**: Investigate conversion tracking (today)
2. **Tomorrow**: Review conversion value attribution
3. **This Week**: Optimize budgets if tracking issue resolved
4. **Next Week**: Pre-Christmas budget push (if appropriate)

**Critical Question to Answer**: Is the 90% conversion drop real or a tracking issue?

**Hypothesis**: Strong evidence suggests tracking issue given:
- 90% conversion drop with only 2% click drop
- 665% CPA increase
- 60% ROAS decline
- Minimal impression/click volume changes

---

**Document Version**: 1.0  
**Generated**: 15th December 2025 12:42 GMT  
**Data Source**: Google Ads API (verified query)
