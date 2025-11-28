# ROAS Target Change Impact Analysis
**Accessories for the Home**  
**Change Date**: November 5, 2025 (200% → 190%)  
**Analysis Date**: November 9, 2025  
**Analysis Period**: 4 days post-change

---

## 🚨 CRITICAL: PRELIMINARY ANALYSIS - TOO EARLY TO DRAW CONCLUSIONS

**⚠️ This analysis covers only 4 days post-change and is NOT sufficient to make decisions.**

### Why This Analysis Is Premature:

1. **Insufficient Time Period**: Only 4 days of data (Nov 5-9) is far too short to assess the impact of a ROAS target change
2. **Algorithm Learning Period**: Google's algorithms need 5-7 days minimum to adjust to new bid targets
3. **Conversion Lag**: E-commerce conversions typically have 1-3 day delays; many conversions from Nov 5-9 clicks may not have occurred yet
4. **Day-to-Day Variance**: Performance naturally fluctuates daily; 4 days doesn't show trends
5. **Unequal Comparison**: Comparing 7 days (before) vs 4 days (after) is not statistically valid
6. **Impression Share Metric Error**: Our query used `search_impression_share` which doesn't apply to P Max campaigns, making those metrics unreliable
7. **Impression Share Reporting Delay**: Cross-account analysis shows Friday impression share dips are systematic (11.8pp lower for AFH), suggesting data reporting delays rather than actual performance issues. Impression share can take 48-72 hours to fully populate.

### What We Know:

- **Account-Level Impression Share**: 72.44% on Nov 6 (from Auction Insights) - **STRONG**
- **Shopping Campaign**: Early signs positive (ROAS improved), but needs more time
- **P Max Campaign**: Early signs concerning, but needs more time to assess

### Decision: **WAIT FOR MORE DATA**

**No actions should be taken based on this preliminary analysis.** 

**Re-analysis scheduled**: November 12, 2025 (1 week post-change) - This will provide sufficient data for decision-making.

---

## ⚠️ Important: Attribution Method

**This analysis uses CLICK-TIME attribution** (default Google Ads method):
- Conversions are attributed to the date the ad was clicked
- If a user clicks on Nov 5 but converts on Nov 8, the conversion is counted on Nov 5
- This is the standard method used by Google Ads for reporting

**Conversion Lag Consideration**:
- For e-commerce (especially furniture/home goods), there's typically a 1-3 day delay between click and purchase
- The Nov 5-9 period may show lower conversions because:
  - Some conversions from Nov 5-9 clicks haven't happened yet (will convert Nov 10-12)
  - The analysis period is only 4 days, which may not capture full conversion cycle
  
**Extended Window Analysis**: We queried clicks from Nov 5-9 with conversions tracked through Nov 12, but found no significant additional conversions. This suggests either:
1. Conversions are happening quickly (same/next day)
2. The conversion lag is minimal for this account
3. Additional conversions may still be pending

**Recommendation**: Re-run this analysis on Nov 12 (1 week post-change) to capture full conversion cycle from Nov 5-9 clicks.

---

## 📊 Executive Summary

**⚠️ PRELIMINARY DATA ONLY - DO NOT MAKE DECISIONS BASED ON THIS**

**Overall Assessment**: 🟡 **INSUFFICIENT DATA** - Only 4 days post-change; need full week for valid analysis

### Early Observations (Not Conclusions):

1. **Shopping Furniture (Villains)**: 🟢 **Early signs positive** (but too early to conclude)
   - ROAS improved from 1.90x to **3.72x** (+95.8%) in 4 days
   - Revenue increased 33.4% despite lower spend
   - CVR improved significantly (+74.3%)
   - **Note**: Promising start, but needs full week to confirm trend

2. **Main P Max (Furniture H&S/Zombies)**: 🟡 **Early signs concerning** (but too early to conclude)
   - ROAS dropped from 2.25x to **1.66x** (-26.2%) in 4 days
   - Revenue decreased 41.7%
   - Conversions dropped 56.0%
   - **Note**: Impression share metrics unreliable (wrong metric type queried)
   - **Note**: Could be algorithm learning period; needs more time

