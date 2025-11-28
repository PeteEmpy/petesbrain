# MCP Service Account Emails

This document lists service account email addresses used by MCP servers for accessing Google services.

## Google Sheets & Docs Service Account

**Email**: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`

**Used by**: Google Sheets MCP Server
**Location**: `shared/mcp-servers/google-sheets-mcp-server/`
**Credentials**: `shared/mcp-servers/google-sheets-mcp-server/credentials.json`

### How to Share Google Sheets or Docs

1. Open the Google Sheet or Google Doc
2. Click "Share" button (top right)
3. Enter: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
4. Set permissions:
   - **Viewer** - Read-only access
   - **Editor** - Read and write access
5. **Uncheck "Notify people"** (service accounts don't need email notifications)
6. Click "Share"

### Getting the Spreadsheet/Document ID

After sharing, get the ID from the URL:

**Google Sheets**:
```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
```

**Google Docs**:
```
https://docs.google.com/document/d/[DOCUMENT_ID]/edit
```

The ID is the long string between `/d/` and `/edit`.

### Available MCP Tools

Once shared, you can use these tools in Claude Code:

**Google Sheets**:
- `mcp__google-sheets__list_sheets` - List all tabs in a spreadsheet
- `mcp__google-sheets__read_cells` - Read cell data from a range
- `mcp__google-sheets__write_cells` - Write data to cells (requires Editor permission)

---

## Future Service Accounts

Add additional service account emails here as new MCP servers are configured.
