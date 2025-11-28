# Weekly Email Split - Business vs News

## Summary

The weekly knowledge base email has been split into two separate emails:

1. **Weekly Business Summary** - Strategic priorities, tasks, performance, meetings
2. **Weekly News Digest** - Industry news, AI updates, newsletters

## Changes Made

### 1. Weekly Business Summary (`knowledge-base-weekly-summary.py`)

**What Changed:**
- Removed all automated news monitoring content (Google Ads news, AI news)
- Removed AI newsletters/emails section
- Updated email subject: "📊 Weekly Business Summary & Week Ahead"
- Updated email title: "📊 Weekly Business Summary"
- Simplified prompt to focus on business content only
- Updated footer to reference separate news digest

**What It Still Includes:**
- ✅ Weekly strategic priorities (AI-generated from client contexts)
- ✅ Upcoming tasks for the week ahead
- ✅ Client performance data from last week
- ✅ Meeting notes imported from Granola
- ✅ New knowledge base documents
- ✅ Key insights and actionable takeaways

**Schedule:**
- Runs every Monday at 8:30 AM
- LaunchAgent: `com.petesbrain.kb-weekly-summary`
- Script location: `/Users/administrator/Documents/PetesBrain/agents/reporting/kb-weekly-summary.py`

### 2. Weekly News Digest (`weekly-news-digest.py`) - NEW!

**What It Includes:**
- 📰 Google Ads industry news (automated monitoring)
- 🤖 AI news and updates (automated monitoring)
- 📧 AI newsletters and emails
- 📊 Relevance scores for all articles
- 🔗 Clickable links to all source articles
- 🌐 Full HTML expanded view with ALL articles

**Features:**
- Articles grouped by source and scored by relevance (1-10)
- Color-coded relevance badges:
  - 9-10: Green (highly relevant)
  - 7-8: Blue (relevant)
  - 5-6: Gray (somewhat relevant)
- Link at top of email to view full HTML version
- All article links preserved and clickable
- AI-powered summary of key themes and insights

**Schedule:**
- **TEST RUN**: Tomorrow (Nov 11) at 8:00 AM
- **Regular schedule**: Every Monday at 9:30 AM (1 hour after business summary)
- LaunchAgent: `com.petesbrain.weekly-news-digest`
- Script location: `/Users/administrator/Documents/PetesBrain/shared/scripts/weekly-news-digest.py`

## Benefits

1. **Focused Business Email**: Strategic priorities and performance without news clutter
2. **Comprehensive News Coverage**: All industry updates in one dedicated email
3. **Better Scanning**: Relevance scores help prioritize reading
4. **Full Access**: HTML view shows ALL articles without truncation
5. **Actionable Links**: Click through to any article source
6. **Reduced Overwhelm**: Separate news consumption from business planning

## Email Flow

**Test Run - Monday Nov 11:**
1. **8:00 AM**: Weekly News Digest (TEST) arrives
   - First test of the new separated news email
   - Includes all industry news and AI updates from last 7 days
   - Full HTML view with clickable links

**Regular Schedule - Every Monday:**
1. **8:30 AM**: Weekly Business Summary arrives
   - Review strategic priorities for the week
   - Check client performance trends
   - Plan tasks and deliverables

2. **9:30 AM**: Weekly News Digest arrives
   - Browse industry news at your convenience
   - Click through to interesting articles
   - Stay current on trends and updates

## File Locations

```
/Users/administrator/Documents/PetesBrain/
├── agents/reporting/
│   └── kb-weekly-summary.py           # Business summary (actively used)
├── shared/scripts/
│   ├── knowledge-base-weekly-summary.py   # Source (same as above)
│   └── weekly-news-digest.py         # News digest
└── ~/Library/LaunchAgents/
    ├── com.petesbrain.kb-weekly-summary.plist
    └── com.petesbrain.weekly-news-digest.plist
```

## Testing

To test the emails manually:

```bash
# Test business summary
ANTHROPIC_API_KEY="your-key" /Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 /Users/administrator/Documents/PetesBrain/agents/reporting/kb-weekly-summary.py

# Test news digest
ANTHROPIC_API_KEY="your-key" /Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 /Users/administrator/Documents/PetesBrain/shared/scripts/weekly-news-digest.py
```

## Logs

Check logs for troubleshooting:

```bash
# Business summary log
tail -f ~/.petesbrain-kb-weekly-summary.log

# News digest log
tail -f ~/.petesbrain-weekly-news-digest.log
```

## Notes

- Both emails sent to: petere@roksys.co.uk
- Both use Claude Sonnet 4.5 for AI analysis
- Both use same Gmail OAuth credentials
- Business summary triggers weekly strategy generator first
- News digest includes articles from last 7 days
