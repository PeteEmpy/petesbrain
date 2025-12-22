#!/bin/bash
#
# Setup Improved Daily Briefing System
#
# This script:
# 1. Re-authenticates Google OAuth with Calendar + Tasks scopes
# 2. Tests the client work generator
# 3. Generates a test briefing to verify everything works
#

set -e  # Exit on error

echo "========================================================================"
echo "SETUP IMPROVED DAILY BRIEFING SYSTEM"
echo "========================================================================"
echo ""

cd /Users/administrator/Documents/PetesBrain

echo "Step 1: Re-authenticate Google OAuth with expanded scopes"
echo "------------------------------------------------------------------------"
echo ""
echo "This will:"
echo "  ✓ Add Google Calendar read access"
echo "  ✓ Add Google Tasks read/write access"
echo "  ✓ Add Gmail read access (for future use)"
echo ""
echo "A browser window will open for authentication."
echo "Press ENTER to continue, or Ctrl+C to cancel..."
read

/usr/local/bin/python3 shared/scripts/reauth-google-oauth.py

echo ""
echo "✅ OAuth re-authentication complete!"
echo ""

echo "Step 2: Test the client work generator"
echo "------------------------------------------------------------------------"
echo ""
echo "This will analyze all 12+ clients and generate today's work list..."
echo ""

ANTHROPIC_API_KEY="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" \
/usr/local/bin/python3 shared/scripts/daily-client-work-generator.py

echo ""
echo "✅ Client work generator test complete!"
echo ""

echo "Step 3: Generate test daily briefing"
echo "------------------------------------------------------------------------"
echo ""
echo "This will generate today's full briefing with:"
echo "  ✓ Calendar events"
echo "  ✓ Client work for all clients"
echo "  ✓ Google Tasks"
echo "  ✓ Performance alerts"
echo "  ✓ AI-generated summary"
echo ""

ANTHROPIC_API_KEY="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" \
GMAIL_USER="petere@roksys.co.uk" \
GMAIL_APP_PASSWORD="pxmsoxiwuazkqhvg" \
/usr/local/bin/python3 agents/reporting/daily-briefing.py

echo ""
echo "========================================================================"
echo "✅ SETUP COMPLETE!"
echo "========================================================================"
echo ""
echo "Your improved daily briefing is now configured!"
echo ""
echo "Next steps:"
echo "  1. Check your email for today's briefing"
echo "  2. Review the briefing file in briefing/$(date +%Y-%m-%d)-briefing.md"
echo "  3. The system will run automatically every morning at 7:00 AM"
echo ""
echo "What's new:"
echo "  ✅ Calendar events now showing correctly"
echo "  ✅ AI-generated client work for ALL clients (not just those with meetings)"
echo "  ✅ Intelligent task prioritization (P0/P1/P2)"
echo "  ✅ Time estimates for each task"
echo "  ✅ Reasons why each task is needed today"
echo ""
