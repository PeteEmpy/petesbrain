# ROK Methodologies - Strategy Experiment System

**Created:** Oct 31, 2025
**Purpose:** Track, evaluate, and scale successful Google Ads strategies across all client accounts

---

## Overview

This system ensures **every strategic change is logged with complete information**, evaluated with data, and successful patterns are **replicated across accounts**.

**The Problem It Solves:**
- Experiments get forgotten or never evaluated
- Learnings aren't documented or shared
- Successful strategies stay siloed to one account
- Failed tests get repeated because nobody remembers

**The Solution:**
- Structured experiment logging (5 essential questions)
- Data-driven impact analysis (actual vs expected)
- Strategy Playbook (proven wins and failures)
- Rollout framework (scale successful tests)

---

## Quick Start

### When You Make a Strategic Change

**Just tell Claude what you're doing:**
- "I'm creating a standalone PMax campaign for Smythson diaries"
- "I'm reducing the UK ROAS target from 4.3 to 3.8"
- "I'm splitting out the travel bags asset group"

**Claude will prompt you with 5 questions:**
1. What are you changing? (be specific)
2. Why? (strategic reasoning)
3. What do you expect? (hypothesis with numbers)
4. When should we review? (timeline)
5. What would success look like? (success criteria)

**Then Claude will:**
- Log it in ROK Experiments sheet
- Add to client CONTEXT.md
- Create review task for timeline specified
- Track everything automatically

---

## When Review Time Comes

**Just say:** "Review the [experiment name]"

**Claude will:**
1. Pull Google Ads performance data (before vs after)
2. Check change history (confirm what changed)
3. Calculate impact (actual vs expected)
4. Present results with recommendation
5. Ask if you want to roll out to other accounts

**You decide:**
- ✅ Roll out (create tasks for other accounts)
- ⚠️ Needs more time (extend monitoring)
- 🔄 Iterate (modify and retest)
- ❌ Revert (document as failed test)

---

## The Core Documents

### 1. [Product Hero Labelizer System](product-hero-labelizer-system.md) ⭐ FOUNDATIONAL
**What:** Product segmentation framework (Heroes, Sidekicks, Villains, Zombies)
**Use:** Foundation for all e-commerce campaign structures
**Status:** Implemented across all ROK e-commerce clients

**Core Concept:**
- Heroes: Top 10% generating 80%+ revenue
- Sidekicks: Strong converters needing visibility
- Villains: Budget drainers with no conversions
- Zombies: Dormant products to test/activate

**Critical:** Understanding this framework is essential for analyzing any e-commerce client performance.

---

### 2. [Strategy Playbook](strategy-playbook.md)
**What:** Library of proven wins, failed tests, and reusable patterns
**Use:** Check before implementing a strategy (has this been tested?)
**Updated:** After each experiment completes

**Sections:**
- Proven Wins (ready to roll out)
- Tests in Progress (currently monitoring)
- Failed Tests (avoid repeating)
- Strategy Patterns Library (when to use each pattern)

---

### 3. [Experiment Logging Guide](experiment-logging-guide.md)
**What:** How to log experiments with complete information
**Use:** Reference for the 5 essential questions
**Key:** Ensures data quality at entry time (not guesswork later)

