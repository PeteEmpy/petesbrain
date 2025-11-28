#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Export Smythson image asset catalog to browsable HTML page.

Creates an HTML page with all images displayed as thumbnails, searchable and filterable.
You can see all images at once and easily copy Asset IDs.

Usage:
    python3 export-image-catalog-html.py --region uk
    python3 export-image-catalog-html.py --region us
"""

import argparse
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List

# Add the MCP server to path to use its OAuth module
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

# Import the OAuth module
from oauth.google_auth import get_headers_with_auto_token, format_customer_id

# Configuration
MANAGER_ID = '2569949686'

REGIONS = {
    'uk': {
        'customer_id': '8573235780',
        'name': 'UK'
    },
    'us': {
        'customer_id': '7808690871',
        'name': 'US'
    },
    'eur': {
        'customer_id': '7679616761',
        'name': 'EUR'
    },
    'row': {
        'customer_id': '5556710725',
        'name': 'ROW'
    },
}


def get_headers():
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(MANAGER_ID)
    return headers


def get_all_image_assets(customer_id: str) -> List[Dict]:
    """Get all image assets from the account with their URLs."""
    headers = get_headers()
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

        assets.append({
            'asset_id': str(asset_data.get('id', '')),
            'name': asset_data.get('name', 'Unnamed'),
            'url': full_size.get('url', ''),
            'width': full_size.get('widthPixels', 0),
            'height': full_size.get('heightPixels', 0),
            'mime_type': image_data.get('mimeType', 'UNKNOWN'),
        })

    return assets


def get_asset_usage(customer_id: str) -> Dict[str, List[str]]:
    """Get where each asset is currently used."""
    headers = get_headers()
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

        if asset_id not in usage_map:
            usage_map[asset_id] = []

        if asset_group_name not in usage_map[asset_id]:
            usage_map[asset_id].append(asset_group_name)

    return usage_map


def generate_html(region_name: str, assets: List[Dict], usage_map: Dict[str, List[str]]) -> str:
    """Generate HTML page with image catalog."""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Smythson {region_name} Image Catalog</title>
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
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}

        .stats {{
            color: #666;
            font-size: 14px;
        }}

        .controls {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .search-box {{
            flex: 1;
            min-width: 250px;
        }}

        .search-box input {{
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #3498db;
        }}

        .filter-group {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .filter-group label {{
            font-size: 14px;
            color: #666;
        }}

        .filter-group select {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}

        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}

        .image-card {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .image-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .image-container {{
            width: 100%;
            height: 200px;
            background: #f8f8f8;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }}

        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}

        .image-loading {{
            color: #999;
            font-size: 12px;
        }}

        .card-info {{
            padding: 15px;
        }}

        .asset-id {{
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
            font-family: 'Monaco', 'Courier New', monospace;
            cursor: pointer;
            user-select: all;
        }}

        .asset-id:hover {{
            color: #3498db;
        }}

        .asset-name {{
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .dimensions {{
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
        }}

        .usage {{
            font-size: 11px;
            color: #666;
            padding: 8px;
            background: #f8f8f8;
            border-radius: 4px;
            margin-top: 8px;
            max-height: 60px;
            overflow-y: auto;
        }}

        .usage.unused {{
            color: #999;
            font-style: italic;
        }}

        .usage-count {{
            display: inline-block;
            background: #3498db;
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 3px;
            margin-right: 5px;
        }}

        .usage-count.zero {{
            background: #95a5a6;
        }}

        .copy-notification {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 15px 20px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
        }}

        .copy-notification.show {{
            opacity: 1;
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Smythson {region_name} Image Catalog</h1>
        <div class="stats">
            Generated: {timestamp} |
            Total Images: <span id="total-count">{len(assets)}</span> |
            Showing: <span id="shown-count">{len(assets)}</span>
        </div>
    </div>

    <div class="controls">
        <div class="search-box">
            <input type="text" id="search" placeholder="Search by Asset ID, name, or dimensions..."
                   oninput="filterImages()">
        </div>
        <div class="filter-group">
            <label for="usage-filter">Usage:</label>
            <select id="usage-filter" onchange="filterImages()">
                <option value="all">All Images</option>
                <option value="used">Used Only</option>
                <option value="unused">Unused Only</option>
            </select>
        </div>
        <div class="filter-group">
            <label for="sort">Sort by:</label>
            <select id="sort" onchange="sortImages()">
                <option value="id">Asset ID</option>
                <option value="name">Name</option>
                <option value="usage">Usage (Most Used)</option>
                <option value="dimensions">Dimensions</option>
            </select>
        </div>
    </div>

    <div class="gallery" id="gallery">
"""

    # Add image cards
    for asset in assets:
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

        html += f"""
        <div class="image-card" data-id="{asset_id}" data-name="{name}"
             data-dimensions="{dimensions}" data-usage="{usage_count}">
            <div class="image-container">
                <img src="{url}" alt="{name}" loading="lazy"
                     onerror="this.parentElement.innerHTML='<div class=\\'image-loading\\'>Image unavailable</div>'">
            </div>
            <div class="card-info">
                <div class="asset-id" onclick="copyAssetId('{asset_id}')"
                     title="Click to copy Asset ID">{asset_id}</div>
                <div class="asset-name" title="{name}">{name}</div>
                <div class="dimensions">{dimensions}</div>
                {usage_html}
            </div>
        </div>
"""

    html += """
    </div>

    <div class="copy-notification" id="copy-notification">
        ✓ Asset ID copied to clipboard!
    </div>

    <script>
        let allCards = [];

        window.onload = function() {
            allCards = Array.from(document.querySelectorAll('.image-card'));
        };

        function copyAssetId(assetId) {
            navigator.clipboard.writeText(assetId).then(() => {
                showNotification();
            });
        }

        function showNotification() {
            const notification = document.getElementById('copy-notification');
            notification.classList.add('show');
            setTimeout(() => {
                notification.classList.remove('show');
            }, 2000);
        }

        function filterImages() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const usageFilter = document.getElementById('usage-filter').value;
            const gallery = document.getElementById('gallery');

            let shownCount = 0;

            allCards.forEach(card => {
                const id = card.dataset.id.toLowerCase();
                const name = card.dataset.name.toLowerCase();
                const dimensions = card.dataset.dimensions.toLowerCase();
                const usage = parseInt(card.dataset.usage);

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
                    shownCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            document.getElementById('shown-count').textContent = shownCount;

            if (shownCount === 0) {
                if (!document.querySelector('.no-results')) {
                    gallery.innerHTML = '<div class="no-results">No images match your filters</div>';
                }
            } else {
                const noResults = document.querySelector('.no-results');
                if (noResults) {
                    noResults.remove();
                }
            }
        }

        function sortImages() {
            const sortBy = document.getElementById('sort').value;
            const gallery = document.getElementById('gallery');

            allCards.sort((a, b) => {
                if (sortBy === 'id') {
                    return a.dataset.id.localeCompare(b.dataset.id);
                } else if (sortBy === 'name') {
                    return a.dataset.name.localeCompare(b.dataset.name);
                } else if (sortBy === 'usage') {
                    return parseInt(b.dataset.usage) - parseInt(a.dataset.usage);
                } else if (sortBy === 'dimensions') {
                    return a.dataset.dimensions.localeCompare(b.dataset.dimensions);
                }
            });

            allCards.forEach(card => gallery.appendChild(card));
        }
    </script>
</body>
</html>
"""

    return html


