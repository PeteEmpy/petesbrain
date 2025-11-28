# Intelligent Task Notes Workflow

**Last Updated:** 2025-11-18

This document explains the intelligent task management system that converts your manual notes into structured task updates with automatic parent/child hierarchy.

---

## Quick Start

1. **Open tasks overview**: `open tasks-overview.html`
2. **Add notes to tasks**: Click "Add Note" on any task
3. **Save all notes**: Click "Save All Notes" button
4. **Tell Claude**: "Process the manual task notes"
5. **Watch the magic**: Claude analyzes and updates everything

---

## The Workflow

### Step 1: Add Notes in Browser

Navigate to any task and click **"Add Note"**. Write what you've done:

**Examples:**
- *"Done. Set up AI/MAX campaign with brand inclusions. Review in 7 days."*
- *"Called client, they approved the budget increase. Implementing tomorrow."*
- *"Started analysis but waiting on data from Google rep."*
- *"Completed the sitelink fixes. Monitor performance next week."*

**Tips:**
- Be natural - write like you're updating a colleague
- Mention if something needs follow-up ("review in X days", "check next week")
- Say "done" or "completed" if you finished the work
- Mention blockers if you're stuck ("waiting on client", "blocked by X")

### Step 2: Save All Notes

Click **"Save All Notes"** button (appears when you have notes).

Downloads `manual-task-notes.json` to your Downloads folder containing:
- Your notes
- Full task context
- Client information
- Current task status

### Step 3: Process with Claude

Tell Claude:
```
Process the manual task notes
```

Or if the file is in a different location:
```
Process the manual task notes from ~/Desktop/manual-task-notes.json
```

---

## What Claude Does

### Intelligent Analysis

For each note, Claude:

1. **Reads full context**: Original task, client, notes, priority
2. **Analyzes your note**: Looks for completion signals, follow-ups, blockers
3. **Makes smart decisions**: Complete? Follow-up needed? More work required?
4. **Takes appropriate action**: Update, complete, create new tasks

### Automated Detection

**Completion Signals:**
- "done", "completed", "finished"
- "implemented", "added", "created"
- "sent", "emailed", "called"

**Follow-up Signals:**
- "review in X days"
- "check next week"
- "revisit Monday"
- "monitor", "follow up"

**Blocker Signals:**
- "waiting on", "blocked by"
- "need", "requires"
- "started but"

---

## The Parent/Child Magic

### Scenario 1: Standalone → Parent (Most Common)

**Your task:**
```
[AFH] Test AI Max for brand campaign with brand inclusions (standalone)
```

**Your note:**
```
"Done. Campaign created with brand targeting.
Campaign ID: 20276730131. Review performance in 7 days."
```

**Claude creates:**
```
[AFH] AI Max Brand Campaign - Setup & Review (PARENT)
  ├─ [AFH] Set up AI Max with brand inclusions (COMPLETED - Nov 18)
  │   Notes: Campaign ID 20276730131. Brand targeting enabled.
  │          Settings: [details]. Live as of Nov 18, 2025.
  │
  └─ [AFH] Review AI Max brand campaign (7-day) (ACTIVE - Due Nov 25)
      Notes: Review after 1 week of data. Check: impressions, CTR,
             conv rate, ROAS vs main PMax. Decision: scale/adjust/pause.
```

### Scenario 2: Child Task with Follow-up

**Your note on a child task:**
```
"Completed demographic analysis. Need to implement
bid adjustments next week."
```

**Claude creates:**
```
[NMA] 3-Week Account Improvement Plan (PARENT - unchanged)
  ├─ Week 1: Pull Demographic Performance Data (COMPLETED - Nov 18)
  │   [Your work documented here]
  │
  └─ Week 2: Implement Demographic Bid Adjustments (NEW - Due Nov 25)
      [Claude creates this as sibling to completed task]
```

### Scenario 3: Simple Completion

**Your note:**
```
"Done. Emailed Helen with Bolton Abbey recommendation."
```

**Claude does:**
- ✅ Marks task as **completed**
- 📝 Expands notes with: "Email sent Nov 18, 2025. Recommendation: pause campaign, reallocate £500/month budget. Awaiting client response."
- No follow-up needed (unless you mentioned one)

---

## Examples from Real Work

### Example 1: Implementation with Review

**Task:** `[Uno Lighting] Enable new customer acquisition on Villains campaign`

**Your note:**
```
"Enabled. Set to new customers only, bid adjustment +20%.
Check results in 2 weeks."
```

