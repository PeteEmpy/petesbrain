# Conversion Lag Detection System

**Status:** ✅ Implemented December 16, 2025
**Component:** InsightEngine (`shared/insight_rules.py`)
**Purpose:** Prevent false insights from incomplete Google Ads data

---

## 🎯 The Problem

**Conversion lag** means conversions can be attributed to clicks that happened 30-90 days ago. This creates a critical data accuracy issue:

### Example: False ROAS Drop

```
Scenario:
- Compare Dec 8-14 (ended 7 days ago) to Dec 15-16 (ended 1 day ago)
- Dec 8-14: 95% of conversions attributed (reliable)
- Dec 15-16: Only 40% of conversions attributed (very incomplete)

If you project Dec 15-16 by multiplying by 3.5x:
- CVR appears to drop 29% → FALSE SIGNAL
- ROAS appears to drop 36% → FALSE SIGNAL

Result: You waste time investigating phantom issues that don't exist.
```

---

## ✅ The Solution

The `InsightEngine` now automatically detects data freshness and:

1. **Blocks insights** if data is <50% complete (too unreliable)
2. **Generates with caveats** if data is 50-90% complete (usable but incomplete)
3. **Generates normally** if data is >90% complete (reliable)

---

## 📊 Data Quality Standards

| Days Since Period End | Completeness | Quality Level | Action |
|----------------------|--------------|---------------|--------|
| 0 (today) | 30% | Incomplete | **BLOCK** insights |
| 1 day | 40% | Incomplete | **BLOCK** insights |
| 2 days | 48% | Incomplete | **BLOCK** insights |
| 3 days | 80% | Partial | Generate with **caveats** + downgrade P0→P1, P1→P2 |
| 4 days | 85% | Partial | Generate with **caveats** + downgrade P0→P1, P1→P2 |
| 5 days | 88% | Partial | Generate with **caveats** + downgrade P0→P1, P1→P2 |
| 6 days | 90% | Partial | Generate with **caveats** + downgrade P0→P1, P1→P2 |
| 7+ days | 95%+ | Complete | **Normal** insights (no caveats) |
| 30+ days | 99% | Complete | **Normal** insights (near 100% attribution) |

---

## 🔧 Implementation

### Code Changes

**File:** `shared/insight_rules.py`

#### New Method: `_check_data_quality()`

```python
def _check_data_quality(
    self,
    period_end_date: Optional[str],
    period_days: int
) -> Dict[str, Any]:
    """
    Calculate data quality based on conversion lag.

    Returns:
        - days_since_end: int
        - completeness: float (0-100)
        - recommended_wait_until: str (YYYY-MM-DD)
        - quality_level: 'incomplete' | 'partial' | 'complete'
    """
```

#### Enhanced Method: `generate_insights()`

```python
def generate_insights(
    self,
    current_metrics: Dict[str, float],
    previous_metrics: Dict[str, float],
    target_roas: Optional[float] = None,
    current_period_end_date: Optional[str] = None,  # NEW
    current_period_days: int = 7  # NEW
) -> List[Dict[str, Any]]:
```

**Key behaviours:**
1. Calls `_check_data_quality()` first
2. Returns data quality warning if completeness <50%
3. Adds data quality metadata to all insights
4. Downgrades priorities if completeness <90%
5. Adds caveats explaining data incompleteness

---

## 📖 Usage Examples

### Example 1: Data Too Fresh (Blocked)

```python
from insight_rules import InsightEngine
from datetime import date

engine = InsightEngine()

# Period ended yesterday (1 day ago)
yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

insights = engine.generate_insights(
    current_metrics={'spend': 2450, 'revenue': 8820, 'roas': 360, ...},
    previous_metrics={'spend': 2100, 'revenue': 8820, 'roas': 420, ...},
    target_roas=400,
    current_period_end_date=yesterday,  # CRITICAL: Pass end date
    current_period_days=7
)

# Result: insights[0]['type'] == 'data_quality_warning'
# Message: "Data too recent for reliable insights (40% complete)"
```

### Example 2: Data Partial (Caveats Added)

```python
# Period ended 4 days ago
four_days_ago = (date.today() - timedelta(days=4)).strftime('%Y-%m-%d')

insights = engine.generate_insights(
    current_metrics=...,
    previous_metrics=...,
    target_roas=400,
    current_period_end_date=four_days_ago,
    current_period_days=7
)

# Result: Normal insights but with:
# - insights[0]['data_quality']['completeness'] = 85
# - insights[0]['priority'] = 'P2' (downgraded from P1)
# - insights[0]['priority_note'] = "Downgraded from P1 due to incomplete data"
# - insights[0]['caveat'] = "⚠️ Based on 85% complete data..."
```

### Example 3: Data Complete (Normal Insights)

```python
# Period ended 7+ days ago
week_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')

insights = engine.generate_insights(
    current_metrics=...,
    previous_metrics=...,
    target_roas=400,
    current_period_end_date=week_ago,
    current_period_days=7
)

# Result: Normal insights with:
# - insights[0]['data_quality']['completeness'] = 95
# - insights[0]['priority'] = 'P1' (no downgrade)
# - No caveats (data is reliable)
```

### Example 4: Backwards Compatibility (No End Date)

