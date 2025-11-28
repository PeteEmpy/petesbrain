---
name: devonshire-monthly-report
description: Generates complete Google Slides monthly Paid Search reports for Devonshire Hotels with branded formatting, data analysis, and recommendations. Use when user says "Devonshire report", "monthly report for Devonshire", or needs to generate Devonshire Hotels performance slides.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Read, Write, Bash, Glob
---

# Devonshire Hotels Monthly Report Generator Skill

---

## Core Workflow

### 1. Pre-Flight Checks

Before generating, verify:
- [ ] It's 2-3 days after month-end (data finalized)
- [ ] Client CONTEXT.md loaded for strategic context
- [ ] Experiment log checked for changes during the month
- [ ] Recent emails reviewed for client feedback or issues

**DO NOT generate mid-month unless explicitly requested for partial update**

### 2. Load Context

**Required reading (in order)**:
1. `clients/devonshire-hotels/CONTEXT.md` - Strategic context, budget tracking, key issues
2. `roksys/spreadsheets/rok-experiments-client-notes.csv` - Filter for Devonshire, check month
3. `clients/devonshire-hotels/emails/` - Recent client communications (last 30 days)
4. `tools/monthly-report-generator/README.md` - Tool reference and campaign IDs

**Campaign Structure to Know**:
- **Main Properties Budget** (£9,000-£11,730): Hotels, PMax, Search, Self-Catering
- **The Hide Budget** (£2,000): Separate tracking
- **Exclusions**: Castles, Weddings, Lismore/Hall tracked separately
- **⚠️ CRITICAL**: The Hide = Highwayman Arms (same property, renamed Oct 10, 2025)
  - Campaign IDs: 23069490466 (current) + 21815704991 (paused historical)
  - ALWAYS combine both when analyzing The Hide

### 3. Query Data via Google Ads MCP

**Date Range**: First day to last day of the target month (e.g., 2025-10-01 to 2025-10-31)

**GAQL Query Structure** (use gaql-query-builder skill):
```sql
SELECT
  campaign.name,
  campaign.id,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions
FROM campaign
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

**Filter Logic**:
- **Main Properties**: Exclude Castles, Weddings, Lismore, Hall, The Hide campaigns
- **The Hide**: Include BOTH campaign IDs (23069490466 + 21815704991)
- **Include paused campaigns** if they have spend in the reporting month

### 4. Calculate Metrics

For each campaign/property:
- **Spend**: cost_micros / 1,000,000 (formatted as £X,XXX.XX)
- **Revenue**: conversions_value (formatted as £X,XXX.XX)
- **ROAS**: (revenue / spend) × 100 (formatted as XXX% - e.g., 420%)
- **Conversions**: Count of bookings + qualified leads
- **CPA**: spend / conversions (formatted as £XX.XX)
- **CTR**: (clicks / impressions) × 100 (formatted as X.XX%)

**Aggregate by**:
1. Property (Devonshire Arms, Cavendish, Beeley Inn, etc.)
2. Campaign Type (Performance Max, Search, Self-Catering)
3. Budget Group (Main Properties vs The Hide)

### 5. Generate Slide Content

**Slide Structure** (14 slides total):

#### Slide 1: Title
```
Title: "Paid Search - [Month YYYY]"
Subtitle: "Devonshire Hotels"
Footer: "Prepared by Rok Systems"
```

#### Slide 2: Executive Summary
```
Title: "Executive Summary"

Content:
- Budget: £X,XXX (vs £X,XXX previous month)
- Spend: £X,XXX.XX (XX% of budget)
- Revenue: £X,XXX.XX
- ROAS: XXX%
- Conversions: XXX bookings
- Key highlights (2-3 bullet points)
```

#### Slide 3: Hotels - Top Performers
```
Title: "Hotels - Top Performers"

Table (sorted by ROAS, top 5):
| Property | Spend | Revenue | ROAS | Conversions |
```

#### Slide 4: Hotels - Attention Needed
```
Title: "Hotels - Attention Needed"

Table (ROAS < 300% or zero conversions):
| Property | Spend | Revenue | ROAS | Issue |
```

#### Slide 5: Campaign Type Breakdown
```
Title: "Campaign Type Breakdown"

Table:
| Type | Spend | Revenue | ROAS | % of Total Spend |
- Performance Max
- Search Campaigns
- Self-Catering
```

#### Slide 6: Self Catering Campaigns
```
Title: "Self Catering Campaigns - Detailed View"

Table:
| Location | Spend | Revenue | ROAS | Conversions |
- Chatsworth SC
- Bolton Abbey SC
```

#### Slide 7: The Hide
```
Title: "The Hide (Separate Budget)"

