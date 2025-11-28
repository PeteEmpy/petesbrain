#!/bin/bash
cd ~/Documents/PetesBrain/infrastructure/mcp-servers
for dir in google-ads-mcp-server google-analytics-mcp-server google-sheets-mcp-server google-tasks-mcp-server google-photos-mcp-server microsoft-ads-mcp-server facebook-ads-mcp-server; do
  echo "Setting up $dir..."
  cd "$dir"
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
  cd ..
done
echo "All Python MCP servers setup complete!"
