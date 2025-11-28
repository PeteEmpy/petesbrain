# Daily Task Generator Setup

Automatically generates a daily to-do list in Google Tasks from recent meeting action items.

## Features

- Scans all meeting notes from the last 7 days
- Extracts action items assigned to Peter or general team tasks
- Creates organized tasks in Google Tasks by client
- Runs automatically every morning at 8:00 AM
- Includes meeting context (title, date, file location) in task notes

## Prerequisites

1. **Google Tasks MCP Server** must be configured in `.mcp.json`
2. **Claude Code must be restarted** after adding the MCP server

## Installation

### 1. Install the LaunchAgent (Automatic Daily Execution)

```bash
# Copy the plist file to LaunchAgents directory
cp /Users/administrator/Documents/PetesBrain/tools/granola-importer/com.petesbrain.dailytasks.plist \
   ~/Library/LaunchAgents/

# Load the agent (starts automatically at 8am daily)
launchctl load ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist

# Verify it's loaded
launchctl list | grep dailytasks
```

### 2. Test Manual Execution

```bash
cd /Users/administrator/Documents/PetesBrain/tools/granola-importer
source venv/bin/activate
python3 generate_daily_tasks.py
```

## Usage

### Run Via Claude Code (with MCP Integration)

Once Claude Code is restarted with the Google Tasks MCP server loaded:

```bash
python3 generate_daily_tasks.py
```

This will:
1. Scan recent meetings (last 7 days)
2. Extract action items for Peter
3. Create tasks in Google Tasks with full context
4. Save a backup JSON file

### Run Standalone (without MCP)

The script can run without MCP tools for testing:

```bash
python3 generate_daily_tasks.py
```

This will:
1. Scan and extract action items
2. Display a summary report
3. Save to `daily-tasks.json` (but won't create Google Tasks)

## Configuration

### Change Scan Period

Edit `generate_daily_tasks.py`:

```python
# Default: 7 days
meetings = get_recent_meeting_notes(days=7)

# Change to 14 days
meetings = get_recent_meeting_notes(days=14)
```

### Change Schedule

Edit `com.petesbrain.dailytasks.plist`:

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>8</integer>  <!-- Change to desired hour (0-23) -->
    <key>Minute</key>
    <integer>0</integer>  <!-- Change to desired minute (0-59) -->
</dict>
```

Then reload:

```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
```

## Task Extraction Rules

The script extracts action items using these patterns:

1. **Explicit assignment**: "Peter: Do something"
2. **General team items**: Bullet points with no specific person mentioned
3. **Team assignments**: "Team: Do something"

## Output Files

- **daily-tasks.json**: Backup of all extracted action items
- **daily-tasks.log**: Stdout from automated runs
- **daily-tasks-error.log**: Errors from automated runs

## Troubleshooting

### Tasks Not Created in Google Tasks

**Problem**: Script runs but tasks don't appear in Google Tasks

**Solution**:
1. Restart Claude Code to load the Google Tasks MCP server
2. Verify MCP server is running: Check `.mcp.json` configuration
3. Test MCP tools manually via Claude Code

### No Action Items Found

**Problem**: Script finds meetings but no action items

**Solution**:
- Check that meetings have "Action Items", "Next Steps", or "Action Points" sections
- Verify action items are formatted as bullet points (- or *)
- Ensure some items are assigned to "Peter:" or are general team items

### LaunchAgent Not Running

**Problem**: Script doesn't run automatically at 8am

**Solution**:

```bash
# Check if loaded
launchctl list | grep dailytasks

# Check logs
tail -f /Users/administrator/Documents/PetesBrain/tools/granola-importer/daily-tasks.log
tail -f /Users/administrator/Documents/PetesBrain/tools/granola-importer/daily-tasks-error.log

# Reload agent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
```

## Uninstallation

```bash
# Unload the agent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist

# Remove the plist file
rm ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
```

## Example Output

```
================================================================================
DAILY TASK GENERATOR - Scanning recent meetings for action items
================================================================================

📅 Scanning meetings from the last 7 days...
   ✓ Found 3 recent meetings

🔍 Extracting action items for Peter...
   • smythson: Paid Search catch up (2025-10-28)
      Found 4 action item(s)
   • tree2mydoor: Gareth & Peter PPC Channel Meet (2025-10-27)
      Found 2 action item(s)

   ✓ Total action items found: 6

================================================================================
CREATING TASKS IN GOOGLE TASKS
================================================================================

   📋 Using task list: 'Client Action Items'

🏢 Creating 4 tasks for SMYTHSON...
   ✓ Created: [smythson] Create PMAX asset groups with Christmas images
   ✓ Created: [smythson] Move diary asset group to new campaign
   ...

✓ Successfully created 6 tasks
```
