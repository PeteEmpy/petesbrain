---
name: daily-summary-email
description: Sends manual daily briefing email with client work, calendar events, tasks, and performance updates. Use when user says "send daily summary", "daily briefing", "send briefing email", or wants to manually trigger the daily report.
allowed-tools: Bash, Read
---

# Daily Summary Email Skill

---

## Core Workflow

When this skill is triggered:

### 1. Verify Prerequisites

Check that environment variables are available:
- `GMAIL_USER` - Email address (petere@roksys.co.uk)
- `GMAIL_APP_PASSWORD` - Gmail app password
- `ANTHROPIC_API_KEY` - For AI summary generation

### 2. Execute Daily Briefing Script

Run the daily briefing generator with proper environment setup:

```bash
cd /Users/administrator/Documents/PetesBrain
export GMAIL_USER="petere@roksys.co.uk"
export GMAIL_APP_PASSWORD="pxmsoxiwuazkqhvg"
export ANTHROPIC_API_KEY="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"
/usr/local/bin/python3 agents/reporting/daily-briefing.py
```

### 3. What the Script Does

The daily briefing script:
1. **Generates client work** - Runs `daily-client-work-generator.py` first
   - Analyzes all 17 clients
   - Creates Google Tasks in "Client Work" list (with duplicate detection)
   - Assigns due dates based on priority (P0=today, P1=tomorrow, P2=3 days)
2. **Collects sections**:
   - Calendar events (today's schedule)
   - Client work (from Google Tasks, filtered by due date = today)
   - Performance anomalies (from last 24 hours)
   - Pending tasks (from Google Tasks)
   - Recent meetings
   - Weekly performance summary
   - Recent audits
   - AI inbox activity
   - Agent status
3. **Generates AI summary** - Executive summary using Claude
4. **Creates files**:
   - Markdown: `briefing/YYYY-MM-DD-briefing.md`
   - HTML: `briefing/YYYY-MM-DD-briefing.html`
5. **Sends email** - Via Gmail SMTP to petere@roksys.co.uk

### 4. Expected Output

**Success indicators**:
- ✅ Briefing generated!
- ✅ Email sent to petere@roksys.co.uk
- File paths displayed

**Files created**:
- `briefing/YYYY-MM-DD-briefing.md` (typically 2-5 KB)
- `briefing/YYYY-MM-DD-briefing.html` (typically 5-10 KB)

### 5. Troubleshooting

**If email fails**:
- Check environment variables are set correctly
- Verify Gmail app password is valid
- Check Gmail API quota hasn't been exceeded

**If client work missing**:
- Verify Google Tasks integration is working
- Check "Client Work" task list exists
- Review `shared/config/ai-tasks-config.json` for correct task list ID

**If calendar events missing**:
- May show authentication scope error (non-critical)
- Calendar integration requires additional OAuth scopes

---

## Integration Notes

**Works with**:
- Google Tasks MCP (for client work and tasks)
- Google Calendar API (for calendar events)
- Daily client work generator (creates Google Tasks)
- Performance monitoring agents (anomaly detection)

**Outputs to**:
- Email inbox (petere@roksys.co.uk)
- Local files: `briefing/YYYY-MM-DD-briefing.md` and `.html`

**Schedule**:
- Automatic: Daily at 7:00 AM via LaunchAgent
- Manual: Run anytime using this skill

---

## Quick Reference

**Command to run manually**:
```bash
cd /Users/administrator/Documents/PetesBrain && \
GMAIL_USER="petere@roksys.co.uk" \
GMAIL_APP_PASSWORD="pxmsoxiwuazkqhvg" \
ANTHROPIC_API_KEY="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" \
python3 agents/reporting/daily-briefing.py
```

**Or use the wrapper script** (if created):
```bash
./shared/scripts/send-daily-summary.sh
```

---

## Related Documentation

- `agents/reporting/daily-briefing.py` - Main script
- `shared/scripts/daily-client-work-generator.py` - Client work generator
- `docs/TASK-INTEGRATION-ARCHITECTURE.md` - Google Tasks integration
- `docs/DAILY-BRIEFING-SYSTEM.md` - Full system documentation

---

**Status**: ✅ Production Ready  
**Owner**: Peter Empson  
**Frequency**: Daily (automatic at 7 AM, manual anytime)

