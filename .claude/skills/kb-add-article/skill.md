---
name: kb-add-article
description: Add articles to the knowledge base with URL fetch, metadata prompts, relevance scoring, and YAML frontmatter. Handles both URL and pasted content with fallback workflow.
allowed-tools: Read, Write, WebFetch, AskUserQuestion
---

# Knowledge Base Article Adder Skill

---

## Core Workflow

When this skill is triggered:

### 1. Detect Input Type

**Ask user**: "Do you have a URL or are you pasting content?"

**Options**:
- URL - I'll fetch it for you
- Pasted text - Paste the content
- Adalysis/paywall - I'll ask for manual paste fallback

### 2. Fetch Content (if URL provided)

**Attempt fetch**:
```
WebFetch(url, prompt="Extract the article title, author, publication date, and full content")
```

**Handle failures gracefully**:
- 404 / 403 → "URL not accessible, switch to pasted content?"
- Timeout → "Couldn't fetch (paywall/blocked), paste content instead?"
- Success → Parse content, proceed to metadata step

### 3. Extract Metadata from Content

**Automatically extract** (if available in content):
- **Title** - Article headline
- **Author** - Article author (if visible)
- **Publication Date** - When article was published
- **Source/Publication** - Where it came from (e.g., "MarTech", "Search Engine Journal", "Google Blog")

### 4. Prompt for Category & Overrides

**Ask user**:
```
Category (required):
- Google Ads
- Performance Max
- AI / Machine Learning
- Facebook Ads
- Microsoft Ads
- E-commerce
- Digital Marketing
- AI News
- Other: [type custom]

Override author? (optional)
Override publication date? (optional, YYYY-MM-DD format)
Any tags? (optional, comma-separated)
```

**Store user selections**:
- category = user choice
- author = extracted OR user override
- published = extracted OR user override
- tags = user input (optional)

### 5. Score Relevance

**Analyze content** for relevance to your business:

**Score 9-10** (Critical):
- Directly applicable to active clients (e.g., new Google Ads feature)
- Major market changes (e.g., iOS privacy update impact)
- Emerging opportunities (e.g., new campaign type)

**Score 7-8** (High):
- Useful for client strategy (e.g., automation best practices)
- General industry knowledge (e.g., seasonal trends)
- Adjacent to current work (e.g., AI copywriting tools)

**Score 5-6** (Moderate):
- Interesting context (e.g., competitor analysis, market reports)
- Supporting knowledge (e.g., psychology of conversion optimization)
- Nice-to-know trends

**Score 3-4** (Low):
- Tangentially related (e.g., general marketing trends)
- Archive value only
- Historical interest

**Score 1-2** (Minimal):
- Very tangential (e.g., unrelated industry)
- Outdated information
- Not useful for business

### 6. Generate YAML Frontmatter

**Format**:
```yaml
---
source: [Publication Name]
url: [Full URL if available, or "Manual entry"]
published: [Date in "Mon, DD Mmm YYYY HH:MM:SS +0000" format, or "Unknown" if not found]
relevance_score: [0-10 number]
primary_topic: [One-line summary of main topic]
fetched: [ISO timestamp: 2025-12-11T14:31:10.687925]
category: [Selected category]
author: [Extracted or overridden]
tags: [Comma-separated tags if provided]
---
```

### 7. Format Content

**Structure**:

```markdown
---
[YAML frontmatter]
---

# [Article Title]

**Source**: [Publication Name]
**URL**: [Full URL or "Manual entry"]
**Published**: [Date]
**Relevance Score**: [N]/10
**Category**: [Category]

## Summary

[Article summary - 1-2 paragraphs covering key points]

## Key Takeaways

[Bullet points of main insights]

## Relevance to Business

[Why this matters for your work - 1-2 sentences]

---

*Article added: [Date]
Manual entry: [If applicable]*
```

### 8. Generate Filename

**Pattern**:
```
YYYY-MM-DD_category_title-slug.md
```

**Rules**:
- Date = today's date (YYYY-MM-DD format)
- Category = lowercase version of selected category
- Title slug = lowercase, max 60 characters, hyphens only
- Example: `2025-12-11_google-ads_new-pmax-features.md`

### 9. Write to Knowledge Base Inbox

**Location**:
```
/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/_inbox/documents/[filename]
```

**Create file** with full content (YAML + markdown)

### 10. Confirm & Summary

**Display**:
```
✅ Article added to knowledge base

📄 File: roksys/knowledge-base/_inbox/documents/[filename]
📊 Relevance Score: [X]/10
🏷️ Category: [Category]
🔗 Source: [Publication/URL]
📅 Published: [Date]

The article will be processed by the knowledge base system and indexed for search.
```

