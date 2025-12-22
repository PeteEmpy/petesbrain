# Time Comparison System

Automated time comparison utilities for Google Ads reporting based on 8020brain.com principles.

**Purpose**: Reveal what's changing in performance through Week over Week (WoW), Month over Month (MoM), and Year over Year (YoY) comparisons with proper same-day alignment, automatic safeguards, and actionable insights.

---

## 🟢 **Quick Start**

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/shared')))
from time_comparisons import get_comparison_periods, parse_performance_data, calculate_changes, format_comparison_report

# 1. Get properly aligned date ranges
periods = get_comparison_periods('WoW')  # 'WoW', 'MoM', or 'YoY'

# 2. Query Google Ads for both periods
current_result = mcp__google_ads__run_gaql(customer_id, manager_id, query_current)
previous_result = mcp__google_ads__run_gaql(customer_id, manager_id, query_previous)

# 3. Parse results
current_metrics = parse_performance_data(current_result)
previous_metrics = parse_performance_data(previous_result)

# 4. Calculate changes with safeguards
changes = calculate_changes(current_metrics, previous_metrics)

# 5. Generate formatted report section
comparison_report = format_comparison_report('Client Name', periods, changes, 'WoW')
```

Done! You now have a complete time comparison section ready to insert into your report.

---

## 🟢 **Why Time Comparisons Matter**

**Time comparisons answer ONE question: "What changed?"**

Without comparison, you just have numbers. With comparison, you have **insight**.

### The Three Core Comparisons

| Comparison | What It Shows | When To Use | Example |
|------------|---------------|-------------|---------|
| **WoW** | Recent trends, immediate changes | Weekly reports, spotting problems quickly | "ROAS dropped 11% this week - investigate" |
| **MoM** | Medium-term trends, smooths volatility | Monthly reviews, strategic planning | "November: £2.2K spend. December: £2.8K spend (+27%)" |
| **YoY** | Seasonal patterns, true growth | Quarterly reviews, understanding if growth is real or seasonal | "Dec 2024: £2.8K. Dec 2025: £3.4K (+21% YoY growth)" |

### Critical Principles

✅ **Same day > same date**: Comparing Monday-to-Monday is more meaningful than comparing the 15th to the 15th (day-of-week patterns matter)

✅ **Both absolute + percentage**: "CPA increased £10" (absolute) and "CPA increased 25%" (percentage) tell different stories

✅ **Safeguards required**: Low volume, holidays, and paused campaigns create misleading comparisons - flag them

---

## 🟢 **Function Reference**

### `get_comparison_periods(comparison_type, reference_date=None)`

Calculate date ranges for time comparisons with same-day alignment.

**Parameters:**
- `comparison_type` (str): `'WoW'`, `'MoM'`, or `'YoY'`
- `reference_date` (datetime, optional): Reference date (defaults to today)

**Returns:**
```python
{
    'current': {'start': '2025-12-15', 'end': '2025-12-21'},
    'previous': {'start': '2025-12-08', 'end': '2025-12-14'}
}
```

**Example:**
```python
# WoW: Current week (Mon-Sun) vs previous week (Mon-Sun)
wow_periods = get_comparison_periods('WoW')

# MoM: Current month (1st to last day) vs previous month
mom_periods = get_comparison_periods('MoM')

# YoY: Current week vs same week last year
yoy_periods = get_comparison_periods('YoY')
```

**Same-Day Alignment Guarantee:**
- WoW: Monday-to-Monday (never compares different days of week)
- MoM: 1st-to-last-day of each month
- YoY: Same calendar week (handles leap years)

---

### `parse_performance_data(api_result)`

Convert Google Ads API result to usable performance metrics.

**Parameters:**
- `api_result` (dict): Result from `mcp__google_ads__run_gaql()`

**Returns:**
```python
{
    'spend': 520.50,
    'conversions': 12,
    'revenue': 2080.00,
    'roas': 4.0,
    'cpa': 43.33
}
```

**Example:**
```python
query = """
    SELECT
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM customer
    WHERE segments.date >= '2025-12-09' AND segments.date <= '2025-12-15'
"""

result = mcp__google_ads__run_gaql(customer_id='8573235780', manager_id='2569949686', query=query)
metrics = parse_performance_data(result)

