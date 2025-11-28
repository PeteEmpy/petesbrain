# Meta Ads MCP Server - PetesBrain Quick Start

This guide is specifically for integrating the Meta Ads MCP Server into the PetesBrain workflow.

## Overview

The Meta Ads MCP Server extends PetesBrain's digital marketing intelligence by providing:

- **Cross-Platform Analytics** - Meta + Google Ads unified insights
- **Client Support** - Superspace and future Meta advertising clients
- **Automated Reporting** - Integration with monthly report generators
- **Performance Monitoring** - Daily alerts and tracking

## Quick Setup for PetesBrain

### 1. Installation (Already Done)

The server is already installed at:
```
/Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server/
```

### 2. Create Virtual Environment

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server

# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Meta App Credentials

1. **Go to [Meta for Developers](https://developers.facebook.com/)**
2. **Create a Business App** (see SETUP.md for detailed steps)
3. **Get your App ID and App Secret**
4. **Enable Marketing API**
5. **Set app to Live mode**

### 4. Create .env File

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server
cp env.example .env
```

Edit `.env`:
```bash
META_APP_ID=your_app_id_here
META_APP_SECRET=your_app_secret_here
```

### 5. Update Claude Desktop Config

Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add Meta Ads server alongside existing servers:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/server.py"
      ]
    },
    "meta-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server/venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server/server.py"
      ]
    },
    "google-tasks": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/server.py"
      ]
    }
  }
}
```

### 6. Restart Claude Desktop

Close and restart Claude Desktop to load the new server.

### 7. Test Authentication

In Claude, run:
```
"List all my Meta ad accounts"
```

This will:
1. Open browser for Facebook login
2. Request permissions
3. Save token to `meta_ads_token.json`
4. Return your ad accounts

## PetesBrain Client Integration

### Superspace (Primary Meta Client)

Superspace runs campaigns on both Google Ads and Meta. Use the Meta Ads MCP server to:

1. **Pull Performance Data**
   ```
   "Get Meta ad performance for Superspace account act_XXXXXXXXX for last 30 days"
   ```

2. **Compare Platforms**
   ```
   "Compare Superspace Google Ads vs Meta Ads performance this month"
   ```

3. **Audience Insights**
   ```
   "Show Meta audience insights for Superspace campaigns"
   ```

### Finding Account IDs

Store client account IDs in PetesBrain client files:

**Location:** `/Users/administrator/Documents/PetesBrain/clients/superspace/meta-account-info.md`

Example content:
```markdown
# Superspace Meta Ads Account

## Account Information
- Account ID: act_123456789
- Account Name: Superspace Ltd
- Currency: GBP
- Timezone: Europe/London

## Campaign Structure
- Brand Campaigns: Campaign ID 987654321
- Product Campaigns: Campaign ID 987654322
- Retargeting: Campaign ID 987654323
```

## Common PetesBrain Workflows

### 1. Weekly Performance Review

```
"Get Meta Ads performance for Superspace (act_123456789) for the last 7 days, 
broken down by campaign"
```

### 2. Monthly Reporting

```
"Generate a monthly Meta Ads report for Superspace showing:
- Campaign performance (impressions, clicks, spend, conversions)
- Best performing ad sets
- Audience demographics breakdown
- Comparison to previous month"
```

### 3. Budget Monitoring

```
"Check Superspace Meta Ads spend for this month and compare to budget"
```

### 4. Campaign Analysis

```
"Analyze Superspace Meta campaigns by device platform and age group 
for the last 30 days"
```

### 5. Cross-Platform Comparison

```
"Compare Google Ads and Meta Ads performance for Superspace:
- Which platform has better ROAS?
- What's the cost per conversion on each?
- Which has better CTR?"
```

## Integration with Existing PetesBrain Tools

### 1. Monthly Report Generator

**Location:** `/Users/administrator/Documents/PetesBrain/tools/monthly-report-generator/`

The Meta Ads data can be integrated into monthly reports alongside Google Ads data.

**Usage in Reports:**
```python
# Example integration (to be added to report generator)
from meta_ads_client import get_account_insights

# Get Meta data
meta_data = get_account_insights(
    account_id="act_123456789",
    date_preset="last_month",
    level="campaign"
)

# Combine with Google Ads data
# Format for report
```

### 2. Performance Monitoring

**Location:** `/Users/administrator/Documents/PetesBrain/agents/performance-monitoring/`

Add Meta Ads to daily performance alerts:

```python
# Check Meta Ads performance daily
# Alert if spend exceeds thresholds
# Track conversion metrics
```

### 3. Client Search

**Location:** `/Users/administrator/Documents/PetesBrain/tools/client-search.py`

Add Meta account info to client search results:

```python
# Include Meta ad account IDs
# Show Meta campaign status
# Link to Meta Business Manager
```

## Data Storage Conventions

### Client-Level Data

Store Meta account information in client directories:

```
/Users/administrator/Documents/PetesBrain/clients/superspace/
├── README.md                      # Main client info
├── meta-account-info.md          # Meta Ads account details
├── meta-campaigns.md             # Campaign documentation
└── meta-performance-data.json    # Historical performance data
```

### Shared Data

Store cross-platform comparisons and insights:

```
/Users/administrator/Documents/PetesBrain/shared/data/
├── meta-ads-mapping.json         # Client to account mapping
├── platform-comparison.json      # Cross-platform metrics
└── meta-performance-history.json # Aggregated performance data
```

## Client Account Mapping

Create a mapping file for easy reference:

**File:** `/Users/administrator/Documents/PetesBrain/shared/data/meta-ads-mapping.json`

```json
{
  "superspace": {
    "account_id": "act_123456789",
    "account_name": "Superspace Ltd",
    "business_id": "123456789",
    "currency": "GBP",
    "timezone": "Europe/London",
    "campaigns": {
      "brand": "987654321",
      "products": "987654322",
      "retargeting": "987654323"
    }
  },
  "future-client": {
    "account_id": "act_987654321",
    "account_name": "Future Client Ltd",
    "business_id": "987654321",
    "currency": "USD",
    "timezone": "America/New_York",
    "campaigns": {}
  }
}
```

## Example Queries for PetesBrain

### Daily Briefing Integration

```
"Generate my daily briefing including:
- Google Ads performance summary
- Meta Ads performance summary
- Budget alerts for both platforms
- Top performing campaigns across platforms"
```

### Client Status Check

```
"Show me complete status for Superspace:
- Google Ads campaigns (active, paused, budget)
- Meta Ads campaigns (active, paused, budget)
- Total spend across platforms this month
- Overall performance metrics"
```

### Optimization Insights

```
"Analyze Superspace campaigns on Meta:
- Which ad sets have highest ROAS?
- What audience segments perform best?
- Compare creative performance
- Suggest budget reallocation"
```

### Troubleshooting Campaign Issues

```
"Check Superspace Meta campaigns for issues:
- Any campaigns with declining performance?
- Budget pacing concerns?
- Low delivery warnings?
- Recommended actions?"
```

## Automated Workflows

### 1. Daily Performance Check

Create a script that runs daily:

```bash
#!/bin/bash
# File: /Users/administrator/Documents/PetesBrain/agents/performance-monitoring/check-meta-ads.sh

source /Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server/venv/bin/activate

python << EOF
from oauth.meta_auth import get_headers_with_auto_token
import requests
import json

# Check all clients
clients = json.load(open('/Users/administrator/Documents/PetesBrain/shared/data/meta-ads-mapping.json'))

for client_name, client_data in clients.items():
    account_id = client_data['account_id']
    # Get yesterday's performance
    # Check against thresholds
    # Send alerts if needed
EOF
```

### 2. Weekly Report Generation

```bash
# Run every Monday morning
# Generate Meta Ads weekly summary
# Email to clients
# Store in client directory
```

### 3. Budget Monitoring

```bash
# Check spend multiple times per day
# Alert if approaching limits
# Track budget pacing
```

## Best Practices for PetesBrain

1. **Consistent Naming**
   - Use client names from `/clients/` directory
   - Format account IDs as `act_XXXXXXXXX`
   - Store all credentials in `.env` files (never in code)

2. **Documentation**
   - Document all client Meta accounts in client README
   - Keep campaign structures updated
   - Log major changes to campaigns

3. **Security**
   - Store tokens securely (gitignored)
   - Use environment variables for credentials
   - Limit access to sensitive files

4. **Monitoring**
   - Set up daily performance checks
   - Alert on budget overruns
   - Track conversion metrics

5. **Integration**
   - Combine Meta and Google Ads data
   - Use consistent date ranges
   - Standardize metric names across platforms

## Troubleshooting PetesBrain-Specific Issues

### Issue: Multiple Clients, Different Accounts

**Solution:** Store account mapping and reference by client name:

```python
import json

# Load mapping
with open('/Users/administrator/Documents/PetesBrain/shared/data/meta-ads-mapping.json') as f:
    mapping = json.load(f)

# Get account for client
superspace_account = mapping['superspace']['account_id']
```

### Issue: Cross-Platform Date Range Mismatches

**Solution:** Use consistent date presets:

```python
# Use same date range for both platforms
date_preset = "last_30d"

# Google Ads query
google_data = run_gaql(customer_id, query, date_range="LAST_30_DAYS")

# Meta Ads query  
meta_data = get_account_insights(account_id, date_preset="last_30d")
```

### Issue: Token Expiration During Automated Runs

**Solution:** Add token refresh to automated scripts:

```python
from oauth.meta_auth import get_oauth_credentials, is_token_valid, load_token

# Check token before running
token_data = load_token()
if not is_token_valid(token_data):
    # This will trigger re-auth if needed
    get_oauth_credentials()
```

## Next Steps

1. **Set up first client** (Superspace) with Meta account mapping
2. **Test basic queries** to verify data access
3. **Integrate with monthly reports** for unified reporting
4. **Set up daily monitoring** for performance alerts
5. **Document workflows** in client directories

## Support

For PetesBrain-specific questions:
- Check `/docs/` directory for system documentation
- Review existing Google Ads integration patterns
- See `/tools/` for example integrations

For Meta Ads API questions:
- See `README.md` for general usage
- See `SETUP.md` for detailed configuration
- Check Meta for Developers documentation

---

**Welcome to unified Meta + Google Ads intelligence in PetesBrain!** 🎉

