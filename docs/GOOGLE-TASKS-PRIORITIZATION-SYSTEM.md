# Google Tasks Prioritization System
**Created**: 2025-11-06
**Purpose**: Systematic framework for prioritizing and managing tasks in Google Tasks

---

## Current State Analysis

**Total Tasks in Peter's List**: 79 incomplete tasks (as of 2025-11-06)

**Task Categories Identified**:
- **Client Work**: Bright Minds (8), Smythson (24), Tree2mydoor (3), Devonshire (4), Crowd Control (2), Godshot (1)
- **Project Work**: Claude Code setup, Product Hero rollout, MCP documentation
- **Personal**: Testosterone prescription, vitamins, VeloViewer, bank statements
- **Wispr Flow Notes**: 8 voice capture tasks (mix of work/personal)
- **Recurring**: Smythson Teams chat updates (8 recurring instances)
- **System/Admin**: Shared drive scan, task validation tests

**Problem**: No clear system for deciding what to work on each day

---

## Prioritization Framework

### **The ROK Priority Matrix**

Every task gets classified on TWO dimensions:

#### **Dimension 1: URGENCY** (Time Sensitivity)
- 🔴 **CRITICAL**: Must be done today (blocking, deadline today, client emergency)
- 🟡 **HIGH**: Should be done this week (upcoming deadline, client expecting)
- 🟢 **MEDIUM**: Next 2 weeks (planned work, no immediate pressure)
- ⚪ **LOW**: Someday/maybe (no deadline, nice to have)

#### **Dimension 2: IMPACT** (Business Value)
- 💰 **REVENUE**: Directly generates/protects revenue (client work, conversion fixes)
- 📊 **EFFICIENCY**: Saves significant time/reduces friction (automation, tools)
- 🎯 **STRATEGIC**: Long-term value (learning, relationships, positioning)
- 🔧 **MAINTENANCE**: Keeps things running (cleanup, admin, recurring tasks)

### **The Priority Score**

Combine urgency + impact to get priority:

| Urgency | Revenue | Efficiency | Strategic | Maintenance |
|---------|---------|------------|-----------|-------------|
| 🔴 CRITICAL | **P0** | **P1** | **P1** | **P2** |
| 🟡 HIGH | **P1** | **P2** | **P2** | **P3** |
| 🟢 MEDIUM | **P2** | **P3** | **P3** | **P4** |
| ⚪ LOW | **P3** | **P4** | **P4** | **P5** |

**Priority Definitions**:
- **P0**: Drop everything, do now (1-3 per week maximum)
- **P1**: Today's focus work (3-5 per day)
- **P2**: This week's planned work (10-15 per week)
- **P3**: Next week / buffer tasks (20-30 in queue)
- **P4**: Someday/maybe (unlimited, review monthly)
- **P5**: Consider deleting (stale, low value)

---

## Daily Workflow

### **Morning Routine (10 minutes)**

**Step 1: Review Today's Tasks**
```
Prompt: "Show me all tasks due today from Google Tasks, sorted by priority"
```

**Step 2: Identify P0/P1 Tasks**
```
Prompt: "Which of today's tasks are CRITICAL (P0) or HIGH PRIORITY (P1)?"
```

**Step 3: Create Today's Focus List**
- Select 3-5 tasks maximum for the day
- Must include all P0 tasks
- Fill remaining slots with P1 tasks
- Everything else goes to "tomorrow" or later

**Step 4: Time Block**
- Assign each task a time block
- P0 tasks: First thing in morning
- P1 tasks: Core working hours
- Buffer time: 20% for emergencies

### **End of Day Routine (5 minutes)**

**Step 1: Review Completion**
```
Prompt: "Mark these tasks complete in Google Tasks: [list]"
```

**Step 2: Reschedule Incomplete**
```
Prompt: "Reschedule incomplete P0/P1 tasks to tomorrow"
```

**Step 3: Plan Tomorrow**
```
Prompt: "What are my top 5 priorities for tomorrow?"
```

---

## Weekly Planning (30 minutes every Monday)

### **Step 1: Week Review (10 mins)**

```
Prompt: "Show me all tasks completed last week"
```

Celebrate wins, identify patterns, review time tracking

### **Step 2: Triage All Open Tasks (15 mins)**

