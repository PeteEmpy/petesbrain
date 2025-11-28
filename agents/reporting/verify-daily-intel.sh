#!/bin/bash
# Daily Intel Report - Quick Status Check
# Run this anytime to verify the system is working

echo "========================================="
echo "Daily Intel Report - Status Check"
echo "========================================="
echo ""

# Check 1: LaunchAgent loaded
echo "1. LaunchAgent Status:"
if launchctl list | grep -q "daily-intel-report"; then
    echo "   ✅ LOADED (will run daily at 7:00 AM)"
else
    echo "   ❌ NOT LOADED"
    echo "   Fix: launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-intel-report.plist"
fi
echo ""

# Check 2: Script file exists
echo "2. Script File:"
if [ -f "/Users/administrator/Documents/PetesBrain/agents/reporting/daily-intel-report.py" ]; then
    SCRIPT_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" /Users/administrator/Documents/PetesBrain/agents/reporting/daily-intel-report.py)
    echo "   ✅ EXISTS (modified: $SCRIPT_DATE)"
else
    echo "   ❌ MISSING"
fi
echo ""

# Check 3: LaunchAgent config
echo "3. LaunchAgent Config:"
if [ -f "$HOME/Library/LaunchAgents/com.petesbrain.daily-intel-report.plist" ]; then
    PLIST_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" ~/Library/LaunchAgents/com.petesbrain.daily-intel-report.plist)
    echo "   ✅ EXISTS (modified: $PLIST_DATE)"
else
    echo "   ❌ MISSING"
fi
echo ""

# Check 4: Today's briefing
echo "4. Today's Briefing:"
TODAY=$(date +%Y-%m-%d)
if [ -f "/Users/administrator/Documents/PetesBrain/briefing/${TODAY}-briefing.md" ]; then
    MD_SIZE=$(ls -lh "/Users/administrator/Documents/PetesBrain/briefing/${TODAY}-briefing.md" | awk '{print $5}')
    HTML_SIZE=$(ls -lh "/Users/administrator/Documents/PetesBrain/briefing/${TODAY}-briefing.html" | awk '{print $5}')
    echo "   ✅ GENERATED"
    echo "   - Markdown: ${MD_SIZE}"
    echo "   - HTML: ${HTML_SIZE}"
else
    echo "   ⏳ NOT YET GENERATED (runs at 7:00 AM)"
fi
echo ""

# Check 5: Recent logs
echo "5. Recent Activity:"
if [ -f "$HOME/.petesbrain-daily-intel-report.log" ]; then
    LAST_RUN=$(tail -1 ~/.petesbrain-daily-intel-report.log 2>/dev/null)
    if [ -n "$LAST_RUN" ]; then
        echo "   Last log entry: $LAST_RUN"
    else
        echo "   No recent activity"
    fi
else
    echo "   No log file found"
fi
echo ""

# Check 6: Python environment
echo "6. Python Environment:"
PYTHON_PATH="/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3"
if [ -f "$PYTHON_PATH" ]; then
    echo "   ✅ Virtual environment exists"
    # Check for required modules
    if $PYTHON_PATH -c "import anthropic, markdown" 2>/dev/null; then
        echo "   ✅ Required modules installed (anthropic, markdown)"
    else
        echo "   ⚠️ Missing required modules"
        echo "   Fix: $PYTHON_PATH -m pip install anthropic markdown"
    fi
else
    echo "   ❌ Virtual environment missing"
fi
echo ""

# Summary
echo "========================================="
echo "Summary:"
echo "========================================="

ISSUES=0

if ! launchctl list | grep -q "daily-intel-report"; then
    ISSUES=$((ISSUES + 1))
fi

if [ ! -f "/Users/administrator/Documents/PetesBrain/agents/reporting/daily-intel-report.py" ]; then
    ISSUES=$((ISSUES + 1))
fi

if [ ! -f "$PYTHON_PATH" ]; then
    ISSUES=$((ISSUES + 1))
fi

if [ $ISSUES -eq 0 ]; then
    echo "✅ ALL SYSTEMS OPERATIONAL"
    echo ""
    echo "Next briefing will be generated:"
    echo "   Tomorrow at 7:00 AM"
    echo ""
    echo "You will receive an email at:"
    echo "   petere@roksys.co.uk"
else
    echo "⚠️ $ISSUES ISSUE(S) FOUND"
    echo ""
    echo "See details above for how to fix."
fi

echo ""
echo "========================================="
