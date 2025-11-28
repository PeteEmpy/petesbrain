# Google Drive MCP Server Setup

## Overview

This MCP server provides bulletproof Google Docs/Drive integration for Pete's Brain.

**What it enables:**
- ✅ Read Google Docs (auto-converted to Markdown)
- ✅ Read Google Sheets (auto-converted to CSV/JSON)
- ✅ Read Google Slides (auto-converted to text)
- ✅ Search across entire Google Drive
- ✅ List and browse folders
- ✅ Create, update, delete files
- ✅ Move and rename files

**Server:** [@piotr-agier/google-drive-mcp](https://github.com/piotr-agier/google-drive-mcp)

---

## Prerequisites

- Node.js and NPM installed (check: `node --version` and `npm --version`)
- Google Cloud account
- Google Drive access

---

## Setup Steps

### Step 1: Google Cloud Console Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create or Select Project:**
   - Create new project: "PetesBrain Google Drive"
   - Or use existing project

3. **Enable Required APIs:**
   - Go to: https://console.cloud.google.com/apis/library
   - Search and enable each:
     - ✅ Google Drive API
     - ✅ Google Docs API
     - ✅ Google Sheets API
     - ✅ Google Slides API

4. **Configure OAuth Consent Screen:**
   - Go to: https://console.cloud.google.com/apis/credentials/consent
   - User Type: **External** (unless you have Google Workspace)
   - App name: "PetesBrain"
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Add these scopes:
     - `https://www.googleapis.com/auth/drive`
     - `https://www.googleapis.com/auth/documents`
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/presentations`
   - Test users: Add your Google email

5. **Create OAuth Credentials:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: **Desktop app**
   - Name: "PetesBrain Desktop"
   - Click "Create"
   - **Download JSON** → Save as `gcp-oauth.keys.json` in this directory

---

### Step 2: Install and Authenticate

Run these commands:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server

# Authenticate (this will open browser)
npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json
```

This will:
1. Open your browser for Google OAuth login
2. Save tokens to `~/.config/google-drive-mcp/tokens.json`
3. Auto-refresh tokens when needed

---

### Step 3: Configuration

The `.mcp.json` configuration has been added automatically. The server will use:

- **Credentials**: `gcp-oauth.keys.json` in this directory
- **Tokens**: `~/.config/google-drive-mcp/tokens.json` (created on first auth)

---

### Step 4: Restart Claude Code

After setup completes, restart Claude Code to load the new MCP server.

---

## Testing

Once configured, test with:

```
User: "List my recent Google Docs"
User: "Read this Google Doc: https://docs.google.com/document/d/[ID]"
User: "Save this Google Doc to clients/devonshire-hotels/documents/"
```

---

## Available Tools

The Google Drive MCP server provides these tools:

### Search & Discovery
- `mcp__google-drive__search` - Search for files across Drive
- `mcp__google-drive__listFolder` - Browse folder contents

### Reading Files
- `mcp__google-drive__readFile` - Read any file (auto-converts Google Workspace formats)
- Google Docs → Markdown
- Google Sheets → CSV
- Google Slides → Plain text
- PDFs, images, etc. → Raw content

### File Management
- `mcp__google-drive__createTextFile` - Create new text/markdown files
- `mcp__google-drive__updateTextFile` - Update existing files
- `mcp__google-drive__createFolder` - Create folders
- `mcp__google-drive__deleteItem` - Delete files/folders
- `mcp__google-drive__renameItem` - Rename items
- `mcp__google-drive__moveItem` - Move to different folder

### Google Workspace
- `mcp__google-drive__createGoogleDoc` - Create new Google Doc
- `mcp__google-drive__updateGoogleDoc` - Update Google Doc content
- `mcp__google-drive__createGoogleSheet` - Create new Sheet
- `mcp__google-drive__updateGoogleSheet` - Update Sheet data
- `mcp__google-drive__createGoogleSlides` - Create presentation

---

## Workflow: Importing Google Docs to Client Folders

### Simple Import

```
User: "Add this Google Doc to Devonshire: https://docs.google.com/document/d/[ID]"
```

Claude Code will:
1. Use `mcp__google-drive__readFile` to fetch document (auto-converted to Markdown)
2. Save to `clients/devonshire-hotels/documents/[filename].md`
3. Add YAML frontmatter with metadata (source URL, date, etc.)

### Batch Import

```
User: "Import all Google Docs from this folder to Smythson documents: https://drive.google.com/drive/folders/[ID]"
```

Claude Code will:
1. List all files in folder
2. Filter for Google Docs
3. Import each to `clients/smythson/documents/`

---

## Troubleshooting

### "401 Unauthorized" Error

**Cause**: OAuth tokens expired or not authenticated

**Fix**:
```bash
npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json
```

### "403 Forbidden" Error

**Cause**: Missing API scopes or test user not added

**Fix**:
1. Go to OAuth consent screen
2. Add your email to "Test users"
3. Verify all 4 APIs are enabled
4. Re-authenticate

### "File not found" Error

**Cause**: File ID incorrect or no access permissions

**Fix**:
1. Verify file URL is correct
2. Check file sharing settings (must have at least View access)
3. Try opening the file in browser first

### Check Server Status

```bash
# List running MCP servers
# (In Claude Code, servers auto-start on demand)

# View MCP logs
# Check Claude Code logs for connection errors
```

---

## Security Notes

- OAuth tokens stored in `~/.config/google-drive-mcp/tokens.json`
- Credentials in `gcp-oauth.keys.json` (gitignored)
- Read/write access to your entire Google Drive
- Tokens auto-refresh (valid indefinitely until revoked)

**To revoke access:**
1. Go to: https://myaccount.google.com/permissions
2. Find "PetesBrain" app
3. Click "Remove Access"

---

## Maintenance

**Re-authenticate** (if tokens corrupted):
```bash
rm ~/.config/google-drive-mcp/tokens.json
npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json
```

**Update server** (get latest version):
```bash
npx @piotr-agier/google-drive-mcp@latest auth --credentials ./gcp-oauth.keys.json
```

---

## Documentation

- **MCP Server Repo**: https://github.com/piotr-agier/google-drive-mcp
- **Google Drive API Docs**: https://developers.google.com/drive/api/guides/about-sdk
- **Google Docs API Docs**: https://developers.google.com/docs/api
