# Microsoft Teams Chat Archives - Paul Riley

**Purpose:** Store Microsoft Teams chat exports with Paul Riley for NDA context and reference.

**Location:** `/clients/national-design-academy/teams-chats/`

---

## File Naming Convention

Format: `paul-riley-YYYY-MM-DD.md`

Examples:
- `paul-riley-2025-11-25.md` - Chat imported on 25 Nov 2025
- `paul-riley-2025-12-01.md` - Next import on 1 Dec 2025

---

## Import Process

### 1. Download from Microsoft Teams
1. Open Teams chat with Paul Riley
2. Export/download conversation
3. Save to Downloads folder

### 2. Before Importing - Check for Duplicates

Run this command to check if content already exists:

```bash
# Check last message in newest file
tail -20 /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/paul-riley-*.md | grep -A 5 "Paul Riley:"

# Search for specific message content
grep -r "specific phrase from new export" /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/
```

### 3. Import New Content

**Tell Claude:**
> "Import the new Teams chat with Paul Riley. Check for duplicates first. The chat export is [paste content or provide file path]"

**Claude will:**
1. Check existing files for duplicate messages
2. Identify where previous import ended
3. Only import NEW messages since last import
4. Create new dated file with only new content

---

## Chat Archive Index

| File | Date Range | Key Topics | Message Count |
|------|-----------|------------|---------------|
| `paul-riley-2025-11-25.md` | Aug-Nov 2025 | Budget reduction, landing page updates, URL mismatch fix, UAE studio diploma | ~80 messages |

---

## Search Tips

### Find Specific Topics

```bash
# Search for budget discussions
grep -i "budget" /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/*.md

# Search for landing page mentions
grep -i "landing page" /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/*.md

# Search for specific URLs
grep "degrees-interior-design" /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/*.md

# Search for revenue/financial discussions
grep -E "(revenue|enrolment.*data|Dubai income)" /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/*.md
```

### View Recent Conversations

```bash
# Last 50 lines of most recent file
tail -50 /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/paul-riley-2025-11-25.md

# All files sorted by date
ls -lt /Users/administrator/Documents/PetesBrain/clients/national-design-academy/teams-chats/
```

---

## Deduplication Strategy

**How we avoid duplicates:**

1. **Unique message markers:** Each import notes exact date and last message
2. **Chronological file naming:** YYYY-MM-DD format keeps imports in order
3. **Manual verification:** Claude checks last message in previous import before adding new content
4. **Message fingerprinting:** Look for exact phrase matches to detect overlap

**If overlap is detected:**
- New file only contains messages AFTER last message in previous file
- No duplicate messages across files
- Each import picks up where last one ended

---

## Context Usage

These chat archives are valuable for:

- **Understanding client preferences** (communication style, priorities)
- **Decision history** (why budgets changed, why campaigns paused)
- **Technical discussions** (landing page updates, URL structure)
- **Business context** (revenue data, enrolment figures, studio courses)
- **Problem-solving** (how issues were discovered and resolved)

**When to reference:**
- Writing client emails (match tone/style from chats)
- Making strategic decisions (refer to past discussions)
- Explaining historical changes (budget cuts, campaign pauses)
- Understanding client pain points (Dubai studio sales, MENA region focus)

---

## Maintenance

### Monthly Review
- Archive old chats if getting too long (>1000 messages)
- Update index table with new imports
- Check for any formatting issues

### Before Each Import
1. Note last message timestamp from previous file
2. Check for message overlap
3. Only import new content

---

**Last Updated:** 25 November 2025
