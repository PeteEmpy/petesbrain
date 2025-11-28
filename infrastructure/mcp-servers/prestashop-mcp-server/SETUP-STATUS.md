# PrestaShop MCP Server - Setup Status

**Client**: Accessories for the Home
**Status**: ⏳ Awaiting API credentials from Andrew Fickling
**Last Updated**: 2025-11-28

---

## ✅ Completed Steps

1. **MCP Server Code** - Created and tested
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/prestashop-mcp-server/`
   - File: `server.py`
   - Features: Products, orders, customers, categories, stock levels (all read-only)

2. **Dependencies Installed**
   - Virtual environment: `.venv/`
   - Packages: `httpx`, `mcp` (all dependencies installed)

3. **Added to Claude Code**
   - Command: `claude mcp add -s user prestashop ...`
   - Status: Active and ready to use

4. **Client CONTEXT.md Updated**
   - Location: `/Users/administrator/Documents/PetesBrain/clients/accessories-for-the-home/CONTEXT.md`
   - Section added: Lines 31-36
   - Placeholders: `[TO BE PROVIDED BY CLIENT]`

5. **Request Sent to Andrew**
   - Date: 2025-11-28
   - Message: Requested API key with GET-only permissions
   - Permissions requested:
     - products
     - orders
     - order_details
     - customers
     - categories
     - stock_availables

---

## ⏳ Pending - Awaiting from Andrew Fickling

**Contact**: andrew@modig.co.uk
**Requested**:
1. ✅ API Key (GET permissions only)
2. ✅ Shop URL (full PrestaShop URL)

**Expected format**:
- Shop URL: `https://accessoriesforthehome.co.uk` (or similar)
- API Key: 32-character alphanumeric string

---

## 🚀 Next Steps - When Credentials Arrive

### Step 1: Update CONTEXT.md (2 mins)

Edit: `/Users/administrator/Documents/PetesBrain/clients/accessories-for-the-home/CONTEXT.md`

Replace lines 31-36:
```markdown
## PrestaShop

**Shop URL**: `https://[ACTUAL-URL-FROM-ANDREW]`
**API Key**: `[ACTUAL-KEY-FROM-ANDREW]`

Access: View-only (GET permissions for reporting)
```

### Step 2: Test Connection (5 mins)

Run a quick test to verify the API key works:

```python
# Test 1: Get client credentials
mcp__prestashop__get_client_credentials(
    client_name="accessories-for-the-home"
)

# Test 2: List products (small sample)
mcp__prestashop__get_products(
    shop_url="[FROM CONTEXT.MD]",
    api_key="[FROM CONTEXT.MD]",
    limit=5
)

# Test 3: Get orders (last 7 days)
mcp__prestashop__get_orders(
    shop_url="[FROM CONTEXT.MD]",
    api_key="[FROM CONTEXT.MD]",
    date_from="2025-11-21",
    date_to="2025-11-28",
    limit=10
)
```

**Expected results**:
- ✅ JSON response with product/order data
- ❌ If error 401: API key incorrect
- ❌ If error 403: Permissions not set correctly

### Step 3: Document Initial Findings (10 mins)

Create initial analysis document:
- Product count
- Category structure
- Order volume (last 30 days)
- Top products by revenue
- Stock issues (if any)

Save to: `/Users/administrator/Documents/PetesBrain/clients/accessories-for-the-home/documents/prestashop-initial-analysis.md`

### Step 4: Update This Status File

Mark as complete and archive this file.

---

## 📚 Documentation Reference

**README**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/prestashop-mcp-server/README.md`

**Available MCP Tools**:
1. `mcp__prestashop__get_client_credentials` - Load from CONTEXT.md
2. `mcp__prestashop__get_products` - List products with filtering
3. `mcp__prestashop__get_product` - Single product by ID
4. `mcp__prestashop__get_orders` - Orders with date filtering
5. `mcp__prestashop__get_order` - Order details with line items
6. `mcp__prestashop__get_customers` - Customer list
7. `mcp__prestashop__get_categories` - Category hierarchy
8. `mcp__prestashop__get_stock_levels` - Stock availability

---

## 🔧 Troubleshooting

### If API key doesn't work:

**Problem**: 401 Unauthorized
- **Solution**: Check API key is copied correctly (no spaces/line breaks)
- **Check**: Verify key status is "Enabled" in PrestaShop admin

**Problem**: 403 Forbidden
- **Solution**: Ask Andrew to verify GET permissions are granted for all resources
- **Check**: Advanced Parameters > Webservice > Edit key > Check all boxes under GET column

**Problem**: No data returned
- **Solution**: PrestaShop returns empty arrays if no records match
- **Check**: Verify products/orders exist in the shop
- **Check**: Date ranges are correct (orders)

**Problem**: Shop URL incorrect
- **Solution**: Must be exact PrestaShop base URL (no /api, no trailing slash)
- **Example**: `https://accessoriesforthehome.co.uk` ✅
- **Example**: `https://accessoriesforthehome.co.uk/api` ❌

---

## 📝 Notes

- **Purpose**: Read-only reporting and analysis to complement Google Ads data
- **Security**: GET permissions only - no write access
- **Credentials**: Stored in client CONTEXT.md (gitignored)
- **Universal**: Same MCP can be used for other PrestaShop clients with different credentials

---

## ✉️ Message Sent to Andrew

```
Hi Andrew,

Hope you're well!

I'm setting up some automated reporting tools for Accessories for the Home
and need read-only access to the PrestaShop API to pull product and order
data for analysis purposes.

Could you set up a Web Services API key for me with the following configuration?

**Configuration needed:**

Location: Advanced Parameters > Webservice > Add new webservice key

**Permissions (GET/View only - no write access):**
- products
- orders
- order_details
- customers
- categories
- stock_availables

**Description:** "Roksys - Reporting & Analysis"

Once you've created the key, could you send me:
1. The API key
2. The shop URL (full PrestaShop URL)

This is purely for read-only reporting - I'll be using it to pull performance
data, stock levels, and order information to complement the Google Ads reporting.

Let me know if you have any questions!

Cheers,
Peter
```

**Sent**: 2025-11-28
**Awaiting response**: Yes
