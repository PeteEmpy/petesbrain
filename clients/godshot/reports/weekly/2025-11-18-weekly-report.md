# Google Ads Weekly Report: Godshot
**Period:** Nov 12-18, 2025 (7 days)
**Generated:** 2025-11-19
**Campaign:** GOD | P Max 700

---

## Executive Summary

### Account Performance
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| **Spend** | £1,401.07 | £1,256.12 | **+11.5%** ⚠️ |
| **Conversions** | 111 | 120 | **-6.9%** ⚠️ |
| **Conv Value** | £7,481.80 | £7,847.82 | **-4.7%** ⚠️ |
| **ROAS** | **534%** | 625% | **-91pp** ⚠️ |
| **CPA** | £12.58 | £10.50 | **+19.8%** ⚠️ |
| **CTR** | 1.30% | 1.19% | +0.11pp ✓ |
| **Avg CPC** | £0.49 | £0.48 | +2.1% |
| **Impressions** | 218,991 | 217,680 | +0.6% |

**Key Takeaway:** ⚠️ **ROAS declining - spending more (+11.5%) but converting less (-6.9%), resulting in 534% ROAS vs 700% target (24% gap).**

---

## Campaign Breakdown

### Active Campaigns

**Single Campaign Structure:**
- GOD | P Max 700 (Performance Max)
- Target ROAS: 700%
- Actual ROAS: 534% (76% of target)
- Status: **Underperforming target by 166 percentage points**

| Campaign | Spend | Conv | Conv Value | ROAS | Clicks | CTR |
|----------|-------|------|------------|------|--------|-----|
| GOD \| P Max 700 | £1,401.07 | 111 | £7,481.80 | 534% | 2,838 | 1.30% |

---

## Performance Analysis

### Week-over-Week Trends

**Daily Breakdown (This Week):**
| Date | Spend | Conv | Conv Value | ROAS |
|------|-------|------|------------|------|
| Nov 12 | £162.83 | 12.9 | £1,138.33 | 699% ✓ |
| Nov 13 | £184.92 | 12.5 | £950.94 | 514% |
| Nov 14 | £159.04 | 14.5 | £1,164.03 | 732% ✓ |
| Nov 15 | £216.02 | 21.0 | £989.42 | 458% |
| Nov 16 | £217.15 | 14.6 | £803.13 | 370% ⚠️ |
| Nov 17 | £222.78 | 19.9 | £1,233.47 | 554% |
| Nov 18 | £238.32 | 16.0 | £1,202.47 | 505% |

**Observations:**
- Only 2 out of 7 days hit 700% ROAS target (Nov 12, Nov 14)
- Worst day: Nov 16 (370% ROAS - £217 spend with only £803 revenue)
- Best day: Nov 14 (732% ROAS)
- Pattern: Daily spend increasing (£163 → £238) but conversion efficiency declining
- No clear day-of-week pattern visible

---

## Root Cause Analysis

### Why ROAS Declined

**Problem:** Spend increased 11.5% but conversion value decreased 4.7%

**Likely Causes:**
1. **Budget Increase Without Algorithm Re-Learning**
   - Spend jumped from ~£180/day to ~£200/day
   - Algo may be expanding reach to lower-quality audiences
   - Typical Performance Max behavior when budget increases

2. **Conversion Tracking Issue Flagged**
   - CONTEXT.md notes recent conversion tracking fix (Nov 10)
   - Current week shows declining conversion rate
   - Need to verify WooCommerce plugin is still functioning correctly

3. **Asset Group Performance Variation**
   - Previous analysis (Nov 4-10) identified Fellow, Rains, Coffee Generic asset groups burning budget with minimal conversions
   - These may still be active and driving increased spend without proportional returns

4. **Seasonal Competition**
   - Entering peak coffee gifting season (Nov-Dec)
   - CPCs increased slightly (+2.1%)
   - More advertisers competing for same audience

---

## Prioritised Recommendations

### 1. ⚠️ **URGENT: Verify Conversion Tracking Accuracy**
**Issue:** ROAS dropped significantly week-over-week despite increased spend
**Impact:** May be missing conversions or tracking incorrectly (£366 gap in weekly revenue vs expected)
**Action:**
- Check WooCommerce Google Ads plugin is active and functioning
- Verify conversions in WooCommerce dashboard match Google Ads reported conversions
- Review conversion tracking setup from Nov 10 fix
- Look for any product ID mismatches (known issue from Oct/Nov)

**Expected Outcome:** If tracking is broken, fix will restore true ROAS visibility

---

### 2. ⚠️ **Review Asset Group Performance**
**Issue:** Previous week identified 3 asset groups (Fellow, Rains, Coffee Generic) with poor performance
**Impact:** These may be consuming 30-40% of daily budget with minimal returns
**Action:**
- Pull asset group performance report for Nov 12-18
- Identify which asset groups are driving conversions vs wasting spend
- Consider pausing underperforming asset groups
- Reallocate budget to winning products (likely Dak, Anglepoise based on previous data)

**Expected Outcome:** +10-15% ROAS improvement by eliminating waste

---

### 3. 🔍 **Consider Temporary Budget Reduction**
**Issue:** ROAS 24% below target (534% vs 700%), spend increased 11.5%
**Impact:** Current spend level appears above optimal efficiency point
**Action:**
- Test reducing daily budget from £200/day back to £180/day for 7 days
- Monitor if ROAS returns closer to 625% (last week's level)
- If ROAS improves, incrementally increase budget in £10/day steps

**Expected Outcome:** Return to 600%+ ROAS at slightly lower spend level

---

### 4. 📊 **Implement Weekly Performance Monitoring**
**Issue:** No systematic tracking of ROAS trends vs 700% target
**Impact:** React to problems rather than prevent them
**Action:**
- Use this weekly report format going forward
- Set alert: If ROAS <600% for 3 consecutive days, investigate immediately
- Track conversion tracking accuracy weekly
- Document any Google Ads optimizations in experiment log

**Expected Outcome:** Earlier detection of performance issues

---

## ROAS Gap Analysis

**Target:** 700% ROAS
**Actual:** 534% ROAS
**Gap:** **-166 percentage points** (24% below target)

**What This Means:**
- For every £1 spent, generating £5.34 revenue instead of target £7.00
- Weekly revenue shortfall: £2,330 (£700 × 7 days at target vs actual)
- Need £1.66 more revenue per £1 spend to hit target

**Path to 700% ROAS:**
Option A: Increase conversion value per conversion by 31% (£67.19 → £88.20 AOV)
Option B: Reduce spend by 24% while maintaining current conversion value
Option C: Increase conversion rate by 31% at current spend level

---

## Next Steps

**This Week (Nov 19-25):**
1. **Tuesday**: Verify conversion tracking accuracy (P0)
2. **Wednesday**: Pull asset group performance report
3. **Thursday**: Pause underperforming asset groups if identified
4. **Friday**: Review 3-day impact of changes

**Next Review:** Monday, Nov 25, 2025

---

## Data Notes

- ROAS calculated as: (Conversion Value / Spend) × 100
- "Week-over-week" compares Nov 12-18 vs Nov 5-11
- Single active campaign structure (Performance Max only)
- Manager Account: 2569949686
- Customer ID: 9922220205

---

**Report Status:** ✅ Phase 1A Test - Godshot
**Time to Generate:** ~5 minutes
**Actionable Insights:** 4 prioritized recommendations