# metrics = {'spend': 520.50, 'conversions': 12, 'revenue': 2080.00, 'roas': 4.0, 'cpa': 43.33}
```

**Handles Edge Cases:**
- Returns zeros for empty/None results (prevents division errors)
- Converts micros to currency (£500,000,000 → £500.00)
- Calculates ROAS and CPA automatically

---

### `calculate_changes(current, previous)`

Calculate absolute and percentage changes with safeguard flags.

**Parameters:**
- `current` (dict): Current period metrics from `parse_performance_data()`
- `previous` (dict): Previous period metrics from `parse_performance_data()`

**Returns:**
```python
{
    'spend': {
        'current': 520.00,
        'previous': 500.00,
        'absolute': 20.00,
        'percentage': 4.0
    },
    'roas': {
        'current': 4.0,
        'previous': 4.5,
        'absolute': -0.5,
        'percentage': -11.1
    },
    # ... (conversions, revenue, cpa)
    'flags': ['LOW_VOLUME', 'LARGE_ROAS_CHANGE']
}
```

**Safeguard Flags:**

| Flag | Trigger | Meaning |
|------|---------|---------|
| `LOW_VOLUME` | <10 conversions in either period | Comparisons may be volatile (small sample size) |
| `LARGE_SPEND_CHANGE` | >50% spend change | Investigate cause (budget change? paused campaign?) |
| `LARGE_ROAS_CHANGE` | >20% ROAS change | Investigate cause (significant performance shift) |
| `ZERO_PREVIOUS_[METRIC]` | Previous period had zero value | Percentage change undefined (100% increase from zero) |

**Example:**
```python
current = {'spend': 520, 'conversions': 8, 'revenue': 2080, 'roas': 4.0, 'cpa': 65.0}
previous = {'spend': 500, 'conversions': 15, 'revenue': 2250, 'roas': 4.5, 'cpa': 33.33}

changes = calculate_changes(current, previous)

# changes['roas'] = {'current': 4.0, 'previous': 4.5, 'absolute': -0.5, 'percentage': -11.1}
# changes['flags'] = ['LOW_VOLUME']  # Only 8 conversions in current period
```

---

### `format_comparison_report(client_name, periods, changes, comparison_type)`

Format comparison data into readable markdown report.

**Parameters:**
- `client_name` (str): Client name for report header
- `periods` (dict): Date ranges from `get_comparison_periods()`
- `changes` (dict): Calculated changes from `calculate_changes()`
- `comparison_type` (str): `'WoW'`, `'MoM'`, or `'YoY'`

**Returns:** Formatted markdown string with:
- Period dates
- Safeguard flags (if any)
- Metrics table (absolute + percentage changes)
- Quick insights based on significant changes

**Example:**
```python
report = format_comparison_report('Smythson', periods, changes, 'WoW')
print(report)
```

**Output:**
```markdown
## Smythson - Week over Week Comparison

**Current Period**: 2025-12-09 to 2025-12-15
**Previous Period**: 2025-12-02 to 2025-12-08

**⚠️ Flags:**
- Low volume: Comparisons may be volatile (<10 conversions)

| Metric | Current | Previous | Change | % Change |
|--------|---------|----------|--------|----------|
| Spend | £520.00 | £500.00 | +£20.00 | +4.0% |
| Revenue | £2080.00 | £2250.00 | -£170.00 | -7.6% |
| ROAS | 4.0x | 4.5x | -0.5x | -11.1% |
| Conversions | 12 | 15 | -3 | -20.0% |
| CPA | £43.33 | £33.33 | +£10.00 | +30.0% |

### Quick Insights

- ⚠️ ROAS declined 11.1% - investigate cause
- ⚠️ CPA increased 30.0% - optimise bidding or targeting
- ⚠️ Conversions declined 20.0% - review campaign performance
```

---

### `get_holiday_flags(start_date, end_date)`

Check if date range includes major UK holidays that may affect comparisons.

**Parameters:**
- `start_date` (str): Start date in `'YYYY-MM-DD'` format
- `end_date` (str): End date in `'YYYY-MM-DD'` format

**Returns:** List of holiday flags found in date range

**UK Holidays Detected:**
- `BLACK_FRIDAY` (last Friday of November)
- `CYBER_MONDAY` (Monday after Black Friday)
- `CHRISTMAS` (Dec 24-26)
- `NEW_YEAR` (Dec 31 - Jan 2)
- `EASTER_PERIOD` (early April)
- `MAY_BANK_HOLIDAY` (May Mondays)
- `AUGUST_BANK_HOLIDAY` (last Monday of August)

**Example:**
```python
flags = get_holiday_flags('2025-11-28', '2025-12-01')
# Returns: ['BLACK_FRIDAY', 'CYBER_MONDAY']

