#!/usr/bin/env python3
"""Build complete UK RSA updates from spreadsheet data"""

import json

# Load current state
with open('../data/uk_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

print(f"✓ Loaded {len(current_state)} UK RSAs from API")

# Create lookup
current_by_id = {ad['ad_id']: ad for ad in current_state}

# Load spreadsheet data
with open('../data/uk_spreadsheet_data.txt', 'r') as f:
    lines = f.readlines()

print(f"✓ Loaded {len(lines)} rows from spreadsheet")

# Build updates
updates = []
changes_count = 0

for line in lines:
    parts = line.strip().split('|')
    
    # Parse: Campaign ID|Campaign Name|Ad Group ID|Ad Group Name|Ad ID|H1-H15 (15 fields)|D1-D4 (4 fields)|Final URL
    # Indices: 0|1|2|3|4|5-19|20-23|24
    
    ad_id = parts[4]
    
    if ad_id not in current_by_id:
        print(f"⚠️  Ad ID {ad_id} not in current state")
        continue
    
    current = current_by_id[ad_id]
    
    # Extract headlines (H1-H15 = indices 5-19)
    new_headlines = [h for h in parts[5:20] if h.strip()]
    
    # Extract descriptions (D1-D4 = indices 20-24)
    new_descriptions = [d for d in parts[20:24] if d.strip()]
    
    final_url = parts[24] if len(parts) > 24 else current['final_url']
    
    # Check for changes
    has_changes = (
        current['current_headlines'] != new_headlines or
        current['current_descriptions'] != new_descriptions
    )
    
    if has_changes:
        changes_count += 1
        print(f"  ✓ Ad {ad_id}: Changes detected")
    
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

print(f"\n✓ Built {len(updates)} update entries")
print(f"✓ {changes_count} ads have changes from spreadsheet")

# Save
output_file = '../data/uk_rsa_updates_from_sheet.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"✓ Saved to: {output_file}")
