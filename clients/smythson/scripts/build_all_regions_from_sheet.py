#!/usr/bin/env python3
"""Build RSA updates from spreadsheet for all regions"""

import json
import sys

sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync')

SPREADSHEET_ID = '189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo'

# Manually parsed UK data from MCP output
UK_SHEET_DATA = [
    # Format: [Campaign ID, Campaign Name, Ad Group ID, Ad Group Name, Ad ID, H1-H15, D1-D4, Final URL]
    ["13811031042", "SMY | UK | Search | Brand Exact", "128117925481", "UK - Brand", "784157361259", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13811031042", "SMY | UK | Search | Brand Exact", "187903967924", "UK - Brand - Sale", "784408654524", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Over 135 years of expertise", "", "Timeless leather craftsmanship", "Personalise your order today", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030701", "UK - semi-brand - home - desk accessories - blotters", "784228048462", "Smythson of Bond Street™", "Luxury leather blotters", "Discover gifts for him & her", "Shop luxury leather blotters", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1888", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/desk-accessories"],
]

def build_updates_for_region(region_name, sheet_data, current_state_file, output_file):
    """Build update JSON from spreadsheet and current state"""
    
    print(f"\n{'='*80}")
    print(f"Building {region_name} RSA Updates from Spreadsheet")
    print(f"{'='*80}\n")
    
    # Load current state
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)
    
    print(f"✓ Loaded {len(current_state)} {region_name} RSAs from API")
    print(f"✓ Got {len(sheet_data)} rows from spreadsheet")
    
    # Create lookup
    current_by_id = {ad['ad_id']: ad for ad in current_state}
    
    # Build updates
    updates = []
    changes_count = 0
    not_found = []
    
    for row in sheet_data:
        ad_id = str(row[4])  # Ad ID at index 4
        
        if ad_id not in current_by_id:
            not_found.append(ad_id)
            continue
        
        current = current_by_id[ad_id]
        
        # Extract headlines (H1-H15 = indices 5-19)
        new_headlines = [h for h in row[5:20] if h]
        
        # Extract descriptions (D1-D4 = indices 20-24)
        new_descriptions = [d for d in row[20:24] if d]
        
        final_url = row[24] if len(row) > 24 else current['final_url']
        
        # Check for changes
        has_changes = (
            current['current_headlines'] != new_headlines or
            current['current_descriptions'] != new_descriptions
        )
        
        if has_changes:
            changes_count += 1
        
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
    
    if not_found:
        print(f"⚠️  {len(not_found)} ads in spreadsheet not found in current state")
    
    print(f"✓ Built {len(updates)} update entries")
    print(f"✓ {changes_count} ads have changes")
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(updates, f, indent=2)
    
    print(f"✓ Saved to: {output_file}")
    
    return len(updates)

# Test with UK first (3 ads)
if __name__ == '__main__':
    count = build_updates_for_region(
        "UK (sample)",
        UK_SHEET_DATA,
        '../data/uk_rsa_current_state.json',
        '../data/uk_rsa_updates_from_sheet.json'
    )
    
    print(f"\n✓ Ready to generate CSV for {count} UK ads")