```python
# Old code that doesn't pass period_end_date still works
insights = engine.generate_insights(
    current_metrics=...,
    previous_metrics=...,
    target_roas=400
    # No period_end_date - assumes data is complete
)

# Result: Normal insights (100% completeness assumed for backwards compatibility)
```

---

## 🧪 Testing

**Test file:** `shared/test_insight_rules_conversion_lag.py`

Comprehensive test covering 5 scenarios:
1. ✅ Period ended today (0 days) → Blocked (30% complete)
2. ✅ Period ended 2 days ago → Blocked (48% complete)
3. ✅ Period ended 4 days ago → Generated with caveats (85% complete)
4. ✅ Period ended 7 days ago → Normal insights (95% complete)
5. ✅ No period_end_date → Backwards compatible (100% complete)

**Run tests:**
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/shared
python3 test_insight_rules_conversion_lag.py
```

---

## 📚 Documentation

Updated documentation files:

1. **`docs/INSIGHT-FRAMEWORK-QUICK-START.md`**
   - Added "CRITICAL FEATURE: Conversion Lag Detection" section
   - Explains data quality standards
   - Shows example protection warning

2. **`docs/INSIGHT-FRAMEWORK-DEMO.md`**
   - Added "🛡️ Conversion Lag Protection" section
   - Shows before/after examples
   - Demonstrates all three data quality levels (blocked, partial, complete)

3. **`docs/CONVERSION-LAG-DETECTION.md`** (this file)
   - Technical implementation details
   - Usage examples
   - Testing procedures

---

## 🔄 Integration with Weekly Reports

**To use conversion lag detection in weekly reports:**

```python
from datetime import datetime, timedelta

# Calculate period dates
current_period_start = datetime(2025, 12, 9).date()
current_period_end = datetime(2025, 12, 15).date()
previous_period_start = datetime(2025, 12, 2).date()
previous_period_end = datetime(2025, 12, 8).date()

# Query Google Ads for both periods
current_metrics = get_google_ads_data(current_period_start, current_period_end)
previous_metrics = get_google_ads_data(previous_period_start, previous_period_end)

# Generate insights WITH conversion lag detection
insights = engine.generate_insights(
    current_metrics,
    previous_metrics,
    target_roas=target_roas,
    current_period_end_date=current_period_end.strftime('%Y-%m-%d'),  # PASS THIS
    current_period_days=(current_period_end - current_period_start).days + 1
)

# Check if data is too fresh
if insights and insights[0]['type'] == 'data_quality_warning':
    # Display warning to user
    print(f"⚠️ Data only {insights[0]['data_quality']['completeness']:.0f}% complete")
    print(f"Wait until {insights[0]['data_quality']['recommended_wait_until']}")
else:
    # Display normal insights
    for insight in insights:
        print(f"{insight['title']}")
        if 'caveat' in insight:
            print(f"⚠️ {insight['caveat']}")
```

---

## 🎓 Industry Best Practices

**Why 7 days?**

Industry research shows:
- **0-2 days**: Most conversions haven't been attributed yet
- **3-6 days**: Majority of conversions attributed but still incomplete
- **7+ days**: 95%+ of conversions attributed (reliable for analysis)
- **30+ days**: Nearly 100% attribution complete

**Conservative approach:** We recommend waiting 7 days after period end for reliable insights. For urgent analysis, 3-6 days is acceptable with clear caveats.

---

## 🔮 Future Enhancements

**Potential improvements:**

1. **Client-specific lag profiles** - Different conversion windows by industry
2. **Campaign-type specific thresholds** - Brand campaigns convert faster than generic
3. **Attribution window detection** - Adjust completeness based on actual attribution window
4. **Historical lag analysis** - Learn actual lag patterns from past data

---

## ✅ Validation Checklist

Before using conversion lag detection in production:

- [✅] InsightEngine correctly blocks insights when completeness <50%
- [✅] InsightEngine adds caveats when completeness 50-90%
- [✅] InsightEngine generates normally when completeness >90%
- [✅] Priority downgrading works (P0→P1, P1→P2)
- [✅] Backwards compatibility maintained (works without period_end_date)
- [✅] Test suite passes all 5 scenarios
- [✅] Documentation updated (Quick Start, Demo, Technical)
- [ ] Weekly report skill updated to pass period_end_date
- [ ] Production testing with real client data

---

## 🚨 Critical Usage Note

**ALWAYS pass `current_period_end_date` when calling `generate_insights()` to enable conversion lag detection.**

Without it, the system assumes data is 100% complete (backwards compatibility mode), and conversion lag protection is disabled.

**Good:**
```python
insights = engine.generate_insights(
    current_metrics, previous_metrics,
    target_roas=400,
    current_period_end_date='2025-12-15',  # ✅ ENABLES PROTECTION
    current_period_days=7
)
```

**Bad (no protection):**
```python
insights = engine.generate_insights(
    current_metrics, previous_metrics,
    target_roas=400
    # ❌ NO PROTECTION - assumes data is complete
)
```

---

**Implemented by:** Claude Code
**Date:** December 16, 2025
**Tested:** ✅ All 5 scenarios pass
**Production Ready:** ⚠️ Pending weekly report skill integration
