# Auto-Labeling System - Complete Guide

The email sync system now **automatically labels** incoming emails with client labels based on intelligent matching.

## How It Works

```
New Email Arrives
    ↓
Auto-Labeler Analyzes
    ↓
Matches to Client (based on domain, sender, keywords)
    ↓
Applies Gmail Label (e.g., "client/accessories-for-the-home")
    ↓
Email Sync Picks It Up
    ↓
Saved to Client Folder as Markdown
```

## Automatic Workflow (4x Daily)

The system runs automatically at **9am, 12pm, 3pm, 6pm**:

1. **Auto-label** - Checks inbox, labels client emails
2. **Sync** - Downloads labeled emails to folders

**You don't need to do anything!** Just receive emails and they'll be organized automatically.

## Matching Logic

The auto-labeler uses **intelligent scoring** to match emails to clients:

| Match Type | Confidence Score | Example |
|------------|------------------|---------|
| **Email Domain** | +50% | `@clearprospects.com` → Clear Prospects |
| **Exact Email** | +40% | `ant@getsuperspace.com` → Superspace |
| **Sender Name** | +20% | "Smythson" in sender → Smythson |
| **Subject Keyword** | +15% | "NDA" in subject → National Design Academy |
| **Body Keyword** | +10% | "godshot" in body → Godshot |

**Minimum confidence:** 70% required to auto-label

### Example Matching

```
Email from: michael.robinson@clearprospects.com
Subject: Project update

Scoring:
✓ Domain match (clearprospects.com) = +50%
✓ Email match = +40%
✓ Body keyword = +10%
-----------------------------------
Total: 100% → Auto-labeled as "client/clear-prospects"
```

## Configuration

Edit `auto-label-config.yaml` to add client email addresses, domains, and keywords:

```yaml
clients:
  accessories-for-the-home:
    label: "client/accessories-for-the-home"
    domains:
      - "accessoriesforthehome.co.uk"  # Matches any email from this domain
    emails:
      - "john@example.com"  # Specific email addresses
    keywords:
      - "accessories for the home"  # Keywords in subject/body
      - "AFH"
    company_names:
      - "Accessories for the Home"  # Company name in sender
```

### Adding a New Client Contact

1. Edit `auto-label-config.yaml`
2. Find the client section
3. Add the email or domain:

```yaml
  smythson:
    emails:
      - "newperson@smythson.com"  # Add this line
```

4. Save the file
5. Next sync will use the new rules

## Manual Commands

### Test Auto-Labeling (Dry Run)

See what would be labeled without actually doing it:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
./sync-all --dry-run
```

Or just auto-label:

```bash
.venv/bin/python3 auto_label.py --dry-run
```

### Run Full Sync Now

Auto-label + sync emails immediately:

```bash
./sync-all
```

### View What Didn't Match

Unmatched emails are logged to `logs/unmatched_emails.log`:

```bash
tail -20 logs/unmatched_emails.log
```

Use this to find client emails you need to add to the config.

## Confidence Threshold

The default minimum confidence is **70%**. You can adjust this in `auto-label-config.yaml`:

```yaml
settings:
  min_confidence: 70  # Lower = more aggressive labeling
```

**Recommendations:**
- **70-80%**: Balanced (recommended)
- **60-70%**: More aggressive (may mislabel some emails)
- **80-90%**: Conservative (only very confident matches)

## Reviewing Auto-Labels

### Check What Was Labeled

```bash
tail -f logs/sync.log
```

Shows all auto-labeling and syncing activity.

### Verify Labels in Gmail

1. Go to Gmail
2. Click on a labeled email
3. Check the labels applied (you'll see `client/client-name`)

### Remove Incorrect Labels

If an email was mislabeled:

1. In Gmail, open the email
2. Click the label icon
3. Uncheck the wrong label
4. Update `auto-label-config.yaml` to prevent future mis-matches

## Example Workflow

### Scenario: New Client Contact

**Email arrives from:** `sarah@newclient.com`

**What happens:**
1. Auto-labeler doesn't recognize it (logs to `unmatched_emails.log`)
2. You check the log and see it's from a client
3. You edit `auto-label-config.yaml`:

```yaml
  new-client:
    domains:
      - "newclient.com"
    emails:
      - "sarah@newclient.com"
```

4. Next sync auto-labels all future emails from that domain
5. You can manually label the old email in Gmail, and it will be synced

## Monitoring

### View Sync Logs

```bash
# Watch live
tail -f logs/sync.log

# Last 50 lines
tail -50 logs/sync.log

# Search for specific client
grep "accessories-for-the-home" logs/sync.log
```

### Check Unmatched Emails

```bash
# View unmatched emails
cat logs/unmatched_emails.log

# Count unmatched emails
wc -l logs/unmatched_emails.log
```

## Troubleshooting

### Emails Not Being Labeled

**Check:**
1. Is the email in your inbox?
2. Is it within the last 7 days? (see `lookback_days` in config)
3. Does it match the configured rules?
4. Run manual test: `./sync-all --dry-run`

### Too Many False Positives

**Solution:** Increase confidence threshold:

```yaml
settings:
  min_confidence: 80  # Increase from 70
```

### Missing Client Emails

**Solution:** Add more matching rules:

```yaml
  client-name:
    domains:
      - "example.com"  # Add domain
      - "example.co.uk"  # Add alternate domain
    emails:
      - "person@example.com"  # Add specific email
    keywords:
      - "project xyz"  # Add keyword that appears in their emails
```

## Advanced Configuration

### Lookback Period

How far back to check for unlabeled emails:

```yaml
settings:
  lookback_days: 7  # Check last 7 days (increase if needed)
```

### Maximum Emails Per Run

Limit emails processed per sync:

```yaml
settings:
  max_emails_per_run: 50  # Increase for bulk labeling
```

### Skip Certain Labels

Don't process emails with these labels:

```yaml
settings:
  skip_labels:
    - "SPAM"
    - "TRASH"
    - "DRAFT"
    - "your-custom-label"  # Add custom labels to skip
```

## Files Reference

```
shared/email-sync/
├── auto_label.py              # Auto-labeling script
├── auto-label-config.yaml     # Client detection rules
├── sync_emails.py             # Email sync script
├── sync-all                   # Run both (auto-label + sync)
├── logs/
│   ├── sync.log              # All sync activity
│   └── unmatched_emails.log  # Emails that didn't match
└── config.yaml               # Sync configuration
```

## Quick Commands Reference

```bash
# Test what would be labeled (safe)
./sync-all --dry-run

# Run full sync now
./sync-all

# View recent activity
tail -50 logs/sync.log

# View unmatched emails
cat logs/unmatched_emails.log

# Edit client detection rules
nano auto-label-config.yaml

# Check cron schedule
crontab -l
```

## Current Configuration

Your system is configured to auto-detect emails from:

✅ **Clear Prospects** - `michael.robinson@clearprospects.com`
✅ **Superspace** - `ant@getsuperspace.com`
✅ All 12 client labels with domains and keywords

As you receive more emails, add their contacts to `auto-label-config.yaml` for automatic labeling!
