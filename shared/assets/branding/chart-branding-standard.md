# Roksys Chart & Visualization Branding Standard

**Version**: 1.0
**Last Updated**: 2025-11-03
**Applies To**: Matplotlib charts, data visualizations, graphs, and analytical reports

---

## Overview

This document defines how Roksys branding should be subtly incorporated into data visualizations, charts, and analytical reports created for clients.

**Guiding Principle**: Branding should be **professional and subtle** - visible enough to establish ownership but never overpowering the data.

---

## Standard Elements

### 1. Logo Placement

**Position**: Bottom-right corner
**Size**: Small, unobtrusive (typically 80-120px wide)
**Opacity**: 60-80% to ensure subtlety
**Padding**: 10-15px from edges

**Matplotlib Implementation**:
```python
from PIL import Image
import matplotlib.pyplot as plt

# Load logo
logo = Image.open('/Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png')

# Add to figure (bottom-right, subtle)
fig.figimage(logo,
             xo=fig.bbox.xmax - logo.width - 20,  # 20px from right
             yo=20,  # 20px from bottom
             alpha=0.7,  # 70% opacity
             zorder=1)
```

### 2. Footer Text Attribution

**Position**: Bottom-center or bottom-right
**Text Format**: `"Report by Rok Systems (roksys.co.uk)"`
**Font Size**: 9-10pt
**Color**: `#999999` (light gray) or `#6CC24A` (Roksys Green for emphasis)
**Style**: Italic

**Matplotlib Implementation**:
```python
fig.text(0.99, 0.01,
         'Report by Rok Systems (roksys.co.uk)',
         ha='right', va='bottom',
         fontsize=9,
         color='#999999',
         style='italic')
```

### 3. Color Accent (Optional)

For data visualizations, consider using **Roksys Green** (`#6CC24A`) as one of the accent colors in the chart palette, especially for:
- Highlighting current year data
- Emphasizing positive trends
- Key data points or markers

**Do NOT** make the entire chart green - use it sparingly as one color in a diverse palette.

---

## Implementation Levels

### Level 1: Minimal (Default for Client Reports)

**Elements**:
- Footer text attribution only
- No logo

**When to Use**: Most client-facing analytical reports where data clarity is paramount

**Example**:
```python
fig.text(0.99, 0.01,
         'Analysis by Rok Systems | roksys.co.uk',
         ha='right', va='bottom',
         fontsize=9, color='#999999', style='italic')
```

### Level 2: Standard (Public/Shareable Reports)

**Elements**:
- Footer text attribution
- Small logo in bottom-right corner (70% opacity)

**When to Use**: Reports that may be shared publicly or used in presentations

**Example**: See "Standard Template" section below

### Level 3: Branded (Marketing/Portfolio Pieces)

**Elements**:
- Logo at top-center or top-right
- Footer text and logo
- Roksys Green accent color in chart
- "Prepared by Rok Systems" subtitle

**When to Use**: Case studies, portfolio pieces, marketing materials

---

## Standard Template (Level 2)

```python
#!/usr/bin/env python3
"""
Standard Roksys-branded chart template
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams
from PIL import Image
from pathlib import Path

# Roksys styling
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# Create figure
fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
fig.patch.set_facecolor('white')

# ... [Your chart code here] ...

# Add Roksys branding (Level 2)
def add_roksys_branding(fig, level=2):
    """Add Roksys branding to matplotlib figure"""

    if level >= 1:
        # Footer text
        fig.text(0.99, 0.01,
                'Report by Rok Systems (roksys.co.uk)',
                ha='right', va='bottom',
                fontsize=9, color='#999999', style='italic')

    if level >= 2:
        # Logo (bottom-right)
        logo_path = Path('/Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png')
        if logo_path.exists():
            logo = Image.open(logo_path)
            # Scale logo to reasonable size (60% of original)
            new_width = int(logo.width * 0.6)
            new_height = int(logo.height * 0.6)
            logo_resized = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Position in bottom-right
            fig.figimage(logo_resized,
                        xo=fig.bbox.xmax - new_width - 15,
                        yo=15,
                        alpha=0.7,
                        zorder=1)

# Apply branding
add_roksys_branding(fig, level=2)

# Save
plt.tight_layout(pad=1.5)
plt.savefig('output.png', dpi=150, bbox_inches='tight')
```

---

## Color Palette Recommendations

When creating multi-line or multi-series charts, use these palettes:

### Professional Palette (Default)
```python
colors = [
    '#0066CC',  # Strong Blue
    '#FF6B35',  # Vibrant Orange
    '#2ECC71',  # Bright Green (close to Roksys Green)
    '#9B59B6',  # Rich Purple
    '#E74C3C',  # Red
    '#F39C12',  # Amber
]
```

### Roksys-Influenced Palette
```python
colors = [
    '#6CC24A',  # Roksys Green (primary)
    '#0066CC',  # Blue
    '#FF6B35',  # Orange
    '#9B59B6',  # Purple
    '#34495E',  # Dark Gray
]
```

**Note**: Use Roksys Green as the **first or most prominent** color when you want to emphasize company branding.

---

## Typography Standards

Match the Roksys typography guidelines:

```python
# Title styling
ax.set_title('Your Chart Title',
             fontsize=20, fontweight='700',  # Bold
             color='#333333',  # Dark gray (or #6CC24A for branded)
             pad=25)

# Axis labels
ax.set_xlabel('X Axis', fontsize=14, fontweight='600')
ax.set_ylabel('Y Axis', fontsize=14, fontweight='600')

# Tick labels
ax.tick_params(labelsize=11, colors='#333333')
```

---

## Examples

### Example 1: NDA Enrolments Chart (Level 1 - Minimal)

Current implementation in `create-monthly-comparison-chart.py`:
- Footer text: ✅ "National Design Academy | Enrolment Analysis"
- Logo: ❌ Not included (appropriate for client data analysis)
- Branding Level: **1 (Minimal)** - Correct for this use case

### Example 2: Portfolio Case Study Chart (Level 3 - Branded)

Would include:
- Logo at top-right
- Title with "Prepared by Rok Systems" subtitle
- Roksys Green accent color for key data series
- Footer with logo and text
- Branding Level: **3 (Branded)**

---

## File Locations

**Logo**: `/Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png`
**Brand Guidelines**: `/Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-brand-guidelines.md`
**This Document**: `/Users/administrator/Documents/PetesBrain/shared/assets/branding/chart-branding-standard.md`

---

## Decision Matrix

| Chart Type | Audience | Branding Level |
|------------|----------|----------------|
| Client internal analysis | Client only | Level 1 (Minimal) |
| Client reports (PDF/email) | Client + stakeholders | Level 2 (Standard) |
| Public case studies | Public/prospects | Level 3 (Branded) |
| Internal analysis | Roksys team | Level 1 (Minimal) |
| Pitch deck visualizations | Prospects | Level 3 (Branded) |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-03 | 1.0 | Initial chart branding standard created |

---

**Maintained By**: Rok Systems (Roksys)
**Contact**: https://roksys.co.uk
