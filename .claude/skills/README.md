# Claude Skills for PetesBrain

**Date Created**: November 5, 2025
**Status**: ✅ Active - 24 Skills Configured (+ 2 standalone)
**Last Updated**: November 28, 2025
**Source**: Adapted from Mike Rhodes' 8020Brain template + Custom ROK Skills

---

## Overview

Claude Code skills are automatically triggered capabilities that activate during conversations when relevant context is detected. Unlike agents (scheduled background tasks) or slash commands (manual triggers), skills use progressive context disclosure and auto-invoke when needed.

**Key Benefits**:
- 🤖 **Auto-triggered** - Claude decides when to use them
- 💾 **Context-efficient** - Only loads what's needed
- 🔧 **Modular** - Dedicated directory per skill
- 🔗 **Composable** - Can call MCP servers, other skills

---

## Shared Resources

### Google Ads Query Optimization Patterns
**Location**: `.claude/skills/google-ads-query-optimization-patterns.md`
**Purpose**: Reusable optimization patterns for Google Ads API queries

**7 Performance Patterns**:
1. **IN Clause Instead of Looping** - 3-10x faster for multiple campaigns
2. **Filter at Query Level** - 2-5x faster by filtering in GAQL
3. **Minimal Field Selection** - Reduce response size by 70%
4. **LIMIT for Top N** - Only fetch needed rows
5. **Combine Related Queries** - Reduce API calls
6. **Cache Static Data** - Avoid repeated queries
7. **Asset Status Filtering** - Critical for accurate asset counts

**Applied in**: `google-ads-text-asset-exporter`, `google-ads-campaign-audit`

**For Developers**: Reference these patterns when building new Google Ads skills to ensure optimal performance.

---

## Installed Skills

### 1. GAQL Query Builder
**Location**: `.claude/skills/gaql-query-builder/`  
**Purpose**: Build Google Ads Query Language (GAQL) queries on-the-fly  
**Triggers**: When discussing Google Ads data extraction, reports, or performance queries

**Use Cases**:
- "Show me campaign performance for last 7 days"
- "Pull product-level data with ROAS and conversion value"
- "Build a query for search term analysis"
- "Get impression share data by campaign"

**Capabilities**:
- Constructs syntactically correct GAQL
- Validates field names and resource compatibility
- Handles date ranges and filters
- Integrates with Google Ads MCP server
- Provides query explanations

**Resources**:
- `skill.md` - Main skill definition
- `query-reference.md` - GAQL field reference guide
- `common-patterns.md` - Frequently used queries

---

### 2. CSV Analyzer
**Location**: `.claude/skills/csv-analyzer/`  
**Purpose**: Automated analysis of CSV performance data  
**Triggers**: When referencing CSV files or uploaded tabular data

**Use Cases**:
- "Analyze this campaign performance export"
- "What are the top/bottom products in this CSV?"
- "Find trends in this data"
- "Identify wasted spend opportunities"

**Capabilities**:
- Detects data types (Google Ads, product data, keywords)
- Calculates derived metrics (ROAS, CTR, CVR)
- Identifies top/bottom performers
- Spots anomalies and trends
- Generates actionable recommendations
- Creates performance distributions

**Output Format**:
- Executive summary
- Key metrics tables
- Top 10 / Bottom 10 performers
- Trend analysis
- 3-5 prioritized recommendations

**Resources**:
- `skill.md` - Main skill definition
- `metric-definitions.md` - Google Ads metrics explained
- `analysis-framework.md` - Analysis methodology

---

### 3. Google Ads Campaign Audit
**Location**: `.claude/skills/google-ads-campaign-audit/`  
**Purpose**: Comprehensive account audits using ROK's framework  
**Triggers**: When discussing account analysis, audits, or performance reviews

**Use Cases**:
- "Audit the Smythson account"
- "How's Devonshire performing this week?"
- "Run a campaign performance review"
- "Analyze impression share opportunities"

**Capabilities**:
- Campaign overview with key metrics
- Product-level performance analysis (Shopping)
- Placement analysis (Shopping, YouTube, Display)
- Budget efficiency and pacing
- Impression share analysis
- Root cause diagnostics
- 3-5 prioritized recommendations

**Integration**:
- Loads client context from `clients/[client]/CONTEXT.md`
- References previous audits from `clients/[client]/audits/`
- Uses Google Ads MCP server for live data
- Follows ROK analysis methodology

**Audit Types**:
- Weekly audit (comprehensive)
- Impression share audit (growth focus)
- Structure audit (architecture review)
- Deep dive audit (extended analysis)

**Resources**:
- `skill.md` - Main skill definition
- `audit-templates.md` - Report templates
- `common-issues.md` - Typical problems and fixes
- `../../../roksys/knowledge-base/rok-methodologies/` - ROK framework

---

### 4. Google Ads Keyword Audit
**Location**: `.claude/skills/google-ads-keyword-audit/`
**Purpose**: Search campaign keyword and query optimization
**Triggers**: When discussing keywords, search terms, or Search campaign optimization

**Use Cases**:
- "Find wasted spend keywords"
- "What negative keywords should I add?"
- "Analyze search term performance"
- "Identify keyword opportunities"

**Capabilities**:
- Wasted spend identification (low ROAS, zero-conversion)
- Growth opportunities (high-performing keywords to scale)
- Search term analysis (negative keyword candidates)
- Match type optimization
- Performance trend detection
- Actionable-only filtering (skips stable keywords)

**Framework**:
- Uses ROK's actionable-only methodology
- Account average × multipliers (0.7 waste, 1.3 opportunity)
- Minimum spend thresholds to reduce noise
- Business language (revenue impact focus)

**Output Includes**:
- Negative keyword lists (bulk upload format)
- Bid adjustment recommendations
- New keyword suggestions
- Declining keyword alerts
- Prioritized action plan with expected impact

**Resources**:
- `skill.md` - Main skill definition
- `negative-keyword-guide.md` - Negative keyword strategies
- `match-type-guide.md` - Match type best practices

---

### 5. Email Draft Generator ⭐ NEW
**Location**: `.claude/skills/email-draft-generator/`
**Purpose**: Generate client-ready HTML email drafts with proper formatting and British English spelling
**Triggers**: When discussing client emails, updates, or communications

**Use Cases**:
- "Draft email to Devonshire about October performance"
- "Write email for Smythson about budget increase"
- "Email National Design Academy about country analysis"
- "Compose update to Tree2mydoor on Christmas campaigns"

