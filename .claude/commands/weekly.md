---
description: Generate weekly Google Ads report for a client
allowed-tools: Read, Write, Bash, mcp__google-ads__run_gaql, mcp__platform-ids__get_client_platform_ids
argument-hint: <client-name>
---

# Weekly Report: $ARGUMENTS

Generate the weekly Google Ads performance report for this client.

Use the `google-ads-weekly-report` skill to generate a comprehensive weekly analysis.

**Client:** $ARGUMENTS
**Date Range:** Last 7 days (unless specified otherwise)

Follow the skill instructions at `.claude/skills/google-ads-weekly-report/SKILL.md` which includes:

1. Load client CONTEXT.md for account IDs and targets
2. Pull Google Ads data via GAQL
3. Calculate ROAS, CPA, WoW changes
4. Generate markdown report
5. Save to `clients/$ARGUMENTS/reports/weekly/`
6. Create tasks only for P0 critical issues meeting thresholds
7. Provide executive summary

Start by reading the client context and pulling the data.
