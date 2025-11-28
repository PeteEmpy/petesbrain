# Adding New Clients to Product Impact Analyzer

**Last Updated**: October 30, 2025

## Overview

This guide walks through the complete process of adding a new client to the Product Impact Analyzer monitoring and weekly analysis system.

## Prerequisites

### Client Requirements

A client can ONLY be added if they have:

✅ **E-commerce with product feeds** (Shopping campaigns)
✅ **Google Merchant Center account** with active products
✅ **Google Ads account** with Shopping or Performance Max campaigns

❌ **Cannot be added** if they are:
- Lead generation only (no products)
- Service-based businesses (hotels, courses, etc.)
- No active product feeds

### Information Needed

Before starting, gather:

1. **Google Ads Customer ID** (10 digits, e.g., "6281395727")
2. **Google Merchant Center ID** (Merchant ID from Shopping campaigns)
3. **Client name** (must match folder name in `/clients/[client-name]/`)
4. **Typical daily revenue** (for setting alert thresholds)
5. **Business context** (from CONTEXT.md file)

---

## Step-by-Step Process

### Step 1: Verify Client Has Product Feeds

**Check if client has Shopping/PMax campaigns with products:**

```bash
# Use MCP Google Ads tool to check for merchant feeds
mcp__google-ads__run_gaql(
    customer_id="CUSTOMER_ID_HERE",
    query="SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.shopping_setting.merchant_id FROM campaign WHERE campaign.advertising_channel_type IN ('SHOPPING', 'PERFORMANCE_MAX') AND campaign.status = 'ENABLED'"
)
```

**What to look for:**
- If `shopping_setting.merchant_id` appears → ✅ Client has product feeds
- If no results or no merchant_id → ❌ Client cannot be added (lead gen only)

**Example Output:**
```json
{
  "campaign": {
    "name": "CPL | HSG | P Max Shopping",
    "advertisingChannelType": "PERFORMANCE_MAX",
    "shoppingSetting": {
      "merchantId": "7481296"  ← This is what you need!
    }
  }
}
```

### Step 2: Find Google Ads Customer ID

If you don't already have it:

```bash
mcp__google-ads__list_accounts()
```

Search output for client name and note the `id` field.

**Example:**
```json
{
  "id": "6281395727",
  "name": "Clear Prospects",
  "access_type": "direct"
}
```

### Step 3: Calculate Alert Thresholds

Based on client size and typical revenue, set intelligent thresholds:

**Tier 1 - Large/Premium (£1,000+ daily revenue):**
- `revenue_drop`: 800-1000
- `revenue_spike`: 1200-1500
- `click_drop_percent`: 30

**Tier 2 - Mid-Size (£200-500 daily revenue):**
- `revenue_drop`: 200-300
- `revenue_spike`: 300-400
- `click_drop_percent`: 40

**Tier 3 - Smaller (£100-200 daily revenue):**
- `revenue_drop`: 100-180
- `revenue_spike`: 150-280
- `click_drop_percent`: 45-50

**How to estimate daily revenue:**
- Check CONTEXT.md for budget info
- Review recent Google Ads spend data
- Use this formula: `monthly_budget / 30 * typical_ROAS = daily_revenue`

### Step 4: Update config.json

Add the client to `tools/product-impact-analyzer/config.json`:

```json
{
  "name": "Client Name",
  "merchant_id": "MERCHANT_ID_FROM_STEP_1",
  "google_ads_customer_id": "CUSTOMER_ID_FROM_STEP_2",
  "enabled": true,
  "monitoring_thresholds": {
    "revenue_drop": 200,
    "revenue_spike": 300,
    "click_drop_percent": 40,
    "comment": "Brief context about client size/type"
  },
  "notes": "Any important context (multi-brand, tracking issues, etc.)"
}
```

**Important:**
- Client name must match the folder name in `/clients/[client-name]/`
- Use lowercase with spaces for name (e.g., "Clear Prospects" not "clear-prospects")
- `enabled: true` to activate monitoring
- `enabled: false` to configure but not monitor yet

### Step 5: Fetch Initial Data

The Product Impact Analyzer needs 7 days of historical data to start.

**Option A: Wait for Automated Run** (Tuesday 9 AM)

The weekly analyzer will automatically fetch data for all enabled clients.

**Option B: Manual Initial Fetch** (Faster)

Create data files manually by running MCP queries:

1. **Fetch Shopping Performance Data:**

```python
# This query is too large for direct output - needs to be saved to file
# You'll need to implement a helper script or wait for automated run
customer_id = "6281395727"  # Replace with actual customer ID

query = """
SELECT
    segments.date,
    segments.product_item_id,
    segments.product_title,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions_value
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS
"""

# Save result to: tools/product-impact-analyzer/data/shopping_[client_name_lowercase].json
```

2. **Fetch Campaign Performance Data:**

