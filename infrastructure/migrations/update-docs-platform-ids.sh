#!/bin/bash
# Quick documentation update for platform-ids references

echo "🔍 Updating documentation to reference centralized platform-ids MCP server..."

# Update CLAUDE.md
sed -i.backup 's/mcp__google-ads__get_client_platform_ids/mcp__platform-ids__get_client_platform_ids/g' /Users/administrator/Documents/PetesBrain.nosync/.claude/CLAUDE.md

# Update slash commands
sed -i.backup 's/mcp__google-ads__get_client_platform_ids/mcp__platform-ids__get_client_platform_ids/g' /Users/administrator/Documents/PetesBrain.nosync/.claude/commands/weekly.md
sed -i.backup 's/mcp__google-ads__get_client_platform_ids/mcp__platform-ids__get_client_platform_ids/g' /Users/administrator/Documents/PetesBrain.nosync/.claude/commands/client.md

# Update skill documentation
find /Users/administrator/Documents/PetesBrain.nosync/.claude/skills -name "skill.md" -exec sed -i.backup 's/mcp__google-ads__get_client_platform_ids/mcp__platform-ids__get_client_platform_ids/g' {} \;

# Update tool documentation
find /Users/administrator/Documents/PetesBrain.nosync/tools -name "TOOL_CLAUDE.md" -exec sed -i.backup 's/mcp__google-ads__get_client_platform_ids/mcp__platform-ids__get_client_platform_ids/g' {} \;
find /Users/administrator/Documents/PetesBrain.nosync/tools -name "README.md" -exec sed -i.backup 's/mcp__google-ads__get_client_platform_ids/mcp__platform-ids__get_client_platform_ids/g' {} \;

echo "✅ Documentation updated!"
echo ""
echo "Backup files created with .backup extension"
echo "Review changes, then remove backups with: find . -name '*.backup' -delete"
