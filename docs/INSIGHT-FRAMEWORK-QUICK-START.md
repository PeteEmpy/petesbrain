# Insight Framework Quick Start Guide

**What we built:** A systematic framework that transforms your weekly reports from "here are some numbers" to "here's what happened, why it happened, and what to do about it."

---

## 🎯 The Core Concept

**Data → Information → Insight → Action**

| Level | What It Is | Example |
|-------|------------|---------|
| **Data** | Raw numbers | Cost: £2,450, ROAS: 360% |
| **Information** | Data + context | ROAS dropped from 420% to 360% (-14%) |
| **Insight** | Information + meaning | CPC increased 22% while CVR stayed flat → external competitive pressure |
| **Action** | Insight + commitment | Test improved ad copy by Friday to increase Quality Score |

**The system now automates levels 1-3 and creates level 4 tasks automatically.**

---

## 📁 What Was Created

### 1. Insight Generation Engine
**File:** `shared/insight_rules.py`

Systematic rules that diagnose WHY metrics changed:

```python
from insight_rules import InsightEngine

engine = InsightEngine()
insights = engine.generate_insights(current_metrics, previous_metrics)
```

**Detects:**
- ROAS drops (diagnoses: CPC inflation vs conversion issues vs product mix)
- ROAS spikes (explains: CVR improvement vs AOV increase vs cost reduction)
- Zero conversion campaigns (identifies waste)
- Spend increases (classifies: profitable scale vs inefficient scale)
- Below-target performance (contextualises gaps)

**For each insight, provides:**
- What changed (information)
- Why it happened (diagnosis)
- What to do about it (recommended direction)
- Priority (P0/P1/P2)

**🔥 CRITICAL FEATURE: Conversion Lag Detection**

The InsightEngine automatically detects when data is too fresh to be reliable:

```python
insights = engine.generate_insights(
    current_metrics,
    previous_metrics,
    target_roas=400,
    current_period_end_date='2025-12-16',  # NEW: Pass period end date
    current_period_days=7
)
```

**Data Quality Standards:**
- **0-2 days after period ends**: 30-48% complete → **BLOCKS insights** (too unreliable)
- **3-6 days**: 80-90% complete → **Generates with caveats** (downgraded priorities P0→P1, P1→P2)
- **7+ days**: 95%+ complete → **Normal insights** (reliable data)

**Why this matters:** Conversions can be attributed up to 30 days after click. Comparing incomplete data (e.g., "this week ending yesterday") to complete data (e.g., "last week") creates false insights. The system now prevents this automatically.

**Example protection:**
```
📊 Period ended 1 day ago (only 40% complete)
⚠️  Data too recent for reliable insights

Recommended action:
- Wait until 2025-12-23 for reliable data (7 days after period ends)
- Or use previous complete week instead
- Or accept that insights may change as more conversions are attributed
```

---

### 2. Enhanced Weekly Report Skill
**File:** `.claude/skills/google-ads-weekly-report/skill.md`

Your weekly report skill now:

1. ✅ Collects data (as before)
2. ✅ Calculates changes (as before)
3. ✅ **NEW: Generates insights** (systematic WHY analysis)
4. ✅ **NEW: Creates tasks from insights** (automatic action items)

**Report structure:**
- Executive Summary (Level 2: Information) - tables with data
- Performance Analysis (Level 3: Insight) - WHY section explaining changes
- Action Items (Level 4: Action) - tasks created automatically
- Campaign Breakdown (detailed data)

---

### 3. Demo Documentation
**File:** `docs/INSIGHT-FRAMEWORK-DEMO.md`

Before/after comparison showing the transformation from information-only reports to insight-driven reports.

---

## 🚀 How to Use It

### Test It This Week

1. **Pick a client** (Smythson recommended - complex account)

2. **Run the weekly report:**
   ```
   "Generate weekly Google Ads report for Smythson"
   ```

3. **Check the output:**
   - Look for the "Performance Analysis" section
   - Does it explain WHY metrics changed?
   - Are the diagnoses accurate?
   - Are the recommended actions specific and helpful?

4. **Check tasks:**
   - Were tasks created automatically?
   - Do they have clear actions in the notes?
   - Are priorities appropriate (P0/P1/P2)?

---

## 🔍 What to Expect

### Scenario 1: ROAS Drop Due to CPC Increase

**OLD Report:**
```
ROAS: 360% (was 420%, -60pp)
CPC: £2.20 (was £1.80, +22%)
```
*You think: "Hmm, ROAS is down. Is this a problem? What should I do?"*

**NEW Report:**
```
🔍 ROAS Dropped 14% WoW (P1)

Why: CPC increased 22% while conversion rate remained stable at 4.2%.
This indicates auction competition increased, not a performance issue
with your ads or site.

Diagnosis: External competitive pressure

Actions:
- Test improved ad copy to increase Quality Score and reduce CPC
- Add exact match keywords to reduce waste from broad match
- Check Auction Insights for new competitors

✅ Task created: [Smythson] ROAS dropped 14% WoW (P1, Due: Dec 22)
```
*You think: "Got it - competition increased. I need to improve Quality Score. Task created."*

---

### Scenario 2: Zero Conversions with Spend

**OLD Report:**
```
Campaign: Brand Search
Conversions: 0
Spend: £75
```
*You think: "Is zero conversions normal for this campaign? Should I do something?"*

