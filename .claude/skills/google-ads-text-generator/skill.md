---
name: google-ads-text-generator
description: Launches the Google Ads Text Generator web application for creating text assets (headlines, descriptions, search themes, sitelinks, callouts). Use when user says "start the generator", "generate ad copy", "create headlines", or needs Performance Max text assets.
allowed-tools: Bash, Read
---

# Google Ads Text Generator Launch Skill

## Instructions

When this skill is triggered:

1. **Navigate to the generator directory**:
   ```bash
   cd ~/Documents/PetesBrain/tools/google-ads-generator
   ```

2. **IMPORTANT: Check and fix virtual environment if needed**:
   Before starting, verify the virtual environment is healthy:
   ```bash
   cd ~/Documents/PetesBrain/tools/google-ads-generator

   # Test if venv is corrupted by trying a quick pip command with timeout
   if [ -d ".venv" ]; then
       # If pip hangs/fails, the venv is corrupted - rebuild it
       if ! .venv/bin/python -c "import sys; sys.exit(0)" 2>/dev/null; then
           echo "Virtual environment corrupted, rebuilding..."
           rm -rf .venv
           python3 -m venv .venv
           .venv/bin/pip install -q -r requirements.txt
       fi
   fi
   ```

   This prevents hanging issues caused by corrupted virtual environments.

3. **Launch the web application**:
   ```bash
   ./start.sh
   ```

   Or if the script isn't executable:
   ```bash
   bash start.sh
   ```

4. **What happens**:
   - The script checks for `ANTHROPIC_API_KEY` (loads from `.env` file or shell config)
   - Activates or creates the virtual environment (`.venv`)
   - Starts Flask server on `http://localhost:5001`
   - Automatically opens browser to the web interface

5. **Alternative launch methods**:
   - **Desktop app**: `python3 desktop.py` (opens native window)
   - **Double-click**: `Launch Google Ads Text Generator.command` file in Finder
   - **Direct Python**: `source .venv/bin/activate && python3 app.py`

6. **Verify it's running**:
   - Check if port 5001 is listening: `lsof -i :5001`
   - Test connection: `curl http://localhost:5001`
   - Browser should open automatically to `http://localhost:5001`

7. **If API key is missing**:
   - Check for `.env` file in the generator directory
   - If missing, create it: `echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env`
   - Or ensure it's in shell config (`~/.zshrc` or `~/.bashrc`)

8. **To stop the server**:
   ```bash
   pkill -f "app.py"
   ```
   Or press `Ctrl+C` in the terminal where it's running

## Tool Location

**Directory**: `tools/google-ads-generator/`

**Key Files**:
- `start.sh` - Main launch script (recommended)
- `app.py` - Flask web application
- `desktop.py` - Desktop app version
- `.env` - API key configuration (if exists)
- `requirements.txt` - Python dependencies

## Features Available

Once launched, the web interface provides:

1. **URL Analysis Mode**:
   - Enter any website URL
   - Automatically analyzes and generates ad copy
   - Uses Claude AI for intelligent copy generation

2. **Manual Entry Mode**:
   - Product/service name
   - Brand name
   - Website URL
   - Custom context

3. **Asset Generation**:
   - **Search Themes** (50 terms for Performance Max)
   - **Headlines** (50 total: 10 per section, 30 char max)
   - **Descriptions** (50 total: 10 per section, 90 char max)
   - **Sitelinks** (with headlines, descriptions, URLs)
   - **Callout Extensions** (5 total)

4. **Export Options**:
   - CSV format for Google Ads Editor
   - Formatted text output
   - Individual asset type exports

## Prerequisites

- Python 3.10+ installed
- `ANTHROPIC_API_KEY` configured (in `.env` or shell config)
- Virtual environment will be created automatically if missing
- Dependencies installed via `requirements.txt`

## Troubleshooting

### Server won't start or hangs
**MOST COMMON ISSUE: Corrupted virtual environment**
- Symptom: Script hangs at "Starting Flask application..." or imports hang
- Fix: Remove and rebuild the virtual environment:
  ```bash
  cd ~/Documents/PetesBrain/tools/google-ads-generator
  rm -rf .venv
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
  ./start.sh
  ```

**Other checks:**
- Check Python version: `python3 --version` (needs 3.10+)
- Verify API key: `echo $ANTHROPIC_API_KEY`
- Check virtual environment: `ls -la .venv/bin/python`

### Port 5001 already in use
- Find process: `lsof -i :5001`
- Kill existing process: `kill <PID>`
- Or use different port: Edit `app.py` line 444 to change port

### Browser doesn't open
- Manually navigate to: `http://localhost:5001`
- Or: `http://127.0.0.1:5001`

### API key error
- Create `.env` file: `echo 'ANTHROPIC_API_KEY=your-key' > .env`
- Or add to shell config: `export ANTHROPIC_API_KEY='your-key'` in `~/.zshrc`

## Related Tools

- **Google Ads Campaign Audit Skill** - For analyzing account performance
- **GAQL Query Builder Skill** - For building data queries
- **CSV Analyzer Skill** - For analyzing exported performance data

## Notes

- The generator follows ROK specifications for Google Ads text assets
- Assets are organized into 5 sections: Benefits, Technical, Quirky, Call to Action, Brand/Category
- All assets are validated for character limits (30 for headlines, 90 for descriptions)
- The web interface provides real-time validation and formatting
- **Capitalization Standard (Nov 2025)**: All copy uses sentence case (first word + proper nouns capitalized, rest lowercase) based on research showing better CTR, ROAS, and CPA performance

---

**Quick Launch Command**:
```bash
cd ~/Documents/PetesBrain/tools/google-ads-generator && ./start.sh
```

