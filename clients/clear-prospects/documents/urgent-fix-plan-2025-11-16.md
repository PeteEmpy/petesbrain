# Clear Prospects - Urgent Fix Plan
**Date**: 2025-11-16
**Status**: ALL THREE BRANDS UNDERPERFORMING - URGENT ACTION REQUIRED
**For**: Customer meeting tomorrow

---

## Executive Summary

**Last 7 Days Performance (Nov 9-15, 2025):**
- **Total Spend**: £2,800.72
- **Total Revenue**: £1,731.13
- **Total ROAS**: 62% ❌
- **Total Loss**: £1,069.59 (losing £153/day)

All three brands are significantly underperforming targets:
- **HappySnapGifts**: 68% ROAS (Target: 115%) - 47% below target
- **WheatyBags**: 72% ROAS (Target: 130%) - 58% below target
- **BMPM**: 14% ROAS (Target: 70%) - 56% below target, 4 days dry

---

## Root Cause Analysis

### PRIMARY ISSUE: Rank Lost Impression Share (Auction Position Problem)

**What the data shows:**
- HSG campaigns: **74-90% Rank Lost IS** - losing 3 out of 4 possible impressions
- WBS campaigns: **74-90% Rank Lost IS** - losing 3 out of 4 possible impressions
- BMPM campaigns: **90% Rank Lost IS** - losing 9 out of 10 possible impressions

**What this means:**
Google Smart Bidding has **dramatically reduced bids** because campaigns can't hit their ROAS targets. This creates a death spiral:

1. Campaign misses ROAS target
2. Smart Bidding lowers bids to improve efficiency
3. Lower bids = lose auctions = fewer impressions
4. Fewer impressions = fewer conversions
5. Fewer conversions = worse ROAS
6. **Cycle repeats and gets worse**

**Budget is NOT the problem** - most campaigns showing 0-12% Budget Lost IS. The problem is bid competitiveness.

---

## What Changed Recently?

### Nov 11, 2025 - Campaign Audit Implementation

**Changes made:**
1. ✅ Geographic targeting fix (PRESENCE vs PRESENCE_OR_INTEREST) - **This should help**
2. ❌ BMPM PMax target ROAS set to 70% - **This is actually a LOSS target** (spending £100 to make £70 = -30% loss)
3. ✅ WBS PMax H&S budget increased £120→£150/day - **This should help**
4. ⚠️ HSG campaigns consolidated - **May be causing learning period disruption**

**Timing correlation:**
- Changes implemented: Nov 11
- Performance decline visible: Nov 12-15
- **This suggests the changes triggered Smart Bidding learning period**, during which performance typically drops 10-20% for 7-14 days

---

## Immediate Fix Plan (Implement Tomorrow)

### Priority 1: Fix BMPM (Crisis Level)

**Current state:**
- BMPM P Max: £354 spend → £63 revenue (18% ROAS) 🚨
- BMPM Search: £91 spend → £0 revenue (0% ROAS) 🚨
- **Target ROAS: 70%** ← This is a loss target!
- 4 days without conversions

**Actions:**
1. **REMOVE 70% ROAS target from BMPM P Max** - set to "No target ROAS"
   - Why: 70% means losing 30p per £1. Smart Bidding won't spend if it can't hit target
   - Expected result: Algorithm will bid more aggressively, start spending budget

2. **Monitor for 3-5 days:**
   - If ROAS improves to 80-100%: Keep no target, let it run
   - If ROAS stays below 50%: Consider pausing BMPM entirely and focus budget on HSG/WBS

3. **Alternative**: Pause BMPM P Max entirely, redirect £50/day budget to HSG or WBS

**Expected impact**: Conversions should resume within 48 hours. Target break-even (100% ROAS) or better.

---

### Priority 2: Lower WBS ROAS Targets (Severe Underperformance)

