# GAQL Query Reference

## Quick Reference Guide for Google Ads Query Language

### Core Resources

| Resource | Use For | Key Fields |
|----------|---------|------------|
| `campaign` | Campaign metrics | name, id, status, bidding_strategy_type |
| `ad_group` | Ad group metrics | name, id, status, campaign |
| `shopping_performance_view` | Shopping products | segments.product_title, product_item_id |
| `search_term_view` | Search queries | segments.search_term |
| `keyword_view` | Keyword data | ad_group_criterion.keyword.text |
| `ad_group_ad` | Ad performance | ad.final_urls, ad.type |

### Essential Metrics

| Metric | Field Name | Notes |
|--------|------------|-------|
| Impressions | `metrics.impressions` | Raw count |
| Clicks | `metrics.clicks` | Raw count |
| Cost | `metrics.cost_micros` | Divide by 1M for dollars |
| Conversions | `metrics.conversions` | Decimal value |
| Conv Value | `metrics.conversions_value` | Already in dollars |
| CTR | `metrics.ctr` | Decimal (0.05 = 5%) |
| CPC | `metrics.average_cpc` | In micros |
| ROAS | N/A | Calculate: conversions_value / (cost_micros/1M) |

### Date Periods

```sql
WHERE segments.date DURING LAST_7_DAYS
WHERE segments.date DURING LAST_30_DAYS
WHERE segments.date DURING THIS_MONTH
WHERE segments.date DURING LAST_MONTH
WHERE segments.date DURING THIS_YEAR
WHERE segments.date BETWEEN '2024-01-01' AND '2024-01-31'
```

### Status Filters

```sql
WHERE campaign.status = 'ENABLED'
WHERE campaign.status IN ('ENABLED', 'PAUSED')
WHERE ad_group.status = 'ENABLED'
```

### Common Segments

| Segment | Use For |
|---------|---------|
| `segments.date` | Daily breakdown |
| `segments.week` | Weekly data (YYYY-MM-DD of Monday) |
| `segments.month` | Monthly data (YYYY-MM) |
| `segments.device` | Device type (MOBILE, DESKTOP, TABLET) |
| `segments.conversion_action_name` | Conversion type |
| `segments.product_title` | Product name |
| `segments.product_item_id` | Product ID |

### Performance Max Notes

Performance Max campaigns have limited segmentation:
- ✅ Campaign-level metrics work
- ✅ Asset group metrics work (use `campaign_asset_group` resource)
- ❌ Product-level requires `shopping_performance_view`
- ❌ Limited placement visibility

### Cost Conversion

Always remember:
```
Actual Cost = metrics.cost_micros / 1,000,000
Actual CPC = metrics.average_cpc / 1,000,000
```

### Query Limits

- Default limit: 10,000 rows
- Use `LIMIT` clause to restrict results
- Use `ORDER BY` for most relevant results first
- Pagination available via API (not in GAQL syntax)

### Best Practices

1. **Always filter by date** - Queries without date filters are slow
2. **Filter by status** - Include `campaign.status = 'ENABLED'` to exclude removed campaigns
3. **Use LIMIT** - Especially for large accounts
4. **Order by spend** - Most relevant results first
5. **Validate fields** - Check that resource supports the fields you're selecting

