# Pete's Brain - Quick Reference

**Last Updated:** 2025-11-05

## 🚀 Daily Automation Schedule

```
7:00 AM → Daily Briefing (morning intelligence)
8:00 AM → Inbox Processing (smart routing + Google Tasks)
9:00 AM → Knowledge Base Indexing (search updates)
9:00 AM → Email Sync (1 of 4 daily syncs)
```

---

## 📋 Quick Commands

### **Daily Briefing**
```bash
# View today's briefing
cat briefing/$(date +%Y-%m-%d)-briefing.md

# Run manually
python3 agents/reporting/daily-briefing.py
```

### **Inbox Processing**
```bash
# Create task
echo "task: Review Q4 budgets\nDue: Friday" > !inbox/task.md

# Create client note
echo "client: Smythson\n\nGreat performance this week" > !inbox/note.md

# Process now (don't wait for 8 AM)
python3 agents/system/inbox-processor.py
```

### **Google Tasks**
```bash
# View on web
open https://tasks.google.com

# Migrate existing todos
python3 shared/migrate-todos-to-google-tasks.py
```

### **Knowledge Base Search**
```bash
# Statistics
python3 tools/kb-search.py --stats

# Search
python3 tools/kb-search.py "performance max strategies"

# Filter by category
python3 tools/kb-search.py --category "google-ads" "shopping"

# Re-index manually
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

### **Agent Status**
```bash
# List all PetesBrain agents
launchctl list | grep petesbrain

# View logs
tail -f ~/.petesbrain-daily-briefing.log
tail -f ~/.petesbrain-inbox-processor.log
tail -f ~/.petesbrain-kb-indexer.log
```

---

## 📁 Key Locations

| What | Where |
|------|-------|
| Daily Briefings | `briefing/` |
| Inbox | `!inbox/` |
| Todos | `todo/` |
| Client Folders | `clients/[name]/` |
| Knowledge Base | `roksys/knowledge-base/` |
| Google Tasks | https://tasks.google.com |

---

## 🏷️ Inbox Keywords

| Keyword | Result | Example |
|---------|--------|---------|
| `client: Name` | Routes to client documents | `client: Smythson` |
| `task: Title` | Creates todo + Google Task | `task: Review budgets` |
| `knowledge: Topic` | Adds to knowledge base | `knowledge: PMax tips` |
| `email Name:` | Creates email draft | `email Devonshire:` |

---

## 🔍 Search Categories

- `google-ads` - All Google Ads content
- `google-ads/performance-max` - PMax strategies
- `google-ads/shopping` - Shopping campaigns
- `google-ads/search` - Search campaigns
- `google-ads/platform-updates` - Latest updates
- `ai-strategy` - AI & automation (65 files!)
- `analytics` - GA4, tracking, attribution
- `industry-insights` - Market trends
- `rok-methodologies` - ROK frameworks

---

## 📊 System Stats

- **Total Agents:** 31
- **Knowledge Files:** 178 (117K words)
- **Daily Automations:** 7
- **Email Syncs:** 4x daily
- **Active Clients:** 16

---

## 🆘 Quick Troubleshooting

### Agent Not Running?
```bash
# Reload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.[name].plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.[name].plist
```

### Inbox Not Processing?
```bash
# Check logs
tail -f ~/.petesbrain-inbox-processor-error.log

# Run manually
python3 agents/system/inbox-processor.py
```

### Search Not Working?
```bash
# Re-index knowledge base
python3 agents/knowledge-base-indexer/knowledge-base-indexer.py
```

### Google Tasks Not Creating?
```bash
# Check if using correct Python
which python3

# Should use venv for Google APIs
shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3
```

---

## 📚 Documentation

- [Daily Briefing System](docs/DAILY-BRIEFING-SYSTEM.md)
- [Inbox Processing](docs/INBOX-SYSTEM.md)
- [Google Tasks Integration](docs/GOOGLE-TASKS-INTEGRATION.md)
- [Knowledge Base Search](docs/KNOWLEDGE-BASE-SEARCH.md)
- [Full Session Summary](SESSION-2025-11-05.md)
- [All Agents](agents/README.md)

---

## 💡 Pro Tips

1. **Create inbox alias:**
   ```bash
   alias inbox='cd ~/Documents/PetesBrain/!inbox && vim'
   ```

2. **Create kb-search alias:**
   ```bash
   alias kb='cd ~/Documents/PetesBrain && python3 tools/kb-search.py'
   ```

3. **Morning routine:**
   - Read daily briefing
   - Check Google Tasks
   - Process any urgent inbox items

4. **Weekly routine:**
   - Monday: Read weekly KB summary email
   - Review Google Tasks for week ahead
   - Search KB for relevant knowledge

---

**Questions?** Check [SESSION-2025-11-05.md](SESSION-2025-11-05.md) for complete details.

