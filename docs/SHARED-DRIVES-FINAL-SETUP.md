# Shared Drives - Final Setup Summary

**Date**: 2025-10-31
**Status**: ✅ Complete (Manual On-Demand System)

---

## What Was Decided

After discovering that Google Drive MCP doesn't support reliable automated "Shared with Me" scanning, we switched to a **manual on-demand** approach instead.

### Why Manual Instead of Automated?

**Technical limitation**: Google Drive MCP can't programmatically access "Shared with Me" in a way that a background script can use.

**Solution**: Use Claude Code's interactive capabilities to scan on-demand when you need it.

---

## What's Set Up

### ✅ Monthly Recurring Task

**Google Task Created**: "Scan shared drives and update client CONTEXT.md files"
- **Due Date**: 7th of each month (starting November 7, 2025)
- **Task Notes**: Complete instructions on how to trigger scan
- **Recurrence**: Will remind you monthly

### ✅ All Client CONTEXT.md Files Updated

**16 clients** now have "Shared Drive Resources" section:
- accessories-for-the-home
- bright-minds
- clear-prospects
- crowd-control
- devonshire-hotels
- go-glean
- godshot
- grain-guard
- just-bin-bags
- national-design-academy
- otc
- print-my-pdf
- smythson
- superspace
- tree2mydoor
- uno-lighting

### ✅ Helper Scripts Created

**File**: `shared/scripts/shared-drives-monitor-v2.py`
- Helper functions for formatting file entries
- Client keyword matching logic
- CONTEXT.md update functions
- Used by Claude Code during scans

### ✅ Documentation Created

**File**: `docs/SHARED-DRIVES-WORKFLOW.md`
- Complete workflow guide
- How to trigger scans
- Troubleshooting tips
- Integration with weekly email

### ✅ Weekly Email Integration

**File**: `shared/scripts/weekly-meeting-review.py`
- Includes "Shared Drive Updates" section
- Shows files from last 7 days (if any manual scans done)
- Grouped by client
- Clickable links to Google Drive

---

## How to Use

### Monthly Scan (Recommended)

When Google Task reminder appears:

1. **Open Claude Code**

2. **Tell Claude**:
   ```
   Scan shared drives and update client CONTEXT files
   ```

3. **Claude will**:
   - Search Google Drive for shared documents
   - Filter to document types (exclude images)
   - Match files to clients using keywords
   - Update each client's CONTEXT.md
   - Report what was found

4. **Mark task complete** in Google Tasks

### Ad-hoc Updates

When you notice a specific shared file:

```
Update [client-name] CONTEXT.md with this shared file:
"[file name or link]"
```

Example:
```
Update Devonshire CONTEXT.md with this shared file:
"Devonshire Hotels Monthly Report - November 2024"
https://docs.google.com/presentation/d/...
```

---

## What Was Removed

### ❌ Automated Daily Scanning

**Removed**:
- LaunchAgent: `com.petesbrain.shared-drives` (unloaded)
- Automatic 8 AM daily scans

**Why**: Google Drive API doesn't support reliable automated access to "Shared with Me" via MCP server

**Replaced with**: Manual on-demand scanning via Claude Code + monthly Google Task reminder

---

## Client Keyword Matching

Files automatically matched to clients using these keywords:

| Client | Keywords |
|--------|----------|
| devonshire-hotels | devonshire, dev \|, daba, cavendish, beeley, pilsley, fell, hide, highwayman |
| smythson | smythson, smy \| |
| clear-prospects | clear prospects, clearprospects, cp \| |
| tree2mydoor | tree2mydoor, tree 2 my door, t2md |
| superspace | superspace |
| uno-lighting | uno lighting, uno-lighting |
| national-design-academy | nda, national design academy |
| godshot | godshot |
| print-my-pdf | print my pdf, printmypdf, pmypdf |
| bright-minds | bright minds |
| otc | otc, online tech club |

**Note**: If a file doesn't auto-match, you can manually specify which client it belongs to.

---

## File Types Tracked

**Included**:
- ✅ Google Docs
- ✅ Google Sheets
- ✅ Google Slides
- ✅ PDFs

**Excluded**:
- ❌ Images (JPG, PNG, etc.)
- ❌ Videos
- ❌ Zip files
- ❌ Other binary formats

---

## CONTEXT.md Format

Example of what gets added:

```markdown
## Shared Drive Resources

**Last Scanned:** 2025-11-07 14:30

### Key Shared Documents

**Presentations:**
- 📊 **[Devonshire Hotels Monthly Report - November 2024](https://docs.google.com/...)** (Google Slides)
  - Last modified: 2025-11-05

**Spreadsheets:**
- 📊 **[Budget Tracker 2025](https://docs.google.com/...)** (Google Sheets)
  - Last modified: 2025-10-30

**Documents:**
- 📄 **[Campaign Brief - Q4 Strategy](https://docs.google.com/...)** (Google Docs)
  - Last modified: 2025-10-15

_(3 new/updated in last 30 days)_
```

---

## Integration with Weekly Email

The Monday 9 AM weekly email includes a "Shared Drive Updates" section showing:
- Files added/updated in last 7 days
- Only shown if manual scans have been done
- Grouped by client
- Direct links to view on Google Drive

**Note**: This is separate from CONTEXT.md which shows ALL tracked files, not just recent ones.

---

## Next Steps

### First Scan (November 7, 2025)

When the Google Task reminder appears:

1. Open Claude Code
2. Say: "Scan shared drives and update client CONTEXT files"
3. Review what Claude found
4. Check if any files need manual adding
5. Mark task complete

### Ongoing Maintenance

**Monthly**:
- Respond to Google Task reminder
- Trigger scan via Claude Code
- Complete task

**As Needed**:
- When client shares important new document
- Tell Claude to add it to CONTEXT.md immediately
- Don't wait for monthly scan

**Quarterly** (optional):
- Review CONTEXT.md sections
- Remove outdated files (>6 months old)
- Keep sections current and relevant

---

## Files Reference

**Documentation**:
- [docs/SHARED-DRIVES-WORKFLOW.md](SHARED-DRIVES-WORKFLOW.md) - Complete workflow guide
- [docs/DEVONSHIRE-AUTOMATION-COMPLETE.md](DEVONSHIRE-AUTOMATION-COMPLETE.md) - Full automation overview

**Scripts**:
- [shared/scripts/shared-drives-monitor-v2.py](../shared/scripts/shared-drives-monitor-v2.py) - Helper functions

**Client Files**:
- All client CONTEXT.md files have "Shared Drive Resources" section
- Located before "Document History"
- Updated via Claude Code commands

**State File**:
- `shared/data/shared-drives-state.json` (auto-created during scans)
- Tracks recent updates for weekly email

---

## Summary

✅ **What's Working**:
- Monthly Google Task reminder (7th of month)
- On-demand scanning via Claude Code
- Client keyword matching
- CONTEXT.md updates with formatted listings
- Weekly email integration (shows recent updates)
- All 16 client folders prepared

❌ **What's NOT Automated**:
- Daily background scanning (not possible with current MCP)
- Automatic CONTEXT.md updates (requires manual trigger)

💡 **Best Practice**:
- Monthly scans keep everything current
- Ad-hoc updates when you notice new important files
- Claude Code handles all the heavy lifting
- You just trigger it when needed

---

**Status**: Ready to use
**First scan**: November 7, 2025
**Contact**: Just tell Claude Code: "Scan shared drives"

---

**Last Updated**: 2025-10-31
**Setup By**: Claude Code
