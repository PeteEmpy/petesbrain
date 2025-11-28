# Google Drive MCP Server - Setup Checklist

Use this checklist to track your setup progress.

---

## ☐ Part 1: Google Cloud Console (15 minutes)

### ☐ 1.1 Create/Select Project
- [ ] Go to: https://console.cloud.google.com/
- [ ] Create new project "PetesBrain Google Drive" OR select existing project
- [ ] Note project ID: `____________________`

### ☐ 1.2 Enable APIs
Go to: https://console.cloud.google.com/apis/library

- [ ] Enable **Google Drive API**
- [ ] Enable **Google Docs API**
- [ ] Enable **Google Sheets API**
- [ ] Enable **Google Slides API**

### ☐ 1.3 Configure OAuth Consent Screen
Go to: https://console.cloud.google.com/apis/credentials/consent

- [ ] User Type: **External**
- [ ] App name: `PetesBrain`
- [ ] User support email: `____________________`
- [ ] Developer contact email: `____________________`
- [ ] Add scopes:
  - [ ] `https://www.googleapis.com/auth/drive`
  - [ ] `https://www.googleapis.com/auth/documents`
  - [ ] `https://www.googleapis.com/auth/spreadsheets`
  - [ ] `https://www.googleapis.com/auth/presentations`
- [ ] Add test users:
  - [ ] Add your Google email: `____________________`
- [ ] Save and continue

### ☐ 1.4 Create OAuth Credentials
Go to: https://console.cloud.google.com/apis/credentials

- [ ] Click "Create Credentials" → "OAuth client ID"
- [ ] Application type: **Desktop app**
- [ ] Name: `PetesBrain Desktop`
- [ ] Click **Create**
- [ ] **Download JSON** file
- [ ] Rename to `gcp-oauth.keys.json`
- [ ] Save to: `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server/`

---

## ☐ Part 2: Local Setup (5 minutes)

### ☐ 2.1 Verify Files
- [ ] File exists: `gcp-oauth.keys.json` in this directory
- [ ] File is valid JSON (open in text editor to verify)

### ☐ 2.2 Run Authentication
```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server
npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json
```

- [ ] Command opens browser
- [ ] Logged in with Google account
- [ ] Approved permissions
- [ ] Browser shows "Authentication successful"
- [ ] Terminal shows success message
- [ ] Tokens saved to `~/.config/google-drive-mcp/tokens.json`

### ☐ 2.3 Verify Configuration
- [ ] `.mcp.json` includes `google-drive` server (already done ✅)
- [ ] Credentials path is correct in `.mcp.json`

---

## ☐ Part 3: Testing (5 minutes)

### ☐ 3.1 Restart Claude Code
- [ ] Quit Claude Code completely
- [ ] Restart Claude Code
- [ ] Wait for MCP servers to initialize (~10 seconds)

### ☐ 3.2 Test Basic Commands

Try in Claude Code:

**Test 1: List files**
```
"List my recent Google Docs from Drive"
```
- [ ] Command succeeds
- [ ] Shows list of your Google Docs

**Test 2: Read a document**
```
"Read this Google Doc: [paste a Google Docs URL]"
```
- [ ] Command succeeds
- [ ] Shows document content

**Test 3: Import to client folder**
```
"Add this Google Doc to Devonshire: https://docs.google.com/document/d/1Rb1QZEWZKYxM9JMFKHu0sfo3fylwEChH4MwfQw4nE3U"
```
- [ ] Command succeeds
- [ ] File saved to `clients/devonshire-hotels/documents/`
- [ ] File is valid Markdown

---

## ☐ Part 4: Finalization

### ☐ 4.1 Security Check
- [ ] `gcp-oauth.keys.json` is gitignored (already configured ✅)
- [ ] Tokens stored securely in `~/.config/google-drive-mcp/`
- [ ] OAuth consent screen configured correctly

### ☐ 4.2 Documentation
- [ ] Read `README.md` for common workflows
- [ ] Bookmark `SETUP.md` for troubleshooting
- [ ] Understand available MCP tools (see `SETUP.md`)

---

## Troubleshooting

If you encounter issues during setup, see `SETUP.md` → Troubleshooting section.

### Common Issues:

**Browser doesn't open during auth**
- Manually visit the URL shown in terminal

**403 Forbidden after auth**
- Add your email to OAuth consent screen test users
- Re-run auth command

**401 Unauthorized when testing**
- Delete `~/.config/google-drive-mcp/tokens.json`
- Re-run auth command

**MCP server not available in Claude Code**
- Verify `.mcp.json` syntax is valid
- Check credentials file path is absolute
- Restart Claude Code

---

## Status Tracking

**Started**: `____________________` (date)
**Completed**: `____________________` (date)
**Tested by**: `____________________` (your name)

**Notes**:
```
[Add any notes, issues encountered, or customizations here]
```

---

## Next Steps After Setup

Once setup is complete, you can:

1. **Import Google Docs** - Just provide URLs and target client folders
2. **Search Drive** - Find documents across your entire Drive
3. **Bulk import** - Import entire folders of documents
4. **Auto-sync** (future) - Automate document imports on schedule

See `README.md` for common workflows and examples.
