# PetesBrain Sync - Quick Start Guide

**For:** Setting up PetesBrain on your laptop and syncing with desktop

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Choose Your Sync Method

**Option A: Git (Recommended)** ⭐
- Best for: Regular syncing, version control
- Requires: Git repository (GitHub/GitLab)

**Option B: iCloud Drive**
- Best for: Simple setup, no Git needed
- Requires: iCloud Drive enabled

**Option C: rsync**
- Best for: Fast local network sync
- Requires: Both machines on same network

### Step 2: Install on Laptop

**From Desktop (copy script):**
```bash
# On laptop, download installation script
scp administrator@desktop:/Users/administrator/Documents/PetesBrain/shared/scripts/install-petesbrain.sh ~/

# Run installation
chmod +x ~/install-petesbrain.sh
~/install-petesbrain.sh git    # or 'icloud' or 'rsync'
```

**Or from iCloud Backup:**
```bash
# Extract latest backup
cd ~/Documents
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-LATEST.tar.gz

# Set up sync
cd ~/Documents/PetesBrain
chmod +x shared/scripts/sync-petesbrain.sh
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Set Up Automatic Syncing

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

---

## 📋 Daily Usage

### Before Starting Work (Laptop)
```bash
sync-petesbrain pull    # Get latest changes
```

### Before Closing (Either Machine)
```bash
sync-petesbrain push    # Send your changes
```

### Full Sync (Both Directions)
```bash
sync-petesbrain both    # Pull then push
```

---

## ✅ Verify It's Working

**Check sync status:**
```bash
launchctl list | grep petesbrain.sync
```

**View sync logs:**
```bash
tail -f ~/.petesbrain-sync.log
```

**Test manual sync:**
```bash
sync-petesbrain pull
```

---

## 🆘 Troubleshooting

**Sync not working?**
1. Check logs: `tail -f ~/.petesbrain-sync.log`
2. Try manual sync: `sync-petesbrain both`
3. Check Git status: `cd ~/Documents/PetesBrain && git status`

**Need help?**
See full documentation: `docs/SYNC-SYSTEM.md`

---

## 📚 Full Documentation

- **[Sync System Guide](docs/SYNC-SYSTEM.md)** - Complete documentation
- **[Backup System](docs/BACKUP-SYSTEM.md)** - Automated backups
- **[Disaster Recovery](docs/DISASTER-RECOVERY-EMAIL.md)** - Recovery procedures

---

**That's it!** Your PetesBrain is now syncing between desktop and laptop. 🎉

