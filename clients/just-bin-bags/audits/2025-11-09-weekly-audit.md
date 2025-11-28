# Google Ads Audit: Just Bin Bags

**Date Range**: Last 7 days (Nov 2-9, 2025)  
**Audit Date**: November 9, 2025  
**Customer ID**: 9697059148  
**Status**: ✅ Complete

---

## Executive Summary

**Account Overview**: Just Bin Bags operates two Performance Max campaigns for their main brand (JBB) and sub-brand (JHD). Both campaigns target 200% ROAS based on campaign naming convention.

**Key Metrics** (Last 7 Days):
- **Campaigns Active**: 2 Performance Max campaigns
- **Merchant Centers**: 
  - Main brand (JBB): 181788523
  - Sub-brand (JHD): 5085550522

**Note**: Live performance data requires MCP Google Ads connection. This audit provides framework and analysis structure.

---

## Campaign Performance

### Active Campaigns

1. **JBB | P Max 200 21/5**
   - **Type**: Performance Max
   - **Merchant ID**: 181788523 (Main brand)
   - **ROAS Target**: 200% (indicated by "200" in name)
   - **Created**: May 21, 2025 (likely)
   - **Status**: Active

2. **JBB | JHD | P Max Shopping**
   - **Type**: Performance Max  
   - **Merchant ID**: 5085550522 (JHD sub-brand)
   - **Status**: Active

### Campaign Analysis Needed

**To complete this section, fetch live data:**
```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

**Key Questions**:
- Are both campaigns meeting the 200% ROAS target?
- Which campaign (JBB vs JHD) is performing better?
- Is budget allocation optimal between campaigns?

---

## Product-Level Performance

### Product Hero Labelizer Status

**Check Required**: Verify if Product Hero Labelizer is implemented
- Look for `custom_label_0` field in product data
- Check if campaigns use label-based asset groups

**Expected Analysis**:
```sql
SELECT
  segments.product_custom_attribute0,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS
  AND segments.product_custom_attribute0 IN ('heroes', 'sidekicks', 'villains', 'zombies')
```

### Top Products Analysis Needed

**Query for Top 10 Products**:
```sql
SELECT
  segments.product_item_id,
  segments.product_title,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.ctr
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.conversions_value DESC
LIMIT 10
```

**Analysis Points**:
- Identify top revenue-generating products
- Flag products with low ROAS (< 1.5x)
- Check for products with zero conversions but high spend
- Compare JBB vs JHD product performance

---

## Placement Analysis

### Performance Max Placements

Performance Max campaigns serve across multiple placements:
- Shopping tab
- YouTube
- Display Network
- Discover
- Gmail
- Search Partners

**Query for Placement Data**:
```sql
SELECT
  segments.placement,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.ctr
FROM placement_view
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.cost_micros DESC
```

**Key Questions**:
- Which placements drive highest ROAS?
- Are any placements wasting budget?
- Should we exclude underperforming placements?

---

## Budget & Spend Efficiency

### Campaign Budget Analysis

**Check Required**:
- Daily budget allocation between campaigns
- Budget pacing (are campaigns hitting daily caps?)
- Budget efficiency (spend vs performance)

**Questions**:
- Is budget split optimally between JBB and JHD?
- Are campaigns constrained by budget?
- Should budget be reallocated based on performance?

---

## Product Impact Analyzer Integration

**Status**: ⚠️ Not Currently Tracked

Just Bin Bags is not currently configured in Product Impact Analyzer. 

**Recommendation**: Enable Product Impact Analyzer to track:
- Product feed changes (price, stock, titles)
- Correlation between feed changes and performance
- Product-level revenue impact analysis

**Setup Required**:
1. Add Just Bin Bags to `tools/product-impact-analyzer/config.json`
2. Configure merchant IDs: 181788523 (JBB), 5085550522 (JHD)
3. Set up product performance spreadsheets
4. Enable daily monitoring

---

## Root Cause Analysis

### Known Issues to Investigate

1. **JHD Sub-brand Purpose**
   - **Question**: What does JHD represent?
   - **Impact**: Understanding brand structure affects strategy
   - **Action**: Research or ask client about JHD brand

2. **ROAS Target Validation**
   - **Question**: Is 200% ROAS target appropriate?
   - **Impact**: Campaign optimization direction
   - **Action**: Verify target with client, check if being met

3. **Conversion Tracking**
   - **Question**: Is conversion tracking properly configured?
   - **Impact**: Data accuracy for optimization
   - **Action**: Audit conversion setup

4. **Product Feed Quality**
   - **Question**: Are product feeds optimized?
   - **Impact**: Shopping campaign performance
   - **Action**: Review Merchant Center feeds

---

## Prioritized Recommendations

### 1. Fetch Live Performance Data - HIGH PRIORITY
**Action**: Execute GAQL queries via MCP to get current performance metrics
**Impact**: Foundation for all other recommendations
**Effort**: Low (if MCP connected)

### 2. Enable Product Impact Analyzer - HIGH PRIORITY  
**Action**: Configure Just Bin Bags in Product Impact Analyzer
**Impact**: Track feed changes and correlate with performance
**Effort**: Medium (one-time setup)

### 3. Clarify JHD Brand Strategy - MEDIUM PRIORITY
**Action**: Research or ask client about JHD sub-brand purpose
**Impact**: Better campaign strategy and budget allocation
**Effort**: Low

### 4. Review ROAS Targets - MEDIUM PRIORITY
**Action**: Verify if 200% ROAS target is appropriate and being met
**Impact**: Campaign optimization direction
**Effort**: Low

### 5. Audit Conversion Tracking - MEDIUM PRIORITY
**Action**: Review conversion setup and verify data accuracy
**Impact**: Reliable performance data
**Effort**: Medium

### 6. Product-Level Optimization - ONGOING
**Action**: Analyze product performance and optimize budget allocation
**Impact**: Improved ROAS and revenue
**Effort**: Ongoing

---

## Next Steps

1. ✅ **Audit Template Created** - Framework ready for data population
2. ⏳ **Fetch Live Data** - Execute GAQL queries via MCP or Google Ads UI
3. ⏳ **Enable Product Impact Analyzer** - Set up feed change tracking
4. ⏳ **Complete Analysis** - Populate audit with live performance data
5. ⏳ **Generate Action Items** - Create tasks for recommendations
6. ⏳ **Update CONTEXT.md** - Document findings and learnings

---

## Data Sources

- **Google Ads Account**: 9697059148
- **Merchant Centers**: 
  - JBB: 181788523
  - JHD: 5085550522
- **Product Performance Spreadsheets**:
  - JBB: https://docs.google.com/spreadsheets/d/1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA/
  - JHD: https://docs.google.com/spreadsheets/d/1p7hVR4bwMVTiBj8za6pVv3kmnVr8v3YEz2fhGun2YSk/
- **Client Context**: `clients/just-bin-bags/CONTEXT.md`

---

## Follow-Up Questions

1. What does the JHD sub-brand represent? (Different product line? Geographic variant?)
2. Is the 200% ROAS target appropriate for this account?
3. Are conversion tracking and attribution properly configured?
4. Should Product Impact Analyzer be enabled for feed change tracking?
5. What are the business goals and priorities for Q4 2025?

---

**Audit Status**: Framework complete. Ready for live data population via MCP or manual data entry.

**Next Audit**: Schedule follow-up after live data analysis

