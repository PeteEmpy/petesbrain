# Data → Information → Insight → Action Framework
## Before & After Demonstration

This document shows the transformation of your weekly reporting system using the systematic insight framework.

---

## 🔴 BEFORE: Information Only (Level 2)

```markdown
# Google Ads Weekly Report: Smythson
**Period:** Dec 9-15, 2025

## Executive Summary

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Spend | £2,450 | £2,100 | +16.7% |
| Revenue | £8,820 | £8,820 | 0% |
| ROAS | 360% | 420% | -60pp |
| Conversions | 48 | 46 | +4.3% |
| CPC | £2.20 | £1.80 | +22.2% |
| CVR | 4.2% | 4.2% | 0% |
| AOV | £185 | £185 | 0% |
```

**Problem with this approach:**
- ❌ You know WHAT changed (ROAS down 60pp, CPC up 22%)
- ❌ You DON'T know WHY it happened
- ❌ You DON'T know what to do about it
- ❌ No clear next steps
- ❌ No prioritisation
- ❌ Requires manual interpretation every week

**Result:** You spend 30 minutes staring at numbers trying to figure out what's going on.

---

## 🟢 AFTER: Insight + Action (Levels 3 & 4)

```markdown
# Google Ads Weekly Report: Smythson
**Period:** Dec 9-15, 2025

## Executive Summary (Level 2: Information)

| Metric | This Week | Last Week | Change | Trend |
|--------|-----------|-----------|--------|-------|
| Spend | £2,450 | £2,100 | +16.7% | ╱╱─╱ |
| Revenue | £8,820 | £8,820 | 0% | ─── |
| ROAS | 360% | 420% | -60pp | ╲╲── |
| Conversions | 48 | 46 | +4.3% | ─╱─ |
| CPC | £2.20 | £1.80 | +22.2% | ╱╱╱ |

---

## Performance Analysis (Level 3: Insight)

### 🔍 ROAS Dropped 14% WoW (P1)

**What Changed:**
ROAS decreased from 420% to 360% (-14% week-over-week)

**Why It Happened:**
CPC increased 22% (£1.80 → £2.20) while conversion rate remained stable at 4.2%.
This indicates auction competition increased, not a performance issue with your ads or site.
Quality Score is stable, so this is external competitive pressure, not internal ad quality degradation.

**Diagnosis:** External competitive pressure

**Recommended Direction:**
- Test improved ad copy to increase Quality Score and reduce CPC
- Add exact match keywords to reduce waste from broad match
- Check Auction Insights for new competitors
- Consider alternative keyword themes with lower competition

**Supporting Data:**
- Current ROAS: 360%
- Previous ROAS: 420%
- CPC Change: +22%
- CVR Change: 0% (stable at 4.2%)
- AOV Change: 0% (stable at £185)

---

### 🔍 Spend Increased 17% WoW (P1)

**What Changed:**
Spend rose from £2,100 to £2,450 (+16.7% week-over-week)

**Why It Happened:**
Spend increased 17% but ROAS declined 14%. Hitting diminishing returns - the additional
spend is not generating proportional returns. This suggests you're reaching beyond your
core high-intent audience into lower-converting traffic.

**Diagnosis:** Inefficient scale

**Recommended Direction:**
- Consider reducing budgets back to previous level (£2,100/week)
- Analyse what additional traffic/products drove increased spend
- Test incremental increases rather than large jumps
- Review impression share to see if you're maxing out high-quality placements

**Supporting Data:**
- Current spend: £2,450
- Previous spend: £2,100
- Spend change: +17%
- ROAS change: -14% (inefficient scaling)

---

## Action Items (Level 4: Action)

✅ **Created 2 tasks from insights:**

1. **[Smythson] ROAS dropped 14% WoW** (P1 - Due: Dec 22)
   - Diagnosis: External competitive pressure
   - Actions: Test brand + product ad copy, add exact match keywords, check Auction Insights
   - Expected impact: Reduce CPC by 10-15% through improved Quality Score

2. **[Smythson] Spend increased 17% WoW** (P1 - Due: Dec 22)
   - Diagnosis: Inefficient scale
   - Actions: Analyse incremental traffic quality, consider budget reduction
   - Expected impact: Improve efficiency by reducing low-ROAS spend

**All tasks saved to clients/smythson/tasks.json**

---

## Campaign Breakdown

[Rest of report with detailed campaign data...]
```

**Advantages of this approach:**
- ✅ You know WHAT changed (ROAS down 60pp)
- ✅ You know WHY it happened (CPC inflation from competition)
- ✅ You know WHAT to do (test new copy, add exact match)
- ✅ Tasks created automatically with clear actions
- ✅ Prioritised by impact (P1 = important)
- ✅ No manual interpretation needed

**Result:** You open the report Monday morning, see 2 specific tasks with clear actions, and get to work immediately.

---

## The Key Difference

### Before (Information):
> "ROAS dropped 60 points and CPC went up 22%"

**Your reaction:** *"Okay, but why? Is this bad? What should I do?"*

### After (Insight + Action):
> "ROAS dropped because auction competition increased (CPC +22%). Your ads and site are performing fine (CVR stable at 4.2%). This is external pressure. Test improved ad copy to increase Quality Score and reduce CPC. Task created with due date Dec 22."

**Your reaction:** *"Got it. I know exactly what to do. Let me work on the ad copy."*

