# Daily Briefing System Comparison: Mike Rhodes vs PetesBrain

**Date:** 2025-11-19
**Phase:** 3 - Daily Briefing System Integration
**Status:** Analysis Complete - Enhancement Recommendations Ready

---

## Executive Summary

**Key Finding:** PetesBrain's daily briefing system is MORE comprehensive and client-operations focused than Mike's personal productivity briefing. However, Mike's formatting patterns, AI summary approach, and structural organization offer valuable improvements.

**Recommendation:** Enhance PetesBrain's existing system with Mike's best practices while preserving all client-operations features.

---

## System Comparison

### Mike's Briefing System

**Architecture:**
- **Language:** Node.js
- **Trigger:** Manual/scheduled (`npm run briefing:generate`)
- **Focus:** Personal productivity + content creation
- **Output:** Single markdown file (`briefing/YYYY-MM-DD-briefing.md`)

**Data Sources:**
1. **Google Calendar** - Next 7 days of events
2. **Active Talks** - Presentation files from `content/talks/`
3. **Recent Research** - Newsletters + YouTube from last 7 days
4. **Todo Items** - Files from `todo/` directory
5. **Projects Status** - From `projects/PROJECTS.md`
6. **AI Executive Summary** - Claude Haiku generates 2-3 sentence focus summary

**Strengths:**
- ✅ Clean, hierarchical markdown structure
- ✅ AI-generated executive summary (actionable, concise)
- ✅ "Recent research" pattern surfaces latest learnings
- ✅ Time-based filtering (last 7 days)
- ✅ Clear section headers with emojis
- ✅ Minimal, scannable format

**Limitations:**
- ❌ Content creation focus (not operations)
- ❌ No client performance data
- ❌ No anomaly detection
- ❌ No priority system
- ❌ No time estimates
- ❌ Single markdown output only

### PetesBrain's Briefing System

**Architecture:**
- **Language:** Python
- **Trigger:** LaunchAgent scheduled (7:00 AM daily)
- **Focus:** Client operations + agency management
- **Output:** Dual format (markdown + HTML)

**Data Sources:**
1. **Google Calendar** - Today's events
2. **Google Tasks** - Personal tasks with due dates
3. **Client Tasks System** - Internal tasks.json per client
4. **Performance Anomalies** - `daily-performance-anomalies.json`
5. **Recent Meetings** - Last 2 days from meeting-notes/
6. **Client Performance Trends** - Week-over-week tracking
7. **AI Inbox Activity** - Notes processed, tasks created
8. **Pre-verified Tasks** - Automated verification with live data

**Strengths:**
- ✅ Client operations-focused (perfect for agency work)
- ✅ Dual output (markdown for reading, HTML for interaction)
- ✅ Priority system (P0/P1/P2/P3)
- ✅ Time estimates per task
- ✅ Source attribution (where task came from)
- ✅ Pre-verification feature (checks before showing tasks)
- ✅ Performance anomaly detection
- ✅ Client-level performance trends
- ✅ Recent meetings integration
- ✅ Truncated view + full expanded view

**Limitations:**
- ❌ AI executive summary not implemented (tries but fails if no API key)
- ❌ Formatting could be cleaner/more hierarchical
- ❌ No "recent knowledge base updates" section
- ❌ Section ordering could be optimized
- ❌ Some redundancy in task display

---

## Key Patterns to Adopt from Mike

### 1. AI Executive Summary Pattern

**Mike's Approach:**
```javascript
// After assembling all briefing content
const summary = await generateSummary(fullBriefingContent);
// Uses Claude Haiku with max 300 tokens
// Prompt: "Provide 2-3 sentence executive summary highlighting most important things"
```

**Why This Works:**
- Provides instant context ("What matters today?")
- Uses fast, cheap model (Haiku)
- Actionable and direct
- Appears at the top (first thing you see)

