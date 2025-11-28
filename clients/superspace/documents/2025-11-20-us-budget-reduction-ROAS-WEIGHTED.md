# Superspace US Budget Reduction - ROAS-WEIGHTED STRATEGY

**Date:** 2025-11-20 09:05  
**Urgency:** HIGH - Stock depletion  
**Requested by:** Craig Spencer (Co-founder)  
**Strategy:** ROAS-weighted reduction + Pause underperformers  
**Total Reduction:** 20.0% (£2,892/day)  

---

## Executive Summary

**Current Total US Daily Budget:** £14,460/day  
**New Total After Optimization:** £11,568/day  
**Daily Savings:** £2,892/day (-20.0%)  

### Strategy Rationale

Rather than a flat 20% cut across all campaigns, we're using a **performance-weighted approach**:

✅ **Protect high performers** - Campaigns with ROAS >1000% get smaller cuts (12-17%)  
✅ **Cut harder from underperformers** - Campaigns with ROAS <700% get larger cuts (18-19%)  
✅ **Pause non-performers** - Demand Gen campaigns too new to evaluate (£450/day saved)  

This maintains your best revenue drivers while achieving the same 20% total reduction.

---

## ROAS Performance Analysis (Last 14 Days)

| Campaign | ROAS | Daily Budget | Cut % | Performance |
|----------|------|--------------|-------|-------------|
| **Search Brand Inclusion** | **2343%** | £1,700 | **12.2%** | ⭐⭐⭐ SUPERSTAR |
| **Search Generics** | **1072%** | £790 | **16.8%** | ⭐⭐ Excellent |
| **P Max Brand Excluded** | 781% | £3,800 | 17.9% | ⭐ Very Good |
| **Shopping Brand Excluded** | 654% | £3,200 | 18.3% | ✓ Good |
| **Shopping Branded** | 614% | £4,500 | 18.5% | ✓ Decent |
| Play House Test | 0% | £20 | 24.4% | ⚠️ No data |
| Demand Gen | N/A | £300 | **PAUSE** | Too new |
| Demand Gen Retargeting | N/A | £150 | **PAUSE** | Too new |

**Key Insight:** Search Brand Inclusion is your star performer at 2343% ROAS - we're protecting it with only a 12% cut vs 18-24% for others.

---

## Implementation Plan

### STEP 1: PAUSE DEMAND GEN CAMPAIGNS

**These campaigns were created Nov 17 - only 3 days old with no meaningful data yet.**

#### Campaign 1: SUP | US | Demand Gen 60 17/11
- **Current Budget:** £300/day
- **ACTION:** Set Status to **PAUSED**
- **Savings:** £300/day

#### Campaign 2: SUP | US | Demand Gen Retargeting 60 17/11
- **Current Budget:** £150/day
- **ACTION:** Set Status to **PAUSED**
- **Savings:** £150/day

**Total from pausing:** £450/day

---

### STEP 2: REDUCE BUDGETS ON 6 ACTIVE CAMPAIGNS

Listed from HIGHEST to LOWEST ROAS (protect the winners):

#### 1. SUP | US | Search | Brand Inclusion 21/5 550 15/7 incl removed 6/10 600 17/11
- **ROAS:** 2343% ⭐⭐⭐ (BEST PERFORMER)
- **Current:** £1,700/day
- **New:** £1,492.55/day (round to **£1,493**)
- **Cut:** £207.45/day (-12.2%)
- **Budget ID:** 12349718339

#### 2. SUP | US | Search | Generics 650 4/5 AI Max 3/7 Off 15/7 500 On 6/8 550 6/10 600 17/11
- **ROAS:** 1072% ⭐⭐
- **Current:** £790/day
- **New:** £657.18/day (round to **£657**)
- **Cut:** £132.82/day (-16.8%)
- **Budget ID:** 12362766610

#### 3. SUP | US | P Max 700 Brand Excluded 24/2 500 15/7 550 6/10 600 17/11
- **ROAS:** 781% ⭐
- **Current:** £3,800/day
- **New:** £3,121.02/day (round to **£3,121**)
- **Cut:** £678.98/day (-17.9%)
- **Budget ID:** 11914791987

#### 4. SUP | US | Shopping Brand Excluded 700 9/1 500 15/7 550 6/10 600 17/11
- **ROAS:** 654% ✓
- **Current:** £3,200/day
- **New:** £2,613.43/day (round to **£2,613**)
- **Cut:** £586.57/day (-18.3%)
- **Budget ID:** 14021953807

#### 5. SUP | US | Shopping Branded 500 15/7 550 6/10 600 17/11
- **ROAS:** 614% ✓
- **Current:** £4,500/day
- **New:** £3,668.70/day (round to **£3,669**)
- **Cut:** £831.30/day (-18.5%)
- **Budget ID:** 14412940053

#### 6. SUP | US | Search | Play House 40 Broad Test Recommendations trial
- **ROAS:** 0% ⚠️ (No spend/conversions)
- **Current:** £20/day
- **New:** £15.12/day (round to **£15**)
- **Cut:** £4.88/day (-24.4%)
- **Budget ID:** 11922350365

---

