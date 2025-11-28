# Improved Weekly Summary System

## Overview

The weekly summary system has been upgraded to match the daily briefing improvements: **proactive strategic planning for ALL clients**, not just reactive reporting.

## What Changed

### Before ❌

The old weekly summary only showed:
- KB articles added
- AI newsletter summaries
- Upcoming tasks from Google Tasks
- Performance data (if available)

**Problem**: No strategic planning. No proactive analysis of what each client needs THIS WEEK.

### After ✅

The new system:

1. **Analyzes every client strategically** using AI
2. **Generates 2-4 strategic priorities per client** for the week
3. **Classifies by type** (reporting, optimization, planning, communication, review, experiment)
4. **Assigns impact levels** (high/medium/low)
5. **Explains WHY** each priority matters this week
6. **Differentiates strategic (weekly) from tactical (daily)**

## Architecture

### New Component: Weekly Client Strategy Generator

**File**: `shared/scripts/weekly-client-strategy-generator.py`

**What it does**:
- **Checks Google Calendar for weekend plans** (Entire Friday 00:00 - Sunday 11:59pm)
  - Scans whole Friday to catch early finishes or full day off
  - Searches for keywords: holiday, vacation, away, break, grasmere, lake district, travel, trip
  - Detects all-day events (common for holidays)
  - Returns structured data: `{'has_plans': True, 'friday_date': 'Nov 15', 'plans': [...]}`
  - Saves weekend context in JSON for weekly summary email
- Analyzes all 17 clients for STRATEGIC priorities
- Reviews last week's performance trends
- Reads CONTEXT.md for goals and ongoing work
- Checks recent meetings (last 2 weeks) for context
- Reviews what was completed last week
- Uses Claude to identify 2-4 strategic priorities per client

**Strategic vs Tactical**:
- **Strategic** (weekly): "Complete Q4 performance projection", "Develop budget ramp strategy"
- **Tactical** (daily): "Check budget pacing", "Review search terms"

**Test Results**:
```
17/17 clients analyzed
53 strategic priorities identified
- 37 high-impact priorities
- 16 medium-impact priorities
- 0 low-impact priorities (filtered out)

By Type:
- review: 14 priorities
- planning: 11 priorities
- optimization: 11 priorities
- communication: 8 priorities
- reporting: 6 priorities
- experiment: 3 priorities
```

### Enhanced Component: Knowledge Base Weekly Summary

**File**: `shared/scripts/knowledge-base-weekly-summary.py`

**Changes**:
1. Runs `weekly-client-strategy-generator.py` FIRST
2. Loads strategic priorities from JSON
3. Passes to Claude for email generation
4. New section structure:
   - **🎯 Strategic Priorities for This Week** (NEW - FIRST)
   - **📅 Week Ahead - Tactical Tasks** (existing)
   - **📊 Client Performance - Last Week** (existing)
   - AI News Highlights (existing)
   - KB Additions (existing)
   - Key Insights (existing)

## Weekly Email Structure

### Section 0: Weekend Plans Notice (NEW!)

**If weekend plans detected on family calendar:**
- Prominent warning box at top of email
- Shows weekend plan summary (e.g., "Grasmere", "Lake District holiday")
- Recommends finishing by lunchtime Friday with specific date
- Suggests prioritizing high-impact work early in week
- Helps with time management and work-life balance

**Example:**
```
⚠️ WEEKEND PLANS NOTICE
Weekend Plans: Grasmere
Recommendation: Aim to finish by lunchtime Friday (Nov 15) to allow for travel/preparation.
Plan high-impact priorities for Monday-Thursday!
```

**Keywords detected:**
- holiday, vacation, away, break
- grasmere, lake district
- travel, trip

### Section 1: Strategic Priorities (NEW!)

Groups priorities by:
- Strategy type (reporting, optimization, planning, etc.)
- Impact level (high/medium/low)
- Client

For each priority:
- What needs to be accomplished
- WHY it's strategically important
- What success looks like by Friday

**Example**:
```
🔴 HIGH IMPACT PRIORITIES

Reporting & Reviews (3 priorities):
- [devonshire-hotels] Complete October Performance Report with Critical Insights
  WHY: Client meeting next week requires comprehensive month-end analysis

- [accessories-for-the-home] Complete Full-Week ROAS Target Adjustment Impact Analysis
  WHY: ROAS target changed last week, need data to guide next steps

Planning (2 priorities):
- [bright-minds] Q4 Budget Ramp Strategy Validation
  WHY: Budget increase approved, need detailed ramp plan before implementation
```

### Section 2: Week Ahead - Tactical Tasks

Existing section - specific to-dos from Google Tasks

### Section 3: Client Performance

Existing section - last week's performance data

## LaunchAgent Configuration

**File**: `~/Library/LaunchAgents/com.petesbrain.kb-weekly-summary.plist`

**Schedule**: Every Monday at 8:30 AM

**Runs**:
1. `weekly-client-strategy-generator.py` (generates strategic priorities)
2. `knowledge-base-weekly-summary.py` (generates and emails summary)

**No changes needed** - LaunchAgent already configured correctly.

## Strategic vs Tactical Thinking

### Daily Briefing (Tactical)
- "What needs doing TODAY?"
- Urgent issues (P0/P1/P2)
- Quick tasks (10 mins to 2 hours)
- Reactive to immediate needs
- 51 tasks across 17 clients

