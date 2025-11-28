# Product Hero Label Tracking

**Created:** 2025-10-31
**Status:** Active - Tracking started Nov 1, 2025
**Applies to:** All e-commerce clients using Product Hero Labelizer

---

## Overview

This system tracks Product Hero label assignments (Heroes, Sidekicks, Villains, Zombies) over time to:

1. **Validate campaign structure** - Ensure products are in correct asset groups
2. **Analyze label transitions** - Understand what causes products to move between categories
3. **Measure Product Hero effectiveness** - Does moving from Zombie→Sidekick actually improve performance?
4. **Predict ROAS changes** - What happens when we adjust targets for each label category?

---

## Data Sources

### Actual Labels (Nov 1, 2025 onwards)

**Source:** Google Merchant Center custom label fields
**Method:** Daily fetch via Google Ads API
**Confidence:** 100% (actual Product Hero assignments)

**How it works:**
- Product Hero updates labels daily based on performance
- Labels sync to Google Merchant Center as custom attributes (e.g., `custom_label_0`)
- We query Google Ads API daily to capture current labels
- Store changes only (not daily snapshots of unchanged products)

### Inferred Labels (Before Nov 1, 2025)

**Source:** Campaign naming conventions + performance data
**Method:** Retroactive inference from Google Ads change history
**Confidence:** Varies (see Confidence Levels below)

**How it works:**
- Analyze which campaign a product was in on a given date
- Parse campaign name for label indicators (H&S, Zombies, Villains)
- Supplement with performance data when ambiguous
- Always flag as "inferred" with confidence level

---

## Campaign Naming Conventions (ROK Standard)

All e-commerce clients follow these patterns:

### Clear Labels (High Confidence)

| Campaign Name Contains | Inferred Labels | Confidence |
|------------------------|-----------------|------------|
| "Zombies" (alone) | zombies | HIGH |
| "Villains" (alone) | villains | HIGH |

### Ambiguous Labels (Medium Confidence)

| Campaign Name Contains | Inferred Labels | Confidence |
|------------------------|-----------------|------------|
| "H&S" | heroes OR sidekicks | MEDIUM |
| "Heroes & Sidekicks" | heroes OR sidekicks | MEDIUM |
| "Heroes and Sidekicks" | heroes OR sidekicks | MEDIUM |

### Mixed Labels (Low Confidence)

| Campaign Name Contains | Inferred Labels | Confidence |
|------------------------|-----------------|------------|
| "H&S Zombies" | heroes, sidekicks, OR zombies | LOW |
| "H&S and Zombies" | heroes, sidekicks, OR zombies | LOW |
| "Villains and Zombies" | villains OR zombies | MEDIUM |

---

## Confidence Levels

### ACTUAL (100%)
- From Product Hero via custom label fields
- Available: Nov 1, 2025 onwards
- No inference needed

**Example:**
```json
{
  "product_id": "287",
  "date": "2025-11-15",
  "label": "sidekicks",
  "confidence": "actual",
  "source": "custom_label_0"
}
```

### HIGH (80-90%)
- Campaign name explicitly states single label (Zombies, Villains)
- Performance data confirms (zombies have low traffic, villains have clicks but no conversions)

**Example:**
```json
{
  "product_id": "287",
  "date": "2025-10-22",
  "label": "zombies",
  "confidence": "high",
  "source": "campaign_name",
  "evidence": {
    "campaign": "Tree2mydoor | Zombies Activation",
    "clicks_30d": 5,
    "conversions_30d": 0
  }
}
```

### MEDIUM (60-80%)
- Campaign name indicates 2 possible labels (H&S, Villains and Zombies)
- Performance data helps narrow down but not definitive

**Example:**
```json
{
  "product_id": "1229_1083",
  "date": "2025-10-22",
  "label": "heroes_or_sidekicks",
  "confidence": "medium",
  "source": "campaign_name",
  "evidence": {
    "campaign": "AFH | P Max | H&S Zombies Furniture",
    "clicks_30d": 95,
    "conversions_30d": 0,
    "note": "In H&S campaign but no conversions suggests sidekick"
  }
}
```

### LOW (40-60%)
- Campaign name indicates 3+ possible labels (H&S Zombies)
- Performance data ambiguous or insufficient

**Example:**
```json
{
  "product_id": "2590",
  "date": "2025-10-15",
  "label": "heroes_sidekicks_or_zombies",
  "confidence": "low",
  "source": "campaign_name",
  "evidence": {
    "campaign": "Superspace | H&S and Zombies",
    "clicks_30d": 42,
    "conversions_30d": 1,
    "note": "Could be any of the three labels"
  }
}
```

