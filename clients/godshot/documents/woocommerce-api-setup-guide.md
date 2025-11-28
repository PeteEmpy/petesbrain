# WooCommerce API Troubleshooting Guide for Godshot

**Client**: Godshot Coffee  
**Website**: https://mygodshot.com  
**Platform**: WooCommerce (WordPress)  
**Issue**: API returning 403 Forbidden errors  
**Purpose**: Troubleshoot and restore API access for conversion tracking reconciliation

---

## Current Situation

We have WooCommerce API credentials configured, but all API requests are returning `403 Forbidden` errors. This prevents us from:
- Verifying Google Ads conversion tracking accuracy
- Mapping product IDs between Google Shopping feed and WooCommerce
- Reconciling reported revenue vs actual sales
- Performing product-level performance analysis

**This is blocking critical conversion tracking audit work.**

---

## Step 1: Verify API Keys Still Exist

### Check in WordPress Admin

1. **Log into WordPress Admin**:
   - Go to https://mygodshot.com/wp-admin
   - Use your admin credentials

2. **Navigate to WooCommerce API Settings**:
   - Go to **WooCommerce** → **Settings**
   - Click the **Advanced** tab
   - Click **REST API** (or **Legacy API** if using older WooCommerce)

3. **Find Existing API Key**:
   - Look for API key with description: "Pete's Brain - ROK Systems" or similar
   - Check if it still exists and is active
   - Verify permissions are set to **Read/Write**

4. **Check API Key Status**:
   - ✅ **If key exists**: Note the Consumer Key (should start with `ck_`)
   - ❌ **If key doesn't exist**: We'll need to create a new one (see Step 2)

---

## Step 2: Verify REST API is Enabled

### Check WooCommerce Settings

1. **In WooCommerce → Settings → Advanced → REST API**:
   - Ensure REST API is enabled
   - If using WooCommerce 3.5+, check "Legacy REST API" is enabled
   - Some older integrations require legacy API

2. **Check WordPress Permalinks**:
   - Go to **Settings → Permalinks**
   - Ensure permalinks are NOT set to "Plain" (should be Post name, Day and name, etc.)
   - REST API requires permalinks to be enabled
   - Click "Save Changes" even if no changes made (refreshes rewrite rules)

---

## Step 3: Check Security Plugins

### Common Security Plugins That Block API Access

**Wordfence**:
- Go to Wordfence → Firewall → Blocking
- Check if our IP address is blocked
- Go to Wordfence → Tools → Live Traffic to see blocked requests
- Whitelist `/wp-json/wc/` endpoints if needed

**iThemes Security**:
- Go to Security → Settings → Advanced
- Check "REST API" settings
- Ensure REST API isn't disabled
- Check if specific IPs are blocked

**Sucuri**:
- Check Sucuri dashboard for blocked requests
- Review firewall rules for API endpoint blocking

**Other Security Plugins**:
- Check any security plugin settings
- Look for "REST API" or "API" blocking options
- Temporarily disable security plugins to test if they're the cause

**Testing**: Temporarily disable security plugins and test API access. If it works, re-enable plugins and whitelist API endpoints.

---

## Step 4: Check Server Configuration

### Nginx Configuration

If you have access to server configuration, check nginx rules:

```nginx
# Should allow /wp-json/ endpoints
location ~ ^/wp-json/ {
    try_files $uri $uri/ /index.php?$args;
}
```

**Common Issues**:
- Nginx blocking `/wp-json/` endpoints
- Rate limiting too aggressive
- IP-based blocking rules

### Server Firewall

Check server firewall rules:
- Review IP whitelisting/blacklisting
- Check if API requests are being blocked
- Verify rate limiting isn't too strict

### PHP Configuration

Ensure PHP isn't blocking requests:
- Check `max_execution_time` settings
- Verify `memory_limit` is sufficient
- Check for any custom PHP security rules

---

## Step 5: Test API Access Directly

### Using cURL (Command Line)

Test if API works from command line:

```bash
curl -u "ck_d1906a0a64cdc4f9b365d67c6757c0b603335402:cs_ebcb7f623c95498adf6138feb81ce79a8c10530a" \
     https://mygodshot.com/wp-json/wc/v3/products?per_page=1
```

**Expected Result**: Should return JSON product data  
**If 403 Error**: Server-side blocking issue  
**If 401 Error**: Invalid credentials (regenerate keys)  
**If 200 Success**: API works, issue is with MCP server configuration

### Using Postman or Browser

1. **Get Authorization Header**:
   - Consumer Key: `ck_d1906a0a64cdc4f9b365d67c6757c0b603335402`
   - Consumer Secret: `cs_ebcb7f623c95498adf6138feb81ce79a8c10530a`
   - Use Basic Auth with these credentials

2. **Test Endpoint**:
   - URL: `https://mygodshot.com/wp-json/wc/v3/products?per_page=1`
   - Method: GET
   - Auth: Basic Auth (use Consumer Key as username, Secret as password)

