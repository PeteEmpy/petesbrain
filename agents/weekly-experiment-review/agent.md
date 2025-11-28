---
name: weekly-experiment-review
status: active
last_migrated: 2025-11-13
last_updated: 2025-11-24
---

# weekly-experiment-review

## Purpose
Reviews experiments from the ROK experiments CSV that are older than 14 days and ready for outcome assessment. Helps migrate completed experiments to client CONTEXT.md files.

## Schedule
Runs every Friday at 9:30 AM via LaunchAgent.

## Modes

### Automated Mode (--auto)
Used by LaunchAgent. Generates a report of pending experiments without any interactive prompts.
- Saves report to: `data/cache/experiment-review-pending.txt`
- Logs to: `data/cache/experiment-review.log`
- No user input required

### Interactive Mode (default)
Run manually for interactive experiment review:
```bash
python3 agents/weekly-experiment-review/weekly-experiment-review.py
```
Prompts for each experiment outcome and updates CONTEXT.md files.

### Report Mode (--report)
Just print pending experiments without state changes:
```bash
python3 agents/weekly-experiment-review/weekly-experiment-review.py --report
```

## Configuration
- Script: `weekly-experiment-review.py`
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.experiment-review.plist`
- Log: `~/Library/Logs/PetesBrain/experiment-review-stdout.log`
- State file: `data/state/experiment-review-state.json`

## Migration Notes
- Migrated on 2025-11-13 during project restructuring.
- 2025-11-24: Added `--auto` mode for LaunchAgent compatibility (removes `input()` calls).
