# Superspace US Budget Reduction - 10% Conversion Target

**Date:** 2025-11-24
**Requested by:** Craig Spencer
**Strategy:** ROAS-weighted reduction to achieve ~10% conversion reduction
**Total Daily Budget Reduction:** $1,438/day (-12.4%)

---

## Quick Reference - COPY FOR UI CHANGES

```
ACCOUNT: 7482100090

BUDGET CHANGES (Current → New):

1. Shopping Branded         $3,669 → $2,935  (-20%)
   Budget ID: 14412940053

2. P Max Brand Excluded     $3,121 → $2,809  (-10%)
   Budget ID: 11914791987

3. Shopping Brand Excluded  $2,613 → $2,221  (-15%)
   Budget ID: 14021953807

4. Search Brand Inclusion   $1,493 → $1,493  (no change)
   Budget ID: 12349718339

5. Search Generics          $657   → $657    (no change)
   Budget ID: 12362766610

TOTAL: $11,553 → $10,115/day (-12.4%)
```

---

## Detailed Changes

| Campaign | Current | New | Cut | ROAS (7d) | Rationale |
|----------|---------|-----|-----|-----------|-----------|
| Shopping Branded | $3,669 | $2,935 | -20% | 532% | Lowest ROAS - largest cut |
| Shopping Brand Excluded | $2,613 | $2,221 | -15% | 528% | Low ROAS - significant cut |
| P Max Brand Excluded | $3,121 | $2,809 | -10% | 693% | Mid ROAS - moderate cut |
| Search Brand Inclusion | $1,493 | $1,493 | 0% | 2846% | Top performer - protect |
| Search Generics | $657 | $657 | 0% | 1173% | Strong performer - protect |

---

## Expected Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Daily Budget | $11,553 | $10,115 | -12.4% |
| Daily Conversions | ~335 | ~300 | -10% |
| Daily Revenue | ~$136,000 | ~$125,000 | -8% |
| Blended ROAS | 949% | ~1,000%+ | Improved |

**Key Point:** Revenue drops less than conversions (-8% vs -10%) because we're cutting the least efficient spend first.

---

## Brand/Generic Balance

| Type | Before | After |
|------|--------|-------|
| Brand campaigns | 60% of conversions | ~58% |
| Generic campaigns | 40% of conversions | ~42% |

Balance maintained - slight shift toward generic where ROAS is stronger.

---

## Context

This is Phase 4 of the stock management response:

- **Phase 1 (Nov 17-18):** ROAS increased 550% → 600%
- **Phase 2 (Nov 20):** 20% ROAS-weighted reduction ($14,460 → $11,568)
- **Phase 3 (Nov 21):** Additional 10% reduction ($11,568 → $10,397 planned, but current shows $11,553)
- **Phase 4 (Nov 24):** 10% conversion reduction ($11,553 → $10,115)

**Reason:** US Christmas stock continues to deplete; Craig requested strategy to reduce conversions by 10% while maintaining ROAS and brand/generic balance.

---

## Verification Query (GAQL)

Run after changes to confirm:

```sql
SELECT
  campaign.name,
  campaign_budget.amount_micros
FROM campaign
WHERE campaign.name LIKE 'SUP | US%'
  AND campaign.status = 'ENABLED'
ORDER BY campaign_budget.amount_micros DESC
```

**Expected after changes:**
- Shopping Branded: 2,935,000,000 micros ($2,935)
- P Max Brand Excluded: 2,809,000,000 micros ($2,809)
- Shopping Brand Excluded: 2,221,000,000 micros ($2,221)
- Search Brand Inclusion: 1,493,000,000 micros ($1,493) - unchanged
- Search Generics: 657,000,000 micros ($657) - unchanged

---

## Implementation Status

- [x] Shopping Branded: $3,669 → $2,935 ✓
- [x] P Max Brand Excluded: $3,121 → $2,809 ✓
- [x] Shopping Brand Excluded: $2,613 → $2,221 ✓
- [x] Verified via GAQL query ✓
- [x] Logged to tasks-completed.md ✓

---

## Verification (Post-Implementation)

GAQL query confirmed new budgets (2025-11-24):

| Campaign | Budget (micros) | Budget ($) |
|----------|-----------------|------------|
| Shopping Branded | 2,935,000,000 | $2,935 ✓ |
| P Max Brand Excluded | 2,809,000,000 | $2,809 ✓ |
| Shopping Brand Excluded | 2,221,000,000 | $2,221 ✓ |
| Search Brand Inclusion | 1,492,550,000 | $1,493 (unchanged) |
| Search Generics | 657,180,000 | $657 (unchanged) |

**Total Daily Budget: $10,115** (down from $11,553)

---

## Document History

- **Nov 24, 2025:** Document created
- **Nov 24, 2025:** All budget changes implemented and verified via API

---

**Questions?** Contact Peter Empson (petere@roksys.co.uk)
