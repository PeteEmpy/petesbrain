# Email Sync - Pete's Brain

Automatically sync Gmail emails with client labels to local directories as markdown files.

## Features

- ✉️ Syncs emails from Gmail based on labels
- 📤 Syncs sent emails to clients automatically
- 📝 Converts emails to clean markdown format
- 🏷️ Maps Gmail labels to client folders automatically
- 🔄 Automatic sync 4 times daily (9am, 12pm, 3pm, 6pm)
- ⚡ Manual sync command for on-demand syncing
- 🔍 Deduplication - never saves the same email twice
- 📎 Downloads and saves email attachments (documents, spreadsheets, images, etc.)

## Quick Start

### 1. Gmail Setup

#### Create Gmail Label Structure

In Gmail, create labels with this format:
```
client/accessories-for-the-home
client/bright-minds
client/clear-prospects
client/devonshire-hotels
client/godshot
client/national-design-academy
client/otc
client/print-my-pdf
client/smythson
client/superspace
client/tree2mydoor
client/uno-lighting
roksys
personal
```

**To create labels in Gmail:**
1. Go to Gmail settings (gear icon) → "See all settings"
2. Click "Labels" tab
3. Scroll to "Labels" section
4. Click "Create new label"
5. Enter label name (e.g., "client/accessories-for-the-home")
6. Click "Create"

**To label emails:**
- Select an email
- Click the label icon (tag icon)
- Check the appropriate client label
- The email will now be synced on the next run

### 2. Gmail API Setup

#### Enable Gmail API & Get Credentials

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create a new project:**
   - Click project dropdown at top
   - Click "New Project"
   - Name it "Pete's Brain Email Sync"
   - Click "Create"

3. **Enable Gmail API:**
   - In the left sidebar, go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click on it and click "Enable"

4. **Create OAuth 2.0 credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - User Type: "External"
     - App name: "Pete's Brain Email Sync"
     - User support email: your email
     - Developer contact: your email
     - Click "Save and Continue"
     - Scopes: Skip this (click "Save and Continue")
     - Test users: Add your email address
     - Click "Save and Continue"
   - Back to Create OAuth client ID:
     - Application type: "Desktop app"
     - Name: "Email Sync"
     - Click "Create"

5. **Download credentials:**
   - Click the download icon (⬇) next to your newly created OAuth 2.0 Client ID
   - Save the file as `credentials.json`
   - Move it to: `/Users/administrator/Documents/PetesBrain/shared/email-sync/`

### 3. Install Dependencies

```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. First Time Authentication

Run a test sync to authenticate:

```bash
./sync --dry-run
```

This will:
1. Open your browser for Gmail authentication
2. Ask you to allow the app to access Gmail
3. Save an authentication token for future use
4. Show you what would be synced (without actually saving anything)

**Important:** When authenticating, Google will show a warning "This app isn't verified." This is normal for personal projects. Click "Advanced" → "Go to Pete's Brain Email Sync (unsafe)" → "Allow".

### 5. Set Up Automatic Sync

```bash
./setup-cron.sh
```

This will:
- Create the virtual environment if needed
- Install a cron job to run sync 4 times daily
- Offer to run a test sync

### 6. Manual Sync

Anytime you want to sync manually:

```bash
./sync
```

Or for a dry-run (to see what would be synced):

```bash
./sync --dry-run
```

## How It Works

### Label → Folder Mapping

The script automatically maps Gmail labels to client folders based on `config.yaml`:

| Gmail Label | Saves To |
|-------------|----------|
| `client/accessories-for-the-home` | `clients/accessories-for-the-home/emails/` |
| `client/bright-minds` | `clients/bright-minds/emails/` |
| `roksys` | `roksys/emails/` |
| `personal` | `personal/emails/` |

### Email File Format

Emails are saved as markdown files with this naming:
```
YYYY-MM-DD_subject-slug.md
```

Example:
```
2025-10-28_quarterly-budget-review.md
```

### Markdown Format

Each email is converted to markdown:

```markdown
# Subject Line

## Email Details

- **From:** sender@example.com
- **To:** you@example.com
- **Date:** 2025-10-28 14:30:00
- **Gmail ID:** 18abc123def456

---

## Message

[Email body content here, converted from HTML if necessary]

---

## Attachments

- [report.pdf](attachments/2025-01-15/report.pdf) (1.2 MB)
- [screenshot.png](attachments/2025-01-15/screenshot.png) (86.9 KB)
```

**Note:** Attachments are automatically downloaded and saved to `attachments/YYYY-MM-DD/` subdirectories within the same emails folder. The markdown links are relative paths that work when viewing the markdown file.

### Attachment Storage Structure

```
clients/
└── client-name/
    └── emails/
        ├── 2025-01-15_project-update.md
        └── attachments/
            └── 2025-01-15/
                ├── report.pdf
                └── screenshot.png
```

### Deduplication

The script tracks synced emails in `.email-sync-state.json` in the project root. Each email's Gmail ID is stored, so it will never be saved twice, even if you run sync multiple times.

### Sent Emails

The system automatically syncs **both received and sent emails** for complete communication history:

**How it works:**
1. Received emails are synced based on Gmail labels (e.g., `client/smythson`)
2. Sent emails are synced by searching your Sent folder for emails to client domains/addresses
3. Both types are saved to the same client folder

**Sent email format:**
```markdown
# Re: Project Update

