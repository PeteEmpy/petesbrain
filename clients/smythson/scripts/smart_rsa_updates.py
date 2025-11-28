#!/usr/bin/env python3
"""Smart RSA updates - add countdown as next available headline for each ad"""

import json

countdown_text = "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"

def process_region(region, current_state_file, output_file):
    """Process a region - add countdown as next available headline"""
    print(f"\n{'='*80}")
    print(f"Processing {region}")
    print(f"{'='*80}")

    # Load current state
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)

    # Convert to dict if needed
    current_dict = {ad['ad_id']: ad for ad in current_state}

    print(f"Loaded {len(current_dict)} RSAs")

    updates = []
    changed_count = 0
    already_has_countdown = 0
    max_headlines_reached = 0

    for ad_id, ad in current_dict.items():
        current_headlines = ad['current_headlines']
        new_headlines = current_headlines.copy()

        # Check if already has countdown anywhere
        if countdown_text in current_headlines:
            already_has_countdown += 1
            position = current_headlines.index(countdown_text) + 1
            print(f"  ⏭️  {ad_id} already has countdown at H{position}")
            # Include in updates but with no change
            updates.append({
                'campaign_name': ad['campaign_name'],
                'ad_group_name': ad['ad_group_name'],
                'ad_id': ad_id,
                'status': ad['status'],
                'current_headlines': current_headlines,
                'new_headlines': current_headlines,
                'current_descriptions': ad['current_descriptions'],
                'new_descriptions': ad['current_descriptions'],
                'final_url': ad['final_url']
            })
            continue

        # Check if at max headlines (15)
        if len(current_headlines) >= 15:
            print(f"  ⚠️  {ad_id} already has 15 headlines - cannot add more")
            max_headlines_reached += 1
            continue

        # Add countdown as next headline
        new_headlines.append(countdown_text)
        next_position = len(current_headlines) + 1
        changed_count += 1

        print(f"  ✓ {ad_id}: {ad['campaign_name']}")
        print(f"     Adding H{next_position}: '{countdown_text}'")

        updates.append({
            'campaign_name': ad['campaign_name'],
            'ad_group_name': ad['ad_group_name'],
            'ad_id': ad_id,
            'status': ad['status'],
            'current_headlines': current_headlines,
            'new_headlines': new_headlines,
            'current_descriptions': ad['current_descriptions'],
            'new_descriptions': ad['current_descriptions'],
            'final_url': ad['final_url']
        })

    # Save
    with open(output_file, 'w') as f:
        json.dump(updates, f, indent=2)

    print(f"\n  Summary:")
    print(f"    Total RSAs: {len(current_dict)}")
    print(f"    Adding countdown: {changed_count}")
    print(f"    Already have countdown: {already_has_countdown}")
    print(f"    At max headlines: {max_headlines_reached}")
    print(f"    Saved to: {output_file}")

    return len(updates)

# Process each region
print("="*80)
print("Adding countdown as next available headline")
print("="*80)

# USA
usa_count = process_region(
    'USA',
    'clients/smythson/data/usa_rsa_current_state.json',
    'clients/smythson/data/usa_rsa_updates_full.json'
)

# EUR
eur_count = process_region(
    'EUR',
    'clients/smythson/data/eur_rsa_current_state.json',
    'clients/smythson/data/eur_rsa_updates_full.json'
)

# ROW
row_count = process_region(
    'ROW',
    'clients/smythson/data/row_rsa_current_state.json',
    'clients/smythson/data/row_rsa_updates_full.json'
)

print(f"\n{'='*80}")
print("COMPLETE")
print(f"{'='*80}")
print(f"\nUpdates generated:")
print(f"  USA: {usa_count} RSAs")
print(f"  EUR: {eur_count} RSAs")
print(f"  ROW: {row_count} RSAs")

print(f"\nNext: Generate CSVs with:")
for region in ['usa', 'eur', 'row']:
    print(f"\npython3 shared/scripts/generate-rsa-update-csv.py \\")
    print(f"  --client smythson \\")
    print(f"  --input clients/smythson/data/{region}_rsa_updates_full.json \\")
    print(f"  --output {region}_rsa_updates.csv")
