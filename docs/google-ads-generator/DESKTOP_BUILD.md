# Desktop Application - Build Guide

This guide explains how to run and build the Google Ads Text Generator as a standalone desktop application.

## Two Ways to Use the App

### 1. Web Version (Browser-based)
Run the Flask app and access via browser:
```bash
./start.sh
# Then open http://localhost:5001 in your browser
```

### 2. Desktop Version (Native Window)
Run as a desktop application with native window:
```bash
python3 desktop.py
```

## Development - Running Desktop App

**First time setup:**
```bash
# Install dependencies (including pywebview)
pip install -r requirements.txt

# Run desktop app
python3 desktop.py
```

**What happens:**
- Flask server starts in background
- Native desktop window opens automatically
- No browser needed!
- Close window to exit app

## Building Standalone .app (macOS)

### Quick Build

**One command to build:**
```bash
./build.sh
```

This will:
1. Create/activate virtual environment
2. Install all dependencies
3. Run PyInstaller
4. Create `dist/Google Ads Text Generator.app`

### Manual Build

**Step by step:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build with PyInstaller
pyinstaller desktop.spec

# 3. Find the app
ls dist/
```

### Running the Built App

**From Finder:**
1. Open the `dist` folder
2. Double-click `Google Ads Text Generator.app`

**From Terminal:**
```bash
open "dist/Google Ads Text Generator.app"
```

## Distribution

### Sharing the App

**To share with others:**
1. Build the app using `./build.sh`
2. Compress the .app:
   ```bash
   cd dist
   zip -r "Google Ads Text Generator.zip" "Google Ads Text Generator.app"
   ```
3. Share the .zip file
4. Recipients just unzip and double-click to run!

**Requirements for users:**
- macOS 10.13 or later
- No Python installation needed (everything is bundled!)

### First Run on macOS

Users may see "App from unidentified developer" warning:

**To open:**
1. Right-click the .app
2. Select "Open"
3. Click "Open" in the dialog
4. App will run and be trusted from then on

**Or bypass Gatekeeper:**
```bash
xargs -n 1 xattr -d com.apple.quarantine "Google Ads Text Generator.app"
```

## Build Output

After building, you'll have:

```
dist/
└── Google Ads Text Generator.app/
    └── Contents/
        ├── MacOS/
        │   └── Google Ads Text Generator (executable)
        ├── Resources/
        │   └── templates/ (Flask templates)
        └── Info.plist (app metadata)
```

**App size:** ~50-80 MB (includes Python runtime and all dependencies)

## Troubleshooting

### Build Fails

**Error: "pyinstaller: command not found"**
```bash
pip install pyinstaller
```

**Error: Missing templates**
- Check desktop.spec includes: `datas=[('templates', 'templates')]`

**Error: Import errors at runtime**
- Add missing modules to `hiddenimports` in desktop.spec

### Desktop App Issues

**App won't start**
```bash
# Run from terminal to see errors
./dist/Google\ Ads\ Text\ Generator.app/Contents/MacOS/Google\ Ads\ Text\ Generator
```

**Port 5001 already in use**
- Close other instances of the app
- Kill process: `lsof -ti:5001 | xargs kill -9`

**Window opens but blank**
- Flask server may not have started
- Check console output for errors

## Development Tips

### Testing Desktop App (Without Building)

```bash
# Quick test during development
python3 desktop.py
```

### Rebuilding After Changes

```bash
# Quick rebuild (reuses cache)
pyinstaller desktop.spec

# Clean rebuild (slower but thorough)
rm -rf build dist
./build.sh
```

### Adding an Icon

1. Create `icon.icns` file (macOS icon format)
2. Place in project root
3. Update desktop.spec:
   ```python
   app = BUNDLE(
       ...
       icon='icon.icns',  # Add this
       ...
   )
   ```
4. Rebuild

## Comparison: Web vs Desktop

| Feature | Web Version | Desktop Version |
|---------|-------------|-----------------|
| Launch | `./start.sh` + open browser | Double-click .app |
| Window | Browser tab | Native window |
| Terminal | Required (stays open) | Not needed |
| Distribution | Requires Python | Standalone .app |
| Updates | Git pull | Rebuild and redistribute |
| Size | Small (~20KB code) | Large (~60MB bundle) |

## Next Steps

1. **Test the desktop app:** `python3 desktop.py`
2. **Build the .app:** `./build.sh`
3. **Run the .app:** `open "dist/Google Ads Text Generator.app"`
4. **Share:** Zip the .app and send to users!

## Support

For build issues, check:
- PyInstaller documentation: https://pyinstaller.org/
- PyWebView documentation: https://pywebview.flowrl.com/

For app functionality issues, see TESTING_GUIDE.md
