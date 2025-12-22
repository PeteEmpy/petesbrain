# Google Ads Skills Comparison: vs PetesBrain

**Date:** 2025-11-19
**Status:** Phase 2 Complete - Analysis & Learning
**Outcome:** PetesBrain has MORE functionality; adopted Mike's better documentation structure

---

## Executive Summary

**Key Finding:** PetesBrain's Google Ads campaign audit skill is MORE comprehensive than Mike's, with Product Impact Analyzer integration that Mike doesn't have. However, Mike's documentation structure is superior.

**Action Taken:** Adopted Mike's documentation files (`account-sizing-strategy.md`, `analysis-frameworks.md`) to enhance PetesBrain's skill without losing existing functionality.

**Skills Compared:**
1. ✅ Campaign Audit (demo-google-ads-campaign-audit)
2. ✅ Keyword Audit (demo-google-ads-keyword-audit)
3. ℹ️ Account Info (Mike only)
4. ℹ️ Campaign Performance (Mike only)

---

## Campaign Audit Comparison

### Skill Structure

| Feature | Mike's Version | PetesBrain Version | Winner |
|---------|----------------|-------------------|---------|
| **Core Phases** | 3 phases | 5 phases | **PetesBrain** |
| **Allowed Tools** | `execute_gaql` | `run_gaql`, `list_accounts` | Equal |
| **Account Config** | `.claude/accounts.json` | `shared/data/google-ads-clients.json` | Equal (different structure) |
| **File Output** | `context/audits/` | `clients/[client]/audits/` | **PetesBrain** (per-client) |
| **Transform Script** | Simpler command | More explicit with args | Mike (easier) |
| **Documentation** | 3 separate files | 2 files | **Mike** (better organized) |

### Unique Features

