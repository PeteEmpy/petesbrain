# Microsoft Teams Chat Archives - Smythson

**Purpose:** Store Microsoft Teams chat exports for Smythson context and reference.

**Location:** `/clients/smythson/teams-chats/`

---

## Chat Groups

### 1. Paid Search Catch Up
**Participants:** Peter Empson, Alex Clarke, Lauryn (Frank Smythson LTD)
**Purpose:** Regular paid search performance discussions, strategy approvals, promotional planning

---

## File Naming Convention

Format: `[chat-name]-YYYY-MM-DD.md`

Examples:
- `paid-search-catch-up-2025-11-25.md` - Chat imported on 25 Nov 2025
- `paid-search-catch-up-2025-12-01.md` - Next import on 1 Dec 2025

---

## Import Process

### 1. Download from Microsoft Teams
1. Open Teams chat (e.g., "Paid Search Catch Up")
2. Export/download conversation
3. Save to Downloads folder

### 2. Before Importing - Check for Duplicates

Run this command to check if content already exists:

```bash
# Check last message in newest file
tail -20 /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/paid-search-*.md | grep -A 5 "Alex Clarke:\|Peter Empson:"

# Search for specific message content
grep -r "specific phrase from new export" /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/
```

### 3. Import New Content

**Tell Claude:**
> "Import the new Smythson Teams chat. Check for duplicates first. The chat export is [paste content or provide file path]"

**Claude will:**
1. Check existing files for duplicate messages
2. Identify where previous import ended
3. Only import NEW messages since last import
4. Create new dated file with only new content

---

## Chat Archive Index

| File | Chat Group | Date Range | Key Topics | Participants |
|------|-----------|-----------|------------|--------------|
| `paid-search-catch-up-2025-11-25.md` | Paid Search Catch Up | Nov 2025 | Brand vs Non-Brand analysis, Black Friday strategy, Dec promotions | Peter, Alex, Lauryn |

---

## Search Tips

### Find Specific Topics

```bash
# Search for brand performance discussions
grep -i "brand" /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/*.md

# Search for promotion mentions
grep -i "promotion\|promo" /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/*.md

# Search for ROAS discussions
grep -i "roas" /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/*.md

# Search for strategy approvals
grep -E "(strategy|approval|happy to proceed)" /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/*.md
```

### View Recent Conversations

```bash
# Last 50 lines of most recent file
tail -50 /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/paid-search-catch-up-2025-11-25.md

# All files sorted by date
ls -lt /Users/administrator/Documents/PetesBrain/clients/smythson/teams-chats/
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

- **Strategy approvals** (Black Friday, promotional campaigns)
- **Performance discussions** (brand vs non-brand, YoY comparisons)
- **Decision history** (why promotions cancelled/changed)
- **Client preferences** (Alex's communication style, approval patterns)
- **Urgent timelines** ("need approval by 8am tomorrow")

**When to reference:**
- Writing strategy emails (match Alex's "easy to digest" preference)
- Making promotional decisions (understand past promo patterns)
- Explaining YoY performance changes (brand CPC increases, non-brand growth)
- Understanding approval urgency (tight implementation deadlines)

---

## Key Contact Communication Styles

### Alex Clarke
- **Decision-making:** Quick approvals when strategy is clear
- **Preference:** "Easy to digest" strategy presentations
- **Communication:** Appreciative, collaborative ("I am grateful!")
- **Timing:** Responds to urgent requests promptly
- **Data focus:** Wants YoY context, validates numbers before reporting up

### Lauryn
- **Role:** Part of Frank Smythson LTD team
- **Involvement:** In "Paid Search Catch Up" chat
- *Note: Limited messages in this import*

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