**Result:**
```
[Uno Lighting] New Customer Acquisition - Villains (PARENT)
  ├─ Enable new customer acquisition targeting (COMPLETED)
  │   Settings: New customers only, +20% bid adjustment.
  │   Enabled: Nov 18, 2025, 15:30
  │   Campaign: Villains | P Max | Main
  │
  └─ Review new customer acquisition performance (ACTIVE, Due Dec 2)
      Review after 2 weeks. Metrics: new customer %,
      ROAS comparison, incremental revenue.
```

### Example 2: Blocked Work

**Task:** `[Smythson] Discuss revised Q4 projections with client`

**Your note:**
```
"Prepared analysis showing £320k shortfall.
Waiting for meeting with client next week."
```

**Result:**
- Task stays **active**
- Notes expanded: "Analysis prepared Nov 18. Gap: £320k (13.5% short of target). Three options prepared: accept gap, add budget, or revise target. Meeting scheduled for next week to discuss."
- Status updated: Added tag `awaiting-client`
- No completion (you said "waiting")

### Example 3: Multi-phase Implementation

**Task:** `[NMA] Week 1: Add Sitelinks to Active Campaigns`

**Your note:**
```
"Added 6 sitelinks to ROW Engineering. Still need to do
UK Management and UK Motorsport tomorrow."
```

**Result:**
- Task stays **active** (not complete)
- Notes expanded: "Progress Nov 18: ROW Engineering complete (6 sitelinks added). Remaining: UK Engineering Management, UK Motorsport (scheduled Nov 19)."
- Task due date extended if needed

---

## Tips for Best Results

### ✅ Good Notes

- **Be specific about completion**: "Done", "Completed", "Sent"
- **Mention follow-ups explicitly**: "Review in 7 days", "Check next Monday"
- **Include key details**: Campaign IDs, settings, who you contacted
- **Note blockers**: "Waiting on client", "Need data from Google"

**Good example:**
```
"Implemented. Campaign ID 12345. Budget £500/day,
Target ROAS 400%. Live as of 3pm. Review performance
in 5 days before scaling."
```

### ❌ Avoid Vague Notes

- "Working on it" (Too vague - what did you do?)
- "Done" (Done what? Any follow-up?)
- "Made changes" (What changes? Need review?)

**Better version:**
```
"Completed ROAS reduction from 190% to 170%.
Changed Sunday 6pm for Monday readiness.
Monitor daily spend Mon-Wed."
```

---

## Advanced: Custom Hierarchy

### Creating Multi-Level Projects

If you have a complex multi-phase project, you can structure it:

**Phase 1 Note:**
```
"Phase 1 complete: Setup finished.
Phase 2: Run for 2 weeks.
Phase 3: Scale if successful."
```

**Claude creates:**
```
[Client] Project Name (PARENT)
  ├─ Phase 1: Setup (COMPLETED)
  ├─ Phase 2: Test Run (ACTIVE, 2 weeks)
  └─ Phase 3: Scale (PENDING, conditional)
```

### Linking to External Tasks

Reference other tasks in your notes:

```
"Done. This unblocks the Performance Max restructure task."
```

Claude can identify the reference and add cross-links in notes.

---

## Troubleshooting

### "Save All Notes" button not appearing
- Refresh the page (Cmd+R)
- Check you've actually saved notes (click "Save" in note input)

### Notes not detecting follow-up
- Be explicit: "review in 7 days" instead of "review later"
- Use numbers: "check in 5 days" instead of "check soon"

### Task not marked complete
- Check your wording - did you say "done" or "completed"?
- If stuck/waiting, Claude correctly keeps it active
- You can override by telling Claude directly

### Wrong parent/child conversion
- Claude errs on the side of creating hierarchy
- You can ask Claude to flatten if needed
- Or specify in note: "No follow-up needed, just complete this"

---

## The System in Action

**Before:**
- 39 standalone tasks
- Notes scattered across multiple updates
- Unclear what needs follow-up
- Manual tracking of review dates

**After:**
- Intelligent hierarchy (parents group related work)
- Rich, expanded notes with context
- Automatic follow-up task creation
- Proper completion tracking
- Searchable history

**Time Saved:**
- No manual task creation for follow-ups
- No thinking about hierarchy
- No remembering review dates
- Just write what you did naturally

---

## Future Enhancements

Potential additions to the system:

1. **Auto-email notifications**: "Hey, you have a review task due tomorrow"
2. **Performance tracking**: Link follow-up tasks to Google Ads data
3. **Smart scheduling**: "Review Monday" = next Monday's date
4. **Dependency chains**: "Can't start Task B until Task A complete"
5. **Time tracking**: Estimate vs actual time analysis

---

**Remember**: The system is intelligent but not psychic. The more detail you provide in your notes, the better Claude can structure your work.

**Golden Rule**: Write notes like you're telling a colleague what you did. Claude handles the rest.
