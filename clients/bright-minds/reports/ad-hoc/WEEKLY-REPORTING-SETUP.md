# Bright Minds Weekly Reporting - Implementation Summary

**Date**: November 2, 2025
**Status**: ✅ Partially Complete (infrastructure ready, data integration pending)

## What Was Requested

Barry Ricketts (owner) and Sharon (technical lead) require **weekly Monday morning reports** comparing Google Ads performance:

1. **Previous week's performance** vs. last 3-4 weeks (trend)
2. **Year-over-year comparison** (same week last year)
3. **Christmas trajectory analysis** (critical for educational toys peak season)
4. **ROAS progress** toward £4.00 target

**Why**: Client is cautious about Google Ads spend due to poor previous agency experience. Weekly reporting builds trust and demonstrates results.

## What Has Been Implemented

### ✅ 1. CONTEXT.md Updated

**File**: `/clients/bright-minds/CONTEXT.md`

**Changes**:
- Added weekly reporting requirements to "Client Preferences & Communication"
- Documented client cautious approach and need for weekly reassurance
- Updated decision-making section (Barry = owner, Sharon = technical)
- Added Google Ads account ID: 1404868570
- Created ongoing task: "Send weekly Monday report to Barry and Sharon"
- Documented the Nov 2 weekly reporting implementation

### ✅ 2. Automated Internal Weekly Summary

**File**: `/shared/scripts/weekly-meeting-review.py`

**Changes**:
- Added `get_bright_minds_performance()` function (placeholder for now)
- Added Bright Minds section to HTML email report
- Integrated with existing Monday 9 AM automated email
- Shows: week dates, revenue, ROAS vs. target, status

**Purpose**: Peter receives Monday morning summary with Bright Minds performance overview before sending client-facing report.

**What it looks like**:

```
📊 Bright Minds - Google Ads Performance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Week of 2025-10-28 - 2025-11-03
Status: On Track / Needs Attention / Excellent

Revenue:     £[amount]
Ad Spend:    £[amount]
ROAS:        £X.XX (target: £4.00)
Conversions: [number]

Note: This summary is for Peter's internal review.
Separate client-facing report sent to Barry and Sharon.
```

### ✅ 3. Documentation Created

**Files**:
- `/clients/bright-minds/scripts/README.md` - Comprehensive reporting guide
- `/clients/bright-minds/scripts/weekly-report.py` - Report generator script (template)
- `/clients/bright-minds/WEEKLY-REPORTING-SETUP.md` - This file

**Contents**:
- Email template for client-facing reports
- GAQL query examples for Google Ads data
- Tone guidelines (reassuring, data-driven, transparent)
- Client context reminders (previous agency, Christmas trajectory, etc.)

## What Still Needs To Be Done

### ⏳ 1. Google Ads Data Integration (HIGH PRIORITY)

**Task**: Implement MCP GAQL queries in `get_bright_minds_performance()` function

**Required Queries**:

```python
# Week 1 (current/last complete week)
query_week_1 = """
SELECT
    metrics.conversions_value,
    metrics.cost_micros,
    metrics.conversions
FROM customer
WHERE segments.date BETWEEN '2025-10-28' AND '2025-11-03'
"""

# Weeks 2-4 (previous 3 weeks for trend)
# ... similar queries with date ranges

# Same week last year (YoY comparison)
query_lly = """
SELECT
    metrics.conversions_value,
    metrics.cost_micros,
    metrics.conversions
FROM customer
WHERE segments.date BETWEEN '2024-10-30' AND '2024-11-05'
"""
```

**How to implement**:
1. Use MCP Google Ads tool: `mcp__google-ads__run_gaql`
2. Account ID: `1404868570`
3. Query for 4 consecutive weeks + same week last year
4. Calculate ROAS = conversion_value / (cost_micros / 1,000,000)
5. Return structured data dict

### ⏳ 2. Client-Facing Email Generation (MEDIUM PRIORITY)

**Option A - Manual (current approach)**:
- Peter receives internal summary Monday 9 AM
- Manually drafts client email using template
- Sends to Barry and Sharon

**Option B - Automated (future enhancement)**:
- Script generates formatted client email
- Auto-sends Monday mornings
- Requires approval/testing before enabling

