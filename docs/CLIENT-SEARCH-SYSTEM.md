# Client Content Search System

**Status:** ✅ Active  
**Last Updated:** 2025-11-05

## Overview

The Client Content Search System makes all your **client content** instantly searchable. Find relevant information about client strategies, meetings, emails, documents, tasks completed, and Roksys methodologies in seconds.

This system follows the same pattern as the [Knowledge Base Search](./KNOWLEDGE-BASE-SEARCH.md) but for client-specific content.

## Quick Start

### Basic Search
```bash
cd /Users/administrator/Documents/PetesBrain
python3 tools/client-search.py "Q4 strategy"
```

### Search Specific Client
```bash
python3 tools/client-search.py --client smythson "performance max"
```

### Filter by Content Type
```bash
python3 tools/client-search.py --type meeting "budget discussion"
```

### View Statistics
```bash
python3 tools/client-search.py --stats
```

### AI-Powered Search
```bash
# Install first: pip install anthropic
python3 tools/client-search.py --ai "what did we decide about Q4 budgets"
```

## What Gets Indexed

### Client Folders

For each client in `clients/`, the system indexes:

- **CONTEXT.md** - Primary client knowledge and strategic context
- **tasks-completed.md** - Work history and completed tasks
- **meeting-notes/*.md** - All meeting notes
- **emails/*.md** - All email correspondence
- **documents/*.md** - All documents and analysis
- **briefs/*.md** - All client briefs
- **reports/*.md** - Report files (markdown)
- **reports/*.html** - Report files (HTML)

### Roksys Content

From the `roksys/` folder:

- **meeting-notes/*.md** - Internal Roksys meetings
- **documents/*.md** - Internal Roksys documents
- **knowledge-base/rok-methodologies/*.md** - ROK frameworks and processes

### Index Location

**File:** `shared/data/client-index.json`

This JSON file contains:
- All indexed files with metadata
- Client statistics
- Content type breakdown
- Search-optimized previews

## Features

### 🔍 **Advanced Keyword Search**

Fast text-based search with intelligent scoring:
- **Title match**: 10 points
- **Client name match**: 5 points
- **Content type match**: 3 points
- **Path match**: 2 points
- **Content match**: 1 point

Results sorted by relevance score and date.

### 👥 **Client Filtering**

Focus searches on specific clients:
```bash
client-search --client smythson "conversion tracking"
client-search --client devonshire "budget"
```

### 📁 **Content Type Filtering**

Search specific types of content:
- `--type context` - CONTEXT.md files
- `--type meeting` - Meeting notes
- `--type email` - Email correspondence
- `--type document` - Documents and analysis
- `--type brief` - Client briefs
- `--type report` - Reports
- `--type tasks-completed` - Tasks completed files
- `--type methodology` - ROK methodologies (Roksys)

### 📅 **Date Range Filtering**

Filter by date ranges:
```bash
# Content from November onwards
client-search --from 2025-11-01 "weekly meeting"

# Content from October
client-search --from 2025-10-01 --to 2025-10-31 "strategy"

# Recent content
client-search --from 2025-11-01 --client smythson "update"
```

### 🤖 **AI-Powered Analysis** (Optional)

Uses Claude to:
- Analyze relevant files
- Synthesize answers across multiple sources
- Provide actionable recommendations
- Recommend specific files to read

**Standard Mode** (`--ai`):
- Reads content previews
- Analyzes top 10 results
- Fast (2-3 seconds)

**Detailed Mode** (`--ai --detailed`):
- Reads full content (first 3000 chars)
- Analyzes top 3 results deeply
- Slower (5-10 seconds)
- Better for complex questions

## Command Reference

### Search Commands

```bash
# Basic search
python3 tools/client-search.py "your query"

# Filter by client
python3 tools/client-search.py --client "client-name" "query"

# Filter by content type
python3 tools/client-search.py --type meeting "query"

# Date range filtering
python3 tools/client-search.py --from 2025-11-01 "query"
python3 tools/client-search.py --from 2025-10-01 --to 2025-10-31 "query"

# Multiple filters combined
python3 tools/client-search.py --client smythson --type meeting --from 2025-11-01 "strategy"

# Limit results
python3 tools/client-search.py --limit 5 "query"

# AI-powered summary
python3 tools/client-search.py --ai "query"

# Detailed AI search (reads full files)
python3 tools/client-search.py --ai --detailed "query"

# Show statistics
python3 tools/client-search.py --stats
```

### Indexing Commands

```bash
# Build/rebuild index (run after adding new content)
python3 agents/client-indexer/client-indexer.py
```

## Usage Examples

### Example 1: Finding Q4 Strategy Information

```bash
python3 tools/client-search.py "Q4 strategy"
```

**Output:**
```
📚 Found 12 relevant file(s)

1. Q4 Strategy Quick Start
   👤 Smythson
   📁 document
   📅 2025-11-04
   📄 clients/smythson/Q4-STRATEGY-QUICK-START.md
   💭 Quick reference guide for Q4 2025 strategy implementation...

2. Q4 2025 Strategy Tracker
   👤 Smythson
   📁 document
   📅 2025-11-05
   📄 clients/smythson/documents/q4-2025-strategy-tracker.md
   💭 Tracking document for Q4 strategy implementation...
...
```

### Example 2: Finding Smythson Meetings

```bash
python3 tools/client-search.py --client smythson --type meeting "catch up"
```

**Filters** to only Smythson meeting notes containing "catch up".

### Example 3: Recent Content

```bash
python3 tools/client-search.py --from 2025-11-01 "budget"
```

**Finds** all budget-related content from November 2025 onwards.

### Example 4: Multi-Client Search

```bash
python3 tools/client-search.py --type context "Google Ads account structure"
```

**Searches** CONTEXT.md files across all clients for account structure information.

### Example 5: AI-Powered Analysis

```bash
# First install anthropic
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Search with AI
python3 tools/client-search.py --ai "what conversion tracking issues has Smythson had"
```

**Output:**
```
🤖 Analyzing with Claude...

Based on the client content, Smythson has had several conversion tracking issues:

1. Conversion Action Setup: Multiple meetings focused on setting up proper conversion 
   tracking across UK, USA, EUR, and ROW accounts.

2. Google Tag Implementation: Scheduled support meetings with Google in November 2025 
   to resolve tag implementation issues.

3. Cross-Account Tracking: Challenges with tracking conversions consistently across 
   four separate Google Ads accounts.

Recommended files:
- clients/smythson/meeting-notes/2025-10-24-paid-search-catch-up-smythson.md
- clients/smythson/documents/conversion-tracking-setup-request.md
- roksys/knowledge-base/analytics/smythson-conversion-tracking-setup-ga4-google-ads.md

Next steps: Review the scheduled Google support meeting outcomes and verify conversion 
tracking implementation across all accounts.
```

### Example 6: Finding Methodologies

```bash
python3 tools/client-search.py --type methodology "documentation"
```

**Finds** ROK methodology documents about documentation practices.

### Example 7: Statistics

```bash
python3 tools/client-search.py --stats
```

**Shows:**
```
============================================================
  Client Content Statistics
============================================================

📊 Total files: 247
📝 Total words: 185,432
📅 Last indexed: 2025-11-05 10:30:15

👥 Clients:

  Smythson                       89 files  (52,341 words)
  Devonshire Hotels              45 files  (31,287 words)
  National Design Academy        38 files  (28,156 words)
  Roksys                         21 files  (18,943 words)
  Superspace                     18 files  (15,632 words)
  Tree2mydoor                    12 files  (10,234 words)
  ...

📂 Content Types:

  meeting                        67 files  (45,123 words)
  document                       58 files  (38,945 words)
  email                          42 files  (27,834 words)
  context                        15 files  (31,245 words)
  report                         23 files  (21,543 words)
  tasks-completed               12 files  (15,432 words)
  brief                          18 files  (12,876 words)
  methodology                     6 files  (9,829 words)
  ...
```

## How It Works

### 1. Indexing Process

The indexer (`agents/client-indexer/client-indexer.py`) scans all client folders and creates a searchable index:

**For Each File:**
1. Extracts title (from # heading, Subject: line, or filename)
2. Determines client name (from folder structure)
3. Identifies content type (from folder and filename)
4. Extracts date (from filename or content)
5. Counts words and captures preview
6. Stores metadata and preview in index

**Output:** `shared/data/client-index.json`

### 2. Search Process

**Keyword Search:**
1. Splits query into terms
2. Applies filters (client, type, date range)
3. Searches across title, content, client, type, path
4. Scores each match with weighted points
5. Sorts by score and date
6. Returns top results

**AI Enhancement:**
1. Takes top keyword results
2. Reads full content or previews
3. Sends to Claude with query
4. Returns synthesized answer with recommendations

## Integration Examples

### Daily Briefing Integration

Add client content search to daily briefings:

```python
# In agents/reporting/daily-briefing.py

from tools.client_search import keyword_search, load_index

# Add recent client activity section
index = load_index()
results = keyword_search("meeting", index, date_from="2025-11-01", limit=5)
```

### Task Tracking

Find completed tasks:

```bash
client-search --type tasks-completed --client smythson "Q4"
```

### Meeting Prep

Prepare for meetings by reviewing past discussions:

```bash
client-search --client smythson --type meeting --from 2025-10-01 "strategy"
```

### Python Module Usage

Import and use programmatically:

```python
from tools.client_search import keyword_search, load_index, ai_search

# Load index
index = load_index()

# Search
results = keyword_search(
    "Q4 budget", 
    index, 
    client="smythson",
    content_type="meeting",
    limit=10
)

# AI answer (optional)
if ANTHROPIC_AVAILABLE:
    answer = ai_search("What did we discuss about Q4?", results)
```

## CLI Alias (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias cs='cd /Users/administrator/Documents/PetesBrain && python3 tools/client-search.py'
```

Then use:
```bash
cs "Q4 strategy"
cs --client smythson "pmax"
cs --stats
cs --ai "conversion tracking issues"
```

## Maintenance

### Rebuilding the Index

**When to Rebuild:**
- After adding new client content
- After client meetings (new meeting notes)
- After creating documents or reports
- Weekly (recommended)

**How:**
```bash
python3 agents/client-indexer/client-indexer.py
```

Takes ~10-15 seconds depending on content volume.

### Auto-Index (Recommended)

Create a LaunchAgent to rebuild index daily:

```xml
<!-- ~/Library/LaunchAgents/com.petesbrain.client-indexer.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.client-indexer</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/agents/client-indexer/client-indexer.py</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-client-indexer.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-client-indexer-error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.client-indexer.plist
```

### Adding New Content Types

To index additional file types, edit `client-indexer.py`:

```python
# In index_client_folder function, add to patterns list:
patterns = [
    "CONTEXT.md",
    "tasks-completed.md",
    "meeting-notes/*.md",
    "emails/*.md",
    "documents/*.md",
    "briefs/*.md",
    "reports/*.md",
    "reports/*/*.md",
    "reports/*.html",
    "reports/*/*.html",
    "your-new-pattern/*.md",  # Add here
]
```

Then rebuild the index.

## Tips & Best Practices

### 1. Use Specific Search Terms

✅ **Good:** `"Q4 budget revision"`  
❌ **Too Broad:** `"budget"`

✅ **Good:** `"conversion tracking setup"`  
❌ **Too Broad:** `"tracking"`

### 2. Combine Filters for Precision

```bash
# Instead of:
client-search "meeting"

