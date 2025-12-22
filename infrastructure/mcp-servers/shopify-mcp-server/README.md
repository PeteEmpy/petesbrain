# Shopify MCP Server

A Model Context Protocol (MCP) server that enables Claude Desktop to interact with Shopify stores. Access products, orders, customers, inventory, and more through a secure API connection.

## Quick Start

### Installation

You can run this server directly using npx:

```bash
npx @ajackus/shopify-mcp-server
```

Or install globally:

```bash
npm install -g @ajackus/shopify-mcp-server
```

### Configuration

#### 1. Create a Custom App in Shopify

1. **Access App Development:**
   - Log in to your Shopify admin panel
   - Navigate to Settings → Apps and sales channels
   - Click "Develop apps" (you may need to enable custom app development first)

2. **Create the App:**
   - Click "Create an app"
   - Give your app a name (e.g., "MCP Server Integration")
   - Select the app developer (usually yourself)

3. **Configure API Scopes:**
   - Click on "Configure Admin API scopes"
   - Select the scopes based on your needs:
     - **Minimum recommended**: Products (read/write), Orders (read), Customers (read), Inventory (read/write)
     - **For analytics**: Add Analytics (read), Reports (read)
     - **For marketing**: Add Discounts (read/write), Marketing events (read/write)
     - **For content**: Add Online Store pages (read/write), Themes (read)
   - Save your configuration

4. **Install the App:**
   - After configuring scopes, click "Install app"
   - Confirm the installation

5. **Get Your Access Token:**
   - Once installed, go to "API credentials" tab
   - Under "Admin API access token", click "Reveal token once"
   - **Important**: Copy this token immediately - you can only see it once!
   - Keep your access token secure and never commit it to version control

