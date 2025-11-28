# Email Sync - Quick Start Guide

Get up and running in 5 steps!

## Step 1: Create Gmail Labels

In Gmail, create labels for each client using format: `client/client-name`

```
client/accessories-for-the-home
client/bright-minds
client/clear-prospects
(etc...)
roksys
personal
```

**How to create:**
- Gmail → Settings (gear) → "See all settings" → "Labels" → "Create new label"

## Step 2: Get Gmail API Credentials

1. Go to: https://console.cloud.google.com/
2. Create project: "Pete's Brain Email Sync"
3. Enable "Gmail API"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json`
6. Move to: `/Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json`

**Detailed instructions:** See [README.md](README.md#gmail-api-setup)

## Step 3: Install & Authenticate

```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
./setup-cron.sh
```

This will:
- Install Python dependencies
- Authenticate with Gmail (browser will open)
- Set up automatic sync (4 times daily)
- Run a test sync

## Step 4: Label Your Emails

Go to Gmail and label some emails with your client labels. For example:
- Client email from Accessories for the Home → Label: `client/accessories-for-the-home`
- Internal Rok Systems email → Label: `roksys`
- Personal email → Label: `personal`

## Step 5: Sync!

**Manual sync anytime:**
```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
./sync
```

**Automatic sync:** Already set up! Runs at 9am, 12pm, 3pm, 6pm daily.

## Done! 🎉

Your emails will now be saved as markdown files in:
```
clients/[client-name]/emails/YYYY-MM-DD_subject.md
roksys/emails/YYYY-MM-DD_subject.md
personal/emails/YYYY-MM-DD_subject.md
```

## Useful Commands

```bash
# Sync now
./sync

# Preview what would sync (without saving)
./sync --dry-run

# View logs
tail -f logs/sync.log

# Check cron schedule
crontab -l
```

## Need Help?

See [README.md](README.md) for:
- Detailed setup instructions
- Troubleshooting
- Configuration options
- Security notes
