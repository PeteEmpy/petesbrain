# Daily Briefing System

**Created:** November 5, 2025  
**Status:** ✅ Active and Production-Ready  
**Source:** Adapted from Mike Rhodes' 8020Brain template

---

## Overview

Automated daily briefing system that provides a comprehensive morning summary every day at 7:00 AM, combining calendar events, client alerts, recent activities, and AI-generated priorities.

## Features

- 📅 **Calendar Integration** - Today's events (ready for Google Calendar API)
- ⚠️ **Client Alerts** - Performance anomalies from yesterday
- 📊 **Performance Overview** - Weekly trends and notable changes
- 👥 **Recent Meetings** - Meetings from yesterday/today
- ✅ **Completed Tasks** - Recent tasks from last 3 days
- 🤖 **AI Summary** - Claude-generated priority summary
- 📋 **Quick Links** - Fast access to key resources

---

## Quick Start

### View Today's Briefing

```bash
open ~/Documents/PetesBrain/briefing/$(date +%Y-%m-%d)-briefing.md
```

### Generate Briefing Manually

```bash
python3 ~/Documents/PetesBrain/agents/reporting/daily-briefing.py
```

### Check LaunchAgent Status

```bash
launchctl list | grep daily-briefing
```

---

## How It Works

### Schedule

- **When:** Daily at 7:00 AM
- **LaunchAgent:** `com.petesbrain.daily-briefing`
- **Script:** `agents/reporting/daily-briefing.py`

### Data Sources

1. **Client Anomalies** - `shared/data/daily-performance-anomalies.json`
2. **Weekly Performance** - `shared/data/weekly-client-performance.json`
3. **Completed Tasks** - `shared/data/tasks-completed.json`
4. **Meeting Notes** - `clients/*/meeting-notes/*.md`
5. **Calendar** - Google Calendar API (optional, not yet configured)

### Output

**Location:** `briefing/YYYY-MM-DD-briefing.md`  
**Format:** Markdown with emoji indicators  
**Size:** ~1-2 KB per briefing

---

## Briefing Structure

```markdown
# Daily Briefing - Weekday, Month DD, YYYY

## 🎯 Executive Summary
[AI-generated 2-3 sentence priority summary]

---

### Calendar - Today
[Today's calendar events]

---

## ⚠️ Client Alerts (Last 24 Hours)
[Performance anomalies and issues]

---

## 📊 Performance Overview
[Week trends and notable changes]

---

## 👥 Recent Meetings
[Meetings from yesterday/today]

---

## ✅ Recently Completed Tasks
[Last 5 completed tasks]

---

## 📋 Quick Links
[Links to agents, clients, knowledge base, etc.]
```

---

## Configuration

### LaunchAgent

**File:** `~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist`

**Key Settings:**
- **Schedule:** 7:00 AM daily
- **Python:** `/usr/local/bin/python3`
- **Script:** `/Users/administrator/Documents/PetesBrain/agents/reporting/daily-briefing.py`
- **Logs:** `~/.petesbrain-daily-briefing.log`

### Change Schedule

Edit the .plist file:

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>7</integer>      <!-- 0-23 -->
    <key>Minute</key>
    <integer>0</integer>       <!-- 0-59 -->
</dict>
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist
```

### Enable AI Summary

The briefing can generate an AI-powered executive summary using Claude.

**Requirements:**
1. Install anthropic package:
```bash
cd ~/Documents/PetesBrain
pip3 install anthropic
```

2. Add API key to LaunchAgent:
```bash
# Edit the .plist file
nano ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist

# Replace PLACEHOLDER with your actual key:
<key>ANTHROPIC_API_KEY</key>
<string>sk-ant-your-key-here</string>

# Reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist
```

### Enable Google Calendar Integration

**Optional:** Add Google Calendar API integration for calendar events.

**Steps:**
1. Set up Google Calendar API credentials
2. Save credentials to `shared/credentials/`
3. Uncomment calendar integration code in `daily-briefing.py`
4. Install google-api-python-client: `pip3 install google-api-python-client`

---

## Managing Briefings

### View Recent Briefings

```bash
ls -lt ~/Documents/PetesBrain/briefing/
```

### Open in Browser

```bash
# Convert to HTML and open
python3 -m markdown ~/Documents/PetesBrain/briefing/$(date +%Y-%m-%d)-briefing.md > /tmp/briefing.html
open /tmp/briefing.html
```

### Search Briefings

```bash
# Find briefings mentioning a client
grep -r "Smythson" ~/Documents/PetesBrain/briefing/

