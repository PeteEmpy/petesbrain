---
name: blog-article-generator
description: Generates new blog articles for roksys.co.uk WordPress site from recent knowledge base articles with e-commerce focus. Use when user says "generate blog article", "create blog post", "write blog article", or wants to create WordPress blog content.
allowed-tools: Bash, Read, Write
---

# Blog Article Generator Skill

**Capabilities**:
- Generate new blog posts from EXTERNAL NEWS SOURCES ONLY (Search Engine Journal, Marketing Dive)
- Update existing blog posts with new content
- Target existing or future Rok Systems customers specifically
- Write in Peter's tone of voice (first-person, conversational, British English, "you get me" approach)
- Focus on profitability and money-making potential
- Explain the world of Google Ads and recent changes
- Show how changes affect e-commerce business profitability
- Maintain flow and continuity for regular weekly articles
- Publish to WordPress or schedule for future publication
- **CRITICAL**: NEVER uses knowledge base (contains client-specific information)

**Target Audience**:
Blog articles are written for **EXISTING OR FUTURE CUSTOMERS OF ROK SYSTEMS** who:
- Run e-commerce businesses (online stores on Shopify, WooCommerce, Magento, etc.)
- Sell products online and use (or are considering) Google Ads
- Want to understand how Google Ads changes affect their profitability
- Need to understand the world of Google Ads and what's happening in it
- Are interested in how changes impact their business revenue and profitability going forward
- Are not necessarily PPC experts - they need clear, straightforward guidance

**Content Focus**:
- Tell them about the world of Google Ads
- Explain what's changed recently in Google Ads news
- Translate technical changes into what they mean for their e-commerce business in the real world
- Focus on what it actually means for them - what does this mean for their business?
- Remember: customers view things from a profitability/business outcome angle, but translate that naturally without forcing "profitability" language into every article
- Forward-looking perspective on what changes mean for their business

**Important**: Articles are written as regular weekly content with flow and continuity, maintaining Rok Systems' tone of voice from the website.

**Script Location**:
- **Main Script**: `agents/weekly-blog-generator/weekly-blog-generator.py`
- **Working Directory**: `/Users/administrator/Documents/PetesBrain`

**How to Use**:

### Generate New Blog Post

```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="Peter"
export WORDPRESS_APP_PASSWORD="qxxA8shXiVJtD9tlI0RY0Rvf"
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
python3 agents/weekly-blog-generator/weekly-blog-generator.py
```

### Update Existing Blog Post

To regenerate and update the most recent blog post:

```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="Peter"
export WORDPRESS_APP_PASSWORD="qxxA8shXiVJtD9tlI0RY0Rvf"
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
python3 agents/weekly-blog-generator/weekly-blog-generator.py --update
```

**What Happens**:

1. **Fetches Recent Articles**: Pulls from EXTERNAL NEWS SOURCES ONLY (Search Engine Journal, Marketing Dive RSS feeds - NO knowledge base)
2. **Generates Content**: Uses Claude API to synthesize articles into a blog post
3. **E-Commerce Focus**: Writes for online retailers, explains technical terms, focuses on business outcomes
4. **Tone of Voice**: First-person, conversational, British English, relationship-focused
5. **Publishes**: Creates new WordPress post or updates existing one

**CRITICAL SAFETY RULE**: The blog generator ONLY uses external public news sources. It NEVER uses the knowledge base because the knowledge base contains client-specific information (emails, meeting notes, strategies) that must NEVER appear in public blog posts.

**Blog Post Details**:

- **Title Format**: "Google Ads Weekly: [Date]"
- **Length**: 800-1200 words
- **Category**: "Google Ads Weekly" (ID: 5)
- **Tags**: "Google Ads", "PPC", "Industry News", "Paid Search"
- **Status**: Scheduled for Monday 9 AM (or published immediately if updating)
- **Format**: HTML, semantic markup (h2, h3, p, ul, li, a, strong)

**Content Structure**:

1. **Opening**: Brief intro about what's happening this week in Google Ads that matters to their business (conversational, 2-3 sentences)
2. **Main Sections**: 3-5 key developments from articles
3. **Each Section**: 
   - What happened in the world of Google Ads
   - Translate it into what it means for their e-commerce business in the real world
   - What does this actually mean for them? (translate technical to practical)
   - What it means going forward for their business
4. **Closing**: Brief summary tying it all together and forward-looking statement about what to watch for

**Writing Style**:

