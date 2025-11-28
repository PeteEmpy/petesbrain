---
name: text-message-draft-generator
description: Generates client-ready text message drafts for WhatsApp, SMS, or other messaging apps. Use when user says "draft text", "text [client]", "WhatsApp message", "SMS [client]", or needs a short message for a messaging app.
allowed-tools: Read, Write, Bash, Glob
---

# Text Message Draft Generator Skill

---

## Core Workflow

When this skill is triggered:

### 1. Load Client Context
- Read `clients/[client-name]/CONTEXT.md` for:
  - Client preferences (tone, communication style, sensitivities)
  - Strategic context (current campaigns, goals, issues)
  - Recent work and history
- Scan recent documents/messages for context about the topic

### 2. Determine Message Type
Auto-detect the message category:
- **Quick Update** - Brief performance or status update
- **Urgent Alert** - Time-sensitive information requiring immediate attention
- **Action Required** - Client needs to take action soon
- **Check-in** - Casual follow-up or question
- **Confirmation** - Confirm an action or decision
- **Reminder** - Remind about upcoming deadline or task

### 3. Generate Message Content

**Structure (always follow this order)**:
1. **Opening** - Brief greeting (often optional for casual relationships)
2. **Key Message** - Main point in 1-2 sentences (what they need to know)
3. **Action/Next Steps** - What happens next (if applicable)
4. **Closing** - Brief sign-off (often just name or emoji)

**Tone Guidelines**:
- **Casual but professional** - Text messages are more informal than emails
- **Concise** - Get to the point immediately (text messages should be scannable in 5 seconds)
- **Friendly** - Use natural, conversational language
- **Clear** - Avoid jargon unless client uses it regularly
- **Actionable** - If action is needed, make it crystal clear

**Length Guidelines**:
- **Ideal**: 1-3 sentences (50-150 characters)
- **Maximum**: 5 sentences (300 characters)
- If more detail needed, suggest "Happy to discuss on call" or "Will email details"

### 4. Apply Formatting Standards

**HTML Format** (CRITICAL - for browser display, NOT MARKDOWN):

⚠️ **CRITICAL: ALWAYS include copy-to-clipboard button with proper line break formatting**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .message-box {
            background-color: #fff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .message-text {
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .copy-btn {
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .copy-btn:hover {
            background: #2980b9;
        }
        .copy-btn:active {
            background: #21618c;
        }
        .copied {
            background: #27ae60 !important;
        }
        .copy-hint {
            font-size: 12px;
            color: #666;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="message-box">
        <div class="message-text">Message content here with proper line breaks</div>
        <button class="copy-btn" onclick="copyContent()">📋 Copy to Clipboard</button>
        <div class="copy-hint">
            Click the button above to copy, then paste into your messaging app
        </div>
    </div>

    <script>
        function copyContent() {
            // CRITICAL: Use double quotes with \n for line breaks (NOT template literals with backticks)
            // Template literals don't preserve formatting when pasted into Teams/WhatsApp/Slack
            const text = "Paragraph 1 here.\n\nParagraph 2 here.\n\nParagraph 3 here.";

            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                btn.textContent = '✅ Copied!';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = '📋 Copy to Clipboard';
                    btn.classList.remove('copied');
                }, 2000);
            });
        }
    </script>
