# Product Hero Label Tracking - 100% Coverage Solution

## Problem Statement

User needs **100% product-level tracking** for label transitions. Even one product moving between Hero/Sidekick/Villain/Zombie segments can explain major performance shifts.

**Partial coverage (50%) is NOT acceptable** - we need complete product inventory for accurate attribution.

## Challenge

**MCP Token Limit**: 25,000 tokens maximum per response
**GAQL Limitations**:
- ❌ No OFFSET support for pagination
- ❌ No comparison operators (>, <) on product_item_id
- ❌ Cannot filter products by ID ranges
- ❌ LIMIT alone fetches all data, then truncates (still hits token limit)

## Proposed Solutions

### Option 1: Multi-Day Rotation with Date Segmentation ⭐ RECOMMENDED

**Strategy**: Query different date ranges to segment products

```sql
-- Day 1: Products with impressions in days 1-2
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND metrics.impressions > 0
LIMIT 500

-- Day 2: Products with impressions in days 3-4
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND metrics.impressions > 0
LIMIT 500

-- Day 3: Products with impressions in days 5-7
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND metrics.impressions > 0
LIMIT 500
```

**Pros**:
- Naturally segments products by recency
- Works within GAQL limitations
- Deduplicates automatically (products appear in multiple days)

**Cons**:
- Only tracks products WITH recent impressions
- Products with zero impressions won't appear
- May miss inactive products (but those aren't in campaigns anyway)

**Coverage**: ~80-90% of ACTIVE products over 3-day cycle

### Option 2: Weekly Full Export via Google Ads UI

**Strategy**: Manual export from Google Ads UI weekly

1. Google Ads UI → Reports → Predefined → Shopping
2. Select: Product ID + Custom Label fields
3. Date range: Last 30 days
4. Export CSV (no token limits in UI)
5. Process CSV to extract labels

**Pros**:
- 100% coverage guaranteed
- No token limits
- Works for any account size

**Cons**:
- Manual step required
- Weekly frequency (not daily)
- Requires UI access

**Coverage**: 100% of products with impressions in last 30 days

### Option 3: Google Ads API with Pagination ⭐ BEST (requires custom implementation)

**Strategy**: Use Google Ads API directly (not via MCP) with proper pagination support

The Google Ads API supports `page_token` for pagination:

```python
from google.ads.googleads.client import GoogleAdsClient

def fetch_all_labels(customer_id):
    client = GoogleAdsClient.load_from_storage()
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          segments.product_item_id,
          segments.product_custom_attribute1
        FROM shopping_performance_view
        WHERE segments.date DURING LAST_7_DAYS
          AND metrics.impressions > 0
    """

    all_labels = {}
    page_token = None

    while True:
        request = client.get_type("SearchGoogleAdsRequest")
        request.customer_id = customer_id
        request.query = query
        request.page_size = 1000

        if page_token:
            request.page_token = page_token

        response = ga_service.search(request=request)

        for row in response:
            product_id = row.segments.product_item_id
            label = row.segments.product_custom_attribute1
            all_labels[product_id] = label

        page_token = response.next_page_token
        if not page_token:
            break

    return all_labels
```

**Pros**:
- 100% coverage guaranteed
- Automated (no manual steps)
- Proper pagination support
- Works for any account size

**Cons**:
- Requires custom Google Ads API implementation
- Cannot use existing MCP integration
- More complex setup

**Coverage**: 100% of all active products

### Option 4: Hybrid - MCP for Small, API for Large

**Strategy**:
- Small/medium accounts (< 500 products): Use existing MCP approach ✓
- Large accounts (> 500 products): Use Google Ads API with pagination

**Implementation**:
```python
if estimated_products < 500:
    # Use MCP (simple, already working)
    use_mcp_integration()
else:
    # Use Google Ads API (paginated, 100% coverage)
    use_google_ads_api_direct()
```

**Pros**:
- Best of both worlds
- Simple for most clients
- 100% coverage when needed

**Cons**:
- Two different code paths to maintain
- Requires Google Ads API setup for large accounts

**Coverage**: 100% for all clients

## Recommendation

**Immediate (Today)**: Implement **Option 1** (Date Segmentation Rotation)
- Gets us 80-90% coverage quickly
- Works within MCP constraints
- Better than 50% partial coverage

**Long-term (This Week)**: Implement **Option 3** (Google Ads API Direct)
- Provides 100% coverage
- Future-proof for any account size
- Worth the implementation effort

## Implementation Plan

### Phase 1: Date Segmentation (2-3 hours)

1. **Create rotation script** with date-based queries
2. **Test with Uno Lighting**:
   - Day 1: Last 2 days of impressions
   - Day 2: Days 3-4 of impressions
   - Day 3: Days 5-7 of impressions
3. **Merge and deduplicate** results
4. **Measure coverage**: Compare to known product count

### Phase 2: Google Ads API Direct (4-6 hours)

1. **Set up Google Ads API client** (if not already configured)
2. **Implement paginated fetch** function
3. **Test with large accounts** (Uno Lighting, AFH)
4. **Migrate all clients** to new approach
5. **Deprecate MCP label queries** (or keep for small accounts)

## Coverage Goals

**Minimum Acceptable**: 80% (Option 1 - Date Segmentation)
**Target**: 100% (Option 3 - Google Ads API)

## Questions to Answer

1. **How many products per account?** (determines urgency of 100% vs 80%)
2. **How often do products get zero impressions?** (affects Option 1 coverage)
3. **Is weekly manual export acceptable short-term?** (Option 2 as bridge)
4. **Do we have Google Ads API already set up?** (for Option 3)

## Next Steps

**User Decision Required**:
- A) Proceed with 80-90% coverage (date segmentation) - Fast
- B) Invest in 100% coverage (Google Ads API direct) - Best long-term
- C) Use weekly manual exports as bridge - Practical compromise

Once decided, I can implement the chosen approach.
