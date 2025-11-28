# Task Notes Server

Simple HTTP server that receives task notes from `tasks-overview.html` and saves them to a fixed location within PetesBrain.

## Why?

**Problem:** Browser downloads save to Downloads folder, but Claude reads from `/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json`. This caused confusion when processing task notes.

**Solution:** This server provides a fixed endpoint that the HTML can POST to, saving directly to the correct location.

---

## Quick Start

**Start the server:**
```bash
python3 ~/Documents/PetesBrain/shared/scripts/save-task-notes.py
```

**Keep it running** in a background terminal tab while using the task notes workflow.

---

## Usage

1. **Start server** (one terminal tab)
2. **Open** `tasks-overview.html` in browser
3. **Add notes** to tasks
4. **Click** "Process All Notes"
5. **Paste** "Process my task notes" into Claude Code

The server automatically saves to:
`/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json`

---

## Features

- **Fixed location:** No more Downloads folder confusion
- **Auto-creates directory:** Creates `data/state/` if it doesn't exist
- **CORS enabled:** Works from `file://` protocol (local HTML files)
- **Graceful fallback:** HTML falls back to download if server not running
- **Silent operation:** Only logs when notes are saved

---

## Optional: Auto-Start on Login

**Create LaunchAgent** (runs automatically on login):
```bash
# Create plist file
cat > ~/Library/LaunchAgents/com.petesbrain.task-notes-server.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.task-notes-server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/shared/scripts/save-task-notes.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-task-notes-server.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-task-notes-server.log</string>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.task-notes-server.plist
```

**Check if running:**
```bash
launchctl list | grep task-notes-server
```

**View logs:**
```bash
tail -f ~/.petesbrain-task-notes-server.log
```

---

## Troubleshooting

**Port already in use:**
- Change port in script: `run_server(port=8766)`
- Update HTML: `fetch('http://localhost:8766/save-notes'`

**Permissions error:**
```bash
chmod +x ~/Documents/PetesBrain/shared/scripts/save-task-notes.py
```

**Server not responding:**
- Check if running: `lsof -i :8765`
- Restart server
- Check firewall settings

---

## Technical Details

- **Port:** 8765 (configurable)
- **Endpoint:** POST to `http://localhost:8765/save-notes`
- **Content-Type:** `application/json`
- **Response:** `{ success: true, message: "...", file: "...", timestamp: "..." }`
