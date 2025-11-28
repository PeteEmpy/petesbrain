#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Google Ads Asset Library Browser

Universal tool for browsing image assets from any Google Ads account.
Creates an HTML page with images organized by detected categories.

Usage:
    # Browse assets for any Google Ads account
    python3 google-ads-asset-library-browser.py --customer-id 1234567890

    # With manager account
    python3 google-ads-asset-library-browser.py --customer-id 1234567890 --manager-id 9876543210

    # Custom output directory
    python3 google-ads-asset-library-browser.py --customer-id 1234567890 --output-dir /path/to/output

Examples:
    # Smythson UK
    python3 google-ads-asset-library-browser.py --customer-id 8573235780 --manager-id 2569949686

    # Tree2MyDoor
    python3 google-ads-asset-library-browser.py --customer-id 4941701449
"""

import argparse
import os
import sys
import requests
import re
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

# Add the MCP server to path to use its OAuth module
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

# Import the OAuth module
from oauth.google_auth import get_headers_with_auto_token, format_customer_id


def get_headers(manager_id: Optional[str] = None):
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    if manager_id:
        headers['login-customer-id'] = format_customer_id(manager_id)
    return headers


def categorize_asset(name: str) -> str:
    """
    Detect category from asset name using pattern matching.

    Returns category name based on keywords found in the asset name.
    """
    name_lower = name.lower()

    # Check for specific product categories
    if any(word in name_lower for word in ['bag', 'bags', 'tote', 'clutch', 'briefcase', 'backpack', 'handbag']):
        return 'Bags'
    elif any(word in name_lower for word in ['notebook', 'notebooks', 'diary', 'diaries', 'journal', 'planner']):
        return 'Notebooks & Diaries'
    elif any(word in name_lower for word in ['wallet', 'cardholder', 'purse', 'passport']):
        return 'Wallets & Accessories'
    elif any(word in name_lower for word in ['pen', 'pencil', 'writing']):
        return 'Writing Instruments'
    elif any(word in name_lower for word in ['home', 'desk', 'office']):
        return 'Home & Office'
    elif any(word in name_lower for word in ['tech', 'ipad', 'iphone', 'airpod', 'device', 'laptop', 'tablet']):
        return 'Tech Accessories'
    elif any(word in name_lower for word in ['gift', 'stocking', 'xmas', 'christmas', 'holiday']):
        return 'Gifts & Seasonal'
    elif any(word in name_lower for word in ['black friday', 'black_friday', 'bf_', 'blackfriday', 'bfcm']):
        return 'Black Friday'
    elif any(word in name_lower for word in ['ss20', 'ss21', 'ss22', 'ss23', 'ss24', 'aw20', 'aw21', 'aw22', 'aw23', 'aw24']):
        return 'Seasonal Collections'
    elif any(word in name_lower for word in ['mens', 'men\'s', 'male']):
        return 'Men\'s Products'
    elif any(word in name_lower for word in ['womens', 'women\'s', 'female', 'ladies']):
        return 'Women\'s Products'
    elif any(word in name_lower for word in ['logo', 'brand', 'icon']):
        return 'Logos & Branding'
    elif any(word in name_lower for word in ['plant', 'tree', 'flower', 'garden', 'seed']):
        return 'Plants & Nature'
    elif any(word in name_lower for word in ['food', 'coffee', 'drink', 'beverage']):
        return 'Food & Beverage'
    elif 'unnamed' in name_lower or name.strip() == '':
        return 'Unnamed Assets'
    else:
        return 'Other Assets'


def get_all_image_assets(customer_id: str, manager_id: Optional[str] = None) -> List[Dict]:
    """Get all image assets from the account with their URLs."""
    headers = get_headers(manager_id)
    formatted_cid = format_customer_id(customer_id)

    query = """
        SELECT
            asset.id,
            asset.name,
            asset.image_asset.full_size.url,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels,
            asset.image_asset.mime_type
        FROM asset
        WHERE asset.type = 'IMAGE'
        ORDER BY asset.name
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    assets = []
    for result in results:
        asset_data = result.get('asset', {})
        image_data = asset_data.get('imageAsset', {})
        full_size = image_data.get('fullSize', {})

        name = asset_data.get('name', 'Unnamed')
        assets.append({
            'asset_id': str(asset_data.get('id', '')),
            'name': name,
            'url': full_size.get('url', ''),
            'width': full_size.get('widthPixels', 0),
            'height': full_size.get('heightPixels', 0),
            'mime_type': image_data.get('mimeType', 'UNKNOWN'),
            'category': categorize_asset(name),
        })

    return assets