### UNKNOWN
- No campaign data available
- Product not active during period
- Campaign name doesn't match any patterns

---

## Client Configuration

### Standard Configuration

**Default for all e-commerce clients:**
```json
{
  "label_field": "custom_label_0",
  "label_tracking_enabled": true,
  "product_hero_assessment_window_days": 30,
  "label_inference": {
    "enabled": true,
    "start_date": "2025-10-01"
  }
}
```

### Client-Specific Overrides

**Accessories for the Home (exception):**
```json
{
  "name": "Accessories for the Home",
  "product_hero_assessment_window_days": 60
}
```

**If client uses different custom label field:**
```json
{
  "name": "Example Client",
  "label_field": "custom_label_1"
}
```

---

## Data Storage

### Directory Structure

```
tools/product-impact-analyzer/
└── history/
    └── label-transitions/
        ├── accessories-for-the-home/
        │   ├── current-labels.json
        │   ├── 2025-10.json
        │   ├── 2025-11.json
        │   └── 2025-12.json
        ├── tree2mydoor/
        │   ├── current-labels.json
        │   └── 2025-11.json
        └── superspace/
            ├── current-labels.json
            └── 2025-11.json
```

### File Formats

**current-labels.json** (snapshot of latest state):
```json
{
  "last_updated": "2025-11-15T10:00:00Z",
  "source": "actual",
  "products": {
    "287": "heroes",
    "1229_1083": "sidekicks",
    "2562": "villains",
    "593": "zombies"
  }
}
```

**2025-11.json** (monthly transitions):
```json
{
  "month": "2025-11",
  "transitions": [
    {
      "product_id": "287",
      "date": "2025-11-05",
      "from": "sidekicks",
      "to": "heroes",
      "confidence": "actual",
      "trigger": "Revenue exceeded £500/week threshold",
      "evidence": {
        "revenue_before": "£380/week",
        "revenue_after": "£580/week",
        "conversions_increase": "+40%"
      }
    },
    {
      "product_id": "2562",
      "date": "2025-11-12",
      "from": "villains",
      "to": "zombies",
      "confidence": "actual",
      "trigger": "Traffic dropped below threshold",
      "evidence": {
        "clicks_before": "200/week",
        "clicks_after": "5/week"
      }
    }
  ]
}
```

**2025-10.json** (historical/inferred):
```json
{
  "month": "2025-10",
  "note": "Labels for this period are INFERRED from campaign names. Actual Product Hero labels not available.",
  "transitions": [
    {
      "product_id": "1229_1083",
      "date": "2025-10-15",
      "from": "unknown",
      "to": "heroes_or_sidekicks",
      "confidence": "medium",
      "source": "campaign_name_inference",
      "evidence": {
        "campaign": "AFH | P Max | H&S Zombies Furniture",
        "clicks_30d": 95,
        "conversions_30d": 0
      }
    }
  ]
}
```

---

## Tracking Process

### Daily Tracking (Nov 1 onwards)

**Schedule:** Every day at 10:00 AM (same as product monitoring)

**Process:**
```python
1. For each enabled e-commerce client:
   a. Query Google Ads API for all products
   b. Extract custom_label_0 (or configured field)
   c. Compare to yesterday's snapshot (current-labels.json)

2. If label changed:
   a. Log transition with date, from/to labels
   b. Mark as "actual" confidence
   c. Append to monthly transitions file (YYYY-MM.json)
   d. Update current-labels.json

3. If label unchanged:
   a. No storage (saves space)
   b. Current snapshot remains accurate
```

**Output:** Silent operation, no alerts for label changes themselves.

### Weekly Validation (Tuesdays)

**Included in weekly Product Impact Report:**

**Section: "Campaign Structure Validation"**
```
Accessories for the Home - Label Mismatches:

Asset Group: "Furniture - Sidekicks"
Expected filter: custom_label_0 = "sidekicks"

Products in asset group with wrong labels:
❌ Product 1229_1083: Currently labeled "heroes" (should be "sidekicks")
   - Transitioned: sidekicks → heroes on Nov 5
   - Recommendation: Update asset group filter or move to Heroes asset group

✓ Product 2033_2270: Correctly labeled "sidekicks"
✓ Product 953: Correctly labeled "sidekicks"

Summary: 1 of 12 products in this asset group has mismatched label.
```

### Historical Backfill (One-time, Nov 1)

**Script:** `backfill_historical_labels.py`

