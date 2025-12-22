---
description: Load client context and show comprehensive briefing with session continuity
allowed-tools: Read, mcp__platform-ids__get_client_platform_ids
argument-hint: <client-name>
---

# Client Context: $ARGUMENTS

Load full client context including strategic overview, last session summary, open questions, and active tasks. Provides comprehensive briefing for session continuity.

## Steps

1. **Validate client exists**:
   - Check if `clients/$ARGUMENTS/` directory exists
   - If not, list available clients or suggest similar names

2. **Read core context files**:
   - `clients/$ARGUMENTS/CONTEXT.md` (strategic context)
   - `clients/$ARGUMENTS/session-log.md` (most recent session only)
   - `clients/$ARGUMENTS/open-questions.md` (active questions only)
   - `clients/$ARGUMENTS/tasks.json` (current tasks)

3. **Get platform IDs** using `mcp__platform-ids__get_client_platform_ids('$ARGUMENTS')`

4. **Present structured briefing**:

```
🟢 [Client Name] - Context Briefing
==========================================

## ✓ Strategic Context

- Account structure: [from CONTEXT.md]
- Target ROAS / KPIs: [from CONTEXT.md]
- Current focus: [from CONTEXT.md]
- Monthly budget: [from CONTEXT.md]
- Platform IDs: Google Ads [ID], GA4 [ID], Merchant Centre [ID]

## ✓ Last Session Summary

**Date:** [YYYY-MM-DD] ([topic])

**Analysed:**
- [Key points from last session-log.md entry]

**Decided:**
- [Decisions made]

**Still investigating:**
- [Open items from last session]

## ✓ Open Questions ([count])

**High Priority:**
- [Question] (Noticed: YYYY-MM-DD)

**Medium/Low Priority:**
- [Other questions if any]

## ✓ Active Tasks ([count])

**P0 (Critical):**
- [P0 tasks with ⚠️ if overdue]

**P1 (Important):**
- [P1 tasks]

---

**Ready to work on [Client Name]. What would you like to do?**
```

5. **Handle missing files gracefully**:
   - If CONTEXT.md missing: "⚠️ CONTEXT.md not found"
   - If session-log.md missing: "ℹ️ No previous sessions logged yet"
   - If open-questions.md missing: "ℹ️ No open questions tracked"
   - If no recent session: "First session with new continuity system"

## Formatting

- Use British English spelling
- Apply green heading styling (🟢 for H1, ✓ for H2)
- Keep concise but comprehensive
- Focus on actionable context for THIS session
- Show overdue tasks with ⚠️ warning
- For session-log.md, only show the MOST RECENT entry (not full history)
