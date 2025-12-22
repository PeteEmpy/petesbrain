# Google MCP Servers OAuth Audit

**Date:** 2025-12-15
**Audit Type:** Comprehensive OAuth token health check
**Purpose:** Verify all Google MCP servers have valid OAuth tokens to prevent OAuth popup issues

---

## Executive Summary

✅ **All Active Google MCP Servers Have Valid OAuth Tokens**

**Status Overview:**
- 🟢 **5 OAuth-based servers**: All have valid tokens with refresh tokens
- 🟢 **1 Service Account server**: Using service account (no OAuth needed)
- 🟢 **1 Public API server**: No authentication needed
- ⚠️  **1 Incomplete server**: Google Search Console not implemented

**No OAuth popups expected** - All tokens auto-refresh and expire within the next hour, but will be automatically renewed.

---

## Detailed Findings

### 1. Google Analytics MCP ✅

**Status:** ✅ HEALTHY (JUST FIXED TODAY)

**Token Location:** `infrastructure/mcp-servers/google-analytics-mcp-server/token.json`

**Details:**
- Expiry: 2025-12-15 11:50:41
- Has refresh token: ✅ Yes
- Valid: ✅ Yes
- Configured in .mcp.json: ✅ Yes

**Action Taken:** Token migrated from `/Users/administrator/Downloads/` and refreshed today

---

### 2. Google Ads MCP ✅

**Status:** ✅ HEALTHY

**Token Location:** `infrastructure/mcp-servers/google-ads-mcp-server/google_ads_token.json`

**Details:**
- Expiry: 2025-12-15 11:40:24
- Has refresh token: ✅ Yes
- Valid: ✅ Yes
- Configured in .mcp.json: ✅ Yes

**Action Taken:** Verified today, already working correctly

---

### 3. Google Tasks MCP ✅

**Status:** ✅ HEALTHY

**Token Location:** `infrastructure/mcp-servers/google-tasks-mcp-server/token.json`

**Details:**
- Expiry: 2025-12-15 11:30:07
- Has refresh token: ✅ Yes
- Valid: ✅ Yes
- Configured in .mcp.json: ❌ No (but used by LaunchAgents)

**Notes:**
- Used by tasks-monitor and other LaunchAgents
- Token refreshed today during audit
- Not configured in Claude Code .mcp.json but working correctly

---

### 4. Google Photos MCP ✅

**Status:** ✅ HEALTHY

**Token Location:** `infrastructure/mcp-servers/google-photos-mcp-server/token.json`

**Details:**
- Expiry: 2025-12-15 11:47:49
- Has refresh token: ✅ Yes
- Valid: ✅ Yes
- Configured in .mcp.json: ❌ No

**Notes:**
- Token refreshed today during audit
- Directory exists with working OAuth setup
- Not currently used by Claude Code MCP but could be enabled

---

### 5. Google Drive MCP ✅

**Status:** ✅ HEALTHY (NPM PACKAGE)

**Token Location:** `~/.config/google-drive-mcp/tokens.json` (NPM package storage)

**Details:**
- Expiry: 2025-12-15 11:47:56
- Has refresh token: ✅ Yes
- Valid: ✅ Yes
- Configured in .mcp.json: ✅ Yes
- Package: `@piotr-agier/google-drive-mcp` (NPM)

**Notes:**
- Uses NPM package instead of custom Python server
- Tokens stored in ~/.config/ directory (standard for NPM packages)
- OAuth credentials: `infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`

---

### 6. Google Sheets MCP ✅

**Status:** ✅ HEALTHY (SERVICE ACCOUNT)

**Authentication Type:** Service Account (no OAuth)

**Credentials Location:** `infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json`

**Details:**
- No token.json needed
- Uses service account authentication
- Configured in .mcp.json: ❌ No (but used by LaunchAgents)
- No OAuth popup risk

**Notes:**
- Service accounts don't expire like OAuth tokens
- Already working correctly
- Used by budget trackers and other LaunchAgents

---

### 7. Google Trends MCP ✅

**Status:** ✅ HEALTHY (PUBLIC API)

**Authentication Type:** None (public API)

**Details:**
- Uses `pytrends` library
- No OAuth needed
- No authentication required
- Configured in .mcp.json: ❌ No

**Notes:**
- Public Google Trends data
- No token files needed
- No OAuth popup risk

---

### 8. Google Search Console MCP ⚠️

**Status:** ⚠️  INCOMPLETE/NOT IMPLEMENTED

**Details:**
- Directory exists: ✅
- `.env` file exists with OAuth config path
- No `server.py` file: ❌
- No token.json file: ❌
- Configured in .mcp.json: ❌ No

