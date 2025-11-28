#!/bin/bash
echo "Adding all MCP servers to Claude Code..."

claude mcp add -s user google-ads "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/server.py"

claude mcp add -s user google-analytics "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/server.py"

claude mcp add -s user google-sheets "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/server.py"

claude mcp add -s user google-tasks "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server/server.py"

claude mcp add -s user google-trends "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-trends-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-trends-mcp-server/server.py"

claude mcp add -s user google-photos "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-photos-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-photos-mcp-server/server.py"

claude mcp add -s user microsoft-ads "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/microsoft-ads-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/microsoft-ads-mcp-server/server.py"

claude mcp add -s user facebook-ads "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/facebook-ads-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/facebook-ads-mcp-server/server.py"

claude mcp add -s user woocommerce-godshot "node" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/woocommerce-mcp-server-opestro/index.js"

claude mcp add -s user woocommerce-crowdcontrol "node" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/woocommerce-mcp-server-opestro/index.js"

claude mcp add -s user google-drive "npx" "-y" "@piotr-agier/google-drive-mcp"

echo "All MCP servers added!"
