# Step-by-Step: Setting Up PetesBrain on Your Laptop

**Goal:** Get PetesBrain working on your laptop so you can work on weekends

---

## Overview: What We're Doing

1. Install Python 3 on your laptop (needed to run PetesBrain)
2. Copy PetesBrain from your desktop to your laptop
3. Set up everything so it works on the laptop
4. Set up syncing so changes go back and forth

**Time:** About 30-45 minutes total

---

## STEP 1: Open Terminal on Your Laptop

1. Press `Cmd + Space` (opens Spotlight)
2. Type "Terminal"
3. Press Enter
4. Terminal window opens

**You should see:** A prompt like `yourname@laptop ~ %`

---

## STEP 2: Check if Python 3 is Installed

**Type this command:**
```bash
python3 --version
```

**What happens:**

### ✅ If you see: `Python 3.x.x`
- Python 3 is installed!
- **Skip to STEP 3**

### ❌ If you see: `command not found`
- Python 3 is NOT installed
- **Continue to STEP 2A**

---

## STEP 2A: Install Xcode Command Line Tools (If Needed)

**If you see:** `xcode-select: note: No developer tools were found`

**What to do:**
1. A dialog box will appear
2. Click **"Install"**
3. Wait 10-15 minutes (it downloads ~500MB)
4. You'll see "The software was installed"
5. Click **"Done"**

**If dialog doesn't appear, type:**
```bash
xcode-select --install
```

**After installation, verify:**
```bash
xcode-select -p
```

Should show: `/Library/Developer/CommandLineTools`

---

## STEP 2B: Install Python 3 (If Not Installed)

**Option A: Using Homebrew (Easiest)**

1. **Install Homebrew first:**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Follow the prompts
   - It will ask for your password
   - Wait for it to finish

2. **Install Python 3:**
   ```bash
   brew install python3
   ```
   - Wait for it to finish (5-10 minutes)

3. **Verify it worked:**
   ```bash
   python3 --version
   ```
   Should show: `Python 3.x.x`

**Option B: Download from Python.org**

1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.x.x"
3. Run the installer
4. **Important:** Check "Add Python to PATH" during installation
5. Close and reopen Terminal
6. Verify: `python3 --version`

---

## STEP 3: Copy PetesBrain to Your Laptop

**Choose ONE method:**

### Method A: From Git (If You Have a Git Repository)

**On your laptop, type:**
```bash
cd ~/Documents
git clone <your-repo-url> PetesBrain
```

**Replace `<your-repo-url>` with your actual Git repository URL**

**Example:**
```bash
git clone https://github.com/yourusername/petesbrain.git PetesBrain
```

**Then:**
```bash
cd PetesBrain
```

### Method B: From iCloud Backup

**On your laptop, type:**
```bash
cd ~/Documents
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz
```

**Then:**
```bash
cd PetesBrain
```

### Method C: From Desktop via Network

**On your laptop, type:**
```bash
cd ~/Documents
rsync -avz administrator@desktop:/Users/administrator/Documents/PetesBrain ./
```

**Replace `desktop` with your desktop's hostname or IP address**

**Then:**
```bash
cd PetesBrain
```

---

## STEP 4: Run the Setup Script

**This sets up everything automatically:**

```bash
chmod +x shared/scripts/setup-new-machine.sh
./shared/scripts/setup-new-machine.sh
```

**What it does:**
- Checks Python 3 is installed ✅
- Creates virtual environments ✅
- Updates all paths (from `/Users/administrator` to your username) ✅
- Sets up sync scripts ✅
- Validates everything ✅

**Wait for it to finish** (5-10 minutes)

**You'll see:** "Setup Complete!" when done

---

## STEP 5: Copy Credentials from Desktop

**These files need to be copied manually (for security):**

### Option A: Copy via Network (Easiest)

