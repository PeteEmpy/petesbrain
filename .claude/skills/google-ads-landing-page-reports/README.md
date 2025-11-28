# Google Ads Landing Page Reports Skill

## Overview

Universal skill for generating comprehensive landing page performance reports for any Google Ads client. Creates three separate CSV reports covering overall statistics, Performance Max asset groups, and Search campaign ad groups.

## Files

- `skill.md` - Main skill documentation with full technical details
- `generate_landing_page_reports.py` - Universal Python script for report generation
- `README.md` - This file

## Quick Usage

### Via Skill (Recommended)

User says:
- "landing page reports for [client]"
- "generate landing page reports for National Design Academy"
- "landing page performance for Smythson"

### Via Command Line

```bash
# Basic usage (last 90 days)
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  1994728449 \
  national-design-academy

# Custom date range
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  8573235780 \
  smythson \
  --date-from 2024-10-01 \
  --date-to 2024-12-31

# Last 30 days
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  1234567890 \
  client-slug \
  --days 30

# Managed account (requires manager ID)
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  1234567890 \
  client-slug \
  --manager-id 9876543210
```

## Reports Generated

### Report 1: Landing Page Statistics
- **File**: `report1-landing-page-statistics-{days}d.csv`
- **Purpose**: Overall performance by unique landing page URL
- **Data**: Aggregates all campaigns into single view per URL
- **Sorted by**: Conversions (highest first)
- **Use for**: Identifying best/worst performing landing pages

### Report 2: Performance Max Landing Pages
- **File**: `report2-pmax-landing-pages-{days}d.csv`
- **Purpose**: Show which PMax asset groups use which landing pages
- **Data**: Campaign → Asset Group → Landing Page hierarchy
- **Use for**: Auditing PMax configuration, identifying wrong URLs

### Report 3: Search Campaign Landing Pages
- **File**: `report3-search-landing-pages-{days}d.csv`
- **Purpose**: Granular ad group level landing page performance
- **Data**: Campaign → Ad Group → Landing Page with metrics
- **Use for**: Detailed Search campaign analysis

## Output Location

```
/Users/administrator/Documents/PetesBrain/clients/{client-slug}/reports/landing-page-analysis/
```

## Requirements

- Google Ads Customer ID (from client's CONTEXT.md)
- OAuth token (automatically managed)
- Python 3.x with requests library
- Access to Google Ads MCP server OAuth helper

## Authentication

Uses shared OAuth credentials from Google Ads MCP server:
- **Token Location**: `infrastructure/mcp-servers/google-ads-mcp-server/google_ads_token.json`
- **Auto-refresh**: Yes
- **Credentials**: `infrastructure/mcp-servers/google-ads-mcp-server/credentials.json`

No additional setup required if MCP server is configured.

## Common Issues

### "Customer Not Found" Error

**Cause**: Wrong customer ID

**Solution**: Always verify customer ID from CONTEXT.md:
```bash
grep "Google Ads Customer ID" clients/{client-slug}/CONTEXT.md
```

### Empty Report 2 (PMax)

**Cause**: Script queries campaigns first, then asset groups per campaign to avoid API limitations

**Solution**: This is working as designed. If report is empty, client may not have any PMax campaigns.

### 401 Unauthorized

**Cause**: OAuth token expired or invalid

**Solution**: Token should auto-refresh. If it fails, delete token file and re-run:
```bash
rm infrastructure/mcp-servers/google-ads-mcp-server/google_ads_token.json
# Script will trigger OAuth flow on next run
```

## Performance

Typical execution times:
- Small account (<5 campaigns): 5-10 seconds
- Medium account (5-20 campaigns): 10-30 seconds
- Large account (>20 campaigns): 30-60 seconds

## Credits

Created: 2025-11-28
Based on: National Design Academy landing page analysis (P0 task)
Author: Claude Code