if flags:
    print(f"⚠️ Holiday period detected: {', '.join(flags)}")
    print("Comparisons may be affected by seasonal shopping patterns")
```

---

## 🟢 **Integration with Weekly Reports**

The time comparison system is integrated into the `google-ads-weekly-report` skill. Here's how it's used:

### Step-by-Step Integration

**1. Calculate date ranges:**
```python
from time_comparisons import get_comparison_periods
periods = get_comparison_periods('WoW')
```

**2. Query Google Ads for both periods:**
```python
# Current period
current_query = f"""
    SELECT metrics.cost_micros, metrics.conversions, metrics.conversions_value
    FROM customer
    WHERE segments.date >= '{periods['current']['start']}'
      AND segments.date <= '{periods['current']['end']}'
"""
current_result = mcp__google_ads__run_gaql(customer_id, manager_id, current_query)

# Previous period (same query, different dates)
previous_query = current_query.replace(
    periods['current']['start'], periods['previous']['start']
).replace(
    periods['current']['end'], periods['previous']['end']
)
previous_result = mcp__google_ads__run_gaql(customer_id, manager_id, previous_query)
```

**3. Parse, calculate, and format:**
```python
from time_comparisons import parse_performance_data, calculate_changes, format_comparison_report

current_metrics = parse_performance_data(current_result)
previous_metrics = parse_performance_data(previous_result)
changes = calculate_changes(current_metrics, previous_metrics)
comparison_section = format_comparison_report(client_name, periods, changes, 'WoW')
```

**4. Insert into report:**
```markdown
# Google Ads Weekly Report: {client_name}

---

{comparison_section}

---

## Executive Summary
...
```

---

## 🟢 **Best Practices**

### Do's ✅

1. **Always use same-day alignment** - Use `get_comparison_periods()` instead of manually calculating dates
2. **Query customer-level for totals** - Use `FROM customer` for account-level spend/revenue (never campaign-level aggregates)
3. **Include safeguard flags** - Always show flags in reports (LOW_VOLUME, LARGE_ROAS_CHANGE, etc.)
4. **Check for holidays** - Use `get_holiday_flags()` to detect seasonal periods
5. **Show both metrics** - Present absolute (£10) AND percentage (25%) changes
6. **Use British English** - optimise, analyse, realise (not optimize, analyze, realize)

### Don'ts ❌

1. **Don't compare different days** - Never compare Monday to Friday (use WoW alignment)
2. **Don't use campaign-level queries for totals** - Use customer-level (campaign queries can miss data)
3. **Don't ignore low volume** - Flag comparisons with <10 conversions (volatile data)
4. **Don't skip holiday checks** - Black Friday ≠ normal week (flag seasonal periods)
5. **Don't calculate dates manually** - Use the helper functions (they handle edge cases)

---

## 🟢 **Common Use Cases**

### Use Case 1: Weekly Report Automation

```python
# In automated weekly report agent
from time_comparisons import get_comparison_periods, parse_performance_data, calculate_changes, format_comparison_report

# Get WoW periods
periods = get_comparison_periods('WoW')

# Query and compare
current_metrics = parse_performance_data(query_google_ads(periods['current']))
previous_metrics = parse_performance_data(query_google_ads(periods['previous']))
changes = calculate_changes(current_metrics, previous_metrics)

# Generate report section
report_section = format_comparison_report(client_name, periods, changes, 'WoW')

# Insert into weekly report
weekly_report = f"""
# Weekly Report: {client_name}

{report_section}

[rest of report...]
"""
```

### Use Case 2: Monthly Strategy Review

```python
# For monthly client meetings
periods = get_comparison_periods('MoM')

# Get full month performance
current_metrics = parse_performance_data(query_google_ads(periods['current']))
previous_metrics = parse_performance_data(query_google_ads(periods['previous']))
changes = calculate_changes(current_metrics, previous_metrics)

