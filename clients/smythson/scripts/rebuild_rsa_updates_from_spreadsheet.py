#!/usr/bin/env python3
"""Rebuild RSA update JSONs by comparing current state with spreadsheet (via claude mcp calls)"""

import json
import subprocess

SPREADSHEET_ID = '189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo'

REGIONS = {
    'USA': {
        'sheet_range': 'USA!A2:Z100',
        'current_state_file': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/usa_rsa_current_state.json',
        'output_file': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/usa_rsa_updates_full.json'
    },
    'EUR': {
        'sheet_range': 'EUR!A2:Z100',
        'current_state_file': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/eur_rsa_current_state.json',
        'output_file': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/eur_rsa_updates_full.json'
    },
    'ROW': {
        'sheet_range': 'ROW!A2:Z100',
        'current_state_file': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/row_rsa_current_state.json',
        'output_file': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/row_rsa_updates_full.json'
    }
}

def read_sheet_via_mcp(sheet_range):
    """Read Google Sheet data via MCP command"""
    print(f"  Reading spreadsheet range: {sheet_range}")

    cmd = [
        'claude', 'mcp', 'call', 'google-sheets',
        'read_cells',
        '--',
        f'spreadsheet_id={SPREADSHEET_ID}',
        f'range_name={sheet_range}'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    rows = data['result']

    print(f"  ✓ Got {len(rows)} rows from spreadsheet")
    return rows

def parse_spreadsheet_rows(rows):
    """Parse spreadsheet rows into ad_id → data lookup"""
    spreadsheet_rsas = {}

    for row in rows:
        if len(row) < 5:
            continue

        ad_id = row[4]  # Column E (index 4)

        # Extract headlines (columns F-T = indices 5-19 = H1-H15)
        headlines = []
        for i in range(5, 20):
            if i < len(row) and row[i].strip():
                headlines.append(row[i].strip())

        # Extract descriptions (columns U-X = indices 20-23 = D1-D4)
        descriptions = []
        for i in range(20, 24):
            if i < len(row) and row[i].strip():
                descriptions.append(row[i].strip())

        # Final URL (column Y = index 24)
        final_url = row[24].strip() if len(row) > 24 else ''

        spreadsheet_rsas[ad_id] = {
            'headlines': headlines,
            'descriptions': descriptions,
            'final_url': final_url
        }

    return spreadsheet_rsas

def compare_and_build_updates(region, current_state_file, spreadsheet_data):
    """Compare current vs desired and build update JSON"""
    print(f"  Loading current state from {current_state_file}")

    with open(current_state_file, 'r') as f:
        current_state = json.load(f)

    # Convert list to dict if needed
    if isinstance(current_state, list):
        current_dict = {ad['ad_id']: ad for ad in current_state}
    else:
        current_dict = current_state

    print(f"  ✓ Loaded {len(current_dict)} current RSAs")
    print(f"\n  Comparing with spreadsheet...")

    updates = []
    changed_count = 0
    no_change_count = 0
    not_in_spreadsheet = 0

    for ad_id, current in current_dict.items():
        if ad_id not in spreadsheet_data:
            print(f"  ⚠️  {ad_id} not in spreadsheet - skipping")
            not_in_spreadsheet += 1
            continue

        desired = spreadsheet_data[ad_id]

        # Compare
        headlines_changed = current['current_headlines'] != desired['headlines']
        descriptions_changed = current['current_descriptions'] != desired['descriptions']
        url_changed = current['final_url'] != desired['final_url']

        if headlines_changed or descriptions_changed or url_changed:
            changed_count += 1
            print(f"\n  ✓ {ad_id}: {current['campaign_name']}")

            if headlines_changed:
                # Show which headlines changed
                curr_h = current['current_headlines']
                new_h = desired['headlines']
                max_len = max(len(curr_h), len(new_h))

                for i in range(max_len):
                    curr_val = curr_h[i] if i < len(curr_h) else '[missing]'
                    new_val = new_h[i] if i < len(new_h) else '[missing]'
                    if curr_val != new_val:
                        print(f"     H{i+1}: '{curr_val[:40]}...' → '{new_val[:40]}...'")

            if descriptions_changed:
                print(f"     Descriptions changed")

            if url_changed:
                print(f"     URL changed")

            updates.append({
                'campaign_name': current['campaign_name'],
                'ad_group_name': current['ad_group_name'],
                'ad_id': ad_id,
                'status': current['status'],
                'current_headlines': current['current_headlines'],
                'new_headlines': desired['headlines'],
                'current_descriptions': current['current_descriptions'],
                'new_descriptions': desired['descriptions'],
                'final_url': desired['final_url']
            })
        else:
            no_change_count += 1

    print(f"\n  Summary:")
    print(f"    Total RSAs in Google Ads: {len(current_dict)}")
    print(f"    With changes needed: {changed_count}")
    print(f"    No changes: {no_change_count}")
    print(f"    Not in spreadsheet: {not_in_spreadsheet}")

    return updates

# Process each region
print("="*80)
print("Rebuilding RSA updates from spreadsheet comparison")
print("="*80)

for region, config in REGIONS.items():
    print(f"\n{'='*80}")
    print(f"Processing {region}")
    print(f"{'='*80}")

    # Read spreadsheet
    rows = read_sheet_via_mcp(config['sheet_range'])
    spreadsheet_data = parse_spreadsheet_rows(rows)

    print(f"  ✓ Parsed {len(spreadsheet_data)} RSAs from spreadsheet")

    # Compare and build updates
    updates = compare_and_build_updates(
        region,
        config['current_state_file'],
        spreadsheet_data
    )

    # Save
    with open(config['output_file'], 'w') as f:
        json.dump(updates, f, indent=2)

    print(f"  ✓ Saved {len(updates)} updates to {config['output_file']}")

print(f"\n{'='*80}")
print("COMPLETE")
print(f"{'='*80}")
print("\nNext: Generate CSVs with:")
for region in ['usa', 'eur', 'row']:
    print(f"\npython3 shared/scripts/generate-rsa-update-csv.py \\")
    print(f"  --client smythson \\")
    print(f"  --input clients/smythson/data/{region}_rsa_updates_full.json \\")
    print(f"  --output {region}_rsa_updates.csv")
