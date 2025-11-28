# Historical Data Backfill Guide

**Date**: November 2, 2025
**Purpose**: Populate 60-90 days of historical product performance data into Daily Performance sheet

## Overview

The backfill script fetches historical shopping performance data from Google Ads API and writes it to the Daily Performance sheet in Google Sheets. This provides historical baseline for analyzing past issues (like the October AFH sales volatility).

## What Gets Backfilled

**Data Range**: 60-90 days (user-configurable)
**Clients**: All 13 enabled e-commerce clients with `merchant_id` in config.json
**Products**: All products that had impressions during the date range
**Metrics**: Impressions, clicks, conversions, revenue, cost, CTR, conversion rate, ROAS

**Estimated Volume** (90 days):
- ~820,000 rows (13 clients × 90 days × ~700 products/client)
- ~10.7 million cells (13 columns per row)
- Well within Google Sheets limits (10M cells per sheet)

## Running the Backfill

### Prerequisites

1. Google Ads API credentials configured (`google-ads.yaml`)
2. Google Sheets API credentials set (`GOOGLE_APPLICATION_CREDENTIALS`)
3. Daily Performance sheet exists with headers (should already be created)

### Command

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

.venv/bin/python3 backfill_historical_data.py
```

### Interactive Prompts

**Prompt 1**: Confirmation
```
Continue? (yes/no):
```
Type `yes` to proceed.

**Prompt 2**: Days to backfill
```
How many days to backfill? (60-90, default 90):
```
- Press ENTER for 90 days (recommended)
- Or type a number between 1-120

### What Happens During Backfill

1. **Load Configuration**
   - Reads `config.json` for enabled clients
   - Initializes Google Ads and Google Sheets API clients

2. **For Each Client** (13 clients):
   - Fetches shopping performance data from Google Ads API
   - Groups by date (e.g., 90 dates per client)
   - Writes to Daily Performance sheet in batches of 5000 rows
   - Waits 1 second between batches (API rate limiting)
   - Waits 2 seconds between clients

3. **Progress Tracking**
   - Saves progress after each client completes
   - If interrupted (Ctrl+C), can resume from where it stopped
   - Progress stored in `data/backfill_progress.json`

4. **Completion**
   - Prints summary (success/error counts)
   - Cleans up progress file if all successful
   - Provides link to view data in Google Sheets

### Expected Duration

**Rough estimate**:
- 13 clients × (30 seconds fetch + 60 seconds write) = ~20 minutes
- Plus rate limiting delays = **~25-30 minutes total**

Actual time depends on:
- Google Ads API response times
- Google Sheets API write speeds
- Number of products per client
- Network latency

## Safety Features

### API Rate Limiting

- **Between batches**: 1 second delay
- **Between clients**: 2 seconds delay
- **Batch size**: 5000 rows per API call (well within Google's limits)

This ensures the script won't hit rate limits or cause performance issues.

### Progress Tracking

If the script is interrupted (network issue, Ctrl+C, error):
1. Progress is saved after each client completes
2. Run the script again - it will resume from the last completed client
3. Already-completed clients are skipped automatically

**Progress file**: `data/backfill_progress.json`

Example:
```json
{
  "completed_clients": ["Tree2mydoor", "Smythson UK", "Uno Lights"],
  "last_updated": "2025-11-02T14:23:45.123456"
}
```

### Error Handling

- Google Ads API errors are caught and logged
- Google Sheets API errors are caught and logged
- Script continues to next client if one fails
- Final summary shows which clients had errors
- Run again to retry failed clients

## Resuming After Interruption

If the script is interrupted, simply run it again:

```bash
.venv/bin/python3 backfill_historical_data.py
```

You'll see:
```
Resuming from previous run. Already completed: 5 clients
[SKIPPED] Tree2mydoor (already completed)
[SKIPPED] Smythson UK (already completed)
...
Processing: Accessories for the Home
```

## Verifying the Backfill

### Check Google Sheets

Open the spreadsheet:
https://docs.google.com/spreadsheets/d/1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q/edit

**Daily Performance sheet**:
- Should now have rows going back 60-90 days
- Sort by Date column (A) to see oldest dates first
- Check for all 13 client names in Client column (B)

### Verify Date Range

```python
# In a Python shell or notebook:
import pandas as pd

# Load the sheet
df = pd.read_csv("exported_daily_performance.csv")  # Export from Sheets

# Check date range
print(f"Earliest date: {df['Date'].min()}")
print(f"Latest date: {df['Date'].max()}")
print(f"Total days: {df['Date'].nunique()}")

# Check clients
print(f"Clients: {df['Client'].unique()}")
print(f"Total rows: {len(df)}")
```

### Verify Product Counts

```python
# Products per client
print(df.groupby('Client')['Product ID'].nunique())

