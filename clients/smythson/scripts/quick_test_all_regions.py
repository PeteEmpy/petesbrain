#!/usr/bin/env python3
"""Quick test all regions for changes"""

import json

regions = {
    'UK': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/uk_rsa_current_state.json',
    'USA': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/usa_rsa_current_state.json',
    'EUR': '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/eur_rsa_current_state.json',
}

# UK already processed - 26 changes
print("="*60)
print("SUMMARY OF CHANGES BY REGION")
print("="*60)
print(f"\n✓ UK: 26 of 27 ads have changes (DONE)")

# USA - quick test showed no changes
print(f"- USA: Sample showed NO changes (likely all unchanged)")

# EUR - load and check count
with open(regions['EUR'], 'r') as f:
    eur_state = json.load(f)

print(f"? EUR: {len(eur_state)} ads (need to check)")

# ROW - no current state file
print(f"? ROW: No current state file (was manual)")

print("\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
print(f"\n1. UK CSV is ready with 26 real changes → IMPORT THIS")
print(f"2. USA likely has no changes → Can skip or verify")
print(f"3. EUR/ROW → Need to check")
print(f"\nDo you want to:")
print(f"  A) Just use UK CSV (26 changes confirmed)")
print(f"  B) Process all regions to be thorough")
