# Google Ads Audit System

**Status:** ✅ Active  
**Schedule:** Weekly (Monday 10:00 AM)  
**Agent:** `agents/reporting/google-ads-auditor.py`

---

## Overview

Automated Google Ads audit system using ROK's systematic analysis framework. Generates ready-to-execute audit templates for all active clients on a weekly basis.

### What It Does

1. **Generates Audit Templates** - Creates structured, ready-to-run prompts for Google Ads analysis
2. **Multiple Audit Types** - Weekly performance, impression share, keyword optimization, account structure
3. **Client-Specific** - Each client gets their own `audits/` folder with timestamped reports
4. **MCP-Ready** - Templates designed for Claude Code + Google Ads MCP integration
5. **ROK Framework** - Based on proven analysis methodologies from ROK's prompt library

---

## Audit Types

### 1. Weekly Audit (Comprehensive)

**Purpose:** Ongoing performance monitoring  
**Frequency:** Weekly  
**Best For:** Established accounts

**Covers:**
- Campaign overview (impressions, clicks, spend, ROAS)
- Product-level performance (top 10 best/worst)
- Placement analysis (Shopping, YouTube, Display, Discover)
- Audience & asset insights
- Budget efficiency
- Root cause diagnostics
- 3-5 prioritized recommendations

### 2. Impression Share Audit

**Purpose:** Identify impression share loss opportunities  
**Frequency:** Monthly or when IS drops  
**Best For:** Growth phase accounts

**Covers:**
- Impression share metrics by campaign/ad group/product group
- Lost IS due to budget vs rank
- Week-over-week competitive pressure detection
- Growth opportunity quantification
- Budget/bid recovery recommendations

### 3. Keyword Audit

**Purpose:** Search campaign cleanup and optimization  
**Frequency:** Bi-weekly  
**Best For:** Active optimization phase

**Covers:**
- Underperforming keywords (wasted spend)
- High-potential keywords (growth opportunities)
- Declining keywords (CTR/CVR drops >15%)
- Zero-conversion queries (negative keyword candidates)
- Specific bid/optimization recommendations

### 4. Structure Audit

**Purpose:** Evaluate and improve campaign architecture  
**Frequency:** Quarterly or at onboarding  
**Best For:** New accounts or restructures

**Covers:**
- Overly broad product groups
- Segmentation granularity and logic
- Bid control opportunities
- Reporting clarity issues
- Restructuring recommendations

---

## Quick Start

### Command-Line Tool

```bash
# Weekly audit for specific client
./audit --client smythson

# Full audit suite for one client
./audit --client smythson --type full

# Weekly audits for all clients
./audit --all

# Specific audit type
./audit --client smythson --type keyword
./audit --client smythson --type impression_share
./audit --client smythson --type structure
```

### Direct Python Execution

```bash
# Weekly audit
python3 agents/reporting/google-ads-auditor.py --client smythson --type weekly

# Full suite
python3 agents/reporting/google-ads-auditor.py --client smythson --type full

# All clients
python3 agents/reporting/google-ads-auditor.py --all
```

---

## How It Works

### Step 1: Template Generation (Automated)

Every Monday at 10:00 AM, the system:
1. Loops through all active clients
2. Creates `clients/[client]/audits/` folder
3. Generates 4 audit templates per client:
   - Weekly audit
   - Impression share audit
   - Keyword audit
   - Structure audit
4. Creates an audit index file with links and instructions

### Step 2: Audit Execution (Manual with Claude)

For each generated template:

1. **Open Template** - Navigate to `clients/[client]/audits/[date]-[type]-audit-template.md`
2. **Copy Prompt** - Copy the audit prompt from the template
3. **Open Claude Code** - Launch Cursor with Claude
4. **Ensure MCP Connected** - Verify Google Ads MCP server is active
5. **Paste & Run** - Paste prompt, Claude fetches data and generates report
6. **Save Results** - Copy output back into the template file
7. **Create Tasks** - Add action items to Google Tasks
8. **Update Context** - Document key learnings in client CONTEXT.md

### Step 3: Action & Tracking

1. **Prioritize Recommendations** - Focus on high-impact actions
2. **Create Google Tasks** - One task per recommendation
3. **Implement Changes** - Execute in Google Ads UI
4. **Monitor Results** - Track in next week's audit
5. **Document Learnings** - Update client CONTEXT.md

---

## File Structure

```
clients/
└── [client-name]/
    ├── CONTEXT.md
    └── audits/
        ├── 2025-11-05-audit-index.md
        ├── 2025-11-05-weekly-audit-template.md
        ├── 2025-11-05-impression_share-audit-template.md
        ├── 2025-11-05-keyword-audit-template.md
        ├── 2025-11-05-structure-audit-template.md
        └── audit-config-20251105.json
```

### Audit Template Format

Each template includes:
- **Objective** - What this audit is for
- **Execution Instructions** - Step-by-step guide
- **Audit Prompt** - Ready-to-run prompt for Claude
- **Results Section** - Placeholder for audit output
- **Action Items** - Checklist for follow-up
- **Related Files** - Links to context and previous audits

---

## Integration with Other Systems

### Daily Briefing

The daily briefing (7 AM) can reference recent audit findings:
- Check `audits/` folder for recent reports
- Highlight critical recommendations
- Track completion of audit action items

### Google Tasks

When audit is complete:
1. Create Google Task for each recommendation
2. Include link to audit file in task notes
3. Set due dates based on priority
4. Tag with client name

### Weekly Summary

Weekly email summary (Monday 9 AM) can include:
- Link to latest audit index
- Number of audits run vs completed
- High-priority recommendations not yet actioned

### Knowledge Base

Key audit findings can be:
1. Documented in client CONTEXT.md
2. Added to knowledge base as learnings
3. Referenced in future audits

