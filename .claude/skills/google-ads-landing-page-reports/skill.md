# Google Ads Landing Page Reports

## Description
Generates comprehensive landing page performance reports for Google Ads accounts. Creates three separate reports: overall landing page statistics, Performance Max asset group landing pages, and Search campaign landing pages. Works for any client with Google Ads data.

## Trigger Phrases
- "landing page reports for [client]"
- "landing page performance [client]"
- "generate landing page reports"
- "landing page analysis for [client]"

## Allowed Tools
- Read
- Write
- Edit
- Bash
- Grep
- Glob

## Instructions

### Step 1: Get Client Platform IDs

**CRITICAL**: Always get the correct Google Ads Customer ID from the client's CONTEXT.md file.

```bash
# Read the client's CONTEXT.md
Read: /Users/administrator/Documents/PetesBrain/clients/{client-slug}/CONTEXT.md
```

Extract:
- **Google Ads Customer ID** (10-digit number, no dashes)
- Check if there's a Manager Account ID mentioned (some clients are managed accounts)

**Common Mistake**: Do NOT guess or use a customer ID from a different client. Each client has their own unique ID.

### Step 2: Determine Date Range

**Default**: Last 90 days (approximately 3 months)

Calculate:
- `date_to`: Today's date (YYYY-MM-DD format)
- `date_from`: 90 days before today (YYYY-MM-DD format)

**Alternative**: User may specify custom date range (e.g., "last 30 days", "Q4 2024")

### Step 3: Create Report Output Directory

```bash
# Create reports directory if it doesn't exist
mkdir -p /Users/administrator/Documents/PetesBrain/clients/{client-slug}/reports/landing-page-analysis
```

### Step 4: Generate Report 1 - Overall Landing Page Statistics

**Purpose**: Aggregate performance by unique landing page URL across all campaigns.

**Query Resource**: `landing_page_view`

**Script Template**:

```python
#!/usr/bin/env python3
import os
import sys
import csv
import requests
from collections import defaultdict

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "{CUSTOMER_ID}"  # From CONTEXT.md
date_from = "{DATE_FROM}"      # YYYY-MM-DD
date_to = "{DATE_TO}"          # YYYY-MM-DD

print(f"📊 Generating Report 1: Landing Page Statistics")
print(f"📅 Date Range: {date_from} to {date_to}")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

query = f"""
    SELECT
        landing_page_view.unexpanded_final_url,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.conversions,
        metrics.conversions_value,
        metrics.cost_micros
    FROM landing_page_view
    WHERE segments.date BETWEEN '{date_from}' AND '{date_to}'
"""

response = requests.post(url, headers=headers, json={'query': query})

if not response.ok:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
results = data.get('results', [])

# Aggregate by landing page
landing_pages = defaultdict(lambda: {
    'impressions': 0,
    'clicks': 0,
    'conversions': 0,
    'conv_value': 0,
    'cost': 0
})

for row in results:
    url_path = row['landingPageView']['unexpandedFinalUrl']
    metrics = row['metrics']

    landing_pages[url_path]['impressions'] += int(metrics.get('impressions', 0))
    landing_pages[url_path]['clicks'] += int(metrics.get('clicks', 0))
    landing_pages[url_path]['conversions'] += float(metrics.get('conversions', 0))
    landing_pages[url_path]['conv_value'] += float(metrics.get('conversionsValue', 0))
    landing_pages[url_path]['cost'] += int(metrics.get('costMicros', 0)) / 1_000_000

# Write CSV
report_path = '/Users/administrator/Documents/PetesBrain/clients/{client-slug}/reports/landing-page-analysis/report1-landing-page-statistics-{days}d.csv'

with open(report_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Landing Page URL', 'Impressions', 'Clicks', 'CTR', 'Conversions',
        'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
    ])

    # Sort by conversions descending
    sorted_pages = sorted(landing_pages.items(), key=lambda x: x[1]['conversions'], reverse=True)

    for url_path, stats in sorted_pages:
        ctr = (stats['clicks'] / stats['impressions'] * 100) if stats['impressions'] > 0 else 0
        conv_rate = (stats['conversions'] / stats['clicks'] * 100) if stats['clicks'] > 0 else 0
        roas = stats['conv_value'] / stats['cost'] if stats['cost'] > 0 else 0

        writer.writerow([
            url_path,
            stats['impressions'],
            stats['clicks'],
            f"{ctr:.2f}%",
            stats['conversions'],
            f"{conv_rate:.2f}%",
            f"£{stats['cost']:.2f}",
            f"£{stats['conv_value']:.2f}",
            f"{roas:.2f}"
        ])

print(f"✅ Report 1 saved: {len(landing_pages)} unique landing pages")
```

