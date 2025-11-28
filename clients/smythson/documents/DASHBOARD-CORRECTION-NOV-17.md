# Smythson Q4 Dashboard - Major Correction (Nov 17, 2025)

**Status:** ✅ COMPLETE
**Impact:** Significant revision to Q4 projections

---

## What Was Corrected

### Issue Identified
The dashboard was based on an incorrect assumption that P7 (October) had an underspend of £18,553 that would carry forward to P8 (November). In reality, P7 was bang on budget with no carryforward.

### Root Cause
- **Incorrect:** P7 budget £132,519, spent £113,966, rollover £18,553
- **Correct:** P7 budget £151,072, spent £151,072, NO rollover

---

## Budget Corrections

### P7 (Oct 29 - Nov 2)
- Budget: £132,519 → **£151,072** ✅
- Spend: £113,966 → **£151,072** (bang on budget) ✅
- Carryforward: £18,553 → **£0** ✅

### P8 (Nov 3-30)
- Budget: £204,604 → **£186,051** (-£18,553 no carryforward) ✅

### P9 (Dec 1-28)
- Budget: £183,929 (unchanged)
- **NEW:** Christmas delivery cutoff applied (Dec 22)
- Effective spending period: 21 days (not 31 days)
- Effective budget: **£122,598** (21 days × £5,838/day)

### Total Q4 Budget
- **Old:** £570,252
- **New:** £521,052 (P7: £151k + P8: £186k + P9: £184k)
- **Effective:** £459,721 (accounting for Dec 22 cutoff)

---

## Revenue Target Corrections

### November (P8) Targets - Recalculated
| Region | Old Target | New Target | Change |
|--------|-----------|-----------|---------|
| UK | £577,167 | **£491,175** | -£85,992 |
| USA | £354,227 | **£301,401** | -£52,826 |
| EUR | £122,446 | **£104,190** | -£18,256 |
| ROW | £65,596 | **£55,817** | -£9,779 |
| **TOTAL** | £1,119,436 | **£952,583** | **-£166,853** |

**Basis:** £186,051 budget at 512% ROAS (28 days)

### December (P9) Targets - Recalculated with Christmas Cutoff
| Region | Old Target | New Target | Change |
|--------|-----------|-----------|---------|
| UK | £485,564 | **£322,182** | -£163,382 |
| USA | £297,882 | **£201,380** | -£96,502 |
| EUR | £103,001 | **£68,628** | -£34,373 |
| ROW | £55,179 | **£34,965** | -£20,214 |
| **TOTAL** | £941,626 | **£627,155** | **-£314,471** |

**Basis:** £122,598 effective budget at 512% ROAS (21 days, Dec 22 cutoff)

---

## Q4 Overall Projection Impact

### Previous Understanding
- P7: £479,840 (421% ROAS)
- P8: £1,119,436
- P9: £941,626
- **Total: £2,540,902** (107% of £2.38M target) ✅

### Corrected Reality
- P7: £479,840 (318% ROAS - not 421%)
- P8: £952,583
- P9: £627,155 (Christmas cutoff applied)
- **Total: £2,059,578** (87% of £2.38M target) ⚠️

### Gap Analysis
- **Previous gap to target:** +£160k (exceeding target)
- **Corrected gap to target:** -£320k (13.5% short)
- **Swing:** £480k difference in projection

---

## Three Compounding Factors

### 1. No P7 Carryforward
- Lost £18,553 of expected P8 budget
- Impact: -£95k revenue at 512% ROAS

### 2. Lower P7 Baseline
- P7 ROAS was 318%, not 421%
- 24% weaker starting point than understood
- Requires larger seasonal uplift to hit targets

### 3. Christmas Delivery Cutoff
- December campaigns pause ~Dec 22
- Only 21 effective spending days (not 31)
- Lost £61k of planned December budget
- Impact: -£314k revenue

**Combined impact:** -£480k from previous projection

---

## Updated Dashboard Features

