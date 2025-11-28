# Claude Skills - ROK Integration Complete

**Date**: November 5, 2025  
**Status**: ✅ Complete

---

## Overview

Updated Claude Code skills to integrate with **all ROK-specific methodologies and tools**, ensuring audits and analysis are aware of:
- Product Hero Labelizer system (Heroes/Sidekicks/Villains/Zombies)
- Product Impact Analyzer (feed changes → performance correlation)
- Active experiments tracking (rok-experiments-client-notes.csv)
- Impact Analysis Workflow (experiment evaluation framework)
- Strategy Playbook (proven wins and failed tests)

---

## Changes Made

### 1. Google Ads Campaign Audit Skill Enhancement

**File**: `.claude/skills/google-ads-campaign-audit/skill.md`

#### Product Hero Labelizer Integration
- **Phase 2 - Product-Level Performance**: Now includes mandatory label segmentation
- Checks for custom_label_0 implementation (Heroes/Sidekicks/Villains/Zombies)
- Segments all product analysis by labels
- Identifies cross-contamination (products in wrong asset groups)
- Includes label distribution analysis in output
- Provides expected distribution benchmarks

**Key Features Added:**
```markdown
### Product Hero Labelizer Status
**Implementation**: ✅ Active / ⚠️ Not Detected  
**Label Distribution**:
- Heroes ⭐: X products → £X,XXX revenue
- Sidekicks 🎯: X products → £X,XXX revenue  
- Villains 👎: X products → £X spend (⚠️ WASTE)
- Zombies 🧟: X products → £X spend (test)
```

**Red Flags to Identify:**
- Villains appearing in Heroes/Sidekicks asset groups
- Heroes not getting sufficient budget/impressions
- Asset groups without proper custom_label_0 filtering

#### Product Impact Analyzer Integration
**When to check:**
- Shopping campaign performance changes
- Unexplained product-level traffic spikes/drops
- Feed quality issues identified
- Before recommending product feed changes

**How it works:**
1. Check if client is tracked in Product Impact Analyzer
2. Review recent product changes from weekly reports
3. Cross-reference product performance with feed changes
4. Include feed change context in root cause analysis

**Example audit output:**
```
❗ Product "Olive Tree Large" revenue dropped 35% this week.
Product Impact Analyzer shows: Price increased £34.99 → £39.99 on Oct 15.
Root cause: Price increase, not campaign issue.
Recommendation: Review pricing strategy with client.
```

#### Experiments Tracking Integration
**Checks:**
- Active experiments from `rok-experiments-client-notes.csv`
- Performance changes that align with experiment dates
- Experiments approaching review dates

**Audit output section:**
```markdown
## Experiment Context
**Active Experiments**:
- [Experiment]: ROAS 200% → 190% (Nov 5) - Review: Nov 12
- Early results: ROAS 1.88, impression share +8%
```

#### Strategy Playbook Integration
**References:**
- Proven Wins before recommending rollouts
- Failed Tests to avoid repeating mistakes
- Similar patterns from past successes

#### Asset Group Filtering Verification
New mandatory section in audit output:
```markdown
## Asset Group Filtering Verification
| Asset Group | Expected Filter | Actual | Issues |
|-------------|----------------|--------|--------|
| Furniture - Heroes | custom_label_0 = "heroes" | ✅ Match | None |
| Furniture - Sidekicks | custom_label_0 = "sidekicks" | ⚠️ Cross-contamination | Contains 3 Villains! |
```

---

### 2. Weekly Summary Enhancement - Experiments Integration

**File**: `agents/reporting/kb-weekly-summary.py`

#### New Function: `get_recent_experiments()`
- Reads `rok-experiments-client-notes.csv`
- Extracts experiments from last 14 days
- Parses both DD/MM/YYYY and YYYY-MM-DD formats
- Returns structured experiment data

#### Updated Claude Prompt
Added new section **🧪 Active Experiments & Strategic Changes**:
- Groups experiments by client
- Shows what changed, why, and when to review
- Cross-references with performance data
- Highlights experiments needing review this week

**Email output format:**
```
3. 🧪 Active Experiments & Strategic Changes

**Accessories for the Home:**
- 05/11/2025: ROAS reduced 200% → 190% to combat competitive 
  pressure (51-78% rank-lost IS). Review: Nov 12.
  Early signs: Impression share recovering, ROAS stable at 1.88.

**National Design Academy:**
- 05/11/2025: Budget optimization -40% (£40k → £24k/month).
  Protected top performers, eliminated waste on zero-converters.
```

