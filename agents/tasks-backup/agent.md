# Tasks Backup Agent

**Purpose**: Automated backup of all tasks.json files to prevent catastrophic data loss

**Schedule**: Every 3 hours (8 times per day)

**What It Does**:
1. Finds all `tasks.json` files across clients and roksys
2. Creates timestamped compressed archive (tarball)
3. Uploads to Google Drive backup folder
4. Maintains local fallback copies
5. Cleans up backups older than 30 days

**Backup Strategy**:
- **Cloud Storage**: ✅ Google Drive `PetesBrain-Backups/Tasks/` (ACTIVE)
- **Local Fallback**: `/Users/administrator/Documents/PetesBrain/_backups/tasks/` (always saved)
- **Retention**: 30 days local (240 backups maximum)
- **Format**: `tasks-backup-YYYY-MM-DD-HHMM.tar.gz`
- **Redundancy**: Every backup is saved to BOTH cloud and local

**Why This Matters**:
After the incident where tasks were accidentally deleted, this system provides:
- Point-in-time recovery (every 3 hours)
- 30 days of backup history
- Cloud redundancy
- Automated, hands-free protection

**Recovery**:
Use the `.claude/skills/restore-tasks/` skill to restore from any backup point.

**Monitoring**:
Check logs: `~/.petesbrain-tasks-backup.log`

**Related**:
- **Manual Backup Skill**: `.claude/skills/backup-tasks/`
- **Restore Skill**: `.claude/skills/restore-tasks/`
- **Documentation**: `docs/BACKUP-SYSTEM.md`
