#!/bin/bash
echo "Fixing all Python MCP servers..."
cd ~/Documents/PetesBrain/infrastructure/mcp-servers

for dir in google-ads-mcp-server google-analytics-mcp-server google-sheets-mcp-server google-tasks-mcp-server google-photos-mcp-server microsoft-ads-mcp-server facebook-ads-mcp-server; do
  echo "================================"
  echo "Fixing $dir..."
  cd "$dir"
  
  # Remove broken venv if exists
  rm -rf .venv
  
  # Create fresh venv
  /usr/local/bin/python3 -m venv .venv
  
  # Install dependencies
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
  
  # Test if python exists
  if [ -f ".venv/bin/python3" ]; then
    echo "✓ $dir venv created successfully"
  else
    echo "✗ $dir venv creation failed"
  fi
  
  cd ..
done

echo ""
echo "================================"
echo "Setup complete! Now testing servers..."
echo ""

# Test each server
for dir in google-trends-mcp-server google-ads-mcp-server google-analytics-mcp-server google-sheets-mcp-server google-tasks-mcp-server google-photos-mcp-server microsoft-ads-mcp-server facebook-ads-mcp-server; do
  cd "$dir"
  if [ -f ".venv/bin/python3" ]; then
    echo "Testing $dir..."
    timeout 2 .venv/bin/python3 server.py 2>&1 | head -5 || echo "  (Server started - normal for MCP)"
  fi
  cd ..
done

echo ""
echo "All done! Run 'claude mcp list' to verify."