# Find anomaly alerts
grep -r "🔴" ~/Documents/PetesBrain/briefing/
```

### Archive Old Briefings

```bash
# Move briefings older than 30 days
find ~/Documents/PetesBrain/briefing/ -name "*.md" -mtime +30 -exec mv {} ~/Documents/PetesBrain/briefing/archive/ \;
```

---

## Troubleshooting

### Briefing Not Generated

**Check LaunchAgent status:**
```bash
launchctl list | grep daily-briefing
```

**Check logs:**
```bash
cat ~/.petesbrain-daily-briefing-error.log
```

**Manually run to see errors:**
```bash
cd ~/Documents/PetesBrain
python3 agents/reporting/daily-briefing.py
```

### Missing Data

**No anomalies showing:**
- Check `shared/data/daily-performance-anomalies.json` exists
- Ensure daily anomaly detector is running

**No tasks showing:**
- Check `shared/data/tasks-completed.json` format
- Tasks must be from last 3 days

**No meetings showing:**
- Meeting files must contain yesterday's or today's date in filename
- Must be in `clients/*/meeting-notes/*.md`

### AI Summary Not Working

**If showing "AI summary unavailable":**

1. Install anthropic package:
```bash
pip3 install anthropic
```

2. Add API key to LaunchAgent (see Configuration section)

3. Test manually:
```bash
export ANTHROPIC_API_KEY="your-key"
python3 agents/reporting/daily-briefing.py
```

---

## Customization

### Add Custom Sections

Edit `agents/reporting/daily-briefing.py` and add new functions:

```python
def get_custom_section():
    """Add your custom data here"""
    return "**Custom Section Content**\n"

# Then add to briefing_content:
custom_section = get_custom_section()
```

### Change Formatting

Modify the briefing template in `generate_briefing()` function.

### Filter Data

Adjust date ranges, client filters, or thresholds in the data retrieval functions.

---

## Integration with Other Systems

### Email Delivery

**Option 1: Add to weekly summary**

Briefings are already accessible to other agents, so they could be included in weekly summaries.

**Option 2: Standalone email**

Create a separate agent to email the daily briefing:

```python
# agents/reporting/email-daily-briefing.py
# Send today's briefing via email
```

### Slack/Discord Notifications

Could be extended to send briefings to Slack or Discord channels.

### Dashboard Integration

Briefings could be displayed in a web dashboard for quick morning review.

---

## Files Reference

### Scripts
- `agents/reporting/daily-briefing.py` - Main briefing generator

### LaunchAgents
- `~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist` - Daily automation

### Logs
- `~/.petesbrain-daily-briefing.log` - Standard output
- `~/.petesbrain-daily-briefing-error.log` - Errors

### Data Sources
- `shared/data/daily-performance-anomalies.json`
- `shared/data/weekly-client-performance.json`
- `shared/data/tasks-completed.json`
- `clients/*/meeting-notes/*.md`

### Output
- `briefing/YYYY-MM-DD-briefing.md` - Daily briefings

---

## Best Practices

1. **Review Daily** - Check briefing each morning at 7:00 AM
2. **Keep Archive** - Briefings are valuable historical record
3. **Update Data Sources** - Ensure all source systems are running
4. **Customize Sections** - Add/remove sections based on your needs
5. **Enable AI Summary** - Much more useful with Claude's insights

---

## Future Enhancements

### Planned Features

- [ ] Google Calendar integration
- [ ] Budget pacing alerts
- [ ] Client deadline reminders
- [ ] Upcoming campaign launches
- [ ] Yesterday's revenue summary
- [ ] Email delivery option
- [ ] HTML/PDF export
- [ ] Mobile-friendly format

### Nice to Have

- [ ] Weather forecast
- [ ] Industry news highlights
- [ ] Competitor alerts
- [ ] Team availability
- [ ] Birthday/anniversary reminders

---

## Comparison with Mike's System

### What We Adopted ✅

- Daily briefing concept
- Structured markdown format
- Multiple data sources
- AI-generated summary
- Calendar integration pattern

### What We Changed 🔄

- **Python vs Node.js** - Uses Python to match your ecosystem
- **Client-focused** - Emphasizes client alerts and performance
- **Operational data** - Pulls from your existing monitoring systems
- **Agency context** - Designed for marketing agency needs
- **Simple integration** - Works with existing data files

### What We Kept Yours 🎯

- Agent structure and organization
- Data source locations
- Briefing folder for outputs
- LaunchAgent automation
- Production-ready approach

---

## Related Documentation

- [8020Brain Analysis Report](8020BRAIN-ANALYSIS-REPORT.md) - Full template analysis
- [Agents Overview](../agents/README.md) - All automation agents
- [Automation System](AUTOMATION.md) - How automation works
- [Performance Monitoring](PERFORMANCE-MONITORING-COMPLETE.md) - Alert systems

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-05 | 1.0 | Initial daily briefing system created, adapted from Mike Rhodes' 8020Brain template |

---

**Success!** Your daily briefing system is now active. Check `briefing/` folder each morning for your comprehensive daily summary! ☀️

