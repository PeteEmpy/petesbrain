# Shared Scripts Virtual Environment

## Purpose

This `.venv` is a **dedicated virtual environment** for all shared automation scripts in `/shared/scripts/`.

**Created:** 2025-11-10
**Reason:** To prevent missing dependency issues when creating new monitoring/automation scripts.

## Installed Libraries

All scripts in `shared/scripts/` should use this venv and can rely on these libraries:

### Google APIs
- `google-ads` (28.4.0) - Official Google Ads API library (gRPC-based)
- `google-api-python-client` (2.187.0) - Google REST APIs (Sheets, Drive, etc.)
- `google-auth` (2.41.1) - Authentication for Google APIs
- `google-auth-oauthlib` (1.2.3) - OAuth flow for Google APIs
- `google-auth-httplib2` (0.2.1) - HTTP transport for Google Auth

### Anthropic AI
- `anthropic` (0.72.0) - Claude API for AI-powered analysis

### Standard Libraries
- `requests` - HTTP requests
- `PyYAML` - YAML parsing (for google-ads.yaml config)
- All standard Python libraries (smtplib, email, datetime, etc.)

## Usage in Scripts

**Shebang line for all scripts:**
```python
#!/Users/administrator/Documents/PetesBrain/shared/scripts/.venv/bin/python3
```

**Example:**
```python
#!/Users/administrator/Documents/PetesBrain/shared/scripts/.venv/bin/python3
"""
My Monitoring Script
"""

from google.ads.googleads.client import GoogleAdsClient
import anthropic
# ... rest of imports
```

## Usage in LaunchAgents

**ProgramArguments:**
```xml
<key>ProgramArguments</key>
<array>
    <string>/Users/administrator/Documents/PetesBrain/shared/scripts/.venv/bin/python3</string>
    <string>/Users/administrator/Documents/PetesBrain/shared/scripts/my-script.py</string>
</array>
```

## Adding New Libraries

If a new script needs additional libraries:

```bash
shared/scripts/.venv/bin/pip install <package-name>
```

Then **update this README** with the new library and version.

## Scripts Using This Venv

- `wheatybags-monitoring.py` - WheatyBags Search campaign monitoring (10am/5pm emails)
- [Add new scripts here as they're created]

## LaunchAgents Using This Venv

- `com.petesbrain.wheatybags-monitor` - WheatyBags monitoring emails

## DO NOT

- ❌ Do NOT use `/usr/local/bin/python3` for shared scripts
- ❌ Do NOT use MCP server venvs for scripts (`shared/mcp-servers/*/venv/`)
- ❌ Do NOT install packages globally with `pip3 install`

## DO

- ✅ Always use this venv: `shared/scripts/.venv/bin/python3`
- ✅ Install packages to this venv: `shared/scripts/.venv/bin/pip install`
- ✅ Update this README when adding new libraries

## Troubleshooting

**Script says "ModuleNotFoundError"?**
1. Check if library is listed above
2. If not, install it: `shared/scripts/.venv/bin/pip install <package>`
3. Update this README

**LaunchAgent not finding Python?**
1. Check ProgramArguments uses absolute path: `/Users/administrator/Documents/PetesBrain/shared/scripts/.venv/bin/python3`
2. Check script shebang matches

## Maintenance

**To recreate venv from scratch:**
```bash
cd /Users/administrator/Documents/PetesBrain/shared/scripts
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install google-ads google-api-python-client google-auth anthropic
```

**To verify installation:**
```bash
shared/scripts/.venv/bin/pip list
```
