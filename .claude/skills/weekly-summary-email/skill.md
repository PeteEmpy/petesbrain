---
name: weekly-summary-email
description: Sends weekly business summary email with strategic priorities, performance data, meeting notes, and knowledge base updates. Use when user says "send weekly summary", "weekly briefing", "generate weekly summary", or wants to manually trigger the weekly business report.
allowed-tools: Bash, Read
---

# Weekly Summary Email Skill

---

## Core Workflow

When this skill is triggered:

### 1. Verify Prerequisites

Check that environment variables are available:
- `ANTHROPIC_API_KEY` - For AI analysis and summary generation

**Note**: Weekly summary uses Gmail API (not SMTP), so it doesn't need `GMAIL_USER` or `GMAIL_APP_PASSWORD` - it authenticates via OAuth.

### 2. Execute Weekly Summary Script

Run the weekly business summary generator:

```bash
cd /Users/administrator/Documents/PetesBrain
export ANTHROPIC_API_KEY="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"
/usr/local/bin/python3 agents/reporting/kb-weekly-summary.py
```

### 3. What the Script Does

The weekly summary script:
1. **Gathers knowledge base documents** - New documents from last 7 days:
   - google-ads
   - ai-strategy
   - analytics
   - industry-insights
   - rok-methodologies
2. **Fetches upcoming tasks** - Tasks due in the week ahead from Google Tasks
3. **Generates weekly client strategy** - Runs `weekly-client-strategy-generator.py`:
   - Analyzes all 17 clients for strategic priorities
   - Checks weekend plans (Friday-Sunday) for context
   - Generates 2-4 strategic priorities per client
   - Classifies by type (reporting, optimization, planning, etc.)
4. **Gets client performance data** - Last week's performance trends
5. **Loads Granola meeting imports** - Meetings imported from Granola this week
6. **Analyzes with Claude** - AI-powered analysis of all content
7. **Creates HTML email** - Formatted email with all sections
8. **Sends via Gmail API** - Authenticates via OAuth and sends to petere@roksys.co.uk

### 4. Email Content Structure

**Subject**: "📊 Weekly Business Summary & Week Ahead - [Date Range]"

**Sections**:
1. **Strategic Priorities** - AI-generated priorities for each client (2-4 per client)
2. **Upcoming Tasks** - Tasks due in the week ahead
3. **Performance Data** - Last week's client performance trends
4. **Meeting Notes** - Granola imports from this week
5. **Knowledge Base Updates** - New documents added
6. **Key Insights** - AI-generated takeaways and actionable items

### 5. Expected Output

**Success indicators**:
- ✅ Email sent successfully! Message ID: [ID]
- Log messages showing each section loaded

**If no content**:
- Script will skip sending if no new content or upcoming tasks
- Message: "⚠️  No new content or upcoming tasks. Skipping email."

### 6. Troubleshooting

**If authentication fails**:
- Gmail API OAuth token may need refresh
- Check `shared/mcp-servers/google-tasks-mcp-server/token.json` exists
- May need to re-authenticate OAuth flow

**If no content generated**:
- Check if knowledge base has new documents
- Verify weekly strategy generator ran successfully
- Check if there are upcoming tasks in Google Tasks

**If email not sent**:
- Verify Gmail API credentials are valid
- Check OAuth token hasn't expired
- Review error logs for specific issues

---

## Integration Notes

**Works with**:
- Weekly client strategy generator (`shared/scripts/weekly-client-strategy-generator.py`)
- Google Tasks MCP (for upcoming tasks)
- Google Calendar API (for weekend plan detection)
- Granola importer (for meeting notes)
- Knowledge base system (for new documents)

**Outputs to**:
- Email inbox (petere@roksys.co.uk)
- Uses Gmail API (not SMTP)

**Schedule**:
- Automatic: Every Monday at 8:30 AM via LaunchAgent
- Manual: Run anytime using this skill

**Note**: Weekly summary is separate from weekly news digest (which covers industry news and AI newsletters)

---

## Quick Reference

**Command to run manually**:
```bash
cd /Users/administrator/Documents/PetesBrain && \
ANTHROPIC_API_KEY="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" \
python3 agents/reporting/kb-weekly-summary.py
```

**Or use the wrapper script** (if created):
```bash
./shared/scripts/send-weekly-summary.sh
```

---

## Related Documentation

- `agents/reporting/kb-weekly-summary.py` - Main script
- `shared/scripts/weekly-client-strategy-generator.py` - Strategy generator
- `docs/IMPROVED-WEEKLY-SUMMARY.md` - Weekly summary system documentation
- `shared/docs/WEEKLY-EMAIL-SPLIT-SUMMARY.md` - Business vs News split

---

## Weekly Summary vs Weekly News Digest

**Weekly Business Summary** (this skill):
- Strategic priorities
- Tasks and deliverables
- Performance data
- Meeting notes
- Knowledge base updates

**Weekly News Digest** (separate):
- Industry news (Google Ads, etc.)
- AI newsletters
- Automated news monitoring
- Runs separately at 9:30 AM Mondays

---

**Status**: ✅ Production Ready  
**Owner**: Peter Empson  
**Frequency**: Weekly (automatic Monday 8:30 AM, manual anytime)