**On your laptop, type:**
```bash
# Copy MCP config
scp administrator@desktop:/Users/administrator/Documents/PetesBrain/.mcp.json ~/Documents/PetesBrain/

# Copy email credentials
scp administrator@desktop:/Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json ~/Documents/PetesBrain/shared/email-sync/

# Copy Google Drive credentials
scp administrator@desktop:/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json ~/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server/
```

**Repeat for other credential files as needed**

### Option B: Copy via USB Drive

1. Copy files from desktop to USB drive
2. Copy files from USB drive to laptop
3. Place them in the same locations

### Option C: Copy via iCloud Drive

1. Copy files to iCloud Drive on desktop
2. Copy files from iCloud Drive on laptop
3. Place them in the same locations

---

## STEP 6: Update Paths in .mcp.json (If Needed)

**After copying `.mcp.json`, update paths:**

```bash
cd ~/Documents/PetesBrain
sed -i '' 's|/Users/administrator|'"$HOME"'|g' .mcp.json
sed -i '' 's|/Users/administrator/Documents/PetesBrain|'"$HOME/Documents/PetesBrain"'|g' .mcp.json
```

**Or run the setup script again** - it will update paths automatically:
```bash
./shared/scripts/setup-new-machine.sh
```

---

## STEP 7: Set Up Sync Alias

**This makes it easy to sync:**

```bash
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
source ~/.zshrc
```

**Test it:**
```bash
sync-petesbrain --help
```

Should show sync script help or run the script.

---

## STEP 8: Test Everything

### Test 1: Python Works
```bash
source venv/bin/activate
python3 --version
deactivate
```

### Test 2: Sync Works
```bash
sync-petesbrain pull
```

Should sync files from desktop (or show Git pull).

### Test 3: Check Status
```bash
./shared/scripts/check-migration-status.sh
```

Shows what's set up and what's missing.

---

## STEP 9: Set Up Automatic Syncing (Optional)

**This syncs automatically in the background:**

```bash
cd ~/Documents/PetesBrain/shared/scripts
./setup-auto-sync.sh laptop
```

**What this does:**
- Creates a background process
- Pulls latest changes every hour
- You don't have to remember to sync

**Check if it's running:**
```bash
launchctl list | grep petesbrain.sync
```

---

## STEP 10: You're Done!

**Your weekend workflow:**

### Before Starting Work (Laptop)
```bash
sync-petesbrain pull
```
Gets latest changes from desktop.

### While Working
- Work normally - make changes, add files

### Before Closing (Laptop)
```bash
sync-petesbrain push
```
Sends your changes back to desktop.

### Back on Desktop (Monday)
- All weekend changes are already there!
- Or run: `sync-petesbrain pull` to make sure

---

## Troubleshooting

### "Command not found" errors
- Close and reopen Terminal
- Or use full path: `~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh`

### Python 3 not found after installing
- Close and reopen Terminal
- Or run: `source ~/.zshrc`

### Sync doesn't work
- Check Git is configured: `git remote -v`
- Or check iCloud Drive is synced
- See logs: `tail -f ~/.petesbrain-sync.log`

### Credentials not working
- Make sure you copied all credential files
- Check paths in `.mcp.json` are correct
- Restart Claude Desktop after updating `.mcp.json`

---

## Quick Reference

```bash
# Check status
cd ~/Documents/PetesBrain
./shared/scripts/check-migration-status.sh

# Sync commands
sync-petesbrain pull    # Get latest from desktop
sync-petesbrain push    # Send changes to desktop
sync-petesbrain both    # Pull then push

# Check sync status
launchctl list | grep petesbrain.sync

# View sync logs
tail -f ~/.petesbrain-sync.log
```

---

## Need Help?

**Check these guides:**
- `docs/LAPTOP-WEEKEND-SETUP.md` - Complete overview
- `docs/CHECK-PYTHON3.md` - Python 3 installation help
- `docs/XCODE-COMMAND-LINE-TOOLS.md` - Command Line Tools help
- `docs/SYNC-SYSTEM.md` - Sync system documentation

---

**That's it!** Follow these steps one at a time, and you'll have PetesBrain working on your laptop for weekend work.

