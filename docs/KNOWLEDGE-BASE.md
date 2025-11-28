# Knowledge Base System

**Last Updated:** November 5, 2025

The Pete's Brain Knowledge Base is a curated reference library of Google Ads best practices, AI strategies, platform updates, and industry insights. It provides authoritative, up-to-date reference materials that inform strategic advice and recommendations.

For architectural overview, see [CLAUDE.md](../CLAUDE.md).

---

## Overview

**Location**: `roksys/knowledge-base/`

**Purpose**: Self-updating reference library that ensures recommendations are grounded in current best practices, not generic knowledge.

**Current Size**: 178+ documents across 9 categories

---

## How It Works

### Automated Inbox System

The knowledge base uses a three-stage pipeline to automatically curate content:

```
┌──────────────────────────────────────────────────┐
│  STAGE 1: Automated Content Collection          │
│  - RSS monitors (Google Ads & AI news)          │
│  - Manual drops (user adds files to inbox)      │
│  - Email integration (optional)                  │
└──────────────┬───────────────────────────────────┘
               │ Every 6 hours
               ▼
┌──────────────────────────────────────────────────┐
│  STAGE 2: AI Processing                          │
│  - Claude API analyzes content                   │
│  - Determines topic and category                 │
│  - Formats as markdown with frontmatter         │
└──────────────┬───────────────────────────────────┘
               │ Every 2 hours
               ▼
┌──────────────────────────────────────────────────┐
│  STAGE 3: Organization                           │
│  - Files moved to appropriate category           │
│  - Index updated automatically                   │
│  - Ready for Claude Code to reference           │
└──────────────────────────────────────────────────┘
```

### 1. Content Collection (Automated)

**RSS Monitors:**
- Google Ads Industry News Monitor (9+ Google Ads industry sources)
- Facebook Ads Industry News Monitor (10+ Facebook/Meta advertising sources)
- AI News Monitor (12 AI/ML news sources)
- Run every 6 hours via LaunchAgent
- Articles scored 0-10 for relevance (6+ imported)

**Manual Drops:**
- User adds files to `roksys/knowledge-base/_inbox/`
- Supported formats: PDF, markdown, HTML, plain text, video transcripts
- No filename requirements - processor handles everything

**Email Integration (Optional):**
- Connect Gmail sync to forward industry newsletters
- Platform update emails from Google
- See `roksys/knowledge-base/EMAIL-INTEGRATION.md` for setup

### 2. AI Processing

**Processor:** `agents/knowledge-base-processor/knowledge-base-processor.py`

**What it does:**
1. Reads content from inbox
2. Uses Claude API to:
   - Identify main topics and themes
   - Determine appropriate category
   - Extract key insights
   - Generate summary
3. Formats as markdown with YAML frontmatter
4. Moves to category folder
5. Updates KB index

**Runs:** Every 2 hours via LaunchAgent

### 3. Organization

**Category Structure:**
```
knowledge-base/
├── google-ads/
│   ├── performance-max/        # PMax strategies, optimization
│   ├── shopping/                # Shopping campaigns, feed optimization
│   ├── search/                  # Search campaigns, keyword strategies
│   ├── platform-updates/        # Official Google announcements ⭐
│   └── bidding-automation/      # Smart Bidding, tROAS
├── facebook-ads/                # Facebook & Instagram Ads
│   ├── campaigns/              # Campaign strategies, optimization
│   ├── audiences/               # Audience targeting, lookalikes
│   ├── creative/                # Ad creative best practices
│   ├── platform-updates/        # Meta/Facebook announcements ⭐
│   ├── bidding-optimization/   # Bid strategies, cost caps
│   ├── measurement/             # Pixel, Conversions API, attribution
│   └── meta-business-suite/     # Meta Business Suite features
├── ai-strategy/                 # AI in marketing, automation
├── analytics/                   # GA4, attribution, tracking
├── industry-insights/           # Market trends, research
└── rok-methodologies/           # ROK's proprietary frameworks
```

---

