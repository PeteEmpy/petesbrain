#!/usr/bin/env python3
"""Quick test: Do USA ads have changes?"""

import json

# Load current state
with open('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/usa_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

print(f"USA has {len(current_state)} RSAs in current state")
print(f"\nSample ad:")
print(f"  Ad ID: {current_state[0]['ad_id']}")
print(f"  Campaign: {current_state[0]['campaign_name']}")
print(f"  Headlines ({len(current_state[0]['current_headlines'])}): {current_state[0]['current_headlines'][:3]}...")
print(f"  Descriptions ({len(current_state[0]['current_descriptions'])}): {current_state[0]['current_descriptions'][:2]}...")

# Spreadsheet sample for same ad (784198246551)
spreadsheet_headlines = [
    "Smythson of Bond Street™",
    "British heritage since 1887",
    "Shop luxury leather pieces",
    "Personalize your order today",
    "Over 135 years of expertise",
    "Free delivery on orders $500+",
    "Handcrafted in England",
    "Explore luxury Christmas gifts",
    "Shop luxury stocking fillers",
    "Luxury gifts for him",
    "Luxury gifts for her",
    "Gifts for the Home",
    "Timeless leather craftsmanship"
]

spreadsheet_descriptions = [
    "Make the ordinary extraordinary and the everyday timeless with Smythson",
    "A distinctly unique, extraordinary brand catering to extraordinary people since 1887",
    "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given",
    "This Christmas, celebrate the art of thoughtful gifting with Smythson"
]

print(f"\nSpreadsheet sample (same ad):")
print(f"  Headlines ({len(spreadsheet_headlines)}): {spreadsheet_headlines[:3]}...")
print(f"  Descriptions ({len(spreadsheet_descriptions)}): {spreadsheet_descriptions[:2]}...")

# Compare
if current_state[0]['current_headlines'] != spreadsheet_headlines:
    print(f"\n✓ Headlines DIFFERENT")
else:
    print(f"\n- Headlines SAME")

if current_state[0]['current_descriptions'] != spreadsheet_descriptions:
    print(f"✓ Descriptions DIFFERENT")
else:
    print(f"- Descriptions SAME")
