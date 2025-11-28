# Client CONTEXT.md Management Scripts

Scripts for managing client CONTEXT.md files in Pete's Brain.

---

## add-context-note.sh

**Purpose**: Add ad hoc notes to client CONTEXT.md files in a controlled, structured way.

### Quick Start

```bash
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/add-context-note.sh
```

Or create an alias in your `~/.bashrc` or `~/.zshrc`:

```bash
alias add-note='/Users/administrator/Documents/PetesBrain/shared/scripts/add-context-note.sh'
```

Then just run:
```bash
add-note
```

### How It Works

The script provides an interactive menu to:

1. **Select a client** from list of all active clients
2. **Choose a section** to add the note to:
   - Strategic Context
   - Client Preferences
   - Business Context
   - Known Issues
   - Key Learnings
   - Campaign Notes
   - Action Items
   - Quick Reference
   - General (Ad Hoc Notes)

3. **Enter your note** (multi-line supported - press Ctrl+D when done)

4. **Auto-updates**:
   - Adds timestamp to note
   - Updates "Last Updated" date
   - Adds entry to Document History table
   - Creates backup (.backup file)

### Example Session

```bash
$ ./add-context-note.sh

═══════════════════════════════════════════════════
   Add Note to Client CONTEXT.md
═══════════════════════════════════════════════════

Available clients:

1) Accessories For The Home
2) Bright Minds
3) Tree2mydoor
...

Select client number (or 'q' to quit): 3

Adding note for: Tree2mydoor

Which section should this note be added to?

1) Strategic Context - Strategy decisions, approach changes
2) Client Preferences - Communication style, sensitivities discovered
3) Business Context - Product changes, pricing, website updates
4) Known Issues - Current problems or challenges
5) Key Learnings - What works, what doesn't, insights discovered
6) Campaign Notes - Campaign-specific observations
7) Action Items - Tasks or reminders
8) Quick Reference - Links, contacts, important info
9) General Note - Add to end of file

Select section number: 4

Enter your note (press Ctrl+D when finished):
---
Client mentioned stock issues with Mini Myrtle - temporarily pausing that product from campaigns until restocked in 2 weeks.
^D

✓ Note added successfully!

Location: /Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md
Section: ## Known Issues & Challenges
Backup saved: /Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md.backup
```

### What Gets Added

The note will appear in the selected section with timestamp:

```markdown
## Known Issues & Challenges

**Note added 2025-10-28**:
Client mentioned stock issues with Mini Myrtle - temporarily pausing that product from campaigns until restocked in 2 weeks.
```

And an entry in the Document History table:

```markdown
| 2025-10-28 | Ad hoc note added to Known Issues & Challenges | User (via add-context-note.sh) |
```

### Safety Features

- **Automatic backup**: Original file saved as `.backup` before changes
- **Timestamp tracking**: Every note includes date for reference
- **Document history**: All changes logged in history table
- **No data loss**: Appends only - never deletes existing content

### When to Use

Use `add-context-note.sh` when you:
- Have a quick insight or observation to capture
- Learn something important in a call or email
- Want to add context without opening the full file
- Need to quickly log a decision or change

### Alternative Methods

You can also add notes by:

1. **Directly editing CONTEXT.md** in any text editor (for longer updates)
2. **Asking Claude** to update CONTEXT.md (Claude will automatically update when analyzing clients)
3. **Email/Meeting import** (Claude extracts context automatically)

---

## Best Practices

### What to Add to CONTEXT.md

**DO add**:
- Strategic decisions ("Client wants to focus on brand campaigns for Q4")
- Client preferences discovered ("Prefers weekly check-ins, not monthly")
- Business changes ("Launching new product line next month")
- Important insights ("Memorial products perform 2x better than celebration")
- Technical issues discovered ("Conversion tracking broken on mobile checkout")

