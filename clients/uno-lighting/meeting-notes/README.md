# WhatsApp Chat Archives - UNO Lighting

**Purpose:** Store WhatsApp chat exports from UNO Google group for context and reference.

**Location:** `/clients/uno-lighting/whatsapp-chats/`

---

## Chat Groups

### 1. UNO Google
**Participants:** Peter Empson, Richard (Director), Dana (Operations Manager)
**Purpose:** Product feed management, Merchant Centre issues, budget discussions, strategic planning

---

## File Naming Convention

Format: `uno-google-group-YYYY-MM-DD.md`

Examples:
- `uno-google-group-2025-11-25.md` - Chat imported on 25 Nov 2025
- `uno-google-group-2025-12-01.md` - Next import on 1 Dec 2025

---

## Import Process

### 1. Download from WhatsApp
1. Open WhatsApp chat ("UNO Google")
2. Export chat (with or without media)
3. Save to Downloads folder
4. Extract ZIP file if needed

### 2. Before Importing - Check for Duplicates

Run this command to check if content already exists:

```bash
# Check last message in newest file
tail -20 /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/uno-google-*.md | grep -A 5 "Dana:\\|Richard:\\|Peter Empson:"

# Search for specific message content
grep -r "specific phrase from new export" /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/
```

### 3. Import New Content

**Tell Claude:**
> "Import the new UNO WhatsApp chat. Check for duplicates first. The chat export is in Downloads folder"

**Claude will:**
1. Check existing files for duplicate messages
2. Identify where previous import ended
3. Only import NEW messages since last import
4. Create new dated file with only new content

---

## Chat Archive Index

| File | Chat Group | Date Range | Key Topics | Participants |
|------|-----------|-----------|------------|-----------------|
| `uno-google-group-2025-11-25.md` | UNO Google | Mar-Nov 2025 | Product feed management, variant migrations, budget strategy, navigation redesign | Peter, Dana, Richard |

---

## Search Tips

### Find Specific Topics

```bash
# Search for product feed issues
grep -i "feed\\|merchant centre\\|gtin" /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/*.md

# Search for budget discussions
grep -i "budget\\|roas\\|spend" /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/*.md

# Search for variant/SKU issues
grep -i "variant\\|sku\\|mapping" /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/*.md

# Search for specific products
grep -i "spike light\\|trimless\\|banbury" /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/*.md

# Search for strategic discussions
grep -E "(navigation|seasonal|trade|retail)" /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/*.md
```

### View Recent Conversations

```bash
# Last 50 lines of most recent file
tail -50 /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/uno-google-group-2025-11-25.md

# All files sorted by date
ls -lt /Users/administrator/Documents/PetesBrain/clients/uno-lighting/whatsapp-chats/
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

- **Product feed management patterns** (variant migrations, SKU mapping, GTIN fixes)
- **Client communication styles** (Dana's operational focus, Richard's strategic input)
- **Recurring issues** (feed timing, disapproved products, image updates)
- **Budget philosophy** (stock-constrained growth, ROAS targeting, seasonal patterns)
- **Bestseller tracking** (which product versions perform on Google Ads)
- **Strategic recommendations** (navigation redesign, conversion optimisation)

**When to reference:**
- Planning product variant changes (learn from past SKU mapping issues)
- Budget discussions (understand seasonal patterns and ROAS approach)
- Feed management issues (see how similar problems were solved)
- Communication with Dana/Richard (match their communication preferences)
- Website navigation planning (reference September 2025 navigation document)

---

## Key Contact Communication Styles

### Dana (Operations Manager)
- **Role:** Day-to-day product feed management
- **Communication:** Responsive, appreciative, detail-oriented
- **Approach:** Asks for guidance before making changes
- **Timing:** Quick turnarounds on technical fixes
- **Technical level:** Comfortable with GTINs, SKUs, variants, Merchant Centre
- **Proactivity:** Monitors product performance, notices issues early

### Richard (Director)
- **Role:** Strategic decisions (budget, navigation, major changes)
- **Communication:** Less frequent but decisive
- **Approach:** Understands seasonal business patterns
- **Decision-making:** Willing to invest when data supports it
- **Collaboration:** Appreciative of detailed recommendations

---

## Common Issues & Resolutions

### Product Feed Issues
- **Feed timing:** Updates once daily at 2am, manual reruns available
- **Approval delays:** Usually a couple of hours, can take longer if Google re-crawls site
- **Image changes:** Rerun feed manually to pull in new images immediately

### Variant Migrations
- **Best practice:** Inform Peter before making changes
- **SKU mapping:** Keep original SKUs when consolidating products
- **Sales history:** Can be lost if not mapped correctly in Channable
- **Testing period:** New variants take a few days to kick in

### GTIN Problems
- **Validation:** Use https://www.gs1.org/services/verified-by-gs1/results
- **Multiple GTINs:** Created when variants added over time
- **Impact:** Invalid GTINs cause product disapprovals in Merchant Centre

### Bestseller Protection
- **Warning issued:** Don't delete old product versions if they're bestsellers
- **Example:** 5-pack trimless profile outperforms variant selector version
- **Reason:** Established sales history and product IDs in Google's system

---

## Strategic Context

### Dual Customer Base
- **Retail customers:** Look for room-based, type-based, style-based solutions
- **Trade customers:** Need technical/application-based navigation
- **Navigation strategy:** Blended approach with filtering options

### Seasonal Patterns
- **Peak months:** October-November
- **Low month:** December
- **Strategy:** Lower ROAS targets for seasonal uplift, raise again in December

### Performance Metrics (as of May 2025)
- **Main P Max:** £300/day budget (limited by budget)
- **Potential spend:** £540/day at same ROAS
- **Overall ROAS:** 390% (Google Ads) | 482% (overall when including all sales)
- **ROAS target:** 230% (proposed drop to 200% for seasonal uplift)

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
4. Download media files if needed (store in Downloads, reference in chat)

---

**Last Updated:** 25 November 2025
