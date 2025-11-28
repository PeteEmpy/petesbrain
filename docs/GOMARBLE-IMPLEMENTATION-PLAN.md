# GoMarble Prompt Library Implementation Plan

**Date:** 2025-11-19
**Status:** Planning Phase
**Goal:** Integrate GoMarble's structured analytics prompts into PetesBrain for automated client reporting and optimization

**GoMarble Prompt Library:** https://prompting.gomarble.ai/
- Official prompt library with all structured analytics templates
- Organized by platform (Google Ads, Meta Ads, GA4, Shopify)
- Prompts organized into sections/subsections - dig into each to see full library
- Monitor for updates and new prompt releases

---

## Overview

GoMarble's prompt library provides production-grade templates for advertising analytics across Meta Ads, Google Ads, GA4, and Shopify. This implementation plan adapts their approach to ROK's existing infrastructure and client base.

**Your Advantages:**
- ✅ Google Ads MCP already operational
- ✅ Google Analytics MCP already operational
- ✅ 16 active clients with diverse needs
- ✅ Established automation patterns (agents, skills)
- ✅ Task management and reporting systems in place

---

## Phase 1: Quick Wins (Week 1-2)

### Objective
Implement 3 high-value prompts using **existing MCP servers** for immediate client value.

### 1A. Google Ads Weekly E-commerce Report (Priority P0)

**Why Start Here:**
- Uses existing `mcp__google-ads__run_gaql` capability
- Applies to 8 e-commerce clients (Smythson, Superspace, Godshot, Just Bin Bags, etc.)
- Replaces manual monthly reporting with automated weekly insights

**Implementation:**

**Create Skill:** `.claude/skills/google-ads-weekly-report/`

**skill.md content:**
```markdown
# Google Ads Weekly E-commerce Report

Generate comprehensive weekly Google Ads performance analysis for e-commerce clients.

## When to Use
- Weekly client check-ins
- Month-end reporting preparation
- Performance anomaly investigations

## Input Required
- Client name (for CONTEXT.md and account lookup)
- Date range (defaults to last 7 days)

## Output
Markdown report with:
- Campaign overview (spend, conversions, ROAS, CPA)
- Product-level performance (top 10 best/worst by ROAS)
- Placement analysis (Shopping, YouTube, Display, Discover)
- Week-over-week changes (>15% flagged)
- 3-5 prioritized recommendations

## Prompt Template
[Adapted from GoMarble Google Ads Prompt 1]
```

**Test Clients:**
1. **Smythson** - Complex Shopping + PMax setup
2. **Superspace** - Multi-market (UK/US)
3. **Godshot** - Single PMax campaign (simplest test case)

**Success Criteria:**
- Generate report in <5 minutes
- Accurately flag 15%+ performance changes
- Surface product-level insights not visible in Google Ads UI

**Time Estimate:** 4 hours (2 hours skill creation, 2 hours testing)

---

### 1B. Google Ads Auction Insights Analysis (Priority P1)

**Why This Matters:**
- Identifies lost impression share (budget vs rank)
- Explains why campaigns aren't scaling
- Guides budget increase requests to clients

**Client Use Cases:**
- **Devonshire Hotels**: Currently managing budget constraints
- **Accessories for the Home**: Recently increased budget
- **National Motorsports Academy**: High CPA, need impression share context

**Implementation:**

**Create Skill:** `.claude/skills/google-ads-auction-insights/`

**Workflow:**
1. User: "Analyze auction insights for [client]"
2. Skill reads CONTEXT.md for account ID
3. Pulls impression share metrics via GAQL
4. Calculates lost IS% (budget vs rank)
5. Generates recommendation: "Increase budget by £X to recover Y% impression share"

**Output Format:**
```markdown
## Auction Insights: [Client Name]
**Period:** [Date Range]

### Impression Share Summary
| Campaign | IS% | Lost (Budget) | Lost (Rank) | Opportunity |
|----------|-----|---------------|-------------|-------------|
| ...      | ... | ...           | ...         | ...         |

### Key Findings
- [Campaign X] losing 23% IS due to budget caps (potential £X revenue)
- [Campaign Y] losing 12% IS due to rank (needs bid/quality improvements)

### Recommended Actions
1. [Prioritized by revenue impact]
```

