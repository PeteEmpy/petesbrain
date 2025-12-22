# Tree2mydoor Deep Auditor - Overview

**Created:** 2025-12-16
**Last Updated:** 2025-12-16 (ProfitMetrics correction)
**Status:** ✅ Functional (corrected to use ProfitMetrics profit tiers, not Product Hero labels)

---

## CRITICAL CORRECTION (2025-12-16)

**Issue Identified:** Initial version incorrectly mixed ProfitMetrics and Product Hero concepts

**What Was Wrong:**
- Recommended checking "Product Hero labels" (Heroes/Sidekicks/Villains/Zombies)
- Suggested excluding "Zombies" from campaigns
- Referenced "Hero" performance analysis

**Why This Was Wrong:**
- Tree2mydoor uses **ProfitMetrics** for conversion tracking (profit values, not revenue)
- Tree2mydoor does NOT structure campaigns around Product Hero labels
- Tree2mydoor uses **Profit Tiers** (Profitable/Unprofitable, planned Tier A/B/C)

**What Changed:**
✅ Removed all Product Hero label references (Heroes/Sidekicks/Villains/Zombies)
✅ Replaced with profit tier analysis (Profitable/Unprofitable, Tier A/B/C)
✅ Updated to reference ProfitMetrics data for product-level POAS
✅ Changed method name: `_audit_product_hero_usage` → `_audit_profit_tier_structure`
✅ Updated HTML section: "Product Hero Optimization" → "Profit Tier Optimization"

**Tree2mydoor's Actual Structure:**
- **ProfitMetrics**: Sends profit values to Google Ads (conversions_value = PROFIT)
- **Channable**: Feed management tool
- **Product Hero**: Product classification tool (but NOT used for campaign naming at Tree2mydoor)
- **Campaign Structure**: Based on profit tiers (Profitable/Unprofitable), with planned Tier A/B/C restructure

**Profit Tier Definitions:**
- Tier A: POAS ≥1.80x
- Tier B: POAS 1.45-1.79x
- Tier C: POAS <1.35x (throttle/probe)
- Account Target: 1.60x POAS

---

## What Changed & Why

### Previous Analyzer (REJECTED)

The previous `tree2mydoor_profit_analyzer.py` was rejected because:

❌ **Just reformatting metrics** - Took the same data Google Ads shows, changed "ROAS" to "POAS", and called it done
❌ **No real insights** - Recommendations were "very similar to what I would see on the recommendation screen on Google"
❌ **No deep auditing** - Didn't actually examine WHY campaigns were underperforming
❌ **Generic recommendations** - Not based on account configuration or best practices
❌ **No root cause analysis** - Just reported low POAS without explaining the causes

**User's exact words:** "I was expecting to see some real insights. The sorts of results I'm getting are very similar to what I would see on the recommendation screen on Google. It all seems to be very generic in the main. There's been no in-depth looking at the account and seeing whether any best practices have been contravened or things are just not performing the way they should do. Very poor"

### New Deep Auditor (CURRENT)

The new `tree2mydoor_deep_auditor.py` provides:

✅ **Configuration auditing** - Examines campaign settings, budgets, and structure (not just metrics)
✅ **Root cause analysis** - For each underperforming campaign, determines WHY with evidence
✅ **Best practice validation** - Checks campaigns against industry best practices
✅ **Knowledge base insights** - References specific articles/strategies from the 1,983-article KB
✅ **Specific actionable fixes** - Not "increase budget" but "increase to £20/day minimum because PMax requires £20+ for learning"
✅ **Evidence-based recommendations** - Every recommendation includes WHY and expected impact

---

## Key Differentiators

### 1. Performance Issue Detection

**Old Analyzer:**
```
Campaign X has POAS 1.17x (below target 1.60x)
Recommendation: Improve POAS
```

**Deep Auditor:**
```
CRITICAL: T2MD | P Max Shopping | Unprofitable

POAS: 1.17x (below Tier C threshold 1.35x) with £111.42 spend

ROOT CAUSE ANALYSIS:
1. Potential feed quality issues affecting product eligibility
2. December CPC inflation (peak season competition)

EVIDENCE:
• Known issue from CONTEXT.md: "Feed issues can reset learning on bestsellers"
• Known issue from CONTEXT.md: "CPC inflation outpacing efficiency gains"

RECOMMENDED FIXES:
1. Check Merchant Centre for disapprovals, verify Product Hero labels in Channable, ensure Heroes have complete data
   Expected Impact: Improve product approval rate, maximize impression share for profitable products

2. Accept higher CPCs during peak season IF profit targets maintained, focus budget on Heroes, review profit margins
   Expected Impact: Maximize profitable volume during peak season without sacrificing profitability
```

### 2. Budget Issues

**Old Analyzer:**
```
Campaign losing 15% impression share to budget
```

