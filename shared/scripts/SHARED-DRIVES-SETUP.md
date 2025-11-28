# Shared Drives Monitor - Setup Guide

**Created:** 2025-10-31
**Purpose:** Automated monitoring of "Shared with Me" Google Drive for client documents

---

## What It Does

The Shared Drives Monitor automatically tracks client-related documents in your "Shared with Me" Google Drive:

1. **Daily Scans** - Checks for new/modified documents
2. **Client Matching** - Automatically identifies which client each document belongs to
3. **CONTEXT.md Updates** - Adds new findings to each client's CONTEXT.md
4. **Weekly Summaries** - Includes findings in Monday morning email

### What It Tracks

✅ **Documents:** Google Docs, Sheets, Slides, PDFs, Word, Excel, PowerPoint
❌ **Excludes:** Images (JPG, PNG, GIF, etc.)

---

## Current Status

### ✅ Implemented (Oct 31, 2025):
- Devonshire CONTEXT.md updated with shared drive resources
- Key documents identified:
  - Monthly slide decks
  - PMax & AI Insights sheets
  - AI Whisperer analysis tools
  - Website analysis docs

### 🚧 In Progress:
- Full automation script (skeleton created)
- Daily LaunchAgent setup
- Weekly email integration

---

## How to Use

### On-Demand Searches

**Search for specific client documents:**
```
"Search Devonshire Drive for monthly report"
"What's new in Smythson shared drives?"
"Search shared drives for October slides"
```

**Check all clients:**
```
"Scan shared drives for client updates"
"What new documents are in shared drives?"
```

### Automated Daily Scans

**Status:** Pending LaunchAgent setup

**Will do:**
- Run every morning at 8:00 AM
- Check for files modified in last 24 hours
- Update client CONTEXT.md files
- Log findings to `~/.petesbrain-shared-drives.log`

---

## Client Keyword Mapping

The system automatically matches documents to clients based on these keywords:

| Client | Keywords |
|--------|----------|
| Devonshire Hotels | devonshire, dev \|, daba, cavendish, beeley, pilsley, fell, hide, highwayman |
| Smythson | smythson, smy \| |
| Clear Prospects | clear prospects, clearprospects |
| Tree2mydoor | tree2mydoor, tree 2 my door, t2md |
| Superspace | superspace |
| Uno Lighting | uno lighting, uno-lighting |
| National Design Academy | nda, national design academy |
| Godshot | godshot |
| Print My PDF | print my pdf, printmypdf, pmypdf |
| Bright Minds | bright minds |
| OTC | otc, online tech club |

---

## CONTEXT.md Integration

Each client's CONTEXT.md now includes a "Shared Drive Resources" section:

**Contains:**
- Last scanned date
- List of key shared documents
- How to access instructions
- Document descriptions

**Example:**
```markdown
## Shared Drive Resources

**Last Scanned:** 2025-10-31

### Key Shared Documents

**Monthly Reporting:**
- "Devonshire Hotels Monthly Report - November 2024"
  - Paid Search section updated ~7th-8th monthly

**Analysis Tools:**
- "Devonshire Group - PMax & AI Insights" ⭐ ACTIVE
```

---

## Weekly Email Integration

Shared drive findings will be included in the Monday morning weekly summary email:

**Section:** "📁 Shared Drive Updates"
**Contains:**
- New documents found this week
- Modified documents
- Grouped by client
- Direct links to documents

---

## Files & Locations

**Script:** `/Users/administrator/Documents/PetesBrain/shared/scripts/shared-drives-monitor.py`
**State File:** `/Users/administrator/Documents/PetesBrain/shared/data/shared-drives-state.json`
**Log File:** `~/.petesbrain-shared-drives.log`
**LaunchAgent:** `~/Library/LaunchAgents/com.petesbrain.shared-drives.plist` (pending)

---

## Commands

### Manual Scan
```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/shared-drives-monitor.py
```

### Scan Specific Client
```bash
python3 shared/scripts/shared-drives-monitor.py --client devonshire-hotels
```

### Scan Last N Days
```bash
python3 shared/scripts/shared-drives-monitor.py --days 30
```

### Dry Run (Don't Update Files)
```bash
python3 shared/scripts/shared-drives-monitor.py --dry-run
```

### Check Logs
```bash
cat ~/.petesbrain-shared-drives.log
```

---

## Future Enhancements

🔮 **Document Summaries** - Auto-generate summaries of new docs
🔮 **Change Detection** - Track specific changes to existing docs
🔮 **Smart Alerts** - Notify when monthly slide decks are ready
🔮 **Auto-Download** - Save copies of critical docs locally
🔮 **Version Tracking** - Track iterations of monthly reports

---

## Troubleshooting

### No Documents Found

**Check:**
1. Google Drive MCP is connected: `mcp__google-drive__search "test"`
2. You have access to shared drives
3. Keywords match document names

### Wrong Client Assignment

**Fix:**
Update `CLIENT_KEYWORDS` in `shared-drives-monitor.py`

### Missing Recent Documents

**Possible causes:**
- Document modified time not updated by owner
- Document is an image (excluded)
- Keywords don't match any client

---

**Last Updated:** 2025-10-31
**Status:** Partially implemented, full automation pending
