#!/usr/bin/env python3
"""
Rebuild RSA update JSONs from spreadsheet data (not current API state)
This ensures Alex's changes in the spreadsheet are captured
"""

import json
import sys

sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync')

SPREADSHEET_ID = '189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo'

def fetch_spreadsheet_data(tab_name, range_spec):
    """Fetch data from Google Sheets via MCP"""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    import asyncio
    
    async def get_sheet_data():
        server_params = StdioServerParameters(
            command="/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-drive-mcp-server/.venv/bin/python",
            args=["/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-drive-mcp-server/server.py"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool(
                    "getGoogleSheetContent",
                    arguments={
                        "spreadsheetId": SPREADSHEET_ID,
                        "range": f"{tab_name}!{range_spec}"
                    }
                )
                
                if result and len(result.content) > 0:
                    import json
                    return json.loads(result.content[0].text)
                return None
    
    return asyncio.run(get_sheet_data())

def build_updates(region_name, tab_name, current_state_file, output_file):
    """Build update JSON from spreadsheet and current state"""
    
    print(f"\n{'='*80}")
    print(f"Building {region_name} RSA Updates from Spreadsheet")
    print(f"{'='*80}\n")
    
    # Load current state from API
    print(f"Loading current state from {current_state_file}...")
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)
    
    print(f"✓ Loaded {len(current_state)} ads from API")
    
    # Create lookup by ad ID
    current_by_id = {ad['ad_id']: ad for ad in current_state}
    
    # Fetch spreadsheet data
    print(f"\nFetching {tab_name} tab from spreadsheet...")
    sheet_data = fetch_spreadsheet_data(tab_name, "A1:AU200")
    
    if not sheet_data or 'values' not in sheet_data:
        print("❌ Failed to fetch spreadsheet data")
        return
    
    values = sheet_data['values']
    print(f"✓ Got {len(values)-1} rows from spreadsheet")
    
    # Parse spreadsheet
    headers = values[0]
    
    # Find column indices
    ad_id_idx = headers.index('Ad ID')
    campaign_idx = headers.index('Campaign Name')
    ad_group_idx = headers.index('Ad Group Name')
    final_url_idx = headers.index('Final URL')
    
    # Headline columns H1-H15
    h_indices = [headers.index(f'H{i}') for i in range(1, 16)]
    
    # Description columns D1-D4
    d_indices = [headers.index(f'D{i}') for i in range(1, 5)]
    
    updates = []
    matched = 0
    not_found = 0
    
    for row in values[1:]:  # Skip header
        if len(row) <= ad_id_idx:
            continue
            
        ad_id = str(row[ad_id_idx])
        
        # Find current state
        if ad_id not in current_by_id:
            print(f"⚠️  Ad ID {ad_id} not found in current state")
            not_found += 1
            continue
        
        current = current_by_id[ad_id]
        matched += 1
        
        # Extract headlines from spreadsheet
        new_headlines = []
        for idx in h_indices:
            if idx < len(row) and row[idx]:
                new_headlines.append(row[idx])
        
        # Extract descriptions from spreadsheet
        new_descriptions = []
        for idx in d_indices:
            if idx < len(row) and row[idx]:
                new_descriptions.append(row[idx])
        
        # Build update entry
        updates.append({
            'campaign_name': current['campaign_name'],
            'ad_group_name': current['ad_group_name'],
            'ad_id': ad_id,
            'status': current['status'],
            'current_headlines': current['current_headlines'],
            'new_headlines': new_headlines,
            'current_descriptions': current['current_descriptions'],
            'new_descriptions': new_descriptions,
            'final_url': row[final_url_idx] if final_url_idx < len(row) else current['final_url']
        })
    
    print(f"\n✓ Matched {matched} ads from spreadsheet")
    if not_found > 0:
        print(f"⚠️  {not_found} ads in spreadsheet not found in current state")
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(updates, f, indent=2)
    
    print(f"✓ Saved to: {output_file}")
    
    # Show sample diff
    if updates:
        sample = updates[0]
        print(f"\nSample (Ad ID {sample['ad_id']}):")
        print(f"  Campaign: {sample['campaign_name']}")
        
        if sample['current_headlines'] != sample['new_headlines']:
            print(f"  ✓ Headlines changed")
        else:
            print(f"  - Headlines unchanged")
            
        if sample['current_descriptions'] != sample['new_descriptions']:
            print(f"  ✓ Descriptions changed")
        else:
            print(f"  - Descriptions unchanged")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: rebuild_from_spreadsheet.py <region>")
        print("Region: UK, USA, EUR, ROW")
        sys.exit(1)
    
    region = sys.argv[1].upper()
    
    configs = {
        'UK': ('UK', 'UK', '../data/uk_rsa_current_state.json', '../data/uk_rsa_updates_from_sheet.json'),
        'USA': ('USA', 'USA', '../data/usa_rsa_current_state.json', '../data/usa_rsa_updates_from_sheet.json'),
        'EUR': ('EUR', 'EUR', '../data/eur_rsa_current_state.json', '../data/eur_rsa_updates_from_sheet.json'),
        'ROW': ('ROW', 'ROW', '../data/row_rsa_current_state.json', '../data/row_rsa_updates_from_sheet.json'),
    }
    
    if region not in configs:
        print(f"Unknown region: {region}")
        sys.exit(1)
    
    build_updates(*configs[region])
