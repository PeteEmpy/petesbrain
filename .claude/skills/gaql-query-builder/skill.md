---
name: gaql-query-builder
description: Constructs Google Ads Query Language (GAQL) queries for data extraction and custom reports. Use when building GAQL queries, pulling Google Ads metrics, requesting custom reports, or discussing Google Ads API data extraction.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Read
---

# GAQL Query Builder Skill

## Instructions

When this skill is triggered:

1. **Identify the data need**: Understand what metrics, dimensions, and resources the user wants
2. **Determine the resource**: Campaign, ad_group, ad_group_ad, keyword_view, shopping_performance_view, etc.
3. **Build the query**: Construct syntactically correct GAQL following these rules:

### GAQL Query Structure
```
SELECT 
  [resource_name].[field],
  metrics.[metric_name],
  segments.[segment_name]
FROM [resource_name]
WHERE [conditions]
ORDER BY [field] ASC|DESC
LIMIT [number]
```

### Key Resources
- `campaign` - Campaign-level data
- `ad_group` - Ad group data
- `ad_group_ad` - Ad-level data
- `keyword_view` - Search keyword data
- `shopping_performance_view` - Shopping campaign product data
- `search_term_view` - Search query data
- `product_group_view` - Product group data
- `campaign_criterion` - Campaign-level targeting
- `ad_group_criterion` - Ad group-level targeting

### Common Metrics
- `metrics.impressions`
- `metrics.clicks`
- `metrics.cost_micros` (divide by 1,000,000 for actual cost)
- `metrics.conversions`
- `metrics.conversions_value`
- `metrics.ctr`
- `metrics.average_cpc`
- `metrics.search_impression_share`
- `metrics.search_budget_lost_impression_share`
- `metrics.search_rank_lost_impression_share`

### Common Segments
- `segments.date` - Date breakdown
- `segments.day_of_week` - Day of week (MONDAY, TUESDAY, etc.)
- `segments.device` - Device type
- `segments.conversion_action_name` - Conversion action
- `segments.product_title` - Product name (Shopping)
- `segments.product_item_id` - Product ID (Shopping)

### Date Filtering
Use `segments.date` with `BETWEEN` or `DURING`:
```
WHERE segments.date BETWEEN '2024-01-01' AND '2024-01-31'
WHERE segments.date DURING LAST_7_DAYS
WHERE segments.date DURING THIS_MONTH
WHERE segments.date DURING LAST_30_DAYS
```

### Campaign Status Filtering
```
WHERE campaign.status = 'ENABLED'
WHERE ad_group.status IN ('ENABLED', 'PAUSED')
```

4. **Validate the query**: Ensure:
   - Resource name matches fields selected
   - All field names are correct
   - Date ranges use proper format
   - Cost values note micros conversion
   - Status filters use proper ENUM values

5. **Execute via MCP**: If MCP is connected, offer to run the query using:
   ```
   mcp__google-ads__run_gaql(customer_id, query)
   ```

6. **Explain the query**: Briefly describe what data will be returned

## Example Queries

### Weekly Campaign Performance
```sql
SELECT 
  campaign.name,
  campaign.id,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

### Product-Level Shopping Performance
```sql
SELECT 
  segments.product_title,
  segments.product_item_id,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM shopping_performance_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.conversions_value DESC
LIMIT 100
```

### Search Terms Analysis
```sql
SELECT 
  segments.search_term,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions,
  metrics.cost_micros
FROM search_term_view
WHERE segments.date DURING LAST_14_DAYS
  AND campaign.status = 'ENABLED'
  AND metrics.impressions > 10
ORDER BY metrics.impressions DESC
```

### Impression Share Analysis
```sql
SELECT 
  campaign.name,
  metrics.impressions,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.search_budget_lost_impression_share DESC
```

## Integration with MCP

This skill works seamlessly with the Google Ads MCP server at `shared/mcp-servers/google-ads-mcp-server/`.

When building queries:
1. Check if MCP is connected
2. Offer to execute the query immediately
3. Format results in readable tables
4. Suggest follow-up analyses based on results

## Resources

- [GAQL Reference](query-reference.md) - Complete field reference
- [Common Patterns](common-patterns.md) - Frequently used query patterns
- [Google Ads MCP Docs](../../../docs/MCP-SERVERS.md#google-ads-mcp-server)

## Notes

- Always convert `cost_micros` to dollars by dividing by 1,000,000
- `conversions_value` is already in currency units
- Date segments require filtering by date range
- Some resources have field limitations (check resource documentation)
- Performance Max campaigns have limited segmentation options

