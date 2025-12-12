# Credential Backup System - Complete Reference

## Overview

The rollback manager now includes **comprehensive credential backup** as part of every snapshot. This solves the critical gap from the December 10 rollback, when missing credentials caused hours of troubleshooting.

**All credentials are automatically backed up and restored with every snapshot**, including:
- MCP server service account credentials
- Google Ads OAuth tokens and configuration
- Google Drive OAuth keys
- All API keys referenced in `.mcp.json`

---

## What Gets Backed Up

### 1. MCP Server Credentials

Each MCP server directory that contains `credentials.json` or `gcp-oauth.keys.json`:

```
infrastructure/mcp-servers/*/credentials.json         (Google Sheets, Tasks, Photos, Ads)
infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json
```

**Current Discovery**: 5 MCP server credential files backed up

**Example**:
- `infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json` (2.4 KB service account)
- `infrastructure/mcp-servers/google-ads-mcp-server/credentials.json` (OAuth token)
- `infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json` (GCP OAuth)

### 2. Google Ads Configuration

```
~/.google-ads/google-ads.yaml
```

**Contains**: Google Ads API settings and credentials
**Size**: ~117 bytes
**Backed Up**: Yes, every snapshot

### 3. OAuth Credentials Referenced in .mcp.json

The rollback manager **parses `.mcp.json`** and discovers all OAuth credential paths referenced in environment variables:

```json
{
  "GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH": "/Users/administrator/Downloads/client_secret_512285153243-xxx.json",
  "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "/path/to/gcp-oauth.keys.json"
}
```

**Current Discovery**:
- `/Users/administrator/Downloads/client_secret_512285153243-xxx.json` (Google Analytics OAuth)
- `/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`

---

## How Credential Backup Works

### Discovery Process

When you create a snapshot, the rollback manager:

1. **Discovers MCP credentials** - Scans `infrastructure/mcp-servers/` for `credentials.json` and `gcp-oauth.keys.json` files
2. **Discovers system credentials** - Checks `~/.google-ads/google-ads.yaml`
3. **Parses .mcp.json** - Reads all `env` sections to find OAuth credential paths
4. **Discovers ~/.config/ credentials** - Checks for any additional OAuth credentials
5. **Validates file existence** - Only backs up files that actually exist

### Backup Process

For each discovered credential:

1. **Calculate hash** - SHA256 checksum for integrity verification
2. **Copy credential** - Backed up to `infrastructure/rollback-snapshots/{timestamp}/credentials/`
3. **Organize structure** - Files stored with descriptive names (e.g., `mcp_google-sheets-mcp-server_credentials.json`)
4. **Record metadata** - Stored in manifest with:
   - Original path
   - Backup path
   - SHA256 hash
   - File size

---

## Credential Manifest File

Each snapshot includes **CREDENTIAL-MANIFEST.md** showing exactly what was backed up:

```markdown
# Credential Files Backed Up

Snapshot: 20251211_150404
Created: 2025-12-11T15:04:04.904265

## Backed Up Credentials

- **mcp/google-sheets-mcp-server/credentials.json**
  - Original: `/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json`
  - Size: 2388 bytes
  - Hash: `cd37d3a859ec18d7...`

- **~/.google-ads/google-ads.yaml**
  - Original: `/Users/administrator/.google-ads/google-ads.yaml`
  - Size: 117 bytes
  - Hash: `45b89784c6ff2230...`
```

**Purpose**: Transparency and verification that credentials were captured

---

## Restore Process

### Dry-Run: Preview What Will Be Restored

```bash
python3 shared/rollback_manager.py restore 20251211_150404
```

**Output includes credentials section**:
```
🔐 CREDENTIALS:
- Unchanged: mcp/google-sheets-mcp-server/credentials.json
- Unchanged: mcp/google-ads-mcp-server/credentials.json
- Unchanged: ~/.google-ads/google-ads.yaml
✓ Would restore (modified): oauth/client_secret_512285153243-xxx.json
```

**Shows**:
- Which credentials exist in both current state and snapshot
- Which credentials would be modified
- Which credentials are missing (if any)

