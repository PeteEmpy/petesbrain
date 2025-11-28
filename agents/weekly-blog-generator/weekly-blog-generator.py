#!/usr/bin/env python3
"""
Weekly Google Ads Blog Post Generator

Automatically generates and publishes weekly blog posts to WordPress based on
knowledge base articles from the past 7 days. Posts are written in Peter's
tone of voice and published automatically with zero manual intervention.

Runs every Monday at 8:00 AM via LaunchAgent.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import anthropic
import requests
from typing import List, Dict, Any, Optional

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
KB_ROOT = PROJECT_ROOT / "roksys/knowledge-base"
KB_INDEX = PROJECT_ROOT / "data/cache/kb-index.json"
TONE_REFERENCE = PROJECT_ROOT / "roksys/roksys-website-content.md"
LOG_FILE = PROJECT_ROOT / "data/cache/weekly-blog-generator.log"

# WordPress Configuration (set via environment variables)
WP_URL = os.environ.get("WORDPRESS_URL", "")  # e.g., "https://roksys.co.uk"
WP_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WORDPRESS_APP_PASSWORD", "")

# Blog post settings
BLOG_CATEGORY = "Google Ads Weekly"
BLOG_TAGS = ["Google Ads", "PPC", "Industry News", "Paid Search"]


def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    print(log_entry.strip())
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_knowledge_base_index():
    """Load the knowledge base index"""
    if not KB_INDEX.exists():
        log_message("ERROR: Knowledge base index not found. Run knowledge-base-indexer.py first.")
        return None
    
    with open(KB_INDEX, 'r') as f:
        return json.load(f)


def get_recent_articles(days=7, limit=7):
    """Get recent articles from knowledge base"""
    index = load_knowledge_base_index()
    if not index:
        return []
    
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_articles = []
    
    for file_data in index.get("files", []):
        # Check if article is recent
        file_date = file_data.get("date")
        file_modified = file_data.get("modified", 0)
        
        is_recent = False
        
        # Try date field first
        if file_date:
            try:
                # Handle various date formats
                if 'T' in file_date:
                    article_date = datetime.fromisoformat(file_date.replace('Z', '+00:00').split('T')[0])
                else:
                    article_date = datetime.fromisoformat(file_date.split(' ')[0])
                
                if article_date.replace(tzinfo=None) >= cutoff_date:
                    is_recent = True
            except:
                pass
        
        # Fallback to modified timestamp
        if not is_recent and file_modified:
            try:
                modified_date = datetime.fromtimestamp(file_modified)
                if modified_date >= cutoff_date:
                    is_recent = True
            except:
                pass
        
        if is_recent:
            # Filter for Google Ads OR Facebook Ads OR Shopify related content
            category = file_data.get("category", "").lower()
            title = file_data.get("title", "").lower()
            path = file_data.get("path", "").lower()

            # Google Ads filters
            is_google_ads = (
                "google-ads" in category or
                "google ads" in title or
                "ppc" in title or
                "performance max" in title or
                "pmax" in title or
                "demand gen" in title or
                "smart bidding" in title or
                "google-ads" in path
            )

            # Facebook Ads filters
            is_facebook_ads = (
                "facebook-ads" in category or
                "facebook ads" in title or
                "instagram ads" in title or
                "meta ads" in title or
                "meta business" in title or
                "facebook pixel" in title or
                "conversions api" in title or
                "facebook-ads" in path or
                "meta-business-suite" in path
            )

            # Shopify filters
            is_shopify = (
                "shopify" in category or
                "shopify" in title or
                "ecommerce" in title or
                "product feed" in title or
                "google shopping" in title or
                "checkout optimization" in title or
                "shopify" in path
            )

            # AI Strategy filters (relevant to e-commerce/marketing)
            is_ai_strategy = (
                "ai-strategy" in category or
                "ai-strategy" in path or
                "ai" in title or
                "artificial intelligence" in title or
                "machine learning" in title or
                "genai" in title or
                "automation" in title or
                "chatgpt" in title or
                "claude" in title or
                "openai" in title or
                "anthropic" in title
            )

            if is_google_ads or is_facebook_ads or is_shopify or is_ai_strategy:
                recent_articles.append(file_data)
    
    # Sort by date (newest first)
    def sort_key(article):
        date_str = article.get("date", "")
        if date_str:
            try:
                # Convert date string to timestamp for sorting
                if 'T' in date_str:
                    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).timestamp()
                else:
                    return datetime.fromisoformat(date_str).timestamp()
            except:
                pass
        return article.get("modified", 0)

    recent_articles.sort(key=sort_key, reverse=True)
    
    return recent_articles[:limit]


def load_tone_reference():
    """Load tone of voice reference from website content"""
    if not TONE_REFERENCE.exists():
        log_message("WARNING: Tone reference file not found. Using default tone.")
        return ""
    
    with open(TONE_REFERENCE, 'r') as f:
        return f.read()


def generate_blog_post(articles: List[Dict[str, Any]]) -> Dict[str, str]:
    """Generate blog post content using Claude API"""
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return None
    
    client = anthropic.Anthropic(api_key=api_key)
    tone_reference = load_tone_reference()
    
    # Build articles summary and detect platform focus
    articles_text = ""
    has_facebook_ads = False
    has_google_ads = False
    has_shopify = False
    has_ai_strategy = False

    for i, article in enumerate(articles, 1):
        category = article.get('category', '').lower()
        title = article.get('title', '').lower()
        path = article.get('path', '').lower()

        if 'facebook-ads' in category or 'facebook ads' in title or 'meta ads' in title or 'facebook-ads' in path:
            has_facebook_ads = True
        if 'google-ads' in category or 'google ads' in title or 'google-ads' in path:
            has_google_ads = True
        if 'shopify' in category or 'shopify' in title or 'shopify' in path or 'ecommerce' in title:
            has_shopify = True
        if 'ai-strategy' in category or 'ai-strategy' in path or 'ai' in title or 'genai' in title or 'automation' in title:
            has_ai_strategy = True
            
        articles_text += f"""
{i}. **{article.get('title', 'Untitled')}**
   - Category: {article.get('category', 'Unknown')}
   - Source: {article.get('path', 'Unknown')}
   - Preview: {article.get('content_preview', '')[:300]}
