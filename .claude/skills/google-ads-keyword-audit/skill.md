---
name: google-ads-keyword-audit
description: Performs targeted keyword and search term analysis for Google Ads Search campaigns. Identifies wasted spend, growth opportunities, and negative keyword candidates using actionable-only methodology. Use when analysing keywords, search terms, negative keywords, or Search campaign optimisation.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Write, Read, Bash
---

# Google Ads Keyword Audit Skill

## Framework Integration

**Framework Location**: `docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv`
**Framework Guide**: `docs/AUDIT-FRAMEWORK-GUIDE.md`

### Where This Audit Fits

This keyword audit implements **Section 5.6 (Keyword & Query)** and **Section 5.7 (Search Terms)** of the Google Ads Performance Framework.

| Framework Section | This Audit Covers | Additional Framework Items |
|-------------------|-------------------|----------------------------|
| **5.6 - Keyword & Query** | ✅ Keyword performance by match type<br>✅ ROAS analysis by keyword<br>✅ Impression share analysis<br>✅ Negative keyword identification | Quality Score monitoring<br>Ad relevance optimization<br>Landing page experience review |
| **5.7 - Search Terms** | ✅ Search term report analysis (weekly)<br>✅ Search term to keyword matching<br>✅ Search term intent analysis<br>✅ Irrelevant query identification<br>✅ Negative keyword list management | Dynamic search ad query analysis<br>Search term seasonality tracking<br>Negative keyword theme development |

### Framework Frequency Alignment

**This audit should be run**:
- **Weekly**: Search term review, negative keyword additions (Framework 5.6, 5.7)
- **Monthly**: Comprehensive keyword performance review, match type optimization (Framework 5.6)
- **Quarterly**: Strategic keyword restructuring, Quality Score improvement initiatives (Framework 5.6)

### Framework Relationship to Other Audits

```
FOUNDATION Audit (Section 1)
    ↓ (ensures tracking setup)
CAMPAIGN AUDIT (Sections 3-5)
    ↓ (reviews account structure)
→ KEYWORD AUDIT (Sections 5.6-5.7) ← YOU ARE HERE
    ↓ (optimizes keyword/query performance)
WEEKLY OPTIMISATION (Section 5.1-5.15)
```

**Before running this audit**: Ensure Foundation audit (Section 1) has been completed for proper conversion tracking setup.

## Instructions

**⚠️ CRITICAL - Campaign Type Scope**

This skill analyzes **Search campaigns ONLY** (keyword-driven campaigns).

