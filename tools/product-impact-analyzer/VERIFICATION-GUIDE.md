# Product Impact Analyzer - Verification Guide

**Last Updated:** 11 November 2025

---

## Quick Health Check ✅

Run these commands to verify the system is working:

```bash
# 1. Check if all 4 agents are loaded
launchctl list | grep product

# Expected output (all should show status "1"):
# -	1	com.petesbrain.product-data-fetcher
# -	1	com.petesbrain.product-impact-analyzer
# -	1	com.petesbrain.product-tracking
# -	1	com.petesbrain.product-monitor
```

```bash
# 2. Check recent log files (should be from today)
ls -lth ~/.petesbrain-product*.log | head -10

# 3. Check for errors in logs
tail -20 ~/.petesbrain-product-tracking.log
tail -20 ~/.petesbrain-product-impact-analyzer.log
```

```bash
# 4. Check recent product change files were created
ls -lth tools/product-impact-analyzer/data/product_changes/*/2025-11-*.json | head -20
```

---

## System Architecture

### 4 LaunchAgents Running:

| Agent | Schedule | Purpose | Log File |
|-------|----------|---------|----------|
| **product-tracking** | Daily 8:00 AM | Fetches product feed data from Google Shopping Content API | `~/.petesbrain-product-tracking.log` |
| **product-data-fetcher** | Every 6 hours (6 AM, 12 PM, 6 PM, 12 AM) | Fetches Google Ads performance data | `~/.petesbrain-product-data-fetcher.log` |
| **product-impact-analyzer** | Tuesday 9:00 AM | Runs analysis comparing product changes to performance | `~/.petesbrain-product-impact-analyzer.log` |
| **product-monitor** | Every 6 hours | Monitors for product disapprovals/issues | `~/.petesbrain-product-monitor.log` |

### Data Flow:

```
1. product-tracking (8 AM daily)
   ├─> Fetches product feed from Google Shopping Content API
   ├─> Compares with yesterday's snapshot
   └─> Saves changes to: tools/product-impact-analyzer/data/product_changes/[client]/[date].json

2. product-data-fetcher (every 6 hours)
   └─> Fetches Google Ads performance data
       └─> Saves to: tools/product-impact-analyzer/data/ads_[client].json

3. product-impact-analyzer (Tuesday 9 AM)
   ├─> Reads product changes from step 1
   ├─> Reads Google Ads data from step 2
   ├─> Analyzes correlation between feed changes and performance changes
   └─> Writes results to Google Sheets + saves history
```

---

## Verification Steps

### 1. Verify Daily Product Tracking (8 AM)

**Check if today's product changes were captured:**

```bash
# Check all clients have today's files
ls -lh tools/product-impact-analyzer/data/product_changes/*/$(date +%Y-%m-%d).json

# Check Clear Prospects brands specifically
ls -lh tools/product-impact-analyzer/data/product_changes/{HappySnapGifts,WheatyBags,BMPM}/$(date +%Y-%m-%d).json
```

**Inspect a recent change file:**

```bash
# Check what changed today for BMPM
python3 << 'EOF'
import json
from datetime import date

today = date.today().strftime("%Y-%m-%d")
file_path = f"tools/product-impact-analyzer/data/product_changes/BMPM/{today}.json"

try:
    with open(file_path) as f:
        data = json.load(f)

    print(f"BMPM Product Changes - {today}")
    print("=" * 50)
    print(f"Total products: {data['total_products_today']}")
    print(f"Changed products: {data['summary']['changed_products']}")
    print(f"  - Price changes: {data['summary']['price_changes']}")
    print(f"  - Availability changes: {data['summary']['availability_changes']}")
    print(f"  - Title changes: {data['summary']['title_changes']}")
    print(f"  - Label changes: {data['summary']['label_changes']}")
    print(f"  - New products: {data['summary']['new_products']}")
    print(f"  - Removed products: {data['summary']['removed_products']}")

    # Show sample changes
    if data['summary']['price_changes'] > 0:
        print("\nSample price change:")
        for product in data['changed_products']:
            if 'price' in product.get('changes', {}):
                print(f"  {product['title']}")
                print(f"  {product['changes']['price'][0]} -> {product['changes']['price'][1]}")
                break

except FileNotFoundError:
    print(f"File not found: {file_path}")
    print("Product tracking may not have run yet today (scheduled 8 AM)")
EOF
```