"""
    
    # Get current date for post
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    date_str = week_start.strftime("%B %d, %Y")
    
    # Adjust prompt based on content
    platforms = []
    if has_google_ads:
        platforms.append("Google Ads")
    if has_facebook_ads:
        platforms.append("Facebook Ads")
    if has_shopify:
        platforms.append("Shopify")
    if has_ai_strategy:
        platforms.append("AI Strategy")

    platform_focus = " and ".join(platforms) if platforms else "Google Ads"
    agency_description = f"a {platform_focus} agency" if platforms else "a Google Ads agency"
    
    prompt = f"""You are writing a weekly blog post for roksys.co.uk, {agency_description} run by Peter Empson.

TONE OF VOICE REFERENCE:
{tone_reference[:3000]}

Write a weekly blog post that covers the latest {platform_focus} trends and developments from the past week.

TITLE REQUIREMENTS:
Create a quirky, engaging title that:
1. Reflects the TOP news story from the articles (what would customers find most interesting?)
2. Is conversational and slightly humorous - not boring or corporate
3. Hints at what's changing and why it matters to e-commerce businesses
4. Makes people want to click and read (curiosity + relevance)
5. Avoids generic patterns like "Google Ads Weekly" or "This Week In..."
6. Uses a colon structure: [Quirky Hook]: [What It Actually Means]

Examples of good quirky titles:
- "Google's Gone Video Mad: Why Your Product Photos Aren't Enough Anymore"
- "Budget Planning Just Got Smarter: Google Finally Gives You a Crystal Ball"
- "The AI Takeover Continues: Your Shopping Campaigns Are About to Get Weird"
- "Death by a Thousand Clicks: Why Google's Latest Update Actually Helps"

Choose the MOST INTERESTING development from the articles and build your title around it.

ARTICLES TO COVER:
{articles_text}

TARGET AUDIENCE:
This blog post is written for EXISTING OR FUTURE CUSTOMERS OF ROK SYSTEMS who are:
- E-commerce business owners running online stores (Shopify, WooCommerce, Magento, etc.)
- Selling products online and using (or considering) Google Ads{f" and/or Facebook Ads" if has_facebook_ads else ""}
- Wanting to understand what paid advertising changes mean for their business in the real world
- Looking to understand the world of paid advertising and what's happening in it
- Interested in how these changes will impact their business going forward
- Not necessarily PPC experts - they need clear, straightforward guidance

IMPORTANT: Write as if you're talking directly to Rok Systems customers or potential customers. This is about building trust, showing expertise, and helping them understand what {platform_focus} changes mean for their business in the real world. Translate technical information into practical business impact naturally - customers think about profitability and business outcomes, but don't force that language into every sentence.

