# Merchant Center Disapproval Tracking

**Status**: ✅ Ready for deployment
**Last Updated**: October 30, 2025

## Overview

Merchant Center Disapproval Tracking monitors Google Merchant Center for product approval issues and sends immediate alerts when products are disapproved or when disapproval reasons change.

This integrates with the existing Product Impact Analyzer monitoring system to provide complete visibility into why products disappear from your feeds.

## Key Features

### 🔍 Product Status Tracking
- **Real-time status checks** for all products across all clients
- **Disapproval reason tracking** with detailed issue codes
- **Country-specific status** (approved in UK, disapproved in US, etc.)
- **Historical tracking** to detect newly disapproved products

### 🚨 Immediate Alerts
- **New disapproval detection** - Alerts when products newly disapproved
- **Severity classification** - Critical (policy) vs Warning (data quality)
- **Detailed issue descriptions** with resolution guidance
- **Email alerts** during business hours (9 AM - 6 PM, weekdays)

### 📊 Integration with Product Impact Analyzer
- **Complements product monitoring** - Explains WHY products disappeared
- **Shared schedule** - Runs 30 minutes after daily product monitor
- **Unified alerting** - Same email/Slack system as product alerts

## How It Works

### Daily Workflow

```
Every day at 10:30 AM (weekdays):
    ↓
1. Query Merchant Center API for all product statuses
    ↓
2. Identify disapproved products and reasons
    ↓
3. Compare to yesterday's snapshot
    ↓
4. Detect newly disapproved products
    ↓
5. If new disapprovals found AND business hours:
   → Send email alert
    ↓
6. Save today's snapshot for tomorrow
```

### What Gets Tracked

For each product:
- **Product ID** - Merchant Center product identifier
- **Title** - Product name
- **Overall Status** - approved, disapproved, or pending
- **Destination Status** - Status per destination (Shopping, Surfaces, etc.)
- **Country Status** - Approved/disapproved per country
- **Item-Level Issues** - Specific disapproval reasons:
  - Issue code (e.g., `missing_gtin`, `policy_violation`)
  - Description (human-readable explanation)
  - Servability (how severe the issue is)
  - Resolution (how to fix it)
  - Affected countries

### Disapproval Severity Levels

| Severity | Trigger | Example Issues | Action Required |
|----------|---------|----------------|-----------------|
| **Critical** | Policy violations, product cannot be shown | Prohibited content, counterfeit, restricted products | Immediate - product is not serving |
| **Warning** | Data quality issues, may be temporary | Missing GTIN, invalid price, incomplete description | Fix when possible - may have limited serving |

## Installation

### Prerequisites

1. **Google Cloud Project** with Content API for Shopping enabled
2. **Service Account** with Merchant Center access
3. **Credentials file** (`credentials.json`) with Content API scope
4. **Product Impact Analyzer** already set up (`./setup_automation.sh` completed)

### Setup

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_disapproval_monitoring.sh
```

This will:
1. ✅ Create disapproval monitoring LaunchAgent
2. ✅ Configure environment variables
3. ✅ Set up daily 10:30 AM checks (weekdays)
4. ✅ Optionally run test check

### Verify Installation

```bash
# Check LaunchAgent is running
launchctl list | grep disapproval-monitor

# View logs
tail -f ~/.petesbrain-disapproval-monitor.log

# Run test check
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
.venv/bin/python3 disapproval_monitor.py --test
```

## Usage

### Automated (Default)

Once set up, disapproval monitoring runs automatically every weekday at 10:30 AM. **No action required!**

### Manual Runs

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Full check (respects business hours)
.venv/bin/python3 disapproval_monitor.py

# Test mode (ignore business hours, always alert)
.venv/bin/python3 disapproval_monitor.py --test

# Check specific client only
.venv/bin/python3 disapproval_monitor.py --client "Tree2mydoor" --test
```

### Merchant Center Tracker (Standalone)

You can also use the Merchant Center tracker directly for reporting:

```bash
# Check all clients and generate disapproval report
.venv/bin/python3 merchant_center_tracker.py --report

# Check specific client
.venv/bin/python3 merchant_center_tracker.py --client "Tree2mydoor" --report

# Save snapshot to file
.venv/bin/python3 merchant_center_tracker.py --save --report
```

## Email Alerts

### What You'll Receive

Subject: **🚨 Merchant Center Disapprovals - 3 New Issues**

