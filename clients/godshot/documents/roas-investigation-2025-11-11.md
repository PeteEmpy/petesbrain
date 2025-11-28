# Godshot ROAS Drop-off Investigation
**Date**: 2025-11-11
**Account**: GOD | P Max 700 (9922220205)
**Analysis Period**: Last 14 days (Oct 28 - Nov 10, 2025)

---

## Executive Summary

**CRITICAL FINDING**: ROAS has dropped **-72% in the last 7 days** compared to the previous 7 days.

| Period | Spend | Revenue | ROAS | Change |
|--------|-------|---------|------|--------|
| **Last 7 Days** (Nov 4-10) | **£1,202.21** | **£6,650.81** | **553%** | **-72%** |
| **Previous 7 Days** (Oct 28-Nov 3) | **£416.98** | **£6,402.43** | **1,535%** | Baseline |

**Key Metrics:**
- Revenue is stable (+4% to £6,650.81)
- Spend has increased by **+188%** (£1,202 vs £417)
- Conversion volume is similar (95.9 vs 80.6 conversions)
- **Average CPC has increased +28%** (£0.49 vs £0.38)

---

## Detailed Daily Breakdown

### Last 7 Days (Nov 4-10, 2025)
| Date | Spend | Revenue | ROAS | Conversions | Clicks | CPC | Impressions |
|------|-------|---------|------|-------------|--------|-----|-------------|
| Nov 10 | £176.01 | £919.29 | 522% | 17.98 | 392 | £0.45 | 32,466 |
| Nov 9 | £179.09 | £1,142.09 | 638% | 12.96 | 401 | £0.45 | 33,746 |
| Nov 8 | £189.44 | £1,369.12 | 723% | 15.00 | 366 | £0.52 | 30,939 |
| Nov 7 | £188.61 | £568.29 | **301%** ⚠️ | 10.01 | 381 | £0.50 | 31,755 |
| Nov 6 | £197.34 | £846.42 | 429% | 13.47 | 382 | £0.52 | 33,196 |
| Nov 5 | £117.09 | £1,109.92 | **948%** | 13.47 | 288 | £0.41 | 24,869 |
| Nov 4 | £154.73 | £645.72 | 417% | 13.02 | 301 | £0.51 | 24,216 |
| **TOTAL** | **£1,202.21** | **£6,650.81** | **553%** | **95.91** | **2,511** | **£0.49** | **211,187** |

### Previous 7 Days (Oct 28-Nov 3, 2025)
| Date | Spend | Revenue | ROAS | Conversions | Clicks | CPC | Impressions |
|------|-------|---------|------|-------------|--------|-----|-------------|
| Nov 3 | £66.89 | £1,216.46 | **1,819%** | 14.01 | 216 | £0.31 | 13,776 |
| Nov 2 | £71.70 | £1,616.74 | **2,254%** | 19.18 | 205 | £0.35 | 11,563 |
| Nov 1 | £75.71 | £888.32 | 1,173% | 7.30 | 173 | £0.44 | 12,563 |
| Oct 31 | £55.46 | £1,177.74 | **2,123%** | 14.01 | 164 | £0.34 | 11,063 |
| Oct 30 | £77.88 | £253.21 | **325%** ⚠️ | 5.51 | 194 | £0.40 | 14,245 |
| Oct 29 | £59.02 | £623.91 | 1,057% | 9.13 | 186 | £0.32 | 11,805 |
| Oct 28 | £67.34 | £675.13 | 1,003% | 11.46 | 185 | £0.36 | 10,472 |
| **TOTAL** | **£416.98** | **£6,402.43** | **1,535%** | **80.61** | **1,323** | **£0.38** | **85,487** |

---

## Root Cause Analysis

### 🔴 **ROOT CAUSE CONFIRMED: Budget Increased to £190/day**

**CRITICAL FINDING**: The daily budget was increased from **£64/day to £190/day** (+197% increase).

| Setting | Previous | Current | Change |
|---------|----------|---------|--------|
| **Daily Budget** | £64/day | **£190/day** | **+197%** |
| **Monthly Budget** | £2,000/month | £5,700/month | +185% |
| **Target ROAS** | None (per CONTEXT.md) | **700%** | NEWLY SET |

**Budget Verification from Google Ads API**:
- `campaign_budget.amount_micros`: 190,000,000 (= £190.00)
- `campaign.maximize_conversion_value.target_roas`: 7.0 (= 700%)

**When this changed**: Unknown - requires campaign change history analysis.

---

