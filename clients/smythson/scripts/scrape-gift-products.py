#!/usr/bin/env python3
"""
Scrape Smythson gift product pages and create supplemental feed for Custom Label 4.

This script:
1. Scrapes product pages for "Gifts for Him" and "Gifts for Her"
2. Handles pagination to capture all products
3. Extracts product IDs from the page
4. Creates a CSV with columns: id, custom_label_4
5. Populates with product IDs and appropriate gender labels

Usage:
    python3 scrape-gift-products.py
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime

# URLs to scrape
URLS = {
    'Gifts for Him': 'https://www.smythson.com/uk/search/?prefn1=gender&prefv1=For%20Him&q=gifts&start=0&sz=36',
    'Gifts for Her': 'https://www.smythson.com/uk/search/?prefn1=gender&prefv1=For%20Her&q=gifts&start=0&sz=36'
}

def scrape_product_ids(url, label):
    """
    Scrape all product IDs from a Smythson page, handling pagination.

    Args:
        url: The URL to scrape
        label: The custom label to apply (e.g., "Gifts for Him")

    Returns:
        List of tuples: [(product_id, label), ...]
    """
    products = []
    start = 0
    sz = 36  # Products per page

    print(f"\n🔍 Scraping: {label}")
    print(f"📍 URL: {url}")

    while True:
        # Construct paginated URL
        paginated_url = re.sub(r'start=\d+', f'start={start}', url)

        print(f"   Start={start}...", end=" ")

        try:
            # Fetch the page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(paginated_url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Look for product IDs in various possible locations
            page_products = []

            # Method 1: Look for data-itemid attributes (common in product grids)
            product_elements = soup.find_all(attrs={'data-itemid': True})
            for elem in product_elements:
                product_id = elem.get('data-itemid')
                if product_id and product_id not in [p[0] for p in page_products]:
                    page_products.append((product_id, label))

            # Method 2: Look for data-product-id attributes
            if not page_products:
                product_elements = soup.find_all(attrs={'data-product-id': True})
                for elem in product_elements:
                    product_id = elem.get('data-product-id')
                    if product_id and product_id not in [p[0] for p in page_products]:
                        page_products.append((product_id, label))

            # Method 3: Look for product URLs with IDs in links
            if not page_products:
                product_links = soup.find_all('a', href=re.compile(r'/[\w-]+-(\d{6,})\.html'))
                for link in product_links:
                    href = link.get('href', '')
                    match = re.search(r'-(\d{6,})\.html', href)
                    if match:
                        product_id = match.group(1)
                        if product_id not in [p[0] for p in page_products]:
                            page_products.append((product_id, label))

            # Method 4: Look in the page HTML for product data
            if not page_products:
                # Try to find product tiles/cards
                tiles = soup.find_all(['div', 'article', 'li'], class_=re.compile(r'product', re.I))
                for tile in tiles:
                    # Look for ID in various possible attributes
                    for attr in ['data-itemid', 'data-pid', 'data-product-id', 'data-sku', 'id']:
                        if tile.get(attr):
                            product_id = str(tile.get(attr)).strip()
                            # Extract numeric ID if present
                            numeric_match = re.search(r'\d{6,}', product_id)
                            if numeric_match:
                                product_id = numeric_match.group()
                                if product_id not in [p[0] for p in page_products]:
                                    page_products.append((product_id, label))
                                    break

            if not page_products:
                print(f"❌ No products found")
                break

            print(f"✅ Found {len(page_products)} products")
            products.extend(page_products)

            # Check if there are more pages
            # Look for "Show More" or next page indicators
            total_count = soup.find(class_=re.compile(r'result.*count|product.*count', re.I))
            if total_count:
                count_text = total_count.get_text()
                count_match = re.search(r'(\d+)\s*(?:results?|products?)', count_text, re.I)
                if count_match:
                    total = int(count_match.group(1))
                    if start + sz >= total:
                        print(f"   📊 Total products found: {len(products)}")
                        break

            # Move to next page
            start += sz
            time.sleep(1)  # Be polite to the server

            # Safety limit - max 2000 products (should be more than enough)
            if start > 2000:
                print(f"   ⚠️  Safety limit reached (2000+ products)")
                break

        except requests.RequestException as e:
            print(f"❌ Error: {e}")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            break

    return products


def create_csv(products, filename="Smythson_Custom_Label_4_Gifts.csv"):
    """
    Create a CSV file with the product data.

    Args:
        products: List of tuples [(product_id, label), ...]
        filename: Output filename

    Returns:
        Full path to CSV file
    """
    print(f"\n📊 Creating CSV: {filename}")

    # Prepare data
    rows = [['id', 'custom_label_4']]  # Header row

    # Track which products appear in which categories
    product_labels = {}
    for product_id, label in products:
        if product_id not in product_labels:
            product_labels[product_id] = set()
        product_labels[product_id].add(label)

    # Create final label based on which categories each product appears in
    for product_id, labels in product_labels.items():
        if len(labels) > 1:
            # Product appears in both - use combined label
            final_label = "Gifts for Him & Her"
        else:
            # Product only in one category
            final_label = list(labels)[0]
        rows.append([str(product_id), final_label])

    print(f"   Total unique products: {len(rows) - 1}")
    print(f"   - Gifts for Him: {sum(1 for r in rows[1:] if r[1] == 'Gifts for Him')}")
    print(f"   - Gifts for Her: {sum(1 for r in rows[1:] if r[1] == 'Gifts for Her')}")
    print(f"   - Gifts for Him & Her: {sum(1 for r in rows[1:] if r[1] == 'Gifts for Him & Her')}")

    # Save to CSV
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
    csv_path = f'/Users/administrator/Documents/PetesBrain/clients/smythson/product-feeds/Smythson_Custom_Label_4_Gifts_{timestamp}.csv'

    with open(csv_path, 'w') as f:
        for row in rows:
            f.write(','.join(row) + '\n')

    print(f"✅ CSV saved: {csv_path}")
    return csv_path


def main():
    """Main execution function."""
    print("=" * 60)
    print("Smythson Gift Products Scraper")
    print("Custom Label 4: Gifts for Him / Gifts for Her")
    print("=" * 60)

    all_products = []

    # Scrape each URL
    for label, url in URLS.items():
        products = scrape_product_ids(url, label)
        all_products.extend(products)
        print(f"   Subtotal: {len(products)} products")

    if not all_products:
        print("\n❌ No products found. Please check:")
        print("   1. URLs are correct")
        print("   2. Website structure hasn't changed")
        print("   3. Internet connection is working")
        return

    # Create CSV
    csv_path = create_csv(all_products)

    print("\n" + "=" * 60)
    print("✅ COMPLETE")
    print("=" * 60)
    print(f"\n📁 CSV file created: {csv_path}")
    print("\n📋 Next steps:")
    print("   1. Review the CSV file")
    print("   2. Upload to Google Sheets")
    print("   3. Add to Merchant Center as supplemental feed")
    print("   4. Set feed to update 'custom_label_4'")
    print("   5. Verify products show the new label in GMC")


if __name__ == '__main__':
    main()