## Categories

### google-ads/performance-max/

Performance Max campaign strategies, optimization techniques, asset management, audience signals, and best practices.

**Common topics:**
- Asset group optimization
- Audience signal strategies
- Performance Max vs Shopping
- Budget allocation
- Creative best practices

### google-ads/shopping/

Shopping campaigns, product feed optimization, Merchant Center management, product performance, and e-commerce strategies.

**Common topics:**
- Feed optimization
- Product title/description best practices
- Supplemental feeds
- Product segmentation
- Merchant Center troubleshooting

### google-ads/search/

Search campaigns, keyword strategies, ad copy optimization, RSAs (Responsive Search Ads), and search best practices.

**Common topics:**
- Keyword match types
- RSA optimization
- Search query analysis
- Negative keyword strategies
- Ad copy testing

### google-ads/platform-updates/

Official Google Ads announcements, platform changes, algorithm updates, new features, and deprecations.

**Common topics:**
- Algorithm changes
- New campaign types
- Feature launches
- Policy updates
- Beta features

⭐ **CRITICAL**: Check this folder when analyzing performance changes. Platform updates often have 2-4 week delayed impact.

### google-ads/bidding-automation/

Smart Bidding strategies, tROAS (target ROAS), automated bidding, conversion optimization, and bidding best practices.

**Common topics:**
- tROAS optimization
- Learning periods
- Conversion value rules
- Bid strategy selection
- Performance troubleshooting

### ai-strategy/

AI tools for marketing, generative AI, marketing automation, machine learning applications, and AI strategy.

**Common topics:**
- AI content generation
- Marketing automation
- Predictive analytics
- AI assistants and chatbots
- Enterprise AI adoption

### analytics/

Google Analytics 4 (GA4), attribution models, conversion tracking, measurement, and analytics best practices.

**Common topics:**
- GA4 migration
- Conversion tracking setup
- Attribution modeling
- Custom dimensions/metrics
- Data analysis techniques

### industry-insights/

Market trends, competitive intelligence, industry research, case studies, and advertising trends.

**Common topics:**
- E-commerce trends
- Consumer behavior
- Industry benchmarks
- Case studies
- Competitive analysis

### rok-methodologies/

ROK's proprietary frameworks, processes, and methodologies developed through client work.

**Common topics:**
- Experiment logging protocol
- Client analysis workflows
- Product Hero/Villain classification
- ROAS optimization frameworks
- Account audit templates

---

## When to Use the Knowledge Base

**IMPORTANT**: Before providing strategic advice on campaigns, optimization, or platform features, **CHECK THE KNOWLEDGE BASE** for relevant, up-to-date information.

### Primary Use Cases

#### 1. Platform Updates

**When:** Analyzing performance changes, investigating anomalies

**Where:** `knowledge-base/google-ads/platform-updates/`

**Why:** Platform changes have 2-4 week delayed impact. A performance change today might be caused by a Google update 3 weeks ago.

**Process:**
1. Check KB for updates from 2-4 weeks before the performance change
2. Match timing of updates to observed changes
3. Cross-reference with Google Ads Change History
4. Cite KB article when explaining to user

#### 2. Campaign Strategy

**When:** Planning new campaigns, optimizing existing ones

**Where:** Category-specific folders (performance-max/, shopping/, search/)

**Why:** Ensure recommendations follow current best practices

**Process:**
1. Identify campaign type (PMax, Shopping, Search)
2. Check relevant KB category for best practices
3. Read client CONTEXT.md for client-specific constraints
4. Combine KB + context for tailored recommendations

#### 3. Optimization Advice

**When:** Client asks for optimization recommendations

**Where:** `bidding-automation/` for bidding, category folders for other optimizations

**Why:** Reference authoritative guidance rather than generic advice

**Process:**
1. Check KB for current best practices
2. Review client CONTEXT.md for past experiments
3. Consider client's specific situation
4. Provide KB-informed, context-aware recommendations

#### 4. Client Questions

**When:** Client asks about new features, platform changes, or strategies

