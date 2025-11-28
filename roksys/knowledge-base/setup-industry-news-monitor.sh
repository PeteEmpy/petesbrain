#!/bin/bash

# Setup script for Industry News Monitor
# Configures automated RSS feed monitoring for Google Ads industry websites

set -e

echo "🚀 Setting up Industry News Monitor..."
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not found in environment"
    echo ""
    echo "Please add to your ~/.bashrc or ~/.zshrc:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Then run: source ~/.bashrc (or ~/.zshrc)"
    echo ""
    read -p "Press Enter if you've already set it and want to continue..."
fi

# Verify Python dependencies
echo "📦 Checking Python dependencies..."
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 -c "import feedparser, requests, anthropic" 2>/dev/null || {
    echo "Installing missing dependencies..."
    /Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/pip install -q feedparser requests anthropic
    echo "✓ Dependencies installed"
}

# Ensure inbox directory exists
echo "📁 Creating inbox directory..."
mkdir -p /Users/administrator/Documents/PetesBrain/roksys/knowledge-base/_inbox/documents
echo "✓ Inbox ready"

# Unload existing LaunchAgent if running
echo "🔄 Configuring LaunchAgent..."
launchctl unload ~/Library/LaunchAgents/com.petesbrain.industry-news.plist 2>/dev/null || true

# Copy LaunchAgent plist (should already exist from Write tool)
if [ ! -f ~/Library/LaunchAgents/com.petesbrain.industry-news.plist ]; then
    echo "❌ LaunchAgent plist not found. Please create it first."
    exit 1
fi

# Load LaunchAgent
launchctl load ~/Library/LaunchAgents/com.petesbrain.industry-news.plist
echo "✓ LaunchAgent loaded"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 The industry news monitor will now:"
echo "   - Check RSS feeds every 6 hours"
echo "   - Score articles for relevance (0-10)"
echo "   - Add relevant articles (score ≥6) to knowledge base inbox"
echo "   - Articles will be auto-processed by knowledge-base-processor.py"
echo ""
echo "📝 Logs: ~/.petesbrain-industry-news.log"
echo "📥 Inbox: roksys/knowledge-base/_inbox/documents/"
echo ""
echo "🧪 To test manually (don't wait 6 hours):"
echo "   shared/email-sync/.venv/bin/python3 shared/scripts/industry-news-monitor.py"
echo ""
echo "🔍 To check if it's running:"
echo "   launchctl list | grep industry-news"
echo ""
echo "📊 To view recent logs:"
echo "   tail -50 ~/.petesbrain-industry-news.log"
echo ""