**PetesBrain Enhancement:**
```python
def generate_ai_summary(briefing_content):
    """
    Generate AI executive summary using Claude Haiku
    Focus on: Top 3 priorities, critical anomalies, time-sensitive items
    """
    # Use Anthropic API with Haiku model
    # Max 300 tokens
    # Prompt: Focus on client work + today's priorities
```

### 2. Hierarchical Section Structure

**Mike's Pattern:**
```markdown
# Briefing - {Date}

## 🎯 Executive Summary
{AI-generated 2-3 sentences}

---

## 📅 Calendar - Next 7 Days

### Monday, Oct 21
- **14:30** - Meeting Name
- **All Day** - Event Name

---

## 🎤 Active Talks
{Talk status}

---

## 📚 New Research (Last 7 Days)
{Recent learnings}
```

**Why This Works:**
- Clear visual hierarchy
- Emoji section markers (instant recognition)
- Horizontal rules separate major sections
- Grouped by topic, not priority
- Chronological where appropriate

**PetesBrain Current:**
```markdown
# Daily Briefing - {Date}

## 📋 Personal Tasks - DO THESE FIRST
{Tasks grouped by priority within}

## Calendar - Today
{Events}

## 🎯 Executive Summary
{AI attempt - usually fails}

## 🎯 Client Work (Upcoming)
{More tasks}

## ⚠️ Client Alerts
{Anomalies}
```

**Issues:**
- Executive summary appears AFTER tasks (should be first!)
- Too many task sections (personal + client = redundant)
- Section headers not consistently formatted
- Calendar buried (should be near top)

**Enhanced Structure:**
```markdown
# Daily Briefing - {Weekday, Day Month Year}

## 🎯 Executive Summary
{AI-generated summary of today's priorities}

---

## 📅 Calendar - Today
{Today's events}

---

## 🔥 Priority Actions (Urgent)
{P0 tasks only - critical/time-sensitive}

---

## 📋 Today's Work (High Priority)
{P1 tasks due today or overdue}

---

## 📆 This Week's Work
{P1/P2 tasks due within 7 days}

---

## ⚠️ Client Alerts (Last 24 Hours)
{Performance anomalies}

---

## 📊 Performance Overview
{Week trends}

---

## 📚 Recent Knowledge Base Updates (Last 7 Days)
{New platform docs, client insights, experiments}

---

## 👥 Recent Meetings (Last 2 Days)
{Meeting summaries}

---

*[View Full Expanded Briefing](briefing.html) for complete task details*
```

### 3. "Recent Research" Pattern

**Mike's Innovation:**
```markdown
## 📚 New Research (Last 7 Days)

#### Newsletters (3 new)
- 20251018 - [Title](path/to/file.md)
- 20251017 - [Title](path/to/file.md)

#### YouTube Videos (2 new)
- 20251019 - [Video Title](path/to/file.md)
```

**Why This Works:**
- Surfaces latest learnings automatically
- Time-based filtering (last 7 days)
- Clickable links to full content
- Shows count (quick context)

**PetesBrain Adaptation:**
```markdown
## 📚 Recent Knowledge Base Updates (Last 7 Days)

#### Platform Updates (5 new)
- 2025-11-18 - [Google tests journey-aware bidding](roksys/knowledge-base/google-ads/platform-updates/...)
- 2025-11-17 - [Minimizing marketing blind spots](...)

#### Client Insights (3 new)
- 2025-11-19 - [Smythson Black Friday promotion verification](clients/smythson/documents/...)
- 2025-11-18 - [Devonshire keyword pause summary](clients/devonshire-hotels/documents/...)

#### Experiments Logged (2 new)
- 2025-11-18 - [Superspace budget reduction] (rok-experiments-client-notes.csv)
```

**Data Sources:**
- `roksys/knowledge-base/_inbox/documents/` (processed in last 7 days)
- `clients/*/documents/` (created in last 7 days)
- `roksys/spreadsheets/rok-experiments-client-notes.csv` (last 7 days)

### 4. Clean Time Formatting

**Mike's Pattern:**
```
14:30 - Meeting Name
09:00 - Another Event
All Day - Holiday
```

