# Task Cleanup Plan - With Provenance Analysis
**Date:** 2025-11-13
**Status:** Ready for Execution

---

## Summary

**Total Tasks Found:** 266 (247 AI-generated, 19 manual)
**Tasks to Remove:** ~150 (AI-generated duplicates only)
**Tasks to Keep:** ~116 (1 copy per AI pattern + all manual tasks)

---

## Removal Criteria (Conservative)

A task can ONLY be removed if **ALL** of these are true:
1. ✅ Has "Source: AI Generated" metadata
2. ✅ Has "AI Task ID" metadata
3. ✅ Same client + same title as another task
4. ✅ Appears 4+ times
5. ✅ Keep the FIRST occurrence

**Tasks that will NEVER be removed:**
- ❌ Manual tasks (no AI metadata)
- ❌ Strategic tasks with detailed checklists
- ❌ First occurrence of any task pattern
- ❌ Tasks with unique requirements or dates

---

## Client-by-Client Cleanup Plan

### **Bright Minds** (24 entries → 10 entries)
**Will Remove (14 duplicates):**
1. "Monitor ROAS progression toward 400% target" - Remove 7 AI copies, keep 1
2. "Validate conversion tracking post-changes (daily check)" - Remove 5 AI copies, keep 1
3. "Validate Conversion Tracking Post-Changes - ONGOING" - Remove 1 copy-paste duplicate

**Will Keep (10 tasks):**
- 2 manual tasks (detailed conversion tracking checklist, weekly report task)
- 1 copy of "Monitor ROAS" (AI-generated)
- 1 copy of "Validate tracking" (AI-generated)
- Other strategic tasks

**Provenance:**
- Manual tasks identified by lack of "Source: AI Generated" field
- AI tasks have clear metadata showing generation date/time
- Copy-paste duplicate has identical task_id (NzlCNXp6RzJLMnZoWGNadA)

---

### **Smythson** (55 entries → ~45 entries)
**Will Remove (~10 duplicates):**
1. "Move diary asset group to new standalone PMAX campaign" - Remove 7-8 AI copies, keep 1

**Will Keep (~45 tasks):**
- 6 manual tasks (strategic budget/ROAS changes for UK/USA/EUR/ROW)
- All Q4 strategy tasks (December 1 changes, Thanksgiving boost, etc.)
- 1 copy of each AI-generated task pattern

**Provenance:**
- Manual tasks: December budget changes, regional ROAS adjustments
- These have NO AI metadata and appear to be strategic planning
- Must preserve all unique strategic tasks

---

### **National Design Academy** (22 entries → ~14 entries)
**Will Remove (~8 duplicates):**
1. "Update Geographic Performance Analysis dashboard" - Remove 7 AI copies, keep 1
2. "Review budget reduction impact from Nov 5th" - Remove 6 AI copies, keep 1

**Will Keep (~14 tasks):**
- All strategic implementation tasks
- 1 copy of each monitoring task

---

### **Tree2mydoor** (24 entries → ~16 entries)
**Will Remove (~8 duplicates):**
1. "Verify ProfitMetrics conversion tracking" - Remove 7 AI copies, keep 1
2. "Review Olive Tree feed stability" - Remove duplicates

**Will Keep (~16 tasks):**
- 1 manual task (if any)
- October month-end report task
- 1 copy of each verification task

---

### **Other Clients** (Following Same Pattern)
- Go Glean: 22 → ~14 entries
- Grain Guard: 20 → ~13 entries
- Crowd Control: 26 → ~18 entries
- Superspace: 18 → ~11 entries
- Positive Bakes: 22 → ~14 entries
- Godshot: 18 → ~11 entries
- Just Bin Bags: 21 → ~14 entries
- Devonshire Hotels: 21 → ~14 entries
- Accessories for the Home: 16 → ~10 entries
- Uno Lighting: 7 → ~7 entries (mostly manual, minimal cleanup)

---

## How We'll Identify What to Remove

### **Step 1: Scan for AI Metadata**
Look for this pattern in task body:
```
---
**Source:** AI Generated (2025-11-XX XX:XX)
**Client:** [client-name]
**Priority:** P1/P2
**Time Estimate:** XX mins
**Reason:** [reason]
**AI Task ID:** [uuid]
---
```

**If present** = AI-generated (eligible for duplicate removal)
**If absent** = Manual task (NEVER remove)

### **Step 2: Count Occurrences**
For each AI-generated task:
- Count how many times the same title appears for same client
- If 4+ occurrences, keep FIRST, remove rest

### **Step 3: Preserve Manual Tasks**
Tasks without AI metadata = keep ALL copies

### **Step 4: Preserve First Occurrence**
For duplicates, always keep the FIRST occurrence in the file

---

## Example: Bright Minds Cleanup