REQUIREMENTS:
1. Write in first person ("I've been watching...", "Here's what caught my attention...", "Let me tell you about...")
2. Use conversational, straightforward language - "plain and simple" (match the website tone)
3. Be experienced but approachable - show expertise without being stuffy
4. Use British English spelling (analyse not analyze, optimise not optimize)
5. Translate technical {platform_focus} information into what it means for their business in the real world
6. Keep it conversational and relationship-focused - write as a business partner, not just a vendor
7. Use rhetorical questions to engage readers
8. Write as if you're talking directly to them - personal, "you get me" approach
9. Explain technical terms in plain language - assume readers aren't PPC experts
10. Focus on what it actually means for them - translate technical to practical business impact
11. Remember: customers view things from a profitability/business outcome angle, but translate that naturally - don't force "profitability" language into every article
12. Use examples relevant to e-commerce businesses (product feeds, shopping campaigns, online sales, etc.)
13. Maintain flow and continuity - these are regular weekly articles, so reference previous context naturally when relevant
14. Tell them about the world of paid advertising - what's happening, what's changing, what it means
15. PROFESSIONAL NEWS REPORTING VOICE - Report industry news with engaged professional perspective:
    - GOOD: "I've been watching this rollout closely" / "This is something I'm paying attention to" / "Worth keeping tabs on"
    - GOOD: "This changes how I approach..." / "I'm interested to see how this develops" / "I'll be exploring this"
    - ACCEPTABLE GENERAL: "In my experience with accounts..." / "From what I've seen across campaigns..." (general observations, not specific made-up stories)
    - BAD: "I tested this last week with a client and CTR dropped 40%" (specific fabricated test results)
    - BAD: "I uploaded 23 videos for a fashion client" (specific fabricated implementation stories)
    - BALANCE: You're a news reporter WITH professional context. Report what's happening in the industry, add your professional take, but don't invent specific client work or detailed test results you haven't actually run
    - Frequency: 2-3 natural professional observations woven into news reporting

CONTENT FOCUS:
- Explain what's changed recently in {platform_focus} news
- Translate technical changes into what they mean for their e-commerce business in the real world
- Focus on "what does this actually mean for them?" - translate technical to practical
- Help them understand the world of paid advertising ({platform_focus})
- Connect changes to real-world business impact naturally (customers think about profitability, but translate it naturally)
- Be forward-looking - what this means going forward for their business
{f"- When covering Facebook Ads topics, explain them in the context of e-commerce businesses and how they complement or differ from Google Ads" if has_facebook_ads else ""}

