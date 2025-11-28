# Quick Re-Index Guide for Merchant Center Disapprovals

**Problem**: Products disapproved due to "page not found" or caching issues on client website
**Solution**: Immediate re-index through Merchant Center
**Monitoring**: Every 6 hours (6 AM, 12 PM, 6 PM, 12 AM)

## Why This Happens

Some websites have caching issues that cause Google's crawler to get:
- **404 errors** (page not found)
- **Empty pages** (cached blank response)
- **Desktop-only issues** (mobile works, desktop fails)

When Google crawls and gets these errors, it disapproves the product with:
- Issue code: `landing_page_error` or `page_not_found`
- Description: "Cannot access product landing page on desktop"

## Quick Fix Process

### 1. Get Alert (Every 6 Hours)

You'll receive email alert:
```
🚨 Merchant Center Disapproval Alert

🔥 CRITICAL ISSUES
Client X - Product 123
  Issue: landing_page_error
  Cannot access product landing page on desktop
  Resolution: Verify URL is accessible
```

### 2. Verify the Issue

Check if it's a caching issue (not real 404):
```bash
# Test the URL yourself
curl -I "https://client-website.com/product-page"

# Should return 200 OK if page actually exists
```

If you get 200 OK but Google got 404 = caching issue.

### 3. Request Re-Index (Immediate)

**Option A: Via Merchant Center UI** (Fastest)
1. Go to [Google Merchant Center](https://merchants.google.com/)
2. Products → All Products
3. Find the affected product(s)
4. Click "Request Review" button
5. Google will re-crawl within minutes

**Option B: Via Content API** (Bulk, automated - future enhancement)
```bash
# Not yet implemented - requires API call
# POST /content/v2.1/merchantId/products/productId/reindex
```

### 4. Monitor for Re-Approval

Products are usually re-approved within:
- **1-4 hours** if it's a caching issue
- **24 hours** if it's a real fix needed

Next disapproval check (in 6 hours) will detect if re-approved.

## Identifying Caching Issues

**Signs it's a caching issue (not real 404)**:
- ✅ URL works when you test it manually
- ✅ Same products repeatedly disapproved and re-approved
- ✅ Happens in waves (multiple products at once)
- ✅ Only affects desktop (mobile works fine)
- ✅ Client hasn't changed anything

**Signs it's a real issue**:
- ❌ URL returns 404 when you test it
- ❌ Product was actually removed/discontinued
- ❌ URL structure changed
- ❌ Website is down

## Client-Specific Notes

**Clients with recurring caching issues:**

### Clear Prospects (All Brands)
- **Brands Affected**: HappySnapGifts, WheatyBags, BMPM
- **Issue**: Desktop caching causing intermittent 404s - "Cannot access product landing page on desktop"
- **Root Cause**: Website caching configuration (pages load fine manually, fail for Google crawler)
- **Frequency**: Recurring issue, requires monitoring
- **Solution**: Immediate re-index request in Merchant Center when detected
- **Monitoring**: Every 6 hours (6 AM, 12 PM, 6 PM, 12 AM) to catch quickly
- **Prevention**: Working with client to resolve caching configuration
- **Note**: This is why 6-hourly checks were implemented instead of daily

## Automation Opportunities

### Current: Manual Re-Index
1. Get alert → 2. Check issue → 3. Request review in UI

### Future: Auto Re-Index (Phase 4?)
1. Get alert → 2. Script detects `landing_page_error` → 3. Auto-test URL → 4. If 200 OK, auto-request re-index

**Implementation**:
```python
# Pseudo-code for future enhancement
if issue_code == 'landing_page_error':
    url = product['link']
    response = requests.head(url)

    if response.status_code == 200:
        # URL works - likely caching issue
        # Auto-request re-index via Content API
        merchant_center_api.request_review(merchant_id, product_id)
        log("Auto-requested re-index for product {product_id}")
```

## Manual Commands

### Check Specific Client Now
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
.venv/bin/python3 disapproval_monitor.py --client "ClientName" --test
```

### Generate Full Disapproval Report
```bash
.venv/bin/python3 merchant_center_tracker.py --client "ClientName" --report
```

### Check URL Accessibility (Bulk)
```bash
# Extract URLs from disapproval report and test
# Future script: test_product_urls.py
```

## Best Practices

1. **Respond quickly** - 6-hourly checks mean you catch issues fast
2. **Document patterns** - Note which products repeatedly affected
3. **Client communication** - Let client know about caching issues
4. **Fix root cause** - Work with client to resolve caching (CDN config, server headers, etc.)
5. **Track resolution time** - How long from disapproval to re-approval?

## Troubleshooting

### Alert Not Received?
- Check business hours (alerts only 9 AM - 6 PM weekdays)
- Night/weekend disapprovals won't alert until next business day
- Check logs: `tail -f ~/.petesbrain-disapproval-monitor.log`

### Can't Find Product in Merchant Center?
- Search by product ID (the numeric part after `online:en:GB:`)
- Use Products → Diagnostics tab
- Filter by "Disapproved" status

### Re-Index Not Working?
- Wait 4 hours after requesting review
- Check if it's still actually disapproved (not caching on Google's end)
- Verify URL really works (test from different location/device)

## API Rate Limits

**Google Content API for Shopping**:
- **Rate limit**: 1000 queries per 100 seconds per project
- **Daily limit**: Millions of requests (effectively unlimited for our use)

**Our usage (15 clients, 6-hourly checks)**:
- ~15 API calls per check (one per client)
- 4 checks per day = 60 API calls/day
- **Well within limits** ✅

Even checking every client every hour would only be ~360 calls/day = totally fine.

## Summary

**Monitoring frequency**: Every 6 hours
**Alert latency**: Max 6 hours from disapproval to alert
**Fix time**: 1-4 hours from re-index request to re-approval
**Total resolution time**: Usually <10 hours from disapproval to re-approval

For caching issues, this is **fast enough** to prevent significant performance impact while avoiding API overload.

---

**Last Updated**: October 30, 2025
**Status**: 6-hourly monitoring configured
