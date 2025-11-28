# Email Notifications Setup Guide

Get weekly summaries and real-time alerts delivered to your inbox.

## Features

### 📊 Weekly Summary Emails
- **When**: Every Monday at 9:00 AM (configurable)
- **Contains**:
  - Total meetings imported in the last 7 days
  - Breakdown by client
  - List of all meeting files created
  - Warning for unassigned meetings

### 🚨 Real-Time Alerts
- **Unassigned Meeting Alert**: Immediate notification when a meeting can't be auto-assigned
- **Sync Failure Alert**: Notification if the daemon encounters errors

## Quick Setup (5 minutes)

### Step 1: Copy Config File

```bash
cd tools/granola-importer
cp config.example.yaml config.yaml
```

### Step 2: Configure Email Settings

Edit `config.yaml` with your email details:

```yaml
email:
  enabled: true
  recipient: "your-email@example.com"  # Where to send summaries

  smtp:
    host: "smtp.gmail.com"
    port: 587
    use_tls: true
    username: "your-email@gmail.com"
    password: "your-app-password-here"  # See Gmail setup below
```

### Step 3: Gmail App Password Setup (Recommended)

**Gmail users MUST use an App Password (not your regular password):**

1. Go to your Google Account: https://myaccount.google.com/security
2. Enable 2-Step Verification if not already enabled
3. Go to https://myaccount.google.com/apppasswords
4. Create a new App Password:
   - Select app: "Mail"
   - Select device: "Mac"
   - Click "Generate"
5. Copy the 16-character password
6. Paste into `config.yaml` under `smtp.password`

### Step 4: Test Email

```bash
source venv/bin/activate
python3 send_weekly_summary.py
```

You should receive a test email within seconds. Check your inbox!

### Step 5: Schedule Weekly Emails

```bash
./setup_weekly_email.sh
```

This schedules the email to send every Monday at 9:00 AM automatically.

## Configuration Options

### Change Email Day/Time

Edit `config.yaml`:

```yaml
email:
  weekly_summary:
    enabled: true
    day_of_week: 4  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    time: "17:00"   # 5:00 PM (24-hour format)
```

Then re-run: `./setup_weekly_email.sh`

### Enable/Disable Specific Alerts

```yaml
email:
  alerts:
    unassigned_meetings: true   # Alert when meeting can't be assigned
    sync_failures: true          # Alert when daemon errors occur
```

### Disable All Email

```yaml
email:
  enabled: false
```

## Other Email Providers

### Outlook/Office 365

```yaml
smtp:
  host: "smtp-mail.outlook.com"
  port: 587
  use_tls: true
  username: "your-email@outlook.com"
  password: "your-password"
```

### Custom SMTP Server

```yaml
smtp:
  host: "mail.yourcompany.com"
  port: 465
  use_tls: false  # Set true for STARTTLS, false for SSL
  username: "you@yourcompany.com"
  password: "your-password"
```

## Example Weekly Summary Email

```
Subject: 📊 Weekly Meeting Import Summary - October 28, 2025

WEEKLY MEETING IMPORT SUMMARY
================================================
Period: Last 7 days
Total meetings imported: 12

Bright Minds (4 meetings)
----------------------------------------
  • 2025-10-28-q4-strategy-review-bright-minds.md
    Imported: Oct 28, 14:30
  • 2025-10-27-product-roadmap-bright-minds.md
    Imported: Oct 27, 10:15
  ...

Uno Lighting (3 meetings)
----------------------------------------
  • 2025-10-26-design-review-uno-lighting.md
    Imported: Oct 26, 15:45
  ...

⚠️ Unassigned (2 meetings)
----------------------------------------
  • 2025-10-25-internal-planning.md
    Imported: Oct 25, 09:00
  • 2025-10-24-vendor-call.md
    Imported: Oct 24, 13:30

⚠️ ACTION REQUIRED:
2 meeting(s) could not be automatically assigned.
Please review clients/_unassigned/meeting-notes/
and organize manually.
```

## Troubleshooting

### "Authentication failed" error

**Gmail users**: Make sure you're using an App Password, not your regular password.

**Other providers**: Check username/password are correct.

### No email received

1. Check spam/junk folder
2. Verify recipient email in `config.yaml`
3. Test with: `python3 send_weekly_summary.py`
4. Check logs: `cat ~/.petesbrain-granola-weekly-email.log`

### "Connection refused" error

- Check `smtp.host` and `smtp.port` are correct for your provider
- Verify firewall isn't blocking outgoing SMTP connections
- Try toggling `use_tls` setting

### Emails sending but alerts not working

The alerts are integrated into the sync daemon. Make sure:
1. Email is configured in `config.yaml`
2. Sync daemon is running: `launchctl list | grep granola`
3. Alerts are enabled in config:
   ```yaml
   email:
     alerts:
       unassigned_meetings: true
       sync_failures: true
   ```

## Manual Commands

```bash
# Send weekly summary now
python3 send_weekly_summary.py

# Test email configuration
python3 email_reporter.py

# View weekly email logs
tail -f ~/.petesbrain-granola-weekly-email.log

# Stop weekly emails
launchctl unload ~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist

# Restart weekly emails
launchctl load ~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist
```

## Privacy & Security

- ✅ All emails sent directly from your Mac (no third-party services)
- ✅ Your credentials stored locally in `config.yaml`
- ✅ SMTP passwords never logged or transmitted elsewhere
- ⚠️ Keep `config.yaml` secure (don't commit to git)
- ✅ Config file already in `.gitignore`

## Disabling Email Features

To remove email functionality entirely:

```bash
# Stop weekly emails
launchctl unload ~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist
rm ~/Library/LaunchAgents/com.petesbrain.granola-weekly-summary.plist

# Delete config
rm config.yaml

# The tool will continue working without email features
```

## Need Help?

Common issues:
- **Gmail**: Must use App Password (see step 3 above)
- **2FA**: Required for Gmail App Passwords
- **Firewall**: Ensure port 587/465 isn't blocked
- **Config syntax**: YAML is whitespace-sensitive

For more help, check the main README.md or TOOL_CLAUDE.md