# Do:
client-search --client smythson --type meeting --from 2025-10-01 "strategy"
```

### 3. Use Content Types Strategically

- **Context** - Strategic information, account setup
- **Meeting** - Discussions, decisions, action items
- **Email** - Correspondence, approvals, requests
- **Document** - Analysis, reports, tracking
- **Tasks-completed** - Work history, deliverables

### 4. Check Stats to Know What's Available

Before searching unfamiliar territory:
```bash
client-search --stats
```

### 5. Use AI for Synthesis

**Keyword search:** Great for finding specific files  
**AI search:** Great for understanding context across multiple sources

### 6. Date Filters for Recent Work

```bash
# Last month
client-search --from 2025-10-01 "query"

# Last week (adjust date)
client-search --from 2025-10-29 "query"

# Specific period
client-search --from 2025-10-01 --to 2025-10-31 "query"
```

### 7. Rebuild Index Regularly

After significant content additions:
```bash
python3 agents/client-indexer/client-indexer.py
```

## Troubleshooting

### "Index not found" Error

**Cause:** Index hasn't been created yet  
**Fix:** Run indexer
```bash
python3 agents/client-indexer/client-indexer.py
```

### No Results Found

**Check:**
1. Is query too specific?
2. Try removing filters
3. Check `--stats` to see what's indexed
4. Try broader search terms
5. Rebuild index (might be outdated)

### Wrong Results

**Possible Issues:**
1. Index is outdated - rebuild it
2. Search terms are too broad
3. Need more filters (--client, --type, --from)

### AI Search Not Working

**Requirements:**
1. Install: `pip install anthropic`
2. Set API key: `export ANTHROPIC_API_KEY="your-key"`

**Alternative:** Use keyword search (works without AI)

### Slow Performance

**For keyword search:** Should be instant (<1 second)  
**For AI search:** 2-10 seconds is normal

**If slower:**
- Check network connection (AI requires API call)
- Use `--limit 5` to reduce results
- Skip `--detailed` for faster AI responses

### HTML Reports Not Readable

HTML reports are automatically stripped of tags for preview. For full formatting, open the file directly:

```bash
# Find the report
client-search --type report "report name"

