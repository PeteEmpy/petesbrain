# How to Monitor Agents - Quick Reference

**Your agents are automatically monitored, but here's how to check status:**

## ✅ Automatic Monitoring (Already Set Up)

### 1. Daily Briefing Email (Every Morning at 7 AM)
**This is your primary way to check agent status!**

Every morning you'll receive an email with an **Agent Status** section showing:
- How many agents are healthy
- Any critical agents needing attention
- Non-critical issues

**Action:** Just check your email every morning - agent status is right there.

---

### 2. Health Check (Runs Every 30 Minutes)
**Status:** Currently manual - should be automated

The health check automatically:
- Discovers all 35+ agents
- Checks if they're running
- Verifies logs are fresh
- Can auto-restart unhealthy agents

**To check manually:**
```bash
python3 agents/system/health-check.py --verbose
```

**To auto-restart unhealthy:**
```bash
python3 agents/system/health-check.py --restart-unhealthy
```

---

## 🔍 On-Demand Checks

### Quick Status Dashboard
```bash
python3 agents/system/agent-dashboard.py
```

**Shows:**
- All agents with health status
- Critical vs non-critical issues
- Quick actions (restart, view logs)

### Check Specific Agent
```bash
# Detailed status
python3 agents/system/agent-dashboard.py --status ai-inbox-processor

# View recent logs
python3 agents/system/agent-dashboard.py --logs ai-inbox-processor 50

# Restart agent
python3 agents/system/agent-dashboard.py --restart ai-inbox-processor
```

### View Agent Logs Directly
```bash
# Standard output
tail -f ~/.petesbrain-ai-inbox-processor.log

# Errors
tail -f ~/.petesbrain-ai-inbox-processor-error.log
```

---

## 📋 Recommended Monitoring Routine

### Daily (Automatic)
- ✅ **Check Daily Briefing email** - Agent status is included
- ✅ **Health check runs automatically** (every 30 min)

### Weekly (Manual)
- ✅ **Run dashboard:** `python3 agents/system/agent-dashboard.py`
- ✅ **Review any persistent issues**

### When Issues Detected
1. Check Daily Briefing for details
2. Run dashboard for full status
3. View agent logs to diagnose
4. Restart if needed

---

## 🚨 What Gets Monitored

**All 35+ agents automatically:**
- ✅ Process running (LaunchAgent loaded)
- ✅ Log freshness (updated within expected timeframe)
- ✅ Activity verification (workflow-specific checks)

**Critical agents** (auto-detected):
- High-frequency (< 1 hour intervals)
- Core automation (email-sync, inbox-processor, etc.)
- Monitoring agents

**Non-critical agents:**
- Weekly summaries
- Product tracking
- Client-specific automation

---

## 💡 Key Points

1. **Daily Briefing is your primary check** - Agent status appears every morning
2. **Auto-discovery means no config needed** - New agents are automatically monitored
3. **Dashboard for detailed status** - Run anytime for full overview
4. **Health check can auto-restart** - Use `--restart-unhealthy` flag

---

## 🔧 Setting Up Automated Health Check (Recommended)

To ensure health check runs automatically every 30 minutes, create a LaunchAgent:

```bash
# Create LaunchAgent plist
cat > ~/Library/LaunchAgents/com.petesbrain.health-check.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.health-check</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/agents/system/health-check.py</string>
    </array>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-health-check.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-health-check-error.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.health-check.plist
```

---

## 📊 Current Status

**Right now:**
- ✅ 31/35 agents healthy
- ✅ 0 critical issues
- ⚠️ 4 non-critical issues (stale logs for scheduled agents)

**Monitoring:**
- ✅ Daily Briefing includes agent status
- ✅ Dashboard available for detailed checks
- ⚠️ Health check LaunchAgent not yet created (should be automated)

---

**Bottom Line:** Check your Daily Briefing email every morning - that's the easiest way to see agent status. Use the dashboard when you need detailed information or want to restart agents.

