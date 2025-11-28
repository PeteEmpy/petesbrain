# WordPress Blog Navigation Setup - Elementor Sites

**Status**: ✅ Blog page and category created  
**Note**: Menu item must be added manually in Elementor

## What Was Created

1. **Blog Archive Page**
   - **Page ID**: 507
   - **URL**: https://roksys.co.uk/google-ads-blog/
   - **Title**: "Google Ads Blog"

2. **Category Archive**
   - **Category**: "Google Ads Weekly" (ID: 5)
   - **Archive URL**: https://roksys.co.uk/category/google-ads-weekly/
   - All blog posts in this category will appear here

## Elementor Setup Instructions

Since your site uses Elementor, the navigation menu is managed through Elementor's header builder, not the standard WordPress menu system.

### Method 1: Add to Existing Menu Widget (Recommended)

1. **Add Menu Item to WordPress Menu:**
   - Go to WordPress Admin → **Appearance → Menus**
   - Select your main navigation menu
   - Click **"Add Items"** → **"Custom Links"**
   - Set:
     - **Label**: `Blog`
     - **URL**: `https://roksys.co.uk/category/google-ads-weekly/`
   - Click **"Add to Menu"**
   - Drag to desired position
   - Click **"Save Menu"**

2. **Verify in Elementor:**
   - The menu widget in your Elementor header should automatically show the new "Blog" item
   - If it doesn't appear, refresh the Elementor editor

### Method 2: Add Button Widget in Elementor Header

1. **Edit Header Template:**
   - Go to WordPress Admin → **Templates → Theme Builder**
   - Find your Header template → Click **"Edit with Elementor"**
   - Or: **Templates → Saved Templates** → Find header → **Edit**

2. **Add Blog Button:**
   - Drag a **Button** widget from Elementor panel
   - Position it where you want (usually next to other nav items)
   - Set:
     - **Text**: `Blog`
     - **Link**: `https://roksys.co.uk/category/google-ads-weekly/`
   - Style to match your existing navigation
   - Click **"Update"** to save

### Method 3: Add to Footer

- Edit Footer template in Elementor
- Add a Button or Text widget
- Link to: `https://roksys.co.uk/category/google-ads-weekly/`

## Quick Reference

- **Blog Archive URL**: https://roksys.co.uk/category/google-ads-weekly/
- **Blog Page URL**: https://roksys.co.uk/google-ads-blog/
- **Category**: "Google Ads Weekly" (ID: 5)

## Verification

1. ✅ Blog page created (ID: 507)
2. ✅ Category exists (ID: 5)
3. ⚠️ Menu item needs to be added in Elementor (see steps above)

Once you add the link in Elementor, all weekly blog posts will be accessible via the navigation menu.
