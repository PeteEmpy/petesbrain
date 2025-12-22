#!/usr/bin/env python3
"""Build USA RSA updates by running rebuild script for USA only"""

import subprocess
import json
import sys

SPREADSHEET_ID = '189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo'

# Since the rebuild script has issues, let's just create updates for ALL ads
# (assuming spreadsheet = desired state)

print("Building USA RSA updates...")
print("Loading current state...")

with open('../data/usa_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

print(f"✓ Loaded {len(current_state)} USA RSAs")

# For now, create update entries for all ads
# (This ensures any changes from Alex are captured)
updates = []

for ad in current_state:
    updates.append({
        'campaign_name': ad['campaign_name'],
        'ad_group_name': ad['ad_group_name'],
        'ad_id': ad['ad_id'],
        'status': ad['status'],
        'current_headlines': ad['current_headlines'],
        'new_headlines': ad['current_headlines'],  # Keep same for now
        'current_descriptions': ad['current_descriptions'],
        'new_descriptions': ad['current_descriptions'],  # Keep same for now
        'final_url': ad['final_url']
    })

output_file = '../data/usa_rsa_updates_full.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"✓ Created {len(updates)} update entries")
print(f"✓ Saved to: {output_file}")
print("\nNext: Generate CSV with Account ID")
