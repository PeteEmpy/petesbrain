#!/usr/bin/env python3
"""Process ROW spreadsheet data and create update JSON (no current state comparison)."""

import json
from pathlib import Path

# ROW spreadsheet data (4 rows fetched from MCP)
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
    headlines = [row[i].strip() for i in range(5, 20) if row[i] and row[i].strip()]
    descriptions = [row[i].strip() for i in range(20, 24) if row[i] and row[i].strip()]
    return {
        'campaign_id': row[0], 'campaign_name': row[1], 'ad_group_id': row[2],
        'ad_group_name': row[3], 'ad_id': row[4], 'headlines': headlines,
        'descriptions': descriptions, 'final_url': row[24] if len(row) > 24 else ""
    }

print("ROW processing (using spreadsheet as source of truth)")
print("="*80)

# Parse spreadsheet
updates = []
for i, row in enumerate(ROW_SHEET_DATA, 1):
    parsed = parse_row(row)
    if parsed:
        print(f"  Row {i}: Ad {parsed['ad_id']} - {len(parsed['headlines'])} headlines, {len(parsed['descriptions'])} descriptions")
        
        # Create update entry using spreadsheet as both current and new (assumes spreadsheet is correct)
        updates.append({
            'campaign_name': parsed['campaign_name'],
            'ad_group_name': parsed['ad_group_name'],
            'ad_id': parsed['ad_id'],
            'status': 'ENABLED',  # Default status
            'current_headlines': parsed['headlines'],  # Using spreadsheet as "current"
            'new_headlines': parsed['headlines'],
            'current_descriptions': parsed['descriptions'],
            'new_descriptions': parsed['descriptions'],
            'final_url': parsed['final_url']
        })

# Save
output_file = Path(__file__).parent.parent / 'data' / 'row_rsa_updates_from_sheet.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"\n{'='*80}")
print(f"✓ ROW processing complete: {len(updates)} ads")
print(f"  Note: Using spreadsheet as source of truth (no current state file)")
print(f"  Output: {output_file}")
print(f"{'='*80}")
