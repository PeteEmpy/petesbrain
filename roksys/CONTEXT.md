# Rok Systems (Roksys) - Context & Strategic Notes

> **Purpose**: Living document with strategic context about Rok Systems' business, operations, and direction.
> **Last Updated**: 2025-11-12

---

## Company Overview

**Company Name**: Rok Systems (commonly referred to as "Roksys")
**Website**: https://roksys.co.uk
**Tagline**: Digital Marketing
**Founded**: Operating for 22+ years in digital marketing
**Google Ads Manager Account**: 2569949686

**Core Business**: Digital marketing and advertising agency specializing in:
- PPC Management (Google Ads)
- Google Shopping & Performance Max campaigns
- Google Analytics (GA4)
- E-commerce marketing strategy
- Data-driven campaign optimization

**Brand Identity**:
- **Roksys Green**: #6CC24A
- **Roksys Gray**: #808080
- Brand assets stored in: `/shared/assets/branding/`

---

## Strategic Context

### Current Strategic Direction (2025)

**Primary Focus**: Building a "Self-Improving Agency" powered by AI and automation

**Key Initiatives**:

1. **Pete's Brain System** - Central AI-powered operations platform
   - Claude Code integration for automated workflows
   - Centralized client knowledge management (CONTEXT.md files)
   - Automated email sync and categorization
   - Meeting transcript integration (Granola)
   - Google Tasks lifecycle tracking
   - Knowledge base system for best practices

2. **Tool Development** - Building proprietary marketing tools
   - Google Ads Text Generator (production-ready)
   - Granola Meeting Importer (production-ready)
   - Report Generator (prototype stage)
   - Product Impact Analyzer (early development)

3. **Knowledge Base & Learning System**
   - Automated industry news monitoring (Google Ads, AI)
   - Weekly AI newsletter summarization
   - Google Rep email tracking and extraction
   - Continuous learning from experiments and client work

4. **MCP (Model Context Protocol) Integrations**
   - Google Ads API access
   - Google Analytics (GA4) API access
   - Google Sheets automation
   - Google Tasks workflow integration
   - Google Drive document import system

### Business Philosophy

**"Self-Building Agency"**:
- System learns and grows continuously
- Context preservation crucial for business value
- All client history, experiments, strategy changes tracked
- Enables sophisticated AI-powered analysis
- Automation reduces manual work, increases capacity

**Cost Structure**:
- Cursor IDE: $20/month
- Claude Max Plan: $80/month
- Replacing Go Marble: Currently $59/month, increasing to $299 (partial replacement)

**Competitive Advantages**:
- Deep AI integration (ahead of most agencies)
- Proprietary tooling (Google Ads Generator, etc.)
- Comprehensive context preservation system
- Years of PPC experience combined with cutting-edge AI
- Automated workflows that scale without additional headcount

---

## Client Portfolio

**Active Clients** (as of October 2025):

1. **Accessories for the Home** - Home decor e-commerce
2. **Bright Minds** - Education/learning
3. **Clear Prospects** - [Business type TBD]
4. **Devonshire Hotels** - Hospitality
5. **Godshot** - Coffee/specialty products
6. **National Design Academy** - Education, lead generation
7. **OTC** - [Business type TBD]
8. **Print My PDF** - Printing services
9. **Smythson** - Luxury stationery and leather goods (high-budget client)
10. **Superspace** - [Business type TBD]
11. **Tree2mydoor** (T2MD) - Trees and plants e-commerce
12. **Uno Lighting** - Lighting products

**Client Workflow**:
- Each client has dedicated folder in `clients/[client-name]/`
- CONTEXT.md file tracks strategy, history, learnings
- tasks-completed.md tracks completed work
- Automated email sync to client folders
- Meeting notes auto-imported via Granola
- Experiment tracking via Google Sheets CSV exports

---

## Internal Processes & Workflows

### Automated Workflows

**Email Sync System**:
- Gmail integration via Google Cloud MCP connectors
- Automated email processing and client assignment
- Emails saved as markdown with YAML frontmatter
- Location: `clients/[client-name]/emails/`

**Meeting Notes Processing**:
- Granola AI integration for automatic meeting transcription
- Two-stage client detection (title + content analysis)
- Saves AI notes + full transcript
- Runs every 5 minutes checking for new meetings
- Location: `clients/[client-name]/meeting-notes/` or `roksys/meeting-notes/`

**Google Tasks Tracking** (NEW - October 2025):
- Polls Google Tasks API every 6 hours
- Auto-detects client from task list/title/notes
- **Task Creation**: Adds substantial tasks (>50 char notes) to CONTEXT.md "Planned Work"
- **Task Completion**: Moves to "Completed Work" + logs to tasks-completed.md
- Integrates with weekly review email
- Location: `clients/[client-name]/CONTEXT.md` and `tasks-completed.md`

**Weekly Meeting Review Email**:
- Scans past week's meetings across all clients
- Scans completed tasks from Google Tasks
- Claude API analyzes meetings for key decisions, action items, insights
- Generates structured summary email
- Sent via Gmail API every Monday 9 AM
- Script: `shared/scripts/weekly-meeting-review.py`

**Knowledge Base Processing**:
- Inbox system for dropping unprocessed content
- Automated processing every 6 hours
- Claude API categorizes and formats content
- Saves to appropriate category folders
- Location: `roksys/knowledge-base/`

**Industry News Monitoring** (October 2025):
- Monitors 9 Google Ads industry RSS feeds every 6 hours
- AI scores articles for relevance (0-10)
- Imports articles scoring 6+ to knowledge base
- Monitors 12 AI news sources (Marketing AI, OpenAI, Google AI, etc.)
- Scripts: `shared/scripts/industry-news-monitor.py`, `ai-news-monitor.py`

**Knowledge Base Weekly Summary Email**:
- Reviews past week's knowledge base additions
- Includes automated industry/AI news monitoring results
- **NEW (Nov 2025)**: Includes blog post publishing instructions when blog post is created
- Shows blog post title, ID, scheduled date, and direct edit link
- Claude API generates comprehensive summary
- Sent via Gmail API every Monday 8:00 AM (updated from 8:30 AM)
- Script: `agents/reporting/kb-weekly-summary.py`

**WordPress Blog Automation** (November 2025):
- Automated weekly blog post generation from knowledge base articles
- Pulls top 5-7 Google Ads articles from past 7 days
- Uses Claude API to write posts in Peter's tone of voice
- Auto-publishes to WordPress every Monday 9 AM (scheduled)
- Category: "Google Ads Weekly"
- Tags: "Google Ads", "PPC", "Industry News", "Paid Search"
- Runs every Monday 7:30 AM (before KB summary)
- Script: `agents/weekly-blog-generator/weekly-blog-generator.py`
- LaunchAgent: `com.petesbrain.weekly-blog-generator`
- Blog navigation: Blog page created (ID: 507), category archive at `/category/google-ads-weekly/`
- Helper scripts: `publish-blog-post-now.py`, `remove-text-from-post.py`, `wordpress-blog-navigation-setup.py`
- Update functionality: `--update` flag to regenerate and update existing posts
- Skill: `.claude/skills/blog-article-generator/` - Claude skill for blog generation

**Blog Content Approach** (Updated November 9, 2025):
- **Target Audience**: Existing or future Rok Systems customers (e-commerce business owners)
- **Content Focus**: Translate technical Google Ads information into real-world business impact
- **Writing Style**: Natural, conversational, business-focused
- **Key Principle**: Customers view things from profitability/business outcome angle, but translate that naturally - don't force "profitability" language into every article
- **Structure**: Explain what's happening in Google Ads → Translate to what it means for their business → What it means going forward
- **Tone**: First-person, conversational, "you get me" approach from website
- **Flow**: Regular weekly articles with continuity

**Sunday Night Knowledge Base Update Sequence** (November 2025):
- Runs every Sunday at 11:00 PM to ensure KB is fully updated before Monday blog generation
- Sequence: KB processor → Industry news monitor → AI news monitor → KB processor (final)
- Ensures fresh content available for Monday morning blog post
- LaunchAgent: `com.petesbrain.sunday-kb-update`

**Google Sheets Automation**:
- ROK Experiments sheet exported to CSV every 6 hours
- Location: `roksys/spreadsheets/rok-experiments-client-notes.csv`
- Script: `shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`

### Manual Workflows

**Client Analysis Process**:
1. Read CONTEXT.md (primary knowledge base)
2. Read tasks-completed.md (what work has been done)
3. Read experiment notes from CSV
4. Check recent emails (last 30-60 days)
5. Review meeting notes (last 30-60 days)
6. Check all other client folders (documents, briefs, spreadsheets, etc.)
7. Analyze external factors (market, client business, technical issues)
8. **UPDATE CONTEXT.md** with new insights (mandatory)

**Root Cause Analysis Framework**:
- Categorize performance changes into:
  - ✅ Your Actions (account management, budget changes, campaign launches)
  - 🌍 External Factors (seasonality, competitors, market trends)
  - 🏢 Client Business Changes (stock issues, pricing, website changes)
  - ⚙️ Technical Issues (tracking, website performance, platform bugs)

**Cross-Reference Data Sources**:
- Google Analytics (via MCP) - website-level trends
- Client Website (via WebFetch) - product availability, pricing
- Historical Google Ads Data - seasonality, patterns
- Client llms.txt/agents.txt - business model, products
- Completed Tasks - recent work and status updates

---

## Tools & Technologies

### Production Tools