**Key Points**:
- Uses `landing_page_view` resource which aggregates across all campaigns
- Aggregates metrics per unique URL
- Sorted by conversions (highest first) for easy analysis
- Calculates CTR, Conv Rate, and ROAS

### Step 5: Generate Report 2 - Performance Max Landing Pages

**Purpose**: Show which landing pages are used by which PMax asset groups.

**Query Approach**:
1. First get all PMax campaigns
2. Then query asset groups for each campaign individually (avoids 0 results issue)

**Script Template**:

```python
#!/usr/bin/env python3
import os
import sys
import csv
import requests

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "{CUSTOMER_ID}"
date_from = "{DATE_FROM}"
date_to = "{DATE_TO}"

print(f"📊 Generating Report 2: Performance Max Landing Pages")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

# Step 1: Get all PMax campaigns
query_campaigns = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status
    FROM campaign
    WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
      AND campaign.status IN ('ENABLED', 'PAUSED')
"""

response = requests.post(url, headers=headers, json={'query': query_campaigns})
campaigns_data = response.json()

pmax_campaigns = []
for row in campaigns_data.get('results', []):
    pmax_campaigns.append({
        'id': row['campaign']['id'],
        'name': row['campaign']['name'],
        'status': row['campaign']['status']
    })

print(f"Found {len(pmax_campaigns)} Performance Max campaigns")

# Step 2: Query asset groups for each campaign
pmax_data = []

for campaign in pmax_campaigns:
    campaign_id = campaign['id']

    query_ag = f"""
        SELECT
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.final_urls,
            asset_group.status,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM asset_group
        WHERE campaign.id = {campaign_id}
          AND segments.date BETWEEN '{date_from}' AND '{date_to}'
    """

    response = requests.post(url, headers=headers, json={'query': query_ag})

    if not response.ok:
        continue

    ag_data = response.json()

    for row in ag_data.get('results', []):
        landing_pages = ', '.join(row['assetGroup'].get('finalUrls', [])) or 'N/A'

        pmax_data.append({
            'campaign_name': row['campaign']['name'],
            'campaign_status': campaign['status'],
            'asset_group_name': row['assetGroup']['name'],
            'asset_group_status': row['assetGroup']['status'],
            'landing_pages': landing_pages,
            'impressions': int(row['metrics'].get('impressions', 0)),
            'clicks': int(row['metrics'].get('clicks', 0)),
            'conversions': float(row['metrics'].get('conversions', 0)),
            'conv_value': float(row['metrics'].get('conversionsValue', 0)),
            'cost': int(row['metrics'].get('costMicros', 0)) / 1_000_000
        })

# Write CSV
report_path = '/Users/administrator/Documents/PetesBrain/clients/{client-slug}/reports/landing-page-analysis/report2-pmax-landing-pages-{days}d.csv'

with open(report_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Campaign Name', 'Campaign Status', 'Asset Group Name', 'Asset Group Status',
        'Landing Page URL(s)', 'Impressions', 'Clicks', 'Conversions',
        'Conv Value (£)', 'Cost (£)', 'ROAS'
    ])

    for row in pmax_data:
        roas = row['conv_value'] / row['cost'] if row['cost'] > 0 else 0

        writer.writerow([
            row['campaign_name'],
            row['campaign_status'],
            row['asset_group_name'],
            row['asset_group_status'],
            row['landing_pages'],
            row['impressions'],
            row['clicks'],
            row['conversions'],
            f"£{row['conv_value']:.2f}",
            f"£{row['cost']:.2f}",
            f"{roas:.2f}"
        ])

print(f"✅ Report 2 saved: {len(pmax_data)} asset group records")
```

