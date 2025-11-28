# Task Priority Updater

**Type:** System Maintenance
**Schedule:** Daily at 10:00 PM
**Status:** Active

## Purpose

Automatically reassesses all task priorities daily based on due dates to ensure urgent tasks are properly flagged.

## How It Works

1. Scans all client `tasks.json` files
2. Calculates correct priority based on days until due:
   - **P0**: 0-2 days (urgent/immediate)
   - **P1**: 3-14 days (this week/next week)
   - **P2**: 15-30 days (next 2-4 weeks)
   - **P3**: 30+ days (later)
3. Updates priorities if changed
4. Regenerates tasks-overview.html
5. Logs all changes

## Files

- **Script:** `agents/task-priority-updater/task-priority-updater.py`
- **LaunchAgent:** `agents/launchagents/com.petesbrain.task-priority-updater.plist`
- **Logs:** `~/.petesbrain-task-priority-updater.log`

## Why This Matters

- **Automatic escalation:** Tasks due in 5 days (P1) automatically become P0 when 2 days away
- **Correct urgency:** Ensures P0 badge always reflects truly urgent items
- **No manual work:** Runs silently every night
- **Audit trail:** Logs all priority changes for review

## Schedule

**Daily at 10:00 PM** - Every night, ensuring priorities are updated and ready for the next day

## Monitoring

Check logs:
```bash
tail -50 ~/.petesbrain-task-priority-updater.log
```

Check LaunchAgent status:
```bash
launchctl list | grep task-priority-updater
```

## Created

2025-11-18