def export_region_catalog(region: str):
    """Export image catalog for a region to HTML file."""
    customer_id = REGIONS[region]['customer_id']
    region_name = REGIONS[region]['name']

    print(f"\n{'='*80}")
    print(f"EXPORTING IMAGE CATALOG: {region_name}")
    print(f"Customer ID: {customer_id}")
    print(f"{'='*80}")

    # Get all image assets
    print(f"\nQuerying image assets from Google Ads...")
    assets = get_all_image_assets(customer_id)
    print(f"  Found {len(assets)} image assets")

    # Get asset usage
    print(f"\nQuerying where assets are currently used...")
    usage_map = get_asset_usage(customer_id)
    print(f"  Found usage data for {len(usage_map)} assets")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html_content = generate_html(region_name, assets, usage_map)

    # Save HTML file
    output_dir = '/Users/administrator/Documents/PetesBrain/clients/smythson/output'
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f"image-catalog-{region}-{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  Saved to: {filepath}")

    print(f"\n{'='*80}")
    print(f"✅ IMAGE CATALOG CREATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Region: {region_name}")
    print(f"Total Images: {len(assets)}")
    print(f"HTML File: {filepath}")
    print(f"\nOpening in browser...")
    print(f"{'='*80}\n")

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='Export Smythson image asset catalog to HTML'
    )
    parser.add_argument(
        '--region',
        required=True,
        choices=['uk', 'us', 'eur', 'row'],
        help='Region to export image catalog for'
    )
    args = parser.parse_args()

    print(f"\nSmythson Image Catalog HTML Export Tool")
    print(f"Started: {datetime.now().isoformat()}")

    filepath = export_region_catalog(args.region)

    # Open in browser
    import subprocess
    subprocess.run(['open', filepath])

    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
