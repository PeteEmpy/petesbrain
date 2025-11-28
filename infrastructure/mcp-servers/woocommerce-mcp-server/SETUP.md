# WooCommerce MCP Server Setup

This server has been installed and configured in Pete's Brain.

## Configuration Required

To use this MCP server, you need to add your WooCommerce store credentials to `.mcp.json`:

### Step 1: Generate WooCommerce API Keys

1. Log in to your WooCommerce store WordPress admin
2. Go to **WooCommerce → Settings → Advanced → REST API**
3. Click **Add Key**
4. Set permissions (Read/Write recommended)
5. Click **Generate API Key**
6. Copy the **Consumer Key** (ck_xxxxx) and **Consumer Secret** (cs_xxxxx)

### Step 2: Update Configuration

Edit `/Users/administrator/Documents/PetesBrain/.mcp.json` and replace the placeholder values:

```json
"woocommerce": {
  "env": {
    "WORDPRESS_SITE_URL": "https://your-store.com",
    "WOOCOMMERCE_CONSUMER_KEY": "ck_xxxxxxxxxxxxx",
    "WOOCOMMERCE_CONSUMER_SECRET": "cs_xxxxxxxxxxxxx"
  }
}
```

### Step 3: Restart Claude Code

After updating the configuration, restart Claude Code for the changes to take effect.

## Available Features

Once configured, you'll have access to:

- **Products**: Create, read, update, delete products and variations
- **Orders**: Manage orders, add notes, process refunds
- **Customers**: View and manage customer data
- **Catalog**: Manage categories, tags, attributes
- **Store Operations**: Shipping, taxes, coupons, payment gateways
- **Analytics**: Sales reports, product performance, customer insights
- **Inventory**: Stock management and tracking

## Testing

To test if the connection works:

```
List all WooCommerce products for [store URL]
```

## Troubleshooting

- **Authentication errors**: Verify your API keys are correct
- **Connection errors**: Check that WORDPRESS_SITE_URL is correct (include https://)
- **Permission errors**: Ensure API key has appropriate read/write permissions
- **404 errors**: Verify WooCommerce REST API is enabled in your store

## Security Notes

- API keys grant access to your WooCommerce store - keep them secure
- Use read-only permissions if you only need to view data
- Store credentials are only in your local .mcp.json file
- Never commit .mcp.json to version control with real credentials
