#!/usr/bin/env python3
"""
Test URL analysis to see what's being generated
"""

from ad_copy_generator import AdCopyGenerator
import json

# Test with a simple example
test_url = "https://example.com"

print(f"Testing with URL: {test_url}")
print("="*80)

generator = AdCopyGenerator(test_url)

# Create mock content to test (since example.com is minimal)
mock_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Premium Running Shoes - Nike Air Zoom | Nike Store</title>
    <meta name="description" content="Experience ultimate comfort with Nike Air Zoom running shoes. Lightweight design with advanced cushioning.">
</head>
<body>
    <h1>Nike Air Zoom Pegasus 40</h1>
    <h2>Key Features</h2>
    <ul>
        <li>Advanced cushioning technology</li>
        <li>Lightweight breathable mesh</li>
        <li>Responsive foam sole</li>
        <li>Waterproof construction</li>
        <li>Professional-grade performance</li>
    </ul>
    <h2>Benefits</h2>
    <ul>
        <li>Comfortable all-day wear</li>
        <li>Guaranteed satisfaction</li>
        <li>Free shipping on all orders</li>
        <li>Easy returns within 30 days</li>
    </ul>
    <p>
        Transform your running experience with our premium Nike Air Zoom Pegasus 40.
        These professional running shoes feature advanced technology for optimal performance.
    </p>
</body>
</html>
"""

# Manually set the content for testing
from bs4 import BeautifulSoup
generator.content = mock_html
generator.soup = BeautifulSoup(mock_html, 'html.parser')

# Remove script and style elements
for script in generator.soup(["script", "style"]):
    script.decompose()

# Extract info
info = generator.extract_page_info()

print("EXTRACTED INFORMATION:")
print(f"  Title: {info.get('title')}")
print(f"  Product Name: {generator.product_name}")
print(f"  Category: {generator.category}")
print(f"  Brand: {info.get('brand')}")
print(f"  Description: {info.get('description')}")
print(f"\n  H1 tags: {info.get('h1')}")
print(f"  H2 tags: {info.get('h2')}")
print(f"\n  Extracted Features ({len(generator.extracted_features)}):")
for feat in generator.extracted_features[:5]:
    print(f"    - {feat}")
print(f"\n  Extracted Benefits ({len(generator.extracted_benefits)}):")
for ben in generator.extracted_benefits[:5]:
    print(f"    - {ben}")

# Generate ads
print("\n" + "="*80)
print("GENERATED AD COPY:")
print("="*80)

rsa = generator.generate_complete_rsa()

print("\nHEADLINES - BENEFITS:")
for i, h in enumerate(rsa["headlines"]["benefits"][:5], 1):
    print(f"  {i}. {h} [{len(h)} chars]")

print("\nHEADLINES - TECHNICAL:")
for i, h in enumerate(rsa["headlines"]["technical"][:5], 1):
    print(f"  {i}. {h} [{len(h)} chars]")

print("\nDESCRIPTIONS - BENEFITS:")
for i, d in enumerate(rsa["descriptions"]["benefits"][:3], 1):
    print(f"  {i}. {d} [{len(d)} chars]")

print("\nDESCRIPTIONS - TECHNICAL:")
for i, d in enumerate(rsa["descriptions"]["technical"][:3], 1):
    print(f"  {i}. {d} [{len(d)} chars]")
