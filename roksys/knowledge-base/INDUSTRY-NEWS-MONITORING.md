# Industry News Monitoring System

**Automated RSS feed monitoring for Google Ads industry websites**

This system automatically monitors the most respected Google Ads and PPC industry news sources, scores articles for relevance, and imports high-quality content into your knowledge base.

## 🌐 Monitored Sources

The system monitors RSS feeds from these trusted industry sources:

### Essential News & Updates
- **Search Engine Land - Google Ads** - Breaking news and platform updates
- **Search Engine Land - PPC** - PPC strategies and best practices
- **Search Engine Journal - PPC** - Industry analysis and guides

### Thought Leadership & Strategy
- **Google Ads Blog** (Official) - Official Google announcements and features
- **Think with Google** - Consumer trends and strategic insights
- **WordStream Blog** - Data-driven PPC strategies and optimization
- **PPC Hero** - Case studies, experiments, and tactical deep-dives

### Expert Practitioners
- **Neil Patel Blog** - PPC tactics and optimization techniques
- **Unbounce Blog** - Landing page optimization and conversion focus

## 🎯 How It Works

### 1. Automatic Monitoring (Every 6 Hours)

The system runs every 6 hours via macOS LaunchAgent:
- Fetches latest articles from all RSS feeds
- Processes only articles from the last 7 days
- Tracks what's already been processed (no duplicates)

### 2. AI-Powered Relevance Scoring (0-10)

Each article is analyzed by Claude API and scored based on:

**HIGH scores (8-10):**
- Official Google Ads platform updates
- Strategic insights for Google Ads optimization
- Performance Max, Shopping, Search campaign best practices
- Smart Bidding and automation strategies
- Case studies with Google Ads data/results

**MEDIUM scores (5-7):**
- General PPC trends that apply to Google Ads
- Landing page optimization for paid search
- Industry insights relevant to Google Ads strategy
- Analytics and tracking for paid campaigns

**LOW scores (0-4):**
- Generic marketing content (skipped)
- Social media advertising focus (skipped)
- SEO without PPC relevance (skipped)
- Promotional/sales content (skipped)

### 3. Intelligent Filtering

Only articles scoring **6 or higher** are imported to the knowledge base inbox.

### 4. Automatic Processing

Relevant articles are:
1. Added to `roksys/knowledge-base/_inbox/documents/`
2. Automatically processed by `knowledge-base-processor.py` (runs every 6 hours)
3. Categorized and moved to appropriate knowledge base folders
4. Formatted with frontmatter, summaries, and key insights

## 📊 System Status

**Check if running:**
```bash
launchctl list | grep industry-news
```

**View recent logs:**
```bash
tail -50 ~/.petesbrain-industry-news.log
```

**Check inbox:**
```bash
ls -la roksys/knowledge-base/_inbox/documents/
```

## 🔧 Management

### Manual Run (Don't Wait 6 Hours)

```bash
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/industry-news-monitor.py
```

Or with key from environment:
```bash
shared/email-sync/.venv/bin/python3 shared/scripts/industry-news-monitor.py
```

### View State File

The system tracks processed articles in:
```bash
cat shared/data/industry-news-state.json
```

### Reset State (Reprocess All Recent Articles)

```bash
rm shared/data/industry-news-state.json
```

Then run manually to fetch articles from the last 7 days again.

### Stop Monitoring

```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.industry-news.plist
```

### Restart Monitoring

```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.industry-news.plist
```

## 📈 Recent Performance

**Test run (Oct 29, 2025):**
- ✅ **19 articles** checked across 9 sources
- ✅ **12 articles** scored 6+ and imported to inbox
- ✅ **Top scores:**
  - Performance Max ad placements (9/10)
  - CTR optimization strategy (9/10)
  - SEO for PMax campaigns (9/10)
  - Ad fraud from AI browsers (8/10)
  - Q4 ecommerce strategies (7/10)

## 🎓 Integration with Knowledge Base

### Workflow

1. **Monitor** → RSS feeds checked every 6 hours
2. **Score** → Claude API analyzes relevance (0-10)
3. **Filter** → Only scores ≥6 imported
4. **Inbox** → Articles saved to `_inbox/documents/`
5. **Process** → `knowledge-base-processor.py` runs every 6 hours
6. **Organize** → Articles categorized and formatted
7. **Reference** → Claude Code consults KB when providing advice

### When Claude Code Uses This

When you ask about Google Ads strategy, platform updates, or best practices, Claude Code will:
1. Check the knowledge base for relevant recent articles
2. Reference specific documents and insights
3. Combine KB information with client context
4. Provide recommendations grounded in current best practices

**Example queries:**
- "What's the latest on Performance Max optimization?"
- "Are there any recent Google Ads platform updates I should know about?"
- "What are current best practices for Smart Bidding?"
- "Show me recent insights on Q4 ecommerce advertising"

## 🔄 Automation Schedule

- **Industry News Monitor**: Every 6 hours (21600 seconds)
- **Knowledge Base Processor**: Every 6 hours (21600 seconds)
- **Combined**: Fresh industry content processed automatically

## 📝 Logs

**Industry News Monitor:**
- LaunchAgent log: `~/.petesbrain-industry-news.log`
- Application log: `shared/data/industry-news-monitor.log`

**Knowledge Base Processor:**
- LaunchAgent log: `~/.petesbrain-knowledge-base.log`
- Application log: `shared/data/kb-processing.log`

## 🛠️ Configuration

### Adjust Relevance Threshold

Edit `shared/scripts/industry-news-monitor.py`:
```python
# Line 23
MIN_RELEVANCE_SCORE = 6  # Change to 7 or 8 for stricter filtering
```

### Add New RSS Feeds

Edit `shared/scripts/industry-news-monitor.py`:
```python
# Lines 25-35
RSS_FEEDS = {
    "New Source Name": "https://example.com/rss",
    # ... existing feeds
}
```

### Change Monitoring Frequency

Edit `~/Library/LaunchAgents/com.petesbrain.industry-news.plist`:
```xml
<key>StartInterval</key>
<integer>21600</integer>  <!-- 6 hours = 21600 seconds -->
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.industry-news.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.industry-news.plist
```

## 📚 See Also

- `QUICKSTART.md` - Knowledge base inbox system setup
- `EMAIL-INTEGRATION.md` - Email-based content import
- `shared/scripts/knowledge-base-processor.py` - Inbox processor script
- `shared/scripts/industry-news-monitor.py` - RSS monitor script

---

**Status**: ✅ Active and Production-Ready
**Last Updated**: 2025-10-29
**Automation**: LaunchAgent `com.petesbrain.industry-news`