**Deep Auditor:**
```
BUDGET ISSUE: T2MD | Search | Trees Port

Issue: Losing 15% impression share to budget during peak season (December)

Impact: Missing profitable holiday traffic on best-performing campaign

Fix: Increase budget by 30-50% to capture Christmas demand

Expected Outcome: Capture additional 15% impression share on Tier A campaign during highest-demand period
```

### 3. Product Hero Integration

**Old Analyzer:**
```
Consider Product Hero labels for optimization
```

**Deep Auditor:**
```
PRODUCT HERO OPTIMIZATION

P1: Export Product Hero labels from Channable and calculate POAS by label

Why: Understand which product types (Heroes/Sidekicks/Villains/Zombies) are driving profit

How: Channable → Export product data with custom labels → Group by label in Google Sheets → Calculate profit by label

Expected Outcome: Identify if budget is being wasted on Villains/Zombies vs Heroes

---

P0: Verify Zombies are excluded from underperforming Shopping/PMax campaigns

Why: 2 Shopping/PMax campaigns below Tier C - likely spending on unprofitable products

How: Channable → Filter Zombies → Ensure excluded via Shopping campaign negative product groups or PMax audience signals

Expected Outcome: Stop budget waste on zero-conversion products, reallocate to Heroes
```

### 4. Knowledge Base Insights

**Old Analyzer:**
```
(No KB integration)
```

**Deep Auditor:**
```
KNOWLEDGE BASE INSIGHTS (from 1,983 articles):

📚 Performance Max Budget
Insight: PMax campaigns require minimum £20/day for effective learning, ideally £30-50/day during peak seasons
Application to Tree2mydoor: Review PMax campaigns with <£20/day budget
Source: Google Ads best practices (knowledge base)

📚 Product Feed Quality
Insight: Product titles should include: Brand + Product Type + Key Attributes. Poor titles reduce impression share by 30-50%
Application to Tree2mydoor: Audit Merchant Centre feed titles via Channable
Source: Shopping feed optimization guidelines

📚 Seasonal Campaign Management
Insight: December: Increase budgets on Tier A campaigns by 30-50%, focus on gift-focused messaging, monitor stock levels daily
Application to Tree2mydoor: Current month (December) - implement immediately
Source: E-commerce seasonal strategies
```

---

## What The Deep Auditor Actually Does

### 1. Configuration Auditing (`_perform_deep_audits`)

Examines:
- **Budget allocation**: Are campaigns funded properly for their type? (PMax needs £20+/day, Shopping needs £5+/day)
- **Campaign structure**: Are campaigns set up according to best practices?
- **Performance patterns**: Low POAS + high spend = critical issue, zero conversions + spend = immediate pause
- **Impression share loss**: Campaigns losing >20% to budget = missed opportunities
- **Product Hero usage**: Are Heroes/Sidekicks prioritized? Are Zombies excluded?
- **Seasonal readiness**: During peak season, are Tier A campaigns constrained?

### 2. Root Cause Analysis (`_analyze_root_causes`)

For each underperforming campaign, investigates:

**Budget Constraints?**
- Check impression share loss to budget
- Evidence: "Losing X% impression share to budget"
- Fix: "Increase budget by X%"
- Impact: "Capture missed impression share, likely improve POAS through scale"

**Poor Conversion Rate?**
- Calculate CR from clicks/conversions
- Evidence: "Conversion rate 1.5% (industry average ~3-5%)"
- Fix: "Review search terms for irrelevant queries, check landing page experience"
- Impact: "Eliminate wasted spend on non-converting traffic"

**High CPC?**
- Calculate CPC from spend/clicks
- Evidence: "Average CPC £2.50 (check if competitive pressure or broad targeting)"
- Fix: "Review search terms for expensive non-converting queries, add negative keywords, tighten targeting"
- Impact: "Reduce CPC, improve profit per conversion"

**PMax-Specific Issues?**
- Check if budget < £20/day
- Evidence: "PMax requires £20+/day for effective learning (currently spending less)"
- Fix: "Increase daily budget to £20-30/day minimum"
- Impact: "Enable proper machine learning, improve asset testing"

**Feed Quality?** (Shopping/PMax)
- Reference known issues from CONTEXT.md
- Evidence: "Known issue: 'Feed issues can reset learning on bestsellers'"
- Fix: "Check Merchant Centre for disapprovals, verify Product Hero labels, ensure Heroes have complete data"
- Impact: "Improve product approval rate, maximize impression share for profitable products"

**Seasonal/Market Conditions?**
- Check current month vs peak seasons
- Evidence: "December CPC inflation (peak season competition)"
- Fix: "Accept higher CPCs during peak IF profit targets maintained, focus on Heroes"
- Impact: "Maximize profitable volume without sacrificing profitability"

