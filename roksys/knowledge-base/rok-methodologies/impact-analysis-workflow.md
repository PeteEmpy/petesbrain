# Impact Analysis Workflow

**Purpose:** Step-by-step process for evaluating completed experiments and making data-driven rollout decisions.

---

## When to Run Impact Analysis

**Trigger:** Experiment review date arrives (set when experiment was logged)

**Who runs it:** Claude Code (automated, with your approval for decisions)

**Timeline:**
- Structural changes: 14-28 days after implementation
- Budget/ROAS changes: 7-14 days
- Creative tests: 30+ days

---

## The Analysis Process

### Step 1: Data Collection (Claude does this)

**What Claude pulls:**

1. **Google Ads Change History** (via MCP API)
   - Confirm what actually changed in the account
   - Verify implementation date and details
   - Check for any unintended changes

2. **Performance Data** (via MCP GAQL queries)
   - Before period: Same length as test period, immediately before change
   - After period: From implementation date to review date
   - Metrics: Revenue, ROAS, conversions, clicks, cost, impressions
   - Segmentation: By campaign, asset group, product, region (as relevant)

3. **Experiment Log** (from ROK Experiments sheet)
   - What was supposed to happen (hypothesis)
   - Success criteria
   - Strategic reasoning

4. **Context** (from client CONTEXT.md and emails)
   - Any confounding factors (other changes, external events)
   - Client feedback or concerns
   - Business changes affecting results

**Example data pull for Smythson Diaries test:**

```
BEFORE PERIOD: Oct 14-27, 2025 (14 days)
- Diaries in blended H&S campaign
- Diary revenue: £X,XXX
- Diary ROAS: X.XX
- Diary conversions: XXX

AFTER PERIOD: Oct 28 - Nov 10, 2025 (14 days)
- Diaries in standalone campaign
- Diary revenue: £X,XXX
- Diary ROAS: X.XX
- Diary conversions: XXX

CHANGE HISTORY CONFIRMS:
- Campaign "SMY | UK | P Max | Diaries" created Oct 28, 10:42 AM
- Asset group moved Oct 28, 10:45 AM
- Budget set to £XXX/day

CONFOUNDING FACTORS:
- None identified in emails/meetings
- No major external events
- No other campaign changes in this period
```

---

### Step 2: Impact Calculation (Claude does this)

**Calculations:**

1. **Absolute Change:**
   - Revenue: After - Before = £XXX (+/-)
   - ROAS: After - Before = X.XX (+/-)
   - Conversions: After - Before = XXX (+/-)

2. **Percentage Change:**
   - Revenue: (After - Before) / Before * 100 = +X%
   - ROAS: (After - Before) / Before * 100 = +X%

3. **vs. Hypothesis:**
   - Expected: +10% diary revenue
   - Actual: +15% diary revenue
   - Result: BEAT TARGET ✓

4. **Success Criteria Check:**
   - Criterion 1: Revenue +8-12% → Actual: +15% ✓ MET
   - Criterion 2: ROAS 4.0+ → Actual: 4.2 ✓ MET
   - Criterion 3: Easier budget management → Qualitative ✓ (to confirm with you)

5. **Statistical Significance** (if enough data):
   - Sample size sufficient?
   - Confidence level (95%)?
   - Result: Significant / Not significant / Needs more time

---

### Step 3: Results Presentation (Claude presents to you)

**Format:**