**Current state:**
- WBS currently at 72% ROAS (Target: 130%) - missing by 58%
- All WBS campaigns showing 74-90% Rank Lost IS
- Budget increased on Nov 11 but not spending it (can't win auctions)

**Current ROAS targets:**
- WBS P Max H&S: 120% target (1.2)
- WBS Search: 110% target (1.1)
- WBS Villains: 120% target (1.2)
- WBS Zombies: 120% target (1.2)
- WBS Brand: 140% target (1.4)

**Actions:**
1. **Reduce all WBS P Max targets to 100% (1.0)** - break-even target
   - P Max H&S: 120% → **100%**
   - Villains: 120% → **100%**
   - Zombies: 120% → **100%**

2. **Reduce WBS Search targets:**
   - Main Wheat Bags Search: 110% → **100%**
   - Brand: Keep at 140% (only profitable campaign)

3. **Monitor for 7 days:**
   - Target: Get ROAS back to 90-100% range first
   - Once stable at break-even, gradually increase targets by 5% per week (100% → 105% → 110% → 115% → 120%)

**Expected impact**:
- Spend should increase 20-40% as bids become competitive
- ROAS should stabilize at 90-110% within 5-7 days
- Rank Lost IS should drop from 74-90% to 40-60%

---

### Priority 3: Lower HSG ROAS Targets (Moderate Underperformance)

**Current state:**
- HSG currently at 68% ROAS (Target: 115%) - missing by 47%
- All HSG campaigns showing 74-90% Rank Lost IS

**Current ROAS targets:**
- HSG P Max H&S: 120% target (1.2)
- HSG Villains: 130% target (1.3)
- HSG Zombies: 130% target (1.3)
- HSG Photo Face Mask Search: 130% target (1.3) ← Only campaign hitting target
- HSG Products Search: 120% target (1.2)
- HSG Brand: 140% target (1.4)

**Actions:**
1. **Reduce HSG P Max targets to 105% (1.05)** - modest profitability target
   - P Max H&S: 120% → **105%**
   - Villains: 130% → **105%**
   - Zombies: 130% → **105%**

2. **Reduce HSG Search targets:**
   - Photo Face Mask: **KEEP at 130%** (performing well at 120% actual)
   - Products: 120% → **105%**
   - Brand: **KEEP at 140%** (low volume, protect margin)

3. **Monitor for 7 days:**
   - Target: Get ROAS to 95-110% range
   - Once stable, gradually increase by 5% per week

**Expected impact**:
- Spend should increase 15-25%
- ROAS should stabilize at 95-110% within 5-7 days
- Face Mask campaign should maintain 120%+ performance

---

## Why Lower ROAS Targets?

**The counterintuitive truth about Google Smart Bidding:**

When campaigns can't hit their ROAS targets, Smart Bidding enters a **defensive mode**:
- Reduces bids to avoid "wasting" money on unprofitable clicks
- Lower bids = lose auctions = fewer impressions
- Fewer impressions = fewer conversions
- Fewer conversions = even harder to hit ROAS target
- **Death spiral continues**

**Lowering ROAS targets breaks the spiral:**
- Smart Bidding bids more aggressively (lower efficiency requirement)
- Higher bids = win more auctions = more impressions
- More impressions = more clicks = more conversions
- More conversions = more data for Smart Bidding to optimize
- **Performance improves, then gradually tighten targets**

**This is temporary**, not permanent:
1. Week 1: Lower targets to 100-105% (break-even to modest profit)
2. Week 2-3: Monitor, let Smart Bidding stabilize
3. Week 4+: Gradually increase targets by 5% per week until back at original levels
4. **Result**: Campaigns healthy again, hitting higher targets with volume

---

## Alternative Strategies to Consider

### Option A: Aggressive Reset (Recommended if immediate results needed)

**WBS:**
- Remove ALL ROAS targets temporarily (7 days)
- Let campaigns spend budget without efficiency constraints
- Monitor actual ROAS daily
- Re-add targets after 7 days at achieved ROAS level

**HSG:**
- Same approach but only on P Max campaigns
- Keep Search campaigns with reduced targets (105%)

**Pros**: Fastest recovery, high confidence in results
**Cons**: May overspend in first 2-3 days before Smart Bidding adjusts

---

### Option B: Conservative Reset (Lower risk)

**All brands:**
- Lower targets to break-even (100% ROAS)
- Monitor for 14 days
- Gradually increase by 5% per week

**Pros**: Lower risk of overspend, controlled approach
**Cons**: Slower recovery (2-3 weeks vs 1 week)

---

### Option C: Pause & Redirect (If fixes don't work)

**If ROAS doesn't improve within 7 days:**
1. Pause BMPM entirely
2. Redirect BMPM budget (£65/day) to:
   - WBS P Max H&S: +£35/day (£150 → £185)
   - HSG P Max H&S: +£30/day (£70 → £100)

**Why**: Focus budget on brands with conversion history rather than struggling BMPM

---

## Expected Timeline

### Days 1-2 (Nov 16-17)
- Implement ROAS target reductions
- BMPM: Remove target or pause
- Monitor spend levels (should increase 15-40%)
- Watch for conversion resumption

### Days 3-7 (Nov 18-22)
- Smart Bidding learning period
- ROAS should stabilize at 90-110% range
- Rank Lost IS should improve to 40-60%
- Daily losses should reduce from £153/day to £20-50/day (break-even zone)

### Days 8-14 (Nov 23-29)
- Performance stabilization
- If stable at 100-110% ROAS, begin gradual target increases
- First increase: 100% → 105% on best performers

### Week 3+ (Dec 1+)
- Continue gradual ROAS target increases (5% per week)
- Goal: Return to original targets (120-130%) with healthy volume

---

## Success Metrics

**Week 1 targets (by Nov 22):**
- Combined ROAS: **90-110%** (currently 62%)
- Daily spend: **Increase 20-30%** to £360-420/day (currently £280/day)
- Rank Lost IS: **Reduce to 40-60%** (currently 74-90%)
- BMPM: **Resume conversions** (currently 4 days dry)

**Week 2-3 targets (by Dec 6):**
- Combined ROAS: **100-115%**
- Daily losses: **£0-50/day** (currently £153/day loss)
- All campaigns spending budgets healthily

**Month-end target (by Dec 31):**
- HSG: **110-120% ROAS**
- WBS: **115-130% ROAS**
- BMPM: **Break-even or paused**

---

## Questions for Client Tomorrow

1. **Risk tolerance**: Are you comfortable with temporary lower ROAS (100-110%) to recover volume, or prefer slower conservative approach?

2. **BMPM strategy**: Should we:
   - Try to fix BMPM (remove target, monitor 7 days)?
   - Pause BMPM and redirect budget to HSG/WBS?
   - Keep trying but acknowledge it may stay unprofitable?

3. **Budget flexibility**: Can we temporarily increase budgets on HSG/WBS to capitalize on holiday season while we fix issues?

4. **Timeline expectations**: Are you OK with 2-3 week recovery period, or need faster results?

---

## Recommendation

**Implement Option A (Aggressive Reset) for WBS + BMPM:**
- These are in crisis mode (72% and 14% ROAS)
- Need immediate intervention
- Remove ROAS targets for 7 days, monitor actual performance
- Re-add targets at achieved levels

**Implement Option B (Conservative Reset) for HSG:**
- HSG less severe (68% ROAS)
- Lower targets to 105%, monitor 14 days
- Gradual recovery approach

**Monitor daily for first 3 days**, then weekly reviews.

**Expected result**:
- Week 1: ROAS improves to 90-110% range
- Week 2-3: ROAS stabilizes at break-even to modest profit
- Week 4+: Gradually tighten targets back to original levels
- **All brands profitable again by end of December**

---

## Next Steps

**Tomorrow (Nov 16):**
1. Present this plan to client
2. Get approval on approach (Option A, B, or C)
3. Implement ROAS target changes immediately after meeting
4. Set calendar reminder to check performance Mon Nov 18

**Mon Nov 18:**
- Review 2-day impact
- Check if conversions resumed (BMPM)
- Verify spend levels increasing

**Fri Nov 22:**
- Full week review
- Decide if further adjustments needed
- Plan for gradual ROAS target increases

---

**Document prepared by**: Peter Empson / Claude Code
**Date**: 2025-11-16
**Next review**: 2025-11-18
