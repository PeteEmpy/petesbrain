# Backup Safety System Documentation

**Created**: December 19, 2025
**Status**: ✅ ACTIVE
**Purpose**: Prevent data loss through multi-layer backup verification

---

## Overview

This system was implemented after the December 10-19 data loss incident where 9 days of task changes were lost due to backup system failure (29-byte corrupt backup files).

**Key Principle**: "Never trust backups - always verify them"

---

## Architecture

### Layer 1: Verified Backup Creation

**Script**: `shared/backup-verification/safe-backup.sh`
**Frequency**: Every 6 hours
**LaunchAgent**: `com.petesbrain.safe-backup`

**Process**:
1. Creates tar.gz backup of all task files
2. Immediately verifies backup integrity (calls verification script)
3. If verification FAILS: Aborts and alerts
4. If verification PASSES: Copies to multiple locations
5. Cleans up old backups

**Backup Locations**:
- **Local**: `/Users/administrator/Documents/PetesBrain.nosync/_backups/tasks/`
  - Retention: 30 days
  - Fast access for emergency restoration

- **iCloud Drive**: `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/`
  - Retention: 7 days
  - Off-machine redundancy

- **Google Drive**: Via `agents/tasks-backup/tasks-backup.py` (existing system)
  - Retention: Unlimited
  - Long-term archive

### Layer 2: Backup Verification

**Script**: `shared/backup-verification/verify-backup.py`
**Called by**: safe-backup.sh (after every backup)

**Checks Performed**:
1. ✅ File exists and is readable
2. ✅ File size >= 50 KB (not corrupt/truncated)
3. ✅ Tarball structure is valid
4. ✅ Contains >= 10 client task files
5. ✅ All JSON files are valid (parseable)
6. ✅ Total task count is reasonable (not dropped >20% from baseline)

**Outputs**:
- Exit code 0 = PASS, Exit code 1 = FAIL
- Detailed log to `~/.petesbrain-backup-verification.log`
- Alerts written to `~/.petesbrain-backup-alerts.log`
- Updates baseline: `shared/backup-verification/backup-baseline.json`

### Layer 3: Weekly Restoration Testing

**Script**: `shared/backup-verification/weekly-backup-audit.py`
**Frequency**: Every Monday at 9 AM
**LaunchAgent**: `com.petesbrain.weekly-backup-audit`

**Process**:
1. Finds latest backup
2. Counts production tasks (live system)
3. Counts backup tasks (in backup file)
4. Compares counts (alerts if >20% difference)
5. **Actually restores backup to temp directory**
6. Verifies all restored files are valid JSON

**Why This Matters**: Verification can pass but restoration can still fail (permissions, path issues, etc.). This weekly test ensures backups are actually recoverable.

---

## What Changed From Before

### Old System (BROKEN)
- ❌ LaunchAgent bash script creating 29-byte corrupt files
- ❌ No verification after backup creation
- ❌ No alerting on failure
- ❌ Single backup location (iCloud)
- ❌ No restoration testing

### New System (CURRENT)
- ✅ Python-based verified backup with immediate validation
- ✅ Automatic verification after every backup
- ✅ Alerts on any failure (logged + file)
- ✅ Three backup locations (local, iCloud, Google Drive)
- ✅ Weekly restoration testing

---

## Monitoring & Alerts

### Log Files

| Log File | Purpose | Check Frequency |
|----------|---------|----------------|
| `~/.petesbrain-safe-backup.log` | Backup execution log | After issues |
| `~/.petesbrain-safe-backup-error.log` | Backup errors | Daily |
| `~/.petesbrain-backup-verification.log` | Verification details | After issues |
| `~/.petesbrain-backup-alerts.log` | **CRITICAL ALERTS** | **Daily** |
| `~/.petesbrain-weekly-audit.log` | Weekly audit results | Every Monday |

### How to Check System Health

**Quick Health Check**:
```bash
# Check if agents are running
launchctl list | grep petesbrain | grep -E "(safe-backup|weekly-audit)"

# Check recent backup
ls -lh ~/Documents/PetesBrain.nosync/_backups/tasks/ | tail -5

# Check for alerts
tail -20 ~/.petesbrain-backup-alerts.log
```

**Weekly Health Check** (Every Monday):
```bash
# Review weekly audit results
tail -50 ~/.petesbrain-weekly-audit.log

# Look for "✅ WEEKLY AUDIT PASSED"
# If not found, investigate immediately
```

### Red Flags

⚠️ **IMMEDIATE ACTION REQUIRED** if you see:
- "Backup file is suspiciously small" (corrupt backup)
- "Too few client task files" (missing data)
- "Task count dropped X% from baseline" (data loss)
- "Restoration test failed" (backup not recoverable)
- No recent backup in `_backups/tasks/` (agent not running)

---

## Manual Operations

### Create Backup Manually

```bash
cd ~/Documents/PetesBrain.nosync
./shared/backup-verification/safe-backup.sh
```

### Verify Existing Backup

```bash
python3 ~/Documents/PetesBrain.nosync/shared/backup-verification/verify-backup.py \
    /path/to/backup-file.tar.gz
```

### Run Weekly Audit Manually

```bash
python3 ~/Documents/PetesBrain.nosync/shared/backup-verification/weekly-backup-audit.py
```

### Restore from Backup

