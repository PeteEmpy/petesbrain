#!/bin/bash
# Get all coffee products from Godshot website

COFFEE_PRODUCTS=(
  "dak-milky-cake-250g"
  "dak-honeymoon-250g"
  "dak-strawberry-kiss-250g"
  "dak-cream-donut-250g"
  "dak-orange-flirt-250g"
  "dak-berry-blues-250g"
  "dak-yuzu-crew-125g"
  "dak-panettone-250g"
  "dak-purple-rain-250g"
  "dak-passion-twist-250g"
)

echo "product_slug,product_name,product_id,sku"

for slug in "${COFFEE_PRODUCTS[@]}"; do
  # Fetch product page and extract ID
  response=$(curl -s "https://mygodshot.com/product/$slug/")

  # Extract product ID from schema markup
  product_id=$(echo "$response" | grep -o '"productID":"[0-9]*"' | grep -o '[0-9]*' | head -1)

  # Extract SKU
  sku=$(echo "$response" | grep -o '"sku":"[^"]*"' | sed 's/"sku":"\([^"]*\)"/\1/' | head -1)

  # Extract product name
  product_name=$(echo "$response" | grep -o '<h1[^>]*class="product_title[^"]*"[^>]*>[^<]*' | sed 's/<h1[^>]*>//' | sed 's/&amp;/\&/g')

  echo "$slug,$product_name,$product_id,$sku"
done
