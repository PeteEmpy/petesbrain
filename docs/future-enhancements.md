# Pete's Brain - Future Enhancements

Central backlog of ideas, improvements, and features to implement when needed.

**Last Updated**: 2025-11-09

---

## Recently Completed ✅

### Product Impact Analyzer - Phase 2 (Full Automation)
**Status**: ✅ **COMPLETED** - October 30, 2025
**Effort**: High
**Value**: High

Transformed the Product Impact Analyzer from Claude-assisted to fully automated weekly workflow.

**What Was Built**:
- ✅ Automated weekly execution (Tuesday 9 AM via LaunchAgent)
- ✅ HTML email report generation with professional design
- ✅ Historical trend tracking system
- ✅ Statistical anomaly detection (z-score based)
- ✅ Predictive insights from trend analysis
- ✅ Data fetcher script for MCP integration
- ✅ One-command setup script (`setup_automation.sh`)
- ✅ Comprehensive Phase 2 documentation

**New Components**:
- `run_automated_analysis.py` - Main automation orchestrator
- `fetch_data.py` - MCP data fetching helper
- `trend_analyzer.py` - Trend analysis and anomaly detection
- `setup_automation.sh` - Automated setup
- `com.petesbrain.product-impact-analyzer.plist` - LaunchAgent config
- `PHASE2.md` - Complete Phase 2 documentation

**Location**: `tools/product-impact-analyzer/`

**Documentation**:
- `tools/product-impact-analyzer/PHASE2.md` - Complete guide
- `tools/product-impact-analyzer/README.md` - Updated for Phase 2

---

## High Priority

Ideas that would provide significant value or solve current pain points.

### Report Generator - Interactive Data Visualization Tool
**Status**: Prototype Built
**Effort**: Medium (integration work remaining)
**Value**: High

Professional, interactive report generation system for Google Ads and Analytics data with graphical visualizations.

