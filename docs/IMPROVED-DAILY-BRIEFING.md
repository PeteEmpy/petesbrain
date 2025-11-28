# Improved Daily Briefing System

## Overview

The daily briefing system has been completely overhauled to address the critical issue: **it wasn't generating work for all 12+ clients**.

Previously, the briefing would only show tasks from Google Tasks and meetings from the calendar. If a client had no explicit meeting or task, they would be invisible - even if they needed daily attention.

## What Changed

### Before ❌

The old system only showed:
- Calendar events (but OAuth scope was broken)
- Google Tasks (but OAuth scope was broken)
- Performance anomalies (reactive only)
- Recent meeting notes

**Result**: Briefings said "No events scheduled for today" and "No active tasks" when you had 12 clients to manage.

### After ✅

The new system:

1. **Analyzes every client proactively** using AI
2. **Generates specific, actionable tasks** for clients that need attention
3. **Prioritizes work** with P0 (urgent), P1 (high), P2 (normal) labels
4. **Provides time estimates** for each task
5. **Explains why** each task is needed today
6. **Fixed OAuth scopes** for Calendar and Tasks integration

## Architecture

### Components

#### 1. Client Work Generator (`daily-client-work-generator.py`)

**What it does:**
- Scans all clients in `/clients/` directory
- For each client, analyzes:
  - `CONTEXT.md` - current status, priorities, ongoing work
  - Recent meeting notes (last 7 days)
  - Recent performance alerts
  - Recent audit reports
- Uses Claude (Haiku) to determine 1-3 specific tasks needed TODAY
- Prioritizes tasks as P0/P1/P2 with time estimates
- Saves to `shared/data/daily-client-work.json`

**Example output:**
```json
{
  "client": "smythson",
  "task": "Review Q4 dashboard data and update budget pacing calculations",
  "priority": "P1",
  "time_estimate": "30 mins",
  "reason": "Dashboard was updated yesterday, need to verify calculations are working correctly"
}
```

#### 2. OAuth Re-authentication (`reauth-google-oauth.py`)

**What it does:**
- Re-authenticates Google OAuth with expanded scopes:
  - `https://www.googleapis.com/auth/tasks` (Tasks read/write)
  - `https://www.googleapis.com/auth/calendar.readonly` (Calendar read)
  - `https://www.googleapis.com/auth/gmail.readonly` (Gmail read - future use)
- Saves new token to `shared/mcp-servers/google-tasks-mcp-server/token.json`

**When to run:**
- First-time setup
- If you add new Google API scopes
- If OAuth token expires and can't auto-refresh

#### 3. Enhanced Daily Briefing (`daily-briefing.py`)

**What changed:**
- Now runs client work generator FIRST (before generating briefing)
- Includes new "🎯 Client Work Generated for Today" section
- Shows calendar events (now working with proper OAuth scopes)
- Shows Google Tasks (now working with proper OAuth scopes)
- Provides AI executive summary of the entire day

**Briefing structure:**
```
# Daily Briefing - Monday, November 10, 2025

## 🎯 Executive Summary
[AI-generated 2-3 sentence summary of the day]

### Calendar - Today
[All meetings and events from Google Calendar]

## 🎯 Client Work Generated for Today
[AI-analyzed work for all clients]

### 🔴 URGENT (P0)
[Critical tasks that must be done today]

### 🟡 HIGH PRIORITY (P1)
[Important tasks for today]

### ⚪ NORMAL PRIORITY (P2)
[Standard tasks for today]

## ⚠️ Client Alerts (Last 24 Hours)
[Performance anomalies, budget alerts, etc.]

## 📋 Tasks in Google Tasks
[Existing tasks from Google Tasks]

## 📊 Performance Overview
[Week-over-week trends]

## 👥 Recent Meetings
[Meetings from yesterday]

## 📝 AI Inbox Processing (Yesterday)
[Notes processed, tasks created, etc.]

## 🤖 Agent Status
[Health status of all LaunchAgents]

## 🔍 Recent Google Ads Audits
[Audits generated in last 7 days]
```

## Setup Instructions

### First-Time Setup

Run the setup script:

```bash
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/setup-improved-briefing.sh
```

This will:
1. Re-authenticate Google OAuth (opens browser)
2. Test the client work generator
3. Generate a test briefing

**Important**: During OAuth re-authentication, make sure to:
- Sign in with your `petere@roksys.co.uk` Google account
- Grant all requested permissions (Tasks, Calendar, Gmail)
- Click "Continue" if you see security warnings (this is your own OAuth app)

### Manual Components

If you need to run components individually:

#### Re-authenticate OAuth only:
```bash
/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py
```

#### Generate client work only:
```bash
ANTHROPIC_API_KEY="..." /usr/local/bin/python3 shared/scripts/daily-client-work-generator.py
```

#### Generate briefing only:
```bash
ANTHROPIC_API_KEY="..." \
GMAIL_USER="petere@roksys.co.uk" \
GMAIL_APP_PASSWORD="..." \
/usr/local/bin/python3 agents/reporting/daily-briefing.py
```

## Automation

### LaunchAgent Configuration

The daily briefing runs automatically via:
```
~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist
```

**Schedule**: Every day at 7:00 AM

**What it runs**:
1. Client work generator (analyzes all clients)
2. Daily briefing generator (includes calendar, tasks, client work)
3. Email sender (sends briefing to your inbox)

### Logs

Check logs if something goes wrong:

