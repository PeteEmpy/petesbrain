# Deploy Universal Client Context Sync System

## Overview
Test and finalize the automated sync system that updates all 16 client Google Docs daily from CONTEXT.md files.

## What's Already Complete
✅ All 16 client Google Docs created
✅ Registry file: shared/data/client-google-docs.json (tracks all doc IDs)
✅ Universal sync script: shared/scripts/sync-all-client-contexts.sh
✅ Reference sheet: CLAUDE-AI-CUSTOM-INSTRUCTIONS.txt (for Claude.ai usage)

## Tasks to Complete

### 1. Test Universal Sync Script
```bash
cd /Users/administrator/Documents/PetesBrain
bash shared/scripts/sync-all-client-contexts.sh
```

**Expected behavior:**
- Reads all 16 clients from shared/data/client-google-docs.json
- Copies each CONTEXT.md to Google Drive Desktop sync folder
- Creates dated file: [Client Name]-CONTEXT-2025-11-08.md
- Creates symlink: [Client Name]-CONTEXT-LATEST.md
- Updates Google Doc automatically via Google Drive Desktop

**Check:**
- Files appear in: ~/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My Drive/PetesBrain-Context/
- Google Docs update with latest content (check 2-3 docs manually)
- Log file created at: ~/.petesbrain-client-contexts.log

### 2. Update LaunchAgent to Use Universal Script

**Current LaunchAgent:**
~/Library/LaunchAgents/com.petesbrain.tree2mydoor-context-upload.plist

**Action:** Update to use universal sync script instead of Tree2MyDoor-specific one

```bash
# 1. Unload current agent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.tree2mydoor-context-upload.plist

# 2. Edit the plist file - change ProgramArguments to:
#    <string>/Users/administrator/Documents/PetesBrain/shared/scripts/sync-all-client-contexts.sh</string>

# 3. Reload agent
launchctl load ~/Library/LaunchAgents/com.petesbrain.tree2mydoor-context-upload.plist

# 4. Verify it's loaded
launchctl list | grep tree2mydoor
```

**Schedule:** Daily at 7:00 AM GMT

### 3. Monitor First Automated Run

**Check on Saturday morning (Nov 9):**
```bash
# View log to confirm it ran
cat ~/.petesbrain-client-contexts.log

# Check sync folder for dated files
ls -la ~/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My\ Drive/PetesBrain-Context/

# Spot check 2-3 Google Docs to confirm they updated
```

### 4. Update CLAUDE.md Documentation

Add this system to the "Client Workflows" section:

**Location:** /Users/administrator/Documents/PetesBrain/CLAUDE.md

**Add after "Google Ads Client Analysis" section:**

```markdown
### Client Context Google Docs (Auto-Synced)

**Purpose**: All 16 Roksys clients have Google Docs that auto-sync daily at 7 AM GMT with their CONTEXT.md files. These docs can be referenced in Claude.ai custom instructions for ad-hoc reporting.

**System Components**:
- **Google Docs**: One per client, stored in Google Drive
- **Registry**: shared/data/client-google-docs.json (tracks doc IDs and URLs)
- **Sync Script**: shared/scripts/sync-all-client-contexts.sh (universal script for all clients)
- **LaunchAgent**: ~/Library/LaunchAgents/com.petesbrain.tree2mydoor-context-upload.plist (runs daily at 7 AM)
- **Reference Sheet**: CLAUDE-AI-CUSTOM-INSTRUCTIONS.txt (URLs for Claude.ai)

**Usage in Claude.ai**:
1. Open CLAUDE-AI-CUSTOM-INSTRUCTIONS.txt
2. Copy relevant client's Google Doc URL
3. Paste in Claude.ai: "Reference this document for [Client Name] context: [URL]"

**Monitoring**:
- Log file: ~/.petesbrain-client-contexts.log
- Sync folder: ~/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My Drive/PetesBrain-Context/
- Manual sync: bash shared/scripts/sync-all-client-contexts.sh
```

## Files Referenced

**Registry (complete, do not modify):**
/Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json

**Universal Sync Script:**
/Users/administrator/Documents/PetesBrain/shared/scripts/sync-all-client-contexts.sh

**Reference Sheet (for Claude.ai usage):**
/Users/administrator/Documents/PetesBrain/CLAUDE-AI-CUSTOM-INSTRUCTIONS.txt

**LaunchAgent Config:**
~/Library/LaunchAgents/com.petesbrain.tree2mydoor-context-upload.plist

## Success Criteria
- [ ] Manual test run completes without errors
- [ ] All 16 clients sync to Google Drive folder
- [ ] Google Docs update with latest content
- [ ] LaunchAgent updated to use universal script
- [ ] First automated run (Sat Nov 9) succeeds
- [ ] CLAUDE.md documentation updated with new system

## Troubleshooting

**If sync fails:**
- Check log: cat ~/.petesbrain-client-contexts.log
- Verify Google Drive Desktop is running
- Check registry JSON is valid: python3 -c "import json; json.load(open('shared/data/client-google-docs.json'))"
- Test script manually first

**If Google Docs don't update:**
- Google Drive Desktop may need time to sync (wait 5-10 mins)
- Check files exist in sync folder
- Verify Google Drive Desktop sync status (menu bar icon)

**If LaunchAgent doesn't run:**
- Check if loaded: launchctl list | grep tree2mydoor
- View system logs: log show --predicate 'process == "launchd"' --last 1h | grep tree2mydoor
- Test manual run first to ensure script works