def get_asset_usage(customer_id: str, manager_id: Optional[str] = None) -> Dict[str, List[str]]:
    """Get where each asset is currently used in Performance Max campaigns."""
    headers = get_headers(manager_id)
    formatted_cid = format_customer_id(customer_id)

    query = """
        SELECT
            asset.id,
            campaign.name,
            asset_group.name,
            asset_group_asset.field_type
        FROM asset_group_asset
        WHERE asset_group_asset.field_type IN ('MARKETING_IMAGE', 'SQUARE_MARKETING_IMAGE',
                                                 'PORTRAIT_MARKETING_IMAGE', 'LOGO')
        AND asset_group_asset.status = 'ENABLED'
        AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    usage_map = {}
    for result in results:
        asset_id = str(result.get('asset', {}).get('id', ''))
        asset_group_name = result.get('assetGroup', {}).get('name', '')
        field_type = result.get('assetGroupAsset', {}).get('fieldType', '')

        usage_str = f"{asset_group_name} ({field_type})"

        if asset_id not in usage_map:
            usage_map[asset_id] = []

        usage_map[asset_id].append(usage_str)

    return usage_map


def generate_grouped_html(customer_id: str, assets: List[Dict], usage_map: Dict[str, List[str]]) -> str:
    """Generate HTML page with images grouped by category."""

    # Group assets by category
    categories = defaultdict(list)
    for asset in assets:
        categories[asset['category']].append(asset)

    # Sort categories - put most useful ones first
    category_order = [
        'Bags',
        'Notebooks & Diaries',
        'Wallets & Accessories',
        'Writing Instruments',
        'Home & Office',
        'Tech Accessories',
        'Plants & Nature',
        'Food & Beverage',
        'Men\'s Products',
        'Women\'s Products',
        'Gifts & Seasonal',
        'Black Friday',
        'Seasonal Collections',
        'Logos & Branding',
        'Other Assets',
        'Unnamed Assets',
    ]

    sorted_categories = []
    for cat in category_order:
        if cat in categories:
            sorted_categories.append((cat, categories[cat]))

    # Add any categories not in our predefined order
    for cat, assets_list in sorted(categories.items()):
        if cat not in category_order:
            sorted_categories.append((cat, assets_list))

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Asset Library Browser - {customer_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}

        .header {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 10px;
        }}

        .header-info {{
            color: #7f8c8d;
            font-size: 14px;
        }}

        .controls {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: sticky;
            top: 20px;
            z-index: 100;
        }}

        .controls-row {{
            display: flex;
            gap: 15px;
            align-items: center;
            margin-bottom: 10px;
        }}

        .controls input, .controls select, .controls button {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}

        .controls input {{
            flex: 1;
            max-width: 400px;
        }}

        .controls button {{
            background: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }}

        .controls button:hover {{
            background: #2980b9;
        }}

        .stats {{
            font-size: 13px;
            color: #7f8c8d;
        }}

        .category-section {{
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .category-header {{
            background: #34495e;
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }}

        .category-header:hover {{
            background: #2c3e50;
        }}

        .category-title {{
            font-size: 18px;
            font-weight: 600;
        }}

        .category-count {{
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 14px;
        }}

        .category-content {{
            padding: 20px;
            display: none;
        }}

        .category-content.active {{
            display: block;
        }}

        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}

        .image-card {{
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .image-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .image-container {{
            width: 100%;
            height: 200px;
            background: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}

        .image-loading {{
            color: #95a5a6;
            font-size: 14px;
        }}

        .card-info {{
            padding: 12px;
        }}

        .asset-id {{
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            color: #3498db;
            font-weight: 600;
            margin-bottom: 6px;
            cursor: pointer;
            display: inline-block;
            padding: 4px 8px;
            background: #ecf0f1;
            border-radius: 4px;
        }}

        .asset-id:hover {{
            background: #3498db;
            color: white;
        }}

        .asset-name {{
            font-size: 12px;
            color: #2c3e50;
            margin-bottom: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .dimensions {{
            font-size: 11px;
            color: #7f8c8d;
            margin-bottom: 8px;
        }}

        .usage {{
            font-size: 11px;
            color: #7f8c8d;
            padding-top: 8px;
            border-top: 1px solid #ecf0f1;
        }}

        .usage-count {{
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            margin-right: 4px;
            font-weight: 600;
        }}

        .usage-count.zero {{
            background: #95a5a6;
        }}

        .unused {{
            color: #95a5a6;
        }}

        .notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
        }}

        .notification.show {{
            opacity: 1;
        }}

        .expand-collapse-all {{
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }}

        .expand-collapse-all button {{
            padding: 6px 12px;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Google Ads Asset Library Browser</h1>
        <div class="header-info">
            <div>Customer ID: {customer_id}</div>
            <div>Total Images: {len(assets)} | Grouped by Category</div>
            <div>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
    </div>

    <div class="controls">
        <div class="expand-collapse-all">
            <button onclick="expandAll()">Expand All Categories</button>
            <button onclick="collapseAll()">Collapse All Categories</button>
        </div>
        <div class="controls-row">
            <input type="text" id="search" placeholder="Search by Asset ID, name, or dimensions..."
                   oninput="filterImages()">
            <select id="usage-filter" onchange="filterImages()">
                <option value="all">All images</option>
                <option value="used">Currently used</option>
                <option value="unused">Not used</option>
            </select>
        </div>
        <div class="stats">
            Showing <span id="shown-count">{len(assets)}</span> of {len(assets)} images
        </div>
    </div>

    <div id="categories">
"""

    # Generate category sections
    for category_name, category_assets in sorted_categories:
        category_id = category_name.replace(' ', '-').replace('\'', '').replace('&', 'and').lower()

        html += f"""
    <div class="category-section" data-category="{category_id}">
        <div class="category-header" onclick="toggleCategory('{category_id}')">
            <span class="category-title">{category_name}</span>
            <span class="category-count" id="count-{category_id}">{len(category_assets)} images</span>
        </div>
        <div class="category-content" id="content-{category_id}">
            <div class="image-grid">
"""

        # Add image cards for this category
        for asset in category_assets:
            asset_id = asset['asset_id']
            name = asset['name']
            dimensions = f"{asset['width']}×{asset['height']}"
            url = asset['url']
            usage = usage_map.get(asset_id, [])
            usage_count = len(usage)

            usage_html = ''
            if usage:
                usage_list = '<br>'.join(usage[:5])
                if len(usage) > 5:
                    usage_list += f'<br>...and {len(usage) - 5} more'
                usage_html = f'<div class="usage"><span class="usage-count">{usage_count}</span>{usage_list}</div>'
            else:
                usage_html = '<div class="usage unused"><span class="usage-count zero">0</span>Not currently used</div>'

            # Escape quotes in name for HTML attributes
            name_escaped = name.replace('"', '&quot;').replace("'", '&#39;')

            html += f"""
                <div class="image-card" data-id="{asset_id}" data-name="{name_escaped}"
                     data-dimensions="{dimensions}" data-usage="{usage_count}"
                     data-category="{category_id}">
                    <div class="image-container">
                        <img src="{url}" alt="{name_escaped}" loading="lazy"
                             onerror="this.parentElement.innerHTML='<div class=\\'image-loading\\'>Image unavailable</div>'">
                    </div>
                    <div class="card-info">
                        <div class="asset-id" onclick="copyAssetId('{asset_id}')"
                             title="Click to copy Asset ID">{asset_id}</div>
                        <div class="asset-name" title="{name_escaped}">{name}</div>
                        <div class="dimensions">{dimensions}</div>
                        {usage_html}
                    </div>
                </div>
"""

        html += """
            </div>
        </div>
    </div>
"""

    html += """
    </div>

    <div class="notification" id="notification">
        Asset ID copied to clipboard!
    </div>

    <script>
        const allCards = document.querySelectorAll('.image-card');
        const allCategories = document.querySelectorAll('.category-section');

        function copyAssetId(assetId) {
            navigator.clipboard.writeText(assetId).then(() => {
                showNotification();
            });
        }

        function showNotification() {
            const notif = document.getElementById('notification');
            notif.classList.add('show');
            setTimeout(() => {
                notif.classList.remove('show');
            }, 2000);
        }

        function toggleCategory(categoryId) {
            const content = document.getElementById('content-' + categoryId);
            content.classList.toggle('active');
        }

        function expandAll() {
            document.querySelectorAll('.category-content').forEach(content => {
                content.classList.add('active');
            });
        }

        function collapseAll() {
            document.querySelectorAll('.category-content').forEach(content => {
                content.classList.remove('active');
            });
        }

        function filterImages() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const usageFilter = document.getElementById('usage-filter').value;

            const categoryCounts = {};
            let totalShownCount = 0;

            allCards.forEach(card => {
                const id = card.dataset.id.toLowerCase();
                const name = card.dataset.name.toLowerCase();
                const dimensions = card.dataset.dimensions.toLowerCase();
                const usage = parseInt(card.dataset.usage);
                const category = card.dataset.category;

                const matchesSearch = !searchTerm ||
                    id.includes(searchTerm) ||
                    name.includes(searchTerm) ||
                    dimensions.includes(searchTerm);

                const matchesUsage =
                    usageFilter === 'all' ||
                    (usageFilter === 'used' && usage > 0) ||
                    (usageFilter === 'unused' && usage === 0);

                if (matchesSearch && matchesUsage) {
                    card.style.display = '';
                    categoryCounts[category] = (categoryCounts[category] || 0) + 1;
                    totalShownCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Update category counts
            allCategories.forEach(section => {
                const categoryId = section.dataset.category;
                const count = categoryCounts[categoryId] || 0;
                const countEl = document.getElementById('count-' + categoryId);
                if (countEl) {
                    countEl.textContent = count + ' images';
                }

                // Hide categories with no visible images
                if (count === 0) {
                    section.style.display = 'none';
                } else {
                    section.style.display = '';
                }
            });

            document.getElementById('shown-count').textContent = totalShownCount;
        }

        // Auto-expand first category on load
        window.addEventListener('load', () => {
            const firstCategory = document.querySelector('.category-content');
            if (firstCategory) {
                firstCategory.classList.add('active');
            }
        });
    </script>
</body>
</html>
"""

    return html


