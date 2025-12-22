# Session Continuity System

**Status:** Active (Implemented: 2025-12-22)
**Purpose:** Transform AI from amnesiac assistant to genuine partner through systematic context capture and reintroduction

---

## Overview

The Session Continuity System solves the fundamental problem of AI memory: **every conversation starts from zero unless you deliberately maintain continuity**.

Without continuity:
- You repeat yourself constantly
- AI can't build on previous analyses
- Decisions get forgotten and re-litigated
- Knowledge doesn't accumulate

With continuity:
- AI knows what you decided last time
- Analyses build on each other
- Decisions stay made
- Knowledge compounds over time

**Key insight:** "Continuity is a practice, not a technology." (Mike Rhodes, 8020brain.com)

---

## System Components

### 1. Session Log (`session-log.md`)

**Location:** `clients/{client}/session-log.md`

**Purpose:** Conversation handoffs - end each session with a summary that briefs the next session

**Format:**
```markdown
## Session: YYYY-MM-DD (Brief Topic Description)

**Analysed:**
- What data/campaigns/issues we examined
- What patterns or insights emerged

**Decided:**
- Actions taken (budget changes, bid adjustments, pauses, etc.)
- Strategic decisions made
- Experiments launched

**Still investigating:**
- Open questions that need more data
- Issues requiring follow-up
- Hypotheses to test

**Next session:**
- What to check/review next time
- Expected outcomes to verify
- Follow-up analyses needed
```

**When to update:**
- After every significant work session (30+ minutes)
- After making important decisions
- After launching experiments or major changes
- After discovering unexpected patterns

**Effort:** 2 minutes per session
**Impact:** Eliminates "wait, what did we decide last time?" problem

---

### 2. Open Questions (`open-questions.md`)

**Location:** `clients/{client}/open-questions.md`

**Purpose:** Track unresolved questions, patterns to investigate, curiosities that aren't urgent enough for tasks but important to remember

**Format:**
```markdown
**Question:** [Clear, specific question]
**Noticed:** YYYY-MM-DD
**Context:** [What triggered this question? What were you looking at?]
**Hypothesis:** [Your initial theory about why/what's happening]
**Need:** [What data/time/analysis would resolve this?]
**Priority:** [High/Medium/Low - how important is this to understand?]
**Status:** [Open/Investigating/Resolved]
```

**When to add questions:**
- When you notice an interesting pattern but don't have time to investigate
- When you discover something that needs more data to understand
- When you have a hypothesis that requires time to test
- When you spot anomalies that aren't urgent but worth tracking

**When to resolve questions:**
- When you gather the needed data
- When time reveals the pattern (e.g., seasonality)
- When you run the analysis that answers the question
- Move to "Resolved Questions" section with the answer

**Difference from tasks:**
- Tasks = actionable work with deadlines
- Open questions = curiosity without urgency

---

### 3. Context Briefing (`/client` command)

**Usage:** `/client <client-name>`

**Purpose:** Start every session with full context - load strategic overview, last session summary, open questions, and active tasks

**Output format:**
```
🟢 [Client Name] - Context Briefing
==========================================

## ✓ Strategic Context
- Account structure, targets, current focus, budget

## ✓ Last Session Summary
- Date, topic, key decisions, open items

## ✓ Open Questions (count)
- Active questions by priority

## ✓ Active Tasks (count)
- P0/P1 tasks (P2/P3 on request)

---

**Ready to work on [Client Name]. What would you like to do?**
```

**When to use:**
- At the start of EVERY client work session
- Before weekly performance reviews
- Before making strategic decisions
- After time away from a client (1+ weeks)

**Effort:** 60 seconds to load + read
**Impact:** Never start from zero - always have full context

---

## The Five Practices (Mike Rhodes Framework)

### 1. Conversation Handoffs

**Practice:** End each session with a summary of what was discussed and decided

**Implementation:** Update `session-log.md` after every significant session

**Example:**
```markdown
## Session: 2025-12-20 (Shopping Campaign Optimisation)

**Analysed:**
- Shopping campaign structure (5 campaigns, 3 product groups)
- Product performance by margin tier
- Bidding strategy effectiveness

**Decided:**
- Pause low-margin products in "All Products" campaign
- Create dedicated campaign for high-margin leather goods
- Increase bids 20% on Panama collection

**Still investigating:**
- Why "Travel" category ROAS dropped from 450% to 280%

**Next session:**
- Check Travel category performance after 7 days
- Review new campaign structure results
```