# Total products across all clients
print(f"Total unique products: {df['Product ID'].nunique()}")
```

## Analyzing Historical Data

Once backfilled, you can analyze past issues:

### Example: Accessories for the Home October Volatility

```python
# Filter for AFH in October
afh_oct = df[
    (df['Client'] == 'Accessories for the Home') &
    (df['Date'] >= '2025-10-01') &
    (df['Date'] <= '2025-10-31')
]

# Daily aggregates
daily = afh_oct.groupby('Date').agg({
    'Clicks': 'sum',
    'Revenue (£)': 'sum',
    'Cost (£)': 'sum'
}).reset_index()

daily['ROAS'] = daily['Revenue (£)'] / daily['Cost (£)']
daily['Clicks per £100 Revenue'] = daily['Clicks'] / daily['Revenue (£)'] * 100

# Plot trends
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(daily['Date'], daily['Clicks per £100 Revenue'])
plt.xlabel('Date')
plt.ylabel('Clicks per £100 Revenue')
plt.title('AFH Traffic Efficiency - October 2025')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Create Pivot Tables in Google Sheets

**Daily aggregates by client**:
1. Data → Pivot table
2. Rows: Date, Client
3. Values: SUM of Clicks, SUM of Revenue, SUM of Cost
4. Calculated fields: ROAS = Revenue / Cost

**Product performance ranking**:
1. Data → Pivot table
2. Rows: Client, Product Title
3. Values: SUM of Revenue, SUM of Clicks, SUM of Conversions
4. Filter: Date range (e.g., last 30 days)
5. Sort by Revenue descending

## Troubleshooting

### Error: "GOOGLE_APPLICATION_CREDENTIALS not set"

**Solution**:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Or run with credentials:
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \
  .venv/bin/python3 backfill_historical_data.py
```

### Error: "Invalid range 'Daily Performance!A2'"

**Cause**: Daily Performance sheet doesn't exist

**Solution**:
```bash
# Create the sheets first
.venv/bin/python3 create_sheets.py

# Write headers
# (Should already be done, but if not, run monitor once)
.venv/bin/python3 monitor.py
```

### Error: "Resource exhausted" or "Rate limit exceeded"

**Cause**: Too many API requests

**Solution**:
- Script already includes rate limiting
- Wait 5-10 minutes and run again (will resume from progress)
- Consider reducing batch size in script (line 195: `batch_size = 5000`)

### Slow Performance

**Causes**:
- Large number of products per client
- Network latency
- Google Sheets write performance

**Solutions**:
- Let it run - it's a one-time operation
- Run during off-peak hours (evening/night)
- Consider reducing `days_back` (e.g., 60 instead of 90)

### Script Hangs or Freezes

**Solution**:
- Press Ctrl+C to interrupt
- Check logs for error messages
- Run again (will resume from progress)

### Some Clients Show No Data

**Causes**:
1. Client had no products with impressions during date range
2. Customer ID incorrect in config.json
3. API authentication issue

**Solution**:
```bash
# Test fetch for specific client
.venv/bin/python3 -c "
from backfill_historical_data import HistoricalDataBackfiller
from pathlib import Path

backfiller = HistoricalDataBackfiller(Path('config.json'), days_back=30)
data = backfiller.fetch_client_data('CUSTOMER_ID', 30)
print(f'Fetched {len(data)} days of data')
"
```

## After Backfill Completes

### Clean Up (Optional)

The progress file is automatically deleted on successful completion. If you want to manually clean up:

```bash
rm data/backfill_progress.json
```

### Validate Data Quality

1. Check date range covers expected period
2. Verify all 13 clients have data
3. Spot-check a few products against Google Ads UI
4. Compare aggregates to account-level metrics

### Start Using Historical Data

Now you can:
- Analyze past performance issues (e.g., AFH October volatility)
- Compare current performance to historical baselines
- Identify seasonal patterns
- Track product lifecycle changes over time
- Validate Product Hero label transitions

## Re-Running the Backfill

You typically only need to run this once, but you can re-run if:
- You want to refresh historical data
- You added new clients to config.json
- Initial backfill had errors

**Note**: Running again will **append** data, not replace it. If you want to replace, manually delete rows from Daily Performance sheet first.

## Support

**Logs**: Check script output for detailed progress and error messages

**Progress file**: `data/backfill_progress.json` shows completed clients

**Spreadsheet**: https://docs.google.com/spreadsheets/d/1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q/edit

**Questions**: Review [CONSOLIDATION-COMPLETE.md](CONSOLIDATION-COMPLETE.md) for system architecture

---

**Generated**: November 2, 2025
**Version**: 1.0
**Script**: `backfill_historical_data.py`
