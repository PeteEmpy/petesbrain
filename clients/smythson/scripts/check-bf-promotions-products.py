#!/usr/bin/env python3
"""
Check if Black Friday promotion product IDs exist in Smythson UK (GB) feed
"""

import csv
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from google.ads.googleads.client import GoogleAdsClient

# Initialize Google Ads client
client = GoogleAdsClient.load_from_storage()
ga_service = client.get_service("GoogleAdsService")

CUSTOMER_ID = "8573235780"
MANAGER_ID = "2569949686"

def load_promotion_ids(csv_file):
    """Load product IDs from Black Friday promotions CSV"""
    product_ids = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row['Item Id'].strip()
            if item_id:
                product_ids.append(item_id)
    return product_ids

def check_products_in_batches(product_ids, batch_size=100):
    """Check products in batches to avoid query size limits"""

    total = len(product_ids)
    gb_products = []
    non_gb_products = []
    missing_products = set(product_ids)

    print(f"Checking {total} product IDs in batches of {batch_size}...")
    print()

    for i in range(0, total, batch_size):
        batch = product_ids[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size

        print(f"Batch {batch_num}/{total_batches}: Checking {len(batch)} IDs...")

        # Create IN clause for this batch
        ids_str = "', '".join(batch)

        query = f"""
            SELECT
                shopping_product.merchant_center_id,
                shopping_product.item_id,
                shopping_product.title,
                shopping_product.resource_name,
                shopping_product.status
            FROM shopping_product
            WHERE
                shopping_product.item_id IN ('{ids_str}')
                AND shopping_product.merchant_center_id = '102535465'
        """

        try:
            response = ga_service.search(
                customer_id=CUSTOMER_ID,
                query=query,
                login_customer_id=MANAGER_ID
            )

            for row in response:
                product = row.shopping_product
                item_id = product.item_id
                resource_name = product.resource_name

                # Remove from missing set
                if item_id in missing_products:
                    missing_products.remove(item_id)

                # Check if it's a GB product
                if '~en~GB~' in resource_name or '~GB~' in resource_name:
                    gb_products.append({
                        'item_id': item_id,
                        'title': product.title,
                        'resource_name': resource_name,
                        'status': product.status.name
                    })
                else:
                    # Extract market code from resource name
                    parts = resource_name.split('~')
                    market = parts[-2] if len(parts) >= 2 else 'UNKNOWN'

                    non_gb_products.append({
                        'item_id': item_id,
                        'title': product.title,
                        'market': market,
                        'resource_name': resource_name,
                        'status': product.status.name
                    })

        except Exception as e:
            print(f"  ❌ Error in batch {batch_num}: {e}")
            continue

    print()
    return gb_products, non_gb_products, list(missing_products)

def main():
    csv_file = '/Users/administrator/Documents/PetesBrain/clients/smythson/documents/BlackFridayPromotions2025.f406579615.gb.en.u1763467357616000.feeduploadreport.csv'

    print("=" * 80)
    print("SMYTHSON BLACK FRIDAY PROMOTIONS - PRODUCT AVAILABILITY CHECK")
    print("=" * 80)
    print()

    # Load product IDs
    product_ids = load_promotion_ids(csv_file)
    print(f"Loaded {len(product_ids)} product IDs from promotions feed")
    print()

    # Check products
    gb_products, non_gb_products, missing_products = check_products_in_batches(product_ids)

    # Print results
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()

    print(f"✅ Products found in GB (UK) feed: {len(gb_products)}")
    print(f"❌ Products found in OTHER markets only: {len(non_gb_products)}")
    print(f"⚠️  Products not found in ANY market: {len(missing_products)}")
    print(f"📊 Total products checked: {len(product_ids)}")
    print()

    # Show GB products (if any)
    if gb_products:
        print("=" * 80)
        print("GB PRODUCTS FOUND (Can accept promotions)")
        print("=" * 80)
        for p in gb_products[:20]:  # Show first 20
            print(f"  {p['item_id']}: {p['title']} [{p['status']}]")
        if len(gb_products) > 20:
            print(f"  ... and {len(gb_products) - 20} more")
        print()

    # Show market breakdown of non-GB products
    if non_gb_products:
        print("=" * 80)
        print("MARKET BREAKDOWN (Non-GB products)")
        print("=" * 80)

        market_counts = {}
        for p in non_gb_products:
            market = p['market']
            market_counts[market] = market_counts.get(market, 0) + 1

        for market, count in sorted(market_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {market}: {count} products")
        print()

        # Show sample of non-GB products
        print("Sample non-GB products (first 10):")
        for p in non_gb_products[:10]:
            print(f"  {p['item_id']} ({p['market']}): {p['title']}")
        print()

    # Show missing products sample
    if missing_products:
        print("=" * 80)
        print("PRODUCTS NOT FOUND IN MERCHANT CENTRE")
        print("=" * 80)
        print("Sample (first 20):")
        for pid in sorted(missing_products)[:20]:
            print(f"  {pid}")
        if len(missing_products) > 20:
            print(f"  ... and {len(missing_products) - 20} more")
        print()

    # Final verdict
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    if len(gb_products) == 0:
        print("❌ NONE of the promotion product IDs exist in the GB (UK) feed.")
        print("   All 598 promotions will fail with 'Offer does not exist' error.")
    else:
        percentage = (len(gb_products) / len(product_ids)) * 100
        print(f"⚠️  Only {len(gb_products)}/{len(product_ids)} ({percentage:.1f}%) products found in GB feed.")
        print(f"   {len(product_ids) - len(gb_products)} promotions will fail.")
    print("=" * 80)

if __name__ == '__main__':
    main()