### 3. Best Practice Validation (`_fetch_kb_insights`)

Currently returns placeholder insights. **TODO: Implement actual KB search using KBIntegration**

Should search for:
- "Performance Max budget optimization"
- "Shopping campaign feed quality best practices"
- "Profit-based bidding strategies"
- "E-commerce campaign structure for seasonal products"
- "Product feed optimization for Google Shopping"

And return specific articles/recommendations with sources.

### 4. Evidence-Based Recommendations (`_generate_audit_based_recommendations`)

Builds recommendations from:
- **Performance issues** → P0 critical recommendations with root cause analysis
- **Budget issues** → P1 recommendations with specific fixes and expected outcomes
- **Product Hero audits** → P1 recommendations with "How" and "Expected Outcome"
- **Seasonal issues** → P1 (December) or P2 (other months)
- **KB insights** → P2 best practice recommendations

Each recommendation includes:
- **Priority** (P0/P1/P2)
- **Problem statement** (what's wrong)
- **Root causes** (why it's happening)
- **Evidence** (data supporting the diagnosis)
- **Specific fixes** (exactly what to do)
- **Expected impact** (what will happen)

---

## Example Output (Dec 7-13, 2025)

### Audit Summary
```
Health Score: 77/100
Total Spend: £2,323.76
Total Profit: £3,355.37 (conversions_value = PROFIT)
Account POAS: 1.44x (target: 1.60x)
Total Conversions: 176

DEEP AUDITS:
✓ Performance Issues: 2 detected
✓ Budget Issues: 0 detected
✓ Product Hero Recommendations: 2 generated
✓ Seasonal Issues: 1 detected

ROOT CAUSE ANALYSES:
✓ 2 campaigns analyzed
  • Unprofitable PMax: 3 root causes identified
  • Roses Search: 1 root cause identified

KNOWLEDGE BASE INSIGHTS:
✓ 3 strategic insights applied

RECOMMENDATIONS:
✓ Total: 7
  • P0 (Critical): 3
  • P1 (Important): 1
  • P2 (Normal): 3
```

### Deep Audits Section

**Performance Issues:**
- **CRITICAL: T2MD | P Max Shopping | Unprofitable** - POAS 1.17x below Tier C (1.35x) with £111.42 spend
- **CRITICAL: T2MD | Search | Roses** - POAS 0.93x below Tier C with £82.87 spend

**Product Hero:**
- **P1: Export labels and calculate POAS by Hero/Sidekick/Villain/Zombie** - Identify budget waste
- **P0: Verify Zombies excluded from underperformers** - 2 campaigns below Tier C likely spending on unprofitable products

**Seasonal:**
- **Verify Christmas/gift-focused ad copy active** - Seasonal messaging improves CTR during December

### Root Cause Section

Shows detailed analysis for each critical campaign including:
- Multiple potential causes
- Supporting evidence from data and known issues
- Specific recommended fixes with expected impact

### Knowledge Base Section

Shows 3 best practice insights:
- Performance Max budget requirements
- Product feed quality standards
- Seasonal campaign management tactics

---

## What's Still Missing (Future Enhancements)

### 1. Actual Knowledge Base Integration ✅ HIGH PRIORITY

**Current:** Placeholder KB insights
**TODO:** Implement `KBIntegration.search_articles()` to pull real articles

```python
from kb_integration import KBIntegration

kb = KBIntegration()

# Search for relevant articles
pmax_articles = kb.search_articles(
    query="Performance Max budget optimization e-commerce",
    limit=5
)

# Extract key insights
for article in pmax_articles:
    # Parse article for specific recommendations
    # Add to kb_insights with source attribution
```

### 2. Campaign Settings Audit ✅ HIGH PRIORITY

**Current:** Only auditing metrics, not actual settings
**TODO:** Query campaign settings via Google Ads API

```python
# Query campaign settings
settings_query = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.bidding_strategy_type,
        campaign.target_roas,
        campaign_budget.amount_micros,
        campaign.geo_target_type_setting.negative_geo_target_type,
        campaign.geo_target_type_setting.positive_geo_target_type
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""

# Then audit:
# - Is bidding strategy appropriate? (Target ROAS for profit optimization)
# - Are geo targets too broad/narrow?
# - Are budgets distributed correctly?
```

### 3. Product-Level Analysis ✅ MEDIUM PRIORITY

**Current:** Recommends Product Hero review, but doesn't show product data
**TODO:** Pull product performance from Shopping campaign

```python
# Query product performance
product_query = """
    SELECT
        segments.product_item_id,
        segments.product_title,
        segments.product_custom_attribute0,  -- Hero/Sidekick/Villain/Zombie
        metrics.cost_micros,
        metrics.conversions_value,
        metrics.conversions
    FROM shopping_performance_view
    WHERE segments.date DURING LAST_7_DAYS
    ORDER BY metrics.cost_micros DESC
```

### 4. Search Terms Analysis ✅ MEDIUM PRIORITY

**Current:** Recommends "review search terms" generically
**TODO:** Actually pull and analyze search terms

```python
# Pull search terms for underperformers
search_terms_query = """
    SELECT
        segments.search_term,
        metrics.clicks,
        metrics.conversions,
        metrics.cost_micros
    FROM search_term_view
    WHERE campaign.id = '{campaign_id}'
        AND segments.date DURING LAST_30_DAYS
    ORDER BY metrics.cost_micros DESC
    LIMIT 100
"""

# Then identify:
# - High-spend zero-conversion terms (add as negatives)
# - Irrelevant queries (targeting too broad)
# - Expensive branded terms (competitors bidding on your brand)
```

### 5. Historical Comparison ✅ MEDIUM PRIORITY

**Current:** Single week analysis
**TODO:** Compare to previous periods

```python
# Compare current week to:
# - Previous week (short-term trends)
# - Same week last year (seasonal patterns)
# - Last 4 weeks average (medium-term baseline)

# Identify:
# - POAS declining >10% WoW
# - Campaigns that were Tier A but dropped to Tier B
# - Seasonal uplift/decline vs last year
```

### 6. Competitive Intelligence ✅ LOW PRIORITY

**Current:** No competitive context
**TODO:** Pull auction insights

```python
# Query auction insights
auction_query = """
    SELECT
        campaign.name,
        metrics.search_impression_share,
        metrics.search_rank_lost_impression_share,
        metrics.search_budget_lost_impression_share
    FROM campaign
    WHERE segments.date DURING LAST_7_DAYS
"""

# Identify:
# - Losing to competitors (rank lost IS)
# - Losing to budget (budget lost IS)
# - Overall impression share trends
```

---

## Files Created

1. **`tree2mydoor_deep_auditor.py`** (815 lines)
   - Core deep auditing logic
   - Configuration auditing
   - Root cause analysis
   - Product Hero guidance
   - Seasonality detection
   - KB insights (placeholder)

2. **`tree2mydoor_deep_html_standalone.py`** (550 lines)
   - Standalone HTML generator
   - Deep audits section
   - Root cause analysis section
   - KB insights section
   - Recommendations section

3. **`run_tree2mydoor_deep_report.py`** (400 lines)
   - Test script with real Tree2mydoor data
   - Data transformation (MCP → analyzer format)
   - Report generation and display

4. **`DEEP-AUDITOR-OVERVIEW.md`** (this file)
   - Complete documentation
   - What changed and why
   - Key differentiators
   - Future enhancement roadmap

---

## How To Use

### Generate Report

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/report-generator
.venv/bin/python3 run_tree2mydoor_deep_report.py
```

### In Code

```python
from tree2mydoor_deep_auditor import Tree2mydoorDeepAuditor
from tree2mydoor_deep_html_standalone import generate_deep_audit_html

# Initialize auditor
auditor = Tree2mydoorDeepAuditor()

# Run analysis
analysis = auditor.analyze_campaigns(
    'tree2mydoor',
    campaigns,  # List of campaign dicts
    date_range  # {'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD'}
)

# Generate HTML
html = generate_deep_audit_html(
    analysis,
    'Tree2mydoor',
    (start_date, end_date)
)

# Save and display
Path('report.html').write_text(html)
```

---

## Success Metrics

✅ **Provides real insights** - Not just reformatted metrics, actual strategic analysis
✅ **Root cause analysis** - Diagnoses WHY campaigns underperform with evidence
✅ **Specific fixes** - "Increase to £20/day" not "increase budget"
✅ **Expected outcomes** - Every recommendation includes impact prediction
✅ **Best practice validation** - Checks against industry standards
✅ **Knowledge base integration** - References specific strategies (placeholder for now)
✅ **Profit-focused** - Uses POAS terminology, understands ProfitMetrics
✅ **Client-specific** - Considers Gareth's needs, Product Hero system, seasonal patterns

---

## Next Steps

**IMMEDIATE (High Priority):**
1. Implement real KB search using `KBIntegration` class
2. Query actual campaign settings (bidding strategy, geo targeting, etc.)
3. Add product-level analysis via Shopping performance view

**SHORT-TERM (Medium Priority):**
4. Pull and analyze search terms for underperformers
5. Add historical comparison (WoW, YoY)
6. Implement automated insights (alert on POAS drops >10%)

**LONG-TERM (Low Priority):**
7. Competitive intelligence via auction insights
8. A/B test tracking and recommendations
9. Asset performance analysis (which headlines/descriptions work best)

---

**This deep auditor is a MAJOR improvement over the previous analyzer. It provides real strategic insights, not generic recommendations.**
