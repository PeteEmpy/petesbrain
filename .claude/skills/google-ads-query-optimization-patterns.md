# Google Ads API Query Optimization Patterns

## Overview

Common optimization patterns for Google Ads GAQL queries to improve performance across all skills. These patterns reduce API calls, decrease latency, and improve skill execution speed.

---

## Pattern 1: Use IN Clause Instead of Looping (3-10x faster)

### Problem
Looping through campaigns/ad groups and making separate API calls is very slow:

```python
# ❌ SLOW - Multiple API calls
for campaign_id in campaign_ids:
    query = f"... WHERE campaign.id = {campaign_id} ..."
    response = ga_service.search(customer_id=customer_id, query=query)
    all_rows.extend(list(response))
```

**Performance:**
- 5 campaigns = 5 API calls
- Each call: ~500ms network + processing
- Total time: ~2.5 seconds minimum

### Solution
Use SQL-style `IN` clause to query multiple resources in a single call:

```python
# ✅ FAST - Single API call
campaign_ids_str = ', '.join(campaign_ids)
query = f"... WHERE campaign.id IN ({campaign_ids_str}) ..."
response = ga_service.search(customer_id=customer_id, query=query)
all_rows = list(response)
```

**Performance:**
- 5 campaigns = 1 API call
- Total time: ~500ms
- **5x faster**

### When to Use
- Querying multiple campaigns
- Querying multiple ad groups
- Any scenario with a list of IDs to fetch

### Example Use Cases
- **Text Asset Export**: Query all campaigns at once instead of per-campaign
- **Campaign Audit**: Get settings for top N campaigns in single query
- **Performance Reports**: Fetch data for multiple campaigns simultaneously
- **Budget Analysis**: Query budget data across campaign list

---

## Pattern 2: Filter at Query Level, Not in Python (2-5x faster)

### Problem
Fetching all data then filtering in Python wastes bandwidth and processing:

```python
# ❌ SLOW - Fetches too much data
query = """
    SELECT campaign.name, campaign.id
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""
response = ga_service.search(customer_id=customer_id, query=query)

# Filter in Python
gifting_campaigns = [row for row in response
                    if 'gift' in row.campaign.name.lower()]
```

### Solution
Apply filters in the GAQL query using `REGEXP_MATCH` or `LIKE`:

```python
# ✅ FAST - Filters at API level
query = """
    SELECT campaign.name, campaign.id
    FROM campaign
    WHERE campaign.status = 'ENABLED'
    AND campaign.name REGEXP_MATCH '(?i)(gift|christmas|holiday)'
"""
response = ga_service.search(customer_id=customer_id, query=query)
```

### When to Use
- Filtering by name/text patterns
- Limiting to specific date ranges
- Any filter that can be expressed in GAQL

### Benefits
- Less data transferred over network
- Less memory usage
- Faster processing

---

## Pattern 3: Only Select Fields You Need

### Problem
Selecting unnecessary fields increases response size and processing time:

```python
# ❌ SLOW - Too many fields
query = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign.start_date,
        campaign.end_date,
        campaign.serving_status,
        campaign.ad_serving_optimization_status,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros
    FROM campaign
"""
```

### Solution
Only select fields you actually use:

```python
# ✅ FAST - Minimal fields
query = """
    SELECT
        campaign.id,
        campaign.name,
        metrics.cost_micros
    FROM campaign
"""
```

### Impact
- 10 fields vs 3 fields = ~70% reduction in response size
- Faster JSON parsing
- Lower memory footprint

---

## Pattern 4: Use LIMIT for Top N Queries

### Problem
Fetching all rows when you only need top performers:

```python
# ❌ SLOW - Fetches everything
query = """
    SELECT campaign.name, metrics.cost_micros
    FROM campaign
    ORDER BY metrics.cost_micros DESC
"""
response = list(ga_service.search(customer_id=customer_id, query=query))
top_20 = response[:20]  # Only use first 20
```

### Solution
Use `LIMIT` clause in the query:

```python
# ✅ FAST - Only fetches what's needed
query = """
    SELECT campaign.name, metrics.cost_micros
    FROM campaign
    ORDER BY metrics.cost_micros DESC
    LIMIT 20
"""
response = list(ga_service.search(customer_id=customer_id, query=query))
```

### When to Use
- "Top N campaigns by spend"
- "Bottom 10 performers"
- Any scenario where you need ranked subset

---

## Pattern 5: Combine Related Queries When Possible

### Problem
Making separate queries for related data:

```python
# ❌ SLOW - 2 separate queries
query1 = "SELECT campaign.id, campaign.name FROM campaign"
campaigns = ga_service.search(customer_id=customer_id, query=query1)

query2 = "SELECT campaign.id, metrics.cost_micros FROM campaign"
performance = ga_service.search(customer_id=customer_id, query=query2)
```

### Solution
Combine into single query with all needed fields:

