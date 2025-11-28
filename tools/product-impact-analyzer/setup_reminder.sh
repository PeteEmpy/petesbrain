#!/bin/bash
#
# Setup Tuesday email reminder for Product Impact Analyzer
#
# This script creates a launchd job that sends you an email every Tuesday at 9:00 AM
# reminding you to run the product impact analysis.
#

set -e

echo "==================================================================="
echo "Product Impact Analyzer - Tuesday Reminder Setup"
echo "==================================================================="
echo

# Get user's email
read -p "Enter your email address: " USER_EMAIL

if [ -z "$USER_EMAIL" ]; then
    echo "Error: Email address required"
    exit 1
fi

echo
echo "Creating reminder script..."

# Create the reminder script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REMINDER_SCRIPT="$SCRIPT_DIR/send_reminder.sh"

cat > "$REMINDER_SCRIPT" << EOF
#!/bin/bash
#
# Send Tuesday reminder email
#

EMAIL="$USER_EMAIL"
SUBJECT="⏰ Tuesday Reminder: Run Product Impact Analysis"

BODY="Hi,

It's Tuesday! Time to run your weekly Product Impact Analysis.

HOW TO RUN:
1. Open Claude Code
2. Say: \"Run the product impact analysis\"
3. That's it! Claude will handle the rest.

WHAT YOU'LL GET:
- Summary of product changes from last week
- Impact on Google Ads Shopping performance
- Detailed report written to your Google Sheet

DOCUMENTATION:
$SCRIPT_DIR/README.md

Questions? Just ask Claude: \"How do I run the impact analyzer?\"

---
Automated reminder from Product Impact Analyzer
Last setup: $(date)
"

# Send email using macOS mail command
echo "\$BODY" | mail -s "\$SUBJECT" "\$EMAIL"

echo "[\$(date)] Reminder sent to \$EMAIL" >> "$SCRIPT_DIR/reminder.log"
EOF

chmod +x "$REMINDER_SCRIPT"

echo "✓ Reminder script created: $REMINDER_SCRIPT"
echo

# Create launchd plist
echo "Creating launchd schedule..."

PLIST_NAME="com.roksystems.product-impact-analyzer.reminder"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>

    <key>ProgramArguments</key>
    <array>
        <string>$REMINDER_SCRIPT</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>2</integer>  <!-- Tuesday = 2 (0=Sunday, 1=Monday, etc) -->
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/reminder.log</string>

    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/reminder_error.log</string>
</dict>
</plist>
EOF

echo "✓ Launchd plist created: $PLIST_PATH"
echo

# Load the launchd job
echo "Loading launchd job..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo "✓ Launchd job loaded"
echo

# Test the reminder (optional)
echo "==================================================================="
echo "Setup complete!"
echo "==================================================================="
echo
echo "You will now receive an email every Tuesday at 9:00 AM at:"
echo "  $USER_EMAIL"
echo
echo "The email will remind you to run: \"Run the product impact analysis\""
echo
echo "COMMANDS:"
echo "  Test reminder now:  $REMINDER_SCRIPT"
echo "  View logs:          tail -f $SCRIPT_DIR/reminder.log"
echo "  Disable reminder:   launchctl unload $PLIST_PATH"
echo "  Re-enable reminder: launchctl load $PLIST_PATH"
echo
read -p "Send a test reminder now? (y/n): " TEST_NOW

if [[ "$TEST_NOW" == "y" || "$TEST_NOW" == "Y" ]]; then
    echo
    echo "Sending test email..."
    "$REMINDER_SCRIPT"
    echo "✓ Test email sent! Check your inbox at $USER_EMAIL"
fi

echo
echo "Done! 🎉"
