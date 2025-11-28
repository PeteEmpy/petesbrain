# Blog Post Styling Guide

## Current Approach

**WordPress Theme Styling** (Default)
- Posts use your WordPress theme's default blog post styles
- No custom CSS added
- Clean semantic HTML structure
- Theme handles all visual formatting

## HTML Structure Generated

The script generates clean semantic HTML:

```html
<h2>Main Section Heading</h2>
<p>Paragraph text with <strong>emphasis</strong> and <a href="url">links</a>.</p>

<h3>Subsection Heading</h3>
<p>More content...</p>

<ul>
  <li>Bullet point one</li>
  <li>Bullet point two</li>
</ul>
```

## Your Brand Colors

From `CLAUDE.md`:
- **Roksys Green**: #6CC24A
- **Roksys Gray**: #808080

## Styling Options

### Option 1: Theme Default (Current)
✅ **Pros:**
- Matches rest of your site automatically
- No maintenance needed
- Consistent with existing blog posts

❌ **Cons:**
- No control over specific styling
- Depends on theme quality

### Option 2: Custom CSS Block
Add a custom CSS block to each post:

```html
<style>
h2 { color: #6CC24A; border-bottom: 2px solid #6CC24A; padding-bottom: 10px; }
h3 { color: #808080; margin-top: 20px; }
a { color: #6CC24A; }
a:hover { text-decoration: underline; }
</style>
```

### Option 3: WordPress Custom CSS
Add CSS to WordPress → Appearance → Customize → Additional CSS

```css
.post-content h2 {
    color: #6CC24A;
    border-bottom: 2px solid #6CC24A;
    padding-bottom: 10px;
}

.post-content h3 {
    color: #808080;
    margin-top: 20px;
}

.post-content a {
    color: #6CC24A;
}
```

## Recommendation

**Start with Option 1 (Theme Default)**
- See how posts look with your current theme
- If styling needs improvement, add Option 3 (WordPress Custom CSS)
- This applies to all posts, not just automated ones

## Example Output Structure

A typical post will look like:

```html
<h2>Performance Max Gets Bigger</h2>
<p>I've been keeping an eye on Performance Max developments this week, and there's some interesting news...</p>

<h3>Waze Integration</h3>
<p>Google's expanded Performance Max to include Waze ads. Here's what that means for your campaigns...</p>

<h3>B2B Adoption</h3>
<p>More B2B brands are shifting from keyword-only strategies to Performance Max...</p>

<h2>What This Means for Advertisers</h2>
<p>Plain and simple, if you're not already testing Performance Max, now's the time...</p>
```

WordPress will style these elements according to your theme's CSS.