Content:
- Budget: £2,000
- Spend: £X,XXX.XX (XX% of budget)
- Revenue: £X,XXX.XX
- ROAS: XXX%
- Conversions: XX bookings
- Note: Launched Oct 10, 2025 (formerly Highwayman Arms)
```

#### Slide 8: Weddings
```
Title: "Weddings Campaigns"
Content: "Data available when campaigns are live"
(Placeholder for future)
```

#### Slide 9: Lismore and The Hall
```
Title: "Lismore and The Hall"
Content: "Data available when campaigns are live"
(Placeholder for future)
```

#### Slide 10: Key Insights - Highlights
```
Title: "Key Insights - Highlights"

Bullet points (3-5):
- Top performing properties and why
- Successful optimizations from the month
- Notable improvements or wins
- Client feedback implemented
```

#### Slide 11: Key Insights - Areas for Improvement
```
Title: "Key Insights - Areas for Improvement"

Bullet points (3-5):
- Underperforming campaigns and root causes
- Budget pacing issues (if any)
- Conversion tracking problems (if identified)
- Technical issues or data anomalies
```

#### Slide 12: Recommendations - Part 1
```
Title: "Recommendations for [Next Month]"

Bullet points (3-4):
- Budget adjustments recommended
- Campaign structure changes
- Bid strategy optimizations
- New tests to implement
```

#### Slide 13: Recommendations - Part 2
```
Title: "Recommendations for [Next Month] (continued)"

Bullet points (2-3):
- Seasonal considerations
- Creative refresh needs
- Tracking improvements
- Strategic priorities
```

### 6. Format with Brand Colors

**Estate Escapes Brand Colors** (from CONTEXT.md):
- **Estate Blue**: `#00333D` - Table headers, emphasis
- **Stone**: `#E5E3DB` - Table row backgrounds
- **White**: `#FFFFFF` - Header text
- **Dark Gray**: `#333333` - Data text

**Table Formatting**:
```
Header Row: Estate Blue background, White text, bold
Data Rows: Stone background (alternating with white), Dark Gray text
Borders: Light gray (#CCCCCC)
Font: Arial, 11pt for data, 14pt for headers
```

### 7. Generate Insights

**Highlights** (What went well):
- Cross-reference performance with experiment log
- Identify campaigns that exceeded expectations
- Note any external factors (from emails/context)
- Attribute wins to specific actions taken

**Areas for Improvement** (What needs attention):
- Flag ROAS < 300%
- Note conversion tracking issues
- Identify budget pacing problems
- Call out data anomalies

**Root Cause Analysis**:
- Check experiment log for changes made during month
- Review emails for client-reported issues
- Consider seasonality (compare to same month last year if data available)
- Distinguish between controllable (our actions) and external factors

### 8. Generate Recommendations

**Framework** (use all three categories):

**Immediate Actions** (Next 2 weeks):
- Budget adjustments needed urgently
- Pausing underperforming campaigns
- Conversion tracking fixes
- Quick wins

**Strategic Tests** (Next 30 days):
- New campaign structures
- Bid strategy changes
- Audience expansions
- Creative refreshes

**Long-term Priorities** (Next quarter):
- Seasonal prep (e.g., Christmas, summer bookings)
- Account structure overhauls
- New campaign types (e.g., Demand Gen)
- Advanced features (e.g., Hotel Ads integration)

