# Brand vs Non-Brand Performance Analysis

**Category**: Google Ads

**Difficulty**: Beginner

**Time Investment**: 20-30 minutes

---

## When to Use

This analysis helps answer: **"Should I invest more in brand or non-brand campaigns?"**

**Specific scenarios**:
- Quarterly business reviews
- Budget allocation decisions across channels
- ROAS target calibration (brand typically performs 2-3x better)
- Understanding true acquisition efficiency
- Client asks "Why is our ROAS dropping?" (often: brand/non-brand mix shift)

**Ideal frequency**: Quarterly, or when significant budget changes are planned

---

## Prerequisites

**Data Requirements**:
- 90+ days of conversion data (minimum for confidence)
- Both brand and non-brand campaigns active
- Conversion tracking properly configured

**Tools Required**:
- [`query-google-ads-performance.py`](../../shared/scripts/query-google-ads-performance.py)
- Google Sheets or Excel for analysis
- Access to Google Ads account

**Knowledge Requirements**:
- Understand difference between brand (searches for your brand name) and non-brand (generic product searches)
- Basic ROAS calculation (Revenue / Cost)
- Campaign naming conventions for the client

---

## Process

### Step 1: Export Performance Data

Query all campaigns for the analysis period:

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/query-google-ads-performance.py \
  --customer-id 8573235780 \
  --start-date 2025-09-01 \
  --end-date 2025-11-25 \
  --output csv \
  --file brand-analysis.csv
