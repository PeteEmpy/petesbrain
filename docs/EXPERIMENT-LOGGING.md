# Experiment Logging Protocol

**Last Updated:** November 5, 2025

This document describes the mandatory prompting protocol for logging experiments in the ROK Experiments tracking system.

For architectural overview, see [CLAUDE.md](../CLAUDE.md). For client analysis workflows, see [CLIENT-WORKFLOWS.md](CLIENT-WORKFLOWS.md).

---

## Overview

Every strategic change made to client Google Ads accounts should be logged as an experiment with:
- **WHY**: What was driving this change?
- **WHAT**: What are you expecting to see?
- **WHEN**: When should we check back on this?
- **SUCCESS**: What would make this a win?

This enables tracking actual vs expected outcomes and builds institutional knowledge.

---

## MANDATORY PROMPTING PROTOCOL

**CRITICAL**: You MUST ask the 5 essential questions in these situations.

### Trigger Situations

#### 1. User asks you to log/add to experiment spreadsheet

- "Add this to experiments"
- "Log this experiment"
- "These budgets have been changed" (implies logging needed)
- ANY mention of updating rok-experiments-client-notes.csv

#### 2. You're about to write to rok-experiments-client-notes.csv

- BEFORE adding any row to the spreadsheet
- Even if user gave you a description

#### 3. You discover strategic changes in Google Ads Change History

- Campaign structure changes (new campaigns, paused campaigns)
- Budget changes >10%
- ROAS target changes
- New asset groups or ad groups
- Ask: "I see you made [change] on [date]. Should we log this as an experiment?"

---

## The Prompting Flow

### When Triggered, IMMEDIATELY Ask (Conversational Tone)

**Example:**
```
Got it - I can see you've made [describe the change]. Before I log this,
let me grab a few quick details so we can track the impact properly:

- What was driving this change? [contextualize the "why" based on what you know]
- What are you expecting to see? [suggest likely outcomes based on the change]
- When should we check back on this? [suggest a reasonable timeline]
- What would make this a win? [suggest success criteria based on the change]

Even quick answers are fine - I'll format it all properly!
```

### Be Conversational and Helpful

- Frame questions naturally, not as a checklist
- Show you understand the context
- Suggest possible answers to make it easier
- Keep it friendly and collaborative

### What You Do With Answers (Even Incomplete)

1. Format into proper experiment log entry
2. Add to rok-experiments-client-notes.csv
3. Update client CONTEXT.md if significant
4. Confirm it's logged

### DO NOT

- Skip the questions and assume you know
- Log experiments without prompting first
- Wait for "complete" answers (brief is fine)

---

## Working with Incomplete Answers

**The act of asking matters more than perfect answers.**

### Examples of Formatting Incomplete Answers

#### User: "Just need to hit budget target"
→ You format as: "WHY: Spending ahead of monthly budget, need to control spend"

#### User: "End of month"
→ You format as: "REVIEW: Nov 30, 2025"

#### User: "Not overspend"
→ You format as: "SUCCESS: Daily spend stays within £X budget, ROAS maintains 570%+"

---

## Experiment Log Entry Format

### CSV Structure

File: `roksys/spreadsheets/rok-experiments-client-notes.csv`

Columns:
- **Timestamp**: YYYY-MM-DD HH:MM:SS
- **Client**: Client name (match existing client folders)
- **Note**: Detailed experiment description
- **Tags**: Comma-separated tags (optional)

### Note Format

```
[CHANGE DESCRIPTION]

WHY: [What was driving this change]
WHAT: [What are you expecting to see]
WHEN: [When should we check back on this]
SUCCESS: [What would make this a win]
```

### Example Entry

```csv
2025-11-05 14:30:00,Smythson,"Increased daily budget from £150 to £200 for Shopping campaign

WHY: Q4 demand surge, inventory fully stocked, want to capture holiday traffic
WHAT: Expecting 30-40% revenue increase, ROAS to hold at 400%+
WHEN: Review Nov 12 (1 week after change)
SUCCESS: Revenue £280+/day (up from £200/day), ROAS maintains 400%+",budget,shopping,q4
```

---

## Context-Aware Suggestions

When asking the questions, provide smart suggestions based on:

### The Type of Change

**Budget Increase:**
- WHY: "Is this because performance is strong and you want to scale? Or hitting impression share cap?"
- WHAT: "Expecting proportional revenue increase? Or testing if performance holds at higher spend?"
- WHEN: "Usually 5-7 days for budget changes to stabilize"
- SUCCESS: "ROAS maintaining current levels? Or specific revenue target?"

**ROAS Target Decrease:**
- WHY: "Trying to increase volume? Hitting impression share limits?"
- WHAT: "Expecting more clicks/conversions at similar or slightly lower efficiency?"
- WHEN: "Smart Bidding takes 1-2 weeks to learn new target"
- SUCCESS: "Conversion volume increase of X%? Revenue increase of Y%?"

**Campaign Launch:**
- WHY: "What gap is this filling? New product category? Geographic expansion?"
- WHAT: "Initial expectations for new campaigns are usually conservative"
- WHEN: "Smart Bidding learning period is typically 2-3 weeks"
- SUCCESS: "What metrics would justify keeping this campaign running?"

**Pause/Pause:**
- WHY: "Performance issue? Budget reallocation? Seasonal decision?"
- WHAT: "Expecting savings to go elsewhere? Or just reducing total spend?"
- WHEN: "Immediate impact, but review in 1 week to see reallocation effects"
- SUCCESS: "Budget reallocated successfully? Overall account performance maintained?"

### The Client Context

