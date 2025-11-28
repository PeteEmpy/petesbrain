# Google Trends - Quick Start

**Status:** ✅ Installed and configured
**Next:** Restart Claude Code to activate

---

## After Restart - Test Commands

### 1. Basic Test
```
Check Google Trends for "wedding venues" over the last 12 months
```

### 2. Year-over-Year Comparison
```
Show me year-over-year trends for "wedding venues" comparing 2024 vs 2025
```

### 3. Using the Trends Skill
```
/trends

Then ask: Analyze wedding venues search trends with year-over-year comparison
```

---

## Alternative: Run Analysis Script Directly

If rate limit has cleared (wait 5-10 minutes after restart):

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server
.venv/bin/python wedding_venues_analysis.py
```

This will show:
- Monthly comparison table (2024 vs 2025)
- Percentage changes with arrows (↑/↓)
- Overall statistics
- Key insights and trend direction
- Saved JSON data at `/tmp/wedding_venues_yoy.json`

---

## What's Installed

✅ **MCP Server** - 6 functions for trend analysis
✅ **Trends Skill** - `.claude/skills/trends.md`
✅ **Configuration** - Added to `.mcp.json` (line 65-68)
✅ **Weekly Agent** - `agents/performance-monitoring/trend-monitor.py`
✅ **Documentation** - Complete integration guide

---

## Common Queries

**Seasonal patterns:**
```
Show me 5-year trends for "christmas trees" to identify seasonal patterns
```

**Keyword research:**
```
What are the rising related searches for "sustainable fashion"?
```

**Geographic analysis:**
```
Which UK regions have highest search interest for "luxury hotels"?
```

**Compare categories:**
```
Compare Google Trends for "notebooks" vs "planners" vs "journals"
```

---

## Documentation

- **Quick Guide:** [README.md](README.md)
- **Full Integration:** [INTEGRATION-GUIDE.md](INTEGRATION-GUIDE.md)
- **Trends Skill:** `.claude/skills/trends.md`
- **System Docs:** [docs/GOOGLE-TRENDS-INTEGRATION.md](../../docs/GOOGLE-TRENDS-INTEGRATION.md)

---

## Rate Limiting Note

Google allows ~10 requests per minute. If you get 429 errors:
- Wait 60 seconds
- Use the MCP server (it has built-in retry logic)
- Don't make rapid successive requests

The rate limit from setup will clear within 5-10 minutes after restart.

---

**Ready to use after Claude Code restart!** 🎉