---

### 2. Starting With Context

**Practice:** Begin conversations by providing the handoff from last time

**Implementation:** Run `/client <client-name>` at the start of every session

**Example workflow:**

```
You: /client smythson

Claude: [Loads full briefing including last session]

🟢 Smythson - Context Briefing
==========================================

## ✓ Last Session Summary

**Date:** 2025-12-20 (Shopping campaign optimisation)

**Decided:**
- Paused low-margin products
- Created dedicated leather goods campaign

**Still investigating:**
- Travel category ROAS drop (450% → 280%)

You: "Let's check if Travel category recovered"
```

**This picks up exactly where you left off** - no need to remember or re-explain context.

---

### 3. Open Questions Tracking

**Practice:** Maintain a list of unresolved questions

**Implementation:** Add to `open-questions.md` as curiosities emerge

**Example:**

During weekly review, you notice: "Smythson's mobile ROAS is 50% lower than desktop"

Not urgent enough for a task, but worth understanding.

Add to `open-questions.md`:
```markdown
**Question:** Why is mobile ROAS 50% lower than desktop?
**Noticed:** 2025-12-22
**Context:** Weekly performance review, consistent pattern for 4 weeks
**Hypothesis:** Mobile users researching, converting later on desktop?
**Need:** Cross-device attribution analysis
**Priority:** Medium
**Status:** Open
```

Next time you have capacity for deep analysis, consult open-questions.md and investigate.

When resolved, move to "Resolved Questions" section:
```markdown
**Question:** Why is mobile ROAS 50% lower than desktop?
**Resolution:** Cross-device attribution confirmed - 60% of mobile clicks lead to desktop conversions within 7 days
**Resolved:** 2025-12-29
**Action taken:** Adjusted mobile bid modifier to +30% to account for assist value
```

---

### 4. History References

**Practice:** Point AI to past analyses and create explicit connections

**Implementation:** Reference `tasks-completed.md`, `reports/`, and `session-log.md` when making decisions

**Example:**

You're considering: "Should we increase bids on Smythson's Panama collection?"

**Before deciding, check history:**

```bash
grep -r "Panama" clients/smythson/tasks-completed.md
grep -r "increased bids" clients/smythson/session-log.md
```

Find: "2025-10-15: Increased Panama bids 25%, ROAS dropped from 420% to 360%, reversed after 10 days"

**Now you can reference this history explicitly:**

```
You: "Should we increase bids on Panama collection?"

Claude: [Checks history]

"⚠️ Historical context: We tested this in October 2025.

**What happened:**
- Increased bids 25%
- ROAS dropped 60 points (420% → 360%)
- Reversed after 10 days

**Why it failed:**
- Strong organic demand
- Higher bids drove lower-intent clicks
- Conversion rate dropped 15%

**Recommendation:** Don't repeat the same experiment.

**Alternative:** Test increased bids ONLY on high-intent keywords"
```

**This prevents repeating failed experiments** and builds institutional memory.

---

### 5. Building on Previous Work

**Practice:** Treat sessions as chapters in an ongoing story, not isolated events

**Implementation:** Each session explicitly references and builds on the last

**Example progression:**

**Month 1 (October):**
```markdown
## Session: 2025-10-15 (Budget Analysis)

**Analysed:** Spend distribution across Devonshire campaigns

**Decided:** Reduced Chatsworth budget (overspending vs ROAS)

**Next session:** Monitor Chatsworth results
```

**Month 2 (November):**
```markdown
## Session: 2025-11-12 (Budget Optimisation)

**Context:** Following up on Chatsworth budget reduction (Oct 15)

**Analysed:**
- Chatsworth ROAS improved from 320% to 380% (60 points)
- Applied same logic to Cavendish (similar pattern)

**Decided:** Create budget rebalancing framework for all properties

**Next session:** Review entire portfolio with new framework
```

**Month 3 (December):**
```markdown
## Session: 2025-12-10 (Portfolio Optimisation)

**Context:** Applying budget framework created Nov 12

**Analysed:** All 8 properties using rebalancing framework

**Decided:**
- Identified 3 more over-budget campaigns
- Automated budget checks via Python script

**Impact:** Turned single campaign fix into systematic solution
```

