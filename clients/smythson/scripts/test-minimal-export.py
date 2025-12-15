#!/usr/bin/env python3
"""Create minimal test export with just first 4 RSAs to debug"""

import csv

# Create minimal test file
rows = [
    # Header
    ['Action', 'Customer ID', 'Campaign', 'Ad group', 'Ad ID', 'Headline 1', 'Headline 2', 'Headline 3', 'Description 1', 'Description 2', 'Final URL'],

    # Test rows - just the first 4 from UK
    ['Edit', '8573235780', 'SMY | UK | Search | Brand Exact', 'UK - Brand', '784157361259',
     'Smythson of Bond Street™', 'British heritage since 1887', 'Shop luxury leather pieces',
     'Make the ordinary extraordinary', 'Discover the perfect gift', 'https://www.smythson.com/uk/'],

    ['Edit', '8573235780', 'SMY | UK | Search | Brand Exact', 'UK - Brand - Sale', '784408654524',
     'Smythson of Bond Street™', 'British heritage since 1887', 'Shop luxury leather pieces',
     'Make the ordinary extraordinary', 'Discover the perfect gift', 'https://www.smythson.com/uk/'],

    ['Edit', '8573235780', 'SMY | UK | Search | Brand Plus', 'UK - semi-brand - home - desk accessories - blotters', '784228048462',
     'Smythson of Bond Street™', 'Luxury leather blotters', 'Shop luxury leather blotters',
     'Make the ordinary extraordinary', 'Discover the perfect gift', 'https://www.smythson.com/uk/'],

    ['Edit', '8573235780', 'SMY | UK | Search | Brand Plus', 'UK - semi-brand - home - games', '784228048447',
     'Smythson of Bond Street™', 'Luxury games & playing cards', 'Shop games & playing cards',
     'Discover classic artisan sets', 'Ensure every event is memorable', 'https://www.smythson.com/uk/']
]

# Write test file
with open('test-minimal-uk.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("✅ Created test-minimal-uk.csv with 4 RSAs")
print("\nTest with this file first to see which ones work:")
print("  1. Ad ID 784157361259 - Brand Exact / UK - Brand")
print("  2. Ad ID 784408654524 - Brand Exact / UK - Brand - Sale")
print("  3. Ad ID 784228048462 - Brand Plus / desk accessories")
print("  4. Ad ID 784228048447 - Brand Plus / games")
print("\nIf these 4 work, we can identify the pattern of what's failing.")