### Actual Restore: Credentials Restored Automatically

```bash
python3 shared/rollback_manager.py restore 20251211_150404 --force
```

**Restore process**:

1. **Creates auto-backup** of current state (including current credentials)
2. **Restores each credential**:
   - Verifies backup file exists
   - Creates parent directory if needed
   - Copies credential back to original location
   - Logs success or failure
3. **Reports results**:
   ```
   ✓ Restored credential: mcp/google-sheets-mcp-server/credentials.json
   ✓ Restored credential: mcp/google-ads-mcp-server/credentials.json
   ✓ Restored credential: ~/.google-ads/google-ads.yaml
   ```

---

## Safety Guarantees

### 1. No Credentials Lost

**Before any restore**:
- Current credentials are backed up (in a new snapshot marked "auto-backup")
- You can restore from this auto-backup if needed
- You have a complete chain: Original Snapshot → Auto-Backup → New State

### 2. Integrity Verification

**Each credential backed up with**:
- SHA256 hash for change detection
- Size recorded for verification
- Complete audit trail in manifest

**Before restore**:
- Dry-run shows exactly which credentials would change
- Hash comparison shows if credential has been modified

### 3. Isolated Restore

**Credentials restored separately from**:
- Plist files (agent configurations)
- Config files (.mcp.json, secrets.py)
- System state (git, venvs)

This means you can:
- Restore credentials without restoring agents
- See credential changes independently from other changes

---

## Solving the Dec 10 Problem

**What happened on Dec 10**: After rollback, credentials were missing/hard to find

**Why it won't happen again**:

1. **Automatic Discovery**: Credentials are found automatically, not manually
2. **Complete Backup**: Every credential is backed up (not cherry-picked)
3. **Manifest Transparency**: CREDENTIAL-MANIFEST.md shows exactly what's backed up
4. **Dry-Run Preview**: You see all credentials before actually restoring
5. **Verification**: Hashes ensure credentials are restored correctly
6. **Audit Trail**: Complete log of which credentials were in each snapshot

**Scenario**: System breaks after migration
```bash
# See what credentials would be restored
python3 shared/rollback_manager.py restore 20251211_150404

# Output shows all 9 credentials ready to restore
# Then restore everything
python3 shared/rollback_manager.py restore 20251211_150404 --force

# All credentials restored, system is operational
```

---

## Credential Locations Discovered

### Automatically Discovered

✅ `infrastructure/mcp-servers/*/credentials.json` - All service accounts
✅ `infrastructure/mcp-servers/*/gcp-oauth.keys.json` - All OAuth keys
✅ `~/.google-ads/google-ads.yaml` - Google Ads config
✅ `~/.config/google-drive-mcp/credentials.json` - Drive OAuth (if exists)
✅ Paths referenced in `.mcp.json` environment variables

### Currently Backed Up (in your system)

1. `infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json` - Service account
2. `infrastructure/mcp-servers/google-photos-mcp-server/credentials.json` - Service account
3. `infrastructure/mcp-servers/google-tasks-mcp-server/credentials.json` - Service account
4. `infrastructure/mcp-servers/google-ads-mcp-server/credentials.json` - OAuth token
5. `infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json` - GCP OAuth
6. `~/.google-ads/google-ads.yaml` - Google Ads settings
7. `/Users/administrator/Downloads/client_secret_512285153243-xxx.json` - Google Analytics OAuth
8-9. Additional OAuth references from `.mcp.json`

---

## Storage Locations

### Snapshot Credential Directory

```
infrastructure/rollback-snapshots/{TIMESTAMP}/
├── manifest.json                                  (Main metadata)
├── CREDENTIAL-MANIFEST.md                        (Credential list - human readable)
├── credentials/
│   ├── mcp_google-sheets-mcp-server_credentials.json
│   ├── mcp_google-ads-mcp-server_credentials.json
│   ├── mcp_google-drive-mcp-server_gcp-oauth.keys.json
│   ├── home_.google-ads_google-ads.yaml
│   └── oauth_client_secret_512285153243-xxx.json
├── plist/                                        (Agent configs)
├── config/                                       (.mcp.json, secrets.py, paths.py)
└── venv-state.json                              (Venv metadata)
```

