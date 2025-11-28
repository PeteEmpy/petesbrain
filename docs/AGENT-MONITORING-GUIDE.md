# Agent Monitoring Guide

**How to ensure agents are running correctly and catch issues early**

## 1. Daily Briefing (Automatic - Every Morning)

**When:** Every day at 7 AM  
**Where:** Email + `clients/_system/daily-briefings/YYYY-MM-DD.md`

The Daily Briefing automatically includes an **Agent Status** section showing:
- Total agents healthy/unhealthy
- Critical agents needing attention
- Non-critical issues

**Example:**
```markdown
## 🤖 Agent Status

**31/35 agents healthy**

⚠️ **2 critical agent(s) need attention:**

- 🔴 **email-sync**: Email sync workflow (every 6 hours)
- 🔴 **ai-inbox-processor**: AI inbox processor (every 10 min)

⚪ **4 non-critical agent(s) with issues:**

- ⚪ **label-snapshots**: Product label snapshots (daily)
```

**Action:** Check your Daily Briefing email every morning to see agent status.

---

## 2. Agent Dashboard (On-Demand)

**Command:**
```bash
python3 agents/system/agent-dashboard.py
```

**Shows:**
- All agents with health status
- Critical vs non-critical issues
- Recent log activity
- Quick actions (restart, view logs)

**Usage:**
```bash
# Full dashboard
python3 agents/system/agent-dashboard.py

# Check specific agent
python3 agents/system/agent-dashboard.py --status ai-inbox-processor

# View agent logs
python3 agents/system/agent-dashboard.py --logs ai-inbox-processor 50

# Restart unhealthy agent
python3 agents/system/agent-dashboard.py --restart ai-inbox-processor
```

---

## 3. Health Check (Automated + Manual)

**Automated:** Runs every 30 minutes via LaunchAgent  
**Manual:**
```bash
# Quick check
python3 agents/system/health-check.py

# Verbose (shows all agents)
python3 agents/system/health-check.py --verbose

# Auto-restart unhealthy agents
python3 agents/system/health-check.py --restart-unhealthy
```

**Logs:** `~/.petesbrain-health-check.log`

**What it checks:**
- ✅ Process running (LaunchAgent loaded)
- ✅ Log freshness (updated within expected timeframe)
- ✅ Activity verification (workflow-specific checks)

---

## 4. Check LaunchAgent Status

**View all agents:**
```bash
launchctl list | grep petesbrain
```

**Check specific agent:**
```bash
launchctl list com.petesbrain.ai-inbox-processor
```

**View agent logs:**
```bash
# Standard output
tail -f ~/.petesbrain-ai-inbox-processor.log

# Errors
tail -f ~/.petesbrain-ai-inbox-processor-error.log
```

---

## 5. Quick Status Check Script

Create a simple script to check status anytime:

```bash
#!/bin/bash
# Quick agent status check
cd /Users/administrator/Documents/PetesBrain
python3 agents/system/agent-dashboard.py | grep -A 5 "SUMMARY"
```

---

## 6. Monitoring Schedule

**Current Monitoring:**
- ✅ **Health Check**: Every 30 minutes (automatic)
- ✅ **Daily Briefing**: Every morning at 7 AM (includes agent status)
- ✅ **Auto-discovery**: All agents automatically monitored

**Recommended Checks:**
1. **Daily**: Check Daily Briefing email (7 AM)
2. **Weekly**: Run dashboard: `python3 agents/system/agent-dashboard.py`
3. **When issues**: Use dashboard to investigate and restart

---

## 7. What Gets Monitored Automatically

**All 35+ agents are automatically discovered and monitored:**
- Process status (loaded/not loaded)
- Log freshness (based on schedule)
- Activity verification (workflow-specific)

**Critical agents** (auto-detected):
- High-frequency agents (< 1 hour intervals)
- Core automation (email-sync, inbox-processor, etc.)
- Monitoring agents (anomaly-detector, health-check)

**Non-critical agents:**
- Weekly summaries
- Product tracking
- Client-specific automation

---

## 8. Troubleshooting Workflow

**If agent shows unhealthy:**

1. **Check logs:**
   ```bash
   tail -50 ~/.petesbrain-AGENT-NAME.log
   tail -50 ~/.petesbrain-AGENT-NAME-error.log
   ```

2. **Check LaunchAgent:**
   ```bash
   launchctl list com.petesbrain.AGENT-NAME
   ```

3. **Restart agent:**
   ```bash
   python3 agents/system/agent-dashboard.py --restart AGENT-NAME
   # OR
   launchctl stop com.petesbrain.AGENT-NAME
   launchctl start com.petesbrain.AGENT-NAME
   ```

4. **Run manually to test:**
   ```bash
   # Check script path in dashboard
   python3 agents/system/agent-dashboard.py --status AGENT-NAME
   # Then run script directly
   python3 PATH/TO/SCRIPT.py
   ```

---

## 9. Setting Up Alerts (Optional)

**Email alerts on critical failures:**

The health check can be enhanced to send email alerts when critical agents fail. Currently, issues are:
- Logged to `~/.petesbrain-health-check.log`
- Reported in Daily Briefing
- Visible in dashboard

**To add email alerts**, modify `agents/system/health-check.py` to send emails on critical failures.

---

## 10. Verification Checklist

**Daily:**
- [ ] Check Daily Briefing email (7 AM)
- [ ] Review agent status section

**Weekly:**
- [ ] Run dashboard: `python3 agents/system/agent-dashboard.py`
- [ ] Check for any persistent issues

**When adding new agent:**
- [ ] Verify it appears in dashboard (auto-discovered)
- [ ] Check health check picks it up
- [ ] Verify logs are being written
- [ ] Test manual run works

---

## Quick Reference

**Check status:**
```bash
python3 agents/system/agent-dashboard.py
```

**Health check:**
```bash
python3 agents/system/health-check.py --verbose
```

**View logs:**
```bash
tail -f ~/.petesbrain-AGENT-NAME.log
```

**Restart agent:**
```bash
python3 agents/system/agent-dashboard.py --restart AGENT-NAME
```

---

**Key Point:** With auto-discovery, you don't need to manually configure monitoring. Just check your Daily Briefing every morning, and run the dashboard when you want detailed status.