**Time Estimate:** 6 hours (skill creation + GAQL query optimization)

---

### 1C. GA4 Traffic Source Performance (Priority P1)

**Why This Matters:**
- Clients ask "Which channels are working?"
- Attribution confusion (GA4 vs Google Ads conversion counting)
- Budget allocation decisions

**Client Use Cases:**
- **Smythson**: Multi-channel strategy needs attribution clarity
- **Superspace**: Understanding organic vs paid performance
- **Tree2MyDoor**: Seasonal traffic pattern analysis

**Implementation:**

**Create Skill:** `.claude/skills/ga4-channel-performance/`

**Uses:** `mcp__google-analytics__get_traffic_sources` + `mcp__google-analytics__run_report`

**Output:**
```markdown
## Traffic Source Performance: [Client]
**Period:** [Date Range]

### Channel Overview
| Channel        | Sessions | Revenue  | ROAS | Conv Rate | vs Previous |
|----------------|----------|----------|------|-----------|-------------|
| Organic Search | ...      | ...      | N/A  | ...       | +12%        |
| Paid Search    | ...      | ...      | 420% | ...       | -5%         |
| Paid Social    | ...      | ...      | 380% | ...       | +18%        |
| Direct         | ...      | ...      | N/A  | ...       | +3%         |

### Attribution Comparison
- Last-click: £X revenue attributed to Paid Search
- Data-driven: £Y revenue attributed to Paid Search
- **Discrepancy:** £Z (+15% more credit to Paid Search in data-driven)

### Recommendations
[Underperforming channels with high spend]
[Undervalued channels with strong assisted conversions]
```

**Time Estimate:** 5 hours

---

## Phase 2: Client-Facing Automation (Week 3-4)

### Objective
Create **automated monthly client reports** using GoMarble's visual storytelling approach.

### 2A. Monthly Client Dashboard Generator

**Replaces:** Manual monthly report creation (currently ad-hoc)

**Applies to:** All 16 clients (prioritize top 5 by revenue)

**Implementation:**

**Create Agent:** `agents/monthly-client-dashboard/`

**Workflow:**
1. Runs on 1st of each month
2. For each active client:
   - Reads CONTEXT.md for account details
   - Pulls Google Ads data (previous month vs 2 months prior)
   - Pulls GA4 data (if property ID exists)
   - Generates visual HTML dashboard using GoMarble format
   - Saves to `clients/[client]/reports/monthly/YYYY-MM-dashboard.html`
   - Creates draft email in `clients/[client]/documents/`

**Template Structure (GoMarble-inspired):**
```html
<!DOCTYPE html>
<html>
<head>
  <!-- ROK branding, not GoMarble -->
  <link rel="stylesheet" href="/shared/assets/branding/roksys-report-styles.css">
</head>
<body>
  <div class="chapter">
    <h2>Chapter 1: The Bottom Line</h2>
    <div class="metrics-grid">
      <div class="metric">
        <span class="value">£42,156</span>
        <span class="label">Revenue</span>
        <span class="change positive">+18% vs Oct</span>
      </div>
      <!-- More metrics -->
    </div>
    <div class="story-box">
      <strong>The Story:</strong> November revenue grew 18% while maintaining
      ROAS at 420%, indicating efficient scaling without quality degradation.
    </div>
  </div>

  <div class="chapter">
    <h2>Chapter 2: Where Revenue Came From</h2>
    <!-- Campaign breakdown with charts -->
  </div>

  <!-- More chapters -->
</body>
</html>
```

**"Chapters" (GoMarble Visual Storytelling Format):**
1. **The Bottom Line** - Revenue, ROAS, spend, conversions (headline metrics)
2. **Campaign Performance** - Which campaigns drove results
3. **Product Winners** - Top 10 products (e-commerce clients only)
4. **What Changed** - Week-over-week trends and anomalies
5. **Looking Ahead** - Next month goals and experiments planned

