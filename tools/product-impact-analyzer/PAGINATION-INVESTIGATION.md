# GAQL Pagination Investigation - Oct 31, 2025

## Problem

Large Google Ads accounts (Accessories for the Home, Uno Lights, Clear Prospects) exceed the 25,000 token limit when fetching product labels via MCP.

**Example failures:**
- AFH (7972994730): 52,543 tokens
- Uno Lights (6413338364): 54,993 tokens
- Clear Prospects (6281395727): 190,783 tokens

## Attempted Solutions

### 1. OFFSET-based Pagination ❌

**Attempt:**
```sql
SELECT segments.product_item_id, segments.product_custom_attribute0
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS AND metrics.impressions > 0
LIMIT 500 OFFSET 500
```

**Result:** GAQL error: "unexpected input OFFSET"

**Conclusion:** GAQL does not support OFFSET

---

### 2. Comparison Operator Pagination ❌

**Attempt:**
```sql
SELECT segments.product_item_id, segments.product_custom_attribute0
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS
  AND metrics.impressions > 0
  AND segments.product_item_id > '2042'
ORDER BY segments.product_item_id
LIMIT 500
```

**Result:** GAQL error: "> is not a valid operator to use with 'segments.product_item_id'"

**Valid operators:** =, !=, LIKE, NOT LIKE, IN, NOT IN, IS NULL, IS NOT NULL, REGEXP_MATCH, NOT REGEXP_MATCH

**Conclusion:** Cannot use WHERE product_item_id > 'last_id' for pagination

---

### 3. Reduced Date Range ❌

**Attempt:**
```sql
SELECT segments.product_item_id, segments.product_custom_attribute0
FROM shopping_performance_view
WHERE segments.date DURING LAST_3_DAYS AND metrics.impressions > 0
LIMIT 10000
```

**Result:** GAQL error: "Invalid date literal supplied for DURING operator: LAST_3_DAYS"

**Valid DURING values:** LAST_7_DAYS, LAST_14_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH, etc.

**With LAST_14_DAYS:** Still 58,524 tokens (exceeds limit)

**Conclusion:** Date range reduction insufficient for large accounts

---

## Working Solution

### Partial Coverage with LIMIT ✅

**Approach:**
```sql
SELECT segments.product_item_id, segments.product_custom_attribute0
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS AND metrics.impressions > 0
ORDER BY segments.product_item_id
LIMIT 500
```

**Result:**
- Successfully fetches first 500 products (alphabetically)
- Response size: ~10,000-15,000 tokens (well under limit)
- Products: 1004, 1048, 1055... 2042 (alphabetical order)

**Pros:**
- Works within token limits
- Enables transition tracking for covered products
- Provides representative sample

**Cons:**
- Misses products later in alphabetical order
- ~500 of potentially 1000+ products tracked

**Partial coverage better than no coverage**

---

## Alternative Approaches (Not Implemented)

### A. Sampled Tracking

Track different product batches on different days using IN operator:

**Day 1:** Products starting with 0-4
```sql
WHERE segments.product_item_id IN ('0%', '1%', '2%', '3%', '4%')
```

**Day 2:** Products starting with 5-9, A-M

**Day 3:** Products starting with N-Z

**Pros:** Full coverage over 3 days
**Cons:** Complex scheduling, delayed complete snapshot

---

### B. Aggregate Tracking

Query counts by label instead of product-level detail:

```sql
SELECT
  segments.product_custom_attribute0 as label,
  COUNT(DISTINCT segments.product_item_id) as product_count
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS AND metrics.impressions > 0
GROUP BY segments.product_custom_attribute0
```

**Pros:** Always fits in token limit, shows distribution
**Cons:** Loses product-level transitions

---

## Implementation Decision

**Chosen:** Partial Coverage with LIMIT 500

**Rationale:**
1. Simple implementation
2. Works immediately without complex scheduling
3. Provides ~50% coverage for large accounts (better than 0%)
4. Transition tracking still valuable even if partial
5. Can be enhanced later with sampled tracking if needed

**Updated Code:**
- `label_tracking_executor.py`: Uses LIMIT 500 by default
- `LABEL-TRACKING-COMPLETE.md`: Documents limitations
- Large accounts tracked with partial coverage noted

---

## GAQL Limitations Summary

**What GAQL Doesn't Support:**
- ❌ OFFSET clause
- ❌ Comparison operators (>, <, >=, <=) on most fields
- ❌ Cursor-based pagination
- ❌ SKIP/TAKE patterns
- ❌ Subqueries for pagination

**What GAQL Does Support:**
- ✅ LIMIT (but fetches all, returns subset - doesn't help token limit)
- ✅ ORDER BY (determines which subset LIMIT returns)
- ✅ IN operator (can filter to product ID subsets)
- ✅ REGEXP_MATCH (can pattern-match product IDs)

---

## Token Limit Breakdown

Based on testing with AFH (7972994730):

| Query Type | Products | Tokens | Status |
|------------|----------|--------|--------|
| LIMIT 10000 | ~1000 | 52,543 | ❌ Exceeds 25K |
| LIMIT 2000 | ~1000 | 52,543 | ❌ Exceeds 25K (still fetches all) |
| LIMIT 500 + ORDER BY | 500 | ~12,000 | ✅ Within limit |

**Key insight:** LIMIT without ORDER BY doesn't reduce API response size. LIMIT + ORDER BY returns first N sorted results, which does fit within token limit.

---

## Future Enhancements

If full coverage becomes critical:

1. **Implement sampled tracking** (3-day rotation)
2. **Use REGEXP_MATCH** to filter product IDs by pattern
3. **Aggregate tracking** for high-level monitoring
4. **Separate MCP calls** per product category (if categories defined)

**Current status:** Partial coverage sufficient for transition detection and validation purposes.

---

**Investigation Date:** October 31, 2025
**Investigated By:** Claude Code (Sonnet 4.5)
**Documented For:** ROK Systems Product Hero Label Tracking System
