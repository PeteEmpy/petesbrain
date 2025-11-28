#!/bin/bash
#
# Install Granola Sync Daemon as macOS LaunchAgent
# This makes the daemon start automatically when you log in
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_NAME="com.petesbrain.granola-importer"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python3"
LOG_FILE="$HOME/.petesbrain-granola-importer.log"

echo "=================================================="
echo "Granola Sync Daemon - Service Installer"
echo "=================================================="
echo ""

# Check if venv exists, create if not
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "✓ Virtual environment created"
fi

# Check if python3 is available in venv
if [ ! -x "$PYTHON_PATH" ]; then
    echo "❌ Error: Virtual environment python not found"
    echo "Please run: python3 -m venv $SCRIPT_DIR/venv"
    exit 1
fi

echo "✓ Found Python 3: $PYTHON_PATH"

# Check if dependencies are installed
cd "$SCRIPT_DIR"
if ! "$PYTHON_PATH" -c "import requests" 2>/dev/null; then
    echo ""
    echo "⚠️  Dependencies not installed"
    echo "Installing dependencies from requirements.txt..."
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi

echo "✓ Dependencies installed"

# Create LaunchAgent directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Create plist file
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${SCRIPT_DIR}/sync_daemon.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>${LOG_FILE}</string>

    <key>StandardErrorPath</key>
    <string>${LOG_FILE}</string>

    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>
</dict>
</plist>
EOF

echo "✓ Created LaunchAgent: $PLIST_FILE"

# Load the service
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

echo "✓ Service loaded and started"
echo ""
echo "=================================================="
echo "Installation Complete!"
echo "=================================================="
echo ""
echo "The Granola sync daemon is now running and will:"
echo "  • Check for new meetings every 5 minutes"
echo "  • Start automatically when you log in"
echo "  • Log activity to: $LOG_FILE"
echo ""
echo "Useful commands:"
echo "  View logs:    tail -f $LOG_FILE"
echo "  Stop service: launchctl stop ${PLIST_NAME}"
echo "  Start service: launchctl start ${PLIST_NAME}"
echo "  Uninstall:    ./uninstall_service.sh"
echo ""