```
Prompt: "List all incomplete tasks from Google Tasks, grouped by client/project"
```

For each task, ask:
1. **Is this still relevant?** (If no → Delete)
2. **What's the urgency?** (Critical/High/Medium/Low)
3. **What's the impact?** (Revenue/Efficiency/Strategic/Maintenance)
4. **When realistically?** (This week/Next week/This month/Someday)

Update due dates accordingly.

### **Step 3: This Week's Plan (5 mins)**

```
Prompt: "Show me all P0, P1, and P2 tasks due this week"
```

Sanity check:
- Do I have time for all P0/P1 tasks?
- Are P2 tasks realistic or should they move to next week?
- Any conflicts or dependencies?

---

## Task Categories: Special Handling

### **Client Work**

**Rule**: Client work always gets priority over internal work.

**Classification**:
- Client deadline/emergency = P0
- Client request this week = P1
- Client planned work = P2
- Client "nice to have" = P3

**Daily Limits**:
- Each client should have max 2-3 active tasks
- If more, consolidate or defer

### **Recurring Tasks**

**Rule**: Recurring tasks get assigned fixed priority.

**Examples**:
- Smythson Teams chat → **P3** (every 2 weeks, 15 mins)
- Monthly reports → **P1** (week before due)
- Shared drive scan → **P2** (first week of month)
- Product Impact Analyzer → **Automated** (not a task)

**Handling**:
- If recurring task builds up multiple instances → Consolidate to one
- If consistently not doing → Adjust recurrence or delete

### **Wispr Flow Voice Notes**

**Rule**: Process all voice notes weekly, not daily.

**Friday Afternoon Routine** (30 mins):
```
Prompt: "Show me all Wispr Flow tasks from this week"
```

For each note:
1. **Personal** → Handle immediately or add to personal todo
2. **Client** → Create proper client task with context
3. **Idea** → Add to knowledge base or Someday/Maybe
4. **Junk** → Delete

Delete the Wispr task after processing.

### **Personal Tasks**

**Rule**: Personal urgent tasks = P1, personal planning = P3

**Examples**:
- Prescription needed today = P1
- Vitamins order = P3 (do during admin time)
- Bank statements (deadline) = P1 on due date

**Handling**:
- Schedule personal P3 tasks for Friday afternoon "admin hour"
- Don't let personal P3s clog daily focus

---

## Task Naming Convention

**Format**: `[Client/Project] Action Verb - Specific Outcome - PRIORITY`

**Good Examples**:
- `[Bright Minds] Investigate GA4 Conversion Overlap - URGENT` ✅
- `[Smythson] Review UK ROAS Reduction Impact (Nov 15 Change)` ✅
- `[Devonshire] Complete Slide-by-Slide Review` ✅

**Bad Examples**:
- `20251106 065906 Wispr Personal Note For Today Order Some Magnesium` ❌ (too verbose, no context)
- `Update MCP server documentation` ❌ (too vague, no outcome)
- `New iPad task` ❌ (no information)

**Naming Rules**:
1. Start with [Client/Project] tag
2. Use action verb (Investigate, Review, Complete, Fix, etc.)
3. Be specific about the outcome
4. Keep under 80 characters if possible
5. Add priority tag if URGENT or time-sensitive

---

## Cleanup Protocols

### **Weekly Cleanup (Fridays, 15 mins)**

**Delete**:
- Completed tasks older than 30 days
- Stale Wispr notes (processed)
- Duplicate tasks
- "Test" tasks

**Archive**:
- Completed project milestones (document in CONTEXT.md first)
- Old recurring task instances (keep latest only)

**Consolidate**:
- Multiple similar tasks → One task with subtasks in notes
- Wispr voice notes → Proper structured tasks

### **Monthly Cleanup (First Monday, 30 mins)**

```
Prompt: "Show me all tasks with no due date"
```

For each:
- Assign a realistic due date OR
- Move to Someday/Maybe list OR
- Delete if no longer relevant

```
Prompt: "Show me all tasks due more than 4 weeks ago"
```

For each:
- Complete now (if quick) OR
- Reschedule realistically OR
- Delete if no longer relevant

---

## Implementation Plan (Tomorrow's Task)

### **Phase 1: Initial Cleanup (60 mins)**

