# Claude Skills - Quick Start Guide

**For**: Pete Empson / ROK Team  
**Date**: November 5, 2025  
**Time to Read**: 3 minutes

---

## What Are Skills?

Think of skills as **instant expertise** that activates automatically when you're working with Claude.

**Example**:
```
You: "How's Smythson performing this week?"
     ↓
     (Campaign audit skill auto-triggers)
     ↓
Claude: [Pulls live data, analyzes performance, gives 3-5 recommendations]
```

No setup, no manual prompts needed—just ask naturally.

---

## Your 4 Installed Skills

### 1. 🔍 GAQL Query Builder
**Ask**: "Build me a query for..."  
**Gets**: Syntactically correct Google Ads queries  
**Use for**: Custom reports, specific metrics, ad hoc data pulls

### 2. 📊 CSV Analyzer
**Ask**: [Upload CSV] "Analyze this data"  
**Gets**: Insights, top/bottom performers, recommendations  
**Use for**: Exported reports, product data, campaign performance

### 3. 🎯 Campaign Audit
**Ask**: "Audit [client] account"  
**Gets**: Full performance review with ROK framework  
**Use for**: Weekly reviews, client prep, optimization planning

### 4. 🔑 Keyword Audit
**Ask**: "Find wasted spend keywords"  
**Gets**: Negative keywords, bid adjustments, opportunity list  
**Use for**: Search campaign cleanup, SQR analysis, budget optimization

---

## How to Use (3 Simple Steps)

### Step 1: Just Ask
Use natural language:
- ✅ "Audit Smythson for this week"
- ✅ "Show me product performance"
- ✅ "Find keywords with zero conversions"
- ✅ "Build a query for impression share data"

### Step 2: Skill Auto-Triggers
Claude detects what you need and activates the right skill automatically.

### Step 3: Get Results
- Live data from Google Ads (via MCP)
- Actionable insights
- Specific recommendations
- Ready-to-use outputs

---

## Real-World Examples

### Before Client Call
```
You: "Quick Devonshire audit for this week"

→ 2 minutes later:
Executive summary, key metrics, 3 priority actions ready
```

### Analyzing Export
```
You: [Upload CSV] "What's the story here?"

→ Instant analysis:
Top performers, problem areas, budget recommendations
```

### Finding Waste
```
You: "Show me wasted spend in Search campaigns"

→ Gets you:
Keyword pause list, negative keywords, savings estimate
```

---

## What Makes Skills Different?

### vs Your Agents (Background Tasks)
**Agents**: Run on schedules, monitor proactively  
**Skills**: Activate during conversations, on-demand analysis

### vs Manual Analysis
**Manual**: 20-30 minutes per audit  
**Skills**: 2-5 minutes, automatically formatted

### vs MCP Servers
**MCP**: Provides raw data access  
**Skills**: Uses MCP but adds analysis, context, recommendations

**All work together**: Agents monitor → Alert you → You ask Claude → Skill analyzes via MCP → You implement

---

## Quick Reference Card

| I Need To... | Ask Claude... | Skill Used |
|-------------|---------------|------------|
| Review account performance | "Audit [client] account" | Campaign Audit |
| Find wasted keywords | "Find wasted spend keywords" | Keyword Audit |
| Analyze CSV export | [Upload] "Analyze this" | CSV Analyzer |
| Build custom query | "Build query for..." | GAQL Builder |
| Get impression share | "Show impression share loss" | Campaign Audit |
| Find negative keywords | "What negatives should I add?" | Keyword Audit |
| Check product performance | "Show product-level data" | Campaign Audit + CSV |

---

## Pro Tips

### 1. Be Specific About Clients
✅ "Audit Smythson account"  
❌ "Audit account" (which one?)

### 2. Mention Time Ranges
✅ "Last week's performance"  
✅ "Last 30 days"  
(Default is usually 7 days)

### 3. Reference Previous Audits
✅ "Compare to last week's audit"  
(Skills can load previous audit files)

### 4. Ask Follow-Up Questions
```
You: "Audit Smythson"
Claude: [Provides audit]
You: "Dig deeper into YouTube placement"
Claude: [Focuses on YouTube analysis]
```

---

## Common Issues (Quick Fixes)

### "Skill not triggering"
→ Use more explicit language: "Use the campaign audit skill for Smythson"

### "Can't access Google Ads data"
→ Check MCP connection: See `docs/MCP-SERVERS.md`

### "Wrong client context loaded"
→ Specify full path: "Load clients/smythson/CONTEXT.md"

---

## Time Savings

| Task | Before | With Skills | Saved |
|------|--------|-------------|-------|
| Weekly audit | 25 min | 5 min | 20 min |
| CSV analysis | 15 min | 3 min | 12 min |
| Keyword cleanup | 35 min | 10 min | 25 min |
| Query building | 8 min | 2 min | 6 min |

**Average**: 1-2 hours saved per day

---

## Next Steps

1. **Try it now**: "Audit [your most active client] for this week"
2. **Experiment**: Upload a CSV export and ask for analysis
3. **Compare**: See how it differs from your scheduled Monday audits
4. **Iterate**: Skills learn from usage patterns

---

## Need More Detail?

- **Full Documentation**: `docs/CLAUDE-SKILLS-SETUP.md`
- **Technical Details**: `.claude/skills/README.md`
- **ROK Framework**: `roksys/knowledge-base/rok-methodologies/`
- **MCP Setup**: `docs/MCP-SERVERS.md`

---

**Remember**: Skills work best when you just talk naturally to Claude. No special syntax, no manual steps—just ask what you need.

**Status**: ✅ Ready to use right now  
**Setup Required**: None (already done)  
**Cost**: Free (uses existing MCP access)

---

*Created: November 5, 2025*  
*Part of industry resources integration project*

