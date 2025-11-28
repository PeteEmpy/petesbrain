#!/bin/bash
#
# Rollout Label Tracking to All Clients
#
# This script coordinates the full rollout:
# 1. Fetches current labels via MCP for all enabled clients
# 2. Creates current-labels.json snapshots
# 3. Generates October 2025 baselines
#
# Run with: ./rollout_label_tracking.sh
#

echo ""
echo "======================================================================"
echo "LABEL TRACKING ROLLOUT - ALL CLIENTS"
echo "======================================================================"
echo ""

cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

echo "Step 1: Generating MCP queries for all enabled clients..."
python3 fetch_all_labels.py
echo ""

echo "======================================================================"
echo "⏸️  PAUSED FOR MCP EXECUTION"
echo "======================================================================"
echo ""
echo "Next: Ask Claude Code to execute the MCP queries in pending_label_queries.json"
echo ""
echo "After MCP execution, Claude Code will:"
echo "  1. Process all MCP responses"
echo "  2. Create current-labels.json for each client"
echo "  3. Generate October 2025 baselines"
echo "  4. Update todos and mark rollout complete"
echo ""
echo "======================================================================"
echo ""