**Capabilities**:
- Auto-loads client CONTEXT.md for tone and preferences
- Applies British vs American English based on client market
- Formats as HTML with tight spacing (line-height: 1.4, 6px margins)
- Uses `<strong>` tags for emphasis (not `<b>`)
- Formats ROAS as percentage (400% not £4.00)
- Auto-saves to `clients/[client]/documents/email-draft-YYYY-MM-DD-[topic].html`
- Opens in browser for easy copy/paste to Apple Mail

**Email Types**:
- Performance updates
- Budget proposals
- Strategy proposals
- Issue updates
- Action required
- General updates

**Integration**:
- Loads client preferences from CONTEXT.md
- References recent reports and documents
- Uses Google Ads MCP for live metrics when relevant
- Integrates with experiment log for context

**Resources**:
- `skill.md` - Main skill definition
- `client-preferences.md` - Client-specific tone and style
- `british-vs-american-english.md` - Spelling reference

**Time Saved**: ~10-15 minutes per email

---

### 6. Text Message Draft Generator ⭐ NEW
**Location**: `.claude/skills/text-message-draft-generator/`
**Purpose**: Generate client-ready text message drafts with proper formatting and British English spelling. Outputs displayed in browser for easy copy/paste to messaging apps
**Triggers**: When discussing text messages, SMS, WhatsApp, or messaging clients

**Use Cases**:
- "Draft text message to Devonshire about October performance"
- "Write text for Smythson about budget approval"
- "WhatsApp National Design Academy about campaign update"
- "Send a text to Tree2mydoor about Christmas campaigns"
- "Message [client] about [topic]"

**Capabilities**:
- Auto-loads client CONTEXT.md for tone and preferences
- Applies British vs American English based on client market
- Formats as HTML for browser display with clean styling
- Concise messaging (under 300 characters ideally)
- Formats ROAS as percentage (400% not £4.00)
- Auto-saves to `clients/[client]/documents/text-draft-YYYY-MM-DD-[topic].html`
- Opens in browser for easy copy/paste to messaging apps (WhatsApp, Messages, etc.)

**Message Types**:
- Quick updates
- Urgent alerts
- Action required
- Check-ins
- Confirmations
- Reminders

**Tone Guidelines**:
- Casual but professional (more informal than emails)
- Concise (scannable in 5 seconds)
- Friendly and conversational
- Clear and actionable

**Integration**:
- Loads client preferences from CONTEXT.md
- References recent reports and documents
- Uses Google Ads MCP for live metrics when relevant
- Integrates with experiment log for context

**Resources**:
- `skill.md` - Main skill definition

**Time Saved**: ~5-10 minutes per text message (from manual drafting to ready-to-send)

---

### 7. Devonshire Monthly Report Generator ⭐ NEW
**Location**: `.claude/skills/devonshire-monthly-report/`
**Purpose**: Generate complete Google Slides monthly Paid Search reports for Devonshire Hotels
**Triggers**: When discussing Devonshire monthly reports or slides

**Use Cases**:
- "Generate October report for Devonshire"
- "Create Devonshire monthly slides"
- "Devonshire November Paid Search report"