**Where:** Relevant category based on question

**Why:** Cross-reference KB docs with client context for informed answers

**Process:**
1. Search KB for relevant documents
2. Read client CONTEXT.md for past discussions
3. Combine for comprehensive, contextual answer
4. Cite sources (KB articles + client history)

#### 5. New Features

**When:** Client asks about or considers adopting new Google Ads features

**Where:** `platform-updates/` and relevant category

**Why:** Check if KB has documentation before giving generic advice

**Process:**
1. Search KB for feature name
2. Review any platform updates about the feature
3. Check for ROK methodologies or case studies
4. Provide informed recommendation with sources

---

## Integration with Client Work

### Standard Workflow

When working on client tasks:

1. **Read client CONTEXT.md** (business context, history, preferences)
2. **Check relevant KB documents** (platform best practices, recent updates)
3. **Combine both sources** for informed, contextual advice
4. **Reference both sources** in recommendations

### Example: Asset Group Expansion Decision

**User:** "Should we enable asset group expansion for Smythson's PMax campaign?"

**Claude Code Process:**

1. **Read client context:**
   ```bash
   Read: clients/smythson/CONTEXT.md
   ```
   Learns: Smythson is luxury brand with strict brand guidelines, past issues with automated features showing products incorrectly

2. **Check KB:**
   ```bash
   Read: roksys/knowledge-base/google-ads/performance-max/asset-group-expansion.md
   ```
   Learns: Asset expansion increases reach but reduces control, best for brands comfortable with automation

3. **Provide recommendation:**
   > Based on KB best practices (knowledge-base/google-ads/performance-max/asset-group-expansion.md),
   > asset expansion can increase reach by 10-15% but reduces creative control.
   >
   > Given Smythson's strict brand guidelines and past issues with automated features
   > (per CONTEXT.md), I'd recommend starting conservatively:
   > - Enable for one asset group as a test
   > - Monitor ad preview closely for first week
   > - Compare performance vs non-expanded asset groups
   > - Scale if creative quality maintained
   >
   > This aligns with your brand-first approach while testing the feature's potential.

4. **Reference both sources:**
   - KB provides best practices
   - CONTEXT.md provides client-specific constraints
   - Recommendation combines both

---

## Citation Format

When using KB information, cite the source:

### In-Line Citations

- "Per knowledge-base/google-ads/performance-max/asset-optimization.md, the recommended approach is..."
- "According to recent platform updates (KB: platform-updates/2025-10-pmax-changes.md), Google now..."
- "ROK's methodology (KB: rok-methodologies/experiment-logging-guide.md) suggests..."

### Reference Citations

When providing detailed recommendations:
```
RECOMMENDATION: Increase tROAS from 400% to 450%

RATIONALE:
- KB Reference: knowledge-base/google-ads/bidding-automation/troas-optimization.md
  "When impression share is capped at 90%+, increasing tROAS by 10-15% can unlock
  additional volume while maintaining efficiency"
- Client Context: Per CONTEXT.md, current impression share is 95% (capped)
- Expected Outcome: Volume increase 15-20%, ROAS maintains 400%+
```

---

## Adding Content to the Knowledge Base

### User Workflow (Automated)

1. **Drop files in inbox:** `roksys/knowledge-base/_inbox/{emails,documents,videos}/`
2. **Wait for processing:** Every 2 hours automatically, or manual run
3. **Files organized:** Automatically categorized and formatted

### Manual Processing

```bash
cd /Users/administrator/Documents/PetesBrain
python3 agents/knowledge-base-processor/knowledge-base-processor.py
```

### Claude Code Workflow (When Asked to Add Content)

1. User provides URL, article text, or video transcript
2. Analyze content to determine category
3. Create formatted markdown with frontmatter
4. Save to appropriate category folder
5. Update knowledge base README index

### File Format

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
- Key point 3

## Full Content
[content here]