```bash
cd ~/Documents/PetesBrain.nosync
tar -xzf _backups/tasks/tasks-backup-YYYYMMDD-HHMMSS.tar.gz

# This will extract to clients/*/tasks.json (overwrites current)
# BE CAREFUL - always check what you're restoring first
```

### Check Baseline

```bash
cat ~/Documents/PetesBrain.nosync/shared/backup-verification/backup-baseline.json
```

---

## Recovery Procedures

### If Backup Verification Fails

1. **Check the alert log**:
   ```bash
   tail -50 ~/.petesbrain-backup-alerts.log
   ```

2. **Identify the issue**:
   - File too small? = Incomplete backup creation
   - Invalid JSON? = Data corruption
   - Missing files? = tar command failed

3. **Trigger manual backup**:
   ```bash
   ./shared/backup-verification/safe-backup.sh
   ```

4. **If still failing**: Check disk space, permissions, paths

### If Data Loss Detected

1. **Find latest good backup**:
   ```bash
   ls -lt ~/Documents/PetesBrain.nosync/_backups/tasks/
   ```

2. **Verify backup before restoring**:
   ```bash
   python3 shared/backup-verification/verify-backup.py \
       _backups/tasks/tasks-backup-20XX-XX-XX-XXXXXX.tar.gz
   ```

3. **Extract to temp location first**:
   ```bash
   mkdir /tmp/backup-restore-test
   tar -xzf _backups/tasks/tasks-backup-20XX-XX-XX-XXXXXX.tar.gz -C /tmp/backup-restore-test
   ```

4. **Compare against production**:
   ```bash
   diff -r /tmp/backup-restore-test/clients clients
   ```

5. **Restore carefully** (client by client):
   ```bash
   cp /tmp/backup-restore-test/clients/client-name/tasks.json \
      clients/client-name/tasks.json
   ```

---

## Maintenance

### Update Verification Thresholds

Edit `shared/backup-verification/verify-backup.py`:

```python
MIN_BACKUP_SIZE_KB = 50      # Minimum acceptable size
MIN_CLIENT_FILES = 10        # Minimum number of task files
TASK_COUNT_DROP_THRESHOLD = 0.20  # Alert if >20% drop
```

### Add New Backup Location

Edit `shared/backup-verification/safe-backup.sh`:

```bash
# Add to Configuration section
NEW_BACKUP_DIR="/path/to/new/location"

# Add to backup process
log "Copying to new backup location..."
cp "${TEMP_DIR}/${BACKUP_NAME}" "$NEW_BACKUP_DIR/"
```

### Change Backup Frequency

Edit `~/Library/LaunchAgents/com.petesbrain.safe-backup.plist`:

```xml
<key>StartInterval</key>
<integer>21600</integer>  <!-- 6 hours = 21600 seconds -->
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.safe-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.safe-backup.plist
```

---

## Testing

### Test Backup Creation

```bash
./shared/backup-verification/safe-backup.sh
# Should output: "✅ Safe backup completed successfully"
```

### Test Verification

```bash
# Test with good backup
python3 shared/backup-verification/verify-backup.py \
    _backups/tasks/tasks-backup-20251219-144528.tar.gz
# Should output: "✅ Backup verification PASSED"

# Test with corrupt backup (create tiny file)
echo "corrupt" > /tmp/test-corrupt.tar.gz
python3 shared/backup-verification/verify-backup.py /tmp/test-corrupt.tar.gz
# Should output: "❌ Backup verification FAILED"
```

### Test Weekly Audit

```bash
python3 shared/backup-verification/weekly-backup-audit.py
# Should output: "✅ WEEKLY AUDIT PASSED"
```

---

## Troubleshooting

### "Backup file does not exist"
- Check disk space: `df -h`
- Check permissions: `ls -la shared/backup-verification/`
- Check if agent is running: `launchctl list | grep safe-backup`

### "Could not parse X.json"
- Check if file is actually JSON: `head -20 clients/client-name/tasks.json`
- Check file encoding: `file clients/client-name/tasks.json`
- Try manual verification: `python3 -m json.tool < file.json`

### "Task count dropped significantly"
- Check if tasks were legitimately completed (check tasks-completed.md)
- Check baseline file: `cat shared/backup-verification/backup-baseline.json`
- If false positive, update baseline manually

### Weekly audit not running
- Check if agent is loaded: `launchctl list | grep weekly-audit`
- Check error log: `tail ~/.petesbrain-weekly-audit-error.log`
- Test manually: `python3 shared/backup-verification/weekly-backup-audit.py`

---

## Future Enhancements

Potential improvements (not yet implemented):

1. **Email Alerts**: Send email when backup fails (requires SMTP setup)
2. **Slack/Teams Notifications**: Real-time alerts to messaging platform
3. **Dashboard**: Web interface showing backup health status
4. **Automated Recovery**: If data loss detected, prompt for automated restore
5. **Backup Encryption**: Encrypt backups before uploading to cloud

---

## Related Documentation

- `/docs/INCIDENTS.md` - Historical incident records (including Dec 10-19 data loss)
- `/docs/BACKUP-SYSTEM.md` - Original backup system documentation (pre-safety system)
- `agents/tasks-backup/README.md` - Google Drive backup agent documentation

---

**Status**: ✅ System operational as of December 19, 2025
**Next Review**: January 19, 2026 (30 days)