**PetesBrain Current:**
```
**09:00 AM** - Event  (12-hour format with AM/PM)
```

**Recommendation:** Keep 12-hour format (more familiar for UK users) but make consistent:
```
09:00 AM - Meeting Name
02:30 PM - Client Call
All day - Holiday
```

### 5. Error Handling Pattern

**Mike's Approach:**
```javascript
// If Google Calendar fails
return "### Calendar - Today\n\n*Calendar integration temporarily unavailable*\n"

// If AI summary fails
summary = "*AI summary unavailable*"

// If no data
return "**No {source} found**\n"
```

**Why This Works:**
- Graceful degradation
- Briefing still generates
- Clear error messages
- No stack traces in output

**PetesBrain Enhancement:**
Apply same pattern consistently across all data sources.

---

## Recommendations for PetesBrain Enhancement

### Priority 1: Fix Executive Summary Placement

**Current Issue:**
- Executive summary appears AFTER personal tasks and calendar
- Usually shows "AI summary unavailable - ANTHROPIC_API_KEY not set"

**Fix:**
1. Move executive summary to TOP (right after title)
2. Implement proper Anthropic API integration
3. Use Claude Haiku (fast + cheap)
4. Focus summary on: Top 3 client priorities + critical anomalies + time-sensitive items

### Priority 2: Restructure Sections

**New Order:**
1. 🎯 Executive Summary (AI-generated)
2. 📅 Calendar - Today
3. 🔥 Priority Actions (P0 only)
4. 📋 Today's Work (P1 due today)
5. 📆 This Week (P1/P2 upcoming)
6. ⚠️ Client Alerts
7. 📊 Performance Overview
8. 📚 Recent KB Updates (NEW)
9. 👥 Recent Meetings

**Rationale:**
- Most urgent first (executive summary sets context)
- Calendar second (affects all planning)
- Tasks grouped by urgency, not source
- Learning/context sections at end

### Priority 3: Add "Recent KB Updates" Section

**Implementation:**
```python
def get_recent_kb_updates():
    """
    Get KB updates from last 7 days across:
    - Platform updates (roksys/knowledge-base/google-ads/platform-updates/)
    - Client documents (clients/*/documents/)
    - Experiment log (rok-experiments-client-notes.csv)
    """
    seven_days_ago = datetime.now() - timedelta(days=7)

    updates = {
        'platform': [],  # From KB _inbox processing
        'clients': [],   # Recent client docs
        'experiments': []  # Recent experiment log entries
    }

    # Scan and categorize
    # Return formatted markdown
```

**Value:**
- Connects daily work to recent learnings
- Surfaces platform changes that affect strategies
- Highlights recent client developments
- Shows experiment results

### Priority 4: Implement Proper AI Summary

**Implementation:**
```python
def generate_executive_summary(briefing_data):
    """
    Generate AI executive summary using Claude Haiku

    Args:
        briefing_data: Dict with calendar, tasks, anomalies, trends

    Returns:
        2-3 sentence summary focusing on:
        - Top 3 client priorities today
        - Any critical anomalies requiring attention
        - Time-sensitive items
    """
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Build context from briefing data
        context = f"""
Today's Date: {datetime.now().strftime('%A, %B %d, %Y')}

Calendar: {len(briefing_data['calendar_events'])} events today
Priority Tasks: {briefing_data['p0_count']} urgent, {briefing_data['p1_today_count']} high priority
Critical Alerts: {briefing_data['critical_anomalies_count']}
Performance: {briefing_data['clients_up']} clients up, {briefing_data['clients_down']} clients down

Task Details:
{briefing_data['top_5_tasks']}

Anomalies:
{briefing_data['anomalies']}
"""

        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"""You are Pete's AI assistant for Rok Systems, a digital marketing agency.

Based on this briefing data, provide a 2-3 sentence executive summary highlighting the most important client priorities for today. Be direct and actionable. Focus on urgent work and critical issues.

{context}

Provide only the summary, no preamble."""
            }]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"*AI summary unavailable - {str(e)}*"
```

