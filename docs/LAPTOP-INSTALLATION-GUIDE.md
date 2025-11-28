# PetesBrain Laptop Installation - Step-by-Step Guide

**Mode Recommendation:** Use **Chat mode** for this installation - it's best for interactive, line-by-line guidance where you can ask questions and get immediate help.

---

## Pre-Installation Checklist

Before starting, make sure you have:
- [ ] Your laptop turned on and connected to internet
- [ ] Terminal/command line access
- [ ] Your desktop machine accessible (for copying files)
- [ ] iCloud Drive enabled (if using iCloud method)
- [ ] Git installed (if using Git method) - check with: `git --version`

---

## Step 1: Open Terminal

**On your laptop:**

1. Press `Cmd + Space` to open Spotlight
2. Type "Terminal" and press Enter
3. Terminal window should open

**Verify:** You should see a prompt like: `yourname@laptop ~ %`

---

## Step 2: Check Your Current Location

**Type this command:**
```bash
pwd
```

**Expected output:** Something like `/Users/yourname` or `/Users/yourname/Desktop`

**What this does:** Shows your current directory (where you are)

---

## Step 3: Navigate to Documents Folder

**Type this command:**
```bash
cd ~/Documents
```

**Verify:**
```bash
pwd
```

**Expected output:** `/Users/yourname/Documents`

