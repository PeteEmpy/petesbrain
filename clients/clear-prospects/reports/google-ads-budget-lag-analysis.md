# Clear Prospects - Google Ads Budget Lag Analysis

**Date**: December 16, 2025
**Issue**: Google Ads doesn't instantly reduce spend when budgets are cut - is there sufficient buffer?

---

## The Budget Lag Problem

### Current Phase 2 → Phase 3 Transition
- **Phase 2**: £820/day (HSG £678, WBS £543, BMPM £0 paused)
- **Phase 3**: £50/day (HSG £27, WBS £22, BMPM £1)
- **Reduction**: 94% budget cut

**Problem**: Google Ads will NOT respect this immediately.

---

## Google Ads Budget Behavior

### Intraday Spend Patterns
When you deploy a budget change during the day:

**Morning deployment (9am)**:
- Google may have already spent 30-40% of original daily budget
- Example: £820/day budget → £250-330 already spent by 9am
- New £50/day budget doesn't stop existing ad delivery immediately

**Expected actual spend on deployment day**: £150-250 (not £50)

### Pacing Adjustment Period
Google Ads algorithm needs 24-48 hours to fully adjust to new budgets:

| Timeframe | Expected Behavior |
|-----------|-------------------|
| **Deployment day** | 40-60% of old budget (£330-490) |
| **Day 2** | 20-30% of old budget (£160-250) |
| **Day 3+** | Reaches target budget (£50) |

### 2x Daily Budget Rule
Google can overspend daily budgets by up to **2x on individual days** (though it balances over the month):
- Daily budget: £50
- Potential actual spend: £100 (on some days)

---

## Impact on Five-Phase Strategy

### SCENARIO A: Last Order Date = Monday Dec 15 (Already Passed)

**If we deploy Phase 3 on Tuesday Dec 16 at 9am**:

| Date | Target Budget | Likely Actual Spend | Overspend |
|------|---------------|---------------------|-----------|
| Tue Dec 16 | £50 | £250-350 | +£200-300 |
| Wed Dec 17 | £50 | £120-180 | +£70-130 |
| Thu Dec 18 | £50 | £60-80 | +£10-30 |
| Fri Dec 19 | £50 | £50-60 | £0-10 |

**Total Phase 3 (Dec 16-19)**:
- **Target**: £200 (4 days × £50)
- **Likely actual**: £480-670
- **Overspend**: £280-470

**Plus Phase 3 continues Dec 20-25** (6 more days):
- **Target**: £300 (6 days × £50)
- **Likely actual**: £300-360 (should stabilize by then)

**Total shutdown period overspend**: £280-470 over 10 days

---

## Is There Sufficient Buffer?

### Original Five-Phase Budget Projection

| Phase | Duration | Daily Target | Total Budget |
|-------|----------|--------------|--------------|
| Phase 1 | 1 day | £845 | £845 |
| Phase 2 | 4 days | £820 | £3,280 |
| Phase 3 | 6 days | £50 | £300 |
| Phase 4 | 11 days | £150 | £1,650 |
| Phase 5 | 25 days | £439 | £10,975 |
| **TOTAL** | **47 days** | - | **£17,050** |

**Average daily**: £363/day

### Revised with Google Ads Lag (Worst Case)

| Phase | Duration | Target Budget | Likely Actual | Overspend |
|-------|----------|---------------|---------------|-----------|
| Phase 1 | 1 day | £845 | £845 | £0 |
| Phase 2 | 4 days | £3,280 | £3,280 | £0 |
| **Phase 3** | **10 days** | **£500** | **£800-980** | **£300-480** |
| Phase 4 | 11 days | £1,650 | £1,650-1,800 | £0-150 |
| Phase 5 | 25 days | £10,975 | £10,975 | £0 |
| **TOTAL** | **47 days** | **£17,050** | **£17,550-17,905** | **£500-855** |

**Overspend impact**: +3-5% over entire period

**Answer**: Yes, there's buffer in the overall strategy, BUT:
- Overspend happens during shutdown period (when we want minimal spend)
- Defeats the purpose of Phase 3 if we spend £800-980 instead of £500
- Post-last-order-date overspend on low-value orders

---

## Solutions to Minimize Lag

### Option 1: PAUSE Instead of Budget Reduction (Immediate Stop) ✅ RECOMMENDED

**For post-last-order-date scenario**:
Instead of reducing budgets to £50/day, **PAUSE all campaigns immediately**.

**Advantages**:
- ✅ Instant stop (within minutes)
- ✅ No gradual wind-down period
- ✅ No overspend lag
- ✅ Can ENABLE campaigns for Phase 4 (Boxing Day recovery)

**Disadvantages**:
- ⚠️ Campaigns lose "warmth" (learning data)
- ⚠️ May take 24-48 hours to ramp back up in Phase 4
- ⚠️ Potential impact on Quality Score

**CSV modification**:
Change Phase 3 CSV from:
```
21730574366,CPL | HSG | P Max | All | H&S,510.00,20.46,BUDGET_CHANGE
```

To:
```
21730574366,CPL | HSG | P Max | All | H&S,510.00,0.00,PAUSE
```

### Option 2: Late-Night Deployment (Minimize Next-Day Impact)