**Process:**
```bash
python backfill_historical_labels.py \
  --start-date 2025-10-01 \
  --end-date 2025-10-31 \
  --all-clients
```

**What it does:**
1. For each client, for each day in October:
   - Query Google Ads change history: which campaign had this product?
   - Parse campaign name using patterns
   - Query performance data for that product (30-day window)
   - Infer label with confidence level
   - Store in `2025-10.json` as inferred

2. Flag entire file with caveat:
   ```
   "note": "Labels inferred from campaign names.
            Actual Product Hero labels not available before Nov 1, 2025."
   ```

---

## Usage Examples

### Example 1: Performance Analysis (Claude investigating)

**User:** "Why did revenue drop on Oct 22 for AFH?"

**Claude process:**
```python
1. Check what changed on Oct 22 (Google Ads change history)
2. Find: ROAS reduced 210% → 200%
3. Check which products spiked in traffic
4. Find: Products 1229_1083, 2562, 1186
5. Query historical labels for Oct 22:
   - 1229_1083: "heroes_or_sidekicks" (medium confidence, inferred)
   - 2562: "zombies" (high confidence, inferred)
   - 1186: "heroes_or_sidekicks" (medium confidence, inferred)
6. Query current labels (Nov 1):
   - 1229_1083: "sidekicks" (actual)
   - 2562: "villains" (actual) ← TRANSITION!
   - 1186: "heroes" (actual)
7. Check transitions:
   - 2562: zombies → villains (Oct 22-31)
   - Reason: Got 1,195 clicks but 0 conversions
```

**Claude response:**
```
Revenue drop on Oct 22 was caused by ROAS reduction triggering traffic
spike from low-converting products:

Product 2562 (Zuiver Cooler):
- Oct 22 label: zombies (inferred, high confidence)
- Current label: villains (actual)
- Transition: Oct 22-31, zombies → villains
- Cause: ROAS reduction activated zombie product, got 1,195 clicks,
  0 conversions. Product Hero relabeled as villain.

⚠️ Note: Oct 22 labels are inferred from campaign names
(actual labels available from Nov 1 onwards)
```

### Example 2: Monthly Label Review

**User:** "Review label transitions for AFH in November"

**Claude process:**
```python
1. Read: history/label-transitions/accessories-for-the-home/2025-11.json
2. Group transitions by type:
   - Heroes → Sidekicks: []
   - Sidekicks → Heroes: [287, 593]
   - Zombies → Sidekicks: [1450, 2890]
   - Sidekicks → Villains: [2590]
   - Other: []
3. Analyze performance impact for each transition
4. Generate summary report
```

**Claude response:**
```
AFH Label Transitions - November 2025 (Actual labels ✓)

Positive Transitions:
✓ Sidekicks → Heroes: 2 products
  - Product 287: £380/week → £580/week (+53%)
  - Product 593: £290/week → £510/week (+76%)

✓ Zombies → Sidekicks: 2 products
  - Product 1450: £0 → £120/week (activation successful)
  - Product 2890: £0 → £85/week (activation working)

Negative Transitions:
❌ Sidekicks → Villains: 1 product
  - Product 2590: Investigation needed - why did conversions drop?

Analysis: Zombie activation campaigns are working (2 promotions to
Sidekick). Hero promotions show strong performance gains (+50-75%
revenue). One product degraded to Villain - investigate pricing or
listing quality issues.
```

### Example 3: Product Hero ROI Analysis (After 3-6 months)

**User:** "Does Product Hero Labelizer actually work? Show me the data."

**Claude process:**
```python
1. Query all transitions from Nov 2025 - March 2026
2. Group by transition type
3. Calculate average performance change for each type
4. Compare to control group (products that didn't transition)
```

**Claude response:**
```
Product Hero ROI Analysis (Nov 2025 - Mar 2026, 5 months data)

Zombie Activation Success Rate:
- Products promoted Zombie → Sidekick: 47
- Average revenue before: £0/week
- Average revenue after: £145/week
- ROI: Positive (new revenue from dormant products)

Sidekick → Hero Promotions:
- Products promoted: 23
- Average revenue before: £320/week
- Average revenue after: £580/week (+81%)
- Performance improvement: Significant

Villain Identification Accuracy:
- Products labeled as Villains: 156
- Average clicks: 85/week
- Average conversions: 0.2/week
- Average ROAS: 0.3 (30% return)
- Conclusion: Correctly identified budget drainers

Overall Conclusion: Product Hero Labelizer is effective. Zombie
activation generates new revenue, Hero promotions show strong gains,
and Villain identification prevents waste.
```

