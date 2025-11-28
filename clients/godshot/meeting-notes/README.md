# WhatsApp Chat Archives - Godshot

**Purpose:** Store WhatsApp chat exports from Godshot for context and reference.

**Location:** `/clients/godshot/whatsapp-chats/`

---

## Chat Groups

### 1. GS - increasing web sales
**Participants:** Peter Empson, Sam Amdjadi (Director), Zoe Godshot (Operations/E-commerce Manager)
**Purpose:** Budget scaling, brand strategy, technical feed management, operational coordination

---

## File Naming Convention

Format: `gs-increasing-web-sales-YYYY-MM-DD.md`

Examples:
- `gs-increasing-web-sales-2025-11-25.md` - Chat imported on 25 Nov 2025
- `gs-increasing-web-sales-2025-12-01.md` - Next import on 1 Dec 2025

---

## Import Process

### 1. Download from WhatsApp
1. Open WhatsApp chat ("GS - increasing web sales")
2. Export chat (with or without media)
3. Save to Downloads folder
4. Extract ZIP file if needed

### 2. Before Importing - Check for Duplicates

Run this command to check if content already exists:

```bash
# Check last message in newest file
tail -30 /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/gs-increasing-*.md | grep -A 5 "Sam Amdjadi:\\|Zoe Godshot:\\|Peter Empson:"

# Search for specific message content
grep -r "specific phrase from new export" /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/
```

### 3. Import New Content

**Tell Claude:**
> "Import the new Godshot WhatsApp chat. Check for duplicates first. The chat export is in Downloads folder"

**Claude will:**
1. Check existing files for duplicate messages
2. Identify where previous import ended
3. Only import NEW messages since last import
4. Create new dated file with only new content

---

## Chat Archive Index

| File | Chat Group | Date Range | Key Topics | Participants |
|------|-----------|-----------|------------|-----------------|
| `gs-increasing-web-sales-2025-11-25.md` | GS - increasing web sales | Sept 2024-Nov 2025 | Budget scaling (£20→£130/day), brand strategy (Fellow/Anglepoise/Kinto), feed migration, Nov 20 sale (29x ROAS), 2025 planning | Peter, Sam, Zoe |

---

## Search Tips

### Find Specific Topics

```bash
# Search for budget discussions
grep -i "budget\\|roas\\|spend" /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/*.md

# Search for brand performance
grep -i "fellow\\|anglepoise\\|kinto\\|rains\\|stutterheim" /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/*.md

# Search for operational challenges
grep -i "staff\\|stretched\\|exhausting\\|store" /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/*.md

# Search for technical issues
grep -i "feed\\|gtin\\|ean\\|channable\\|wp engine" /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/*.md

# Search for strategic planning
grep -E "(turnover|forecast|planning|2025)" /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/*.md
```

### View Recent Conversations

