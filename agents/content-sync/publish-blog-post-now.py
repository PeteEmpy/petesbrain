#!/usr/bin/env python3
"""
Publish Scheduled WordPress Blog Post

Finds the most recent scheduled blog post and publishes it immediately.
"""

import os
import sys
import requests
from datetime import datetime
from typing import Optional, Dict

# WordPress Configuration (set via environment variables)
WP_URL = os.environ.get("WORDPRESS_URL", "")  # e.g., "https://roksys.co.uk"
WP_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WORDPRESS_APP_PASSWORD", "")

# Blog settings
BLOG_CATEGORY = "Google Ads Weekly"


def get_auth():
    """Get WordPress authentication tuple"""
    if not all([WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
        print("ERROR: WordPress credentials not configured")
        print("Set WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD environment variables")
        return None
    
    app_password = WP_APP_PASSWORD.replace(' ', '')
    return (WP_USERNAME, app_password)


def get_category_id(auth: tuple, category_name: str) -> Optional[int]:
    """Get category ID by name"""
    categories_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/categories"
    
    response = requests.get(
        categories_url,
        params={"search": category_name},
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        categories = response.json()
        for cat in categories:
            if cat["name"].lower() == category_name.lower():
                return cat["id"]
    
    return None


def find_scheduled_post(auth: tuple, category_id: Optional[int] = None) -> Optional[Dict]:
    """Find the most recent scheduled post"""
    posts_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    params = {
        "status": "future",
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
            # Return the most recent scheduled post
            return posts[0]
    
    return None


def publish_post_now(auth: tuple, post_id: int) -> bool:
    """Publish a scheduled post immediately"""
    post_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    
    # Get current post data
    response = requests.get(post_url, auth=auth, timeout=10)
    
    if response.status_code != 200:
        print(f"✗ Failed to fetch post: {response.status_code}")
        return False
    
    post_data = response.json()
    
    # Update to publish now
    update_data = {
        "status": "publish",
        "date": datetime.now().isoformat()
    }
    
    response = requests.post(
        post_url,
        json=update_data,
        auth=auth,
        timeout=30
    )
    
    if response.status_code == 200:
        updated_post = response.json()
        post_link = updated_post.get("link", "")
        print(f"✓ Post published successfully!")
        print(f"  Post ID: {post_id}")
        print(f"  Title: {updated_post.get('title', {}).get('rendered', 'Unknown')}")
        print(f"  URL: {post_link}")
        return True
    else:
        print(f"✗ Failed to publish post: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


def main():
    print("=" * 60)
    print("Publish Scheduled WordPress Blog Post")
    print("=" * 60)
    
    auth = get_auth()
    if not auth:
        return 1
    
    # Get category ID (optional, but helps filter)
    print("\n1. Finding category...")
    category_id = get_category_id(auth, BLOG_CATEGORY)
    if category_id:
        print(f"✓ Found category '{BLOG_CATEGORY}' (ID: {category_id})")
    else:
        print(f"⚠️  Category '{BLOG_CATEGORY}' not found (will search all scheduled posts)")
    
    # Find scheduled post
    print("\n2. Searching for scheduled posts...")
    scheduled_post = find_scheduled_post(auth, category_id)
    
    if not scheduled_post:
        print("✗ No scheduled posts found")
        print("   Check if there are any posts with 'future' status")
        return 1
    
    post_id = scheduled_post.get("id")
    post_title = scheduled_post.get("title", {}).get("rendered", "Unknown")
    scheduled_date = scheduled_post.get("date", "")
    
    print(f"✓ Found scheduled post:")
    print(f"  Post ID: {post_id}")
    print(f"  Title: {post_title}")
    print(f"  Scheduled for: {scheduled_date}")
    
    # Confirm
    print(f"\n3. Publishing post now...")
    if publish_post_now(auth, post_id):
        print("\n✅ Success! Post is now live.")
        return 0
    else:
        print("\n❌ Failed to publish post.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

