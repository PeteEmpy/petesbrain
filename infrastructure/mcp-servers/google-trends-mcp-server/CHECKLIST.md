# Google Trends Integration Checklist

Complete this checklist to activate Google Trends integration in PetesBrain.

## Installation Status

### ✅ Completed (Automated)

- [x] MCP server created with 6 core functions
- [x] Virtual environment created
- [x] Dependencies installed (pytrends, mcp, pandas)
- [x] Server added to `.mcp.json`
- [x] Automated agent script created
- [x] LaunchAgent plist file created
- [x] Documentation written (README, Integration Guide)
- [x] Test suite created
- [x] Setup script created

### ⏳ Manual Steps Required

- [ ] **Restart Claude Code** (REQUIRED to load MCP server)
- [ ] Test integration with: "Check Google Trends for christmas trees"
- [ ] Install LaunchAgent (optional, for automated monitoring):
  ```bash
  cp agents/launchagents/com.petesbrain.trend-monitor.plist ~/Library/LaunchAgents/
  launchctl load ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist
  ```
- [ ] Verify agent status:
  ```bash
  launchctl list | grep trend-monitor
  ```

## Post-Installation Verification

### 1. Test MCP Server

After restarting Claude Code, try these commands:

```plaintext
✓ Can you check Google Trends for "christmas trees" over the last 3 months?
✓ What are the rising related searches for "coffee subscription"?
✓ Compare trends for "notebooks" vs "planners" over the last year
✓ Which UK regions have highest interest for "luxury hotels"?
```

Expected: Structured JSON responses with trend data

### 2. Test Automated Agent (Optional)

```bash
# Run agent manually
cd /Users/administrator/Documents/PetesBrain
python3 agents/performance-monitoring/trend-monitor.py

# Check it created history files
ls shared/data/trend-history/

# View logs
cat ~/.petesbrain-trend-monitor.log
```

Expected: Log output showing trends fetched for each client

### 3. Verify Configuration

```bash
# Check .mcp.json
cat .mcp.json | grep -A 3 google-trends

# Check server exists
ls shared/mcp-servers/google-trends-mcp-server/server.py

# Check venv
ls shared/mcp-servers/google-trends-mcp-server/.venv/bin/python
```

## Quick Reference

### File Locations

- **MCP Server:** `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/`
- **Agent Script:** `/Users/administrator/Documents/PetesBrain/agents/performance-monitoring/trend-monitor.py`
- **LaunchAgent:** `~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist`
- **Documentation:** `shared/mcp-servers/google-trends-mcp-server/INTEGRATION-GUIDE.md`
- **Trend History:** `shared/data/trend-history/` (created on first run)

### Common Commands

```bash
# Run test suite (wait for rate limits)
cd shared/mcp-servers/google-trends-mcp-server
.venv/bin/python test_trends.py

# Run agent manually
python3 agents/performance-monitoring/trend-monitor.py

# Check agent status
launchctl list | grep trend-monitor

# View agent logs
cat ~/.petesbrain-trend-monitor.log

# Reload agent after changes
launchctl unload ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist
```

## Troubleshooting

### Issue: MCP functions not available in Claude Code

**Solution:**
1. Verify `.mcp.json` has `google-trends` entry
2. Restart Claude Code completely
3. Try a simple query: "Check Google Trends for coffee"

### Issue: 429 Rate Limit Errors

**Solution:**
- Wait 60 seconds between requests
- Use automated agent (runs weekly) instead of frequent manual queries
- Add 10-second delays between multiple queries

### Issue: No data returned / empty results

**Solution:**
- Try broader timeframe (`today 12-m` instead of `today 3-m`)
- Use generic product categories, not brand names
- Check keyword spelling
- Some niche terms lack sufficient data

### Issue: Agent not running

**Solution:**
```bash
# Check if loaded
launchctl list | grep trend-monitor

# If not loaded
launchctl load ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist

# If errors, check logs
cat ~/.petesbrain-trend-monitor-error.log
```

## Integration with Workflows

### When Analyzing Client Performance

**Old Workflow:**
1. Read CONTEXT.md
2. Check tasks-completed.md
3. Review experiment log
4. Check Google Ads changes
5. Consult Knowledge Base

**New Workflow:**
1. Read CONTEXT.md
2. Check tasks-completed.md
3. Review experiment log
4. **Check Google Trends** ← NEW
5. Check Google Ads changes
6. Consult Knowledge Base

### Example Query

```plaintext
I'm analyzing Tree2mydoor's Q4 performance. Can you:
1. Check Google Trends for "christmas trees" over the last 5 years to identify seasonal patterns
2. Compare current search interest vs last year
3. Get related rising searches for potential campaign expansion
```

## Next Steps

Once integration is verified:

1. **Add trend checks to client analysis routine**
   - Always check trends when investigating performance changes
   - Document trend patterns in CONTEXT.md

2. **Use for strategic planning**
   - Seasonal budget allocation
   - Product category prioritization
   - Geographic targeting decisions

3. **Incorporate into monthly reports**
   - Add "Market Trends" section
   - Provide context for performance changes
   - Identify opportunities based on rising searches

4. **Monitor automated agent**
   - Check logs weekly: `cat ~/.petesbrain-trend-monitor.log`
   - Review trend history: `ls shared/data/trend-history/`
   - Update client CONTEXT.md with insights

## Success Criteria

Integration is successful when:

- [ ] Can query Google Trends data directly in Claude Code
- [ ] Responses include structured trend data (0-100 scale)
- [ ] Can analyze seasonal patterns over 5 years
- [ ] Can discover related rising/top searches
- [ ] Can compare multiple keywords side-by-side
- [ ] Can identify geographic opportunities
- [ ] Automated agent runs weekly (optional)
- [ ] Trend insights inform client strategy

## Documentation

- **Quick Start:** See README.md in server directory
- **Full Guide:** See INTEGRATION-GUIDE.md for complete usage examples
- **System Docs:** See docs/GOOGLE-TRENDS-INTEGRATION.md for architecture
- **Agent Docs:** See agents/README.md for monitoring setup

---

**Status:** ✅ Installation Complete
**Next Action:** Restart Claude Code and test with sample query
**Support:** See INTEGRATION-GUIDE.md for troubleshooting
