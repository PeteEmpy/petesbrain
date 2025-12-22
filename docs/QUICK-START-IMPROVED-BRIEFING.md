# Quick Start: Improved Daily Briefing

## TL;DR

Your daily briefing was broken - it said "no tasks" when you have 17 clients needing attention.

**Fixed today:**
- ✅ AI now analyzes ALL clients daily (not just those with meetings)
- ✅ Generates specific, actionable tasks with priorities and time estimates
- ✅ Fixed Google Calendar and Tasks OAuth authentication
- ✅ Test run found **51 tasks across 17 clients** (7 urgent, 29 high-priority)

## Run Setup Now

```bash
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/setup-improved-briefing.sh
```

This will:
1. Re-authenticate Google OAuth (opens browser - **allow all permissions**)
2. Test the client work generator
3. Generate today's full briefing
4. Email it to you

**Time required**: 5 minutes

## What You'll Get

### Before (Broken)
```
Calendar - Today
❌ No events scheduled for today

Tasks for Today
❌ No active tasks

→ Result: Empty briefing when you have 17 clients to manage
```

### After (Fixed)
```
Calendar - Today
✅ 09:00 AM - Meeting with Devonshire Hotels
✅ 02:00 PM - Smythson Catch-up

🎯 Client Work Generated for Today

17/17 clients need attention today
51 tasks identified

🔴 URGENT (P0): 7 tasks

[clear-prospects] Verify Google Merchant Center product re-indexing
  • 30 mins - Critical ongoing issue with 89 products disapproved

[crowd-control] Verify Conversion Tracking Configuration
  • 1 hour - Only 54% of conversions being reported

[godshot] Audit Google Ads conversion tracking
  • 2 hours - 80% mismatch between Ads and WooCommerce sales

[otc] Pull October performance data
  • 1 hour - Client ultimatum about business survival

... and more

🟡 HIGH PRIORITY (P1): 29 tasks
⚪ NORMAL (P2): 15 tasks
```

## How It Works

Every morning at 7:00 AM, the system:

1. **Analyzes every client** using AI:
   - Reads their CONTEXT.md (current status, priorities)
   - Checks recent meetings (last 7 days)
   - Reviews performance alerts
   - Examines recent audits

2. **Generates 1-3 specific tasks per client**:
   - What to do (specific, actionable)
   - Priority level (P0/P1/P2)
   - Time estimate (10 mins to 2 hours)
   - Why it's needed today

3. **Emails you a comprehensive briefing**:
   - Calendar events (now working!)
   - Client work for all clients
   - Google Tasks
   - Performance alerts
   - AI executive summary

## Priority Levels

- **P0 (🔴)**: Do immediately - emergencies, critical issues
- **P1 (🟡)**: Do today - important work, client requests
- **P2 (⚪)**: Do this week - routine monitoring, proactive work

## Test It Right Now

Want to see what work is needed today?

```bash
cd /Users/administrator/Documents/PetesBrain

# Generate client work
ANTHROPIC_API_KEY="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" \
/usr/local/bin/python3 shared/scripts/daily-client-work-generator.py
```

This takes ~2 minutes and shows you exactly what needs doing for each client.

## Troubleshooting

### "Request had insufficient authentication scopes"

**Fix**: Re-authenticate OAuth
```bash
/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py
```

### "No client work generated"

**Fix**: Check ANTHROPIC_API_KEY is set in LaunchAgent
```bash
cat ~/Library/LaunchAgents/com.petesbrain.daily-briefing.plist | grep ANTHROPIC
```

### "No events scheduled" but you have meetings

**Fix**: Re-run setup (adds Calendar scope to OAuth)
```bash
./shared/scripts/setup-improved-briefing.sh
```

## Next Steps

After setup:

1. ✅ **Check your email** - you'll get the full briefing
2. ✅ **Review the P0 tasks** - handle these immediately
3. ✅ **Review the P1 tasks** - plan these for today
4. ✅ **Glance at P2 tasks** - plan these for the week

## What Changed

### Files Created
- `shared/scripts/daily-client-work-generator.py` - AI analyzes all clients
- `shared/scripts/reauth-google-oauth.py` - Fixes OAuth scopes
- `shared/scripts/setup-improved-briefing.sh` - One-command setup

### Files Modified
- `agents/reporting/daily-briefing.py` - Includes client work section

### How OAuth Changed
**Before**: Only Tasks scope (broken)
**After**: Tasks + Calendar + Gmail scopes (working)

## Cost

**Daily cost**: ~$0.01-0.02 in Claude API calls
- 17 clients × ~$0.001 per analysis = ~$0.02
- Uses Claude Haiku (cheapest, fastest model)

**Annual cost**: ~$7-10

Worth it to have 51 prioritized tasks instead of "no tasks" 😊

## Full Documentation

See [IMPROVED-DAILY-BRIEFING.md](IMPROVED-DAILY-BRIEFING.md) for complete details.

## Run Setup Now!

Don't wait - fix your daily briefing system now:

```bash
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/setup-improved-briefing.sh
```

Takes 5 minutes. You'll get your first improved briefing in your inbox this evening or tomorrow morning.
