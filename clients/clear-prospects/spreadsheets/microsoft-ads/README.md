# Microsoft Ads Data Exports

This folder contains raw data exports from Microsoft Ads for analysis and reporting.

**Location:** `clients/clear-prospects/spreadsheets/microsoft-ads/` (following standard client folder structure)

## Purpose

Since the Microsoft Ads MCP server is currently unavailable (Azure Portal issues with Microsoft Ads technical support), this folder stores manually exported data from the Microsoft Ads UI for processing.

## Export Instructions

### Monthly Performance Export (12 months)

1. Log into Microsoft Ads UI
2. Navigate to **Reports** → **Performance Reports**
3. Set date range: Last 12 months
4. Select columns:
   - Date (month level)
   - Campaign Name
   - Impressions
   - Clicks
   - CTR
   - Avg CPC
   - Spend
   - Conversions
   - Conv Rate
   - Conv Value
   - ROAS
5. Export as CSV
6. Save to this folder with naming convention: `YYYY-MM-DD-microsoft-ads-12month-performance.csv`

### Campaign-Level Export

1. Navigate to **Campaigns** tab
2. Set date range: Last 12 months
3. Export all campaigns with performance metrics
4. Save as: `YYYY-MM-DD-microsoft-ads-campaigns.csv`

### Product-Level Export (Shopping Campaigns)

If applicable for e-commerce campaigns:
1. Navigate to **Shopping Campaigns** → **Products**
2. Set date range: Last 12 months
3. Export product performance data
4. Save as: `YYYY-MM-DD-microsoft-ads-products.csv`

## File Naming Convention

```
YYYY-MM-DD-microsoft-ads-[report-type].csv
```

Examples:
- `2025-11-20-microsoft-ads-12month-performance.csv`
- `2025-11-20-microsoft-ads-campaigns.csv`
- `2025-11-20-microsoft-ads-products.csv`

## Processing

Once data is exported to this folder:
1. Claude Code can read and analyse the CSV files
2. Generate comprehensive performance reports
3. Create visualisations and trend analysis
4. Output reports to `clients/clear-prospects/reports/microsoft-ads/`

## Current Status

**Blocker:** Azure Portal issues preventing MCP access
**Status:** With Microsoft Ads technical support
**Workaround:** Manual CSV exports (this folder)
**Last Updated:** 2025-11-20
