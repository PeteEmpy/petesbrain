Subject: PetesBrain - Complete Disaster Recovery Protocol

---

# PetesBrain Disaster Recovery Protocol

**Use this if:** Your computer crashes, is lost, stolen, or otherwise unavailable and you need to restore everything on a new/repaired Mac.

---

## 📦 What's Backed Up

Your complete PetesBrain project is automatically backed up to iCloud Drive:

**Location:** iCloud Drive → PetesBrain-Backups folder  
**Frequency:** Weekly (every Monday 3 AM) + on-demand  
**Retention:** Last 10 backups  
**Size:** ~1 GB compressed per backup

---

## 🚨 Emergency Recovery Steps

### Step 1: Access iCloud Drive

**From any computer with internet:**

1. Go to: https://www.icloud.com
2. Sign in with your Apple ID: **petere@roksys.co.uk** (or your Apple ID)
3. Click "iCloud Drive"
4. Navigate to folder: **PetesBrain-Backups**
5. You'll see files named: `PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz`

**From a new/repaired Mac:**

1. Sign into your Apple ID in System Settings
2. Enable iCloud Drive (System Settings → Apple ID → iCloud → iCloud Drive: ON)
3. Wait for iCloud to sync (may take a few minutes)
4. Open Finder → iCloud Drive → PetesBrain-Backups

---

### Step 2: Download Latest Backup

**Via iCloud.com:**
- Click the backup file (choose the most recent date/time)
- Click download icon (cloud with down arrow)
- Save to Downloads folder

**Via Mac Finder:**
- The backup is already on your computer via iCloud Drive
- Located at: `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/`

---

### Step 3: Extract the Backup

**Open Terminal** (Applications → Utilities → Terminal) and run:

```bash
# Navigate to your Documents folder
cd ~/Documents

# Extract the backup (replace YYYYMMDD-HHMMSS with your actual backup date/time)
tar -xzf ~/Downloads/PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz
```

**Or if accessing from iCloud Drive directly:**

```bash
cd ~/Documents
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz
```

This creates: `/Users/[yourusername]/Documents/PetesBrain/`

---

### Step 4: Verify Recovery

```bash
# Check the project is there
ls -la ~/Documents/PetesBrain

# You should see folders like:
# - agents/
# - clients/
# - docs/
# - shared/
# - tools/
# - roksys/
```

---

## 🔧 Reinstalling Dependencies

Your project needs Python and some system packages. Here's how to reinstall everything:

### 1. Install Homebrew (Package Manager)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3

```bash
brew install python@3.11
```

### 3. Reinstall Python Virtual Environments

The backup includes venv folders but they may not work on a new machine. Recreate them:

```bash
# For email sync tools
cd ~/Documents/PetesBrain/shared/email-sync
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# For product impact analyzer
cd ~/Documents/PetesBrain/tools/product-impact-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# For Google Ads generator
cd ~/Documents/PetesBrain/tools/google-ads-generator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# For Granola importer
cd ~/Documents/PetesBrain/tools/granola-importer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

---

## 🤖 Reactivating Automated Agents

Your 20+ automated agents are configured via LaunchAgents. These are already in the backup, but need to be reloaded:

### Reload All Agents

```bash
# Load all PetesBrain agents
launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist
```

### Verify Agents Are Running

```bash
# Check how many are loaded
launchctl list | grep petesbrain | wc -l

# Should show: 28 (or similar number)
```

### Check Agent Status

```bash
# View all running agents
launchctl list | grep petesbrain
```

---

## 🔑 Credentials & API Keys

**Important:** Your credentials are backed up in the project but you may need to verify API access:

### Files Containing Credentials:

1. **Google Ads API:** `~/google-ads.yaml`
2. **Google Services:** `~/Documents/PetesBrain/shared/credentials/*.json`
3. **MCP Servers:** `~/Documents/PetesBrain/shared/mcp-servers/*/credentials.json`

### If Credentials Are Missing:

**Google Ads API:**
- Download from: Google Ads API Center
- Save to: `~/google-ads.yaml`

**Google Analytics/Sheets:**
- Download from: Google Cloud Console
- Save to: `~/Documents/PetesBrain/shared/credentials/`

**Claude API Key:**
- Get from: https://console.anthropic.com
- Add to: `~/.zshrc` as `export ANTHROPIC_API_KEY="your-key"`

---

## 🧪 Testing the Recovery

Run these commands to verify everything works:

```bash
# Test backup system
~/Documents/PetesBrain/shared/scripts/backup-petesbrain.sh

