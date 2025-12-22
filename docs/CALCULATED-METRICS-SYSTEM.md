# Calculated Metrics System

**Status**: Implemented (2025-12-14)
**Phase**: Ads to AI Phase 1 - Automated Reporting

---

## Overview

The Calculated Metrics system provides **bulletproof metric calculation** for Google Ads automation. It ensures that weekly reports, analysis tools, and AI prompts never break due to division-by-zero errors, incorrect aggregation, or missing context.

**Core Principle**: Raw data (impressions, clicks, cost, conversions, conversion value) becomes **useful information** (CTR, CPA, ROAS, conversion rate) through **safe, contextual calculation**.

---

## The Four Critical Rules

### 1. Handle Division by Zero

**Problem**: Raw calculations crash when denominators are zero.

```python
# ❌ WRONG - Will crash automation
roas = conversions_value / cost  # What if cost = 0?
cpa = cost / conversions  # What if conversions = 0?
```

**Solution**: Return `None` for undefined metrics, display as "N/A"

```python
# ✅ CORRECT - Safe calculation
from shared.calculated_metrics import calculate_roas, format_metric

roas = calculate_roas(conversions_value=5400, cost=1200)  # 4.5
display = format_metric(roas, 'roas')  # "4.50x"

# Zero handling
roas_zero = calculate_roas(0, 0)  # None
display_zero = format_metric(roas_zero, 'roas')  # "N/A"
```

### 2. Build in Context

**Problem**: "£50 CPA" means nothing without comparison.

**Solution**: Always show target, previous period, and account average.

```python
from shared.calculated_metrics import add_context, format_metric_with_context

# Add context to metric
roas_with_context = add_context(
    current_metric=3.8,
    target=4.0,           # From CONTEXT.md
    previous=4.2,         # From previous week
    account_average=4.5   # From account aggregate
)

# Display with context
print(format_metric_with_context(roas_with_context, 'roas', 'ROAS'))
# Output:
# ROAS: 3.80x
# vs Target (4.00x): ◆ -5.0%
# vs Previous: ⚠️ -9.5%
# vs Account: ⚠️ -15.6%
```

### 3. Aggregate Properly (Never Average Percentages)

**Problem**: You can't average ROAS or CPA.

```python
# ❌ WRONG
campaign_1_roas = 5.0  # £100 spend, £500 revenue
campaign_2_roas = 3.0  # £900 spend, £2,700 revenue
average_roas = (5.0 + 3.0) / 2  # 4.0 - INCORRECT

# ✅ CORRECT - Aggregate first, calculate second
from shared.calculated_metrics import aggregate_metrics

campaigns = [
    {'cost': 100, 'conversions_value': 500, 'conversions': 10},
    {'cost': 900, 'conversions_value': 2700, 'conversions': 90}
]

account_totals = aggregate_metrics(campaigns)
# Result: {
#   'total_cost': 1000,
#   'total_revenue': 3200,
#   'roas': 3.2  # CORRECT (not 4.0!)
# }
```

**Why it matters**: The £900 campaign dominates the account, so account ROAS should be closer to 3.0x, not 4.0x.

### 4. Think About Campaign vs Account Level

**Campaign-level**: Calculate ROAS for each campaign individually
**Account-level**: Sum all costs, sum all revenue, then calculate ROAS

```python
from shared.calculated_metrics import process_campaign_metrics, aggregate_metrics

# Process individual campaigns
campaigns = []
for campaign_data in gaql_results:
    metrics = process_campaign_metrics(
        raw_data=campaign_data['metrics'],
        target_roas=4.0,
        previous_data=previous_campaign_data
    )
    campaigns.append(metrics)

# Aggregate to account level (sum first, calculate second)
account_totals = aggregate_metrics(
    campaigns=campaigns,
    cost_key='cost',
    revenue_key='revenue',
    conversions_key='conversions'
)
```

---

## Module Reference

### Location

**Module**: `/Users/administrator/Documents/PetesBrain/shared/calculated_metrics.py`
**Tests**: `/Users/administrator/Documents/PetesBrain/shared/test_calculated_metrics.py`
**Example**: `/Users/administrator/Documents/PetesBrain/shared/weekly_report_example.py`