```python
query = """
SELECT
    campaign.name,
    segments.date,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
    AND campaign.status = 'ENABLED'
"""

# Save result to: tools/product-impact-analyzer/data/ads_[client_name_lowercase].json
```

**File naming convention:**
- Shopping data: `shopping_clear_prospects.json` (use underscores, lowercase)
- Ads data: `ads_clear_prospects.json`

### Step 6: Test the Integration

Run the analyzer in dry-run mode to verify:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Dry run (doesn't send email)
.venv/bin/python3 run_automated_analysis.py --dry-run 2>&1 | grep -A 5 "Client Name"
```

**What to check:**
- ✅ No errors about missing data files
- ✅ Client appears in analysis output
- ✅ Product changes detected (if any)
- ✅ Thresholds logged correctly

**Common errors:**

❌ `Warning: No ads data for Client Name`
- **Fix**: Create the data files in Step 5

❌ `Error: Cannot find client 'Client Name' in config`
- **Fix**: Check client name matches exactly (case-sensitive on Linux/Mac)

❌ `Error: Merchant ID not found`
- **Fix**: Verify merchant ID is correct from Step 1

### Step 7: Test Monitoring

Run the monitor script to verify threshold detection:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Run monitor
.venv/bin/python3 monitor.py 2>&1 | grep -A 10 "Client Name"
```

**What to check:**
- ✅ Client is being monitored
- ✅ Thresholds logged: "Using thresholds for Client Name: Rev drop £X..."
- ✅ Snapshot created in `/monitoring/snapshot_client_name_*.json`
- ✅ No alerts (unless there are actual issues)

**First run behavior:**
- First monitoring run creates baseline snapshot
- No alerts on first run (needs previous snapshot for comparison)
- Second run (next day) will compare and alert if needed

### Step 8: Wait for Automated Runs

Once configured, the client will automatically be included in:

**Weekly Analysis (Tuesdays 9 AM):**
- Fetches last 7 days of product + ads data
- Runs impact analysis
- Sends HTML email report
- LaunchAgent: `com.petesbrain.product-impact-analyzer.plist`

**Daily Monitoring (Weekdays 10 AM):**
- Fetches yesterday's data
- Compares to previous day
- Sends alerts if thresholds exceeded (business hours only)
- LaunchAgent: `com.petesbrain.product-monitor.plist`

### Step 9: Update Documentation

Document the new client addition:

1. **Update this file** ([ADDING-CLIENTS.md](ADDING-CLIENTS.md)) with any lessons learned

2. **Update [PER-CLIENT-THRESHOLDS.md](PER-CLIENT-THRESHOLDS.md)** with:
   - Client tier classification
   - Threshold rationale
   - Any special notes

3. **Update client CONTEXT.md** (`/clients/[client-name]/CONTEXT.md`):
   - Add note about Product Impact Analyzer monitoring enabled
   - Document any product feed issues discovered
   - Note baseline performance for future reference

---

## Complete Example: Adding Clear Prospects

Here's the complete process used to add Clear Prospects:

### 1. Verification

```bash
# Checked for product feeds
mcp__google-ads__run_gaql(
    customer_id="6281395727",
    query="SELECT campaign.shopping_setting.merchant_id FROM campaign..."
)

# Result: Found 3 merchant IDs (multi-brand):
# - HSG (HappySnapGifts): 7481296
# - WBS (WheatyBags): 7481286
# - BMPM: 7522326
# Decision: Use HSG (7481296) as primary
```

### 2. Customer ID

```bash
mcp__google-ads__list_accounts()
# Found: "6281395727" for "Clear Prospects"
```

### 3. Thresholds

From CONTEXT.md:
- Multi-brand promotional merchandise
- Smaller accounts
- Critical GMC issues (89 products disapproved)
- Estimated £150-250/day revenue

**Set thresholds:**
- `revenue_drop`: 150 (Tier 3 - smaller account)
- `revenue_spike`: 250
- `click_drop_percent`: 45 (more sensitive due to small volume)

### 4. Config Update

Added to `config.json`:

```json
{
  "name": "Clear Prospects",
  "merchant_id": "7481296",
  "google_ads_customer_id": "6281395727",
  "enabled": true,
  "monitoring_thresholds": {
    "revenue_drop": 150,
    "revenue_spike": 250,
    "click_drop_percent": 45,
    "comment": "Multi-brand (HSG, WBS, BMPM), smaller accounts, £150-250/day est."
  },
  "notes": "Multi-brand promotional merchandise (HSG/WBS/BMPM). Using HSG merchant ID 7481296 as primary. Other merchant IDs: WBS=7481286, BMPM=7522326. Has critical GMC disapproval issues (89 products Oct 2025)."
}
```

### 5. Data Fetch

Waiting for next automated run (Tuesday 9 AM) to fetch initial data.

**Alternative**: Manually run MCP queries and save to:
- `data/shopping_clear_prospects.json`
- `data/ads_clear_prospects.json`

### 6. Testing

```bash
# Dry run test
.venv/bin/python3 run_automated_analysis.py --dry-run 2>&1 | grep "Clear Prospects"

# Output:
# [2025-10-30] ⚠ Warning: No ads data for Clear Prospects
# Expected - waiting for initial data fetch
```

### 7. Monitor Test

```bash
.venv/bin/python3 monitor.py 2>&1 | grep -A 5 "Clear Prospects"

# Output:
# [2025-10-30] Monitoring client: Clear Prospects
# [2025-10-30]   Using thresholds: Rev drop £150, Rev spike £250, Click drop 45%
# [2025-10-30]   No previous snapshot - establishing baseline
```

✅ Clear Prospects successfully configured and ready for automated monitoring!

---

## Troubleshooting

### Client Shows as Enabled But Not Analyzed

**Symptom**: Client in config with `enabled: true` but doesn't appear in reports

**Checks:**
1. Verify data files exist:
   ```bash
   ls data/shopping_*.json data/ads_*.json
   ```

2. Check file naming matches client name (lowercase, underscores):
   ```bash
   # Config: "Clear Prospects"
   # Files should be: shopping_clear_prospects.json, ads_clear_prospects.json
   ```

3. Verify data files contain data:
   ```bash
   cat data/shopping_clear_prospects.json | jq '.results | length'
   # Should show number of rows, not 0
   ```

### No Product Data Despite Having Shopping Campaigns

**Possible causes:**
1. **Wrong merchant ID**: Double-check merchant ID from campaign query
2. **No recent product performance**: Products may not have clicks in last 7 days
3. **Merchant feed issues**: Check Google Merchant Center for disapprovals
4. **Date range issue**: Query may be looking at wrong date range

**Fix:**
```bash
# Verify products exist in Merchant Center
# Check Shopping performance view has data:
mcp__google-ads__run_gaql(
    customer_id="CUSTOMER_ID",
    query="SELECT segments.product_item_id, metrics.clicks FROM shopping_performance_view WHERE segments.date DURING LAST_30_DAYS LIMIT 10"
)
```

### Alerts Not Triggering

**Checks:**
1. **Business hours only**: Alerts only send 9 AM - 6 PM weekdays
2. **Thresholds too high**: Lower thresholds if needed
3. **No previous snapshot**: First run creates baseline, alerts start on second run
4. **Monitoring disabled**: Check LaunchAgent is loaded:
   ```bash
   launchctl list | grep petesbrain
   ```

### Multi-Brand Clients

**Issue**: Client has multiple merchant IDs (like Clear Prospects with HSG, WBS, BMPM)

**Solution Options:**

**Option A - Primary Brand Only** (Used for Clear Prospects):
- Choose the largest/main brand's merchant ID
- Add notes about other brands
- Simpler setup, focuses on primary business

**Option B - Separate Entries** (More detailed):
- Create separate config entries for each brand
- Each gets own thresholds
- More granular monitoring
- More complex setup

**Recommendation**: Start with Option A, upgrade to Option B if needed.

---

## Client Addition Checklist

Use this checklist when adding a new client:

- [ ] Verify client has Shopping/PMax campaigns with product feeds
- [ ] Find Google Ads customer ID via `list_accounts()`
- [ ] Find Merchant ID from campaign query
- [ ] Check client CONTEXT.md for business context
- [ ] Calculate appropriate alert thresholds (revenue drop/spike, click %)
- [ ] Add client to `config.json` with all fields
- [ ] Set `enabled: true` or `false`
- [ ] Test with `run_automated_analysis.py --dry-run`
- [ ] Test with `monitor.py`
- [ ] Wait for automated weekly run OR manually fetch initial data
- [ ] Verify client appears in next weekly email report
- [ ] Verify monitoring snapshot created
- [ ] Update [PER-CLIENT-THRESHOLDS.md](PER-CLIENT-THRESHOLDS.md)
- [ ] Update client CONTEXT.md with monitoring status
- [ ] Document any issues or learnings in this file

---

## Summary

**Total Clients Currently Configured**: 16

**Enabled for Monitoring**: 10
- Tree2mydoor, Smythson UK, BrightMinds, Accessories for the Home
- Go Glean UK, Superspace UK, Uno Lights
- Devonshire Hotels, Godshot, Clear Prospects

**Disabled (Lead Gen / No Product Feeds)**: 6
- National Design Academy (lead gen - courses)
- OTC / Camera Manuals (on hold - client crisis)
- Print My PDF (on hold - sister business to OTC)
- WheatyBags, HappySnapGifts, BMPM (sub-brands of Clear Prospects)

**Next Steps**:
- Monitor Clear Prospects performance in first week
- Adjust thresholds if needed based on actual data
- Consider enabling sub-brands (WBS, HSG, BMPM) as separate entities if needed

---

**Version**: 1.0
**Last Updated**: October 30, 2025
**Maintained By**: Claude Code + Pete's Brain system