3. **Check Response**:
   - ✅ **200 OK**: API works, issue elsewhere
   - ❌ **403 Forbidden**: Server blocking (security plugin, firewall, nginx)
   - ❌ **401 Unauthorized**: Invalid credentials (regenerate keys)

---

## Step 6: Regenerate API Keys (If Needed)

If API keys are missing or need to be regenerated:

### Create New API Key

1. **In WooCommerce → Settings → Advanced → REST API**:
   - Click **Add key** or **Create an API key**
   - Fill in details:
     - **Description**: "Pete's Brain - ROK Systems - Google Ads Integration"
     - **User**: Select an admin user
     - **Permissions**: **Read/Write** (we need read for products/orders, write for order notes)

2. **Save the Keys** (IMPORTANT - You can only see these ONCE):
   - **Consumer Key**: Will look like `ck_1234567890abcdef...`
   - **Consumer Secret**: Will look like `cs_1234567890abcdef...`
   - **Copy both keys immediately** - you won't be able to see them again!

3. **Send Keys Securely**:
   - **DO NOT email** the keys in plain text
   - Options:
     - Share via password-protected document
     - Share via phone call (read them out)
     - Share via encrypted messaging (Signal, WhatsApp)
     - Use a password manager share link

4. **Update Configuration**:
   - I'll update `.mcp.json` with new credentials
   - Test connection immediately after update

---

## Step 7: IP Whitelisting (If IP Blocking is Issue)

If the issue is IP-based blocking:

1. **Identify Our IP Address**:
   - Contact Peter to get current IP address
   - May need to whitelist multiple IPs if using dynamic IPs

2. **Whitelist in Security Plugin**:
   - Add IP to Wordfence whitelist
   - Add IP to iThemes Security whitelist
   - Add IP to any other security plugin whitelists

3. **Whitelist in Server Firewall**:
   - Add IP to server firewall whitelist
   - Add IP to nginx allow rules if applicable

---

## Common Solutions

### Solution 1: Permalinks Not Enabled
**Fix**: Go to Settings → Permalinks → Save Changes (even if no changes)

### Solution 2: Security Plugin Blocking
**Fix**: Whitelist `/wp-json/wc/` endpoints in security plugin

### Solution 3: Legacy API Disabled
**Fix**: Enable "Legacy REST API" in WooCommerce → Settings → Advanced → REST API

### Solution 4: API Keys Revoked
**Fix**: Regenerate API keys and update configuration

### Solution 5: Server Firewall Blocking
**Fix**: Whitelist IP address or `/wp-json/` endpoints in firewall

---

## Testing After Fix

Once you've made changes:

1. **Test with cURL** (see Step 5)
2. **Contact Peter** to test MCP connection
3. **Verify Product Access**: Should be able to retrieve product list
4. **Verify Order Access**: Should be able to retrieve recent orders

---

## What We'll Do Once Fixed

### Immediate:
1. ✅ Export full product catalog with IDs, prices, stock levels
2. ✅ Map Google Shopping feed product IDs to WooCommerce product IDs
3. ✅ Compare Google Ads conversions vs actual WooCommerce sales
4. ✅ Verify conversion tracking accuracy

### Short-Term:
1. ✅ Set up weekly reconciliation process
2. ✅ Create product performance dashboard
3. ✅ Monitor stock levels for top products
4. ✅ Track price changes and impact

---

## FAQs

### Q: Is this safe?
**A**: Yes. WooCommerce API keys are designed for this exact purpose. We're using read-only access for most functions. Keys can be revoked at any time.

### Q: Will this slow down my website?
**A**: No. API requests happen in the background and don't impact website performance. We'll only query data once per day.

### Q: What data will you access?
**A**: Products (ID, title, price, stock), Orders (order number, total, items), Basic customer data (order count, total spend - anonymized). We cannot see passwords, payment details, or sensitive personal data.

### Q: Can I revoke access later?
**A**: Yes! You can revoke or regenerate API keys at any time from WooCommerce → Settings → Advanced → REST API.

### Q: What if I don't have server access?
**A**: Contact your website developer or hosting provider. They'll know how to check security plugins and server configuration.

---

## Contact

**Peter Empson**  
Email: petere@roksys.co.uk  
Phone: 07932 454652

**For Technical Issues**: Contact your website developer or hosting provider to troubleshoot server-side blocking.

---

## Next Steps

1. ✅ Check API keys exist in WooCommerce dashboard
2. ✅ Verify REST API is enabled
3. ✅ Review security plugins for blocking
4. ✅ Test API access with cURL/Postman
5. ✅ Contact Peter with results or if you need new API keys
6. ✅ Once fixed, Peter will test MCP connection and verify data access

**Timeline**: Once API access is restored, we can have product reconciliation completed within 24 hours.

