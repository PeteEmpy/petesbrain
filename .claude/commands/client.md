---
description: Load client context and show status summary
allowed-tools: Read, mcp__google-ads__get_client_platform_ids, mcp__google-tasks__list_tasks
argument-hint: <client-name>
---

# Client Context: $ARGUMENTS

Load the context for this client and provide a quick status summary.

## Steps

1. **Read client CONTEXT.md**:
   ```
   Read: clients/$ARGUMENTS/CONTEXT.md
   ```

2. **Get platform IDs** using `mcp__google-ads__get_client_platform_ids('$ARGUMENTS')`

3. **Check for active tasks** in `clients/$ARGUMENTS/tasks.json`

4. **Provide summary** in this format:

```
## [Client Name] - Quick Summary

**Platform IDs:**
- Google Ads: [ID]
- Merchant Centre: [ID]
- GA4: [ID]

**Active Tasks:** [count]
- [P0/P1 tasks if any]

**Key Context:**
- [2-3 key points from CONTEXT.md - targets, current focus, recent changes]

**Recent Activity:**
- [Last email sync date if available]
- [Any recent reports]

Ready to work on [Client Name]. What would you like to do?
```

Keep summary concise - this is for quick orientation, not deep analysis.