**NEW Report:**
```
🔍 Zero Conversions with £75 Spend (P0)

Why: Campaign spent £75 this week with zero conversions. This represents
approximately £325/month in wasted spend if trend continues.

Diagnosis: Zero conversion campaign

Actions:
- Check conversion tracking is working correctly
- Review search terms for irrelevant traffic
- Evaluate landing page relevance and quality
- Consider pausing if consistently underperforming

✅ Task created: [Client] Zero conversions with £75 spend (P0, Due: Dec 18)
```
*You think: "This is urgent - £325/month waste. Checking conversion tracking now."*

---

## 🎓 Understanding the Diagnoses

The engine uses specific logic to diagnose issues:

### ROAS Drop Patterns

| Pattern | Diagnosis | Typical Actions |
|---------|-----------|-----------------|
| CPC ↑, CVR stable | External competitive pressure | Improve Quality Score, add exact match |
| CVR ↓, CPC stable | Landing page/conversion issue | Check site, test pages, review checkout |
| AOV ↓, other stable | Product mix/pricing issue | Review product performance, test bundles |
| Mixed changes | Data anomaly or mixed factors | Check attribution, review daily breakdown |

### Spend Increase Patterns

| Pattern | Diagnosis | Typical Actions |
|---------|-----------|-----------------|
| Spend ↑, ROAS ↑ | Profitable scale | Continue, consider further increases |
| Spend ↑, ROAS stable | Neutral scale | Monitor closely, stable is good |
| Spend ↑, ROAS ↓ | Inefficient scale | Consider budget reduction, analyse incremental traffic |

---

## ⚙️ Adjusting the Rules

If you find the insights too sensitive or not sensitive enough, adjust thresholds in `shared/insight_rules.py`:

```python
# Current thresholds (line 54-66)
if changes['roas_change_pct'] < -10:  # ROAS drop threshold
if changes['roas_change_pct'] > 15:   # ROAS spike threshold
if changes['spend_change_pct'] > 15:  # Spend increase threshold
if current_metrics.get('roas', 0) < target_roas * 0.90:  # Below target threshold
```

**Recommendations:**
- Start with current thresholds (10-15%)
- Run 2-3 weeks of reports
- Adjust if too noisy (raise thresholds) or missing issues (lower thresholds)

---

## 📊 Task Creation Logic

Tasks are created when:

1. **Priority is P0 or P1** (from automatic diagnosis)
2. **Action is clear** (not just "monitor")
3. **Impact is measurable** (revenue opportunity or waste reduction)

**P0 tasks:**
- Zero conversion campaigns with >£50 spend
- Landing page/conversion issues (CVR drops >10%)
- Due: 2 days

**P1 tasks:**
- External competitive pressure (CPC inflation)
- Inefficient scaling (spend up, ROAS down)
- Below-target performance
- Due: 7 days

**P2 insights:**
- ROAS improvements (good news - monitor)
- Profitable scaling (continue current approach)
- Not converted to tasks (stay in report only)

---

## 🔄 Integration with Your Workflow

### Current State
1. You run weekly report skill
2. Report includes data tables
3. You manually interpret and create tasks

### New State
1. You run weekly report skill
2. Report includes:
   - Data tables (as before)
   - **Performance Analysis section** (NEW - automatic WHY)
   - **Action Items section** (NEW - tasks created)
3. You open tasks.json and start working

**Time saved per report:** 20-30 minutes (no manual interpretation needed)

---

## 🚀 Next Steps (Phase 2)

Once you're comfortable with Phase 1:

1. **Add AI layer** - Use Claude to analyse patterns the rule engine might miss
2. **Schedule automation** - Run reports automatically every Monday 7am
3. **Client communication** - Auto-generate client email summaries from insights
4. **Trend tracking** - Track insight patterns over time ("3 weeks of competitive pressure")

---

## 💡 Key Takeaways

1. **Data alone is useless** - You need to know WHY metrics changed
2. **Insights drive action** - "ROAS dropped" → "External competition" → "Test new ad copy"
3. **Systematise interpretation** - Don't rely on manual analysis every week
4. **Automate task creation** - Let insights create your todo list

---

## 🆘 Troubleshooting

**No insights generated:**
- Check thresholds - changes might be below detection levels
- Verify metrics have proper keys ('roas', 'cpc', 'cvr', etc.)
- Run test: `python3 shared/insight_rules.py`

**Too many insights:**
- Raise thresholds in `insight_rules.py` (change -10 to -15, etc.)
- Add minimum spend filters (ignore campaigns <£100/week)

**Insights not helpful:**
- Review diagnosis logic in `_analyse_roas_drop()` etc.
- Add new diagnosis patterns for your specific scenarios
- Adjust recommended actions to match your workflow

**Tasks not created:**
- Check priority (only P0/P1 create tasks)
- Verify actionable keywords present in recommendations
- Check `ClientTasksService` is accessible

---

## 📚 Further Reading

- `docs/INSIGHT-FRAMEWORK-DEMO.md` - Before/after comparison with examples
- `shared/insight_rules.py` - Full source code with all diagnosis logic
- `.claude/skills/google-ads-weekly-report/skill.md` - Complete skill implementation

---

**Ready?** Run your first insight-driven report and experience the difference between information and insight.
