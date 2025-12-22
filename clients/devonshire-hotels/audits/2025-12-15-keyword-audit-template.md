# Keyword Audit - devonshire-hotels

**Date:** 2025-12-15 10:00  
**Type:** Keyword and search query optimization  
**Status:** 🟡 Template Ready - Run with Claude + MCP

---

## 🎯 Audit Objective

Keyword and search query optimization

### Framework Integration

**Framework Location**: `docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv`
**Framework Guide**: `docs/AUDIT-FRAMEWORK-GUIDE.md`
**Detailed Skill**: `.claude/skills/google-ads-keyword-audit/skill.md`

**This audit covers**:
- **Section 5.6** - Keyword & Query Performance (match types, ROAS, impression share)
- **Section 5.7** - Search Terms Review (search term report, negative keywords, intent analysis)

**Framework frequency**: Weekly (search term review), Monthly (comprehensive keyword optimization)

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
You are a senior Google Ads analyst using the Google Ads Performance Framework.

**Client**: devonshire-hotels
**Framework Reference**: Sections 5.6 (Keyword & Query) + 5.7 (Search Terms)
**Framework Guide**: docs/AUDIT-FRAMEWORK-GUIDE.md

Analyze all active Search campaigns and provide only actionable insights by:

1. **Reporting on keywords and search queries** that meet these criteria:
→ Keywords or queries with spend ≥ $50 and ROAS below account average × 0.7 (potential waste)
   - Framework Check (5.6): Keyword-level ROAS analysis
→ Keywords or queries with ≥ 2 conversions and ROAS ≥ account average × 1.3 (growth opportunities)
   - Framework Check (5.6): Keyword bidding strategy & impression share
→ Keywords or queries with week-over-week CTR or CVR declines > 15% (need optimization)
   - Framework Check (5.6): Query-level performance trends
→ Queries generating spend with zero conversions (negative keyword candidates)
   - Framework Check (5.7): Irrelevant search term identification

2. **For all items above**, recommend specific optimizations:
→ Bid increases or decreases (Framework 5.6: Keyword bidding strategy)
→ Adding new exact or phrase match keywords (Framework 5.7: Search term to keyword matching)
→ Adding negative keywords (Framework 5.7: Negative keyword list management)
→ Ad copy or landing page improvements (Framework 5.6: Ad relevance optimization)

3. **Skip any keywords or queries** that show stable or good performance and require no action.

4. **Provide a concise Markdown report** including:
→ Summary tables limited to actionable items only
→ Bullet-pointed, prioritized recommendations (P0/P1/P2)
→ Framework alignment summary (which framework items passed/failed)
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

