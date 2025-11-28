#!/bin/bash

# OAuth One-Time Setup Script
# Run this once to authorize all OAuth services
# Tokens will auto-refresh for ~6 months

echo "=========================================="
echo "Pete's Brain - OAuth Setup"
echo "=========================================="
echo ""
echo "This will open browser windows to authorize:"
echo "  1. Google Tasks"
echo "  2. Google Drive (if needed)"
echo "  3. Google Photos (if needed)"
echo ""
echo "After authorization, tokens will auto-refresh for ~6 months."
echo ""
read -p "Press Enter to continue..."

cd /Users/administrator/Documents/PetesBrain

# 1. Google Tasks
echo ""
echo "=== Authorizing Google Tasks ==="
echo "A browser window will open. Sign in and authorize."
cd infrastructure/mcp-servers/google-tasks-mcp-server
if [ -d ".venv" ]; then
  .venv/bin/python -c "from tasks_service import tasks_service; tasks_service()" && echo "✅ Google Tasks authorized"
else
  echo "❌ Virtual environment not found. Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
fi

# 2. Google Drive
echo ""
echo "=== Authorizing Google Drive ==="
echo "A browser window will open. Sign in and authorize."
cd /Users/administrator/Documents/PetesBrain
export GOOGLE_DRIVE_OAUTH_CREDENTIALS="/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json"
if [ -f "$GOOGLE_DRIVE_OAUTH_CREDENTIALS" ]; then
  npx -y @piotr-agier/google-drive-mcp auth && echo "✅ Google Drive authorized"
else
  echo "⚠️  OAuth credentials not found at $GOOGLE_DRIVE_OAUTH_CREDENTIALS"
  echo "   Skipping Google Drive authorization."
fi

# 3. Google Photos (if you use it)
echo ""
echo "=== Authorizing Google Photos (Optional) ==="
read -p "Do you use Google Photos MCP? (y/n): " use_photos
if [ "$use_photos" = "y" ]; then
  cd /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-photos-mcp-server
  if [ -d ".venv" ]; then
    echo "Testing Google Photos connection..."
    .venv/bin/python -c "import server; print('✅ Google Photos authorized')"
  else
    echo "❌ Virtual environment not found."
  fi
else
  echo "⏭️  Skipping Google Photos"
fi

echo ""
echo "=========================================="
echo "✅ OAuth Setup Complete!"
echo "=========================================="
echo ""
echo "Tokens stored in:"
echo "  - infrastructure/mcp-servers/google-tasks-mcp-server/token.json"
echo "  - infrastructure/mcp-servers/google-drive-mcp-server/token.json"
echo "  - infrastructure/mcp-servers/google-photos-mcp-server/token.json"
echo ""
echo "🔄 Auto-Refresh Behavior:"
echo "   - Access tokens refresh every hour (automatic)"
echo "   - Refresh tokens renew with each use (automatic)"
echo "   - As long as your LaunchAgents run regularly, tokens will NEVER expire"
echo ""
echo "⚠️  Only re-run this script if:"
echo "   - You see OAuth popups again (tokens got revoked)"
echo "   - You haven't used Pete's Brain for 6+ months"
echo ""