**Prioritization**:
- Lead with highest revenue impact
- Consider client bandwidth (don't overwhelm)
- Reference CONTEXT.md for client preferences
- Align with strategic goals

### 9. Create Google Slides

**Method**: Use existing Python script (recommended) or Google Drive MCP

**Python Script** (Preferred):
```bash
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
python3 generate_devonshire_slides.py --month YYYY-MM
```

**MCP Method** (Fallback):
```
Use mcp__google-drive__createGoogleSlides with structured slide data
```

**Output**:
- Presentation ID returned
- Link to Google Slides: `https://docs.google.com/presentation/d/[ID]`
- Editable by user for final review

### 10. Post-Generation

After creating slides:
1. **Confirm to user**: "Created [Month] report: [Google Slides link]"
2. **Summary**: Provide 3-sentence executive summary
3. **Next steps**: "Review slides, then copy into shared deck for Gary"
4. **Offer**: "Want me to draft the email to Gary?"

---

## Data Validation Checks

Before finalizing report, verify:
- [ ] **The Hide data** includes both campaign IDs (current + paused)
- [ ] **Main Properties** excludes The Hide, Castles, Weddings
- [ ] **ROAS percentages** formatted correctly (420% not £4.20)
- [ ] **Spend totals** match budget tracker spreadsheet
- [ ] **Zero-conversion campaigns** flagged and explained
- [ ] **Date range** is complete month (1st to last day)
- [ ] **Paused campaigns** with spend are included
- [ ] **Currency formatting** consistent (£X,XXX.XX)

---

## Common Issues and Solutions

### Issue: Zero Conversions for a Campaign
**Check**:
1. Is conversion tracking working? (Check recent weeks)
2. Did the campaign run all month? (Check status history)
3. Is this expected for this property? (Check CONTEXT.md)

**Solution**: Flag in "Areas for Improvement" with explanation

### Issue: ROAS Calculation Error
**Check**:
1. Revenue and spend both in same currency
2. Divide by zero handling (if spend = 0)
3. ROAS formatted as percentage (multiply by 100)

**Solution**: Return "N/A" if invalid, investigate if unexpected

### Issue: Budget Mismatch
**Check**:
1. Budget tracker spreadsheet for official budget
2. Any mid-month budget changes (experiment log)
3. Separate budgets (Main vs The Hide)

**Solution**: Use budget from CONTEXT.md budget tracking section

### Issue: Missing Campaign Data
**Check**:
1. Campaign launched mid-month? (Include partial data)
2. Campaign paused but has spend? (Include it)
3. New campaign not in campaign list? (Add to tracking)

**Solution**: Note in recommendations to update campaign tracking

---

## Integration with Other Skills

**Works with**:
- **gaql-query-builder** - Construct data queries
- **email-draft-generator** - Draft report delivery email to Gary
- **csv-analyzer** - Analyze exported data if needed

**Data sources**:
- Google Ads MCP (live data)
- CONTEXT.md (strategic context, budget tracking)
- Experiment log CSV (changes made during month)
- Client emails (context on issues or feedback)

---

## Client Delivery Workflow

After generating slides:

1. **Review**: User reviews presentation for accuracy
2. **Customize**: Make any final edits (commentary, emphasis)
3. **Copy to Shared Deck**: Devonshire has a multi-section deck (SEO, Paid Search, etc.)
4. **Email Gary**: Send link to Gary at A Cunning Plan for review
5. **Gary Reviews**: Gary adds context and forwards to Devonshire Hotels

**Email Template** (use email-draft-generator skill):
```
Subject: Devonshire Hotels - [Month] Paid Search Report

Hi Gary,

[Month]'s Paid Search report is ready for your review:
[Google Slides link]

Key highlights:
- [Highlight 1]
- [Highlight 2]
- [Highlight 3]

Let me know if you need any changes before forwarding to the client.

Best,
Pete
```

---

## Time Savings

**Before Automation**:
- Data queries: 30-45 minutes
- Table creation: 30-45 minutes
- Performance analysis: 30-60 minutes
- Commentary writing: 20-30 minutes
- Slide formatting: 20-30 minutes
**Total: 2-3 hours per month**

**With This Skill**:
- Trigger skill: "Generate October report for Devonshire"
- Claude loads context, queries data, generates slides: ~3-5 minutes
- User reviews and customizes: 15-20 minutes
**Total: ~20 minutes per month**

**Monthly Time Saved**: ~2.5 hours

---

## Campaign IDs Reference

### Main Properties (£9,000-£11,730 budget)
- **Performance Max**: 18899261254
- **Chatsworth Location**: 19654308682
- **Bolton Abbey Location**: 22720114456
- **Chatsworth SC**: 19534201089
- **Bolton Abbey SC**: 22536922700

### The Hide (£2,000 budget)
- **Current**: 23069490466 ("The Hide")
- **Historical**: 21815704991 ("Highwayman Arms" - paused Oct 10, 2025)
- **⚠️ ALWAYS combine both for accurate reporting**

### Excluded from Main Budget
- Castles campaigns
- Weddings campaigns
- Lismore and The Hall campaigns
- The Hide campaigns

---

## Success Criteria

A good Devonshire monthly report should:
1. **Be immediately presentable** - Ready to copy into shared deck
2. **Tell the story** - Clear narrative from data to insights to recommendations
3. **Be accurate** - All metrics validated against source data
4. **Be actionable** - Specific next steps, not generic advice
5. **Match brand** - Estate Blue/Stone colors, professional formatting
6. **Save time** - 2+ hours saved vs manual creation
7. **Provide context** - Reference strategic decisions and client feedback

---

## Related Documentation

- `tools/monthly-report-generator/README.md` - Full tool documentation
- `tools/monthly-report-generator/QUICKSTART.md` - Quick reference
- `clients/devonshire-hotels/CONTEXT.md` - Strategic context and budget tracking
- `clients/devonshire-hotels/reports/` - Previous reports for reference
- `.claude/skills/gaql-query-builder/` - Data query skill
- `.claude/skills/email-draft-generator/` - Report delivery email skill

---

**Status**: ✅ Production Ready
**Owner**: Peter Empson
**Client**: Devonshire Hotels (via A Cunning Plan)
**Frequency**: Monthly (3rd of each month after data finalizes)
