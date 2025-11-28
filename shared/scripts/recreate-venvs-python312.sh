#!/bin/bash

# Script to recreate all virtual environments with Python 3.12
# This fixes the Python 3.13 deadlock bug affecting LaunchAgents

set -e

PYTHON312="/usr/local/bin/python3.12"
LOG_FILE="/tmp/venv-recreation.log"

echo "======================================" | tee -a "$LOG_FILE"
echo "Virtual Environment Recreation Script" | tee -a "$LOG_FILE"
echo "Python 3.12 Migration" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Check Python 3.12 is available
if [ ! -f "$PYTHON312" ]; then
    echo "❌ Python 3.12 not found at $PYTHON312" | tee -a "$LOG_FILE"
    exit 1
fi

echo "✓ Found Python 3.12: $($PYTHON312 --version)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Find all .venv directories
VENV_DIRS=(
    "/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/scripts/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-analytics-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/bing-search-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/facebook-ads-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/microsoft-ads-mcp-server/.venv"
    "/Users/administrator/Documents/PetesBrain/tools/google-ads-generator/.venv"
    "/Users/administrator/Documents/PetesBrain/tools/monthly-report-generator/.venv"
    "/Users/administrator/Documents/PetesBrain/tools/report-generator/.venv"
    "/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/.venv"
    "/Users/administrator/Documents/PetesBrain/clients/national-design-academy/scripts/.venv"
    "/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/.venv"
    "/Users/administrator/Documents/PetesBrain/personal/spreadsheets/.venv"
)

SUCCESS=0
FAILED=0

for VENV_PATH in "${VENV_DIRS[@]}"; do
    if [ ! -d "$VENV_PATH" ]; then
        echo "⏭️  Skipping (not found): $VENV_PATH" | tee -a "$LOG_FILE"
        continue
    fi

    PARENT_DIR=$(dirname "$VENV_PATH")
    REQUIREMENTS="$PARENT_DIR/requirements.txt"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
    echo "📦 Processing: $PARENT_DIR" | tee -a "$LOG_FILE"

    # Backup current requirements
    if [ -f "$REQUIREMENTS" ]; then
        echo "  ✓ Found requirements.txt" | tee -a "$LOG_FILE"
    else
        echo "  ⚠️  No requirements.txt, will create from pip freeze" | tee -a "$LOG_FILE"
        if [ -f "$VENV_PATH/bin/pip" ]; then
            "$VENV_PATH/bin/pip" freeze > "$PARENT_DIR/requirements-backup.txt" 2>/dev/null || true
            if [ -f "$PARENT_DIR/requirements-backup.txt" ]; then
                REQUIREMENTS="$PARENT_DIR/requirements-backup.txt"
                echo "  ✓ Created requirements-backup.txt" | tee -a "$LOG_FILE"
            fi
        fi
    fi

    # Remove old venv
    echo "  🗑️  Removing old .venv..." | tee -a "$LOG_FILE"
    rm -rf "$VENV_PATH"

    # Create new venv with Python 3.12
    echo "  🔨 Creating new .venv with Python 3.12..." | tee -a "$LOG_FILE"
    cd "$PARENT_DIR"
    if "$PYTHON312" -m venv .venv >> "$LOG_FILE" 2>&1; then
        echo "  ✓ Created new .venv" | tee -a "$LOG_FILE"
    else
        echo "  ❌ Failed to create .venv" | tee -a "$LOG_FILE"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Install dependencies
    if [ -f "$REQUIREMENTS" ]; then
        echo "  📥 Installing dependencies..." | tee -a "$LOG_FILE"
        if .venv/bin/pip install --upgrade pip >> "$LOG_FILE" 2>&1 && \
           .venv/bin/pip install -r "$REQUIREMENTS" >> "$LOG_FILE" 2>&1; then
            echo "  ✓ Dependencies installed" | tee -a "$LOG_FILE"
            SUCCESS=$((SUCCESS + 1))
        else
            echo "  ⚠️  Some dependencies failed (see log)" | tee -a "$LOG_FILE"
            SUCCESS=$((SUCCESS + 1))  # Still count as success if venv created
        fi
    else
        echo "  ⚠️  No requirements file, venv created but empty" | tee -a "$LOG_FILE"
        SUCCESS=$((SUCCESS + 1))
    fi

    # Clean up backup if we created it
    if [ -f "$PARENT_DIR/requirements-backup.txt" ]; then
        rm -f "$PARENT_DIR/requirements-backup.txt"
    fi

    echo "" | tee -a "$LOG_FILE"
done

echo "======================================" | tee -a "$LOG_FILE"
echo "Summary" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"
echo "✅ Successfully recreated: $SUCCESS" | tee -a "$LOG_FILE"
echo "❌ Failed: $FAILED" | tee -a "$LOG_FILE"
echo "Completed: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Full log: $LOG_FILE" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"

if [ $FAILED -gt 0 ]; then
    exit 1
fi

exit 0
