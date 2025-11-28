# Bing Search MCP Server - Quick Start Guide

## Step 1: Get Your Bing API Key

1. **Go to [Azure Portal](https://portal.azure.com/)**
2. **Click "Create a resource"** (or use existing resource group)
3. **Search for "Bing Search v7"**
4. **Click "Create"** and fill in:
   - Name: `bing-search-mcp` (or any name)
   - Pricing tier: **F1 (Free)** - 1,000 queries/month, or **S1 (Standard)** - unlimited
   - Resource group: Create new or use existing
   - Region: Choose closest to you
5. **Click "Review + create" → "Create"**
6. **Once created, go to the resource → "Keys and Endpoint"**
7. **Copy "Key 1"** - this is your `BING_API_KEY`

## Step 2: Configure Environment

Create `.env` file in the server directory:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/bing-search-mcp-server
cp env.example .env
```

Edit `.env` and add your API key:

```bash
BING_API_KEY=your_actual_api_key_here
BING_API_ENDPOINT=https://api.bing.microsoft.com/v7.0
```

## Step 3: Add to Claude Desktop Config

The server is already set up in your `.mcp.json` file. Just restart Claude Desktop!

If you need to add it manually, edit `.mcp.json`:

```json
{
  "mcpServers": {
    "bing-search": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/bing-search-mcp-server/.venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/bing-search-mcp-server/server.py"
      ],
      "env": {
        "BING_API_KEY": "your_bing_api_key_here"
      }
    }
  }
}
```

## Step 4: Restart Claude Desktop

Close and restart Claude Desktop to load the new server.

## Step 5: Test It!

Try these commands in Claude:

```
"Search the web for 'Python web scraping best practices'"

"Find images of 'modern office design'"

"Search news for 'artificial intelligence developments'"

"What are the trending topics in the UK?"
```

## Usage Examples

### Web Search
- "Search for information about sustainable fashion brands"
- "Find the latest research on climate change"

### Image Search  
- "Search for product photography examples"
- "Find images of luxury hotels"

### News Search
- "What's the latest news about AI?"
- "Search news for 'UK economy' in the Business category"

### Video Search
- "Find tutorial videos about Python"
- "Search for cooking recipe videos"

### Trending Topics
- "What are trending topics right now?"
- "Show me trending topics in Business"

## Troubleshooting

**"Invalid API key" error:**
- Verify your API key in Azure Portal
- Check the `.env` file has the correct key
- Make sure there are no extra spaces

**"Rate limit exceeded":**
- Free tier: 1,000 queries/month
- Wait or upgrade to Standard tier

**Server not connecting:**
- Check `.mcp.json` has correct paths
- Restart Claude Desktop
- Check server logs for errors

