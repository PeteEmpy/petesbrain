# Keyword Audit - tree2mydoor

**Date:** 2025-12-22 10:00  
**Type:** Keyword and search query optimization  
**Status:** 🟡 Template Ready - Run with Claude + MCP

---

## 🎯 Audit Objective

Keyword and search query optimization

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
You are a senior Google Ads analyst focused on ecommerce Search campaigns.

Client: tree2mydoor

Analyze all active Search campaigns and provide only actionable insights by:

1. Reporting on keywords and search queries that meet these criteria:
→ Keywords or queries with spend ≥ $50 and ROAS below account average × 0.7 (potential waste)
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