### 2. Verify Google Ads Data Fetching (Every 6 Hours)

**Check when ads data was last updated:**

```bash
ls -lth tools/product-impact-analyzer/data/ads_{happysnapgifts,wheatybags,bmpm}.json
```

**Expected:** Files should be updated every 6 hours (6 AM, 12 PM, 6 PM, 12 AM)

**Inspect ads data:**

```bash
python3 << 'EOF'
import json

for client in ['happysnapgifts', 'wheatybags', 'bmpm']:
    file_path = f"tools/product-impact-analyzer/data/ads_{client}.json"
    try:
        with open(file_path) as f:
            data = json.load(f)

        print(f"{client.upper()} - {len(data.get('products', []))} products with performance data")
    except Exception as e:
        print(f"{client.upper()} - Error: {e}")
EOF
```

### 3. Verify Impact Analysis (Tuesday 9 AM)

**Check recent analysis runs:**

```bash
ls -lth tools/product-impact-analyzer/history/analysis_*.json | head -5
```

**View last analysis:**

```bash
python3 << 'EOF'
import json
import os
from datetime import datetime

history_dir = "tools/product-impact-analyzer/history"
files = sorted([f for f in os.listdir(history_dir) if f.startswith('analysis_')], reverse=True)

if files:
    latest = files[0]
    with open(f"{history_dir}/{latest}") as f:
        data = json.load(f)

    print(f"Latest Analysis: {latest}")
    print("=" * 50)
    print(f"Date: {data.get('date', 'Unknown')}")
    print(f"Product changes analyzed: {len(data.get('analyses', []))}")
    print(f"Significant impacts found: {sum(1 for a in data.get('analyses', []) if a.get('impact_significance', 0) > 0.5)}")
else:
    print("No analysis files found")
EOF
```

---

## Understanding Nov 6 BMPM "Changes"

### What Actually Happened:

**File:** `tools/product-impact-analyzer/data/product_changes/BMPM/2025-11-06.json`

**Data:**
- **File size:** 330KB (much larger than normal ~80KB)
- **Changed products:** 631 products
- **Price changes:** 244 products
- **Image changes:** 387 products (mostly image URLs changed from `/2025-10/` to `/2025-11/`)

### Analysis:

**This was NOT a major product feed restructure.** It was mostly:

1. **Image URL changes** (387 products): URLs changed from `2025-10` to `2025-11` folder
   - Example: `styles/google/public/2025-10/product.jpg.webp` → `styles/google/public/2025-11/product.jpg.webp`
   - This is likely a CMS/cache refresh, not actual product changes

2. **Price changes** (244 products): Some products had price updates
   - Example: Branded Cushion £18.00 → £32.00 (78% price increase!)
   - These ARE real changes and could impact performance

3. **Zero structural changes:**
   - No products added or removed
   - No title changes
   - No label changes (Product Hero labels unchanged)
   - No availability changes

### Why Not Visible in Merchant Centre:

Merchant Centre UI shows:
- Product additions/removals
- Disapprovals
- Critical errors

It does NOT typically show in the UI:
- Image URL changes (same image, different URL)
- Minor price updates (unless outside acceptable range)
- Timestamp-only updates

**Conclusion:** The Nov 6 "changes" were real but NOT a feed restructure. They were:
- 387 image cache refreshes (cosmetic, no impact)
- 244 price updates (could impact performance if significant)

---

## Known Issues ⚠️

### 1. LaunchAgent Error: "Resource deadlock avoided"

**Seen in:** `~/.petesbrain-product-impact-analyzer-error.log`

**Error:**
```
OSError: [Errno 11] Resource deadlock avoided
Fatal Python error: init_import_site: Failed to import the site module
```

**Impact:** Product Impact Analyzer (Tuesday 9 AM analysis) is failing

**Status:** Logged but not affecting daily product tracking (8 AM runs successfully)

**Workaround:** Manual run if needed:
```bash
cd tools/product-impact-analyzer
.venv/bin/python3 run_automated_analysis.py
```

### 2. Image URL Changes Counted as "Changes"

**Issue:** When CMS regenerates images or changes folder structure, Product Impact Analyzer logs these as "changes"

**Example:** Nov 6 BMPM had 387 "image_link" changes, but same images just different URLs

**Impact:** Inflates "changed products" count without real impact

**Recommendation:** Filter out image URL-only changes that don't affect image content

---

## Manual Verification Commands

