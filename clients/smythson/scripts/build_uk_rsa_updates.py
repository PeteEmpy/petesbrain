#!/usr/bin/env python3
"""Build full UK RSA updates JSON from current state + spreadsheet changes"""

import json

# Load current state from Google Ads
with open('/Users/administrator/Documents/PetesBrain/clients/smythson/data/uk_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

# Spreadsheet data (new/desired headlines) - from the Google Sheet
spreadsheet_data = [
    {"ad_id": "784157361259", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784408654524", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048462", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048447", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048453", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048465", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048444", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048456", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048459", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048468", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784228048450", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784197388692", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780966363483", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687964", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687982", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687985", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687991", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687979", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687976", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687967", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687973", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687970", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687988", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "780374687994", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "784157389885", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "773478848874", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"},
    {"ad_id": "773478848871", "new_h8": "Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}"}
]

# Create lookup for new H8 values
new_h8_lookup = {item['ad_id']: item['new_h8'] for item in spreadsheet_data}

print(f"\nBuilding full update JSON for {len(current_state)} UK RSAs...")

updates = []
changed_count = 0

for ad in current_state:
    ad_id = ad['ad_id']

    # Get current headlines
    current_headlines = ad['current_headlines']

    # Get new H8 value
    new_h8 = new_h8_lookup.get(ad_id)

    if not new_h8:
        print(f"⚠️  No H8 update for {ad_id}")
        continue

    # Build new headlines (replace H8)
    new_headlines = current_headlines.copy()

    # Find position of H8 (index 7 = H8)
    if len(new_headlines) >= 8:
        old_h8 = new_headlines[7]
        new_headlines[7] = new_h8

        if old_h8 != new_h8:
            changed_count += 1
            print(f"  ✓ {ad['campaign_name']} > {ad['ad_group_name']}")
            print(f"     Old H8: {old_h8}")
            print(f"     New H8: {new_h8}")
    else:
        print(f"  ⚠️  {ad_id} has only {len(new_headlines)} headlines (< 8)")
        continue

    # Build update entry
    updates.append({
        'campaign_name': ad['campaign_name'],
        'ad_group_name': ad['ad_group_name'],
        'ad_id': ad_id,
        'status': ad['status'],
        'current_headlines': current_headlines,
        'new_headlines': new_headlines,
        'current_descriptions': ad['current_descriptions'],
        'new_descriptions': ad['current_descriptions'],  # Unchanged
        'final_url': ad['final_url']
    })

# Save to JSON
output_path = '/Users/administrator/Documents/PetesBrain/clients/smythson/data/uk_rsa_updates_full.json'
with open(output_path, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"\n{'='*80}")
print(f"SUMMARY")
print(f"{'='*80}")
print(f"Total RSAs: {len(current_state)}")
print(f"With changes: {changed_count}")
print(f"Saved to: {output_path}")
print(f"\nNext: Generate CSV with:")
print(f"  python3 shared/scripts/generate-rsa-update-csv.py --client smythson --input {output_path} --output uk_rsa_updates.csv")
