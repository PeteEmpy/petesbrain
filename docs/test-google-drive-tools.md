# Google Drive MCP Tools Test

## Test Instructions for Other Claude Session

Copy and paste this into your other Claude Code session:

```
Please call the MCP tool directly:

mcp__google-drive__search with parameters:
- query: "name contains 'test'"
- page_size: 5
```

## Expected Result

You should see a list of files from Google Drive that match the search query.

## If It Fails

The error message will tell us:
1. "Tool not found" = MCP server not loaded in that session
2. "Permission denied" = Tool exists but needs permission
3. Other error = Different issue

## Verification Command

Run this in your other session's terminal:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync
claude mcp list | grep google-drive
```

Should show:
```
google-drive: .../google-drive-mcp-server-custom/.venv/bin/python .../server.py - ✓ Connected
```