**Key Points**:
- **CRITICAL**: Query campaigns first, then asset groups per campaign
- Do NOT try to query all asset groups at once with date filter (returns 0 results)
- Shows campaign → asset group → landing page hierarchy
- Useful for identifying which asset groups use which pages

### Step 6: Generate Report 3 - Search Campaign Landing Pages

**Purpose**: Show landing page performance at ad group level for Search campaigns.

**Query Resource**: `ad_group_ad`

**Script Template**:

```python
#!/usr/bin/env python3
import os
import sys
import csv
import requests

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import get_headers_with_auto_token

customer_id = "{CUSTOMER_ID}"
date_from = "{DATE_FROM}"
date_to = "{DATE_TO}"

print(f"📊 Generating Report 3: Search Campaign Landing Pages")

headers = get_headers_with_auto_token()
url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"

query = f"""
    SELECT
        campaign.name,
        ad_group.name,
        ad_group_ad.ad.final_urls,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.conversions,
        metrics.conversions_value,
        metrics.cost_micros
    FROM ad_group_ad
    WHERE campaign.advertising_channel_type = 'SEARCH'
      AND ad_group_ad.status = 'ENABLED'
      AND ad_group.status = 'ENABLED'
      AND campaign.status IN ('ENABLED', 'PAUSED')
      AND segments.date BETWEEN '{date_from}' AND '{date_to}'
"""

response = requests.post(url, headers=headers, json={'query': query})

if not response.ok:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
results = data.get('results', [])

# Write CSV
report_path = '/Users/administrator/Documents/PetesBrain/clients/{client-slug}/reports/landing-page-analysis/report3-search-landing-pages-{days}d.csv'

with open(report_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Campaign Name', 'Ad Group Name', 'Landing Page URL', 'Impressions',
        'Clicks', 'CTR', 'Conversions', 'Conv Rate', 'Cost (£)', 'Conv Value (£)', 'ROAS'
    ])

    for row in results:
        campaign_name = row['campaign']['name']
        ad_group_name = row['adGroup']['name']

        final_urls = row.get('adGroupAd', {}).get('ad', {}).get('finalUrls', [])
        landing_page = final_urls[0] if final_urls else 'N/A'

        metrics = row['metrics']
        impressions = int(metrics.get('impressions', 0))
        clicks = int(metrics.get('clicks', 0))
        conversions = float(metrics.get('conversions', 0))
        conv_value = float(metrics.get('conversionsValue', 0))
        cost = int(metrics.get('costMicros', 0)) / 1_000_000

        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
        roas = conv_value / cost if cost > 0 else 0

        writer.writerow([
            campaign_name,
            ad_group_name,
            landing_page,
            impressions,
            clicks,
            f"{ctr:.2f}%",
            conversions,
            f"{conv_rate:.2f}%",
            f"£{cost:.2f}",
            f"£{conv_value:.2f}",
            f"{roas:.2f}"
        ])

print(f"✅ Report 3 saved: {len(results)} ad records")
```

**Key Points**:
- Uses `ad_group_ad` resource
- Filters for Search campaigns only
- Shows campaign → ad group → landing page
- Can be very detailed (1000+ rows for large accounts)

### Step 7: Summary Output

After generating all three reports, provide user with:

1. **File locations** (full paths)
2. **Record counts** for each report
3. **Key insights** from the data (top performers, notable patterns)
4. **File sizes** (to indicate data volume)

**Example Summary**:

```
✅ All 3 Landing Page Performance Reports Complete

📊 Report Summary:

Report 1: Landing Page Statistics
- File: report1-landing-page-statistics-90d.csv (17 KB)
- Data: 154 unique landing pages
- Top performer: [URL] with [X] conversions

Report 2: Performance Max Landing Pages
- File: report2-pmax-landing-pages-90d.csv (13 KB)
- Data: 59 asset group records across 15 campaigns
- Shows: Which asset groups use which landing pages

Report 3: Search Campaign Landing Pages
- File: report3-search-landing-pages-90d.csv (203 KB)
- Data: 1,142 ad records
- Shows: Granular ad group level performance

📁 Location:
/Users/administrator/Documents/PetesBrain/clients/{client-slug}/reports/landing-page-analysis/
```

## Common Issues and Solutions

### Issue 1: Query Returns 0 Results

**Symptoms**: Asset group or landing page queries return empty results despite knowing data exists.

