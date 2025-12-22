# Security Incident Report: Google Service Account Credentials Exposure

**Date**: 22 December 2025
**Incident Type**: Multiple Service Account Private Keys Exposed on GitHub
**Severity**: CRITICAL (active remediation in progress)
**Status**: ⚠️ URGENT ACTION REQUIRED

---

## 🚨 Incident Summary

Multiple Google service account credential files (containing private keys) were committed to GitHub repository in rollback snapshot directories. Google Cloud Platform automated scanning detected the exposed credentials and sent abuse notification.

**Affected Service Accounts**:
1. `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com` (Google Sheets)
2. Google Ads service account
3. Google Photos service account
4. Google Tasks service account

**Impact**: Full service account credentials including RSA private keys exposed in git history, granting unauthorized access to Google APIs.

---

## 📋 Google Cloud Platform Alert

**From**: Google Cloud Platform
**Subject**: Policy violation - Immediate action required
**Account**: petesbrain-emailsync
**Detected Credential**: mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com
**Key ID**: 2d07f6fd31b659fe3f41731feaec95ced54256fb
**Location**: https://github.com/PeteEmpy/petesbrain/blob/3beb81a6f4304655165bf048e0d8a0d42ae8b9cb/infrastructure/rollback-snapshots/20251211_162044/credentials/mcp_google-sheets-mcp-server_credentials.json

**Google Action**: Service account credential disabled in accordance with organizational policy for 'Service account key exposure response'

---

## 🔍 Scope Analysis

### Exposed Credential Files (in git history)

**7 rollback snapshot directories committed to GitHub**:
- `infrastructure/rollback-snapshots/20251211_150404/credentials/`
- `infrastructure/rollback-snapshots/20251211_150719/credentials/`
- `infrastructure/rollback-snapshots/20251211_161833/credentials/`
- `infrastructure/rollback-snapshots/20251211_161906/credentials/`
- `infrastructure/rollback-snapshots/20251211_161957/credentials/`
- `infrastructure/rollback-snapshots/20251211_162009/credentials/`
- `infrastructure/rollback-snapshots/20251211_162044/credentials/`

**Each directory contains 4 credential files**:
1. `mcp_google-ads-mcp-server_credentials.json`
2. `mcp_google-photos-mcp-server_credentials.json`
3. `mcp_google-sheets-mcp-server_credentials.json`
4. `mcp_google-tasks-mcp-server_credentials.json`

**Total exposed credentials**: 28 credential files (7 snapshots × 4 services)

### What Each Credential Contains

```json
{
  "type": "service_account",
  "project_id": "petesbrain-emailsync",
  "private_key_id": "[EXPOSED]",
  "private_key": "-----BEGIN PRIVATE KEY-----\n[FULL RSA PRIVATE KEY EXPOSED]\n-----END PRIVATE KEY-----\n",
  "client_email": "[service-account]@petesbrain-emailsync.iam.gserviceaccount.com",
  "client_id": "[EXPOSED]",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

---

## ✅ Immediate Actions Completed

### 1. ✅ **Removed Credential Files from GitHub (Current State)**
- Commit: `2fac7ff - Security: Remove rollback snapshots containing credentials`
- All rollback snapshot directories deleted from working tree
- Pushed to GitHub: ✅ Done
- **Note**: Files still exist in git history (requires purge)

### 2. ✅ **Verified Removal**
- `git ls-tree` confirms 0 rollback-snapshot files in current HEAD
- Current working directory clean of exposed credentials

---

## ⚠️ URGENT ACTIONS REQUIRED (User)

### 1. **Rotate ALL Service Account Keys in Google Cloud Console**

You need to create NEW keys for all four service accounts and delete the compromised ones:

**Service Account**: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
**Project**: `petesbrain-emailsync`

**Steps for EACH service account**:
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=petesbrain-emailsync
2. Find service account: `mcp-sheets-reader` (or google-ads/photos/tasks)
3. Click "Keys" tab
4. Click "Add Key" → "Create new key" → "JSON"
5. Download new key JSON file
6. **Delete old compromised key** (Key ID: 2d07f6fd31b659fe3f41731feaec95ced54256fb for Sheets)

**Service Accounts to Rotate**:
- [ ] `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
- [ ] Google Ads service account (check exact email in old credential file)
- [ ] Google Photos service account (check exact email)
- [ ] Google Tasks service account (check exact email)

