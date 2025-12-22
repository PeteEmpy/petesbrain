# Clear Prospects - Last Order Date Analysis

**Date**: December 16, 2025
**Issue**: Five-phase deployment doesn't account for last order dates for Christmas delivery

---

## The Problem

Current five-phase strategy assumes gift products (HSG/WBS) have full Christmas value through Dec 19. But customers can't receive orders placed after the **last order date** before Christmas (Dec 25).

This creates a gap period:
- **After last order date**: Orders still possible, but post-Christmas delivery only
- **Before shutdown**: Staff still available, fulfillment slower but possible
- **Current strategy**: No differentiation in spending during this period

---

## Key Dates & Constraints

### Business Calendar
- **Michael finishes**: Dec 19
- **Staff finish**: Dec 23
- **Christmas Day**: Dec 25
- **Reopening**: Jan 6, 2025

### Delivery Capabilities
- **Next-day delivery**: Order before 12 noon (HSG & WBS)
- **Standard delivery**: 2-3 working days

### Last Order Date Scenarios

| Scenario | Last Order Date | Rationale |
|----------|----------------|-----------|
| **Aggressive** | Dec 19 at 12 noon | Last day Michael is there, safe buffer |
| **Realistic** | Dec 20-21 | Staff still there but reduced capacity |
| **Latest Possible** | Dec 23 at 12 noon | Staff finish Dec 23, next-day delivery |

**Most likely**: Dec 19-20 (accounting for reduced capacity and holiday processing)

---

## Current Five-Phase Strategy (No Last Order Date Consideration)

| Phase | Dates | Daily Spend | Strategy |
|-------|-------|-------------|----------|
| Phase 1 | Dec 15 | £845 | ✓ DEPLOYED - Christmas peak |
| Phase 2 | Dec 16-19 | £820 | BMPM pause, HSG/WBS peak |
| Phase 3 | Dec 20-25 | £50 | Shutdown keep warm |
| Phase 4 | Dec 26-Jan 5 | £150 | Boxing Day recovery |
| Phase 5 | Jan 6+ | £439 | Seasonal budgets |

**Gap**: Phase 2 (Dec 16-19) doesn't differentiate between:
- **Before last order date** - Full Christmas gift value
- **After last order date** - Post-Christmas delivery only

---

## Impact by Brand

### HappySnapGifts (HSG) - High Impact ⚠️
- **Business Type**: Personalised photo gifts
- **Peak Season**: Christmas (highest gift-giving season)
- **Value Change**: After last order date, conversion value drops significantly
- **Current Phase 2 Budget**: £678/day
- **Recommendation**: Reduce post-last-order-date OR rely on website messaging

### WheatyBags (WBS) - Medium Impact ⚠️
- **Business Type**: Heat packs, therapeutic products
- **Peak Season**: Winter (pain relief, cold weather)
- **Value Change**: Less time-sensitive than HSG, but still gift-focused
- **Current Phase 2 Budget**: £543/day
- **Recommendation**: Moderate reduction post-last-order-date

### BMPM - No Impact ✅
- **Business Type**: B2B promotional merchandise
- **Peak Season**: Year-round (trade customers)
- **Value Change**: None - already PAUSED in Phase 2 due to losses
- **Current Phase 2 Budget**: £0/day (PAUSED)
- **Recommendation**: No change (already paused)

---

## Revised Strategy Options

### Option A: Six-Phase Deployment (Budget Reduction)

Add **Phase 2B** to handle post-last-order-date period:

| Phase | Dates | Daily Spend | Strategy |
|-------|-------|-------------|----------|
| Phase 1 | Dec 15 | £845 | ✓ DEPLOYED |
| **Phase 2A** | **Dec 16-19** | **£820** | **BMPM pause, HSG/WBS peak (BEFORE last order date)** |
| **Phase 2B** | **Dec 20** | **£300** | **Post-last-order reduction (60% cut on gifts)** |
| Phase 3 | Dec 21-25 | £50 | Shutdown keep warm |
| Phase 4 | Dec 26-Jan 5 | £150 | Boxing Day recovery |
| Phase 5 | Jan 6+ | £439 | Seasonal budgets |

**Phase 2B Budget Allocation** (£300/day):
- HSG: £204/day (30% of Phase 2A - £678 → £204)
- WBS: £96/day (30% of Phase 2A - £543 → £163)
- BMPM: £0/day (stays paused)

**Rationale**:
- Dec 20 is after Michael finishes (Dec 19)
- Staff still there but reduced capacity
- Website messaging about post-Christmas delivery
- Maintain some spend to capture delayed delivery orders

### Option B: Keep Current Strategy, Add Website Messaging

**No budget changes**, rely on:
- Clear website messaging: "Orders placed after Dec 19 will deliver after Christmas"
- Customer self-selection
- Accept potentially lower conversion rates Dec 20

**Pros**:
- Simpler deployment (5 phases instead of 6)
- Captures customers willing to order for post-Christmas delivery
- Based on 2023 data: Dec 20 had £577 spend at 105% ROAS (profitable)

**Cons**:
- Risk of wasted spend if conversion rates drop significantly
- No historical data for post-last-order-date performance

### Option C: Product Hero Segmentation

**Split campaigns by performance tier**:
- **Heroes & Sidekicks** (consistent converters): Maintain through Dec 20
- **Villains** (inconsistent): Reduce after Dec 19
- **Zombies** (weak): Pause after Dec 19

**Current campaign breakdown**:
- HSG H&S PMax (£510/day) - Mix of all tiers
- WBS H&S PMax (£310/day) - Mix of all tiers
- HSG/WBS Villains campaigns (£13-28/day each)
- HSG/WBS Zombies campaigns (£28-29/day each)

**Challenge**: Performance Max asset groups can't be split by product tier

---

## Recommendation

**Preferred: Option B (Keep Current Strategy + Website Messaging)**

**Reasoning**:
1. **2023 Data Shows Dec 20 Was Profitable**: £577 spend, 105% ROAS (before shutdown)
2. **Website Messaging Handles Self-Selection**: Customers aware of delivery dates
3. **Simpler Deployment**: 5 phases easier to manage than 6
4. **Post-Christmas Orders Still Valuable**: Gift returns, delayed giving, New Year gifts

**Required Action**:
- Confirm last order date with Michael (likely Dec 19 or Dec 20)
- Ensure website clearly displays "Orders after [date] deliver after Christmas"
- Monitor Dec 20 performance closely
- If ROAS drops below 100%, consider early Phase 3 deployment

**Fallback**:
If Dec 20 shows poor performance (ROAS <100%), deploy Phase 3 early:
```bash
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv
```

---

## Next Steps

1. **Confirm last order date** - Check with Michael or website
2. **Verify website messaging** - Ensure clear delivery warnings
3. **Monitor Dec 20 performance** - Watch ROAS closely
4. **Prepare Phase 2B CSV** (if needed) - Have fallback ready

---

**Current Status**: Five-phase strategy ready to deploy, but last order date consideration adds strategic context for Dec 20 decision.
