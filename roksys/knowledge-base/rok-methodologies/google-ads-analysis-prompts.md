---
title: Google Ads Analysis Prompts - ROK Systematic Analysis Framework
source: GoMarble Prompt Library (https://prompting.gomarble.ai/)
date_added: 2025-10-30
tags: [google-ads, analysis, prompts, ecommerce, shopping, search, methodology, claude, mcp]
category: ROK Methodologies
---

## Summary

This is ROK's systematic framework for analyzing Google Ads accounts using Claude Code with MCP integration. These prompts provide structured, repeatable analysis across different campaign types and optimization objectives.

**Key Analysis Areas Covered:**
- E-commerce weekly performance analysis (campaigns, products, placements)
- Auction insights and impression share optimization
- Keyword and search query optimization
- Account segmentation and restructuring
- Competitive analysis and budget recovery

**Usage:** These prompts can be used directly with Claude Code when connected to Google Ads via MCP, or adapted for manual analysis workflows.

---

## Prompt 1: Google Ads – E-commerce Weekly Analysis (Campaigns, Products, Placements & Optimization Insights)

**Use Case:** Comprehensive weekly performance review for e-commerce accounts
**Best For:** Performance Max, Shopping, and multi-channel campaigns
**Output:** Executive summary with product-level insights and prioritized recommendations

### Prompt

```
You are a senior Google Ads analyst specializing in e-commerce Google Ads.

Account: [ACCOUNT_ID]
Date Range: [Last 7 days]

Please perform the following analyses:

1. Campaign Overview
Summarize total impressions, clicks, spend, conversions, conversion value, ROAS, CTR, CVR, and CPA.

2. Product-Level Performance
Break down performance metrics (impressions, clicks, spend, conversions, ROAS) by product or product group.

Identify the top 10 best-performing and bottom 10 worst-performing products by ROAS and conversion volume.

Flag products with week-over-week changes in ROAS or conversions exceeding ±15%.

3. Placement Analysis
Analyze spend and conversion performance across key placements (Shopping, YouTube, Display, Discover, Gmail).

Highlight which placements drive the highest ROAS and which are underperforming.

4. Audience & Asset Insights
Review the audience segments contributing most to conversions and revenue.

Identify any underperforming asset groups or creatives causing wasted spend or low CTR.

5. Spend & Budget Efficiency
Check for pacing issues, budget caps, or inefficient spend allocation within campaigns.

6. Root Cause Diagnostics
For flagged products or placements, diagnose potential issues such as feed data quality, auction competition, or creative fatigue.

7. Recommendations
Prioritize 3–5 actionable recommendations for bidding, budget allocation, feed improvements, or creative refreshes.

8. Output Format
Provide a structured Markdown report with:
→ An executive summary highlighting key metrics and notable changes.
→ Tables for product-level and placement performance (limit to 20 rows).
→ Bullet-pointed insights and prioritized next steps.

Use human-friendly metrics (e.g., dollars, percentages) and clear headings.
```

### Key Insights

- **Holistic View:** Covers campaigns, products, placements, audiences, and creative performance
- **Root Cause Analysis:** Goes beyond metrics to diagnose feed quality, auction dynamics, creative fatigue
- **Actionable Output:** Prioritizes 3-5 specific recommendations rather than overwhelming with data
- **Product Focus:** E-commerce specific with product-level ROAS and conversion tracking

---

## Prompt 2: Maximize Shopping Campaign Performance via Auction Insights

**Use Case:** Identify impression share loss opportunities and competitive pressures
**Best For:** Shopping campaigns with budget constraints or rank issues
**Output:** Auction insights report with impression share recovery recommendations

### Prompt

```
You are a senior Google Ads analyst with expertise in Shopping campaigns.

For the Account: [ACCOUNT_ID], analyze auction insights and impression share data for the active Shopping campaigns over the period {{date_range}}.

Please perform the following:

1. For each campaign, ad group, and product group, report:
→ Impression Share (IS)
→ Lost Impression Share due to Budget (IS Lost Budget %)
→ Lost Impression Share due to Rank (IS Lost Rank %)
→ Average Position or Top of Page Rate, if available

2. Identify where impression share loss is most significant (>10%) and determine whether it is primarily due to budget constraints or rank issues.

3. Detect any notable week-over-week changes in impression share metrics that may indicate competitive pressure or new entrants in auctions.

4. Provide insights on which campaigns or product groups have the highest opportunity for growth if the budget is increased or bids are improved.

5. Recommend prioritized actions, such as:
→ Increasing budgets to recover lost impression share due to budget caps
→ Raising bids or improving quality signals for segments losing impression share due to rank
→ Restructuring campaigns or product groups to better compete in auctions

Output: A clear, concise Markdown report including:
→ Tables summarizing key impression share metrics at the campaign, ad group, and product group levels
→ A bullet-point summary of major findings and root causes
→ A prioritized action plan based on potential revenue impact

Present all data using clear visualizations with minimal technical jargon, focusing on business impact rather than ad metrics. Format as a visual dashboard with clear section dividers.
```

### Key Insights

- **Impression Share Focus:** Identifies exactly where you're losing visibility (budget vs. rank)
- **Growth Opportunities:** Quantifies potential revenue impact of budget/bid increases
- **Competitive Intelligence:** Detects WoW changes indicating new competitive pressure
- **Segmented View:** Analysis at campaign, ad group, and product group levels
- **Business Language:** Focuses on revenue impact rather than technical metrics

---

## Prompt 3: Optimize Underperforming and High-Potential Keywords

**Use Case:** Search campaign optimization focused on actionable keyword insights
**Best For:** Search campaigns with wasted spend or untapped growth opportunities
**Output:** Actionable-only keyword report with specific bid/optimization recommendations

### Prompt

```
You are a senior Google Ads analyst focused on ecommerce Search campaigns.

Account: [ACCOUNT_ID]
Date Range: [SPECIFY_DATE_RANGE]

Analyze all active Search campaigns and provide only actionable insights by:

1. Reporting on keywords and search queries that meet these criteria:
→ Keywords or queries with spend ≥ $X and ROAS below account average × 0.7 (potential waste)
→ Keywords or queries with ≥ 2 conversions and ROAS ≥ account average × 1.3 (growth opportunities)
→ Keywords or queries with week-over-week CTR or CVR declines > 15% (need ad or landing page optimization)
→ Queries generating spend with zero conversions (negative keyword candidates)

2. For all items above, recommend specific optimizations, such as:
→ Bid increases or decreases
→ Adding new exact or phrase match keywords
→ Adding negative keywords
→ Ad copy or landing page improvements

3. Skip any keywords or queries that show stable or good performance and require no action.

4. Provide a concise Markdown report including:
→ Summary tables limited to actionable items only
→ Bullet-pointed, prioritized recommendations
→ Clear section headers and human-readable metrics

Focus solely on what can be improved or optimized.
```

### Key Insights

- **Actionable-Only Filtering:** Skips stable keywords, shows only what needs attention
- **Smart Thresholds:** Uses account average × multipliers (0.7, 1.3) for relative benchmarking
- **Four Opportunity Types:** Waste, growth, decline, zero-conversion spend
- **Specific Recommendations:** Not just "optimize" but exact actions (bid changes, negatives, ad copy)
- **Efficiency Focus:** Saves time by filtering out noise

---

## Prompt 4: Google Ads Account Segmentation Analysis & Restructuring Plan

**Use Case:** Evaluate campaign structure and identify restructuring opportunities
**Best For:** Accounts with overly broad product groups or unclear segmentation
**Output:** Segmentation assessment with restructuring recommendations

### Prompt

```
You are a senior Google Ads expert. Help me analyze the account.

Account: [ACCOUNT_ID]
Date Range: [SPECIFY_DATE_RANGE]

Please follow these steps:

1. Identify overly broad product groups that may be masking performance details.

2. Evaluate the granularity and logic of the current segmentation.

3. Suggest restructuring approaches to improve bid control and reporting clarity.

Return a Markdown report with segmentation insights and actionable restructuring advice.
```

### Key Insights

- **Structural Analysis:** Looks at campaign architecture, not just performance
- **Bid Control Focus:** Identifies where broad groups prevent proper bid optimization
- **Reporting Clarity:** Finds segments that hide important performance variations
- **Restructuring Guidance:** Provides specific approaches to improve segmentation
- **Short and Focused:** Simple prompt that can uncover major structural issues

---

## Prompt 5: Google Ads Auction Insights Analysis & Recommendations

**Use Case:** Deep dive into auction dynamics and competitive positioning
**Best For:** Search campaigns with impression share concerns
**Output:** Auction insights report with budget/bid recovery recommendations

### Prompt

```
Act as a Google Ads expert and help me analyze Account: [ACCOUNT_ID]

Review the auction insights for Search campaigns for Date Range: [SPECIFY_DATE_RANGE]

Please follow these steps:

1. Report impression share, lost impression share due to budget, and lost impression share due to rank at both campaign and ad group levels.

2. Detect significant changes indicating competitive pressures.

3. Recommend budget or bid changes to recover impression share.

Deliver a Markdown report with data tables, insights, and prioritized recommendations.
```

### Key Insights

- **Search Campaign Focus:** Similar to Prompt 2 but specifically for Search campaigns
- **Two-Level Analysis:** Campaign and ad group level impression share metrics
- **Competitive Pressure Detection:** Identifies changes in auction dynamics
- **Recovery Recommendations:** Specific budget/bid actions to regain visibility
- **Simpler than Prompt 2:** More focused, less detail on product groups

---

## Usage Guidelines

### When to Use Each Prompt

| Prompt | Best Used For | Frequency | Client Stage |
|--------|--------------|-----------|--------------|
| **Prompt 1: E-commerce Weekly Analysis** | Ongoing performance monitoring | Weekly | Established accounts |
| **Prompt 2: Shopping Auction Insights** | Impression share optimization | Monthly or when IS drops | Growth phase |
| **Prompt 3: Keyword Optimization** | Search campaign cleanup | Bi-weekly | Active optimization |
| **Prompt 4: Account Segmentation** | Structural improvements | Quarterly or at onboarding | New accounts or restructures |
| **Prompt 5: Search Auction Insights** | Competitive analysis | Monthly or when IS drops | All stages |

### Integration with Claude Code MCP

These prompts are designed to work with Claude Code's Google Ads MCP integration:

1. **Setup:** Ensure Google Ads MCP server is configured (see `shared/mcp-servers/google-ads-mcp-server/`)
2. **Usage:** Replace `[ACCOUNT_ID]` with actual customer ID
3. **Data Fetching:** Claude Code will use `mcp__google-ads__run_gaql` to fetch data
4. **Analysis:** Claude applies the prompt framework to generate structured insights
5. **Output:** Markdown reports saved to client folders for documentation

### Customization Tips

- **Adjust Thresholds:** Modify percentages (±15%, 0.7×, 1.3×) based on client volatility
- **Add Client Context:** Reference client CONTEXT.md for business-specific insights
- **Combine Prompts:** Use Prompt 1 weekly, then dive deeper with Prompts 2-3 as needed
- **Export Results:** Save outputs to `clients/[client-name]/documents/` for history

---

## ROK Analysis Workflow

**Step 1: Weekly Overview (Prompt 1)**
Run comprehensive e-commerce analysis to identify major changes and opportunities

**Step 2: Deep Dive Based on Findings**
- If impression share is down → Use Prompt 2 or 5
- If keyword performance is inconsistent → Use Prompt 3
- If segmentation seems unclear → Use Prompt 4

**Step 3: Document Findings**
- Save reports to client folder
- Update CONTEXT.md with key learnings
- Add experiments to ROK Experiments sheet if testing changes

**Step 4: Implement Recommendations**
- Prioritize by potential revenue impact
- Track changes in Google Tasks
- Monitor results in next weekly analysis

---

## Advanced Techniques

### Combining with Root Cause Analysis

When performance changes, use these prompts AFTER checking:
1. **CONTEXT.md** - Client business changes, stock issues, seasonality
2. **Completed Tasks** - Recent account management actions
3. **Knowledge Base** - Recent platform updates or industry changes
4. **Google Analytics** - Website-level conversion rate changes
5. **Client Website** - Product availability, pricing, promotions

Then run the appropriate prompt to separate controllable (your actions) from uncontrollable (external) factors.

### Prompt Chaining for Comprehensive Analysis

```
Step 1: Run Prompt 1 (Weekly Analysis)
↓
Step 2: Identify specific issue (e.g., Shopping ROAS decline)
↓
Step 3: Run Prompt 2 (Shopping Auction Insights)
↓
Step 4: Diagnose root cause (e.g., lost IS due to budget)
↓
Step 5: Implement recommendation (budget increase)
↓
Step 6: Track in Google Tasks and CONTEXT.md
```

### Creating Custom Variations

These prompts can be adapted for:
- **Display campaigns** - Modify Prompt 1 for placement/audience focus
- **Video campaigns** - Adapt for YouTube-specific metrics (VTR, CPV)
- **Lead gen** - Replace ROAS with CPL and lead quality metrics
- **Brand campaigns** - Focus on impression share, SOV, and awareness metrics

---

## Related Resources

- **ROK Experiments Sheet:** Track tests mentioned in these analyses
- **Client CONTEXT.md:** Always cross-reference with client-specific context
- **Knowledge Base - Platform Updates:** Check for recent Google changes affecting metrics
- **MCP Documentation:** `shared/mcp-servers/google-ads-mcp-server/` for technical setup

---

## Document History

| Date | Change |
|------|--------|
| 2025-10-30 | Initial import from GoMarble Prompt Library |