**This is compounding knowledge:**
- Month 1: Fix one issue
- Month 2: Generalise the pattern
- Month 3: Systematise the solution

**Without continuity**, you'd fix Chatsworth in October, forget about it, and discover the same issue with Cavendish in March.

**With continuity**, you systematise the solution and prevent future occurrences.

---

## Workflow Integration

### Starting a Client Work Session

**Step 1:** Load context
```
/client smythson
```

**Step 2:** Read the briefing (60 seconds)
- Strategic context
- Last session summary
- Open questions
- Active tasks

**Step 3:** Decide what to work on based on context
- Follow up on "Next session" items from last time
- Check "Still investigating" items
- Address P0/P1 tasks
- Or investigate an open question

**Step 4:** Do the work

**Step 5:** Update session-log.md (2 minutes)
- What you analysed
- What you decided
- What's still being investigated
- What to check next session

**Total overhead:** 3 minutes (60s to load context + 2 min to update log)
**Value:** Infinite (never lose context, decisions compound over time)

---

### During Work Sessions

**When you notice something interesting but non-urgent:**

Add to `open-questions.md`:
```markdown
**Question:** [What you noticed]
**Noticed:** [Today's date]
**Context:** [What triggered this]
**Hypothesis:** [Your initial theory]
**Need:** [What would resolve this]
**Priority:** [High/Medium/Low]
**Status:** Open
```

**When you reference past decisions:**

Search relevant files:
```bash
# Search tasks archive
grep -r "keyword" clients/smythson/tasks-completed.md

# Search session logs
grep -r "budget" clients/smythson/session-log.md

# Search reports
grep -r "ROAS" clients/smythson/reports/
```

**When you make important decisions:**

