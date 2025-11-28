# Weekly Google Ads Blog Post Generator

**Automated WordPress blog post generation from knowledge base articles**

## Overview

This system automatically generates and publishes weekly blog posts to your WordPress site (roksys.co.uk) based on recent Google Ads articles from your knowledge base. Posts are written in your tone of voice and target existing or future Rok Systems customers.

**Runs:** Every Monday at 7:30 AM  
**Publishes:** Every Monday at 9:00 AM (scheduled)

**Last Updated:** November 9, 2025

---

## Target Audience

Blog articles are written for **EXISTING OR FUTURE CUSTOMERS OF ROK SYSTEMS** who:
- Run e-commerce businesses (online stores on Shopify, WooCommerce, Magento, etc.)
- Sell products online and use (or are considering) Google Ads
- Want to understand what Google Ads changes mean for their business in the real world
- Need to understand the world of Google Ads and what's happening in it
- Are not necessarily PPC experts - they need clear, straightforward guidance

---

## How It Works

### 1. Content Collection
- Pulls top 5-7 Google Ads articles from knowledge base (last 7 days)
- Filters for relevant content (Google Ads, PPC, Performance Max, etc.)
- Sorts by date (newest first)

### 2. Content Generation
- Uses Claude API to synthesize articles into a weekly blog post
- Writes in your tone of voice (from `roksys-website-content.md`)
- Translates technical Google Ads information into real-world business impact
- First-person, conversational style
- British English spelling
- 800-1200 words

### 3. WordPress Publishing
- Creates WordPress post via REST API
- Sets category: "Google Ads Weekly"
- Sets tags: "Google Ads", "PPC", "Industry News", "Paid Search"
- Schedules for Monday 9 AM publication
- Auto-creates categories/tags if they don't exist

---

## Content Approach

### Writing Style
- **First-person**: "I've been watching...", "Here's what caught my attention...", "Let me tell you about..."
- **Conversational and straightforward**: "plain and simple" (matches website tone)
- **Experienced but approachable**: Business partner approach, not just vendor
- **Personal**: "you get me" approach from the website
- **Translates technical to practical**: Explains what Google Ads changes mean for their business in the real world
- **Natural business focus**: Customers view things from a profitability/business outcome angle, but translate that naturally - don't force "profitability" language into every article

### Content Focus
- Tell them about the world of Google Ads
- Explain what's changed recently in Google Ads news
- Translate technical changes into what they mean for their e-commerce business in the real world
- Focus on "what does this actually mean for them?" - translate technical to practical
- Maintain flow and continuity - these are regular weekly articles

### Post Structure
- **Opening**: Brief intro about what's happening this week in Google Ads that matters to their business (2-3 sentences, conversational)
- **Main sections**: 3-5 key developments from articles
- **Each section**:
  - What happened in the world of Google Ads
  - Translate it into what it means for their e-commerce business in the real world
  - What does this actually mean for them? (translate technical to practical)
  - What it means going forward for their business
- **Closing**: Brief summary tying it all together and forward-looking statement about what to watch for

---

## Usage

### Generate New Blog Post

```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="Peter"
export WORDPRESS_APP_PASSWORD="your_password"
export ANTHROPIC_API_KEY="your_api_key"
python3 agents/content-sync/weekly-blog-generator.py
```

### Update Existing Blog Post

To regenerate and update the most recent blog post:

```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="Peter"
export WORDPRESS_APP_PASSWORD="your_password"
export ANTHROPIC_API_KEY="your_api_key"
python3 agents/content-sync/weekly-blog-generator.py --update
```

This will:
1. Find the most recent blog post (scheduled or published)
2. Regenerate content with current criteria
3. Update the existing post with new content
4. Preserve post status and scheduled date if applicable

---

## Setup Instructions

### Step 1: Get WordPress Application Password

