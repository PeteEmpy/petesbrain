# Google Rep Email Tracking System

## Overview

Automatically tracks, organizes, and processes emails from Google representatives into both client folders and the knowledge base. This creates a dual repository system where Google rep communications are available for both client-specific context and broader learning.

## How It Works

### 1. Email Detection

**Auto-labeling** (`shared/email-sync/auto-label-config.yaml`)
- Detects emails from @google.com addresses
- Filters out automated emails (noreply, calendar-notification, etc.)
- Identifies personal Google reps by email address
- Looks for keywords: "Google support", "Google consultation", "Performance Max"

**Known Google Reps** (automatically tracked):
- devinferreira@google.com (Smythson)
- solomiyak@google.com (National Design Academy)
- allyhamps@google.com (National Design Academy)
- patrickwhite@google.com (National Design Academy)
- technical-solutions@google.com (Technical support)
- brahmendra@google.com (Print My PDF)

### 2. Dual-Save System

When a Google rep email arrives:

**Step 1: Client Folder Save**
- Email syncs to: `clients/[client-name]/emails/`
- Keeps client-specific context intact
- Includes attachments in: `clients/[client-name]/emails/attachments/`

**Step 2: Knowledge Base Copy**
- Email copies to: `roksys/knowledge-base/_inbox/emails/`
- Filename prefixed with: `google-rep_{client-name}_`
- Allows KB processing for broader insights

**Step 3: KB Processing** (every 6 hours)
- Analyzes email content with Claude API
- Extracts attachments and Google Doc/Drive links
- Categorizes (likely `google-ads/platform-updates`)
- Creates formatted markdown document
- Organizes into knowledge base

### 3. Workflow Diagram

```
New Google Rep Email Arrives
    ↓
Step 1: Auto-Labeler
    - Labels as "google-reps"
    ↓
Step 2: Email Sync
    - Saves to client folder
    - Downloads attachments
    ↓
Step 3: KB Copy Script
    - Copies to KB inbox
    - Adds client prefix
    ↓
Step 4: KB Processor (every 6 hours)
    - Analyzes with Claude
    - Extracts documents
    - Organizes into KB
```

## Files & Locations

### Scripts

**Email Sync Workflow**: `shared/email-sync/sync-all`
- Runs: Auto-label → Sync → Copy to KB

**KB Copy Script**: `shared/scripts/copy-google-rep-emails-to-kb.py`
- Finds Google rep emails in client folders
- Copies to KB inbox with client prefix
- Only copies emails from last 30 days
- Runs automatically after email sync

**Historical Extraction**: `shared/scripts/extract-google-rep-docs.py`
- Scans last 12 months of emails
- Generates report of all Google rep emails
- Creates inbox entries for documents

### Configuration

**Auto-labeling**: `shared/email-sync/auto-label-config.yaml`
```yaml
google-reps:
  label: "google-reps"
  domains:
    - "google.com"
  emails:
    - "devinferreira@google.com"
    - "solomiyak@google.com"
    # ... etc
  keywords:
    - "Google support"
    - "Google consultation"
```

**Email sync**: `shared/email-sync/config.yaml`
```yaml
client_labels:
  # ... client labels
  "google-reps": "roksys/knowledge-base/_inbox/emails"
```

### Logs

- Email sync: `shared/email-sync/logs/auto_label.log`
- KB copy: `shared/data/google-rep-kb-copy.log`
- KB processing: `~/.petesbrain-knowledge-base.log`

## Reports & Monitoring

### Historical Report

**Location**: `roksys/google-rep-emails-report.md`

**Contents**:
- All Google rep emails from last 12 months
- Grouped by client
- Shows Google rep names and document links
- Includes file paths for reference

**Generate report**:
```bash
cd /Users/administrator/Documents/PetesBrain
python3 shared/scripts/extract-google-rep-docs.py
```

### Live Monitoring

**Check KB inbox**:
```bash
ls -la roksys/knowledge-base/_inbox/emails/ | grep google-rep
```

**View logs**:
```bash
# Email sync and labeling
tail -f shared/email-sync/logs/auto_label.log

# KB copy process
tail -f shared/data/google-rep-kb-copy.log

# KB processing
tail -f ~/.petesbrain-knowledge-base.log
```