- First-person ("I've been watching...", "Here's what caught my attention...", "Let me tell you about...")
- Conversational and straightforward - "plain and simple" (matches website tone)
- Experienced but approachable - business partner approach, not just vendor
- British English spelling (analyse, optimise, etc.)
- Explains technical terms in plain language
- Translates technical changes into what they mean for their business in the real world
- Focuses on what it actually means for them - what does this mean for their business?
- Relates everything back to real-world business impact naturally (customers view from profitability angle, but don't force the language)
- Uses e-commerce examples (product feeds, shopping campaigns, online sales)
- Maintains flow and continuity - these are regular weekly articles
- Personal, "you get me" approach from the website

**WordPress Configuration**:

- **Site URL**: https://roksys.co.uk
- **Admin URL**: https://roksys.co.uk/wp-admin
- **Username**: Peter
- **Application Password**: Stored in LaunchAgent (`com.petesbrain.weekly-blog-generator.plist`)
- **Blog Category**: "Google Ads Weekly" (ID: 5)
- **Blog Page**: "Google Ads Blog" (ID: 507)
- **Category Archive**: https://roksys.co.uk/category/google-ads-weekly/

**Automation**:

- **Weekly Generation**: Runs automatically every Monday at 7:30 AM
- **Publishes**: Every Monday at 9:00 AM (scheduled)
- **Sunday KB Update**: Sunday 11:00 PM (ensures fresh content for blog)

**When This Skill Activates**:

1. User asks to generate/create/write a blog article
2. User wants to update or regenerate a blog post
3. User requests blog content creation
4. User mentions needing new blog content

**Prerequisites**:

- WordPress credentials configured (in LaunchAgent or environment variables)
- Anthropic API key configured
- External RSS feeds accessible (Search Engine Journal, Marketing Dive)
- **NOTE**: Does NOT require knowledge base (uses external sources only)

**Troubleshooting**:

### "No recent articles found"
- Check knowledge base index: `python3 agents/knowledge-base-indexer/knowledge-base-indexer.py`
- Verify articles exist from last 7 days
- Check `shared/data/kb-index.json` exists

### "WordPress credentials not configured"
- Set environment variables before running script
- Or check LaunchAgent plist: `agents/launchagents/com.petesbrain.weekly-blog-generator.plist`

### "Failed to generate blog post content"
- Check ANTHROPIC_API_KEY is set correctly
- Verify API key has sufficient credits
- Check Claude API status

### Post not appearing on WordPress
- Check log file: `~/.petesbrain-weekly-blog.log`
- Verify post was created (check WordPress admin)
- If scheduled, check "Scheduled" posts in WordPress admin

**Related Skills**:

- **WordPress Blog Manager** - For managing existing posts, publishing scheduled posts, editing content
- **Knowledge Base** - Source of articles used for blog generation

**Resources**:

- `agents/weekly-blog-generator/weekly-blog-generator.py` - Main blog generator script
- `agents/content-sync/WEEKLY-BLOG-GENERATOR-README.md` - Detailed documentation
- `roksys/roksys-website-content.md` - Tone of voice reference
- `agents/launchagents/com.petesbrain.weekly-blog-generator.plist` - LaunchAgent configuration
- `shared/data/weekly-blog-generator.log` - Log file
- `shared/data/kb-index.json` - Knowledge base index

**Quick Reference**:

**Generate New Post**:
```bash
cd /Users/administrator/Documents/PetesBrain && \
export WORDPRESS_URL="https://roksys.co.uk" && \
export WORDPRESS_USERNAME="Peter" && \
export WORDPRESS_APP_PASSWORD="qxxA8shXiVJtD9tlI0RY0Rvf" && \
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" && \
python3 agents/weekly-blog-generator/weekly-blog-generator.py
```

**Update Existing Post**:
```bash
cd /Users/administrator/Documents/PetesBrain && \
export WORDPRESS_URL="https://roksys.co.uk" && \
export WORDPRESS_USERNAME="Peter" && \
export WORDPRESS_APP_PASSWORD="qxxA8shXiVJtD9tlI0RY0Rvf" && \
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" && \
python3 agents/weekly-blog-generator/weekly-blog-generator.py --update
```

**Check Logs**:
```bash
tail -f ~/.petesbrain-weekly-blog.log
```

---

**Note**: This skill generates blog articles for existing or future Rok Systems customers. Articles explain the world of Google Ads, what's changed recently, and translate technical changes into what they mean for their e-commerce business in the real world. Remember that customers view things from a profitability/business outcome angle, but translate that naturally without forcing "profitability" language into every article. Focus on "what does this actually mean for them?" Articles maintain flow and continuity as regular weekly content, written in Rok Systems' tone of voice from the website.

