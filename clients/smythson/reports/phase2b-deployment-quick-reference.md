# Phase 2B Deployment Quick Reference
## Post Last Orders - Wednesday 17th December 8am

---

## Overview

**What:** Reduce US/EUR/ROW budgets to 70%, reallocate to UK
**When:** Wednesday 17th December 2025, 8am
**Why:** Last orders closed midnight 16th Dec for US/EUR/ROW
**Duration:** 6 days (Dec 17-22)

---

## Budget Changes

| Account | Phase 2A (Dec 15-16) | Phase 2B (Dec 17-22) | Change | % Change | Strategy |
|---------|---------------------|---------------------|--------|----------|----------|
| **UK**  | £3,050/day | £3,857/day | **+£807** | **+26%** | 🚀 BOOST (receives reallocation) |
| **USA** | £1,725/day | £1,208/day | **-£517** | **-30%** | 📉 REDUCE (last orders closed) |
| **EUR** | £690/day | £483/day | **-£207** | **-30%** | 📉 REDUCE (last orders closed) |
| **ROW** | £288/day | £202/day | **-£86** | **-30%** | 📉 REDUCE (last orders closed) |
| **TOTAL** | £5,750/day | £5,750/day | £0 | 0% | ✅ Maintained |

---

## Budget Reallocation Math

**Savings from US/EUR/ROW reduction:**
- USA: £1,725 → £1,208 = -£517
- EUR: £690 → £483 = -£207
- ROW: £288 → £202 = -£86
- **Total saved:** £810/day

**Allocated to UK:**
- UK: £3,050 → £3,857 = +£807

**Difference:** £3/day rounding

---

## Deployment Checklist

### Pre-Deployment (Evening Dec 16 or Morning Dec 17)

- [ ] Verify last orders closed at midnight 16th Dec
- [ ] Run deployment script: `/clients/smythson/scripts/deploy-phase2b-post-last-orders.py`
- [ ] Script will:
  - Query current state from all 4 accounts
  - Create backup: `backup-phase2b-post-last-orders-dec17.json`
  - Calculate exact budget changes needed
  - Wait for permission

### Deployment (8am Dec 17)

- [ ] Review backup file
- [ ] Choose allocation method:
  - Option A: Uniform 30% reduction across all campaigns
  - Option B: Performance-weighted (use Phase 2A weights)
- [ ] Execute budget changes via Google Ads API
- [ ] Verify changes applied correctly

### Post-Deployment

- [ ] Monitor performance first 24 hours
- [ ] Check UK is receiving increased traffic/conversions
- [ ] Verify US/EUR/ROW maintain acceptable ROAS at 70%
- [ ] Document actual performance vs projections

---

## Expected Performance

**Phase 2B Targets:**
- Daily spend: £5,750
- Expected ROAS: 600% (conservative, post-last-orders)
- Projected revenue: £34,500/day
- Total 6 days: £207,000 revenue on £34,500 spend

**Comparison to Phase 2A:**
- Phase 2A: 700% ROAS (all markets active)
- Phase 2B: 600% ROAS (international reduced, UK focused)
- Acceptable drop given international market closures

---

## Risk Mitigation

### UK Budget Increase (+26%)

**Risk:** Algorithm learning period from budget change
**Mitigation:**
- Increase is moderate (<50% threshold)
- UK market still taking orders (actual demand)
- Monitor ROAS impact over 24-48 hours

**Action if ROAS drops >20%:**
- Consider partial reversal (reduce increase to +15%)
- Wait additional 24 hours for algorithm stabilization

### US/EUR/ROW Budget Reduction (-30%)

**Risk:** Campaigns may still show for international traffic
**Mitigation:**
- 70% budget maintains presence (not paused)
- Matches reduced demand post last-orders
- Preserves account health

**Action if spend drops >50%:**
- Campaigns may be budget-limited too early in day
- Consider slight increase (to 75-80%)

---

## Key Files

**Deployment Script:**
`/clients/smythson/scripts/deploy-phase2b-post-last-orders.py`

**Implementation Plan:**
`/clients/smythson/reports/p9-budget-allocation-implementation-plan-dec15.md`

**Backup Location:**
`/clients/smythson/reports/backup-phase2b-post-last-orders-dec17.json`

---

## Contact & Escalation

**If issues arise:**
1. Check backup file can restore previous state
2. Verify total daily budget still equals £5,750
3. Monitor ROAS trends over 24-48 hours
4. Consider partial adjustment if performance drops >20%

**Peter availability:**
- Available throughout Dec 17-22 for monitoring
- Away Dec 27+ but taking computer (not off-grid)

---

## Next Phase

**Phase 3: Christmas Lull (Dec 23-25)**
- Deploy: Sunday Dec 22, 6pm
- Further reduce US/EUR/ROW (maintain 70% of Phase 2B)
- UK reduces slightly but maintains strong presence
- Total daily: £3,000/day

**Phase 4: Boxing Day (Dec 26)**
- Deploy: Wednesday Dec 25, 6pm
- MAXIMIZE all regions
- Total daily: £10,000 (single day)
- Projected 1,350% ROAS based on 2024 data
