#!/usr/bin/env python3
"""Build EUR RSA updates by loading current state and preserving it"""

import json
import sys

print("Building EUR RSA updates...")
print("Loading current state...")

with open('../data/eur_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

print(f"✓ Loaded {len(current_state)} EUR RSAs")

# Create update entries for all ads (preserving current state)
updates = []

for ad in current_state:
    updates.append({
        'campaign_name': ad['campaign_name'],
        'ad_group_name': ad['ad_group_name'],
        'ad_id': ad['ad_id'],
        'status': ad['status'],
        'current_headlines': ad['current_headlines'],
        'new_headlines': ad['current_headlines'],  # Keep same
        'current_descriptions': ad['current_descriptions'],
        'new_descriptions': ad['current_descriptions'],  # Keep same
        'final_url': ad['final_url']
    })

output_file = '../data/eur_rsa_updates_full.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"✓ Created {len(updates)} update entries")
print(f"✓ Saved to: {output_file}")
print("\nNext: Generate CSV with Account ID")