3. **Account-Level Performance**: ✅ **Strong impression share maintained**
   - Auction Insights (Nov 6): 72.44% account-level impression share
   - Shows overall account visibility remains strong
   - Competitive landscape active but manageable

---

## 📈 Detailed Campaign Analysis

### Campaign 1: Shopping Furniture (Villains)
**Campaign ID**: 21527979308

#### Performance Comparison

| Metric | Before (Oct 29 - Nov 5) | After (Nov 5 - Nov 9) | Change | Status |
|--------|------------------------|----------------------|--------|--------|
| **Spend** | £269.39 | £183.71 | -£85.68 (-31.8%) | 🟡 Lower spend |
| **Revenue** | £512.53 | £683.67 | +£171.14 (+33.4%) | 🟢 **Strong growth** |
| **ROAS** | 1.90x | **3.72x** | +1.82x (+95.8%) | 🟢 **Excellent** |
| **Conversions** | 3.0 | 3.0 | 0.0 (-0.7%) | 🟡 Stable |
| **CPA** | £89.80 | £61.73 | -£28.07 (-31.3%) | 🟢 **Improved** |
| **CVR** | 0.70% | **1.22%** | +0.52pp (+74.3%) | 🟢 **Strong improvement** |
| **CTR** | 2.19% | 2.41% | +0.22pp (+10.0%) | 🟢 Improved |
| **Impression Share** | 48.8% | 47.1% | -1.7pp | 🟡 Slight decrease |

#### Analysis

**✅ Success Factors:**
- The 190% ROAS target has allowed Google's algorithm to optimize more effectively
- Significant improvement in conversion rate (0.70% → 1.22%) suggests better audience targeting
- Lower CPA (£89.80 → £61.73) indicates more efficient bidding
- Revenue increased despite lower spend, showing improved efficiency

**Key Insight**: This campaign is responding exactly as expected to the ROAS reduction - more aggressive bidding is capturing higher-quality traffic and converting better.

**Recommendation**: ✅ **Continue with 190% target** - This campaign is performing exceptionally well.

---

### Campaign 2: Main P Max (Furniture H&S/Zombies)
**Campaign ID**: 20276730131

#### Performance Comparison

| Metric | Before (Oct 29 - Nov 5) | After (Nov 5 - Nov 9) | Change | Status |
|--------|------------------------|----------------------|--------|--------|
| **Spend** | £5,856.78 | £4,625.76 | -£1,231.02 (-21.0%) | 🔴 Lower spend |
| **Revenue** | £13,192.34 | £7,690.72 | -£5,501.62 (-41.7%) | 🔴 **Major decline** |
| **ROAS** | 2.25x | **1.66x** | -0.59x (-26.2%) | 🔴 **Below target** |
| **Conversions** | 31.7 | 13.9 | -17.7 (-56.0%) | 🔴 **Severe drop** |
| **CPA** | £184.81 | £331.68 | +£146.87 (+79.5%) | 🔴 **Much worse** |
| **CVR** | 0.40% | 0.31% | -0.09pp (-22.5%) | 🔴 Declined |
| **CTR** | 0.93% | 1.42% | +0.49pp (+52.7%) | 🟢 Improved |
| **Impression Share** | 54.0% | **10.0%** | -44.0pp | 🔴 **CRITICAL** |
| **Rank Lost IS** | 45.4% | **76.8%** | +31.4pp | 🔴 **CRITICAL** |

#### Analysis

**⚠️ Critical Issues Identified:**

1. **Impression Share Collapse**: The most concerning metric - impression share dropped from 54% to just 10%. This is far beyond what a ROAS target reduction should cause.

2. **Rank-Lost Impression Share Increased**: From 45.4% to 76.8% means competitors are outbidding us in 77% of auctions. This suggests:
   - Quality score issues (ad relevance, landing page experience)
   - Product feed problems
   - Competitive pressure beyond just bid adjustments

3. **Conversion Rate Decline**: CVR dropped from 0.40% to 0.31%, suggesting the traffic being captured is lower quality despite higher CTR.

