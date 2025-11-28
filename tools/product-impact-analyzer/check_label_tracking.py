#!/usr/bin/env python3
"""Check which clients have label tracking enabled"""

import json
from pathlib import Path

config_path = Path(__file__).parent / 'config.json'
with open(config_path) as f:
    config = json.load(f)

print('=== LABEL TRACKING STATUS ===\n')

enabled_clients = []
disabled_clients = []

for client in config['clients']:
    if client.get('enabled') and client.get('merchant_id') and client['merchant_id'] != 'UNKNOWN':
        name = client['name']
        lt = client.get('label_tracking', {})
        is_enabled = lt.get('enabled', False)
        label_field = lt.get('label_field', 'N/A')
        notes = lt.get('notes', '')

        if is_enabled:
            enabled_clients.append((name, label_field))
        else:
            disabled_clients.append((name, notes))

print('ENABLED LABEL TRACKING:')
for name, field in sorted(enabled_clients):
    print(f'  ✓ {name} (field: {field})')

print(f'\nDISABLED LABEL TRACKING:')
for name, notes in sorted(disabled_clients):
    print(f'  ✗ {name}')
    if notes:
        print(f'    Reason: {notes}')

print(f'\nTotal enabled: {len(enabled_clients)}')
print(f'Total disabled: {len(disabled_clients)}')