STRUCTURE:
- Opening: Brief intro about what's happening this week in {platform_focus} that matters to their business (2-3 sentences, conversational)
- Main sections: Cover 3-5 key developments from the articles
- Each section should:
  - Explain what happened in the world of paid advertising (specify if it's Google Ads or Facebook Ads)
  - Translate it into what it means for their e-commerce business in the real world
  - What does this actually mean for them? (translate technical to practical)
  - What it means going forward for their business
- Closing: Brief summary tying it all together and forward-looking statement about what to watch for

LENGTH: 800-1200 words

RESPONSE FORMAT:
Return your response in this exact format:

TITLE: [Your quirky, engaging title here]

CONTENT:
[HTML content starts here]

Write the blog post in HTML format suitable for WordPress, using proper semantic HTML:
- Use <h2> for main section headings
- Use <h3> for subsections
- Use <p> for paragraphs
- Use <ul> and <li> for lists
- Use <a href="url"> for links to source articles
- Use <strong> for emphasis (not <b>)
- Keep HTML clean and semantic - WordPress theme will handle styling

Do NOT include:
- Inline styles or CSS
- <style> tags
- <div> wrappers unless necessary
- Any styling - just semantic HTML structure
- The title in the HTML content (it will be added separately by WordPress)"""

    try:
        log_message("Generating blog post with Claude...")
        
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text

        # Extract title and content from response
        if "TITLE:" in response_text and "CONTENT:" in response_text:
            parts = response_text.split("CONTENT:")
            title_part = parts[0].replace("TITLE:", "").strip()
            content = parts[1].strip()
        else:
            # Fallback to default title if format not followed
            title_part = f"Google Ads Weekly: {date_str}"
            content = response_text

        # Extract HTML if wrapped in code blocks
        if "```html" in content:
            content = content.split("```html")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        title = title_part

        # Generate excerpt (first 150 words)
        excerpt = content.replace("<h2>", "").replace("</h2>", "").replace("<p>", "").replace("</p>", "")[:150] + "..."
        
        return {
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "date": today.isoformat()
        }
        
    except Exception as e:
        log_message(f"ERROR generating blog post: {e}")
        return None


def publish_to_wordpress(post_data: Dict[str, str]) -> bool:
    """Publish blog post to WordPress via REST API"""
    
    if not all([WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
        log_message("ERROR: WordPress credentials not configured")
        log_message("Set WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD environment variables")
        return False
    
    # WordPress REST API endpoint
    api_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    # Authentication
    # Remove spaces from app password if present (WordPress accepts both formats)
    app_password = WP_APP_PASSWORD.replace(' ', '')
    auth = (WP_USERNAME, app_password)
    
    # Calculate publish date (next Monday at 9 AM)
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # If today is Monday, schedule for next Monday
    
    publish_date = today + timedelta(days=days_until_monday)
    publish_date = publish_date.replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Get or create category
    category_id = get_or_create_category(BLOG_CATEGORY, auth)
    
    # Get or create tags
    tag_ids = []
    for tag in BLOG_TAGS:
        tag_id = get_or_create_tag(tag, auth)
        if tag_id:
            tag_ids.append(tag_id)
    
    # Prepare post data
    post_payload = {
        "title": post_data["title"],
        "content": post_data["content"],
        "excerpt": post_data["excerpt"],
        "status": "future",  # Schedule for future
        "date": publish_date.isoformat(),
        "categories": [category_id] if category_id else [],
        "tags": tag_ids,
        "format": "standard"
    }
    
    try:
        log_message(f"Publishing to WordPress: {post_data['title']}")
        log_message(f"Scheduled for: {publish_date.strftime('%Y-%m-%d %H:%M')}")
        
        response = requests.post(
            api_url,
            json=post_payload,
            auth=auth,
            timeout=30
        )
        
        if response.status_code == 201:
            post_id = response.json().get("id")
            post_url = response.json().get("link")
            log_message(f"✓ Successfully published! Post ID: {post_id}")
            log_message(f"✓ Post URL: {post_url}")
            return True
        else:
            log_message(f"ERROR: WordPress API returned {response.status_code}")
            log_message(f"Response: {response.text}")
            
            # Helpful error messages
            if response.status_code == 401:
                if "not allowed to create posts" in response.text:
                    log_message("")
                    log_message("TROUBLESHOOTING:")
                    log_message("  The user account needs Editor or Administrator role")
                    log_message("  Check: WordPress → Users → Your Profile → Role")
                    log_message("  Or verify the username is correct")
                else:
                    log_message("")
                    log_message("TROUBLESHOOTING:")
                    log_message("  Check Application Password is correct")
                    log_message("  Verify username is correct")
                    log_message("  Ensure Application Passwords are enabled in WordPress")
            
            return False
            
    except Exception as e:
        log_message(f"ERROR publishing to WordPress: {e}")
        return False


def get_or_create_category(name: str, auth: tuple) -> int:
    """Get existing category or create new one"""
    categories_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/categories"
    
    # Check if category exists
    response = requests.get(
        categories_url,
        params={"search": name},
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        categories = response.json()
        for cat in categories:
            if cat["name"].lower() == name.lower():
                return cat["id"]
    
    # Create category
    response = requests.post(
        categories_url,
        json={"name": name},
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 201:
        return response.json()["id"]
    
    return None


def get_or_create_tag(name: str, auth: tuple) -> int:
    """Get existing tag or create new one"""
    tags_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/tags"
    
    # Check if tag exists
    response = requests.get(
        tags_url,
        params={"search": name},
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        tags = response.json()
        for tag in tags:
            if tag["name"].lower() == name.lower():
                return tag["id"]
    
    # Create tag
    response = requests.post(
        tags_url,
        json={"name": name},
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 201:
        return response.json()["id"]
    
    return None


def find_most_recent_post(auth: tuple, category_id: Optional[int] = None) -> Optional[Dict]:
    """Find the most recent blog post (scheduled or published)"""
    posts_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    params = {
        "per_page": 10,
        "orderby": "date",
        "order": "desc"
    }
    
    if category_id:
        params["categories"] = category_id
    
    response = requests.get(
        posts_url,
        params=params,
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        posts = response.json()
        if posts:
            # Return the most recent post
            return posts[0]
    
    return None


def update_existing_post(post_id: int, post_data: Dict[str, str], auth: tuple) -> bool:
    """Update an existing WordPress post with new content"""
    post_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    
    # Get current post to preserve some metadata
    response = requests.get(post_url, auth=auth, timeout=10)
    
    if response.status_code != 200:
        log_message(f"ERROR: Failed to fetch existing post: {response.status_code}")
        return False
    
    current_post = response.json()
    
    # Prepare update data
    update_data = {
        "title": post_data["title"],
        "content": post_data["content"],
        "excerpt": post_data["excerpt"]
    }
    
    # Preserve status and date if it's scheduled
    if current_post.get("status") == "future":
        update_data["status"] = "future"
        update_data["date"] = current_post.get("date")
    
    try:
        log_message(f"Updating existing post ID {post_id}...")
        
        response = requests.post(
            post_url,
            json=update_data,
            auth=auth,
            timeout=30
        )
        
        if response.status_code == 200:
            updated_post = response.json()
            post_url_link = updated_post.get("link", "")
            log_message(f"✓ Successfully updated post!")
            log_message(f"✓ Post ID: {post_id}")
            log_message(f"✓ Post URL: {post_url_link}")
            return True
        else:
            log_message(f"ERROR: WordPress API returned {response.status_code}")
            log_message(f"Response: {response.text}")
            return False
            
    except Exception as e:
        log_message(f"ERROR updating WordPress post: {e}")
        return False


def regenerate_and_update_post():
    """Regenerate blog post with e-commerce focus and update the most recent post"""
    
    log_message("=" * 70)
    log_message("Regenerating Blog Post with E-Commerce Focus")
    log_message("=" * 70)
    
    if not all([WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
        log_message("ERROR: WordPress credentials not configured")
        log_message("Set WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD environment variables")
        return False
    
    auth = (WP_USERNAME, WP_APP_PASSWORD.replace(' ', ''))
    
    # Get category ID
    category_id = get_or_create_category(BLOG_CATEGORY, auth)
    
    # Find most recent post
    log_message("Finding most recent blog post...")
    recent_post = find_most_recent_post(auth, category_id)
    
    if not recent_post:
        log_message("ERROR: No blog posts found. Cannot update.")
        return False
    
    post_id = recent_post.get("id")
    post_title = recent_post.get("title", {}).get("rendered", "Unknown")
    post_status = recent_post.get("status", "unknown")
    
    log_message(f"Found post:")
    log_message(f"  Post ID: {post_id}")
    log_message(f"  Title: {post_title}")
    log_message(f"  Status: {post_status}")
    
    # Get recent articles
    log_message("\nFetching recent articles from knowledge base...")
    articles = get_recent_articles(days=7, limit=7)
    
    if not articles:
        log_message("No recent articles found. Cannot regenerate.")
        return False
    
    log_message(f"Found {len(articles)} recent articles")
    
    # Generate new blog post
    log_message("\nGenerating new blog post with e-commerce focus...")
    post_data = generate_blog_post(articles)
    
    if not post_data:
        log_message("Failed to generate blog post content")
        return False
    
    log_message(f"✓ Generated new blog post: {post_data['title']}")
    
    # Update existing post
    log_message("\nUpdating existing post...")
    if update_existing_post(post_id, post_data, auth):
        log_message("=" * 70)
        log_message("Blog post successfully updated!")
        log_message("=" * 70)
        return True
    else:
        log_message("=" * 70)
        log_message("Failed to update blog post. Check logs for details.")
        log_message("=" * 70)
        return False


def main():
    """Main function to generate and publish weekly blog post"""
    
    # Check if we're updating an existing post
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        sys.exit(0 if regenerate_and_update_post() else 1)
    
    log_message("=" * 70)
    log_message("Weekly Google Ads Blog Post Generator Started")
    log_message("=" * 70)
    
    # Get recent articles
    log_message("Fetching recent articles from knowledge base...")
    articles = get_recent_articles(days=7, limit=7)
    
    if not articles:
        log_message("No recent articles found. Skipping blog post generation.")
        return
    
    log_message(f"Found {len(articles)} recent articles")
    
    # Generate blog post
    post_data = generate_blog_post(articles)
    
    if not post_data:
        log_message("Failed to generate blog post content")
        return
    
    log_message(f"✓ Generated blog post: {post_data['title']}")
    
    # Publish to WordPress
    if publish_to_wordpress(post_data):
        log_message("=" * 70)
        log_message("Blog post successfully published to WordPress!")
        log_message("=" * 70)
    else:
        log_message("=" * 70)
        log_message("Failed to publish to WordPress. Check logs for details.")
        log_message("=" * 70)
        # Save draft locally as backup
        draft_file = PROJECT_ROOT / f"data/cache/blog-draft-{datetime.now().strftime('%Y%m%d')}.html"
        with open(draft_file, 'w') as f:
            f.write(f"<h1>{post_data['title']}</h1>\n{post_data['content']}")
        log_message(f"Draft saved to: {draft_file}")


if __name__ == "__main__":
    main()

