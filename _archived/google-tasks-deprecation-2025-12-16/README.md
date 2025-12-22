# Google Tasks Deprecation Archive

**Date:** December 16, 2025
**Status:** Archived - No longer in use

## Overview

This directory contains all files related to the Google Tasks integration that was deprecated on December 16, 2025.

**Reason for Deprecation:**
- PetesBrain migrated to a single internal task system (`clients/{client}/tasks.json`)
- Google Tasks API had limitations (no recurring task support, sync complexity)
- Maintenance overhead of two separate task systems
- Risk of tasks getting lost between systems

## Migration Summary

- **Date:** December 16, 2025
- **Tasks Migrated:** 15 relevant tasks moved to internal system
- **Tasks Archived:** 77 low-priority tasks archived to `data/backups/google-tasks-backup-2025-12-16.json`
- **Agents Updated:** 6 agents updated to use internal system only
- **LaunchAgent Unloaded:** `co.roksys.petesbrain.sync-todos-to-google-tasks.plist`

## Archived Files

### Agents
- `agents/sync-todos-to-google-tasks/` - Sync agent (no longer needed)

### Core Library
- `shared/google_tasks_client.py` - Google Tasks API client

### Utility Scripts (shared/)
- `shared/deduplicate-google-tasks.py`
- `shared/migrate-todos-to-google-tasks.py`

### Utility Scripts (shared/scripts/)
- `shared/scripts/cleanup_google_tasks.py`
- `shared/scripts/update_google_task.py`
- `shared/scripts/migrate-google-tasks-final.py`
- `shared/scripts/import-from-google-tasks.py`

### Utility Scripts (scripts/)
- `scripts/cleanup-google-tasks-artifacts.py`

### MCP Server
- `infrastructure/mcp-servers/google-tasks-mcp-server/` - Entire MCP server implementation

## Related Documentation

See `docs/GOOGLE-TASKS-DEPRECATION-PLAN.md` for complete deprecation plan and execution details.

## Restoration (if needed)

If Google Tasks integration needs to be restored:
1. Copy files back from this archive directory
2. Re-enable MCP server in `.mcp.json`
3. Reload LaunchAgent: `launchctl load ~/Library/LaunchAgents/co.roksys.petesbrain.sync-todos-to-google-tasks.plist`
4. Revert agent changes (check git history for December 16, 2025)
5. Revert documentation updates

---

**Historical Note:** This archive preserves the Google Tasks integration for reference. Do not delete without consulting deprecation plan documentation.