**Client Customization:**
- E-commerce clients: Include product performance
- Lead gen clients (NDA, NMA): Include lead quality metrics
- Hotel clients (Devonshire): Include booking value, occupancy correlation

**Time Estimate:** 12 hours (template design + data integration)

---

### 2B. Weekly Client Email Digests

**Use Case:** Replace ad-hoc "weekly check-in" emails with consistent format

**Implementation:**

**Create Agent:** `agents/weekly-client-digest/`

**Schedule:** Every Monday 6am (review Sunday performance)

**Format (Email, not dashboard):**
```
Subject: [Client Name] - Weekly Performance Summary (Nov 11-17)

Hi [Client Contact],

Here's your weekly snapshot:

📊 LAST WEEK AT A GLANCE
Revenue: £X (+Y% vs prior week)
ROAS: X% (target: Y%)
Conversions: X (+Y vs prior week)

✅ WHAT'S WORKING
• [Campaign X] increased ROAS to 520% (+12% WoW)
• [Product Y] became #1 seller with £X revenue
• Mobile traffic conversion rate up 8%

⚠️ WATCHING CLOSELY
• [Campaign Z] ROAS dropped to 280% (investigating)
• [Placement] costs increased 15% with flat conversions

📅 THIS WEEK'S FOCUS
• [Action item from last meeting/task]
• [Scheduled optimization]

Let me know if you'd like to discuss any of these points.

Best,
Peter
```

**Trigger:** Can also be run on-demand: "Generate weekly digest for Smythson"

**Time Estimate:** 8 hours

---

## Phase 3: Optimization Automation (Week 5-6)

### Objective
Implement **proactive optimization detection** - system tells you what needs fixing.

### 3A. Creative Fatigue Detector (Meta Ads)

**Prerequisites:** Meta Ads MCP server setup required (not currently active)

**Skip for now** - Focus on Google Ads where infrastructure exists.

---

### 3B. Google Ads Budget Opportunity Detector

**Why This Matters:**
- Identifies campaigns hitting budget caps with strong ROAS
- Quantifies revenue opportunity from budget increases
- Generates client budget increase recommendations

**Implementation:**

**Create Agent:** `agents/budget-opportunity-detector/`

**Schedule:** Daily 9am check

**Logic (GoMarble-inspired):**
```python
# Pseudo-code
for each client:
    campaigns = get_campaigns_with_metrics(last_14_days)

    for campaign in campaigns:
        # Check if limited by budget
        if campaign.impression_share_lost_budget > 10%:
            if campaign.roas > client_target_roas * 1.2:  # 20% above target
                # Calculate opportunity
                current_daily_budget = campaign.daily_budget
                lost_is_pct = campaign.impression_share_lost_budget

                # Estimate: recovering 50% of lost IS
                recommended_increase = current_daily_budget * (lost_is_pct / 100) * 0.5
                estimated_revenue_gain = campaign.avg_daily_revenue * (lost_is_pct / 100) * 0.5

                # Create task if material opportunity
                if estimated_revenue_gain > 500:  # £500+ opportunity
                    create_task(
                        client=client,
                        title=f"[{client}] Budget increase opportunity: {campaign.name}",
                        priority="P1",
                        notes=f"""
                        Campaign: {campaign.name}
                        Current ROAS: {campaign.roas}%
                        Lost IS (Budget): {lost_is_pct}%

                        Recommendation: Increase budget by £{recommended_increase}/day
                        Estimated revenue gain: £{estimated_revenue_gain}/day

                        Current: £{current_daily_budget}/day
                        Proposed: £{current_daily_budget + recommended_increase}/day
                        """
                    )
```

**Output:** Creates P1 tasks in Task Manager for manual review

**Time Estimate:** 10 hours (GAQL queries + opportunity calculation logic)

---

### 3C. Keyword Waste Detector

**Adaptation:** GoMarble "Google Ads Keyword Optimization" prompt

**Implementation:**

**Create Agent:** `agents/keyword-waste-detector/`

**Schedule:** Weekly (Sunday 8pm, ready for Monday review)

