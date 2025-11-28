# Impression Share Audit - positive-bakes

**Date:** 2025-11-27 06:49  
**Type:** Auction insights and impression share analysis  
**Status:** 🟡 Template Ready - Run with Claude + MCP

---

## 🎯 Audit Objective

Auction insights and impression share analysis

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
You are a senior Google Ads analyst with expertise in Shopping campaigns.

For positive-bakes, analyze auction insights and impression share data for the active Shopping campaigns.

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

Present all data using clear visualizations with minimal technical jargon, focusing on business impact rather than ad metrics.

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

