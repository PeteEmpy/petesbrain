# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Client Overview

**Just Bin Bags Group** is a UK-based e-commerce business operating two brands:
- **Just Bin Bags (JBB)**: Main brand - polythene solutions, bin bags, and disposable products
- **Just Health Disposables (JHD)**: Sub-brand - healthcare disposables and medical supplies

Both brands share a single Google Ads account (Customer ID: 9697059148) but have separate WooCommerce stores and merchant feeds.

---

## Key Commands

### ROAS Dashboard

Generate monthly ROAS dashboard combining revenue from both WooCommerce stores:

```bash
cd scripts
python3 generate-roas-dashboard.py --months 12  # Default: 12 months
```

**Outputs**: `reports/roas-dashboard.html` (interactive dashboard with graphs)

**Data sources**:
- WooCommerce revenue: Fetched automatically via MCP servers
- Google Ads cost: Loaded from `data/google-ads-cost-cache.json`

Update Google Ads costs:
```bash
# Edit data/google-ads-cost-cache.json
{
  "2025-11": 1500.00,
  "YYYY-MM": cost_in_gbp
}
```

### Audits

Run Google Ads audit for the account:

```bash
cd scripts
python3 run-audit.py
```

---

## Architecture

### Multi-Brand Structure

This client operates **two separate e-commerce brands under one Google Ads account**:

| Brand | WooCommerce Store | MCP Server | Merchant ID |
|-------|------------------|------------|-------------|
| Just Bin Bags (JBB) | https://justbinbags.co.uk | `woocommerce-justbinbags` | 181788523 |
| Just Health Disposables (JHD) | https://justhealthdisposables.co.uk | `woocommerce-justhealthdisposables` | 5085550522 |

**Shared Resources**:
- Google Ads Account: 9697059148
- Client folder: `/clients/just-bin-bags/`
- Tasks, documents, and reports

### WooCommerce MCP Servers

Two WooCommerce MCP servers are configured in Claude Code (user-scoped):

```bash
# Verify connectivity
claude mcp list | grep woocommerce
```

Both servers:
- Use the same base server code (`woocommerce-mcp-server-opestro`)
- Have separate environment configurations (URL, consumer key/secret)
- Fetch orders with status "completed" for revenue calculations

### ROAS Dashboard Data Flow

```
generate-roas-dashboard.py
    ├─> WooCommerce API (JBB) → Revenue £X
    ├─> WooCommerce API (JHD) → Revenue £Y
    ├─> google-ads-cost-cache.json → Cost £Z
    └─> Calculate: ROAS = (£X + £Y) / £Z
         └─> Generate: reports/roas-dashboard.html
```

**Key implementation details**:
- Uses `requests` library with HTTP Basic Auth for WooCommerce
- Reads MCP config via `claude mcp get <server-name>` to extract credentials
- Falls back to hardcoded WooCommerce URLs if MCP config unavailable
- Filters orders by date range and "completed" status only
- Supports custom month ranges via `--months N` parameter

---

## Directory Structure

```
just-bin-bags/
├── CONTEXT.md                    # Strategic notes, platform IDs, business context
├── tasks.json                    # Active tasks (internal system)
├── tasks-completed.md            # Archived completed tasks
├── scripts/
│   ├── generate-roas-dashboard.py   # Main ROAS dashboard generator
│   ├── README-ROAS-DASHBOARD.md     # Dashboard documentation
│   └── run-audit.py                 # Google Ads audit script
├── data/
│   └── google-ads-cost-cache.json   # Monthly ad spend (manual entry)
├── reports/
│   └── roas-dashboard.html          # Generated dashboard (gitignored)
├── product-feeds/                   # Merchant feed data
├── audits/                          # Historical audit reports
├── documents/                       # Client documentation
├── emails/                          # Email correspondence
└── meeting-notes/                   # Client meeting transcripts
```

---

## Platform IDs

Critical identifiers for API integration:

- **Google Ads Customer ID**: `9697059148`
- **Merchant Centre IDs**:
  - JBB Main Brand: `181788523`
  - JHD Sub-brand: `5085550522`
- **GA4 Property ID**: [TBD]

**WooCommerce Stores**:
- JBB: `https://justbinbags.co.uk`
- JHD: `https://justhealthdisposables.co.uk`

---

## Dependencies

Python packages required for scripts:

```bash
pip install requests python-dateutil
```

MCP servers (already configured):
- `woocommerce-justbinbags` - Connected ✓
- `woocommerce-justhealthdisposables` - Connected ✓

---

## Important Notes

### ROAS Calculation

```
ROAS = Total Revenue / Google Ads Cost

Where:
- Total Revenue = JBB WooCommerce Revenue + JHD WooCommerce Revenue
- Only "completed" orders count towards revenue
- Google Ads cost covers both brands (shared account)
```

### Google Ads Cost Data

Currently uses **manual cache file** (`data/google-ads-cost-cache.json`).

**To update monthly costs**: Edit the JSON file with format `{"YYYY-MM": cost_in_gbp}`

**Future enhancement**: Integrate Google Ads MCP server to fetch costs automatically via GAQL.

### Task Management

This client uses the **internal task system** (`tasks.json`), not Google Tasks, because:
- Both brands share one client folder
- Tasks relate to the overall account, not individual brands

---

## Troubleshooting

### WooCommerce connection fails

Check MCP server status:
```bash
claude mcp get woocommerce-justbinbags
claude mcp get woocommerce-justhealthdisposables
```

Verify credentials in environment variables are correct.

### Dashboard shows £0.00 for Google Ads cost

Update the cache file:
```bash
# Edit data/google-ads-cost-cache.json
{
  "2025-11": 1500.00,
  "2025-10": 1450.00
}
```

### ROAS dashboard displays no data

1. Check WooCommerce MCP servers are connected
2. Verify date range has completed orders
3. Ensure Google Ads cost cache has data for requested months
4. Check script output for API errors

---

## Voice Transcription Aliases

When processing voice commands, recognize these variations:
- JBB, just been bags, Just Bin Bag, JustBinBags, bin bags
- JHD, just health disposables, Just Health Disposal