```python
# ✅ FAST - 1 combined query
query = """
    SELECT
        campaign.id,
        campaign.name,
        metrics.cost_micros
    FROM campaign
"""
response = ga_service.search(customer_id=customer_id, query=query)
```

### When to Use
- When fields come from same resource (campaign, ad_group, etc.)
- When date ranges are identical
- When filters/conditions are the same

---

## Pattern 6: Cache Account-Level Data

### Problem
Re-querying static data on every skill run:

```python
# ❌ SLOW - Queries account info every time
def get_campaigns():
    query = "SELECT campaign.id, campaign.name FROM campaign"
    return ga_service.search(customer_id, query)
```

### Solution
Cache data that doesn't change frequently:

```python
# ✅ FAST - Cache campaign list
_campaign_cache = {}

def get_campaigns(customer_id, force_refresh=False):
    cache_key = f"{customer_id}_campaigns"

    if not force_refresh and cache_key in _campaign_cache:
        return _campaign_cache[cache_key]

    query = "SELECT campaign.id, campaign.name FROM campaign"
    campaigns = list(ga_service.search(customer_id, query))

    _campaign_cache[cache_key] = campaigns
    return campaigns
```

### When to Use
- Campaign names/IDs (rarely change)
- Account settings
- Customer hierarchy
- Static configuration data

### When NOT to Use
- Metrics (constantly changing)
- Bid/budget data (frequently updated)
- Status fields (can change often)

---

## Pattern 7: Enable Asset Status Filtering (Critical for Accuracy)

### Problem
Querying assets without filtering by status includes REMOVED/PAUSED assets:

```python
# ❌ WRONG - Includes removed assets
query = """
    SELECT
        asset_group.name,
        asset.text_asset.text
    FROM asset_group_asset
    WHERE asset_group.status = 'ENABLED'
"""
```

**Result:** Shows 29 headlines when Google Ads limit is 15 (includes 14 removed)

### Solution
Always filter BOTH asset_group AND asset_group_asset status:

```python
# ✅ CORRECT - Only active assets
query = """
    SELECT
        asset_group.name,
        asset.text_asset.text
    FROM asset_group_asset
    WHERE asset_group.status = 'ENABLED'
    AND asset_group_asset.status = 'ENABLED'  # Critical!
"""
```

**Result:** Shows exactly 15 active headlines (Google Ads limit)

### When to Use
- **Always** when querying asset_group_asset table
- Any asset-related query (images, videos, text, etc.)
- PMAX campaign asset audits

### Why It Matters
- Historical assets remain in the account with REMOVED status
- Without this filter, you'll see duplicates and incorrect counts
- Causes confusion when comparing to Google Ads UI

---

## Skill-Specific Applications

### google-ads-text-asset-exporter
- ✅ Pattern 1: Use IN clause for campaign IDs
- ✅ Pattern 3: Only select needed fields (campaign.name, asset.text_asset.text)
- ✅ Pattern 7: Filter asset_group_asset.status = 'ENABLED'

### google-ads-campaign-audit
- ✅ Pattern 1: Query top N campaigns in single call
- ✅ Pattern 4: Use LIMIT for spend concentration analysis
- ✅ Pattern 5: Combine settings + metrics in same query

### google-ads-keyword-audit (future)
- Pattern 1: Use IN clause for ad group IDs
- Pattern 2: Filter keywords by match type at query level
- Pattern 4: LIMIT to top performing keywords

### google-ads-performance-reporter (future)
- Pattern 1: Query multiple campaigns at once
- Pattern 2: Filter by date range in GAQL
- Pattern 6: Cache campaign structure

---

## Implementation Checklist

When writing a new Google Ads skill, verify:

- [ ] Are you looping through IDs? → Use IN clause instead
- [ ] Filtering in Python? → Move filters to GAQL WHERE clause
- [ ] Selecting all fields? → Reduce to only needed fields
- [ ] Need top N? → Use LIMIT in query
- [ ] Multiple related queries? → Combine into one
- [ ] Querying static data repeatedly? → Add caching
- [ ] **Querying assets? → MUST filter asset_group_asset.status = 'ENABLED'**

---

## Performance Comparison

### Example: Text Asset Export for 5 Campaigns

**Before optimization:**
- 5 separate queries (one per campaign)
- Each query: ~500ms
- Total time: ~2.5 seconds
- Data transferred: ~500KB

**After optimization:**
- 1 combined query with IN clause
- Single query: ~600ms
- Total time: ~600ms
- Data transferred: ~500KB

**Result: 4x faster** (2.5s → 0.6s)

---

## References

- Google Ads GAQL Reference: https://developers.google.com/google-ads/api/docs/query/overview
- IN Operator: https://developers.google.com/google-ads/api/docs/query/operators
- REGEXP_MATCH: https://developers.google.com/google-ads/api/docs/query/operators#regexp_match
- Performance Best Practices: https://developers.google.com/google-ads/api/docs/best-practices

---

## Last Updated
2025-11-10 - Added Pattern 7 (Asset Status Filtering) based on critical bug fix
