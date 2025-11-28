# Quick Check: Is Python 3 Installed?

**For:** Checking Python 3 installation on your laptop

---

## Quick Check Commands

Open Terminal on your laptop and run these commands:

### 1. Check if Python 3 is installed:

```bash
python3 --version
```

**Expected output:**
- ✅ `Python 3.x.x` (any version 3.x) = Python 3 is installed
- ❌ `command not found` = Python 3 is NOT installed

### 2. Check if pip3 is available:

```bash
pip3 --version
```

**Or if that doesn't work:**

```bash
python3 -m pip --version
```

**Expected output:**
- ✅ `pip x.x.x` = pip is installed
- ❌ `command not found` = pip is NOT installed

### 3. Find where Python 3 is installed:

```bash
which python3
```

**Expected output:**
- ✅ `/usr/bin/python3` or `/usr/local/bin/python3` = Python 3 location
- ❌ (nothing) = Python 3 not found in PATH

---

## If Python 3 is NOT Installed

### Step 1: Install Xcode Command Line Tools (Required First!)

**Before installing Python 3, you need Xcode Command Line Tools:**

When you see the message:
```
xcode-select: note: No developer tools were found, requesting install.
```

**Do this:**
1. A dialog box will appear asking to install Command Line Tools
2. Click **"Install"** 
3. Wait for installation to complete (this may take 10-15 minutes)
4. You'll see: "The software was installed"

**Or install manually:**
```bash
xcode-select --install
```

**Verify installation:**
```bash
xcode-select -p
```

Should show: `/Library/Developer/CommandLineTools` or `/Applications/Xcode.app/Contents/Developer`

### Step 2: Install Python 3

**Option A: Using Homebrew (Recommended):**

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3
```

**Option B: Using official installer:**

1. Go to: https://www.python.org/downloads/
2. Download Python 3.x for macOS
3. Run the installer
4. Make sure to check "Add Python to PATH" during installation

### Step 3: Verify Installation

After installing, close and reopen Terminal, then:

```bash
python3 --version
```

Should show: `Python 3.x.x`

---

## If Python 3 IS Installed

Great! You can proceed with the migration setup:

```bash
cd ~/Documents/PetesBrain
./shared/scripts/check-migration-status.sh
```

This will check:
- ✅ Python 3 installation
- ✅ Virtual environments
- ✅ Path updates
- ✅ Credentials
- ✅ Everything else needed for migration

---

## Common Issues

### Xcode Command Line Tools Installation

**If you see:** `xcode-select: note: No developer tools were found`

**Solution:** 
1. Click "Install" in the dialog that appears
2. Or run: `xcode-select --install`
3. Wait for installation to complete (10-15 minutes)
4. Then proceed with Python 3 installation

**If installation fails or dialog doesn't appear:**
```bash
# Try manual installation
sudo xcode-select --install

# Or download from Apple Developer site
# https://developer.apple.com/download/all/
```

### "Python 3 not found" but you just installed it

**Solution:** Close and reopen Terminal, or run:

```bash
source ~/.zshrc
```

### "Permission denied" when running scripts

**Solution:** Make scripts executable:

```bash
chmod +x shared/scripts/*.sh
```

### Python 3 installed but pip3 not found

**Solution:** Install pip separately:

```bash
python3 -m ensurepip --upgrade
```

Or install via Homebrew:

```bash
brew install python3
```

### Homebrew installation fails

**If Homebrew installation fails, it's likely because Xcode Command Line Tools aren't installed yet.**

**Solution:**
1. Install Xcode Command Line Tools first (see above)
2. Then try Homebrew installation again

---

## Next Steps

Once Python 3 is confirmed installed:

1. **Run status check:**
   ```bash
   cd ~/Documents/PetesBrain
   ./shared/scripts/check-migration-status.sh
   ```

2. **Run setup script:**
   ```bash
   ./shared/scripts/setup-new-machine.sh
   ```

3. **Follow the prompts** - the script will guide you through everything!

---

**Note:** Since you're using ZSH (default on macOS), all scripts will automatically use `~/.zshrc` for aliases and environment variables. No special configuration needed!