**The 5 Questions:**
1. What? (1 sentence, specific)
2. Why? (strategic reasoning)
3. Expected? (hypothesis with numbers)
4. When? (review timeline)
5. Success? (how we'll know it worked)

---

### 4. [Impact Analysis Workflow](impact-analysis-workflow.md)
**What:** Step-by-step process for evaluating experiments
**Use:** Review experiments at timeline milestone
**Automated:** Claude does data pulling and calculations

**Process:**
1. Data Collection (Google Ads + Context)
2. Impact Calculation (actual vs expected)
3. Results Presentation (formatted report)
4. Decision Making (your choice)
5. Documentation (update all systems)

---

### 5. Client CONTEXT.md - Strategy Experiments Log
**What:** Client-specific experiment tracking
**Use:** See what's been tested on each account
**Location:** `clients/[client-name]/CONTEXT.md`

**Sections:**
- Active Tests (currently monitoring)
- Completed Tests (with results)
- Proven Winners (rolled from other accounts)

---

## How It All Works Together

```
┌─────────────────────────────────────────────────────────────┐
│                   YOU MAKE A CHANGE                         │
│  "I'm creating a standalone PMax campaign for diaries"     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CLAUDE PROMPTS 5 QUESTIONS                     │
│  What? Why? Expected? When? Success criteria?              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 LOGGED IN 3 PLACES                          │
│  1. ROK Experiments Google Sheet                           │
│  2. Client CONTEXT.md (Active Tests)                       │
│  3. Review task created for timeline                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                   [14-28 days pass]
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  REVIEW DATE ARRIVES                        │
│  "Review the Diaries experiment"                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CLAUDE PULLS & ANALYZES DATA                   │
│  - Google Ads performance (before vs after)                │
│  - Change history (confirm changes)                        │
│  - Calculate impact (actual vs expected)                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               RESULTS PRESENTED TO YOU                      │
│  Success: +15% revenue (expected +10%) ✓                   │
│  Recommendation: Roll out to USA and EUR                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   YOU DECIDE                                │
│  ✅ Roll out  ⚠️ More time  🔄 Iterate  ❌ Revert         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              DOCUMENTED IN 4 PLACES                         │
│  1. Strategy Playbook (Proven Win)                         │
│  2. Client CONTEXT.md (Completed Tests)                    │
│  3. ROK Experiments Sheet (Actual Outcome)                 │
│  4. Rollout tasks created (USA, EUR)                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               PATTERN REUSED ACROSS ACCOUNTS                │
│  Proven strategy available for future implementations      │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration with Other ROK Systems

**Three complementary systems working together:**

### 1. Product Hero Labelizer (FOUNDATIONAL)
**Focus:** Product-level performance classification
**Output:** Daily-updated product labels (Heroes, Sidekicks, Villains, Zombies)
**Purpose:** Foundation for campaign structure decisions

**Examples:**
- Products automatically classified by performance
- Labels drive asset group segmentation
- Informs budget allocation strategies

---

### 2. Product Impact Analyzer
**Focus:** Tactical product-level changes
**Output:** Weekly reports on product performance changes

**Examples:**
- Product added/removed from catalog
- Price changes
- Stock issues
- Product disapprovals

---

### 3. Strategy Experiments System
**Focus:** Strategic account-level changes
**Output:** Proven strategies to replicate across accounts

**Examples:**
- Campaign structure changes
- Budget/ROAS adjustments
- New features/targeting
- Asset group strategies

---

**Together - Complete Performance Analysis:**

1. **Product Hero Labelizer** → Classifies products (what performs)
2. **Product Impact Analyzer** → Tracks catalog changes (what changed at product level)
3. **Strategy Experiments** → Tests structural changes (what you did strategically)

**Combined Answer:** Why performance changed and what to do next.

**Example Analysis:**
- Revenue dropped 15% on Oct 22
- **Labelizer:** Spike came from Sidekicks asset group
- **Product-level:** Specific products (Zuiver chairs, sideboards) drove spike
- **Label verification:** Products were labeled "heroes" and "villains" NOT "sidekicks"
- **Root cause:** Asset group filtering broken - wrong products served
- **Fix:** Add explicit product filters: `custom_label_0 = "sidekicks"`

---

## Monthly Workflow

**1st of Each Month:**

1. **Review Last Month's Experiments**
   - Check all experiments that completed
   - Update with actual results
   - Categorize: Success / Failure / Mixed

2. **Update Strategy Playbook**
   - Add proven wins
   - Document failures with learnings
   - Identify new patterns

3. **Identify Rollout Opportunities**
   - Which successful tests should scale?
   - Which accounts are good candidates?
   - Create rollout tasks

4. **Optional: Share Monthly Summary**
   - Email to team/clients
   - Show what was tested and learned
   - Demonstrate data-driven approach

---

## Key Principles

### 1. Log Everything at Entry Time
**Why:** Memory fades, details get lost
**How:** 5 essential questions when making change
**Result:** Complete data for future analysis

### 2. Quantify Expectations
**Why:** "Improve performance" isn't measurable
**How:** Hypothesis with numbers (+10% revenue, ROAS 4.0+)
**Result:** Clear success/failure criteria

### 3. Review on Schedule
**Why:** Experiments never get evaluated without timeline
**How:** Set review date when logging, create task
**Result:** All tests evaluated with data

### 4. Document Everything
**Why:** Institutional knowledge, avoid repeating mistakes
**How:** Update Playbook, CONTEXT.md, Experiments sheet
**Result:** Searchable library of proven patterns

### 5. Scale Successes
**Why:** Winning strategies should spread, not stay siloed
**How:** Identify rollout candidates, create tasks
**Result:** Efficiency gains across all accounts

---

## Examples

### Proven Win: Product-Specific PMax Campaigns
**Tested:** Smythson UK - Diaries (Oct 2025)
**Result:** +15% revenue, ROAS 4.2 (vs 3.8 blended)
**Rolled Out:** Smythson USA, Smythson EUR
**Pattern:** When product has distinct seasonality and >15% of revenue

### Failed Test: Blanket ROAS Reduction
**Proposed:** Smythson - 15% ROAS cut across all campaigns
**Why Failed:** Ignores regional differences (UK 4.3 vs USA 2.5)
**Better Alternative:** Regional ROAS targets based on market maturity
**Learning:** Segment by performance before blanket changes

### Category Asset Groups
**Tested:** Smythson UK - 5 category-specific asset groups
**Status:** Monitoring (review Nov 11)
**Expected:** Higher-margin categories outperform blended average
**If Successful:** Roll out to other multi-category e-commerce clients

---

## FAQs

**Q: What if I forget to log an experiment?**
A: Log it retroactively. Better late than never. Include what you remember about why you made the change.

**Q: What if results are mixed?**
A: That's valuable learning! Document what worked and what didn't. Consider iterating with modifications.

**Q: How do I know when to roll out a strategy?**
A: Clear wins (met all success criteria) = roll out. Mixed results = iterate first. Failures = document and avoid.

**Q: Do I have to log every tiny change?**
A: No. Focus on strategic changes: campaign structure, budget shifts, ROAS adjustments, new features. Not minor bid tweaks or keyword additions.

**Q: What if an experiment is interrupted?**
A: Note the interruption (e.g., "paused for stock issues"). Either extend timeline or document as "incomplete - inconclusive."

**Q: How long should I keep failed tests in the Playbook?**
A: Indefinitely. Failed tests are valuable learning to prevent repeating mistakes. Tag them clearly so they're easy to reference.

---

## File Structure

```
roksys/knowledge-base/rok-methodologies/
├── README.md (this file - overview of all ROK methodologies)
├── product-hero-labelizer-system.md (FOUNDATIONAL - Heroes/Sidekicks/Villains/Zombies)
├── strategy-playbook.md (proven wins, failures, patterns)
├── experiment-logging-guide.md (5 questions, best practices)
└── impact-analysis-workflow.md (review process, automation)

clients/[client-name]/
└── CONTEXT.md (includes Strategy Experiments Log section)

roksys/spreadsheets/
└── rok-experiments-client-notes.csv (synced from Google Sheet)
```

---

## Next Steps

1. **Start using it:** Next time you make a strategic change, log it properly
2. **Review your first experiment:** Pick one recent change and do a full impact analysis
3. **Build the Playbook:** As experiments complete, add patterns to Strategy Playbook
4. **Scale wins:** Identify successful strategies to roll out to other accounts

---

*This system turns your experimentation into institutional knowledge and scales successful strategies across all accounts.*