### Core Functions

#### `calculate_roas(conversions_value, cost)`
Calculate Return on Ad Spend with division-by-zero handling.

```python
roas = calculate_roas(5400, 1200)  # 4.5
roas_zero = calculate_roas(0, 0)  # None
```

#### `calculate_cpa(cost, conversions)`
Calculate Cost per Acquisition with division-by-zero handling.

```python
cpa = calculate_cpa(1200, 28)  # 42.86
cpa_zero = calculate_cpa(1200, 0)  # None
```

#### `calculate_ctr(clicks, impressions)`
Calculate Click-Through Rate as decimal.

```python
ctr = calculate_ctr(350, 10000)  # 0.035
```

#### `calculate_conversion_rate(conversions, clicks)`
Calculate Conversion Rate as decimal.

```python
conv_rate = calculate_conversion_rate(28, 350)  # 0.08
```

#### `format_metric(value, metric_type, show_na=True, decimal_places=2)`
Format metric for display with N/A handling.

```python
format_metric(4.567, 'roas')  # "4.57x"
format_metric(None, 'roas')  # "N/A"
format_metric(1234.56, 'currency')  # "£1,234.56"
format_metric(0.0345, 'percentage')  # "3.45%"
```

**Types**: `'currency'`, `'roas'`, `'percentage'`, `'decimal'`, `'integer'`

#### `calculate_variance(actual, target)`
Calculate percentage variance from target.

```python
variance = calculate_variance(3.8, 4.0)  # -5.0 (5% below target)
variance = calculate_variance(4.8, 4.0)  # +20.0 (20% above target)
```

#### `format_variance(variance, include_sign=True)`
Format variance with colour indicators.

```python
format_variance(20.5)  # "✓ +20.5%"  (significantly above)
format_variance(-15.3)  # "⚠️ -15.3%"  (significantly below)
format_variance(-5.2)  # "◆ -5.2%"   (slightly below)
```

**Indicators**:
- `✓` = +10% or more (significantly above target)
- `◆` = Between -10% and +10% (near target)
- `⚠️` = -10% or worse (significantly below target)

#### `aggregate_metrics(campaigns, cost_key, revenue_key, conversions_key)`
Aggregate campaign data to account level with proper calculation.

```python
campaigns = [
    {'cost': 1200, 'conversions_value': 5400, 'conversions': 28},
    {'cost': 800, 'conversions_value': 3200, 'conversions': 24}
]

account = aggregate_metrics(campaigns)
# Returns: {
#   'total_cost': 2000,
#   'total_revenue': 8600,
#   'total_conversions': 52,
#   'roas': 4.3,
#   'cpa': 38.46
# }
```

#### `add_context(current_metric, target, previous, account_average)`
Add context to a metric with comparisons.

```python
context = add_context(
    current_metric=3.8,
    target=4.0,
    previous=4.2,
    account_average=4.5
)

# Returns: {
#   'value': 3.8,
#   'vs_target': -5.0,
#   'vs_previous': -9.52,
#   'vs_account': -15.56
# }
```

#### `convert_micros_to_currency(micros)`
Convert Google Ads micros to £.

```python
cost = convert_micros_to_currency(1200000000)  # 1200.0
```

#### `process_campaign_metrics(raw_data, target_roas, previous_data)`
Complete workflow: convert micros, calculate metrics, add context.

```python
raw = {
    'cost_micros': 1200000000,
    'conversions_value_micros': 5400000000,
    'conversions': 28
}

previous_raw = {
    'cost_micros': 1100000000,
    'conversions_value_micros': 4400000000,
    'conversions': 25
}

result = process_campaign_metrics(raw, target_roas=4.0, previous_data=previous_raw)

# Returns: {
#   'cost': 1200.0,
#   'revenue': 5400.0,
#   'conversions': 28,
#   'roas': {
#       'value': 4.5,
#       'vs_target': 12.5,
#       'vs_previous': 12.5,
#       'vs_account': None
#   },
#   'cpa': {
#       'value': 42.86,
#       'vs_target': None,
#       'vs_previous': -3.45,
#       'vs_account': None
#   }
# }
```

---

## Integration into Weekly Reports

