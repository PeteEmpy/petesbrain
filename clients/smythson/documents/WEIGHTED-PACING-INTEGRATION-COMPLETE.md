# Smythson Q4 Dashboard - Weighted Pacing Integration

**Date:** 2025-11-07
**Status:** ✅ COMPLETE - Integration successful, awaiting quota reset for sheet update

---

## What Was Done

Integrated **actual Q4 2024 revenue distribution** into the dashboard's weighted pacing calculations, replacing assumed multipliers with real historical data.

---

## Changes Made

### 1. Revenue Distribution Analysis Script

**File:** `clients/smythson/scripts/calculate-q4-2024-revenue-distribution.py`

**Purpose:** Fetch and analyze November 2024 UK revenue data from Google Ads

**Key Findings:**
- Total November 2024 revenue: £608,165
- Average daily revenue: £20,272
- **Black Friday (Nov 23):** 2.39x average = £48,543 (8.0% of month)
- **Cyber Monday (Nov 29):** 2.65x average = £53,710 (8.8% of month)
- **Black Friday week (Nov 22-30):** 53.2% of entire month's revenue
- **First half (Nov 1-15):** Only 28% of revenue
- **Second half (Nov 16-30):** 72% of revenue

**Output:** `q4-2024-revenue-distribution.json` containing daily multipliers for each day of November 2024

---

### 2. Dashboard Script Updates

**File:** `clients/smythson/scripts/update-q4-dashboard.py`

**Function Updated:** `calculate_weighted_pacing()` (lines 198-305)

**Changes:**

#### Old Approach (Assumed Multipliers):
```python
# Hardcoded assumptions
peak_dates = {
    datetime(2025, 11, 25): 1.5,  # Black Friday weekend
    datetime(2025, 11, 29): 1.5,  # Cyber Monday
    datetime(2025, 12, 15): 1.3,  # Pre-Christmas
}
```

#### New Approach (Real Data):
```python
# Load actual Q4 2024 revenue distribution
with open('q4-2024-revenue-distribution.json', 'r') as f:
    q4_2024_data = json.load(f)

# Extract daily multipliers (e.g., Nov 23 = 2.39x)
q4_multipliers = {}
for date_str, multiplier in q4_2024_data['daily_multipliers'].items():
    date_parts = date_str.split('-')
    month = int(date_parts[1])
    day = int(date_parts[2])
    q4_multipliers[(month, day)] = multiplier

# Apply real multipliers to each day
for day_offset in range(total_days):
    day = start_date + timedelta(days=day_offset)
    day_key = (day.month, day.day)

    if day_key in q4_multipliers:
        weight = q4_multipliers[day_key]  # Real 2024 data
    else:
        weight = 1.0  # Default
```

---

## Impact on Dashboard

### Example: November 7, 2025 (Today)

**Linear Pacing:** 14.8% (4 days / 27 days)
**Weighted Pacing:** 7.2% (based on Q4 2024 actual distribution)
**Difference:** -7.6% (weighted shows LOWER expectation early in month)

**Why this matters:**
- Dashboard now shows realistic expected revenue at any point in November
- Early month (Nov 3-14): Lower expectations (0.4x - 0.6x multipliers)
- Mid month (Nov 15-21): Building momentum (0.6x - 1.2x multipliers)
- Black Friday week (Nov 22-30): Major spike (1.8x - 2.7x multipliers)

### Example: November 23, 2025 (Black Friday)

**Linear Pacing:** 74.1% (20 days / 27 days)
**Weighted Pacing:** 54.5% (based on Q4 2024 actual distribution)
**Difference:** -19.6% (weighted shows even by Black Friday, only half the revenue achieved)

---

## Validation Tests

**Test 1: Data Loading** ✅
```
✅ Q4 2024 data loaded successfully
Total days with data: 30
```

**Test 2: Key Multipliers** ✅
```
Nov 1 (early): 0.41x
Nov 15 (mid): 0.56x
Nov 22 (BF week start): 1.76x
Nov 23 (Black Friday): 2.39x
Nov 29 (Cyber Monday): 2.65x
```

**Test 3: Weighted Pacing Calculation** ✅
```
Nov 7: Linear 14.8% vs Weighted 7.2% (-7.6% difference)
Nov 23: Linear 74.1% vs Weighted 54.5% (-19.6% difference)
```

---

## Next Dashboard Update

**Status:** Script ready, but Google Sheets API quota exceeded (60 writes/minute limit)

**When quota resets** (within 1 hour), the script will:
1. Load Q4 2024 revenue distribution automatically
2. Calculate weighted expected revenue using real historical patterns
3. Update dashboard with accurate "Expected Revenue" values
4. Show traffic light indicators (🟢🟡🔴) based on realistic pacing

**Manual trigger** (if needed):
```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts
source .venv/bin/activate
python3 update-q4-dashboard.py
```

**Automated schedule:** Daily at 7:00 AM via LaunchAgent

---

## December 2024 Data - Still Pending

**Status:** November 2024 data integrated ✅, December 2024 data still using fallback multipliers

**Fallback multipliers for December:**
- Dec 15-23 (pre-Christmas): 1.3x
- Dec 24-25 (Christmas): 0.8x / 0.6x
- Dec 26-28 (post-Christmas): 0.9x

**To fetch December 2024 data:**
1. Update `calculate-q4-2024-revenue-distribution.py` with December date range
2. Fetch Dec 1-31, 2024 UK revenue via Google Ads API
3. Add December multipliers to `q4-2024-revenue-distribution.json`
4. December pacing will automatically use real data

---

## Technical Notes

### Error Handling
The script includes fallback behavior:
- If `q4-2024-revenue-distribution.json` cannot be loaded, falls back to basic multipliers
- If a specific day has no data, defaults to 1.0x multiplier
- December 2024 uses fallback multipliers until real data is fetched

### Phase Transition Adjustments
The script still applies a 0.85x multiplier for 3 days after major account changes:
- Nov 15: Phase 2 (UK ROAS reduction, ROW launch)
- Nov 25: Phase 3 (USA budget increase)
- Dec 1: Phase 4 (All regions ROAS reductions)

This accounts for Smart Bidding re-learning periods after strategic changes.

---

## Summary

✅ **Q4 2024 revenue distribution analyzed** (November 2024 UK actual data)
✅ **Daily multipliers calculated** (0.41x early November → 2.65x Cyber Monday)
✅ **Dashboard script updated** to load and use real historical data
✅ **Weighted pacing function replaced** assumed multipliers with actual Q4 2024 patterns
✅ **Testing validated** correct loading and calculation
⏳ **Dashboard update pending** Google Sheets API quota reset (within 1 hour)
📋 **December 2024 data** still needed (currently using fallback multipliers)

The dashboard now answers your original question: **"What proportion of revenue was achieved last year on the various days during the month?"** by using actual Q4 2024 data instead of assumptions.
