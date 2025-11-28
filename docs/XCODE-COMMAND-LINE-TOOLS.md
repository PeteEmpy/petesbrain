# Xcode Command Line Tools - Installation Guide

**For:** macOS users setting up Python 3 and development tools

---

## What Are Xcode Command Line Tools?

Xcode Command Line Tools are essential development tools for macOS. They include:
- Compilers (gcc, clang)
- Build tools (make, git)
- Required for Homebrew, Python 3, and many other development tools

**You DON'T need the full Xcode app** - just the command line tools (much smaller download).

---

## Installation

### Method 1: Automatic (Recommended)

When you try to install Homebrew or run certain commands, macOS will prompt you:

```
xcode-select: note: No developer tools were found, requesting install.
```

**What to do:**
1. A dialog box will appear: "The xcode-select command requires the command line developer tools"
2. Click **"Install"**
3. Wait for download and installation (10-15 minutes, ~500MB)
4. You'll see: "The software was installed"
5. Click **"Done"**

### Method 2: Manual Installation

If the dialog doesn't appear, install manually:

```bash
xcode-select --install
```

This will trigger the same installation dialog.

### Method 3: Download from Apple Developer

If automatic installation doesn't work:

1. Go to: https://developer.apple.com/download/all/
2. Sign in with your Apple ID (free account works)
3. Search for "Command Line Tools for Xcode"
4. Download the latest version for your macOS version
5. Run the installer

---

## Verify Installation

After installation, verify it worked:

```bash
xcode-select -p
```

**Expected output:**
- `/Library/Developer/CommandLineTools` (if only CLI tools installed)
- `/Applications/Xcode.app/Contents/Developer` (if full Xcode installed)

**Check version:**
```bash
xcode-select --version
```

Should show: `xcode-select version xxxx`

**Test git (included in CLI tools):**
```bash
git --version
```

Should show: `git version x.x.x`

---

## Troubleshooting

### Installation Stuck or Fails

**Solution 1: Reset and retry**
```bash
sudo xcode-select --reset
xcode-select --install
```

**Solution 2: Check disk space**
- Command Line Tools need ~500MB free space
- Check with: `df -h`

**Solution 3: Download manually**
- Use Method 3 above (download from Apple Developer site)

### "Command Line Tools are already installed" but they don't work

**Solution:**
```bash
# Check current path
xcode-select -p

# If pointing to wrong location, switch to CLI tools
sudo xcode-select --switch /Library/Developer/CommandLineTools

# Or if you have Xcode installed, switch to it
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

### After Installation, Commands Still Don't Work

**Solution:**
1. Close and reopen Terminal
2. Or restart your Mac
3. Verify with: `xcode-select -p`

---

## Why You Need This

**For PetesBrain migration, you need Command Line Tools for:**

1. **Homebrew** (if installing Python 3 via Homebrew)
   - Homebrew requires Command Line Tools to compile packages

2. **Python 3** (if building from source)
   - Python needs compilers to build extensions

3. **Git** (included in CLI tools)
   - Needed for syncing PetesBrain

4. **Other development tools**
   - Many Python packages need build tools

---

## Next Steps

After Command Line Tools are installed:

1. **Install Python 3:**
   ```bash
   # Via Homebrew (recommended)
   brew install python3
   
   # Or download from python.org
   ```

2. **Verify Python 3:**
   ```bash
   python3 --version
   ```

3. **Continue with PetesBrain setup:**
   ```bash
   cd ~/Documents/PetesBrain
   ./shared/scripts/check-migration-status.sh
   ```

---

## System Requirements

- **macOS:** 10.15 (Catalina) or later
- **Disk Space:** ~500MB free
- **Internet:** Required for download
- **Time:** 10-15 minutes for download and installation

---

**Note:** This is a one-time installation. Once installed, Command Line Tools stay on your system and update automatically with macOS updates.