## Key Insights
- Actionable insight 1
- Strategic implication 2
- Recommendation 3
```

---

## Automated News Monitoring

### Google Ads Industry News Monitor

**Location:** `agents/industry-news-monitor/industry-news-monitor.py`
**Schedule:** Every 6 hours via LaunchAgent
**Sources:** 9+ Google Ads industry websites

**What it monitors:**
- Search Engine Land (Google Ads & PPC)
- Search Engine Journal (PPC)
- Google Ads Blog (Official)
- Think with Google
- WordStream Blog
- PPC Hero
- Neil Patel Blog
- Unbounce Blog

**Process:**
1. Checks RSS feeds for new articles
2. Uses Claude API to score relevance (0-10)
3. Articles scoring 6+ imported to KB inbox
4. KB processor categorizes and formats

### Facebook Ads Industry News Monitor

**Location:** `agents/facebook-news-monitor/facebook-news-monitor.py`
**Schedule:** Every 6 hours via LaunchAgent
**Sources:** 10+ Facebook/Meta advertising industry websites

**What it monitors:**
- Meta for Business Blog (Official)
- Social Media Examiner (Facebook Ads)
- AdEspresso Blog
- WordStream (Facebook Ads)
- Hootsuite Blog (Facebook)
- Buffer Blog (Facebook)
- Sprout Social (Facebook)
- Reddit r/FacebookAds
- And more...

**Process:**
1. Checks RSS feeds for new articles
2. Uses Claude API to score relevance (0-10)
3. Articles scoring 6+ imported to KB inbox
4. KB processor categorizes and formats

**Configuration:**
- Relevance threshold: 6/10 minimum
- State tracking: `shared/data/industry-news-state.json`
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.industry-news.plist`
- Log: `~/.petesbrain-industry-news.log`

### AI News Monitor

**Location:** `agents/ai-news-monitor/ai-news-monitor.py`
**Schedule:** Every 6 hours via LaunchAgent
**Sources:** 12 AI/ML news websites

**What it monitors:**
- **Marketing AI:** Marketing AI Institute, MarTech, Adweek
- **Major AI Companies:** OpenAI Blog, Google AI Blog, Microsoft AI Blog, Anthropic News
- **AI News & Analysis:** MIT Technology Review, VentureBeat, AI News
- **Practical AI/ML:** Machine Learning Mastery, Towards Data Science

**Scoring criteria:**
- **HIGH (8-10):** AI tools for marketing, generative AI, marketing automation, AI strategy
- **MEDIUM (5-7):** General AI trends, AI product launches, ML fundamentals
- **LOW (0-4):** Pure academic research, non-marketing AI applications

**Configuration:**
- Relevance threshold: 6/10 minimum
- State tracking: `shared/data/ai-news-state.json`
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.ai-news.plist`
- Log: `~/.petesbrain-ai-news.log`

### Manual Commands

```bash
# Run industry news monitor manually
cd /Users/administrator/Documents/PetesBrain
ANTHROPIC_API_KEY="key" agents/industry-news-monitor/industry-news-monitor.py

# Run AI news monitor manually
ANTHROPIC_API_KEY="key" agents/ai-news-monitor/ai-news-monitor.py

# Process KB inbox after news import
python3 agents/knowledge-base-processor/knowledge-base-processor.py
```

---

## Maintenance

### Automated Processing

- **Inbox processing:** Every 2 hours via LaunchAgent
- **Industry news import:** Every 6 hours via LaunchAgent
- **AI news import:** Every 6 hours via LaunchAgent

### Logs

- **KB Processor:** `~/.petesbrain-knowledge-base.log` and `shared/data/kb-processing.log`
- **Industry News:** `~/.petesbrain-industry-news.log`
- **AI News:** `~/.petesbrain-ai-news.log`

### State Files

- **KB Processing:** `shared/data/kb-state.json`
- **Industry News:** `shared/data/industry-news-state.json`
- **AI News:** `shared/data/ai-news-state.json`

### Manual Commands

```bash
# Check KB processor status
launchctl list | grep knowledge-base