# Test system health
python3 ~/Documents/PetesBrain/agents/system/health-check.py

# Check agent status
launchctl list | grep petesbrain
```

---

## 📱 Quick Recovery Checklist

- [ ] Access iCloud Drive (icloud.com or Mac Finder)
- [ ] Download latest backup from PetesBrain-Backups folder
- [ ] Extract to ~/Documents/PetesBrain
- [ ] Install Homebrew
- [ ] Install Python 3
- [ ] Recreate virtual environments (4 folders)
- [ ] Load LaunchAgents
- [ ] Verify credentials exist
- [ ] Test system health
- [ ] Verify agents running

**Total time:** 30-60 minutes depending on download speeds

---

## 🆘 If You're Stuck

### Can't find backups?

**Check:**
1. iCloud.com → iCloud Drive → PetesBrain-Backups
2. On Mac: Finder → iCloud Drive → PetesBrain-Backups
3. Path: `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/`

### Backup file won't extract?

**Try:**
```bash
# Check file exists
ls -lh ~/Downloads/PetesBrain-backup-*.tar.gz

# Extract with verbose output
tar -xzvf ~/Downloads/PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz -C ~/Documents/
```

### LaunchAgents won't load?

**Try:**
```bash
# Unload first (ignore errors)
launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist 2>/dev/null

# Then load
launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist
```

### Virtual environments fail?

**Make sure Python 3 is installed:**
```bash
which python3
python3 --version  # Should show Python 3.11 or higher
```

---

## 📋 Important File Locations Reference

### Primary Backup Location:
```
iCloud Drive → PetesBrain-Backups/
~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/
```

### Project Location After Recovery:
```
~/Documents/PetesBrain/
```

### LaunchAgents:
```
~/Library/LaunchAgents/com.petesbrain.*.plist
```

### Credentials:
```
~/google-ads.yaml
~/Documents/PetesBrain/shared/credentials/
~/Documents/PetesBrain/shared/mcp-servers/*/credentials.json
```

### Virtual Environments to Recreate:
```
~/Documents/PetesBrain/shared/email-sync/.venv
~/Documents/PetesBrain/tools/product-impact-analyzer/.venv
~/Documents/PetesBrain/tools/google-ads-generator/.venv
~/Documents/PetesBrain/tools/granola-importer/.venv
```

---

## 🎯 Success Indicators

**You've successfully recovered when:**

✅ Project exists at ~/Documents/PetesBrain  
✅ All folders present (agents, clients, docs, shared, tools, roksys)  
✅ `launchctl list | grep petesbrain` shows 28+ agents  
✅ `python3 agents/system/health-check.py` runs without errors  
✅ Backup command works: `~/Documents/PetesBrain/shared/scripts/backup-petesbrain.sh`  

---

## 📚 Additional Documentation

Once recovered, these documents in your project explain everything:

- **agents/README.md** - All 20+ agents documented
- **docs/BACKUP-SYSTEM.md** - Backup system details
- **docs/AUTOMATION.md** - How automation works
- **README.md** - Project overview

---

## 💾 Keep This Email Accessible

**Recommended:**
1. Email this to yourself at multiple email addresses
2. Save in password manager (1Password, LastPass, etc.)
3. Print a physical copy and keep somewhere safe
4. Save to personal Dropbox/Google Drive as backup

---

**Last Updated:** November 5, 2025  
**Backup System Version:** 1.0  
**Project Version:** Production with 20+ agents

---

**You're protected.** Your backups run automatically every Monday at 3 AM, and you can create backups anytime by typing `backup-petesbrain` in Terminal. Everything goes to iCloud automatically.

---

*This disaster recovery protocol was created as part of PetesBrain's comprehensive backup system implemented November 5, 2025.*