### **BEFORE (Planned Work section):**
```markdown
### [Bright Minds] Validate Conversion Tracking Post-Changes - ONGOING
<!-- task_id: NzlCNXp6RzJLMnZoWGNadA -->
**Status:** 📋 In Progress
[Detailed checklist...]
(NO AI METADATA - KEEP THIS)

### [Bright Minds] Validate Conversion Tracking Post-Changes - ONGOING
<!-- task_id: NzlCNXp6RzJLMnZoWGNadA -->
**Status:** 📋 In Progress
[Detailed checklist...]
(DUPLICATE TASK_ID - REMOVE THIS)

### [Bright Minds] Monitor ROAS progression toward 400% target
<!-- task_id: ckQtMnhOLUFjal9hd2lOWQ -->
**Source:** AI Generated (2025-11-11 09:30)
**AI Task ID:** 5e6b7401-055a-4a92-9401-eee2e53db330
(AI GENERATED - KEEP FIRST)

### [Bright Minds] Monitor ROAS progression toward 400% target
<!-- task_id: XYZ -->
**Source:** AI Generated (2025-11-11 10:30)
**AI Task ID:** different-uuid
(AI GENERATED DUPLICATE - REMOVE)

[6 more "Monitor ROAS" copies with AI metadata - REMOVE ALL]

### [Bright Minds] Validate conversion tracking post-changes (daily check)
<!-- task_id: bWVaMmItVTNDLVVjRVZGYQ -->
**Source:** AI Generated (2025-11-11 09:29)
**AI Task ID:** b6061e92-3eb9-4a25-aa17-14d65f1552f5
(AI GENERATED - KEEP FIRST)

[5 more "Validate tracking" copies with AI metadata - REMOVE ALL]
```

### **AFTER (Cleaned):**
```markdown
### [Bright Minds] Validate Conversion Tracking Post-Changes - ONGOING
<!-- task_id: NzlCNXp6RzJLMnZoWGNadA -->
**Status:** 📋 In Progress
[Detailed checklist...]
(MANUAL TASK - PRESERVED)

### [Bright Minds] Monitor ROAS progression toward 400% target
<!-- task_id: ckQtMnhOLUFjal9hd2lOWQ -->
**Source:** AI Generated (2025-11-11 09:30)
**AI Task ID:** 5e6b7401-055a-4a92-9401-eee2e53db330
(AI TASK - KEPT FIRST OCCURRENCE)

### [Bright Minds] Validate conversion tracking post-changes (daily check)
<!-- task_id: bWVaMmItVTNDLVVjRVZGYQ -->
**Source:** AI Generated (2025-11-11 09:29)
**AI Task ID:** b6061e92-3eb9-4a25-aa17-14d65f1552f5
(AI TASK - KEPT FIRST OCCURRENCE)

--- Cleanup Note ---
Removed 14 duplicate task entries on 2025-11-13:
- 1 copy-paste duplicate (same task_id)
- 7 AI-generated "Monitor ROAS" duplicates
- 5 AI-generated "Validate tracking" duplicates
- 1 other duplicate

All manual tasks preserved. AI tasks deduplicated to first occurrence only.
```

---

## Safety Verification

Before removing ANY task, verify:
1. ✅ Has "Source: AI Generated" in body (not just similar title)
2. ✅ Has "AI Task ID" field
3. ✅ Same client AND same title as kept version
4. ✅ NOT the first occurrence
5. ✅ NOT a manual task

---

## Expected Impact

**Before Cleanup:**
- 266 total task entries across all clients
- Daily task generator creates ~150-200 daily tasks
- Daily Intel Report is overwhelming

**After Cleanup:**
- ~116 unique task entries (247 AI → ~97 unique, + 19 manual)
- Daily task generator creates ~50-80 daily tasks (56% reduction)
- Daily Intel Report is actionable

**Preserved:**
- ALL 19 manual tasks (user-created/requested)
- ALL strategic tasks (budgets, ROAS changes, campaign launches)
- 1 copy of each AI monitoring task

---

## Execution Order

1. **Bright Minds** (test case - 24 → 10 entries)
2. **National Design Academy** (22 → 14 entries)
3. **Tree2mydoor** (24 → 16 entries)
4. Review first 3 clients with user
5. If approved, proceed with remaining 11 clients
6. Final verification pass

---

## Documentation

Each cleaned CONTEXT.md will get:
1. Updated "Last Updated" date
2. Document History entry:
   ```
   | 2025-11-13 | TASK DEDUPLICATION: Removed X duplicate AI-generated task entries. Preserved all manual tasks and first occurrence of each AI task pattern. Cleanup based on provenance analysis showing Source: AI Generated metadata. | Claude Code |
   ```

---

*Analysis Date: 2025-11-13*
*Approval Required: YES*
*Ready to Execute: PENDING USER APPROVAL*