# View KB processor logs
cat ~/.petesbrain-knowledge-base.log | tail -50

# Run KB processor manually
python3 agents/knowledge-base-processor/knowledge-base-processor.py

# Check news monitor status
launchctl list | grep industry-news
launchctl list | grep ai-news
```

---

## Email Integration (Optional)

The knowledge base can integrate with the email sync system to automatically import:
- Google Ads platform update emails
- Industry newsletter content (Search Engine Land, WordStream, etc.)
- AI/ML updates from trusted sources

See `roksys/knowledge-base/EMAIL-INTEGRATION.md` for setup instructions.

---

## Setup

### Initial Setup

1. **Install dependencies:**
   ```bash
   cd /Users/administrator/Documents/PetesBrain
   cd agents/facebook-news-monitor
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export ANTHROPIC_API_KEY="your-key-here"
   ```

3. **Install LaunchAgents:**
   ```bash
   # Copy plist files
   cp agents/launchagents/com.petesbrain.knowledge-base.plist ~/Library/LaunchAgents/
   cp agents/launchagents/com.petesbrain.industry-news.plist ~/Library/LaunchAgents/
   cp agents/launchagents/com.petesbrain.ai-news.plist ~/Library/LaunchAgents/

   # Load agents
   launchctl load ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist
   launchctl load ~/Library/LaunchAgents/com.petesbrain.industry-news.plist
   launchctl load ~/Library/LaunchAgents/com.petesbrain.ai-news.plist
   ```

4. **Test:**
   ```bash
   # Add test file to inbox
   echo "Test content" > roksys/knowledge-base/_inbox/documents/test.txt

   # Run processor manually
   python3 agents/knowledge-base-processor/knowledge-base-processor.py

   # Check if processed
   ls roksys/knowledge-base/
   ```

### Setup Script

```bash
# Automated setup (if available)
cd /Users/administrator/Documents/PetesBrain/roksys/knowledge-base
./setup-automation.sh
```

---

## Quick Start Guide

See `roksys/knowledge-base/QUICKSTART.md` for detailed setup instructions.

---

## Search and Discovery

### Finding Relevant Documents

```bash
# Search by keyword
grep -r "keyword" roksys/knowledge-base/

# Search specific category
grep -r "keyword" roksys/knowledge-base/google-ads/shopping/

# List recent additions
ls -lt roksys/knowledge-base/google-ads/platform-updates/ | head -10

# Search by tag (requires frontmatter parsing)
# Or use tools/kb-search.py for advanced search
```

### Knowledge Base Search Tool

**Location:** `tools/kb-search.py`
**Purpose:** Search 178+ knowledge base documents instantly

See `docs/KNOWLEDGE-BASE-SEARCH.md` for complete documentation.

---

## Best Practices

### For Claude Code

1. **Check KB before strategic advice** - Ensure recommendations are current
2. **Cite KB sources** - Show where recommendations come from
3. **Combine KB + context** - KB provides best practices, CONTEXT.md provides client constraints
4. **Update client context** - When KB insights inform client work, document in CONTEXT.md
5. **Check platform updates** - When analyzing performance changes, check KB for updates 2-4 weeks prior

### For Users

1. **Drop files in inbox** - Don't organize manually, let the processor handle it
2. **Trust the automation** - Files are processed every 2 hours automatically
3. **Review processed files** - Check that categorization makes sense
4. **Update when needed** - If KB article is outdated, replace or supplement it
5. **Share valuable content** - When you find great articles, drop them in the inbox

---

## Statistics

**As of November 2025:**
- 178+ documents
- 9 categories
- 50+ platform updates
- 30+ Performance Max docs
- 25+ Shopping docs
- 20+ AI strategy docs
- Auto-import from 21 RSS sources (9 Google Ads + 12 AI)
- Processing every 2 hours
- News monitoring every 6 hours

---

**Remember:** The Knowledge Base is your source of truth for platform best practices. Always consult it before providing strategic advice, and always combine it with client CONTEXT.md for tailored recommendations.