**Step 1: Delete Obvious Junk (10 mins)**
- Test tasks
- Completed but not marked
- Irrelevant old tasks

**Step 2: Process Wispr Notes (15 mins)**
- Personal → Handle or schedule
- Client → Create proper task
- Ideas → Knowledge base
- Delete Wispr task

**Step 3: Consolidate Duplicates (10 mins)**
- Multiple Smythson Q4 milestones → One master task
- Recurring tasks → Keep latest instance only

**Step 4: Assign Due Dates to Everything (15 mins)**
- No task without a due date
- Be realistic with dates
- Use "Someday/Maybe" list for unclear timing

**Step 5: Rename Poor Task Names (10 mins)**
- Follow naming convention
- Add [Client] tags
- Make outcomes specific

### **Phase 2: Priority Assignment (30 mins)**

**Step 1: Client Tasks**
- Go through each client
- Assign urgency + impact
- Set realistic due dates

**Step 2: Project Tasks**
- Assess current projects
- Priority based on ROI
- Defer low-value work

**Step 3: Personal Tasks**
- Separate urgent from planning
- Schedule admin hour for P3 personal tasks

### **Phase 3: This Week's Plan (15 mins)**

**Today (Wednesday)**:
- P0: All Bright Minds URGENT tasks (3 tasks, ~55 mins)
- P1: 2-3 additional client tasks

**Thursday**:
- P1: Bright Minds THIS WEEK tasks
- P1: 1-2 Smythson Q4 milestone reviews
- P2: Start any Devonshire work

**Friday**:
- P2: Remaining client work
- P3: Personal admin hour
- P3: Wispr note processing
- Weekly cleanup

---

## Tools & Automation

### **Google Tasks Labels/Lists Strategy**

**Current Setup**: Single "Peter's List"

**Recommended**: Keep single list BUT use task prefixes

**Why**:
- Multiple lists = context switching
- Single list = everything in one place
- Prefixes = Easy filtering with search
- Due dates = Natural prioritization

### **Daily Focus View**

**Morning Command**:
```
Prompt: "Show me my top 5 priorities for today from Google Tasks"
```

**Claude Will**:
- Query Google Tasks API
- Filter by due date (today or overdue)
- Apply priority scoring
- Return top 5 with time estimates
- Suggest time blocks

### **Weekly Planning View**

**Monday Morning Command**:
```
Prompt: "Generate my weekly task plan"
```

**Claude Will**:
- Query all open tasks
- Group by client/project
- Calculate realistic capacity (5-6 hours/day)
- Suggest task distribution across week
- Identify overcommitments

### **Cleanup Command**

**Friday Afternoon Command**:
```
Prompt: "Run weekly task cleanup"
```

**Claude Will**:
- Identify stale tasks (>4 weeks old)
- Find tasks with no due date
- Consolidate Wispr notes
- Suggest deletions
- Archive completed work

---

## Success Metrics

### **Daily Success**

✅ **Good Day**:
- Completed all P0 tasks
- Completed 80%+ of P1 tasks
- No surprises/emergencies
- Clear plan for tomorrow

⚠️ **Review Needed**:
- P0 tasks incomplete
- <50% of P1 tasks done
- Constant firefighting
- Working on P3/P4 while P1 incomplete

### **Weekly Success**

✅ **Good Week**:
- All client deadlines met
- Major project milestones hit
- Task list feels manageable
- Personal tasks not neglected

⚠️ **Review Needed**:
- Missed client deadlines
- Constantly behind
- Task list growing not shrinking
- Burnout feeling

### **Leading Indicators of Problems**

🚨 **Red Flags**:
- More than 5 P0 tasks at once (overcommitted)
- More than 100 open tasks (poor cleanup)
- Same task rescheduled 3+ times (unrealistic or not important)
- Recurring tasks piling up (wrong recurrence or should be automated)
- Personal tasks all overdue (burnout risk)

---

## Sample Scenarios

### **Scenario 1: Client Emergency**

**Situation**: Crowd Control conversion tracking broken (client losing money)

**Action**:
1. Create new task: `[Crowd Control] Fix Conversion Tracking - CLIENT EMERGENCY`
2. Set due date: Today
3. Priority: P0 (CRITICAL + REVENUE)
4. Time estimate: 2 hours
5. Reschedule 2 P1 tasks to tomorrow
6. Work on P0 immediately

