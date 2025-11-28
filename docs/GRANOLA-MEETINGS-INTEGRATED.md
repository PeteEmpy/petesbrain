# Granola Meeting Imports Integrated into Weekly Summary

## Overview

The separate weekly meeting import summary email has been integrated into the main weekly summary report. This consolidation reduces email clutter and provides a more comprehensive view of the week.

## What Changed

### Before ❌

**Two separate weekly emails:**

1. **Monday 8:30 AM** - Main weekly summary
   - Strategic priorities
   - Client performance
   - Tasks for the week
   - AI news, KB updates

2. **Monday (separate time)** - Granola meeting import summary
   - List of meetings imported from Granola
   - Grouped by client
   - Warning for unassigned meetings

**Problem**: Two emails to read, duplicated effort, harder to get full weekly picture.

### After ✅

**Single comprehensive weekly email (Monday 8:30 AM):**

1. Strategic Priorities
2. Week Ahead - Tactical Tasks
3. **Meeting Notes Imported This Week** (NEW in main email!)
   - Automatically included from Granola
   - Grouped by client
   - Shows meeting count and filenames
   - Warns about unassigned meetings
4. Client Performance
5. Automated Industry Monitoring
6. AI News Highlights
7. Knowledge Base Additions

**Benefits**: Single email with complete weekly overview, less email clutter, better context.

## How It Works

### Data Flow

```
1. Granola App
   ↓ (auto-syncs meetings)

2. tools/granola-importer/.import_history.json
   ↓ (stores import records)

3. knowledge-base-weekly-summary.py
   ↓ (reads import history)
   ↓ (passes to Claude for summary)

4. Weekly Summary Email
   📧 Meeting imports included in comprehensive email
```

### Integration Points

**File**: `shared/scripts/knowledge-base-weekly-summary.py`

**New Function**: `get_granola_meeting_imports()`
- Reads `.import_history.json` from Granola importer
- Filters meetings from last 7 days
- Groups by client
- Formats for email display

**Data Structure**:
```python
{
    'total': 15,  # Total meetings imported
    'grouped': {
        'Devonshire Hotels': [
            {'filename': '2025-11-05-budget-discussion.md', 'time_display': 'Nov 05, 14:30'},
            {'filename': '2025-11-07-monthly-check-in.md', 'time_display': 'Nov 07, 10:00'}
        ],
        'Smythson': [
            {'filename': '2025-11-04-q4-strategy.md', 'time_display': 'Nov 04, 15:00'}
        ],
        '⚠️ Unassigned': [
            {'filename': '2025-11-06-unknown-client.md', 'time_display': 'Nov 06, 11:00'}
        ]
    },
    'has_unassigned': True  # Warning flag
}
```

### Email Display

The weekly summary email now includes a section like:

```html
📝 Meeting Notes Imported This Week

15 meetings automatically imported from Granola and saved to client folders

By Client:
• Devonshire Hotels (2 meetings)
  - 2025-11-05-budget-discussion.md (Nov 05, 14:30)
  - 2025-11-07-monthly-check-in.md (Nov 07, 10:00)

• Smythson (1 meeting)
  - 2025-11-04-q4-strategy.md (Nov 04, 15:00)

⚠️ Action Required: 1 meeting could not be automatically assigned to a client
Review clients/_unassigned/meeting-notes/ and organize manually
```

## LaunchAgent Changes

### Disabled

**File**: `~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist`

**Status**: Disabled (unloaded)

**Reason**: No longer needed - functionality integrated into main weekly summary