### Manifest Structure

```json
{
  "credential_files": [
    {
      "name": "mcp/google-sheets-mcp-server/credentials.json",
      "original": "/Users/administrator/Documents/PetesBrain.nosync/...",
      "backup": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/rollback-snapshots/20251211_150404/credentials/...",
      "hash": "cd37d3a859ec18d7...",
      "size_bytes": 2388
    },
    ...
  ]
}
```

---

## Usage Examples

### Example 1: Create Snapshot with Credentials

```bash
python3 shared/rollback_manager.py create "Before venv repairs" "pre-venv-fix"
```

**Output**:
```
🔐 Backing up credentials...
   ✅ Backed up 9 credential files

✅ Snapshot created: 20251211_150404
   Description: Before venv repairs
   Category: pre-venv-fix
   Location: /Users/administrator/Documents/PetesBrain.nosync/infrastructure/rollback-snapshots/20251211_150404
   Files backed up: 83 (71 plist + 3 config + 9 credentials)
```

### Example 2: List Snapshots with Credential Count

```bash
python3 shared/rollback_manager.py list
```

**Output**:
```
1. [20251211_150404]
   Description: Before venv repairs
   Category: pre-venv-fix
   Created: 5m ago
   Files: 71 plist, 3 config, 🔐 9 credentials    ← Shows credential count
```

### Example 3: Dry-Run Restore to Preview Credentials

```bash
python3 shared/rollback_manager.py restore 20251211_150404
```

**Output includes**:
```
🔐 CREDENTIALS:
- Unchanged: mcp/google-sheets-mcp-server/credentials.json
✓ Would restore (modified): oauth/client_secret_512285153243-xxx.json
```

### Example 4: Actually Restore with Credentials

```bash
python3 shared/rollback_manager.py restore 20251211_150404 --force
```

**Output**:
```
🔐 Restoring credentials...
✓ Restored credential: mcp/google-sheets-mcp-server/credentials.json
✓ Restored credential: mcp/google-ads-mcp-server/credentials.json
✓ Restored credential: ~/.google-ads/google-ads.yaml
✓ Restored credential: oauth/client_secret_512285153243-xxx.json

Restored 74 files
Auto-backup created: 20251211_150417
```

---

## FAQ

### Q: What if a credential file is added after the snapshot?

**A**: New credential files won't be in old snapshots, but the next snapshot will capture them. The system auto-discovers all credentials at snapshot time.

### Q: Can I add manual credential locations to back up?

**A**: Currently, the system discovers credentials automatically. To back up additional credentials:
1. Store them in one of the known locations (e.g., `infrastructure/mcp-servers/*/credentials.json`)
2. Reference them in `.mcp.json` environment variables
3. Or place in `~/.config/` subdirectories

### Q: Are credentials ever logged or printed?

**A**:
- ❌ Credential contents are never logged or printed
- ❌ Credential paths are never echoed to console (only names)
- ✅ Hashes are printed (for verification only, not the actual credentials)
- ✅ File sizes are printed (for transparency)

### Q: What if a credential file is moved or deleted?

**A**: The restore process handles missing files gracefully:
- If backup is missing → Warns and skips it
- If original location is missing → Creates parent directory and restores it
- Detailed logging shows what succeeded and what failed

### Q: Can credentials be restored separately from other files?

**A**: Not currently. Restore is all-or-nothing for the snapshot. However:
- Dry-run lets you see exactly what would change
- You can restore to a specific point in time
- Auto-backup captures current credentials before any restore

---

## Technical Details

### Discovery Algorithm

```python
credentials = {}

# 1. Find MCP server credentials
for server_dir in infrastructure/mcp-servers/:
    if credentials.json exists: back it up
    if gcp-oauth.keys.json exists: back it up

# 2. Find system credentials
if ~/.google-ads/google-ads.yaml exists: back it up

# 3. Parse .mcp.json for OAuth paths
for env_var in .mcp.json['mcpServers'][*]['env']:
    if env_var contains 'OAUTH' and path exists: back it up

# 4. Find config-stored credentials
if ~/.config/google-drive-mcp/credentials.json exists: back it up
```

