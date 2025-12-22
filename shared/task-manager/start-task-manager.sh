#!/bin/bash
#
# Task Manager Startup Script
#
# Single command to start the entire Task Manager system with validation.
# This script:
# 1. Validates configuration (safety checks)
# 2. Starts servers (if not already running)
# 3. Verifies servers are running
# 4. Opens Task Manager in browser
#
# Usage: ./start-task-manager.sh
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BOLD}${BLUE}🚀 Task Manager Startup${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: Validate configuration
echo -e "${BOLD}🔍 Step 1: Validating Configuration${NC}"
echo ""

if ! python3 validate.py; then
    EXIT_CODE=$?
    echo ""
    if [ $EXIT_CODE -eq 1 ]; then
        echo -e "${RED}${BOLD}❌ Validation failed - Task Manager cannot start safely${NC}"
        echo -e "${RED}Fix the critical issues above and try again${NC}"
        exit 1
    elif [ $EXIT_CODE -eq 2 ]; then
        echo -e "${YELLOW}${BOLD}⚠️  Warnings detected - proceeding with caution${NC}"
        echo ""
    fi
fi

echo ""
echo -e "${GREEN}✅ Validation passed${NC}"
echo ""

# Step 2: Start servers (if not already running)
echo -e "${BOLD}🌐 Step 2: Starting Servers${NC}"
echo ""

# Load LaunchAgents (they check PID files automatically)
echo "Loading Task Manager server..."
launchctl load ~/Library/LaunchAgents/com.petesbrain.task-manager-server.plist 2>/dev/null || true

echo "Loading Task Notes API server..."
launchctl load ~/Library/LaunchAgents/com.petesbrain.task-notes-server.plist 2>/dev/null || true

# Give servers time to start
echo "Waiting for servers to start..."
sleep 3

echo ""

# Step 3: Verify servers running
echo -e "${BOLD}🔍 Step 3: Verifying Servers${NC}"
echo ""

# Check port 8767 (Task Manager HTML)
if lsof -ti :8767 > /dev/null 2>&1; then
    PID_8767=$(lsof -ti :8767)
    echo -e "${GREEN}✅ Task Manager server running on port 8767 (PID $PID_8767)${NC}"
else
    echo -e "${RED}❌ Task Manager server not running on port 8767${NC}"
    echo -e "${RED}Check logs: tail -f ~/.petesbrain-task-manager-server-error.log${NC}"
    exit 1
fi

# Check port 5002 (Task Notes API)
if lsof -ti :5002 > /dev/null 2>&1; then
    PID_5002=$(lsof -ti :5002)
    echo -e "${GREEN}✅ Task Notes API running on port 5002 (PID $PID_5002)${NC}"
else
    echo -e "${RED}❌ Task Notes API not running on port 5002${NC}"
    echo -e "${RED}Check logs: tail -f ~/.petesbrain-task-notes-server-error.log${NC}"
    exit 1
fi

echo ""

# Step 4: Open Task Manager in browser
echo -e "${BOLD}🌐 Step 4: Opening Task Manager${NC}"
echo ""

open "http://localhost:8767/tasks-manager.html"

echo -e "${GREEN}✅ Task Manager started successfully${NC}"
echo ""

# Show server status
echo -e "${BOLD}Server Status:${NC}"
launchctl list | grep -E "task-manager-server|task-notes-server" | awk '{
    if ($2 == 0) {
        status = "\033[0;32m✅\033[0m"
    } else {
        status = "\033[0;31m❌\033[0m"
    }
    printf "  %s PID %s (exit code %s): %s\n", status, $1, $2, $3
}'

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${GREEN}✅ Task Manager Ready${NC}"
echo ""
echo -e "${BOLD}URLs:${NC}"
echo "  Task Manager: http://localhost:8767/tasks-manager.html"
echo "  Health Dashboard: http://localhost:8767/health-dashboard.html (Phase 3)"
echo ""
echo -e "${BOLD}Logs:${NC}"
echo "  Task Manager: tail -f ~/.petesbrain-task-manager-server.log"
echo "  Task Notes API: tail -f ~/.petesbrain-task-notes-server.log"
echo ""
echo -e "${BOLD}Stop Servers:${NC}"
echo "  launchctl unload ~/Library/LaunchAgents/com.petesbrain.task-manager-server.plist"
echo "  launchctl unload ~/Library/LaunchAgents/com.petesbrain.task-notes-server.plist"
echo ""
