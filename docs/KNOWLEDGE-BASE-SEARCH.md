# Knowledge Base Search System

**Status:** ✅ Active  
**Last Updated:** 2025-11-05

## Overview

The Knowledge Base Search System makes your **178 knowledge files** (117,000+ words) instantly searchable. Find relevant information about Google Ads, AI strategy, analytics, and ROK methodologies in seconds.

## Quick Start

### Basic Search
```bash
cd /Users/administrator/Documents/PetesBrain
python3 tools/kb-search.py "performance max strategies"
```

### View Statistics
```bash
python3 tools/kb-search.py --stats
```

### Search Specific Category
```bash
python3 tools/kb-search.py --category "google-ads" "shopping campaigns"
```

### AI-Powered Search (requires anthropic library)
```bash
# Install first: pip install anthropic
python3 tools/kb-search.py --ai "how to optimize pmax campaigns"
```

## Features

### 📊 **Knowledge Base Statistics**
- **178 files** indexed
- **117,324 words** of knowledge
- **10 categories** organized

**Breakdown:**
- `ai-strategy` - 65 files (48,397 words) - AI in marketing, automation, ML
- `uncategorized` - 49 files (22,932 words) - Inbox emails and misc
- `analytics` - 18 files (12,748 words) - GA4, attribution, tracking
- `industry-insights` - 17 files (8,878 words) - Market trends, competitive intel
- `google-ads/platform-updates` - 13 files (8,654 words) - Platform announcements
- `rok-methodologies` - 6 files (9,829 words) - ROK frameworks and processes
- `google-ads/performance-max` - 2 files (837 words) - PMax strategies
- `google-ads/search` - 2 files (825 words) - Search campaigns
- `google-ads/shopping` - 2 files (787 words) - Shopping campaigns

### 🔍 **Keyword Search**
Fast text-based search across:
- File titles (weighted heavily)
- Content previews
- Categories and paths

### 🤖 **AI-Powered Search** (Optional)
Uses Claude to:
- Analyze relevant files
- Summarize key findings
- Recommend specific files to read
- Answer complex questions

### 📁 **Category Filtering**
Focus searches on specific topics:
- `--category "google-ads"` - All Google Ads content
- `--category "ai-strategy"` - AI and automation
- `--category "analytics"` - Tracking and measurement

## How It Works

### 1. Indexing

The system creates a searchable index of all knowledge base files:

```bash
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

**What it indexes:**
- Title (extracted from # heading)
- Category (from folder structure)
- Content preview (first 500 characters)
- Metadata (date, word count, file size)
- Full path

**Index Location:** `shared/data/kb-index.json`

### 2. Searching

**Keyword Algorithm:**
1. Splits query into terms
2. Searches across title, content, category
3. Scores each match (title=10, category=5, content=1)
4. Returns top results sorted by relevance

**AI Enhancement:**
1. Takes top keyword results
2. Reads full content or previews
3. Sends to Claude with query
4. Returns synthesized answer

## Command Reference

### Search Commands

```bash
# Basic search
python3 tools/kb-search.py "your query"

# Limit results
python3 tools/kb-search.py --limit 5 "query"

# Filter by category
python3 tools/kb-search.py --category "google-ads" "query"

# AI-powered summary
python3 tools/kb-search.py --ai "query"

# Detailed AI search (reads full files)
python3 tools/kb-search.py --ai --detailed "query"

# Show statistics
python3 tools/kb-search.py --stats
```

### Indexing Commands

```bash
# Rebuild index (run after adding new knowledge)
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

## Usage Examples

### Example 1: Finding PMax Strategies

```bash
python3 tools/kb-search.py "performance max optimization"
```

**Output:**
```
📚 Found 15 relevant file(s)

1. PMax Ad Examples for Every Placement (+Tips to Optimize for Each One)
   📁 google-ads/performance-max
   📄 google-ads/performance-max/pmax-ad-placement-examples-optimization-guide.md
   💭 title: Performance Max Ad Examples and Placement-Specific Optimization Guide

2. Stop Wasting Ad Spend: 8 Step SEO Checklist for Maximizing Google PMax and AI Max ROI
   📁 google-ads/performance-max
   📄 google-ads/performance-max/pmax-ai-max-seo-checklist-roi-optimization.md
   💭 title: SEO Checklist for Maximizing Google Performance Max and AI Max Campaign ROI
...
```

### Example 2: Finding AI Strategy Content

```bash
python3 tools/kb-search.py --category "ai-strategy" "enterprise adoption"
```

**Filters** to only AI strategy files mentioning enterprise adoption.

### Example 3: Getting Statistics

```bash
python3 tools/kb-search.py --stats
```

**Shows:**
- Total files and words
- Last index date
- Category breakdown with counts

### Example 4: AI-Powered Answer (Requires Setup)

```bash
# First install anthropic
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Search with AI
python3 tools/kb-search.py --ai "what are the latest google ads bidding strategies"
```

**Output:**
```
🤖 Analyzing with Claude...

Based on the knowledge base, the latest Google Ads bidding strategies focus on:

1. Smart Bidding automation with tROAS...
2. Performance Max campaigns...
3. Value-based bidding...

Recommended files:
- google-ads/bidding-automation/smart-bidding-guide.md
- google-ads/platform-updates/2025-bidding-updates.md
```

