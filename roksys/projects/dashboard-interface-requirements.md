# Dashboard Interface - Requirements Gathering

**Created**: 2025-11-10
**Status**: 📊 Monitoring & Research Phase
**Goal**: Design a Google-based browser dashboard for easy access to client audits, tasks, emails, documents, and actionable information

---

## Project Vision

**The Problem**: Information is scattered across multiple files, folders, emails, and systems. Need a central, web-based interface that makes information **easily accessible and actionable**.

**Watchwords**:
- Easy access to information
- Actionable insights
- Single source of truth
- Browser-based (Google ecosystem)

**Timeline**: Research & monitor for 2-3 weeks, then present recommendations in weekly summary

---

## Usage Patterns Observed

### Week 1 (2025-11-10 onwards)

**Session 2025-11-10**:
- ✅ Investigating Smythson Q4 dashboard automation issues
- ✅ Needed to access: dashboard script, logs, CONTEXT.md, status documentation
- ✅ Fixed API quota issues and integrated into weekly summary email
- Pattern: Debugging automation → Reading logs → Updating documentation → Testing

**Key Insights**:
- Needed quick access to automation health/status
- Logs and error tracking important for troubleshooting
- Documentation frequently updated after fixes
- Integration points between systems (dashboard → weekly email)

---

## Information Access Patterns

### What Information Is Accessed Frequently

**Client Data** (observed patterns):
- [ ] Client CONTEXT.md files
- [ ] Meeting notes
- [ ] Email drafts
- [ ] Performance data
- [ ] Audit reports
- [ ] Task lists

**System Data** (observed patterns):
- [x] Automation logs (LaunchAgent status, error logs)
- [x] Dashboard status (Smythson Q4 example)
- [ ] Script outputs
- [ ] Scheduled job status

**Cross-References** (observed patterns):
- [x] Dashboard → Weekly summary integration
- [ ] Client tasks → Google Tasks
- [ ] Email sync → Meeting notes
- [ ] Performance data → Strategy planning

---

## User Workflows Observed

### 1. **Automation Troubleshooting** (2025-11-10)
**Steps**:
1. User reports issue ("dashboard not updating")
2. Check automation logs
3. Read script code
4. Identify root cause (API quota exceeded)
5. Fix code (batch updates)
6. Test solution
7. Update documentation
8. Integrate with existing systems (weekly email)

**Pain Points**:
- Needed to know dashboard automation existed
- Logs buried in home directory
- No central "system health" view
- Documentation scattered across multiple files

**Ideal Dashboard View**:
- System health status (all LaunchAgents at a glance)
- Quick access to logs for failing jobs
- Links to relevant scripts and documentation
- Integration points visualization

---

## Potential Dashboard Sections

### Core Sections (to be refined based on observations)

#### 1. **System Health**
- LaunchAgent status (39 agents - green/yellow/red)
- Recent errors and warnings
- Last run times
- Quick links to logs

#### 2. **Client Overview**
- Client cards with quick stats
- Recent activity (emails, meetings, tasks)
- Performance alerts
- Links to CONTEXT.md, audits, documents

#### 3. **Tasks & Priorities**
- Weekly strategic priorities
- Upcoming tasks (from Google Tasks)
- Overdue items
- Client-specific task lists

#### 4. **Recent Activity**
- Email drafts created
- Meeting notes imported
- Audits completed
- Documents generated

#### 5. **Performance Dashboards**
- Smythson Q4 (example from today)
- Other client-specific dashboards
- Week-over-week comparisons
- Alerts for underperformance

#### 6. **Quick Actions**
- Run specific automation scripts
- Generate reports
- Create email drafts
- Access frequently used documents

---

## Technical Considerations

### Platform Options

**Google Sites** (low-code):
- ✅ Easy to build and maintain
- ✅ Lives in Google ecosystem
- ✅ Can embed Google Sheets dashboards
- ❌ Limited interactivity
- ❌ No custom backend logic

**Google Apps Script + Google Sheets**:
- ✅ Familiar (already using for dashboards)
- ✅ Can pull data from JSON files
- ✅ Can trigger scripts
- ❌ Limited UI flexibility
- ❌ Spreadsheet-based (not true web app)

**Custom Web App (Flask/FastAPI + Google OAuth)**:
- ✅ Full control over UI/UX
- ✅ Can integrate with all existing systems
- ✅ Real-time data updates
- ✅ Can trigger automation scripts
- ❌ Requires hosting
- ❌ More maintenance overhead

**Hybrid Approach**:
- Google Sheets for data aggregation
- Google Data Studio for visualizations
- Google Sites for navigation/structure
- Links to existing dashboards

---

## Data Sources Available

### Existing JSON Exports
- `shared/data/smythson-q4-dashboard.json` (new - created today)
- `shared/data/weekly-client-performance.json`
- `shared/data/weekly-client-strategy.json`
- `shared/data/tasks-state.json`
- `shared/data/granola-google-docs-history.json`

### Google Integrations
- Google Tasks (tasks data)
- Google Sheets (dashboards like Smythson Q4)
- Google Docs (meeting notes, client docs)
- Google Drive (file search, recent activity)
- Gmail (via email-sync)