### Before: Manual Calculation (Fragile)

```python
# OLD APPROACH ❌
roas = conversions_value / cost  # Can crash
cpa = cost / conversions  # Can crash
wow_change = ((current - previous) / previous) * 100  # Can crash
```

### After: Calculated Metrics (Bulletproof)

```python
# NEW APPROACH ✅
from shared.calculated_metrics import process_campaign_metrics, aggregate_metrics

# Process campaign data
metrics = process_campaign_metrics(
    raw_data=gaql_result['metrics'],
    target_roas=4.0,
    previous_data=previous_gaql_result['metrics']
)

# Aggregate to account level
account = aggregate_metrics(campaigns)

# Never crashes, always has context
```

**See**: `/Users/administrator/Documents/PetesBrain/shared/weekly_report_example.py` for complete example.

---

## Testing

### Run Tests

```bash
cd /Users/administrator/Documents/PetesBrain
python3 shared/test_calculated_metrics.py
```

**Expected output**: All tests pass

### Test Coverage

✅ Division by zero handling (returns None, not error)
✅ Proper aggregation (sum-first-calculate-second)
✅ Context calculation (variance vs target/previous)
✅ Formatting (N/A for None, currency/percentage/ROAS)
✅ Micros conversion (Google Ads API data)
✅ Edge cases (very small/large numbers, mixed zeros)

### Critical Test: Never Average Percentages

```python
# Example: Never average percentages
campaigns = [
    {'cost': 100, 'conversions_value': 500},  # 5.0x ROAS
    {'cost': 900, 'conversions_value': 2700}  # 3.0x ROAS
]

# Wrong approach (averaging)
average_roas = (5.0 + 3.0) / 2  # 4.0 ❌

# Correct approach (aggregate first)
account = aggregate_metrics(campaigns)
assert account['roas'] == 3.2  # ✅

# Verify averaging would be wrong
assert account['roas'] != 4.0  # CRITICAL TEST
```

This test **must pass** to prevent strategic errors.

---

## Usage Examples

### Example 1: Weekly Report Executive Summary

```python
from shared.calculated_metrics import (
    process_campaign_metrics,
    aggregate_metrics,
    add_context,
    format_metric,
    format_variance
)

# Get current and previous week data from GAQL
current_campaigns = [...]  # From mcp__google_ads__run_gaql
previous_campaigns = [...]

# Process campaigns
processed = []
for campaign in current_campaigns:
    metrics = process_campaign_metrics(
        raw_data=campaign['metrics'],
        target_roas=target_roas,
        previous_data=find_previous_campaign(campaign['name'])
    )
    processed.append(metrics)

# Aggregate to account level
account = aggregate_metrics(processed)

# Display with context
print(f"Account ROAS: {format_metric(account['roas'], 'roas')}")
print(f"vs Target ({target_roas}x): {format_variance(variance)}")
```

### Example 2: Campaign Performance Table

```python
# Generate markdown table with context
for campaign in processed_campaigns:
    roas = format_metric(campaign['roas']['value'], 'roas')
    vs_target = format_variance(campaign['roas']['vs_target'])
    vs_previous = format_variance(campaign['roas']['vs_previous'])

    print(f"| {campaign['name']} | {roas} | {vs_target} | {vs_previous} |")
```

### Example 3: Task Creation Thresholds

```python
from shared.calculated_metrics import calculate_variance

# Check if ROAS drop meets threshold for task creation
roas_variance = calculate_variance(current_roas, previous_roas)

if roas_variance < -20:  # More than 20% drop
    # Create P0 task - significant performance decline
    create_task(
        title=f"[{client}] Investigate ROAS drop ({roas_variance:.0f}%)",
        priority='P0'
    )
```

---

## Connection to AI Automation Journey

### Phase 1: Automated Reporting (Current)

**Before Calculated Metrics**:
- Reports could crash (division by zero)
- Numbers lacked meaning (no context)
- Account totals were wrong (averaged ROAS)
- **Could not trust automation**

**After Calculated Metrics**:
- Reports always work (graceful error handling)
- Numbers have meaning (context included)
- Account totals are accurate (proper aggregation)
- **Can now trust automation completely**