### Hash Verification

All credentials backed up with SHA256:
- Enables change detection (see if credential modified since snapshot)
- Provides integrity verification (detect corruption)
- Allows validation that restore succeeded correctly

### File Organization

Credentials stored with readable names:
```
mcp/google-sheets-mcp-server/credentials.json  →  mcp_google-sheets-mcp-server_credentials.json
~/.google-ads/google-ads.yaml                  →  home_.google-ads_google-ads.yaml
oauth/client_secret_xxx.json                   →  oauth_client_secret_xxx.json
```

This organization makes them easy to locate in snapshots.

---

## Troubleshooting

### "No credentials found to backup"

**Cause**: No credential files discovered during snapshot
**Solution**:
- Verify credential files exist in expected locations
- Check that `infrastructure/mcp-servers/*/credentials.json` files exist
- Verify `~/.google-ads/google-ads.yaml` exists
- Check `.mcp.json` OAuth references are correct

### "Failed to restore credential X"

**Causes**:
1. Parent directory can't be created (permissions issue)
2. Source backup file is corrupted
3. File already exists and can't be overwritten

**Solution**:
- Check file permissions: `ls -la {parent_dir}`
- Check disk space: `df -h`
- Verify backup integrity in snapshot
- Check error message for specific reason

### "Credential not in backup but exists in current system"

**This is normal** if:
- Credentials added after the snapshot was created
- Using a newer snapshot that includes the credential
- The credential is from a different configuration

**Solution**: Create a new snapshot before making changes to capture current credentials

---

## Best Practices

1. **Create snapshots before major changes**
   ```bash
   python3 shared/rollback_manager.py create "Before venv repairs" "pre-venv-fix"
   ```

2. **Always dry-run before restoring**
   ```bash
   python3 shared/rollback_manager.py restore 20251211_150404  # Preview
   python3 shared/rollback_manager.py restore 20251211_150404 --force  # Execute
   ```

3. **Check CREDENTIAL-MANIFEST.md before restoring**
   - Verify all expected credentials are backed up
   - Check that credentials haven't been manually modified since snapshot
   - Review hash values for integrity

4. **Keep multiple snapshots**
   - Before Phase 4: `python3 ... create "Pre-Phase-4" "pre-phase-4"`
   - Before venv fixes: `python3 ... create "Pre-venv-repair" "pre-venv-fix"`
   - Before any major system change: `python3 ... create "Before [change]" "[category]"`

5. **Test restore process**
   - Use dry-run regularly to practice
   - Verify credentials would be restored correctly
   - Know the restore command before you need it

---

## Security Notes

### Credential Safety

- ✅ Credentials backed up with same permissions as originals
- ✅ Stored in project repository (git-controlled)
- ✅ Never printed to logs or console
- ✅ Only visible to users with filesystem access
- ⚠️ Stored in plaintext (no encryption) - repository access = credential access

### Who Has Access

**Credentials accessible to anyone who can**:
- Read `infrastructure/rollback-snapshots/*/credentials/` directory
- Read git history (if snapshots are committed)

**Recommendations**:
- Keep `.gitignore` updated to exclude credentials if sensitive
- Restrict filesystem access to PetesBrain directory
- Use appropriate permissions on `~/Library/LaunchAgents/`

---

## Integration with Rollback System

Credential backup is **part of every rollback snapshot**. It integrates with:

1. **Snapshot Creation** - Credentials discovered and backed up automatically
2. **Snapshot Listing** - Shows credential count in snapshot list
3. **Dry-Run Restore** - Credentials included in preview
4. **Actual Restore** - Credentials restored with all other files
5. **Auto-Backup** - Credentials backed up before any restore

---

*Last updated: December 11, 2025*
*System version: Rollback Manager with Credential Backup (v2.0)*