**Causes**:
1. Wrong customer ID (most common)
2. Querying all asset groups at once with date filter
3. OAuth token expired

**Solutions**:
1. **Always verify customer ID** from CONTEXT.md - do not guess
2. **For PMax**: Query campaigns first, then query asset groups per campaign
3. **OAuth**: The `get_headers_with_auto_token()` function automatically refreshes tokens

### Issue 2: 401 Unauthorized / Customer Not Found

**Cause**: Using wrong customer ID

**Solution**:
```bash
# Always read from CONTEXT.md
grep "Google Ads Customer ID" /Users/administrator/Documents/PetesBrain/clients/{client-slug}/CONTEXT.md
```

Extract the 10-digit number (no dashes).

### Issue 3: Managed Account Access

**Symptoms**: 401 errors even with correct customer ID

**Cause**: Account is managed by an MCC (manager account) and requires `login-customer-id` header

**Solution**:
```python
# Check CONTEXT.md for manager account ID
# Add to headers if present
if manager_id:
    headers['login-customer-id'] = manager_id
```

### Issue 4: Script Can't Import oauth.google_auth

**Cause**: Python path not set correctly

**Solution**:
```python
# Always include at top of script
import sys
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')
```

## Technical Details

### Authentication Method

Uses custom OAuth helper from Google Ads MCP server:
- **Module**: `oauth.google_auth`
- **Function**: `get_headers_with_auto_token()`
- **Token Location**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/google_ads_token.json`
- **Auto-refresh**: Yes (handles expired tokens automatically)

### API Version

Uses Google Ads API v22:
```
https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search
```

### Query Method

Uses `search` endpoint (NOT `searchStream`):
- Returns JSON format
- Easier to parse
- Suitable for report generation

### Data Aggregation

**Report 1**: Uses `defaultdict` to aggregate metrics per URL
**Report 2**: Direct mapping (one row per asset group)
**Report 3**: Direct mapping (one row per ad)

### Performance Considerations

- **Report 1**: Usually 50-500 unique landing pages
- **Report 2**: Usually 20-100 asset groups
- **Report 3**: Can be 1000+ rows for large accounts
- All queries typically complete in <10 seconds

## Skill Execution Checklist

When user requests landing page reports:

- [ ] Read client's CONTEXT.md
- [ ] Extract correct Google Ads Customer ID
- [ ] Determine date range (default: 90 days)
- [ ] Create reports directory
- [ ] Generate Report 1 (overall statistics)
- [ ] Generate Report 2 (PMax asset groups)
- [ ] Generate Report 3 (Search campaigns)
- [ ] Verify all files created
- [ ] Preview first few rows of each report
- [ ] Provide summary with file paths and key insights

## Examples

### Example 1: Basic Usage

**User**: "Generate landing page reports for Smythson"

**Process**:
1. Read `/Users/administrator/Documents/PetesBrain/clients/smythson/CONTEXT.md`
2. Extract customer ID: `8573235780`
3. Date range: Last 90 days
4. Generate all 3 reports
5. Save to `clients/smythson/reports/landing-page-analysis/`

### Example 2: Custom Date Range

**User**: "Landing page performance for NDA for Q4 2024"

**Process**:
1. Read client CONTEXT.md
2. Calculate Q4 dates: `2024-10-01` to `2024-12-31`
3. Generate reports with custom date range
4. File names: `report1-landing-page-statistics-q4-2024.csv`

### Example 3: Monthly Report

**User**: "November landing page report for Tree2mydoor"

**Process**:
1. Read CONTEXT.md (check voice aliases: "Tree2mydoor" → "tree-to-my-door")
2. Date range: `2024-11-01` to `2024-11-30`
3. Generate reports
4. File names include "november-2024"

## Related Skills

- `google-ads-weekly-report` - Broader performance analysis
- `google-ads-campaign-audit` - Campaign structure review
- `google-ads-keyword-audit` - Search term analysis

## Notes

- **British English**: All output uses British spelling (analyse, optimise)
- **Currency**: Default is GBP (£) - modify for multi-currency clients
- **Date Format**: Always YYYY-MM-DD for API queries
- **Sorting**: Report 1 sorted by conversions DESC for quick insights
