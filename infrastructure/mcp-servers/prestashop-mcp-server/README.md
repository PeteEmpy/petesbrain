# PrestaShop MCP Server

Universal MCP server for PrestaShop Web Services API (reporting focus).

## Features

- **Products**: List products, get product details, filter by active status
- **Orders**: List orders with date filtering, get order details with line items
- **Customers**: List customers, filter by active status
- **Categories**: Get product category hierarchy
- **Stock**: Get stock availability levels
- **Client Credentials**: Auto-load credentials from client CONTEXT.md files

## Setup Instructions

### 1. Enable PrestaShop Web Services

**Ask the client to complete these steps:**

1. Log in to PrestaShop Admin Panel
2. Navigate to: **Advanced Parameters > Webservice**
3. Enable Web Services: Set **Enable PrestaShop's webservice** to **Yes**
4. Click **Save**

### 2. Generate API Key

**Ask the client to complete these steps:**

1. In the same Webservice page, click **Add new webservice key**
2. Fill in the form:
   - **Key**: Click **Generate** to create a random API key (or create a custom one)
   - **Key description**: Enter "MCP Server - Reporting" (or similar)
   - **Status**: Set to **Enabled**
3. **Permissions**: Under "Permissions", grant **View (GET)** permissions for:
   - ✅ products
   - ✅ orders
   - ✅ order_details
   - ✅ customers
   - ✅ categories
   - ✅ stock_availables
4. Click **Save**
5. **Copy the API Key** - you'll need this for the next step

### 3. Add Credentials to Client CONTEXT.md

Add the following section to `/Users/administrator/Documents/PetesBrain/clients/accessories-for-the-home/CONTEXT.md`:

```markdown
## PrestaShop

**Shop URL**: `https://your-shop-domain.com`
**API Key**: `YOUR_API_KEY_HERE`

Access: View-only (GET permissions for reporting)
```

Replace:
- `https://your-shop-domain.com` with the actual shop URL (no trailing slash)
- `YOUR_API_KEY_HERE` with the API key from step 2

### 4. Install Dependencies

```bash
cd /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/prestashop-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Add to Claude Code

```bash
claude mcp add -s user prestashop \
  "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/prestashop-mcp-server/.venv/bin/python" \
  "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/prestashop-mcp-server/server.py"
```

## Usage

### Get Client Credentials

```python
mcp__prestashop__get_client_credentials(
    client_name="accessories-for-the-home"
)
```

### List Products

```python
mcp__prestashop__get_products(
    shop_url="https://your-shop.com",
    api_key="YOUR_API_KEY",
    limit=50,
    active_only=True,
    sort="name_ASC"
)
```

### Get Orders (Date Range)

```python
mcp__prestashop__get_orders(
    shop_url="https://your-shop.com",
    api_key="YOUR_API_KEY",
    date_from="2025-01-01",
    date_to="2025-01-31",
    limit=100
)
```

### Get Single Order with Line Items

```python
mcp__prestashop__get_order(
    shop_url="https://your-shop.com",
    api_key="YOUR_API_KEY",
    order_id="12345"
)
```

### Get Stock Levels

```python
mcp__prestashop__get_stock_levels(
    shop_url="https://your-shop.com",
    api_key="YOUR_API_KEY",
    product_id="123"  # Optional - leave blank for all products
)
```

## Example Workflow

```python
# 1. Get credentials from client CONTEXT.md
creds = mcp__prestashop__get_client_credentials(
    client_name="accessories-for-the-home"
)

# 2. Get orders for last 30 days
orders = mcp__prestashop__get_orders(
    shop_url=creds['shop_url'],
    api_key=creds['api_key'],
    date_from="2025-10-28",
    date_to="2025-11-28",
    limit=500
)

# 3. Analyse revenue, top products, etc.
```

## Troubleshooting

### "401 Unauthorized"
- Check API key is correct in CONTEXT.md
- Verify Web Services are enabled in PrestaShop admin

### "403 Forbidden"
- Check API key has GET permissions for the requested resource
- Verify API key status is "Enabled"

### "No data returned"
- PrestaShop returns empty arrays if no matching records
- Check date ranges and filters are correct
- Verify products/orders exist in the shop

### "CONTEXT.md not found"
- Ensure client name matches folder name exactly
- Client names are normalised to lowercase with hyphens

## API Reference

All tools return JSON data. PrestaShop uses XML internally but the MCP server converts to JSON for easier processing.

### Available Tools

1. **get_client_credentials** - Load credentials from client CONTEXT.md
2. **get_products** - List products with filtering and sorting
3. **get_product** - Get single product by ID
4. **get_orders** - List orders with date filtering
5. **get_order** - Get order details with line items
6. **get_customers** - List customers
7. **get_categories** - Get product category hierarchy
8. **get_stock_levels** - Get stock availability

## Security Notes

- API keys are stored in client CONTEXT.md files (gitignored)
- Only GET (read) permissions are granted - no write access
- Credentials are never logged or stored in MCP server code
- All API requests use HTTPS (enforced by PrestaShop)
