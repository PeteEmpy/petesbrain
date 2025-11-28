# Client Analysis Workflows

**Last Updated:** November 5, 2025

This document contains detailed operational procedures for working with clients in PetesBrain. For architectural overview, see [CLAUDE.md](../CLAUDE.md).

## Table of Contents

1. [Google Ads Client Analysis Workflow](#google-ads-client-analysis-workflow)
2. [Adding Context On The Fly](#adding-context-on-the-fly)
3. [Multi-Source Performance Analysis](#multi-source-performance-analysis)
4. [Root Cause Analysis Framework](#root-cause-analysis-framework)
5. [Client Folder Structure](#client-folder-structure)
6. [AI Discoverability Files](#ai-discoverability-files-llmstxt--agentstxt)

---

## Google Ads Client Analysis Workflow

**CRITICAL**: The **CONTEXT.md file is the beating heart of the client analysis system**. It must be maintained and referenced for every client interaction.

### Required Data Sources

- `clients/[client-name]/CONTEXT.md` - **PRIMARY CLIENT KNOWLEDGE BASE**
- `clients/[client-name]/tasks-completed.md` - Auto-generated completed tasks log
- `roksys/spreadsheets/rok-experiments-client-notes.csv` - Experiment tracking

### MANDATORY 10-Step Process

When working with any client, ALWAYS follow this process:

#### 1. **DISCOVER all client content** (CRITICAL - DO NOT SKIP)

```bash
# Use Bash to list all folders and files
ls -la /Users/administrator/Documents/PetesBrain/clients/[client-name]/
```

**IMPORTANT**: The client folder structure is NOT fixed. New folders may be added at any time:
- Standard folders: emails/, meeting-notes/, documents/, briefs/, presentations/, spreadsheets/
- New standard folders (Oct 2025): reports/, product-feeds/, scripts/
- Custom folders: contracts/, proposals/, assets/, research/, etc.

**You MUST discover and use ALL content**, regardless of folder name. If a new subfolder exists, read and analyze its contents.

#### 2. **FIRST: Read CONTEXT.md** (CRITICAL - DO NOT SKIP)

```bash
Read: /Users/administrator/Documents/PetesBrain/clients/[client-name]/CONTEXT.md
```

This is your primary knowledge base. If it doesn't exist, create it using the template from `clients/_templates/CONTEXT.md`.

#### 3. **Read completed tasks history**

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
- Reference task notes when discussing what's been done
- If file doesn't exist, the client has no recorded completed tasks yet

#### 4. **Read the experiment notes** (CRITICAL - THIS EXPLAINS PERFORMANCE CHANGES)

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

#### 5. **Check recent email communications**

```bash
Read: /Users/administrator/Documents/PetesBrain/clients/[client-name]/emails/
```

- List emails and identify recent ones (last 30-60 days based on filename dates)
- Read relevant emails about performance, requests, issues, or strategy discussions
- Look for client concerns, budget discussions, stock issues, seasonal notes

#### 6. **Review meeting notes**

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

#### 7. **Check ALL other folders** (discovered in step 1)

- Standard folders: documents/, briefs/, presentations/, spreadsheets/
- **ANY custom folders** added by user (contracts/, proposals/, reports/, research/, etc.)
- Read key files from ALL folders to understand complete client context
- **CRITICAL**: Never assume folder structure is fixed - always discover what exists

#### 8. **Analyze external factors and root causes**

When performance changes, investigate beyond account management actions:

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

#### 9. **Synthesize all context**

Use information from CONTEXT.md, completed tasks (including task notes!), **experiments**, emails, meetings, and ALL discovered folders.

See [Multi-Source Performance Analysis](#multi-source-performance-analysis) section below for detailed framework.

#### 10. **UPDATE CONTEXT.md** (MANDATORY - DO NOT SKIP)

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

---

## Adding Context On The Fly

The user can paste context directly into chat using these patterns:

### 1. Simple format (you choose section):
```
Add to [client] context:
[text to add]
```

### 2. Specify section:
```
Add to [client] context - [section]:
[text to add]
```

### 3. Natural language:
- "Update Smythson CONTEXT.md: [text]"
- "Add this note to Tree2mydoor: [text]"
- "Save to Clear Prospects context: [text]"

### When You See These Patterns:

1. Identify the client name (match against existing client folders)
2. If section specified, add to that section; otherwise ask which section or use "Ad Hoc Notes"
3. Add the text with timestamp to CONTEXT.md
4. Update "Last Updated" date
5. Add to Document History table
6. Confirm what was added and where

### Section Keywords to Recognize:

- "strategy" → Strategic Context
- "preference" or "communication" → Client Preferences
- "business" or "product" → Business Context
- "issue" or "problem" → Known Issues
- "learning" or "insight" → Key Learnings
- "campaign" → Campaign Notes
- "action" or "todo" → Action Items
- "contact" or "link" → Quick Reference

---

## Multi-Source Performance Analysis

### CRITICAL: Match performance changes to ALL available sources

When you see a performance spike/drop, CHECK ALL sources:
- **Experiment notes (rok-experiments-client-notes.csv)** - Strategic change: what/why/expected outcome
- **Completed tasks (tasks-completed.md)** - Tactical implementation: how/when/status
- **Google Ads Change History** - Via MCP API or UI, see what actually changed in the account
- **Knowledge Base** - Google platform updates (2-4 weeks prior for delayed impact)
- **External factors** - Client business changes, market conditions

### Why Google Ads Change History Matters

- Captures changes NOT logged in experiments (automatic Google changes, policy updates, disapprovals)
- Shows exact timing of changes (down to the hour)
- Reveals unintended changes (accidental edits, API changes, third-party tools)
- Cross-validates experiment notes (confirms what was logged actually happened)
- **Important**: Change history is NOT definitive - many factors affect performance beyond logged changes

### Analysis Framework (Check ALL Sources)

#### 1. Product-Level Performance (CRITICAL for e-commerce - check FIRST)

- Google Ads Shopping performance by product (via MCP GAQL queries)
- Product Impact Analyzer reports (weekly analysis, product changes)
- Merchant Center product status (disapprovals, out of stock)
- Best/worst performing products (revenue, ROAS, clicks)
- Product changes: additions, removals, price changes
- **Why this matters**: Account-level metrics hide product-level stories. A 10% account revenue drop might be one bestseller going out of stock.

#### 2. Account Changes (verify what actually changed)

- Google Ads Change History (via MCP or UI)
- Experiment notes (strategic intent)
- Completed tasks (implementation details)

#### 3. Platform Evolution (delayed 2-4 weeks)

- Knowledge Base for Google platform updates
- Algorithm changes, new features

#### 4. External Factors

- Client business changes (stock, pricing, website)
- Market conditions, seasonality
- Competitive landscape

#### 5. Technical Issues

- Conversion tracking problems
- Website performance
- Merchant Center disapprovals

### Analysis Process for E-commerce Shopping Campaigns

#### 1. Start with product-level data (most granular, most revealing):

- Query Shopping performance by product via MCP
- Identify which products drove the performance change
- Check if top performers are still active, in stock, properly priced
- Look for product additions/removals that explain account changes

#### 2. Connect products to account changes:

- Cross-validate experiment notes against Google Ads change history
- Check if experiments affected specific products or categories
- Reference Product Impact Analyzer for product change timeline

#### 3. Check platform and external factors:

- Knowledge Base for platform updates (2-4 weeks delayed)
- Merchant Center for product disapprovals/stock issues
- Client communications for business changes

#### 4. Synthesize complete story:

- Separate into categories: (a) product changes, (b) account management, (c) platform, (d) external, (e) technical
- **Lead with product insights**: "Revenue dropped 15% due to top product (SKU 287, £680/week) going out of stock"
- Include account-level context: "This was flagged in Product Impact Analyzer and confirmed via Merchant Center"
- Cite all sources with evidence

**Important**: For e-commerce, ALWAYS drill down to product level before drawing conclusions. Account-level metrics can be misleading.

### Example Multi-Source Analyses

#### Example 1: Product-level cause (e-commerce)

> "Revenue dropped 15% (£680/week) starting Oct 20.
> - **Product Performance**: SKU 287 (Olive Tree Large) revenue dropped from £680/week to £0
> - **Merchant Center**: Product 287 marked out of stock Oct 19
> - **Product Impact Analyzer**: Flagged product removal Oct 20
> - Change History: No account changes ✗
> - Experiments: No strategic changes ✗
> - Conclusion: Revenue drop caused by top-selling product going out of stock. Product 287 represented 15% of total account revenue."

#### Example 2: Platform update (with evidence)

> "Performance improved 20% starting Oct 15.
> - Product Performance: Improvement spread across all products (no single driver)
> - Change History: No account changes Oct 10-20 ✗
> - Experiments: No strategic changes ✗
> - Knowledge Base: Smart Bidding update rolled out Oct 1 ✓
> - Conclusion: Improvement aligns with Google Smart Bidding update (2-week learning period from Oct 1)."

#### Example 3: Unexplained (no evidence)

> "Revenue improved 20% starting Oct 15.
> - Product Performance: Improvement spread across top 10 products (no single driver)
> - Change History: No account changes Oct 10-20 ✗
> - Experiments: No strategic changes ✗
> - Knowledge Base: No platform updates in prior 4 weeks ✗
> - Merchant Center: No product additions or stock changes ✗
> - Conclusion: Unable to determine cause from available data. Recommend monitoring to see if pattern continues and checking with client for undocumented changes."

**CRITICAL**: Only cite specific factors when you have EVIDENCE (from emails, meetings, Knowledge Base, change history, etc.). Do NOT speculate about "possible" or "likely" causes without supporting data.

---

## Root Cause Analysis Framework

When explaining performance changes, always categorize causes:

### ✅ Your Actions (Account Management)

- Budget changes, bid adjustments, campaign launches
- ROAS target modifications, audience changes
- Ad copy updates, keyword additions/removals
- Campaign structure changes
- **Reference completed tasks** (from tasks-completed.md) to show what work has been done

### 🌍 External Factors (Market/Competitive)

- Seasonality, competitor activity, market trends
- Economic conditions, industry changes
- Search demand shifts, auction dynamics

### 🏢 Client Business Changes

- Stock/inventory issues, product launches
- Pricing changes, promotions, sales
- Website changes, technical issues
- Business strategy shifts

### ⚙️ Technical Issues

- Conversion tracking problems
- Website performance issues
- Pixel/tag implementation problems
- Platform bugs or policy issues

**Goal**: Use every available data source (CONTEXT.md, tasks-completed.md, experiments, emails, meetings, GA4, client website) to provide comprehensive, evidence-based explanations for performance changes, distinguishing between controllable (your actions) and uncontrollable (external) factors.

---

## Client Folder Structure

Standardized as of Oct 30, 2025:

### Root Level (only essential files)

- **`CONTEXT.md`** ⭐ - **PRIMARY KNOWLEDGE BASE** - Living document with strategic context, learnings, and insights
- **`tasks-completed.md`** ⭐ - **COMPLETED TASKS LOG** - Auto-generated log of all completed Google Tasks for this client
- `README.md` - (Optional) High-level client overview (business model, contacts, key facts)
- `llms.txt` / `agents.txt` - (Optional) AI discoverability files (if created)

### Standard Folders

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

---

## Additional Data Sources to Cross-Reference

When analyzing performance, proactively check these additional sources if available:

### 1. Google Analytics (via MCP)

- Use `mcp__google-analytics__*` tools to check website traffic trends
- Compare Google Ads traffic to overall site traffic
- Check conversion rate changes at the website level
- Identify if issues are Google Ads-specific or site-wide

### 2. Client Website (via WebFetch)

- Check if products mentioned in campaigns are still available
- Verify pricing matches ad copy
- Look for site changes, promotions, or banners
- Check if tracking pixels are present (GTM, Google Ads tags)

### 3. Historical Google Ads Data

- Compare current period to same period last year (seasonality)
- Look for recurring patterns or anomalies
- Check if similar changes happened before and what caused them

### 4. Client llms.txt/agents.txt (if available)

- Review business model, product offerings, target audience
- Check for seasonal notes or business cycle information

### 5. Spreadsheets in Client Folder

- Look for previous analysis, reports, or data exports
- Check for documented patterns or insights

### 6. Completed Tasks (tasks-completed.md)

- Review what work has been completed for this client
- **CRITICAL**: Read task notes carefully - they contain status updates, caveats, and follow-up requirements
- Check if recent tasks address current issues or questions
- Reference completed tasks AND their notes when explaining actions taken
- Use to avoid duplicating recent work and to understand pending items
- Roksys internal tasks tracked in `roksys/tasks-completed.md`

---

## AI Discoverability Files (llms.txt & agents.txt)

**Location**: `clients/[client-name]/llms.txt` and `clients/[client-name]/agents.txt`
**Purpose**: Make client businesses discoverable by AI assistants like ChatGPT, Claude, and Gemini

### When to Create

When a client needs to improve their AI discoverability for customer support, lead generation, or brand awareness.

### Process

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

---

## Data Freshness

**CSV files**: Auto-updated every 6 hours from the [ROK | Experiments Google Sheet](https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/)

**Export script**: `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`

**File structure**:
- `rok-experiments-client-notes.csv` - Timestamped experiment log (Timestamp, Client, Note, Tags)
- `rok-experiments-client-list.csv` - Simple list of all ROK clients
