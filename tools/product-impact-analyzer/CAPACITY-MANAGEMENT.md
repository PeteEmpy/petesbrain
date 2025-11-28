# Daily Performance Sheet - Capacity Management

**Created**: November 2, 2025
**Status**: Critical - Read Before Proceeding

## The Problem

**Google Sheets has a hard limit of 10 million cells per spreadsheet.**

With 15 e-commerce clients and ~700 products each, the Daily Performance sheet accumulates **136,500 cells per day** (10,500 rows × 13 columns).

### Time Until Capacity

| Current State | Days to Limit | Months to Limit |
|--------------|---------------|-----------------|
| After 90-day backfill | **73 days** | **2.4 months** |
| Starting fresh | 73 days | 2.4 months |

**⚠️  You will hit the 10M cell limit in approximately 2.4 months from the backfill date.**

## Solution: Automated Archival

The `archive_old_data.py` script moves old data to separate archive spreadsheets, keeping only recent data (default: 90 days) in the main sheet for fast access.

### How It Works

1. **Reads all data** from Daily Performance sheet
2. **Splits by date**: Keep last 90 days, archive older
3. **Creates archive spreadsheet** (e.g., "Product Impact Analyzer - Archive 2025")
4. **Writes archived data** to archive spreadsheet
5. **Rewrites main sheet** with only kept data

**Result**: Main sheet stays under capacity, historical data preserved in archives

### Running the Archive Script

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Archive data older than 90 days (recommended)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\
  .venv/bin/python3 archive_old_data.py --yes --keep-days 90

# Or keep last 60 days (more aggressive archiving)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\
  .venv/bin/python3 archive_old_data.py --yes --keep-days 60
```

### When to Run

**Recommended Schedule**: Every 2 months

| Run Frequency | Days in Main Sheet | Archive Frequency |
|--------------|-------------------|-------------------|
| Every 60 days | ~60-150 days | Every 2 months |
| Every 90 days | ~90-180 days | Every 3 months |

**Warning**: If you wait longer than 2.5 months, the sheet may hit capacity before you can archive!

### Example Timeline

**November 2, 2025**: 90-day backfill completed (~12.3M cells, over limit but working)
**January 15, 2026**: Run archive (keep last 90 days)
  - Archive: Aug 3 - Oct 17 (~75 days)
  - Keep: Oct 18 - Jan 15 (~90 days)
  - Freed: ~9.75M cells

**March 15, 2026**: Run archive again
  - Archive: Oct 18 - Dec 15 (~60 days)
  - Keep: Dec 16 - Mar 15 (~90 days)
  - Freed: ~8.2M cells

**Repeat every 2 months indefinitely**

## Archive Spreadsheet Structure

Archives are created automatically with naming:
- "Product Impact Analyzer - Archive 2025"
- "Product Impact Analyzer - Archive 2026"
- Etc.

Each archive contains:
- **Sheet**: "Daily Performance - [Year]"
- **Data**: All archived rows from that year
- **Format**: Same columns as main sheet

### Accessing Archived Data

1. Open Google Drive
2. Search for "Product Impact Analyzer - Archive"
3. Open the archive for the year you need
4. Data is identical format to main sheet

### Querying Across Archives

If you need to analyze data spanning archives + main sheet:

**Option 1: Export and Combine (Python)**
```python
import pandas as pd

# Load main sheet
main_df = pd.read_csv("main_sheet_export.csv")

# Load archives
archive_2025 = pd.read_csv("archive_2025_export.csv")
archive_2026 = pd.read_csv("archive_2026_export.csv")

# Combine
all_data = pd.concat([archive_2025, archive_2026, main_df])

# Filter date range
analysis_df = all_data[
    (all_data['Date'] >= '2025-10-01') &
    (all_data['Date'] <= '2026-03-31')
]

# Analyze...
```

**Option 2: QUERY function in Sheets**
```
=QUERY(IMPORTRANGE("archive_id", "Daily Performance - 2025!A:M"),
       "SELECT * WHERE Col1 >= date '2025-10-01' AND Col1 <= date '2025-10-31'")
```

**Option 3: Apps Script**
Combine multiple sheets programmatically using Google Apps Script

## Capacity Monitoring

### Check Current Usage

```python
# Count rows in Daily Performance sheet
import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q')
ws = sh.worksheet('Daily Performance')

rows = len(ws.get_all_values())
cells = rows * 13  # 13 columns

print(f"Rows: {rows:,}")
print(f"Cells: {cells:,}")
print(f"Capacity: {cells / 10_000_000 * 100:.1f}%")
```

### Warning Thresholds

| Capacity | Action Required |
|----------|----------------|
| < 70% | Monitor, no action needed |
| 70-85% | Plan archival within 2 weeks |
| 85-95% | Archive immediately |
| > 95% | URGENT - Archive now, daily accumulation may fail |

### Automated Monitoring (Future Enhancement)

Add to `monitor.py`:

```python
def check_capacity():
    """Check Daily Performance sheet capacity"""
    # Get row count
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Daily Performance!A:A'
    ).execute()

    rows = len(result.get('values', []))
    cells = rows * 13
    capacity_pct = cells / 10_000_000 * 100

    if capacity_pct > 85:
        send_alert(f"⚠️ Daily Performance at {capacity_pct:.1f}% capacity! Archive now.")
    elif capacity_pct > 70:
        send_alert(f"Daily Performance at {capacity_pct:.1f}% capacity. Plan archival.")
