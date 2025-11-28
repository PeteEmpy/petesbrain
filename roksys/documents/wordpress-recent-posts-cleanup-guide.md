# WordPress Recent Posts Sidebar - Cleanup Guide

**Created:** 2025-11-20
**Issue:** Recent Posts widget showing 3 lines per post (messy, hard to read)
**Solution:** Custom CSS to make it compact and readable

---

## Quick Fix Instructions

### Step 1: Access WordPress Customizer
1. Log in to WordPress admin: `https://roksys.co.uk/wp-admin`
2. Go to **Appearance → Customize**
3. Scroll down and click **Additional CSS**

### Step 2: Add Custom CSS
1. Open the CSS file: `roksys/documents/wordpress-recent-posts-css.css`
2. Copy all the CSS code
3. Paste it into the **Additional CSS** box in WordPress Customizer
4. Click **Publish** to save

### Step 3: Verify
1. Visit your blog page: `https://roksys.co.uk/category/google-ads-weekly/`
2. Check the "Recent Posts" sidebar on the right
3. Each post should now be much more compact

---

## What This CSS Does

**Before:**
```
┌─────────────────────────────────┐
│ Long Article Title That Wraps  │
│ to Multiple Lines               │
│ November 18, 2025               │  ← 3 lines per post
└─────────────────────────────────┘
```

**After:**
```
┌─────────────────────────────────┐
│ Long Article Title              │
│ Nov 18, 2025                    │  ← 2 lines, much cleaner
├─────────────────────────────────┤  ← Separator line
│ Next Article Title              │
│ Nov 17, 2025                    │
└─────────────────────────────────┘
```

**Changes:**
- ✅ Smaller, tighter line spacing
- ✅ Dates are smaller and lighter grey
- ✅ Separator lines between posts
- ✅ Cleaner hover effect (Roksys green)
- ✅ Excerpts hidden (if they were showing)
- ✅ Better title wrapping

---

## Ultra-Compact Option

If you want even **more** compact (hide dates completely):

1. Find the "ULTRA-COMPACT VERSION" section in the CSS
2. Uncomment it by removing the `/*` and `*/` markers
3. This will hide dates and make it even tighter (1 line per post)

**Ultra-compact result:**
```
┌─────────────────────────────────┐
│ Article Title One               │
├─────────────────────────────────┤
│ Article Title Two               │
├─────────────────────────────────┤
│ Article Title Three             │
└─────────────────────────────────┘
```

---

## Customization Options

### Change the separator line color:
```css
border-bottom: 1px solid #YOUR_COLOR;
```

### Change the hover color (currently Roksys green):
```css
color: #6CC24A; /* Change this hex code */
```

### Adjust spacing between posts:
```css
margin-bottom: 8px !important;  /* Make larger for more space */
padding-bottom: 8px !important; /* Make larger for more space */
```

---

## File Location

**CSS File:** `/Users/administrator/Documents/PetesBrain/roksys/documents/wordpress-recent-posts-css.css`

**Backup:** This CSS is version-controlled in the PetesBrain repository, so you can always retrieve it if needed.

---

## Support

If you need adjustments to spacing, colors, or styling, just ask and I can update the CSS file for you.
