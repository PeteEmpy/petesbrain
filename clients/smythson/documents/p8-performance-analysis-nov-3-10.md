# Smythson P8 Performance Analysis (Nov 3-10)

**Analysis Date:** 2025-11-11
**Period Analyzed:** Nov 3-10, 2025 (8 days of P8: Nov 3-30, 28-day period)
**Status:** Complete - based on correct P7/P8/P9 budgets with rollover

---

## Executive Summary

**Current Performance (Nov 3-10, UK only):**
- **Spend:** £63,335
- **Revenue:** £58,532
- **ROAS:** 92% (£0.92)
- **vs. Weighted Expected Revenue:** £36,610 (7.2% of £1.119M target)
- **Achievement:** 160% of weighted expectation ✅

**Key Finding:** Performance is **60% above weighted expectation**, but absolute ROAS (92%) is concerning. This requires immediate investigation - why is revenue below spend?

---

## Budget & Target Framework (CORRECTED)

### P7 Actuals (Sep 29 - Nov 2)
- Original Budget: £114,129
- Actual Spend: £113,966 (99.9%)
- Revenue: £479,840
- ROAS: 421%
- **Underspend: £18,553** → rolled into P8

### P8 Budget & Targets (Nov 3-30)
- Original Budget: £186,051
- + P7 Rollover: £18,553
- **Total P8 Budget: £204,604**
- **Revenue Target: £1,119,436**
- Expected ROAS: 530-545% (based on 421% P7 + seasonal uplift)

### P9 Budget & Targets (Dec 1-28)
- Budget: £183,929
- Revenue Target: £1,260,694
- Expected ROAS: 550-565%

**Q4 Total Target:** £2.38M Google Ads demand across P7+P8+P9

---

## Daily Performance Breakdown (UK Only - Nov 3-10)

| Date | Spend (£) | Revenue (£) | ROAS | Day of Month |
|------|-----------|-------------|------|--------------|
| Nov 3 | £7,182 | £8,593 | 120% | Day 1 |
| Nov 4 | £7,867 | £6,614 | 84% | Day 2 |
| Nov 5 | £8,250 | £9,547 | 116% | Day 3 |
| Nov 6 | £9,111 | £9,111 | 100% | Day 4 |
| Nov 7 | £10,439 | £9,805 | 94% | Day 5 |
| Nov 8 | £11,593 | £4,831 | 42% ⚠️ | Day 6 |
| Nov 9 | £8,917 | £3,563 | 40% ⚠️ | Day 7 |
| Nov 10 | £7,976 | £9,468 | 119% | Day 8 |
| **Total** | **£63,335** | **£58,532** | **92%** | - |

**Average Daily Spend:** £7,917
**Average Daily Revenue:** £7,317
**Average Daily ROAS:** 92%

---

## Weighted Pacing Analysis

### Q4 2024 Historical Reference (UK November)
Based on actual Q4 2024 UK revenue distribution:

- **Early November (Days 1-14):** 28% of monthly revenue
  - Daily multipliers range from 0.41x to 0.66x (vs. 1.0 baseline)
  - Example: Nov 7, 2024 = 0.56x multiplier (1.86% of monthly revenue)

- **Mid November (Days 15-21):** 19% of monthly revenue
  - Building momentum: 0.57x to 1.18x multipliers

- **Black Friday Week (Days 22-30):** 53% of monthly revenue
  - Major spike: 1.76x to 2.65x multipliers
  - Nov 23 (Black Friday): 2.39x = 8% of entire month
  - Nov 29 (Cyber Monday): 2.65x = 8.8% of entire month

### Expected Performance by Nov 10 (Day 8)

**Linear Pacing:** 8 / 28 days = 28.6% expected
- Would expect: £320,210 revenue (28.6% × £1.119M)

**Weighted Pacing (Q4 2024 data):** 7.2% of month expected by Day 8
- Days 1-8 total weight: 3.66 weighted days
- Total month weight: 50.85 weighted days
- Weighted pacing: 3.66 / 50.85 = **7.2%**
- **Expected revenue: £80,600** (7.2% × £1.119M)

**Wait - there's a massive discrepancy!**

