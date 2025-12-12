#!/usr/bin/env python3
"""
Weekly Google Ads Blog Post Generator

Automatically generates and publishes weekly blog posts to WordPress based on
external news sources and public announcements. Posts are written in Peter's
tone of voice and published automatically with zero manual intervention.

Data sources: Google Ads official blog, industry news, Google Trends, public announcements.
NO internal client data is used.

Runs every Monday at 8:00 AM via LaunchAgent.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import anthropic

# Add shared module to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from secrets import get_secret
import requests
from typing import List, Dict, Any, Optional
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
TONE_REFERENCE = PROJECT_ROOT / "roksys/roksys-website-content.md"
LOG_FILE = PROJECT_ROOT / "data/cache/weekly-blog-generator.log"

# External news sources (public, no internal data)
GOOGLE_ADS_BLOG_URL = "https://ads.google.com/intl/en_uk/home/"
SEARCH_ENGINE_JOURNAL_RSS = "https://www.searchenginejournal.com/feed/"
MARKETING_DIVE_PPC_RSS = "https://www.marketingdive.com/news/"
GOOGLE_NEWS_URL = "https://news.google.com/rss/topics/CAAqKggKJjRDQkJDQkoxNW1nZ0FNRUtLS0pCUU1SVVFBR0tOS0pBQlBIAQ"

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


def fetch_rss_feed(url: str, days=7) -> List[Dict[str, Any]]:
    """Fetch articles from an RSS feed (external news source)"""
    articles = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        cutoff_date = datetime.now() - timedelta(days=days)

        for item in root.findall('.//item'):
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                description_elem = item.find('description')

                if title_elem is not None and title_elem.text:
                    title = title_elem.text.strip()
                    link = link_elem.text if link_elem is not None else ""
                    description = description_elem.text if description_elem is not None else ""

                    # Parse publication date
                    pub_date = None
                    if pub_date_elem is not None and pub_date_elem.text:
                        try:
                            # RSS uses RFC 2822 date format
                            from email.utils import parsedate_to_datetime
                            pub_date = parsedate_to_datetime(pub_date_elem.text)
                        except:
                            pub_date = datetime.now()

                    # Check if article is recent enough
                    if pub_date and pub_date.replace(tzinfo=None) >= cutoff_date:
                        # Filter for PPC/ads-related content
                        combined_text = (title + " " + description).lower()
                        if any(keyword in combined_text for keyword in
                               ["google ads", "ppc", "paid search", "performance max", "pmax",
                                "facebook ads", "meta ads", "instagram ads", "ecommerce",
                                "shopping campaign", "advertising", "digital marketing"]):

                            articles.append({
                                "title": title,
                                "link": link,
                                "description": description[:300] if description else "",
                                "date": pub_date.isoformat() if pub_date else datetime.now().isoformat(),
                                "source": "external-news",
                                "category": "industry-news"
                            })
            except Exception as e:
                continue

        return articles
    except Exception as e:
        log_message(f"ERROR fetching RSS feed from {url}: {e}")
        return []


def get_external_news_articles(days=7, limit=7) -> List[Dict[str, Any]]:
    """Get recent articles from external news sources only (no internal data)"""
    all_articles = []

    # Fetch from multiple external RSS feeds
    rss_feeds = [
        SEARCH_ENGINE_JOURNAL_RSS,
        MARKETING_DIVE_PPC_RSS,
    ]

    for feed_url in rss_feeds:
        articles = fetch_rss_feed(feed_url, days=days)
        all_articles.extend(articles)

    # Sort by date (newest first)
    all_articles.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Return top articles
    return all_articles[:limit]


def load_tone_reference():
    """Load tone of voice reference from website content"""
    if not TONE_REFERENCE.exists():
        log_message("WARNING: Tone reference file not found. Using default tone.")
        return ""
    
    with open(TONE_REFERENCE, 'r') as f:
        return f.read()


def generate_blog_post(articles: List[Dict[str, Any]]) -> Dict[str, str]:
    """Generate blog post content using Claude API"""

    api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not found in Keychain or environment")
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

CRITICAL: This blog post uses EXTERNAL NEWS SOURCES ONLY. Do NOT reference any internal client data, case studies, or specific implementations. All content is based on public news, announcements, and industry articles.

TONE OF VOICE REFERENCE:
{tone_reference[:3000]}

Write a weekly blog post that covers the latest {platform_focus} trends and developments from the past week based on public industry news and announcements.

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
    - GOOD: "Based on what we're seeing in the industry..." / "Industry patterns suggest..."
    - BAD: ANY specific client stories, case studies, or names (NEVER identify clients by industry or context)
    - BAD: "I tested this last week with a client and CTR dropped 40%" (DO NOT invent client test results)
    - BAD: "I uploaded 23 videos for a fashion client" (DO NOT invent client implementation stories)
    - CRITICAL: No client data, no case studies, no specific implementations - only general professional observations about industry trends
    - Frequency: 1-2 general professional observations only (but never specific client work)

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

    # Check for duplicate post
    duplicate_post_id = check_for_duplicate_post(post_data["title"], auth, category_id)
    if duplicate_post_id:
        log_message(f"⚠ Duplicate detected: Post with title '{post_data['title'][:50]}...' already exists (ID: {duplicate_post_id})")
        log_message("Skipping creation to prevent duplicates")
        return True  # Consider this a success (no duplicate created)

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


def check_for_duplicate_post(title: str, auth: tuple, category_id: int) -> Optional[int]:
    """Check if a post with the same title already exists from the past 7 days
    Returns post ID if duplicate found, None otherwise"""
    posts_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"

    # Get posts from the past 7 days in this category
    cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()

    params = {
        "per_page": 50,
        "categories": category_id,
        "after": cutoff_date,
        "orderby": "date",
        "order": "desc"
    }

    try:
        response = requests.get(
            posts_url,
            params=params,
            auth=auth,
            timeout=10
        )

        if response.status_code == 200:
            posts = response.json()
            for post in posts:
                post_title = post.get("title", {}).get("rendered", "") if isinstance(post.get("title"), dict) else post.get("title", "")
                # Check if title matches exactly or is very similar (allowing for HTML encoding)
                if post_title.lower() == title.lower() or post_title.replace("&#8217;", "'").lower() == title.lower():
                    return post["id"]
    except Exception as e:
        log_message(f"WARNING: Could not check for duplicates: {e}")

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
    
    # Get recent articles from external news sources (no internal data)
    log_message("\nFetching recent articles from external news sources...")
    articles = get_external_news_articles(days=7, limit=7)
    
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

    # Get recent articles from external news sources (no internal data)
    log_message("Fetching recent articles from external news sources...")
    articles = get_external_news_articles(days=7, limit=7)
    
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

