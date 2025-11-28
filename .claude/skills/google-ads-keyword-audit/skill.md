---
name: google-ads-keyword-audit
description: Performs targeted keyword and search term analysis for Google Ads Search campaigns. Identifies wasted spend, growth opportunities, and negative keyword candidates using actionable-only methodology. Use when analysing keywords, search terms, negative keywords, or Search campaign optimisation.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Write, Read, Bash
---

# Google Ads Keyword Audit Skill

## Instructions

When this skill is triggered:

1. **Identify the scope**:
   - Specific campaigns or full account
   - Date range (default: last 14 days for keyword analysis)
   - Minimum spend threshold (default: $50)
   - Account average metrics for relative benchmarking

2. **Load account context**:
   - Calculate account average ROAS, CTR, CVR
   - Identify campaign-specific benchmarks
   - Reference client margin goals (if available)

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

### Phase 3: Search Term Analysis
Analyze search queries:
- High-spend, zero-conversion queries (negative keyword candidates)
- Irrelevant queries triggered by broad/phrase match
- High-performing queries not yet added as keywords
- Query-level CTR and conversion patterns

**Output**: Negative keyword list and new keyword suggestions

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

### High Spend, Low ROAS Keywords
| Keyword | Campaign | Spend | Conversions | ROAS | Recommendation |
|---------|----------|-------|-------------|------|----------------|
| [keyword] | [campaign] | $XXX | X | 0.XX | Pause or reduce bid by 50% |
| ... | ... | ... | ... | ... | ... |

**Total waste identified**: $X,XXX in last [period]

### Zero-Conversion Queries (Negative Keywords)
| Search Term | Impressions | Clicks | Spend | Recommendation |
|-------------|------------|--------|-------|----------------|
| [query] | XXX | XX | $XXX | Add as negative keyword (campaign level) |
| ... | ... | ... | ... | ... |

**Action**: Add [N] negative keywords

## 🟢 Growth Opportunities

### High-Performing Keywords (Scale These)
| Keyword | Campaign | Conversions | ROAS | Current Bid | Recommendation |
|---------|----------|-------------|------|-------------|----------------|
| [keyword] | [campaign] | XX | X.XX | $X.XX | Increase bid to $X.XX (+20%) |
| ... | ... | ... | ... | ... | ... |

**Potential additional revenue**: $X,XXX/month

### Strong Queries to Add as Keywords
| Search Term | Impressions | Conversions | ROAS | Match Type | Recommendation |
|-------------|------------|-------------|------|------------|----------------|
| [query] | XXX | XX | X.XX | Phrase | Add as exact match keyword |
| ... | ... | ... | ... | ... | ... |

**Action**: Add [N] new exact match keywords

## 🟡 Declining Performance (Monitor & Adjust)

### Keywords with Performance Drops
| Keyword | Campaign | Metric | Change WoW | Possible Cause | Recommendation |
|---------|----------|--------|------------|----------------|----------------|
| [keyword] | [campaign] | CTR | -25% | Ad fatigue | Refresh ad copy |
| [keyword] | [campaign] | CVR | -18% | Landing page issue | Check page load time |
| ... | ... | ... | ... | ... | ... |

## Match Type Analysis

### Current Distribution
- Exact: XX% of spend, ROAS: X.XX
- Phrase: XX% of spend, ROAS: X.XX
- Broad: XX% of spend, ROAS: X.XX

### Recommendations
1. [Match type adjustment with reasoning]
2. [Additional match type strategy]

## Search Term Patterns

### Low CTR Queries (Relevance Issues)
[Queries with CTR < 1% indicating poor ad relevance]

**Action**: Review ad copy or add as negatives

### Irrelevant Query Themes
[Grouped irrelevant queries by theme]
- Theme 1: [e.g., "free", "DIY", "images"]
- Theme 2: [e.g., competitor names]

**Action**: Add broad match negatives

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
   -- Keyword performance
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
   
   -- Search terms
   SELECT 
     segments.search_term,
     metrics.impressions,
     metrics.clicks,
     metrics.cost_micros,
     metrics.conversions
   FROM search_term_view
   WHERE segments.date DURING LAST_14_DAYS
     AND campaign.status = 'ENABLED'
     AND metrics.clicks > 0
   ORDER BY metrics.cost_micros DESC
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

### Negative Keyword File
Formatted for bulk upload:
```
Campaign,[Campaign Name],Negative Keyword,[keyword],Broad
Campaign,[Campaign Name],Negative Keyword,[keyword],Phrase
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