---

## Implementation Summary

**What Changed in the System:**

1. **Added `shared/insight_rules.py`** - Systematic insight generation engine
2. **Updated `google-ads-weekly-report` skill** - Integrated InsightEngine into workflow
3. **Task creation driven by insights** - Not arbitrary thresholds

**How It Works:**

```python
# Step 1: Collect data (you already do this)
current_metrics = {
    'spend': 2450,
    'revenue': 8820,
    'roas': 360,
    'cpc': 2.20,
    'cvr': 4.2,
    'aov': 185
}

# Step 2: Generate insights (NEW - automatic diagnosis)
from insight_rules import InsightEngine
engine = InsightEngine()

insights = engine.generate_insights(current_metrics, previous_metrics, target_roas=400)

# Step 3: Create tasks from insights (NEW - automatic action)
for insight in insights:
    if insight['priority'] in ['P0', 'P1']:
        create_task(
            title=f"[Smythson] {insight['title']}",
            notes=f"{insight['why_it_happened']}\n\nActions:\n{insight['recommended_direction']}",
            priority=insight['priority']
        )
```

**Effort Required:**
- Setup: 10 minutes (already done!)
- Per report: 0 minutes extra (it's automatic)

**Value Delivered:**
- Save 30 mins per report (no manual interpretation)
- Catch issues you might miss (systematic analysis)
- Clear action items every week (no ambiguity)
- Consistent quality (not dependent on your mood/energy)

---

## Next Steps for You

Your enhanced system is ready to use. Here's what to do:

1. **This Week:** Run a weekly report for one client (Smythson recommended)
   ```
   "Generate weekly Google Ads report for Smythson"
   ```

2. **Compare:** Look at the "Performance Analysis" section - does it explain WHY metrics changed?

3. **Check Tasks:** Were tasks created automatically with clear actions?

4. **Iterate:** After 2-3 weeks, we can refine the insight rules based on what's most useful

---

## 🛡️ Conversion Lag Protection (CRITICAL FEATURE)

**The Problem We Solved:**

When you compare incomplete data to complete data, you get false insights. For example:

- **Complete week** (Dec 8-14, ended 7 days ago): 95%+ conversions attributed
- **Incomplete week** (Dec 15-16, ended 1 day ago): Only ~40% conversions attributed

If you project the incomplete week ("multiply by 3.5x"), you'd see CVR appear to drop 29% - but this is FALSE. The conversions just haven't been attributed yet.

**The Solution:**

The InsightEngine now automatically detects data freshness and protects you from false insights:

### Example: Data Too Fresh (Blocked)

```markdown
## Weekly Report: Clear Prospects
**Period:** Dec 15-16, 2025 (ended 1 day ago)

⚠️ **Data Quality Warning**

Current period ended **1 day ago** (only **40% complete**)

**Why we can't generate insights:**
Conversions can be attributed up to 30 days after click. Data from periods that ended <3 days ago is too incomplete for reliable analysis.

**Recommended actions:**
- Wait until **2025-12-23** for reliable data (7 days after period ends)
- For immediate analysis, use previous complete week instead
- Or accept that insights may change as more conversions are attributed
```

**Result:** No false insights. No wasted time investigating phantom issues.

### Example: Data Partial (Generated with Caveats)

```markdown
## Weekly Report: Clear Prospects
**Period:** Dec 12-18, 2025 (ended 4 days ago)

## Performance Analysis

### 🔍 ROAS dropped 14% WoW (P2)

⚠️ **Based on 85% complete data** (period ended 4 days ago). True performance may differ as more conversions are attributed.

**What Changed:**
ROAS decreased from 420% to 360% (-14% week-over-week)

**Why It Happened:**
CPC increased 22% while conversion rate remained stable at 4.2%...

**Priority Note:** Downgraded from P1 due to incomplete data
```

**Result:** You get insights, but with clear caveats and downgraded priority until data is complete.

### Example: Data Complete (Normal Insights)

```markdown
## Weekly Report: Clear Prospects
**Period:** Dec 8-14, 2025 (ended 9 days ago)

## Performance Analysis

### 🔍 ROAS dropped 14% WoW (P1)

**What Changed:**
ROAS decreased from 420% to 360% (-14% week-over-week)

**Why It Happened:**
CPC increased 22% while conversion rate remained stable at 4.2%. This indicates auction competition increased, not a performance issue with your ads or site.

**Diagnosis:** External competitive pressure

**Actions:**
- Test improved ad copy to increase Quality Score and reduce CPC
- Add exact match keywords to reduce waste from broad match
- Check Auction Insights for new competitors

✅ **Task created:** [Clear Prospects] ROAS dropped 14% WoW (P1, Due: Dec 22)
```

**Result:** Reliable insights with normal priorities and automatic task creation.

---

## The Bigger Picture

This is **Phase 1** of your automation journey - moving from manual interpretation to systematic insight generation.

**Phase 2** (next): Add AI analysis on top of the systematic rules for even deeper insights.

**Phase 3** (later): Schedule this to run automatically every Monday morning, so you wake up to insights + tasks without lifting a finger.

You're building the foundation for a fully autonomous reporting system that doesn't just show you numbers - it tells you what they mean and what to do about it.

---

**Ready to test it?** Run your first insight-driven weekly report this week and see the difference.
