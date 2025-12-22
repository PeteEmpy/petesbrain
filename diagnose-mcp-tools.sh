#!/bin/bash
# MCP Tool Diagnostics Script
# Run this in your other Claude Code terminal to diagnose the issue

echo "=== MCP Tool Diagnostics ==="
echo ""

echo "1. Current Working Directory:"
pwd
echo ""

echo "2. Google Drive MCP Server Status:"
claude mcp list | grep -A 1 "google-drive" || echo "   ❌ NOT FOUND in MCP list"
echo ""

echo "3. All Google-related MCP Servers:"
claude mcp list | grep "google-"
echo ""

echo "4. Project .mcp.json exists?"
if [ -f "/Users/administrator/Documents/PetesBrain.nosync/.mcp.json" ]; then
    echo "   ✅ YES"
    echo "   Google Drive entry:"
    grep -A 8 '"google-drive"' /Users/administrator/Documents/PetesBrain.nosync/.mcp.json
else
    echo "   ❌ NO"
fi
echo ""

echo "5. Google Drive server processes running:"
ps aux | grep "google-drive-mcp-server-custom/server.py" | grep -v grep | wc -l | xargs echo "   Processes:"
echo ""

echo "6. Test direct tool call:"
echo "   Try this in Claude: 'Use mcp__google-drive__search to find files with budget in the name'"
echo ""

echo "=== End Diagnostics ==="