---

## ROK Analysis Framework

This system implements ROK's systematic Google Ads analysis methodology:

### Source

[ROK Analysis Prompts](../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md)

### Key Principles

1. **Actionable-Only Focus** - Skip stable metrics, show what needs attention
2. **Relative Benchmarking** - Use account average × multipliers (0.7, 1.3)
3. **Root Cause Analysis** - Beyond metrics to diagnose feed, auction, creative issues
4. **Business Language** - Revenue impact, not just ad metrics
5. **Prioritized Recommendations** - 3-5 specific actions, not overwhelming lists

### Prompt Chaining Workflow

```
Monday 10 AM: Generate all audit templates
↓
Run Weekly Audit (Prompt 1) - Overall health
↓
Identify specific issues (e.g., Shopping ROAS decline)
↓
Run targeted audit (Impression Share or Keyword)
↓
Diagnose root cause (budget, rank, quality)
↓
Implement recommendation
↓
Track in Google Tasks + CONTEXT.md
↓
Next Monday: Monitor results in new weekly audit
```

---

## Active Clients

Current clients with audit generation enabled:

- Smythson
- Devonshire Hotels
- Tree2MyDoor
- UNO Lighting
- Superspace

To add more clients, edit `CLIENTS` list in `agents/reporting/google-ads-auditor.py`.

---

## Customization

### Adjust Thresholds

In the audit prompts, you can modify:
- Performance change thresholds: `±15%` → your preference
- ROAS multipliers: `0.7×`, `1.3×` → adjust for client volatility
- Minimum spend thresholds: `$50` → adjust for account size

### Add Client Context

Templates automatically load client CONTEXT.md if available. Prompts can reference:
- Business changes
- Stock issues
- Seasonality
- Recent experiments

### Custom Audit Types

To create custom audits:
1. Add method to `GoogleAdsAuditor` class
2. Define new audit prompt
3. Add to `AUDIT_TYPES` dictionary
4. Update CLI arguments

---

## LaunchAgent Configuration

**File:** `~/Library/LaunchAgents/com.petesbrain.google-ads-auditor.plist`

**Schedule:**
- **Day:** Monday (1)
- **Time:** 10:00 AM
- **Command:** `python3 google-ads-auditor.py --all`

**Logs:**
- Output: `~/.petesbrain-google-ads-auditor.log`
- Errors: `~/.petesbrain-google-ads-auditor-error.log`

### Management

```bash
# View status
launchctl list | grep google-ads-auditor

# View logs
tail -f ~/.petesbrain-google-ads-auditor.log
tail -f ~/.petesbrain-google-ads-auditor-error.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.google-ads-auditor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.google-ads-auditor.plist

# Run manually
launchctl start com.petesbrain.google-ads-auditor
```

---

## Advanced Usage

### Combine with Root Cause Analysis

Before running audits, check:
1. **CONTEXT.md** - Client business changes
2. **Completed Tasks** - Recent account actions
3. **Knowledge Base** - Platform updates
4. **Google Analytics** - Website conversion rate changes
5. **Client Website** - Availability, pricing, promotions

Then run appropriate audit to separate controllable vs uncontrollable factors.

### Create Custom Variations

Adapt prompts for:
- **Display campaigns** - Focus on placement/audience
- **Video campaigns** - YouTube-specific metrics (VTR, CPV)
- **Lead gen** - CPL and lead quality instead of ROAS
- **Brand campaigns** - Impression share, SOV, awareness

### Export & Share

Completed audits can be:
1. Saved as PDFs for client presentation
2. Shared in Google Drive client folders
3. Referenced in status reports
4. Used as templates for proposals

---

## Troubleshooting

### No Templates Generated

```bash
# Check LaunchAgent status
launchctl list | grep google-ads-auditor

# Check error logs
tail ~/.petesbrain-google-ads-auditor-error.log

# Run manually to see errors
python3 agents/reporting/google-ads-auditor.py --all
```

### MCP Connection Issues

If Claude can't fetch Google Ads data:
1. Check MCP server status in Cursor settings
2. Verify Google Ads credentials
3. Test with simple query: "List campaigns"
4. Restart Cursor if needed

### Prompts Not Working

If audit prompts don't generate good results:
1. Check if client has Google Ads data
2. Verify date range is appropriate
3. Adjust thresholds for account size
4. Add more client context to prompt

---

## Related Documentation

- [ROK Analysis Prompts](../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md) - Full framework
- [Daily Briefing System](DAILY-BRIEFING-SYSTEM.md) - Morning intelligence
- [Google Tasks Integration](GOOGLE-TASKS-INTEGRATION.md) - Action tracking
- [Client Context](../clients/[client]/CONTEXT.md) - Business intelligence

---

## Roadmap

### Completed ✅
- [x] Audit template generator
- [x] 4 audit types (weekly, impression share, keyword, structure)
- [x] Weekly automated generation
- [x] Client-specific folders
- [x] MCP-ready prompts
- [x] Command-line tool
- [x] Documentation

### Future Enhancements 🔮
- [ ] Integrate audit links into daily briefing
- [ ] Auto-create Google Tasks from audit recommendations
- [ ] Email notification when audits are ready
- [ ] Audit completion tracking dashboard
- [ ] Historical audit comparison
- [ ] AI-powered audit result summarization

---

## Statistics

**Clients:** 5 active  
**Audit Types:** 4 per client  
**Templates Generated Weekly:** 20 (4 × 5)  
**Estimated Time Saved:** 2-3 hours per audit  
**ROI:** Standardized, repeatable analysis framework

---

**Last Updated:** 2025-11-05  
**Agent:** `agents/reporting/google-ads-auditor.py`  
**Version:** 1.0