**DON'T add**:
- Day-to-day task notes (use a separate task manager)
- Temporary information that will be irrelevant soon
- Information already captured elsewhere (don't duplicate)

### Keep It Updated

- Add notes immediately after calls/meetings
- Review and clean up quarterly
- Cross-reference with experiment log entries
- Update when strategy changes

---

## Troubleshooting

### Script not found
```bash
# Make sure you're in the right directory
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/add-context-note.sh
```

### Permission denied
```bash
chmod +x /Users/administrator/Documents/PetesBrain/shared/scripts/add-context-note.sh
```

### Note didn't save correctly
- Check the `.backup` file - your original is safe
- Copy content from backup if needed
- Report issue if problem persists

---

---

## review-meeting-client.sh

**Purpose**: Review and correct client assignment for meeting notes imported by Granola.

### Quick Start

```bash
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/review-meeting-client.sh
```

Or create an alias:
```bash
alias review-meetings='/Users/administrator/Documents/PetesBrain/shared/scripts/review-meeting-client.sh'
```

### How It Works

The Granola meeting importer does its best to detect which client a meeting is about, but it's not always accurate. This script helps you review and correct assignments.

**Process**:
1. Shows all meetings from last 7 days
2. You select one to review
3. Shows preview of meeting content
4. Options:
   - Move to different client
   - Move to roksys (company meeting)
   - Keep as is
   - Cancel

### When to Use

Run this weekly or after importing meetings to:
- Fix incorrectly assigned meetings
- Move company/internal meetings to roksys
- Ensure meetings are in the right client folders

### Example

```bash
$ ./review-meeting-client.sh

Recent meetings (last 7 days):

1) 2025-10-27 - accessories-for-the-home
   2025-10-27-30-min-meeting-between-mike-rhodes-and-peter...

Enter meeting number to review: 1

[Shows preview]

What would you like to do?
1) Move to different client
2) Move to roksys (company meeting)
3) Keep as is
4) Cancel

Select option: 2

✓ Moved to roksys/meeting-notes/
```

---

## weekly-meeting-review.py

**Purpose**: Automatically analyze recent meetings, extract actionable insights, and send a comprehensive weekly summary email.

### Overview

This automated system:
- Scans all client and company meeting notes from the last 7 days
- Uses Claude API to analyze each meeting for:
  - Key decisions and action items
  - Strategic insights and changes in direction
  - Client concerns or requests
  - Performance discussions
  - Budget or timeline changes
- Creates tasks in Google Tasks for identified action items
- Generates a structured HTML email report
- Sends the report to petere@roksys.co.uk every Monday at 9:00 AM

### How It Works

**Automated Process**:
1. Every Monday at 9 AM, launchd triggers the script
2. Script finds all meetings modified in last 7 days from:
   - `clients/*/meeting-notes/` (client meetings)
   - `roksys/meeting-notes/` (company meetings)
3. For each meeting:
   - Reads meeting notes and full transcript
   - Sends to Claude API for analysis
   - Claude extracts:
     * Key decisions made
     * Action items and deliverables
     * Strategic insights
     * Client concerns or requests
     * Performance discussions
     * Timeline or budget changes
4. Creates tasks in Google Tasks for action items with:
   - Task title from action item
   - Due date (if mentioned)
   - Notes with context from meeting
5. Generates structured HTML email with:
   - Executive summary of the week
   - Per-meeting analysis sections
   - Action items with assignments
   - Strategic insights by client
   - Color coding (blue for client, purple for company)
6. Sends report via Gmail API

**Email Report Includes**:
- Total meeting count
- Analyzed insights for each meeting
- Consolidated action items list
- Strategic recommendations
- Links to meeting notes for reference

### Setup & Testing

**Prerequisites**:
- Anthropic API key in `~/.bashrc` or `~/.zshrc`: `export ANTHROPIC_API_KEY='sk-ant-...'`
- Gmail API credentials configured (service account or OAuth2)
- Google Tasks API setup via MCP server

**First Time Setup**:
```bash
# Test the script manually first to authenticate
cd /Users/administrator/Documents/PetesBrain
GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
  shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

This will:
1. Find recent meetings
2. Analyze each meeting using Claude API
3. Create tasks in Google Tasks for action items
4. Generate the summary report
5. Prompt for Gmail authentication (one-time if needed)
6. Send test email to petere@roksys.co.uk

**Enable Automated Weekly Reports**:
```bash
# Load the launchd job (runs every Monday 9 AM)
launchctl load ~/Library/LaunchAgents/com.roksys.weekly-meeting-review.plist

# Check if it's loaded
launchctl list | grep weekly-meeting-review

# View logs
cat /Users/administrator/Documents/PetesBrain/roksys/spreadsheets/weekly-meeting-review.log
cat /Users/administrator/Documents/PetesBrain/roksys/spreadsheets/weekly-meeting-review-error.log
```

**Disable Automated Reports**:
```bash
launchctl unload ~/Library/LaunchAgents/com.roksys.weekly-meeting-review.plist
```

**Run Manually** (outside of schedule):
```bash
shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

### Schedule Configuration

**Default Schedule**: Every Monday at 9:00 AM

To change the schedule, edit the plist file:
```bash
nano ~/Library/LaunchAgents/com.roksys.weekly-meeting-review.plist
```

**Example Schedules**:

Every Monday at 9 AM (current):
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key>
    <integer>1</integer>  <!-- 0=Sunday, 1=Monday, etc -->
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

Every Friday at 5 PM:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key>
    <integer>5</integer>
    <key>Hour</key>
    <integer>17</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

After editing, reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.roksys.weekly-meeting-review.plist
launchctl load ~/Library/LaunchAgents/com.roksys.weekly-meeting-review.plist
```

### What Gets Reported

**For Each Meeting**:
- Filename with date
- Current folder location (client name or "company")
- Participants list
- Modification date/time
- First 15 lines of content (excluding YAML frontmatter)

**Meeting Categories**:
- **Client meetings** (blue badge): In `clients/[client-name]/meeting-notes/`
- **Company meetings** (purple badge): In `roksys/meeting-notes/`

### Troubleshooting

**No email received**:
1. Check logs: `cat roksys/spreadsheets/weekly-meeting-review.log`
2. Check errors: `cat roksys/spreadsheets/weekly-meeting-review-error.log`
3. Verify launchd job loaded: `launchctl list | grep weekly-meeting-review`
4. Test manually: Run script directly to check for errors

**Authentication errors**:
```bash
# Re-authenticate by running manually
shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

This will prompt for Gmail authentication again if token expired.

**No meetings found**:
- Report will still be sent saying "No meetings found in last 7 days"
- This is normal if no meetings were added/modified recently

---

## Future Enhancements

Potential improvements:
- [ ] Support for adding to specific subsections in add-context-note
- [ ] Tag system for categorizing notes
- [ ] Search/filter notes by date or keyword
- [ ] Bulk note import from text file
- [ ] Integration with email sync to auto-extract insights
- [ ] Auto-detection of company vs client meetings based on keywords
- [ ] **Calendar integration for meeting validation**: Cross-reference meeting notes with Google Calendar events to help validate client assignments
  - Calendar event title may contain client name
  - Event description could have client context
  - Attendee email addresses might indicate client (e.g., client domain names)
  - Could auto-suggest correct client based on calendar metadata
  - Would require Google Calendar API setup (similar to Gmail API)
  - Could enhance both Granola import accuracy and weekly review validation

---

**Last Updated**: 2025-10-28
**Maintained By**: ROK Systems / Pete's Brain