# Check for large changes requiring discussion
if 'LARGE_ROAS_CHANGE' in changes['flags']:
    print(f"⚠️ Major ROAS shift: {changes['roas']['percentage']:.1f}%")
    print("Requires strategy discussion in monthly meeting")
```

### Use Case 3: Year-End Performance Review

```python
# For annual client review
periods = get_comparison_periods('YoY')

# Compare same period last year
current_metrics = parse_performance_data(query_google_ads(periods['current']))
previous_metrics = parse_performance_data(query_google_ads(periods['previous']))
changes = calculate_changes(current_metrics, previous_metrics)

# True growth (accounts for seasonality)
yoy_report = format_comparison_report(client_name, periods, changes, 'YoY')
print("Year-over-year growth (seasonal adjustment):")
print(yoy_report)
```

---

## 🟢 **Testing**

A comprehensive test suite is available:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/shared
python3 test_time_comparisons.py
```

**Tests verify:**
- ✅ Date ranges calculated correctly (Mon-Sun alignment for WoW)
- ✅ Safeguard flags trigger appropriately
- ✅ Edge cases handled (zero values, low volume)
- ✅ Holiday detection works
- ✅ Report formatting produces valid markdown
- ✅ British English spelling used throughout

**Expected output:**
```
🎉 ALL TESTS PASSED! Time comparison system ready for production.
```

---

## 🟢 **Troubleshooting**

### Issue: "Dates don't align to Monday-Sunday"

**Cause:** Manually calculating dates instead of using `get_comparison_periods()`

**Fix:**
```python
# ❌ Wrong
current_start = '2025-12-15'  # Could be any day
current_end = '2025-12-21'

# ✅ Correct
periods = get_comparison_periods('WoW')  # Always Mon-Sun
```

### Issue: "Percentage change shows 100% when previous was zero"

**Cause:** Dividing by zero in previous period

**Fix:** The system automatically handles this and adds `ZERO_PREVIOUS_[METRIC]` flag. No action needed - just acknowledge the flag in your report.

### Issue: "ROAS changes are volatile week-to-week"

**Cause:** Low conversion volume (<10 conversions)

**Fix:** The system flags this as `LOW_VOLUME`. Consider using MoM comparison for more stable trends:
```python
# Use MoM for low-volume accounts
periods = get_comparison_periods('MoM')  # Smooths out weekly volatility
```

### Issue: "Black Friday week shows massive changes"

**Cause:** Seasonal shopping patterns (normal)

**Fix:** Check holiday flags and add context to report:
```python
holiday_flags = get_holiday_flags(periods['current']['start'], periods['current']['end'])
if 'BLACK_FRIDAY' in holiday_flags:
    print("Note: Black Friday period - expect higher volume than typical week")
```

---

## 🟢 **File Locations**

| File | Purpose |
|------|---------|
| `shared/time_comparisons.py` | Core module with all functions |
| `shared/test_time_comparisons.py` | Comprehensive test suite |
| `shared/TIME_COMPARISONS_README.md` | This documentation file |
| `.claude/skills/google-ads-weekly-report/skill.md` | Integration example (weekly reports) |

---

## 🟢 **Changelog**

### Version 1.0 (2025-12-16)
- ✅ Initial release
- ✅ WoW, MoM, YoY comparison support
- ✅ Same-day alignment (Monday-to-Monday)
- ✅ Safeguard flags (LOW_VOLUME, LARGE_ROAS_CHANGE, etc.)
- ✅ Holiday detection (UK holidays)
- ✅ British English throughout
- ✅ Comprehensive test suite (5/5 tests passing)
- ✅ Integration with google-ads-weekly-report skill

---

## 🟢 **Credits**

Based on automated reporting principles from **Mike Rhodes' 8020brain.com**:
- Same day > same date (day-of-week patterns matter)
- Both absolute + percentage changes
- Safeguards for low volume, holidays, and campaign changes
- Phase 1: Automated Reporting (this system implements core comparison logic)

---

## 🟢 **Support**

For questions or issues with the time comparison system:

1. **Run the test suite** - `python3 test_time_comparisons.py`
2. **Check this documentation** - Common use cases and troubleshooting above
3. **Review the code** - `time_comparisons.py` has extensive docstrings
4. **Check integration example** - `.claude/skills/google-ads-weekly-report/skill.md`

---

**Last Updated:** 2025-12-16
**Status:** ✅ Production Ready
**Tests:** 5/5 Passing