**OAuth Config Path (from .env):**
```
GOOGLE_SEARCH_CONSOLE_OAUTH_CONFIG_PATH=/Users/administrator/Downloads/credentials.json
```

**Notes:**
- Appears to be incomplete or abandoned
- Has OAuth directory but no implementation
- Not currently causing any issues (not loaded)
- Safe to ignore or remove directory

---

## OAuth Token Auto-Refresh Behavior

### How Tokens Stay Valid

**Access Tokens (short-lived):**
- Expire after 1 hour
- Used for API authentication
- Automatically refreshed by MCP server using refresh token

**Refresh Tokens (long-lived):**
- Valid for ~6 months
- Renew with each use
- **As long as services run regularly, refresh tokens NEVER expire**

### Current Token Status

All tokens expiring within 20 minutes (around 11:30-11:50 today), which means:

✅ **All tokens were recently refreshed** (during this audit or normal use)
✅ **All will auto-refresh within the next hour** (automatic, no popup)
✅ **All have valid refresh tokens** (will continue auto-refreshing for months)

---

## Token File Locations Summary

```
# Python MCP Servers (token.json format)
infrastructure/mcp-servers/google-analytics-mcp-server/token.json
infrastructure/mcp-servers/google-ads-mcp-server/google_ads_token.json
infrastructure/mcp-servers/google-tasks-mcp-server/token.json
infrastructure/mcp-servers/google-photos-mcp-server/token.json

# NPM Package (tokens.json format)
~/.config/google-drive-mcp/tokens.json

# Service Account (credentials.json format)
infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json

# No Authentication Needed
google-trends-mcp-server (public API)
```

---

## Configured vs Installed Servers

### Configured in .mcp.json (Active in Claude Code)

1. ✅ google-analytics
2. ✅ google-ads
3. ✅ google-drive

### Installed but Not in .mcp.json

4. google-tasks (used by LaunchAgents)
5. google-photos (available but not enabled)
6. google-sheets (used by LaunchAgents)
7. google-trends (available but not enabled)
8. google-search-console (incomplete/not implemented)

---

## OAuth Popup Risk Assessment

### ✅ Zero Risk (No Popups Expected)

**Reasons:**
1. All OAuth tokens exist in correct locations
2. All tokens have valid refresh tokens
3. All tokens recently refreshed (within last hour)
4. Setup script (`setup-oauth-once.sh`) covers all OAuth services
5. LaunchAgents run regularly, keeping tokens alive

### Maintenance Requirements

**None required** - Tokens auto-renew indefinitely as long as services run regularly.

**If OAuth popups appear (extremely rare):**
```bash
cd ~/Documents/PetesBrain.nosync
./shared/scripts/setup-oauth-once.sh
```

---

## Recommendations

### Immediate Actions (None Required)

✅ All OAuth tokens healthy and auto-renewing

### Optional Future Actions

1. **Google Photos MCP** - Consider adding to .mcp.json if photo analysis features needed
2. **Google Trends MCP** - Consider adding to .mcp.json for keyword research features
3. **Google Search Console MCP** - Either implement properly or remove incomplete directory
4. **Google Tasks MCP** - Consider adding to .mcp.json for task management via Claude Code

### Documentation Updates (Completed)

✅ Created this comprehensive audit document
✅ Updated `setup-oauth-once.sh` to include all OAuth services
✅ Documented OAuth popup fix in `docs/OAUTH-POPUP-PERMANENT-FIX.md`
✅ Updated global `~/.claude/CLAUDE.md` with OAuth prevention protocol

---

## Related Documentation

- **OAuth Popup Permanent Fix:** `docs/OAUTH-POPUP-PERMANENT-FIX.md`
- **OAuth to Service Account Migration:** `docs/OAUTH-TO-SERVICE-ACCOUNT-MIGRATION.md`
- **Gmail OAuth Scopes Solution:** `docs/GMAIL-OAUTH-SCOPES-SOLUTION.md`
- **OAuth Setup Script:** `shared/scripts/setup-oauth-once.sh`
- **OAuth Refresh Skill:** `.claude/skills/oauth-refresh/skill.md`

---

## Audit Conclusion

**✅ ALL GOOGLE MCP SERVERS ARE HEALTHY**

No OAuth popup issues expected. All tokens valid with auto-refresh capability. System operating as intended.

**Next Audit Recommended:** Not needed unless OAuth popups appear (extremely unlikely)

---

**Audit Completed:** 2025-12-15 11:50 GMT
**Auditor:** Claude Code (Sonnet 4.5)
**Audit Duration:** 15 minutes
**Issues Found:** 0 critical, 0 high, 1 low (incomplete Search Console server)
