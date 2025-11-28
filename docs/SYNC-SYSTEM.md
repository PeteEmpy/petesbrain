# PetesBrain Sync System

**Created:** November 7, 2025  
**Status:** ✅ Ready for Use

---

## Overview

Complete sync system for keeping PetesBrain synchronized between your desktop and laptop machines. Supports multiple sync methods and automatic syncing.

## Sync Methods

### 1. Git-Based Sync (Recommended) ⭐

**Best for:** Regular syncing, version control, conflict resolution

**Requirements:**
- Git repository (GitHub, GitLab, or private Git server)
- Git installed on both machines

**Setup:**
1. Create a Git repository (GitHub, GitLab, etc.)
2. On desktop: `git remote add origin <your-repo-url>`
3. On desktop: `git push -u origin main`
4. On laptop: Run installation script with `git` method

**Usage:**
```bash
sync-petesbrain pull   # Get latest from remote
sync-petesbrain push   # Send local changes to remote
sync-petesbrain both   # Pull then push
```

### 2. iCloud Drive Sync

**Best for:** Simple setup, no Git required, automatic cloud backup

**Requirements:**
- iCloud Drive enabled on both machines
- Existing backup system (already configured)

**Setup:**
1. Ensure backups are running on desktop (`backup-petesbrain`)
2. On laptop: Run installation script with `icloud` method
3. iCloud Drive will sync backups automatically

**Usage:**
```bash
sync-petesbrain pull   # Extract latest backup from iCloud
sync-petesbrain push   # Create new backup in iCloud
```

### 3. rsync Direct Sync

**Best for:** Fast local network sync, no cloud required

**Requirements:**
- Both machines on same network
- SSH access between machines

**Setup:**
1. Enable SSH on desktop
2. On laptop: Run installation script with `rsync` method
3. Provide desktop hostname/IP when prompted

**Usage:**
```bash
sync-petesbrain pull   # Sync from desktop to laptop
```

---

## Installation on Laptop

### Quick Install

See **[Laptop Installation Guide](LAPTOP-INSTALLATION-GUIDE.md)** for detailed step-by-step instructions.

**Quick version:**

### Manual Installation

1. **Copy PetesBrain to laptop:**
   ```bash
   # Option A: From iCloud backup
   cd ~/Documents
   tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-LATEST.tar.gz
   
   # Option B: From Git
   git clone <your-repo-url> ~/Documents/PetesBrain
   
   # Option C: Via rsync
   rsync -avz administrator@desktop:/Users/administrator/Documents/PetesBrain ~/Documents/
   ```

2. **Install sync script:**
   ```bash
   cd ~/Documents/PetesBrain
   chmod +x shared/scripts/sync-petesbrain.sh
   ```

3. **Set up alias:**
   ```bash
   echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
   source ~/.zshrc
   ```

---

## Automatic Syncing

### Set Up Automatic Sync (LaunchAgent)

**On Desktop:**
```bash
cd ~/Documents/PetesBrain/shared/scripts
./setup-auto-sync.sh desktop
```

**On Laptop:**
```bash
cd ~/Documents/PetesBrain/shared/scripts
./setup-auto-sync.sh laptop
```

This creates a LaunchAgent that syncs:
- **Desktop**: Every 2 hours (pushes changes)
- **Laptop**: Every hour (pulls changes)

### Manual Sync Schedule

**Check sync status:**
```bash
launchctl list | grep petesbrain.sync
```

**View sync logs:**
```bash
tail -f ~/.petesbrain-sync.log
```

**Disable automatic sync:**
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.sync.plist
```

**Enable automatic sync:**
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.sync.plist
```

---

## Daily Workflow

### On Desktop (Primary Machine)

1. **Work normally** - Make changes, add files, etc.
2. **Before closing:** Run `sync-petesbrain push` to sync changes
3. **Automatic:** LaunchAgent pushes every 2 hours