---

## Category Reference

**Quick decision tree**:

```
Is it about Google Ads features?
  → Google Ads

Is it specifically about Performance Max?
  → Performance Max

Is it about AI/ML technology?
  → AI / Machine Learning

Is it about Facebook/Meta advertising?
  → Facebook Ads

Is it about Microsoft Ads/Bing?
  → Microsoft Ads

Is it about e-commerce/shopping/retail?
  → E-commerce

Is it general marketing/copywriting/CRO?
  → Digital Marketing

Is it general AI news (not specific to ads)?
  → AI News

Doesn't fit?
  → Other: [custom]
```

---

## Content Extraction Guidelines

**If using WebFetch**:
- Extract title from `<h1>` or metadata
- Extract author from byline, schema markup, or author tags
- Extract publication date from article metadata or timestamp
- Get main content (remove navigation, ads, related articles)
- Preserve key formatting (subheadings, lists, emphasis)

**If manual paste**:
- User provides raw content
- Script extracts title (usually first line)
- Prompts for author/date if not obvious
- Uses content as-is

**If fetch fails** (paywall/blocked):
- Gracefully fall back to manual paste
- Use title/url from initial context if available
- Mark as "Content from paste" in file

---

## Fallback Workflow (Paywall/Blocked Content)

**Scenario**: User provides URL, WebFetch fails (e.g., Adalysis, Medium paywall)

**Prompt**:
```
The URL didn't load (paywall/blocked).

You have two options:
1. Paste the content manually
2. Cancel and save URL/title only for manual review later
```

**If paste**:
- Use pasted content as article body
- Keep source/URL metadata from original request
- Mark source as "Paywalled article" or "Manual paste"
- Lower relevance scoring (might be incomplete)

**If cancel**:
- Create minimal entry with URL + title only
- File location: `_inbox/documents/[date]_[category]_[title-slug]-url-only.md`
- Content: Just YAML + title + "See URL for full content"

---

## Quality Checks

Before writing, verify:
- [ ] Category selected
- [ ] Title extracted or user-provided
- [ ] URL accessible (or marked as manual paste)
- [ ] Relevance score 1-10
- [ ] Filename follows pattern
- [ ] YAML frontmatter valid (properly formatted)
- [ ] Summary captures main points
- [ ] Relevance to business explained

---

## Examples

### Example 1: Google Ads Article (URL Fetch)

**User**: Provides URL to Google Blog article about PMax updates

**Steps**:
1. Fetch succeeds ✅
2. Extract: Title "New PMax features for Q1 2026", published date, author
3. Ask: Category? → "Performance Max"
4. Generate relevance score: 9/10 (directly applicable to active clients)
5. Write file: `2025-12-11_performance-max_new-pmax-features-q1-2026.md`
6. Confirm: "✅ Article added | Score: 9/10 | File: roksys/knowledge-base/..."

### Example 2: Paywalled Article (Fallback to Paste)

**User**: Provides Adalysis URL (paywall)

**Steps**:
1. Fetch fails ❌ (403 paywall)
2. Prompt: "Paste content?"
3. User pastes article text
4. Extract: Title from pasted content, author if visible
5. Ask: Category? → "Google Ads"
6. Ask: Publication date? → "2025-12-10"
7. Generate relevance score: 7/10
8. Write file: `2025-12-11_google-ads_adalysis-article.md`
9. Note in file: "Content from paywalled source - pasted manually"

### Example 3: AI News (Auto-score)

**User**: Provides URL to AI news article about Claude updates

**Steps**:
1. Fetch succeeds ✅
2. Extract metadata
3. Ask: Category? → "AI News"
4. Generate relevance score: 6/10 (interesting context for automation, but not directly client-facing)
5. Write file: `2025-12-11_ai-news_claude-updates-december.md`
6. Confirm with relevance rationale

---

## Integration Notes

**Works with**:
- WebFetch (for URL content)
- Knowledge base system (inbox feeds into main KB)
- Manual paste fallback (for paywalled content)

**Outputs to**:
- `/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/_inbox/documents/[filename]`

**Processing**:
- Knowledge base system processes inbox weekly
- Moves articles to main KB structure
- Makes searchable via kb-search skill

**For editing later**:
- Files can be manually edited before KB processing
- Changes preserved when article moves to main KB

---

## Success Criteria

A well-added article should:
1. Have complete metadata (YAML frontmatter)
2. Include clear summary of key points
3. Explain relevance to business
4. Be properly categorised
5. Have realistic relevance score (3-8 typical, 9-10 rare)
6. Follow filename convention
7. Be saved to correct location
8. Display confirmation with score
