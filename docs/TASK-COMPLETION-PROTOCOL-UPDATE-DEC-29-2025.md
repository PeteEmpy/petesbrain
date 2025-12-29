# Task Completion Protocol Update - December 29, 2025

## The Issue

**Date**: December 29, 2025
**Incident**: Task incorrectly marked for completion when manual note only requested investigation

**What Happened**:
- User added manual note: "How are these terms tracking?"
- This was a **question requesting investigation**, not a completion instruction
- I (Claude) incorrectly interpreted this as an instruction to:
  1. Investigate the terms ✅ (correct)
  2. Complete the task ❌ (incorrect)
- User stopped the process before completion occurred
- **Correct behavior**: Investigate → Report findings → Leave task open

---

## Root Cause

The previous protocol was **ambiguous** about when to complete tasks vs. when to just execute instructions.

**Previous guidance** (lines 420-430 in old CLAUDE.md):
```
**B) Instruction to Execute** (Contains action verbs)
- STOP - DO NOT just add as note
- EXECUTE the instruction FIRST
- Verify the result
- **THEN** complete the task (if instruction says "then complete")
- Log execution details to tasks-completed.md
```

**The problem**:
- "THEN complete the task" appeared to be the default action
- "(if instruction says 'then complete')" was in parentheses (seemed optional)
- Not clear enough that completion requires EXPLICIT instruction

**Missing categories**:
- No explicit category for "Questions" (How is X?, What's the status?)
- No explicit category for "Instructions WITHOUT completion" (Review X, Investigate Y)

---

## The Fix

Updated `.claude/CLAUDE.md` lines 407-472 with crystal-clear completion rules.

### New Critical Rule (Added)

**🚨 CRITICAL RULE: NEVER complete a task unless EXPLICITLY instructed to do so.**

**Tasks can ONLY be completed in these TWO ways:**
1. **User clicks "Complete" button in Task Manager UI** (automatic)
2. **Manual note explicitly says to complete it** (e.g., "Done", "Complete", "Close it", "then complete")

### New 5-Category Decision Tree

Replaced ambiguous 3-category system with explicit 5-category system:

| Category | Keywords | Action | Complete? |
|----------|----------|--------|-----------|
| **A) Explicit Completion** | "Done", "Finished", "Complete", "Close it", "Mark done" | Complete immediately | ✅ YES |
| **B) Conditional Completion** | "Check X, then complete", "Verify Y and close" | Execute, verify, then complete | ✅ YES |
| **C) Question/Investigation** | "How is X?", "What's the status?", "Check if..." | Execute, report findings | ❌ NO |
| **D) Instruction WITHOUT Completion** | "Review X", "Investigate Y", "Analyze Z" | Execute, report findings | ❌ NO |
| **E) Comment** | Just notes, no actions | Add as note to task | ❌ NO |

### Key Examples Added

| Manual Note | Action Required | Complete Task? |
|-------------|----------------|----------------|
| **"How are these terms tracking?"** | **1. Investigate 2. Report findings** | **❌ NO** |
| "Review the performance and let me know" | 1. Review 2. Report findings | ❌ NO |
| "What's the current status?" | 1. Check status 2. Report | ❌ NO |
| "Investigate this issue" | 1. Investigate 2. Report | ❌ NO |
| "Confirm recent stats show profit, then complete it" | 1. Pull stats 2. Verify 3. Complete | ✅ YES |
| "Done" | Complete immediately | ✅ YES |

---

## Behavioral Change

**Before** (ambiguous):
```
Manual note: "How are these terms tracking?"
→ Investigate terms ✅
→ Complete task ❌ (INCORRECT - no completion requested)
```

**After** (explicit):
```
Manual note: "How are these terms tracking?"
→ Category: C) Question/Investigation
→ Investigate terms ✅
→ Report findings to user ✅
→ DO NOT complete task ✅
→ Clear manual note ✅
```

---

## Completion Authority

**ONLY 2 ways to complete a task:**

1. **UI Button Click** (automatic via Task Manager)
   - User clicks "Complete" button
   - System automatically completes task
   - No Claude involvement

2. **Explicit Manual Note** (via manual-task-notes.json)
   - **Explicit**: "Done", "Complete", "Finished", "Close it", "Mark done"
   - **Conditional**: "Check X, then complete", "Verify Y and close"
   - **NOT Questions**: "How is X?", "What's the status?"
   - **NOT Instructions**: "Review X", "Investigate Y"

---

## Prevention Measures

**Documentation**:
- ✅ Updated `.claude/CLAUDE.md` (lines 407-472)
- ✅ Added 🚨 CRITICAL RULE header (impossible to miss)
- ✅ Created this incident document

**Testing**:
- Next "Process my task notes" request will validate new protocol
- Future questions like "How is X?" should NOT trigger completion

**Monitoring**:
- User will validate behavior over next few uses
- If issue recurs, escalate to systemic protocol enforcement

---

## Files Changed

| File | Lines | Change |
|------|-------|--------|
| `.claude/CLAUDE.md` | 407-472 | Complete rewrite of task notes protocol |
| `docs/TASK-COMPLETION-PROTOCOL-UPDATE-DEC-29-2025.md` | New | This document |

---

## Commit Reference

```
commit c275a2c
Author: Claude Code
Date: December 29, 2025

CRITICAL: Update task completion protocol - never complete without explicit instruction
```

---

## Related Documentation

- **Global Instructions**: `.claude/CLAUDE.md` (lines 407-472)
- **Task System Guide**: `docs/INTERNAL-TASK-SYSTEM.md`
- **Incidents Log**: `docs/INCIDENTS.md`

---

**Status**: ✅ **RESOLVED** - Protocol updated, committed, documented