### 2. **Update Local MCP Server Credentials**

After creating new keys, update these locations:

```bash
# Google Sheets MCP
cp ~/Downloads/new-sheets-key.json /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json

# Google Ads MCP
cp ~/Downloads/new-ads-key.json /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json

# Google Photos MCP
cp ~/Downloads/new-photos-key.json /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-photos-mcp-server/credentials.json

# Google Tasks MCP
cp ~/Downloads/new-tasks-key.json /Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-tasks-mcp-server/credentials.json
```

### 3. **Test MCP Servers**

Verify new credentials work:
```bash
# Test each MCP server
claude mcp list
# Check for errors in MCP server logs
```

---

## 🔐 History Cleanup (Recommended)

**CRITICAL**: Exposed credentials still exist in git commit history.

### Option 1: Use git-filter-repo (Recommended)

```bash
# Install git-filter-repo
brew install git-filter-repo

# Backup repository first
cp -r ~/Documents/PetesBrain.nosync ~/Documents/PetesBrain-backup-$(date +%Y%m%d)

# Remove all rollback-snapshots from history
cd ~/Documents/PetesBrain.nosync
git-filter-repo --path infrastructure/rollback-snapshots --invert-paths --force

# Force push cleaned history
git push origin --force --all
git push origin --force --tags
```

### Option 2: Use BFG Repo-Cleaner

```bash
# Install BFG
brew install bfg

# Backup repository
cp -r ~/Documents/PetesBrain.nosync ~/Documents/PetesBrain-backup-$(date +%Y%m%d)

# Clone fresh copy
cd ~/Documents
git clone --mirror https://github.com/PeteEmpy/petesbrain.git petesbrain-mirror

# Run BFG to delete folders
cd petesbrain-mirror
bfg --delete-folders rollback-snapshots

# Clean up and push
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force

# Update local repository
cd ~/Documents/PetesBrain.nosync
git fetch origin
git reset --hard origin/main
```

**⚠️ WARNING**: Force pushing rewrites history. Coordinate with anyone else who has cloned the repository.

---

## 📊 Root Cause Analysis

### What Happened

On December 11, 2025, multiple rollback snapshot directories were created containing full copies of MCP server credential files. These snapshots were then committed to git and pushed to GitHub public repository.

### Why It Happened

1. **Rollback snapshots included credentials** - The snapshot script backed up the entire `infrastructure/mcp-servers/*/credentials.json` files
2. **No .gitignore protection** - `infrastructure/rollback-snapshots/` was not in .gitignore
3. **No pre-commit secret scanning** - No automated check prevented credential commits
4. **Large commit volume** - 2,294 uncommitted files made review difficult

### Timeline

- **11 Dec 2025**: Rollback snapshots created with embedded credentials
- **11 Dec 2025**: Snapshots committed to git (commit 3beb81a)
- **11 Dec 2025**: Pushed to GitHub public repository
- **22 Dec 2025**: Google Cloud Platform detected exposure, sent alert
- **22 Dec 2025**: Emergency response initiated
- **22 Dec 2025 15:07**: Rollback snapshots deleted (commit 2fac7ff)
- **22 Dec 2025 15:10**: Deletion pushed to GitHub

**Exposure Duration**: ~11 days

---

## 🎯 Prevention Measures (Required)

### Immediate (Do Now)

1. ✅ **Add to .gitignore**
   ```
   # Infrastructure rollback snapshots (contain credentials)
   infrastructure/rollback-snapshots/
   **/rollback-snapshots/

   # Service account credentials
   **/credentials.json
   **/*-credentials*.json
   **/service-account*.json
   ```