**Detection Criteria:**
1. **Wasted Spend:**
   - Spend ≥ £50 in last 30 days
   - ROAS < account_average × 0.7
   - Action: Pause or reduce bids

2. **Growth Opportunities:**
   - ≥ 2 conversions in last 30 days
   - ROAS ≥ account_average × 1.3
   - Impression share lost (rank) > 10%
   - Action: Increase bids

3. **Zero-Conversion Waste:**
   - Spend ≥ £20
   - Zero conversions in last 30 days
   - Action: Pause

**Output:**
- CSV file: `clients/[client]/reports/keyword-opportunities/YYYY-MM-DD-keyword-review.csv`
- Creates tasks for manual review before applying changes
- Logs to experiment tracker when changes applied

**Time Estimate:** 12 hours (complex GAQL queries + logic)

---

## Phase 4: Cross-Channel Integration (Week 7-8)

### Objective
Implement **unified reporting** across Google Ads + GA4 (Shopify/Meta later).

### 4A. Blended Metrics Calculator

**GoMarble Concept:** "MER = Shopify Revenue / (Meta Spend + Google Spend)"

**ROK Adaptation:** "MER = GA4 Revenue / Google Ads Spend"

**Implementation:**

**Create Utility:** `shared/blended_metrics.py`

**Functions:**
```python
def calculate_mer(client_name, date_range):
    """
    Calculate Marketing Efficiency Ratio (blended ROAS).

    Returns GA4 transaction revenue divided by Google Ads spend.
    Useful for understanding true revenue attribution vs Google Ads reported conversions.
    """

def calculate_attribution_discrepancy(client_name, date_range):
    """
    Compare Google Ads conversion value vs GA4 transaction revenue.

    Identifies:
    - Over-attribution (Google Ads reports more than GA4)
    - Under-attribution (GA4 sees more revenue than Google Ads)
    """

def generate_cross_platform_report(client_name, date_range):
    """
    Creates "Analyst Pack" style report:
    - Google Ads reported metrics
    - GA4 attributed metrics
    - Blended metrics
    - Discrepancy analysis
    """
```

**Use Case:**
When client says "Google Ads says ROAS is 420% but I'm not seeing that revenue in my bank account" - this explains the gap.

**Time Estimate:** 8 hours

---

### 4B. Analyst Pack Generator

**GoMarble Format:** 14 days vs prior 14 days across all platforms

**ROK Implementation:** Google Ads + GA4 unified view

**Create Skill:** `.claude/skills/analyst-pack/`

**Output Sections:**
1. **Executive Summary (L14 vs P14):**
   - Google Ads: Spend, Conv, ROAS, CTR, CPC
   - GA4: Revenue, Sessions, Conv Rate, Traffic Sources
   - Blended: MER, attribution gap
   - One-line "what changed & why"

2. **Campaign Performance Table:**
   - Top 12 campaigns by spend
   - Metrics: Spend, Conv, ROAS, CTR, CPC, Δ% vs P14
   - Outlier flags (>20% change)

3. **Traffic Source Insights:**
   - GA4 channel performance
   - Organic vs Paid comparison
   - Attribution model differences

4. **One-Slide Brief:**
   - What changed
   - Top 3 drivers
   - Biggest risk
   - Key unknowns

**When to Use:**
- Monthly client reports
- Performance investigation
- Budget allocation discussions
- Client business reviews

**Time Estimate:** 10 hours

---

## Phase 5: Advanced Automation (Week 9-12)

### Objective
Implement **predictive and seasonal analysis** for strategic planning.

### 5A. Seasonal Pattern Analyzer

**GoMarble:** "12+ months historical data, identify performance peaks"

**ROK Application:**
- **Smythson**: Christmas gifting season (Nov-Dec)
- **Superspace**: Back-to-school (Aug-Sep)
- **Devonshire Hotels**: Wedding season (May-Sep), Christmas events (Nov-Dec)

**Implementation:**

**Create Skill:** `.claude/skills/seasonal-analysis/`

