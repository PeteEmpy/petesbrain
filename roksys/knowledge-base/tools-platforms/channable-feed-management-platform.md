# Channable: Product Feed Management Platform

**Platform Type**: Multichannel eCommerce Feed Management
**Primary Use**: Product feed optimization for Google Shopping, marketplaces, and advertising platforms
**Trusted By**: 11,000+ companies
**Website**: channable.com

## Overview

Channable is a centralized feed management platform that enables agencies and e-commerce businesses to manage product listings, advertising, and optimization across multiple online channels from a single interface. The platform serves as an intermediary between product data sources (e-commerce platforms, spreadsheets, databases) and advertising channels (Google Shopping, Meta, marketplaces).

**Core Functionality**: Import raw product data from any source → Apply intelligent rules and transformations → Export optimized feeds to any channel format

## Key Features

### 1. Data Import & Sources
- Connect to any data source (XML, CSV, JSON, API)
- Direct integrations with major e-commerce platforms (Shopify, Magento 2, WooCommerce, etc.)
- Google Sheets support (must be set to public for Channable to fetch)
- Feed merging capabilities using matching identifiers

### 2. Rules Engine (Core Value)
Channable's "intelligent and intuitive AI rule system" processes product data using IF-THEN logic:

**Rule Types**:
- **Filling Rules**: Apply same value to all products (e.g., set all items to "in stock")
- **Search Rules**: Extract data from other fields (e.g., find size in title)
- **Exclusion Rules**: Remove products that don't meet criteria
- **Modification Rules**: Transform data (e.g., price adjustments, title optimization)
- **Master Rules**: Apply rule groups across multiple exports

**Example Rules**:
```
IF price is empty THEN exclude product
IF GTIN is missing THEN set identifier_exists to FALSE
IF category contains "shoes" THEN set custom_label_0 to "Footwear"
```

### 3. Quality Assurance
- **Instant Feed Quality Checks**: Identifies errors before export
- **Error Classification**: Mandatory (must fix), Recommended (improves visibility), Optional (supplementary)
- **70-80% Error Reduction**: Channable instantly filters out errors on import
- **GTIN Validation**: Built-in rule to identify valid/invalid GTINs
- **Image Detection**: Rule to identify products missing images

### 4. Google Shopping / Merchant Center Integration

**Two Integration Methods**:
1. **Live API**: Real-time synchronization with Google Merchant Center
2. **Feed Updates**: Periodic feed uploads (scheduled)

**Key Capabilities**:
- Automatic field mapping to Google Shopping requirements
- All mandatory fields formatted correctly
- Real-time performance insights (CTR, conversion rate) within Channable dashboard
- Support for Merchant Center Next
- CSS (Comparison Shopping Service) functionality

### 5. Multi-Channel Support
- 3,000+ channel-specific feed templates
- Automated format conversion for different channels
- Dynamic stock and promotion updates
- Separate optimizations per channel from single data source

## Google Shopping: Common Issues & Solutions

### Top 10 Errors (From Channable Documentation)

#### 1. **Invalid GTIN**
- **Cause**: GTINs don't meet format requirements
- **Solution**: Use GTIN validation rule to identify and exclude invalid codes

#### 2. **Insufficient Product Identifiers**
- **Cause**: Missing 2 of 3 required attributes (GTIN, brand, MPN)
- **Solution**: Set "identifier_exists" field to FALSE if GTIN or MPN absent

#### 3. **Item Requires a GTIN**
- **Cause**: GTIN submitted but incorrect format
- **Solution**: Apply GTIN check rule to identify problematic items

#### 4. **Incorrect Prices**
- **Cause**: Website prices update before feed refresh; mismatch with advertised prices
- **Solution**: Ensure feed scheduling aligns with website updates; avoid price modification rules that create discrepancies

#### 5. **Missing Images**
- **Cause**: Products submitted without images
- **Solution**: Use image detection rule to identify and exclude products lacking images

#### 6. **Images Too Small**
- **Cause**: Images fail size requirements (min 100x100px, max 16MB, visuals occupying 75-90%)
- **Solution**: Verify image dimensions match Google's specifications before submission

#### 7. **Generic Images**
- **Cause**: Images containing logos or "no image available" text
- **Solution**: Ensure all images authentically represent actual products