#### Integration Flow
1. Script calls `get_recent_experiments(days=14)`
2. Passes experiments to `analyze_knowledge_base_with_claude()`
3. Claude analyzes experiments alongside performance data
4. Email includes experiments as **Section 3** (after Performance, before Industry News)

---

## Skills Updated

### ✅ google-ads-campaign-audit
**Enhancements:**
- Product Hero Labelizer (mandatory for e-commerce)
- Product Impact Analyzer integration
- Experiments tracking
- Strategy Playbook references
- Asset group filtering verification

### ✅ kb-weekly-summary (Python script)
**Enhancements:**
- Experiments CSV reading
- Weekly experiment summary in email
- Cross-referencing experiments with performance

---

## Key ROK Methodologies Now Integrated

### 1. Product Hero Labelizer System
**File**: `roksys/knowledge-base/rok-methodologies/product-hero-labelizer-system.md`
- Heroes ⭐: Top 10% revenue generators
- Sidekicks 🎯: Good converters needing visibility
- Villains 👎: Budget drainers (exclude!)
- Zombies 🧟: Dormant products (test activation)

**Skills integration**: Audits now check for label implementation and segmentation

### 2. Product Impact Analyzer
**Location**: `tools/product-impact-analyzer/`
- Correlates feed changes with ad performance
- Identifies what feed changes helped/hurt
- Weekly automated reports

**Skills integration**: Audits cross-reference product performance with feed changes

### 3. Experiments Logging System
**File**: `roksys/spreadsheets/rok-experiments-client-notes.csv`
- All strategic changes logged with hypothesis
- Review dates tracked
- Expected outcomes documented

**Skills integration**: 
- Audits reference active experiments
- Weekly emails include experiment summaries
- Performance analyzed in context of tests

### 4. Impact Analysis Workflow
**File**: `roksys/knowledge-base/rok-methodologies/impact-analysis-workflow.md`
- Framework for evaluating completed experiments
- Before/after comparison methodology
- Rollout decision criteria

**Skills integration**: Audits flag experiments approaching review dates

### 5. Strategy Playbook
**File**: `roksys/knowledge-base/rok-methodologies/strategy-playbook.md`
- Proven Wins (successful strategies to replicate)
- Failed Tests (mistakes to avoid)
- Rollout candidates

**Skills integration**: Audits reference Playbook before recommending changes

---

## Updated Audit Output Structure

```markdown
# Google Ads Audit: [Client Name]

## Executive Summary
[Overall health, major findings]

## Key Metrics
[Performance table]

## Campaign Performance
[Campaign breakdown]

## Product-Level Insights (Shopping)
### Product Hero Labelizer Status ⭐🎯👎🧟
[Label distribution and performance by label]

### Best Products (Top 10 Heroes)
[Top performers]

### Worst Performers (Villains Draining Budget)
[Products to exclude]

## Asset Group Filtering Verification
[Check for cross-contamination]

## Placement Analysis
[Placement performance]

## Budget & Impression Share
[IS analysis]

## Root Cause Analysis
[Issues with Product Hero and feed change context]

## Prioritized Recommendations
[Actions with expected impact]

## Experiment Context ⭐ NEW
**Active Experiments**:
- [List of active tests]

**Product Feed Changes**:
- [Recent feed changes from Product Impact Analyzer]

**Relevant Playbook Strategies**:
- [Proven Wins applicable here]

## Follow-Up Questions
[Including experiment and feed change questions]

## Next Steps
[Actions + experiment reviews + Product Impact Analyzer checks]
```

---

## Client Context Files Integration

All audits now reference:
- `clients/[client-name]/CONTEXT.md` - Business context, **active experiments**
- `clients/[client-name]/audits/` - Previous audits
- `roksys/spreadsheets/rok-experiments-client-notes.csv` - Experiment log
- Product Impact Analyzer reports (if client tracked)
- Strategy Playbook (proven wins/failures)

---

## Weekly Email Structure (Updated)

