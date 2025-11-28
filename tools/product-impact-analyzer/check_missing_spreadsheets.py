#!/usr/bin/env python3
"""Check which clients are missing Product Performance spreadsheets"""

import json
from pathlib import Path

config_path = Path(__file__).parent / 'config.json'
with open(config_path) as f:
    config = json.load(f)

missing = []
has_sheet = []

for client in config['clients']:
    if client.get('enabled') and client.get('merchant_id') and client['merchant_id'] != 'UNKNOWN':
        name = client['name']
        has_id = 'product_performance_spreadsheet_id' in client
        if has_id:
            has_sheet.append(name)
        else:
            missing.append(name)

print('=== CLIENTS WITH SPREADSHEETS ===')
for c in sorted(has_sheet):
    print(f'✓ {c}')

print('\n=== CLIENTS MISSING SPREADSHEETS ===')
for c in sorted(missing):
    print(f'✗ {c}')

print(f'\nTotal with spreadsheets: {len(has_sheet)}')
print(f'Total missing spreadsheets: {len(missing)}')
