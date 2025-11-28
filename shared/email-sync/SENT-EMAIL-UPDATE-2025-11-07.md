# Sent Email Support Added - 2025-11-07

## Summary

Both the **email sync** and **auto-labeling** systems now fully support **sent emails**, providing complete bidirectional email tracking for all client communications.

## What's New

### 1. Auto-Labeling for Sent Emails
- `auto_label.py` now processes both inbox AND sent emails
- Matches sent emails based on **To:** field (recipient domains/emails)
- Uses same confidence scoring system (minimum 70 points)
- Separate logs for inbox and sent emails

### 2. Email Sync for Sent Emails
- `sync_emails.py` already had sent email support (enabled via `sync_sent_emails: true` in config)
- Sent emails marked with **[SENT]** prefix in filename
- Sent emails include **📤 Sent Email** indicator in markdown

## Changes Made

### Files Modified

**`shared/email-sync/auto_label.py`**:
- Added `_process_emails_with_query()` - Generic query processor for inbox/sent
- Added `_match_client_sent()` - Matches sent emails based on To: field
- Modified `auto_label_emails()` - Now processes both inbox and sent emails
- Updated logging to separate inbox/sent unmatched emails

**`shared/email-sync/AUTO-LABELING.md`**:
- Updated overview to mention sent email support
- Added confidence scoring details for sent emails
- Updated example output to show both inbox and sent processing
- Updated use cases to highlight bidirectional tracking

**`shared/email-sync/config.yaml`**:
- Already had `sync_sent_emails: true` (no changes needed)

**`shared/email-sync/auto-label-config.yaml`**:
- No changes needed - same client detection rules work for both directions

## How It Works

### Inbox Emails (From: field)
1. Match sender domain against client domains (e.g., `from:person@smythson.com`)
2. Match sender email against known client emails
3. Check keywords in subject/body
4. Confidence scoring: domain=+50, email=+40, subject keyword=+15, body keyword=+10

### Sent Emails (To: field) - NEW
1. Match recipient domain against client domains (e.g., `to:garry@acunningplan.co.uk`)
2. Match recipient email against known client emails
3. Check keywords in subject/body (for additional confirmation)
4. Confidence scoring: domain=+50, email=+40, subject keyword=+15, body keyword=+10

## Testing Results

Dry run test on 2025-11-07:
- **Total processed**: 200 emails (100 inbox + 100 sent)
- **Successfully labeled**: 36 emails
- **No match found**: 164 emails (mostly automated scripts, personal emails)
- **Errors**: 0

### Example Matches

**Inbox email matched**:
```
[6] Inbox: <garry@acunningplan.co.uk>
    Subject: RE: The Hide - PPC
    Matched: devonshire-hotels (confidence: 90%)
    Reasons: domain:acunningplan.co.uk, email:garry@acunningplan.co.uk
    [DRY RUN] Would label as: client/devonshire-hotels
```

**Sent email matched**:
```
[15] Sent: garry@acunningplan.co.uk
    Subject: Re: Monthly Report
    Matched: devonshire-hotels (confidence: 90%)
    Reasons: to_domain:acunningplan.co.uk, to_email:garry@acunningplan.co.uk
    [DRY RUN] Would label as: client/devonshire-hotels
```

## Usage

### Standalone Auto-Labeling
```bash
# Label both inbox and sent emails
cd shared/email-sync
source .venv/bin/activate
python3 auto_label.py

# Dry run to test
python3 auto_label.py --dry-run
```

### Email Sync (includes sent emails)
```bash
# Sync both inbox and sent emails
cd shared/email-sync
source .venv/bin/activate
python3 sync_emails.py

# Dry run to test
python3 sync_emails.py --dry-run
```

### Automated Workflow
The LaunchAgent (`com.petesbrain.email-sync.plist`) runs email sync every 6 hours, which now includes:
1. Auto-labeling inbox emails
2. Auto-labeling sent emails
3. Syncing labeled inbox emails
4. Syncing labeled sent emails

## Benefits

✅ **Complete communication history** - Both incoming and outgoing emails in one place
✅ **Automatic labeling** - No manual tagging needed for sent emails
✅ **Context aware** - CONTEXT.md updates can reference both sides of conversations
✅ **Bidirectional tracking** - See full email threads, not just one side
✅ **Separate indicators** - Sent emails clearly marked with [SENT] prefix and 📤 icon

## File Naming

**Inbox emails**:
```
2025-11-07_budget-update-for-november.md
```

**Sent emails**:
```
2025-11-07_[SENT] re-budget-update-for-november.md
```

## Logging

**Unmatched emails logged separately**:
- `shared/email-sync/logs/unmatched_inbox_emails.log`
- `shared/email-sync/logs/unmatched_sent_emails.log`

This makes it easier to review and add missing client detection rules.

## Next Steps

No action required - the system is fully functional and will automatically process sent emails in the next sync cycle.

To verify:
1. Check `clients/[client]/emails/` folders for [SENT] files after next sync
2. Review logs for any unmatched sent emails that should be labeled
3. Add missing client domains/emails to `auto-label-config.yaml` if needed

## Documentation

See [AUTO-LABELING.md](AUTO-LABELING.md) for complete documentation on:
- How the auto-labeling system works
- Confidence scoring details
- Configuration options
- Troubleshooting guide