**What this does:** Changes to your Documents folder (where we'll install PetesBrain)

---

## Step 4: Choose Your Installation Method

You have 3 options. Choose ONE:

### Option A: From iCloud Backup (Easiest - Recommended) ⭐

**Best if:** You have iCloud Drive enabled and backups are running

**Continue to Step 5A**

### Option B: From Desktop via Network (scp/rsync)

**Best if:** Both machines are on same network

**Continue to Step 5B**

### Option C: From Git Repository

**Best if:** You have a Git repository set up

**Continue to Step 5C**

---

## Step 5A: Install from iCloud Backup

### Step 5A.1: Check iCloud Backups Available

**Type this command:**
```bash
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/ | head -5
```

**Expected output:** List of backup files like `PetesBrain-backup-20251107-123456.tar.gz`

**If you see "No such file or directory":**
- iCloud Drive might not be synced yet
- Wait a few minutes and try again
- Or use Option B or C instead

### Step 5A.2: Find Latest Backup

**Type this command:**
```bash
ls -t ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz | head -1
```

**Expected output:** Full path to latest backup file

**Copy this path** - you'll need it in next step

### Step 5A.3: Extract the Backup

**Type this command (replace BACKUP_PATH with the path from Step 5A.2):**
```bash
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz
```

**Or if that doesn't work, use the exact path:**
```bash
tar -xzf "BACKUP_PATH"
```

**What this does:** Extracts PetesBrain from the backup file

**Wait for it to finish** - this may take 1-2 minutes

### Step 5A.4: Verify Installation

**Type this command:**
```bash
ls -la PetesBrain
```

**Expected output:** Should show PetesBrain directory with folders like `clients/`, `tools/`, `shared/`, etc.

**If successful:** Skip to Step 6

---

## Step 5B: Install from Desktop via Network

### Step 5B.1: Get Desktop IP Address

**On your desktop machine:**
1. Open System Settings → Network
2. Note your IP address (e.g., `192.168.1.100`)

**Or use this command on desktop:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Step 5B.2: Copy Installation Script

**On your laptop, type (replace DESKTOP_IP with actual IP):**
```bash
scp administrator@DESKTOP_IP:/Users/administrator/Documents/PetesBrain/shared/scripts/install-petesbrain.sh ~/
```

**Example:**
```bash
scp administrator@192.168.1.100:/Users/administrator/Documents/PetesBrain/shared/scripts/install-petesbrain.sh ~/
```

**You'll be prompted for password** - enter your desktop password

### Step 5B.3: Run Installation Script

**Type this command:**
```bash
chmod +x ~/install-petesbrain.sh
~/install-petesbrain.sh rsync
```

**Follow the prompts** - it will ask for desktop hostname/IP

**If successful:** Skip to Step 6

---

## Step 5C: Install from Git Repository

### Step 5C.1: Clone Repository

**Type this command (replace REPO_URL with your Git repository URL):**
```bash
git clone REPO_URL ~/Documents/PetesBrain
```

**Example (GitHub):**
```bash
git clone https://github.com/yourusername/petesbrain.git ~/Documents/PetesBrain
```

**Or if you have SSH set up:**
```bash
git clone git@github.com:yourusername/petesbrain.git ~/Documents/PetesBrain
```

### Step 5C.2: Verify Installation

**Type this command:**
```bash
cd ~/Documents/PetesBrain && ls -la
```

**Expected output:** Should show PetesBrain directory contents

**If successful:** Continue to Step 6

---

## Step 6: Navigate to PetesBrain Directory

**Type this command:**
```bash
cd ~/Documents/PetesBrain
```

**Verify:**
```bash
pwd
```

**Expected output:** `/Users/yourname/Documents/PetesBrain`

---

## Step 7: Make Sync Script Executable

**Type this command:**
```bash
chmod +x shared/scripts/sync-petesbrain.sh
```

**Verify:**
```bash
ls -la shared/scripts/sync-petesbrain.sh
```

**Expected output:** Should show `-rwxr-xr-x` (the 'x' means executable)

---

## Step 8: Set Up Command Alias

### Step 8.1: Check Which Shell You're Using

**Type this command:**
```bash
echo $SHELL
```

**Expected output:** `/bin/zsh` or `/bin/bash`

### Step 8.2: Add Alias to Shell Config

**If output was `/bin/zsh`, type:**
```bash
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
```

**If output was `/bin/bash`, type:**
```bash
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.bashrc
```

**Most likely zsh on modern Macs** - so use the first command

### Step 8.3: Reload Shell Config

**Type this command:**
```bash
source ~/.zshrc
```

**Or if using bash:**
```bash
source ~/.bashrc
```

### Step 8.4: Test the Alias

**Type this command:**
```bash
sync-petesbrain --help
```

**Expected output:** Should show sync script help or run the script

**If you see "command not found":**
- Try closing and reopening Terminal
- Or manually run: `~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh --help`

---

## Step 9: Set Up Python Environment (Optional but Recommended)

### Step 9.1: Check Python Version

**Type this command:**
```bash
python3 --version
```

**Expected output:** `Python 3.x.x` (any 3.x version is fine)

**If you see "command not found":**
- Install Python from python.org or use Homebrew: `brew install python3`

### Step 9.2: Create Virtual Environment

**Type this command:**
```bash
cd ~/Documents/PetesBrain
python3 -m venv venv
```

**What this does:** Creates isolated Python environment

**Wait for it to finish** - may take 30 seconds

### Step 9.3: Activate Virtual Environment

**Type this command:**
```bash
source venv/bin/activate
```

**Expected output:** Your prompt should now show `(venv)` at the beginning

**Example:** `(venv) yourname@laptop PetesBrain %`

### Step 9.4: Install Dependencies (If requirements.txt exists)

**Type this command:**
```bash
pip install -r requirements.txt
```

**Note:** This may not be needed if there's no requirements.txt file

**If you see "No such file":** That's okay, skip this step

---

## Step 10: Test Installation

### Step 10.1: Verify Directory Structure

**Type this command:**
```bash
ls -la
```

**Expected output:** Should show folders like:
- `clients/`
- `tools/`
- `shared/`
- `docs/`
- `agents/`

### Step 10.2: Test Sync Script

**Type this command:**
```bash
sync-petesbrain pull
```

**Or if alias didn't work:**
```bash
~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh pull
```

**Expected output:** Should show sync process (may take a minute)

**If you see errors:** Don't worry - we'll set up automatic sync next

---

## Step 11: Set Up Automatic Syncing

### Step 11.1: Navigate to Scripts Directory

**Type this command:**
```bash
cd ~/Documents/PetesBrain/shared/scripts
```

### Step 11.2: Make Setup Script Executable

**Type this command:**
```bash
chmod +x setup-auto-sync.sh
```

### Step 11.3: Run Setup Script

**Type this command:**
```bash
./setup-auto-sync.sh laptop
```

**Expected output:** Should show:
- "Creating LaunchAgent..."
- "Loading LaunchAgent..."
- "Automatic Sync Configured!"

### Step 11.4: Verify Automatic Sync is Running

**Type this command:**
```bash
launchctl list | grep petesbrain.sync
```

**Expected output:** Should show a process ID and status

**If you see nothing:** That's okay - it may take a moment to start

---

## Step 12: Set Up Environment Variables (If Needed)

### Step 12.1: Check if You Need API Keys

**Some tools may need API keys. Check:**
```bash
grep -r "ANTHROPIC_API_KEY" ~/Documents/PetesBrain/docs/ | head -3
```

**If you see references to API keys:** You may need to set them up

### Step 12.2: Add API Key to Shell Config (If Needed)

**Type this command (replace YOUR_KEY with actual key):**
```bash
echo 'export ANTHROPIC_API_KEY="YOUR_KEY"' >> ~/.zshrc
```

**Then reload:**
```bash
source ~/.zshrc
```

**Note:** Only do this if you actually need API keys for tools you'll use

---

## Step 13: Final Verification

### Step 13.1: Check Everything is Installed

**Type this command:**
```bash
cd ~/Documents/PetesBrain && ls -la
```

**Should see:** All main directories

### Step 13.2: Check Sync Script Works

**Type this command:**
```bash
sync-petesbrain pull
```

**Should see:** Sync process running

### Step 13.3: Check Automatic Sync Status

**Type this command:**
```bash
launchctl list | grep petesbrain
```

**Should see:** Sync agent listed

### Step 13.4: View Sync Logs

**Type this command:**
```bash
tail -20 ~/.petesbrain-sync.log
```

**Should see:** Recent sync activity (may be empty if just set up)

---

## ✅ Installation Complete!

**You're all set!** PetesBrain is now installed on your laptop.

---

## Daily Usage

**Before starting work:**
```bash
sync-petesbrain pull
```

**Before closing:**
```bash
sync-petesbrain push
```

**Check sync status:**
```bash
tail -f ~/.petesbrain-sync.log
```

---

## Troubleshooting

### "Command not found" errors
- Close and reopen Terminal
- Or use full path: `~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh`

### Sync fails
- Check logs: `tail -f ~/.petesbrain-sync.log`
- Try manual sync: `sync-petesbrain both`
- Check Git status: `cd ~/Documents/PetesBrain && git status`

### Need help?
- See full docs: `docs/SYNC-SYSTEM.md`
- Check logs: `~/.petesbrain-sync.log`

---

## Next Steps

1. **Test sync:** Run `sync-petesbrain pull` to get latest changes
2. **Work normally:** Make changes, add files
3. **Sync regularly:** Run `sync-petesbrain push` before closing
4. **Automatic sync:** Already set up - runs every hour

---

**Ready to start?** Begin with Step 1 and work through each step. If you get stuck at any point, ask for help!

