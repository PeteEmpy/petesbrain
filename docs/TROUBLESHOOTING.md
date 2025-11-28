# Troubleshooting Guide

Common issues and solutions for Pete's Brain systems.

## LaunchAgent Issues

### Check if automation is active

```bash
launchctl list | grep petesbrain
```

This will show all Pete's Brain LaunchAgents and their status.

### Reload a specific agent

If an agent is not running or behaving incorrectly:

```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.[name].plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.[name].plist
```

Replace `[name]` with the specific service:
- `weekly-review` - Weekly meeting review email
- `kb-summary` - Knowledge base weekly summary
- `industry-news` - Industry news monitor
- `ai-news` - AI news monitor
- `tasks-monitor` - Google Tasks tracking
- `googlesheets.export` - Google Sheets exports
- `knowledge-base` - Knowledge base processor

### View logs

Each LaunchAgent should write to a log file. Check the log to see what's happening:

```bash
cat ~/.petesbrain-[name].log
```

Or for services that log to alternate locations, check the `StandardOutPath` and `StandardErrorPath` in the `.plist` file.

### Common LaunchAgent Problems

**Agent won't start:**
1. Check the plist file syntax is valid (use `plutil` to validate)
2. Verify all paths in the plist are absolute and correct
3. Check file permissions on the script being executed
4. Ensure the Python virtual environment exists and has correct permissions

**Agent runs but fails:**
1. Check the log file for error messages
2. Run the script manually with the same command specified in the plist
3. Verify environment variables are set correctly in the plist
4. Check that API keys and credentials are valid

---

## MCP Server Connection Issues

### Verify virtual environment and credentials

```bash
cd shared/mcp-servers/[server-name]
source .venv/bin/activate
python server.py  # Run manually to test
```

### Check .mcp.json configuration

1. Verify all paths in `.mcp.json` are absolute, not relative
2. Check that credential files exist at the specified paths
3. Ensure the MCP server command is correct

### Common MCP Server Problems

**Server won't start:**
- Check virtual environment exists and has dependencies installed
- Verify Python version compatibility (most require Python 3.8+)
- Check that required environment variables are set

**Authentication failures:**
- Delete expired token files (usually `token.json` in server directory)
- Re-run authentication flow
- Verify OAuth credentials or service account credentials are valid

**Server starts but tools don't work:**
- Check API quotas haven't been exceeded
- Verify the account has proper permissions for the resources being accessed
- Test API credentials directly with simple API calls

---

## Google API Authentication

### OAuth Token Expiration

If OAuth tokens expire, you'll see authentication errors. To fix:

1. Delete `token.json` in the MCP server directory:
   ```bash
   rm shared/mcp-servers/[server-name]/token.json
   ```

2. Re-run the server - it will prompt for re-authentication:
   ```bash
   cd shared/mcp-servers/[server-name]
   source .venv/bin/activate
   python server.py
   ```

3. Follow the browser OAuth flow that opens
4. Restart Claude Code to pick up the new token

### OAuth Popup on Every Claude Code Startup

**Problem**: Browser OAuth window appears every time Claude Code starts, even after authorizing

**Root Cause**: MCP server's OAuth config path not specified in `.mcp.json`, causing it to re-authenticate every session

**Solution** (Google Analytics example):

1. **Check if token exists but keeps prompting**:
   ```bash
   ls -lh /Users/administrator/Downloads/google_analytics_token.json
   # If token exists but expired, delete it
   rm /Users/administrator/Downloads/google_analytics_token.json
   ```

2. **Add OAuth config path to `.mcp.json`**:
   ```json
   "google-analytics": {
     "command": "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/.venv/bin/python",
     "args": ["/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/server.py"],
     "env": {
       "CLIENT_IDS_PATH": "/Users/administrator/Documents/PetesBrain/data/state/client-platform-ids.json",
       "PLATFORM_IDS_HELPER": "/Users/administrator/Documents/PetesBrain/shared/platform_ids.py",
       "GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH": "/Users/administrator/Downloads/client_secret_XXXXX.apps.googleusercontent.com.json"
     }
   }
   ```

