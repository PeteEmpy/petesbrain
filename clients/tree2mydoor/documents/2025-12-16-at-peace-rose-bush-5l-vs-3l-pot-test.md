# At Peace Rose Bush: 5L vs 3L Pot Variant Test

**Launch Date:** 16th December 2025
**Status:** Active
**Product:** At Peace Rose Bush
**Test Type:** Product Variant (Pot Size)

---

## Experiment Overview

Tree2mydoor is introducing a premium 5-litre pot variant of the "At Peace Rose Bush" alongside the existing 3-litre pot version. The 5L variant offers:
- Better quality (improved root structure)
- Higher price point
- Better product positioning

This document serves as a **baseline marker** to track the 5L variant's performance from launch date onwards.

---

## Product Details

### Control (Existing)
- **Product:** At Peace Rose Bush - 3L Pot
- **SKU:** TBC (to be confirmed from feed update)
- **Price:** TBC
- **Status:** Active since before Dec 2025

### Variant (New)
- **Product:** At Peace Rose Bush - 5L Pot
- **SKU:** **APRBG5W** ✓ Confirmed 16 Dec 2025
- **Price:** Higher than 3L (TBC)
- **Launch:** 16th December 2025

**Note:** A second rose variety may also receive a larger pot variant - to be confirmed by Ryan.

---

## Baseline Performance (30 Days Pre-Launch)

**Period:** 16th November 2025 - 15th December 2025
**Account-Wide Metrics** (all campaigns):

| Metric | Value |
|--------|-------|
| Impressions | 802,675 |
| Clicks | 9,208 |
| Conversions | 534.5 |
| Revenue | £9,869.48 |
| Spend | £7,179.72 |
| ROAS | 137% |
| CPA | £13.43 |
| CVR | 5.81% |

**Note:** Product-specific baseline for "At Peace Rose Bush - 3L" will be available once SKU is confirmed from Merchant Center feed.

---

## How to Analyse This Experiment

### Phase 1: Initial Launch (Dec 16 - Jan 15, 2026)
Allow 30 days for the 5L variant to accumulate data.

**Analysis Steps:**
1. Pull product-level performance from Google Ads Merchant Center reports
2. Filter by product title containing "At Peace Rose Bush"
3. Segment by SKU (3L vs 5L)
4. Compare:
   - Conversion rate
   - Average order value
   - ROAS
   - Total revenue contribution

### Phase 2: 90-Day Review (Dec 16, 2025 - Mar 16, 2026)
Assess whether the 5L variant is cannibalising 3L sales or expanding the market.

**Key Questions:**
- Did total "At Peace Rose Bush" revenue increase?
- What's the revenue split between 3L and 5L?
- Is 5L attracting a different customer segment?
- Does 5L have better profit margins despite higher price?

### Phase 3: Decision Point (After 90 Days)
Based on performance, decide:
- **Strong 5L performance:** Transition fully to 5L pots, phase out 3L
- **Both performing well:** Continue offering both variants
- **3L still dominant:** Keep 5L as premium option only

---

## GAQL Query for Future Analysis

**5L Variant SKU Confirmed:** APRBG5W

Use this query to compare 3L vs 5L performance:

```sql
SELECT
  segments.product_item_id,
  segments.product_title,
  metrics.clicks,
  metrics.impressions,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_micros
FROM shopping_performance_view
WHERE
  (segments.product_item_id = 'APRBG5W'
   OR segments.product_title LIKE '%At Peace Rose Bush%')
  AND segments.date >= '2025-12-16'
  AND segments.date <= 'YYYY-MM-DD'
ORDER BY segments.product_item_id, metrics.conversions_value DESC
```

**Quick 5L-only query:**
```sql
SELECT
  segments.product_item_id,
  segments.date,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_micros
FROM shopping_performance_view
WHERE
  segments.product_item_id = 'APRBG5W'
  AND segments.date >= '2025-12-16'
ORDER BY segments.date
```

Or use the Shopping Product Stats report in Google Ads UI:
- Go to Reports > Predefined reports > Shopping > Shopping Product Stats
- Filter: Product title contains "At Peace Rose Bush"
- Date range: 16th Dec 2025 onwards
- Split by Product Item ID

---

## Success Criteria (To Be Defined)

**Revenue Growth:**
- [ ] TBC - Define minimum revenue contribution for 5L variant
- [ ] TBC - Define acceptable 3L revenue retention level

**Performance Benchmarks:**
- [ ] TBC - 5L conversion rate target
- [ ] TBC - 5L ROAS target
- [ ] TBC - 5L average order value target

**Market Validation:**
- [ ] TBC - Minimum volume threshold to continue offering 5L

---

## Timeline

| Date | Event |
|------|-------|
| 16 Dec 2025 | Experiment documented (this file created) |
| 17 Dec 2025 | Expected: 5L variant appears in product feed |
| TBC | SKUs confirmed and documented |
| 15 Jan 2026 | 30-day initial review |
| 16 Mar 2026 | 90-day full analysis |

---

## Related Assets

**Campaign:** T2MD | P Max | HP&P 150 5/9 140 23/10 (ID: 15820346778)
**Asset Groups:**
- "Roses" (6450483755) - Main rose gifts collection
- "Fab Birthday Roses" (6449408517)
- "In Memoriam Roses" (6455482796)

**Product Feed:** Tree2mydoor Merchant Center (ID: TBC from CONTEXT.md)

---

## Notes

- Ryan (Collaber) will confirm the second rose variety receiving a larger pot
- This is a business-driven product test, not a formal Google Ads Experiment
- Analysis will be retrospective using date-based segmentation
- Feed updates typically occur daily around midnight

---

**Created:** 16th December 2025
**Last Updated:** 16th December 2025
**Next Review:** 15th January 2026