```
================================================================================
MERCHANT CENTER DISAPPROVAL ALERT
Alert Time: October 30, 2025 10:35 AM
Total: 5 disapprovals (3 new)
================================================================================

🔥 CRITICAL ISSUES (Immediate Action Required)
────────────────────────────────────────────────────────────────────────────────
🆕 Tree2mydoor - Product 287
   Title: Olive Tree Large
   Issue: prohibited_content
   Product contains prohibited content or violates Google Shopping policies
   Affected Countries: GB, US
   Resolution: Remove prohibited content or remove product from feed

🆕 Smythson - Product FCB7007
   Title: Card Holder Black
   Issue: counterfeit
   Product appears to be counterfeit or unauthorized replica
   Affected Countries: US
   Resolution: Provide proof of authenticity or remove from feed

⚠️  WARNINGS (Data Quality Issues)
────────────────────────────────────────────────────────────────────────────────
🆕 BrightMinds - Product 1234
   Title: Educational Toy Set
   Issue: missing_gtin
   Product is missing required GTIN (barcode)
   Resolution: Add valid GTIN to product feed

   Accessories for the Home - Product 5678
   Title: Decorative Cushion
   Issue: invalid_price
   Product price is invalid or incorrectly formatted
   Resolution: Update price to valid format (e.g., 29.99 GBP)

================================================================================
Fix these issues in Google Merchant Center:
https://merchants.google.com/
================================================================================
```

## API Details

### Google Content API for Shopping

The Merchant Center tracker uses the **Google Content API for Shopping v2.1** to query product statuses.

**API Endpoints Used**:
- `productstatuses.get` - Get status for specific product
- `productstatuses.list` - List all product statuses for a merchant

**Required Scopes**:
- `https://www.googleapis.com/auth/content` (read-only access)

**Authentication**:
- Service Account with Merchant Center access
- JSON credentials file specified via `GOOGLE_APPLICATION_CREDENTIALS`

### Service Account Setup

1. **Create Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to IAM & Admin → Service Accounts
   - Create new service account
   - Grant "Merchant Center Content" role

2. **Enable Content API**:
   - Go to APIs & Services → Library
   - Search for "Content API for Shopping"
   - Enable the API