**Google Ads Text Generator**:
- Location: `tools/google-ads-generator/`
- Purpose: Generate optimized ad copy (headlines & descriptions)
- Tech Stack: Flask, Claude API, PyWebView
- Features:
  - 5 content categories (Benefits, Technical, Quirky, CTA, Brand)
  - ROK-optimized character limits (Headlines 25-30, Descriptions 70-90)
  - CSV/Clipboard export for Google Ads Editor
  - Web app (http://localhost:5001) and desktop app versions
- Status: Production-ready, actively used

**Granola Meeting Importer**:
- Location: `tools/granola-importer/`
- Purpose: Auto-import meeting transcripts from Granola AI
- Tech Stack: Python, Granola API
- Features:
  - Background daemon (checks every 5 minutes)
  - Two-stage client detection
  - Exports markdown with YAML frontmatter
  - Saves AI notes + full transcript
- Status: Production-ready, running continuously

### Development Tools

**Report Generator**:
- Location: `tools/report-generator/`
- Purpose: Generate professional, interactive reports with data visualizations
- Tech Stack: Flask, Chart.js, WeasyPrint (PDF)
- Features (Built):
  - Interactive Chart.js visualizations
  - Q4 Strategy Report template (fully functional)
  - Multiple report types scaffolded
  - Export to HTML/JSON
  - Client auto-discovery
- Status: Prototype - needs MCP integration, additional templates, PDF export
- Priority: High value, medium effort remaining

**Product Impact Analyzer**:
- Location: `tools/product-impact-analyzer/`
- Purpose: Analyze impact of product changes on Google Ads performance
- Status: Early development

### Core Technologies

**Development Environment**:
- Cursor IDE ($20/month) - AI-powered code editor
- Claude Code - Terminal integration for Claude
- Python 3.13 - Primary language
- Flask - Web framework
- PyWebView - Desktop app wrapper

**AI & APIs**:
- Claude API (Anthropic) - $80/month Max plan
  - Primary for ad copy generation
  - Analysis and summarization
  - Knowledge base processing
- MCP (Model Context Protocol) - API integrations
  - Google Ads
  - Google Analytics (GA4)
  - Google Sheets
  - Google Tasks
  - Google Drive (configured, awaiting OAuth)

**Infrastructure**:
- macOS LaunchAgents - Scheduled automation
- Git - Version control
- Google Cloud Platform - API credentials
- Gmail API - Email automation

---

## Company Goals & Direction

### Short-Term Goals (Q4 2025 - Q1 2026)

1. **Complete Report Generator Tool**
   - Add live Google Ads/Analytics MCP integration
   - Build out additional report templates
   - Implement PDF export functionality
   - Enable automated scheduled reports

2. **Refine AI Workflows**
   - Optimize automated email insights extraction
   - Improve client assignment accuracy in meeting notes
   - Enhance knowledge base categorization
   - Calendar integration for meeting validation

3. **Scale Client Portfolio**
   - Leverage automation to handle more clients without adding headcount
   - Use AI tools to maintain service quality at scale
   - Prove ROI of Pete's Brain system with existing clients

### Medium-Term Vision (2026)

**"The Self-Improving Agency"**:
- AI system that learns continuously from every client interaction
- Context preservation becomes the core business asset
- Sophisticated analysis capabilities exceed human-only agencies
- Proprietary tools provide competitive moat
- Automation enables significant capacity expansion

**Business Model Evolution**:
- More clients, same team size (or solo operation)
- Premium pricing justified by AI-enhanced insights
- Faster turnaround times via automation
- Higher quality strategic advice via knowledge base

### Long-Term Vision

**Exit Strategy**:
- Pete's Brain system (the AI infrastructure) becomes the sellable asset
- Not just client list, but the entire knowledge base and tooling
- "The system is the pension" - as valuable as the client relationships
- Could operate continuously with minimal intervention
- Potential for white-label licensing to other agencies

**Market Positioning**:
- First-mover advantage in AI-native agency operations
- Proprietary tooling gives 2-3 year lead over competitors
- Deep integration of AI throughout all operations
- Reputation as the "AI-powered PPC agency"

---

## Key Learnings & Insights

### What's Working Well (October 2025)

**AI Integration Success**:
- Claude Code system built in one day, immediately productive
- Automated workflows saving 5-10 hours/week
- Context preservation enabling more sophisticated client analysis
- AI-generated ad copy performing as well as manual copy

**Automation Wins**:
- Meeting notes auto-import eliminates manual data entry
- Email sync keeps client folders current automatically
- Industry news monitoring surfaces relevant updates without manual searching
- Weekly summary emails save review time

**Tool Development**:
- Google Ads Generator proven successful with multiple clients
- Report Generator prototype shows promise for client presentations
- MCP integrations provide direct API access without complex auth

### Challenges & Learnings

**AI Learning Curve**:
- "Absolutely buried in AI" - steep but rewarding learning curve
- Many directions possible, requires discipline to focus
- Rabbit holes are tempting but recognizing U-turns is critical
- "500 things all at the same time" - prioritization essential

**Technical Challenges**:
- Google Sheets integration still has limitations in Claude Code
- Some MCP servers (like Google Drive) require complex OAuth setup
- LaunchAgent automation works but needs monitoring/logs
- Client assignment accuracy in auto-imported meetings needs improvement

**Process Insights**:
- Years of PPC experience + AI = powerful combination
- Junior practitioners may struggle without experience foundation
- Context preservation is more valuable than expected
- Automation works best for repeatable tasks, not novel problems

### Industry Trends (2025)

**Google Ads Platform**:
- CPCs increasing across all accounts (significant YoY increase)
- Performance Max campaigns pushed by Google as "easy" entry point
- Competition intensifying (Temu, Amazon, more advertisers)
- AI Max on search campaigns expanding reach and overlap
- Impression shares harder to achieve, more expensive

**AI in Marketing**:
- LLMs.txt and agents.txt becoming critical for AI discoverability
- ChatGPT moving into Google's space with Atlas browser
- Shopping features coming to AI chat interfaces (game changer)
- Agencies need to be ready for AI-driven commerce channels

**Competitive Landscape**:
- Most agencies still manual, not AI-integrated
- 2-3 year advantage window for AI-native agencies
- Tools like Go Marble offering automation but at high cost ($299/month)
- Opportunity to build proprietary tools and sell/license later

---

## Key Relationships & Resources

### Google Representatives

**Recent Interactions** (last 12 months):
- National Design Academy: Solomiya K. (solomiyak@google.com), Technical Solutions team
- Smythson: Devin Ferreira (devinferreira@google.com) - Conversion tracking support
- Print My PDF: Brahmendra (brahmendra@google.com)
- National Design Academy: Ally Hamps (allyhamps@google.com), Patrick White (patrickwhite@google.com)

**Google Rep Email Tracking**:
- Automated report generation: `roksys/google-rep-emails-report.md`
- Tracks all Google rep communications across clients
- Updated automatically

### Industry Information Sources

**Automated Monitoring** (RSS feeds):
- Search Engine Land (Google Ads & PPC)
- Search Engine Journal (PPC)
- Google Ads Blog (Official)
- Think with Google
- WordStream Blog
- PPC Hero
- Neil Patel Blog
- Unbounce Blog

**AI News Sources**:
- Marketing AI Institute
- MarTech
- Adweek
- OpenAI Blog
- Google AI Blog
- Microsoft AI Blog
- Anthropic News
- MIT Technology Review
- VentureBeat

### Professional Network

**Mike Rhodes** (October 2025):
- 30-minute setup consultation for Claude Code
- Shared "Brain" system architecture insights
- Provided guidance on MCP setup, Cursor workflow
- Recommended Claude Max plan over API for cost control
- Suggested focus on Commands over Skills for control

---

## Internal Operations

### File & Folder Structure

**Project Root**: `/Users/administrator/Documents/PetesBrain/`

**Key Directories**:
- `clients/` - All client work and context
- `roksys/` - Rok Systems internal business (this folder)
- `tools/` - Proprietary tool development
- `shared/` - Shared resources and scripts
- `docs/` - Project documentation

**This Folder** (`roksys/`):
- `CONTEXT.md` - This file (company context)
- `README.md` - High-level overview
- `tasks-completed.md` - Completed internal tasks
- `emails/` - Business correspondence
- `meeting-notes/` - Internal/company meetings
- `knowledge-base/` - Curated reference materials
- `spreadsheets/` - Business data, experiment tracking
- `documents/` - Business documents, contracts, policies

### Experiment Tracking

**System**: Google Sheets → CSV export every 6 hours
**Sheet**: [ROK | Experiments](https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/)
**Export Location**: `roksys/spreadsheets/rok-experiments-client-notes.csv`

**Tracks**:
- Client-specific experiments and tests
- Strategy changes and their rationale
- Performance impacts of changes
- Learning from successes and failures

### Financial Runway Calculator

**System**: Google Sheets cash flow projection through semi-retirement (October 2027)
**Sheet**: [Roksys Forecast](https://docs.google.com/spreadsheets/d/1XK0k528vaqtN0Qmg15iqzv5TLGv0UwlSaUV5W_Gyf1A/edit?gid=0#gid=0)

**Purpose**: Track cash position and runway to semi-retirement

**Structure**:
- **Forecast Sheet**: Monthly cash flow projection (Jan 2025 - Oct 2027)
- **Inc Sheet**: Client retainer income breakdown by month
- **Expenditure Sheet**: (minimal, expenditure tracked in Forecast)

**Key Dates**:
- **October 2027**: Semi-retirement date (scaling back operations)
- **November 2027**: Dividends reduce from £4,000 to £1,000/month

**Projections Include**:
- Monthly client income (updated as clients won/lost)
- Fixed expenses (car, pension, insurance, other)
- Salary and dividends
- PAYE quarterly payments (January & July: £6,500)
- Corporation tax payments (February each year: conservative £20k estimates)

**Current Position** (as of Nov 2025):
- Starting balance: £51,000 (Jan 2025)
- Monthly income: £9,450 (Feb 2026 onwards)
- Projected balance at semi-retirement (Oct 2027): £54,594
- Post semi-retirement cash flow: +£3,880/month surplus

**Usage**:
- Update Inc sheet when clients change
- Share spreadsheet URL with Claude Code for updated runway analysis
- No automation needed - manual updates as business changes

### Knowledge Base System

**Location**: `roksys/knowledge-base/`

**Purpose**:
- Authoritative reference for Google Ads best practices
- Platform updates and announcements
- AI strategy guidance
- ROK methodologies and frameworks

**Categories**:
- `google-ads/` - Platform guidance (PMax, Shopping, Search, Bidding, Updates)
- `ai-strategy/` - AI in marketing and advertising
- `analytics/` - GA4, attribution, tracking
- `industry-insights/` - Market trends, competitive intel
- `rok-methodologies/` - ROK's proprietary frameworks

**Automated Processes**:
- Inbox processing every 6 hours
- Industry news monitoring (9 sources) every 6 hours
- AI news monitoring (12 sources) every 6 hours
- Weekly summary email every Monday 9 AM

### WordPress Site Management

**Site Information**:
- **URL**: https://roksys.co.uk
- **Admin URL**: https://roksys.co.uk/wp-admin
- **Platform**: WordPress with Elementor page builder
- **Theme**: Elementor-based theme

**Access Credentials**:
- **Username**: Peter
- **Application Password**: Configured in LaunchAgent environment variables
- **Application Password Name**: "Weekly Blog Generator"
- **Password Location**: `~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist`
- **Note**: Application password stored in LaunchAgent plist file (check environment variables section)

**Blog System**:
- **Category**: "Google Ads Weekly" (ID: 5)
- **Category Archive**: https://roksys.co.uk/category/google-ads-weekly/
- **Blog Page**: "Google Ads Blog" (ID: 507)
- **Blog Page URL**: https://roksys.co.uk/google-ads-blog/
- **Auto-Publish**: Every Monday 9:00 AM (scheduled)
- **Generator Schedule**: Every Monday 7:30 AM
- **Sunday KB Update**: Sunday 11:00 PM (ensures fresh content for blog)

**Navigation**:
- Blog navigation managed via Elementor Header Builder
- Menu item must be added manually in Elementor (not standard WordPress menu)
- Blog archive link: https://roksys.co.uk/category/google-ads-weekly/
- **Setup Guide**: `agents/content-sync/BLOG-NAVIGATION-SETUP.md`

**Helper Scripts**:
- `agents/weekly-blog-generator/weekly-blog-generator.py` - Auto-generates weekly posts
- `agents/content-sync/publish-blog-post-now.py` - Publish scheduled posts immediately
- `agents/content-sync/remove-text-from-post.py` - Remove text from posts
- `agents/content-sync/wordpress-blog-navigation-setup.py` - Set up navigation

**Documentation**:
- `agents/content-sync/WORDPRESS-SETUP.md` - Setup and configuration
- `agents/content-sync/WORDPRESS-TROUBLESHOOTING.md` - Common issues and fixes
- `agents/content-sync/BLOG-NAVIGATION-SETUP.md` - Navigation setup guide (Elementor)
- `agents/content-sync/WEEKLY-BLOG-GENERATOR-README.md` - Full blog generator documentation

**Quick Access**:
- **Admin Login**: https://roksys.co.uk/wp-admin
- **Blog Archive**: https://roksys.co.uk/category/google-ads-weekly/
- **Edit Post**: https://roksys.co.uk/wp-admin/post.php?post=[ID]&action=edit
- **Application Password**: Check LaunchAgent plist: `~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist`

---

## Quick Reference

### Important Links

**Google Ads Manager**: 2569949686
**Website**: https://roksys.co.uk
**Experiment Tracking Sheet**: https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/
**Annual Income Tracker (Spending Runway)**: https://docs.google.com/spreadsheets/d/1XK0k528vaqtN0Qmg15iqzv5TLGv0UwlSaUV5W_Gyf1A/ (sheet: "inc")
  - Monthly revenue by client for revenue vs time allocation analysis
  - Updated regularly, used for resource planning and client prioritization

### Key Scripts & Commands

**Email Review**:
```bash
cat roksys/google-rep-emails-report.md
```

**Run Manual Weekly Review**:
```bash
GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
  shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

**Run Manual Knowledge Base Processing**:
```bash
python3 shared/scripts/knowledge-base-processor.py
```

**Check Industry News Monitor**:
```bash
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/industry-news-monitor.py
```

**Run Google Ads Generator**:
```bash
cd tools/google-ads-generator
export ANTHROPIC_API_KEY='your-key'
./start.sh  # Web app on http://localhost:5001
```

**Check LaunchAgent Status**:
```bash
launchctl list | grep petesbrain
```

### Log Locations

- Weekly Meeting Review: `~/.petesbrain-weekly-review.log`
- Knowledge Base Processing: `~/.petesbrain-knowledge-base.log`
- Industry News Monitor: `~/.petesbrain-industry-news.log`
- AI News Monitor: `~/.petesbrain-ai-news.log`
- Google Tasks Monitor: `~/.petesbrain-tasks-monitor.log`
- Google Sheets Export: `~/.petesbrain-googlesheets-export.log`

---

## Document History

| Date | Change Made | Updated By |
|------|-------------|------------|
| 2025-10-30 | Initial creation - comprehensive company context | Claude Code |
| 2025-11-08 | Added WordPress site management section, WordPress blog automation, updated schedules | Claude Code |
| 2025-11-12 | Added Annual Income Tracker (Spending Runway) spreadsheet reference for revenue analysis | Claude Code |

## Planned Work

### Check Anthropic API Credits Balance
<!-- task_id: VmVub3c0WWhHQVB0UGpULQ -->
**Status:** 📋 In Progress  

📊 API CREDITS MONITORING TEST

**Current Balance (Oct 30, 2025):** $21.13

**Why Checking:**
You enabled "MAX Only" models in Cursor (Sonnet 4 1M, Opus 4.1) on Oct 30, 2025. We need to verify if these models consume your API credits or if they're included in your Claude Max subscription (£90/month).

**What to Check:**
1. Go to: https://console.anthropic.com/settings/billing
2. Check current credit balance
3. Compare to $21.13 baseline

**Expected Results:**
✅ Balance ~$21.13 = MAX models use your subscription (keep using them!)
❌ Balance significantly lower = MAX models drain API credits (disable them!)

---

### Order self-adhesive pads for dash cam
<!-- task_id: UU9QVUp0V3B4WmJTU1JVMA -->
**Status:** 📋 In Progress  

Personal task: Order self-adhesive pads and install them on the dash cam mount.



### Review AI Subscriptions - Nov 17
<!-- task_id: WFNkdWhDaGVTbV9wa2VKWA -->
**Status:** 📋 In Progress  

Review after 2 weeks of Cursor Pro Plus upgrade.

Full analysis: roksys/documents/ai-subscriptions-analysis-nov-2025.md

Current: Claude Max £90 + Cursor £32 + ChatGPT £16 = £138/month

Check: Cursor limits? Claude API balance? ChatGPT usage?



### TEST: Verify task creation goes to Peter's List
<!-- task_id: UzE3NmU1eGdNQUtGQzJNRQ -->
**Status:** 📋 In Progress  

This is a test task to verify it's created in the correct list


### 5 Nov 2025 At 16:44 Quick Note
<!-- task_id: U0J6NE5BS0JGLUh0cV9zag -->
**Status:** 📋 In Progress  

Roksys starling and tide bank statements for 1st jun 2024 to 31st may 2025. To be done on the 6th November


### Roksys Bank Statements
<!-- task_id: OXJjbTVaT3VBbWtKS2tCYw -->
**Status:** 📋 In Progress  

# 5 Nov 2025 At 16:44 Quick Note

**Created:** 2025-11-05 16:45  
**Source:** 5 Nov 2025 at 16:44-quick-note.txt


### Optimize Google Ads Daily Summary Alert Timing
<!-- task_id: LUNyQ29LakUyUFVTcm5BMw -->
**Status:** 📋 In Progress  

due: within 1 week
client: Rock Systems
Adjust daily summary email timing to ensure accurate reporting:
1. Confirm Google Ads data typically becomes available 24 hours after the reporting day
2. Reschedule daily summary email to 4:00 PM to capture complete data
3. Verify data accuracy after time adjustment
4. Update alert system configuration


### Generate LinkedIn CV for Twine
<!-- task_id: VTlLaVNTVndTMkd3X3VwRQ -->
**Status:** 📋 In Progress  

client: Rok Systems
Extract and compile a professional CV for Rok Systems using their LinkedIn profile data, preparing it for Twine platform integration


### Enhanced 20251106 192439 Wispr Rok Systems Create Cv From Linkedin Profile For Tw
<!-- task_id: Zkp1RkpPMjdVRUlySkRQeQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251106-192439-wispr-rok systems create cv from linkedin profile for tw.md
**Type:** task
**Client:** Rok Systems
**Priority:** medium
**Processed:** 2025-11-07 08:25
---
task: Generate LinkedIn CV for Twine
client: Rok Systems
Extract and compile a professional CV for Rok Systems using their LinkedIn profile data, preparing it for Twine platform integration
---
**Context Summary:** Rok Systems needs a CV generated from their LinkedIn profile to be used in Twine platform integration.
---
**Original Note:**
# Wispr Flow Note
Rok Systems create CV from LinkedIn profile for Twine.
---
*Source: Wispr Flow*
*Created: 2025-11-06 19:24:39.794 +00:00*
*Note ID: 0728c977-a44d-4d5d-9af9-c4a9164dc1b4*


### Roksys Bank Statements
<!-- task_id: OXJjbTVaT3VBbWtKS2tCYw -->
**Status:** 📋 In Progress  

# 5 Nov 2025 At 16:44 Quick Note

**Created:** 2025-11-05 16:45  
**Source:** 5 Nov 2025 at 16:44-quick-note.txt


### Optimize Google Ads Daily Summary Alert Timing
<!-- task_id: LUNyQ29LakUyUFVTcm5BMw -->
**Status:** 📋 In Progress  

due: within 1 week
client: Rock Systems
Adjust daily summary email timing to ensure accurate reporting:
1. Confirm Google Ads data typically becomes available 24 hours after the reporting day
2. Reschedule daily summary email to 4:00 PM to capture complete data
3. Verify data accuracy after time adjustment
4. Update alert system configuration


### Generate LinkedIn CV for Twine
<!-- task_id: VTlLaVNTVndTMkd3X3VwRQ -->
**Status:** 📋 In Progress  

client: Rok Systems
Extract and compile a professional CV for Rok Systems using their LinkedIn profile data, preparing it for Twine platform integration


### Enhanced 20251106 192439 Wispr Rok Systems Create Cv From Linkedin Profile For Tw
<!-- task_id: Zkp1RkpPMjdVRUlySkRQeQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251106-192439-wispr-rok systems create cv from linkedin profile for tw.md
**Type:** task
**Client:** Rok Systems
**Priority:** medium
**Processed:** 2025-11-07 08:25
---
task: Generate LinkedIn CV for Twine
client: Rok Systems
Extract and compile a professional CV for Rok Systems using their LinkedIn profile data, preparing it for Twine platform integration
---
**Context Summary:** Rok Systems needs a CV generated from their LinkedIn profile to be used in Twine platform integration.
---
**Original Note:**
# Wispr Flow Note
Rok Systems create CV from LinkedIn profile for Twine.
---
*Source: Wispr Flow*
*Created: 2025-11-06 19:24:39.794 +00:00*
*Note ID: 0728c977-a44d-4d5d-9af9-c4a9164dc1b4*


### TEST: Verify task creation goes to Peter's List
<!-- task_id: UzE3NmU1eGdNQUtGQzJNRQ -->
**Status:** 📋 In Progress  

This is a test task to verify it's created in the correct list


### 5 Nov 2025 At 16:44 Quick Note
<!-- task_id: U0J6NE5BS0JGLUh0cV9zag -->
**Status:** 📋 In Progress  

Roksys starling and tide bank statements for 1st jun 2024 to 31st may 2025. To be done on the 6th November


### Enhanced 20251031 173727 Google Chat 19A3Cd90
<!-- task_id: QWdWRnBtWGZhd3VBb3J1Xw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251031-173727-google-chat-19a3cd90.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 10:32

# Google Chat Message (via Gmail)

**Space:** Collaber PPC Chat
**From:** Gareth Mitchell <gareth@collaber.co.uk>
**Time:** 2025-10-31 17:37:27
**Email ID:** 19a3cd90a7ddd6a8

---

Peter Empson

Peter Empson



@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for this.  
But I finally managed to get some instructions. Please take a look at the

---

**Source:** Google Chat (via Gmail notification)
**Space:** Collaber PPC Chat



---

**Original Note:**
# Google Chat Message (via Gmail)

**Space:** Collaber PPC Chat
**From:** Gareth Mitchell <gareth@collaber.co.uk>
**Time:** 2025-10-31 17:37:27
**Email ID:** 19a3cd90a7ddd6a8

---

Peter Empson

Peter Empson



@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for this.  
But I finally managed to get some instructions. Please take a look at the

---

**Source:** Google Chat (via Gmail notification)
**Space:** Collaber PPC Chat


### Enhanced 20251105 225227 Whatsapp 19A57824
<!-- task_id: MmNUWDRhZmRRNnhsT0Rkbg -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251105-225227-whatsapp-19a57824.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 10:32

# WhatsApp Message (via Email)

**From:** As [shared](https
**Time:** 2025-11-05 22:52:27
**Email ID:** 19a57824b39813ca

---

//blog.whatsapp.com/making-it-easier-to-add-and-manage-contacts?content_id=PpLv99jNFYUuIoG) last year, we are excited that WhatsApp will soon support one of our most requested features – the ability to adopt a username. This has strong benefits for people and businesses alike: usernames offer people a simple way to further protect their privacy by displaying their username rather than their phone number when messaging with others in 1:1 conversations and in groups. When available next year, this optional feature will give people more control over how they share their contact information. For businesses, usernames will allow you to easily build your brand presence on WhatsApp based on your name rather than your phone number, making it easier for customers to connect with

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** As [shared](https



---

**Original Note:**
# WhatsApp Message (via Email)

**From:** As [shared](https
**Time:** 2025-11-05 22:52:27
**Email ID:** 19a57824b39813ca

---

//blog.whatsapp.com/making-it-easier-to-add-and-manage-contacts?content_id=PpLv99jNFYUuIoG) last year, we are excited that WhatsApp will soon support one of our most requested features – the ability to adopt a username. This has strong benefits for people and businesses alike: usernames offer people a simple way to further protect their privacy by displaying their username rather than their phone number when messaging with others in 1:1 conversations and in groups. When available next year, this optional feature will give people more control over how they share their contact information. For businesses, usernames will allow you to easily build your brand presence on WhatsApp based on your name rather than your phone number, making it easier for customers to connect with

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** As [shared](https


### Enhanced 20251109 081911 Wispr Go Clean  This Seems To Be A Drop Off In Profitabi
<!-- task_id: Vm1ESjJscFoxTmQ4YUhHTA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-081911-wispr-go clean- this seems to be a drop-off in profitabi.md
**Type:** completion
**Client:** None
**Priority:** high
**Urgency:** normal
**Estimated Time:** 2-3 hours
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 09:41

**Dependencies/Blockers:**
- Financial reports
- Previous month's performance data

**Related Tasks:**
- Monthly Financial Review
- Quarterly Profitability Analysis

**COMPLETION NOTE** - Route to documents folder

Perform a comprehensive audit of November financial performance to understand the drop in profitability. Steps include:
1. Analyze revenue streams
2. Identify potential causes for revenue decline
3. Develop strategic recommendations to mitigate profitability issues
4. Create action plan for addressing identified challenges

---

**Context Summary:** Identified potential profitability challenges in November requiring strategic review and improvement planning.

---

**Original Note:**
# Wispr Flow Note

Go clean! This seems to be a drop-off in profitability in November. I need to do an audit and then make suggestions on what can be done to improve the profitability in these leaner months

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:19:11.126 +00:00*
*Note ID: 86175072-ada4-4b9c-9aba-c345b1b0775f*



### Enhanced 20251023 140030 Whatsapp 19A115F3
<!-- task_id: Nm5pMno2OWtMdmVHek9WQQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251023-140030-whatsapp-19a115f3.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 10:32

# WhatsApp Message (via Email)

**From:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline
**Time:** 2025-10-23 14:00:30
**Email ID:** 19a115f3775046a4

---

none;

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline



---

**Original Note:**
# WhatsApp Message (via Email)

**From:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline
**Time:** 2025-10-23 14:00:30
**Email ID:** 19a115f3775046a4

---

none;

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline


### Enhanced 20251109 145926 Wispr Send Details To Stag Park  Our Bank Account  And R
<!-- task_id: YkR5QXlrNGhGc0FGc25Naw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-145926-wispr-send details to stag park- our bank account- and r.md
**Type:** task
**Client:** None
**Priority:** medium
**Urgency:** normal
**Estimated Time:** 45 min
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 16:52

**Dependencies/Blockers:**
- Confirm specific details to send to Stag Park
- Verify bank account information
- Identify what needs to be rebooked

task: Stag Park Details and Rebooking
due: 2025-12-29
time: 45 min

Complete two main actions:
1. Send details to Stag Park (specific details not specified)
2. Rebook an event/reservation for December 29th
3. Update bank account information

---

**Context Summary:** Personal task involving communication with Stag Park and potential rebooking for a future date.

---

**Original Note:**
# Wispr Flow Note

Send details to Stag Park, our bank account, and rebook somewhere else for the 29th of December.This is a personal note.

---
*Source: Wispr Flow*
*Created: 2025-11-09 14:59:26.546 +00:00*
*Note ID: 6982aa92-4863-4988-bdf8-83308496f8fe*


### Enhanced 20251109 080415 Wispr The Laptop Sync Isn T Working For Roxys So I Need
<!-- task_id: UGtsWWVyNTBnM1lFRzljVA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-080415-wispr-the laptop sync isn-t working for roxys so i need.md
**Type:** completion
**Client:** ROXYS
**Priority:** high
**Urgency:** urgent
**Estimated Time:** 2 hours
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 09:41

**Dependencies/Blockers:**
- Verify laptop connection
- Check sync command syntax
- Test system compatibility

**Related Tasks:**
- ROXYS System Integration
- Laptop Connectivity Audit

client: ROXYS

**COMPLETION NOTE** - Route to documents folder

Diagnose and resolve the sync command issue for the ROXYS laptop system. Investigate why the command is not being recognized or processed correctly when typed on the laptop.

---

**Context Summary:** ROXYS laptop sync system experiencing command recognition issues that require immediate troubleshooting.

---

**Original Note:**
# Wispr Flow Note

The laptop sync isn't working for ROXYS so I need to investigate this. It doesn't see the command when I type it on my laptop. This is fairly urgent and probably needs to be done by close of play on Monday

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:04:15.327 +00:00*
*Note ID: cd1ae496-9d99-4967-b795-61305b1cf8a9*


### Enhanced 20251109 092920 Wispr Change Automatic Blog Creation And Posting So That
<!-- task_id: UFNWczVnQUdyYXBTd29Peg -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-092920-wispr-change automatic blog creation and posting so that.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 09:39

# Wispr Flow Note

Change automatic blog creation and posting so that the article is aimed more at an e-commerce client or potentially e-commerce client for me, rather than at the moment it's aimed at other PPC agencies

---
*Source: Wispr Flow*
*Created: 2025-11-09 09:29:20.390 +00:00*
*Note ID: aea77c97-00aa-40ca-8aac-68ee73039991*



---

**Original Note:**
# Wispr Flow Note

Change automatic blog creation and posting so that the article is aimed more at an e-commerce client or potentially e-commerce client for me, rather than at the moment it's aimed at other PPC agencies

---
*Source: Wispr Flow*
*Created: 2025-11-09 09:29:20.390 +00:00*
*Note ID: aea77c97-00aa-40ca-8aac-68ee73039991*


### [NDA] Review National Motorsports Academy (NMA) performance
<!-- task_id: aV95T00wZ3RFT29ISHJTMg -->
**Status:** 📋 In Progress  

Review Microsoft Ads performance for National Motorsports Academy account. Check campaign structure, spending, conversions, and overall account health.


### [MEDIUM] BMPM - Review Missing Shipping Issues (non-condom products)
<!-- task_id: bkVxa3dYUXlpRXBCVUk1dw -->
**Status:** 📋 In Progress  

**Priority**: MEDIUM
**Products Affected**: Subset of 23 disapproved products (excluding condoms)

**Issue**: Missing shipping configuration on some products

**Note**: BMPM has 23 total disapprovals:
- Condom products (policy violation - EXPECTED, no action)
- Missing shipping (technical issue - NEEDS FIX)
- Sensitive content (expected for some products)

**Action Items**:
1. Access BMPM Merchant Center (ID: 7522326)
2. Filter disapprovals to identify missing shipping issues
3. Exclude condom-related policy violations (expected)
4. Fix shipping configuration for affected products

**Expected Impact**: Restore non-condom products with shipping issues

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md


### [HIGH] Uno Lights - Fix Landing Page Errors (32 products)
<!-- task_id: WVhmamJzdXhTaVBtclR5SA -->
**Status:** 📋 In Progress  

**Priority**: HIGH
**Products Affected**: 32 LED lighting products blocked due to landing page errors

**Issue**: Product URLs returning 404 errors when Google crawls

**Action Items**:
1. Access Uno Lights Merchant Center (ID: 513812383)
2. Export list of 32 disapproved products
3. Test each product URL for 404/500 errors
4. Common fixes:
   - Update URLs in product feed if products moved
   - Fix broken website links/redirects
   - Restore product pages if accidentally deleted
   - Check for URL encoding issues

**Expected Impact**: Restore 32 products to Shopping ads

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md


### [HIGH] BrightMinds - Enable CSS for Free Listings (256 products)
<!-- task_id: SWNiYlhoSEZibmlFNU1NMQ -->
**Status:** 📋 In Progress  

**Priority**: HIGH
**Products Affected**: 256 products not showing in Free Listings (Shopping tab)

**Primary Issue**: CSS not selected for Free Listings destination

**Action Items**:
1. Access BrightMinds Merchant Center (ID: 5291988198)
2. Navigate to: Growth → Manage Programs → Shopping Ads (Free Listings)
3. Select CSS provider (likely Google Shopping CSS)
4. Enable Free Listings destination for products

**Additional Issues to Fix**:
- Custom label formatting (custom_label_2_does_not_have_valid_format)
  - Review custom_label_2 field format requirements
- Landing page errors
  - Identify products with 404/500 errors and fix URLs

**Expected Impact**: Unlock free organic traffic via Shopping tab for 256 products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md


### Enhanced 20251112 194624 Wispr Personal Notes  Book In Lucy S Car For Service
<!-- task_id: RmNTeGFvQ1hCYXRjS1R1aQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251112-194624-wispr-personal notes- book in lucy-s car for service.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-12 21:25

# Wispr Flow Note

Personal notes: Book in Lucy’s car for service.

---
*Source: Wispr Flow*
*Created: 2025-11-12 19:46:24.156 +00:00*
*Note ID: 96868cb8-ff45-49e8-9594-92af721382fb*



---

**Original Note:**
# Wispr Flow Note

Personal notes: Book in Lucy’s car for service.

---
*Source: Wispr Flow*
*Created: 2025-11-12 19:46:24.156 +00:00*
*Note ID: 96868cb8-ff45-49e8-9594-92af721382fb*


### [NDA] Review National Motorsports Academy (NMA) performance
<!-- task_id: aV95T00wZ3RFT29ISHJTMg -->
**Status:** 📋 In Progress  

Review Microsoft Ads performance for National Motorsports Academy account. Check campaign structure, spending, conversions, and overall account health.


### Enhanced 20251109 145926 Wispr Send Details To Stag Park  Our Bank Account  And R
<!-- task_id: YkR5QXlrNGhGc0FGc25Naw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-145926-wispr-send details to stag park- our bank account- and r.md
**Type:** task
**Client:** None
**Priority:** medium
**Urgency:** normal
**Estimated Time:** 45 min
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 16:52

**Dependencies/Blockers:**
- Confirm specific details to send to Stag Park
- Verify bank account information
- Identify what needs to be rebooked

task: Stag Park Details and Rebooking
due: 2025-12-29
time: 45 min

Complete two main actions:
1. Send details to Stag Park (specific details not specified)
2. Rebook an event/reservation for December 29th
3. Update bank account information

---

**Context Summary:** Personal task involving communication with Stag Park and potential rebooking for a future date.

---

**Original Note:**
# Wispr Flow Note

Send details to Stag Park, our bank account, and rebook somewhere else for the 29th of December.This is a personal note.

---
*Source: Wispr Flow*
*Created: 2025-11-09 14:59:26.546 +00:00*
*Note ID: 6982aa92-4863-4988-bdf8-83308496f8fe*


### Enhanced 20251109 081911 Wispr Go Clean  This Seems To Be A Drop Off In Profitabi
<!-- task_id: Vm1ESjJscFoxTmQ4YUhHTA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-081911-wispr-go clean- this seems to be a drop-off in profitabi.md
**Type:** completion
**Client:** None
**Priority:** high
**Urgency:** normal
**Estimated Time:** 2-3 hours
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 09:41

**Dependencies/Blockers:**
- Financial reports
- Previous month's performance data

**Related Tasks:**
- Monthly Financial Review
- Quarterly Profitability Analysis

**COMPLETION NOTE** - Route to documents folder

Perform a comprehensive audit of November financial performance to understand the drop in profitability. Steps include:
1. Analyze revenue streams
2. Identify potential causes for revenue decline
3. Develop strategic recommendations to mitigate profitability issues
4. Create action plan for addressing identified challenges

---

**Context Summary:** Identified potential profitability challenges in November requiring strategic review and improvement planning.

---

**Original Note:**
# Wispr Flow Note

Go clean! This seems to be a drop-off in profitability in November. I need to do an audit and then make suggestions on what can be done to improve the profitability in these leaner months

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:19:11.126 +00:00*
*Note ID: 86175072-ada4-4b9c-9aba-c345b1b0775f*


### Enhanced 20251023 140030 Whatsapp 19A115F3
<!-- task_id: Nm5pMno2OWtMdmVHek9WQQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251023-140030-whatsapp-19a115f3.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 10:32

# WhatsApp Message (via Email)

**From:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline
**Time:** 2025-10-23 14:00:30
**Email ID:** 19a115f3775046a4

---

none;

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline



---

**Original Note:**
# WhatsApp Message (via Email)

**From:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline
**Time:** 2025-10-23 14:00:30
**Email ID:** 19a115f3775046a4

---

none;

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>/*
 * Styles for the rich-text messages content.
 * This files is embedded into email messages we send
 * so all the rules should be written in vanilla css.
 * This file doesn't have any effect on the activities content
 * as tailwindcss-typography plugin is used to style them.
 */
.messages-content {
  outline


### Enhanced 20251109 092920 Wispr Change Automatic Blog Creation And Posting So That
<!-- task_id: UFNWczVnQUdyYXBTd29Peg -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-092920-wispr-change automatic blog creation and posting so that.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 09:39

# Wispr Flow Note

Change automatic blog creation and posting so that the article is aimed more at an e-commerce client or potentially e-commerce client for me, rather than at the moment it's aimed at other PPC agencies

---
*Source: Wispr Flow*
*Created: 2025-11-09 09:29:20.390 +00:00*
*Note ID: aea77c97-00aa-40ca-8aac-68ee73039991*



---

**Original Note:**
# Wispr Flow Note

Change automatic blog creation and posting so that the article is aimed more at an e-commerce client or potentially e-commerce client for me, rather than at the moment it's aimed at other PPC agencies

---
*Source: Wispr Flow*
*Created: 2025-11-09 09:29:20.390 +00:00*
*Note ID: aea77c97-00aa-40ca-8aac-68ee73039991*


### Enhanced 20251109 080415 Wispr The Laptop Sync Isn T Working For Roxys So I Need
<!-- task_id: UGtsWWVyNTBnM1lFRzljVA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-080415-wispr-the laptop sync isn-t working for roxys so i need.md
**Type:** completion
**Client:** ROXYS
**Priority:** high
**Urgency:** urgent
**Estimated Time:** 2 hours
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 09:41

**Dependencies/Blockers:**
- Verify laptop connection
- Check sync command syntax
- Test system compatibility

**Related Tasks:**
- ROXYS System Integration
- Laptop Connectivity Audit

client: ROXYS

**COMPLETION NOTE** - Route to documents folder

Diagnose and resolve the sync command issue for the ROXYS laptop system. Investigate why the command is not being recognized or processed correctly when typed on the laptop.

---

**Context Summary:** ROXYS laptop sync system experiencing command recognition issues that require immediate troubleshooting.

---

**Original Note:**
# Wispr Flow Note

The laptop sync isn't working for ROXYS so I need to investigate this. It doesn't see the command when I type it on my laptop. This is fairly urgent and probably needs to be done by close of play on Monday

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:04:15.327 +00:00*
*Note ID: cd1ae496-9d99-4967-b795-61305b1cf8a9*


### Enhanced 20251031 173727 Google Chat 19A3Cd90
<!-- task_id: QWdWRnBtWGZhd3VBb3J1Xw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251031-173727-google-chat-19a3cd90.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-09 10:32

# Google Chat Message (via Gmail)

**Space:** Collaber PPC Chat
**From:** Gareth Mitchell <gareth@collaber.co.uk>
**Time:** 2025-10-31 17:37:27
**Email ID:** 19a3cd90a7ddd6a8

---

Peter Empson

Peter Empson



@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for this.  
But I finally managed to get some instructions. Please take a look at the

---

**Source:** Google Chat (via Gmail notification)
**Space:** Collaber PPC Chat



---

**Original Note:**
# Google Chat Message (via Gmail)

**Space:** Collaber PPC Chat
**From:** Gareth Mitchell <gareth@collaber.co.uk>
**Time:** 2025-10-31 17:37:27
**Email ID:** 19a3cd90a7ddd6a8

---

Peter Empson

Peter Empson



@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for this.  
But I finally managed to get some instructions. Please take a look at the

---

**Source:** Google Chat (via Gmail notification)
**Space:** Collaber PPC Chat


### Enhanced 20251106 192439 Wispr Rok Systems Create Cv From Linkedin Profile For Tw
<!-- task_id: Zkp1RkpPMjdVRUlySkRQeQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251106-192439-wispr-rok systems create cv from linkedin profile for tw.md
**Type:** task
**Client:** Rok Systems
**Priority:** medium
**Processed:** 2025-11-07 08:25

---

task: Generate LinkedIn CV for Twine
client: Rok Systems

Extract and compile a professional CV for Rok Systems using their LinkedIn profile data, preparing it for Twine platform integration

---

**Context Summary:** Rok Systems needs a CV generated from their LinkedIn profile to be used in Twine platform integration.

---

**Original Note:**
# Wispr Flow Note

Rok Systems create CV from LinkedIn profile for Twine.

---
*Source: Wispr Flow*
*Created: 2025-11-06 19:24:39.794 +00:00*
*Note ID: 0728c977-a44d-4d5d-9af9-c4a9164dc1b4*


### Enhanced 20251108 120522 Wispr Personal Notes  Magnesium And Zinc Tablets Ordered
<!-- task_id: RXd5TlBOMmNzR214X0ZCdw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251108-120522-wispr-personal notes- magnesium and zinc tablets ordered.md
**Type:** general
**Client:** None
**Priority:** None
**Processed:** 2025-11-08 16:32

---

Ordered magnesium and zinc dietary supplements for personal health tracking.


---

**Original Note:**
# Wispr Flow Note

Personal Notes: Magnesium and zinc tablets ordered.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:22.562 +00:00*
*Note ID: 52c0b46e-086b-42d1-be48-4332cab3945d*


### Optimize Google Ads Daily Summary Alert Timing
<!-- task_id: LUNyQ29LakUyUFVTcm5BMw -->
**Status:** 📋 In Progress  

due: within 1 week
client: Rock Systems
Adjust daily summary email timing to ensure accurate reporting:
1. Confirm Google Ads data typically becomes available 24 hours after the reporting day
2. Reschedule daily summary email to 4:00 PM to capture complete data
3. Verify data accuracy after time adjustment
4. Update alert system configuration


### Generate LinkedIn CV for Twine
<!-- task_id: VTlLaVNTVndTMkd3X3VwRQ -->
**Status:** 📋 In Progress  

client: Rok Systems
Extract and compile a professional CV for Rok Systems using their LinkedIn profile data, preparing it for Twine platform integration


### Enhanced 20251112 194624 Wispr Personal Notes  Book In Lucy S Car For Service
<!-- task_id: RmNTeGFvQ1hCYXRjS1R1aQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251112-194624-wispr-personal notes- book in lucy-s car for service.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-12 21:25

# Wispr Flow Note

Personal notes: Book in Lucy’s car for service.

---
*Source: Wispr Flow*
*Created: 2025-11-12 19:46:24.156 +00:00*
*Note ID: 96868cb8-ff45-49e8-9594-92af721382fb*



---

**Original Note:**
# Wispr Flow Note

Personal notes: Book in Lucy’s car for service.

---
*Source: Wispr Flow*
*Created: 2025-11-12 19:46:24.156 +00:00*
*Note ID: 96868cb8-ff45-49e8-9594-92af721382fb*


### Enhanced 20251109 092920 Wispr Change Automatic Blog Creation And Posting So That
<!-- task_id: c0F3a3QwclVLTnRmWE1LMA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-092920-wispr-change automatic blog creation and posting so that.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Change automatic blog creation and posting so that the article is aimed more at an e-commerce client or potentially e-commerce client for me, rather than at the moment it's aimed at other PPC agencies

---
*Source: Wispr Flow*
*Created: 2025-11-09 09:29:20.390 +00:00*
*Note ID: aea77c97-00aa-40ca-8aac-68ee73039991*



---

**Original Note:**
# Wispr Flow Note

Change automatic blog creation and posting so that the article is aimed more at an e-commerce client or potentially e-commerce client for me, rather than at the moment it's aimed at other PPC agencies

---
*Source: Wispr Flow*
*Created: 2025-11-09 09:29:20.390 +00:00*
*Note ID: aea77c97-00aa-40ca-8aac-68ee73039991*


### Enhanced 20251109 084517 Wispr Personal Text Dave Regarding The Mods To Bob
<!-- task_id: Zmc3OVFaOUVVUGJEckZ2OA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-084517-wispr-personal text dave regarding the mods to bob.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Personal text Dave regarding the mods to Bob.

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:45:17.519 +00:00*
*Note ID: 1d500f8c-883e-44f0-806b-028a8d85e236*



---

**Original Note:**
# Wispr Flow Note

Personal text Dave regarding the mods to Bob.

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:45:17.519 +00:00*
*Note ID: 1d500f8c-883e-44f0-806b-028a8d85e236*


### Enhanced 20251113 134749 Wispr Hi  I M
<!-- task_id: YzdxR3RYbGJkU01ZMkE3Rw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251113-134749-wispr-hi- i-m.md
**Type:** general
**Client:** None
**Priority:** None
**Urgency:** None
**Estimated Time:** None
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-16 20:24

Incomplete note - appears to be a voice transcription fragment


---

**Original Note:**
# Wispr Flow Note

Hi, I'm

---
*Source: Wispr Flow*
*Created: 2025-11-13 13:47:49.034 +00:00*
*Note ID: 4eea964e-40b2-4ac6-b7d0-497609b9fc97*


### Enhanced 20251109 145926 Wispr Send Details To Stag Park  Our Bank Account  And R
<!-- task_id: UGdMb2NiMUMtZGJYU3MycQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-145926-wispr-send details to stag park- our bank account- and r.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Send details to Stag Park, our bank account, and rebook somewhere else for the 29th of December.This is a personal note.

---
*Source: Wispr Flow*
*Created: 2025-11-09 14:59:26.546 +00:00*
*Note ID: 6982aa92-4863-4988-bdf8-83308496f8fe*



---

**Original Note:**
# Wispr Flow Note

Send details to Stag Park, our bank account, and rebook somewhere else for the 29th of December.This is a personal note.

---
*Source: Wispr Flow*
*Created: 2025-11-09 14:59:26.546 +00:00*
*Note ID: 6982aa92-4863-4988-bdf8-83308496f8fe*


### Enhanced 20251106 140214 Wispr Https Business Google Com Uk Think Ai Excellenc
<!-- task_id: Q0F0YTJ4aU82UldoNl8yXw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251106-140214-wispr-https-business-google-com-uk-think-ai-excellenc.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

[https://business.google.com/uk/think/ai-excellence/ai-mode-google-marketing-search-strategy/?utm\_medium=email&utm\_source=d-curation-depth-listicle&utm\_team=twg-emea&utm\_campaign=TwG-EMEA-CD-L-2025-11-06-Marketing-growth-Knak&utm\_content=list-3a&utm\_theme=AI&mkt\_tok=MTcyLUdPUC04MTEAAAGd-D8LEMq6rdNqXn6TpEzOt1cZIWRBg4m\_jPRF2nG5p-g12oQiQqgfNkQh4S7Fp-j-q7VqVhw\_KBJtHUxydvccAfb\_SL5svuXHKubiK0tMBdYPv5A](https://business.google.com/uk/think/ai-excellence/ai-mode-google-marketing-search-strategy/?utm_medium=email&utm_source=d-curation-depth-listicle&utm_team=twg-emea&utm_campaign=TwG-EMEA-CD-L-2025-11-06-Marketing-growth-Knak&utm_content=list-3a&utm_theme=AI&mkt_tok=MTcyLUdPUC04MTEAAAGd-D8LEMq6rdNqXn6TpEzOt1cZIWRBg4m_jPRF2nG5p-g12oQiQqgfNkQh4S7Fp-j-q7VqVhw_KBJtHUxydvccAfb_SL5svuXHKubiK0tMBdYPv5A)

---
*Source: Wispr Flow*
*Created: 2025-11-06 14:02:14.682 +00:00*
*Note ID: 6c6063d9-ed67-4a69-b2a1-504f495d122b*



---

**Original Note:**
# Wispr Flow Note

[https://business.google.com/uk/think/ai-excellence/ai-mode-google-marketing-search-strategy/?utm\_medium=email&utm\_source=d-curation-depth-listicle&utm\_team=twg-emea&utm\_campaign=TwG-EMEA-CD-L-2025-11-06-Marketing-growth-Knak&utm\_content=list-3a&utm\_theme=AI&mkt\_tok=MTcyLUdPUC04MTEAAAGd-D8LEMq6rdNqXn6TpEzOt1cZIWRBg4m\_jPRF2nG5p-g12oQiQqgfNkQh4S7Fp-j-q7VqVhw\_KBJtHUxydvccAfb\_SL5svuXHKubiK0tMBdYPv5A](https://business.google.com/uk/think/ai-excellence/ai-mode-google-marketing-search-strategy/?utm_medium=email&utm_source=d-curation-depth-listicle&utm_team=twg-emea&utm_campaign=TwG-EMEA-CD-L-2025-11-06-Marketing-growth-Knak&utm_content=list-3a&utm_theme=AI&mkt_tok=MTcyLUdPUC04MTEAAAGd-D8LEMq6rdNqXn6TpEzOt1cZIWRBg4m_jPRF2nG5p-g12oQiQqgfNkQh4S7Fp-j-q7VqVhw_KBJtHUxydvccAfb_SL5svuXHKubiK0tMBdYPv5A)

---
*Source: Wispr Flow*
*Created: 2025-11-06 14:02:14.682 +00:00*
*Note ID: 6c6063d9-ed67-4a69-b2a1-504f495d122b*


### Enhanced 20251114 145834 Wispr Personal Notes For Monday 1   Sort The Hose Out
<!-- task_id: LTk3SmdSZjRtTG42RmlSZg -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251114-145834-wispr-personal notes for monday-1-  sort the hose out.md
**Type:** task
**Client:** None
**Priority:** low
**Urgency:** normal
**Estimated Time:** 15-30 min
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-16 20:54

**Related Tasks:**
- Garden Maintenance

task: Hose Maintenance
due: end of this week
time: 15-30 min

Inspect and organize the garden hose. Check for any damages, tangles, or storage issues that need to be addressed.


---

**Original Note:**
# Wispr Flow Note

Personal notes for Monday:

1.  Sort the hose out

---
*Source: Wispr Flow*
*Created: 2025-11-14 14:58:34.907 +00:00*
*Note ID: 09031715-87b5-4618-aa64-88fb445d3ca4*


### Enhanced 20251116 180221 Wispr Personal  Ring Doctor  Re Blood Test
<!-- task_id: RVhfZ2JmRFU3cm02dDVheA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251116-180221-wispr-personal- ring doctor- re blood test.md
**Type:** task
**Client:** None
**Priority:** medium
**Urgency:** normal
**Estimated Time:** 15 min
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-17 06:51

**Dependencies/Blockers:**
- locate contact number for doctor's office

task: Follow Up on Blood Test
due: within next 3-5 business days
time: 15 min

Contact medical provider to discuss recent blood test results. Ensure to have test reference number or date ready when calling.


---

**Original Note:**
# Wispr Flow Note

Personal. Ring doctor. Re blood test.

---
*Source: Wispr Flow*
*Created: 2025-11-16 18:02:21.141 +00:00*
*Note ID: 293d48e0-5d51-4ad6-a74f-4cff17675ce5*


### Enhanced 20251108 120522 Wispr Personal Notes  Magnesium And Zinc Tablets Ordered
<!-- task_id: WFZ0VWp1UVZIVjhNeFNCNA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251108-120522-wispr-personal notes- magnesium and zinc tablets ordered.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Personal Notes: Magnesium and zinc tablets ordered.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:22.562 +00:00*
*Note ID: 52c0b46e-086b-42d1-be48-4332cab3945d*



---

**Original Note:**
# Wispr Flow Note

Personal Notes: Magnesium and zinc tablets ordered.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:22.562 +00:00*
*Note ID: 52c0b46e-086b-42d1-be48-4332cab3945d*


### Enhanced 20251112 194624 Wispr Personal Notes  Book In Lucy S Car For Service
<!-- task_id: blYyY0J0emhPZV83cTdRaw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251112-194624-wispr-personal notes- book in lucy-s car for service.md
**Type:** task
**Client:** None
**Priority:** medium
**Urgency:** normal
**Estimated Time:** 30 min
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-16 20:24

**Dependencies/Blockers:**
- Confirm Lucy's preferred service center
- Check Lucy's availability

task: Schedule Car Service for Lucy
due: within next 7 days
time: 30 min

Contact Lucy's preferred automotive service center to book a maintenance appointment for her vehicle. Confirm service details, availability, and potential time slots.

---

**Context Summary:** Personal task to schedule vehicle maintenance for Lucy

---

**Original Note:**
# Wispr Flow Note

Personal notes: Book in Lucy’s car for service.

---
*Source: Wispr Flow*
*Created: 2025-11-12 19:46:24.156 +00:00*
*Note ID: 96868cb8-ff45-49e8-9594-92af721382fb*


### Enhanced 20251109 080415 Wispr The Laptop Sync Isn T Working For Roxys So I Need
<!-- task_id: MjczRDNYRDhHbkpBcDhpZA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-080415-wispr-the laptop sync isn-t working for roxys so i need.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

The laptop sync isn't working for ROXYS so I need to investigate this. It doesn't see the command when I type it on my laptop. This is fairly urgent and probably needs to be done by close of play on Monday

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:04:15.327 +00:00*
*Note ID: cd1ae496-9d99-4967-b795-61305b1cf8a9*



---

**Original Note:**
# Wispr Flow Note

The laptop sync isn't working for ROXYS so I need to investigate this. It doesn't see the command when I type it on my laptop. This is fairly urgent and probably needs to be done by close of play on Monday

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:04:15.327 +00:00*
*Note ID: cd1ae496-9d99-4967-b795-61305b1cf8a9*


### Enhanced 20251109 081911 Wispr Go Clean  This Seems To Be A Drop Off In Profitabi 1
<!-- task_id: M1R6NGxvVGFIZmM4NTFtTQ -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-081911-wispr-go clean- this seems to be a drop-off in profitabi-1.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Go clean! This seems to be a drop-off in profitability in November. I need to do an audit and then make suggestions on what can be done to improve the profitability in these leaner months

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:19:11.126 +00:00*
*Note ID: 86175072-ada4-4b9c-9aba-c345b1b0775f*



---

**Original Note:**
# Wispr Flow Note

Go clean! This seems to be a drop-off in profitability in November. I need to do an audit and then make suggestions on what can be done to improve the profitability in these leaner months

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:19:11.126 +00:00*
*Note ID: 86175072-ada4-4b9c-9aba-c345b1b0775f*


### Enhanced 20251108 120535 Wispr Personal Note  Velo Viewer Subscription Cancelled
<!-- task_id: S1RndHlpaTZQcVlCejZkeA -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251108-120535-wispr-personal note- velo viewer subscription cancelled.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Personal note: Velo viewer subscription cancelled.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:35.969 +00:00*
*Note ID: 10a287da-3ee8-412a-986b-de0369d39f97*



---

**Original Note:**
# Wispr Flow Note

Personal note: Velo viewer subscription cancelled.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:35.969 +00:00*
*Note ID: 10a287da-3ee8-412a-986b-de0369d39f97*


### Enhanced 20251106 140517 Wispr Check The Hoses Of Water Hose On Amazon For Curren
<!-- task_id: RzdWMzlBNVY1dUdSeUlhMw -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251106-140517-wispr-check the hoses of water hose on amazon for curren.md
**Type:** general
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-13 08:26

# Wispr Flow Note

Check the hoses of water hose on Amazon for current control. Budget change required?

---
*Source: Wispr Flow*
*Created: 2025-11-06 14:05:17.983 +00:00*
*Note ID: d189ac5a-a0b4-4695-9fd9-ea7106dc1070*



---

**Original Note:**
# Wispr Flow Note

Check the hoses of water hose on Amazon for current control. Budget change required?

---
*Source: Wispr Flow*
*Created: 2025-11-06 14:05:17.983 +00:00*
*Note ID: d189ac5a-a0b4-4695-9fd9-ea7106dc1070*


### Enhanced 20251109 081911 Wispr Go Clean  This Seems To Be A Drop Off In Profitabi
<!-- task_id: al9QbWJudS1vWGM4TFVOTg -->
**Status:** 📋 In Progress  

# AI-Enhanced Note
**Original:** 20251109-081911-wispr-go clean- this seems to be a drop-off in profitabi.md
**Type:** completion
**Client:** N/A
**Priority:** N/A
**Urgency:** N/A
**Estimated Time:** N/A
**Model Used:** haiku
**Processed:** 2025-11-17 08:22

**COMPLETION NOTE** - Route to documents folder

# Wispr Flow Note

Go clean! This seems to be a drop-off in profitability in November. I need to do an audit and then make suggestions on what can be done to improve the profitability in these leaner months

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:19:11.126 +00:00*
*Note ID: 86175072-ada4-4b9c-9aba-c345b1b0775f*



---

**Original Note:**
# Wispr Flow Note

Go clean! This seems to be a drop-off in profitability in November. I need to do an audit and then make suggestions on what can be done to improve the profitability in these leaner months

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:19:11.126 +00:00*
*Note ID: 86175072-ada4-4b9c-9aba-c345b1b0775f*


### [NMA] Week 2.6: Compare US/UAE vs ROW Management performance (30 mins)
<!-- task_id: SjZKYWJIMUJsekk3T2ExVg -->
**Status:** 📋 In Progress  

After 2 weeks of country campaigns running alongside ROW Management, compare performance:

US campaign: Conversions, CPA, CTR vs ROW Management
UAE campaign: Conversions, CPA, CTR vs ROW Management

Decision: If country campaigns prove superior, gradually shift budget from ROW Management. Do NOT pause immediately - gradual migration.


### [NMA] Week 3.4: 3-week progress report & next phase planning (2 hours)
<!-- task_id: WHZ1TWl5VTA5UFNlaEtNOA -->
**Status:** 📋 In Progress  

Compile 3-week performance summary (Nov 17-Dec 8).

Report contents:
- Conversion change: 47.8 → ? (target: 55-65)
- CPA change: £169k → ? (target: £130-150k)
- All 13 optimizations completed
- Wins and learnings
- Recommendations for next phase (Dec 9-29)

Share with Paul Riley, Anwesha, internal team.

Next phase preview: Scale winning campaigns, additional country campaigns, day-of-week adjustments (deferred from Nov 17).


### [NMA] Week 3.3: Create Engineering asset group for PMax (3 hours)
<!-- task_id: V2NaMDQ1YnZlajJ1UzYxcA -->
**Status:** 📋 In Progress  

Create separate Engineering asset group in UK PMax campaign.

Assets needed:
- 15 headlines (engineering-focused)
- 5 long headlines
- 5 descriptions
- Engineering-specific images (labs, cars, projects)
- Videos (student testimonials)
- Final URLs: Engineering landing pages only

Expected: +5-10 conversions/month, better audience segmentation, improved ad relevance for engineering searches.


### [NMA] Week 3.2: Expand ROW Engineering keyword portfolio (2 hours)
<!-- task_id: ekJNZ0g0ODY5eDBIUlpiSw -->
**Status:** 📋 In Progress  

ROW Engineering is best performer (£34,744 CPA vs £169k avg). Add 15-20 related keywords.

Suggestions: automotive engineering courses, motorsport engineering online, automotive technology degree, vehicle engineering programs, racing engineering courses, automotive design degree, motorsport management degree.

Match type: 70% Broad, 30% Exact. Consider budget increase to £80/day if Nov 29 review shows strong performance.

Expected: +10-15 conversions/month


### [NMA] Week 2.5: Remove zero-impression keywords (30 mins)
<!-- task_id: VEEtaDZaLUNQTkNBdTVMSQ -->
**Status:** 📋 In Progress  

Pause ~150 keywords identified in Week 1 review.

Focus on keywords with QS <3 and 0 impressions in 90 days.

Expected impact: Cleaner account structure, improved account-level quality score, easier monitoring.


### [NMA] Week 2.4: Create UAE country-specific campaign (2 hours)
<!-- task_id: LXc2SGFXckR2VXhmY3E2Nw -->
**Status:** 📋 In Progress  

Campaign: NMA | Search | UAE | Engineering
- Daily Budget: £20
- Target CPA: £40
- Keywords: Middle East engineering education terms
- Ad copy: UAE partnerships, regional relevance
- Sitelinks: International student support

Expected: 1-2 conversions in first month. Run alongside ROW Management for 2 weeks.


### [NMA] Week 2.3: Create US country-specific campaign (2 hours)
<!-- task_id: c25lSHA3cVNfZlF5YlJVVA -->
**Status:** 📋 In Progress  

Campaign: NMA | Search | US | Engineering
- Daily Budget: £30
- Target CPA: £60
- Keywords: US-focused engineering terms
- Ad copy: US career outcomes, accreditation
- Sitelinks: US application process, alumni in US

Expected: 2-4 conversions in first month. Run alongside ROW Management for 2 weeks, compare performance.


### [NMA] Week 2.2: Apply demographic bid adjustments (30 mins)
<!-- task_id: TnRkMzdhamlETXRibkJaNQ -->
**Status:** 📋 In Progress  

Based on Week 1 demographic analysis.

Conservative approach: Apply -20% bid adjustment (NOT exclusions) to segments with CPA >2x average.

Likely segments: 18-24, possibly 65+.

Test for 2 weeks before further adjustments. Maintains reach while optimizing.


### [NMA] Week 2.1: Review Target CPA performance (1 hour) - CRITICAL
<!-- task_id: UW5saE1IMFVIZmhqN3JCbg -->
**Status:** 📋 In Progress  

3-week review of Target CPA (implemented Nov 10).

Compare CPAs to targets:
- UK Search: Target £100
- ROW Search: Target £50  
- UK Management: Target £150

If within 20% of target: continue. If 20-50% above: reduce budget 10-15%. If 50%+ above: review structure.

Decide on budget adjustments (e.g., ROW Engineering £40→£80/day if performing well).


### [NMA] Week 1.6: Review new keywords - Quality Score check (30 mins)
<!-- task_id: V0RaWkpoLS1xZ2MzQmVmRA -->
**Status:** 📋 In Progress  

1-week checkpoint for 5 keywords added Nov 17.

Success criteria:
- Quality Score 7+ 
- CTR >5%
- Impressions >100/day for broad match

Pause underperformers. Document performance in tasks-completed.md.


### [NMA] Week 1.5: Review zero-impression keywords (1 hour)
<!-- task_id: REZCWjFaNGtQY3RFcnlDdA -->
**Status:** 📋 In Progress  

Run GAQL query for keywords with 0 impressions in 90 days. Check Quality Scores.

Categorize: Low search volume vs Poor relevance vs Budget constraint.

Prepare list (~150 keywords) for removal in Week 2. Export before pausing.


### [NMA] Week 1.4e: Monitor new keywords - Day 5 (15 mins)
<!-- task_id: RmFoeHd2U1ljS3BrMXM5bg -->
**Status:** 📋 In Progress  

Daily check of 5 keywords (PB_2025 label). Track impressions, position, clicks, CTR.


### [NMA] Week 1.4d: Monitor new keywords - Day 4 (15 mins)
<!-- task_id: eVdOeVNiUW8zc196YVRJOA -->
**Status:** 📋 In Progress  

Daily check of 5 keywords (PB_2025 label). Track impressions, position, clicks, CTR.


### [NMA] Week 1.4c: Monitor new keywords - Day 3 (15 mins)
<!-- task_id: T2U2R1RyejNBU2ZhSWE2dw -->
**Status:** 📋 In Progress  

Daily check of 5 keywords (PB_2025 label). Track impressions, position, clicks, CTR.


### [NMA] Week 1.4b: Monitor new keywords - Day 2 (15 mins)
<!-- task_id: cmNsZHRJc0hEWHJoZ01Lcw -->
**Status:** 📋 In Progress  

Daily check of 5 keywords (PB_2025 label). Track impressions, position, clicks, CTR.


### [NMA] Week 1.4a: Monitor new keywords - Day 1 (15 mins)
<!-- task_id: YTRiTEJfZTBLOTEya041Mw -->
**Status:** 📋 In Progress  

Check 5 keywords added Nov 17 (label PB_2025):
- automotive engineering degree
- automotive design courses
- masters in motorsport engineering
- automotive engineering master
- degree in automotive engineering

Track: impressions, avg position, clicks, CTR. Quality Score after 7 days.


### [NMA] Week 1.2: Add sitelinks to active campaigns (2 hours)
<!-- task_id: RkpwWWx2R3dGMGVwQVRpRw -->
**Status:** 📋 In Progress  

Add 4-6 sitelinks to priority campaigns:
- ROW Engineering Search
- UK Engineering Management
- UK Motorsport

Ideas: Course Guides, Application Process, Career Outcomes, Alumni Stories, Study Options, Payment Plans

Expected: +10-15% CTR, +5-8% conversion rate


### [NMA] Week 1.1: Fix disapproved sitelinks (30 mins)
<!-- task_id: M1VlX0p4NnY3aGJ1NHhfNQ -->
**Status:** 📋 In Progress  

Fix 2 sitelinks:
1. Course Guide Download - Change "Earn as Your Learn" to "Earn as You Learn"
2. Motorsport Engineering - Change "Find Out More" to specific benefit

Re-enable after edits. Part of 3-week improvement plan.


### Sort the hose out
<!-- task_id: MS1Ha0dZZDBfRTcxcmhhaQ -->
**Status:** 📋 In Progress  

Personal task from Wispr Flow (Nov 14)

Source: Wispr Flow note
Created: 2025-11-14


### Ring doctor - Re blood test
<!-- task_id: YURHWWpRbUg1dWhfdzE0Zw -->
**Status:** 📋 In Progress  

Personal task from Wispr Flow (Nov 16)

Source: Wispr Flow note
Created: 2025-11-16


### Decide: Resubscribe to Cursor Pro?
<!-- task_id: bmhCaVdUQW5xV29zU29SQg -->
**Status:** 📋 In Progress  

Your Cursor Pro Plus subscription ends today - downgrade to Free tier complete.

DECISION: Resubscribe to Cursor Pro ($20/month)?

EVALUATE:
- Hit Free tier limits? (100-200 tab completions, 50 AI chats)
- Was it frustrating or manageable?
- Missing unlimited features?

OPTIONS:
1. Stay Free - Save $20/month (Claude Code still unlimited)
2. Resubscribe Pro $20/month - More completions
3. Upgrade Pro Plus $40/month - Unlimited

SAVINGS SO FAR:
- API optimization: $40-80/month
- Cursor cancelled: $40/month
- Total: $80-120/month saved

Note: Resubscribing to Pro still saves $20/month vs before!


## Details

Roksys starling and tide bank statements for 1st jun 2024 to 31st may 2025. To be done on the 6th November

## Status

- [ ] Todo

## Notes


## Details

Roksys starling and tide bank statements for 1st jun 2024 to 31st may 2025. To be done on the 6th November

## Status

- [ ] Todo

## Notes


## 💰 CLAUDE SUBSCRIPTION COST-BENEFIT ANALYSIS

**Current Spend:**
- Claude Max: £90/month (~$113 USD)
- Cursor Pro: $20/month (includes Claude access)
- Total Claude spend: £90 + any API credits used

**Alternative: Downgrade to Claude Pro:**
- Claude Pro: £20/month (~$25 USD)
- Cursor Pro: $20/month
- Total: £45/month vs £110/month current = **£65/month savings (£780/year)**

**Questions to Answer (Nov 13):**

1. **Usage Level Check:**
   - Go to: https://claude.ai (click your profile)
   - Look for usage statistics/metrics
   - How many Claude Code sessions in past 2 weeks?
   - How many messages/tasks completed?
   - Did you hit any limits or slowdowns?

2. **Speed/Priority Access:**
   - Did you experience "High demand" messages in past 2 weeks?
   - Did Claude Code feel slow or rate-limited at any point?
   - Was response time consistently fast?

3. **Feature Usage:**
   - Did you use the "MAX Only" models extensively?
   - Did you need the extended context windows (1M tokens)?
   - Could you have done the same work on Claude Pro?

4. **Business Value:**
   - How many client reports/analyses did you generate?
   - How much time did Claude Code save you?
   - What's the ROI of £90/month for your business?

**Decision Matrix:**

**KEEP Claude Max (£90/month) IF:**
✅ You use Claude Code daily (5+ hours/week)
✅ You frequently hit usage limits on the trial
✅ Priority access/speed is critical for your workflow
✅ You use extended context (1M tokens) regularly
✅ £90/month ROI is justified by time saved

**DOWNGRADE to Claude Pro (£20/month) IF:**
❌ You use Claude Code occasionally (< 5 hours/week)
❌ You never hit usage limits
❌ Regular Sonnet 4.5 models handle all your needs
❌ £70/month savings would be significant
❌ Cursor's built-in Claude handles most coding

**FINANCIAL COMPARISON:**

Current Setup:
- Claude Max: £90/month
- Cursor Pro: $20/month (~£16)
- ChatGPT Plus: $20/month (~£16)
- **Total: ~£122/month**

Optimized Setup Option 1 (Downgrade Claude):
- Claude Pro: £20/month (for Claude Code)
- Cursor Pro: £16/month (for coding)
- ChatGPT Plus: £16/month
- **Total: ~£52/month = £70/month savings**

Optimized Setup Option 2 (Drop ChatGPT):
- Claude Max: £90/month
- Cursor Pro: £16/month
- **Total: ~£106/month = £16/month savings**

Optimized Setup Option 3 (Most Efficient):
- Claude Pro: £20/month
- Cursor Pro: £16/month
- **Drop ChatGPT** (use Claude for everything)
- **Total: ~£36/month = £86/month savings (£1,032/year)**

---

**Context:**
Your last API charge was August 2025 (before heavy Claude Code/Cursor usage). If balance is unchanged after 2 weeks of MAX model usage, it confirms they're covered by your Max subscription.

**Related:**
- Claude Max subscription: £90/month (unlimited Claude Code + web)
- Cursor Pro: $20/month (built-in models)
- API key in code (claude_copywriter.py): Separate, necessary for Google Ads tools

**Action Items (Nov 13):**
1. Check API balance vs $21.13 baseline
2. Review actual Claude usage over 2 weeks
3. Evaluate speed/priority access value
4. Make informed decision: Keep Max, Downgrade to Pro, or optimize further
5. If downgrading, cancel Max before Nov 18, 2025 (renewal date per screenshot)

Dashboard link: https://console.anthropic.com/settings/billing
Claude.ai billing: https://claude.ai/settings/billing


## Completed Work

### WordPress Blog Automation System (November 8, 2025)
**Status:** ✅ Completed

**What Was Built:**
- Fully automated weekly blog post generator for roksys.co.uk
- Pulls articles from knowledge base (last 7 days)
- Writes in Peter's tone of voice (from roksys-website-content.md)
- Auto-publishes to WordPress every Monday 9 AM
- Zero manual intervention required

**Key Features:**
- Blog generator runs Monday 7:30 AM (before KB summary)
- KB weekly summary runs Monday 8:00 AM (includes blog post info)
- Sunday night KB update sequence (11:00 PM) ensures fresh content
- Blog navigation setup (page ID: 507, category archive ready)
- Helper scripts for manual publishing and text removal

**Files Created:**
- `agents/weekly-blog-generator/weekly-blog-generator.py` - Main blog generator
- `agents/content-sync/publish-blog-post-now.py` - Publish scheduled posts immediately
- `agents/content-sync/remove-text-from-post.py` - Remove text from posts
- `agents/content-sync/wordpress-blog-navigation-setup.py` - Blog navigation setup
- `agents/launchagents/com.petesbrain.weekly-blog-generator.plist` - Blog generator schedule
- `agents/launchagents/com.petesbrain.sunday-kb-update.plist` - Sunday KB update sequence
- `agents/content-sync/BLOG-NAVIGATION-SETUP.md` - Navigation setup docs
- `.claude/skills/wordpress-blog-manager/` - WordPress management skill

**WordPress Configuration:**
- URL: https://roksys.co.uk
- Username: Peter
- Application Password: Configured in LaunchAgent
- Blog Category: "Google Ads Weekly" (ID: 5)
- Blog Page: "Google Ads Blog" (ID: 507)
- Category Archive: https://roksys.co.uk/category/google-ads-weekly/

**Schedule Optimization:**
- Blog generator: Monday 7:30 AM (ensures KB is updated)
- KB weekly summary: Monday 8:00 AM (includes blog post info)
- Sunday KB update: Sunday 11:00 PM (final update before blog generation)

**Integration:**
- KB weekly summary email now includes blog post publishing instructions
- Blog posts automatically appear in category archive
- Navigation menu item needs to be added manually in Elementor (header builder)

**WordPress Skill Created:**
- New skill: `wordpress-blog-manager` for managing WordPress content
- Provides WordPress access information and credentials
- Auto-triggers when discussing WordPress blog management

### Claude Code: Read documentation and Indie Dev Dance tutorials
<!-- task_id: LWtsQlpIa3o2UzV1R3RQbw -->
**Status:** ✅ Completed (2025-10-30)  

From Claude Code setup meeting on 2025-10-27. Study Claude Code documentation at docs.claude.com to understand capabilities, best practices, and advanced features. Watch Indie Dev Dance YouTube channel for practical tutorials and real-world examples. Goal: Build foundational knowledge before implementing custom commands/skills.


### Order testosterone prescription from GP
<!-- task_id: M29YMWhOMVVZNmtrLVlRNw -->
**Status:** ✅ Completed (2025-11-03)  

📧 **EMAIL READY TO SEND:**

**To:** gp.n84617@nhs.net
**Subject:** Repeat Prescription - Peter Empson

---

**COPY THIS EMAIL BODY:**

Hi

Could I please have a repeat prescription for 

Tostran 2% Gel



Peter Empson
9 Pinewood Close
PR8 5LL

DOB 29/7/64

07932 454652

Regards

Peter



e:petere@roksys.co.uk
t:07932 454652

---

💡 **INSTRUCTIONS:**
1. Click "New Email" in Gmail
2. To: gp.n84617@nhs.net
3. Subject: Repeat Prescription - Peter Empson
4. Copy the email body above and paste
5. Send
6. Mark this task complete

(Email body taken from your last prescription request on Oct 11, 2025)


### verify google tasks integration works
<!-- task_id: Qk1ncGMtNWU4UlJMemtVZA -->
**Status:** ✅ Completed (2025-11-05)  

Open Google Tasks app or visit tasks.google.com to see this task!
Due: tomorrow


### verify google tasks integration works
<!-- task_id: YzhTX1JQZEJzT3g3b21JTw -->
**Status:** ✅ Completed (2025-11-05)  

Open Google Tasks app or visit tasks.google.com to see this task!
Due: tomorrow


### [Devonshire] Change landing page for cottages
<!-- task_id: aDZnNEhVTTJiclBucDQ0dQ -->
**Status:** ✅ Completed (2025-11-05)  

Change landing page for the following self-catering ad groups:
- Chatsworth Estate Cottages
- Chatsworth Self Catering
- Peak District Cottages

These are ad groups within the Chatsworth Escapes Self Catering campaign.

Note: Shepherds Huts, Hunting Tower, Russian Cottage, and Yorkshire Cottages should NOT be changed.


### Enhanced 20251108 120522 Wispr Personal Notes  Magnesium And Zinc Tablets Ordered
<!-- task_id: RXd5TlBOMmNzR214X0ZCdw -->
**Status:** ✅ Completed (2025-11-09)  

# AI-Enhanced Note
**Original:** 20251108-120522-wispr-personal notes- magnesium and zinc tablets ordered.md
**Type:** general
**Client:** None
**Priority:** None
**Processed:** 2025-11-08 16:32

---

Ordered magnesium and zinc dietary supplements for personal health tracking.


---

**Original Note:**
# Wispr Flow Note

Personal Notes: Magnesium and zinc tablets ordered.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:22.562 +00:00*
*Note ID: 52c0b46e-086b-42d1-be48-4332cab3945d*



### Scan shared drives and update client CONTEXT.md files
<!-- task_id: ZG4wRVdHVEJhT2JKUi0yRA -->
**Status:** ✅ Completed (2025-11-09)  

Monthly on-demand scan of Google Drive "Shared with Me" to categorize and organize shared documents.

**Process:**
1. Tell Claude Code: "Scan shared drives and update files"
2. Claude will search Google Drive for shared documents
3. Files automatically categorized into THREE types:
   - **Client files** → Update client CONTEXT.md files
   - **Roksys/industry files** → Add to knowledge base inbox
   - **Personal files** → Flag for your review
4. Claude updates appropriate locations and reports findings

**What it tracks:**

**Client Resources:**
- Monthly reports and presentations
- Campaign briefs and strategy documents  
- Product data and supplemental feeds
- Client-maintained documentation

**Roksys Knowledge Base:**
- Google Ads platform updates and best practices
- Industry insights and research
- Marketing automation and AI strategies
- ROK methodologies and playbooks

**Personal Knowledge:**
- Your learning resources and training materials
- Personal notes and strategy ideas
- Books, courses, research

**Categorization Keywords:**
- Clients: Matched by client name/campaign prefix
- Roksys: "google ads", "ppc", "pmax", "roas", "ga4", "methodology", etc.
- Personal: "peter empson", "personal", "learning", "training", etc.

**Frequency:** Monthly (first week of month recommended)

This ensures client CONTEXT.md files stay current AND your knowledge base grows automatically from shared resources.


### Personal text Dave regarding the mods to Bob.
<!-- task_id: YlJNdDRuUGw0WUJtdW1Lbg -->
**Status:** ✅ Completed (2025-11-10)  

# Wispr Flow Note

Personal text Dave regarding the mods to Bob.



### Enhanced 20251109 084517 Wispr Personal Text Dave Regarding The Mods To Bob
<!-- task_id: R0twcmhLYnJtbjk4b3FsdA -->
**Status:** ✅ Completed (2025-11-10)  

# AI-Enhanced Note
**Original:** 20251109-084517-wispr-personal text dave regarding the mods to bob.md
**Type:** general
**Client:** None
**Priority:** None
**Urgency:** None
**Estimated Time:** None
**Model Used:** claude-3-5-haiku-20241022
**Processed:** 2025-11-09 09:40

Personal communication needed with Dave about modifications related to Bob


---

**Original Note:**
# Wispr Flow Note

Personal text Dave regarding the mods to Bob.

---
*Source: Wispr Flow*
*Created: 2025-11-09 08:45:17.519 +00:00*
*Note ID: 1d500f8c-883e-44f0-806b-028a8d85e236*


### Personal text Dave regarding the mods to Bob.
<!-- task_id: YlJNdDRuUGw0WUJtdW1Lbg -->
**Status:** ✅ Completed (2025-11-10)  

# Wispr Flow Note

Personal text Dave regarding the mods to Bob.


### Enhanced 20251108 120535 Wispr Personal Note  Velo Viewer Subscription Cancelled
<!-- task_id: UGdPcGxtSTZQcG41T3Rhcg -->
**Status:** ✅ Completed (2025-11-09)  

# AI-Enhanced Note
**Original:** 20251108-120535-wispr-personal note- velo viewer subscription cancelled.md
**Type:** general
**Client:** None
**Priority:** None
**Processed:** 2025-11-08 16:32

---

Velo Viewer subscription has been cancelled.


---

**Original Note:**
# Wispr Flow Note

Personal note: Velo viewer subscription cancelled.

---
*Source: Wispr Flow*
*Created: 2025-11-08 12:05:35.969 +00:00*
*Note ID: 10a287da-3ee8-412a-986b-de0369d39f97*


### P0 AFH Reduce ROAS target 190 to 170 percent Q4 peak
<!-- task_id: MTJkeFhHN3NnbzdPZG5CNw -->
**Status:** ✅ Completed (2025-11-16)  

Reduce AFH P Max H&S Zombies Furniture campaign ROAS from 190 to 170 percent. CR trending up, budget utilization high, ready for Q4 scaling per Nov 10 strategy. Customer ID 7972994730

