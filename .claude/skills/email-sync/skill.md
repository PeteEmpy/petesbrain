---
name: email-sync
description: Runs the complete email sync workflow - auto-labels incoming and sent emails, syncs them to client folders, and copies Google rep emails to knowledge base. Use when user says "sync emails", "run email sync", "label and sync emails", or wants to manually trigger the email workflow.
allowed-tools: Bash, Read
---

# Email Sync Skill

## Instructions

When this skill is triggered, run the email sync workflow using the manual commands below.

---

## Manual Commands

### Run Email Sync Manually

```bash
# Sync emails now (auto-label + sync)
shared/scripts/sync-emails.sh
```

Or run the Python script directly:
```bash
cd shared/email-sync
.venv/bin/python3 email_sync_workflow.py
```

### Dry Run (Preview Without Changes)

```bash
# See what would be labeled and synced
shared/scripts/sync-emails.sh --dry-run
```

Or:
```bash
cd shared/email-sync
.venv/bin/python3 email_sync_workflow.py --dry-run
```

### Check Status

```bash
# Check if sync agent is running
launchctl list | grep email-sync

# View recent sync logs
tail -50 ~/.petesbrain-email-sync.log

# Check for errors
tail -50 ~/.petesbrain-email-sync-error.log

# View sync state
cat .email-sync-state.json | jq
```

### Force Re-Sync All Emails

```bash
# Delete sync state (will re-sync all emails)
rm .email-sync-state.json

# Run sync
shared/scripts/sync-emails.sh
```

---

## What Happens

When you run email sync:

1. **Step 1: Auto-Labeling**
   - Scans inbox emails for client detection (sender domain/email/keywords)
   - Scans sent emails for client detection (recipient domain/email/keywords)
   - Applies Gmail labels: `client/[client-name]`
   - Uses confidence scoring (minimum 70 points required)

2. **Step 2: Email Sync**
   - Syncs labeled emails to `clients/[client-name]/emails/`
   - Sent emails marked with `[SENT]` prefix
   - Downloads attachment info
   - Deduplication: Never syncs the same email twice

3. **Step 3: Google Rep Emails** (if script exists)
   - Copies Google rep emails to knowledge base inbox
   - Routes to `roksys/knowledge-base/_inbox/emails/`

## File Locations

### Main Scripts
- **Workflow**: `shared/email-sync/email_sync_workflow.py`
- **Convenience Script**: `shared/scripts/sync-emails.sh`
- **Auto-Labeling**: `shared/email-sync/auto_label.py`
- **Email Sync**: `shared/email-sync/sync_emails.py`

### Configuration
- **Client Detection Rules**: `shared/email-sync/auto-label-config.yaml`
- **Sync Configuration**: `shared/email-sync/config.yaml`
- **Sync State**: `.email-sync-state.json` (tracks synced emails)

### Logs
- **Sync Log**: `~/.petesbrain-email-sync.log`
- **Error Log**: `~/.petesbrain-email-sync-error.log`
- **Unmatched Emails**: `shared/email-sync/logs/unmatched_inbox_emails.log` and `unmatched_sent_emails.log`

### Output Locations
- **Client Emails**: `clients/[client-name]/emails/YYYY-MM-DD_subject.md`
- **Sent Emails**: `clients/[client-name]/emails/YYYY-MM-DD_[SENT]_subject.md`
- **Google Rep Emails**: `roksys/knowledge-base/_inbox/emails/`

## Schedule

### Email Sync Agent
- **Frequency:** Every 6 hours (21600 seconds)
- **LaunchAgent:** `com.petesbrain.email-sync`
- **Log:** `~/.petesbrain-email-sync.log`
- **Error Log:** `~/.petesbrain-email-sync-error.log`

### Manual Run
The sync can be run manually anytime using the commands above.

## Troubleshooting

### Sync Not Running

```bash
# Check LaunchAgent status
launchctl list | grep email-sync

# If not loaded, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.email-sync.plist

# Check logs for errors
tail -50 ~/.petesbrain-email-sync-error.log
```

### Emails Not Being Labeled

**Check client detection rules:**
- Review `shared/email-sync/auto-label-config.yaml`
- Add missing domains/emails/keywords for clients

**Review unmatched emails:**
```bash
# Check unmatched inbox emails
cat shared/email-sync/logs/unmatched_inbox_emails.log

# Check unmatched sent emails
cat shared/email-sync/logs/unmatched_sent_emails.log
```

**Test labeling:**
```bash
# Dry run to see what would be labeled
shared/scripts/sync-emails.sh --dry-run
```

### Emails Not Syncing

**Verify labels exist in Gmail:**
- Check Gmail has labels: `client/[client-name]`
- Verify emails have labels applied

**Check configuration:**
- Review `shared/email-sync/config.yaml` for label mappings
- Ensure `sync_sent_emails: true` if you want sent emails synced

**Check sync state:**
```bash
# View sync state
cat .email-sync-state.json | jq

# Reset sync state (will re-sync all)
rm .email-sync-state.json
```

### Authentication Errors

```bash
# Re-authenticate by running manually
shared/scripts/sync-emails.sh
```

This will prompt for Gmail authentication if token expired.

## State Management

The sync tracks processed emails to avoid duplicates.

**State File:** `.email-sync-state.json`

**Contents:**
```json
{
  "synced_ids": ["email-id-1", "email-id-2", ...],
  "last_sync": "2025-11-08T16:00:00"
}
```

**On First Run:**
- No state file exists
- Syncs all labeled emails
- Creates state file with synced email IDs

**On Subsequent Runs:**
- Reads state file
- Only syncs emails not already synced
- Updates state file with new email IDs

## Related Skills

- **Email Draft Generator** - For creating client emails
- **Knowledge Base Processor** - Processes synced emails in KB
- **Weekly Meeting Review** - Includes email summaries

## Notes

- **Idempotent**: Safe to run multiple times (won't duplicate emails)
- **Smart Processing**: Only processes emails without client labels (avoids re-processing)
- **Bidirectional**: Handles both inbox and sent emails
- **Clear Marking**: Sent emails marked with `[SENT]` prefix
- **Logged**: All operations logged for troubleshooting

---

**Quick Command**:
```bash
shared/scripts/sync-emails.sh
```

