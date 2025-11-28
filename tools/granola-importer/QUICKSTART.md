# Quick Start Guide - Granola Meeting Importer

Get your Granola meetings automatically imported in 5 minutes!

## Prerequisites

- ✅ Granola AI desktop app installed and logged in
- ✅ Python 3 installed on your Mac
- ✅ Existing client folders in `clients/` directory

## Step 1: Install Dependencies

```bash
cd tools/granola-importer

# Create virtual environment (already done)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install packages (already done)
pip install -r requirements.txt
```

## Step 2: Test API Connection

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Test Granola API connection
python3 granola_api.py
```

You should see:
```
✓ Successfully authenticated with Granola API
✓ Credentials loaded from: /Users/[you]/Library/Application Support/Granola/supabase.json
✓ Fetched 5 recent meetings:
  1. Meeting Title (2025-10-28T10:30:00Z)
  ...
```

## Step 3: Test Client Detection

```bash
python3 client_detector.py
```

You should see all your clients listed and test results showing successful matching.

## Step 4: Import Your First Meeting

```bash
# Import meetings from the last 7 days
python3 import_meeting.py --days 7
```

You'll see output like:
```
🔍 Fetching meetings from last 7 days...
   Found 3 meetings

📄 Processing: 'Bright Minds Q4 Strategy Review'
   ✓ Detected client: Bright Minds (100% via title)
   ✓ Saved to: /path/to/clients/bright-minds/meeting-notes/2025-10-28-q4-strategy-review-bright-minds.md

✓ Imported 3 meetings from last 7 days
```

## Step 5: Check Your Files

```bash
# View imported meetings
ls -la clients/bright-minds/meeting-notes/

# View a meeting file
cat clients/bright-minds/meeting-notes/2025-10-28-q4-strategy-review-bright-minds.md
```

## Step 6: Start Automatic Sync (Optional)

For fully automated import, install the background sync daemon:

```bash
# Install as macOS service (starts on login)
./install_service.sh
```

Or run manually in a terminal:

```bash
source venv/bin/activate
python3 sync_daemon.py
```

The daemon will:
- Check for new meetings every 5 minutes
- Automatically detect and assign clients
- Log activity to `~/.petesbrain-granola-importer.log`

## Viewing Logs

```bash
# View daemon logs
tail -f ~/.petesbrain-granola-importer.log

# View import history
cat .import_history.json
```

## Common Commands

```bash
# Import specific meeting by ID
python3 import_meeting.py --meeting-id "abc123xyz"

# Import last 30 days (limit 10 meetings)
python3 import_meeting.py --days 30 --limit 10

# Import all new meetings
python3 import_meeting.py --all

# Run daemon once (test without loop)
python3 sync_daemon.py --once

# Custom check interval (10 minutes)
python3 sync_daemon.py --interval 600
```

## Troubleshooting

### Can't find Granola credentials

**Error**: `FileNotFoundError: Granola credentials not found`

**Fix**:
1. Make sure Granola desktop app is installed
2. Log into Granola app
3. Check credentials exist: `ls ~/Library/Application\ Support/Granola/supabase.json`

### Meeting saved to _unassigned

**Reason**: Title and content didn't match any client

**Fix**:
1. Check the meeting in `clients/_unassigned/meeting-notes/`
2. Manually move to correct client folder
3. Use more specific meeting titles that include client names
4. Mention client name early in meetings

### Dependencies not found

**Error**: `ModuleNotFoundError: No module named 'requests'`

**Fix**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## What's Next?

- Check `clients/_unassigned/` for any meetings that need manual assignment
- Review `README.md` for full documentation
- Read `TOOL_CLAUDE.md` for technical details
- Customize detection thresholds if needed

## Stopping the Service

```bash
# Stop background daemon
launchctl stop com.petesbrain.granola-importer

# Uninstall service completely
./uninstall_service.sh
```

## Support

- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Project Docs: See README.md and TOOL_CLAUDE.md
