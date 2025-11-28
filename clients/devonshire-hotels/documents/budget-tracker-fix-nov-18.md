# Devonshire Budget Tracker - Fixed November 18, 2025

## Problem
The automated budget tracker stopped working due to:
1. **Broken import paths**: Scripts referenced `shared/mcp-servers/` instead of `infrastructure/mcp-servers/`
2. **Virtual environment issues**: Google Sheets venv had broken dependencies
3. **Subprocess complexity**: Original design used subprocess calls to different venvs, adding complexity

## Solution

### Fixed Scripts
1. **`agents/budget-tracking/devonshire-budget-tracker.py`** (general template)
2. **`clients/devonshire-hotels/scripts/update_budget_tracker.py`** (LaunchAgent uses this)

### Changes Made
1. **Updated import paths**:
   - Changed from: `shared/mcp-servers/`
   - Changed to: `infrastructure/mcp-servers/`

2. **Replaced subprocess approach with direct imports**:
   - Old: Called separate Python processes via subprocess
   - New: Direct imports from MCP servers using path manipulation

3. **Consolidated dependencies**:
   - Installed Google Sheets API dependencies in Google Ads venv
   - Now uses single venv with all required packages
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

4. **Updated shebang**:
   - Changed from: `#!/usr/bin/env python3`
   - Changed to: `#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3`

5. **Updated LaunchAgent**:
   - File: `/Users/administrator/Library/LaunchAgents/com.petesbrain.devonshire-budget.plist`
   - Changed Python path to use Google Ads venv (has all dependencies)
   - Reloaded with: `launchctl bootstrap gui/$(id -u) ...`

### Test Results
```
[2025-11-18 18:39:41] UPDATE COMPLETE
[2025-11-18 18:39:41] Dev Properties: £5,946.92 / £9,000.00 (110.1% pacing)
[2025-11-18 18:39:41] The Hide: £1,243.60 / £2,000.00 (103.6% pacing)
[2025-11-18 18:39:41] Combined Total: £7,190.52
```

✅ Successfully fetches data from Google Ads API
✅ Successfully updates Google Sheets
✅ Calculates all metrics correctly
✅ LaunchAgent loaded and ready to run daily at 9:00 AM

## Schedule
- **Frequency**: Daily at 9:00 AM
- **LaunchAgent**: com.petesbrain.devonshire-budget
- **Log file**: `/Users/administrator/.petesbrain-devonshire-budget.log`

## Monitoring
Check log file to verify daily runs:
```bash
tail -f ~/.petesbrain-devonshire-budget.log
```

Check LaunchAgent status:
```bash
launchctl list | grep devonshire-budget
```

## Next Run
The script will automatically run tomorrow (Nov 19) at 9:00 AM with the correct data and updated budget calculations reflecting today's revenue-proportional budget changes.