1. **📅 Week Ahead** (Tasks)
2. **📊 Client Performance** (Last 7 days)
3. **🧪 Active Experiments & Strategic Changes** ⭐ NEW
4. **🤖 Automated Industry Monitoring** (Google Ads + AI news)
5. **AI News Highlights**
6. **Knowledge Base Additions**
7. **Key Insights for ROK**
8. **This Week in Numbers**

---

## Example: Accessories for the Home Audit (Nov 5)

### Before Integration ❌
```
Main P Max ROAS: 1.96
Recommendation: Consider reducing ROAS target to increase volume
```

### After Integration ✅
```
Main P Max (Furniture H&S) ROAS: 1.96

Product Hero Context:
- Campaign contains Heroes + Sidekicks asset groups
- Rank-lost IS: 51.3% (competitive pressure from Cox & Cox)

Active Experiment:
- Nov 5: ROAS target reduced 200% → 190%
- Hypothesis: Combat 51-78% rank-lost IS
- Expected: ROAS 1.85-1.90, IS increase 10-15%
- Review: Nov 12

Product Feed Changes (Product Impact Analyzer):
- None in last 7 days

Recommendation:
- Monitor experiment (Day 2/7)
- Early signs: ROAS 1.88 (within target), IS showing recovery
- Continue as planned, full evaluation Nov 12
```

---

## Files Modified

1. `.claude/skills/google-ads-campaign-audit/skill.md`
2. `agents/reporting/kb-weekly-summary.py`
3. `roksys/spreadsheets/rok-experiments-client-notes.csv` (added Accessories experiment)
4. `clients/accessories-for-the-home/CONTEXT.md` (updated with experiment)

---

## Benefits

### 1. **Context-Aware Audits**
- Understands Product Hero label structure
- Recognizes feed changes as root causes
- Aware of active experiments
- References proven strategies

### 2. **Integrated Analysis**
- Performance changes explained by experiments
- Product issues linked to feed changes
- Recommendations aligned with Playbook
- Cross-contamination detected automatically

### 3. **Experiment Tracking**
- Active experiments visible in weekly emails
- Review dates flagged in audits
- Performance analyzed in context of tests
- Rollout opportunities identified

### 4. **Feed Change Correlation**
- Product performance linked to feed changes
- Price changes identified as root causes
- Feed quality issues surfaced
- Data-driven feed recommendations

### 5. **Knowledge Reuse**
- Playbook strategies referenced
- Failed tests avoided
- Proven wins suggested for rollout
- Cross-account learning captured

---

## Next Steps

### Immediate
- ✅ Skills updated with ROK methodologies
- ✅ Weekly summary includes experiments
- ✅ Product Hero integration complete
- ✅ Product Impact Analyzer referenced

### Future Enhancements
1. **Automated Experiment Evaluation**
   - Script to check experiments approaching review dates
   - Auto-pull before/after performance
   - Generate impact reports

2. **Strategy Playbook Automation**
   - Successful experiments → auto-add to Playbook
   - Failed tests → auto-document learnings
   - Rollout candidates → auto-generate tasks

3. **Product Hero Monitoring**
   - Alert on label transitions (Hero → Sidekick)
   - Flag cross-contamination automatically
   - Track budget allocation by label

4. **Feed Change Alerts**
   - Product Impact Analyzer → immediate alerts
   - High-impact changes flagged
   - Root cause auto-linked to campaigns

---

## Testing

### Test Case 1: Accessories for the Home Audit ✅
**Result**: 
- Product Hero labels detected and analyzed
- Active ROAS experiment identified
- Audit output included experiment context
- Recommendations aligned with experiment

### Test Case 2: Weekly Email Generation
**Next Run**: Monday, Nov 11, 2025 (8:30 AM)
**Expected Output**:
- Section 3: "🧪 Active Experiments"
- Accessories experiment listed
- National Design Academy budget optimization listed
- Review dates flagged

---

## Conclusion

Claude Code is now **fully integrated with ROK's operational systems**:
- ✅ Product Hero Labelizer (account structure framework)
- ✅ Product Impact Analyzer (feed → performance correlation)
- ✅ Experiments System (strategic change tracking)
- ✅ Impact Analysis Workflow (experiment evaluation)
- ✅ Strategy Playbook (proven wins/failures)

**All audits and analysis now operate with full ROK context**, making recommendations data-driven, experiment-aware, and aligned with proven strategies.

---

**Last Updated**: November 5, 2025  
**Maintained By**: Peter Empson, ROK Systems