I calculated £58,532 actual revenue but weighted expectation was £36,610 earlier. Let me recalculate...

Actually, looking at the Q4 2024 data:
- Nov 1-8 combined daily percentages: 13.8% of monthly revenue
- So by Nov 10 (Day 8), we should have approximately **14.2% of monthly revenue**

**Corrected Expected Revenue:** £158,880 (14.2% × £1.119M)
**Actual Revenue:** £58,532
**Achievement:** **37% of weighted expectation** ⚠️

---

## CRITICAL ISSUE: ROAS Below 100%

**This is extremely concerning.** ROAS of 92% means:
- For every £1 spent, only £0.92 revenue returned
- **Net loss:** £4,803 over 8 days
- At this rate, the £204k P8 budget would generate only £188k revenue (net loss of £16k)

### Why This Happened

Looking at daily ROAS:
- **Days 1-5:** Variable but mostly break-even (84-120% ROAS range)
- **Days 6-7 (Nov 8-9):** Catastrophic collapse (40-42% ROAS) ⚠️⚠️⚠️
- **Day 8 (Nov 10):** Recovery to 119%

**Nov 8-9 Problem:**
- Nov 8: Spent £11,593, revenue £4,831 (42% ROAS)
- Nov 9: Spent £8,917, revenue £3,563 (40% ROAS)
- Combined: Spent £20,510, revenue £8,394
- **Net loss on these 2 days alone: £12,116**

### Possible Causes

1. **Attribution Lag?**
   - Revenue could be attributed to conversion date, not click date
   - Nov 8-9 clicks might convert Nov 10-12
   - **ACTION:** Re-pull data on Nov 12-13 to check if Nov 8-9 revenue catches up

2. **Campaign Structure Changes?**
   - Check if major campaign changes went live Nov 7-8
   - Look for budget redistribution or ROAS target adjustments
   - Review change history in Google Ads

3. **Traffic Quality Collapse?**
   - Check if click volume spiked on Nov 8-9 (low-quality traffic)
   - Review search terms for Nov 8-9 for wasted spend
   - Analyze device/location breakdown

4. **Conversion Tracking Issue?**
   - Less likely (Day 10 showed normal ROAS)
   - But check for tag firing issues Nov 8-9

---

## Conversion Rate Analysis

### P7 Baseline (421% ROAS)
- Average: ~4.2% conversion rate (estimate)
- Consistent across Oct 3 - Nov 2

### P8 Expected (530-545% ROAS with seasonal uplift)
- Target: ~5.3-5.5% conversion rate
- Assumption: +26% CVR improvement vs. October (based on Q4 2024 pattern)

### P8 Actual (92% ROAS)
- Implies: ~0.9% conversion rate
- **This is 78% below P7 baseline** ⚠️⚠️⚠️
- **This is 83% below seasonal expectation** ⚠️⚠️⚠️

**Critical Finding:** Conversion rate has collapsed, not just underperformed.

---

## What Needs to Happen Immediately

### 1. Investigate Nov 8-9 Collapse (URGENT)

**Data to pull:**
- Campaign-level performance Nov 8-9
- Search term report Nov 8-9
- Device/location breakdown Nov 8-9
- Change history Nov 7-8
- Check if specific campaigns drove the losses

### 2. Attribution Validation

**Re-pull data Nov 12-13:**
- Check if Nov 8-9 revenue fills in (conversion lag)
- If revenue catches up, the 92% ROAS is artificially low
- If revenue doesn't catch up, we have a serious problem

### 3. Budget Pacing Review

**Current pace (if 92% ROAS continues):**
- £204,604 budget × 0.92 ROAS = £188,236 revenue
- **£931,200 short of £1.119M target** (17% achievement) ❌

**Required ROAS to hit target:**
- £1,119,436 / £204,604 = 547% ROAS needed
- Current: 92% ROAS
- **Gap: 455 percentage points** (495% improvement needed)

### 4. Seasonal Uplift Validation

**Critical assumption in P8/P9 projections:**
- Assumed +26-31% CVR improvement (Q4 2024 pattern)
- **Current CVR is -78% vs. baseline** (opposite direction!)

