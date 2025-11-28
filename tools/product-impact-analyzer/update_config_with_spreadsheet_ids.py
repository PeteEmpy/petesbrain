#!/usr/bin/env python3
"""Add spreadsheet IDs to config.json"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config.json'

# Spreadsheet IDs from MCP creation
spreadsheet_ids = {
    "Tree2mydoor": "1fQ_OO48IzoojEi2nlcDRQAA9Me6vWzvRi7nyJ0YvycA",
    "Smythson UK": "1DtK0MX5qwISwO8blvbBT9rEQWqn-uVFp5hS3xBR-glo",
    "BrightMinds": "12jpLRhbMmZ-cIhmI53dY6hB520GhZGoKN_NTDxfX3ks",
    "Accessories for the Home": "1V23MwIeSDTj5ECBJAOIukENzy3YMxUoOEMiSP2IZAWM",
    "Go Glean UK": "1Jqy3Y4jQGUQFwyvjTHAb0JCOAxwndaIvZItvkU-xaqw",
    "Superspace": "1N8H0n1qL3jWHdWxKlbyF0ywjQ1Hn5YSbgxgC4Ig2B6s",
    "Uno Lights": "1vQAD5xOA-u2LWwB1AzxJJd1RJIBbqHpHHmlseO0Ko-A",
    "Godshot": "1Hrr27rAc1PpVxefSLja5TlEAD4Dg1rqNxbqn4FeaYCk",
    "HappySnapGifts": "1nTJyS3I5GlkRJfTeoTWBX3ehV-EDYnHOIn7Yq7raXd0",
    "WheatyBags": "1htjYR0YM5TFmd1NwIS6M6jSev86VsEJ5-okkX-5MOdI",
    "BMPM": "1EenJFkPWGZ6c_ZhsKKYudDcW2Nt8Jeamc1m55BPR5dU",
    "Grain Guard": "1VFyGERR0OHX12CwP76YUWexegrEoyhAaReGGRX9kMjw",
    "Crowd Control": "1V3RY5Kw5b22nzveWfDNQfjzsJ8CVdV4km0pXE3Nfofw",
    "Just Bin Bags": "1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA"
}

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Update each client
updated = 0
for client in config['clients']:
    client_name = client['name']
    if client_name in spreadsheet_ids:
        client['product_performance_spreadsheet_id'] = spreadsheet_ids[client_name]
        print(f"✓ {client_name}: {spreadsheet_ids[client_name]}")
        updated += 1

# Save config
with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=2)

print(f"\n✓ Updated {updated} clients in config.json")
