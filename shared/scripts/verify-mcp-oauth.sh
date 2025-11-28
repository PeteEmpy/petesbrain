#!/bin/bash
#
# MCP OAuth Token Verification Script
# Checks that all OAuth-based MCP servers have valid tokens and proper .mcp.json config
#

echo "========================================="
echo "MCP OAuth Token Verification"
echo "========================================="
echo ""

# Check Google Analytics
echo "=== Google Analytics ==="
if grep -q "GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH" .mcp.json; then
    echo "✅ OAuth config path set in .mcp.json"

    if [ -f "/Users/administrator/Downloads/google_analytics_token.json" ]; then
        echo "✅ Token file exists"
        expiry=$(cat /Users/administrator/Downloads/google_analytics_token.json | grep -o '"expiry":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$expiry" ]; then
            echo "   Expires: $expiry"
        fi
    else
        echo "⚠️  Token file missing (will be created on next startup)"
    fi
else
    echo "❌ GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH NOT SET in .mcp.json"
    echo "   This will cause OAuth popup on every startup!"
fi
echo ""

# Check Google Drive
echo "=== Google Drive ==="
if [ -f ~/.config/google-drive-mcp/tokens.json ]; then
    echo "✅ Token file exists"
    token_date=$(stat -f "%Sm" ~/.config/google-drive-mcp/tokens.json)
    echo "   Last modified: $token_date"
else
    echo "⚠️  Token file missing at ~/.config/google-drive-mcp/tokens.json"
fi
echo ""

# Check Google Tasks
echo "=== Google Tasks ==="
if [ -f infrastructure/mcp-servers/google-tasks-mcp-server/token.json ]; then
    echo "✅ Token file exists"
    token_date=$(stat -f "%Sm" infrastructure/mcp-servers/google-tasks-mcp-server/token.json)
    echo "   Last modified: $token_date"
else
    echo "⚠️  Token file missing"
fi
echo ""

# Check Google Photos
echo "=== Google Photos ==="
if [ -f infrastructure/mcp-servers/google-photos-mcp-server/token.json ]; then
    echo "✅ Token file exists"
    token_date=$(stat -f "%Sm" infrastructure/mcp-servers/google-photos-mcp-server/token.json)
    echo "   Last modified: $token_date"
else
    echo "⚠️  Token file missing"
fi
echo ""

echo "========================================="
echo "Summary"
echo "========================================="
echo "If you see any ❌ or ⚠️  above, you may experience OAuth popups."
echo "See docs/TROUBLESHOOTING.md for fixes."
echo ""
