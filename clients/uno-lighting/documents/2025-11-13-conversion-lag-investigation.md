# Conversion Lag Investigation - Nov 13, 2025

## Trigger

User question: "Are we seeing any uptake in conversion rate over the last seven days against the previous that would mean we can implement the Q4 strategy to reduce target ROAS?"

## Initial Analysis (INCORRECT)

**Data pulled by click date:**
- Last 7 days (Nov 6-12): 1.64% CR, 137% ROAS
- Previous 7 days (Oct 30 - Nov 5): 1.93% CR, 207% ROAS
- **Conclusion**: Performance declining, DO NOT reduce ROAS

**Additional findings:**
- Impression share collapsed Nov 11-12 (47% → 10%)
- Rank lost IS spiked to 90% (Singles Day competition)
- Conversions down 25%

## User Insight

> "Can you take a look at the conversion values by time and the ROAS by time? See whether it's actually the time to purchase that's actually causing this perceived drop in conversion rate"

## Corrected Analysis (ACCURATE)

**Data pulled by conversion date:**

| Date | Conv (Click Date) | Conv (Conversion Date) | Lag % |
|------|------------------|----------------------|-------|
| Nov 12 | 11.94 | 15.00 | +26% |
| Nov 11 | 7.84 | 13.00 | +66% |
| Nov 10 | 15.65 | 16.00 | +2% |
| Nov 9 | 9.05 | 13.00 | +44% |

**Revised 7-day performance:**
- Last 7 days (Nov 6-12): **2.30% CR, 224% ROAS** ✅
- Previous 7 days: 2.05% CR, 202% ROAS
- **TRUE conclusion**: Performance IMPROVING (+12% CR, +11% ROAS)

## Key Finding

**Account experiences 1-2 day conversion lag:**
- 26-66% of conversions come 1-2 days after click
- Recent 2-3 days ALWAYS appear worse when analyzed by click date
- This is normal attribution pattern (customers research before purchasing)

## Metrics Used

**WRONG (for recent data):**
- `metrics.conversions` (attributes to click date)
- `metrics.conversions_value` (attributes to click date)

**CORRECT (for recent data):**
- `metrics.conversions_by_conversion_date` (attributes to purchase date)
- `metrics.conversions_value_by_conversion_date` (attributes to purchase date)

## Impact on Decision

**Original (incorrect) decision:** Hold ROAS, performance declining

**Revised (correct) decision:** Proceed with Q4 strategy, performance strong

## Budget Strategy Finding

**Separate finding during analysis:**
- Account currently NOT budget-limited (budget lost IS ~0%)
- Nov 11-12 impression share drop caused by rank (auction competition), not budget
- £500/day budget increase approved but should NOT be implemented yet
- **Trigger to implement**: Budget lost IS >10% OR peak demand hits current spend limits

## Actions Taken

1. ✅ Updated CONTEXT.md with conversion lag warning
2. ✅ Updated CONTEXT.md with budget strategy (hold until constraint appears)
3. ❌ Initially logged to experiment sheet (corrected - removed)
4. ✅ Created this analysis document

## Lesson Learned

**Always check conversion lag before drawing conclusions about recent performance.**

Use this query pattern for accurate recent performance:
```sql
SELECT
  segments.date,
  metrics.conversions,  -- Click date (for historical)
  metrics.conversions_by_conversion_date,  -- Conversion date (for recent)
  metrics.conversions_value,  -- Click date
  metrics.conversions_value_by_conversion_date  -- Conversion date
FROM customer
WHERE segments.date DURING LAST_14_DAYS
```

Compare both - if there's a large gap in recent days, data hasn't matured yet.
