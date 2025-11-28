#!/usr/bin/env python3
"""
Remove Text from WordPress Blog Post

Finds the most recent blog post and removes specified text from it.
"""

import os
import sys
import requests
from typing import Optional, Dict

# WordPress Configuration (set via environment variables)
WP_URL = os.environ.get("WORDPRESS_URL", "")  # e.g., "https://roksys.co.uk"
WP_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WORDPRESS_APP_PASSWORD", "")

# Text to remove
TEXT_TO_REMOVE = "Conguid Portitur Aliquet"


def get_auth():
    """Get WordPress authentication tuple"""
    if not all([WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
        print("ERROR: WordPress credentials not configured")
        print("Set WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD environment variables")
        return None
    
    app_password = WP_APP_PASSWORD.replace(' ', '')
    return (WP_USERNAME, app_password)


def get_recent_post(auth: tuple) -> Optional[Dict]:
    """Get the most recent published post"""
    posts_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    params = {
        "status": "publish",
        "per_page": 1,
        "orderby": "date",
        "order": "desc"
    }
    
    response = requests.get(
        posts_url,
        params=params,
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        posts = response.json()
        if posts:
            return posts[0]
    
    return None


def remove_text_from_post(auth: tuple, post_id: int, text_to_remove: str) -> bool:
    """Remove specified text from a WordPress post"""
    post_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    
    # Get current post data
    response = requests.get(post_url, auth=auth, timeout=10)
    
    if response.status_code != 200:
        print(f"✗ Failed to fetch post: {response.status_code}")
        return False
    
    post_data = response.json()
    current_content_raw = post_data.get("content", {}).get("raw", "")
    current_content_rendered = post_data.get("content", {}).get("rendered", "")
    
    # Show a preview of the content
    print(f"\n   Post content preview (first 500 chars):")
    preview = current_content_raw[:500] if current_content_raw else current_content_rendered[:500]
    print(f"   {preview}...")
    
    # Try case-insensitive search
    text_lower = text_to_remove.lower()
    content_lower = current_content_raw.lower() if current_content_raw else current_content_rendered.lower()
    
    # Check if text exists (case-insensitive)
    if text_lower not in content_lower:
        print(f"\n⚠️  Text '{text_to_remove}' not found in post content")
        print(f"   Searching for variations...")
        
        # Try searching for individual words
        words = text_to_remove.split()
        found_words = []
        for word in words:
            if word.lower() in content_lower:
                found_words.append(word)
        
        if found_words:
            print(f"   Found some words: {', '.join(found_words)}")
            print(f"   But exact phrase not found.")
        else:
            print(f"   None of the words found either.")
        
        return False
    
    # Find the actual text (preserve case)
    # Try to find it in raw content first
    if current_content_raw:
        if text_to_remove in current_content_raw:
            updated_content = current_content_raw.replace(text_to_remove, "")
        elif text_lower in content_lower:
            # Case-insensitive replacement
            import re
            pattern = re.compile(re.escape(text_to_remove), re.IGNORECASE)
            updated_content = pattern.sub("", current_content_raw)
        else:
            updated_content = current_content_raw
    else:
        # Use rendered content
        if text_to_remove in current_content_rendered:
            updated_content = current_content_rendered.replace(text_to_remove, "")
        else:
            import re
            pattern = re.compile(re.escape(text_to_remove), re.IGNORECASE)
            updated_content = pattern.sub("", current_content_rendered)
    
    # Also try removing with HTML tags if it's wrapped
    updated_content = updated_content.replace(f"<p>{text_to_remove}</p>", "")
    updated_content = updated_content.replace(f"<div>{text_to_remove}</div>", "")
    updated_content = updated_content.replace(f"<span>{text_to_remove}</span>", "")
    
    # Remove any extra whitespace/newlines left behind
    import re
    updated_content = re.sub(r'\n\s*\n\s*\n', '\n\n', updated_content)  # Remove triple+ newlines
    
    # Update post
    update_data = {
        "content": updated_content
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
        print(f"\n✓ Text removed successfully!")
        print(f"  Post ID: {post_id}")
        print(f"  Title: {updated_post.get('title', {}).get('rendered', 'Unknown')}")
        print(f"  URL: {post_link}")
        return True
    else:
        print(f"✗ Failed to update post: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


def search_all_posts(auth: tuple, text_to_remove: str) -> list:
    """Search all posts for the text"""
    posts_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    params = {
        "status": ["publish", "future", "draft"],
        "per_page": 20,
        "orderby": "date",
        "order": "desc"
    }
    
    response = requests.get(
        posts_url,
        params=params,
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        posts = response.json()
        matching_posts = []
        
        text_lower = text_to_remove.lower()
        
        for post in posts:
            content_raw = post.get("content", {}).get("raw", "")
            content_rendered = post.get("content", {}).get("rendered", "")
            content_to_search = content_raw if content_raw else content_rendered
            
            if text_lower in content_to_search.lower():
                matching_posts.append(post)
        
        return matching_posts
    
    return []


def main():
    print("=" * 60)
    print("Remove Text from WordPress Blog Post")
    print("=" * 60)
    
    auth = get_auth()
    if not auth:
        return 1
    
    # Search all posts
    print(f"\n1. Searching all posts for '{TEXT_TO_REMOVE}'...")
    matching_posts = search_all_posts(auth, TEXT_TO_REMOVE)
    
    if not matching_posts:
        print(f"✗ Text '{TEXT_TO_REMOVE}' not found in any posts")
        print("\n   The text might be:")
        print("   - In a widget or sidebar")
        print("   - In page content (not a post)")
        print("   - Already removed")
        print("   - In a different format/spelling")
        return 1
    
    print(f"✓ Found text in {len(matching_posts)} post(s):")
    for post in matching_posts:
        post_id = post.get("id")
        post_title = post.get("title", {}).get("rendered", "Unknown")
        print(f"  - Post ID {post_id}: {post_title}")
    
    # Remove from all matching posts
    print(f"\n2. Removing '{TEXT_TO_REMOVE}' from post(s)...")
    success_count = 0
    for post in matching_posts:
        post_id = post.get("id")
        post_title = post.get("title", {}).get("rendered", "Unknown")
        print(f"\n   Processing: {post_title} (ID: {post_id})...")
        if remove_text_from_post(auth, post_id, TEXT_TO_REMOVE):
            success_count += 1
    
    if success_count > 0:
        print(f"\n✅ Success! Removed text from {success_count} post(s).")
        return 0
    else:
        print("\n❌ Failed to remove text from any posts.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

