#!/bin/bash
# Quick wrapper to show today's changes for Tree2mydoor
# Uses the MCP Google Ads tools via Claude Code

CUSTOMER_ID="4941701449"
TODAY=$(date +%Y-%m-%d)

echo "Querying Google Ads changes for $CUSTOMER_ID on $TODAY..."
echo ""

# You would run this within Claude Code environment to access MCP tools
# Or use the Python implementation that calls the MCP server directly
python3 << EOF
# This would need to be adapted to call MCP tools
# For now, this script serves as documentation

print("Use the query_google_ads_changes.py script with MCP tools available")
print("Or query directly via Claude Code with:")
print("")
print("mcp__google-ads__run_gaql with query:")
print("SELECT change_event.change_date_time, change_event.resource_change_operation,")
print("       change_event.user_email, change_event.change_resource_name")
print("FROM change_event")
print("WHERE change_event.change_date_time >= '$TODAY 00:00:00'")
print("AND change_event.change_date_time <= '$TODAY 23:59:59'")
print("ORDER BY change_event.change_date_time DESC")
EOF
