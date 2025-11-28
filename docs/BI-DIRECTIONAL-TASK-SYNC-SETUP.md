# Bi-Directional Task Sync - Setup Guide

## Quick Start

### 1. Install LaunchAgent for Local → Google Sync

The sync script needs to run periodically to sync local changes to Google Tasks:

```bash
# Copy LaunchAgent to your LaunchAgents directory
cp agents/launchagents/com.petesbrain.sync-todos-to-google-tasks.plist \
   ~/Library/LaunchAgents/

# Load the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.petesbrain.sync-todos-to-google-tasks.plist

# Verify it's loaded
launchctl list | grep petesbrain.sync-todos
```

### 2. Verify Tasks Monitor is Running

The Google → Local sync runs automatically via tasks-monitor:

```bash
# Check if tasks-monitor is loaded
launchctl list | grep petesbrain.tasks-monitor

# If not loaded, load it:
launchctl load ~/Library/LaunchAgents/com.petesbrain.tasks-monitor.plist
```

### 3. Test the Sync

**Test Google → Local:**
1. Complete a task in Google Tasks
2. Wait for tasks-monitor to run (or run manually):
   ```bash
   python3 agents/system/tasks-monitor.py
   ```
3. Check local todo file - status should update

**Test Local → Google:**
1. Edit a local todo file:
   - Change status to `- [x] Completed`
   - Or change title/notes
2. Run sync script:
   ```bash
   python3 agents/system/sync-todos-to-google-tasks.py
   ```
3. Check Google Tasks - should reflect changes

## Sync Frequency

- **Google → Local**: Every 1 hour (via tasks-monitor)
- **Local → Google**: Every 1 hour (via sync-todos LaunchAgent)

Both sync scripts run hourly for near real-time synchronization.

## Manual Sync

Run either script manually anytime:

```bash
# Sync Google Tasks → Local files
python3 agents/system/tasks-monitor.py

# Sync Local files → Google Tasks
python3 agents/system/sync-todos-to-google-tasks.py
```

