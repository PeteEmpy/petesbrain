# Experiment Logging Guide

**Purpose:** Ensure every strategic change is logged with complete information for future analysis.

---

## The 5 Essential Questions

When logging ANY strategic change (campaign structure, budget, ROAS, new features), answer these:

### 1. What are you changing? (1 sentence)
**Be specific and factual.**

✅ Good:
- "Creating standalone PMax campaign for Smythson Diaries"
- "Reducing UK ROAS target from 4.3 to 3.8"
- "Splitting Travel Bags asset group into separate campaign"

❌ Too vague:
- "Optimizing campaigns"
- "Making some changes"
- "Testing new structure"

---

### 2. Why? (Strategic reasoning)
**What's the business/performance reason for this change?**

✅ Good:
- "Diaries have distinct AW25 seasonality and need dedicated budget control"
- "UK market is mature and can handle volume growth at lower ROAS"
- "Travel Bags represent 20% of revenue with 50% higher ROAS than blended average"

❌ Too vague:
- "To improve performance"
- "Google recommended it"
- "Testing something"

**Prompts to help:**
- What problem are you solving?
- What opportunity are you capturing?
- What data/insight led to this decision?

---

### 3. What do you expect to happen? (Hypothesis with numbers)
**Quantify your expectations. Be specific.**

✅ Good:
- "+10% diary revenue, maintain ROAS 4.0+"
- "Volume increase 20%, ROAS drop 5-10% (acceptable for growth)"
- "Travel Bags ROAS 5.0+ vs current blended 3.8"

❌ Too vague:
- "Performance will improve"
- "Should see some increase"
- "Better results"

**Prompts to help:**
- What metric will improve?
- By how much?
- What's acceptable trade-off? (e.g., lower ROAS for higher volume)

---

### 4. When should we review this? (Timeline)
**When will we have enough data to evaluate?**

**Guidelines:**
- **Structural changes** (new campaigns, asset groups): 14-28 days
- **Budget changes**: 7-14 days
- **ROAS/bidding changes**: 14-21 days (Google learning period)
- **Creative/copy tests**: 30+ days (need volume)

✅ Good:
- "14 days (Nov 11, 2025)"
- "30 days (need full month of data)"
- "After Black Friday (Dec 2)"

❌ Too vague:
- "Soon"
- "When it's ready"
- "A few weeks"

---

### 5. What would success look like? (Success criteria)
**How will you know it worked?**

✅ Good:
- "Diary revenue +8-12%, ROAS maintains 4.0+, easier budget management"
- "Volume +20%, ROAS stays above 3.5, profitable growth"
- "Asset group ROAS 5.0+, makes up 25%+ of campaign revenue"

❌ Too vague:
- "Better performance"
- "Positive results"
- "Things improve"

**Prompts to help:**
- What's the minimum acceptable outcome?
- What would make this a clear win?
- What would make you roll this out to other accounts?

---

## Quick Reference Template

```
EXPERIMENT: [1 sentence - what changed]

WHY: [Strategic reasoning - what problem/opportunity]

HYPOTHESIS: [Expected outcome with numbers]

REVIEW DATE: [Specific date, X days out]

SUCCESS CRITERIA: [How we'll know it worked]

TAGS: [e.g., pmax, structure, budget, roas, creative]
```

---

## Example: Complete Experiment Log

```
EXPERIMENT: Created standalone PMax campaign for Smythson UK Diaries

WHY: Diaries have distinct AW25 seasonality (peak Sept-Dec) and represent
significant revenue. Need dedicated budget control during peak season and
clearer performance signals (not blended with other products).

HYPOTHESIS: +10% diary revenue vs blended performance, ROAS maintains or
improves from 3.8 baseline, easier budget allocation during peak.

REVIEW DATE: Nov 11, 2025 (14 days)

SUCCESS CRITERIA:
- Diary revenue increase 8-12%
- ROAS 4.0+ (vs 3.8 blended)
- Budget management easier (qualitative)
- If successful, roll out to USA and EUR

TAGS: pmax, structure, product-segmentation, seasonal
```