```bash
# Last 50 lines of most recent file
tail -50 /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/gs-increasing-web-sales-2025-11-25.md

# All files sorted by date
ls -lt /Users/administrator/Documents/PetesBrain/clients/godshot/whatsapp-chats/
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

- **Budget scaling philosophy** (gradual increases, ROAS preservation)
- **Brand strategy evolution** (diversification from Fellow to multi-brand)
- **Operational reality** (physical store struggles, capacity constraints)
- **Client communication styles** (Sam's entrepreneurial transparency, Zoe's operational detail)
- **Technical challenges** (feed migrations, GTIN management, hosting issues)
- **Pricing strategy** (competitive matching, margin preservation)
- **Crisis management** (Instagram hack, staff issues, exhaustion periods)

**When to reference:**
- Budget increase discussions (understand gradual scaling approach)
- Brand expansion planning (see Fellow competitive pressure, Anglepoise success)
- Operational capacity planning (Sam/Zoe stretched to limit in peak)
- Feed management issues (Channable replacement, GTIN field discovery)
- 2025 forecasting (limited data, seasonal vs baseline performance)
- Communication with Sam/Zoe (match their transparency and detail level)

---

## Key Contact Communication Styles

### Sam Amdjadi (Director)
- **Role:** Strategic direction, brand relationships, business planning
- **Communication:** Transparent about struggles, entrepreneurial mindset
- **Decision-making:** "Only one way to find out" - test and learn approach
- **Challenges:** Exhaustion, staff issues, Instagram hacks
- **Philosophy:** Staff-free model if possible, focus vs spread
- **Timing:** Hands-on during crises (early hours on sale night)
- **Financial:** Cash flow conscious, investment-oriented

### Zoe Godshot (Operations/E-commerce Manager)
- **Role:** Day-to-day operations, product management, fulfilment
- **Communication:** Detail-oriented, technical questions
- **Workload:** "Incessant packing" - stretched capacity
- **Technical:** Learning curve on GTINs/EANs, implementing colour swatches
- **Proactivity:** Trustpilot reviews, pricing adjustments, product pages
- **Implementation:** Hands-on with website management

---

## Performance Milestones

### Budget Journey
- **Sept 5, 2024:** £20/day reactivation
- **Sept 15:** £35/day (rebuild momentum)
- **Sept 26:** £65/day (matching April performance)
- **Oct-Nov:** £79/day regular spend
- **Nov 20 Sale:** £130/day capacity
- **Target:** 700% ROAS maintained

### Key Performance Events
- **Sept 23:** Sales +42%, £405 spend, 700% ROAS
- **Nov 20 Sale:** 29x ROAS (extraordinary)
- **2024 Turnover:** ~£270k inc. VAT (with June-Aug pause)

### Brand Performance Evolution
- **Sept 2024:** Fellow-dependent
- **Oct 2024:** Diversification (Dak, Rains, 19-69, Kinto)
- **Oct 28:** Anglepoise onboarding
- **Nov 11:** Anglepoise 400%+ ROAS (separate campaign)

---

## Technical Evolution

### Feed Management
- **Sept 6:** 502 gateway errors with Channable
- **Oct 11:** Channable replaced with new system
- **Nov 19:** GTIN field discovery (2 support tickets)
- **Nov 20:** WP Engine dedicated server migration

### Data Quality Improvements
- Product title optimisation (bestsellers prioritised)
- Brand name standardisation for grouping
- Colour attribute dual-system (brand swatches + generic filter)
- EAN/GTIN ongoing addition

---

## Strategic Context

### Physical Store vs Online Dilemma
- **Current:** Sam + Zoe stretched 7 days/week
- **Challenge:** Staff = "number one problem"
- **Consideration:** Close physical store, focus online only
- **Glasgow trend:** Independent businesses open 3 days/week to avoid recruitment

### Brand Portfolio Philosophy
- **Approach:** Don't become "Amazon of higher end products"
- **Strategy:** Find products "going under the radar"
- **Build:** One product → gradual brand presence
- **Diversify:** "Better not to have all your eggs in one basket"

### Pricing & Margin
- **Philosophy:** "Go in too high rather than too low - preserve margin"
- **Method:** Test and adjust based on performance
- **Example:** Anglepoise £30 margin at £90 sale price
- **Learning:** Nov 20 sale showed extreme price sensitivity

### 2025 Planning Constraints
- **Targets:** £500k / £750k / £1m annual turnover being considered
- **Challenge:** Limited baseline data (seasonal spike in Nov/Dec)
- **Budget:** Campaigns were budget-limited during peak
- **Operational:** Can they fulfill higher volumes?

---

## Crisis Events Timeline

### Instagram Hacks
- **Previous:** Lost account with 40k followers
- **Nov 20, 2024:** 12,000 follower account hacked/ransomed
- **Impact:** "Contemplated just stopping everything"
- **Timing:** During critical sale event planning

### Operational Crises
- **Sept 2024:** Disgruntled ex-employee negative review campaign (legal action)
- **Oct 2024:** COVID during peak period
- **Oct 2024:** Blocked drain at shop
- **General:** Exhaustion - "we have days when we just want to stop"

---

## Common Issues & Solutions

### GTIN/EAN Management
- **Challenge:** Difficult to extract from Lightspeed/WooCommerce
- **Solution:** PDF spreadsheet format (item_id + EAN columns)
- **Importance:** Critical for competitive products (Anglepoise)
- **Tool:** https://search.google.com/test/rich-results for validation

### Fellow Brand Challenges
- **Issue:** Increased competition, lower ROAS targets from competitors
- **Impact:** Overstocked position
- **Context:** Amazon sales stopped by Fellow
- **Response:** Diversification strategy

### Feed Management
- **Channable:** Replaced after month of 502 errors
- **Discovery:** GTIN field required 2 support tickets to locate
- **Optimisation:** Product titles (bestsellers first)
- **Brand grouping:** Requires "brand" field populated

### Operational Capacity
- **Peak stress:** Nov 20 sale (worked till early hours)
- **Christmas:** Zoe needs break from "incessant packing" mid-Jan
- **Solution:** Training additional person to support Zoe

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
