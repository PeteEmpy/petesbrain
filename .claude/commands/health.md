# Health Check Command

Run system health check on all automated workflows.

## Instructions

When the user types `/health`, immediately invoke the `system-health-check` skill:

```
Skill(command='system-health-check')
```

This will:
1. Check all 50+ LaunchAgent workflows
2. Report which are healthy vs unhealthy
3. Flag critical failures (essential workflows)
4. Offer to restart unhealthy workflows
5. Show diagnostic info for any issues

## Expected Output

The skill will present:
- Overall health summary (X/Y workflows healthy)
- Critical failures with 🔴
- Non-critical issues with ⚠️
- List of healthy systems ✅
- Diagnostic logs for any failures

## Usage

Just type `/health` and the system health check will run automatically.
