#!/bin/bash
# Setup script for Knowledge Base Inbox automation

echo "═══════════════════════════════════════════════════════════"
echo "  Knowledge Base Inbox Automation Setup"
echo "═══════════════════════════════════════════════════════════"
echo

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY is not set in your environment"
    echo
    echo "Please add this to your ~/.bashrc or ~/.zshrc:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo
    read -p "Enter your Anthropic API key now (or press Enter to skip): " api_key

    if [ -n "$api_key" ]; then
        # Update the plist file
        sed -i '' "s/YOUR_API_KEY_HERE/$api_key/" ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist
        echo "✓ API key added to LaunchAgent"
    else
        echo "⚠️  You'll need to manually edit ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist"
        echo "   Replace YOUR_API_KEY_HERE with your actual API key"
    fi
else
    # Update the plist file with the existing API key
    sed -i '' "s/YOUR_API_KEY_HERE/$ANTHROPIC_API_KEY/" ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist
    echo "✓ Using ANTHROPIC_API_KEY from environment"
fi

echo
echo "Loading LaunchAgent..."

# Unload if already loaded
launchctl unload ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist 2>/dev/null

# Load the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist

if [ $? -eq 0 ]; then
    echo "✓ LaunchAgent loaded successfully"
else
    echo "✗ Failed to load LaunchAgent"
    exit 1
fi

echo
echo "═══════════════════════════════════════════════════════════"
echo "  Setup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo
echo "The knowledge base processor will now run every 6 hours."
echo
echo "To check status:"
echo "  launchctl list | grep knowledge-base"
echo
echo "To view logs:"
echo "  tail -f ~/.petesbrain-knowledge-base.log"
echo
echo "To test immediately:"
echo "  cd /Users/administrator/Documents/PetesBrain"
echo "  shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-processor.py"
echo
echo "Inbox location:"
echo "  /Users/administrator/Documents/PetesBrain/roksys/knowledge-base/_inbox/"
echo
echo "Drop files into _inbox/emails/, _inbox/documents/, or _inbox/videos/"
echo "They'll be automatically processed and organized."
echo