def export_asset_library(customer_id: str, manager_id: Optional[str] = None,
                         output_dir: Optional[str] = None):
    """Export asset library browser for a Google Ads account."""

    print(f"\n{'='*80}")
    print(f"GOOGLE ADS ASSET LIBRARY BROWSER")
    print(f"Customer ID: {customer_id}")
    if manager_id:
        print(f"Manager ID: {manager_id}")
    print(f"{'='*80}")

    # Get all image assets
    print(f"\nQuerying image assets from Google Ads...")
    assets = get_all_image_assets(customer_id, manager_id)
    print(f"  Found {len(assets)} image assets")

    # Get asset usage
    print(f"\nQuerying where assets are currently used...")
    usage_map = get_asset_usage(customer_id, manager_id)
    print(f"  Found usage data for {len(usage_map)} assets")

    # Generate HTML
    print(f"\nGenerating grouped HTML page...")
    html = generate_grouped_html(customer_id, assets, usage_map)

    # Determine output directory
    if output_dir is None:
        output_dir = '/Users/administrator/Documents/PetesBrain/output'

    os.makedirs(output_dir, exist_ok=True)

    # Save to file
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f"asset-library-browser-{customer_id}-{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Saved to: {filepath}")

    print(f"\n{'='*80}")
    print(f"✅ ASSET LIBRARY BROWSER CREATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Customer ID: {customer_id}")
    print(f"Total Images: {len(assets)}")
    print(f"HTML File: {filepath}")
    print(f"\nOpening in browser...")
    print(f"{'='*80}\n")

    # Open in browser
    os.system(f'open "{filepath}"')


def main():
    parser = argparse.ArgumentParser(
        description='Google Ads Asset Library Browser - Browse image assets from any Google Ads account',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Browse assets for a single account
  %(prog)s --customer-id 1234567890

  # Browse with manager account access
  %(prog)s --customer-id 1234567890 --manager-id 9876543210

  # Custom output directory
  %(prog)s --customer-id 1234567890 --output-dir /path/to/output

  # Smythson UK
  %(prog)s --customer-id 8573235780 --manager-id 2569949686
        """
    )
    parser.add_argument(
        '--customer-id',
        required=True,
        help='Google Ads customer ID (10 digits, no dashes)'
    )
    parser.add_argument(
        '--manager-id',
        help='Manager account ID (if accessing via manager account)'
    )
    parser.add_argument(
        '--output-dir',
        help='Output directory for HTML file (default: ~/Documents/PetesBrain/output)'
    )
    args = parser.parse_args()

    print(f"\nGoogle Ads Asset Library Browser")
    print(f"Started: {datetime.now().isoformat()}")

    export_asset_library(args.customer_id, args.manager_id, args.output_dir)

    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