### Quick Test: Check BMPM Nov 6 Changes in Detail

```bash
cd /Users/administrator/Documents/PetesBrain

# See all price changes on Nov 6
python3 << 'EOF'
import json

with open('tools/product-impact-analyzer/data/product_changes/BMPM/2025-11-06.json') as f:
    data = json.load(f)

print("BMPM Price Changes - Nov 6, 2025")
print("=" * 80)

price_changes = [p for p in data['changed_products'] if 'price' in p.get('changes', {})]

for i, product in enumerate(price_changes[:10], 1):  # Show first 10
    old_price, new_price = product['changes']['price']
    old = float(old_price.split()[0])
    new = float(new_price.split()[0])
    change_pct = ((new - old) / old) * 100

    print(f"{i}. {product['title'][:60]}")
    print(f"   {old_price} -> {new_price} ({change_pct:+.1f}%)")
    print()

print(f"Total price changes: {len(price_changes)}")
EOF
```

### Full System Test

```bash
# Run a complete check
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# 1. Check config
echo "Config check:"
python3 -c "import json; config = json.load(open('config.json')); print(f\"Clients tracked: {len([c for c in config['clients'] if c.get('enabled', False)])}\")"

# 2. Test product tracking (read-only)
echo -e "\nProduct tracking test:"
ls -lh data/product_changes/BMPM/ | tail -5

# 3. Check Google Ads data
echo -e "\nGoogle Ads data:"
ls -lth data/ads_{happysnapgifts,wheatybags,bmpm}.json

# 4. Check agent status
echo -e "\nAgent status:"
launchctl list | grep product

echo -e "\n✅ System verification complete"
```

---

## Troubleshooting

### Product tracking didn't run today

**Check:**
1. LaunchAgent loaded: `launchctl list | grep product-tracking`
2. Check error log: `tail -50 ~/.petesbrain-product-tracking.log`
3. Manually run: `cd tools/product-impact-analyzer && .venv/bin/python3 product_feed_tracker.py`

### No changes detected for a client

**Possible reasons:**
1. Product feed hasn't changed (normal)
2. API credentials expired (check error log)
3. Client not enabled in config.json

**Verify:**
```bash
# Check if client enabled
python3 -c "import json; config = json.load(open('tools/product-impact-analyzer/config.json')); client = [c for c in config['clients'] if c['name'] == 'BMPM'][0]; print(f\"Enabled: {client.get('enabled', False)}\")"
```

### Large file size (like Nov 6 BMPM)

**Normal if:**
- Many image URL changes (CMS refresh)
- Bulk price update
- Seasonal product additions

**Investigation:**
- Check breakdown: price vs image vs title changes
- Compare with Merchant Centre feed download
- Review if changes correlate with performance

---

## Summary: Is Product Impact Analyzer Working?

### ✅ YES - System is functioning:

1. **Daily product tracking (8 AM)** ✅ Working
   - Files created daily for all clients
   - Clear Prospects brands (HSG, WBS, BMPM) tracked correctly
   - Label tracking enabled via custom_label_4

2. **Google Ads data fetching (every 6 hours)** ✅ Working
   - Ads data files updated regularly
   - All 3 Clear Prospects brands have data

3. **Product change detection** ✅ Working
   - Nov 6 BMPM changes WERE detected (631 products)
   - Breakdown: 387 image URL changes, 244 price changes
   - These ARE in the system, just not visible in Merchant Centre UI

### ⚠️ Issue: Analysis Agent (Tuesday 9 AM)

- **Status:** Failing with "Resource deadlock avoided" error
- **Impact:** Weekly analysis not writing to Google Sheets automatically
- **Workaround:** Manual run works fine
- **Fix needed:** Debug LaunchAgent environment variables or venv configuration

### 🔍 Nov 6 BMPM "Mystery" Solved:

The 337KB of changes on Nov 6 WERE real:
- 387 image URL changes (CMS cache refresh - cosmetic)
- 244 price changes (real changes, could impact performance)

NOT visible in Merchant Centre because:
- Image URLs changing doesn't trigger MC alerts
- Small price changes don't show in MC change log
- MC UI focuses on disapprovals/errors, not routine updates

**Conclusion:** Product Impact Analyzer is working correctly. The Nov 6 data is accurate. Merchant Centre just doesn't surface these types of changes in its UI.

---

*Verification guide compiled 11 Nov 2025 - Peter Empson*