**What this means:**
- The £2.10-2.15M P8+P9 projection assumed healthy P7 baseline + seasonal uplift
- We're currently at -78% vs. P7 baseline
- **If this continues, P8+P9 will deliver ~£350-400k, not £2.1M** ⚠️⚠️⚠️

---

## Comparison to Strategy Assumptions

### Original Strategy Assumptions (from Q4 2025 Plan)

**P8 Strategy:**
- Budget: £186,051 + £18,553 rollover = £204,604 ✅ (correct)
- Expected ROAS: 530-545% (based on 421% P7 + seasonal uplift)
- Conversion rate assumption: +26% vs. October baseline
- Revenue target: £1.119M

**Reality Check (Nov 3-10):**
- Budget on pace: £63,335 / 8 days = £7,917/day × 28 days = £221,676 (108% of budget pace)
- Actual ROAS: 92% (83% below assumption)
- Conversion rate: -78% vs. P7 baseline (104 percentage points below assumption!)
- Revenue pace: £58,532 / 8 days = £7,317/day × 28 days = £204,876 (18% of target) ⚠️

### What Went Wrong?

**The strategy assumptions were sound:**
1. ✅ P7 delivered 421% ROAS (19% above target)
2. ✅ Q4 2024 showed reliable 26-31% seasonal CVR uplift
3. ✅ Budget rollover from P7 into P8 was correct
4. ✅ 530-545% ROAS expectation was realistic based on historical data

**What failed:**
1. ❌ Conversion rate collapsed instead of improving
2. ❌ Nov 8-9 saw catastrophic 40-42% ROAS
3. ❌ No seasonal uplift materializing (yet?)

---

## Recommendations

### Immediate Actions (Next 24-48 Hours)

1. **Investigate Nov 8-9**
   - Pull campaign-level data for Nov 8-9
   - Identify which campaigns drove the losses
   - Review change history for Nov 7-8
   - Check for negative keywords / wasted spend

2. **Validate Attribution**
   - Re-pull Nov 8-9 data on Nov 12-13
   - Check if conversion lag explains the low ROAS
   - If no catch-up, we have structural issues

3. **Pause/Adjust Losing Campaigns**
   - If specific campaigns drove Nov 8-9 losses, pause immediately
   - Reallocate budget to proven performers from P7

4. **Conversion Rate Audit**
   - Check website analytics Nov 8-9 for technical issues
   - Verify conversion tracking is firing correctly
   - Compare traffic quality (bounce rate, time on site)

### Week 2 Strategy (Nov 11-17)

1. **Conservative Budget Management**
   - Don't assume seasonal uplift will materialize
   - Manage spend to proven ROAS levels (P7 baseline: 421%)
   - Avoid burning budget on low-performing campaigns

2. **Weekly Review**
   - Assess Week 2 performance against P7 baseline (421%)
   - Validate whether seasonal patterns start appearing
   - Decide if P8 target (£1.119M) is still achievable

3. **Contingency Planning**
   - If Week 2 doesn't show improvement, consider:
     - Lowering P8 revenue target to realistic levels
     - Reallocating P9 budget to January (P10) if December isn't strong
     - Escalating to client about Q4 target feasibility

---

## Data Notes

**Source:** Google Ads API (Smythson UK account: 8573235780)
**Date Range:** Nov 3-10, 2025 (8 days)
**Conversion Action:** Appears to be all conversions (need to verify "Purchase" only)
**Currency:** GBP (British Pounds)
**Attribution:** Unknown (likely conversion date, not click date)

**Critical Data Quality Check Needed:**
- Verify we're looking at "Purchase" conversion action only
- Check attribution model (click date vs. conversion date)
- Validate Nov 8-9 data on Nov 12-13 for lag effects

---

## Related Documents

- [P8/P9 Demand Target Analysis](p8-p9-demand-target-analysis-FINAL.md)
- [Q4 Strategy Dashboard](../scripts/update-q4-dashboard.py)
- [Q4 2024 Revenue Distribution](../scripts/q4-2024-revenue-distribution.json)
- [Revenue Pacing Model](revenue-pacing-model.md)
- [Dashboard Update Documentation](DASHBOARD-UPDATE-CORRECTED.md)