**Capabilities**:
- Queries Google Ads API for complete month data
- Generates 14-slide presentation with branded formatting
- Applies Estate Blue (#00333D) and Stone (#E5E3DB) brand colors
- Calculates property-level performance metrics
- Generates insights and recommendations automatically
- Creates actionable next steps for following month
- Outputs Google Slides link ready for review

**Report Structure**:
- Executive summary (budget, ROAS, key metrics)
- Hotels performance (top performers + attention needed)
- Campaign type breakdown (PMax, Search, Self-Catering)
- The Hide separate budget tracking
- Key insights (highlights + areas for improvement)
- Recommendations for next month

**Integration**:
- Loads Devonshire CONTEXT.md for strategic context
- References experiment log for changes during month
- Uses Google Ads MCP for live data
- Checks budget tracker spreadsheet
- Reviews recent client emails for context

**Data Validation**:
- Combines The Hide + Highwayman Arms (same property, renamed)
- Excludes Castles, Weddings, Lismore/Hall from main budget
- Validates zero-conversion campaigns
- Ensures ROAS formatted as percentage

**Resources**:
- `skill.md` - Main skill definition
- References `tools/monthly-report-generator/` for campaign IDs
- Uses `clients/devonshire-hotels/CONTEXT.md` for strategic context

**Time Saved**: ~2.5 hours per month (from 3 hours manual to 20 minutes automated)

---

### 8. Google Ads Text Generator Launch ⭐ NEW
**Location**: `.claude/skills/google-ads-text-generator/`
**Purpose**: Launch the Google Ads Text Generator web application for creating ad copy assets
**Triggers**: When discussing launching the generator or creating Google Ads text assets

**Use Cases**:
- "Launch Google Ads Text Generator"
- "Start the generator"
- "Open the Google Ads generator"
- "I need to create ad copy"
- "Generate headlines and descriptions"

**Capabilities**:
- Automatically navigates to generator directory
- Runs `start.sh` script to launch Flask web server
- Opens browser automatically to `http://localhost:5001`
- Handles API key configuration
- Manages virtual environment setup
- Provides troubleshooting guidance

**What It Launches**:
- Web interface for URL analysis and manual entry
- Generates 50 headlines (30 char max) across 5 sections
- Generates 50 descriptions (90 char max) across 5 sections
- Creates 50 search themes for Performance Max
- Generates sitelinks and callout extensions
- Exports assets as CSV for Google Ads Editor

**Integration**:
- Uses `ANTHROPIC_API_KEY` from `.env` or shell config
- Follows ROK specifications for asset generation
- Validates character limits automatically
- Provides real-time formatting

**Resources**:
- `skill.md` - Main skill definition
- References `tools/google-ads-generator/` directory

**Time Saved**: ~5-10 minutes per launch (no need to remember commands/paths)

---

### 9. Granola Meeting Importer ⭐ NEW
**Location**: `.claude/skills/granola-importer/`
**Purpose**: Automatically import Granola meeting notes from Google Docs (created by Zapier) into client folders
**Triggers**: When discussing importing Granola meetings, syncing meeting notes, or processing recent meetings

**Use Cases**:
- "Import Granola meetings from the last week"
- "Any new Granola meetings?"
- "Sync my meeting notes"
- "Import the Granola meeting from yesterday"
- "Process recent meetings"

**Capabilities**:
- Searches Google Drive for documents matching `"ROK | Granola -"`
- Parses meeting title, attendees, and transcript
- Intelligent client detection (email domains, keywords, fuzzy matching)
- Saves to appropriate client folder or `_unassigned`
- Extracts action items and creates Google Tasks
- Enriches with Granola API attendee data (optional)
- AI analysis for executive summaries (optional)
- Creates review tasks for CONTEXT.md updates

**Import Workflow**:
1. Find Google Docs matching pattern in Shared Drive
2. Parse document content (title, attendees, transcript)
3. Detect client using 3-tier matching system
4. Enrich with Granola API data (if available)
5. Save markdown file to client folder
6. Extract action items → Google Tasks
7. Create review task for CONTEXT.md updates

**Client Detection**:
- **Email Domain Matching** (Primary): Matches attendee emails to clients
- **Title-Based Detection** (Secondary): Fuzzy string matching
- **Content-Based Detection** (Fallback): Analyzes transcript for mentions

**Integration**:
- Google Drive API for document search
- Google Docs API for content fetching
- Granola API for attendee enrichment (optional)
- Google Tasks API for action items
- Client detector from `tools/granola-importer/`
- AI analysis via Anthropic API (optional)

**Output**:
- Meeting files: `clients/[client]/meeting-notes/YYYY-MM-DD-meeting-title-client.md`
- Action items: Google Tasks in "Client Action Items" list
- Review tasks: For updating CONTEXT.md with insights
- Unmatched meetings: Tracked in `shared/data/granola-unmatched-meetings.json`

**Resources**:
- `skill.md` - Main skill definition
- `technical-reference.md` - Complete technical documentation
- References `agents/granola-google-docs-importer/granola-google-docs-importer.py`
- Uses `tools/granola-importer/client_detector.py`

**Time Saved**: ~10-15 minutes per import session (automated client detection, action items, file organization)

---

### 10. WordPress Blog Manager ⭐ NEW
**Location**: `.claude/skills/wordpress-blog-manager/`
**Purpose**: Manage WordPress blog posts, navigation, and content for roksys.co.uk
**Triggers**: When discussing WordPress blog posts, publishing, editing, or site access

**Use Cases**:
- "Publish the scheduled blog post now"
- "Remove text from the blog post"
- "How do I access the WordPress site?"
- "Update blog navigation"
- "Check blog post status"
- "What's the WordPress admin URL?"
- "Show me WordPress credentials"

**Capabilities**:
- Publish scheduled blog posts immediately
- Remove text from blog posts
- Set up blog navigation (Elementor-compatible)
- Access WordPress admin and site information
- Manage blog categories and tags
- View blog post status and URLs
- Provide WordPress access credentials and URLs

**WordPress Access Information**:
- **Site URL**: https://roksys.co.uk
- **Admin URL**: https://roksys.co.uk/wp-admin
- **Username**: Peter
- **Application Password**: Stored in LaunchAgent (`com.petesbrain.weekly-blog-generator.plist`)
- **Blog Category**: "Google Ads Weekly" (ID: 5)
- **Blog Page**: "Google Ads Blog" (ID: 507)
- **Category Archive**: https://roksys.co.uk/category/google-ads-weekly/

**Available Scripts**:
- `agents/content-sync/weekly-blog-generator.py` - Auto-generates weekly posts
- `agents/content-sync/publish-blog-post-now.py` - Publish scheduled posts immediately
- `agents/content-sync/remove-text-from-post.py` - Remove text from posts
- `agents/content-sync/wordpress-blog-navigation-setup.py` - Set up navigation

**Elementor Notes**:
- Site uses Elementor page builder
- Navigation menu managed via Elementor Header Builder
- Blog menu item must be added manually in Elementor (not standard WordPress menu)

**Resources**:
- `skill.md` - Main skill definition
- `agents/content-sync/WORDPRESS-SETUP.md` - Setup instructions
- `agents/content-sync/WORDPRESS-TROUBLESHOOTING.md` - Common issues
- `agents/content-sync/BLOG-NAVIGATION-SETUP.md` - Navigation setup guide
- `roksys/CONTEXT.md` - WordPress access credentials and site information

**Time Saved**: Quick access to WordPress info and credentials without searching files

---

### 11. Blog Article Generator ⭐ NEW
**Location**: `.claude/skills/blog-article-generator/`
**Purpose**: Generate new blog articles for roksys.co.uk with e-commerce focus
**Triggers**: When asking to generate/create/write blog articles or blog posts

**Use Cases**:
- "Generate a new blog article"
- "Create a blog post for this week"
- "Write a new blog article"
- "Update the current blog post with e-commerce focus"
- "Regenerate the blog article"

**Capabilities**:
- Generate new blog posts from recent knowledge base articles
- Update existing blog posts with new content
- Automatically target e-commerce business owners (not PPC agencies)
- Write in Peter's tone of voice (first-person, conversational, British English)
- Publish to WordPress or schedule for future publication
- Use recent Google Ads articles from knowledge base (last 7 days)

**Target Audience**:
Blog articles are written for **EXISTING OR FUTURE CUSTOMERS OF ROK SYSTEMS** who run e-commerce businesses and want to understand:
- The world of Google Ads and what's happening in it
- What's changed recently in Google Ads news
- What technical changes mean for their business in the real world
- What does this actually mean for them?

**Important**: Articles translate technical Google Ads information into real-world business impact. Customers view things from a profitability/business outcome angle, but this is translated naturally without forcing "profitability" language into every article. Articles are regular weekly content with flow and continuity, written in Rok Systems' tone of voice from the website.

**Available Scripts**:
- `agents/content-sync/weekly-blog-generator.py` - Generate new posts (runs Monday 7:30 AM)
- `agents/content-sync/weekly-blog-generator.py --update` - Update existing post

**Resources**:
- `skill.md` - Main skill definition
- `agents/content-sync/WEEKLY-BLOG-GENERATOR-README.md` - Detailed documentation
- `roksys/roksys-website-content.md` - Tone of voice reference

**Time Saved**: Quick blog article generation without remembering script paths and credentials

---

### 12. Agent Dashboard
**Location**: `.claude/skills/agent-dashboard/`  
**Purpose**: Monitor and manage all PetesBrain LaunchAgents  
**Triggers**: When asking about agent status, health checks, or monitoring

**Use Cases**:
- "Check agent status"
- "Are all agents working?"
- "Show me which agents have issues"
- "Restart the email-sync agent"
- "View logs for ai-inbox-processor"

**Capabilities**:
- Auto-discovers all 35+ LaunchAgents
- Shows health status (healthy/unhealthy)
- Identifies critical vs non-critical issues
- View agent logs
- Restart unhealthy agents
- Integrates with health check system

**Resources**:
- `skill.md` - Main skill definition
- References `agents/system/agent-dashboard.py`
- References `agents/system/health-check.py`
- References `shared/scripts/launchagent_discovery.py`

**Time Saved**: Quick status checks without remembering commands

---

### 13. Future Development Documenter ⭐ NEW
**Location**: `.claude/skills/future-development-documenter/`  
**Purpose**: Automatically document incomplete work, half-finished agents, or partial implementations into future developments section  
**Triggers**: When discussing incomplete work, partial features, blocked items, or deferred implementations

**Use Cases**:
- "Document the WhatsApp processing as future development"
- "Add this incomplete feature to future enhancements"
- "This agent is half-finished, document it for later"
- "Create a future development entry for this blocked work"
- "File this partial implementation for future pickup"

**Capabilities**:
- Analyzes incomplete work and identifies what's done vs. needed
- Formats entries according to future-enhancements.md structure
- Determines appropriate priority (High/Medium/Low)
- Extracts relevant files, scripts, and documentation
- Creates comprehensive future development entries
- Links to existing documentation and code
- Identifies blockers and dependencies

**Output Format**:
- Properly formatted entry in `docs/future-enhancements.md`
- Status (Partial Implementation, Blocked, Documented)
- What's Built vs. Current Limitations
- Future Development Tasks organized by phase
- Decision points and dependencies
- Links to code and documentation

**Integration**:
- Updates `docs/future-enhancements.md` - Main future developments document
- Creates detailed docs in `docs/FUTURE-DEVELOPMENT/` if needed
- Links to code files, agents, and related documentation
- Follows established format and priority guidelines

**Resources**:
- `skill.md` - Main skill definition
- `instructions.md` - Documentation process and guidelines
- `resources.md` - Format templates and examples

**Time Saved**: Ensures incomplete work is properly documented and can be picked up later without losing context

---

## How Skills Work

### Trigger Mechanism
Skills activate automatically when Claude detects relevant context:

```
User: "How's the Smythson account performing this week?"
↓
Claude recognizes: account name + performance question
↓
Triggers: google-ads-campaign-audit skill
↓
Skill loads: CONTEXT.md, audit templates, ROK framework
↓
Claude: Pulls data via MCP and generates comprehensive audit
```

### Progressive Context Loading
Skills use three-level disclosure:
1. **Metadata** - Always loaded (skill name, triggers)
2. **Instructions** - Loaded when triggered (how to execute)
3. **Resources** - Loaded as needed (templates, references)

This is far more efficient than MCP servers that "explode your context window on bootup."

### Integration with MCP
Skills work seamlessly with your configured MCP servers:
- **Google Ads MCP**: Pull live account data via GAQL
- **Google Sheets MCP**: Export analysis to sheets
- **Google Analytics MCP**: Cross-reference GA4 data

### Composability
Skills can call other skills:
- **GAQL Builder** → used by **Campaign Audit** for data queries
- **CSV Analyzer** → used for exported report analysis
- **All skills** → can use MCP servers and slash commands

---

## Usage Examples

### Example 1: Quick Campaign Review
```
You: "Show me Devonshire's Shopping campaign performance"

Claude (using campaign-audit skill):
- Loads Devonshire CONTEXT.md
- Triggers GAQL query builder for performance data
- Uses Google Ads MCP to pull last 7 days
- Generates executive summary with insights
- Provides 3-5 recommendations
```

### Example 2: Data Analysis
```
You: "Analyze this product performance CSV I just exported"

Claude (using csv-analyzer skill):
- Detects CSV contains product data
- Calculates ROAS, CTR for each product
- Identifies top 10 and bottom 10 products
- Flags anomalies and trends
- Recommends budget reallocations
```

### Example 3: Query Building
```
You: "I need impression share data by campaign with budget lost IS"

Claude (using gaql-query-builder skill):
- Constructs appropriate GAQL query
- Validates resource and fields
- Offers to execute via MCP
- Formats results in readable table
```

### Example 4: Keyword Cleanup
```
You: "Find wasted spend keywords in the Smythson Search campaigns"

Claude (using keyword-audit skill):
- Pulls keyword performance data
- Identifies high-spend, zero-conversion keywords
- Groups irrelevant search terms
- Generates negative keyword list
- Provides bulk upload CSV
```

---

## Skill vs Agent vs Command

Understanding when to use each:

| Feature | Skills | Agents | Slash Commands |
|---------|--------|--------|----------------|
| **Trigger** | Auto (by Claude) | Scheduled | Manual |
| **Context** | Progressive | N/A | Full |
| **Use Case** | Interactive analysis | Background monitoring | One-off tasks |
| **Example** | Campaign audit | Daily performance alert | Generate commit message |

**Your Setup**:
- **Agents** (35 running): Background monitoring, data fetching, alerts
- **Skills** (12 directory + 2 standalone = 14 total): Interactive analysis when working with Claude
- **MCP Servers** (5 configured): External data access (Google Ads, GA4, etc.)

All three work together! Agents monitor in the background, skills activate during conversations, MCP provides data access.

---

## File Structure

```
.claude/
└── skills/
    ├── README.md                           # This file
    ├── gaql-query-builder/
    │   ├── skill.md                        # Skill definition
    │   ├── query-reference.md              # GAQL fields reference
    │   └── common-patterns.md              # Query templates
    ├── csv-analyzer/
    │   ├── skill.md                        # Skill definition
    │   ├── metric-definitions.md           # Metrics explained
    │   └── analysis-framework.md           # Analysis methodology
    ├── google-ads-campaign-audit/
    │   ├── skill.md                        # Skill definition
    │   ├── audit-templates.md              # Report templates
    │   └── common-issues.md                # Troubleshooting
    ├── google-ads-keyword-audit/
    │   ├── skill.md                        # Skill definition
    │   ├── negative-keyword-guide.md       # Negative keywords
    │   └── match-type-guide.md             # Match types
    ├── email-draft-generator/ ⭐ NEW
    │   ├── skill.md                        # Skill definition
    │   ├── client-preferences.md           # Client-specific styles
    │   └── british-vs-american-english.md  # Spelling reference
    ├── text-message-draft-generator/ ⭐ NEW
    │   └── skill.md                        # Skill definition
    └── devonshire-monthly-report/ ⭐ NEW
        └── skill.md                        # Skill definition
    ├── task-sync/ ⭐ NEW
    │   └── skill.md                        # Skill definition
    ├── daily-summary-email/ ⭐ NEW
    │   └── skill.md                        # Skill definition
    └── weekly-summary-email/ ⭐ NEW
        └── skill.md                        # Skill definition
    └── markdown-browser-display/ ⭐ NEW
        └── skill.md                        # Skill definition
    └── backup-tasks/ ⭐ NEW
        └── skill.md                        # Skill definition
    └── restore-tasks/ ⭐ NEW
        └── skill.md                        # Skill definition

---

## Testing Skills

To verify skills are working:

### Test 1: GAQL Builder
```
You: "Build me a GAQL query for campaign performance last 7 days"
Expected: Claude constructs query with proper syntax
```

### Test 2: CSV Analyzer
```
You: "I have a campaign performance CSV to analyze" [attach file]
Expected: Claude automatically analyzes and provides insights
```

### Test 3: Campaign Audit
```
You: "Audit the Smythson account for last week"
Expected: Claude triggers full audit with ROK framework
```

### Test 4: Keyword Audit
```
You: "Find wasted spend keywords in Search campaigns"
Expected: Claude identifies high-spend zero-conversion keywords
```

---

## ROK Framework Integration

All analysis skills implement ROK's proven methodologies from:
`roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md`

### Key Principles
1. **Actionable-Only Focus** - Skip stable metrics, show what needs attention
2. **Relative Benchmarking** - Use account average × multipliers
3. **Root Cause Analysis** - Beyond metrics to diagnose issues
4. **Business Language** - Revenue impact, not just ad metrics
5. **Prioritized Actions** - 3-5 specific recommendations

### Thresholds Used
- **Significant change**: ±15%
- **Critical change**: ±30%
- **Waste multiplier**: 0.7 × account average
- **Opportunity multiplier**: 1.3 × account average
- **Excellent ROAS**: >4.0
- **Poor ROAS**: <1.5

---

## Customization

To modify skills:

1. **Edit skill.md** - Change trigger patterns or instructions
2. **Add resources** - Create new reference files
3. **Adjust thresholds** - Modify benchmarks for specific clients
4. **Add templates** - Create client-specific audit formats

Skills automatically reload when files are edited.

---

## Troubleshooting

### Skill Not Triggering
- Check trigger patterns in `skill.md`
- Ensure file is in correct location
- Verify Claude Code can access `.claude/skills/`
- Restart Claude Code

### MCP Not Connected
- Check `.mcp.json` configuration
- Verify credentials are valid
- Run OAuth flow if needed
- See `docs/MCP-SERVERS.md`

### Wrong Data Retrieved
- Check GAQL query syntax
- Verify customer_id is correct
- Ensure date ranges are valid
- Check campaign/resource status filters

---

## Related Documentation

- **Agents System**: `agents/README.md` - Background automation
- **MCP Servers**: `docs/MCP-SERVERS.md` - Data integrations
- **Audit System**: `docs/GOOGLE-ADS-AUDIT-SYSTEM.md` - Scheduled audits
- **ROK Framework**: `roksys/knowledge-base/rok-methodologies/` - Analysis methods
- **8020Brain Analysis**: `docs/8020BRAIN-ANALYSIS-REPORT.md` - Mike's system review

---

## Credits

Skills adapted from Mike Rhodes' 8020Brain template with enhancements for:
- ROK analysis framework integration
- Client-specific context loading
- Google Ads MCP server integration
- Multi-client agency workflow
- Automated audit template generation

**Original source**: Mike Rhodes (8020Brain)  
**Adapted by**: Pete Empson / ROK  
**Date**: November 5, 2025

---

## Quick Reference

| Task | Skill to Use |
|------|--------------|
| Build GAQL query | gaql-query-builder |
| Analyze CSV export | csv-analyzer |
| Account performance review | google-ads-campaign-audit |
| Find wasted keywords | google-ads-keyword-audit |
| Impression share analysis | google-ads-campaign-audit |
| Product performance review | google-ads-campaign-audit + csv-analyzer |
| Search term cleanup | google-ads-keyword-audit |
| Budget recommendations | google-ads-campaign-audit |
| **Draft client email** | **email-draft-generator** ⭐ |
| **Draft text message** | **text-message-draft-generator** ⭐ |
| **Devonshire monthly report** | **devonshire-monthly-report** ⭐ |
| **WordPress blog management** | **wordpress-blog-manager** ⭐ |
| **Document incomplete work** | **future-development-documenter** ⭐ |
| **Sync tasks manually** | **task-sync** ⭐ |
| **Send daily summary email** | **daily-summary-email** ⭐ |
| **Send weekly summary email** | **weekly-summary-email** ⭐ |
| **Display markdown in browser** | **markdown-browser-display** ⭐ |
| **Verify outstanding tasks** | **task-verification** ⭐ |
| **Backup tasks immediately** | **backup-tasks** ⭐ |
| **Restore tasks from backup** | **restore-tasks** ⭐ |
| **Generate weekly report (single client)** | **google-ads-weekly-report** ⭐ |
| **Generate Clear Prospects reports (3 brands)** | **clear-prospects-weekly-reports** ⭐ |

---

## Time Savings Summary

**Email Draft Generator**: ~10-15 minutes per email
- Before: Manual drafting, formatting, spell-checking
- After: Auto-triggered, formatted, ready to send

**Text Message Draft Generator**: ~5-10 minutes per text message
- Before: Manual drafting, formatting, checking length
- After: Auto-triggered, concise, ready to send

**Devonshire Monthly Report**: ~2.5 hours per month
- Before: 3 hours (data queries, tables, analysis, slides)
- After: 20 minutes (review and customize)

**Google Ads Text Generator**: ~5-10 minutes per launch
- Before: Remembering commands, navigating directories, troubleshooting
- After: Auto-triggered launch with error handling

**Total Estimated Monthly Savings**: ~5-8 hours (across all clients and reports)

**WordPress Blog Manager**: Instant access to WordPress credentials and URLs
- Before: Searching through files for WordPress info
- After: Auto-triggered skill provides all access information

---

### 14. Task Sync ⭐ NEW
**Location**: `.claude/skills/task-sync/`
**Purpose**: Manually synchronize tasks between local todo files and Google Tasks
**Triggers**: When discussing syncing tasks, updating task status, or refreshing task synchronization

**Use Cases**:
- "Sync my tasks now"
- "Update tasks from Google Tasks"
- "Refresh task synchronization"
- "Sync todos manually"
- "Force a task sync"

**Capabilities**:
- Runs both sync scripts:
  - `tasks-monitor.py` - Syncs Google Tasks → Local files
  - `sync-todos-to-google-tasks.py` - Syncs Local files → Google Tasks
- Ensures bi-directional synchronization is current
- Reports sync results and any errors
- Useful for immediate updates or troubleshooting

**What Gets Synced**:
- Task completion status
- Title changes
- Notes/details changes
- Due date changes
- Task uncompletion (moved back to active)

**Integration**:
- Uses `agents/system/tasks-monitor.py` for Google → Local sync
- Uses `agents/system/sync-todos-to-google-tasks.py` for Local → Google sync
- References `shared/google_tasks_client.py` for Google Tasks API
- Tracks sync state via JSON files

**Resources**:
- `skill.md` - Main skill definition
- References `docs/BI-DIRECTIONAL-TASK-SYNC.md` for full documentation

**Time Saved**: Instant manual sync vs waiting for hourly automatic sync

---

### 15. Daily Summary Email ⭐ NEW
**Location**: `.claude/skills/daily-summary-email/`
**Purpose**: Send manual daily briefing email with client work, calendar events, tasks, and performance updates
**Triggers**: When asking to send daily summary, daily briefing, or today's briefing

**Use Cases**:
- "Send daily summary"
- "Send daily briefing"
- "Run daily briefing email"
- "Generate daily summary"
- "Daily briefing"
- "Send today's briefing"

**Capabilities**:
- Generates comprehensive daily briefing
- Runs client work generator (creates Google Tasks)
- Collects calendar events, tasks, performance data
- Generates AI-powered executive summary
- Sends formatted email via Gmail SMTP
- Creates markdown and HTML files locally

**What's Included**:
- Client work for today (from Google Tasks)
- Calendar events
- Performance anomalies
- Pending tasks
- Recent meetings
- Weekly performance summary
- AI inbox activity
- Agent status

**Integration**:
- Uses `agents/reporting/daily-briefing.py`
- Integrates with Google Tasks (client work)
- Uses Google Calendar API
- Requires Gmail SMTP credentials

**Resources**:
- `skill.md` - Main skill definition

**Time Saved**: Quick manual trigger vs waiting for 7 AM automatic run

---

### 16. Weekly Summary Email ⭐ NEW
**Location**: `.claude/skills/weekly-summary-email/`
**Purpose**: Send manual weekly business summary email with strategic priorities, performance data, meeting notes, and knowledge base updates
**Triggers**: When asking to send weekly summary, weekly briefing, or week's summary

**Use Cases**:
- "Send weekly summary"
- "Send weekly briefing"
- "Run weekly summary email"
- "Generate weekly summary"
- "Weekly briefing"
- "Send week's summary"

**Capabilities**:
- Generates comprehensive weekly business summary
- Runs weekly client strategy generator
- Gathers knowledge base documents from last 7 days
- Fetches upcoming tasks for week ahead
- Loads client performance data
- Includes Granola meeting imports
- Sends formatted email via Gmail API

**What's Included**:
- Strategic priorities (2-4 per client)
- Upcoming tasks for week ahead
- Performance data from last week
- Meeting notes imported from Granola
- Knowledge base updates
- AI-generated insights and takeaways

**Integration**:
- Uses `agents/reporting/kb-weekly-summary.py`
- Integrates with weekly strategy generator
- Uses Google Tasks MCP
- Uses Gmail API (OAuth authentication)

**Resources**:
- `skill.md` - Main skill definition

**Note**: Separate from weekly news digest (which covers industry news and AI newsletters)

**Time Saved**: Quick manual trigger vs waiting for Monday 8:30 AM automatic run

---

### 17. Markdown Browser Display ⭐ NEW
**Location**: `.claude/skills/markdown-browser-display/`
**Purpose**: Display markdown files as formatted HTML in a browser window
**Triggers**: When asking to display markdown files in browser or view files as HTML

**Use Cases**:
- "Display this on a browser"
- "Show this in browser"
- "Open this in browser"
- "Display [filename] in browser"
- "View [filename] in browser"
- "Render markdown in browser"
- "Show markdown as HTML"

**Capabilities**:
- Converts markdown to HTML with beautiful styling
- Automatically opens in default browser
- Handles code blocks, tables, lists, and all markdown features
- Applies professional CSS styling
- Works with any markdown file in workspace

**What It Does**:
1. Identifies markdown file (from context, file path, or currently open file)
2. Converts markdown to HTML using markdown library
3. Applies CSS styling for readability
4. Creates temporary HTML file
5. Opens in default browser automatically

**Integration**:
- Works with any markdown file
- Uses Python `markdown` library
- Uses Python `webbrowser` module
- Creates temporary HTML files

**Resources**:
- `skill.md` - Main skill definition
- `shared/scripts/display_markdown_in_browser.py` - Conversion script

**Time Saved**: Quick browser preview vs manually converting or opening raw markdown

---

### 18. Task Verification ⭐ NEW
**Location**: `.claude/skills/task-verification/`
**Purpose**: On-demand verification of Google Tasks using automated pre-verification system
**Triggers**: When asking to verify tasks, check tasks, or re-verify outstanding work

**Use Cases**:
- "Verify all outstanding tasks"
- "Verify tasks for Superspace"
- "Check all urgent verification tasks"
- "Verify budget tasks across all clients"
- "Re-verify Smythson campaign status tasks"

**Capabilities**:
- Loads tasks from Google Tasks API
- Identifies verifiable tasks (budget checks, ROAS verification, campaign status)
- Runs batch verification with intelligent API call batching
- Presents results grouped by status (✅ Success, ⚠️ Warning, ❌ Error)
- Offers to mark verified tasks as complete
- Logs verification data to CONTEXT.md and tasks-completed.md

**Verification Types**:
- **Budget Checks**: Daily budget levels and actual spend
- **Campaign Status**: ENABLED/PAUSED state verification
- **Performance Thresholds**: ROAS/CPA vs target thresholds
- **Settings Verification**: Bid strategy settings validation

**Filtering Options**:
- By client: "Verify all [client] tasks"
- By priority: "Verify urgent tasks"
- By verification type: "Check all budget tasks"
- All verification tasks: "Verify all outstanding tasks"

**API Efficiency**:
- Batching reduces API calls by 40-80%
- One API call per client per data type
- Cached data reused for multiple verifications

**Integration**:
- Uses `shared/scripts/task_verifier.py` module
- Integrates with Google Tasks MCP
- Uses Google Ads MCP for verification queries
- Logs results to client CONTEXT.md files

**Resources**:
- `skill.md` - Main skill definition
- References `docs/TASK-PRE-VERIFICATION-PROTOTYPE.md` for system architecture

**Time Saved**: ~5-10 minutes per verification session (automated batch verification vs manual API queries)

---

### 19. OAuth Token Refresh ⭐ NEW
**Location**: `.claude/skills/oauth-refresh/`
**Purpose**: Re-authorize OAuth tokens for Google services that require user authentication
**Triggers**: When OAuth browser popups appear or LaunchAgents fail with authentication errors

**Use Cases**:
- "Refresh OAuth tokens"
- "Fix Google Tasks authentication"
- "Re-authorize Google Drive access"
- When LaunchAgents show exit code 78 (authentication error)

**What It Does**:
1. Checks current OAuth token status and expiry
2. Identifies which services need re-authorization
3. Runs setup script to open browser windows
4. Stores refresh tokens that auto-renew indefinitely
5. Verifies tokens are properly configured

**Services Covered**:
- ✅ **Google Tasks** - Required (API doesn't support service accounts)
- ✅ **Google Drive** - Optional (easier than sharing files with service account)
- ✅ **Google Photos** - Required if used (API only works with OAuth)

**Not Needed For**:
- Google Sheets (uses service account)
- Google Ads (uses YAML config)
- Gmail/Email Sync (uses service account)

**Key Features**:
- Detects failed LaunchAgents (exit code 78)
- Tests token refresh capability
- Explains which services need OAuth vs service accounts
- Verifies connection after setup

**Auto-Refresh Behavior**:
- Access tokens refresh every hour (automatic)
- Refresh tokens renew with each use (automatic)
- As long as LaunchAgents run regularly, tokens never expire
- Only need to re-run if: tokens revoked manually or 6+ months unused

**Resources**:
- `skill.md` - Main skill definition
- References `docs/OAUTH-TO-SERVICE-ACCOUNT-MIGRATION.md` for technical details
- Uses `shared/scripts/setup-oauth-once.sh` setup script

**Time Saved**: ~10-15 minutes per OAuth issue (automated diagnosis + guided setup vs manual troubleshooting)

---

### 20. Backup Tasks ⭐ NEW
**Location**: `.claude/skills/backup-tasks/`
**Purpose**: Run critical tasks backup immediately and verify success
**Triggers**: When asking to backup tasks, save tasks, or create task backup

**Use Cases**:
- "Backup my tasks now"
- "Save tasks to backup"
- "Create a task backup before making changes"
- "Run critical tasks backup"
- "Backup tasks immediately"

**Capabilities**:
- Runs critical tasks backup script (`backup-tasks-critical.sh`)
- Creates 37KB backup in ~1 second
- Syncs to iCloud Drive automatically
- Verifies backup creation and shows location
- Reports backup size and timestamp
- Shows next automatic backup time

**What Gets Backed Up**:
- All `clients/*/tasks.json` files
- All `clients/*/tasks-completed.md` files
- `roksys/spreadsheets/rok-experiments-client-notes.csv`

**Integration**:
- Uses `shared/scripts/backup-tasks-critical.sh`
- Syncs to iCloud Drive: `PetesBrain-Backups/critical-tasks/`
- Keeps last 20 backups (5 days worth at 6-hour intervals)

**Resources**:
- `skill.md` - Main skill definition
- References `docs/BACKUP-SYSTEM.md` for backup system documentation

**Time Saved**: ~30 seconds per backup (automated verification vs manual command execution)

---

### 21. Restore Tasks ⭐ NEW
**Location**: `.claude/skills/restore-tasks/`
**Purpose**: Restore tasks from critical backup when task files are lost or corrupted
**Triggers**: When task files are deleted, corrupted, or need to be restored

**Use Cases**:
- "Restore tasks from backup"
- "Recover deleted task files"
- "Restore tasks to earlier version"
- "Roll back task changes"
- "Recover task data"

**Capabilities**:
- Lists available task backups (last 20)
- Shows backup timestamps and age
- Confirms before restoring (destructive operation)
- Creates safety backup of current state (optional)
- Restores selected backup
- Verifies restoration success
- Supports selective restore (one client only)

**Safety Features**:
- Always asks for confirmation before restoring
- Shows which backup will be used
- Optional safety backup of current state
- Can restore specific client vs all clients
- Verification checks after restoration

**What Gets Restored**:
- Only task files: tasks.json, tasks-completed.md, experiment spreadsheet
- Everything else unchanged (CONTEXT.md, emails, meetings, etc.)

**Integration**:
- Restores from iCloud Drive backups
- Uses `tar` extraction (selective or full)
- Verifies file integrity after restoration
- Reports detailed restoration results

**Resources**:
- `skill.md` - Main skill definition
- References `docs/BACKUP-SYSTEM.md` for backup system documentation

**Important Notes**:
- Destructive operation (replaces current task files)
- Always confirms with user first
- Can restore from any of last 20 backups (5 days)
- Alternative to restoring from full system backup

**Time Saved**: ~2-5 minutes per restoration (automated backup listing + verification vs manual tar commands)

---

### 22. Google Ads Weekly Report ⭐ NEW
**Location**: `.claude/skills/google-ads-weekly-report/`
**Purpose**: Generate comprehensive weekly Google Ads performance analysis for e-commerce clients
**Triggers**: When discussing weekly reports, Google Ads analysis, or performance reviews

**Use Cases**:
- "Weekly report for [client]"
- "Google Ads weekly analysis [client]"
- "Generate weekly performance report"
- "Create [client] weekly report"

**Capabilities**:
- Pulls account, campaign, product, and placement performance data
- Calculates ROAS, CPA, conversion rate, and week-over-week changes
- Identifies campaigns and products requiring attention (>15% change)
- Generates markdown and HTML reports with ROK branding
- Creates tasks automatically for P0 critical issues only
- Smart task creation with threshold criteria

**Report Sections**:
- Executive summary (account performance)
- Campaign breakdown (top performers + attention needed)
- Product performance (top 10, bottom 10, notable changes)
- Placement analysis (Shopping, YouTube, Display, Discover)
- Week-over-week trends
- Prioritized recommendations (P0-P3)

**Task Creation Logic** (Smart - Not Flooding):
- ✅ Creates tasks ONLY for P0 recommendations
- ✅ P0 MUST meet threshold criteria:
  - ROAS drop >20% WoW
  - Campaign with 0 conversions spending >£50/week
  - ROAS >15% below target
  - Identified waste >£100/month
- ❌ P1/P2/P3 recommendations stay in report (informational)
- 📊 Result: ~3-5 tasks/week from 16 clients (only critical issues)

**Integration**:
- Loads client CONTEXT.md for strategic context
- Uses Google Ads MCP for live data
- References experiment log for recent changes
- Saves to `clients/[client]/reports/weekly/`
- Updates `data/state/weekly-reports-generated.json`

**Resources**:
- `skill.md` - Main skill definition
- Adapted from GoMarble Prompt Library

**Time Saved**: ~30-45 minutes per weekly report (automated data extraction + analysis vs manual)

---

### 23. Clear Prospects Weekly Reports ⭐ NEW
**Location**: `.claude/skills/clear-prospects-weekly-reports/`
**Purpose**: Generate three separate weekly Google Ads reports for Clear Prospects' three brands
**Triggers**: When asking for "Clear Prospects weekly reports" (plural or singular)

**Use Cases**:
- "Clear Prospects weekly reports"
- "Clear Prospects weekly report"
- "Generate Clear Prospects reports"

**Capabilities**:
- Generates 3 complete brand-specific reports in one command
- Filters campaigns by brand prefix (CPL | HSG |, CPL | WBS |, CPL | BMPM |)
- Filters product data by Merchant Centre ID
- Brand-specific header colors in HTML reports
- Individual task creation per brand
- Multi-brand summary showing all three at once

**Brands Covered**:
1. **HappySnapGifts (HSG)** - Photo gifts, face masks, bunting
   - MC ID: 7481296
   - Target ROAS: ~115%
2. **WheatyBags (WBS)** - Wheat bags, hot water bottles, heat packs
   - MC ID: 7481286
   - Target ROAS: ~130%
3. **British Made Promotional Merchandise (BMPM)** - B2B promotional products
   - MC ID: 7522326
   - Target ROAS: 70%

**Output Files** (per brand):
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-hsg-weekly-report.md`
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-hsg-weekly-report.html`
- (Same for wbs and bmpm)

**Multi-Brand Summary**:
Shows performance snapshot for all 3 brands with status indicators:
- ✅ On target
- ⚠️ Needs attention
- 🔴 Critical

**Brand-Specific Context**:
- HSG: Face masks channel optimization (Search vs Shopping)
- WBS: Budget utilization and impression share monitoring
- BMPM: Profitability restructuring (new 70% ROAS target)

**Integration**:
- Same data logic as google-ads-weekly-report skill
- Client-specific filtering for multi-brand account
- Brand-aware task creation with prefix tags
- All reports use Clear Prospects account (6281395727)

**Resources**:
- `skill.md` - Main skill definition
- References Clear Prospects CONTEXT.md for brand context

**Time Saved**: ~1.5-2 hours per week (3 reports automated vs manual generation)

---

### 24. Google Ads Landing Page Reports ⭐ NEW
**Location**: `.claude/skills/google-ads-landing-page-reports/`
**Purpose**: Generate comprehensive landing page performance reports for any Google Ads client
**Triggers**: When asking for "landing page reports", "landing page performance", or "landing page analysis"

**Use Cases**:
- "Landing page reports for [client]"
- "Generate landing page reports for National Design Academy"
- "Landing page performance for Smythson"
- "Analyse landing pages for Tree2mydoor"

**Capabilities**:
- **Universal Script**: Works for any client with Google Ads account
- **Three Comprehensive Reports**: Overall statistics, PMax asset groups, Search campaigns
- **Automatic Customer ID Detection**: Reads from client CONTEXT.md
- **Flexible Date Ranges**: Default 90 days, or custom ranges
- **OAuth Handled Automatically**: No manual authentication needed
- **Production-Tested**: Successfully used for National Design Academy P0 task

**Reports Generated**:

1. **Report 1: Overall Landing Page Statistics**
   - Aggregates performance by unique landing page URL
   - Covers ALL campaigns (PMax, Search, Display, etc.)
   - Metrics: Impressions, Clicks, CTR, Conversions, Conv Rate, Cost, Conv Value, ROAS
   - Sorted by conversions (highest first)
   - Typical output: 50-500 unique landing pages

2. **Report 2: Performance Max Landing Pages**
   - Shows which asset groups use which landing pages
   - Campaign → Asset Group → Landing Page hierarchy
   - Identifies paused vs enabled asset groups
   - Useful for auditing PMax configuration
   - Typical output: 20-100 asset group records

3. **Report 3: Search Campaign Landing Pages**
   - Granular ad group level analysis
   - Campaign → Ad Group → Landing Page with full metrics
   - Only enabled ads in enabled/paused campaigns
   - Very detailed (can be 1000+ rows for large accounts)
   - Useful for Search campaign deep dives

**Command Line Usage**:
```bash
# Basic (last 90 days)
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  1994728449 \
  national-design-academy

# Custom date range
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  8573235780 \
  smythson \
  --date-from 2024-10-01 \
  --date-to 2024-12-31

# Last 30 days
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  1234567890 \
  client-slug \
  --days 30

# Managed account
.claude/skills/google-ads-landing-page-reports/generate_landing_page_reports.py \
  1234567890 \
  client-slug \
  --manager-id 9876543210
```

**Output Location**:
```
clients/{client-slug}/reports/landing-page-analysis/
  ├── report1-landing-page-statistics-90d.csv
  ├── report2-pmax-landing-pages-90d.csv
  └── report3-search-landing-pages-90d.csv
```

**Technical Details**:
- **API Version**: Google Ads API v22
- **Query Resources**: `landing_page_view`, `asset_group`, `ad_group_ad`
- **Authentication**: OAuth via shared Google Ads MCP server credentials
- **Performance**: Typically completes in 10-60 seconds depending on account size
- **Critical Pattern**: PMax queries must query campaigns first, then asset groups per campaign (avoids 0 results issue)

**Common Issues Solved**:
1. **Wrong Customer ID**: Always reads from CONTEXT.md (no more guessing)
2. **Empty PMax Results**: Uses correct two-step query pattern
3. **OAuth Errors**: Automatic token refresh handled by helper
4. **Managed Accounts**: Supports optional `manager-id` parameter

**Integration**:
- Uses Google Ads MCP server OAuth helper (`oauth.google_auth`)
- Reads client platform IDs from CONTEXT.md
- Auto-creates report directory if not exists
- British English output (analyse, optimise)

**Resources**:
- `skill.md` - Complete technical documentation (500+ lines)
- `generate_landing_page_reports.py` - Universal Python script with CLI args
- `README.md` - Quick reference guide

**Real-World Example**:
Used successfully for National Design Academy's P0 task (Monday 2nd Dec call with Paul Riley):
- Report 1: 154 unique landing pages
- Report 2: 59 PMax asset groups across 15 campaigns
- Report 3: 1,142 Search ad records
- Generated in ~15 seconds

**Time Saved**: ~30-45 minutes per report request (vs manual export + formatting)

---

**Status**: ✅ All 24 skills operational and integrated with MCP servers
**Last Updated**: November 28, 2025

