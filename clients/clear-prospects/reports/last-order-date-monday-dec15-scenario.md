# Clear Prospects - Last Order Date: Monday Dec 15 Scenario

**Date**: December 16, 2025 (Tuesday)
**Scenario**: Last order date for Christmas delivery was **Monday, December 15 at 12 noon**

---

## 🚨 CRITICAL IMPLICATION

If the last order date was **Monday Dec 15**, then:

**TODAY (Tuesday Dec 16) onwards**, all orders will deliver **AFTER Christmas** (Dec 26+).

**Current deployment**:
- Phase 1 (Dec 15): £845/day ✓ DEPLOYED (within last order date window)
- **Phase 2 (Dec 16-19): £820/day** ← **CURRENTLY RUNNING**
- Phase 3 (Dec 20-25): £50/day

**The Problem**: Phase 2 is spending £820/day on **post-Christmas delivery only**.

---

## Timeline Analysis

### Monday 15th December (YESTERDAY)
- **Last order date**: 12 noon for next-day delivery (arrives Dec 16, well before Christmas)
- **Phase 1 deployed**: £845/day peak budget
- **Gift value**: FULL Christmas value ✅

### Tuesday 16th December (TODAY)
- **Orders placed today**: Next-day delivery = Wed Dec 17
- **Christmas is**: Thursday Dec 25 (8 days away)
- **Delivery window**: 8 days before Christmas
- **BUT**: Michael finishes Dec 19, staff finish Dec 23
- **Likely delivery**: Dec 26+ (post-Christmas)
- **Gift value**: ⚠️ **Post-Christmas delivery only**

**Current spend**: £820/day (BMPM paused, HSG/WBS at peak)

### Wednesday 17th - Friday 19th December
- **Phase 2 continues**: £820/day
- **Fulfillment capacity**: Reducing (Michael finishes Dec 19)
- **All orders**: Post-Christmas delivery
- **Gift value**: ⚠️ **Very low** (delayed giving, returns, New Year)

### Saturday 20th December onwards
- **Phase 3**: £50/day shutdown (staff finish Dec 23)
- **Minimal spend**: Keep campaigns warm only

---

## Impact by Brand (Last Order Date = Monday Dec 15)

### HappySnapGifts (HSG) - 🚨 CRITICAL IMPACT
- **Current Phase 2 budget**: £678/day
- **Product type**: Personalised photo gifts (Christmas-focused)
- **Value after last order date**:
  - **Pre-Christmas orders**: High value (gifts for Christmas Day)
  - **Post-Christmas orders**: Low value (delayed giving, returns, regifts)
  - **Estimated value drop**: 60-80%

**Implication**: Spending £678/day for 60-80% lower conversion value

### WheatyBags (WBS) - ⚠️ HIGH IMPACT
- **Current Phase 2 budget**: £543/day (£310 H&S + £233 other campaigns)
- **Product type**: Heat packs, therapeutic products
- **Value after last order date**:
  - **Pre-Christmas orders**: Medium-high (Christmas gifts)
  - **Post-Christmas orders**: Medium (still useful for winter, less time-sensitive than photo gifts)
  - **Estimated value drop**: 40-60%

**Implication**: Spending £543/day for 40-60% lower conversion value

### BMPM - ✅ NO IMPACT
- **Current Phase 2 budget**: £0/day (PAUSED)
- **Already paused** due to losses (drove -£290 in Dec 1-12)

---

## Financial Impact (Monday Dec 15 Last Order Date)

### If Phase 2 Continues at £820/day (Dec 16-19)

**Assumption**: Post-Christmas conversion value drops 50-70% vs pre-Christmas

| Scenario | Daily Spend | Expected ROAS | Daily Profit/Loss |
|----------|-------------|---------------|-------------------|
| **Pre-Christmas** (Dec 15) | £845 | 145% | +£380 profit |
| **Post-Christmas** (Dec 16-19) | £820 | 50-70% | **-£246 to -£410 loss/day** |

**Total Phase 2 loss (4 days)**: **-£984 to -£1,640**

### 2023 Data Context

From Christmas 2023 analysis:
- **Dec 20** (pre-shutdown): £577 spend, 105% ROAS (profitable)
- **Dec 21** (staff backlog): £47 spend, 135% ROAS (profitable but minimal spend)
- **Dec 24-25** (Christmas): £85 avg spend, 37% ROAS (**LOST £111**)

**Key insight**: Even Dec 20, 2023 was profitable at £577/day. But that was likely still within last order date window OR website messaging was effective.

---

## Revised Strategy Options (Last Order Date = Monday Dec 15)

### Option A: Immediate Phase 3 Deployment (TODAY) 🚨 URGENT

