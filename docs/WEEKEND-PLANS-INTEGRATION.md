# Weekend Plans Calendar Integration

## Overview

The weekly summary system now automatically checks your Google Calendar for weekend plans and adjusts the weekly briefing accordingly.

## How It Works

### Automatic Detection

Every Monday at 8:30 AM when the weekly summary runs:

1. **Checks Calendar**: Scans **entire Friday** (00:00) through Sunday 11:59pm
   - Covers early finishes on Friday
   - Covers taking the whole Friday off
   - Covers weekend travel/holidays
2. **Looks for Keywords**: holiday, vacation, away, break, grasmere, lake district, travel, trip
3. **Detects All-Day Events**: Common pattern for holidays/time off
4. **Saves Context**: Stores weekend plans in `weekly-client-strategy.json`

### Email Display

If weekend plans are detected, the weekly summary email includes:

**At the top of the email:**
```
⚠️ WEEKEND PLANS NOTICE
Weekend Plans: Grasmere
Recommendation: Aim to finish by lunchtime Friday (Nov 15) to allow for travel/preparation.
Plan high-impact priorities for Monday-Thursday!
```

This helps you:
- Know when to front-load work
- Plan to finish early Friday
- Prioritize high-impact work for early in the week
- Maintain work-life balance

## Keywords Detected

The system looks for these keywords in calendar events:

**Holidays & Time Off:**
- holiday
- vacation
- away
- break

**Specific Locations:**
- grasmere
- lake district
- travel
- trip

## Example Calendar Events

Events that WILL trigger the notice:
- "Grasmere Weekend"
- "Lake District Holiday"
- "Away - Family Time"
- "Vacation"
- Any all-day event Friday-Sunday

Events that WON'T trigger:
- "Dinner with friends" (no keywords)
- "Birthday party" (no keywords)
- Regular meetings

## Data Flow

```
1. weekly-client-strategy-generator.py
   ↓ (checks Google Calendar)
   ↓ (detects weekend plans)
   ↓ (saves to JSON)

2. weekly-client-strategy.json
   {
     "weekend_plans": {
       "has_plans": true,
       "friday_date": "Nov 15",
       "summary": "Grasmere",
       "all_plans": [...]
     }
   }

3. knowledge-base-weekly-summary.py
   ↓ (reads JSON)
   ↓ (passes to Claude)
   ↓ (generates email with prominent notice)

4. Weekly Summary Email
   📧 Weekend Plans Notice displayed at top
```

## OAuth Permissions

The system uses the same Google Calendar OAuth token as the daily briefing.

**Required Scope:**
- `https://www.googleapis.com/auth/calendar.readonly`

This scope is already included in the MCP Google Tasks server token at:
```
/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/token.json
```

No additional authentication needed!

## Manual Testing

Test weekend detection manually:

```bash
cd /Users/administrator/Documents/PetesBrain

# Run strategy generator (includes weekend check)
ANTHROPIC_API_KEY="..." \
/usr/local/bin/python3 shared/scripts/weekly-client-strategy-generator.py

# Check output
cat shared/data/weekly-client-strategy.json | grep -A 10 "weekend_plans"
```

**Expected Output (with plans):**
```
📅 Checking calendar for weekend plans...
   🏖️  Weekend plans found: Grasmere
   ⚠️  Consider finishing by lunchtime Friday (Nov 15)
```

**Expected Output (no plans):**
```
📅 Checking calendar for weekend plans...
   ✓ No weekend plans detected - full week available
```

## Adding New Keywords

To detect additional keywords, edit:

**File:** `shared/scripts/weekly-client-strategy-generator.py`

**Line 77:**
```python
keywords = ['holiday', 'vacation', 'away', 'break', 'grasmere', 'lake district', 'travel', 'trip']
```

Simply add your keywords to the list!

## Files Modified

### Created
- `docs/WEEKEND-PLANS-INTEGRATION.md` (this file)

### Modified
- `shared/scripts/weekly-client-strategy-generator.py`
  - Added `get_weekend_plans()` function
  - Calendar query from Friday 5pm through Sunday
  - Keyword detection
  - JSON output includes weekend context

- `shared/scripts/knowledge-base-weekly-summary.py`
  - Extracts weekend plans from strategy JSON
  - Passes weekend context to Claude prompt
  - Instructs Claude to display prominent notice
  - Section 0: Weekend Plans Notice (new)

- `docs/IMPROVED-WEEKLY-SUMMARY.md`
  - Added weekend plans documentation
  - Updated architecture section
  - New email structure section

## Benefits

1. **Work-Life Balance**: Automatically reminds you to plan for early Friday finish
2. **Better Planning**: Encourages front-loading high-impact work
3. **No Manual Tracking**: Just add events to family calendar as normal
4. **Flexible Keywords**: Detects various types of time off
5. **Zero Configuration**: Works automatically once set up

## Example Scenarios

### Scenario 1: Grasmere Weekend (This Week's Example)

**Calendar Event:** "Grasmere Weekend" (Friday-Sunday, all-day)

**Email Display:**
```
⚠️ WEEKEND PLANS NOTICE
Weekend Plans: Grasmere Weekend
Recommendation: Aim to finish by lunchtime Friday (Nov 15)
```

**Result:** You see this Monday morning and plan to complete high-impact priorities by Thursday.

### Scenario 2: No Plans

**Calendar:** No events matching keywords

**Email Display:** No weekend notice section

**Result:** Standard weekly summary, full week available

### Scenario 3: Multiple Events

**Calendar:**
- "Lake District Holiday" (Saturday-Sunday)
- "Dinner reservation" (Friday evening)

**Email Display:**
```
⚠️ WEEKEND PLANS NOTICE
Weekend Plans: Lake District Holiday
Recommendation: Aim to finish by lunchtime Friday (Nov 15)
```

**Result:** Shows the holiday event (keyword match), ignores dinner

## Cost

No additional cost - uses existing:
- Google Calendar API (free tier, read-only)
- OAuth token (already set up)
- Claude API calls (same weekly summary call)

## Troubleshooting

### "No weekend plans detected" but you have plans

**Cause:** Event doesn't contain recognized keywords

**Fix:** Either:
1. Update calendar event to include keyword (e.g., "Grasmere Weekend Holiday")
2. Add new keywords to `weekly-client-strategy-generator.py` line 77

### "Could not check calendar" error

**Cause:** OAuth token missing Calendar scope

**Fix:**
```bash
/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py
```

### Weekend plans in JSON but not in email

**Cause:** `knowledge-base-weekly-summary.py` not reading weekend context

**Fix:** Check the script is using the latest version:
```bash
grep "weekend_context" shared/scripts/knowledge-base-weekly-summary.py
```

Should see: `weekend_context = ""`

## Future Enhancements

Potential improvements:
- Detect multi-day holidays (e.g., Christmas week)
- Adjust task priorities based on reduced week
- Calculate recommended hours per day
- Integration with daily briefing for Thursday/Friday reminders
- Support for half-day events
- Configurable finish times (not just lunchtime)

## Summary

This integration ensures you never miss planning for weekend time off. The system:
- ✅ Automatically checks calendar
- ✅ Detects weekend plans via keywords
- ✅ Displays prominent notice in email
- ✅ Recommends Friday lunchtime finish
- ✅ Helps maintain work-life balance
- ✅ Zero manual effort required

Just add events to your calendar as normal, and the weekly summary adapts automatically!
