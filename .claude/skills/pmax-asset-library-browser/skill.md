# PMax Asset Library Browser Skill

**Type:** Execution
**Priority:** P0
**Effort:** 30 minutes
**Use:** Browse Google Ads Performance Max image assets by category

---

## What This Skill Does

Opens an interactive browser interface showing all image assets from a Google Ads account, organised by auto-detected categories with:
- Visual grid view with click-to-copy Asset IDs
- Category grouping (Bags, Diaries, Seasonal, etc.)
- Usage tracking (where each image is currently used)
- Searchable and filterable interface

---

## When to Use

User says:
- "Browse asset library for [client]"
- "Show me [client]'s images"
- "Open asset library browser"
- "Find images for [client]"
- "What images does [client] have?"

---

## Execution

The skill will:

1. Identify the client and retrieve their Google Ads customer ID from CONTEXT.md
2. Run the universal asset library browser script with the customer ID
3. Generate and open an HTML page showing all images organised by category
4. Display images with their Asset IDs, dimensions, and current usage

---

## Inputs Required

- **Client name** (e.g., "Smythson", "Tree2MyDoor")

---

## What Gets Created

- HTML file in `/Users/administrator/Documents/PetesBrain/output/`
- Format: `asset-library-browser-{customer_id}-{date}.html`
- Automatically opened in browser

---

## Key Features

**Category Auto-Detection:**
- Bags, Notebooks & Diaries, Wallets, Tech Accessories, Plants & Nature, etc.
- Based on asset filenames and patterns

**Interactive Interface:**
- Click any Asset ID to copy to clipboard
- Search by ID, name, or dimensions
- Filter by usage (used/unused)
- Expand/collapse categories

**Usage Tracking:**
- Shows which campaigns/asset groups use each image
- Highlights unused images
- Usage count badges

---

## Technical Details

**Script Location:** `/Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py`

**Customer ID Source:** Client CONTEXT.md files contain Google Ads customer IDs

**API Queries:**
- Fetches all IMAGE assets from account
- Queries asset group usage for Performance Max campaigns
- Retrieves dimensions, URLs, and metadata

---

## Example Usage

**User:** "Browse asset library for Smythson"

**Skill Actions:**
1. Read `/Users/administrator/Documents/PetesBrain/clients/smythson/documents/CONTEXT.md`
2. Extract customer ID: `8573235780` and manager ID: `2569949686`
3. Execute: `python3 /Users/administrator/Documents/PetesBrain/shared/scripts/google-ads-asset-library-browser.py --customer-id 8573235780 --manager-id 2569949686`
4. HTML page generated and opened in browser

---

## Error Handling

**Missing customer ID:** Inform user and ask which account to browse
**API errors:** Report authentication or permission issues
**No images found:** Inform user the account has no image assets

---

## Related Skills

- `google-ads-text-asset-exporter` - Export text assets from PMax campaigns
- `google-ads-campaign-audit` - Audit campaign structure and settings

---

## Benefits

- **Fast image discovery** - Visual browsing vs manual Google Ads UI
- **Easy Asset ID copying** - Click to copy for spreadsheets
- **Usage visibility** - Identify unused assets for cleanup
- **Category organisation** - Find images by product type
