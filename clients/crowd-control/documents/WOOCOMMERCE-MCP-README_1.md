# WooCommerce MCP Setup for Crowd Control

## Current Status

✅ **Website Confirmed**: https://crowdcontrolcompany.co.uk (WooCommerce)
✅ **Client Guide Created**: [documents/woocommerce-api-setup-guide.md](documents/woocommerce-api-setup-guide.md)
❌ **API Credentials**: Not yet received from client
❌ **MCP Configuration**: Pending credentials

---

## What's Needed from Client

The client needs to generate WooCommerce REST API credentials and send them securely. Full instructions are in the setup guide.

**Required Information**:
1. **Consumer Key**: `ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. **Consumer Secret**: `cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## How to Configure MCP Once Credentials Received

### Step 1: Update .mcp.json

Edit `/Users/administrator/Documents/PetesBrain/.mcp.json` and modify the `woocommerce` entry:

**Current configuration** (configured for Godshot Coffee):
```json
"woocommerce": {
  "command": "node",
  "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/woocommerce-mcp-server/build/index.js"],
  "env": {
    "WORDPRESS_SITE_URL": "https://mygodshot.com",
    "WOOCOMMERCE_CONSUMER_KEY": "ck_d1906a0a64cdc4f9b365d67c6757c0b603335402",
    "WOOCOMMERCE_CONSUMER_SECRET": "cs_ebcb7f623c95498adf6138feb81ce79a8c10530a"
  }
}
```

**New configuration** (for Crowd Control):
```json
"woocommerce": {
  "command": "node",
  "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/woocommerce-mcp-server/build/index.js"],
  "env": {
    "WORDPRESS_SITE_URL": "https://crowdcontrolcompany.co.uk",
    "WOOCOMMERCE_CONSUMER_KEY": "[PASTE CLIENT'S CONSUMER KEY HERE]",
    "WOOCOMMERCE_CONSUMER_SECRET": "[PASTE CLIENT'S CONSUMER SECRET HERE]"
  }
}
```

**Note**: If you need to keep both Godshot and Crowd Control WooCommerce access, you can create a second MCP server entry:
```json
"woocommerce-godshot": {
  "command": "node",
  "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/woocommerce-mcp-server/build/index.js"],
  "env": {
    "WORDPRESS_SITE_URL": "https://mygodshot.com",
    "WOOCOMMERCE_CONSUMER_KEY": "ck_d1906a0a64cdc4f9b365d67c6757c0b603335402",
    "WOOCOMMERCE_CONSUMER_SECRET": "cs_ebcb7f623c95498adf6138feb81ce79a8c10530a"
  }
},
"woocommerce-crowdcontrol": {
  "command": "node",
  "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/woocommerce-mcp-server/build/index.js"],
  "env": {
    "WORDPRESS_SITE_URL": "https://crowdcontrolcompany.co.uk",
    "WOOCOMMERCE_CONSUMER_KEY": "[CLIENT KEY]",
    "WOOCOMMERCE_CONSUMER_SECRET": "[CLIENT SECRET]"
  }
}
```

### Step 2: Test the Connection

After updating `.mcp.json`, restart Claude Code and test the connection:

```bash
# In Claude Code, try these MCP tools:
# (They'll show as mcp__woocommerce__* or mcp__woocommerce-crowdcontrol__* depending on config)

# Test product access
mcp__woocommerce__get_products (or mcp__woocommerce-crowdcontrol__get_products)

# Test order access
mcp__woocommerce__get_orders
```

Expected result: You should see product data from Crowd Control's WooCommerce store.

### Step 3: Verify Data Accuracy

Once connected, do a quick sanity check:
1. Pull 5-10 products and verify they match the Google Shopping feed
2. Pull recent orders and check revenue totals match WooCommerce dashboard
3. Verify product IDs match the Google Merchant Center feed

---

## What We'll Do Once Connected

### Immediate (Week 1):
1. **Stock Status Check** for missing 2024 hero products:
   - Product 6735 (FlexMaster 110)
   - Product 6733 (FlexPro 160)
   - Product 8025 (Belt Barrier 10 Pack)
   - Check: In stock? Pricing? Visibility settings?

2. **Pricing Audit**:
   - Compare October 2024 prices to October 2025 prices
   - Identify if price increases contributed to conversion rate drop

3. **Product Catalog Export**:
   - Get full product catalog with stock levels, prices, categories
   - Compare to Merchant Center feed for discrepancies

### Short-Term (Weeks 2-4):
1. **Offline Conversion Import** (Historical):
   - Export orders from July-October 2025
   - Map orders to Google Ads clicks (via click time + order time correlation)
   - Import as offline conversions retroactively
   - Recalculate true ROAS

2. **Order Analysis**:
   - Identify which products drive offline/repeat orders
   - Check if multi-pack/bundle buyers are repeat customers (indicating B2B/trade)
   - Quantify online vs offline conversion split

3. **Automation Setup**:
   - Daily order sync to check for new completed orders
   - Auto-import offline conversions within 90-day Google Ads window
   - Weekly stock level monitoring for hero products

### Medium-Term (Ongoing):
1. **Product Performance Dashboard**:
   - Track stock levels, prices, and sales velocity
   - Alert when hero products go out of stock
   - Monitor for Merchant Center feed sync issues

2. **Customer Audience Building**:
   - Export customer email lists (anonymized) for remarketing
   - Build audiences based on purchase history (high-value, repeat, product category)
   - Use for PMax and Display campaigns

3. **Feed Optimization**:
   - Ensure product feed always reflects current stock/pricing
   - Prevent ad spend on out-of-stock products
   - Auto-pause products when stock reaches zero

---

## Benefits of WooCommerce Integration

### For Performance Analysis:
- **True ROAS Calculation**: Include offline/trade orders in conversion value
- **Product-Level Insights**: Track which products sell online vs offline
- **Inventory Correlation**: Connect stock-outs to performance drops

### For Campaign Optimization:
- **Prevent Wasted Spend**: Don't advertise out-of-stock products
- **Dynamic Budget Allocation**: Prioritize in-stock, high-margin items
- **Seasonal Planning**: Predict stock needs based on ad performance

### For Offline Conversion Tracking:
- **Import Historical Orders**: Retroactively add Jul-Oct 2025 conversions
- **Ongoing Sync**: Daily import of new orders
- **B2B Attribution**: Track trade orders back to Google Ads

---

## Security Notes

- API keys stored in `.mcp.json` (local file, not shared)
- Never commit `.mcp.json` to public repos
- Keys can be revoked by client at any time from WooCommerce dashboard
- We only read data - no write access to products/orders/prices

---

## Next Actions

**For Peter**:
1. ✅ Create setup guide for client
2. ✅ Identify website and confirm WooCommerce
3. ✅ Document configuration steps
4. ❌ Send setup guide to client
5. ❌ Wait for API credentials
6. ❌ Configure MCP when credentials received
7. ❌ Test connection and verify data

**For Client**:
1. ❌ Log into WordPress admin (https://crowdcontrolcompany.co.uk/wp-admin)
2. ❌ Generate API keys (WooCommerce → Settings → Advanced → REST API)
3. ❌ Send keys securely to Peter (see guide for secure methods)

---

## Contact

**Peter Empson**
Email: petere@roksys.co.uk
Phone: 07932 454652

Send API credentials via:
- Encrypted email
- Password-protected document
- Phone call (read out the keys)
- Secure messaging (Signal, WhatsApp)

**DO NOT** send keys in plain text email.
