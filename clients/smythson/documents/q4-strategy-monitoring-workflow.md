# Smythson Q4 Strategy - Monitoring Workflow

**Quick Reference**: How to track and evaluate the Q4 strategy rollout

---

## Weekly Routine (Every Monday)

### 1. Pull Performance Data
**Ask Claude:**
```
"Pull Smythson performance data for last week - all regions"
```

**Claude will:**
- Query Google Ads for UK, USA, EUR, ROW
- Show: spend, revenue, ROAS, conversions
- Compare to previous week
- Highlight any significant changes

---

### 2. Update Tracker
**Ask Claude:**
```
"Update the Q4 strategy tracker with last week's data"
```

**Claude will:**
- Add weekly data to cumulative table
- Calculate % of budget used
- Show progress toward £780K target
- Add weekly commentary

---

### 3. Check for Red Flags
**Claude automatically checks:**
- ⚠️ ROAS drops >15% from target
- ⚠️ Revenue declining unexpectedly
- ⚠️ Budget pacing off (>15%)
- ⚠️ Regional performance issues

**If red flags:** Claude alerts you and suggests course corrections

---

## At Each Milestone (When Changes Go Live)

### Before Implementation
**Example: Nov 15 - UK ROAS Reduction**

1. **Record baseline** (week before change):
   ```
   "Pull UK performance for Oct 29 - Nov 14 as baseline for ROAS reduction"
   ```

2. **Confirm what's changing**:
   - UK ROAS: 4.3 → 3.8
   - Budget: unchanged at £2,716/day
   - Expected: +10-15% revenue, ROAS 3.8-4.0

3. **Make the change in Google Ads**

4. **Log it**:
   ```
   "Log the UK ROAS reduction as implemented - review in 14 days"
   ```

---

### After Implementation (Review Period)

**Example: Nov 29 (14 days after Nov 15 change)**

1. **Pull results**:
   ```
   "Review UK ROAS reduction results - Nov 15-28 vs baseline"
   ```

2. **Claude analyzes**:
   - Actual revenue change: +X%
   - Actual ROAS: X.XX
   - vs Expected: +10-15% revenue, ROAS 3.8-4.0
   - Verdict: Success / Mixed / Failed

3. **Update tracker**:
   ```
   "Update Q4 tracker with UK ROAS reduction results"
   ```
   Claude fills in "Actual Results" and "Impact Assessment"

4. **Decision**:
   - ✅ Working as expected → Continue
   - ⚠️ Mixed results → Adjust or extend monitoring
   - ❌ Not working → Revert or modify

---

## Monthly Review Checkpoints

### Mid-November (Nov 15)
**Major review point - assess first 2 weeks**

**Ask Claude:**
```
"Run Smythson Q4 mid-November review"
```

**Claude will:**
- Summarize UK & EUR launches (Oct 29)
- Summarize USA launch (Nov 1)
- Overall Q4 progress vs target
- Projected end-of-quarter performance
- Recommendations for upcoming changes

**Questions to answer:**
1. Are we on track for £780K target?
2. Should we proceed with planned Nov 15 changes?
3. Any adjustments needed?

---

### December 1 Review
**Assess November performance before peak season push**

**Ask Claude:**
```
"Run Smythson Q4 December review"
```

**Claude will:**
- November total performance (all regions)
- Impact of UK ROAS reduction (Nov 15)
- Impact of USA Thanksgiving boost (Nov 25)
- ROW market assessment (2 weeks data)
- Readiness for December changes

**Questions to answer:**
1. Did November meet expectations?
2. Should we proceed with Dec 1 ROAS reductions?
3. Any budget reallocation needed?

---

### Mid-December (Dec 15)
**Revenue target validation**

**Ask Claude:**
```
"Run Smythson Q4 revenue validation - are we hitting target?"
```

**Claude will:**
- Q4 revenue to date (Oct 29 - Dec 15)
- Projected final revenue (based on pace)
- Gap to £780K target
- Final 2 weeks forecast
- Last-minute optimization opportunities

**Questions to answer:**
1. Will we hit £780,691 target?
2. Any emergency adjustments needed?
3. Push harder or maintain course?

---

### End of Quarter (Dec 31)
**Final assessment and learnings**

**Ask Claude:**
```
"Run final Smythson Q4 assessment"
```

**Claude will:**
- Complete final tracker with all results
- Actual vs target (revenue, spend, ROAS)
- What worked / what didn't
- Regional performance comparison
- Key learnings for Strategy Playbook

**Outputs:**
1. Updated tracker with all final data
2. Q4 post-mortem summary
3. Recommendations for Q1 2026
4. Proven patterns added to Strategy Playbook

---

## Simple Voice Commands (Via Wispr Flow)

### Weekly Updates
- "Update Smythson Q4 tracker"
- "Pull Smythson weekly performance"
- "Any Smythson red flags?"

### Milestone Reviews
- "Review UK ROAS reduction results"
- "How's the USA Thanksgiving boost performing?"
- "Check Smythson December changes"

### Quick Checks
- "Where are we on Smythson Q4 target?"
- "Show Smythson budget pacing"
- "Compare Smythson regions"

### Course Corrections
- "Smythson EUR underperforming - what should I do?"
- "Should I proceed with planned UK ROAS drop?"
- "Revert USA budget increase"

---

## What Claude Does Automatically

**Every week:**
- Pulls performance data when asked
- Updates tracker tables
- Calculates progress to target
- Checks for red flags
- Adds commentary

**At milestones:**
- Reminds you review is due (via Google Task)
- Compares actual vs expected
- Recommends: continue / adjust / revert
- Updates experiment log
- Documents learnings

**End of quarter:**
- Completes final assessment
- Adds successful strategies to Playbook
- Creates rollout tasks if patterns work

---

## Integration with Other Systems

**This tracker connects to:**

1. **Google Tasks**: Milestone reminders already created
2. **ROK Experiments Sheet**: Each phase logged with hypothesis
3. **Strategy Playbook**: Successful patterns documented
4. **Smythson CONTEXT.md**: All results added to learnings
5. **Weekly Email**: Budget tracking included automatically

**You just need to:**
- Ask Claude for updates (weekly)
- Review results at milestones (every 2-4 weeks)
- Make go/no-go decisions on upcoming changes

**Claude handles:**
- Data pulling
- Calculations
- Documentation
- Red flag alerts
- Recommendations

---

## Example Full Workflow (Nov 15 UK ROAS Reduction)

**Nov 8 (1 week before):**
```
You: "Pull UK baseline before Nov 15 ROAS change"
Claude: [Shows Oct 29 - Nov 14 data]
        Revenue: £X,XXX/week
        ROAS: 4.3
        Ready for Nov 15 reduction
```

**Nov 15 (implementation day):**
```
You: [Make change in Google Ads: ROAS 4.3→3.8]
You: "Logged UK ROAS reduction - review Nov 29"
Claude: [Updates tracker, creates review task for Nov 29]
```

**Nov 22 (mid-monitoring check):**
```
You: "How's UK ROAS reduction looking?"
Claude: [Shows Nov 15-21 data]
        Revenue: +12% vs baseline ✓
        ROAS: 3.9 ✓
        Early signals positive
```

**Nov 29 (formal review):**
```
You: "Review UK ROAS reduction results"
Claude: [Full analysis]
        Revenue: +14% (expected +10-15%) ✓ SUCCESS
        ROAS: 3.9 (expected 3.8-4.0) ✓ SUCCESS
        Verdict: Working as planned - continue
        [Updates tracker, marks milestone complete]
```

---

**Simple, systematic, data-driven. Nothing falls through the cracks.**
