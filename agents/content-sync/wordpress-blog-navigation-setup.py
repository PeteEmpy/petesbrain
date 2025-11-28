#!/usr/bin/env python3
"""
WordPress Blog Navigation Setup

Adds blog navigation to WordPress site by:
1. Creating a blog archive page (if it doesn't exist)
2. Adding a "Blog" menu item to the main navigation menu
3. Setting up category archive links

Runs once to set up navigation, then blog posts will be accessible.
"""

import os
import sys
import requests
from typing import Optional, Dict, Any

# WordPress Configuration (set via environment variables)
WP_URL = os.environ.get("WORDPRESS_URL", "")  # e.g., "https://roksys.co.uk"
WP_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WORDPRESS_APP_PASSWORD", "")

# Blog settings
BLOG_CATEGORY = "Google Ads Weekly"
BLOG_PAGE_TITLE = "Google Ads Blog"
BLOG_MENU_LABEL = "Blog"


def get_auth():
    """Get WordPress authentication tuple"""
    if not all([WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
        print("ERROR: WordPress credentials not configured")
        print("Set WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD environment variables")
        return None
    
    app_password = WP_APP_PASSWORD.replace(' ', '')
    return (WP_USERNAME, app_password)


def get_category_archive_url(category_name: str) -> str:
    """Get the URL for a category archive page"""
    # WordPress category archives are typically at /category/category-slug/
    category_slug = category_name.lower().replace(' ', '-')
    return f"{WP_URL.rstrip('/')}/category/{category_slug}/"


def create_blog_page(auth: tuple) -> Optional[int]:
    """Create a blog archive page if it doesn't exist"""
    pages_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/pages"
    
    # Check if page already exists
    response = requests.get(
        pages_url,
        params={"search": BLOG_PAGE_TITLE, "per_page": 10},
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        pages = response.json()
        for page in pages:
            if page['title']['rendered'] == BLOG_PAGE_TITLE:
                print(f"✓ Blog page already exists (ID: {page['id']})")
                return page['id']
    
    # Create new page
    category_url = get_category_archive_url(BLOG_CATEGORY)
    
    page_content = f"""<h2>Google Ads Weekly Blog</h2>
<p>Stay up to date with the latest Google Ads trends, updates, and insights.</p>
<p><a href="{category_url}" class="button">View All Posts</a></p>
<p>This page displays all posts in the "{BLOG_CATEGORY}" category.</p>
"""
    
    page_data = {
        "title": BLOG_PAGE_TITLE,
        "content": page_content,
        "status": "publish"
    }
    
    response = requests.post(
        pages_url,
        json=page_data,
        auth=auth,
        timeout=30
    )
    
    if response.status_code == 201:
        page_id = response.json().get("id")
        page_url = response.json().get("link")
        print(f"✓ Created blog page (ID: {page_id})")
        print(f"  URL: {page_url}")
        return page_id
    else:
        print(f"✗ Failed to create blog page: {response.status_code}")
        print(f"  Response: {response.text}")
        return None


def get_menu_id(auth: tuple, menu_name: str = "Primary Menu") -> Optional[int]:
    """Get menu ID by name"""
    # WordPress REST API doesn't have a direct menu endpoint in core
    # We'll need to use a workaround or check via admin
    # For now, return None and we'll add menu item via alternative method
    return None


def add_menu_item_via_customizer(auth: tuple, page_id: int) -> bool:
    """Add menu item using WordPress Customizer API (if available)"""
    # WordPress menu management via REST API is limited
    # This would require custom endpoints or manual setup
    print("⚠️  Menu item must be added manually in WordPress")
    print(f"   Go to: Appearance → Menus → Add '{BLOG_MENU_LABEL}' → Link to page ID {page_id}")
    return False


def add_menu_item_via_plugin(auth: tuple, page_id: int) -> bool:
    """Attempt to add menu item via REST API (requires menu support)"""
    # Try to use wp/v2/menus endpoint if available
    menus_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/menus"
    
    response = requests.get(menus_url, auth=auth, timeout=10)
    
    if response.status_code == 200:
        menus = response.json()
        if menus:
            menu_id = menus[0].get('id')
            menu_items_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/menu-items"
            
            menu_item_data = {
                "title": BLOG_MENU_LABEL,
                "type": "post_type",
                "object": "page",
                "object_id": page_id,
                "menu": menu_id
            }
            
            response = requests.post(
                menu_items_url,
                json=menu_item_data,
                auth=auth,
                timeout=30
            )
            
            if response.status_code == 201:
                print(f"✓ Added '{BLOG_MENU_LABEL}' to menu")
                return True
    
    return False


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


def print_setup_instructions(page_id: Optional[int], category_id: Optional[int]):
    """Print manual setup instructions"""
    print("\n" + "=" * 60)
    print("BLOG NAVIGATION SETUP INSTRUCTIONS")
    print("=" * 60)
    
    if page_id:
        print(f"\n✓ Blog page created (ID: {page_id})")
        print(f"  View: {WP_URL}/google-ads-blog/")
    
    if category_id:
        category_url = get_category_archive_url(BLOG_CATEGORY)
        print(f"\n✓ Category archive available")
        print(f"  URL: {category_url}")
    
    print("\n📋 ELEMENTOR SETUP STEPS:")
    print("\nSince you're using Elementor, add the blog link via Elementor Header Builder:")
    print("\n1. Edit Header Template in Elementor:")
    print("   - Go to WordPress Admin → Templates → Theme Builder")
    print("   - Find your Header template and click 'Edit with Elementor'")
    print("   - Or: Templates → Saved Templates → Find your header → Edit")
    
    print("\n2. Add Blog Link to Navigation:")
    print("   Option A - Add to Existing Menu Widget:")
    print("   - Find your navigation menu widget in the header")
    print("   - Go to WordPress Admin → Appearance → Menus")
    print("   - Add a new menu item:")
    print(f"     * Label: '{BLOG_MENU_LABEL}'")
    if category_id:
        print(f"     * URL: {get_category_archive_url(BLOG_CATEGORY)}")
    print("   - Save menu")
    print("   - The menu widget in Elementor should automatically update")
    
    print("\n   Option B - Add Button/Link Widget:")
    print("   - In Elementor header editor, drag a 'Button' or 'HTML' widget")
    print("   - Position it where you want the Blog link")
    print("   - Set button text: 'Blog'")
    if category_id:
        print(f"   - Set link: {get_category_archive_url(BLOG_CATEGORY)}")
    print("   - Style to match your navigation")
    print("   - Click 'Update' to save header")
    
    print("\n3. Alternative: Add to Footer:")
    print("   - Edit Footer template in Elementor")
    print("   - Add a Button or Text widget")
    print(f"   - Link to: {get_category_archive_url(BLOG_CATEGORY)}")
    
    print("\n4. Verify Blog Posts are Visible:")
    print(f"   - Visit: {get_category_archive_url(BLOG_CATEGORY)}")
    print("   - All posts in 'Google Ads Weekly' category should appear")
    
    print("\n💡 Quick Link to Use:")
    if category_id:
        print(f"   {get_category_archive_url(BLOG_CATEGORY)}")
    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("WordPress Blog Navigation Setup")
    print("=" * 60)
    
    auth = get_auth()
    if not auth:
        return 1
    
    # Create blog page
    print("\n1. Creating blog archive page...")
    page_id = create_blog_page(auth)
    
    # Get category ID
    print("\n2. Checking category...")
    category_id = get_category_id(auth, BLOG_CATEGORY)
    if category_id:
        print(f"✓ Category '{BLOG_CATEGORY}' exists (ID: {category_id})")
    else:
        print(f"⚠️  Category '{BLOG_CATEGORY}' not found")
        print("   (It will be created automatically when first blog post is published)")
    
    # Try to add menu item programmatically
    print("\n3. Attempting to add menu item...")
    if page_id:
        # Try plugin method first
        if not add_menu_item_via_plugin(auth, page_id):
            # Fall back to instructions
            add_menu_item_via_customizer(auth, page_id)
    
    # Print setup instructions
    print_setup_instructions(page_id, category_id)
    
    print("\n✅ Setup complete!")
    print("   Since you're using Elementor, follow the Elementor-specific steps above")
    print("   to add the Blog link to your header navigation.")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

