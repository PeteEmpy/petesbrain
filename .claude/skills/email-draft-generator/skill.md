---
name: email-draft-generator
description: Generates client-ready HTML email drafts with proper formatting, British English spelling, and client-specific context. Use when user says "draft email", "write email", "email [client] about", "compose email", or needs to send a client communication.
allowed-tools: Read, Write, Bash, Glob
---

# Email Draft Generator Skill

---

## Core Workflow

When this skill is triggered:

### 1. Load Client Context
- Read `clients/[client-name]/CONTEXT.md` for:
  - Client preferences (tone, communication style, sensitivities)
  - Strategic context (current campaigns, goals, issues)
  - Recent work and history
- Scan recent documents/emails for context about the topic

### 2. Determine Email Type
Auto-detect the email category:
- **Performance Update** - Monthly/weekly performance summary
- **Budget Proposal** - Budget increase/decrease recommendations
- **Strategy Proposal** - New campaign or optimization ideas
- **Issue Update** - Problem resolution or status update
- **Action Required** - Client needs to take action
- **General Update** - Routine check-in or information sharing

### 3. Generate Email Content

**Structure (always follow this order)**:
1. **Opening** - Brief greeting and context-setting
2. **Key Message** - Main point in 1-2 sentences (what they need to know)
3. **Supporting Details** - Data, analysis, or explanation (2-4 paragraphs max)
4. **Action Items** - What happens next (if applicable)
5. **Closing** - Professional sign-off

**Tone Guidelines**:
- **Professional but friendly** - ROK's style is approachable, not corporate
- **Data-driven** - Include specific metrics when relevant
- **Solution-focused** - Frame problems with recommended solutions
- **Concise** - Busy clients, get to the point quickly
- **Confident** - You're the expert, provide clear guidance

### 4. Apply Formatting Standards

**⚠️ CRITICAL: ALWAYS use the canonical email template module**

All email drafts MUST use `shared/email_template.py` to ensure consistent formatting.

**Template Standards** (Verdana 13px + Copy Button):
- Font: Verdana 13px
- Line-height: 1.5
- Copy-to-clipboard button with green styling
- British English spelling (UK clients)
- Proper paragraph spacing

**Using the template module:**

```python
from shared.email_template import render_email, save_email_draft

# Build your email content as HTML
content = '''
    <p>Quick update on last week's performance:</p>

    <table>
        <tr>
            <th>Metric</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Revenue</td>
            <td>£3,500</td>
        </tr>
        <tr>
            <td>ROAS</td>
            <td>320%</td>
        </tr>
    </table>

    <p>All looking good.</p>
'''

# Render with template
html = render_email(
    content=content,
    recipient_name="Barry",  # From client context
    sender_name="Peter",     # Default
    sign_off="Regards"       # Or "Best", "Kind regards", etc.
)

# Save and open
filepath = "clients/bright-minds/documents/email-draft-2025-12-15-weekly-update.html"
save_email_draft(html, filepath, open_in_browser=True)
```

**Content formatting** (within the `content` parameter):
- Use `<p>` for paragraphs
- Use `<ul>` and `<li>` for bullet lists
- Use `<table>` for data tables
- Use `<strong>` for emphasis
- Use `<br>` for line breaks within paragraphs

**NEVER create email HTML manually** - always use the template module

**British English Rules** (UK clients only):
- analyse (not analyze)
- optimise (not optimize)
- customisation (not customization)
- emphasise (not emphasize)
- realise (not realize)
- colour (not color)
- behaviour (not behavior)

**US clients** (Superspace US, etc.): Use American spelling

**ROAS Format** (CRITICAL):
- Always express as percentage: **400%**, **292%**, **550%**
- NEVER as £X.XX format (not £4.00, £2.92, £5.50)

### 5. Save and Open

**Filename format**:
```
clients/[client-name]/documents/email-draft-YYYY-MM-DD-[topic-slug].html
```

**Topic slug rules**:
- Lowercase, hyphens only
- Max 4-5 words
- Examples: `october-performance`, `budget-increase-proposal`, `pmax-strategy-update`

**After saving**:
1. Confirm file location to user
2. Open file in default browser automatically (user copies from browser to Apple Mail)
3. Provide brief summary of email content

---

## Email Type Templates

### Performance Update Email
```
Opening: Brief context (time period, what's being covered)
↓
Key Metrics: 2-3 headline numbers (revenue, ROAS, spend)
↓
Analysis: What drove the performance (1-2 paragraphs)
↓
Recommendations: 2-3 specific next steps
↓
Closing: What happens next
```

### Budget Proposal Email
```
Opening: Current situation context
↓
Opportunity: What you've identified (data-driven)
↓
Recommendation: Specific budget change with expected impact
↓
Rationale: Why this makes sense (2-3 points)
↓
Next Steps: What you need from client
```

### Strategy Proposal Email
```
Opening: Context for the proposal
↓
Current State: Brief snapshot of relevant performance
↓
Opportunity: What could be improved/tested
↓
Proposal: Specific strategy with expected outcomes
↓
Timeline: When this would happen and how long to test
```

### Issue Update Email
```
Opening: Acknowledge the issue
↓
Root Cause: What happened (brief, factual)
↓
Resolution: What's been done to fix it
↓
Impact: How it affected performance (if measurable)
↓
Prevention: Steps taken to prevent recurrence
```

---

## Data Integration

**Pull live data when relevant**:
- Use Google Ads MCP for performance metrics
- Reference recent reports from `clients/[client]/reports/`
- Check experiment log for recent changes
- Review tasks-completed.md for recent work