## Adding New Google Reps

When you start working with a new Google rep:

1. **Add to auto-labeling config**:
   Edit: `shared/email-sync/auto-label-config.yaml`

   Under `google-reps` → `emails`, add:
   ```yaml
   - "newrep@google.com"
   ```

2. **That's it!** The system will automatically:
   - Label their emails
   - Sync to client folders
   - Copy to KB inbox
   - Process into knowledge base

## Document Extraction

### Automatic Detection

The system automatically detects:
- **Attachments**: PDF, PPTX, DOCX, etc.
- **Google Docs**: docs.google.com/document/d/...
- **Google Sheets**: docs.google.com/spreadsheets/d/...
- **Google Slides**: docs.google.com/presentation/d/...
- **Google Drive**: drive.google.com/file/d/...

### Document Processing

**Attachments**:
- Saved to: `clients/[client]/emails/attachments/[date]/`
- Copied to KB inbox with email
- Processed by KB processor

**Google Doc Links**:
- Extracted from email body
- Added to KB inbox as reference
- URL preserved for access

## Manual Operations

### Copy Recent Google Rep Emails

Copy emails from last 30 days to KB inbox:
```bash
cd /Users/administrator/Documents/PetesBrain
python3 shared/scripts/copy-google-rep-emails-to-kb.py
```

### Extract Historical Documents

Scan last 12 months and generate report:
```bash
python3 shared/scripts/extract-google-rep-docs.py
cat roksys/google-rep-emails-report.md
```

### Trigger KB Processing

Process KB inbox immediately (don't wait 6 hours):
```bash
shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-processor.py
```

## Weekly Summary Integration

Google rep emails are included in the Monday weekly summary:

**Email sections**:
- **AI News Highlights**: Industry updates
- **Google Ads Updates**: Platform changes from Google reps
- **Knowledge Base Additions**: New documents from reps
- **Key Insights**: Strategic takeaways

The system combines:
- Google rep emails from KB
- AI newsletters
- All KB documents added this week

## Statistics

**Current Status** (as of 2025-10-29):
- **13 Google rep emails** identified from last 12 months
- **3 clients** with Google rep communications
- **6 unique Google rep contacts** tracked
- **0 documents** extracted (no links found in historical emails)
- **13 emails** copied to KB inbox

**Clients with Google Reps**:
- Smythson (3 emails)
- National Design Academy (9 emails)
- Print My PDF (1 email)

## Troubleshooting

### Email not being detected

1. Check auto-labeling log:
   ```bash
   tail -50 shared/email-sync/logs/auto_label.log
   ```

2. Verify email address is in config:
   ```bash
   grep -A 10 "google-reps:" shared/email-sync/auto-label-config.yaml
   ```

3. Check if email is from automated address (excluded):
   - noreply, calendar-notification, etc.

### Email not copied to KB inbox

1. Check copy script log:
   ```bash
   tail -50 shared/data/google-rep-kb-copy.log
   ```

2. Verify email is in client folder:
   ```bash
   find clients/*/emails -name "*google*" -mtime -7
   ```

3. Run copy script manually:
   ```bash
   python3 shared/scripts/copy-google-rep-emails-to-kb.py
   ```

### Documents not being extracted

1. Check if email has document links:
   ```bash
   grep -i "docs.google\|drive.google" clients/[client]/emails/[email-file]
   ```

2. Check if attachments were downloaded:
   ```bash
   ls -la clients/[client]/emails/attachments/
   ```

3. Run KB processor manually to see errors:
   ```bash
   shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-processor.py
   ```

## Future Enhancements

Potential improvements to consider:

1. **Google Drive Integration**: Automatically download shared Google Docs/Sheets
2. **Deck Recognition**: Parse email body for "deck" mentions and prompt for upload
3. **Meeting Recordings**: Track Google Meet recordings and transcripts
4. **Rep Dashboard**: Visualize Google rep interactions by client/date
5. **Notification System**: Alert when high-value documents are shared

---

**Last Updated**: 2025-10-29
**Maintained By**: Automated system + Claude Code
