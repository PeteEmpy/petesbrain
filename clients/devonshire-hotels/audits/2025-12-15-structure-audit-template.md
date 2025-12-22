# Structure Audit - devonshire-hotels

**Date:** 2025-12-15 10:00  
**Type:** Account segmentation and restructuring analysis  
**Status:** 🟡 Template Ready - Run with Claude + MCP

---

## 🎯 Audit Objective

Account segmentation and restructuring analysis

### Framework Integration

**Framework Location**: `docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv`
**Framework Guide**: `docs/AUDIT-FRAMEWORK-GUIDE.md`

**This audit covers**:
- **Section 3.1** - Account Strategy & Structure
- **Section 3.3** - Campaign Organisation
- **Section 4.1** - Campaign Settings Review
- **Section 5.2** - Budget Allocation & Account Structure

**Framework frequency**: Quarterly (comprehensive structural review)

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
You are a senior Google Ads expert analyzing devonshire-hotels using the Google Ads Performance Framework.

**Framework Reference**: Sections 3.1, 3.3, 4.1, 5.2 (Account Structure)
**Framework Guide**: docs/AUDIT-FRAMEWORK-GUIDE.md

Please follow these steps:

1. **Identify overly broad product groups** that may be masking performance details.
   - Framework Check (3.3): Campaign organisation by product/service line
   - Framework Check (5.2): Budget allocation logic

2. **Evaluate the granularity and logic** of the current segmentation.
   - Framework Check (3.1): Account structure appropriate for business model
   - Framework Check (4.1): Campaign settings optimize for segmentation

3. **Suggest restructuring approaches** to improve bid control and reporting clarity.
   - Framework Check (5.2): Structural improvements for budget optimization
   - Framework Check (3.3): Campaign naming conventions and organisation

Return a Markdown report with:
- Segmentation insights with framework references
- Actionable restructuring advice
- Framework alignment summary (which items passed/failed)
- Prioritized recommendations (P0/P1/P2)

```

---

## 📊 Audit Results

<!-- Claude will populate this section when run -->

*Run the audit prompt above to generate results here*

---

## 📝 Action Items

- [ ] Review audit findings
- [ ] Check framework alignment summary (which sections passed/failed)
- [ ] Prioritize recommendations by impact (P0/P1/P2)
- [ ] Create Google Tasks for each action
- [ ] Update client CONTEXT.md with key learnings
- [ ] Document framework items that failed for next comprehensive audit
- [ ] Schedule follow-up structural audit (quarterly)

---

## 🔗 Related Files

- [Client Context](../CONTEXT.md)
- **[Framework Guide](../../../docs/AUDIT-FRAMEWORK-GUIDE.md)** ← Framework usage instructions
- **[Framework Checklist](../../../docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv)** ← Complete 457-item framework
- [ROK Analysis Prompts](../../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md)
- [Previous Audits](./)

