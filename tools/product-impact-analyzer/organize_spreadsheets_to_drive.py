#!/usr/bin/env python3
"""
Organize Product Impact Analyzer spreadsheets into Google Drive folder structure

This script:
1. Finds/creates the proper folder structure for each client
2. Moves spreadsheets into: PetesBrain/clients/[client]/spreadsheets/
3. Updates the config.json with new locations (if needed)
"""

import json
import sys
from pathlib import Path

# Client name to folder mapping
CLIENT_FOLDER_MAP = {
    'Tree2mydoor': 'tree2mydoor',
    'Smythson UK': 'smythson',
    'BrightMinds': 'bright-minds',
    'Accessories for the Home': 'accessories-for-the-home',
    'Go Glean UK': 'go-glean',
    'Superspace': 'superspace',
    'Uno Lights': 'uno-lighting',
    'Godshot': 'godshot',
    'HappySnapGifts': 'clear-prospects',
    'WheatyBags': 'clear-prospects',
    'BMPM': 'clear-prospects',
    'Grain Guard': 'grain-guard',
    'Crowd Control': 'crowd-control',
    'Just Bin Bags': 'just-bin-bags',
    'Just Bin Bags JHD': 'just-bin-bags'
}

# Brand-specific filenames for multi-brand clients
BRAND_FILENAME_MAP = {
    'HappySnapGifts': 'product-performance-happysnapgifts',
    'WheatyBags': 'product-performance-wheatybags',
    'BMPM': 'product-performance-bmpm',
    'Just Bin Bags': 'product-performance-jbb',
    'Just Bin Bags JHD': 'product-performance-jhd'
}

def main():
    config_path = Path(__file__).parent / 'config.json'

    with open(config_path) as f:
        config = json.load(f)

    print("=" * 80)
    print("ORGANIZING PRODUCT IMPACT ANALYZER SPREADSHEETS")
    print("=" * 80)
    print()

    moves = []

    for client in config['clients']:
        sheet_id = client.get('product_performance_spreadsheet_id')
        if not sheet_id:
            continue

        client_name = client['name']
        folder_name = CLIENT_FOLDER_MAP.get(client_name)

        if not folder_name:
            print(f"⚠️  {client_name}: No folder mapping defined, skipping")
            continue

        # Determine filename
        if client_name in BRAND_FILENAME_MAP:
            filename = BRAND_FILENAME_MAP[client_name]
        else:
            filename = 'product-performance'

        # Target path
        target_path = f"PetesBrain/clients/{folder_name}/spreadsheets/{filename}"

        moves.append({
            'client': client_name,
            'sheet_id': sheet_id,
            'target_path': target_path
        })

        print(f"📊 {client_name}")
        print(f"   Sheet ID: {sheet_id}")
        print(f"   Target: {target_path}")
        print()

    print("=" * 80)
    print(f"READY TO MOVE {len(moves)} SPREADSHEETS")
    print("=" * 80)
    print()
    print("Use Google Drive MCP tools to:")
    print("1. Create folder structure if needed")
    print("2. Move each spreadsheet to target location")
    print("3. Verify new locations")
    print()

    # Save move plan
    with open('spreadsheet_move_plan.json', 'w') as f:
        json.dump(moves, f, indent=2)

    print("✅ Move plan saved to: spreadsheet_move_plan.json")

if __name__ == '__main__':
    main()
