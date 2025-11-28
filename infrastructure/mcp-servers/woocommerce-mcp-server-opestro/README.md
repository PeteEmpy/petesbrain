# WooCommerce MCP Server

A Model Context Protocol (MCP) server for integrating WooCommerce with Claude and other AI assistants.

## Overview

This server provides tools for AI assistants to interact with a WooCommerce store, allowing them to:

- Fetch recent orders with optional filtering
- Retrieve detailed information about specific orders by ID

The server implements the [Model Context Protocol](https://modelcontextprotocol.io/) specification, making it compatible with MCP-enabled AI assistants like Claude for Desktop.

## Prerequisites

- Node.js v18 or higher
- A WooCommerce store with REST API access
- WooCommerce API credentials (consumer key and secret)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/techspawn/woocommerce-mcp-server.git
cd woocommerce-mcp-server
```

2. Install dependencies:

```bash
npm install
```

## Configuration

You need to configure your WooCommerce API credentials. You can do this by:

1. Setting environment variables when running the server:

```bash
WOOCOMMERCE_URL=https://your-store.com \
WOOCOMMERCE_CONSUMER_KEY=your-consumer-key \
WOOCOMMERCE_CONSUMER_SECRET=your-consumer-secret \
node index.js
```

2. Or by editing the default values in the `index.js` file:

```javascript
const woocommerceConfig = {
  url: process.env.WOOCOMMERCE_URL || 'https://your-store.com',
  consumerKey: process.env.WOOCOMMERCE_CONSUMER_KEY || 'your-consumer-key',
  consumerSecret: process.env.WOOCOMMERCE_CONSUMER_SECRET || 'your-consumer-secret',
  version: 'wc/v3'
};
```

## Running the Server

To run the server directly:

```bash
node index.js
```

Or using the npm script:

```bash
npm start
```

## Integration with Claude for Desktop

To connect this server to Claude for Desktop:

1. Make sure you have [Claude for Desktop](https://claude.ai/desktop) installed
2. Open your Claude Desktop configuration file located at:
   - Windows: `%USERPROFILE%\AppData\Roaming\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

3. Add your WooCommerce MCP server configuration (create the file if it doesn't exist):

```json
{
  "mcpServers": {
    "woocommerce": {
      "command": "node",
      "args": [
        "/ABSOLUTE/PATH/TO/woocommerce-mcp-server/index.js"
      ],
      "env": {
        "WOOCOMMERCE_URL": "https://your-store.com",
        "WOOCOMMERCE_CONSUMER_KEY": "your-consumer-key",
        "WOOCOMMERCE_CONSUMER_SECRET": "your-consumer-secret"
      }
    }
  }
}
```

4. Save the file and restart Claude for Desktop

## Available Tools

### `getRecentOrders`

Fetches a list of recent orders from your WooCommerce store.

Parameters:
- `status` (optional): Filter orders by status (e.g., "processing", "completed", "on-hold")
- `limit` (optional, default: 5): Number of orders to return

### `getOrderById`

Retrieves detailed information about a specific order.

Parameters:
- `id`: The order ID to retrieve

## Building Your Own MCP Server with JavaScript

This section provides a guide to creating your own MCP server using JavaScript/Node.js.

### 1. Set up a new project

```bash
mkdir my-mcp-server
cd my-mcp-server
npm init -y
```

### 2. Install dependencies

```bash
npm install @modelcontextprotocol/sdk axios zod
```

### 3. Create your server file (index.js)

Start with the basic structure:

```javascript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Initialize server
const server = new McpServer({
  name: "My MCP Service",
  version: "1.0.0",
});

// Define and register your tools
server.tool(
  "myToolName",
  {
    // Define parameters using Zod schemas
    param1: z.string().describe("Description of param1"),
    param2: z.number().optional().describe("Optional parameter")
  },
  async ({ param1, param2 }) => {
    // Tool implementation logic here
    const result = `Processed ${param1} with value ${param2 || 'none'}`;
    
    // Return result in the expected format
    return {
      content: [
        {
          type: "text",
          text: result
        }
      ]
    };
  }
);

// Connect the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 4. Make your package.json ES module compatible

```json
{
  "type": "module",
  "scripts": {
    "start": "node index.js"
  }
}
```

### 5. Define tools

MCP tools are defined with three components:
- Name: A unique identifier for the tool
- Parameters: Schema for input parameters (using Zod)
- Handler: Async function that processes the inputs and returns results

Example:

```javascript
server.tool(
  "calculateTotal",
  {
    items: z.array(
      z.object({
        name: z.string(),
        price: z.number(),
        quantity: z.number().int().positive()
      })
    ).describe("Array of items to calculate total for")
  },
  async ({ items }) => {
    const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    return {
      content: [
        {
          type: "text",
          text: `Total: $${total.toFixed(2)}`
        }
      ]
    };
  }
);
```

### 6. Testing locally

You can test your MCP server locally using the stdio transport:

```bash
node index.js
```

### 7. Debugging tips

- Use `console.error()` for debugging, not `console.log()` which interferes with stdio transport
- Check the logs in Claude for Desktop for errors
- Ensure your tool handlers properly handle exceptions

## Resources

- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [MCP JavaScript SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [WooCommerce REST API documentation](https://woocommerce.github.io/woocommerce-rest-api-docs/)

## License

MIT 