### **Scenario 2: Weekly Planning Overload**

**Situation**: 15 P1 tasks due this week (unrealistic)

**Action**:
1. Re-evaluate each task:
   - Which are actually P0? (Real deadlines)
   - Which can move to next week? (No hard deadline)
   - Which can be deleted? (No longer relevant)
2. Realistic capacity: 5-6 hours/day × 5 days = 25-30 hours
3. Reserve 20% for emergencies = 20-24 productive hours
4. Each task = 1-2 hours = 10-20 tasks maximum
5. Reschedule bottom 5 tasks to next week

### **Scenario 3: Wispr Notes Piling Up**

**Situation**: 8 unprocessed Wispr voice notes

**Action**:
1. Friday afternoon: Batch process all 8
2. For each note:
   - Personal (vitamins, prescriptions) → Add to personal list with Friday admin time
   - Client (budget questions) → Create proper client task with context
   - Ideas (AI article link) → Add to knowledge base inbox
   - Junk (old meeting note) → Delete
3. Delete all 8 Wispr tasks after processing
4. Set recurring reminder: "Process Wispr notes" every Friday 4pm

---

## Templates

### **New Task Template**

```
Title: [Client/Project] Action Verb - Specific Outcome
Due: [Realistic date]
Notes:
Priority: [P0/P1/P2/P3/P4]
Urgency: [CRITICAL/HIGH/MEDIUM/LOW]
Impact: [REVENUE/EFFICIENCY/STRATEGIC/MAINTENANCE]

Context:
- Why: [Why is this needed?]
- Success: [What does done look like?]
- Time: [Estimated time]
- Blockers: [Any dependencies?]

Reference: [Link to CONTEXT.md, audit, or doc]
```

### **Weekly Planning Template**

```
# Week of [Date]

## Top Priorities (P0/P1)
1. [Client] - [Task] - [Time estimate]
2. [Client] - [Task] - [Time estimate]
3. [Project] - [Task] - [Time estimate]

## This Week (P2)
- [Task] - [Day]
- [Task] - [Day]

## Admin Time (P3)
- Friday 4-5pm: Personal tasks + Wispr processing + Cleanup

## Deferred to Next Week
- [Task] - [Reason]
- [Task] - [Reason]

## Capacity Check
- Available hours: [X hours]
- Committed hours: [Y hours]
- Buffer: [Z hours]
- Status: [GOOD / TIGHT / OVERCOMMITTED]
```

---

## FAQ

**Q: What if I have 5 P0 tasks in one day?**
A: You're overcommitted. Negotiate deadlines, delegate, or work late. Then review weekly planning to prevent this.

**Q: What if a P3 task keeps getting rescheduled?**
A: Ask: "If I never do this, what happens?" If answer is "nothing", delete it. If answer is "eventually problems", schedule it realistically or automate it.

**Q: How do I handle "Someday/Maybe" tasks?**
A: Create a separate list or use due date "2099-12-31". Review monthly. Most will eventually be deleted.

**Q: What about urgent personal tasks during work time?**
A: Personal urgent = P1. Handle immediately. But if happening often, review life systems (e.g., set prescription reminders 2 weeks in advance).

**Q: What if client asks for something urgent but I'm fully booked?**
A: Client request = P1 minimum. Options:
1. Do it (reschedule other work)
2. Negotiate timeline (push back respectfully)
3. Delegate (if you have team)
Pick based on relationship value and revenue at risk.

---

## Next Steps

**Tomorrow Morning (Nov 7)**:
1. Run Initial Cleanup (60 mins)
2. Assign Priorities (30 mins)
3. Create This Week's Plan (15 mins)
4. Update CONTEXT.md with new system

**Every Monday**:
1. Weekly Review (10 mins)
2. Triage Open Tasks (15 mins)
3. Create Week Plan (5 mins)

**Every Friday**:
1. Process Wispr Notes (30 mins)
2. Weekly Cleanup (15 mins)
3. Archive Completed Work (5 mins)

**Monthly (First Monday)**:
1. Deep Cleanup (30 mins)
2. Review Success Metrics (15 mins)
3. Adjust System (15 mins)

---

**Last Updated**: 2025-11-06
**Status**: Ready for Implementation
**Next Review**: 2025-12-06 (30 days post-implementation)