</body>
</html>
```

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

**Emoji Guidelines**:
- Use sparingly - only if appropriate for client relationship
- Common professional emojis: ✅ ✓ 📊 📈 ⚠️ 💡
- Avoid excessive emojis (max 1-2 per message)

### 5. Save and Open

**Filename format**:
```
clients/[client-name]/documents/text-draft-YYYY-MM-DD-[topic-slug].html
```

**Topic slug rules**:
- Lowercase, hyphens only
- Max 3-4 words
- Examples: `october-update`, `budget-approval`, `pmax-alert`

**After saving**:
1. Confirm file location to user
2. Open file in default browser automatically (user copies from browser to messaging app)
3. Provide brief summary of message content

---

## Message Type Templates

### Quick Update Message
```
Opening: [Optional greeting]
↓
Key Info: 1-2 sentences with main point
↓
Closing: [Brief sign-off]
```

**Example**:
```
Hi [Name], quick update: October campaigns hit 420% ROAS, up from 380% last month. Revenue was £24k. Will email full breakdown later today. Pete
```

### Urgent Alert Message
```
Opening: [Alert indicator]
↓
Issue: What happened (1 sentence)
↓
Action: What needs to happen (1 sentence)
↓
Timeline: When (if urgent)
```

**Example**:
```
⚠️ Quick heads up: Your Shopping campaign hit daily budget limit at 2pm today. Performance is strong (450% ROAS). Should I increase budget for tomorrow? Pete
```

### Action Required Message
```
Opening: [Brief context]
↓
Request: What you need (1 sentence)
↓
Deadline: When (if applicable)
```

**Example**:
```
Hi [Name], need approval to increase budget from £200 to £280/day. Current ROAS is 480% so this should drive +£380/day revenue. Can you confirm by end of day? Pete
```

### Check-in Message
```
Opening: [Casual greeting]
↓
Question/Update: What you're checking on (1-2 sentences)
```

**Example**:
```
Hey [Name], how did the new product launch go? Saw some good early performance on the ads. Pete
```

### Confirmation Message
```
Opening: [Brief context]
↓
Confirmation: What's confirmed (1 sentence)
↓
Next Steps: What happens next (if applicable)
```

**Example**:
```
Hi [Name], confirmed the budget increase is live from tomorrow. Will monitor closely and update you end of week. Pete
```

### Reminder Message
```
Opening: [Brief greeting]
↓
Reminder: What to remember (1 sentence)
↓
Deadline: When (if applicable)
```

**Example**:
```
Hi [Name], reminder that the Q4 strategy review is scheduled for Friday 2pm. Will send agenda tomorrow. Pete
```

---

## Data Integration

**Pull live data when relevant**:
- Use Google Ads MCP for performance metrics
- Reference recent reports from `clients/[client]/reports/`
- Check experiment log for recent changes
- Review tasks-completed.md for recent work

**Metrics to include** (when relevant, keep brief):
- Revenue / Conversion Value (round to nearest £100 or £1k)
- ROAS (as percentage!)
- Key change (up/down percentage)

**Date ranges**:
- Keep references brief: "this week", "last month", "today"
- Avoid specific date ranges unless critical

---

## Quality Checks

Before saving, verify:
- [ ] British English spelling (for UK clients)
- [ ] ROAS expressed as percentage (not £X.XX)
- [ ] HTML format with proper styling
- [ ] Message is concise (under 300 characters ideally)
- [ ] Client name spelled correctly
- [ ] Filename follows convention
- [ ] Saved to correct client folder
- [ ] Tone matches client preferences from CONTEXT.md
- [ ] Appropriate level of formality for text messaging

---

## Client-Specific Preferences

Load these from CONTEXT.md automatically:

**Devonshire Hotels**:
- More formal than average (still casual for text, but professional)
- Focus on profitability metrics
- Prefer brief updates with email follow-up for details

**Smythson**:
- Brand-conscious, careful with messaging
- More formal tone even in texts
- Keep messages brief and professional

**National Design Academy**:
- Fast-moving, responsive to changes
- More casual tone acceptable
- Action-oriented messages work well

**Superspace**:
- Data-driven, analytical
- Casual tone acceptable
- Include key metrics when relevant

**Add others as needed** - Check CONTEXT.md for each client

---

## Example Outputs

### Example 1: Quick Update
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .message-box {
            background-color: #fff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .message-text {
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .copy-hint {
            font-size: 12px;
            color: #666;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="message-box">
        <div class="message-text">Hi [Name], quick update: October campaigns hit 420% ROAS, up from 380% last month. Revenue was £24k. Will email full breakdown later today. Pete</div>
        <div class="copy-hint">
            💡 Copy the text above and paste into your messaging app (WhatsApp, Messages, etc.)
        </div>
    </div>
</body>
</html>
```

### Example 2: Urgent Alert
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .message-box {
            background-color: #fff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .message-text {
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .copy-hint {
            font-size: 12px;
            color: #666;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="message-box">
        <div class="message-text">⚠️ Quick heads up: Your Shopping campaign hit daily budget limit at 2pm today. Performance is strong (450% ROAS). Should I increase budget for tomorrow? Pete</div>
        <div class="copy-hint">
            💡 Copy the text above and paste into your messaging app (WhatsApp, Messages, etc.)
        </div>
    </div>
</body>
</html>
```

### Example 3: Action Required
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .message-box {
            background-color: #fff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .message-text {
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .copy-hint {
            font-size: 12px;
            color: #666;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="message-box">
        <div class="message-text">Hi [Name], need approval to increase budget from £200 to £280/day. Current ROAS is 480% so this should drive +£380/day revenue. Can you confirm by end of day? Pete</div>
        <div class="copy-hint">
            💡 Copy the text above and paste into your messaging app (WhatsApp, Messages, etc.)
        </div>
    </div>
</body>
</html>
```

---

## Edge Cases

**Multiple recipients**:
- Usually avoid group texts for client communications
- If group text needed, use "Hi both" or "Hi team"
- Consider if email would be more appropriate

**Sensitive topics** (budget cuts, poor performance):
- Lead with solution, not problem
- Be factual, not defensive
- Consider if email would be more appropriate for sensitive topics

**Complex topics**:
- If topic is complex, suggest email or call instead
- Text messages are for quick updates, not detailed explanations
- Use: "Happy to discuss on call" or "Will email details"

**Urgent issues**:
- Use emoji indicators (⚠️) for urgent items
- Clear action required statement
- Timeline for response/action

**Long messages**:
- If message exceeds 300 characters, consider splitting into two messages
- Or suggest switching to email for full details

---

## Success Criteria

A good text message draft should:
1. **Be immediately copy/paste ready** - No edits needed
2. **Match client tone** - Reflects relationship and preferences
3. **Be concise** - Scannable in 5 seconds, under 300 characters ideally
4. **Include relevant data** - Specific metrics when applicable (briefly)
5. **Be actionable** - Clear next steps if action needed
6. **Be correctly formatted** - HTML for browser display, proper styling
7. **Be appropriate for text messaging** - More casual than email, but still professional

---

## Integration Notes

**Works with**:
- Client CONTEXT.md files
- Google Ads MCP (for live metrics)
- Recent reports and documents
- Experiment logs (for context on changes)

**Outputs to**:
- `clients/[client-name]/documents/text-draft-YYYY-MM-DD-[topic].html`
- Auto-opens in browser for copy/paste to messaging apps

**Follow-up**:
- After user sends message, ask if they want it logged to experiment notes
- Suggest adding key decisions to CONTEXT.md if significant

**Browser Opening**:
- After saving the HTML file, use Python's `webbrowser` module to open automatically
- Command: `import webbrowser; webbrowser.open('file:///absolute/path/to/file.html')`
- This allows user to easily copy text from browser and paste into messaging app