**Deploy Phase 3 at 11pm** instead of 9am:
- Google has already spent most of the day's budget
- Next day starts fresh with new £50/day budget
- Reduces overspend from £280-470 to £100-150

**Advantages**:
- ✅ Reduces lag impact by 60-70%
- ✅ Campaigns stay "warm"
- ✅ Simpler than creating intermediate phases

**Disadvantages**:
- ⚠️ Still some overspend on deployment day
- ⚠️ Requires out-of-hours deployment

### Option 3: Gradual Step-Down (Phase 2B + Phase 2C)

**Create intermediate phases**:
- **Phase 2B** (Day 1): £400/day (50% reduction)
- **Phase 2C** (Day 2): £200/day (75% reduction)
- **Phase 3** (Day 3+): £50/day (94% reduction)

**Advantages**:
- ✅ Google algorithm adjusts more smoothly
- ✅ Predictable spend patterns
- ✅ Maintains some campaign warmth

**Disadvantages**:
- ⚠️ Still spending £600-800 over 2 days on post-Christmas delivery
- ⚠️ More complex deployment (3 CSV files instead of 1)
- ⚠️ Delays reaching target £50/day budget

### Option 4: Accept Overspend (Build into Strategy)

**Acknowledge the lag** and plan for it:
- Phase 3 target: £50/day
- Phase 3 likely actual: £80-100/day (averaged over 10 days)
- Total overspend: £300-500

**Advantages**:
- ✅ Realistic expectations
- ✅ No additional deployment complexity
- ✅ Campaigns stay warm for Phase 4

**Disadvantages**:
- ⚠️ Wasted spend during shutdown period
- ⚠️ Post-last-order-date inefficiency

---

## Recommendation by Scenario

### SCENARIO A: Last Order Date Has PASSED (Dec 15 or earlier)

**Recommended**: **Option 1 - PAUSE campaigns immediately**

**Reasoning**:
- We're already past last order date
- Gift products have minimal value (post-Christmas delivery)
- Every day of overspend is wasted money
- Can restart campaigns for Boxing Day (Phase 4, Dec 26)

**Action**:
1. Create `phase3-shutdown-PAUSE-dec16.csv` (all campaigns PAUSED)
2. Deploy immediately
3. Restart campaigns Dec 26 with Phase 4 budgets

**New Phase 3 timeline**:
- Dec 16-25: ALL CAMPAIGNS PAUSED (£0/day actual)
- Dec 26: ENABLE campaigns with Phase 4 budgets (£150/day)

### SCENARIO B: Last Order Date = Dec 18-19 (Still Within Window)

**Recommended**: **Option 2 - Late-night deployment**

**Reasoning**:
- Still valuable to keep campaigns running through last order date
- Minimize overspend AFTER last order date
- Simpler than gradual step-down

**Action**:
1. Continue Phase 2 (£820/day) through last order date
2. Deploy Phase 3 at **11pm on last order date**
3. Next morning starts with £50/day budgets

**Example** (if last order date = Dec 18):
- Dec 16-18: Phase 2 (£820/day)
- Dec 18 at 11pm: Deploy Phase 3
- Dec 19-25: Phase 3 (£50/day, minimal lag)

### SCENARIO C: Last Order Date = Dec 20+ (Late)

**Recommended**: **Option 4 - Accept overspend**

**Reasoning**:
- Original five-phase timing is correct
- Overspend is minimal in context of overall strategy
- No need to complicate deployment

**Action**:
- Continue with original five-phase deployment
- Expect Phase 3 to spend £80-100/day instead of £50/day
- Total impact: £300-500 overspend (within acceptable range)

---

## Updated CSV Files Needed

### If PAUSE Strategy (Scenario A)

**Create**: `phase3-shutdown-PAUSE-dec16.csv`

**Content**:
```csv
customer_id,manager_id,campaign_id,campaign_name,current_budget_gbp,new_budget_gbp,action
6281395727,,21173762063,CPL | BMPM | P Max Shopping,15.00,0.00,PAUSE
6281395727,,384585297,CPL | BMPM | Search | Promotional Merchandise,10.00,0.00,PAUSE
6281395727,,211394337,CPL | HSG | Search | Brand,20.00,0.00,PAUSE
... (all 13 campaigns)
```

**Then create**: `phase4-boxing-day-ENABLE-dec26.csv`

**Content**: Same as current Phase 4, but change action to ENABLE + budget change

---

## Summary: Budget Lag Impact

| Scenario | Deployment Strategy | Expected Overspend | Acceptable? |
|----------|---------------------|-------------------|-------------|
| **Last order date passed** | PAUSE immediately | £0 (instant stop) | ✅ YES |
| **Last order date Dec 18-19** | Late-night deploy | £100-150 (minimal) | ✅ YES |
| **Last order date Dec 20+** | Accept lag | £300-500 (over 47 days) | ✅ YES |

**Overall answer**: **YES, there's sufficient buffer**, but strategy should be adjusted based on last order date to minimize waste:

- **Post-last-order-date**: PAUSE campaigns (no lag)
- **Within last order window**: Late-night deployment (minimal lag)
- **Original timing correct**: Accept overspend (acceptable in context)

---

**Next Step**: Wait for Michael's response to determine which strategy to deploy.