**Workflow:**
1. Pull 24 months Google Ads data via GAQL
2. Calculate monthly performance index (each month vs annual average)
3. Identify:
   - Strongest months (>120% of average)
   - Weakest months (<80% of average)
   - Week-of-month patterns (first week vs last week)
   - Day-of-week patterns

4. Generate recommendations:
   - Budget allocation calendar
   - Campaign launch timing
   - Creative refresh schedule

**Output:**
```markdown
## Seasonal Performance: [Client]
**Analysis Period:** Nov 2023 - Oct 2025

### Performance Heat Map
| Month | 2023 Index | 2024 Index | 2025 Index | Pattern |
|-------|------------|------------|------------|---------|
| Jan   | 85%        | 82%        | --         | Low     |
| Feb   | 92%        | 88%        | --         | Low     |
| ...   | ...        | ...        | ...        | ...     |
| Nov   | 145%       | 152%       | --         | Peak    |
| Dec   | 168%       | 175%       | --         | Peak    |

### Strategic Insights
- **Christmas period (Nov-Dec)**: Consistently 150%+ of average
  - Recommendation: Increase budget by 50% starting Nov 1
  - Historical ROAS: Maintains 400%+ even with increased spend

- **Q1 slowdown (Jan-Mar)**: Consistently 80-90% of average
  - Recommendation: Reduce budget by 20%, focus on efficiency
  - Shift budget to brand awareness/retargeting
```

**Time Estimate:** 12 hours (data processing + visualization)

---

### 5B. Growth Opportunity Modeler

**GoMarble:** "Project revenue from 20% spend increase with marginal ROAS decay"

**ROK Application:**
When client asks: "What happens if we increase budget by £500/day?"

**Implementation:**

**Create Skill:** `.claude/skills/growth-projection/`

**Model:**
```python
def project_budget_increase_impact(
    client_name,
    campaign_id,
    current_daily_budget,
    proposed_daily_budget,
    historical_days=30
):
    """
    Project revenue impact from budget increase.

    Methodology:
    1. Calculate historical marginal ROAS at different spend levels
    2. Fit diminishing returns curve
    3. Project ROAS at new spend level
    4. Estimate revenue impact (best case, base case, worst case)
    5. Calculate breakeven spend increase
    """

    # Pull historical data
    daily_performance = get_daily_campaign_data(campaign_id, historical_days)

    # Calculate marginal ROAS by spend quartile
    # Example: Days with £400-500 spend had 420% ROAS, days with £500-600 had 380% ROAS
    marginal_roas_curve = calculate_marginal_returns(daily_performance)

    # Project at new spend level
    budget_increase = proposed_daily_budget - current_daily_budget
    projected_roas = estimate_roas_at_spend(marginal_roas_curve, proposed_daily_budget)

    # Best case: No diminishing returns (current ROAS maintained)
    best_case_revenue = budget_increase * current_roas

    # Base case: Projected ROAS from curve
    base_case_revenue = budget_increase * projected_roas

    # Worst case: 70% of projected ROAS (conservative)
    worst_case_revenue = budget_increase * (projected_roas * 0.7)

    return {
        'current_daily_budget': current_daily_budget,
        'proposed_daily_budget': proposed_daily_budget,
        'budget_increase': budget_increase,
        'current_roas': current_roas,
        'projected_roas': projected_roas,
        'best_case': best_case_revenue,
        'base_case': base_case_revenue,
        'worst_case': worst_case_revenue,
        'confidence': calculate_confidence(marginal_roas_curve)
    }
```

**Output:**
```markdown
## Budget Increase Projection: [Campaign Name]

### Scenario
- Current: £500/day
- Proposed: £700/day (+£200/day)
- Historical ROAS: 420%

### 30-Day Projections

**Best Case Scenario (95% confidence)**
- Projected ROAS: 420% (no diminishing returns)
- Additional Revenue: £6,300/month
- ROI: 315% on incremental spend

**Base Case Scenario (70% confidence)**
- Projected ROAS: 380% (10% diminishing returns)
- Additional Revenue: £5,700/month
- ROI: 285% on incremental spend

**Worst Case Scenario (40% confidence)**
- Projected ROAS: 265% (30% diminishing returns)
- Additional Revenue: £3,975/month
- ROI: 199% on incremental spend

### Recommendation
Proceed with budget increase. Even in worst case, incremental ROAS (265%) exceeds minimum target (200%).

### Risk Factors
- Model based on 30 days data (limited confidence)
- Market competition may have changed
- Seasonal effects not fully captured
```

