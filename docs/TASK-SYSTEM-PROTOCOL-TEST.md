# Task System Protocol Test

**Purpose:** Verify Claude Code follows the task creation protocol correctly
**Created:** 2025-11-19
**Reference:** `docs/TASK-SYSTEM-DECISION-GUIDE.md`

---

## How to Use This Test

**In any new Claude Code session, paste one of these scenarios and verify Claude:**

1. ✅ States which system it will use BEFORE creating the task
2. ✅ Explains WHY based on the decision tree
3. ✅ References the decision guide if needed
4. ❌ Does NOT create the task in the wrong system

---

## Test Scenarios

### Scenario 1: Weekly Recurring Client Task

**User says:**
> "Create a task to review Superspace budget and ROAS every Thursday"

**Expected Response:**
```
I need to create this task in the Internal Client Task System because:

1. Is this client work? → YES (Superspace)
2. Does it recur? → YES (weekly)
3. Decision: MUST use Internal System

Recurring tasks cannot go in Google Tasks (API limitation).

Let me create this using ClientTasksService...
```

**FAIL if Claude:**
- Creates task in Google Tasks
- Doesn't mention the decision tree
- Creates task in both systems

---

### Scenario 2: One-Time Client Task

**User says:**
> "Create a task to analyze NDA's Black Friday campaign performance by Dec 1st"

**Expected Response:**
```
I need to create this task in the Internal Client Task System because:

1. Is this client work? → YES (NDA)
2. Does it recur? → NO (one-time)
3. Does it have multiple sub-tasks? → NO
4. Decision: Use Internal System (default for client work)

Let me create this using ClientTasksService...
```

**FAIL if Claude:**
- Creates task in Google Tasks
- Doesn't explain the decision
- Skips the internal system

---

### Scenario 3: Personal Reminder

**User says:**
> "Remind me to book a dental appointment next week"

**Expected Response:**
```
I need to create this task in Google Tasks because:

1. Is this client work? → NO (personal)
2. Decision: Use Google Tasks ("Peter's List")

Let me create this using the Google Tasks MCP tool...
```

**FAIL if Claude:**
- Creates task in Internal System
- Tries to create in both systems

---

### Scenario 4: Meeting Action Items (Multiple Related Tasks)

**User says:**
> "Create tasks for these 5 action items from today's Devonshire meeting:
> 1. Review sitelink performance
> 2. Update budget tracker
> 3. Check ROAS trends
> 4. Analyze new campaign
> 5. Send monthly report"

**Expected Response:**
```
I need to create this in the Internal Client Task System because:

1. Is this client work? → YES (Devonshire)
2. Does it recur? → NO
3. Does it have multiple related sub-tasks? → YES (5 action items from same meeting)
4. Decision: Use Internal System (parent/child hierarchy)

I'll create a parent task for the meeting with 5 child tasks...
```

**FAIL if Claude:**
- Creates separate standalone tasks instead of parent/child
- Creates tasks in Google Tasks
- Creates 5 separate parent tasks

---

### Scenario 5: The Trick Question (Recurring Personal)

**User says:**
> "Create a weekly reminder to check my personal email inbox every Monday"

**Expected Response:**
```
This is a tricky one - let me think through the decision tree:

1. Is this client work? → NO (personal email)
2. Decision: Use Google Tasks ("Peter's List")

However, there's a limitation: Google Tasks API doesn't support recurring tasks.

Options:
- I can create a one-time task in Google Tasks, but you'll need to manually
  recreate it each week
- OR if this is truly important to track weekly, I could create it in the
  Internal System even though it's personal (not standard practice)

Which would you prefer?
```

**FAIL if Claude:**
- Silently creates recurring task in Google Tasks (API doesn't support this)
- Doesn't acknowledge the limitation
- Doesn't offer alternatives

---

### Scenario 6: Duplicate Prevention

**User says:**
> "I just created a task in the client work list for Smythson's Christmas campaign.
> Can you also add it to Google Tasks so I see it on my phone?"

**Expected Response:**
```
⚠️ I should NOT do this. Here's why:

The Internal Client Task System and Google Tasks are completely separate systems
that don't sync. Creating the same task in both would create a duplicate that
could cause confusion.

The task you created in the "client work list" (Internal System) will appear in:
- Daily briefings
- Client task reports
- tasks.json file

If you need mobile access to client tasks, we'd need a different solution
(perhaps a mobile view of the internal system, or accepting that Google Tasks
is only for personal reminders).

Reference: docs/TASK-SYSTEM-DECISION-GUIDE.md (see "NEVER" section)
```

**FAIL if Claude:**
- Creates duplicate task in Google Tasks
- Doesn't explain the separation
- Doesn't reference the decision guide

---

## Quick Verification Checklist

For ANY task creation request, Claude should:

- [ ] State which system it will use
- [ ] Explain the decision based on the decision tree
- [ ] NOT create recurring tasks in Google Tasks
- [ ] NOT create client work in Google Tasks (unless AI-generated)
- [ ] NOT create the same task in both systems
- [ ] Reference `docs/TASK-SYSTEM-DECISION-GUIDE.md` if there's any ambiguity

---

## If Claude Fails a Test

1. Point to this test document
2. Point to `docs/TASK-SYSTEM-DECISION-GUIDE.md`
3. Point to `docs/CLAUDE.md` Task Management section (line 342)
4. Request Claude re-read the decision tree before proceeding

---

## Success Criteria

✅ **Protocol is working if:**
- Claude consistently asks the 3 decision questions
- No recurring tasks are created in Google Tasks
- Client work defaults to Internal System
- Personal tasks go to Google Tasks
- Duplicates are prevented

❌ **Protocol needs fixing if:**
- Claude creates tasks without stating which system
- Recurring tasks appear in Google Tasks
- Client work tasks appear in Google Tasks (except AI-generated "Client Work" list)
- Same task exists in both systems

---

**Last Updated:** 2025-11-19
**Status:** ✅ Active Test Document
**Next Review:** After 10 task creation sessions to verify protocol adherence
