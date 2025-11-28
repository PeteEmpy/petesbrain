# Bright Minds - Weekly Reporting

## Overview

Bright Minds requires **weekly Monday morning reports** comparing Google Ads performance week-over-week and year-over-year. This is critical for building trust with a client who is cautious about Google Ads spend due to poor previous agency experience.

## Reporting Flow

### 1. Internal Weekly Summary (Automated)

**Script**: `/Users/administrator/Documents/PetesBrain/shared/scripts/weekly-meeting-review.py`
**Runs**: Every Monday at 9:00 AM (automated via LaunchAgent)
**Recipient**: petere@roksys.co.uk

**What it includes**:
- Recent meetings (last 7 days)
- Completed tasks (last 7 days)
- Budget status (Devonshire, Smythson)
- **Bright Minds Google Ads performance** (NEW - added Nov 2, 2025)
  - Last complete week (Mon-Sun)
  - Revenue, ROAS, conversions
  - Progress toward £4.00 ROAS target
- Shared drive updates

**Purpose**: Peter's internal review before sending client-facing reports.

**Note**: This email summary is **for Peter only** - it provides a quick overview to prepare for client communication.

### 2. Client-Facing Report (Manual, for now)

**Recipients**:
- Barry Ricketts (barry@brightminds.co.uk) - Business owner
- Sharon (sharon@brightminds.co.uk) - Technical lead

**Required Content**:
- Previous week's performance (conversion value, ROAS, conversions)
- Week-over-week comparison (last 3-4 weeks trend)
- Year-over-year comparison (same week last year)
- Trajectory toward Christmas goals
- ROAS progress toward £4.00 target
- Brief commentary on performance

**Tone**:
- Reassuring (build trust after poor previous agency)
- Data-driven (show clear evidence of results)
- Transparent (explain any spend increases with ROI context)
- Forward-looking (Christmas trajectory for educational toys)

## Current Status

### ✅ Implemented

1. **CONTEXT.md updated** with weekly reporting requirements
2. **Weekly summary email** now includes Bright Minds performance section
3. **Account ID** documented (1404868570)
4. **Target ROAS** set (£4.00)

### ⏳ Pending Implementation

1. **Google Ads data queries** - MCP GAQL queries for:
   - Last 4 weeks of data (week-by-week)
   - Same period last year
   - Current performance metrics

2. **Client-facing email generation** - Automated script to:
   - Query Google Ads via MCP
   - Calculate trends and comparisons
   - Generate formatted email content
   - Optional: Auto-send to Barry and Sharon

## Quick Start

### Running the Internal Weekly Summary (Manual)

```bash
cd /Users/administrator/Documents/PetesBrain
shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

This will generate and send the internal weekly summary email to Peter with Bright Minds performance included.

### Generating Client-Facing Report (Template)

**IMPORTANT**: Keep it simple! Barry needs concise summaries, not detailed analysis.

```
Subject: Bright Minds - Weekly Update ([Week dates])

Hi Barry and Sharon,

Quick update for last week:

Revenue: £[amount] | Ad Spend: £[amount] | ROAS: [XXX]%

[1-2 sentences explaining what's happening - is performance improving, stable, or needs attention?]

[If relevant: 1 sentence about Christmas trajectory or trend]

All looking good / We're keeping a close eye on [specific area] / Great progress this week.

Let me know if you have any questions.

Best regards,
Peter

---
Peter Empson | Rok Systems
petere@roksys.co.uk | 07932 454652
```

**Example 1 - Good Week**:
```
Hi Barry and Sharon,

Quick update for last week:

Revenue: £1,245 | Ad Spend: £380 | ROAS: 328%

Performance is trending in the right direction. We're still in the learning phase after the October restructure, and ROAS is steadily moving toward our 400% target. Christmas traffic is starting to pick up as expected for educational toys.

All looking good.

Best regards,
Peter
```

**Example 2 - Needs Attention**:
```
Hi Barry and Sharon,

Quick update for last week:

Revenue: £890 | Ad Spend: £420 | ROAS: 212%

Revenue was down slightly this week, which looks like a stock issue with a few bestselling products. I've checked the feed and flagged the items - once they're back in stock we should see performance bounce back.

We're keeping a close eye on it.

Best regards,
Peter
```

## Data Sources

### Google Ads Account: 1404868570 (BrightMinds)

**Key Metrics to Query**:
- `metrics.conversions_value` - Revenue
- `metrics.cost_micros` - Ad spend (divide by 1,000,000)
- `metrics.conversions` - Conversion count
- Calculated: ROAS = conversion_value / cost

**Date Ranges Needed**:
1. **Current week** (last complete Mon-Sun)
2. **Previous 3 weeks** (for trend)
3. **Same week last year** (YoY comparison)

**Example GAQL Query**:
```sql
SELECT
    metrics.conversions_value,
    metrics.cost_micros,
    metrics.conversions,
    metrics.clicks,
    metrics.impressions
FROM customer
WHERE segments.date BETWEEN '2025-10-28' AND '2025-11-03'
```

## Next Steps

1. **Implement MCP GAQL queries** in `get_bright_minds_performance()` function
2. **Add trend calculation** (4-week comparison logic)
3. **Add YoY comparison** (query last year's data)
4. **Create client email generator** (separate script or extend weekly-meeting-review.py)
5. **Test with actual data** and validate calculations
6. **Optional**: Automate client email sending (requires approval)

## Important Notes

### Client Context (from CONTEXT.md)

- **Previous agency**: Did not deliver results - client is cautious
- **Weekly reporting**: REQUIRED every Monday to build trust
- **Business**: Educational toys (peak season: Christmas)
- **Target ROAS**: £4.00 (currently in learning phase post-restructure)
- **Key contacts**: Barry (owner, final authority), Sharon (technical, day-to-day)

### Communication Principles

1. **Always frame spend increases with ROI context**
   - Example: "Extra £594 spend generated £1,735 revenue"

2. **Explain learning phases clearly**
   - Example: "ROAS currently £2.92, heading toward £4.00 target as campaigns optimize"

3. **Compare to seasonal baselines, not just raw YoY**
   - Example: "22% growth above normal October seasonal patterns"

4. **Reassure during transitions**
   - Example: "This is expected during the learning phase after account restructure"

5. **Emphasize Christmas trajectory for educational toys**
   - October typically shows 18.5% seasonal increase
   - Q4 is peak season for children's educational toys

## Files

- `/clients/bright-minds/CONTEXT.md` - Client context and preferences
- `/clients/bright-minds/scripts/weekly-report.py` - Report generator (pending MCP implementation)
- `/shared/scripts/weekly-meeting-review.py` - Internal weekly summary (includes Bright Minds section)
- This file: Documentation and templates

## Support

For questions or issues with reporting:
- Check CONTEXT.md for client communication preferences
- Review experiment log: `/roksys/spreadsheets/rok-experiments-client-notes.csv`
- Check Knowledge Base for Google Ads best practices: `/roksys/knowledge-base/google-ads/`
