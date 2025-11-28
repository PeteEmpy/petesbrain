#!/bin/bash
#
# Setup Weekly Label Validation Reports via LaunchAgent
#
# This script creates a LaunchAgent that sends weekly email reports
# every Monday at 9 AM with label validation and transition analysis
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_PATH="$HOME/Library/LaunchAgents/com.petesbrain.weekly-label-reports.plist"

echo "Setting up Weekly Label Validation Reports..."
echo

# Check if Python virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Error: Virtual environment not found at $SCRIPT_DIR/.venv"
    echo "Please run: cd $SCRIPT_DIR && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if GMAIL_APP_PASSWORD is set
if [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "⚠️  Warning: GMAIL_APP_PASSWORD environment variable not set"
    echo "Email sending will fail without this. Set it in ~/.bashrc or ~/.zshrc"
    echo
fi

# Create LaunchAgent plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.weekly-label-reports</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>source \$HOME/.bashrc 2>/dev/null || source \$HOME/.zshrc 2>/dev/null; ${SCRIPT_DIR}/.venv/bin/python3 ${SCRIPT_DIR}/label_validation_report.py --send-email</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>

    <key>StandardOutPath</key>
    <string>${HOME}/.petesbrain-weekly-label-reports.log</string>

    <key>StandardErrorPath</key>
    <string>${HOME}/.petesbrain-weekly-label-reports-error.log</string>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "✅ Created LaunchAgent plist at: $PLIST_PATH"
echo

# Load the LaunchAgent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ LaunchAgent loaded successfully"
echo
echo "Schedule: Every Monday at 9:00 AM"
echo "Logs: ~/.petesbrain-weekly-label-reports.log"
echo "Error log: ~/.petesbrain-weekly-label-reports-error.log"
echo
echo "Report includes:"
echo "  - Product changes (additions/removals)"
echo "  - Label distribution by segment"
echo "  - Label transitions detected"
echo "  - Performance highlights"
echo
echo "To check status:"
echo "  launchctl list | grep weekly-label-reports"
echo
echo "To test manually:"
echo "  cd $SCRIPT_DIR && .venv/bin/python3 label_validation_report.py"
echo
echo "To send test email:"
echo "  cd $SCRIPT_DIR && .venv/bin/python3 label_validation_report.py --send-email"
echo
echo "To unload:"
echo "  launchctl unload $PLIST_PATH"
echo
