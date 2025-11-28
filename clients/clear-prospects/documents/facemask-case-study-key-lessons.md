# Face Masks Case Study - Key Lessons Learned

**Date**: November 2025
**Campaign**: CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9
**Analysis Period**: May-November 2025
**Status**: ✅ Data verified against Google Ads API (Nov 12, 2025)

---

## Performance Summary

**6-Month Trend (Campaign-Level ROAS):**
- May 2025: 95% (losing money)
- June 2025: 103% (marginally profitable)
- July 2025: 124% (best summer month)
- August 2025: 107% (profitable but inconsistent)
- September 2025: 105% (restructure implemented Sep 15)
- October 2025: 105% (stabilising)
- November 2025: 129% (best performance - partial month)

**Improvement**: +36% ROAS from worst (May) to best (November)

---

## Root Cause: Channel Competition Fragmenting Conversion Data

### The Problem

Multiple campaign types were competing for the same "personalised face masks" search queries:
- Search campaigns
- Shopping campaigns (Villains, Zombies, H&S labels)
- Performance Max campaigns

**Result**: Budget fragmented across channels, preventing Smart Bidding from getting sufficient conversion data in any single campaign to optimise effectively.

### Why This Matters

Smart Bidding algorithms require **conversion volume** to learn and optimise:
- Each campaign competing for the same query splits conversions
- Low conversion volume per campaign = slow learning, poor optimisation
- Volatile performance as budget shifts between channels

---

## The Solution (September 15, 2025)

### Actions Taken

1. **Consolidated budget** from Shopping/PMax into the Search campaign
2. **Implemented AI Max bidding** with Target ROAS 130%
3. **Paused competing campaigns** for face masks queries
4. **Allowed 6-8 week learning period** for Smart Bidding to stabilise

### Follow-Up Optimisation (November 4, 2025)

Added exact match negative keyword `[personalised face masks]` to all Shopping and PMax campaigns to prevent any remaining channel competition.

---

## Key Strategic Lessons

### 1. Shopping Isn't Always Best for E-commerce

**Conventional wisdom**: Shopping campaigns are best for product-based searches.

**Reality**: For products with **specific customisation intent** (e.g., "personalised face masks"), Search campaigns can outperform Shopping because:
- User has already decided what they want
- They're looking for customisation options, not browsing
- Search ads allow clear messaging about personalisation capabilities
- Shopping feeds focus on visual browsing (better for discovery)

**Application**: Identify products where search intent indicates specific customisation needs rather than visual browsing.

---

### 2. Channel Competition Fragments Smart Bidding Data

**Problem**: Multiple campaigns targeting the same queries split conversion data.

**Impact**:
- Slower Smart Bidding learning
- More volatile performance
- Inefficient budget allocation

**Solution**: Consolidate to the best-performing channel for specific high-value queries.

**Method**:
1. Analyse performance by channel for key search terms
2. Identify clear winner (in this case: Search at 142% ROAS vs Shopping at 44%)
3. Consolidate budget to winning channel
4. Use negative keywords to prevent competing channels from bidding on the query

---

### 3. Volume Reduction Can Improve Efficiency

**What Happened**:
- Spend dropped from £3,248/month (May) to £306/month (November)
- But ROAS improved from 95% to 129%

**Why This Is Positive**:
- Lower spend = focusing on best-performing traffic only
- Higher ROAS = each pound spent generates more return
- Better for profitability even if absolute revenue is lower

**Lesson**: Don't chase volume at the expense of efficiency. Sometimes reducing spend to focus on high-quality traffic improves overall profitability.

---

### 4. Data Verification is Critical

**What Went Wrong Initially**:
- Original analysis (Nov 4) claimed "83% → 292%" improvement
- These figures could not be verified from Google Ads API
- Caused confusion and required correction

**Corrected Approach**:
- Always verify performance claims against Google Ads API before publishing
- Document data sources with date ranges
- Flag partial month data with caveats
- Add data quality notes when figures cannot be reproduced

**Added to CLAUDE.md**: Data Verification Protocol to prevent recurrence.

---

## When to Apply This Methodology

### Red Flags Indicating Channel Competition Issues:

1. **Volatile ROAS** across months despite stable strategy
2. **Low conversion volume** per campaign (< 30/month)
3. **Same search terms** appearing in multiple campaign types
4. **Budget shifting** between campaigns frequently
5. **Smart Bidding "learning" state** persisting for weeks

### Application Process:

1. **Identify high-value search terms** with volatile performance
2. **Analyse by channel**: Pull search term reports for each campaign type
3. **Calculate channel-level ROAS**: Which channel converts best for this term?
4. **Consolidate to winner**: Move budget to best-performing channel
5. **Add negative keywords**: Prevent other channels from competing
6. **Monitor for 6-8 weeks**: Allow Smart Bidding learning period

### Next Applications:

- **Photo cushions** (Clear Prospects - HSG): Similar product, likely similar channel dynamics
- **Other customisation products**: Any product with "personalised", "custom", "with your" in search terms

---

## Caveats & Monitoring

### Data Quality Note

November performance (129% ROAS) is based on **partial month data** (Nov 1-11). Need to confirm this sustains through full month before declaring conclusive success.

### Monitoring Plan

- **Short-term** (Nov 12-30): Verify November ROAS sustains through month-end
- **Medium-term** (December): Test if structure holds under Christmas seasonal demand
- **Long-term** (Jan-Feb): Confirm improvement wasn't just seasonal anomaly

### Success Metrics

- ROAS sustains above 120% consistently
- Monthly ROAS volatility reduces (standard deviation < 10%)
- CPA stabilises around £5-6 range
- Smart Bidding learning indicators show "optimised" status

---

## Documentation References

- **Full Case Study**: `clients/clear-prospects/reports/monthly/november-2025-facemask-case-study.html`
- **CONTEXT.md Entry**: Updated Nov 12, 2025 with corrected figures
- **Experiment Log**: Sep 15, 2025 entry in rok-experiments-client-notes.csv
- **CLAUDE.md Warning**: Target CPA vs Target ROAS distinction added
- **Data Source**: Google Ads API campaign-level data (verified Nov 12, 2025)

---

## Template for Similar Analyses

When investigating volatile campaign performance:

```
1. Pull 6-month historical data (campaign-level, not search term)
2. Check for multiple campaigns targeting same queries
3. Analyse channel performance (Search vs Shopping vs PMax)
4. Calculate conversion volume per campaign
5. Identify fragmentation (< 30 conversions/month per campaign = red flag)
6. Test consolidation to best-performing channel
7. Monitor for 6-8 weeks (Smart Bidding learning period)
8. Document results with verified API data
```

Remember: **Always verify claims against Google Ads API before publishing.**