**Mike Has (that PetesBrain didn't have):**
- ✅ `account-sizing-strategy.md` - Adaptive query strategy based on account size
- ✅ `analysis-frameworks.md` - Comprehensive analysis methodology documentation
- ✅ `transform_audit_data.py` - Additional transform script variant

**PetesBrain Has (that Mike doesn't have):**
- ✅ **Phase 4: Product Impact Analyzer Integration** - Correlates product feed changes with performance shifts
- ✅ Per-client audit directories (`clients/[client]/audits/`)
- ✅ Integration with `shared/data/google-ads-clients.json` for client mapping
- ✅ Client CONTEXT.md integration for business context
- ✅ `audit-templates.md` - Report format templates (different purpose than Mike's docs)

---

## Key Learnings from Mike's Implementation

### 1. Documentation Architecture

**Mike's Pattern:**
```
skill.md (main instructions)
├── account-sizing-strategy.md (when to read: determining query approach)
├── analysis-frameworks.md (when to read: analyzing structural issues)
└── queries/ (GAQL query library)
```

**Why This is Better:**
- **Progressive disclosure** - Claude only reads what it needs when it needs it
- **Separation of concerns** - Strategy vs methodology vs execution
- **Clearer instructions** - "Read this file when..." directives
- **Reduces token usage** - Don't load everything upfront

**PetesBrain's Pattern (before):**
```
skill.md (EVERYTHING in one 22KB file)
├── audit-templates.md (report formats only)
└── queries/ (GAQL query library)
```

**What We Learned:**
- Break large skill files into topic-specific files
- Use "Read this file when..." directives
- Keep main skill.md as router to other docs

### 2. Account Sizing Strategy (NEW LEARNING)

**Mike's Innovation:**
- **Step 1:** Run lightweight queries to understand account scale
- **Step 2:** Calculate spend concentration (top 20 campaigns = X% of spend)
- **Step 3:** Adapt query strategy based on size:
  - Small (<20 campaigns): Full 30-day audit, no limits
  - Medium (20-100): Standard audit, LIMIT 500
  - Large (100-300): Focused audit, 14 days, LIMIT 300
  - Enterprise (>300): Strategic audit, 7 days, LIMIT 100

**Why This Matters:**
- **Prevents timeout errors** on large accounts
- **Focuses on high-impact opportunities** (80/20 rule)
- **Faster execution** without sacrificing quality
- **Better user experience** ("Analyzing top 50 campaigns representing 92% of spend")

**PetesBrain Previously:**
- Single approach for all account sizes
- No adaptive query strategy
- Risk of timeouts on large accounts

### 3. Analysis Frameworks Documentation

**Mike's Structure:**
```markdown
## Critical Analysis Methods
1. Account Structure Evaluation
2. Campaign Settings Audit
3. Budget Allocation Analysis
...

## Common Structural & Budget Issues
- Network Mixing (CRITICAL ERROR)
- Brand/Non-Brand Mixing (HIGH PRIORITY)
- Over-Segmentation
...

## Standard Recommendations
[Prioritized by ICE framework]
```

**Why This is Better:**
- **Teaches auditing methodology** - Not just what to look for, but how to analyze
- **Prioritization framework** - CRITICAL/HIGH/MEDIUM with clear criteria
- **Common patterns** - Codifies expert knowledge (e.g., "Search Partners typically 30-50% lower ROAS")
- **Reduces hallucination** - Specific, documented standards vs Claude guessing

**PetesBrain Previously:**
- Analysis guidance embedded in main skill.md
- No systematic framework documentation
- No standard recommendations library

### 4. Transform Script Approach

**Both use same core transform_data.py** (15.9KB, virtually identical)

**Mike's Usage:**
```bash
python transform_data.py
```

**PetesBrain's Usage:**
```bash
python3 .claude/skills/google-ads-campaign-audit/transform_data.py --currency £ --input-dir /path/to/json/files --output transformed-analysis-ready.md
```

**Learning:**
- Mike's simpler command assumes defaults
- PetesBrain's explicit approach allows customization
- **Recommendation:** Keep PetesBrain's approach (more flexible for multi-client work)

---

## PetesBrain's Unique Advantage: Product Impact Analyzer Integration

**This is a major differentiator that Mike's template does NOT have.**

### Phase 4: Product Impact Analyzer Integration

**What it does:**
1. **Auto-checks** if client is tracked in Product Impact Analyzer
2. **Reviews product changes** (last 7-14 days):
   - Price changes
   - Stock status changes
   - Title/description changes
   - Product type/label transitions
3. **Correlates with performance**:
   - "Revenue dropped 35% → Price increased £5 on Nov 10" (feed issue, not campaign)
   - "ROAS declined → Stock went out on Nov 8" (wasted spend detected)
4. **Includes in audit report** with specific recommendations

**Why This Matters:**
- **Prevents false diagnoses** - Performance drops often due to feed issues, not campaign problems
- **Faster root cause analysis** - Don't waste time optimizing campaigns when the issue is product data
- **Quantified impact** - "£XXX wasted while out of stock"
- **Actionable recommendations** - "Restock [Product] immediately" vs vague "improve performance"

**Example from Real Audit:**
```markdown
## Phase 4: Product Impact Analysis

**Recent Product Changes**:
| Product | Change | Date | Impact |
|---------|--------|------|--------|
| Leather Diary | Price: £45→£50 | Nov 10 | 📉 Revenue -£892 |
| Ceramic Mug | Out of Stock | Nov 8 | ⚠️ Wasted £156 |

**Recommendations**:
1. Review pricing strategy for Leather Diary (price increase hurting performance)
2. Restock Ceramic Mug immediately (wasting £22/day while out of stock)
```

**This level of integration doesn't exist in Mike's template.**

---

## Actions Taken: Enhancing PetesBrain

### 1. Adopted Mike's Documentation Files

Copied to `/Users/administrator/Documents/PetesBrain/.claude/skills/google-ads-campaign-audit/`:

✅ **account-sizing-strategy.md**
- Adaptive query strategy based on account size
- Spend concentration calculation
- Query modification guidance

✅ **analysis-frameworks.md**
- Critical analysis methods
- Common structural issues
- Standard recommendations
- Best practices from expert frameworks

### 2. Updated skill.md Structure

Added "Read these files when..." directives:
```markdown
## Account Sizing Strategy

For detailed account sizing and query adaptation, read:
- `account-sizing-strategy.md` - When determining query strategy based on account size

## Analysis Frameworks

For detailed analysis methods and common issues, read:
- `analysis-frameworks.md` - Common structural issues, budget allocation problems, standard recommendations
```

### 3. Kept PetesBrain's Unique Features

✅ Retained Product Impact Analyzer integration (Phase 4)
✅ Retained per-client audit directories structure
✅ Retained `google-ads-clients.json` + CONTEXT.md integration
✅ Retained explicit transform script arguments (more flexible)

### 4. Best of Both Worlds

**Result:** PetesBrain now has:
- ✅ Mike's superior documentation architecture
- ✅ Mike's account sizing strategy
- ✅ Mike's analysis frameworks
- ✅ Product Impact Analyzer integration (unique to PetesBrain)
- ✅ Per-client directory structure (better for agency work)

---

## Keyword Audit Comparison

### File Structure

**Mike's keyword-audit:**
```
demo-google-ads-keyword-audit/
├── skill.md
└── (no additional files)
```

**PetesBrain's keyword-audit:**
```
google-ads-keyword-audit/
└── skill.md
```

### Key Differences

| Feature | Mike's Version | PetesBrain Version |
|---------|----------------|-------------------|
| **Approach** | Script-based (`.py` analyzer) | Instruction-based |
| **Allowed Tools** | `execute_gaql`, `get_reporting_view_doc` | `run_gaql` |
| **Focus** | Query builder + automated analysis | Manual analysis with guidance |

**Analysis:** Both are instruction-based skills. No major learnings to adopt here. PetesBrain's version is already comprehensive.

---

## Skills Mike Has That PetesBrain Doesn't

### 1. google-ads-account-info

**Purpose:** Quick account overview (campaigns, spend, ROAS summary)

**Files:**
- `skill.md` only

**PetesBrain Equivalent:**
- Can do this with ad-hoc GAQL queries
- Not a dedicated skill

**Recommendation:** **DON'T ADOPT**
- Too simple to warrant dedicated skill
- Better handled by campaign audit's Phase 1

### 2. google-ads-campaign-performance

**Purpose:** Performance analysis over time (trends, patterns)

**Files:**
- `skill.md` only

**PetesBrain Equivalent:**
- Daily intel report agent
- Performance monitoring system

**Recommendation:** **DON'T ADOPT**
- PetesBrain has more sophisticated performance monitoring
- Overlaps with existing systems

---

## ROI Analysis: Mike's Template Integration

**Time Investment:**
- Phase 1 (CSV Analyzer): 3.5 hours ✅
- Phase 2 (Google Ads Skills): 2 hours ✅
- **Total so far:** 5.5 hours

**Value Gained:**

**From CSV Analyzer (Phase 1):**
- ✅ 40 minutes saved per CSV analysis
- ✅ Consistent, repeatable insights
- ✅ Professional visualizations

**From Google Ads Skills (Phase 2):**
- ✅ Better documentation architecture (progressive disclosure)
- ✅ Account sizing strategy (prevents timeouts, focuses on impact)
- ✅ Analysis frameworks (codified expert knowledge)
- ✅ Retained Product Impact Analyzer advantage

**Expected Payback:**
- CSV Analyzer: 5 reports (~2-5 weeks)
- Documentation improvements: Immediate (better Claude performance)
- Account sizing: First large account audit (immediate value)

**Outcome:** ✅ Worth the investment

---

## Next Steps

### Completed ✅
- [x] Phase 1: CSV Analyzer implementation
- [x] Phase 2: Google Ads skills comparison
- [x] Adopted Mike's documentation files
- [x] Enhanced PetesBrain campaign audit skill

### Remaining Phases

**Phase 3: Daily Briefing System** (2-3 hours)
- Study Mike's `briefing-generator` skill
- Integrate with existing Google Calendar MCP, tasks, performance anomalies
- Create unified morning briefing

**Phase 4: Knowledge Base Search** (4-5 hours)
- Make 178+ knowledge base docs searchable
- Study Mike's `brain-advisor` agent
- Implement semantic search capability

**Phase 5: Inbox Processing** (2-3 hours)
- Create `!inbox/` folder for quick capture
- Implement action keyword routing
- Process every 6 hours via LaunchAgent

**Phase 6: Learn from remaining agents** (3-4 hours)
- Study prompt engineering patterns
- Document workflow patterns
- Create `MIKE-RHODES-PATTERNS.md`

---

## Key Takeaways

### What Mike Does Better
1. **Documentation architecture** - Progressive disclosure, topic-specific files
2. **Account sizing strategy** - Adaptive approach for different scales
3. **Analysis frameworks** - Codified expert knowledge, standard recommendations

### What PetesBrain Does Better
1. **Product Impact Analyzer integration** - Unique, high-value feature
2. **Per-client directory structure** - Better for agency work
3. **Client context integration** - CONTEXT.md + google-ads-clients.json
4. **Transform script flexibility** - Explicit arguments for customization

### Best Practices Learned
1. **Break large skills into topic-specific files**
2. **Use "Read this file when..." directives**
3. **Adapt query strategy to account size**
4. **Document analysis frameworks** (reduces hallucination)
5. **Quantify impact** in all recommendations
6. **Keep unique advantages** while adopting better patterns

---

**Status:** Phase 2 COMPLETE ✅
**Next:** Phase 3 - Daily Briefing System
**Confidence:** High - PetesBrain enhanced without losing advantages
