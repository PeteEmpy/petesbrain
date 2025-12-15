#!/usr/bin/env python3
import json
from collections import Counter

data = json.load(open('data/product_feed_history/BrightMinds/2025-12-14.json'))
products = data['products']

print(f'Total products: {len(products)}')
print(f'Product data type: {type(products)}')

if isinstance(products, list):
    sample = products[0]
    print('\nSample product:')
    import pprint
    pprint.pprint(sample)

    avail = [p.get('availability', 'MISSING') for p in products]
    counts = Counter(avail)
    print(f'\n\nAvailability distribution:')
    pprint.pprint(dict(counts))

    out_of_stock = [p for p in products if p.get('availability') == 'out of stock']
    print(f'\n\nOut of stock products: {len(out_of_stock)}')
    if out_of_stock:
        print('Sample out of stock:')
        for p in out_of_stock[:5]:
            pid = p.get('product_id', '')
            # Normalize product ID for matching with Google Ads
            if 'shopify_GB_' in pid:
                normalized = pid.split('_')[-1]  # Get variant ID
            else:
                normalized = pid
            print(f"  {normalized}: {p.get('title', 'N/A')[:60]}")
else:
    # It's a dict
    print('\nProducts is a dict with keys:', list(products.keys())[:10])
    first_key = list(products.keys())[0]
    print(f'\nSample product (key={first_key}):')
    import pprint
    pprint.pprint(products[first_key])