3. **Restart Claude Code** - It will create fresh token with auto-refresh

4. **Verify fix**:
   ```bash
   # Check new token was created
   ls -lh /Users/administrator/Downloads/google_analytics_token.json

   # Check token has expiry (not expired)
   cat /Users/administrator/Downloads/google_analytics_token.json | grep expiry
   ```

**Why this works**:
- Without `GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH` in `.mcp.json`, the MCP server can't find the credentials or stored token
- Even if token exists, it won't be loaded without the config path
- Adding the env variable allows proper token storage and auto-refresh

**Other OAuth-based MCP servers**:
- **Google Drive**: Uses `~/.config/google-drive-mcp/tokens.json` (npx-based, managed automatically)
- **Google Tasks**: Token stored in `infrastructure/mcp-servers/google-tasks-mcp-server/token.json`
- **Google Photos**: Token stored in `infrastructure/mcp-servers/google-photos-mcp-server/token.json`

### Service Account Issues

For servers using service account credentials (e.g., Google Sheets):

1. Verify the service account JSON file exists and is valid
2. Check that the service account has been granted access to the resources
   - For Google Sheets: Share the sheet with the service account email
   - For Google Drive: Share folders/files with the service account email
3. Verify the service account has the necessary API permissions in Google Cloud Console

### Common Google API Errors

**403 Forbidden:**
- Service account doesn't have access to the resource
- Share the resource with the service account email address

**401 Unauthorized:**
- OAuth token has expired - delete `token.json` and re-authenticate
- API key is invalid or missing

**429 Too Many Requests:**
- API quota exceeded - wait and retry, or request quota increase in Google Cloud Console

**404 Not Found:**
- Resource ID is incorrect
- Resource was deleted or moved
- Account doesn't have access to see the resource

---

## Claude Code Issues

### Multiple Installations

If `claude doctor` shows multiple installations:

```bash
claude migrate-installer
```

This will migrate to the native installer which doesn't require sudo for updates.

### Context Too Large

If CLAUDE.md or MCP tools context is too large:

**CLAUDE.md too large:**
- Move detailed documentation to separate files in `docs/`
- Keep only essential guidance in CLAUDE.md
- Reference external docs with links

**MCP tools context too large:**
- Disable unused MCP servers in `.mcp.json`
- Review if all tools from each server are needed
- Consider splitting functionality across multiple specialized servers

### Auto-updates Not Working

If Claude Code auto-updates aren't working:

**npm-global installation:**
- Requires sudo for updates, which won't work automatically
- Solution: Run `claude migrate-installer` to switch to native installer

**Permission issues:**
- Check file permissions on `~/.local/bin/claude` (native install)
- Ensure you own the installation directory

---

## Python Script Issues

### Virtual Environment Problems

**venv doesn't exist:**
```bash
cd [script-directory]
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Wrong Python version:**
```bash
python3 --version  # Check version
# If too old, install newer Python and recreate venv
```

**Dependencies missing:**
```bash
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Environment Variables Not Set

Many scripts require environment variables (API keys, credentials):

**Check if set:**
```bash
echo $ANTHROPIC_API_KEY
echo $GOOGLE_APPLICATION_CREDENTIALS
```

**Set temporarily:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

**Set permanently (add to `~/.bashrc` or `~/.zshrc`):**
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Script Fails Silently

Check log files for error messages:
- LaunchAgent logs: `~/.petesbrain-[name].log`
- Script-specific logs: Check `shared/data/` for log files
- System logs: `tail -f /var/log/system.log` (macOS)

---

## Database/State File Issues

### State Files Corrupted

If state files become corrupted (JSON parsing errors):

**Backup and reset:**
```bash
# Backup the corrupted file
cp shared/data/[file].json shared/data/[file].json.bak

# Reset to empty state
echo '{}' > shared/data/[file].json
# OR for arrays:
echo '[]' > shared/data/[file].json
```

