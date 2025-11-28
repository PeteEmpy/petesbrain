# Date Range Standard Implementation Plan

**Status:** In Progress
**Started:** 20 November 2025
**Priority:** CRITICAL - Affects data quality across all reporting

## Problem Statement

Google Ads and GA4 have 24-48 hour data processing lag. Including today/yesterday in reports produces **incomplete data and misleading analysis**, leading to poor strategic decisions.

**Real Impact:** Incomplete conversion data has caused us to:
- Pause winning campaigns that appeared to be underperforming
- Miss scaling opportunities
- Produce inaccurate client reports

## Solution

**Mandatory Standard:** All date ranges must exclude today and yesterday (2-day lag buffer).

- **7-day reports:** Days -9 to -3 (7 complete days)
- **Weekly reports:** Last complete Mon-Sun week (ending 2+ days ago)
- **Monthly reports:** Previous complete month only

## Implementation Status

### ✅ Completed

1. **CLAUDE.md Updated** (2025-11-20)
   - Added "Date Range Standards (MANDATORY - CRITICAL)" section
   - Includes Python examples, GAQL patterns, and validation rules
   - Location: Lines 159-247

2. **Shared Utility Created** (2025-11-20)
   - File: `shared/date_utils.py`
   - Functions:
     - `get_complete_date_range()` - 7/30/custom day ranges
     - `get_complete_week_range()` - Mon-Sun weeks
     - `get_complete_month_range()` - Full calendar months
     - `get_comparison_periods()` - WoW/MoM comparisons
     - `format_gaql_date_range()` - GAQL query formatter
     - `validate_date_range()` - Enforce lag buffer
   - Quick access: `get_last_7_complete_days()`, `get_last_complete_week()`, etc.

### 🔄 In Progress

3. **Agent Inventory** - Identifying all agents that need updates

### ⏳ Pending

4. **Agent Code Updates** - Implement date_utils in all reporting agents
5. **Agent Documentation Updates** - Update agent.md files with date range standards
6. **Skills Updates** - Update reporting skills to use date_utils
7. **Testing** - Verify all agents produce correct date ranges

## Agents Requiring Code Updates

### High Priority (Performance/Reporting Agents)

**These directly affect client reports and strategic decisions:**

1. **daily-intel-report.py** - Daily briefing with Google Ads/Analytics data
2. **weekly-client-strategy-generator.py** - Weekly client performance reports
3. **weekly-experiment-review.py** - A/B test and experiment analysis
4. **campaign-audit-agent.py** - Campaign performance audits
5. **google-ads-auditor.py** - Google Ads account audits
6. **datastory-report.py** - DataStory report generation
7. **weekly-meeting-review.py** - Meeting summaries with performance data

### Medium Priority (Monitoring Agents)

**These track changes but don't directly generate client-facing reports:**

8. **daily-anomaly-detector.py** - Performance anomaly detection
9. **trend-monitor.py** - Trend monitoring
10. **baseline-calculator.py** - Performance baseline calculation
11. **fetch-weekly-performance.py** - Weekly performance data fetcher
12. **daily-budget-monitor.py** - Budget monitoring
13. **devonshire-budget-tracker.py** - Devonshire-specific budget tracking

### Low Priority (Supporting Agents)

**These use dates but not for performance reporting:**

14. **file-organizer.py** - File organization by date
15. **knowledge-base-processor.py** - KB document processing
16. **kb-weekly-summary.py** - KB weekly summary
17. **weekly-blog-generator.py** - Blog post generation
18. **tasks-monitor.py** - Task monitoring
19. **nda-enrolments-tracker.py** - Enrolment tracking

### No Changes Needed

**These agents don't query performance data:**

- News monitors (facebook, shopify, industry, ai) - Monitor RSS feeds, no lag
- Specs monitors/processors - Monitor documentation changes
- Chat/inbox processors - Process incoming messages
- Content sync agents - Sync content, not performance data
- System agents - Infrastructure monitoring

## Implementation Checklist

### For Each Agent

- [ ] Review current date logic
- [ ] Replace with `shared.date_utils` functions
- [ ] Add lag buffer validation
- [ ] Update agent.md documentation
- [ ] Test date ranges produced
- [ ] Verify GAQL queries use correct format

### Standard Replacement Pattern

**Before:**
```python
from datetime import datetime, timedelta
end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)
```

**After:**
```python
from shared.date_utils import get_last_7_complete_days
start_date, end_date = get_last_7_complete_days()
```

**GAQL Before:**
```python
query = "SELECT ... WHERE segments.date DURING LAST_7_DAYS"
```

**GAQL After:**
```python
from shared.date_utils import get_last_7_complete_days, format_gaql_date_range
start, end = get_last_7_complete_days()
query = f"SELECT ... WHERE {format_gaql_date_range(start, end)}"
```

## Testing Protocol

For each updated agent:

1. **Dry Run:** Execute agent with logging to see date ranges
2. **Verify:** Confirm end_date is at least 2 days before today
3. **Compare:** Check before/after data to confirm lag impact
4. **Document:** Note any significant data differences found

## Expected Impact

### Positive Outcomes

- ✅ Accurate conversion data in all reports
- ✅ Correct ROAS calculations
- ✅ Better strategic decisions
- ✅ Reliable WoW/MoM comparisons
- ✅ Trustworthy automated alerts

### Known Issues This Fixes

1. **Go Glean PMax Audit (2025-11-20):** Used `LAST_7_DAYS` including Nov 18-20
   - Showed 135% ROAS (incomplete)
   - Should use Nov 11-17 (complete)
   - Likely showing better performance than measured

2. **Weekly reports showing declining conversions on Mondays**
   - Due to Sunday/Saturday data being incomplete
   - Should exclude those days from weekly totals

3. **A/B test analysis ending "yesterday"**
   - Final days always show declining performance (incomplete data)
   - Misleads test conclusions

## Timeline

- **Week 1 (Nov 20-26):** High Priority agents (7 agents)
- **Week 2 (Nov 27-Dec 3):** Medium Priority agents (6 agents)
- **Week 3 (Dec 4-10):** Low Priority agents + Skills
- **Week 4 (Dec 11-17):** Testing, validation, documentation

## Success Criteria

- [ ] All 13 priority agents updated to use date_utils
- [ ] Zero agents using `LAST_7_DAYS` or similar in GAQL
- [ ] Zero agents using `datetime.now()` for end dates without lag buffer
- [ ] All agent.md files document date range approach
- [ ] Skills updated to use date_utils
- [ ] Testing confirms improved data accuracy

## References

- **Standard:** `CLAUDE.md` lines 159-247
- **Utility:** `shared/date_utils.py`
- **Example Issue:** Go Glean PMax Audit 2025-11-20
- **Discussion:** User feedback 2025-11-20

---

**Last Updated:** 20 November 2025
**Next Review:** 27 November 2025 (after Week 1 completions)