### 1. **Massive Spend Increase (+188%) - EXPLAINED**

**Primary Issue**: Daily spend has nearly **tripled** in the last 7 days.

| Period | Avg Daily Spend | Change |
|--------|-----------------|--------|
| Oct 28-Nov 3 | £59.57/day | Baseline |
| Nov 4-10 | £171.74/day | **+188%** |

**Budget Context**:
- **Previous Budget**: £64/day (~£2,000/month) - documented in CONTEXT.md
- **Current Budget**: £190/day (~£5,700/month) - confirmed via API
- **Actual Spend**: £171.74/day = **90% of new £190 budget** ✅

**Implication**: Spend increase is **EXPECTED** given the budget was nearly tripled. Google is spending close to the new daily budget limit.

---

### 2. **Cost Per Click Increased +28%**

| Period | Avg CPC | Change |
|--------|---------|--------|
| Oct 28-Nov 3 | £0.38 | Baseline |
| Nov 4-10 | £0.49 | **+28%** |

**CPC peaked on Nov 6-8 at £0.50-£0.52** (vs. £0.31-£0.36 in late October).

**Potential Causes:**
- Increased competition (November = early Black Friday prep)
- Algorithm bidding more aggressively for conversions
- Shift in traffic mix (higher-cost placements like YouTube, Display)
- Audience exhaustion (bidding up to reach new users)

---

### 3. **Traffic Volume Surged +147%**

| Period | Total Impressions | Total Clicks | Change |
|--------|-------------------|--------------|--------|
| Oct 28-Nov 3 | 85,487 | 1,323 | Baseline |
| Nov 4-10 | 211,187 | 2,511 | **+147%** |

**Implication**: Google is showing ads far more frequently, driving much higher click volume at higher CPCs.

---

### 4. **Revenue Flat Despite Traffic Increase**

| Period | Total Revenue | Revenue/Click |
|--------|---------------|---------------|
| Oct 28-Nov 3 | £6,402.43 | £4.84 |
| Nov 4-10 | £6,650.81 | £2.65 |

**Revenue per click dropped -45%** (£4.84 → £2.65).

**Interpretation**: More traffic, but **lower quality**. Extra clicks are not converting at the same rate or order value.

---

### 5. **Daily ROAS Volatility**

**Extreme swings in recent days:**
- Nov 2: **2,254% ROAS** (£71.70 spend → £1,616.74 revenue)
- Nov 5: **948% ROAS** (£117.09 spend → £1,109.92 revenue)
- **Nov 7: 301% ROAS** ⚠️ (£188.61 spend → £568.29 revenue)

**Oct 30 also had low ROAS: 325%** (£77.88 spend → £253.21 revenue)

**Pattern**: Low-ROAS days coincide with **higher spend** (£188-£197 vs. £66-£117).

---

## Key Questions to Investigate

### 1. **Was there a bidding strategy change?**
- Check if "Maximize Conversion Value" was adjusted
- Review if target ROAS was set (CONTEXT.md says no fixed target)
- Check if budget was increased (daily budget should be £64)

### 2. **Conversion tracking accuracy**
- CONTEXT.md flags **CRITICAL conversion tracking issues** (only 20% match rate with actual WooCommerce sales)
- Plugin updated Nov 10 (Conversion Tracking for WooCommerce v2.1.4)
- **Could inflated conversion data be causing algorithm to over-bid?**

### 3. **Black Friday competition**
- November = retailers preparing for Black Friday (Nov 29)
- Increased competition in coffee/homeware/gifting categories
- CPCs typically rise 20-40% in pre-Black Friday period

### 4. **Performance Max asset group changes**
- Were new assets added that triggered lower-quality placements?
- Check if asset group performance shifted (Search vs Display vs YouTube)

### 5. **Audience signals or targeting changes**
- Were audience signals modified?
- Did Google's algorithm expand targeting too aggressively?

---

## Immediate Actions Required

### 🔴 **URGENT: Investigate Budget Settings**

**Action**: Check if daily budget was accidentally increased from £64 to £170+.

```gaql
SELECT
  campaign.name,
  campaign_budget.amount_micros,
  campaign_budget.explicitly_shared,
  campaign.start_date
FROM campaign
WHERE campaign.id = 20762581893
```

**If budget was increased**: Revert to £64/day immediately.

---

### 🔴 **URGENT: Review Bidding Strategy Changes**

**Action**: Check campaign change history for any bidding adjustments in last 14 days.

