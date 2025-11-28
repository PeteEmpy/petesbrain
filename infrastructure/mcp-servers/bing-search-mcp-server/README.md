# Bing Search API MCP Server 🔍

**A FastMCP-powered Model Context Protocol server for Bing Search API integration**

**Note:** This is for Bing Search API (web search, images, news, videos). For Microsoft Advertising/Bing Ads campaign management, use the `microsoft-ads-mcp-server` instead.

Connect Bing Search API directly to Claude Desktop and other MCP clients for web search, image search, news search, video search, and trending topics.

## ✨ Features

- 🔍 **Web Search** - Search the web with customizable results
- 🖼️ **Image Search** - Find images with filters (size, color, type, license)
- 📰 **News Search** - Search news articles by category and date
- 🎥 **Video Search** - Find videos with resolution and length filters
- 📈 **Trending Topics** - Get trending topics by market and category
- 🚀 **FastMCP Framework** - Built on the modern MCP standard
- 🖥️ **Claude Desktop Ready** - Direct integration with Claude Desktop

## 📋 Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `web_search` | Search the web | `query`, `count`, `offset`, `market`, `safe_search` |
| `image_search` | Search for images | `query`, `count`, `image_type`, `size`, `color`, `license` |
| `news_search` | Search news articles | `query`, `count`, `category`, `sort_by` |
| `video_search` | Search for videos | `query`, `count`, `resolution`, `video_length`, `pricing` |
| `trending_topics` | Get trending topics | `market`, `category`, `count` |

## 🚀 Quick Start

### Prerequisites

Before setting up the MCP server, you'll need:
- Python 3.10+ installed
- A Microsoft Azure account
- Bing Search API subscription

## 🔧 Step 1: Azure Portal Setup

### 1.1 Create Bing Search Resource

