#!/bin/bash

# Sync Google Ads MCP credentials to laptop

echo "Syncing Google Ads MCP server credentials to laptop..."

# Copy credentials file
scp /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json \
    administrator@Peters-MacBook-15.local:/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json

# Copy .env file
scp /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env \
    administrator@Peters-MacBook-15.local:/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env

echo "✅ Credentials synced successfully"
echo ""
echo "Note: You may need to restart Claude Code on the laptop to pick up the new credentials."
