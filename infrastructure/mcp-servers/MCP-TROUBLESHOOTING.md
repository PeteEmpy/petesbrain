# MCP Server Troubleshooting Guide

## Quick Fixes

### When Google Ads MCP queries fail:

**FIRST: Try the restart script**
```bash
./shared/mcp-servers/restart-mcp-servers.sh
```
Then restart Claude Code (Cmd+Q, wait 5 seconds, reopen).

**SECOND: Run health check**
```bash
cd shared/mcp-servers/google-ads-mcp-server
./health-check.sh
```

## Common Issues

### 1. "ModuleNotFoundError" - Missing fastmcp dependency

**Problem:** MCP server configured in `.mcp.json` but tools don't load. Server fails with `ModuleNotFoundError: No module named 'fastmcp'`

**Root Cause:** FastMCP servers require `fastmcp` package in requirements.txt (per MCP-IMPLEMENTATION-PATTERNS.md line 36)

**Fix:**
```bash
cd infrastructure/mcp-servers/[server-name]

# 1. Add fastmcp to requirements.txt if missing
echo "fastmcp>=0.8.0" >> requirements.txt

# 2. Install dependencies
.venv/bin/pip install -r requirements.txt

# 3. Test server starts
.venv/bin/python server.py
# Should see: "Starting [Server Name] MCP Server..." (then Ctrl+C to stop)

# 4. Restart Claude Code
```

**Verify:**
```bash
# Test server.py imports work
.venv/bin/python -c "from fastmcp import FastMCP; print('fastmcp OK')"
```

**Example:** YouTube MCP Server (fixed December 16, 2025) - was missing fastmcp in requirements.txt

### 2. "ModuleNotFoundError" - Other missing dependencies

**Problem:** MCP server's venv is missing Python packages

**Fix:**
```bash
cd shared/mcp-servers/google-ads-mcp-server
.venv/bin/pip install -r requirements.txt
```

**Verify:**
```bash
./health-check.sh  # If available
```

### 2. MCP query times out or hangs

**Problem:** Server process is stuck or crashed

**Fix:**
```bash
# Kill stuck processes
pkill -f "google-ads-mcp-server"

# Restart Claude Code completely
# Cmd+Q, wait 5 seconds, reopen
```

### 3. MCP server not starting at all

**Check .mcp.json paths:**
```bash
cat .mcp.json | grep google-ads -A 5
```

Should show:
```json
"google-ads": {
  "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv/bin/python",
  "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/server.py"],
```

**Verify paths exist:**
```bash
ls -la shared/mcp-servers/google-ads-mcp-server/.venv/bin/python
ls -la shared/mcp-servers/google-ads-mcp-server/server.py
```

### 4. "Authentication failed" errors

**Check google-ads.yaml:**
```bash
cat ~/google-ads.yaml
```

Should have:
- developer_token
- client_id
- client_secret
- refresh_token

**Test authentication manually:**
```bash
cd shared/mcp-servers/google-ads-mcp-server
.venv/bin/python list_accounts_direct.py
```

### 5. Claude Code can't see MCP tools

**Problem:** .mcp.json not loaded or corrupted

**Fix:**
1. Validate JSON syntax:
```bash
cat .mcp.json | python3 -m json.tool
```

2. Check file location:
```bash
ls -la .mcp.json
# Should be in /Users/administrator/Documents/PetesBrain/.mcp.json
```

3. Restart Claude Code completely

## Preventive Measures

### 1. Keep venvs updated

Add to monthly maintenance:
```bash
cd shared/mcp-servers/google-ads-mcp-server
.venv/bin/pip install --upgrade google-ads fastmcp google-api-python-client
```

### 2. Monitor MCP logs

When queries fail, check:
```bash
tail -100 ~/Library/Logs/Claude/mcp*.log
```

### 3. Regular health checks

Before important work:
```bash
cd shared/mcp-servers/google-ads-mcp-server
./health-check.sh
```

## Debugging Steps

### Step 1: Is the server running?

```bash
ps aux | grep mcp-server
```

Should see multiple Python processes for different MCP servers.

### Step 2: Can the server start manually?

```bash
cd shared/mcp-servers/google-ads-mcp-server
GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml .venv/bin/python server.py
```

Should see "Starting Google Ads MCP Server..." and FastMCP banner.
Press Ctrl+C to stop.

### Step 3: Can Python import the libraries?

```bash
shared/mcp-servers/google-ads-mcp-server/.venv/bin/python -c "
from google.ads.googleads.client import GoogleAdsClient
print('✅ Import successful')
"
```

### Step 4: Can we query Google Ads API directly?

```bash
cd shared/mcp-servers/google-ads-mcp-server
.venv/bin/python list_accounts_direct.py
```

Should list all your Google Ads accounts.

## Nuclear Option

If nothing works, rebuild the venv:

```bash
cd shared/mcp-servers/google-ads-mcp-server
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

Then restart Claude Code.

## Getting Help

If issue persists:

1. Capture logs:
```bash
tail -200 ~/Library/Logs/Claude/mcp*.log > ~/Desktop/mcp-logs.txt
```

2. Run diagnostics:
```bash
cd shared/mcp-servers/google-ads-mcp-server
./health-check.sh > ~/Desktop/health-check.txt 2>&1
```

3. Check server startup:
```bash
GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml \
shared/mcp-servers/google-ads-mcp-server/.venv/bin/python \
shared/mcp-servers/google-ads-mcp-server/server.py \
> ~/Desktop/server-startup.txt 2>&1 &

sleep 5
pkill -f google-ads-mcp-server
```

Attach all three files when asking for help.
