# Agent Monitoring System - Quick Reference

**Created:** 2025-11-08  
**Status:** ✅ Active

## Overview

Comprehensive auto-discovery system that monitors **all** PetesBrain LaunchAgents without manual configuration.

## Quick Commands

### View All Agents Status
```bash
python3 agents/system/agent-dashboard.py
```

### Check Health of All Agents
```bash
python3 agents/system/health-check.py --verbose
```

### Restart Unhealthy Agents
```bash
python3 agents/system/health-check.py --restart-unhealthy
```

### View Specific Agent
```bash
python3 agents/system/agent-dashboard.py --status ai-inbox-processor
```

### View Agent Logs
```bash
python3 agents/system/agent-dashboard.py --logs ai-inbox-processor
```

## What Gets Monitored

**Automatically discovers and monitors:**
- ✅ All `com.petesbrain.*` LaunchAgents
- ✅ Process status (loaded/not loaded)
- ✅ Log freshness (based on schedule)
- ✅ Activity verification (workflow-specific checks)
- ✅ Critical vs non-critical classification

**Current Status:** 35 agents discovered and monitored

## Where You'll See Status

1. **Daily Briefing** (7 AM daily)
   - Agent status section
   - Shows healthy/unhealthy counts
   - Highlights critical issues

2. **Agent Dashboard** (manual)
   - Full status overview
   - Quick actions (restart, view logs)
   - Detailed agent information

3. **Health Check Logs**
   - `~/.petesbrain-health-check.log`
   - Records all health checks and issues

## Files Created

- `shared/scripts/launchagent_discovery.py` - Auto-discovery system
- `agents/system/health-check.py` - Enhanced health check (auto-discovery)
- `agents/system/agent-dashboard.py` - Interactive dashboard
- `docs/SYSTEM-HEALTH-MONITORING.md` - Full documentation

## Benefits

✅ **No Manual Configuration** - Discovers agents automatically  
✅ **Comprehensive** - Monitors all 35+ agents  
✅ **Intelligent** - Understands schedules and criticality  
✅ **Visible** - Status in Daily Briefing every morning  
✅ **Actionable** - Dashboard for quick status checks  