### Priority 5: Clean Up Task Display

**Current Issues:**
- "Personal Tasks" and "Client Work" are redundant (all tasks are work)
- Truncation with "View all X tasks" is good but could be clearer
- Time estimates and sources get repetitive

**Improved Format:**
```markdown
## 🔥 Priority Actions (3 urgent)

**Due Nov 20** · **[Just Bin Bags] Follow-up review of conversion tracking**
⏱️ 30 mins · 📍 Client request
```

Consolidate personal + client tasks into priority-based sections:
- 🔥 Priority Actions (P0)
- 📋 Today's Work (P1 due today)
- 📆 This Week (P1/P2 upcoming)

---

## Implementation Plan

### Phase 1: Core Structure Improvements (1-2 hours)

**Tasks:**
1. ✅ Reorder sections (executive summary first)
2. ✅ Consolidate task sections (remove personal/client split)
3. ✅ Add horizontal rules between major sections
4. ✅ Standardize section headers with emojis
5. ✅ Move calendar near top

**Files to Modify:**
- `agents/daily-intel-report/daily-intel-report.py`

**Testing:**
```bash
cd /Users/administrator/Documents/PetesBrain/agents/daily-intel-report
python3 daily-intel-report.py
open ../../briefing/$(date +%Y-%m-%d)-briefing.html
```

### Phase 2: AI Executive Summary (30-45 mins)

**Tasks:**
1. ✅ Implement `generate_executive_summary()` function
2. ✅ Add Anthropic API integration
3. ✅ Build context from briefing data
4. ✅ Handle errors gracefully
5. ✅ Place at top of briefing