```
📊 EXPERIMENT IMPACT REPORT
Experiment: Smythson UK - Diaries Standalone PMax Campaign
Review Date: Nov 11, 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ SUCCESS - ROLL OUT RECOMMENDED

HYPOTHESIS vs. ACTUAL:
Expected: +10% diary revenue, ROAS 4.0+
Actual: +15% diary revenue, ROAS 4.2
Result: BEAT TARGET ✓

KEY METRICS:

Revenue:
  Before: £6,800 (14 days)
  After: £7,820 (14 days)
  Change: +£1,020 (+15.0%) ✓ BEAT TARGET (+10% expected)

ROAS:
  Before: 3.8 (blended in H&S campaign)
  After: 4.2 (standalone campaign)
  Change: +0.4 (+10.5%) ✓ MET TARGET (4.0+ expected)

Conversions:
  Before: 142 (14 days)
  After: 163 (14 days)
  Change: +21 (+14.8%)

Cost:
  Before: £1,789
  After: £1,862
  Change: +£73 (+4.1%) - efficient spend increase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUCCESS CRITERIA CHECK:
✓ Revenue increase 8-12%: ACTUAL +15% (exceeded)
✓ ROAS 4.0+: ACTUAL 4.2 (met)
✓ Budget management easier: [Confirm with user]

STATISTICAL SIGNIFICANCE: 95% confidence (sufficient data)

CONFOUNDING FACTORS: None identified

GOOGLE ADS CHANGE HISTORY CONFIRMS:
- Campaign created Oct 28, 10:42 AM
- Asset group moved Oct 28, 10:45 AM
- Budget set correctly
- No other changes during test period

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDATION: ROLL OUT IMMEDIATELY

Rollout Candidates (High Priority):
1. Smythson USA - Same diary product line
2. Smythson EUR - Same diary product line

Rollout Candidates (Medium Priority):
3. Tree2mydoor - Christmas trees (similar seasonal pattern)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:
1. Add to Strategy Playbook as "Proven Win"
2. Update Smythson CONTEXT.md (move to Completed Tests)
3. Update ROK Experiments sheet with results
4. Create rollout tasks for USA and EUR
5. Share results with client (optional)
```

---

### Step 4: Decision Making (You decide)

**Your options:**

1. **✅ APPROVE ROLLOUT**
   - Add to Strategy Playbook
   - Create tasks for rollout candidates
   - Update all documentation

2. **⚠️ NEEDS MORE TIME**
   - Extend monitoring period
   - Set new review date
   - Note reasons for extension

3. **🔄 ITERATE**
   - Make modifications based on learnings
   - Re-test with adjustments
   - Log as new experiment

4. **❌ REVERT**
   - Change didn't work as expected
   - Roll back to previous state
   - Document as failed test in Playbook

---

### Step 5: Documentation (Claude does this after your decision)

**If APPROVED for rollout:**

1. **Update ROK Experiments Sheet:**
   - Actual Outcome column: "+15% revenue, ROAS 4.2 ✓ SUCCESS"
   - Rollout Status: "SUCCESS - rolled to USA Nov 15, EUR Nov 18"

2. **Update Client CONTEXT.md:**
   - Move from "Active Tests" to "Completed Tests"
   - Add actual results
   - Mark as SUCCESS with rollout status

3. **Update Strategy Playbook:**
   - Add to "Proven Wins" section
   - Include all details (hypothesis, results, when to use)
   - List rollout candidates

4. **Create Rollout Tasks:**
   - "Smythson USA: Implement Diaries standalone campaign (proven win from UK)"
   - "Smythson EUR: Implement Diaries standalone campaign (proven win from UK)"
   - Include success criteria and expected results

**If FAILED or MIXED:**

1. **Update ROK Experiments Sheet:**
   - Actual Outcome: Describe what happened
   - Rollout Status: "FAILED - reverted" or "MIXED - needs iteration"

2. **Update Client CONTEXT.md:**
   - Move to "Completed Tests"
   - Document learnings

3. **Update Strategy Playbook:**
   - Add to "Failed Tests" section
   - Explain why it failed
   - Document lessons learned
   - Suggest better alternatives

---

## Example Scenarios

### Scenario 1: Clear Success (Smythson Diaries)

**Results:** +15% revenue, ROAS 4.2, all success criteria met
**Decision:** ✅ APPROVE ROLLOUT
**Action:**
- Add to Playbook as Proven Win
- Roll out to USA and EUR
- Consider for other seasonal products