**DO NOT attempt to analyze**:
- Product-level performance in Search campaigns (Search campaigns don't have product data)
- Product Hero labels in relation to Search keywords (Product Hero only applies to PMax/Shopping campaigns)
- "Which keywords drive Hero/Villain sales" (Search keywords don't interact with Product Hero labels)

**Why**: Search campaigns are optimized through keyword/query analysis, not product segmentation. Product Hero labels only apply to campaigns that pull from the Merchant Center feed (PMax and Shopping campaigns).

When this skill is triggered:

1. **Identify the scope**:
   - Specific Search campaigns or full account (Search campaigns only)
   - Date range (default: last 14 days for keyword analysis)
   - Minimum spend threshold (default: $50)
   - Account average metrics for relative benchmarking

2. **Load account context**:
   - Calculate account average ROAS, CTR, CVR
   - Identify campaign-specific benchmarks
   - Reference client margin goals (if available)
   - **Note**: If client uses Product Hero, you may reference PMax/Shopping performance as comparison benchmarks, but DO NOT attempt to connect Search keywords to Product Hero labels

3. **Execute keyword audit using ROK framework**:

### Phase 1: Wasted Spend Analysis
Identify keywords with:
- Spend ≥ threshold AND ROAS < account_avg × 0.7
- High spend with zero conversions (>$100, 0 conversions)
- Declining CTR/CVR (>15% drop WoW)

**Output**: Pause or reduce bid recommendations

### Phase 2: Growth Opportunities
Identify keywords with:
- ≥2 conversions AND ROAS ≥ account_avg × 1.3
- High impression share with strong performance
- Phrase/broad match queries performing well (exact match candidates)

**Output**: Bid increase or expansion recommendations

### Phase 3: Search Term Analysis (Three-Tier Classification)

**⚠️ STATISTICAL RIGOR REQUIREMENTS**:
- Use **60-day lookback period** minimum for search term data (not 7-14 days)
- Apply **30+ clicks threshold** for high-confidence negative keyword recommendations (Tier 1)
- Never make product assumptions - rely purely on statistical performance data
- Account for conversion lag when analyzing recent periods (last 2-3 days typically have incomplete conversion data)

**Three-Tier Classification System**:

**Tier 1 - High Confidence Negative Keywords** (Immediate Action):
- ≥30 clicks, 0 conversions, ≥£20 spend (60-day period)
- Statistical significance: ~4 clicks/day sustained over 2 months
- Action: Add as exact match negative keywords immediately
- False positive risk: Very low (<5%)

**Tier 2 - Medium Confidence Negative Keywords** (Monitor Closely):
- 10-29 clicks, 0 conversions (60-day period)
- Statistical significance: Moderate (1-4 clicks/day)
- Action: Track for 7 more days, auto-flag if reaches 30+ clicks with 0 conversions
- False positive risk: Moderate (10-20%)

**Tier 3 - Insufficient Data** (Continue Monitoring):
- <10 clicks (60-day period)
- Statistical significance: Low (<1.5 clicks/day)
- Action: No action - insufficient data for decision
- Note: May move to Tier 2 in next analysis period

**Additional Analysis**:
- High-performing queries not yet added as keywords
- Query-level CTR and conversion patterns
- Irrelevant query themes for broad/phrase match negatives

**Output**: Three separate tier tables, tier-specific CSV files, and new keyword suggestions

### Phase 4: Match Type Optimization
Review match type distribution:
- Broad vs phrase vs exact performance
- Query diversity by match type
- Match type migration opportunities
- Negative keyword coverage gaps

**Output**: Match type adjustment recommendations

### Phase 5: Performance Trends
Identify:
- Keywords with >15% WoW performance change
- Seasonal patterns affecting specific keywords
- Quality Score indicators (CTR as proxy)
- Competitive pressure signs (CPC increases)

**Output**: Monitoring alerts and bid adjustments

4. **Format output** using actionable-only approach:

```markdown
# Keyword Audit: [Client Name]
**Date Range**: [Start] to [End]  
**Analysis Date**: [Today]  
**Campaigns Analyzed**: [List]

## Executive Summary
[2-3 sentences: Key findings, wasted spend identified, opportunity value]

**Quick Stats**:
- Keywords analyzed: XXX
- Actionable items: XX
- Potential monthly savings: $X,XXX
- Potential growth opportunity: $X,XXX

## 🔴 Wasted Spend (Immediate Action Required)

**Framework Reference**: Section 5.6 - Keyword & Query Performance Analysis

### High Spend, Low ROAS Keywords
| Keyword | Campaign | Spend | Conversions | ROAS | Recommendation |
|---------|----------|-------|-------------|------|----------------|
| [keyword] | [campaign] | $XXX | X | 0.XX | Pause or reduce bid by 50% |
| ... | ... | ... | ... | ... | ... |

**Total waste identified**: $X,XXX in last [period]
**Framework Check**: ✅ / ❌ Keyword-level ROAS analysis complete (Framework 5.6)

### 🔴 Tier 1 - High Confidence Negative Keywords (Immediate Action)
**Framework Reference**: Section 5.7 - Search Term Report Review
**Criteria**: ≥30 clicks, 0 conversions, ≥£20 spend (60-day period)
**Statistical Confidence**: Very High (~4+ clicks/day sustained over 2 months)
**False Positive Risk**: <5%

| Search Term | Clicks | Spend | Daily Click Rate | Recommendation |
|-------------|--------|-------|-----------------|----------------|
| [query] | XX | £XXX | X.X clicks/day | Add as [exact] match negative keyword immediately |
| ... | ... | ... | ... | ... |

**Action**: Add [N] negative keywords immediately (use `add-negative-keywords.py` or bulk upload)
**Expected Impact**: £XXX/month waste reduction
**Framework Check**: ✅ / ❌ Irrelevant search term identification (Framework 5.7)

---

### 🟡 Tier 2 - Medium Confidence Negative Keywords (Monitor Closely)
**Criteria**: 10-29 clicks, 0 conversions (60-day period)
**Statistical Confidence**: Moderate (1-4 clicks/day)
**False Positive Risk**: 10-20%
**Auto-Flag Date**: [Date 7 days from now]

| Search Term | Clicks | Spend | Daily Click Rate | Status |
|-------------|--------|-------|-----------------|--------|
| [query] | XX | £XXX | X.X clicks/day | Monitor - review in 7 days |
| ... | ... | ... | ... | ... |

**Action**: Continue monitoring - system will auto-flag any terms reaching 30+ clicks with 0 conversions
**Next Review**: [Date 7 days from analysis date]
**Tracking System**: Tier 2 terms logged to `tier2_tracker.json` for automated monitoring

---

### 🔵 Tier 3 - Insufficient Data (Continue Monitoring)
**Criteria**: <10 clicks (60-day period)
**Statistical Confidence**: Low (<1.5 clicks/day)
**Action Required**: None - insufficient data for decision

**Summary**: [N] search terms with <10 clicks identified (not shown in detail - insufficient statistical power)

**Note**: These terms may move to Tier 2 in next analysis period if click volume increases

---

### ✅ Converting Search Terms (Keep Active)
**Framework Reference**: Section 5.7 - Search Term to Keyword Matching

| Search Term | Clicks | Conversions | ROAS | Status |
|-------------|--------|-------------|------|--------|
| [query] | XX | X.X | XXX% | Performing well - no action needed |
| ... | ... | ... | ... | ... |

**Summary**: [N] converting terms identified with average ROAS of XXX%

## 🟢 Growth Opportunities

**Framework Reference**: Section 5.6 - Keyword Bidding Strategy & Impression Share

### High-Performing Keywords (Scale These)
| Keyword | Campaign | Conversions | ROAS | Current Bid | Recommendation |
|---------|----------|-------------|------|-------------|----------------|
| [keyword] | [campaign] | XX | X.XX | $X.XX | Increase bid to $X.XX (+20%) |
| ... | ... | ... | ... | ... | ... |

**Potential additional revenue**: $X,XXX/month
**Framework Check**: ✅ / ❌ Keyword impression share analysis complete (Framework 5.6)

### Strong Queries to Add as Keywords
**Framework Reference**: Section 5.7 - Search Term to Keyword Matching

| Search Term | Impressions | Conversions | ROAS | Match Type | Recommendation |
|-------------|------------|-------------|------|------------|----------------|
| [query] | XXX | XX | X.XX | Phrase | Add as exact match keyword |
| ... | ... | ... | ... | ... | ... |

**Action**: Add [N] new exact match keywords
**Framework Check**: ✅ / ❌ High-performing queries added as keywords (Framework 5.7)

## 🟡 Declining Performance (Monitor & Adjust)

### Keywords with Performance Drops
| Keyword | Campaign | Metric | Change WoW | Possible Cause | Recommendation |
|---------|----------|--------|------------|----------------|----------------|
| [keyword] | [campaign] | CTR | -25% | Ad fatigue | Refresh ad copy |
| [keyword] | [campaign] | CVR | -18% | Landing page issue | Check page load time |
| ... | ... | ... | ... | ... | ... |

## Match Type Analysis

**Framework Reference**: Section 5.6 - Keyword Match Type Distribution & Performance

### Current Distribution
- Exact: XX% of spend, ROAS: X.XX
- Phrase: XX% of spend, ROAS: X.XX
- Broad: XX% of spend, ROAS: X.XX

### Recommendations
1. [Match type adjustment with reasoning]
2. [Additional match type strategy]

**Framework Check**: ✅ / ❌ Match type performance analysis by ROAS (Framework 5.6)

## Search Term Patterns

**Framework Reference**: Section 5.7 - Search Term Intent Analysis

### Low CTR Queries (Relevance Issues)
[Queries with CTR < 1% indicating poor ad relevance]

**Action**: Review ad copy or add as negatives
**Framework Check**: ✅ / ❌ Query-level CTR analysis complete (Framework 5.6)

### Irrelevant Query Themes
**Framework Reference**: Section 5.7 - Negative Keyword Theme Development

[Grouped irrelevant queries by theme]
- Theme 1: [e.g., "free", "DIY", "images"]
- Theme 2: [e.g., competitor names]

**Action**: Add broad match negatives
**Framework Check**: ✅ / ❌ Negative keyword themes identified (Framework 5.7)

## Prioritized Action Plan

### This Week (High Impact)
1. **Add [N] negative keywords** - Save ~$XXX/month
   - [Specific negative keywords list]
2. **Pause [N] underperforming keywords** - Save $XXX/month
   - [Keyword IDs or names]
3. **Increase bids on [N] high-performers** - Add ~$XXX revenue/month
   - [Specific keywords and new bids]

### Next 2 Weeks (Medium Impact)
4. **Add [N] new exact match keywords** - Capture missed traffic
5. **Refresh ad copy for declining keywords**
6. **Review landing pages for low-CVR keywords**

### Ongoing (Monitoring)
7. **Weekly search term review** - Catch new negatives
8. **Monitor bid adjustments impact**
9. **Track Quality Score indicators**

## Detailed Analysis

### Negative Keyword Recommendations
```
Campaign: [Campaign Name]
Add negatives:
- [negative keyword]
- [negative keyword]
- [negative keyword]

Match type: [Broad/Phrase/Exact]
Expected monthly savings: $XXX
```

[Repeat for each campaign]

### Bid Adjustment Recommendations
```
Keyword: [Keyword]
Campaign: [Campaign]
Current bid: $X.XX
Recommended bid: $X.XX
Reasoning: ROAS of X.XX with only X% impression share
Expected impact: +X conversions/month
```

[Repeat for priority keywords]

## Framework Alignment Summary

**Overall Framework Coverage**: Section 5.6 (Keyword & Query) + Section 5.7 (Search Terms)

### Framework Items Completed in This Audit

| Framework Item | Status | Notes |
|----------------|--------|-------|
| **5.6 - Exact match keyword performance** | ✅ / ❌ | [Brief finding] |
| **5.6 - Phrase match keyword performance** | ✅ / ❌ | [Brief finding] |
| **5.6 - Broad match keyword performance** | ✅ / ❌ | [Brief finding] |
| **5.6 - Keyword-level ROAS analysis** | ✅ / ❌ | [Brief finding] |
| **5.6 - Keyword bidding strategy review** | ✅ / ❌ | [Brief finding] |
| **5.6 - Keyword match type distribution** | ✅ / ❌ | [Brief finding] |
| **5.6 - Keyword impression share analysis** | ✅ / ❌ | [Brief finding] |
| **5.6 - Negative keyword coverage** | ✅ / ❌ | [Brief finding] |
| **5.7 - Search term report review (weekly)** | ✅ / ❌ | [Brief finding] |
| **5.7 - Search term to keyword matching** | ✅ / ❌ | [Brief finding] |
| **5.7 - Search term intent analysis** | ✅ / ❌ | [Brief finding] |
| **5.7 - Irrelevant search term identification** | ✅ / ❌ | [Brief finding] |
| **5.7 - Negative keyword list management** | ✅ / ❌ | [Brief finding] |
| **5.7 - Negative keyword theme development** | ✅ / ❌ | [Brief finding] |

### Framework Items NOT Covered (Require Separate Analysis)

- **5.6 - Quality Score monitoring** (requires Quality Score data export)
- **5.6 - Ad relevance optimization** (covered in Ad Copy audit)
- **5.6 - Landing page experience** (covered in Landing Page audit)
- **5.7 - Search term seasonality tracking** (requires multi-month historical analysis)
- **5.7 - Dynamic search ad query analysis** (only if DSA campaigns present)

### Next Framework Steps

**Recommended frequency**:
- This audit covers weekly optimization tasks (Framework 5.6, 5.7)
- Schedule next comprehensive keyword audit: [Date, 4 weeks from now]
- Schedule Quality Score deep-dive: [Date, quarterly]

## Data Quality Notes
- [Any tracking issues noticed]
- [Date range limitations]
- [Campaign exclusions and why]

## Follow-Up Actions
- [ ] Implement negative keywords (use bulk sheet)
- [ ] Adjust bids for [N] keywords
- [ ] Pause [N] waste keywords
- [ ] Add [N] new keywords
- [ ] Schedule follow-up audit in [timeframe]
```

5. **Actionable-Only Filtering**:
   - Skip keywords performing acceptably
   - Only show items requiring action
   - Use account average × 0.7 and × 1.3 thresholds
   - Minimum spend threshold to avoid noise

6. **Use MCP for data** (if connected):
   ```sql
   -- Keyword performance (14-day for immediate issues)
   SELECT
     ad_group_criterion.keyword.text,
     campaign.name,
     metrics.impressions,
     metrics.clicks,
     metrics.cost_micros,
     metrics.conversions,
     metrics.conversions_value
   FROM keyword_view
   WHERE segments.date DURING LAST_14_DAYS
     AND campaign.status = 'ENABLED'
   ORDER BY metrics.cost_micros DESC

   -- Search terms (60-day for statistical significance)
   -- ⚠️ CRITICAL: Use 60-day period for three-tier classification
   SELECT
     search_term_view.search_term,
     metrics.impressions,
     metrics.clicks,
     metrics.cost_micros,
     metrics.conversions,
     metrics.conversions_value
   FROM search_term_view
   WHERE segments.date >= '[60 days ago]'
     AND segments.date <= '[yesterday]'
     AND metrics.clicks > 0
   ORDER BY metrics.cost_micros DESC

   -- Note: Use explicit date range (not DURING operator)
   -- Example: segments.date >= '2025-10-18' AND segments.date <= '2025-12-17'
   ```

## ROK Framework Integration

### Actionable-Only Criteria
**Show keyword if ANY of these are true**:
- Spend ≥ $50 AND ROAS < account_avg × 0.7 (waste)
- Conversions ≥ 2 AND ROAS ≥ account_avg × 1.3 (opportunity)
- WoW CTR/CVR decline > 15% (declining)
- Spend > $100 AND conversions = 0 (zero-conv waste)

**Skip keyword if**:
- Performance stable and acceptable
- Spend below minimum threshold
- No clear action to take

### Thresholds
- **Minimum spend**: $50 (configurable)
- **Waste multiplier**: 0.7 × account average
- **Opportunity multiplier**: 1.3 × account average
- **Significant change**: ±15%
- **Critical change**: ±30%

### Three-Tier Classification Logic (Python)

```python
def classify_search_term(clicks, conversions, spend, period_days=60):
    """
    Classify search term into three-tier system.

    Args:
        clicks: Total clicks in period
        conversions: Total conversions in period
        spend: Total spend in period (float)
        period_days: Analysis period (default: 60)

    Returns:
        dict with tier, confidence, daily_click_rate, recommendation
    """
    daily_click_rate = clicks / period_days

    # Tier 1: High Confidence Negative Keywords
    if clicks >= 30 and conversions == 0 and spend >= 20:
        return {
            'tier': 1,
            'confidence': 'very_high',
            'daily_click_rate': daily_click_rate,
            'false_positive_risk': '<5%',
            'recommendation': 'Add as exact match negative keyword immediately',
            'action': 'immediate'
        }

    # Tier 2: Medium Confidence Negative Keywords
    elif 10 <= clicks < 30 and conversions == 0:
        import datetime
        next_review = datetime.date.today() + datetime.timedelta(days=7)
        return {
            'tier': 2,
            'confidence': 'moderate',
            'daily_click_rate': daily_click_rate,
            'false_positive_risk': '10-20%',
            'recommendation': f'Monitor closely - review on {next_review.strftime("%Y-%m-%d")}',
            'action': 'monitor',
            'next_review_date': next_review.strftime('%Y-%m-%d')
        }

    # Tier 3: Insufficient Data
    elif clicks < 10 and conversions == 0:
        return {
            'tier': 3,
            'confidence': 'low',
            'daily_click_rate': daily_click_rate,
            'false_positive_risk': 'N/A',
            'recommendation': 'No action - insufficient data',
            'action': 'none'
        }

    # Converting term
    elif conversions > 0:
        roas = ((conversions_value / (spend / 1000000)) * 100) if spend > 0 else 0
        return {
            'tier': 'converting',
            'confidence': 'N/A',
            'daily_click_rate': daily_click_rate,
            'recommendation': 'Performing well - no action needed',
            'action': 'none',
            'roas': f'{roas:.0f}%'
        }

    return None

# Usage example:
search_terms_data = [
    {'term': 'led strip lights', 'clicks': 177, 'conversions': 0, 'spend': 152.08},
    {'term': 'plaster in ceiling', 'clicks': 23, 'conversions': 0, 'spend': 45.32},
    {'term': 'some query', 'clicks': 7, 'conversions': 0, 'spend': 12.50},
    {'term': 'uno lighting', 'clicks': 89, 'conversions': 15.2, 'spend': 125.40, 'conversions_value': 1900.00}
]

tier1_terms = []
tier2_terms = []
tier3_terms = []
converting_terms = []

for term_data in search_terms_data:
    classification = classify_search_term(
        clicks=term_data['clicks'],
        conversions=term_data['conversions'],
        spend=term_data['spend']
    )

    if classification['tier'] == 1:
        tier1_terms.append({**term_data, **classification})
    elif classification['tier'] == 2:
        tier2_terms.append({**term_data, **classification})
    elif classification['tier'] == 3:
        tier3_terms.append({**term_data, **classification})
    elif classification['tier'] == 'converting':
        converting_terms.append({**term_data, **classification})

# Generate CSV files
import csv
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')
client_slug = 'uno-lighting'  # Replace with actual client

# Tier 1 CSV
with open(f'clients/{client_slug}/reports/keyword-audit-{today}-tier1.csv', 'w', newline='') as f:
    if tier1_terms:
        writer = csv.DictWriter(f, fieldnames=['term', 'clicks', 'spend', 'conversions', 'daily_click_rate', 'tier', 'confidence', 'recommendation'])
        writer.writeheader()
        writer.writerows(tier1_terms)

# Tier 2 CSV
with open(f'clients/{client_slug}/reports/keyword-audit-{today}-tier2.csv', 'w', newline='') as f:
    if tier2_terms:
        writer = csv.DictWriter(f, fieldnames=['term', 'clicks', 'spend', 'conversions', 'daily_click_rate', 'tier', 'confidence', 'next_review_date'])
        writer.writeheader()
        writer.writerows(tier2_terms)

# (Similar for tier3 and converting)
```

### Business Language
- Focus on revenue impact, not just metrics
- Quantify savings and growth potential
- Use clear action verbs (pause, increase, add, remove)
- Explain "why" not just "what"

## Output Formats

### Standard Report
Full analysis with all sections (use for comprehensive audits)

### Quick Action List
Just the prioritized actions (use for rapid implementation)

### Tier-Specific CSV Files
Generate four separate CSV files for tier-based workflow:

**1. tier1_negative_keywords.csv** (High Confidence - Immediate Action)
```csv
search_term,clicks,spend,conversions,daily_click_rate,tier,confidence,recommendation
led strip lights,177,152.08,0,2.95,1,very_high,Add as exact match negative keyword immediately
```

**2. tier2_negative_keywords.csv** (Medium Confidence - Monitor)
```csv
search_term,clicks,spend,conversions,daily_click_rate,tier,confidence,next_review_date
plaster in ceiling,23,45.32,0,0.38,2,moderate,2025-12-24
```

**3. tier3_insufficient_data.csv** (Low Confidence - Continue Monitoring)
```csv
search_term,clicks,spend,conversions,daily_click_rate,tier,confidence,action
some query,7,12.50,0,0.12,3,low,No action - insufficient data
```

**4. converting_search_terms.csv** (Performing Well - Keep Active)
```csv
search_term,clicks,conversions,spend,roas,status
uno lighting,89,15.2,125.40,1520%,Performing well - no action needed
```

**CSV Generation Instructions**:
1. Calculate daily_click_rate = total_clicks / 60 (for 60-day period)
2. Sort each tier by spend (descending) within the tier
3. Include all metadata columns for downstream analysis
4. Save files to `clients/{client-slug}/reports/keyword-audit-YYYY-MM-DD-tier{N}.csv`

### Negative Keyword Bulk Upload File
Formatted for Google Ads Editor (Tier 1 only):
```
Campaign,[Campaign Name],Negative Keyword,[keyword],Exact
Campaign,[Campaign Name],Negative Keyword,[keyword],Exact
```

## Resources

- [ROK Keyword Methodology](../../../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md)
- [Negative Keyword Strategies](negative-keyword-guide.md)
- [Match Type Best Practices](match-type-guide.md)

## Notes

- Focus on Search campaigns (Shopping has limited keyword control)
- Consider seasonality when identifying trends
- Cross-reference with landing page performance when CVR is low
- Always provide bulk upload formats for efficiency
- Track recommendation implementation success rate