Add note to current session entry (you'll formalise at end of session)

---

### Ending a Client Work Session

**Mandatory:** Update `session-log.md`

**Template:**
```markdown
## Session: YYYY-MM-DD (Brief Topic)

**Analysed:**
- [What you examined]

**Decided:**
- [Actions taken]
- [Experiments launched]

**Still investigating:**
- [Open items]

**Next session:**
- [What to check next time]
```

**Time:** 2 minutes
**Frequency:** After every significant session (30+ minutes of work)

---

## Examples

### Example 1: Weekly Performance Review With Continuity

**Without continuity (old approach):**
```
You: "Run weekly report for Smythson"
Claude: *Generates report with this week's data*
You: *Read report, make mental notes*
```

**With continuity (new approach):**
```
You: /client smythson

Claude: [Loads briefing showing last week's decisions]

## ✓ Last Session Summary
**Date:** 2025-12-15 (Shopping optimisation)
**Decided:** Paused low-margin products, created leather goods campaign
**Still investigating:** Travel category ROAS drop

You: "Run weekly report for Smythson"

Claude: [Generates report WITH callbacks to last week]

## Week-Over-Week Changes

**ROAS:** 420% → 385% (-35 points)
- **Context:** Last week we paused low-margin products
- **Expected:** Short-term ROAS dip as new campaign ramps
- **Status:** On track (leather goods campaign: 450% ROAS)

**Travel Category ROAS:** 280% (unchanged)
- **Context:** Open question from Dec 15 - still investigating
- **Recommendation:** Schedule deep-dive session this week
```

**See the difference?** The report builds on previous analysis instead of treating every week as independent.

---

### Example 2: Campaign Optimisation With History References

**Without continuity:**
```
You: "Should we increase bids on Panama collection?"
Claude: *Analyses current data, makes recommendation*
```

**With continuity:**
```
You: "Should we increase bids on Panama collection?"

Claude: [Checks session-log.md and tasks-completed.md]

"⚠️ Historical context: We tested this in October 2025.

**What happened:**
- Increased bids 25%
- ROAS dropped 60 points
- Reversed after 10 days

**Why it failed:**
- Strong organic demand meant higher bids drove lower-intent traffic
- Conversion rate dropped 15%

**Recommendation:** Don't repeat the same experiment

**Alternative:** Test increased bids ONLY on high-intent keywords
(e.g., 'panama leather diary' vs 'panama collection')"
```

**This is the power of history references** - you don't waste time repeating failed experiments.

---

### Example 3: Building on Previous Work Across Months

**Scenario:** Optimising Devonshire Hotels budget allocation over 3 months

**October session:**
```markdown
## Session: 2025-10-15 (Budget Analysis)

**Analysed:** Spend distribution across all campaigns

**Decided:**
- Identified Chatsworth overspending (15% above target)
- Reduced daily budget from £45 to £38

**Still investigating:** Whether other properties have similar issues

**Next session:** Monitor Chatsworth results after 7 days
```

**November session:**
```markdown
## Session: 2025-11-12 (Budget Pattern Recognition)

**Context:** Following up on Chatsworth budget reduction (Oct 15 session)

**Analysed:**
- Chatsworth ROAS improved from 320% to 380% (+60 points) ✅
- Reviewed other properties for similar pattern
- Found Cavendish also overspending

**Decided:**
- Applied same logic to Cavendish (reduced £50 → £43)
- Created budget rebalancing framework document

**Still investigating:** Portfolio-wide systematic approach

**Next session:** Apply framework to entire portfolio
```

**December session:**
```markdown
## Session: 2025-12-10 (Portfolio-Wide Optimisation)

**Context:** Applying budget framework from Nov 12 session

**Analysed:** All 8 properties using rebalancing framework

**Decided:**
- Identified 3 more over-budget campaigns
- Implemented budget adjustments
- Created automated budget monitoring script (checks weekly)

**Impact:**
- Month 1: Fixed one campaign
- Month 2: Generalised the pattern
- Month 3: Systematised the solution ✅

**Next session:** Monitor automated script results
```

**This is compounding knowledge** - each month builds on the last, eventually creating systematic solutions.

---

## File Structure

```
clients/
├── smythson/
│   ├── CONTEXT.md                 # Strategic context (permanent)
│   ├── session-log.md             # Session summaries (append only)
│   ├── open-questions.md          # Unresolved questions (living document)
│   ├── tasks.json                 # Active tasks (daily management)
│   ├── tasks-completed.md         # Completed tasks archive (permanent)
│   ├── reports/                   # Weekly/monthly reports (historical)
│   └── ...
├── tree2mydoor/
│   ├── CONTEXT.md
│   ├── session-log.md
│   ├── open-questions.md
│   └── ...
└── ...
```

**Key files for session continuity:**
1. `session-log.md` - Conversation handoffs
2. `open-questions.md` - Curiosity tracking
3. `CONTEXT.md` - Strategic context (read via `/client`)
4. `tasks-completed.md` - Historical decisions (searchable archive)

---

## Best Practices

### DO:

✅ **Update session-log.md after every significant session** (30+ minutes)
✅ **Start every session with `/client <name>`** to load context
✅ **Add open questions as they emerge** - don't wait
✅ **Reference history explicitly** when making decisions
✅ **Keep session summaries concise** (bullet points, not essays)
✅ **Move resolved questions to "Resolved" section** with the answer
✅ **Search archives before repeating analyses** (grep is your friend)

### DON'T:

❌ **Don't skip session summaries** ("I'll remember" = you won't)
❌ **Don't start work without loading context** (defeats the purpose)
❌ **Don't create tasks for every open question** (use open-questions.md)
❌ **Don't forget to document decisions** (future you needs this)
❌ **Don't write novels in session-log.md** (brief summaries only)
❌ **Don't lose track of "Still investigating" items** (follow up next session)

---

## Maintenance

### Weekly:
- Review open-questions.md and resolve any questions you now have answers to
- Check that all significant sessions from the week have session-log.md entries

### Monthly:
- Archive very old session-log.md entries (keep last 3 months easily accessible)
- Review resolved questions for patterns (can inform playbooks)

### Quarterly:
- Review session-log.md for strategic patterns across clients
- Create playbooks from repeated successful approaches
- Update CONTEXT.md if strategic priorities have shifted

---

## Integration With Existing Systems

### Relationship to Other Files

| File | Purpose | Relationship to Session Continuity |
|------|---------|-----------------------------------|
| `CONTEXT.md` | Strategic context | Loaded by `/client` command, referenced in session-log.md |
| `tasks.json` | Active tasks | Shown in briefing, decisions logged to session-log.md |
| `tasks-completed.md` | Task archive | Historical reference for session-log.md |
| `reports/` | Weekly/monthly reports | Build on session-log.md summaries |
| `meeting-notes/` | Client conversations | Referenced in session-log.md decisions |

### Workflow Integration

**Daily Intel Report** (7 AM email):
- Could be enhanced to include "Last session summary" from session-log.md
- Could flag open questions that have aged (noticed >30 days ago)

**Weekly Reports** (google-ads-weekly-report skill):
- Already builds on previous analysis
- Could explicitly reference session-log.md for context

**Task Creation**:
- When creating tasks from analysis, note in session-log.md
- When completing tasks, note key outcomes in session-log.md

---

## Success Metrics

**You'll know the system is working when:**

1. **You never ask "wait, what did we decide about X?"**
   - All decisions logged in session-log.md

2. **AI references past analyses without prompting**
   - History is searchable and referenceable

3. **You stop repeating failed experiments**
   - Historical context prevents re-testing known failures

4. **Analyses build on each other across months**
   - Each session compounds on previous work

5. **Open questions get resolved over time**
   - Curiosity tracked → investigated → answered

6. **You can onboard new team members instantly**
   - Full client history in session-log.md + open-questions.md

---

## Troubleshooting

### "I forgot to update session-log.md after my last session"

**Solution:** Update it now from memory, mark as "[Retroactive]"

```markdown
## Session: 2025-12-20 (Shopping optimisation) [Retroactive: Added 2025-12-22]

**Analysed:**
- [What you remember]

**Decided:**
- [Key decisions you recall]
```

**Prevention:** Set calendar reminder or add to end-of-session checklist

---

### "My session-log.md is getting too long"

**Solution:** Archive old entries

Create `session-log-archive-2025.md` and move entries older than 3 months.

Keep session-log.md focused on recent context (last 3 months).

---

### "I don't know if something should be a task or an open question"

**Decision tree:**

Is it actionable right now? → **Task**
Does it have a deadline? → **Task**
Is it urgent or important? → **Task**

Is it interesting but not urgent? → **Open Question**
Does it need more data/time to understand? → **Open Question**
Is it curiosity without clear action? → **Open Question**

---

### "How detailed should session summaries be?"

**Rule of thumb:** Bullet points, not paragraphs

**Good:**
```markdown
**Analysed:**
- Shopping campaign structure (5 campaigns, 3 product groups)
- Product performance by margin tier

**Decided:**
- Paused low-margin products
- Created leather goods campaign
```

**Too brief:**
```markdown
**Analysed:** Campaigns
**Decided:** Made changes
```

**Too detailed:**
```markdown
**Analysed:**
First, I examined the Shopping campaign structure in detail. I found that there were 5 campaigns running, and within those campaigns there were 3 different product groups organized by margin tier. I looked at the performance data for each product group, examining ROAS, conversion rate, and spend levels. I noticed that the low-margin products were consuming budget but not delivering proportional returns...

[200 more words]
```

**Sweet spot:** Enough detail that future-you understands the context, but brief enough to scan in 30 seconds.

---

## Setup & Installation

### Initial Setup (Already Complete)

All clients now have:
- ✅ `session-log.md` template
- ✅ `open-questions.md` template
- ✅ `/client` command updated for full briefings

### For New Clients

When adding a new client, the setup script creates both files automatically:

```bash
python3 setup-session-continuity.py
```

Or manually create from templates in any existing client folder.

---

## Further Reading

**Internal Documentation:**
- `/Users/administrator/Documents/PetesBrain/docs/INTERNAL-TASK-SYSTEM.md` - Task management
- `/Users/administrator/Documents/PetesBrain/docs/ADDING-A-NEW-CLIENT.md` - Client onboarding
- `/Users/administrator/Documents/PetesBrain.nosync/.claude/CLAUDE.md` - Global instructions

**External Resources:**
- Mike Rhodes' 8020brain.com - "Session Continuity" concept from Ads to AI Skill Map (Phase 4: Business Context)

---

## Version History

**Version 1.0** (2025-12-22):
- Initial implementation across all 20 client folders
- Created `session-log.md` and `open-questions.md` templates
- Updated `/client` command for full briefings
- Created setup automation script

---

**The goal:** Transform AI from amnesiac assistant to genuine partner through systematic context capture and reintroduction.

**The practice:** Capture (session-log.md), Store (open-questions.md), Reintroduce (/client command)

**The result:** Knowledge that compounds over time, decisions that build on history, AI that gets smarter every week.