### Phase 2: AI Analysis (Next Step)

Once calculated metrics are bulletproof, you can:

```python
# Feed reliable, contextualized data to AI
analysis = claude.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{
        "role": "user",
        "content": f"""Analyze this Google Ads performance:

Account ROAS: 4.2x (Target: 4.0x, +5% vs target)
Week-over-week: +8% improvement

Performance Max: 4.8x ROAS (+20% vs target, +12% WoW)
Shopping: 3.3x ROAS (-18% vs target, -12% WoW)

What should I do?"""
    }]
)
```

The AI can provide strategic recommendations **because the data is reliable and has context**.

### Phase 3: Automated Insights (Future)

Schedule AI analysis to run automatically every Monday:

```python
# LaunchAgent runs weekly report with AI analysis
# calculated_metrics ensures data is always correct
# AI generates recommendations
# Tasks created automatically for P0 issues
```

---

## Best Practices

### ✅ DO

- **Always use calculated_metrics** for any ROAS, CPA, CTR, conversion rate calculation
- **Always include context** (vs target, vs previous, vs account average)
- **Always aggregate first** when calculating account-level metrics
- **Always handle None** gracefully in display logic
- **Always test edge cases** (zero conversions, zero cost, etc.)

### ❌ DON'T

- **Never calculate ROAS** with raw division (`value / cost`)
- **Never average ROAS** across campaigns
- **Never assume** conversions or cost are non-zero
- **Never show** division-by-zero errors to users (use N/A)
- **Never calculate** account metrics from campaign averages

---

## Troubleshooting

### "All metrics show N/A"

**Cause**: Division by zero (likely no conversions or zero cost)
**Solution**: This is correct behaviour - campaigns with zero data show N/A

### "Account ROAS doesn't match campaign average"

**Cause**: You're averaging ROAS instead of aggregating
**Solution**: Use `aggregate_metrics()` - it sums totals first, then calculates

### "Variance shows ± when it should be 0%"

**Cause**: Floating point precision (19.999999 vs 20.0)
**Solution**: Tests use approximate equality (`abs(x - y) < 0.01`)

### "Context is None even though I provided target"

**Cause**: Target is 0 or None
**Solution**: Check CONTEXT.md has valid target_roas value

---

## Migration Guide

### For Existing Weekly Reports

1. **Import the module**:
   ```python
   from shared.calculated_metrics import process_campaign_metrics, aggregate_metrics
   ```

2. **Replace manual calculations**:
   ```python
   # OLD ❌
   roas = conversions_value / cost

   # NEW ✅
   metrics = process_campaign_metrics(raw_data, target_roas=4.0)
   roas = metrics['roas']['value']
   ```

3. **Add context to displays**:
   ```python
   # OLD ❌
   print(f"ROAS: {roas:.2f}x")

   # NEW ✅
   print(format_metric_with_context(metrics['roas'], 'roas', 'ROAS'))
   ```

4. **Fix account aggregation**:
   ```python
   # OLD ❌
   avg_roas = sum(campaign_roas) / len(campaigns)

   # NEW ✅
   account = aggregate_metrics(campaigns)
   account_roas = account['roas']
   ```

### For New Reports

Use the complete workflow from `weekly_report_example.py`:

```python
from shared.weekly_report_example import process_weekly_report_data

report_data = process_weekly_report_data(
    current_data=gaql_current,
    previous_data=gaql_previous,
    target_roas=4.0
)
```

---

## Related Documentation

- **Ads to AI Skill Map**: Phase 1 - Automated Reporting
- **Weekly Report Skill**: `.claude/skills/google-ads-weekly-report/skill.md`
- **Data Verification Protocol**: `docs/DATA-VERIFICATION-PROTOCOL.md`
- **Task System**: `docs/TASK-SYSTEM-DECISION-GUIDE.md`

---

## Version History

- **2025-12-14**: Initial implementation of calculated metrics system
- **Status**: Production-ready, all tests passing
- **Next**: Integrate into all weekly report workflows

---

**For questions or issues**: This system is foundational to Phase 1 automation. If metrics don't calculate correctly, reports will be unreliable and AI analysis (Phase 2) will give wrong recommendations.