**Command used**:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist
```

### Still Active

**File**: `~/Library/LaunchAgents/com.petesbrain.kb-weekly-summary.plist`

**Schedule**: Monday 8:30 AM

**Now includes**: Meeting imports + all existing summary content

## Granola Importer Still Active

**File**: `~/Library/LaunchAgents/com.petesbrain.granola-google-docs-importer.plist`

**Status**: Still running (unchanged)

**Function**: Continues to sync Granola meetings → client folders

**Schedule**: Every 30 minutes

The importer daemon is unaffected - it continues to:
- Monitor Granola for new meetings
- Auto-assign to client folders
- Save import history to `.import_history.json`

Only the **separate weekly summary email** has been removed.

## Files Modified

### Modified
- `shared/scripts/knowledge-base-weekly-summary.py`
  - Added `get_granola_meeting_imports()` function
  - Updated `analyze_knowledge_base_with_claude()` to accept meeting_imports parameter
  - Added meeting imports to Claude prompt
  - Added "Meeting Notes Imported This Week" section to prompt instructions
  - Updated `main()` to get meeting imports and pass to analyzer

### Disabled (Not Deleted)
- `~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist`
  - Still exists on disk but unloaded from launchctl
  - Can be re-enabled if needed

### Unchanged
- `tools/granola-importer/email_reporter.py` - Still exists for other alerts
- `tools/granola-importer/.import_history.json` - Still used for tracking
- `~/Library/LaunchAgents/com.petesbrain.granola-google-docs-importer.plist` - Still syncing

### Created
- `docs/GRANOLA-MEETINGS-INTEGRATED.md` (this file)

## Testing

Test the integration:

```bash
cd /Users/administrator/Documents/PetesBrain

# Generate weekly summary with meeting imports
ANTHROPIC_API_KEY="..." \
/usr/local/bin/python3 shared/scripts/knowledge-base-weekly-summary.py
```

**Expected Output**:
```
📝 Loading Granola meeting imports...
  Found 15 meeting(s) imported this week
  ⚠️  Some meetings are unassigned - require manual review
```

**In Email**:
- New "Meeting Notes Imported This Week" section
- Grouped by client
- Shows filenames and timestamps
- Warning if unassigned meetings exist

## Unassigned Meetings Handling

### Detection

If meetings couldn't be auto-assigned to a client:
- `has_unassigned: True` flag is set
- Logged during weekly summary generation
- Displayed prominently in email

### Email Warning

The email includes a clear action item:

```
⚠️ Action Required
1 meeting could not be automatically assigned to a client.

What to do:
1. Review clients/_unassigned/meeting-notes/
2. Determine the correct client from meeting content
3. Move the file to appropriate client's meeting-notes/ folder
```

### Manual Review

Unassigned meetings are saved to:
```
/Users/administrator/Documents/PetesBrain/clients/_unassigned/meeting-notes/
```

Move them to the correct client:
```bash
# Example: Moving a meeting to smythson
mv clients/_unassigned/meeting-notes/2025-11-06-strategy.md \
   clients/smythson/meeting-notes/
```

## Benefits

### For You
1. **One Email Instead of Two** - Easier to manage inbox
2. **Complete Weekly Picture** - All information in one place
3. **Better Context** - See meetings alongside performance data and tasks
4. **Consistent Timing** - Everything arrives Monday 8:30 AM

### For System
1. **Simpler Architecture** - One email generation process
2. **Better Integration** - Meeting data can inform strategic priorities
3. **Less Maintenance** - One LaunchAgent instead of two
4. **More Cohesive** - Related information grouped together

## Rollback (If Needed)

To restore the separate weekly meeting email:

```bash
# Re-enable the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist

# Verify it's running
launchctl list | grep granola-weekly-summary
```

The plist file still exists and is unchanged, so rollback is simple.

## Future Enhancements

Potential improvements now that meeting data is in main summary:

1. **AI Analysis of Meeting Topics**
   - Identify common themes across client meetings
   - Highlight action items from meetings in task section
   - Cross-reference meeting notes with performance data

2. **Meeting-Performance Correlation**
   - "Smythson had 2 meetings this week and performance is up 15%"
   - Link budget discussions to actual budget changes

3. **Proactive Alerts**
   - "No meetings with Client X in 3 weeks - schedule check-in?"
   - "Meeting about budget increase but no budget change detected"

4. **Meeting Preparation**
   - Next week's meetings shown with relevant context
   - Pull recent performance data for upcoming calls

## Cost

No change in cost:
- Same Claude API calls (one weekly summary generation)
- Meeting import data adds ~100-200 tokens to prompt
- Marginal cost: ~$0.0001 per week

## Summary

The Granola meeting import summary has been successfully integrated into the main weekly summary email. You'll now receive:

- ✅ One comprehensive email instead of two
- ✅ Meeting imports included automatically
- ✅ Better weekly overview with all context
- ✅ Warnings for unassigned meetings
- ✅ Simpler system architecture

The separate weekly meeting summary email is disabled but can be easily re-enabled if needed.

Next Monday's weekly summary will include your meeting imports automatically!