### File System
- Client CONTEXT.md files
- Meeting notes markdown files
- Email drafts (HTML)
- Audit reports
- LaunchAgent logs

---

## Previous Failed Attempts

**Why Previous Projects "Weren't Quite Right"** (to investigate):
- [ ] What projects were attempted before?
- [ ] What didn't work about them?
- [ ] What was missing?
- [ ] What was overcomplicated?

---

## Questions to Answer Through Observation

1. **What information do you access most frequently?**
   - Observed: Automation logs, client CONTEXT.md files, dashboards
   - To monitor: Email drafts, meeting notes, task lists, performance data

2. **What are the most common workflows?**
   - Observed: Debugging → Fix → Document → Integrate
   - To monitor: Client work, reporting, strategy planning, communication

3. **What takes the most time to find?**
   - To monitor: Which files/data require multiple navigation steps?

4. **What information needs to be cross-referenced?**
   - Observed: Dashboard status → Weekly summary
   - To monitor: Tasks → Client context, Performance → Strategy priorities

5. **What would you check daily if it was easy to access?**
   - To observe over next 2-3 weeks

6. **What actions do you take repeatedly?**
   - To observe: Script runs, email drafts, report generation

---

## Next Steps

1. **Monitor for 2-3 weeks** (until ~2025-11-25 to 2025-12-01)
   - Observe which files/data accessed most frequently
   - Note pain points and time-consuming searches
   - Identify patterns in cross-referencing needs
   - Track repeated workflows

2. **Analyze patterns** (end of monitoring period)
   - Categorize information by access frequency
   - Identify most valuable quick-access sections
   - Determine which integrations are most important
   - Understand which existing systems work well

3. **Design proposal** (present in weekly summary)
   - Mockup of dashboard interface
   - Prioritized feature list
   - Technical approach recommendation
   - Implementation phases (MVP → Full)

4. **Iterate based on feedback**
   - Build MVP with most critical sections
   - Test with real workflows
   - Refine based on actual usage
   - Expand gradually

---

## Monitoring Log

### 2025-11-10
**Session Focus**: Smythson Q4 dashboard automation fix

**Information Accessed**:
- `/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/update-q4-dashboard.py`
- `~/.petesbrain-smythson-dashboard.log`
- `~/Library/LaunchAgents/com.petesbrain.smythson-dashboard.plist`
- `/Users/administrator/Documents/PetesBrain/clients/smythson/CONTEXT.md`
- `/Users/administrator/Documents/PetesBrain/clients/smythson/documents/strategy-dashboard-status.md`
- `/Users/administrator/Documents/PetesBrain/shared/scripts/knowledge-base-weekly-summary.py`

**Workflow**:
1. Identify broken automation (dashboard not updating)
2. Read automation logs to find errors
3. Analyze script code to find root cause
4. Fix Google Sheets API quota issue (78 calls → 1 batch call)
5. Install missing dependencies
6. Integrate with weekly summary email (no separate daily emails)
7. Test end-to-end
8. Update documentation

**Pain Points**:
- No central view of LaunchAgent health (had to check logs manually)
- Dashboard automation failure went unnoticed for 5 days
- Integration points not documented (had to modify two scripts)

**Ideal Dashboard Features for This Workflow**:
- **System Health Dashboard**: All 39 LaunchAgents with status (green/red)
- **Recent Errors**: Last 24 hours of errors across all automations
- **Integration Map**: Visual showing how systems connect (dashboard → weekly email)
- **Quick Test**: Button to manually trigger automation and see immediate results

**Time Savings if Dashboard Existed**:
- Current: ~15 minutes to identify issue, find logs, locate scripts
- With Dashboard: ~2 minutes (status overview → click error → view log → click to edit script)

---

## Design Principles (Emerging)

Based on today's session and user feedback:

1. **Information Should Be Easily Accessible**
   - No more than 2 clicks to any piece of information
   - Search functionality across all content
   - Smart defaults (show most relevant info first)

2. **Make Everything Actionable**
   - Not just data display - include actions
   - "Fix" buttons next to errors
   - "Generate" buttons for common tasks
   - Direct links to edit source files

3. **Single Source of Truth**
   - Dashboard aggregates from existing systems (don't duplicate data)
   - Real-time or near-real-time updates
   - Clear "last updated" timestamps

4. **Progressive Disclosure**
   - Overview → Details → Actions
   - Show summaries by default, expand for details
   - Don't overwhelm with everything at once

5. **Respect Existing Workflows**
   - Don't replace what already works (like Google Sheets dashboards)
   - Enhance and connect existing tools
   - Make it optional (can still work without dashboard)

---

## Future Review Date

**Target**: Include in weekly summary on **2025-11-25** or **2025-12-02**

**What to Include**:
- Summary of usage patterns observed
- Most frequently accessed information types
- Common workflows identified
- Dashboard mockup/proposal
- Implementation recommendation
- Estimated time savings

---

**Note**: This is a living document. Will be updated automatically as usage patterns are observed over the next 2-3 weeks.