1. **Go to [Azure Portal](https://portal.azure.com/)**
2. **Click "Create a resource"**
3. **Search for "Bing Search v7"**
4. **Click "Create"**
5. **Configure:**
   - Subscription: Your Azure subscription
   - Resource group: Create new or use existing
   - Name: e.g., "bing-search-mcp"
   - Pricing tier: Choose F1 (Free) or S1 (Standard)
   - Region: Choose your preferred region
6. **Click "Review + create" then "Create"**

### 1.2 Get API Key

1. **Once the resource is created, go to the resource**
2. **Navigate to "Keys and Endpoint"**
3. **Copy Key 1** - this is your `BING_API_KEY`
   - ⚠️ **Important:** Keep this key secure!

### 1.3 Note the Endpoint

The endpoint is typically:
```
https://api.bing.microsoft.com/v7.0
```

## 🔧 Step 2: Installation & Setup

### 2.1 Install Dependencies

```bash
cd shared/mcp-servers/bing-search-mcp-server

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Environment Configuration

Create a `.env` file:

```bash
cp env.example .env
```

Edit `.env` with your credentials:

```bash
BING_API_KEY=your_bing_api_key_here
BING_API_ENDPOINT=https://api.bing.microsoft.com/v7.0
```

## 🖥️ Step 3: Claude Desktop Integration

### 3.1 Add to .mcp.json

Edit `/Users/administrator/Documents/PetesBrain/.mcp.json` and add:

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

**Important:** 
- Use **absolute paths** for all file locations
- Replace placeholder values with your actual API key
- Consider using environment variables instead of hardcoding secrets

### 3.2 Restart Claude Desktop

Close and restart Claude Desktop to load the new configuration.

## 📖 Usage Examples

### Web Search

```
"Search the web for 'Python web scraping best practices'"

"Find information about 'sustainable fashion brands UK'"
```

### Image Search

```
"Search for images of 'modern office design'"

"Find 'product photography examples' with size Large and color ColorOnly"
```

### News Search

```
"Search news for 'artificial intelligence developments'"

"Find latest news about 'climate change' in the ScienceAndTechnology category"
```

### Video Search

```
"Search for videos about 'Python tutorials'"

"Find 'cooking recipes' videos with resolution 720p and length Medium"
```

### Trending Topics

```
"What are the trending topics in the UK?"

"Show me trending topics in the Business category"
```

## 🛠️ Tool Parameters

### Web Search Parameters

- `query` (required): Search query string
- `count` (optional, default: 10): Number of results (1-50)
- `offset` (optional, default: 0): Number of results to skip
- `market` (optional, default: "en-US"): Market code (e.g., 'en-GB', 'fr-FR')
- `safe_search` (optional, default: "Moderate"): 'Off', 'Moderate', or 'Strict'

### Image Search Parameters

- `query` (required): Search query string
- `count` (optional, default: 20): Number of results (1-150)
- `image_type` (optional): 'AnimatedGif', 'Clipart', 'Line', 'Photo', 'Shopping', 'Transparent'
- `size` (optional): 'Small', 'Medium', 'Large', 'Wallpaper', 'All'
- `color` (optional): 'ColorOnly', 'Monochrome', 'Black', 'Blue', 'Red', etc.
- `license` (optional): 'Public', 'Share', 'ShareCommercially', 'Modify', 'ModifyCommercially', 'All'

### News Search Parameters

- `query` (required): Search query string
- `count` (optional, default: 10): Number of results (1-100)
- `category` (optional): 'Business', 'Entertainment', 'Health', 'Politics', 'ScienceAndTechnology', 'Sports', 'US', 'World'
- `sort_by` (optional): 'Date' (newest first) or 'Relevance' (most relevant)

### Video Search Parameters

- `query` (required): Search query string
- `count` (optional, default: 20): Number of results (1-105)
- `resolution` (optional): 'All', '480p', '720p', '1080p'
- `video_length` (optional): 'All', 'Short' (< 5 min), 'Medium' (5-20 min), 'Long' (> 20 min)
- `pricing` (optional): 'All', 'Free', 'Paid'

### Trending Topics Parameters

- `market` (optional, default: "en-US"): Market code
- `category` (optional): Category filter
- `count` (optional, default: 10): Number of topics (1-20)

## 🛠️ Troubleshooting

### Authentication Issues

| Issue | Solution |
|-------|----------|
| **Invalid API key** | Verify key in Azure Portal → Keys and Endpoint |
| **401 Unauthorized** | Check API key is correct and active |
| **403 Forbidden** | Verify Bing Search API subscription is active |

### API Issues

| Issue | Solution |
|-------|----------|
| **Rate limit exceeded** | Wait and retry, or upgrade to Standard tier |
| **Invalid market code** | Use valid market codes (e.g., 'en-US', 'en-GB') |
| **Invalid parameter** | Check parameter values match allowed options |

### Configuration Issues

| Issue | Solution |
|-------|----------|
| **Environment variables not set** | Check `.env` file and Claude config `env` section |
| **Module import errors** | Run `pip install -r requirements.txt` |
| **Python path issues** | Use absolute path to Python executable |

## 📊 API Limits

Bing Search API has rate limits:
- **Free Tier (F1):** 3 queries per second, 1,000 queries per month
- **Standard Tier (S1):** 3 queries per second, unlimited queries

Implement caching and rate limiting as needed.

## 🔒 Security Best Practices

- ✅ **Never commit `.env` file** to version control
- ✅ **Use environment variables** in production
- ✅ **Rotate API keys** periodically
- ✅ **Set secure file permissions:** `chmod 600 .env`
- ✅ **Monitor API usage** in Azure Portal

## 📄 Market Codes

Common market codes:
- `en-US` - United States (English)
- `en-GB` - United Kingdom (English)
- `en-AU` - Australia (English)
- `fr-FR` - France (French)
- `de-DE` - Germany (German)
- `es-ES` - Spain (Spanish)
- `it-IT` - Italy (Italian)
- `ja-JP` - Japan (Japanese)
- `zh-CN` - China (Simplified Chinese)

See [Bing API Documentation](https://learn.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-web-api-v7-reference#market-codes) for full list.

## 📄 License

This project follows the same license as other PetesBrain MCP servers.

---

**Made for PetesBrain**

*Connect Bing Search API directly to AI assistants and unlock powerful web search capabilities.*