## Quick Reference Sheet

**COPY THIS TO KEEP OPEN WHILE MAKING CHANGES:**

```
ACCOUNT: 7482100090

PAUSE (Set Status = PAUSED):
- Demand Gen 60 17/11
- Demand Gen Retargeting 60 17/11

BUDGET CHANGES:
1. Search Brand Inclusion → £1,493    (was £1,700)  [ROAS 2343% - protect!]
2. Search Generics       → £657      (was £790)    [ROAS 1072%]
3. P Max Brand Excluded  → £3,121    (was £3,800)  [ROAS 781%]
4. Shopping Brand Excl   → £2,613    (was £3,200)  [ROAS 654%]
5. Shopping Branded      → £3,669    (was £4,500)  [ROAS 614%]
6. Play House Test       → £15       (was £20)     [ROAS 0%]
```

---

## Verification Query

After making changes, run this GAQL to verify:

```sql
SELECT 
  campaign.name,
  campaign.status,
  campaign_budget.amount_micros
FROM campaign 
WHERE campaign.name LIKE 'SUP | US%'
ORDER BY campaign_budget.amount_micros DESC
```

**Expected Results:**

| Campaign | Status | Amount (micros) | Daily (GBP) |
|----------|--------|-----------------|-------------|
| Shopping Branded | ENABLED | 3,669,000,000 | £3,669 |
| P Max Brand Excluded | ENABLED | 3,121,000,000 | £3,121 |
| Shopping Brand Excluded | ENABLED | 2,613,000,000 | £2,613 |
| Search Brand Inclusion | ENABLED | 1,493,000,000 | £1,493 |
| Search Generics | ENABLED | 657,000,000 | £657 |
| Play House Test | ENABLED | 15,000,000 | £15 |
| Demand Gen | **PAUSED** | 300,000,000 | £300 |
| Demand Gen Retargeting | **PAUSED** | 150,000,000 | £150 |

**Active budget total:** £11,568/day  
**Paused:** £450/day  
**Total savings:** £2,892/day (-20.0%)

---

## Why This Approach Is Better

### Flat 20% Cut (Original Plan):
- Search Brand Inclusion (2343% ROAS): Cut £340/day
- Shopping Branded (614% ROAS): Cut £900/day
- **Problem:** Cuts equally from your best and worst performers

### ROAS-Weighted Cut (New Plan):
- Search Brand Inclusion (2343% ROAS): Cut £207/day ✅ Protected
- Shopping Branded (614% ROAS): Cut £831/day ✅ Cut harder
- **Benefit:** Maintains your revenue engines while hitting same 20% total

**Net Effect:** Same £2,892/day savings, but preserves more high-ROAS traffic.

---

## Context & Rationale

**Reason for Change:**
- US Christmas stock selling faster than anticipated
- Tracking to be out of stock by next week (week of Nov 25)
- 20% reduction is Phase 1 of potential 40-50% total reduction over next 3-4 days

**Why Pause Demand Gen:**
- Campaigns only 3 days old (created Nov 17)
- No conversion data yet to evaluate performance
- £450/day budget better deployed elsewhere or saved
- Can re-enable once stock position stabilizes

**Why Budget Reduction vs ROAS Increase:**
- Budget cuts take effect within 2-3 hours
- Previous ROAS increase (550%→600% on Nov 17-18) takes 3-5 days to fully kick in
- Stock timeline requires immediate impact

**Client Communication:**
- Craig Spencer requested this via email Nov 20, 13:41
- Ant Erwin (Co-founder) CC'd on thread
- Asked for 20% now, potential 40-50% within 3-4 days

---

## Next Steps After Implementation

1. **Monitor Impact (Next 2-3 hours):**
   - Check spend levels drop by ~£2,300-2,500/day (80% budget deployment)
   - Verify ROAS remains strong on top performers

2. **Stock Depletion Tracking:**
   - Monitor daily sales rate vs stock levels
   - Prepare for Phase 2 (additional 20%) on Friday if needed

3. **Communication:**
   - Send confirmation email to Craig with:
     - New budget breakdown
     - ROAS performance context
     - Expected impact on stock runway
     - When to check back for Phase 2

4. **Documentation:**
   - Log to tasks-completed.md
   - Update CONTEXT.md
   - Add to experiment tracker

---

## Documentation Checklist

After implementation:

- [ ] Verify 2 campaigns paused (Demand Gen)
- [ ] Verify 6 budgets changed via GAQL query
- [ ] Total active budget = £11,568/day
- [ ] Log to `tasks-completed.md` with full ROAS context
- [ ] Update `CONTEXT.md` with Nov 20 ROAS-weighted strategy
- [ ] Log to `api-changes-log.json`
- [ ] Send confirmation email to Craig
- [ ] Add to `rok-experiments-client-notes.csv`
- [ ] Note Search Brand Inclusion as top performer (2343% ROAS)

---

**Implementation Window:** Now (Thu Nov 20, 9:00am)  
**Expected Completion:** 15-20 minutes  
**Verification:** GAQL query + spend monitoring  

---

**ROAS-weighted plan saved to:** `/tmp/superspace-roas-weighted-reduction.json`