**Recommendation**: Start with Option A (manual) to ensure quality and tone, then automate once pattern is established.

### ⏳ 3. Trend Analysis Logic (MEDIUM PRIORITY)

**Task**: Add week-over-week comparison and trend detection

**Logic needed**:
```python
# Compare current week to previous weeks
trend = "improving" if week1_roas > week2_roas > week3_roas else "stable"

# YoY growth calculation
yoy_growth = ((week1_revenue - lly_revenue) / lly_revenue) * 100

# Christmas trajectory (compare to seasonal baseline)
expected_seasonal_lift = 0.185  # 18.5% typical October increase
actual_vs_expected = calculate_variance()
```

### ⏳ 4. Testing with Real Data (HIGH PRIORITY)

**Before first client email**:
1. Run queries with actual Google Ads data
2. Verify ROAS calculations match Google Ads UI
3. Test trend analysis logic
4. Review commentary tone and content
5. Get Peter's approval on first draft

## How To Use (Current State)

### Monday Morning Workflow

**9:00 AM - Automated Internal Summary Arrives**
- Check email from weekly-meeting-review.py
- Review Bright Minds section (currently shows placeholder data)
- Note: Revenue, ROAS, conversions

**9:15 AM - Generate Client-Facing Report (Manual)**
1. Open template: `/clients/bright-minds/scripts/README.md`
2. Copy email template
3. Fill in bracketed placeholders with actual data from Google Ads UI
4. Add commentary:
   - Week-over-week trend (4 weeks)
   - Year-over-year comparison
   - Christmas trajectory analysis
   - 2-3 key insights
5. Send to Barry and Sharon

**Time required**: ~15-20 minutes per week (until automated)

## Important Reminders

### Client Communication Principles

1. **KEEP IT SIMPLE**: Barry wants concise updates (3-4 sentences max), not detailed analysis
2. **Build Trust**: Client is cautious due to previous agency - weekly reporting critical
3. **Data-Driven**: Show key numbers (Revenue, Spend, ROAS) but don't overwhelm with detail
4. **Transparent**: Explain what's happening in plain language (avoid jargon)
5. **Reassuring**: Simple closing line ("All looking good" or "Keeping an eye on [X]")

### Key Context

- **Previous agency**: Did not deliver results → client skeptical
- **Business**: Children's educational toys (STEM focus)
- **Seasonality**: October +18.5% baseline, Christmas is peak
- **Target ROAS**: 400% (currently in learning phase post-Oct 8 restructure)
- **Contacts**: Barry (owner, final decisions), Sharon (technical, day-to-day)

## Files Reference

| File | Purpose |
|------|---------|
| `/clients/bright-minds/CONTEXT.md` | Client knowledge base (preferences, history, context) |
| `/clients/bright-minds/scripts/README.md` | Reporting documentation and templates |
| `/clients/bright-minds/scripts/weekly-report.py` | Report generator (pending data integration) |
| `/shared/scripts/weekly-meeting-review.py` | Automated Monday internal summary (includes Bright Minds) |
| This file | Implementation summary and next steps |

## Next Actions

**Immediate (this week)**:
1. [ ] Implement MCP GAQL queries in `get_bright_minds_performance()`
2. [ ] Test with actual Google Ads data
3. [ ] Send first manual client-facing report (template-based)
4. [ ] Get client feedback on report format/content

**Short-term (next 2 weeks)**:
1. [ ] Add trend analysis logic (4-week comparison)
2. [ ] Add YoY comparison logic
3. [ ] Refine email template based on client feedback
4. [ ] Consider automation for client-facing emails

**Long-term (ongoing)**:
1. [ ] Monitor ROAS progression toward £4.00
2. [ ] Track Christmas performance vs. trajectory
3. [ ] Build trust through consistent weekly reporting
4. [ ] Adjust strategy based on performance trends

## Questions?

- Check CONTEXT.md for client preferences and communication style
- Review experiment log for strategic context: `/roksys/spreadsheets/rok-experiments-client-notes.csv`
- See Knowledge Base for Google Ads best practices: `/roksys/knowledge-base/google-ads/`

---

**Implementation by**: Claude Code
**Date**: November 2, 2025
**Status**: Infrastructure complete, data integration pending