### Weighted Pacing for Spend
✅ Expected spend now uses weighted pacing (not linear)
✅ Accounts for Black Friday spikes, learning periods, phase transitions

### Christmas Delivery Cutoff
✅ December expected spend limited to 21 days
✅ Revenue targets reflect 21-day spending window
✅ Fallback multipliers updated (Dec 23-25: 0.1-0.3x)

### Regional Budget Allocations
✅ November: £186,051 split by region (44%/36%/14%/6%)
✅ December: £122,598 effective split (21 days only)
✅ All revenue targets recalculated from corrected budgets

---

## Files Updated

### 1. `update-q4-dashboard.py`
- Total Q4 budget: £570,252 → £521,052
- November revenue targets recalculated (all regions)
- December revenue targets recalculated (all regions)
- Christmas delivery cutoff constant added (`CHRISTMAS_DELIVERY_CUTOFF = Dec 22`)
- Effective December spend days: 21 (not 31)
- December spend calculations use `EFFECTIVE_DECEMBER_SPEND_DAYS`
- Fallback multipliers updated for Dec 23-25

### 2. `SMYTHSON-Q4-AUTHORITATIVE-FIGURES.md`
- P7 budget/spend corrected (£151,072 not £113,966)
- P8 budget corrected (£186,051 not £204,604)
- November revenue targets updated
- December revenue targets updated (with Christmas cutoff)
- Blended ROAS target updated (456% to 518% required)
- Budget constraint section rewritten (stretch → unrealistic)
- Added 3 compounding factors section

### 3. Dashboard Spreadsheet
✅ Script ran successfully (111 cells updated)
✅ All expected values now reflect corrected budgets
✅ Weighted pacing applied to both spend and revenue
✅ December calculations account for 21-day spending period

---

## Revised Q4 Assessment

### Client Target
£2,380,000 Google Ads demand

### Realistic Projection
£2,059,578 at 512% blended ROAS

**Gap:** £320,422 (13.5% short)

### Why This is Challenging
1. **P7 baseline:** 318% ROAS (weak starting point)
2. **Required uplift:** 61% ROAS improvement (318% → 512%)
3. **Budget constraint:** £459k effective (not £570k)
4. **Time constraint:** Christmas cutoff limits December to 21 days

### Achievability Assessment
- **Achievable:** £2,060k (87% of target)
- **Stretch:** £2,150k with exceptional Black Friday/Christmas
- **Client target (£2.38M):** Not realistic with current budget

### Required for Target
To hit £2,380,000 would require:
- 518% blended ROAS (63% above P7 baseline)
- Sustained exceptional performance throughout P8/P9
- OR additional £98k budget

---

## Next Steps

### Immediate
✅ Dashboard corrected and running daily at 7 AM
✅ All target values updated in spreadsheet
✅ Authoritative figures document updated

### Communication
- [ ] Discuss revised projections with client
- [ ] Set realistic expectation: £2,060k achievable
- [ ] Present options: accept gap OR add budget

### Monitoring
- Track actual vs. weighted expected (not linear)
- Focus on P8 Black Friday performance (critical period)
- Review Dec 1-10 to confirm seasonal uplift pattern

---

## Key Takeaways

1. **The target was based on incorrect budget assumptions**
   - No P7 carryforward changes everything
   - £49k less effective budget than expected

2. **Three factors compound the challenge**
   - No carryforward + weaker baseline + Christmas cutoff = -£480k

3. **Dashboard now reflects realistic expectations**
   - Weighted pacing for both spend and revenue
   - Christmas delivery cutoff properly accounted for
   - All calculations based on correct budgets

4. **Target requires discussion with client**
   - 13.5% gap is not insignificant
   - Performance can't bridge this gap alone
   - Budget increase OR revised target needed

---

**Document Created:** 2025-11-17
**Corrections Applied:** P7 budget, P8 budget, November targets, December targets, Christmas cutoff
**Dashboard Status:** ✅ Fully corrected and operational