1. Log into WordPress admin: `https://roksys.co.uk/wp-admin`
2. Go to **Users → Your Profile**
3. Scroll down to **Application Passwords**
4. Enter name: "Weekly Blog Generator"
5. Click **Add New Application Password**
6. **Copy the password immediately** (you can only see it once!)

### Step 2: Configure Environment Variables

Edit the LaunchAgent plist file:
```bash
nano ~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist
```

Update these values:
```xml
<key>WORDPRESS_URL</key>
<string>https://roksys.co.uk</string>
<key>WORDPRESS_USERNAME</key>
<string>your_wordpress_username</string>
<key>WORDPRESS_APP_PASSWORD</key>
<string>your_application_password_here</string>
```

### Step 3: Install LaunchAgent

```bash
# Copy plist to LaunchAgents directory
cp agents/launchagents/com.petesbrain.weekly-blog-generator.plist ~/Library/LaunchAgents/

# Load the agent
launchctl load ~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist

# Verify it's loaded
launchctl list | grep weekly-blog
```

### Step 4: Test Manually

Run the script manually to test:
```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="your_username"
export WORDPRESS_APP_PASSWORD="your_password"
export ANTHROPIC_API_KEY="your_api_key"
python3 agents/content-sync/weekly-blog-generator.py
```

Check the log:
```bash
tail -f ~/.petesbrain-weekly-blog.log
```

---

## Post Format

**Title:** "Google Ads Weekly: [Date]"

**Length:** 800-1200 words

**Format:** HTML, semantic markup (h2, h3, p, ul, li, a, strong)

---

## Troubleshooting

### "No recent articles found"
- Check that knowledge base index is up to date: `python3 agents/content-sync/knowledge-base-indexer.py`
- Verify articles exist in knowledge base from last 7 days

### "WordPress API returned 401"
- Check Application Password is correct
- Verify username is correct
- Ensure Application Passwords are enabled in WordPress

### "WordPress API returned 403"
- Check user has permission to publish posts
- Verify REST API is enabled (should be by default)

### Post not appearing
- Check WordPress post is scheduled (not published immediately)
- Look in WordPress admin → Posts → Scheduled
- Check log file: `~/.petesbrain-weekly-blog.log`

---

## Files

- **Script:** `agents/content-sync/weekly-blog-generator.py`
- **LaunchAgent:** `agents/launchagents/com.petesbrain.weekly-blog-generator.plist`
- **Tone Reference:** `roksys/roksys-website-content.md`
- **Log:** `~/.petesbrain-weekly-blog.log`
- **Draft Backup:** `shared/data/blog-draft-YYYYMMDD.html` (if WordPress publish fails)
- **Skill:** `.claude/skills/blog-article-generator/` - Claude skill for blog generation

---

## Customization

### Change Schedule
Edit the LaunchAgent plist:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key>
    <integer>1</integer>  <!-- 0=Sunday, 1=Monday, etc. -->
    <key>Hour</key>
    <integer>7</integer>
    <key>Minute</key>
    <integer>30</integer>
</dict>
```

### Change Post Length
Edit `weekly-blog-generator.py`:
```python
LENGTH: 800-1200 words  # Change this in the prompt
```

### Change Category/Tags
Edit `weekly-blog-generator.py`:
```python
BLOG_CATEGORY = "Google Ads Weekly"
BLOG_TAGS = ["Google Ads", "PPC", "Industry News", "Paid Search"]
```

---

## Status

✅ Script created  
✅ LaunchAgent configured and running  
✅ WordPress credentials configured  
✅ Blog generator runs automatically every Monday 7:30 AM  
✅ Posts publish automatically every Monday 9:00 AM  
✅ Update functionality added (`--update` flag)  
✅ Skill created for easy blog generation  
✅ Content approach refined (November 9, 2025)

**Current Configuration:**
- Target audience: Existing or future Rok Systems customers
- Content focus: Translate technical Google Ads info into real-world business impact
- Writing style: Natural, conversational, business-focused (without forcing profitability language)
- Regular weekly articles with flow and continuity

Posts publish automatically every Monday!
