# Roksys Brand Guidelines

## Company Information

**Full Name**: Rok Systems
**Common Name/Abbreviation**: Roksys
**Tagline**: Digital Marketing
**Website**: https://roksys.co.uk

---

## Color Palette

### Primary Colors

**Roksys Green** (Primary)
- Hex: `#6CC24A`
- RGB: `rgb(108, 194, 74)`
- Usage: Primary headings, buttons, key highlights, gradients

**Roksys Gray** (Secondary)
- Hex: `#808080`
- RGB: `rgb(128, 128, 128)`
- Usage: Secondary text, subtle badges, "ROK" in logo

### Accent Colors

**Dark Green** (Accent)
- Hex: `#5CB85C`
- RGB: `rgb(92, 184, 92)`
- Usage: Gradient end points, hover states, darker sections

**White** (Background)
- Hex: `#FFFFFF`
- RGB: `rgb(255, 255, 255)`
- Usage: Backgrounds, contrast

**Light Gray** (Neutral)
- Hex: `#F8F9FA`
- RGB: `rgb(248, 249, 250)`
- Usage: Section backgrounds, subtle containers

### Highlight Colors (Use Sparingly)

**Warning Yellow** (Alerts/Highlights)
- Hex: `#FFC107`
- RGB: `rgb(255, 193, 7)`
- Usage: Important callouts, dominant badges

**Success Green** (Positive Metrics)
- Hex: `#28A745`
- RGB: `rgb(40, 167, 69)`
- Usage: Can substitute with primary Roksys Green

---

## Typography

**Primary Font Stack**:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
```

**Headings**:
- Color: `#6CC24A` (Roksys Green)
- Font Weight: 600-700 (semi-bold to bold)

**Body Text**:
- Color: `#333` (dark gray)
- Font Weight: 400 (normal)

**Secondary Text**:
- Color: `#666` (medium gray)
- Font Weight: 400

---

## Logo Usage

### Logo Files

**Primary Logo**: `roksys-logo-200x50.png`
- Dimensions: 200px × 50px
- Format: PNG with transparency
- Location: `/shared/assets/branding/roksys-logo-200x50.png`

### Logo Placement Guidelines

**Header Placement**:
- Position: Centered at top of document
- Margin Bottom: 30px minimum
- Background: White or light gray

**Footer Placement**:
- Position: Centered at bottom
- Margin Top: 20px minimum
- Background: White or light gray

**HTML Implementation**:
```html
<img src="../../shared/assets/branding/roksys-logo-200x50.png"
     alt="Rok Systems (Roksys) - Digital Marketing"
     style="margin-bottom: 30px;">
```

---

## Gradients

### Primary Gradient (Green)
```css
background: linear-gradient(135deg, #6CC24A 0%, #5CB85C 100%);
```
**Usage**: Hero sections, important highlights, call-to-action areas

### Secondary Gradient (Horizontal Bar Charts)
```css
background: linear-gradient(90deg, #6CC24A 0%, #5CB85C 100%);
```
**Usage**: Progress bars, chart fills, horizontal elements

---

## Component Styles

### Badges

**Primary Badge** (Campaign/Category):
```css
.badge-primary {
    background: #808080;
    color: white;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: 600;
}
```

**Date Badge** (Dates/Timestamps):
```css
.badge-date {
    background: #6CC24A;
    color: white;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: 600;
}
```

**Dominant Badge** (Highlights):
```css
.badge-dominant {
    background: #FFC107;
    color: #333;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
}
```

### Cards

```css
.card {
    background: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}
```

### Tables

**Table Headers**:
```css
thead tr {
    background: #6CC24A;
    color: white;
}
```

**Total/Summary Rows**:
```css
.table-total-row {
    background: #6CC24A;
    color: white;
    font-weight: bold;
}
```

---

## Document Structure

### Standard Header

