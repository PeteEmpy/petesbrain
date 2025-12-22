#!/usr/bin/env python3
"""Rebuild ROW RSA updates by comparing current state with spreadsheet data."""

import json
from pathlib import Path

# ROW spreadsheet data (4 rows - fetched from spreadsheet)
ROW_SHEET_DATA = [
    ["6551615752", "SMY | AUS | Search | Brand Ai", "77517328486", "AUS - Brand - Exact & Phrase", "784326640550", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Personalise your order today", "", "Over 135 years of expertise", "Timeless leather craftsmanship", "Luxury personalised gifts", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
    ["22503794801", "SMY | ROW | Search | Brand Ai", "185727479264", "ROW | Brand", "784326640553", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Personalise your order today", "", "Over 135 years of expertise", "Luxury personalised gifts", "Timeless leather craftsmanship", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
    ["6552020619", "SMY | ROW | Search | Brand Diaries and Organisers", "138656304694", "ROW - semi-brand - diaries and organisers - diaries", "773497251588", "Smythson of Bond Street™", "Luxury Leather Diaries", "Over 135 Years Of Expertise", "Luxury Leather Craftsmanship", "", "Enjoy Complimentary Returns", "Personalisation Available", "Personalise Your Order Today", "Discover Gifts For Him & Her", "Shop The 2026 Diary Collection", "Exclusive Luxury Gift Wrapping", "Uncover Our Latest Collection", "Smythson Portobello Diary", "Crafted in England", "", "Start Planning Next Year's Adventures With Our 2026 Diaries.", "Crafted with Featherweight Paper And Leather For Effortless Planning.", "Discover Luxury Leather Diaries, Bags, Notebooks, Stationery & More.", "Explore Gold-Stamped Initials Motifs & More To Make Your Diary Uniquely Yours.", "https://www.smythson.com/int/diaries-and-books/diaries/all-diaries"],
    ["23241919876", "SMY | ROW | Search | Competitor | Ai", "189913732924", "ROW | Brand", "784326640556", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Personalise your order today", "", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
]

def parse_row(row):
    """Parse spreadsheet row - columns 5-19 headlines, 20-23 descriptions, 24 final URL"""
    if len(row) < 25:
        return None
    
    ad_id = row[4]
    headlines = [row[i].strip() for i in range(5, 20) if row[i] and row[i].strip()]
    descriptions = [row[i].strip() for i in range(20, 24) if row[i] and row[i].strip()]
    
    return {
        'ad_id': ad_id,
        'headlines': headlines,
        'descriptions': descriptions,
        'final_url': row[24] if len(row) > 24 else ""
    }

print("="*80)
print("ROW RSA Rebuild - Comparing Current State vs Spreadsheet")
print("="*80)

# Load current state
current_state_file = Path(__file__).parent.parent / 'data' / 'row_rsa_current_state.json'
with open(current_state_file, 'r') as f:
    current_state = json.load(f)

# Convert to dict for lookup
current_dict = {ad['ad_id']: ad for ad in current_state}
print(f"\n✓ Loaded {len(current_dict)} current RSAs from Google Ads")
print(f"  Active ad IDs: {list(current_dict.keys())}")

# Parse spreadsheet
spreadsheet_dict = {}
for row in ROW_SHEET_DATA:
    parsed = parse_row(row)
    if parsed:
        spreadsheet_dict[parsed['ad_id']] = parsed

print(f"\n✓ Parsed {len(spreadsheet_dict)} RSAs from spreadsheet")
print(f"  Spreadsheet ad IDs: {list(spreadsheet_dict.keys())}")

# Compare and build updates - INCLUDE ALL ACTIVE ADS (even with no changes) for verification
all_ads = []
changed_count = 0
no_change_count = 0
not_in_current = 0

print(f"\n{'='*80}")
print("Comparison Results")
print(f"{'='*80}")

for ad_id, spreadsheet_ad in spreadsheet_dict.items():
    if ad_id not in current_dict:
        print(f"\n⚠️  Ad {ad_id} in spreadsheet but NOT in current Google Ads state (REMOVED)")
        print(f"   Skipping this ad...")
        not_in_current += 1
        continue
    
    current = current_dict[ad_id]
    
    # Compare
    headlines_changed = current['current_headlines'] != spreadsheet_ad['headlines']
    descriptions_changed = current['current_descriptions'] != spreadsheet_ad['descriptions']
    url_changed = current.get('final_url', '') != spreadsheet_ad['final_url']
    
    if headlines_changed or descriptions_changed or url_changed:
        changed_count += 1
        print(f"\n✓ Ad {ad_id}: {current['campaign_name']}")
        
        if headlines_changed:
            print(f"   HEADLINES CHANGED:")
            curr_h = current['current_headlines']
            new_h = spreadsheet_ad['headlines']
            max_len = max(len(curr_h), len(new_h))
            
            for i in range(max_len):
                curr_val = curr_h[i] if i < len(curr_h) else '[missing]'
                new_val = new_h[i] if i < len(new_h) else '[missing]'
                if curr_val != new_val:
                    print(f"     H{i+1}: '{curr_val}' → '{new_val}'")
        
        if descriptions_changed:
            print(f"   DESCRIPTIONS CHANGED")
            
        if url_changed:
            print(f"   URL CHANGED")
    else:
        no_change_count += 1
        print(f"\n  Ad {ad_id}: No changes needed (including for verification)")
    
    # Add ALL active ads (changed or not) for CSV generation
    all_ads.append({
        'campaign_name': current['campaign_name'],
        'ad_group_name': current['ad_group_name'],
        'ad_id': ad_id,
        'status': current['status'],
        'current_headlines': current['current_headlines'],
        'new_headlines': spreadsheet_ad['headlines'],
        'current_descriptions': current['current_descriptions'],
        'new_descriptions': spreadsheet_ad['descriptions'],
        'final_url': spreadsheet_ad['final_url']
    })

# Save ALL active ads (for verification CSV)
output_file = Path(__file__).parent.parent / 'data' / 'row_rsa_updates_from_sheet.json'
with open(output_file, 'w') as f:
    json.dump(all_ads, f, indent=2)

print(f"\n{'='*80}")
print("Summary")
print(f"{'='*80}")
print(f"  Total RSAs in current state: {len(current_dict)}")
print(f"  Total RSAs in spreadsheet: {len(spreadsheet_dict)}")
print(f"  With changes needed: {changed_count}")
print(f"  No changes: {no_change_count}")
print(f"  In spreadsheet but REMOVED in Google Ads: {not_in_current}")
print(f"\n✓ Saved {len(all_ads)} active ads (for verification) to: {output_file}")
print(f"  Note: Excluded {not_in_current} REMOVED ad(s) from CSV")
print(f"{'='*80}")
