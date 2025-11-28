# Google Drive MCP Server

**Bulletproof Google Docs/Drive integration for Pete's Brain**

## Quick Start

### 1. Complete Google Cloud Setup

Follow the detailed guide in [`SETUP.md`](./SETUP.md) to:
- Create OAuth credentials in Google Cloud Console
- Enable required APIs (Drive, Docs, Sheets, Slides)
- Download `gcp-oauth.keys.json` to this directory

### 2. Authenticate

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server
npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json
```

This opens your browser for Google OAuth login. Tokens are saved to `~/.config/google-drive-mcp/tokens.json`.

### 3. Restart Claude Code

The MCP server is already configured in `.mcp.json`. Just restart Claude Code to activate it.

### 4. Test It

Try these commands in Claude Code:

```
"List my recent Google Docs"
"Read this Google Doc: https://docs.google.com/document/d/1Rb1QZEWZKYxM9JMFKHu0sfo3fylwEChH4MwfQw4nE3U"
"Add that Google Doc to Devonshire client folder"
```

---

## Common Workflows

### Import Single Google Doc to Client Folder

```
User: "Add this Google Doc to [client-name]: [Google Docs URL]"
```

Claude Code will:
1. Fetch the document (auto-converted to Markdown)
2. Save to `clients/[client-name]/documents/[filename].md`
3. Add metadata (source URL, date imported, etc.)

### Import Multiple Docs from Folder

```
User: "Import all Google Docs from this folder to Smythson: [Google Drive folder URL]"
```

### Search and Import

```
User: "Find all Google Docs about 'Q4 strategy' and import relevant ones to clients/"
```

---

## What It Can Do

✅ **Read files** - Auto-converts Google Docs/Sheets/Slides to Markdown/CSV/text
✅ **Search Drive** - Find files across your entire Google Drive
✅ **List folders** - Browse folder contents with path support
✅ **Create files** - Create new Google Docs, Sheets, text files
✅ **Update files** - Edit existing documents
✅ **File management** - Delete, rename, move files/folders

---

## File Conversions

| Google Format | Converts To |
|---------------|-------------|
| Google Docs | Markdown |
| Google Sheets | CSV / JSON |
| Google Slides | Plain text |
| PDFs | Text extraction |
| Images | Base64 / metadata |
| Other files | Raw content |

---

## Status: ⏳ Pending Setup

**Current status**: Configuration ready, awaiting OAuth credentials

**Next step**: Complete Google Cloud setup (see `SETUP.md`)

**Setup checklist**: See `SETUP_CHECKLIST.md`

---

## Documentation

- **Full Setup Guide**: [`SETUP.md`](./SETUP.md)
- **Setup Checklist**: [`SETUP_CHECKLIST.md`](./SETUP_CHECKLIST.md)
- **Upstream Repo**: https://github.com/piotr-agier/google-drive-mcp
- **Google Drive API**: https://developers.google.com/drive/api

---

## Troubleshooting

See `SETUP.md` → Troubleshooting section for common issues and fixes.

**Quick fixes:**
- 401 error → Re-authenticate: `npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json`
- 403 error → Add your email to OAuth consent screen test users
- File not found → Verify file sharing permissions
