# Weekly Audit - smythson

**Date:** 2025-11-05 11:05  
**Type:** Comprehensive weekly performance review  
**Status:** 🟡 Template Ready - Run with Claude + MCP

---

## 🎯 Audit Objective

Comprehensive weekly performance review

---

## 📋 Execution Instructions

### Option 1: Claude Code + MCP (Recommended)

1. Open Claude Code (Cursor)
2. Ensure Google Ads MCP server is connected
3. Copy the prompt below
4. Paste into Claude Code
5. Claude will fetch data and generate the report
6. Save output to this file

### Option 2: Manual Analysis

1. Export data from Google Ads UI
2. Use the prompt as a framework
3. Manually analyze and document findings

---

## 🤖 Audit Prompt

```
You are a senior Google Ads analyst specializing in e-commerce Google Ads.

Client: smythson
Date Range: Last 7 days

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

---

## 📊 Audit Results

<!-- Claude will populate this section when run -->

*Run the audit prompt above to generate results here*

---

## 📝 Action Items

- [ ] Review audit findings
- [ ] Prioritize recommendations by impact
- [ ] Create Google Tasks for each action
- [ ] Update client CONTEXT.md with key learnings
- [ ] Schedule follow-up audit

---

## 🔗 Related Files

- [Client Context](../CONTEXT.md)
- [ROK Analysis Prompts](../../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md)
- [Previous Audits](./)