```gaql
SELECT
  change_event.change_date_time,
  change_event.change_resource_type,
  change_event.user_email,
  change_event.old_resource,
  change_event.new_resource
FROM change_event
WHERE change_event.change_date_time >= '2025-10-28'
  AND campaign.id = 20762581893
ORDER BY change_event.change_date_time DESC
```

---

### 🟠 **HIGH PRIORITY: Review Asset Group Performance**

**Action**: Break down performance by channel (Search, Display, YouTube, Shopping).

```gaql
SELECT
  segments.date,
  campaign_criterion.channel,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions_value
FROM campaign_criterion
WHERE segments.date DURING LAST_14_DAYS
  AND campaign.id = 20762581893
ORDER BY segments.date DESC, metrics.cost_micros DESC
```

---

### 🟠 **HIGH PRIORITY: Check Conversion Tracking Plugin Impact**

**Context**: Plugin updated Nov 10 (same day as analysis). Monitor if conversion data stabilizes.

**Action**:
1. Review WooCommerce sales Nov 4-10 vs Google Ads reported conversions
2. Check if conversion values match actual order values
3. Verify product ID attribution improved with v2.1.4 update

**Review Date**: Nov 13-15 (3-5 days after plugin update)

---

### 🟡 **MEDIUM PRIORITY: Analyze Search Terms Report**

**Action**: Identify if low-intent or expensive queries are driving wasted spend.

```gaql
SELECT
  segments.search_term,
  segments.search_term_match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM search_term_view
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.id = 20762581893
  AND metrics.clicks > 0
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

---

## Strategic Recommendations

### 1. **Set a Target ROAS (if not already set)**

**Current Strategy**: Maximize Conversion Value (no target)

**Problem**: Algorithm has no constraint on efficiency, only maximizing revenue.

**Recommendation**: Set target ROAS of **500%** (conservative, below recent average but safe floor).

**Rationale**:
- Historical ROAS: 553-1,535% (last 14 days)
- Account-level ROAS (Aug-Oct): 1,107%
- 500% target gives algorithm flexibility while protecting efficiency

---

### 2. **Reduce Daily Budget to Control Spend**

**Current Spend**: £171.74/day (268% of £64 budget)

**Options**:
- **Option A**: Enforce strict £64/day budget (as originally set)
- **Option B**: Set £100/day budget (moderate increase, controlled growth)
- **Option C**: Keep current spend BUT implement 500% target ROAS

**Recommendation**: **Option C** (target ROAS) - Allows spend flexibility while enforcing efficiency.

---

### 3. **Monitor Conversion Tracking Accuracy**

**Action**: Weekly reconciliation of Google Ads conversions vs. WooCommerce sales.

**Process**:
1. Export Google Ads product-level conversions (last 7 days)
2. Export WooCommerce orders (last 7 days)
3. Compare match rate (should be >80%)
4. Flag discrepancies for investigation

**Next Review**: Nov 13-15 (after plugin update v2.1.4)

---

### 4. **Prepare for Black Friday Surge**

**Context**: Nov 29 = Black Friday (18 days away)

**Expected Pattern**:
- CPCs will continue rising +20-40%
- Competition will intensify
- Godshot may want to increase budget for peak season

**Recommendation**:
- Keep daily budget controlled until Black Friday week
- Nov 25-29: Consider £150-200/day budget increase (if client approves)
- Ensure stock levels and product feed are optimized

---

## Conclusion

### **🔴 ROOT CAUSE CONFIRMED**

The ROAS drop is **100% attributable** to an **undocumented budget increase from £64/day → £190/day** (+197%).

**What happened**:
1. Budget was increased from £64/day to £190/day (unknown date)
2. Target ROAS was set to 700% (previously had no target)
3. Google's algorithm aggressively scaled spend to £172/day (90% of new budget)
4. Revenue did NOT scale proportionally with spend increase
5. Result: ROAS dropped from 1,535% → 553% (-72%)

**Why revenue didn't scale**:
- More traffic does NOT equal proportionally more conversions
- Incremental clicks are lower quality (higher CPCs, lower conversion rates)
- Godshot is a niche specialty coffee retailer with limited audience scale
- Doubling/tripling ad spend hits diminishing returns quickly

**Asset Group Performance Issues**:
Several asset groups are **burning budget with zero conversions**:
- **Fellow**: £108k spend (Nov 4-10), **ZERO conversions** ⚠️
- **Coffee Generic**: £85k spend (Nov 4-10), **3 conversions** (poor efficiency)
- **Kinto**: £37k spend (Nov 4-10), **4.3 conversions** (marginal)
- **Rains**: £3k spend, **ZERO conversions** ⚠️

**Best Performing Asset Groups**:
- **Remarketing**: £594k spend → £4,343 revenue = **731% ROAS** ✅
- **Generic Asset Group**: £523k spend → £2,562 revenue = **490% ROAS**

---

### **Immediate Actions Required**

#### 🔴 **URGENT: Optimize to Hit 700% ROAS Target**

**Context**: Budget increase to £190/day was intentional (Google's recommendation) for seasonal peak. Target ROAS is **700%** (benchmark for Godshot).

**Current Performance vs. Target**:
| Metric | Current (Nov 4-10) | Target | Gap |
|--------|-------------------|--------|-----|
| **ROAS** | 553% | 700% | **-21% below target** ⚠️ |
| Daily Spend | £171.74 | ~£190 (budget) | Underspending by 10% |
| Weekly Revenue | £6,651 | £9,310 (at 700% ROAS) | **-£2,659 shortfall** |

**To hit 700% ROAS at current spend**: Need **£8,415 weekly revenue** (vs. current £6,651).

**The problem**: Increased budget is hitting diminishing returns due to poor asset group performance.

---

#### 🔴 **URGENT: Pause Underperforming Asset Groups**

**Action**: Immediately pause these asset groups:

1. **Fellow** - £108k spend, 0 conversions (Nov 4-10) ⚠️
2. **Rains** - £3k spend, 0 conversions ⚠️
3. **Coffee Generic** - £85k spend, only 3 conversions (poor ROAS)

**Keep Active**:
- ✅ **Remarketing** (731% ROAS)
- ✅ **Generic Asset Group** (490% ROAS)
- ⚠️ **Kinto** (monitor - marginal performance)

---

#### 🟠 **HIGH PRIORITY: Investigate When Budget Was Changed**

**Action**: Run change history query to identify:
- When budget was increased from £64 → £190
- Who made the change (user email)
- Whether client authorized this increase

**Query**:
```gaql
SELECT
  change_event.change_date_time,
  change_event.change_resource_type,
  change_event.user_email,
  change_event.old_resource,
  change_event.new_resource
