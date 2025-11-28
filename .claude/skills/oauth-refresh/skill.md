---
name: oauth-refresh
description: Re-authorizes OAuth tokens for Google services (Tasks, Drive, Photos). Use when OAuth browser popups appear, LaunchAgents fail with authentication errors (exit code 78), or tokens need refreshing.
allowed-tools: Bash, Read
---

# OAuth Token Refresh Skill

## Overview

This skill runs the OAuth setup script to re-authorize Google services that require user authentication. It's needed when:
- OAuth browser popups appear during normal operation
- LaunchAgents fail with exit code 78 (authentication error)
- Tokens have been manually revoked in Google Account settings
- Pete's Brain hasn't been used for 6+ months

## What This Skill Does

1. Checks current OAuth token status
2. Runs the setup script: `shared/scripts/setup-oauth-once.sh`
3. Opens browser windows for authorization (one per service)
4. Stores refresh tokens that auto-renew indefinitely
5. Verifies tokens are properly configured

## Services That Need OAuth

**✅ Requires OAuth** (can't use service accounts):
- **Google Tasks** - Personal task lists API doesn't support service accounts
- **Google Drive** - Easier than sharing all files with service account
- **Google Photos** - API only works with user OAuth
- **Gmail/Email Sync** - Needs `gmail.modify` scope for auto-labeling emails

**⏭️ Already Working** (no OAuth needed):
- Google Sheets (uses service account)
- Google Ads (uses YAML config)

## Instructions for Claude Code

When this skill is invoked:

### Step 1: Check Token Status

```bash
# Check if tokens exist and when they expire
echo "=== Current OAuth Token Status ==="
for token in shared/mcp-servers/*/token.json; do
  if [ -f "$token" ]; then
    service=$(dirname "$token" | xargs basename)
    echo ""
    echo "Service: $service"
    if command -v jq &> /dev/null; then
      expiry=$(jq -r '.expiry // .token_expiry // "unknown"' "$token")
      has_refresh=$(jq -r 'if .refresh_token then "✅ Yes" else "❌ No" end' "$token")
      echo "  Expiry: $expiry"
      echo "  Has refresh token: $has_refresh"
    else
      echo "  Token file exists: ✅"
    fi
  fi
done
```

### Step 2: Check Recent LaunchAgent Failures

```bash
# Check which LaunchAgents failed recently (exit code 78 = auth issue)
echo ""
echo "=== Recent LaunchAgent Authentication Errors ==="
launchctl list | grep petesbrain | grep -E "^\-\s+78"

# Show recent errors from key services
echo ""
echo "=== Recent Errors from OAuth Services ==="
tail -20 ~/.petesbrain-tasks-monitor.log 2>/dev/null || echo "No tasks-monitor log found"
```

### Step 3: Explain What Will Happen

Tell the user:
```
I'll now run the OAuth setup script. This will:
1. Open browser windows for Google Tasks and Google Drive
2. Ask you to sign in and authorize Pete's Brain
3. Store refresh tokens that auto-renew indefinitely
4. Take about 2-3 minutes

The browser windows will open automatically. Just:
- Sign in with your Google account
- Click "Allow" when prompted
- Wait for "Success" message before closing

Ready to proceed?
```

### Step 4: Run the Setup Script

```bash
cd /Users/administrator/Documents/PetesBrain
./shared/scripts/setup-oauth-once.sh
```

**Note**: This script is INTERACTIVE and will:
- Open browser windows automatically
- Wait for user to authorize in browser
- Display success messages when complete

### Step 5: Verify Success

After the script completes:

```bash
# Verify tokens were created/updated
echo ""
echo "=== Verifying Token Setup ==="

# Check Google Tasks token
if [ -f "shared/mcp-servers/google-tasks-mcp-server/token.json" ]; then
  echo "✅ Google Tasks token exists"
  if command -v jq &> /dev/null; then
    has_refresh=$(jq -r 'if .refresh_token then "✅" else "❌"' shared/mcp-servers/google-tasks-mcp-server/token.json)
    echo "   Refresh token: $has_refresh"
  fi
else
  echo "❌ Google Tasks token missing"
fi

# Check Google Drive token
if [ -f "shared/mcp-servers/google-drive-mcp-server/token.json" ]; then
  echo "✅ Google Drive token exists"
else
  echo "❌ Google Drive token missing"
fi

# Test Google Tasks connection
echo ""
echo "=== Testing Google Tasks Connection ==="
cd shared/mcp-servers/google-tasks-mcp-server
.venv/bin/python -c "from tasks_service import tasks_service; service = tasks_service(); print('✅ Google Tasks API working')" 2>&1 || echo "❌ Google Tasks test failed"
```

### Step 6: Report Results

Summarize for the user:
```
✅ OAuth tokens refreshed successfully!

What was updated:
- Google Tasks: [status]
- Google Drive: [status]

These tokens will now auto-refresh indefinitely as long as your LaunchAgents run regularly.

You should NOT see OAuth popups anymore unless:
- You manually revoke access in Google Account settings
- Pete's Brain is unused for 6+ consecutive months
```

## Troubleshooting

### If Browser Windows Don't Open

```bash
# The script might be waiting for manual authorization
# Check if there's a URL printed in the console
# Copy and paste it into your browser manually
```

### If Tokens Still Don't Work After Setup

```bash
# Check if the OAuth credentials file exists
ls -la shared/mcp-servers/google-tasks-mcp-server/credentials.json

# If missing, the OAuth app isn't configured
# User needs to set up OAuth credentials in Google Cloud Console
```

### If Virtual Environment Missing

```bash
cd shared/mcp-servers/google-tasks-mcp-server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Common Issues

**Issue**: "Virtual environment not found" error
**Fix**: Create venv and install dependencies (see above)

**Issue**: Browser windows don't close automatically
**Fix**: Normal behavior - user must close them manually after seeing "Success"

**Issue**: "Credentials file not found" error
**Fix**: OAuth app not configured in Google Cloud Console - beyond scope of this skill

**Issue**: Tokens work but LaunchAgents still fail
**Fix**: Problem is elsewhere, not OAuth - check specific LaunchAgent logs

## Related Documentation

- Full technical details: `docs/OAUTH-TO-SERVICE-ACCOUNT-MIGRATION.md`
- Setup script: `shared/scripts/setup-oauth-once.sh`
- Automation docs: `docs/AUTOMATION.md`

## Success Criteria

Skill completes successfully when:
- ✅ Browser windows opened and user authorized
- ✅ Token files created/updated with refresh tokens
- ✅ Test connection to Google Tasks succeeds
- ✅ User understands tokens will auto-refresh indefinitely