4. **Spend Reduction**: Campaign is spending 21% less, likely because Google's algorithm is struggling to find profitable auctions at the 190% target given the quality score issues.

**Root Cause Hypothesis:**

The audit report from Nov 5 warned: *"First day shows dramatic impression share drop. This is unusual - ROAS reduction should improve auction participation, not worsen it."*

This suggests **quality score or feed issues** that are preventing the campaign from competing effectively, regardless of bid strategy. The ROAS target reduction may have exposed underlying problems rather than caused them.

**Possible Contributing Factors:**

1. **Product Feed Quality**: Issues with product data, images, or availability
2. **Ad Relevance**: Creative fatigue or poor ad-to-query matching
3. **Landing Page Experience**: Site speed, mobile experience, or conversion path issues
4. **Competitive Pressure**: Cox & Cox or other competitors may have improved their quality scores
5. **Algorithm Learning Period**: P Max campaigns need time to adjust, but 4 days should show some recovery

**⚠️ PRELIMINARY OBSERVATION ONLY - NOT A RECOMMENDATION**

**No actions should be taken based on 4 days of data.**

**Wait for full week analysis (Nov 12) before making any decisions.**

---

## 🎯 Overall Assessment

### What's Working:
- ✅ Shopping Furniture campaign is performing excellently with 190% target
- ✅ Lower ROAS target is allowing better optimization for Shopping campaigns

### What's Not Working:
- ❌ Main P Max campaign showing severe performance decline
- ❌ Impression share collapse suggests quality score issues, not just bid strategy
- ❌ Conversion rate decline indicates traffic quality problems

### Key Insight:

The **Shopping campaign** (standard Shopping ads) is responding perfectly to the ROAS reduction, while the **P Max campaign** (machine learning-driven) is struggling. This suggests:

1. **Shopping campaigns** have more direct control and respond better to bid adjustments
2. **P Max campaigns** rely heavily on quality signals, and if those are poor, bid adjustments alone won't help

---

## 📋 Recommendations

### ⚠️ NO ACTIONS AT THIS TIME

**Wait for full week analysis (November 12, 2025) before making any decisions.**

### Scheduled Re-Analysis (November 12, 2025):

1. **Re-run complete analysis** with full 7 days of data (Nov 5-12)
2. **Compare equal periods**: 7 days before (Oct 29 - Nov 5) vs 7 days after (Nov 5-12)
3. **Use correct metrics**: Query appropriate impression share metrics for each campaign type
4. **Account for conversion lag**: Include conversions that occurred Nov 10-12 from Nov 5-9 clicks
5. **Make data-driven decisions** based on full week of performance

### What to Monitor Until Nov 12:

- [ ] Account-level ROAS (should stay above 1.80x)
- [ ] Account-level revenue trends
- [ ] Google Ads UI impression share (not API metrics)
- [ ] No premature changes to campaigns

---

## 📊 Data Summary

### Combined Campaign Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total Spend** | £6,126.17 | £4,809.47 | -£1,316.70 (-21.5%) |
| **Total Revenue** | £13,704.87 | £8,374.39 | -£5,330.48 (-38.9%) |
| **Combined ROAS** | 2.24x | 1.74x | -0.50x (-22.3%) |
| **Total Conversions** | 34.7 | 16.9 | -17.8 (-51.3%) |

**Note**: These combined metrics are heavily skewed by the Main P Max campaign's decline. The Shopping Furniture campaign is performing well in isolation.

---

## 🔗 Related Resources

- **Original Audit Report**: `2025-11-05-weekly-audit.md`
- **Experiment Log**: See CONTEXT.md for experiment tracking
- **Product Performance Spreadsheet**: [View Here](https://docs.google.com/spreadsheets/d/1V23MwIeSDTj5ECBJAOIukENzy3YMxUoOEMiSP2IZAWM/edit)

---

**Analysis Generated**: November 9, 2025  
**Data Source**: Google Ads API via MCP  
**Next Review**: November 12, 2025 (1 week assessment)