**Dependencies:**
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key"
```

### Phase 3: Recent KB Updates Section (1 hour)

**Tasks:**
1. ✅ Implement `get_recent_kb_updates()` function
2. ✅ Scan platform updates (last 7 days)
3. ✅ Scan client documents (last 7 days)
4. ✅ Scan experiment log (last 7 days)
5. ✅ Format as clickable links

**Data Sources:**
- `roksys/knowledge-base/_inbox/documents/*.md`
- `clients/*/documents/*.{md,html}`
- `roksys/spreadsheets/rok-experiments-client-notes.csv`

### Phase 4: Testing & Refinement (30 mins)

**Test Cases:**
1. ✅ Generate briefing with all features
2. ✅ Verify AI summary is actionable
3. ✅ Check KB updates appear correctly
4. ✅ Confirm task priorities display properly
5. ✅ Test error handling (missing API key, no data, etc.)

---

## Before/After Comparison

### Before (Current PetesBrain)

```markdown
# Daily Briefing - Wednesday, November 19, 2025

📄 **[View Full Expanded Briefing](briefing.html)**

---

## 📋 Personal Tasks - DO THESE FIRST

**📆 Coming Up (Next 7 Days):**

---

### Calendar - Today

**No events scheduled for today**

---

## 🎯 Executive Summary

*AI summary unavailable - ANTHROPIC_API_KEY not set*

---

## 🎯 Client Work (Upcoming)

**15 task(s)** due in next 7 days

### 🔴 URGENT (P0)

**Nov 20** · **[Just Bin Bags] Follow-up review...**
⏱️ Est. time not set · 📍 Google Tasks
```

**Issues:**
- Executive summary buried and broken
- Task sections redundant (personal + client)
- Calendar location not prominent
- No KB updates section
- Structure not scannable

### After (Enhanced)

```markdown
# Daily Briefing - Wednesday, November 19, 2025

## 🎯 Executive Summary

Focus today on Just Bin Bags conversion tracking follow-up (30 mins, due tomorrow) and Devonshire budget recommendations (client requested by Nov 21). Accessories For The Home shows stable 196% ROAS - continue monitoring. No critical anomalies detected yesterday.

---

## 📅 Calendar - Today

**No events scheduled for today**

---

## 🔥 Priority Actions (3 urgent)

**Due Nov 20** · **[Just Bin Bags] Follow-up review of conversion tracking**
⏱️ 30 mins · 📍 Client request

**[Accessories For The Home] Monitor ROAS change impact** ✅ PRE-VERIFIED
⏱️ 15 mins · 📍 Proactive monitoring
✅ 196% ROAS (last 7 days) ✓ → Reply "accessories verified - close" to complete

**Due Nov 21** · **[Devonshire] Analyse property campaign budgets**
⏱️ 45 mins · 📍 Client request (Helen)

---

## 📋 Today's Work (2 tasks)

**Due Today** · **[Client] Task Name**
⏱️ Time · 📍 Source

---

## 📆 This Week (10 tasks)

*[View all upcoming tasks](briefing.html#upcoming-tasks)*

---

## ⚠️ Client Alerts (Last 24 Hours)

**No anomalies detected yesterday ✅**

---

## 📊 Performance Overview

**Week Trends:** 0 Up ↗️  |  0 Stable →  |  0 Down ↘️

---

## 📚 Recent Knowledge Base Updates (Last 7 Days)

#### Platform Updates (3 new)
- 2025-11-18 - [Google tests journey-aware bidding](path)
- 2025-11-17 - [Minimizing marketing blind spots](path)

#### Client Developments (2 new)
- 2025-11-19 - [Smythson Black Friday verification](path)
- 2025-11-18 - [Devonshire keyword pause summary](path)

#### Experiments Logged (1 new)
- 2025-11-18 - Superspace budget reduction to £330/day

---

## 👥 Recent Meetings (Last 2 Days)

**No meetings in last 2 days**

---

*[View Full Expanded Briefing](briefing.html) for complete task details and notes*
```

**Improvements:**
- ✅ AI summary at top (context-setting)
- ✅ Calendar prominent
- ✅ Tasks grouped by urgency (not source)
- ✅ KB updates section surfaces learnings
- ✅ Clear hierarchy and scannable
- ✅ Professional, actionable

---

## Success Criteria

**Phase 3 will be complete when:**

1. ✅ Executive summary generates successfully with Anthropic API
2. ✅ Summary appears at TOP of briefing (right after title)
3. ✅ Section order optimized (summary → calendar → urgent tasks → upcoming → context)
4. ✅ "Recent KB Updates" section implemented and working
5. ✅ Task sections consolidated (no personal/client split)
6. ✅ Briefing generates in <5 seconds
7. ✅ Both markdown and HTML versions updated
8. ✅ Error handling graceful (missing API key, no data, etc.)

**Testing:**
- Generate briefing with all features enabled
- Verify AI summary is actionable and relevant
- Check KB updates surface correctly
- Confirm task display is clear and scannable
- Test on actual day with real calendar events/tasks

---

## ROI Analysis

**Time Investment:**
- Phase 1 (Structure): 1-2 hours
- Phase 2 (AI Summary): 30-45 mins
- Phase 3 (KB Updates): 1 hour
- Phase 4 (Testing): 30 mins
- **Total: 3-4 hours**

**Value Gained:**
- ✅ Executive summary provides instant daily context (saves 5-10 mins/day decision time)
- ✅ Better structure = more scannable (saves 2-3 mins/day)
- ✅ KB updates surface learnings (prevents missing important info)
- ✅ Cleaner task display = faster prioritization
- ✅ Professional format matches Mike's quality standards

**Expected Payback:**
- 5-10 minutes saved daily = ~40-80 mins/week
- Payback in 2-3 weeks
- Then ongoing efficiency + better decision-making

---

## Next Steps

1. **Implement Phase 1** (core structure improvements)
2. **Implement Phase 2** (AI executive summary)
3. **Implement Phase 3** (KB updates section)
4. **Test thoroughly** with real data
5. **Document changes** in agent.md
6. **Update LaunchAgent** if schedule changes

**Ready to proceed?** Start with Phase 1 (structure improvements) as it provides immediate value and sets foundation for other enhancements.
