#!/usr/bin/env python3
"""
Query performance for Bagpus WheatyBags product.
Fetches all WheatyBags products and filters for 'bagpus' in title.
"""

import json
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

GOOGLE_ADS_CONFIG = Path.home() / "google-ads.yaml"
CUSTOMER_ID = "6281395727"  # WheatyBags (Clear Prospects account)

def fetch_bagpus_product():
    """Fetch performance data for Bagpus product"""

    client = GoogleAdsClient.load_from_storage(str(GOOGLE_ADS_CONFIG))
    ga_service = client.get_service("GoogleAdsService")

    # Query all products for last 30 days
    query = """
        SELECT
          segments.product_item_id,
          segments.product_title,
          segments.product_custom_attribute4,
          metrics.impressions,
          metrics.clicks,
          metrics.conversions,
          metrics.cost_micros,
          metrics.conversions_value
        FROM shopping_performance_view
        WHERE segments.date DURING LAST_30_DAYS
          AND metrics.impressions > 0
    """

    try:
        request = client.get_type("SearchGoogleAdsStreamRequest")
        request.customer_id = CUSTOMER_ID
        request.query = query

        stream = ga_service.search_stream(request=request)

        # Aggregate by product (GAQL returns daily rows)
        products = {}
        all_titles = set()

        for batch in stream:
            for row in batch.results:
                product_id = row.segments.product_item_id
                title = row.segments.product_title
                label = getattr(row.segments, 'product_custom_attribute4', None)

                if product_id and title:
                    all_titles.add(title)

                # Filter for products containing "bagpuss" or "wheat"
                title_lower = title.lower()
                if product_id and title and ('bagpuss' in title_lower or 'wheat' in title_lower):

                    if product_id not in products:
                        products[product_id] = {
                            'product_id': product_id,
                            'title': title,
                            'label': label,
                            'impressions': 0,
                            'clicks': 0,
                            'conversions': 0,
                            'cost': 0,
                            'revenue': 0
                        }

                    products[product_id]['impressions'] += row.metrics.impressions
                    products[product_id]['clicks'] += row.metrics.clicks
                    products[product_id]['conversions'] += row.metrics.conversions
                    products[product_id]['cost'] += row.metrics.cost_micros / 1_000_000
                    products[product_id]['revenue'] += row.metrics.conversions_value

        if not products:
            print("\n❌ No wheat/bagpuss products found")
            return None

        # Filter for just Bagpuss products
        bagpuss_products = {pid: data for pid, data in products.items() if 'bagpuss' in data['title'].lower()}

        if bagpuss_products:
            print(f"\n{'='*80}")
            print(f"BAGPUSS WHEATYBAGS PRODUCT PERFORMANCE (Last 30 Days)")
            print(f"{'='*80}\n")
            products = bagpuss_products
        else:
            print(f"\n{'='*80}")
            print(f"NO BAGPUSS PRODUCTS FOUND - Showing all Wheat products")
            print(f"{'='*80}\n")
            print(f"Found {len(products)} wheat products. First 10 titles:")
            for i, (pid, data) in enumerate(list(products.items())[:10]):
                print(f"  {i+1}. {data['title']}")
            print()

        for prod in products.values():
            ctr = (prod['clicks'] / prod['impressions'] * 100) if prod['impressions'] > 0 else 0
            conv_rate = (prod['conversions'] / prod['clicks'] * 100) if prod['clicks'] > 0 else 0
            roas = (prod['revenue'] / prod['cost'] * 100) if prod['cost'] > 0 else 0

            print(f"Product ID: {prod['product_id']}")
            print(f"Title: {prod['title']}")
            print(f"Label: {prod['label'] or 'None'}")
            print(f"\nPerformance Metrics:")
            print(f"  Impressions: {prod['impressions']:,}")
            print(f"  Clicks: {prod['clicks']:,}")
            print(f"  CTR: {ctr:.2f}%")
            print(f"  Conversions: {prod['conversions']:.1f}")
            print(f"  Conversion Rate: {conv_rate:.2f}%")
            print(f"  Cost: £{prod['cost']:.2f}")
            print(f"  Revenue: £{prod['revenue']:.2f}")
            print(f"  ROAS: {roas:.0f}%")
            print(f"\n{'='*80}\n")

        return products

    except GoogleAdsException as ex:
        print(f"❌ Google Ads API Error:")
        for error in ex.failure.errors:
            print(f"  {error.message}")
        return None

if __name__ == "__main__":
    fetch_bagpus_product()