# Open it
open clients/client-name/reports/report.html
```

## File Structure

```
PetesBrain/
├── tools/
│   └── client-search.py              # Main search tool
├── agents/
│   └── content-sync/
│       └── client-indexer.py         # Index builder
├── shared/
│   └── data/
│       └── client-index.json         # Searchable index
├── clients/
│   ├── smythson/
│   │   ├── CONTEXT.md               # Indexed
│   │   ├── tasks-completed.md       # Indexed
│   │   ├── meeting-notes/*.md       # Indexed
│   │   ├── emails/*.md              # Indexed
│   │   ├── documents/*.md           # Indexed
│   │   ├── briefs/*.md              # Indexed
│   │   └── reports/*.{md,html}      # Indexed
│   ├── devonshire-hotels/
│   │   └── [same structure]
│   └── [other clients]/
│       └── [same structure]
└── roksys/
    ├── meeting-notes/*.md            # Indexed
    ├── documents/*.md                # Indexed
    └── knowledge-base/
        └── rok-methodologies/*.md    # Indexed
```

## Comparison: Client Search vs KB Search

| Feature | Client Search | KB Search |
|---------|--------------|-----------|
| **Content Source** | Client folders + Roksys | Knowledge base |
| **Primary Use** | Client-specific work | General knowledge |
| **Content Types** | Meetings, emails, docs, context | Articles, research, methodologies |
| **Filtering** | Client, type, date range | Category |
| **Best For** | "What did we do?" | "How do we do it?" |
| **Index File** | `client-index.json` | `kb-index.json` |
| **Indexer** | `client-indexer.py` | `knowledge-base-indexer.py` |
| **Tool** | `client-search.py` | `kb-search.py` |

**Use Both:**
- **Client Search** - Find what happened with Smythson
- **KB Search** - Find how to optimize Performance Max

## Future Enhancements

### Planned Features
- 🔄 Auto-index after inbox processing
- 📊 Search analytics (most searched clients/topics)
- 🔗 Integration with task management
- 📧 Email thread reconstruction
- 📈 Client activity timeline view
- 🏷️ Tag-based organization
- 💾 Search history
- 🔍 Fuzzy matching for typos
- 📱 Web interface

### Advanced Features to Consider
- Cross-reference with knowledge base
- Automatic meeting summaries
- Client work pattern analysis
- Recommendation engine for similar past work
- Export search results to reports

## Related Documentation

- [Knowledge Base Search System](./KNOWLEDGE-BASE-SEARCH.md) - Similar system for knowledge base
- [Inbox Processing System](./INBOX-PROCESSING-SYSTEM.md) - How content gets created
- [Automation Guide](./AUTOMATION.md) - Automated systems overview
- [Google Tasks Integration](./GOOGLE-TASKS-INTEGRATION.md) - Task management

## Summary

The Client Content Search System provides:

✅ **Fast search** across all client content  
✅ **Advanced filtering** by client, type, date  
✅ **AI-powered analysis** for complex queries  
✅ **Unified access** to meetings, emails, documents  
✅ **ROK methodologies** included in search  
✅ **Simple CLI** with kb-search UX pattern  

**Get Started:**
```bash
# Index content
python3 agents/client-indexer/client-indexer.py

# Search
python3 tools/client-search.py "your query"

# Stats
python3 tools/client-search.py --stats
```

---

**System Status:** Ready to use  
**Index Location:** `shared/data/client-index.json`  
**Last Updated:** 2025-11-05