---

## Integration with Other Systems

### Product Impact Analyzer

**Enhanced with label context:**
- When a product's performance changes, check if label also changed
- Example: "Revenue increased £200 on Nov 5 when product was relabeled sidekick → hero"

### Weekly Email Reports

**New section: "Label Transitions This Week"**
- Show notable transitions (Sidekick→Hero, Hero→Villain, etc.)
- Flag structural issues (products in wrong asset groups)
- Summary stats (X products promoted, Y products degraded)

### Strategy Experiments

**Test label-based strategies:**
- "What ROAS target works best for Sidekicks?"
- "Should Heroes and Sidekicks be in same campaign or separate?"
- "How long does Zombie activation take to show results?"

---

## Caveats and Limitations

### Historical Data (Before Nov 1, 2025)

**Limitations:**
- Labels are INFERRED from campaign names, not actual Product Hero assignments
- Hero vs Sidekick distinction is ambiguous in "H&S" campaigns
- Performance window (7-30 days) may not match Product Hero's assessment period
- Confidence varies based on campaign naming clarity

**Always include caveat when using inferred labels:**
```
⚠️ Labels before Nov 1, 2025 are inferred from campaign naming
conventions and may not reflect actual Product Hero classifications.
Confidence level: [HIGH/MEDIUM/LOW]
```

### Product Hero Assessment Window

**Standard:** 30 days (most clients)
**Exception:** 60 days (Accessories for the Home)

**Implication:**
- A product's label reflects its performance over the assessment window
- Recent changes (last 7 days) may not yet be reflected in label
- Label changes lag behind actual performance shifts

### Label Transition Timing

**Product Hero updates:** Daily
**Our tracking:** Daily at 10 AM

**Implication:**
- We capture label changes within 24 hours
- Exact timestamp of Product Hero's label change not known
- Date represents "change detected on" not "change occurred at"

---

## Troubleshooting

### Missing Labels for Historical Period

**Problem:** No inferred label available for a product on a specific date

**Possible causes:**
1. Product not active during that period
2. Product not in any campaign (disapproved or paused)
3. Campaign name doesn't match known patterns

**Solution:**
- Mark as "unknown" confidence
- Check Google Ads change history for that product
- May need to manually review campaign structure for that client

### Label Mismatch vs Asset Group

**Problem:** Product labeled "heroes" but in "Sidekicks" asset group

**This is EXPECTED behavior when:**
1. Product recently transitioned (label updated but asset group filter hasn't)
2. Asset group lacks proper product filters
3. Product Hero's assessment differs from campaign structure

**Action:**
- Flag in weekly report
- User decides: update asset group filter or accept mismatch
- Not an error, but a structural decision point

### Confidence Too Low for Analysis

**Problem:** Historical analysis requires high confidence but data is "medium" or "low"

**Solution:**
- Use broader categories: "Not a zombie" vs "Zombie"
- Acknowledge limitation in analysis
- Wait for actual tracking data to accumulate (3-6 months)

---

## Maintenance

### Daily (Automated)
- Fetch current labels for all clients
- Detect and log transitions
- Update current-labels.json

### Weekly (Automated)
- Validate asset group structure
- Include in weekly email report
- Flag mismatches for review

### Monthly (Manual)
- Review transitions for each client
- Analyze patterns (what causes promotions/degradations)
- Update client CONTEXT.md with insights

### Quarterly (Manual)
- ROI analysis: Is Product Hero delivering value?
- Strategy experiments: Test label-based optimizations
- Refine inference rules based on actual data

---

## Future Enhancements

### Phase 2 (After 3-6 months of data)

**Predictive Analytics:**
- Predict which Sidekicks will become Heroes
- Identify Zombies worth activating
- Flag Heroes at risk of degrading

**ROAS Optimization:**
- Optimal ROAS targets per label category
- Performance curves: ROAS vs volume by label
- Budget allocation recommendations

**Automated Structural Fixes:**
- Auto-suggest asset group filter corrections
- Recommend campaign structure changes
- Alert when products should move campaigns

---

## Related Documentation

- [Product Hero Labelizer System](../../roksys/knowledge-base/rok-methodologies/product-hero-labelizer-system.md) - Framework overview
- [Product Impact Analyzer README](README.md) - Main tool documentation
- [PHASE2.md](PHASE2.md) - Automated weekly reporting
- [MONITORING.md](MONITORING.md) - Real-time monitoring system

---

**Last Updated:** 2025-10-31
**Maintained By:** ROK Systems