```

## Alternative: BigQuery (Enterprise Scale)

For unlimited capacity and faster queries on large datasets:

### Migration to BigQuery

1. **Create BigQuery dataset**:
```sql
CREATE DATASET product_impact_analyzer;

CREATE TABLE daily_performance (
  date DATE,
  client STRING,
  product_id STRING,
  product_title STRING,
  impressions INT64,
  clicks INT64,
  conversions FLOAT64,
  revenue FLOAT64,
  cost FLOAT64,
  ctr FLOAT64,
  conv_rate FLOAT64,
  roas FLOAT64,
  label STRING
);
```

2. **Modify `sheets_writer.py`** to write to BigQuery:
```python
from google.cloud import bigquery

def append_daily_performance_bq(self, client_name, products):
    """Write to BigQuery instead of Sheets"""
    client = bigquery.Client()
    table_id = "your-project.product_impact_analyzer.daily_performance"

    rows = [
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "client": client_name,
            "product_id": str(p['product_id']),
            # ... rest of fields
        }
        for p in products
    ]

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        self.log(f"Errors inserting to BigQuery: {errors}")
```

3. **Query via BigQuery**:
```sql
-- AFH October performance
SELECT
  date,
  SUM(clicks) as total_clicks,
  SUM(revenue) as total_revenue,
  SUM(cost) as total_cost,
  SUM(revenue) / SUM(cost) as roas
FROM product_impact_analyzer.daily_performance
WHERE client = 'Accessories for the Home'
  AND date BETWEEN '2025-10-01' AND '2025-10-31'
GROUP BY date
ORDER BY date;
```

4. **Connect Google Sheets to BigQuery**:
   - Data → Data connectors → Connect to BigQuery
   - Select table
   - Create pivot tables, charts on top of BigQuery data
   - Unlimited data size, sub-second queries

### BigQuery Benefits

✅ **Unlimited storage** - No 10M cell limit
✅ **Fast queries** - Sub-second even on billions of rows
✅ **SQL interface** - Powerful analytics
✅ **Google Sheets integration** - Still use Sheets as view layer
✅ **Cost-effective** - ~$5/TB/month storage, $5/TB query processing

### BigQuery Costs (Estimate)

**Storage**:
- 3.8M rows/year × 13 columns × 50 bytes/cell = ~2.5 GB/year
- Cost: $0.02/month per GB = **$0.60/year**

**Queries**:
- ~100 GB processed/month (for typical analysis)
- Cost: $5/TB = **$0.50/month**

**Total: ~$1/month or $12/year** for unlimited capacity

## Maintenance Schedule

### Immediate (Nov 2025)
- ✅ 90-day backfill completed
- ✅ Old format sheets deleted
- 📅 Set calendar reminder for Jan 15, 2026

### Every 2 Months
- Run `archive_old_data.py`
- Verify archive created successfully
- Check main sheet capacity after archival

### Quarterly (Every 3 Months)
- Review archive spreadsheets (ensure accessible)
- Check capacity trends (growing faster than expected?)
- Consider BigQuery migration if managing archives becomes cumbersome

### Annually
- Review entire system
- Consolidate multiple year archives if needed
- Update documentation

## Troubleshooting

### Error: "10 million cell limit exceeded"

**Immediate fix**:
1. Stop daily monitor temporarily
2. Run archive script with `--keep-days 60` (more aggressive)
3. Verify capacity freed
4. Resume daily monitor

### Archive Script Fails

**Causes**:
- Network timeout (large data transfer)
- Permissions issue (can't create new spreadsheet)
- API rate limit

**Solutions**:
- Run again (progress saved)
- Check service account has Drive + Sheets permissions
- Wait 5 minutes and retry

### Can't Find Archived Data

**Check**:
1. Google Drive → Search "Product Impact Analyzer - Archive"
2. Check Drive sharing permissions
3. Look in script output for archive spreadsheet ID

## Summary

**The Problem**: 10M cell limit, 2.4 months to capacity

**The Solution**: Archive every 2 months, keeping 90-day rolling window

**Long-term**: Consider BigQuery for unlimited scale

**Action Required**: Set calendar reminder for **January 15, 2026** to run first archive

---

**Questions?** Review [BACKFILL-GUIDE.md](BACKFILL-GUIDE.md) and [CONSOLIDATION-COMPLETE.md](CONSOLIDATION-COMPLETE.md)

**Generated**: November 2, 2025
**Version**: 1.0