#### 2. Configure Claude Desktop

   Edit your Claude Desktop config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

   Add the Shopify server configuration:

   ```json
   {
     "mcpServers": {
       "shopify": {
         "command": "npx",
         "args": ["@ajackus/shopify-mcp-server"],
         "env": {
           "SHOPIFY_STORE_DOMAIN": "your-store.myshopify.com",
           "SHOPIFY_ACCESS_TOKEN": "shpat_your_access_token_here",
           "SHOPIFY_LOG_LEVEL": "warning"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to apply the changes

## Features

This MCP server provides comprehensive access to the Shopify Admin API with 70+ tools covering all major store operations.

### Core Commerce Tools

#### Products & Inventory
- **Products**: List, get, create, update products with full variant support
- **Inventory**: Track levels, adjust quantities, get forecasting data
- **Collections**: Browse and manage product collections
- **Metafields**: Set custom data on any resource
- **Metaobjects**: Create and manage custom data structures (GraphQL exclusive)

#### Orders & Fulfillment
- **Orders**: List and retrieve order details
- **Draft Orders**: Create and manage draft orders
- **Fulfillment**: Create fulfillments, manage fulfillment orders
- **Shipping**: Get shipping zones, rates, and carrier services

#### Customers & B2B
- **Customers**: List, retrieve, and analyze customer data
- **Companies**: Manage B2B companies and contacts
- **Customer Analytics**: Behavior tracking, lifetime value, retention metrics

### Financial Tools
- **Transactions**: View order transactions and payment details
- **Refunds**: Process full or partial refunds
- **Gift Cards**: Create and manage gift cards
- **Financial Reports**: Revenue, expenses, profit summaries

### Marketing & Content
- **Discounts**: Create discount codes and automatic discounts
- **Price Rules**: Manage complex pricing strategies
- **Pages & Blogs**: Create and manage content pages and blog articles
- **URL Redirects**: Set up URL redirects for SEO
- **Marketing Reports**: Campaign performance and ROI tracking

### Analytics & Reporting

#### Sales Analytics
- **Sales Reports**: Comprehensive sales data with customizable granularity
- **Product Analytics**: Best sellers, conversion rates, performance metrics
- **Financial Summary**: Revenue, taxes, shipping, refunds breakdown
- **Custom Reports**: Build reports with specific metrics and dimensions

#### Customer Analytics
- **Customer Reports**: New vs returning, average order value, lifetime value
- **Abandonment Reports**: Cart and checkout abandonment analytics
- **Retention Metrics**: Churn rate, retention rate analysis

#### Traffic & Conversion
- **Traffic Reports**: Sessions, visitors, bounce rate, page views
- **Conversion Funnel**: Track customer journey from visit to purchase
- **Marketing Attribution**: Channel performance and ROI

### Store Configuration
- **Themes**: List installed themes
- **Webhooks**: Create and manage webhook subscriptions
- **Markets**: Configure international markets and currencies
- **Locations**: Manage store and warehouse locations
- **Abandoned Checkouts**: Track and analyze abandoned carts

### Example Commands

Ask Claude to:
- "Generate a sales report for last month"
- "Show me which products have less than 10 units in stock"
- "Create a 20% discount code for VIP customers"
- "Get customer retention metrics for Q4"
- "List abandoned checkouts from the past week"
- "Show conversion funnel analytics for Black Friday"
- "Create a blog post about our new product launch"
- "Set up a webhook for new orders"
- "Generate a custom report on product performance by category"

## API Scopes Required

For full functionality, configure your Shopify app with these scopes:

### Essential Scopes
- `read_products`, `write_products` - Product management
- `read_orders` - Order viewing
- `read_customers` - Customer data access
- `read_inventory`, `write_inventory` - Inventory management

### Extended Scopes (for complete feature set)
- `read_draft_orders`, `write_draft_orders` - Draft order management
- `read_fulfillments`, `write_fulfillments` - Fulfillment processing
- `read_shipping` - Shipping configuration
- `read_analytics` - Analytics and reporting
- `read_marketing_events`, `write_marketing_events` - Marketing tools
- `read_discounts`, `write_discounts` - Discount management
- `read_price_rules`, `write_price_rules` - Pricing strategies
- `read_reports` - Advanced reporting
- `read_themes` - Theme management
- `read_content`, `write_content` - Pages and blog management
- `read_metaobjects`, `write_metaobjects` - Custom data structures
- `read_gift_cards`, `write_gift_cards` - Gift card management

### Scope Management Strategy

**Important**: You don't need to grant all scopes! The MCP server adapts to available permissions:

1. **Start with minimal scopes** - Only grant what you currently need
2. **Add scopes as needed** - If a tool returns "authorization error", add the required scope
3. **Security first** - Never grant write scopes unless you need to modify data
4. **Limit by access token** - The safest way to restrict functionality is by limiting scopes at the Shopify app level

Example scenarios:
- **Read-only analytics**: Only grant read scopes for products, orders, customers, and reports
- **Inventory management**: Add inventory write scope only
- **Full e-commerce**: Grant all relevant scopes for complete functionality

The server will work with whatever scopes you provide - tools requiring missing scopes will simply return authorization errors without affecting other functionality.

## Configuration Options

### Environment Variables

- `SHOPIFY_STORE_DOMAIN` (required) - Your Shopify store domain
- `SHOPIFY_ACCESS_TOKEN` (required) - Your Admin API access token
- `SHOPIFY_API_VERSION` (optional) - API version (defaults to latest)
- `SHOPIFY_LOG_LEVEL` (optional) - Logging level: `error`, `warning`, `info`, `debug` (defaults to `warning`)
- `TRANSPORT_MODE` (optional) - Transport mode: `stdio` (default) or `sse`
- `PORT` (optional) - HTTP port for SSE mode (defaults to 3000)

### Logging

The server uses proper logging to stderr to avoid interfering with the MCP protocol:
- **Error**: Critical errors that prevent operation
- **Warning**: Important notices (default level)
- **Info**: General operational information
- **Debug**: Detailed debugging information including HTTP requests

Set `SHOPIFY_LOG_LEVEL=debug` to see all API requests and responses.

## Local Development

If you want to run from source:

```bash
git clone https://github.com/ajackus/shopify-mcp-server.git
cd shopify-mcp-server
npm install
npm run build
```

Then update your Claude config to use the local build:

```json
{
  "mcpServers": {
    "shopify": {
      "command": "node",
      "args": ["/path/to/shopify-mcp-server/build/index.js"],
      "env": {
        "SHOPIFY_STORE_DOMAIN": "your-store.myshopify.com",
        "SHOPIFY_ACCESS_TOKEN": "shpat_your_access_token_here"
      }
    }
  }
}
```

## Troubleshooting

If the server doesn't appear in Claude:

1. Check that your credentials are correct
2. Ensure Claude Desktop is fully restarted
3. Look for errors in the MCP logs
4. Try running the server manually to test:
   ```bash
   SHOPIFY_STORE_DOMAIN=your-store.myshopify.com \
   SHOPIFY_ACCESS_TOKEN=shpat_your_token \
   npx @ajackus/shopify-mcp-server
   ```

## Security

- Never share or commit your access tokens
- Use environment variables for credentials
- Create separate apps with minimal scopes for different use cases
- Regularly rotate your access tokens

## SSE Mode (HTTP Transport)

The server supports SSE (Server-Sent Events) transport for HTTP-based access, enabling deployment to cloud platforms.

### Local SSE Testing

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Run in SSE mode
TRANSPORT_MODE=sse \
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com \
SHOPIFY_ACCESS_TOKEN=shpat_your_token \
SHOPIFY_LOG_LEVEL=warning \
PORT=3000 \
node build/index.js
```

The server will start on `http://localhost:3000` with:
- SSE endpoint: `GET /sse`
- Messages endpoint: `POST /messages?sessionId={id}`
- Health check: `GET /health`

### Deploy to Render.com

1. **Fork or push this repository to GitHub**

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration

3. **Set Environment Variables:**
   - `SHOPIFY_STORE_DOMAIN`: Your store domain
   - `SHOPIFY_ACCESS_TOKEN`: Your API access token
   - Other variables are pre-configured in `render.yaml`

4. **Deploy:**
   - Click "Create Web Service"
   - Your server will be available at `https://your-app.onrender.com`

5. **Configure Claude Desktop for SSE:**

   ```json
   {
     "mcpServers": {
       "shopify-remote": {
         "transport": {
           "type": "sse",
           "url": "https://your-app.onrender.com/sse"
         }
       }
     }
   }
   ```

### Docker Deployment

Build and run with Docker:

```bash
# Build image
docker build -t shopify-mcp-server .

# Run container
docker run -p 3000:3000 \
  -e SHOPIFY_STORE_DOMAIN=your-store.myshopify.com \
  -e SHOPIFY_ACCESS_TOKEN=shpat_your_token \
  -e SHOPIFY_LOG_LEVEL=warning \
  shopify-mcp-server
```

## License

MIT

## Contributing

Issues and pull requests are welcome at: https://github.com/ajackus/shopify-mcp-server