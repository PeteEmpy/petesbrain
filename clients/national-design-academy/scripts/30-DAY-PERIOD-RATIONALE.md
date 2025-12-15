# 30-Day Analysis Period - Rationale

**Date**: 12 December 2025
**Decision**: Use last 30 days (Nov 12 - Dec 12, 2025) with 2,000 minimum impressions

---

## Why 30 Days Instead of 90 Days?

### Problem with 90-Day Period

**90 days (Sep 14 - Dec 12) includes:**
- September: Back-to-school season (different intent patterns)
- October/November: Mid-semester (different search behavior)
- Early December: Pre-holiday period

**Issues:**
1. **Stale data** - Performance from 3 months ago may not reflect current state
2. **Seasonal drift** - Mixing different seasonal patterns reduces accuracy
3. **Campaign changes** - Budgets, audiences, and strategies may have changed
4. **Low signal** - 1,000 impressions over 90 days = only 11/day (too low)

### Benefits of 30-Day Period

**30 days (Nov 12 - Dec 12):**
- **Fresh data** - Recent performance is most actionable
- **Consistent season** - Single month reduces seasonal noise
- **Active assets only** - 2,000 impressions = ~67/day (ensures active testing)
- **Statistically valid** - 2,000 impressions can detect 30-50% CTR differences

---

## Statistical Validity

### Impression Requirements for CTR Comparison

To detect CTR differences with 95% confidence:

| CTR Difference | Impressions Needed |
|----------------|-------------------|
| 2% vs 4% (100% difference) | ~1,000 |
| 3% vs 4% (33% difference) | ~3,000 |
| 2.5% vs 3% (20% difference) | ~8,000 |

**Our threshold: 2,000 impressions**
- Can detect: 50%+ CTR differences (e.g., 2% vs 3%)
- Cannot detect: Small differences <20% (but these aren't worth optimizing anyway)

### Activity Requirement

**2,000 impressions over 30 days = ~67 impressions/day**

This ensures:
- Asset is actively serving (not dormant)
- Recent performance (not just historical)
- Sufficient daily volume for reliable CTR measurement

---

## Comparison of Options

| Option | Period | Min Impressions | Impressions/Day | Pros | Cons |
|--------|--------|-----------------|-----------------|------|------|
| **A (Chosen)** | 30 days | 2,000 | ~67/day | Fresh, statistically valid, active assets | Might miss low-volume underperformers |
| B | 60 days | 3,000 | ~50/day | More data, catches trends | Less fresh, includes older performance |
| C | 90 days | 5,000 | ~56/day | Maximum data | Stale data, seasonal mixing |

---

## Impact on Asset Selection

### Old Criteria (90 days, 1,000 impressions)
- **Lower bar** - Includes dormant/low-volume assets
- **More assets flagged** - But includes stale/irrelevant data
- **11 impressions/day** - Could include assets with intermittent serving

### New Criteria (30 days, 2,000 impressions)
- **Higher bar** - Only active, high-volume assets
- **Fewer assets flagged** - But each one is genuinely worth optimizing
- **67 impressions/day** - Ensures consistent, recent performance

---

## Expected Outcomes

**When we re-run `populate-by-asset-type.py`:**

1. **Fewer total assets flagged** - Because many won't meet 2,000 impressions in 30 days
2. **Higher quality selections** - Each flagged asset is genuinely underperforming
3. **More actionable insights** - Recent data = relevant to current state
4. **Better ROI on API costs** - Only generating alternatives for truly problematic assets

---

## Configuration

```python
# Date range for 30-day analysis (fresh, actionable data)
START_DATE = '2025-11-12'  # Last 30 days
END_DATE = '2025-12-12'

# Relative performance thresholds
MIN_IMPRESSIONS = 2000  # 2,000 impressions = ~67/day over 30 days
RELATIVE_CTR_THRESHOLD = 0.5  # Flag assets below 50% of group median CTR
```

**Adjustable per client:**
- High-volume accounts: Keep 2,000 or increase to 5,000
- Low-volume accounts: Decrease to 1,000 BUT extend period to 60 days
- More aggressive: Set threshold to 0.75 (75% of median)

---

## Future Considerations

### For Other Clients

**High-volume accounts (>100K impressions/month):**
```python
START_DATE = 30 days ago
MIN_IMPRESSIONS = 5000  # ~167/day
```

**Low-volume accounts (<20K impressions/month):**
```python
START_DATE = 60 days ago
MIN_IMPRESSIONS = 1000  # ~17/day
```

### Seasonal Businesses

For seasonal businesses (e.g., holiday products):
- Use **same period last year** as comparison
- Or use **30 days within peak season** only
- Avoid mixing on-season and off-season data

---

## Summary

**30 days + 2,000 impressions** strikes the optimal balance:
- ✅ Recent, actionable data
- ✅ Statistically valid CTR comparisons
- ✅ Active assets only (not dormant)
- ✅ Efficient use of Claude API costs
- ✅ Consistent seasonal context

**This is now the recommended standard for all PMax asset replacement projects.**