3. **Grant Merchant Center Access**:
   - Go to [Google Merchant Center](https://merchants.google.com/)
   - Settings → Users
   - Add service account email as user with "Standard" access

4. **Download Credentials**:
   - In Service Accounts, click on your service account
   - Keys → Add Key → Create new key → JSON
   - Save as `credentials.json`
   - Set `GOOGLE_APPLICATION_CREDENTIALS` env variable to path

## Configuration

### Monitoring Settings

Edit `config.json` to customize behavior:

```json
{
  "monitoring": {
    "enabled": true,
    "alert_hours_start": 9,   // Start alerting at 9 AM
    "alert_hours_end": 18,    // Stop alerting at 6 PM
    "slack_webhook": null     // Optional Slack webhook for alerts
  }
}
```

### Client Configuration

Each client needs a `merchant_id` to enable disapproval tracking:

```json
{
  "clients": [
    {
      "name": "Tree2mydoor",
      "merchant_id": "107469209",  // Required for Merchant Center tracking
      "google_ads_customer_id": "4941701449",
      "enabled": true
    }
  ]
}
```

**Finding Merchant IDs**:
1. Go to [Google Merchant Center](https://merchants.google.com/)
2. Your merchant ID is shown in the top-left corner
3. Or check URL: `merchants.google.com/mc/accounts/{MERCHANT_ID}/`

## Integration with Product Impact Analyzer

### How They Work Together

**Product Monitoring** (10:00 AM):
- Detects that 5 products disappeared from feed
- Sends alert: "5 products missing from Tree2mydoor feed"

**Disapproval Monitoring** (10:30 AM):
- Checks Merchant Center status
- Finds those 5 products are disapproved
- Sends alert: "5 products disapproved due to missing GTIN"

**Result**: You now know WHY the products disappeared!

### Shared Infrastructure

Both monitoring systems use:
- Same configuration file (`config.json`)
- Same client list and merchant IDs
- Same email alert system
- Same business hours logic
- Same log file format

## Data Storage

### Snapshot Files

Located in `monitoring/`:

- `disapprovals_current.json` - Latest product status snapshot
- `disapprovals_previous.json` - Previous day's snapshot (for comparison)

**Purpose**: Detect newly disapproved products by comparing today vs yesterday.

### Snapshot Format

```json
{
  "timestamp": "2025-10-30T10:30:00",
  "clients": {
    "Tree2mydoor": [
      {
        "product_id": "online:en:GB:287",
        "title": "Olive Tree Large",
        "status": "disapproved",
        "destination_statuses": {
          "Shopping": {
            "status": "disapproved",
            "approved_countries": [],
            "pending_countries": [],
            "disapproved_countries": ["GB", "US"]
          }
        },
        "item_level_issues": [
          {
            "code": "missing_gtin",
            "servability": "disapproved",
            "resolution": "Add valid GTIN to product feed",
            "description": "Product is missing required GTIN",
            "detail": "GTIN is required for products in this category",
            "documentation": "https://support.google.com/merchants/...",
            "affected_countries": ["GB", "US"]
          }
        ],
        "last_checked": "2025-10-30T10:30:15"
      }
    ]
  }
}
```

## Common Disapproval Reasons

### Critical Issues (Policy Violations)

| Issue Code | Description | Resolution |
|------------|-------------|------------|
| `prohibited_content` | Product violates Google Shopping policies | Remove product or fix policy violation |
| `counterfeit` | Suspected counterfeit or replica | Provide proof of authenticity |
| `restricted` | Restricted product (weapons, drugs, etc.) | Remove from feed |
| `adult_content` | Adult or sexually suggestive content | Remove or use appropriate category |

### Warning Issues (Data Quality)

| Issue Code | Description | Resolution |
|------------|-------------|------------|
| `missing_gtin` | Product missing GTIN (barcode) | Add valid GTIN to feed |
| `invalid_price` | Price format is invalid | Fix price format (e.g., "29.99 GBP") |
| `missing_image_link` | Product image URL missing | Add valid image URL |
| `invalid_image_link` | Image URL broken or invalid | Fix image URL |
| `missing_title` | Product title missing | Add product title |
| `title_too_long` | Title exceeds character limit | Shorten title to <150 chars |
| `missing_description` | Product description missing | Add description |
| `out_of_stock` | Product marked as out of stock | Update availability or remove |

## Logs & Monitoring

### Log Files

| File | Purpose |
|------|---------|
| `~/.petesbrain-disapproval-monitor.log` | Standard output |
| `~/.petesbrain-disapproval-monitor-error.log` | Error output |

### View Logs

```bash
# Tail standard log
tail -f ~/.petesbrain-disapproval-monitor.log

# View last run
tail -20 ~/.petesbrain-disapproval-monitor.log

# Check for errors
cat ~/.petesbrain-disapproval-monitor-error.log
```

### Check Status

```bash
# Is LaunchAgent running?
launchctl list | grep disapproval-monitor

# View LaunchAgent details
launchctl print user/$(id -u)/com.petesbrain.disapproval-monitor

# Reload LaunchAgent (after config changes)
launchctl unload ~/Library/LaunchAgents/com.petesbrain.disapproval-monitor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.disapproval-monitor.plist
```

## Troubleshooting

### No Alerts Received

1. **Check Merchant Center API access**:
   ```bash
   .venv/bin/python3 merchant_center_tracker.py --client "Tree2mydoor"
   ```
   If you see "403 Forbidden", service account doesn't have Merchant Center access.

2. **Check business hours**:
   - Alerts only sent 9 AM - 6 PM, weekdays
   - Test mode bypasses this: `disapproval_monitor.py --test`

3. **Check email configuration**:
   - Verify `GMAIL_APP_PASSWORD` is set
   - Check error log for SMTP errors

4. **Check for new disapprovals**:
   - First run won't alert (establishes baseline)
   - Second run compares to baseline and alerts

### Service Account Permission Issues

**Error**: `403 Forbidden` or `USER_PERMISSION_DENIED`

**Solution**:
1. Go to [Google Merchant Center](https://merchants.google.com/)
2. Settings → Users
3. Add service account email with "Standard" access
4. Wait 5-10 minutes for permissions to propagate
5. Retry

### Invalid Merchant ID

**Error**: `Merchant ID not found` or `UNKNOWN merchant`

**Solution**:
1. Find correct merchant ID in Merchant Center (top-left corner)
2. Update `config.json` with correct merchant ID
3. Reload LaunchAgent

### LaunchAgent Not Running

```bash
# Check if loaded
launchctl list | grep disapproval-monitor

# If not loaded, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.disapproval-monitor.plist

# Check for errors
cat ~/.petesbrain-disapproval-monitor-error.log
```

## Best Practices

### Monitoring Frequency

**Recommended**: Daily at 10:30 AM (current default)

- Catches disapprovals within 24 hours
- Runs after product monitor (10:00 AM) for context
- Business hours only (no weekend spam)

**Not Recommended**: Hourly or more frequent

- Merchant Center status doesn't change that often
- Creates unnecessary API load
- Risk of hitting API quotas

### Alert Fatigue Prevention

1. **Fix issues promptly** - Don't let disapprovals pile up
2. **Use business hours** - No alerts at night or weekends
3. **Review severity** - Critical issues get immediate attention
4. **Check snapshots** - Only new disapprovals trigger emails

### Integration with Client Work

When you see a product disapproval alert:

1. **Check Merchant Center** for full details
2. **Update client CONTEXT.md** with the issue
3. **Fix the underlying cause** (missing data, policy violation, etc.)
4. **Monitor for re-approval** (usually within 24 hours)
5. **Document in client folder** for future reference

## Future Enhancements

Potential improvements:

1. **Auto-resolution** - Automatically fix common issues (e.g., add missing GTIN)
2. **Trend analysis** - Track which issue types are most common per client
3. **Integration with Product Impact** - Correlate disapprovals with revenue drops
4. **Merchant Center feed sync** - Automatically update feeds to fix issues
5. **Multi-country tracking** - Alert per-country status changes

## Support

Questions or issues?

- **Logs**: Check `~/.petesbrain-disapproval-monitor.log` first
- **Test run**: `python3 disapproval_monitor.py --test`
- **API docs**: [Google Content API](https://developers.google.com/shopping-content/reference/rest)
- **Ask Claude**: "Why am I not getting disapproval alerts?"

---

**Built with**: Python 3, Google Content API for Shopping, macOS LaunchAgent
**Version**: 1.0.0
**Release Date**: October 30, 2025