**Time Estimate:** 16 hours (statistical modeling + validation)

---

## Phase 6: Meta Ads Integration (Week 13-16)

**Prerequisites:**
1. Meta Ads MCP server setup and authentication
2. Client Meta Ads account access
3. API permissions configured

**Skip for now** - Focus on Google Ads where infrastructure exists and client base is strongest.

**Future Prompts to Implement:**
- Weekly Meta performance dashboard
- Creative fatigue detection
- Audience profitability analysis
- Cross-channel Meta + Google unified reporting

---

## Phase 7: Shopify Integration (Future)

**Prerequisites:**
1. Shopify MCP server or API integration
2. Client Shopify store access
3. Product catalog data structure

**Applies to Clients:**
- Godshot (WooCommerce, not Shopify - would need WooCommerce MCP)
- Crowd Control (WooCommerce)
- Potentially future e-commerce clients

**Future Prompts to Implement:**
- 90-day business health audit
- Customer lifetime value analysis
- Product performance scorecards
- Unified Shopify + Google Ads + Meta reporting

---

## Implementation Roadmap

### Timeline Summary

| Phase | Focus | Duration | Key Deliverables | Priority |
|-------|-------|----------|------------------|----------|
| **Phase 1** | Quick Wins | Week 1-2 | 3 skills (Google Ads + GA4 reports) | P0 |
| **Phase 2** | Client Reports | Week 3-4 | Automated monthly dashboards | P0 |
| **Phase 3** | Optimization | Week 5-6 | Budget + keyword opportunity detection | P1 |
| **Phase 4** | Cross-Channel | Week 7-8 | Blended metrics + Analyst Pack | P1 |
| **Phase 5** | Advanced | Week 9-12 | Seasonal patterns + growth modeling | P2 |
| **Phase 6** | Meta Ads | Week 13-16 | Meta reporting and optimization | P2 |
| **Phase 7** | Shopify | Future | E-commerce deep integration | P3 |

---

## Success Metrics

### Phase 1 Success (Week 2)
- ✅ Generate weekly report for 3 test clients
- ✅ Reports take <5 minutes to generate
- ✅ Identify at least 1 actionable insight per client
- ✅ Client feedback: "This is useful"

### Phase 2 Success (Week 4)
- ✅ Automated monthly reports for top 5 clients
- ✅ Save 2+ hours per client per month (10 hours/month total)
- ✅ Client feedback: "This is clearer than Google Ads UI"

### Phase 3 Success (Week 6)
- ✅ System proactively identifies 3+ optimization opportunities
- ✅ At least 1 opportunity results in budget increase approval
- ✅ Measurable revenue increase from optimization

### Overall Success (Week 12)
- ✅ 50% reduction in manual reporting time
- ✅ Proactive optimization detection in production
- ✅ Client satisfaction improvement (survey)
- ✅ At least 2 budget increases approved based on system recommendations

---

## Resource Requirements

### Time Investment
- **Phase 1**: 15 hours (quick wins)
- **Phase 2**: 20 hours (automation)
- **Phase 3**: 22 hours (optimization)
- **Phase 4**: 18 hours (cross-channel)
- **Phase 5**: 28 hours (advanced)
- **Total Phases 1-5**: ~103 hours (~2.5 weeks full-time, ~10 weeks part-time)

### Infrastructure
- ✅ Google Ads MCP (already operational)
- ✅ Google Analytics MCP (already operational)
- ✅ Task management system (already operational)
- ⏳ Meta Ads MCP (future - Phase 6)
- ⏳ Shopify/WooCommerce MCP (future - Phase 7)

### Documentation
- Create prompt templates in `roksys/prompt-library/`
- Update CLAUDE.md with new skills
- Create client-facing example reports
- Document GAQL query patterns