## Email Details
- **From:** Peter Empson <petere@roksys.co.uk>
- **To:** client@example.com
- **Date:** 2025-10-21 13:15:33

---

**📤 Sent Email**

---

## Message
[Your sent message content]
```

**Filename format:** Sent emails use `sent-` prefix in the filename
- Example: `2025-10-21_sent-re-project-update.md`

**Client matching:** The system uses domains and email addresses from `auto-label-config.yaml`:
- If you send to `michael@clearprospects.com` → saved to `clear-prospects/emails/`
- If you send to `@smythson.com` → saved to `smythson/emails/`

**Enable/disable:** Set `sync_sent_emails: true/false` in `config.yaml`

## Configuration

Edit `config.yaml` to customize:

```yaml
# Add new client labels
client_labels:
  "client/new-client": "new-client"

# Adjust sync settings
sync:
  max_emails_per_run: 100  # Max emails per sync
  include_attachments: true  # Track attachment info

# Change filename format
filename_format: "{date}_{subject}.md"
max_filename_length: 100
```

## Cron Schedule

By default, emails sync 4 times daily:
- 9:00 AM
- 12:00 PM (noon)
- 3:00 PM
- 6:00 PM

**To change the schedule:**
```bash
crontab -e
```

Find the line with `sync_emails.py` and modify the schedule:
```
# Format: minute hour day month weekday command
0 9,12,15,18 * * * /path/to/sync_emails.py
```

Cron schedule examples:
- Every hour: `0 * * * *`
- Every 2 hours: `0 */2 * * *`
- Twice daily (9am, 6pm): `0 9,18 * * *`
- Every 30 minutes: `*/30 * * * *`

## Viewing Logs

Automatic syncs log to `logs/sync.log`:

```bash
# View last 20 lines
tail -20 shared/email-sync/logs/sync.log

# Watch logs in real-time
tail -f shared/email-sync/logs/sync.log
```

## Troubleshooting

### "credentials.json not found"

**Solution:** Download OAuth credentials from Google Cloud Console (see step 2.5 above)

### "Authentication failed"

**Solution:**
1. Delete `token.json`
2. Run `./sync --dry-run` again to re-authenticate
3. Make sure you allow all permissions when prompted

### "No emails found"

**Possible causes:**
1. No emails have the client labels
2. All emails with labels have already been synced
3. Label names don't match `config.yaml`

**Check:**
```bash
# View your current labels in Gmail
# Go to Gmail → Settings → Labels

# Check what's configured
cat config.yaml
```

### Cron job not running

**Check if cron job is installed:**
```bash
crontab -l | grep sync_emails
```

**Check logs:**
```bash
tail -f shared/email-sync/logs/sync.log
```

**Test manually:**
```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
./sync
```

### Duplicate emails being saved

This shouldn't happen due to deduplication, but if it does:

**Check state file:**
```bash
cat /Users/administrator/Documents/PetesBrain/.email-sync-state.json
```

**Reset state (will re-sync all emails):**
```bash
rm /Users/administrator/Documents/PetesBrain/.email-sync-state.json
```

## Security Notes

- ⚠️ **Never commit `credentials.json` or `token.json` to git**
- ⚠️ **These files contain authentication to your Gmail account**
- ✅ Both files are already in `.gitignore`
- ✅ Emails are stored locally only
- ✅ The app only requests read access to Gmail (and label modification for tracking)

## Commands Reference

```bash
# Manual sync
./sync

# Dry run (preview without saving)
./sync --dry-run

# Setup automatic sync
./setup-cron.sh

# View cron jobs
crontab -l

# Remove cron job
crontab -e  # Delete the sync_emails.py line

# View sync logs
tail -f logs/sync.log

# Check what would be synced
./sync --dry-run
```

## File Structure

```
shared/email-sync/
├── sync_emails.py       # Main sync script
├── config.yaml          # Configuration & label mappings
├── requirements.txt     # Python dependencies
├── setup-cron.sh       # Automatic sync setup
├── sync                # Manual sync command
├── credentials.json    # Gmail API credentials (download from Google)
├── token.json          # Authentication token (auto-generated)
├── .venv/              # Python virtual environment
├── logs/               # Sync logs
└── README.md           # This file
```

## Workflow Example

### Daily Workflow

1. **Receive client email** → Label it in Gmail with `client/client-name`
2. **Automatic sync runs** at 9am, 12pm, 3pm, 6pm
3. **Email appears** in `clients/client-name/emails/2025-10-28_subject.md`
4. **Read or reference** the markdown file anytime

### Manual Sync

```bash
# Label some emails in Gmail
# Then run:
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
./sync

# Output:
# Processing label: client/accessories-for-the-home → accessories-for-the-home
#   Found 3 emails
#   ✓ Quarterly budget review (2025-10-28)
#   ✓ Product launch feedback (2025-10-27)
#   ✓ Meeting notes follow-up (2025-10-26)
#
# Sync Complete!
# Total emails processed: 3
# Newly synced: 3
```

## Support

For issues or questions:
1. Check troubleshooting section above
2. Check logs: `tail -f logs/sync.log`
3. Run in dry-run mode: `./sync --dry-run`
4. Check Gmail labels match `config.yaml`