```bash
# Main briefing log
tail -f ~/.petesbrain-daily-briefing.log

# Error log
tail -f ~/.petesbrain-daily-briefing-error.log
```

## How Client Work Analysis Works

The AI analysis considers multiple factors:

### 1. Client Context (`CONTEXT.md`)

Example priorities extracted:
- "Budget increase needed for Q4"
- "Testing new ad copy variants"
- "Performance trending down this week"
- "Awaiting client approval on campaign changes"

### 2. Recent Meetings

Looks for action items like:
- "Peter: Review performance and send recommendations"
- "Follow up on budget discussion by Friday"

### 3. Performance Alerts

If a client had anomalies yesterday:
- "Spend spiked 40% above normal"
- "Conversion rate dropped below threshold"

### 4. Pending Audits

If an audit was generated in last 7 days:
- "Implement findings from weekly audit"
- "Review optimization recommendations"

### 5. Proactive Checks

Even if nothing specific is flagged:
- "Check budget pacing (currently at 82% for month at 70% elapsed)"
- "Review search terms and add negatives"
- "Monitor product feed status"

## Priority Levels

### P0 - Urgent (🔴)
- Client emergencies
- Budget overspend alerts
- Broken campaigns
- Missed deadlines
- Account suspensions

**Time expectation**: Handle immediately, within 1 hour

### P1 - High Priority (🟡)
- Meeting follow-ups due today
- Weekly optimization tasks
- Client requests
- Performance investigations
- Audit implementations

**Time expectation**: Complete today

### P2 - Normal Priority (⚪)
- Routine monitoring
- Proactive optimizations
- Documentation updates
- Long-term projects

**Time expectation**: Complete this week

## Time Estimates

The system provides time estimates for planning:
- "10 mins" - Quick check or review
- "30 mins" - Standard task (review + action)
- "1 hour" - In-depth analysis or optimization
- "2 hours" - Complex project work

**Pro tip**: Add up all P0 and P1 time estimates to see your minimum committed time for the day.

## Troubleshooting

### "No events scheduled for today" (but you have meetings)

**Cause**: OAuth token doesn't have Calendar scope

**Fix**:
```bash
/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py
```

### "No active tasks" (but you have Google Tasks)

**Cause**: OAuth token doesn't have Tasks scope or has wrong permissions

**Fix**:
```bash
/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py
```

### "No client work generated"

**Cause**: ANTHROPIC_API_KEY not set or client work generator failed

**Fix**:
```bash
# Check if ANTHROPIC_API_KEY is in LaunchAgent plist
cat ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist | grep ANTHROPIC

# Test client work generator manually
ANTHROPIC_API_KEY="..." /usr/local/bin/python3 shared/scripts/daily-client-work-generator.py
```

### OAuth errors: "insufficient authentication scopes"

**Cause**: Token was created with old scopes and needs refresh

**Fix**:
```bash
# Delete old token
rm shared/mcp-servers/google-tasks-mcp-server/token.json

# Re-authenticate
/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py
```

## API Usage & Costs

### Claude API Usage

The system makes these API calls daily:

1. **Client work generator**: 1 API call per client (15+ calls)
   - Model: Claude Haiku (cheapest, fastest)
   - Cost: ~$0.01 per day total
   - Tokens: ~500 output tokens per client

2. **Executive summary**: 1 API call
   - Model: Claude Haiku
   - Cost: ~$0.001 per call
   - Tokens: ~300 output tokens

**Total daily cost**: ~$0.01 - $0.02

### Google API Usage

- **Tasks API**: Read operations only (free tier)
- **Calendar API**: Read operations only (free tier)
- **Gmail API**: Not currently used (ready for future)

All Google API usage is well within free tier limits.

## Future Enhancements

Potential improvements:

1. **Learn from task completion patterns**
   - Track which suggested tasks actually get done
   - Improve prioritization based on completion history

2. **Client urgency scoring**
   - Assign each client an urgency score (0-100)
   - Dynamically adjust task priorities based on urgency

3. **Budget pacing integration**
   - Auto-generate tasks when budgets are under/over pacing
   - Calculate exact budget adjustments needed

4. **Email parsing integration**
   - Analyze recent client emails for urgency signals
   - Auto-generate tasks from client requests

5. **Performance trend detection**
   - Identify clients trending down before they become anomalies
   - Proactive optimization suggestions

6. **Meeting preparation**
   - Generate pre-meeting briefings for each client
   - Pull relevant performance data automatically

## Files Changed

### New Files
- `shared/scripts/daily-client-work-generator.py`
- `shared/scripts/reauth-google-oauth.py`
- `shared/scripts/setup-improved-briefing.sh`
- `docs/IMPROVED-DAILY-BRIEFING.md` (this file)

### Modified Files
- `agents/reporting/daily-briefing.py`
  - Added `get_client_work_for_today()` function
  - Updated briefing template to include client work section
  - Added client work generator subprocess call

### Data Files Created
- `shared/data/daily-client-work.json` (generated daily)
  - Contains AI-analyzed tasks for all clients
  - Used by daily briefing

## Support

If you encounter issues:

1. Check logs: `~/.petesbrain-daily-briefing.log`
2. Verify OAuth: `/usr/local/bin/python3 shared/google_calendar_client.py`
3. Test client work generator manually
4. Re-run setup script: `./shared/scripts/setup-improved-briefing.sh`

For OAuth issues, the most common fix is simply re-authenticating with the correct scopes.
