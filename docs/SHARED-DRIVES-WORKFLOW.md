# Shared Drives - Manual Update Workflow

**Status**: Active (manual on-demand scanning)
**Frequency**: Monthly (first week of month)
**Google Task**: "Scan shared drives and update client CONTEXT.md files"

---

## Overview

Shared files from Google Drive are automatically categorized into three types:

1. **Client Resources** → Client CONTEXT.md files
2. **Roksys Knowledge Base** → `roksys/knowledge-base/_inbox/documents/`
3. **Personal Knowledge** → Your personal notes/learning resources

Files are matched using keywords and automatically routed to the appropriate location when you trigger a scan.

## When to Update

**Monthly Scan** (recommended):
- First week of each month
- Google Task reminder set for 7th of each month
- Ensures all client CONTEXT.md files stay current

**Ad-hoc Updates**:
- When client shares new important document
- When you notice new monthly reports
- After client meetings that reference shared resources

---

## How to Trigger a Scan

### Option 1: Full Scan (All Clients)

Simply tell Claude Code:
```
Scan shared drives and update client CONTEXT files
```

Claude will:
1. Search Google Drive for shared documents
2. Categorize files into three types:
   - **Client files** → Update client CONTEXT.md
   - **Roksys/industry files** → Add to knowledge base inbox
   - **Personal files** → Flag for your review
3. Update appropriate locations with findings
4. Report what was found in each category

### Option 2: Specific Client Update

If you know about a specific document:
```
Update [client-name] CONTEXT.md with this shared file: [file name or link]
```

Example:
```
Update Devonshire CONTEXT.md with this shared file:
"Devonshire Hotels Monthly Report - November 2024"
```

---

## What Gets Tracked

The system matches and tracks:

**Document Types**:
- ✅ Google Docs
- ✅ Google Sheets
- ✅ Google Slides
- ✅ PDFs
- ❌ Images (excluded)
- ❌ Videos (excluded)

**Content Categories**:
- Monthly reports and presentations
- Campaign briefs and strategy documents
- Product data and supplemental feeds
- Client-maintained documentation

---

## File Categorization System

Files are automatically categorized using a **three-tier priority system**:

### Priority 1: Client Files (Most Specific)

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
| accessories-for-the-home | afh, accessories for the home |
| crowd-control | crowd control |
| go-glean | go glean |
| grain-guard | grain guard |
| just-bin-bags | just bin bags, jbb |

**Action**: Add to `clients/[client-name]/CONTEXT.md`

### Priority 2: Roksys Knowledge Base (Industry/Platform Content)

**Keywords**: google ads, ppc, performance max, pmax, shopping campaigns, smart bidding, troas, roas, conversion tracking, google analytics, ga4, gtm, merchant center, facebook ads, meta ads, digital marketing, paid search, sem, ai in marketing, automation, machine learning, industry insights, platform updates, best practices, rok, roksys, methodology, strategy, playbook

**Action**: Add to `roksys/knowledge-base/_inbox/documents/` for processing

**Examples**:
- "Google Ads Performance Max Best Practices 2025.pdf"
- "Smart Bidding Strategy Guide.docx"
- "Roksys Q4 2025 Methodology Updates.pdf"
- "Industry Insights - AI in Digital Marketing.pdf"

### Priority 3: Personal Knowledge (Your Learning)

**Keywords**: peter empson, petere, personal, notes to self, learning, training, course, tutorial, book, reading, research, ideas

**Action**: Flag for your review / add to personal notes

**Examples**:
- "Peter's Notes - Google Ads Strategy Ideas.docx"
- "Personal Learning - Machine Learning Course.pdf"

### Priority 4: Uncategorized

**Action**: Claude will list these and ask you where they should go

**Note**: If a file doesn't auto-match, you can manually specify the category by telling Claude.

---

## CONTEXT.md Format

Each client's CONTEXT.md includes this section:

```markdown
## Shared Drive Resources

**Last Scanned:** 2025-11-01 14:30

### Key Shared Documents

**Presentations:**
- 📊 **[Monthly Report - November 2024](https://docs.google.com/...)** (Google Slides)
  - Last modified: 2025-11-05

**Spreadsheets:**
- 📊 **[Budget Tracker 2025](https://docs.google.com/...)** (Google Sheets)
  - Last modified: 2025-10-30

**Documents:**
- 📄 **[Campaign Brief - Q4 Strategy](https://docs.google.com/...)** (Google Docs)
  - Last modified: 2025-10-15

_(3 new/updated in last 30 days)_
```