#### 8. **Mobile Product Page Inaccessibility**
- **Cause**: Product links cannot be accessed via mobile devices
- **Solution**: Check crawl error details in Google Merchant Center; resolve connectivity issues

#### 9. **Desktop Product Page Inaccessibility**
- **Cause**: Product links unreachable (404s, redirects, connection failures)
- **Solution**: Diagnose errors (404, HTTP 5xx, hostname issues); correct URL accessibility

#### 10. **Policy Violations**
- **Cause**: Products violate Google's merchant policies
- **Solution**: Review Google's policy guidelines; use rules to exclude violating products by EAN or category

## Troubleshooting Guide

### Import Problems

**XML/Data Source Issues**:
- Verify XML link is correct and accessible
- Ensure Google Sheets are set to public
- Check authentication credentials for API connections

**Timing Conflicts**:
- If Channable updates feed simultaneously with internal updates, you may get:
  - Error messages (can't fetch feed)
  - Empty feeds
  - Previous day's data
- **Solution**: Schedule Channable imports AFTER internal updates complete; manually refresh if needed

**Missing Field Data**:
- For standard fields (size, color): Create filling or search rules
- For unique data: Add fields to imports or merge feeds using matching identifiers

### Export Feed Errors

**Unmapped Fields**:
- Connect fields to corresponding export requirements during finalization step
- Map Channable field names to channel-specific field names

**Invalid Values**:
- Use Finalize section to identify accepted values for each channel
- Apply rules to standardize product data to channel requirements

**Duplicate Identifiers**:
- Use deduplication rules (if losing duplicates is acceptable)
- Update import source with unique identifiers
- Consider feed merging to consolidate duplicates

**Invalid GTIN/EAN Codes**:
- Exclude invalid entries using GTIN validation rule
- Update import feed with properly formatted codes
- Use feed merging to add correct GTINs from secondary source

## Best Practices for Rok Systems Clients

### 1. Feed Setup Workflow
1. **Import**: Connect to product data source
2. **Rules**: Apply transformations and optimizations
3. **Quality**: Review errors and fix with rules
4. **Finalize**: Map fields to channel requirements
5. **Export**: Set up channel connection and schedule

### 2. Rule Organization
- Use **Master Rule Groups** for changes needed across multiple channels
- Document complex rules with clear naming conventions
- Test rules on small product set before applying to entire feed

### 3. Scheduling Best Practices
- Schedule feed updates AFTER website inventory updates
- For Google Shopping: Update 2-4 times daily for stock changes
- Avoid update times that conflict with high-traffic periods

### 4. Quality Monitoring
- Review Quality step errors weekly
- Prioritize Mandatory errors first
- Address Recommended errors to improve visibility
- Use Channable's built-in validation rules before export

### 5. Performance Optimization
- Monitor performance metrics in Channable dashboard (available via API integration)
- Create custom labels for segmentation in Google Ads
- Use rules to enhance titles, descriptions for better CTR
- Segment products by performance (bestsellers, new arrivals, clearance)

## Integration with Pete's Brain System

### Product Impact Analyzer
- Channable changes can be tracked via Merchant Center snapshots
- Rule changes may explain product-level performance shifts
- Document significant rule changes in experiment log

### Client CONTEXT.md
- Note which clients use Channable
- Document Channable account credentials location
- Track major feed optimization projects

### Knowledge Base Usage
- Reference this document when troubleshooting feed issues
- Update with new learnings from client implementations
- Cross-reference with Google Shopping best practices

## Common Client Scenarios

### Scenario 1: Product Disapprovals After Rule Change
**Investigation Steps**:
1. Review recent rule changes in Channable
2. Check Quality step for new errors
3. Compare before/after product data for affected items
4. Check Google Merchant Center for specific disapproval reasons

### Scenario 2: Price Mismatch Errors
**Root Cause**: Feed updates don't align with website price changes
**Solution**:
- Coordinate feed schedule with website update timing
- Remove price modification rules that create discrepancies
- Consider more frequent feed updates

### Scenario 3: Stock Sync Issues
**Root Cause**: Channable fetches feed before website inventory updates
**Solution**:
- Schedule Channable imports 30+ minutes after inventory sync
- Use manual fetch if automated timing causes issues
- Consider switching to API integration for real-time updates

### Scenario 4: New Products Not Appearing
**Investigation Steps**:
1. Confirm products exist in import feed
2. Check for exclusion rules that might filter them out
3. Verify all mandatory fields are populated
4. Check Quality step for errors on new products

### Scenario 5: Platform Migration (BigCommerce → Shopify, WooCommerce → Shopify, etc.)
**Problem**: Product IDs change during migration, breaking Google Merchant Center history and campaign performance

**Symptoms**:
- All products appear as "new" in Merchant Center
- Performance Max loses product-level learning
- Shopping campaign product groups break
- Product performance history lost
- Channable rules based on old IDs stop working

**Critical Issue**: Each e-commerce platform uses its own internal ID system:
- **BigCommerce**: Product ID format (e.g., "12345")
- **Shopify**: Different product ID format (e.g., "shopify_GB_67890_45678")
- **WooCommerce**: Different again (e.g., "woo_UK_123")

**Impact on Google Shopping**:
- Google uses `item_id` (often called `id` or `offer_id`) as the unique identifier
- When IDs change, Google treats these as completely new products
- All historical performance data is orphaned
- Campaigns lose optimization learning
- Product ratings/reviews may not carry over

**Solutions**:

**Option 1: Maintain Original IDs (BEST)**
- During migration, map old platform IDs to a custom field in new platform
- Configure Channable to use original IDs as `item_id` in Google Shopping feed
- **Benefit**: Preserves all Google Shopping history and campaign learning
- **Implementation**:
  1. Export product IDs from old platform before migration
  2. Import as metafield/custom field in new platform
  3. In Channable, map custom field → `item_id` for Google Shopping export

**Option 2: Use SKU as Identifier (RECOMMENDED IF NO CUSTOM FIELD)**
- If SKUs remain consistent across platforms
- Configure Channable to use SKU as `item_id` instead of platform product ID
- **Benefit**: SKUs typically don't change during migration
- **Limitation**: Only works if SKUs are unique and consistent
- **Implementation**: In Channable rules, set `id` field to SKU field from import

**Option 3: Manual ID Mapping (LABOUR-INTENSIVE)**
- Create mapping spreadsheet: Old ID → New ID
- Use Channable feed merge to apply old IDs to new product data
- **Benefit**: Complete control over ID mapping
- **Limitation**: Time-consuming, requires maintenance
- **Implementation**:
  1. Create Google Sheet with columns: `new_id`, `original_id`
  2. In Channable, import Google Sheet as secondary feed
  3. Use feed merge on `new_id` to add `original_id`
  4. Use rule to set `id` field to `original_id`

**Option 4: Accept Fresh Start (LAST RESORT)**
- Let product IDs change, accept loss of history
- **When to use**: Very small catalog, new to Google Shopping, or poor historical performance
- **Mitigation**: Export performance data before migration for reference

**Prevention for Future Migrations**:
- Always use SKU or custom identifier field as `item_id` from day one
- Document ID strategy in client CONTEXT.md
- Never rely on platform-native product IDs for external integrations

**Positive Bakes Case Study** (2025-01):
- Migrated BigCommerce → Shopify
- Product IDs changed during migration
- Impact: Channable feed now uses Shopify IDs instead of original IDs
- Result: All products appear new in Google Merchant Center
- Solution Required: Implement Option 1 or 2 above to restore historical continuity

## Technical Details

### Feed Update Timing
- Channable can update feeds on schedule (hourly, daily, etc.)
- Manual refresh available for immediate updates
- Import timing must be coordinated with source data updates

### Error Reduction Impact
- Typical error reduction: 70-80% through automatic filtering
- Quality step identifies remaining issues for rule-based fixes
- Reduces manual data cleaning significantly

### Channel Templates
- 3,000+ pre-built templates for different channels
- Templates handle field mapping and format requirements
- Custom templates can be created for unique channels

## Resources

- **Website**: channable.com
- **Help Center**: helpcenter.channable.com
- **Free Trial**: Available to test functionality before choosing price plan
- **Setup Requirement**: Google Merchant Center account required for Google Shopping integration

## Related Knowledge Base Articles

- [Google Shopping Feed Optimization](../google-ads/shopping/)
- [Google Merchant Center Best Practices](../google-ads/shopping/)
- [Product Feed Management Strategies](../google-ads/shopping/)

---

**Last Updated**: 2025-11-07
**Relevance**: HIGH - Used for majority of Rok Systems clients
**Status**: Active platform with ongoing feature development
