# Merchant API Access Issue & Solution

## Problem

The Merchant API requires the service account to be explicitly added as a user to each Merchant Center account with "Standard" or "Admin" access.

**Error**: `401 The caller does not have access to the accounts: [107469209]`

This is a **breaking change** from the deprecated Content API for Shopping, which allowed broader access via OAuth.

## Why This Happened

1. **Merchant API** (new) requires per-account user permissions
2. **Content API for Shopping** (deprecated) worked with our existing service account
3. Google forced the migration by deprecating the old API

## Solution Options

### Option 1: Use Google Ads API for Product Data (RECOMMENDED)

**Pros**:
- Service account already has access (we're using Google Ads API)
- No additional setup required
- Works immediately

**Cons**:
- Only provides product data for products with impressions in Google Ads
- May miss recently added products or products with zero impressions

**Implementation**: Query Google Ads API for Shopping product data:
```python
# GAQL query to fetch product attributes
query = """
    SELECT
        segments.product_item_id,
        segments.product_title,
        segments.product_brand,
        segments.product_type_l1,
        segments.product_custom_label0,
        segments.product_custom_label1,
        segments.product_custom_label2,
        segments.product_custom_label3,
        segments.product_custom_label4
    FROM shopping_performance_view
    WHERE segments.date = 'YESTERDAY'
"""
```

This gives us most product attributes we track, and captures all products that have any Google Ads activity.

### Option 2: Add Service Account to All Merchant Center Accounts (MANUAL)

**Steps** (repeat for each of 15 clients):
1. Log into Merchant Center account
2. Go to **Settings** > **Users**
3. Click **Add User**
4. Add email: `petesbrain-emailsync@petesbrain-emailsync.iam.gserviceaccount.com`
5. Set access level: **Standard** or **Admin**
6. Save

**Pros**:
- Full access to all product attributes
- Includes products with zero impressions

**Cons**:
- Manual setup required for 15 accounts
- Client approval may be needed
- Ongoing maintenance (new accounts require setup)

### Option 3: Revert to Content API for Shopping (TEMPORARY)

Google hasn't fully disabled the Content API yet. We could revert temporarily.

**Pros**:
- Works immediately
- No additional setup

**Cons**:
- **Will stop working** when Google fully deprecates the API
- Not a long-term solution

## Recommended Path Forward

**Use Option 1: Google Ads API for Product Data**

**Reasoning**:
1. **Works immediately** - no setup required
2. **Captures what matters** - products with Google Ads activity are the products we care about for performance analysis
3. **Already implemented** - we're using Google Ads API for performance data
4. **More reliable** - fewer moving parts, one API instead of two

**Trade-off accepted**:
- We may miss newly added products with zero impressions
- This is acceptable because our goal is to track product *performance* and *changes that affect performance*
- Products with zero impressions by definition have no performance to analyze

## Implementation Plan

I'll update `product_feed_tracker.py` to use the Google Ads API instead of Merchant API.

**Query approach**:
- Query `shopping_performance_view` for yesterday's date
- Extract unique product IDs and attributes
- Store as daily snapshot (same format as current)
- Change detection works identically

**Benefits**:
- No breaking changes to rest of system
- Same snapshot format
- Works with existing LaunchAgents
- Minimal code changes

---

**Decision**: Proceed with Option 1 (Google Ads API) unless you prefer Option 2 (manual Merchant Center setup).