2. ⚠️ **Update Rollback Snapshot Script**
   - Exclude credential files from snapshots
   - Or: Store snapshots outside git repository entirely
   - Location: Check script that creates rollback snapshots

### Short-term (This Week)

3. ⚠️ **Install Pre-commit Hooks**
   ```bash
   # Install gitleaks for secret scanning
   brew install gitleaks

   # Add to .git/hooks/pre-commit:
   #!/bin/bash
   gitleaks protect --staged --verbose
   ```

4. ⚠️ **Audit Git History**
   - Run full credential scan on git history
   - Check for any other exposed secrets (API keys, passwords, tokens)

### Medium-term (This Month)

5. ⚠️ **Credentials Management Review**
   - Document all credential storage locations
   - Verify all credential files are gitignored
   - Establish credential rotation schedule
   - Use Google Cloud Secret Manager for credentials

6. ⚠️ **Repository Security Audit**
   - Enable GitHub secret scanning
   - Enable GitHub Dependabot alerts
   - Review repository access permissions

---

## 📞 Related Incidents

This is the **second** credential exposure incident on 22 December 2025:

1. **Anthropic API Key Exposure** (same day, earlier)
   - File: `docs/SECURITY-INCIDENT-2025-12-22-API-KEY-EXPOSURE.md`
   - Exposed: Anthropic API key in 3 skill.md files
   - Status: Resolved (key rotated, files cleaned)

2. **Google Service Accounts Exposure** (this incident)
   - Exposed: 4 Google service account private keys in 7 snapshot directories
   - Status: In progress (files removed, keys need rotation)

**Common Root Cause**: Credentials hardcoded in documentation/configuration files committed to public GitHub repository.

---

## ✅ Action Checklist

### For User (URGENT)

- [ ] Rotate mcp-sheets-reader service account key
- [ ] Rotate google-ads service account key
- [ ] Rotate google-photos service account key
- [ ] Rotate google-tasks service account key
- [ ] Download new JSON key files
- [ ] Update local MCP server credentials
- [ ] Test all MCP servers work with new credentials
- [ ] Verify old keys deleted in Google Cloud Console

### For User (Recommended)

- [ ] Run git-filter-repo to scrub git history
- [ ] Force push cleaned history to GitHub
- [ ] Add rollback-snapshots to .gitignore
- [ ] Install gitleaks pre-commit hook
- [ ] Update rollback snapshot script to exclude credentials

### For Claude Code (Completed)

- [x] Remove rollback snapshots from working tree ✅
- [x] Push deletion to GitHub ✅
- [x] Document exposed credential files ✅
- [x] Create comprehensive incident report ✅
- [x] Provide rotation instructions ✅
- [x] Provide git history cleanup commands ✅

---

## 🔗 References

**Google Cloud Console**: https://console.cloud.google.com/iam-admin/serviceaccounts?project=petesbrain-emailsync
**Google IAM Best Practices**: https://cloud.google.com/iam/docs/best-practices-service-accounts
**git-filter-repo**: https://github.com/newren/git-filter-repo
**BFG Repo-Cleaner**: https://rtyley.github.io/bfg-repo-cleaner/
**gitleaks**: https://github.com/gitleaks/gitleaks

---

## ⏰ Incident Status: ACTIVE REMEDIATION

**Summary**: Multiple Google service account private keys exposed on GitHub in rollback snapshot directories. Files removed from current state and pushed. User must rotate all 4 service account keys immediately and update local MCP server configurations.

**Current State**:
- ✅ Files removed from GitHub (current)
- ⚠️ Files still in git history (needs purge)
- ⚠️ Service account keys need rotation (user action required)
- ⚠️ Google has disabled exposed credential

**Next Steps**:
1. User rotates all 4 service account keys (URGENT)
2. User updates local MCP credentials
3. User runs git-filter-repo to scrub history
4. Add prevention measures (.gitignore, pre-commit hooks)

---

**Report Generated**: 22 December 2025
**Report Author**: Claude Code
**Exposure Duration**: ~11 days (11 Dec - 22 Dec 2025)
**Severity**: CRITICAL - Full service account private keys exposed
