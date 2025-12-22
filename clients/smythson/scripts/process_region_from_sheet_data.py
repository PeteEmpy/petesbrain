#!/usr/bin/env python3
"""
Process a single region's RSA updates from saved spreadsheet data
Usage: python3 process_region_from_sheet_data.py <region>
"""

import json
import sys

def parse_spreadsheet_row(row):
    """Parse a row from MCP spreadsheet output into structured data"""
    # Row format: [Campaign ID, Campaign Name, Ad Group ID, Ad Group Name, Ad ID, H1-H15, D1-D4, Final URL]
    # Indices: 0, 1, 2, 3, 4, 5-19, 20-23, 24
    
    return {
        'ad_id': str(row[4]),
        'headlines': [h for h in row[5:20] if h],
        'descriptions': [d for d in row[20:24] if d],
        'final_url': row[24] if len(row) > 24 else ''
    }

def build_updates(region_name, sheet_data_rows, current_state_file, output_file):
    """Build update JSON from spreadsheet rows and current state"""
    
    print(f"\n{'='*80}")
    print(f"Building {region_name} RSA Updates from Spreadsheet")
    print(f"{'='*80}\n")
    
    # Load current state
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)
    
    print(f"✓ Loaded {len(current_state)} {region_name} RSAs from API")
    print(f"✓ Processing {len(sheet_data_rows)} rows from spreadsheet")
    
    # Create lookup
    current_by_id = {ad['ad_id']: ad for ad in current_state}
    
    # Parse spreadsheet rows
    updates = []
    changes_count = 0
    matched = 0
    not_found = []
    
    for row in sheet_data_rows:
        parsed = parse_spreadsheet_row(row)
        ad_id = parsed['ad_id']
        
        if ad_id not in current_by_id:
            not_found.append(ad_id)
            continue
        
        current = current_by_id[ad_id]
        matched += 1
        
        # Check for changes
        has_changes = (
            current['current_headlines'] != parsed['headlines'] or
            current['current_descriptions'] != parsed['descriptions']
        )
        
        if has_changes:
            changes_count += 1
        
        updates.append({
            'campaign_name': current['campaign_name'],
            'ad_group_name': current['ad_group_name'],
            'ad_id': ad_id,
            'status': current['status'],
            'current_headlines': current['current_headlines'],
            'new_headlines': parsed['headlines'],
            'current_descriptions': current['current_descriptions'],
            'new_descriptions': parsed['descriptions'],
            'final_url': parsed['final_url'] or current['final_url']
        })
    
    if not_found:
        print(f"⚠️  {len(not_found)} ads in spreadsheet not found in current state")
    
    print(f"✓ Matched {matched} ads")
    print(f"✓ Built {len(updates)} update entries")
    print(f"✓ {changes_count} ads have changes")
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(updates, f, indent=2)
    
    print(f"✓ Saved to: {output_file}")
    
    return len(updates), changes_count

if __name__ == '__main__':
    print("This script requires spreadsheet data to be provided manually")
    print("Use Claude Code MCP tools to fetch data and call build_updates() directly")
