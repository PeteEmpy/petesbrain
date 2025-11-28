# WooCommerce API Setup Guide for Crowd Control

**Client**: Crowd Control Company (CCC UK)
**Website**: https://crowdcontrolcompany.co.uk
**Platform**: WooCommerce (confirmed)
**Purpose**: Enable direct product data access for offline conversion tracking and campaign optimization

---

## Why We Need WooCommerce API Access

Currently, we can only see conversions that happen on-site through Google Analytics tracking. However, as you mentioned, many of your B2B trade orders happen offline (phone, email, repeat customers, etc.).

**With WooCommerce API access, we can**:
1. **Import offline/trade orders** as Google Ads conversions (retroactively!)
2. **Get real-time product data** (stock levels, pricing, new products)
3. **Optimize product feeds** based on actual inventory
4. **Build customer audiences** for remarketing
5. **Calculate TRUE ROAS** including all revenue sources

**Impact**: Your actual ROAS is likely **200-300%+** instead of the reported 162%, once trade orders are included.

---

## Step 1: Generate WooCommerce API Keys

### Instructions for Your Website Administrator:

1. **Log into WordPress Admin**:
   - Go to https://crowdcontrolcompany.co.uk/wp-admin
   - Use your admin credentials

2. **Navigate to WooCommerce API Settings**:
   - Go to **WooCommerce** → **Settings**
   - Click the **Advanced** tab
   - Click **REST API** (or **Legacy API** if using older WooCommerce)

3. **Create New API Key**:
   - Click **Add key** or **Create an API key**
   - Fill in the details:
     - **Description**: "Pete's Brain - ROK Systems - Google Ads Integration"
     - **User**: Select an admin user (or your own account)
     - **Permissions**: **Read/Write** (we need read for products, write for order notes)

4. **Save the Keys** (IMPORTANT - You can only see these ONCE):
   - **Consumer Key**: Will look like `ck_1234567890abcdef1234567890abcdef12345678`
   - **Consumer Secret**: Will look like `cs_1234567890abcdef1234567890abcdef12345678`

   **Copy both keys immediately** - you won't be able to see them again!

5. **Send Keys Securely**:
   - **DO NOT email** the keys in plain text
   - Options:
     - Share via password-protected document
     - Share via phone call (read them out)
     - Share via encrypted messaging (Signal, WhatsApp)
     - Use a password manager share link (1Password, LastPass)

---

## Step 2: Test API Access (I'll Do This)

Once you provide the keys, I'll:
1. Configure the MCP server with your credentials
2. Test read access to products
3. Test read access to orders
4. Verify data matches your WooCommerce dashboard

---

## Step 3: What Data We'll Access

### What We CAN See:
✅ **Products**: ID, title, price, SKU, stock quantity, categories
✅ **Orders**: Order number, total, items purchased, customer email (anonymized for analytics)
✅ **Order Status**: Completed, processing, pending
✅ **Basic Customer Data**: Order count, total spend (for audience building)

### What We CANNOT See:
❌ Customer passwords or login credentials
❌ Payment card details (these are never stored in WooCommerce)
❌ Any sensitive personal data beyond what's needed for orders

### Data Security:
- API keys stored locally on Pete's Brain system only
- Never shared with third parties
- Used only for Google Ads optimization
- Can be revoked at any time from your WooCommerce dashboard

---

## Step 4: Offline Conversion Import Process

Once API is set up:

1. **Historical Import** (One-Time):
   - Export orders from July 2024 - November 2024
   - Map to Google Ads clicks via order date/time
   - Import as offline conversions
   - Recalculate campaign ROAS

2. **Ongoing Import** (Automated):
   - Check for new completed orders daily
   - Identify orders that came from Google Ads traffic
   - Auto-import as conversions within 90 days of click
   - Update campaign performance metrics

3. **Trade Order Tracking**:
   - For B2B orders that happen via phone/email:
   - Ask: "How did you hear about us?" or "Did you find us online?"
   - Add order note: "Source: Google Ads"
   - Our system will pick up these notes and import appropriately

---

## FAQs

### Q: Is this safe?
**A**: Yes. WooCommerce API keys are designed for this exact purpose. Thousands of businesses use them for integrations with accounting software, inventory systems, and marketing platforms. We're using read-only access for most functions.

### Q: Can I revoke access later?
**A**: Yes! You can revoke or regenerate API keys at any time from WooCommerce → Settings → Advanced → REST API. The integration will simply stop working until new keys are provided.

### Q: Will this slow down my website?
**A**: No. API requests happen in the background and don't impact website performance. We'll only query data once per day for order imports.

### Q: What if I don't have a website admin?
**A**: If you manage the site yourself, follow the steps above. If you have a developer/agency, forward them this guide - they'll know exactly what to do.

### Q: What about GDPR compliance?
**A**: Using WooCommerce order data for marketing optimization is GDPR-compliant as long as:
- You have legitimate interest (you do - optimizing ad spend)
- Customers can opt out (they can - via your privacy policy)
- Data is used only for intended purpose (we will - Google Ads only)

We're not sending customer data to Google - only conversion values and anonymous order IDs.

---

## Alternative: CSV Export (If API Access Not Possible)

If you can't or don't want to provide API access, we can do manual imports:

1. **Monthly Export from WooCommerce**:
   - Go to WooCommerce → Orders
   - Filter by date range (last month)
   - Export to CSV
   - Send CSV to me securely

2. **Process**:
   - I'll manually map orders to Google Ads clicks
   - Import as offline conversions
   - Update ROAS calculations

**Downside**: This is manual, slower, and less accurate than API integration.

---

## Next Steps

1. ✅ **Get API Keys** (follow Step 1 above)
2. ✅ **Send Keys to Peter** (securely - see options in Step 1)
3. ⏳ **I'll Configure & Test** (takes 15 minutes)
4. ⏳ **Historical Import** (we'll import July-Nov 2024 orders)
5. ⏳ **Set Up Automation** (daily sync going forward)

**Timeline**: Once you provide keys, we can have historical data imported within 24 hours and automation running within 48 hours.

---

## Contact

If you have questions or need help generating the API keys:

**Peter Empson**
Email: petere@roksys.co.uk
Phone: 07932 454652
Company: ROK Systems - Digital Marketing

---

## Technical Details for Your Developer (If Applicable)

**API Version**: WooCommerce REST API v3
**Endpoint**: https://crowdcontrolcompany.co.uk/wp-json/wc/v3/
**Authentication**: Basic Auth (Consumer Key as username, Secret as password)
**Required Permissions**: Read/Write (primarily read products and orders)
**Scope**: Products, Orders, Customers (aggregated data only)
**Integration Platform**: MCP (Model Context Protocol) server running locally
**Security**: Keys stored in environment variables, never committed to code
**Frequency**: Daily order sync, weekly product sync

**Endpoints We'll Use**:
- `GET /wp-json/wc/v3/products` - Product catalog
- `GET /wp-json/wc/v3/orders` - Order data
- `GET /wp-json/wc/v3/customers` - Aggregated customer stats (no PII)
- `GET /wp-json/wc/v3/reports/sales` - Sales reports

**We will NOT**:
- Modify products or inventory
- Delete or cancel orders
- Access customer passwords or payment info
- Share data outside Google Ads optimization purposes
