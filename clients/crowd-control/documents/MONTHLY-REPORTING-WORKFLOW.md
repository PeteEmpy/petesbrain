# Crowd Control - Monthly Reporting Workflow

> **Purpose**: Standardized process for monthly performance email updates to Jeremy
> **Created**: 2025-11-05
> **Based on**: October 2025 performance email (email-draft-2025-11-05-october-performance-tracking-update.html)

---

## Timing

**When**: First week of each month (e.g., Nov 5 for October performance)
**Recipient**: Jeremy @ Queue Solutions

---

## Email Structure Template

### 1. Opening
- Brief, friendly opening
- State purpose: "Quick update on the account for [MONTH]"

### 2. Key Metrics Summary (if significant changes)
- Revenue comparison (month-over-month and year-over-year)
- Order volume comparison
- ROAS performance vs targets
- Any immediate issues flagged upfront

### 3. Account Performance Section
**Header**: `<strong>Account performance:</strong>`

Include:
- Total website revenue for the month
- Order count (current vs prior year)
- Overall efficiency assessment
- Context on whether performance is strong/weak and why
- Month-over-month trends

### 4. Product Performance Insights
**Focus on**: What's driving the numbers

Include:
- Top performing products/categories
- New product performance (with specific ROAS figures)
- Product mix changes from prior year
- Any standout performers worth highlighting
- Categories to watch

**Example format**:
> "In October, the hose reels (garden, air, and electric cable reels) generated £834 revenue at 239% ROAS across 20+ variants. The 15m garden hose reel in particular is doing very well."

### 5. Strategic Updates (if applicable)
- Campaign adjustments made during the month
- Budget changes
- ROAS target modifications
- Structural changes
- Experiment results

### 6. Technical Issues (only if relevant)
- Any tracking problems discovered
- Website issues affecting performance
- Fixes implemented
- Timeline for resolution

### 7. AI Project Update
**Header**: `<strong>AI project update:</strong>`

Brief mention of:
- How AI monitoring would have helped with current issues
- Progress on automation systems
- Expected benefits for client
- Timeline for implementation

**Tone**: Practical, not promotional. Show value through specific examples.

### 8. Timeline (if relevant)
Use bullet list for key dates:
- When issues occurred
- When fixes were implemented
- When verification checks are scheduled

### 9. Closing
- Simple sign-off: "I'll keep you posted on [specific follow-up item]"
- Standard signature

---

## Data Sources Checklist

Before drafting email, gather:

- [ ] **Google Ads data** (via MCP GAQL queries):
  - Campaign performance for the month
  - Product-level Shopping performance
  - Conversion metrics
  - ROAS by campaign/product

- [ ] **WooCommerce data** (via WooCommerce MCP or API):
  - Total orders for the month
  - Revenue attributed to Google Ads
  - Top selling products
  - Year-over-year comparison

- [ ] **Experiment notes** (rok-experiments-client-notes.csv):
  - What changes were made during the month
  - Why changes were made
  - Expected outcomes

- [ ] **CONTEXT.md** (clients/crowd-control/CONTEXT.md):
  - Any ongoing issues
  - Client preferences
  - Strategic context

- [ ] **Product Impact Analyzer reports** (if available):
  - Weekly product change analysis
  - Label transitions (Hero/Sidekick/Villain/Zombie)

- [ ] **Meeting notes** (if any meetings occurred):
  - Action items from discussions
  - Client requests or concerns

---

## Analysis Framework

### Step 1: Compare Actual vs Expected
- Check experiment notes for what was planned/changed
- Compare actual results to expected outcomes
- Flag any surprises (positive or negative)

### Step 2: Product-Level Analysis
- Identify top 10 revenue-generating products
- Check ROAS by product category
- Look for new products performing well/poorly
- Note any stock issues or disapprovals

### Step 3: Year-over-Year Context
- Compare to same month prior year
- Account for seasonality
- Note shifts in product mix

### Step 4: Root Cause Analysis
When explaining performance changes, categorize:
- **Your Actions** (campaign management, bid changes, etc.)
- **External Factors** (market, competition, seasonality)
- **Client Business Changes** (stock, pricing, website)
- **Technical Issues** (tracking, website problems)

### Step 5: Forward-Looking
- What should be monitored next month
- Upcoming changes or tests planned
- Expected impact of recent changes

---

## Tone & Style Guidelines

**Reference emails**:
- October 2025 email (this file's basis)
- Previous emails to Michael Robinson (Clear Prospects) for general tone

**Key characteristics**:
- **Concise**: Get to the point quickly
- **Factual**: Use specific numbers and evidence
- **Balanced**: Include both good news and issues
- **Practical**: Focus on what matters to the business
- **Professional but friendly**: Not overly formal

**Avoid**:
- Overly technical jargon
- Lengthy explanations unless critical
- Apologetic tone for normal business issues
- Promises without timelines

---

## HTML Formatting Standards

Use the Roksys company-wide email standard (as of Nov 5, 2025):

```html
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.4;
    color: #333;
}
p, ul, ol {
    margin: 10px 0;
}
li {
    margin: 6px 0;
}
strong {
    font-weight: 600;
}
</style>
```

**Spelling**: British English (analyse, optimise, customisation)

**File naming**: `email-draft-YYYY-MM-DD-monthly-update-[month-name].html`

**Location**: `clients/crowd-control/`

---

## Delivery Process

1. Draft email in HTML format
2. Save to `clients/crowd-control/email-draft-YYYY-MM-DD-monthly-update-[month].html`
3. Auto-open in browser for review
4. User copies from browser to Apple Mail
5. User reviews, adjusts if needed, and sends

---

## Example: October 2025 Email Breakdown

**File**: email-draft-2025-11-05-october-performance-tracking-update.html

**What worked well**:
- Led with the critical issue (tracking failure)
- Explained impact clearly (46.5% missing conversions)
- Provided context on actual performance (303% vs 162% ROAS)
- Included specific product insights (hose reels at 239% ROAS)
- Mentioned AI project in practical, helpful way
- Clear timeline of what happened when
- Disclosed cost ($149 USD) upfront

**Structure**:
1. Opening (brief, friendly)
2. What I found (tracking issue with evidence)
3. The impact (Smart Bidding implications)
4. What I've done (plugin installed, cost disclosed)
5. Account performance (positive context)
6. Product insights (hose reels detail)
7. AI project update (practical value)
8. Timeline (key dates)
9. Next steps (Thursday verification)

---

## Monthly Checklist

- [ ] Gather all data sources (Google Ads, WooCommerce, experiments, CONTEXT.md)
- [ ] Analyze performance vs prior month and prior year
- [ ] Identify key drivers (products, campaigns, changes)
- [ ] Check for technical issues or anomalies
- [ ] Review experiment notes for context on changes made
- [ ] Draft email following structure template
- [ ] Apply HTML formatting standards (10px paragraph spacing)
- [ ] Save with proper filename and location
- [ ] Auto-open in browser for user review
- [ ] Update CONTEXT.md with any new insights from analysis
- [ ] Add completed task to tasks-completed.md

---

## Notes

- This workflow was established based on the October 2025 performance email
- Adjust structure as needed based on what's most relevant each month
- Not every section is required every month - use judgment
- Focus on insights that matter to the business, not just data dumps
- Reference this document when drafting monthly emails for consistency