## Integration with Other Tools

### Daily Briefing

The knowledge base search can be integrated into the daily briefing:

```python
# In agents/reporting/daily-briefing.py

from tools.kb_search import keyword_search, load_index

# Add relevant knowledge section
index = load_index()
results = keyword_search("recent updates", index, limit=3)
```

### Inbox Processor

When capturing knowledge items:

```markdown
# In !inbox/pmax-tip.md

knowledge: Performance Max

New insight: PMax works best with 30-day conversion history.
```

→ Gets indexed automatically!

### CLI Alias (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias kb='cd /Users/administrator/Documents/PetesBrain && python3 tools/kb-search.py'
```

Then use:
```bash
kb "shopping feeds"
kb --stats
kb --ai "pmax strategies"
```

## Maintenance

### Rebuilding the Index

**When:**
- After adding new knowledge files
- After the knowledge-base-processor runs
- Weekly (good practice)

**How:**
```bash
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

Takes ~5 seconds for 178 files.

### Auto-Index (Recommended)

Create a LaunchAgent to rebuild index daily:

```xml
<!-- ~/Library/LaunchAgents/com.petesbrain.kb-indexer.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.kb-indexer</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/agents/knowledge-base-indexer/knowledge-base-indexer.py</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-kb-indexer.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-kb-indexer-error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.kb-indexer.plist
```

## Advanced Features

### AI Search Modes

**Standard Mode** (`--ai`):
- Reads content previews (500 chars each)
- Analyzes top 10 results
- Fast (2-3 seconds)
- Good for quick answers

**Detailed Mode** (`--ai --detailed`):
- Reads full content (first 2000 chars)
- Analyzes top 3 results deeply
- Slower (5-10 seconds)
- Better for complex questions

### Custom Scoring

The search algorithm weights matches:
- **Title match:** 10 points
- **Category match:** 5 points  
- **Content match:** 1 point

This prioritizes files with relevant titles over body mentions.

### Multi-Term Queries

Search supports multiple terms:
```bash
kb "google ads shopping feed optimization"
```

Each term scores independently, summed for total score.

## Tips & Best Practices

### 1. Use Specific Terms

✅ **Good:** `"performance max asset groups"`  
❌ **Too Broad:** `"google ads"`

### 2. Filter by Category

When you know the topic area:
```bash
kb --category "analytics" "conversion tracking"
```

### 3. Check Stats First

Unknown what's available? Check stats:
```bash
kb --stats
```

### 4. Use AI for Complex Questions

**Keyword search:** Great for finding files  
**AI search:** Great for synthesizing answers

```bash
# Find files
kb "pmax"

# Get answer
kb --ai "how should I structure my pmax campaigns for best results?"
```

### 5. Rebuild Index Regularly

After knowledge base updates:
```bash
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

## Troubleshooting

### "Index not found" Error

**Cause:** Index hasn't been created yet  
**Fix:** Run indexer
```bash
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

### No Results

**Check:**
1. Is query too specific?
2. Try broader terms
3. Check `--stats` to see what's available
4. Try different category

### AI Search Not Working

**Requirements:**
1. Install: `pip install anthropic`
2. Set API key: `export ANTHROPIC_API_KEY="your-key"`

**Alternative:** Use keyword search (works without AI)

### Slow Performance

**For keyword search:** Should be instant  
**For AI search:** 2-10 seconds is normal

**If slower:**
- Check network connection (AI requires API call)
- Use `--limit 5` to reduce results
- Skip `--detailed` for faster responses

## File Structure

```
PetesBrain/
├── tools/
│   └── kb-search.py                    # Main search tool
├── agents/
│   └── content-sync/
│       └── knowledge-base-indexer.py   # Index builder
├── shared/
│   └── data/
│       └── kb-index.json               # Searchable index
└── roksys/
    └── knowledge-base/                 # 178 knowledge files
        ├── ai-strategy/                # 65 files
        ├── google-ads/                 # 17 files total
        ├── analytics/                  # 18 files
        ├── industry-insights/          # 17 files
        └── rok-methodologies/          # 6 files
```

## Future Enhancements

### Planned Features
- 🔄 Auto-index after knowledge base processor runs
- 📱 Web interface for search
- 🔗 Integration with daily briefing
- 📊 Search analytics (what's searched most)
- 🏷️ Tag-based filtering
- 💾 Search history
- 🔍 Fuzzy matching for typos

### API Integration

The search can be imported as a Python module:

```python
from tools.kb_search import keyword_search, load_index, ai_search

# Load index
index = load_index()

# Search
results = keyword_search("pmax strategies", index, limit=10)

# AI answer (optional)
if ANTHROPIC_AVAILABLE:
    answer = ai_search("how to optimize pmax", results)
```

## Statistics

**Current Knowledge Base:**
- 📚 178 files
- 📝 117,324 words
- 📁 10 categories
- 🔍 Searchable in <1 second

**Most Content:**
1. AI Strategy (65 files, 48K words)
2. Analytics (18 files, 13K words)
3. Industry Insights (17 files, 9K words)

---

**Related Documentation:**
- [Knowledge Base Overview](../roksys/knowledge-base/README.md)
- [Knowledge Base Processor](../roksys/knowledge-base/QUICKSTART.md)
- [Automation Guide](./AUTOMATION.md)