Files are grouped by type and include:
- File name (with clickable link)
- File type (Google Docs/Sheets/Slides/PDF)
- Last modified date

---

## Monthly Workflow

**Week 1 of Month**:

1. **Google Task reminder** appears: "Scan shared drives and update client CONTEXT.md files"

2. **Trigger scan** in Claude Code:
   ```
   Scan shared drives and update client CONTEXT files
   ```

3. **Review results**:
   - Claude reports what was found
   - Check if any important files were missed
   - Manually add any that weren't auto-matched

4. **Complete task** in Google Tasks

5. **Next month**: Task recurs automatically

---

## Ad-hoc Updates

**When client shares new document**:

Example: Devonshire emails you their November monthly report

1. **Quick update**:
   ```
   Update Devonshire CONTEXT.md - Shared Drive Resources:

   New file: "Devonshire Hotels Monthly Report - November 2024"
   Type: Google Slides
   Contains Paid Search section (updated monthly ~7th-8th)
   ```

2. Claude adds it to the CONTEXT.md immediately

**Benefits**:
- Instant documentation
- Don't wait for monthly scan
- Ensures nothing important is missed

---

## Maintenance

### Adding New Client Keywords

If files aren't matching correctly, update keywords:

**Tell Claude Code**:
```
Add keyword "[keyword]" to [client-name] shared drive matching
```

Example:
```
Add keyword "DH Monthly" to devonshire-hotels shared drive matching
```

### Removing Outdated Files

Periodically review CONTEXT.md sections and remove outdated files:

```
Remove old files from [client-name] Shared Drive Resources section
Keep only files from last 6 months
```

---

## Integration with Weekly Email

The weekly Monday email (9 AM) includes a "Shared Drive Updates" section showing:
- New/updated files in last 7 days
- Grouped by client
- Clickable links to view on Google Drive

**Note**: Weekly email only shows RECENT updates (7 days), while CONTEXT.md shows ALL tracked files.

---

## Troubleshooting

### File Not Matched to Client

**Issue**: Important file found but not matched to any client

**Solution**: Manually specify client
```
Add this file to [client-name] CONTEXT.md:
[file name or link]
```

### Too Many Files Showing Up

**Issue**: Client folder has hundreds of old files cluttering CONTEXT.md

**Solution**: Filter by date
```
Update [client-name] Shared Drive Resources
Only include files modified in last 6 months
```

### Missing Expected File

**Issue**: You know file is shared but scan doesn't find it

**Possible causes**:
1. File is in "My Drive" not "Shared with Me"
2. File name doesn't match client keywords
3. File type is excluded (image, video)

**Solution**: Manually add it
```
Add to [client-name] CONTEXT.md:
[file name and link]
```

---

## Files Reference

**Related Documentation**:
- [docs/DEVONSHIRE-AUTOMATION-COMPLETE.md](DEVONSHIRE-AUTOMATION-COMPLETE.md) - Complete automation overview
- [shared/scripts/shared-drives-monitor-v2.py](../shared/scripts/shared-drives-monitor-v2.py) - Helper functions for updates

**CONTEXT.md Sections**:
- All 16 client CONTEXT.md files have "Shared Drive Resources" section
- Located before "Document History" section
- Updated via manual Claude Code commands

---

## Summary

✅ **What Works**:
- Monthly Google Task reminder (7th of month)
- On-demand scanning via Claude Code
- Automatic client matching using keywords
- CONTEXT.md updates with formatted file listings
- Weekly email showing recent updates

❌ **What Doesn't Work**:
- Automatic daily scanning (removed - not reliable)
- Direct script execution (requires Claude Code interaction)

💡 **Best Practice**:
- Do monthly scans for comprehensive updates
- Do ad-hoc updates when you notice new important files
- Review CONTEXT.md sections quarterly to remove outdated files

---

**Last Updated**: 2025-10-31
**Author**: Claude Code
