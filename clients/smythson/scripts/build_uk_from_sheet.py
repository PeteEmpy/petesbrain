#!/usr/bin/env python3
"""Build UK RSA updates from spreadsheet"""

import json

# Spreadsheet data (columns: Campaign ID, Campaign Name, Ad Group ID, Ad Group Name, Ad ID, H1-H15, D1-D4, Final URL)
# Headers at index: Ad ID=4, H1=5...H15=19, D1=20...D24=23, Final URL=24

spreadsheet_rows = [
    ["13811031042", "SMY | UK | Search | Brand Exact", "128117925481", "UK - Brand", "784157361259", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13811031042", "SMY | UK | Search | Brand Exact", "187903967924", "UK - Brand - Sale", "784408654524", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Over 135 years of expertise", "", "Timeless leather craftsmanship", "Personalise your order today", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030701", "UK - semi-brand - home - desk accessories - blotters", "784228048462", "Smythson of Bond Street™", "Luxury leather blotters", "Discover gifts for him & her", "Shop luxury leather blotters", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1888", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/desk-accessories"],
]

# Load current state
with open('../data/uk_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

print(f"Loaded {len(current_state)} UK RSAs from API")
print(f"Loaded {len(spreadsheet_rows)} UK RSAs from spreadsheet")

# Create lookup
current_by_id = {ad['ad_id']: ad for ad in current_state}

# Build updates
updates = []

for row in spreadsheet_rows:
    ad_id = row[4]
    
    if ad_id not in current_by_id:
        print(f"Warning: Ad ID {ad_id} not in current state")
        continue
    
    current = current_by_id[ad_id]
    
    # Extract headlines (H1-H15 = indices 5-19)
    new_headlines = [h for h in row[5:20] if h]
    
    # Extract descriptions (D1-D4 = indices 20-23)
    new_descriptions = [d for d in row[20:24] if d]
    
    final_url = row[24]
    
    updates.append({
        'campaign_name': current['campaign_name'],
        'ad_group_name': current['ad_group_name'],
        'ad_id': ad_id,
        'status': current['status'],
        'current_headlines': current['current_headlines'],
        'new_headlines': new_headlines,
        'current_descriptions': current['current_descriptions'],
        'new_descriptions': new_descriptions,
        'final_url': final_url
    })

print(f"\nBuilt {len(updates)} update entries")

# Check for differences
changes = 0
for u in updates:
    if u['current_headlines'] != u['new_headlines'] or u['current_descriptions'] != u['new_descriptions']:
        changes += 1

print(f"✓ {changes} ads have changes")

# Save
output_file = '../data/uk_rsa_updates_from_sheet.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"✓ Saved to: {output_file}")
