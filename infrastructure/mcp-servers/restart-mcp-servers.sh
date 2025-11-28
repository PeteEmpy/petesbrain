#!/bin/bash
# Restart MCP Servers
# Use this when MCP queries are failing in Claude Code

echo "===== Restarting MCP Servers ====="
echo ""

# Function to kill server processes
kill_mcp_processes() {
    echo "1. Killing existing MCP server processes..."

    # Kill Python-based MCP servers
    pkill -f "google-ads-mcp-server/server.py" 2>/dev/null
    pkill -f "google-analytics-mcp-server/server.py" 2>/dev/null
    pkill -f "google-sheets-mcp-server/server.py" 2>/dev/null
    pkill -f "google-tasks-mcp-server/server.py" 2>/dev/null
    pkill -f "facebook-ads-mcp-server/server.py" 2>/dev/null
    pkill -f "microsoft-ads-mcp-server/server.py" 2>/dev/null

    echo "   ✅ Killed stale processes"
    sleep 1
}

# Function to verify venvs
check_venvs() {
    echo ""
    echo "2. Checking virtual environments..."

    SERVERS=(
        "google-ads-mcp-server"
        "google-analytics-mcp-server"
        "google-sheets-mcp-server"
        "google-tasks-mcp-server"
    )

    for server in "${SERVERS[@]}"; do
        if [ -d "shared/mcp-servers/$server/.venv" ]; then
            echo "   ✅ $server venv exists"
        else
            echo "   ❌ $server venv MISSING"
        fi
    done
}

# Main execution
kill_mcp_processes
check_venvs

echo ""
echo "===== MCP Servers Reset ====="
echo ""
echo "Next steps:"
echo "  1. Close Claude Code completely (Cmd+Q)"
echo "  2. Wait 5 seconds"
echo "  3. Restart Claude Code"
echo "  4. Try your MCP query again"
echo ""
echo "If still failing:"
echo "  • Run health check: cd shared/mcp-servers/google-ads-mcp-server && ./health-check.sh"
echo "  • Check logs: ~/Library/Logs/Claude/mcp*.log"