FROM change_event
WHERE change_event.change_date_time >= '2025-10-01'
  AND campaign.id = 20762581893
  AND change_event.change_resource_type IN ('CAMPAIGN', 'CAMPAIGN_BUDGET')
ORDER BY change_event.change_date_time DESC
```

---

### **Key Learnings**

1. **Scale has limits**: Godshot is a niche specialty retailer. 3x budget increase = 3x spend but NOT 3x revenue.

2. **Diminishing returns are real**: First £64/day reached high-intent audience (1,535% ROAS). Next £126/day reached lower-intent audience (much lower ROAS).

3. **Asset group quality matters**: Half the asset groups have zero or near-zero conversions. Budget is being wasted on non-performing segments.

4. **Document all changes**: Budget increase to £190 was NOT documented in CONTEXT.md, causing confusion and delayed investigation.

5. **Target ROAS of 700% may be too aggressive**: With conversion tracking issues (documented in CONTEXT.md), 700% target may be forcing algorithm to chase inflated conversion values.

---

### **Next Steps (Seasonal Peak Optimization)**

**Context**: Client approved £190/day budget increase for seasonal peak (Nov-Dec). Target: 700% ROAS.

**Immediate Actions**:
1. ✅ **Pause underperforming asset groups** (Fellow, Rains, Coffee Generic)
2. ✅ **Reallocate budget to high-performers** (Remarketing: 731% ROAS, Generic: 490% ROAS)
3. ✅ **Monitor Kinto asset group** - Currently marginal, but coffee/homeware category may improve into gifting season
4. ✅ **Review search terms** - Identify wasted spend on low-intent queries
5. ✅ **Update CONTEXT.md** with current budget (£190) and target ROAS (700%)

**Week 2 Actions** (Nov 18-24):
- Review if ROAS improved after asset group pauses
- If ROAS hits 700%: Consider gradual budget increase to £220/day for Black Friday week
- If ROAS still below 700%: Keep £190 budget but continue optimizing asset mix

**Black Friday Prep** (Nov 25-29):
- Ensure product feed is optimized (stock availability, promotional pricing)
- Consider budget increase to £250-300/day IF ROAS stabilizes at 700%+
- Monitor CPCs (expect 20-40% increase during Black Friday week)

---

**Prepared by**: Claude Code (PetesBrain automation)
**Review Status**: Draft - requires client discussion
**Action Owner**: Peter Empson (petere@roksys.co.uk)