```html
<div class="header">
    <img src="../../shared/assets/branding/roksys-logo-200x50.png"
         alt="Rok Systems (Roksys) - Digital Marketing"
         style="margin-bottom: 30px;">
    <h1>[Report Title]</h1>
    <p class="subtitle">[Report Subtitle]</p>
    <span class="campaign-badge">[Campaign Name]</span>
    <span class="date-badge">[Date Range]</span>
</div>
```

### Standard Footer

```html
<div class="footer">
    <img src="../../shared/assets/branding/roksys-logo-200x50.png"
         alt="Rok Systems (Roksys) - Digital Marketing"
         style="margin-bottom: 20px;">
    <p>
        <strong>Data Source:</strong> [Data source details]<br>
        [Additional metadata]<br>
        Generated: [Date] | Report by <strong style="color: #6CC24A;">Rok Systems</strong> (<a href="https://roksys.co.uk" style="color: #6CC24A;">roksys.co.uk</a>)
    </p>
</div>
```

---

## Usage Examples

### Example 1: Section Headers
```css
h2 {
    color: #6CC24A;
    font-size: 2.2em;
    margin-bottom: 30px;
}
```

### Example 2: Highlight Sections
```css
.highlight-section {
    background: linear-gradient(135deg, #6CC24A 0%, #5CB85C 100%);
    border-radius: 15px;
    padding: 40px;
    color: white;
}
```

### Example 3: Key Insights Box
```css
.key-insight {
    background: #d4edda;
    border-left: 4px solid #6CC24A;
    padding: 20px;
    border-radius: 8px;
}
```

---

## Don'ts

❌ **Don't** use blue colors (old branding - replaced by green)
❌ **Don't** stretch or distort the logo
❌ **Don't** place logo on busy backgrounds
❌ **Don't** use neon or overly saturated greens
❌ **Don't** mix Roksys green with conflicting color schemes

---

## Files & Locations

**Brand Assets Directory**: `/Users/administrator/Documents/PetesBrain/shared/assets/branding/`

**Files**:
- `roksys-logo-200x50.png` - Primary logo (200×50px)
- `roksys-brand-guidelines.md` - This document

**Original Logo Location**: `/Users/administrator/Documents/Documents - iMac/** Rok Systems/Logo/`

---

## Standard HTML Report Header (November 2025)

**APPROVED STANDARD** - Use this for all HTML reports unless client-specific branding overrides.

### Header Styling

```css
.header {
    background: linear-gradient(135deg, #2d5016 0%, #1a3009 100%);
    color: #ffffff;
    padding: 30px;
    margin: -40px -40px 30px -40px;
    position: relative;
}

.logo {
    position: absolute;
    top: 20px;
    right: 30px;
    width: 120px;
    background: white;
    padding: 5px;
    border-radius: 4px;
}

h1 {
    margin: 0 0 15px 0;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.meta {
    font-size: 12px;
    color: #ffffff;
    opacity: 1;
    font-weight: 500;
}
```

### Logo Path (Use Absolute Path)

```html
<img src="file:///Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png"
     alt="Roksys Logo"
     class="logo">
```

**Key Features:**
- ✅ Dark green gradient background (#2d5016 to #1a3009) for excellent text contrast
- ✅ Pure white text (#ffffff) with text shadow for readability
- ✅ Logo on white background in top-right corner
- ✅ Absolute file path for logo (works from any folder depth)
- ✅ Professional, high-contrast appearance suitable for client-facing documents

**When to Override:**
- Client has specific branding requirements (e.g., white papers, co-branded documents)
- Document type requires different styling (e.g., invoices, contracts)
- Explicit instruction to use alternative branding

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-30 | 1.0 | Initial brand guidelines created |
| 2025-11-18 | 2.0 | Added standard HTML report header with dark green gradient |

---

**Last Updated**: 2025-11-18
**Maintained By**: Rok Systems (Roksys) - https://roksys.co.uk