**Common state files:**
- `shared/data/tasks-state.json` - Google Tasks tracking state
- `shared/data/tasks-completed.json` - Completed tasks log
- `shared/data/industry-news-state.json` - Industry news monitor state
- `shared/data/ai-news-state.json` - AI news monitor state
- `shared/data/kb-processing.log` - Knowledge base processor log

---

## Email/Gmail Issues

### Gmail API Quota Exceeded

Gmail API has usage quotas. If exceeded:

1. Wait for quota to reset (usually daily)
2. Check quota usage in Google Cloud Console
3. Request quota increase if needed

### Emails Not Sending

**Check credentials:**
```bash
ls -la shared/email-sync/credentials.json
# Should exist and be readable
```

**Test Gmail API access:**
```bash
cd shared/email-sync
source .venv/bin/activate
python -c "from google.oauth2 import service_account; print('OK')"
```

**Check service account has Gmail API access:**
- Go to Google Cloud Console
- Verify Gmail API is enabled
- Check service account has necessary permissions

---

## Granola Meeting Importer Issues

### Meetings Not Importing

**Check Granola API key:**
- Verify `GRANOLA_API_KEY` is set in the environment
- Test API key with a simple curl request

**Check daemon is running:**
```bash
ps aux | grep granola
```

**Restart daemon:**
```bash
cd tools/granola-importer
./stop.sh  # If stop script exists
./start.sh
```

### Wrong Client Assignment

Granola's AI may mis-assign meetings to wrong clients:

**Run validation script:**
```bash
./shared/scripts/review-meeting-client.sh
```

This will list all meetings and let you move them to the correct client folder.

---

## Git Issues

### Uncommitted Changes Blocking Operations

If you have many uncommitted changes:

**View status:**
```bash
git status
```

**Commit changes:**
```bash
git add -A
git commit -m "[category]: description"
```

**Or stash changes temporarily:**
```bash
git stash
# Do your operation
git stash pop  # Restore changes
```

### Merge Conflicts

If you get merge conflicts:

1. Open the conflicted files
2. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Manually resolve conflicts
4. Remove conflict markers
5. Stage and commit the resolved files

---

## Systemic Issues Protocol

### When One Issue Might Be Everywhere

**If you discover a structural or configuration issue in ONE location, always check if it's SYSTEMIC across all similar locations.**

**Example**: Found `tasks.json` in wrong location (`product-feeds/` instead of client root) for one client. Immediately discovered 15+ other clients had the same issue.

**Protocol**:
1. **Discover** - Issue found in one location
2. **Question** - "Could this be wrong elsewhere?"
3. **Audit** - Run system-wide check (`find`, Python scan, etc.)
4. **Document** - Record total scope (X clients/files affected)
5. **Fix** - Migrate ALL at once (single comprehensive script)
6. **Verify** - Re-run audit (should find 0 remaining issues)
7. **Prevent** - Update documentation to prevent recurrence

**Key principle**: "Fix one, check all, migrate everything."

**Full protocol**: See `/docs/SYSTEMIC-ISSUE-PROTOCOL.md` for detailed procedures and examples.

---

## Getting Help

### Log Files to Check

When troubleshooting, check these logs in order:

1. **LaunchAgent logs**: `~/.petesbrain-*.log`
2. **Script-specific logs**: `shared/data/*.log`
3. **System logs**: `/var/log/system.log` (macOS)
4. **Claude Code logs**: Check terminal output when running `claude` commands

### Useful Diagnostic Commands

```bash
# Check all Pete's Brain LaunchAgents
launchctl list | grep petesbrain

# Check Python virtual environments
ls -la shared/*/.*venv

# Check file permissions
ls -la shared/scripts/
ls -la shared/mcp-servers/

# Check disk space
df -h

# Check running processes
ps aux | grep -E "python|claude|granola"
```

### Contact Information

For issues specific to:
- **Claude Code**: https://github.com/anthropics/claude-code/issues
- **Pete's Brain custom code**: Document the issue and contact the maintainer