**Deploy Phase 3 NOW** (Tuesday Dec 16):
```bash
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv
```

**New timeline**:
- Phase 1: Dec 15 ✓ DEPLOYED
- ~~Phase 2: Dec 16-19~~ ❌ SKIP
- **Phase 3: Dec 16-25** ← **DEPLOY NOW** (£50/day)
- Phase 4: Dec 26-Jan 5 (£150/day)
- Phase 5: Jan 6+ (£439/day)

**Pros**:
- Stops potential losses immediately
- Aligns spend with post-Christmas value
- Keeps campaigns warm for Boxing Day

**Cons**:
- Loses potential post-Christmas orders (delayed giving, returns)
- No historical data for this scenario

### Option B: Create Phase 2B (Post-Last-Order Reduction)

**Create new CSV** for Dec 16-19 at **£200-300/day** (60-65% reduction):
- HSG: £135-200/day (70-80% reduction from £678)
- WBS: £108-163/day (60-70% reduction from £543)
- BMPM: £0/day (stays paused)

**Deploy immediately**:
```bash
# Create phase2b-post-last-order-dec16.csv
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase2b-post-last-order-dec16.csv
```

**New timeline**:
- Phase 1: Dec 15 ✓ DEPLOYED
- **Phase 2B: Dec 16-19** ← **DEPLOY NOW** (£200-300/day post-last-order)
- Phase 3: Dec 20-25 (£50/day shutdown)
- Phase 4: Dec 26-Jan 5 (£150/day)
- Phase 5: Jan 6+ (£439/day)

**Pros**:
- Balances risk vs opportunity
- Still captures post-Christmas orders
- Reduces potential losses

**Cons**:
- Still spending £200-300/day with uncertain ROAS

### Option C: Monitor Today (Dec 16), Decide Tomorrow

**Keep Phase 2 running today** (£820/day):
- Monitor conversion rates and ROAS closely
- If ROAS drops below 100% by end of day, deploy Phase 3 tomorrow (Dec 17)
- If ROAS stays above 120-130%, continue Phase 2

**Decision points**:
- **End of day Dec 16**: Check actual ROAS
  - If <100%: Deploy Phase 3 immediately (Dec 17-25)
  - If 100-120%: Deploy Phase 2B (reduced budget)
  - If >120%: Continue Phase 2 as planned

**Pros**:
- Data-driven decision based on actual performance
- Doesn't assume worst-case scenario

**Cons**:
- Risk of 1 day of losses (£820 spend)
- Delayed response

---

## Website Messaging Analysis

**Critical question**: Does Clear Prospects website clearly state:
- "Orders placed after [date] will deliver after Christmas"?
- Prominent placement (homepage, product pages, checkout)?
- Effective customer communication?

**If YES**:
- Customers self-select for post-Christmas delivery
- Phase 2 could continue (conversion rates may hold)
- Website manages expectations

**If NO**:
- Customers may not realise delivery timing
- Higher risk of cart abandonment and lower conversion rates
- Phase 2 continuation is riskier

---

## Recommendation

**Depends on website messaging**:

### Scenario A: Website HAS clear "post-Christmas delivery" messaging
**Recommended**: **Option C** (Monitor today, decide tomorrow)
- Give Phase 2 one day to prove itself
- Check ROAS end of day Tuesday Dec 16
- Deploy Phase 3 or Phase 2B tomorrow if needed

### Scenario B: Website LACKS clear messaging
**Recommended**: **Option A** (Immediate Phase 3 deployment)
- Deploy Phase 3 NOW (£50/day)
- Avoid potential losses
- Wait for Boxing Day recovery (Phase 4)

---

## Urgent Actions Required

1. **VERIFY last order date** - Was it Monday Dec 15? Or later?
2. **CHECK website messaging** - Is post-Christmas delivery clearly communicated?
3. **MONITOR Phase 2 performance** - Check ROAS for today (Dec 16) by 6pm
4. **PREPARE Phase 3 deployment** - Have command ready to execute if needed

---

## CSV Files Status

**Currently ready**:
- ✅ `phase3-shutdown-keep-warm-dec20.csv` (£50/day) - Ready to deploy
- ✅ `phase4-boxing-day-recovery-dec26.csv` (£150/day)
- ✅ `phase5-january-seasonal-jan6.csv` (£439/day)

**May need to create**:
- ❓ `phase2b-post-last-order-dec16.csv` (£200-300/day) - If monitoring shows partial value

---

**CRITICAL**: If last order date was Monday Dec 15, we are currently spending £820/day on post-Christmas delivery only. Need immediate decision on whether to continue or reduce.
