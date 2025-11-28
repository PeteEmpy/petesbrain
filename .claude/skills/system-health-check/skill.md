---
name: system-health-check
description: Checks the health status of all PetesBrain automated agents and workflows. Use when user says "health check", "system status", "check agents", "are my workflows running", or wants to diagnose automation issues.
allowed-tools: Bash, Read
---

# System Health Check Skill

Check the health status of all PetesBrain automated agents and workflows.

## What This Skill Does

This skill runs the health monitoring system to check all 46+ automated workflows:

1. **Process Status**: Is each LaunchAgent loaded and running?
2. **Log Freshness**: Has each workflow run recently (based on its schedule)?
3. **Activity Health**: Is each workflow functioning correctly?

It provides a comprehensive report showing:
- Healthy vs unhealthy workflows
- Critical failures (workflows essential to operations)
- Non-critical issues (optional workflows)
- Detailed status for each workflow

## Instructions

When the user invokes this skill:

1. **Run the health check** with verbose output:
   ```bash
   python3 agents/system/health-check.py --verbose
   ```

2. **Present the results** in a clear, organized way:
   - Overall health summary (X/Y workflows healthy)
   - Critical failures (if any) with red flag 🔴
   - Non-critical issues (if any) with warning ⚠️
   - List of healthy systems ✅

3. **If there are unhealthy workflows**, ask the user:
   - "Would you like me to attempt to restart the unhealthy workflows?"
   - If yes, run: `python3 agents/system/health-check.py --restart-unhealthy`

4. **Provide context** for any issues:
   - What each workflow does (from the description)
   - Why it might be failing (check log files if needed)
   - How to fix manually if auto-restart doesn't work

5. **Show recent activity** for critical failures:
   - Check the workflow's log file (path shown in health check output)
   - Show last 20 lines of the log to help diagnose the issue

## Output Format

Present results in this structure:

```
System Health Check - [Date/Time]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL STATUS: [X/Y workflows healthy]

[If critical failures exist:]
🔴 CRITICAL FAILURES (X):
   • workflow-name - Description
   • workflow-name - Description

[If non-critical issues exist:]
⚠️  NON-CRITICAL ISSUES (X):
   • workflow-name - Description

[If all healthy:]
✅ ALL SYSTEMS OPERATIONAL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[For any failures, show diagnostic info:]

Investigating [workflow-name]:
[Last 20 lines of log file]
```

## Additional Actions

- If user asks "what's wrong with X?", read that workflow's log file and diagnose
- If user wants to see all workflows, list them grouped by category:
  - Core Automation (critical)
  - Weekly Reports
  - Product Tracking
  - Client-Specific

## Notes

- The health check runs automatically every 30 minutes via LaunchAgent
- This skill provides on-demand manual checking
- Some workflows are "critical" (essential) vs "non-critical" (optional)
- Weekly workflows only need to be healthy on their scheduled day (Monday)
