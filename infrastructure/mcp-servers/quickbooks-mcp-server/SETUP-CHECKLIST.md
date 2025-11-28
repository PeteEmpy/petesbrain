# QuickBooks MCP Server - Setup Checklist

Use this checklist to ensure everything is properly configured.

## Pre-Setup

- [ ] Have QuickBooks Online account access
- [ ] Have Python 3.8+ installed
- [ ] Have Cursor installed

## QuickBooks Developer Setup

- [ ] Created account at [developer.intuit.com](https://developer.intuit.com)
- [ ] Created new app in developer portal
- [ ] Selected "QuickBooks Online and Payments"
- [ ] Noted Client ID
- [ ] Noted Client Secret
- [ ] Added redirect URI: `http://localhost:8000/callback`
- [ ] Enabled "Accounting" scope

## Server Installation

- [ ] Navigated to server directory
  ```bash
  cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server
  ```
- [ ] Installed dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Created `.env` file from template
  ```bash
  cp env.example .env
  ```
- [ ] Added credentials to `.env` file
  - Client ID
  - Client Secret
  - Redirect URI

## OAuth Authentication

- [ ] Ran OAuth setup script
  ```bash
  python setup_oauth.py
  ```
- [ ] Browser opened automatically
- [ ] Logged into QuickBooks
- [ ] Selected correct company
- [ ] Clicked "Authorize"
- [ ] Saw success message
- [ ] `token.json` file created

## Connection Testing

- [ ] Ran connection test
  ```bash
  python test_connection.py
  ```
- [ ] All tests passed ✅
  - Environment variables ✓
  - Token file ✓
  - Token refresh ✓
  - API connection ✓
  - Report access ✓

## Cursor Integration

- [ ] Located Cursor settings file:
  ```
  ~/Library/Application Support/Cursor/User/globalStorage/settings.json
  ```
- [ ] Added MCP server configuration:
  ```json
  {
    "mcpServers": {
      "quickbooks-reporting": {
        "command": "python",
        "args": [
          "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/server.py"
        ],
        "env": {
          "QUICKBOOKS_CLIENT_ID": "your_client_id",
          "QUICKBOOKS_CLIENT_SECRET": "your_client_secret"
        }
      }
    }
  }
  ```
- [ ] Saved settings file
- [ ] Restarted Cursor

## Verification

- [ ] Opened Cursor
- [ ] Started new chat
- [ ] Tested with simple query:
  ```
  Get the profit and loss report for this year
  ```
- [ ] Received report data successfully
- [ ] Tested additional queries:
  - [ ] Balance sheet
  - [ ] Cash flow
  - [ ] Company info
  - [ ] Chart of accounts

## Post-Setup

- [ ] Saved `.env` file in secure location (backup)
- [ ] Verified `.env` and `token.json` are in `.gitignore`
- [ ] Documented which QuickBooks company is connected
- [ ] Set calendar reminder for token refresh (in ~90 days)

## Troubleshooting Done

If you encountered issues, check what you fixed:

- [ ] Port 8000 was busy → Changed to different port
- [ ] Browser didn't open → Manually copied URL
- [ ] Wrong company connected → Re-ran setup_oauth.py
- [ ] Scope missing → Added Accounting scope in developer portal
- [ ] Token expired → Re-authenticated
- [ ] Other: _______________

## Notes

Record any important information:

**QuickBooks Company Connected:**
- Company Name: _________________
- Realm ID: _________________
- Date Connected: _________________

**App Details:**
- App Name: _________________
- Client ID (last 5 chars): _________________

**Custom Configuration:**
- Redirect URI (if different): _________________
- Environment (sandbox/production): _________________

---

## Quick Reference Commands

```bash
# Re-authenticate
python setup_oauth.py

# Test connection
python test_connection.py

# Run server directly (for testing)
python server.py

# Check token expiration
cat token.json | grep expires_at

# View logs
tail -f /tmp/quickbooks-mcp.log  # if logging to file
```

## Support

**If all checkboxes are checked and tests pass:**
✅ You're ready to go! Start asking QuickBooks questions in Cursor.

**If something didn't work:**
1. Review the failed step(s) above
2. Check [README.md](./README.md) for detailed troubleshooting
3. Verify credentials in developer portal
4. Make sure QuickBooks company is active

## Security Reminder

🔒 **Never commit these files:**
- `.env` (contains secrets)
- `token.json` (contains auth tokens)

Both are already in `.gitignore` but double-check!

---

**Setup completed on:** _________________ by _________________

**Ready for use:** [ ] YES  [ ] NO

**Next review/re-auth needed:** _________________ (in ~90 days)

