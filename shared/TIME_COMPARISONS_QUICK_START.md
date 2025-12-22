# Time Comparisons - Quick Start Guide

**Status:** ✅ Implemented and tested (2025-12-16)
**Test Results:** 5/5 tests passing

---

## 🟢 **What You Just Got**

A complete automated time comparison system that:
- ✅ Calculates WoW, MoM, YoY date ranges with same-day alignment
- ✅ Parses Google Ads API results automatically
- ✅ Calculates absolute + percentage changes
- ✅ Adds safeguard flags (LOW_VOLUME, LARGE_ROAS_CHANGE, etc.)
- ✅ Detects UK holidays (Black Friday, Christmas, etc.)
- ✅ Generates formatted markdown reports
- ✅ Integrated into your google-ads-weekly-report skill

---

## 🟢 **Files Created**

| File | Purpose | Status |
|------|---------|--------|
| `shared/time_comparisons.py` | Core module (540 lines) | ✅ Ready |
| `shared/test_time_comparisons.py` | Test suite (420 lines) | ✅ Passing |
| `shared/TIME_COMPARISONS_README.md` | Full documentation | ✅ Complete |
| `.claude/skills/google-ads-weekly-report/skill.md` | Updated skill | ✅ Integrated |

---

## 🟢 **How To Use It Now**

### Option 1: Generate a Weekly Report (Automatic Integration)

The time comparison system is already integrated into your weekly report skill:

```bash
# In Claude Code, invoke the skill:
Skill(command='google-ads-weekly-report')

# Then provide client name when prompted
# The report will automatically include:
# - Week over Week comparison section
# - Safeguard flags
# - Quick insights based on changes
```

### Option 2: Use Directly in Python

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/shared')))
from time_comparisons import get_comparison_periods, parse_performance_data, calculate_changes, format_comparison_report

# Get WoW periods (automatically aligned to Mon-Sun)
periods = get_comparison_periods('WoW')
print(f"Current: {periods['current']}")
print(f"Previous: {periods['previous']}")

# Query Google Ads and compare
current_result = mcp__google_ads__run_gaql(customer_id, manager_id, query_current)
previous_result = mcp__google_ads__run_gaql(customer_id, manager_id, query_previous)

current_metrics = parse_performance_data(current_result)
previous_metrics = parse_performance_data(previous_result)

changes = calculate_changes(current_metrics, previous_metrics)

# Generate formatted report section
report = format_comparison_report('Client Name', periods, changes, 'WoW')
print(report)
```

---

## 🟢 **Test It With A Real Client**

Let's test with Smythson:

```python
# 1. Get comparison periods
from time_comparisons import get_comparison_periods
periods = get_comparison_periods('WoW')

# 2. Query Smythson's Google Ads account
customer_id = '8573235780'
manager_id = '2569949686'

current_query = f"""
    SELECT
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM customer
    WHERE
        segments.date >= '{periods['current']['start']}'
        AND segments.date <= '{periods['current']['end']}'
"""

current_result = mcp__google_ads__run_gaql(
    customer_id=customer_id,
    manager_id=manager_id,
    query=current_query
)

# 3. Parse and display
from time_comparisons import parse_performance_data
current_metrics = parse_performance_data(current_result)

print("\nSmythson Current Week Performance:")
print(f"  Spend: £{current_metrics['spend']:,.2f}")
print(f"  Revenue: £{current_metrics['revenue']:,.2f}")
print(f"  ROAS: {current_metrics['roas']:.1f}x")
print(f"  Conversions: {current_metrics['conversions']:.0f}")
print(f"  CPA: £{current_metrics['cpa']:.2f}")
```

**Want to run this test now?** Just say "test time comparisons with Smythson" and I'll execute it.

---

## 🟢 **Next Steps**

### This Week
1. ✅ System is ready - use it in your next weekly report
2. ✅ All functions tested and documented
3. ✅ Integrated into google-ads-weekly-report skill

### Next Week
1. Generate weekly reports for 3-5 clients using the skill
2. Review the comparison sections in the reports
3. Note any insights the safeguard flags surface

### Next Month
1. Add MoM comparisons to monthly client review meetings
2. Use YoY comparisons for year-end reviews
3. Consider automating comparison-based task creation (e.g., create task if ROAS drops >20% WoW)

---

## 🟢 **Key Features You Should Know About**

### Safeguard Flags Protect You From Bad Decisions

The system automatically detects:
- **LOW_VOLUME**: <10 conversions (comparisons unreliable)
- **LARGE_ROAS_CHANGE**: >20% ROAS shift (investigate cause)
- **LARGE_SPEND_CHANGE**: >50% spend shift (budget change? paused campaign?)
- **ZERO_PREVIOUS_[METRIC]**: Can't calculate % change from zero

### Holiday Detection Adds Context

Automatically flags UK holidays in your date range:
- Black Friday, Cyber Monday
- Christmas, New Year
- Easter, Bank Holidays

### Same-Day Alignment Prevents False Signals

Always compares Monday-to-Monday (or 1st-to-1st for MoM):
- ✅ Monday Dec 9 vs Monday Dec 2
- ❌ Monday Dec 9 vs Sunday Dec 8 (wrong!)

### British English Throughout

Uses "optimise", "analyse", "realise" (not US spellings)

---

## 🟢 **Common Questions**

**Q: Do I need to update my existing weekly report skill?**
A: No - it's already updated and ready to use!

**Q: Can I use this for monthly reports?**
A: Yes! Just use `get_comparison_periods('MoM')` instead of `'WoW'`

**Q: What if I want to compare specific custom date ranges?**
A: You can pass a `reference_date` parameter to `get_comparison_periods()`:
```python
from datetime import datetime
custom_date = datetime(2025, 11, 15)  # Mid-November
periods = get_comparison_periods('WoW', reference_date=custom_date)
```

**Q: Does this work for multi-account clients like Smythson?**
A: Yes! Query each account separately and sum the metrics before comparing:
```python
# Query UK, USA, EUR, ROW accounts
uk_metrics = parse_performance_data(query_uk_account())
usa_metrics = parse_performance_data(query_usa_account())

# Sum totals
total_metrics = {
    'spend': uk_metrics['spend'] + usa_metrics['spend'],
    'revenue': uk_metrics['revenue'] + usa_metrics['revenue'],
    # ... etc
}

changes = calculate_changes(total_current, total_previous)
```

---

## 🟢 **Pro Tips**

1. **Always check flags first** - They tell you if the comparison is reliable
2. **Use MoM for strategy** - WoW is noisy, MoM smooths out volatility
3. **Use YoY for growth** - Only YoY accounts for seasonality
4. **Show both metrics** - Absolute (£10) AND percentage (25%) tell different stories
5. **Flag holidays** - Black Friday ≠ normal week (use holiday detection)

---

## 🟢 **Example Output**

Here's what a generated comparison report looks like:

```markdown
## Smythson - Week over Week Comparison

**Current Period**: 2025-12-09 to 2025-12-15
**Previous Period**: 2025-12-02 to 2025-12-08

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

**Ready to use!** Just invoke the `google-ads-weekly-report` skill and it will automatically include time comparisons.

**Questions?** Check `shared/TIME_COMPARISONS_README.md` for full documentation.