### Weekly Summary (Strategic)
- "What should be accomplished THIS WEEK?"
- Strategic priorities (high/medium impact)
- Larger initiatives (planning, reviews, experiments)
- Proactive planning
- 53 priorities across 17 clients

## Key Differences from Daily System

| Aspect | Daily Briefing | Weekly Summary |
|--------|---------------|----------------|
| **Time Horizon** | Today | This Week |
| **Focus** | Tactical tasks | Strategic priorities |
| **Typical Task** | "Check budget pacing (30 mins)" | "Develop Q4 budget strategy (high impact)" |
| **Context Window** | Last 7 days | Last 14 days |
| **Client Data** | Recent alerts, meetings | Performance trends, completed work |
| **Output** | 1-3 tasks per client | 2-4 priorities per client |
| **Priority System** | P0/P1/P2 + time estimate | High/Medium/Low impact + effort level |
| **Classification** | By urgency | By type (reporting, optimization, etc.) |

## Example Strategic Priorities

### High-Impact Reporting
- "Complete October Performance Report with Critical Insights" (Devonshire Hotels)
- "Prepare November Monthly Performance Narrative" (Clear Prospects)

### High-Impact Planning
- "Q4 Budget Ramp Strategy Validation" (Bright Minds)
- "Develop Preliminary Q4 Performance Projection" (Accessories for the Home)

### High-Impact Optimization
- "Merchant Center Disapproval Recovery Strategy" (Clear Prospects)
- "Conversion Tracking Recovery & Performance Impact Assessment" (Crowd Control)

### High-Impact Reviews
- "Complete Full-Week ROAS Target Adjustment Impact Analysis" (Accessories for the Home)
- "Product Category Performance Deep Dive" (Crowd Control)

## Testing

Test the weekly strategy generator:

```bash
cd /Users/administrator/Documents/PetesBrain

ANTHROPIC_API_KEY="..." \
/usr/local/bin/python3 shared/scripts/weekly-client-strategy-generator.py
```

Output:
- Analyzes all 17 clients (~2-3 minutes)
- Saves to `shared/data/weekly-client-strategy.json`
- Shows summary by impact and type

Test the complete weekly summary:

```bash
# Note: Requires Gmail OAuth setup
ANTHROPIC_API_KEY="..." \
/usr/local/bin/python3 shared/scripts/knowledge-base-weekly-summary.py
```

Output:
- Generates strategic priorities
- Creates comprehensive weekly email
- Sends to petere@roksys.co.uk

## Files Modified/Created

### New Files
- `shared/scripts/weekly-client-strategy-generator.py`
- `docs/IMPROVED-WEEKLY-SUMMARY.md` (this file)

### Modified Files
- `shared/scripts/knowledge-base-weekly-summary.py`
  - Added `get_weekly_client_strategy()` function
  - Updated `analyze_knowledge_base_with_claude()` to accept strategy_data
  - Added strategy summaries to Claude prompt
  - Restructured sections (strategic first, then tactical)
  - Runs strategy generator before analysis

### Data Files
- `shared/data/weekly-client-strategy.json` (generated weekly)
  - Strategic priorities for all clients
  - Used by weekly summary email

## Cost

**Weekly cost**: ~$0.02-0.03 in Claude API calls
- 17 clients × ~$0.001-0.002 per strategic analysis
- 1 email summary generation (~$0.005)

**Annual cost**: ~$1.50-2.00

Minimal cost for strategic planning across all clients.

## Integration with Daily Briefing

The two systems work together:

**Monday Morning Workflow**:
1. **8:30 AM**: Weekly summary email arrives
   - Strategic priorities for THE WEEK
   - 53 priorities across 17 clients
   - Organized by impact and type

2. **7:00 AM** (Daily): Daily briefing already ran
   - Tactical tasks for TODAY
   - 51 tasks across 17 clients
   - Organized by urgency (P0/P1/P2)

**Planning Approach**:
1. Monday: Read weekly summary for strategic direction
2. Each morning: Read daily briefing for tactical execution
3. Week end: Review what strategic priorities were accomplished

## Next Steps

After setup is complete:

1. ✅ **Check Monday email** - first improved weekly summary
2. ✅ **Review strategic priorities** - plan your week
3. ✅ **Use with daily briefing** - strategic + tactical view
4. ✅ **Runs automatically** - every Monday at 8:30 AM

## Comparison Example

For client "Smythson":

**Daily Briefing (Tactical)**:
- P1: Update Q4 dashboard with latest data (30 mins)
- P2: Review auction insights and competitive landscape (30 mins)

**Weekly Summary (Strategic)**:
- HIGH: Develop Comprehensive Q4 Performance Projection (high effort, high impact)
  WHY: Q4 strategy requires data-driven forecasting to guide budget allocation decisions
- MEDIUM: Establish Weekly Dashboard Review Cadence (medium effort, medium impact)
  WHY: Systematic monitoring prevents performance drift

See the difference? Strategic thinking vs tactical execution.

## Full Documentation

- Daily system: [IMPROVED-DAILY-BRIEFING.md](IMPROVED-DAILY-BRIEFING.md)
- Quick start: [QUICK-START-IMPROVED-BRIEFING.md](QUICK-START-IMPROVED-BRIEFING.md)
- Weekly system: This document

Both systems follow the same pattern: **proactive AI analysis of ALL clients**.
