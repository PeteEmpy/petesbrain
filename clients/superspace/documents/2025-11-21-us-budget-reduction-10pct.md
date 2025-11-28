# Superspace US Budget Reduction - 10% ROAS-Weighted

**Date:** 2025-11-21 08:37
**Requested by:** Craig Spencer
**Strategy:** ROAS-weighted reduction (Phase 2 of stock management)
**Total Reduction:** 10% (£1,156/day)

---

## Quick Reference - COPY FOR UI CHANGES

```
ACCOUNT: 7482100090

BUDGET CHANGES (Current → New):

1. Shopping Branded         £3,669 → £3,229  (-12%, ROAS 614%)
2. Shopping Brand Excluded  £2,613 → £2,352  (-10%, ROAS 654%)
3. P Max Brand Excluded     £3,121 → £2,809  (-10%, ROAS 781%)
4. Search Generics          £657   → £604    (-8%, ROAS 1072%)
5. Search Brand Inclusion   £1,493 → £1,403  (-6%, ROAS 2343%)

TOTAL: £11,568 → £10,397/day (-10.1%)
```

---

## Detailed Changes

| Campaign | Current | New | Cut | ROAS | Rationale |
|----------|---------|-----|-----|------|-----------|
| Shopping Branded | £3,669 | £3,229 | -12% | 614% | Lowest ROAS - larger cut |
| Shopping Brand Excluded | £2,613 | £2,352 | -10% | 654% | Below average ROAS |
| P Max Brand Excluded | £3,121 | £2,809 | -10% | 781% | Average performer |
| Search Generics | £657 | £604 | -8% | 1072% | Strong performer - protect |
| Search Brand Inclusion | £1,493 | £1,403 | -6% | 2343% | Top performer - protect most |

**Brand/Generic Balance:**
- Before: Brand 45% / Non-brand 55%
- After: Brand 44% / Non-brand 56%
- Balance maintained

---

## Context

- **Phase 1 (Nov 20):** 20% ROAS-weighted reduction (£14,460 → £11,568)
- **Phase 2 (Nov 21):** Additional 10% reduction (£11,568 → £10,397)
- **Reason:** US Christmas stock depleting faster than expected
- **Craig's request:** 10% now, another 10% on Monday (Nov 25)
- **Next review:** Monday Nov 25 for Phase 3 if needed

---

## Verification Query (GAQL)

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
- Shopping Branded: 3,229,000,000 micros (£3,229)
- P Max Brand Excluded: 2,809,000,000 micros (£2,809)
- Shopping Brand Excluded: 2,352,000,000 micros (£2,352)
- Search Brand Inclusion: 1,403,000,000 micros (£1,403)
- Search Generics: 604,000,000 micros (£604)