**What's Built**:
- ✅ Flask web application with interactive UI (http://localhost:5002)
- ✅ Q4 Strategy Report template (fully functional with Smythson data)
- ✅ Interactive Chart.js visualizations (budget allocation, ROAS comparison, revenue tracking)
- ✅ Dynamic chart controls (toggle between different data views)
- ✅ Multiple report types scaffolded (Weekly Performance, Monthly Summary, Campaign Analysis)
- ✅ Export functionality (HTML, JSON, PDF-ready)
- ✅ Client auto-discovery from Pete's Brain structure
- ✅ Report library for browsing saved reports
- ✅ Comprehensive documentation (TOOL_CLAUDE.md, README.md)

**Location**: `tools/report-generator/`

**What Needs Completion**:
1. **MCP Integration** - Connect to live Google Ads/Analytics data
   - Currently uses placeholder data for non-Smythson clients
   - Need to replace fetch functions with real MCP calls
   - Add account mapping for all clients (not just Smythson)

2. **Additional Report Templates** - Complete the scaffolded templates
   - Weekly Performance Report (template exists, needs data structure)
   - Monthly Summary Report (template exists, needs data structure)
   - Campaign Analysis Report (template exists, needs data structure)

3. **PDF Export** - Implement WeasyPrint functionality
   - Library already installed
   - Need to implement HTML-to-PDF conversion
   - Ensure charts render as images in PDF

4. **Scheduled Reports** - Automation capability
   - Weekly/monthly automated generation
   - Email delivery via Gmail API integration
   - Configurable schedules per client

5. **Advanced Features** (optional)
   - Report comparison (week-over-week, YoY)
   - Custom branding per client
   - More chart types (line charts, heatmaps, mixed charts)
   - Interactive filters and date range selectors
   - API endpoints for programmatic access

**Benefits**:
- Professional client-ready reports with interactive visualizations
- Recreates reports like those from external tools (e.g., Marble AI)
- Easy sharing via HTML export or future PDF generation
- Saves time creating manual reports
- Consistent branding and data presentation
- Self-service report generation for any client

**Current Capabilities Demo**:
- Smythson Q4 2025 report shows real October Google Ads data
- 4 regions (UK, USA, EUR, ROW) with performance vs targets
- Interactive charts with hover tooltips and view toggles
- Professional gradient design with color-coded regions
- Timeline milestones and strategic recommendations

**Next Steps**:
1. Add Google Ads MCP integration for live data fetching
2. Build out remaining report templates (weekly, monthly, campaign analysis)
3. Implement PDF export
4. Consider automation/scheduling if valuable

**References**:
- `tools/report-generator/TOOL_CLAUDE.md` - Complete technical documentation
- `tools/report-generator/README.md` - User guide
- Original Smythson report: `clients/smythson/q4-2025-strategy-report.html`

---

### Calendar Integration for Meeting Validation
**Status**: Documented
**Effort**: Medium
**Value**: High

Cross-reference meeting notes with Google Calendar events to validate client assignments.

**Benefits**:
- Calendar event title may contain client name
- Event description could have client context
- Attendee email addresses indicate client (e.g., client domain names)
- Auto-suggest correct client based on calendar metadata
- Improve both Granola import accuracy and weekly review validation

**Implementation Requirements**:
- Google Calendar API setup (similar to existing Gmail API)
- OAuth scope: `https://www.googleapis.com/auth/calendar.readonly`
- Match meeting timestamps from notes to calendar events
- Create attendee domain → client mapping table
- Integrate into both weekly-meeting-review.py and Granola importer

**References**: `shared/scripts/README.md` - Future Enhancements section

---

## Medium Priority

Useful improvements that would enhance workflows.

### WhatsApp Message Processing
**Status**: Partial Implementation
**Effort**: Medium-High
**Value**: Medium

Process WhatsApp messages similar to Google Chat, automatically allocating chats to clients and creating tasks.

**What's Built**:
- ✅ Email-based WhatsApp client (`shared/whatsapp_via_email_client.py`)
- ✅ WhatsApp Business API client structure (`shared/whatsapp_business_client.py`)
- ✅ WhatsApp processor (`agents/system/whatsapp-processor.py`)
- ✅ Basic email-based processing tested successfully (found 3 messages)
- ✅ Integration with inbox routing system

**Current Limitations**:
- ⚠️ Email-based approach requires WhatsApp email notifications (not always available)
- ⚠️ WhatsApp doesn't reliably send email notifications for all messages
- ⚠️ Message extraction depends on email format (may vary)
- ⚠️ WhatsApp Business API requires Meta Developer Account setup and webhook infrastructure

**Future Development Tasks**:

**Phase 1: Improve Email-Based Processing**
- Better email pattern matching for different WhatsApp notification formats
- Enhanced sender identification (phone number extraction, contact matching)
- Handle group messages vs. individual messages
- Extract media attachments if mentioned in emails

**Phase 2: WhatsApp Business API Integration**
- Meta Developer Account setup
- WhatsApp Business App configuration
- Webhook endpoint infrastructure (Flask/FastAPI server)
- Real-time message processing via webhooks
- Message storage/database for received messages

**Phase 3: AI-Enhanced Processing**
- AI-enhanced WhatsApp processor (similar to `ai-google-chat-processor.py`)
- Auto-detect clients and tasks using Claude AI
- LaunchAgent automation for periodic processing

**Phase 4: Alternative Approaches**
- Research WhatsApp Web automation (may violate ToS)
- Evaluate third-party API services (Twilio, etc.)
- Streamlined manual forwarding workflow

**Benefits**:
- Process WhatsApp messages same way as Google Chat
- Automatic client detection and task creation
- Consistent workflow across messaging platforms
- Capture important WhatsApp conversations in client context

**Decision Points Needed**:
1. Which approach to prioritize? (Email-based vs. Business API)
2. Is WhatsApp Business API setup worth the complexity?
3. Should we invest in webhook infrastructure?

**References**:
- `docs/WHATSAPP-PROCESSING.md` - Current implementation guide
- `docs/FUTURE-DEVELOPMENT/WHATSAPP-PROCESSING.md` - Detailed future development plan
- `shared/whatsapp_via_email_client.py` - Email-based client
- `shared/whatsapp_business_client.py` - Business API client
- `agents/system/whatsapp-processor.py` - Message processor

---

### Project Migration & Laptop Sync System
**Status**: ✅ Complete
**Effort**: Medium
**Value**: Medium

Create setup scripts and migration tools to easily transfer the entire Pete's Brain project to another computer (e.g., laptop).

**Challenges**:
- Absolute paths in LaunchAgents, MCP configs, scripts (`/Users/administrator/...`)
- macOS-specific integrations (LaunchAgents, credentials)
- API credentials and OAuth tokens in various locations
- Large data files (client emails, documents, meeting notes)
- Python virtual environments don't transfer (need rebuilding)

**Solutions Implemented**:

**Option A: Git-Based Transfer with Setup Script** ✅ (Recommended)
- ✅ Created `setup-new-machine.sh` that:
  - ✅ Checks for required tools (Python, Git, etc.)
  - ✅ Creates all virtual environments (main + MCP servers)
  - ✅ Prompts for API keys and credentials
  - ✅ Updates paths in LaunchAgents for new machine
  - ✅ Updates paths in MCP config (.mcp.json)
  - ✅ Creates necessary directories
  - ✅ Validates MCP server configs and LaunchAgents
- Works with existing git workflow
- Keeps credentials separate (more secure)
- Easy to keep in sync

**Option B: Full Migration Package** ✅
- ✅ Created `create-migration-package.sh` that:
  - ✅ Creates tarball of entire project (excludes venv, credentials)
  - ✅ Documents what credentials to copy manually
  - ✅ Includes setup script for new machine
  - ✅ Lists manual configuration steps
  - ✅ Creates comprehensive migration instructions
- For complete one-time transfers

**Option C: Laptop-Sync Script** ✅ (Already existed)
- ✅ `sync-petesbrain.sh` already exists:
  - ✅ Syncs via Git or iCloud Drive
  - ✅ Excludes large files/credentials
  - ✅ Updates paths automatically
  - ✅ Keeps code and docs in sync
- For maintaining laptop as secondary machine

**Files Created**:
- `shared/scripts/setup-new-machine.sh` - Comprehensive setup script
- `shared/scripts/create-migration-package.sh` - Migration package creator
- `docs/LAPTOP-INSTALLATION-GUIDE.md` - Step-by-step installation guide (already existed)
- `docs/SYNC-SYSTEM.md` - Sync system documentation (already existed)

**Benefits**:
- Work from laptop when away from main machine
- Easy disaster recovery/backup
- Test changes on different machine before deploying
- Share setup with team members

**Usage**:
1. **For new machine setup:** Run `./shared/scripts/setup-new-machine.sh`
2. **For creating migration package:** Run `./shared/scripts/create-migration-package.sh`
3. **For ongoing sync:** Use `sync-petesbrain pull/push/both`

**References**:
- User request: Oct 31, 2025 (end-of-week session)
- Completed: Nov 7, 2025

---

### Auto-Detection of Company vs Client Meetings
**Status**: Idea
**Effort**: Low-Medium
**Value**: Medium

Use keyword detection to automatically identify company meetings vs client meetings.

**Approach**:
- Keywords like "internal", "team meeting", "standup", "planning"
- Participant analysis (all internal email addresses = company meeting)
- Calendar integration (once implemented) could enhance this
- Auto-route to roksys/meeting-notes/ instead of client folders

**References**: `shared/scripts/README.md` - Future Enhancements section

---

### Integration with Email Sync to Auto-Extract Insights
**Status**: Idea
**Effort**: Medium-High
**Value**: Medium

Automatically extract key insights from emails and update CONTEXT.md files.

**Approach**:
- Run Claude analysis on new emails as they're synced
- Identify strategic decisions, client preferences, issues
- Auto-generate suggested additions to CONTEXT.md
- User reviews and approves before committing

**Benefits**:
- Reduces manual CONTEXT.md maintenance
- Ensures no important context is missed
- Works in background as emails arrive

**References**: `shared/scripts/README.md` - Future Enhancements section

---

### Support for Adding to Specific Subsections in add-context-note
**Status**: Idea
**Effort**: Low
**Value**: Low-Medium

Enhance add-context-note.sh to support adding notes to specific subsections within main sections.

**Example**:
- Strategic Context → Current Strategy (subsection)
- Business Context → Product/Service Details → Pricing (sub-subsection)

**Approach**:
- Parse CONTEXT.md structure to show subsection menu
- Allow hierarchical navigation
- Insert note at correct indentation level

**References**: `shared/scripts/README.md` - Future Enhancements section

---

## Low Priority / Nice to Have

Ideas that would be convenient but aren't critical.

### Tag System for Categorizing Notes
**Status**: Idea
**Effort**: Medium
**Value**: Low

Add tagging to notes in CONTEXT.md for better organization and searchability.

**Approach**:
- YAML frontmatter tags or inline #hashtags
- Search script to find all notes with specific tags
- Examples: #pricing, #strategy, #technical-issue, #experiment

**References**: `shared/scripts/README.md` - Future Enhancements section

---

### Search/Filter Notes by Date or Keyword
**Status**: Idea
**Effort**: Low-Medium
**Value**: Low-Medium

Command-line tool to search across all CONTEXT.md files.

**Features**:
- Search by keyword across all clients
- Filter by date range
- Filter by section type
- Output matching notes with context

**Example**:
```bash
./shared/scripts/search-context.sh "stock issues" --last-30-days
./shared/scripts/search-context.sh "ROAS" --client=tree2mydoor
```

**References**: `shared/scripts/README.md` - Future Enhancements section

---

### Bulk Note Import from Text File
**Status**: Idea
**Effort**: Low
**Value**: Low

Import multiple notes at once from a structured text file.

**Use Case**:
- After a long meeting, user has 10 notes to add
- Write all notes in one file with markers
- Script parses and distributes to correct CONTEXT.md sections

**References**: `shared/scripts/README.md` - Future Enhancements section

---

## How to Use This Document

### Adding New Ideas

Add to appropriate priority section with this format:

```markdown
### [Feature Name]
**Status**: Idea | Documented | In Progress | Blocked
**Effort**: Low | Medium | High
**Value**: Low | Medium | High

[Description of what it does and why it's useful]

**Benefits**: (optional)
- Bullet points

**Implementation Requirements**: (optional)
- What's needed

**Approach**: (optional)
- How it could work

**References**: [where the idea came from or related docs]
```

### Moving to Implementation

When ready to implement:
1. Change status to "In Progress"
2. Create a branch if needed
3. When complete, move to "Completed" section below or remove entirely

### Completed Section

Keep track of what was implemented (date added below completion).

---

## Completed Enhancements

*(Empty - will be populated as features are implemented)*

---

## References

- `shared/scripts/README.md` - Script-specific future ideas
- `CLAUDE.md` - System architecture and workflows
- Client CONTEXT.md files - Client-specific enhancement ideas

---

**Maintained By**: Pete's Brain System
**Review Frequency**: Quarterly or as needed
