# Just Bin Bags Group - ROAS Dashboard

## Overview

This dashboard displays monthly ROAS (Return on Ad Spend) for the Just Bin Bags group, combining revenue from both Just Bin Bags and Just Health Disposables stores against total Google Ads spend.

## Quick Start

```bash
cd /Users/administrator/Documents/PetesBrain/clients/just-bin-bags/scripts
python3 generate-roas-dashboard.py
```

This will:
1. Fetch WooCommerce revenue from both stores (last 12 months)
2. Load Google Ads cost from cache file
3. Calculate monthly ROAS
4. Generate an interactive HTML dashboard
5. Open it in your browser

## Usage

### Generate Dashboard

```bash
# Last 12 months (default)
python3 generate-roas-dashboard.py

# Last 6 months
python3 generate-roas-dashboard.py --months 6

# Last 3 months
python3 generate-roas-dashboard.py --months 3
```

### Update Google Ads Costs

Edit the cache file: `/Users/administrator/Documents/PetesBrain/clients/just-bin-bags/data/google-ads-cost-cache.json`

Format:
```json
{
  "2025-11": 1500.00,
  "2025-10": 1450.00,
  "YYYY-MM": cost_in_gbp
}
```

### Outputs

**HTML Dashboard**: `../reports/roas-dashboard.html`

The dashboard includes:
- Current month ROAS
- Total revenue breakdown (JBB + JHD)
- Google Ads cost
- Average ROAS across all months
- Interactive ROAS trend graph
- Revenue vs Cost bar chart
- Detailed monthly data table

## Data Sources

### WooCommerce Revenue
- **Just Bin Bags**: Fetched via `woocommerce-justbinbags` MCP server
- **Just Health Disposables**: Fetched via `woocommerce-justhealthdisposables` MCP server
- **Method**: Direct WooCommerce REST API calls
- **Filter**: Only "completed" orders counted

### Google Ads Cost
- **Source**: Cache file (manual entry for now)
- **Location**: `../data/google-ads-cost-cache.json`
- **Future**: Will integrate with Google Ads MCP server

## WooCommerce MCP Servers

The script uses the WooCommerce MCP servers configured in Claude Code:

- **woocommerce-justbinbags**
  - URL: https://justbinbags.co.uk
  - Status: Connected ✓

- **woocommerce-justhealthdisposables**
  - URL: https://justhealthdisposables.co.uk
  - Status: Connected ✓

## ROAS Calculation

```
ROAS = Total Revenue / Google Ads Cost

Where:
- Total Revenue = JBB Revenue + JHD Revenue
- Google Ads Cost = Monthly ad spend for account 9697059148
```

## Dependencies

Required Python packages:
```bash
pip install requests python-dateutil
```

## Troubleshooting

### No WooCommerce data

Check MCP servers are connected:
```bash
claude mcp list | grep woocommerce
```

### Google Ads cost is £0.00

Update the cache file with actual monthly costs:
```bash
/Users/administrator/Documents/PetesBrain/clients/just-bin-bags/data/google-ads-cost-cache.json
```

### Script fails with import error

Install required packages:
```bash
pip3 install requests python-dateutil
```

## File Structure

```
just-bin-bags/
├── scripts/
│   ├── generate-roas-dashboard.py   # Main script
│   └── README-ROAS-DASHBOARD.md     # This file
├── data/
│   └── google-ads-cost-cache.json   # Monthly ad costs
└── reports/
    └── roas-dashboard.html          # Generated dashboard
```

## Future Enhancements

- [ ] Integrate Google Ads MCP server to fetch costs automatically
- [ ] Add year-over-year comparison
- [ ] Add forecasting based on historical trends
- [ ] Create LaunchAgent for automatic daily updates
- [ ] Add email notifications for ROAS alerts
- [ ] Export to PDF for client reporting

## Author

Created: 2025-11-27
Last Updated: 2025-11-27