**Metrics to include** (when relevant):
- Revenue / Conversion Value
- ROAS (as percentage!)
- Spend
- Conversions
- Impressions / Clicks (only if relevant to the story)

**Date ranges**:
- Weekly updates: Last 7 days vs previous 7 days
- Monthly updates: Full month vs previous month
- Strategy proposals: Last 30 days for context

---

## Quality Checks

Before saving, verify:
- [ ] British English spelling (for UK clients)
- [ ] ROAS expressed as percentage (not £X.XX)
- [ ] HTML format with proper styling
- [ ] Tight spacing (line-height: 1.4, 6px margins)
- [ ] `<strong>` tags for emphasis (not `<b>`)
- [ ] Client name spelled correctly
- [ ] Filename follows convention
- [ ] Saved to correct client folder
- [ ] Tone matches client preferences from CONTEXT.md

---

## Client-Specific Preferences

Load these from CONTEXT.md automatically:

**Devonshire Hotels**:
- Focus on profitability (revenue per booking matters more than volume)
- Monthly reporting cycle, detailed analysis expected
- Prefer visual data presentations (link to charts/graphs)

**Smythson**:
- Brand-conscious, careful with messaging
- Multiple stakeholders (align on key points)
- Focus on brand vs performance balance

**National Design Academy**:
- Budget-sensitive, ROI-focused
- Fast-moving, responsive to changes
- Geographic performance important (country-level)

**Superspace**:
- Data-driven, analytical
- US + UK markets (different strategies)
- Growth-focused

**Add others as needed** - Check CONTEXT.md for each client

---

## Example Outputs

### Example 1: Performance Update
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.4; color: #333; }
        p { margin: 6px 0; }
        ul, ol { margin: 6px 0; padding-left: 20px; }
        li { margin: 6px 0; }
        strong { font-weight: 600; }
    </style>
</head>
<body>
    <p>Hi [Name],</p>

    <p>Quick update on October's performance for your Google Ads campaigns.</p>

    <p><strong>Key Metrics</strong><br>
    Revenue: £24,680 (+12% vs September)<br>
    ROAS: 420% (target: 400%)<br>
    Spend: £5,876</p>

    <p>The improvement was driven by two main factors: the Performance Max campaign scaled well with the increased budget (now accounting for 65% of revenue), and we paused several underperforming product categories which freed up budget for top performers.</p>

    <p>For November, I'd recommend maintaining this budget level and testing a new asset group focused on your gift range, which typically sees strong demand in the run-up to Christmas.</p>

    <p>Let me know if you'd like to discuss this further.</p>

    <p>Best,<br>
    Pete</p>
</body>
</html>
```

### Example 2: Budget Proposal
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.4; color: #333; }
        p { margin: 6px 0; }
        ul, ol { margin: 6px 0; padding-left: 20px; }
        li { margin: 6px 0; }
        strong { font-weight: 600; }
    </style>
</head>
<body>
    <p>Hi [Name],</p>

    <p>I've spotted a clear opportunity to scale your Shopping campaigns based on recent performance data.</p>

    <p><strong>Current Situation</strong><br>
    Your campaigns are consistently hitting their daily budget limits by early afternoon, meaning we're missing out on profitable traffic. Over the last 30 days, impression share data shows we're losing approximately 35% of potential impressions due to budget constraints.</p>

    <p><strong>Recommendation</strong><br>
    Increase daily budget from £200 to £280 (+40%). Based on current ROAS of 480%, this should generate an additional £380-£450 per day in revenue.</p>

    <p><strong>Why This Makes Sense</strong></p>
    <ul>
        <li>Current ROAS (480%) is well above your target (400%)</li>
        <li>Search impression share is only 52%, indicating strong untapped demand</li>
        <li>Cost per conversion has remained stable despite scaling in previous tests</li>
    </ul>

    <p>I'd suggest implementing this change from November 1st and reviewing after two weeks. If performance holds, we're looking at approximately £10k additional monthly revenue.</p>

    <p>Let me know if you'd like to proceed.</p>

    <p>Best,<br>
    Pete</p>
</body>
</html>
```

---

## Edge Cases

**Multiple recipients**:
- Use "Hi both" or "Hi team" if multiple stakeholders
- Check CONTEXT.md for decision-maker dynamics

**Sensitive topics** (budget cuts, poor performance):
- Lead with solution, not problem
- Be factual, not defensive
- Frame as opportunity to optimize

**Complex topics**:
- Break into multiple emails if needed
- Link to longer documents instead of including everything
- Consider if a meeting would be better

**Urgent issues**:
- More direct opening: "Quick heads up on..."
- Clear action required statement
- Timeline for response/action

---

## Success Criteria

A good email draft should:
1. **Be immediately copy/paste ready** - No edits needed
2. **Match client tone** - Reflects relationship and preferences
3. **Include relevant data** - Specific metrics when applicable
4. **Be actionable** - Clear next steps
5. **Be scannable** - Busy clients can get the gist in 15 seconds
6. **Be correctly formatted** - HTML, British English, tight spacing

---

## Integration Notes

**Works with**:
- Client CONTEXT.md files
- Google Ads MCP (for live metrics)
- Recent reports and documents
- Experiment logs (for context on changes)

**Outputs to**:
- `clients/[client-name]/documents/email-draft-YYYY-MM-DD-[topic].html`
- Auto-opens in browser for copy/paste

**Follow-up**:
- After user sends email, ask if they want it logged to experiment notes
- Suggest adding key decisions to CONTEXT.md