---

### Scenario 2: Mixed Results

**Experiment:** Budget increase from £100 to £150/day
**Results:** +25% revenue (good!), but ROAS dropped from 4.0 to 3.2 (below acceptable 3.5)
**Decision:** ⚠️ ITERATE
**Action:**
- Try smaller budget increase (£100 to £125)
- Or accept lower ROAS if volume growth is strategic priority
- Log as new experiment with adjusted hypothesis

---

### Scenario 3: Clear Failure

**Experiment:** Blanket ROAS reduction across all campaigns
**Results:** Didn't implement (superseded by better strategy)
**Decision:** ❌ DOCUMENT AS FAILED
**Action:**
- Add to Playbook Failed Tests
- Explain why regional approach was better
- Prevent future blanket approaches

---

### Scenario 4: Needs More Time

**Experiment:** New asset group launched
**Results:** After 14 days, only 50 conversions (low sample size)
**Decision:** ⚠️ EXTEND MONITORING
**Action:**
- Extend to 30 days
- Set new review date
- Note: Waiting for sufficient data

---

## Key Principles

### 1. Data Integrity
- Always verify changes in Change History
- Check for confounding factors
- Compare apples to apples (same time periods)

### 2. Context Matters
- Consider seasonality
- Account for external events
- Check if other changes happened simultaneously

### 3. Statistical Significance
- Need sufficient sample size
- 7-14 days minimum for most changes
- 30+ days for low-volume campaigns

### 4. Honest Assessment
- Don't cherry-pick data
- Report failures as learning opportunities
- Mixed results are okay - iterate!

### 5. Scalability
- Successful tests should be replicable
- Document enough detail for others to implement
- Identify rollout candidates proactively

---

## Automation Opportunities

**Future enhancement:** Create `tools/strategy-impact-analyzer/`

**What it would do:**
1. Monitor for experiments approaching review date
2. Auto-pull performance data
3. Calculate impact metrics
4. Generate comparison reports
5. Flag for your review

**For now:** Claude does this manually when you say "Review the Diaries experiment" or when review date arrives

---

## Questions for Evaluation

When reviewing results, ask:

**Performance:**
- Did we meet our hypothesis?
- Which success criteria were met?
- What was the actual vs. expected outcome?

**Confidence:**
- Is the data statistically significant?
- Were there confounding factors?
- Do we need more time?

**Learnings:**
- Why did it work (or not work)?
- What does this tell us about the account?
- What would we do differently?

**Scalability:**
- Should we roll this out?
- Which accounts are good candidates?
- What modifications might be needed?

**Next Steps:**
- Implement elsewhere?
- Iterate and improve?
- Revert and try something different?

---

## Monthly Review Process

**1st of each month:**

1. Review all experiments completed in previous month
2. Update Strategy Playbook with proven wins and failures
3. Identify rollout opportunities across accounts
4. Create rollout tasks for successful tests
5. Share monthly summary with team (optional)

**Template for monthly summary:**

```
📊 MONTHLY STRATEGY REVIEW - [Month Year]

EXPERIMENTS COMPLETED: X

✅ SUCCESSES (X):
- [Client]: [Experiment] - [Result]
- [Client]: [Experiment] - [Result]

❌ FAILURES (X):
- [Client]: [Experiment] - [Learning]

🔄 ONGOING (X):
- [Client]: [Experiment] - [Status]

🎯 ROLLOUT ACTIONS:
- [Proven Win] → Roll out to [Accounts]
- [Proven Win] → Roll out to [Accounts]

📚 STRATEGY PLAYBOOK UPDATES:
- Added [X] proven wins
- Added [X] failed tests
- Updated [X] patterns
```

---

*This workflow ensures every experiment is evaluated rigorously and successful strategies are captured and scaled across accounts.*