---

## Risk Mitigation

### Risk 1: Data Quality Issues
**Mitigation:**
- Start with 3 test clients (Smythson, Superspace, Godshot)
- Validate output against manual reports
- Include error handling for missing data

### Risk 2: Client Confusion
**Mitigation:**
- Use "visual storytelling" approach (GoMarble)
- Include "The Story" summary boxes
- Avoid technical jargon
- Test reports with 1-2 clients before full rollout

### Risk 3: Over-Automation
**Mitigation:**
- All optimization recommendations create tasks (not auto-apply)
- Manual review required for budget/bid changes
- Log all changes to experiment tracker
- Maintain human oversight

### Risk 4: Time Overruns
**Mitigation:**
- Focus on Phase 1 quick wins first (prove value)
- Deprioritize Phase 5-7 if needed
- Use existing MCP capabilities (don't build new integrations)
- Iterate based on client feedback

---

## Next Steps

### Immediate (This Week)
1. **Review this plan** - Validate phases and priorities
2. **Select Phase 1A start date** - Block 4 hours for Google Ads Weekly Report skill
3. **Choose 3 test clients** - Recommend: Godshot (simple), Superspace (medium), Smythson (complex)

### Week 1 Actions
1. Create `.claude/skills/google-ads-weekly-report/` skill
2. Test with Godshot (simplest account)
3. Refine prompt based on output quality
4. Test with Superspace and Smythson
5. Document learnings

### Week 2 Actions
1. Create `.claude/skills/google-ads-auction-insights/` skill
2. Create `.claude/skills/ga4-channel-performance/` skill
3. Review Phase 1 results
4. Decide: Proceed to Phase 2 or iterate Phase 1?

---

## Questions to Consider

Before starting implementation:

1. **Client Selection:**
   - Which 3 clients for Phase 1 testing?
   - Which 5 clients for Phase 2 automated reporting?

2. **Reporting Frequency:**
   - Weekly reports: Email or dashboard?
   - Monthly reports: Auto-send or manual review first?

3. **Automation Boundaries:**
   - Should budget opportunity detector auto-create tasks or just email you?
   - Should keyword waste detector require approval before pausing?

4. **Brand Alignment:**
   - Use GoMarble's "visual storytelling" approach or adapt to ROK style?
   - Keep ROK branding (green, logo) or create separate "analytics dashboard" brand?

5. **Scope Prioritization:**
   - Complete Phases 1-2 before Phase 3, or run in parallel?
   - Skip Meta/Shopify integration entirely and focus on Google ecosystem?

---

## Appendix: GoMarble Prompts Priority Matrix

| Prompt | Value | Effort | ROI | Phase |
|--------|-------|--------|-----|-------|
| Google Ads Weekly E-commerce | High | Low | ⭐⭐⭐⭐⭐ | 1 |
| GA4 Traffic Sources | High | Low | ⭐⭐⭐⭐⭐ | 1 |
| Auction Insights Analysis | High | Medium | ⭐⭐⭐⭐ | 1 |
| Monthly Client Dashboard | High | High | ⭐⭐⭐⭐ | 2 |
| Budget Opportunity Detector | Medium | Medium | ⭐⭐⭐⭐ | 3 |
| Keyword Waste Detector | Medium | Medium | ⭐⭐⭐ | 3 |
| Blended Metrics Calculator | Medium | Low | ⭐⭐⭐ | 4 |
| Analyst Pack | Medium | Medium | ⭐⭐⭐ | 4 |
| Seasonal Pattern Analyzer | Low | High | ⭐⭐ | 5 |
| Growth Opportunity Modeler | Low | High | ⭐⭐ | 5 |
| Meta Creative Fatigue | Low | High | ⭐ | 6 |
| Shopify Business Audit | Low | Very High | ⭐ | 7 |

**Recommendation:** Focus on Phases 1-4 (highest ROI, uses existing infrastructure).

---

**Status:** Ready for review and Phase 1 initiation
**Next Review Date:** After Phase 1 completion (Week 2)