---

## When Claude Code Will Prompt You

**Trigger phrases that will activate prompting:**

- "I'm creating a new [campaign/asset group]..."
- "I'm changing the [budget/ROAS/structure]..."
- "I'm splitting out [product/category]..."
- "I'm testing [anything]..."
- "I'm going to try [anything]..."
- "Let's increase/decrease [metric]..."

**What Claude will do:**
1. Ask the 5 essential questions (if not already provided)
2. Format your answers into proper experiment log
3. Add row to ROK Experiments Google Sheet
4. Update client CONTEXT.md with "Active Tests" entry
5. Create review task for the timeline specified
6. Confirm everything is logged

**You just need to answer the questions - Claude handles the logging.**

---

## What Happens at Review Time

When the review date arrives:

1. **Claude will pull the data:**
   - Google Ads performance (actual results)
   - Change history (confirm what changed)
   - Context from CONTEXT.md and emails

2. **Claude will calculate:**
   - Actual vs expected outcome
   - Statistical significance (if enough data)
   - Whether success criteria met

3. **Claude will present:**
   - Results summary
   - Recommendation: Success/Failure/Mixed/Needs More Time
   - Rollout candidates (if successful)

4. **You decide:**
   - Roll out to other accounts?
   - Iterate and retest?
   - Revert changes?
   - Document in Strategy Playbook?

5. **Claude will update:**
   - ROK Experiments sheet (Actual Outcome)
   - Client CONTEXT.md (move to Completed Tests)
   - Strategy Playbook (if warranted)
   - Create rollout tasks (if approved)

---

## Tips for Better Experiment Logging

### Use Numbers
- "10% increase" not "big increase"
- "ROAS 4.0+" not "higher ROAS"
- "14 days" not "a couple weeks"

### Be Specific
- Name specific campaigns/products/regions
- Include baseline metrics for comparison
- State exact dates for review

### Think About Rollout
- If this works, where else could it apply?
- What would make this a clear win?
- What's the minimum acceptable result?

### Include Context
- What else is happening? (seasonality, promotions, etc.)
- Are there confounding factors?
- What might affect the results?

### Tag Properly
Use consistent tags for later filtering:
- `pmax`, `search`, `shopping`
- `structure`, `budget`, `roas`, `creative`
- `product-segmentation`, `regional`, `seasonal`
- `new-feature`, `optimization`, `expansion`

---

## Common Pitfalls to Avoid

❌ **Logging after the fact**
- Log WHEN you make the change, not days later
- Memory fades, details get lost

❌ **Vague expectations**
- "Should improve" isn't measurable
- Need numbers to evaluate success

❌ **No review timeline**
- Without a date, experiments never get evaluated
- Data sits unused

❌ **Missing the "why"**
- Future-you won't remember the reasoning
- Can't replicate without understanding why it worked

❌ **Not documenting failures**
- Failed tests are valuable learning
- Prevents repeating mistakes

---

## ROK Experiments Sheet Structure

**Columns in the Google Sheet:**

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Auto-generated when row added | 2025-10-28 10:30 |
| Client | Client name | Smythson UK |
| Experiment | What changed (1 sentence) | Created standalone PMax campaign for Diaries |
| Why | Strategic reasoning | Diaries have distinct seasonality, need budget control |
| Hypothesis | Expected outcome | +10% diary revenue, ROAS 4.0+ |
| Review Date | When to evaluate | 2025-11-11 |
| Success Criteria | How we'll know it worked | Revenue +8-12%, ROAS 4.0+, easier budget mgmt |
| Actual Outcome | [Filled at review time] | +15% revenue, ROAS 4.2 ✓ SUCCESS |
| Rollout Status | Next steps | SUCCESS - rolled to USA Nov 15 |
| Tags | For filtering/searching | pmax, structure, product-segmentation |
| Notes | Additional context | AW25 seasonal peak Sept-Dec |

---

*This guide ensures every strategic change is captured with enough detail to evaluate success and replicate wins across accounts.*
