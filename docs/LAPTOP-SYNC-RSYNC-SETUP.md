# Laptop Sync Setup - rsync Method

**Status:** ✅ Configured
**Last Updated:** 2025-11-24
**Method:** Direct rsync over local network

---

## Overview

This is the **simplest and most reliable** sync method when you're always at your desk with both machines on the same network. No cloud services needed - just direct machine-to-machine sync.

## How It Works

- **Desktop**: Source of truth (Peters-Mac-mini.lan)
- **Laptop**: Pulls from desktop before leaving, pushes back when returning
- **Method**: rsync over SSH (local network only)
- **Config**: `.sync-config` file in PetesBrain root

---

## Desktop Setup (COMPLETED ✓)

Desktop is already configured:
- ✅ Sync script updated with rsync support
- ✅ `.sync-config` created with rsync method
- ✅ `sync-petesbrain` alias added to shell

---

## Laptop Setup (Do this before holiday)

### 1. Enable Remote Login on Desktop

On desktop (Peters-Mac-mini):
```bash
# System Settings → General → Sharing → Remote Login → ON
# Or via command line:
sudo systemsetup -setremotelogin on
```

### 2. Copy PetesBrain to Laptop

**Option A: Initial rsync (recommended)**
```bash
# On laptop, from home directory
cd ~/Documents

# First time sync - will copy entire project
rsync -avz --progress \
  --exclude='.git' \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='.DS_Store' \
  --exclude='.venv' \
  --exclude='node_modules' \
  --exclude='.config/venv' \
  administrator@Peters-Mac-mini.lan:/Users/administrator/Documents/PetesBrain/ \
  ~/Documents/PetesBrain/
```

**Option B: USB drive**
```bash
# Copy from USB to laptop
cp -r /Volumes/USB/PetesBrain ~/Documents/
```

### 3. Set Up Laptop Alias

On laptop:
```bash
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Test It Works

On laptop:
```bash
# Test pulling from desktop
sync-petesbrain pull
```

You should see:
```
═══════════════════════════════════════════════════
    PetesBrain Sync
═══════════════════════════════════════════════════

Machine: Peters-MacBook-Pro.local
Type: Laptop
Direction: pull

→ Using rsync direct sync...
→ Syncing from desktop: administrator@Peters-Mac-mini.lan

[rsync progress output]

✓ Pulled from desktop
```

---

## Daily Workflow

### Before Going on Holiday (Laptop)

1. **Sit at your desk** (both machines on same network)
2. **Pull latest from desktop**:
   ```bash
   sync-petesbrain pull
   ```
3. Done! Take laptop on holiday

### While on Holiday (Laptop)

- Work normally on laptop
- All changes stay local
- No need to sync anything

### When You Return (Laptop)

1. **Sit at your desk** (both machines on same network)
2. **Push changes back to desktop**:
   ```bash
   sync-petesbrain push
   ```
3. Done! Desktop now has all your holiday work

### On Desktop

Desktop doesn't need to do anything - just:
```bash
sync-petesbrain push
```

This just confirms it's the source. Laptop will pull from it.

---

## Troubleshooting

### "Connection refused" or "Host unreachable"

**Check:**
1. Both machines on same network?
2. Can ping desktop? `ping Peters-Mac-mini.lan`
3. Is Remote Login enabled on desktop?

**Fix:**
```bash
# On desktop, enable Remote Login
sudo systemsetup -setremotelogin on

# Check it's running
sudo systemsetup -getremotelogin
```

### "Permission denied"

**SSH key not set up.** First time will ask for password. To avoid this:

```bash
# On laptop, create SSH key if you don't have one
ssh-keygen -t ed25519

# Copy to desktop
ssh-copy-id administrator@Peters-Mac-mini.lan
```

### "No such file or directory"

The laptop doesn't have PetesBrain yet. Use the initial rsync from step 2 above.

### sync-petesbrain command not found

```bash
# On laptop, add alias
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
source ~/.zshrc
```

---

## Configuration Files

### `.sync-config` (in PetesBrain root)

```bash
# PetesBrain Sync Configuration
SYNC_METHOD="rsync"

# Desktop hostname (for laptop to pull from)
DESKTOP_HOST="Peters-Mac-mini.lan"
DESKTOP_USER="administrator"
DESKTOP_PATH="/Users/administrator/Documents/PetesBrain"
```

**Important:** This file should be the **same on both machines**.

---

## Advantages of rsync Method

✅ **Fast** - Direct network transfer, no cloud upload/download
✅ **Reliable** - Works every time when on same network
✅ **Simple** - No accounts, tokens, or cloud services
✅ **Secure** - Stays on your local network
✅ **No quotas** - No storage limits or sync issues

---

## Network Requirements

- Both machines must be on **same WiFi network**
- Desktop must have **Remote Login enabled**
- Laptop must be able to **reach desktop hostname** (`Peters-Mac-mini.lan`)

If you're on different networks (e.g., hotel WiFi), this method won't work - you'd need to set up Git sync or iCloud sync instead.

---

## Quick Reference

### Before Holiday
```bash
# On laptop, at desk
sync-petesbrain pull
```

### After Holiday
```bash
# On laptop, at desk
sync-petesbrain push
```

### Check Status
```bash
# On desktop
sync-petesbrain push    # Just confirms desktop is source

# On laptop
sync-petesbrain pull    # Test pulling from desktop
```

---

## Next Steps

1. ✅ Desktop is configured
2. ⏳ Before holiday: Set up laptop (follow "Laptop Setup" above)
3. ⏳ Test pull from laptop while at desk
4. ⏳ Take laptop on holiday
5. ⏳ When back: Push changes from laptop to desktop

---

**Related Documentation:**
- [Sync System Guide](SYNC-SYSTEM.md) - Full sync documentation
- [Backup System](BACKUP-SYSTEM.md) - Automated backups