Pull from CONTEXT.md:
- Known ROAS targets or benchmarks
- Typical performance levels
- Seasonal patterns
- Recent experiments and their outcomes

### The Time of Year

- Q4: Holiday shopping, end-of-year budget spend
- January: New year, budget resets, often slow period
- Summer: Seasonal changes for many clients
- Month-end: Budget pacing adjustments

---

## Integration with Client CONTEXT.md

### When to Also Update CONTEXT.md

Update client CONTEXT.md when experiments are:
- **Strategic** (not just tactical adjustments)
- **Significant** (major budget changes, campaign launches)
- **Learning opportunities** (testing hypotheses)
- **Structural** (account reorganization, new campaign types)

### What to Add to CONTEXT.md

Add to relevant sections:
- **Strategic Context**: Major strategic shifts
- **Campaign Notes**: Campaign-specific experiments
- **Key Learnings**: After reviewing outcomes
- **Planned Work**: Upcoming experiments flagged for execution

---

## Review Process

### Checking Experiment Outcomes

1. Filter CSV for client and date range
2. Look for experiments with WHEN dates that have passed
3. Compare WHAT (expected) vs actual performance data
4. Document learnings in client CONTEXT.md
5. Use insights to inform future experiments

### Example Review

**Experiment (Nov 1):**
```
Increased Shopping budget £150 → £200

WHY: Q4 demand surge, strong performance
WHAT: Expecting 30-40% revenue increase, ROAS 400%+
WHEN: Review Nov 8
SUCCESS: Revenue £280+/day, ROAS 400%+
```

**Review (Nov 8):**
```
ACTUAL: Revenue increased to £265/day (+33%), ROAS 420%
OUTCOME: ✓ Success - Hit revenue target, exceeded ROAS target
LEARNING: Q4 performance strong, shopping campaign can handle higher budgets
while maintaining efficiency. Consider further increases if inventory supports.
```

**Update CONTEXT.md:**
Add to "Key Learnings":
> Nov 8, 2025: Q4 Shopping budget increase successful. Budget scaled from £150 to
> £200/day with revenue increase from £200 to £265/day (+33%) and ROAS improving
> from 400% to 420%. Demonstrates campaign efficiency at higher spend levels during
> Q4. (Ref: Experiment logged Nov 1, reviewed Nov 8)

---

## Common Mistakes to Avoid

### ❌ DON'T: Log without asking

**Bad:**
```
User: "I increased the budget to £200"
Claude: *Immediately adds to CSV without asking WHY/WHAT/WHEN/SUCCESS*
```

**Good:**
```
User: "I increased the budget to £200"
Claude: "Got it! Before I log this, let me grab a few quick details to help us
track the impact. Was this budget increase driven by strong performance you want
to scale, or are you hitting impression share caps? And what are you expecting
to see - proportional revenue increase while maintaining ROAS?"
```

### ❌ DON'T: Assume you know the reasoning

Even if the change seems obvious, ask. The user's actual reasoning may differ from your assumptions.

### ❌ DON'T: Wait for perfect, complete answers

Brief answers are fine. Your job is to format them properly.

### ❌ DON'T: Skip experiments for "small" changes

If the user explicitly asks you to log something, it's worth logging regardless of size.

---

## File Location

**Experiment Log:** `roksys/spreadsheets/rok-experiments-client-notes.csv`

**Auto-sync:** Updated every 6 hours from [ROK | Experiments Google Sheet](https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/)

**Export Script:** `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`

---

## Complete Example Interaction

### User Request:
> "I've paused the Display campaign for Bright Minds. Can you log that?"

### Claude Response:
> "Sure! I can see you've paused the Display campaign. Before I log this, let me
> grab a couple of quick details to help us track the impact:
>
> - What was driving this decision? Was it performance-related, or are you
>   reallocating budget to Shopping/Search which have been performing well?
> - What are you expecting to see? I'm guessing the Display budget will either
>   reduce overall spend, or get reallocated to other campaigns?
> - When should we check back on this - maybe 1 week to see how the account
>   adjusted?
> - What would make this a success - maintaining or improving overall account
>   performance without Display?"

### User Response:
> "Yeah, Display wasn't performing. ROAS was 180% vs 450% on Shopping. Want to
> focus budget on what's working. Check in a week. Success is overall ROAS goes
> up."

### Claude Action:

1. **Logs to CSV:**
```csv
2025-11-05 15:45:00,Bright Minds,"Paused Display campaign

WHY: Display underperforming at 180% ROAS vs Shopping at 450% ROAS, reallocating budget to higher-performing campaigns
WHAT: Expecting overall account ROAS to improve, Display budget to reallocate to Shopping/Search
WHEN: Review Nov 12 (1 week after pause)
SUCCESS: Overall account ROAS improves above current baseline, Shopping/Search scale without efficiency loss",display,budget-reallocation,roas-optimization
```

2. **Confirms:**
> "Logged! I've added this to the experiment tracker with all the details. We'll
> review on Nov 12 to see if overall ROAS improved and whether Shopping/Search
> successfully absorbed the budget. I've also tagged it with 'display',
> 'budget-reallocation', and 'roas-optimization' so we can easily find similar
> experiments later."

3. **Optionally Updates CONTEXT.md** (if strategic):
Add to "Campaign Notes":
> Nov 5, 2025: Paused Display campaign due to underperformance (180% ROAS vs 450%
> on Shopping). Reallocating budget to higher-performing campaigns. Review Nov 12.

---

**Remember:** The goal is to build institutional knowledge. Every logged experiment helps future you (and future Claude instances) understand what was tried, why, and what worked.