```

**What to look for**:
- All campaigns exported (check count matches Google Ads UI)
- Revenue data present (not all zeros)
- Date range covers at least 90 days

**Expected output**: CSV file with campaign-level performance (cost, revenue, conversions, ROAS)

---

### Step 2: Classify Campaigns

Open the CSV and classify each campaign as Brand or Non-Brand:

**Brand campaigns typically contain**:
- "Brand" in campaign name
- "Competitor" (competitor brand bidding)
- Client's actual brand name
- Branded product names

**Non-Brand campaigns**:
- "Generic" in campaign name
- Generic product terms
- "Shopping" (if not brand-filtered)
- "P Max" (usually mix, but count as non-brand unless brand-only)

**Quick method in Excel**:
```
=IF(OR(
  ISNUMBER(SEARCH("brand",A2)),
  ISNUMBER(SEARCH("competitor",A2)),
  ISNUMBER(SEARCH("smythson",A2))
), "Brand", "Non-Brand")
```

**What to look for**:
- Clear split (if 90% are one type, naming convention may need review)
- P Max campaigns (typically count as non-brand unless specifically brand-only)

---

### Step 3: Calculate Channel Metrics

Create summary table:

| Channel | Spend | Revenue | Conversions | ROAS | CPA |
|---------|-------|---------|-------------|------|-----|
| **Brand** | =SUMIF(type,"Brand",cost) | =SUMIF(type,"Brand",revenue) | =SUMIF(type,"Brand",conv) | =Revenue/Spend | =Spend/Conv |
| **Non-Brand** | =SUMIF(type,"Non-Brand",cost) | =SUMIF(type,"Non-Brand",revenue) | =SUMIF(type,"Non-Brand",conv) | =Revenue/Spend | =Spend/Conv |
| **Total** | =SUM | =SUM | =SUM | =Revenue/Spend | =Spend/Conv |

**Calculate key ratios**:
- Brand ROAS vs Non-Brand ROAS ratio (typically 2-3x)
- Spend split (% to brand vs non-brand)
- Revenue contribution (% from brand vs non-brand)

---

### Step 4: Analysis & Interpretation

**Compare to typical ranges**:

| Metric | Healthy Range | What It Means |
|--------|---------------|---------------|
| Brand ROAS | 400-800% | High intent, warm audience |
| Non-Brand ROAS | 200-400% | Cold acquisition |
| Brand vs Non-Brand ratio | 2-3x | Brand typically 2-3x more efficient |
| Brand spend % | 40-60% | Balanced approach |

**Good Signs**:
- Brand ROAS significantly higher than non-brand (expected)
- Both channels profitable (ROAS >100%)
- Spend allocation roughly matches revenue contribution

**Red Flags**:
- Brand ROAS <300% (check brand campaign settings, may have waste)
- Non-brand ROAS <150% (may be overspending on acquisition)
- 80%+ spend on one channel (likely missing opportunity)
- Brand spend >70% (over-reliant on existing demand, not building new audience)

---

## Interpretation Guide

### Decision Framework

**If Brand ROAS >500% AND Non-Brand ROAS >250%**:
- **Action**: Balanced growth - increase both proportionally
- **Rationale**: Both channels healthy, scale together

**If Brand ROAS >600% AND Non-Brand ROAS <250%**:
- **Action**: Shift 10-20% budget from non-brand to brand
- **Rationale**: Brand highly efficient, non-brand struggling
- **Caveat**: Don't over-index on brand long-term (limits new customer acquisition)

**If Brand ROAS 300-500% AND Non-Brand ROAS >350%**:
- **Action**: Investigate brand campaign quality
- **Rationale**: Non-brand shouldn't outperform brand (suggests brand waste)
- **Check**: Broad match keywords in brand, irrelevant traffic, poor negatives

**If Brand spend >65% of total**:
- **Action**: Test increasing non-brand budget (even if ROAS lower)
- **Rationale**: Over-reliance on existing demand, not building pipeline
- **Monitor**: New customer acquisition metrics

**If Non-Brand spend >70% of total AND brand campaigns exist**:
- **Action**: Increase brand budget (low-hanging fruit)
- **Rationale**: Missing high-efficiency opportunities
- **Quick win**: Usually immediate ROAS improvement

---

## Example from Smythson (Q4 2025)

**Context**:
- Luxury stationery/leather goods e-commerce
- Strong brand awareness in UK
- Running both brand and non-brand for years
- Question: "Should we increase Black Friday budget? Where?"

**Data Observed** (Sept-Nov 2025):

| Channel | Spend | Revenue | Conversions | ROAS | Spend % |
|---------|-------|---------|-------------|------|---------|
| **Brand** | £58,347 | £378,619 | 1,856 | **652%** | 58% |
| **Non-Brand** | £42,156 | £125,432 | 687 | **298%** | 42% |
| **Total** | £100,503 | £504,051 | 2,543 | **502%** | 100% |

**Key Findings**:
- Brand ROAS 2.2x higher than non-brand (652% vs 298%)
- Brand driving 75% of revenue with 58% of spend
- Both channels profitable, but brand significantly more efficient

**Decision Made**:
Reallocate Black Friday budget:
- Brand: Increase 35% (from £58k → £78k for event period)
- Non-Brand: Increase 15% (from £42k → £48k for event period)
- Rationale: Leverage brand efficiency during high-intent period

**Outcome** (Black Friday week):
- Brand: 720% ROAS (up from 652% baseline)
- Non-Brand: 285% ROAS (slight drop due to increased competition)
- Overall: 580% ROAS, £127k revenue in one week
- **Result**: Correct call - brand scaled beautifully during peak demand

**Learnings**:
- Brand efficiency increases during high-intent periods (holidays, events)
- Non-brand gets more competitive (harder to scale profitably)
- Having this data beforehand enabled confident budget allocation
- 2-week lead time was perfect for planning

---

## Expected Outcomes

**Decisions Enabled**:
- Budget reallocation between channels (immediate action)
- Differentiated ROAS targets (brand 500%+, non-brand 300%+)
- Understanding which channel to scale first
- Identifying underinvestment or overspend

**Typical Impact**:
- 10-30% overall ROAS improvement (if misallocated before)
- Clearer reporting to clients (channel-level strategy)
- Better forecasting (know which channel drives what)

**Success Criteria**:
- You can confidently answer: "Where should next £1,000 go?"
- Client understands why brand and non-brand have different targets
- Budget allocation aligns with strategic goals (growth vs efficiency)

---

## Common Pitfalls

1. **Treating P Max as "brand" because ROAS is high**
   - What: P Max often captures brand searches, inflating its ROAS
   - Why it happens: P Max doesn't report brand vs non-brand split
   - How to avoid: Count P Max as non-brand unless proven brand-only (via asset groups)

2. **Over-indexing on brand long-term**
   - What: Shifting 80%+ budget to brand because "it performs better"
   - Why it happens: Short-term ROAS focus
   - How to avoid: Balance efficiency (brand) with growth (non-brand). Rule of thumb: 40-60% brand is healthy.

3. **Not accounting for assisted conversions**
   - What: Non-brand often assists brand conversions (user journey: generic search → later brand search)
   - Why it happens: Last-click attribution
   - How to avoid: Check assisted conversion reports, understand non-brand builds awareness for brand

4. **Comparing brand to non-brand as "good vs bad"**
   - What: Expecting both to have same ROAS
   - Why it happens: Misunderstanding channel purpose
   - How to avoid: Brand = efficiency, Non-brand = growth. Both needed.

---

## Variations by Client Type

### E-commerce
- Use this analysis quarterly
- Heavy brand reliance OK if:
  - Strong organic brand search volume
  - Email/social driving brand searches
  - Repeat purchase business model

### Lead Generation
- Non-brand typically more important (building pipeline)
- Brand may be smaller % but still valuable (warm leads)
- Compare cost-per-lead, not just ROAS

### Multi-Location (e.g., Hotels)
- Run analysis per property if campaigns separated
- Brand often includes location name ("Cavendish Hotel")
- Non-brand includes generic terms ("Peak District hotels")

---

## Related Playbooks

*(Coming soon)*
- ROAS Target Calibration - Use this analysis to set differentiated targets
- Budget Allocation Strategy - Feeds into overall budget planning
- Search Term Audit - Identify brand terms bleeding into non-brand campaigns

---

## Tools & Resources

**Universal Scripts Used**:
- [`query-google-ads-performance.py`](../../shared/scripts/query-google-ads-performance.py) - Performance data export

**External Resources**:
- [Google Ads Attribution Models](https://support.google.com/google-ads/answer/6259715) - Understanding assisted conversions
- [Industry ROAS benchmarks](https://www.wordstream.com/blog/ws/2022/03/15/google-ads-industry-benchmarks) - Context for your ranges

---

## Version History

- **v1.0** (Nov 26, 2025) - Initial creation based on Smythson Q4 2025 analysis

---

## Notes

**Attribution caveat**: This analysis uses last-click attribution. In reality, non-brand often assists brand conversions. Consider this when making cuts to non-brand (you may inadvertently hurt brand performance).

**Naming convention dependency**: Relies on clear campaign naming. If campaigns aren't clearly labelled, you'll need to manually classify or improve naming first.

**P Max consideration**: P Max campaigns are a mix of brand and non-brand. If P Max is a large % of spend, this analysis is less precise. Consider using asset group segmentation or search term reports to estimate brand %.
