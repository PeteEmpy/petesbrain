# Client Search - Quick Start

Search all client content (CONTEXT.md, meetings, emails, documents, reports, tasks) instantly.

## Installation

Already installed! Index is built at: `shared/data/client-index.json`

## Basic Usage

```bash
cd /Users/administrator/Documents/PetesBrain

# Basic search
python3 tools/client-search.py "Q4 strategy"

# View statistics
python3 tools/client-search.py --stats
```

## Common Searches

### By Client
```bash
python3 tools/client-search.py --client smythson "conversion tracking"
python3 tools/client-search.py --client devonshire "budget"
```

### By Content Type
```bash
python3 tools/client-search.py --type meeting "strategy"
python3 tools/client-search.py --type email "approval"
python3 tools/client-search.py --type context "account structure"
python3 tools/client-search.py --type document "analysis"
python3 tools/client-search.py --type report "performance"
python3 tools/client-search.py --type tasks-completed "Q4"
python3 tools/client-search.py --type methodology "documentation"
```

### By Date Range
```bash
# Recent content (from Nov 1st)
python3 tools/client-search.py --from 2025-11-01 "meeting"

# Specific month (October)
python3 tools/client-search.py --from 2025-10-01 --to 2025-10-31 "strategy"

# Client + Date
python3 tools/client-search.py --client smythson --from 2025-11-01 "update"
```

### Multiple Filters
```bash
# Smythson meetings about strategy since Oct 20
python3 tools/client-search.py --client smythson --type meeting --from 2025-10-20 "strategy"

# Recent Devonshire documents about budget
python3 tools/client-search.py --client devonshire --type document --from 2025-11-01 "budget"
```

## Content Types Available

- `context` - CONTEXT.md files (client strategic info)
- `meeting` - Meeting notes
- `email` - Email correspondence
- `document` - Documents and analysis
- `brief` - Client briefs
- `report` - Reports (MD and HTML)
- `tasks-completed` - Tasks completed files
- `methodology` - ROK methodologies (Roksys)

## AI Search (Optional)

Requires `anthropic` library and API key:

```bash
# Install
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Use AI search
python3 tools/client-search.py --ai "what conversion tracking issues has Smythson had"

# Detailed AI search (reads full content)
python3 tools/client-search.py --ai --detailed "smythson Q4 strategy decisions"
```

## Rebuilding the Index

Rebuild after adding new client content:

```bash
python3 agents/client-indexer/client-indexer.py
```

Takes ~10-15 seconds. Run this:
- After client meetings (new meeting notes)
- After creating documents/reports
- Weekly (recommended)

## Statistics

See what's indexed:

```bash
python3 tools/client-search.py --stats
```

Shows:
- Total files and words indexed
- Breakdown by client (with file counts)
- Breakdown by content type

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
```

## Tips

1. **Be Specific**: Use specific terms like "Q4 budget revision" vs just "budget"
2. **Use Filters**: Combine --client, --type, --from for precise results
3. **Check Stats First**: Run `--stats` to see what's available
4. **Recent Content**: Use `--from` to focus on recent work
5. **Context Files**: Search `--type context` for account setup info
6. **Methodologies**: Search `--type methodology` for ROK frameworks

## Common Use Cases

### Preparing for a Meeting
```bash
# Review recent discussions
cs --client smythson --type meeting --from 2025-10-01 "strategy"

# Check email correspondence
cs --client smythson --type email --from 2025-10-01 "approval"
```

### Finding Account Information
```bash
# Look at CONTEXT.md
cs --type context --client smythson ""

# Or search for specific info
cs --client smythson "account structure"
```

### Tracking Work History
```bash
# What did we complete for Q4?
cs --type tasks-completed "Q4"

# Recent documents created
cs --type document --from 2025-11-01 ""
```

### Cross-Client Search
```bash
# Find all Q4 strategy content across clients
cs "Q4 strategy"

# Find all conversion tracking discussions
cs --type meeting "conversion tracking"
```

## Full Documentation

See [docs/CLIENT-SEARCH-SYSTEM.md](../docs/CLIENT-SEARCH-SYSTEM.md) for complete guide.

## What's Indexed

**Current Stats:**
- 📊 **953 files** indexed
- 📝 **811,968 words** indexed
- 👥 **17 clients** (16 clients + Roksys)

**Top Clients by Content:**
1. Smythson - 146 files (93,807 words)
2. Devonshire Hotels - 141 files (106,871 words)
3. Clear Prospects - 126 files (140,954 words)
4. Superspace - 111 files (107,640 words)
5. Tree2mydoor - 109 files (140,293 words)

**Content Type Distribution:**
- Emails: 868 files (638,471 words)
- Documents: 34 files (42,331 words)
- Context: 16 files (47,619 words)
- Meetings: 13 files (58,919 words)
- Reports: 13 files (13,620 words)
- Methodologies: 6 files (9,829 words)
- Tasks Completed: 3 files (1,179 words)

---

**Quick Reference Card:**

```
BASIC:     python3 tools/client-search.py "query"
CLIENT:    --client name
TYPE:      --type meeting|email|document|context|report|brief|tasks-completed|methodology
DATE:      --from YYYY-MM-DD [--to YYYY-MM-DD]
AI:        --ai [--detailed]
STATS:     --stats
REBUILD:   python3 agents/client-indexer/client-indexer.py
```

