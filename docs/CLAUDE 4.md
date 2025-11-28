# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pete's Brain** is a collection of AI-powered marketing and advertising tools developed by **Rok Systems** (commonly abbreviated as **Roksys**). The project follows a modular architecture where each tool is self-contained under `tools/[tool-name]/`, with its own dependencies, documentation (TOOL_CLAUDE.md), and can be run independently.

**Company Information**:
- **Full Name**: Rok Systems
- **Common Name**: Roksys
- **Website**: https://roksys.co.uk
- **Tagline**: Digital Marketing
- **Brand Colors**: Roksys Green (#6CC24A), Roksys Gray (#808080)
- **Brand Assets**: `/shared/assets/branding/` (logo, guidelines, CSS templates)

**Reporting Standards**:
- **ROAS Format**: Always express ROAS as a percentage (e.g., 400%, 292%, 550%)
  - NOT as £X.XX format (e.g., NOT £4.00, £2.92, £5.50)
  - This applies to ALL clients, reports, emails, and documentation
  - Conversion: ROAS £4.00 = 400% (multiply by 100)

**Email Output Format** (established Nov 2025):
- **Format**: HTML (not markdown) with proper `<strong>` tags for bold
- **Filename**: `email-draft-YYYY-MM-DD-[topic].html` in client folder
- **Location**: `clients/[client-name]/email-draft-YYYY-MM-DD-[topic].html`
- **Spelling**: British English for UK clients (analyse not analyze, customisation not customization, emphasise not emphasize)
- **Styling**: Tight spacing for readability
  - `line-height: 1.4` (not 1.6+)
  - Paragraph margins: `6px` (not 10px+)
  - List margins: `6px` (not 10px+)
  - Font: System fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`)
- **Delivery**: Auto-open HTML file in browser for copy/paste into Apple Mail
- **Reason**: Ensures clean formatting when copying from browser to email client, avoids color scheme issues

## Quick Reference

**Common Commands**:
- **Check automated workflows**: `launchctl list | grep petesbrain`
- **View workflow logs**: `cat ~/.petesbrain-[workflow-name].log`
- **Run script manually**: `python3 shared/scripts/[script-name].py`
- **Process KB inbox**: `python3 shared/scripts/knowledge-base-processor.py`
- **Check MCP servers**: Review `.mcp.json` for active servers
- **Reload LaunchAgent**: `launchctl unload ~/Library/LaunchAgents/com.petesbrain.[name].plist && launchctl load ~/Library/LaunchAgents/com.petesbrain.[name].plist`

**Standard Python Setup** (all tools/scripts):
```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Architecture

**Modular Tool System**: Each tool under `tools/` is completely independent with its own:
- Virtual environment and `requirements.txt`
- `TOOL_CLAUDE.md` - detailed architecture and implementation notes
- `README.md` - user-facing documentation
- Documentation files in `docs/[tool-name]/`

**Critical Pattern**: The Flask web apps use a **global variable pattern** instead of sessions:
```python
latest_result = None  # Global variable stores latest generation

@app.route('/analyze')
def analyze():
    global latest_result
    latest_result = generated_data  # Store in global
    return jsonify(result)

@app.route('/get_latest_data')
def get_data():
    global latest_result
    return jsonify(latest_result)  # Retrieve from global
```

This means the app is **single-user** and data persists only in memory during runtime.

## Common Development Commands

See individual tool README files for detailed commands. Most tools follow this pattern:
- `./start.sh` - Start the tool
- `./stop.sh` - Stop the tool (if applicable)
- `requirements.txt` - Python dependencies
- `.venv/` - Python virtual environment (standard across all tools)

**Environment Variables**: Required API keys should be set in `~/.bashrc` or `~/.zshrc`:
- `ANTHROPIC_API_KEY` - Required for Claude API (knowledge base processor, news monitors, copywriter)
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google service account JSON (for MCP servers)
- Tool-specific variables documented in each tool's README

**Managing Automated Workflows**:
```bash
# Check status of all LaunchAgents
launchctl list | grep petesbrain

# View logs for a specific workflow
cat ~/.petesbrain-[workflow-name].log

# Reload a LaunchAgent after changes
launchctl unload ~/Library/LaunchAgents/com.petesbrain.[name].plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.[name].plist

# Run a workflow manually (example: knowledge base processor)
python3 shared/scripts/knowledge-base-processor.py
```

## Current Tools

Each tool is self-contained under `tools/[tool-name]/` with its own TOOL_CLAUDE.md documentation.

- **Google Ads Generator** - Generate Google Ads copy optimized for ROK's specifications (Active, production-ready)
- **Granola Meeting Importer** - Auto-import meeting transcripts from Granola AI (Active, production-ready)
- **Product Impact Analyzer** - Analyze impact of product changes on campaign performance (Active, production-ready)
  - **Product Hero Labelizer** - Classifies products as Heroes/Sidekicks/Villains/Zombies based on performance
  - **Label Tracking** - Daily snapshots track label transitions to identify performance patterns
  - **Weekly Reports** - Automated email reports with product change analysis and label validation
  - **Daily Workflow**: Label snapshots taken daily via `./setup_label_snapshots.sh`, weekly reports auto-generated and emailed
  - **Reports Location**: `clients/[client]/reports/product-impact-analyzer/`
- **Monthly Report Generator** - Generate monthly Google Slides presentations for Devonshire Hotels Paid Search (Active, production-ready)
- **Report Generator** - Generate interactive reports with data visualizations (Prototype, future development)

**Documentation**: See each tool's `TOOL_CLAUDE.md` for detailed architecture and `README.md` for usage.

## Adding New Tools

1. Create `tools/[tool-name]/` directory
2. Add `TOOL_CLAUDE.md` with architecture details specific to that tool
3. Add `requirements.txt` for dependencies
4. Add `README.md` for user documentation
5. Add `QUICKSTART.md` for setup instructions (optional but recommended)
6. Place detailed docs in `docs/[tool-name]/`
7. Update this file's "Current Tools" section

## Client Workflows

### AI Discoverability Files (llms.txt & agents.txt)

**Location**: `clients/[client-name]/llms.txt` and `clients/[client-name]/agents.txt`
**Purpose**: Make client businesses discoverable by AI assistants like ChatGPT, Claude, and Gemini

**When to create**: When a client needs to improve their AI discoverability for customer support, lead generation, or brand awareness.

**Process**:
1. User provides client website URL
2. Research website using WebFetch to understand business, products, audience
3. Ask 10 key questions about:
   - Value proposition
   - Ideal customers
   - Top products/services
   - Common customer questions
   - Differentiators
   - Customer journey
   - Problems solved
   - Important pages
4. Create `llms.txt` (500-1500 words):
   - Factual company overview
   - Products/services with descriptions
   - Target audience and use cases
   - Key differentiators
   - Important page links
5. Create `agents.txt` (800-2000 words):
   - AI agent guidance
   - 15-20 common customer Q&As
   - User workflows
   - Key terminology
   - Best practices for helping customers
   - Troubleshooting guidance
6. Provide implementation instructions:
   - Upload to website root directory
   - Verify accessibility at `https://domain.com/llms.txt` and `https://domain.com/agents.txt`
   - Testing with AI assistants
   - Maintenance schedule (quarterly reviews)

**Tone**: Factual, not promotional. Clear, helpful, and structured for AI parsing.

**Files saved locally**: `clients/[client-name]/llms.txt` and `clients/[client-name]/agents.txt`

### Google Ads Client Analysis

**CRITICAL**: The **CONTEXT.md file is the beating heart of the client analysis system**. It must be maintained and referenced for every client interaction.

**Locations**:
- `roksys/spreadsheets/rok-experiments-client-notes.csv` - Experiment tracking
- `clients/[client-name]/CONTEXT.md` - **PRIMARY CLIENT KNOWLEDGE BASE**

**ADDING CONTEXT ON THE FLY**: The user can paste context directly into chat using these patterns:

1. **Simple format** (you choose section):
   ```
   Add to [client] context:
   [text to add]
   ```

2. **Specify section**:
   ```
   Add to [client] context - [section]:
   [text to add]
   ```

3. **Natural language**:
   - "Update Smythson CONTEXT.md: [text]"
   - "Add this note to Tree2mydoor: [text]"
   - "Save to Clear Prospects context: [text]"

**When you see these patterns**:
1. Identify the client name (match against existing client folders)
2. If section specified, add to that section; otherwise ask which section or use "Ad Hoc Notes"
3. Add the text with timestamp to CONTEXT.md
4. Update "Last Updated" date
5. Add to Document History table
6. Confirm what was added and where

**Section keywords to recognize**:
- "strategy" → Strategic Context
- "preference" or "communication" → Client Preferences
- "business" or "product" → Business Context
- "issue" or "problem" → Known Issues
- "learning" or "insight" → Key Learnings
- "campaign" → Campaign Notes
- "action" or "todo" → Action Items
- "contact" or "link" → Quick Reference

**MANDATORY WORKFLOW**: When working with any client, ALWAYS follow this process:

1. **DISCOVER all client content** (CRITICAL - DO NOT SKIP):
   ```bash
   # Use Bash to list all folders and files
   ls -la /Users/administrator/Documents/PetesBrain/clients/[client-name]/
   ```
   **IMPORTANT**: The client folder structure is NOT fixed. New folders may be added at any time:
   - Standard folders: emails/, meeting-notes/, documents/, briefs/, presentations/, spreadsheets/
   - New standard folders (Oct 2025): reports/, product-feeds/, scripts/
   - Custom folders: contracts/, proposals/, assets/, research/, etc.

   **You MUST discover and use ALL content**, regardless of folder name. If a new subfolder exists, read and analyze its contents.

2. **FIRST: Read CONTEXT.md** (CRITICAL - DO NOT SKIP):
   ```bash
   Read: /Users/administrator/Documents/PetesBrain/clients/[client-name]/CONTEXT.md
   ```
   This is your primary knowledge base. If it doesn't exist, create it using the template from `clients/_templates/CONTEXT.md`.

3. **Read completed tasks history**:
   ```bash
   Read: /Users/administrator/Documents/PetesBrain/clients/[client-name]/tasks-completed.md
   ```
   - This file tracks all completed tasks for this client
   - Review recent completions (last 30-60 days) to understand what work has been done
   - **CRITICAL**: Pay close attention to task notes - they contain important status information:
     * Caveats about completion (e.g., "completed but waiting for customer response")
     * Follow-up requirements or blockers
     * Context about why the task was done
     * Additional information not in the title
   - Use this to inform your analysis and avoid duplicate work
   - Reference task notes when discussing what's been done (e.g., "Budget analysis completed on Oct 28, but awaiting client approval per task notes")
   - If file doesn't exist, the client has no recorded completed tasks yet

4. **Read the experiment notes** (CRITICAL - THIS EXPLAINS PERFORMANCE CHANGES):
   ```bash
   Read: /Users/administrator/Documents/PetesBrain/roksys/spreadsheets/rok-experiments-client-notes.csv
   ```
   **Filter for the specific client and look for recent entries (last 30-60 days)**

   **Why this is critical**:
   - Explains performance spikes/drops (e.g., "Revenue jumped 40% on Oct 21" → Check what started that day)
   - Documents what was EXPECTED from each change (compare to actual results)
   - Provides context for account management decisions
   - Shows timeline of strategic changes (budget increases, ROAS adjustments, campaign launches)

   **When analyzing performance**:
   - Match date ranges in metrics to experiment dates
   - Compare actual outcomes to documented expectations
   - Reference specific experiments when explaining changes to user
   - Example: "The revenue spike on Oct 21 corresponds to the BMPM search campaign launch we logged in the experiment sheet"

5. **Check recent email communications**:
   ```bash
   Read: /Users/administrator/Documents/PetesBrain/clients/[client-name]/emails/
   ```
   - List emails and identify recent ones (last 30-60 days based on filename dates)
   - Read relevant emails about performance, requests, issues, or strategy discussions
   - Look for client concerns, budget discussions, stock issues, seasonal notes

6. **Review meeting notes**:
   ```bash
   Read: /Users/administrator/Documents/PetesBrain/clients/[client-name]/meeting-notes/
   ```
   - Check for recent meetings (last 30-60 days)
   - Read notes for strategic decisions, action items, or context about goals

   **IMPORTANT - Client Assignment Validation**:
   - Meeting notes are auto-imported by Granola and client assignment may be incorrect
   - When reading a meeting, check if it's actually about this client:
     * Does meeting discuss this client's business/products/campaigns?
     * Or is it a company/internal meeting that was mis-assigned?
   - If meeting appears to be mis-assigned:
     * Notify user: "This meeting appears to be about [actual topic] not [client]. Should I move it to roksys/meeting-notes/?"
     * User can run `./shared/scripts/review-meeting-client.sh` to correct assignments
   - Company meetings belong in `roksys/meeting-notes/` not client folders

7. **Check ALL other folders** (discovered in step 1):
   - Standard folders: documents/, briefs/, presentations/, spreadsheets/
   - **ANY custom folders** added by user (contracts/, proposals/, reports/, research/, etc.)
   - Read key files from ALL folders to understand complete client context
   - **CRITICAL**: Never assume folder structure is fixed - always discover what exists

8. **Analyze external factors and root causes**: When performance changes, investigate beyond account management actions:

   **Market & Competitive Factors:**
   - Check for mentions of competitors, industry changes, or market conditions in emails/meetings
   - Look for seasonality patterns (compare to same period last year if data available)
   - Consider economic factors mentioned in communications

   **Client Business Changes:**
   - Product launches, discontinuations, or stock shortages (often in emails)
   - Pricing changes or promotions
   - Website changes, redesigns, or technical issues
   - Business model or strategy shifts

   **Technical & Tracking Issues:**
   - Conversion tracking problems mentioned in communications
   - Website performance or speed issues
   - Checkout flow changes
   - Tag/pixel implementation issues

   **Google Ads Platform Changes:**
   - Check Knowledge Base (`roksys/knowledge-base/google-ads/platform-updates/`) for recent Google announcements
   - Algorithm updates or new features (may take 1-2 weeks to impact performance)
   - Policy changes affecting campaigns
   - Auction dynamics shifts
   - Smart Bidding learning period after platform changes
   - **Note**: Platform changes often have **delayed impact** - check updates from 2-4 weeks before the performance change
   - Cross-reference Knowledge Base articles with performance change dates

9. **Synthesize all context**: Use information from CONTEXT.md, completed tasks (including task notes!), **experiments**, emails, meetings, and ALL discovered folders to:

   **CRITICAL: Match performance changes to ALL available sources**:
   - When you see a performance spike/drop, CHECK ALL sources:
     * **Experiment notes (rok-experiments-client-notes.csv)** - Strategic change: what/why/expected outcome
     * **Completed tasks (tasks-completed.md)** - Tactical implementation: how/when/status
     * **Google Ads Change History** - Via MCP API or UI, see what actually changed in the account
     * **Knowledge Base** - Google platform updates (2-4 weeks prior for delayed impact)
     * **External factors** - Client business changes, market conditions

   **Why Google Ads Change History matters**:
   - Captures changes NOT logged in experiments (automatic Google changes, policy updates, disapprovals)
   - Shows exact timing of changes (down to the hour)
   - Reveals unintended changes (accidental edits, API changes, third-party tools)
   - Cross-validates experiment notes (confirms what was logged actually happened)
   - **Important**: Change history is NOT definitive - many factors affect performance beyond logged changes

   **Example combined analysis**:
   > "Revenue dropped 15% on Oct 20.
   > - Experiment notes: BMPM categories paused (expected -£200/week)
   > - Tasks: 3 ad groups paused Oct 19
   > - Change History: Confirms 3 ad groups paused Oct 19, 3:42 PM
   > - Actual: -£180/week ✓ within expected range"

   **Analysis framework** (check ALL sources):
   1. **Product-Level Performance** (CRITICAL for e-commerce - check FIRST):
      - Google Ads Shopping performance by product (via MCP GAQL queries)
      - Product Impact Analyzer reports (weekly analysis, product changes)
      - Merchant Center product status (disapprovals, out of stock)
      - Best/worst performing products (revenue, ROAS, clicks)
      - Product changes: additions, removals, price changes
      - **Why this matters**: Account-level metrics hide product-level stories. A 10% account revenue drop might be one bestseller going out of stock.

   2. **Account Changes** (verify what actually changed):
      - Google Ads Change History (via MCP or UI)
      - Experiment notes (strategic intent)
      - Completed tasks (implementation details)

   3. **Platform Evolution** (delayed 2-4 weeks):
      - Knowledge Base for Google platform updates
      - Algorithm changes, new features

   4. **External Factors**:
      - Client business changes (stock, pricing, website)
      - Market conditions, seasonality
      - Competitive landscape

   5. **Technical Issues**:
      - Conversion tracking problems
      - Website performance
      - Merchant Center disapprovals

   **Analysis process** (for e-commerce Shopping campaigns):
   1. **Start with product-level data** (most granular, most revealing):
      - Query Shopping performance by product via MCP
      - Identify which products drove the performance change
      - Check if top performers are still active, in stock, properly priced
      - Look for product additions/removals that explain account changes

   2. **Connect products to account changes**:
      - Cross-validate experiment notes against Google Ads change history
      - Check if experiments affected specific products or categories
      - Reference Product Impact Analyzer for product change timeline

   3. **Check platform and external factors**:
      - Knowledge Base for platform updates (2-4 weeks delayed)
      - Merchant Center for product disapprovals/stock issues
      - Client communications for business changes

   4. **Synthesize complete story**:
      - Separate into categories: (a) product changes, (b) account management, (c) platform, (d) external, (e) technical
      - **Lead with product insights**: "Revenue dropped 15% due to top product (SKU 287, £680/week) going out of stock"
      - Include account-level context: "This was flagged in Product Impact Analyzer and confirmed via Merchant Center"
      - Cite all sources with evidence

   **Important**: For e-commerce, ALWAYS drill down to product level before drawing conclusions. Account-level metrics can be misleading.

   **Example multi-source analysis**:

   **Example 1: Product-level cause (e-commerce)**:
   > "Revenue dropped 15% (£680/week) starting Oct 20.
   > - **Product Performance**: SKU 287 (Olive Tree Large) revenue dropped from £680/week to £0
   > - **Merchant Center**: Product 287 marked out of stock Oct 19
   > - **Product Impact Analyzer**: Flagged product removal Oct 20
   > - Change History: No account changes ✗
   > - Experiments: No strategic changes ✗
   > - Conclusion: Revenue drop caused by top-selling product going out of stock. Product 287 represented 15% of total account revenue."

   **Example 2: Platform update (with evidence)**:
   > "Performance improved 20% starting Oct 15.
   > - Product Performance: Improvement spread across all products (no single driver)
   > - Change History: No account changes Oct 10-20 ✗
   > - Experiments: No strategic changes ✗
   > - Knowledge Base: Smart Bidding update rolled out Oct 1 ✓
   > - Conclusion: Improvement aligns with Google Smart Bidding update (2-week learning period from Oct 1)."

   **Example 3: Unexplained (no evidence)**:
   > "Revenue improved 20% starting Oct 15.
   > - Product Performance: Improvement spread across top 10 products (no single driver)
   > - Change History: No account changes Oct 10-20 ✗
   > - Experiments: No strategic changes ✗
   > - Knowledge Base: No platform updates in prior 4 weeks ✗
   > - Merchant Center: No product additions or stock changes ✗
   > - Conclusion: Unable to determine cause from available data. Recommend monitoring to see if pattern continues and checking with client for undocumented changes."

   **CRITICAL**: Only cite specific factors when you have EVIDENCE (from emails, meetings, Knowledge Base, change history, etc.). Do NOT speculate about "possible" or "likely" causes without supporting data.

10. **UPDATE CONTEXT.md** (MANDATORY - DO NOT SKIP):

   After reading emails, meetings, and documents, **ALWAYS update CONTEXT.md** with new insights:

   **What to Extract and Add**:
   - Strategic decisions or changes in direction
   - New goals, KPIs, or targets mentioned
   - Client preferences or sensitivities discovered
   - Business changes (products, pricing, stock, website)
   - Technical issues or tracking problems
   - Performance patterns or anomalies
   - Successful or failed experiments/tests
   - Important dates or upcoming events
   - Client concerns or feedback
   - Competitive intelligence mentioned

   **How to Update**:
   - Use the Edit tool to add information to the appropriate section
   - Keep existing information - only add, don't remove (unless correcting errors)
   - Include dates for time-sensitive information
   - Cross-reference sources (e.g., "Per Oct 27 email, stock shortages...")
   - Update "Last Updated" date at the top
   - Add entry to "Document History" table at bottom

   **When to Update**:
   - After processing new emails (if they contain strategic/contextual info)
   - After reviewing meeting notes (always - meetings are high-value context)
   - After client communications reveal new information
   - After discovering important insights during analysis
   - When campaign structure or strategy changes

   **CONTEXT.md is the institutional memory - treat it as sacred. Every insight must be captured.**

**Client Folder Structure** (standardized as of Oct 30, 2025):

**Root Level** (only essential files):
- **`CONTEXT.md`** ⭐ - **PRIMARY KNOWLEDGE BASE** - Living document with strategic context, learnings, and insights
- **`tasks-completed.md`** ⭐ - **COMPLETED TASKS LOG** - Auto-generated log of all completed Google Tasks for this client
- `README.md` - (Optional) High-level client overview (business model, contacts, key facts)
- `llms.txt` / `agents.txt` - (Optional) AI discoverability files (if created)

**Standard Folders**:
- `emails/` - Email communications (markdown, dated filenames: YYYY-MM-DD_*.md)
- `meeting-notes/` - Meeting transcripts and notes (markdown)
- `briefs/` - Campaign briefs and project specs
- `documents/` - Strategy docs, written analysis, investigation notes (markdown)
- `presentations/` - Client presentations and slide decks
- `spreadsheets/` - Data exports and analysis spreadsheets
- `reports/` - **Strategy reports, performance analysis (HTML, PDF)** ⭐ NEW
  - `reports/q[X]-[year]/` - Quarterly reports grouped by period
  - `reports/pmax-analysis/` - Performance Max analysis reports
  - `reports/monthly/` - Monthly performance reports
  - `reports/ad-hoc/` - One-off analysis and investigations
- `product-feeds/` - **Product data, supplemental feeds (CSV, JSON)** ⭐ NEW
  - Active feeds at top level
  - Historical/working files in subdirectories by category (e.g., `card-holders/`, `travel-bags/`)
- `scripts/` - **Client-specific scripts and automation (Python, Bash)** ⭐ NEW

**Documentation**: See `clients/_templates/FOLDER-STRUCTURE.md` for complete standard and migration guidelines

**Additional Data Sources to Cross-Reference:**

When analyzing performance, proactively check these additional sources if available:

1. **Google Analytics (via MCP)**:
   - Use `mcp__google-analytics__*` tools to check website traffic trends
   - Compare Google Ads traffic to overall site traffic
   - Check conversion rate changes at the website level
   - Identify if issues are Google Ads-specific or site-wide

2. **Client Website (via WebFetch)**:
   - Check if products mentioned in campaigns are still available
   - Verify pricing matches ad copy
   - Look for site changes, promotions, or banners
   - Check if tracking pixels are present (GTM, Google Ads tags)

3. **Historical Google Ads Data**:
   - Compare current period to same period last year (seasonality)
   - Look for recurring patterns or anomalies
   - Check if similar changes happened before and what caused them

4. **Client llms.txt/agents.txt** (if available):
   - Review business model, product offerings, target audience
   - Check for seasonal notes or business cycle information

5. **Spreadsheets in Client Folder**:
   - Look for previous analysis, reports, or data exports
   - Check for documented patterns or insights

6. **Completed Tasks (tasks-completed.md)**:
   - Review what work has been completed for this client
   - **CRITICAL**: Read task notes carefully - they contain status updates, caveats, and follow-up requirements
     * Example: "Completed but still waiting for customer response"
     * Example: "Analysis done but client needs to approve changes"
     * Example: "Fixed temporarily, may need further investigation"
   - Check if recent tasks address current issues or questions
   - Reference completed tasks AND their notes when explaining actions taken
   - Use to avoid duplicating recent work and to understand pending items
   - Roksys internal tasks tracked in `roksys/tasks-completed.md`

**Root Cause Analysis Framework:**

When explaining performance changes, always categorize causes:

✅ **Your Actions** (Account Management):
- Budget changes, bid adjustments, campaign launches
- ROAS target modifications, audience changes
- Ad copy updates, keyword additions/removals
- Campaign structure changes
- **Reference completed tasks** (from tasks-completed.md) to show what work has been done

🌍 **External Factors** (Market/Competitive):
- Seasonality, competitor activity, market trends
- Economic conditions, industry changes
- Search demand shifts, auction dynamics

🏢 **Client Business Changes**:
- Stock/inventory issues, product launches
- Pricing changes, promotions, sales
- Website changes, technical issues
- Business strategy shifts

⚙️ **Technical Issues**:
- Conversion tracking problems
- Website performance issues
- Pixel/tag implementation problems
- Platform bugs or policy issues

**Goal**: Use every available data source (CONTEXT.md, tasks-completed.md, experiments, emails, meetings, GA4, client website) to provide comprehensive, evidence-based explanations for performance changes, distinguishing between controllable (your actions) and uncontrollable (external) factors.

**Data freshness**: CSV files are auto-updated every 6 hours from the [ROK | Experiments Google Sheet](https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/)

**Export script**: `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`

**File structure**:
- `rok-experiments-client-notes.csv` - Timestamped experiment log (Timestamp, Client, Note, Tags)
- `rok-experiments-client-list.csv` - Simple list of all ROK clients

### Logging Experiments - MANDATORY PROMPTING PROTOCOL

**CRITICAL**: You MUST ask the 5 essential questions in these situations:

**Trigger Situations:**

1. **User asks you to log/add to experiment spreadsheet**
   - "Add this to experiments"
   - "Log this experiment"
   - "These budgets have been changed" (implies logging needed)
   - ANY mention of updating rok-experiments-client-notes.csv

2. **You're about to write to rok-experiments-client-notes.csv**
   - BEFORE adding any row to the spreadsheet
   - Even if user gave you a description

3. **You discover strategic changes in Google Ads Change History**
   - Campaign structure changes (new campaigns, paused campaigns)
   - Budget changes >10%
   - ROAS target changes
   - New asset groups or ad groups
   - Ask: "I see you made [change] on [date]. Should we log this as an experiment?"

**When triggered, IMMEDIATELY ask (conversational tone):**

Example:
```
Got it - I can see you've made [describe the change]. Before I log this,
let me grab a few quick details so we can track the impact properly:

- What was driving this change? [contextualize the "why" based on what you know]
- What are you expecting to see? [suggest likely outcomes based on the change]
- When should we check back on this? [suggest a reasonable timeline]
- What would make this a win? [suggest success criteria based on the change]

Even quick answers are fine - I'll format it all properly!
```

**Be conversational and helpful:**
- Frame questions naturally, not as a checklist
- Show you understand the context
- Suggest possible answers to make it easier
- Keep it friendly and collaborative

**What you do with answers (even incomplete):**
1. Format into proper experiment log entry
2. Add to rok-experiments-client-notes.csv
3. Update client CONTEXT.md if significant
4. Confirm it's logged

**DO NOT**:
- Skip the questions and assume you know
- Log experiments without prompting first
- Wait for "complete" answers (brief is fine)

**Example of working with incomplete answers:**

User: "Just need to hit budget target"
→ You format as: "WHY: Spending ahead of monthly budget, need to control spend"

User: "End of month"
→ You format as: "REVIEW: Nov 30, 2025"

User: "Not overspend"
→ You format as: "SUCCESS: Daily spend stays within £X budget, ROAS maintains 570%+"

**The act of asking matters more than perfect answers.** See `roksys/knowledge-base/rok-methodologies/experiment-logging-guide.md` for complete protocol.

## Knowledge Base System

**Location**: `roksys/knowledge-base/`
**Purpose**: Curated reference library of Google Ads best practices, AI strategies, platform updates, and industry insights

### How It Works

The knowledge base provides **authoritative, up-to-date reference materials** that Claude Code consults when providing strategic advice. This ensures recommendations are grounded in current best practices, not generic knowledge.

**Automated Inbox System**:
1. User drops files into `roksys/knowledge-base/_inbox/` (emails, PDFs, video transcripts, articles)
2. Processor runs every 6 hours (automated via LaunchAgent)
3. Content analyzed with Claude API to determine topic and category
4. Files formatted as markdown and moved to appropriate category folder
5. Knowledge base index updated automatically

**Categories**:
- `google-ads/performance-max/` - PMax strategies, optimization, best practices
- `google-ads/shopping/` - Shopping campaigns, feed optimization, merchant center
- `google-ads/search/` - Search campaigns, keyword strategies, ad copy
- `google-ads/platform-updates/` - Official Google Ads announcements and changes
- `google-ads/bidding-automation/` - Smart Bidding, tROAS, automated bidding
- `ai-strategy/` - AI in marketing, automation, machine learning applications
- `analytics/` - GA4, attribution models, conversion tracking, measurement
- `industry-insights/` - Market trends, competitive intelligence, research
- `rok-methodologies/` - ROK's proprietary frameworks and processes

### When to Use the Knowledge Base

**IMPORTANT**: Before providing strategic advice on campaigns, optimization, or platform features, **CHECK THE KNOWLEDGE BASE** for relevant, up-to-date information.

**Use cases**:
1. **Platform Updates**: Check `google-ads/platform-updates/` for recent Google changes
2. **Campaign Strategy**: Reference category-specific best practices (PMax, Shopping, Search)
3. **Optimization Advice**: Consult `bidding-automation/` for Smart Bidding guidance
4. **Client Questions**: Cross-reference KB docs with client CONTEXT.md for informed answers
5. **New Features**: Check if KB has documentation before giving generic advice

**Citation Format**: When using KB information, cite the source:
- "Per roksys/knowledge-base/google-ads/performance-max/asset-optimization.md, the recommended approach is..."
- "According to recent platform updates (KB: platform-updates/2025-10-pmax-changes.md), Google now..."

### Integration with Client Work

When working on client tasks:
1. Read client CONTEXT.md (business context, history, preferences)
2. **Check relevant KB documents** (platform best practices, recent updates)
3. Combine both sources for informed, contextual advice
4. Reference both sources in recommendations

**Example workflow**:
```
User: "Should we enable asset group expansion for Smythson's PMax campaign?"

Claude Code:
1. Reads clients/smythson/CONTEXT.md (learns about client preferences, past tests)
2. Checks roksys/knowledge-base/google-ads/performance-max/ for latest guidance
3. Provides recommendation combining:
   - KB best practices on asset expansion
   - Client-specific context (brand guidelines, past performance)
   - Recent platform updates (if available in KB)
```

### Adding Content to the Knowledge Base

**User workflow**:
1. **Drop files in inbox**: `roksys/knowledge-base/_inbox/{emails,documents,videos}/`
2. **Automatic processing**: Every 6 hours, or manual: `python3 shared/scripts/knowledge-base-processor.py`
3. **Organized automatically**: Files categorized and formatted by AI

**Claude Code workflow** (when asked to add content):
1. User provides URL, article text, or video transcript
2. Analyze content to determine category
3. Create formatted markdown with frontmatter (title, date, tags, summary)
4. Save to appropriate category folder
5. Update knowledge base README index

**File format**:
```markdown
---
title: Document Title
source: URL or source name
date_added: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---

## Summary
- Key point 1
- Key point 2

## Full Content
[content here]

## Key Insights
- Actionable insight 1
- Strategic implication 2
```

### Maintenance

- **Automated**: Inbox processed every 6 hours via LaunchAgent
- **Manual processing**: `shared/scripts/knowledge-base-processor.py`
- **Logs**: `~/.petesbrain-knowledge-base.log` and `shared/data/kb-processing.log`
- **Setup**: `roksys/knowledge-base/setup-automation.sh`
- **Documentation**: See `roksys/knowledge-base/QUICKSTART.md` and `EMAIL-INTEGRATION.md`

### Email Integration (Optional)

The knowledge base can integrate with the email sync system to automatically import:
- Google Ads platform update emails
- Industry newsletter content (Search Engine Land, WordStream, etc.)
- AI/ML updates from trusted sources

See `roksys/knowledge-base/EMAIL-INTEGRATION.md` for setup instructions.

### Industry News Monitoring (Automated)

**Location**: `shared/scripts/industry-news-monitor.py`
**Purpose**: Automatically monitor RSS feeds from top Google Ads industry websites
**Status**: Active, production-ready

**What it does**:
1. Monitors RSS feeds from 9 respected industry sources every 6 hours
2. Uses Claude API to score each article for relevance (0-10 scale)
3. Imports articles scoring 6+ to knowledge base inbox
4. Articles automatically processed and categorized by existing inbox system

**Sources monitored**:
- Search Engine Land (Google Ads & PPC)
- Search Engine Journal (PPC)
- Google Ads Blog (Official)
- Think with Google
- WordStream Blog
- PPC Hero
- Neil Patel Blog
- Unbounce Blog

**Running manually**:
```bash
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/industry-news-monitor.py
```

**Automated schedule**:
- Runs every 6 hours via LaunchAgent
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.industry-news.plist`
- Log file: `~/.petesbrain-industry-news.log`

**Configuration**:
- Relevance threshold: 6/10 minimum (configurable in script)
- State tracking: `shared/data/industry-news-state.json`
- Processes articles from last 7 days on first run

**Documentation**: See `roksys/knowledge-base/INDUSTRY-NEWS-MONITORING.md` for complete details

### AI News Monitoring (Automated)

**Location**: `shared/scripts/ai-news-monitor.py`
**Purpose**: Automatically monitor RSS feeds from top AI and machine learning news websites
**Status**: Active, production-ready

**What it does**:
1. Monitors RSS feeds from 12 respected AI news sources every 6 hours
2. Uses Claude API to score each article for relevance to AI in marketing/advertising (0-10 scale)
3. Imports articles scoring 6+ to knowledge base inbox
4. Articles automatically processed and categorized by existing inbox system

**Sources monitored**:
- **Marketing AI**: Marketing AI Institute, MarTech, Adweek
- **Major AI Companies**: OpenAI Blog, Google AI Blog, Microsoft AI Blog, Anthropic News
- **AI News & Analysis**: MIT Technology Review, VentureBeat, AI News
- **Practical AI/ML**: Machine Learning Mastery, Towards Data Science

**Running manually**:
```bash
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/ai-news-monitor.py
```

**Automated schedule**:
- Runs every 6 hours via LaunchAgent
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.ai-news.plist`
- Log file: `~/.petesbrain-ai-news.log`

**Configuration**:
- Relevance threshold: 6/10 minimum (configurable in script)
- State tracking: `shared/data/ai-news-state.json`
- Processes articles from last 7 days on first run

**Scoring criteria**:
- HIGH (8-10): AI tools for marketing, generative AI, marketing automation, AI strategy
- MEDIUM (5-7): General AI trends, AI product launches, ML fundamentals
- LOW (0-4): Pure academic research, non-marketing AI applications

## MCP Server Integrations

**Pete's Brain** uses Model Context Protocol (MCP) servers to integrate with external services. These provide direct access to APIs and data sources.

**Available MCP Servers**:
- **Google Ads** - Query campaign data (GAQL), run keyword planner (✅ Active)
- **Google Analytics** - Query GA4 properties for traffic and conversion data (✅ Active)
- **Google Sheets** - Read/write spreadsheet data, automated exports (✅ Active)
- **Google Tasks** - Manage task lists and tasks, track deliverables (✅ Active)
- **Google Drive** - Import/manage Google Docs, Sheets, Slides
  - ⚠️ **Status**: OAuth configuration in progress
  - **What works**: Read operations (listing, content retrieval)
  - **What's pending**: Write operations pending OAuth credential finalization
- **WooCommerce** - Query product data for Shopping campaigns (⚙️ Configured as needed)

**Detailed Reference**: See `docs/MCP-SERVERS.md` for complete tool listings, parameters, and examples.

**Configuration**: All MCP servers configured in `.mcp.json` with appropriate credentials.

## Automated Workflows

Several background workflows run automatically to keep data synchronized and send summary emails:

**Active Workflows**:
- **Weekly Meeting Review** - Analyzes meetings and completed tasks, sends weekly email (Mondays 9 AM)
- **Knowledge Base Weekly Summary** - Summarizes KB activity and industry news (Mondays 9 AM)
- **Industry News Monitor** - Monitors Google Ads industry RSS feeds (every 6 hours)
- **AI News Monitor** - Monitors AI/ML news RSS feeds (every 6 hours)
- **Knowledge Base Processor** - Processes files in KB inbox (every 6 hours)
- **Google Tasks Tracker** - Syncs tasks to CONTEXT.md and tasks-completed.md (every 6 hours)
- **Email Sync** - Syncs Gmail to client folders as markdown
- **Granola Meeting Import** - Auto-imports meeting transcripts (every 5 minutes)
- **Google Sheets Export** - Exports ROK Experiments sheet to CSV (every 6 hours)

**Key Integration**: Google Tasks Tracker automatically syncs tasks to CONTEXT.md:
- New tasks with >50 char notes → Added to "Planned Work" section
- Completed tasks → Moved to "Completed Work" section + logged to tasks-completed.md
- Task notes contain critical status info - always review when analyzing client work

**Detailed Reference**: See `docs/AUTOMATION.md` for complete details on each workflow, including manual commands, schedules, and configuration.

## Shared Scripts

Key utility scripts in `shared/scripts/`:

- **review-meeting-client.sh** - Validate and correct client assignments for meeting notes
- **add-context-note.sh** - Quickly add notes to client CONTEXT.md files from command line

See `docs/AUTOMATION.md` for automated scripts (weekly-meeting-review.py, tasks-monitor.py, etc.).

## Testing and Development

**Testing Tools**:
```bash
# Test a tool manually
cd tools/[tool-name]
source .venv/bin/activate
python3 -m pytest  # if tests exist

# Test a specific script
cd /Users/administrator/Documents/PetesBrain
ANTHROPIC_API_KEY="your-key" python3 shared/scripts/[script-name].py

# Test with Google credentials
GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
  python3 shared/scripts/[script-name].py
```

**Debugging LaunchAgents**:
```bash
# Check if running
launchctl list | grep com.petesbrain

# View recent errors/output
cat ~/.petesbrain-[name].log | tail -50

# Run once manually to test
launchctl start com.petesbrain.[name]

# Stop a running agent
launchctl stop com.petesbrain.[name]

# Reload after changes
launchctl unload ~/Library/LaunchAgents/com.petesbrain.[name].plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.[name].plist
```

**Development Workflow**:
```bash
# Start a tool for development
cd tools/[tool-name]
./start.sh  # Most tools have start scripts

# Monitor logs in real-time
tail -f ~/.petesbrain-[workflow-name].log

# Test MCP server connection
# Check if MCP server is responding in Claude Code by using an mcp__ tool
```

## Troubleshooting

For common issues and solutions, see `docs/TROUBLESHOOTING.md` which covers:
- LaunchAgent issues (checking status, reloading, viewing logs)
- MCP server connection problems
- Google API authentication
- Python script issues
- Email/Gmail problems
- And more

**Quick checks**:
- LaunchAgents: `launchctl list | grep petesbrain`
- Logs: `cat ~/.petesbrain-[name].log`
- MCP servers: Check `.mcp.json` paths are absolute

## Git Commit Format

Use these prefixes for commits:
- `[tool-name]: description` - Tool-specific changes
- `[project]: description` - Project-wide changes
- `[docs]: description` - Documentation updates
- `[clients]: description` - Multiple client updates
- `[client-name]: description` - Single client work
- `[automation]: description` - Automated workflow changes
- `[mcp]: description` - MCP server integrations
- `[knowledge-base]: description` - Knowledge base content/system changes

**Examples**:
```
[google-ads-generator]: Add support for responsive search ads
[smythson]: Add Q4 2025 strategy report
[automation]: Fix weekly meeting review email formatting
[knowledge-base]: Add Performance Max best practices guide
```