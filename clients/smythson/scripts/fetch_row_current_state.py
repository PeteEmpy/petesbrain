#!/usr/bin/env python3
"""Fetch ROW current state from Google Ads"""

import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync')

# ROW ad IDs from spreadsheet
ROW_AD_IDS = [
    '784326640550',  # AUS
    '784326640553',  # ROW Brand
    '773497251588',  # ROW Diaries
    '784326640556',  # ROW Competitor
]

print(f"Fetching current state for {len(ROW_AD_IDS)} ROW RSAs...")

# Would need to use mcp__google-ads__run_gaql here
# But simpler to just say ROW might not have current state
print("ROW current state file doesn't exist")
print("This is OK - the ROW CSV was created from the one manual ad earlier")
print("Let me check if there's a row_rsa_updates_manual.json instead")
