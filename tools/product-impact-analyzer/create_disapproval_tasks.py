#!/usr/bin/env python3
"""
Create Google Tasks for all client disapproval action items
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.google_tasks_client import GoogleTasksClient
from datetime import datetime, timedelta

def create_disapproval_tasks():
    """Create tasks for each client's disapproval action items"""

    client = GoogleTasksClient()

    # Get or create "Client Work" task list
    task_list_id = client.get_or_create_list("Client Work")

    if not task_list_id:
        print("Error: Could not find or create Client Work task list")
        return

    print(f"Using task list: Client Work (ID: {task_list_id})")
    print("\nCreating disapproval tasks...\n")

    # Define tasks with priority, client, title, notes, and due date
    tasks = [
        {
            "priority": "URGENT",
            "client": "Smythson",
            "title": "[URGENT] Smythson - Fix Greece Shipping Configuration (1,500 products affected)",
            "notes": """**Priority**: URGENT
**Products Affected**: ~1,500 greeting cards blocked from Greece market

**Issue**: Mismatched shipping currency for Greece
- Issue Code: missing_shipping_mismatch_of_shipping_method_and_offer_currency

**Action Items**:
1. Access Smythson Merchant Center (ID: 102535465)
2. Navigate to: Tools → Shipping and Returns
3. Check Greece shipping configuration:
   - Ensure shipping rates are configured in GBP (not EUR)
   - OR exclude Greece if not shipping there
4. Verify fix by re-checking Merchant Center status

**Additional Issues to Address**:
- Missing prices on ~100 greeting cards (check feed for blank price fields)
- Landing page errors on some products (review and fix URLs)

**Expected Impact**: Restore ~1,500 products to Shopping ads

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 3
        },
        {
            "priority": "HIGH",
            "client": "Godshot",
            "title": "[HIGH] Godshot - Fix Policy Violation Product Titles (10 products)",
            "notes": """**Priority**: HIGH
**Products Affected**: 10 premium products blocked due to title triggers

**Products & Fixes Needed**:

1. **"19-69 Miami Blue EDP" (4 variants)**
   - Issue: "Miami Blue" flagged as illegal drugs
   - Suggested Fix: "19-69 Blue Fragrance EDP 30ml"

2. **"A Matter of Concrete" Coffee**
   - Issue: "Concrete" flagged as weapons reference
   - Suggested Fix: "A Matter of Coffee - Laurina3 Varietal"

3. **"Haeckels Marine Facial Cleanser"**
   - Issue: Flagged as prescription drug
   - Suggested Fix: "Haeckels Marine Skincare Face Wash"

**Action Items**:
1. Access Godshot product feed/website
2. Update product titles as suggested above
3. Resubmit feed to Merchant Center (ID: 5291405839)
4. Request manual review if needed

**Expected Impact**: Restore 10 high-value products (fragrances/specialty coffee)

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 3
        },
        {
            "priority": "HIGH",
            "client": "BrightMinds",
            "title": "[HIGH] BrightMinds - Enable CSS for Free Listings (256 products)",
            "notes": """**Priority**: HIGH
**Products Affected**: 256 products not showing in Free Listings (Shopping tab)

**Primary Issue**: CSS not selected for Free Listings destination

**Action Items**:
1. Access BrightMinds Merchant Center (ID: 5291988198)
2. Navigate to: Growth → Manage Programs → Shopping Ads (Free Listings)
3. Select CSS provider (likely Google Shopping CSS)
4. Enable Free Listings destination for products

**Additional Issues to Fix**:
- Custom label formatting (custom_label_2_does_not_have_valid_format)
  - Review custom_label_2 field format requirements
- Landing page errors
  - Identify products with 404/500 errors and fix URLs

**Expected Impact**: Unlock free organic traffic via Shopping tab for 256 products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 3
        },
        {
            "priority": "HIGH",
            "client": "Uno Lights",
            "title": "[HIGH] Uno Lights - Fix Landing Page Errors (32 products)",
            "notes": """**Priority**: HIGH
**Products Affected**: 32 LED lighting products blocked due to landing page errors

**Issue**: Product URLs returning 404 errors when Google crawls

**Action Items**:
1. Access Uno Lights Merchant Center (ID: 513812383)
2. Export list of 32 disapproved products
3. Test each product URL for 404/500 errors
4. Common fixes:
   - Update URLs in product feed if products moved
   - Fix broken website links/redirects
   - Restore product pages if accidentally deleted
   - Check for URL encoding issues

**Expected Impact**: Restore 32 products to Shopping ads

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 6
        },
        {
            "priority": "MEDIUM",
            "client": "Accessories for the Home",
            "title": "[MEDIUM] Accessories for the Home - Fix GTINs and Body Vase Titles (39 products)",
            "notes": """**Priority**: MEDIUM
**Products Affected**: 39 products (15 GTIN issues, 24 body vases)

**Issue A: Invalid GTINs (15 products)**
- Action: Check if GTINs are correct in feed
- If no manufacturer GTIN exists, remove GTIN field entirely
- Only include GTINs for products with real barcodes

**Issue B: Body Vases Flagged as Sexual Content (24 products)**
- Policy violation: Adult content
- Action: Update titles to emphasize "home decor" or "art"
- Example: "Female Form Ceramic Vase" → "Abstract Art Ceramic Vase - Home Decor"
- Request manual review if clearly not adult content

**Merchant Center ID**: 117443871

**Expected Impact**: Restore 39 niche products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 10
        },
        {
            "priority": "MEDIUM",
            "client": "Superspace",
            "title": "[MEDIUM] Superspace - Fix Price Issues (2 products)",
            "notes": """**Priority**: MEDIUM
**Products Affected**: 2 products with price issues

**Issue**: Price mismatch or missing price

**Action Items**:
1. Access Superspace Merchant Center (ID: 645236311)
2. Identify 2 disapproved products
3. Check that prices are:
   - Present and non-zero in feed
   - Match landing page price
   - In correct currency (GBP)
4. Update feed or website to match

**Expected Impact**: Restore 2 products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 10
        },
        {
            "priority": "MEDIUM",
            "client": "Crowd Control",
            "title": "[MEDIUM] Crowd Control - Fix Price Mismatches (6 products)",
            "notes": """**Priority**: MEDIUM
**Products Affected**: 6 products with price mismatches

**Issue**: Feed price doesn't match landing page price

**Action Items**:
1. Access Crowd Control Merchant Center (ID: 563545573)
2. Identify 6 products with price mismatches
3. Compare feed price to landing page price
4. Update feed to match current website price
   - OR update website if feed price is correct

**Expected Impact**: Restore 6 products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 10
        },
        {
            "priority": "MEDIUM",
            "client": "Just Bin Bags",
            "title": "[MEDIUM] Just Bin Bags - Fix Landing Page Errors (6 products)",
            "notes": """**Priority**: MEDIUM
**Products Affected**: 6 products with landing page errors

**Issue**: Product URLs returning 404 errors

**Action Items**:
1. Access Just Bin Bags Merchant Center (ID: 181788523)
2. Export list of 6 disapproved products
3. Test each product URL for errors
4. Fix broken links, redirects, or restore missing pages

**Expected Impact**: Restore 6 products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 10
        },
        {
            "priority": "MEDIUM",
            "client": "BMPM",
            "title": "[MEDIUM] BMPM - Review Missing Shipping Issues (non-condom products)",
            "notes": """**Priority**: MEDIUM
**Products Affected**: Subset of 23 disapproved products (excluding condoms)

**Issue**: Missing shipping configuration on some products

**Note**: BMPM has 23 total disapprovals:
- Condom products (policy violation - EXPECTED, no action)
- Missing shipping (technical issue - NEEDS FIX)
- Sensitive content (expected for some products)

**Action Items**:
1. Access BMPM Merchant Center (ID: 7522326)
2. Filter disapprovals to identify missing shipping issues
3. Exclude condom-related policy violations (expected)
4. Fix shipping configuration for affected products

**Expected Impact**: Restore non-condom products with shipping issues

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 13
        },
        {
            "priority": "LOW",
            "client": "Tree2mydoor",
            "title": "[LOW] Tree2mydoor - Consider Renaming \"Shirazz\" Tree (optional)",
            "notes": """**Priority**: LOW (Optional)
**Products Affected**: 1 tree variety

**Issue**: Tree named "Shirazz" flagged as alcohol (false positive)

**Action Options**:
1. Rename to "Ornamental Tree - Shirazz Variety" to avoid trigger
2. OR leave as-is (acceptable loss - 1 product out of thousands)

**Recommendation**: Monitor only, no immediate action required

**Expected Impact**: NEGLIGIBLE

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md""",
            "due_days": 18
        }
    ]

    # Create each task
    created_count = 0
    for task_data in tasks:
        try:
            # Calculate due date
            due_date = datetime.now() + timedelta(days=task_data["due_days"])
            due_str = due_date.strftime("%Y-%m-%d")

            # Create task
            result = client.create_task(
                title=task_data["title"],
                notes=task_data["notes"],
                due_date=due_str,
                list_name="Client Work"
            )

            if result and "id" in result:
                print(f"✓ Created: {task_data['priority']} - {task_data['client']}")
                created_count += 1
            else:
                print(f"✗ Failed: {task_data['client']} - {result}")

        except Exception as e:
            print(f"✗ Error creating task for {task_data['client']}: {e}")

    print(f"\n{'='*60}")
    print(f"Created {created_count}/{len(tasks)} tasks successfully")
    print(f"{'='*60}\n")
    print("View tasks in Google Tasks:")
    print("https://tasks.google.com/")
    print("\nAction Plan Document:")
    print("/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md")


if __name__ == "__main__":
    create_disapproval_tasks()
