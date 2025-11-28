#!/usr/bin/env python3
"""Build final RSA updates - add countdown to H15 for USA/ROW based on spreadsheet inspection"""

import json

countdown_text = "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"

def process_region(region, current_state_file, headline_position, output_file):
    """Process a region - add countdown at specified headline position"""
    print(f"\n{'='*80}")
    print(f"Processing {region}")
    print(f"{'='*80}")

    # Load current state
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)

    # Convert to dict if needed
    current_dict = {ad['ad_id']: ad for ad in current_state}

    print(f"Loaded {len(current_dict)} RSAs")
    print(f"Target: Add countdown to H{headline_position}")

    updates = []
    changed_count = 0
    already_has_countdown = 0
    too_few_headlines = 0

    for ad_id, ad in current_dict.items():
        current_headlines = ad['current_headlines']
        new_headlines = current_headlines.copy()

        # Check if already has countdown at target position
        if len(current_headlines) >= headline_position and current_headlines[headline_position - 1] == countdown_text:
            already_has_countdown += 1
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

        # If doesn't have enough headlines, ADD the countdown (extend the list)
        if len(current_headlines) < headline_position:
            # Extend to add H15
            while len(new_headlines) < headline_position:
                new_headlines.append('')
            new_headlines[headline_position - 1] = countdown_text
            changed_count += 1
            print(f"  ✓ {ad_id}: {ad['campaign_name']}")
            print(f"     ADDING H{headline_position} (was {len(current_headlines)} headlines): '{countdown_text}'")
        else:
            # Replace existing
            old_text = new_headlines[headline_position - 1]
            new_headlines[headline_position - 1] = countdown_text
            changed_count += 1
            print(f"  ✓ {ad_id}: {ad['campaign_name']}")
            print(f"     H{headline_position}: '{old_text[:40]}...' → '{countdown_text[:40]}...'")

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
    print(f"    With changes: {changed_count}")
    print(f"    Already have countdown: {already_has_countdown}")
    print(f"    Too few headlines: {too_few_headlines}")
    print(f"    Saved to: {output_file}")

    return len(updates)

# Process each region
print("="*80)
print("Building RSA updates with countdown in H15")
print("="*80)

# USA - H15
usa_count = process_region(
    'USA',
    'clients/smythson/data/usa_rsa_current_state.json',
    15,  # H15
    'clients/smythson/data/usa_rsa_updates_full.json'
)

# EUR - Check if needs updates (will process but expect 0 changes based on spreadsheet inspection)
eur_count = process_region(
    'EUR',
    'clients/smythson/data/eur_rsa_current_state.json',
    15,  # Try H15
    'clients/smythson/data/eur_rsa_updates_full.json'
)

# ROW - H15
row_count = process_region(
    'ROW',
    'clients/smythson/data/row_rsa_current_state.json',
    15,  # H15
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