### On Laptop (Secondary Machine)

1. **Before starting work:** Run `sync-petesbrain pull` to get latest
2. **Work normally** - Make changes as needed
3. **Before closing:** Run `sync-petesbrain push` to sync changes back
4. **Automatic:** LaunchAgent pulls every hour

---

## Conflict Resolution

### Git Conflicts

If you get merge conflicts:

```bash
# View conflicts
git status

# Resolve conflicts manually
# Edit conflicted files, remove conflict markers

# Complete merge
git add .
git commit -m "Resolved sync conflicts"
git push
```

### File Conflicts (iCloud/rsync)

The sync script uses timestamps. Newer files win. If you need to keep both:

1. Rename one version before syncing
2. Sync
3. Merge manually if needed

---

## Troubleshooting

### Sync Fails - "No remote configured"

**Solution:** Set up Git remote:
```bash
cd ~/Documents/PetesBrain
git remote add origin <your-repo-url>
git push -u origin main
```

### Sync Fails - "iCloud Drive not found"

**Solution:** 
1. Enable iCloud Drive: System Settings → Apple ID → iCloud → iCloud Drive
2. Wait for sync to complete
3. Run backup on desktop first: `backup-petesbrain`

### Sync Fails - "Permission denied"

**Solution:**
```bash
chmod +x ~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh
```

### Changes Not Syncing

**Check:**
1. Are you committing changes? (Git method)
2. Is iCloud Drive syncing? (iCloud method)
3. Are machines on same network? (rsync method)

**Debug:**
```bash
# Check sync logs
tail -f ~/.petesbrain-sync.log

# Check Git status
cd ~/Documents/PetesBrain
git status

# Check iCloud backups
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/
```

---

## Best Practices

1. **Sync Before Major Changes**
   - Always pull latest before starting work
   - Push changes before closing

2. **Commit Frequently** (Git method)
   - Small, frequent commits are easier to sync
   - Use descriptive commit messages

3. **Monitor Sync Logs**
   - Check logs weekly for errors
   - Fix issues promptly

4. **Test Restore**
   - Periodically verify you can restore from backup
   - Test sync on both machines

5. **Keep Machines Updated**
   - Ensure both machines have latest sync scripts
   - Update Git remotes if repository changes

---

## Files Reference

### Scripts
- `shared/scripts/install-petesbrain.sh` - Installation script
- `shared/scripts/sync-petesbrain.sh` - Main sync script
- `shared/scripts/setup-auto-sync.sh` - Automatic sync setup

### LaunchAgents
- `~/Library/LaunchAgents/com.petesbrain.sync.plist` - Automatic sync agent

### Logs
- `~/.petesbrain-sync.log` - Sync operation log
- `~/.petesbrain-sync-error.log` - Error log

### Configuration
- `.is-desktop` - Marker file (optional, auto-detected)

---

## Quick Reference

### Installation
```bash
# On laptop
~/install-petesbrain.sh git
```

### Manual Sync
```bash
sync-petesbrain pull    # Get latest
sync-petesbrain push    # Send changes
sync-petesbrain both    # Both directions
```

### Automatic Sync
```bash
# Setup (one time)
cd ~/Documents/PetesBrain/shared/scripts
./setup-auto-sync.sh laptop

# Check status
launchctl list | grep petesbrain.sync
```

### Troubleshooting
```bash
# Check logs
tail -f ~/.petesbrain-sync.log

# Check Git status
cd ~/Documents/PetesBrain && git status

# Manual sync
sync-petesbrain both
```

---

## Related Documentation

- [Backup System](BACKUP-SYSTEM.md) - Automated backups
- [Disaster Recovery](DISASTER-RECOVERY-EMAIL.md) - Recovery procedures
- [System Health Monitoring](SYSTEM-HEALTH-MONITORING.md) - Monitor sync status

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-07 | 1.0 | Initial sync system with Git, iCloud, and rsync support |

