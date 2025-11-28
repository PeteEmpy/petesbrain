#!/usr/bin/env python3
"""
Quick test script to swap assets on Test Asset Group using test spreadsheet.
This is a temporary test script - not for production use.
"""

# Test spreadsheet configuration
TEST_SPREADSHEET_ID = '1DteIfAtGPsnkRYiUwD5Q08NzEq9DsFBOIc3aXonndWI'
TEST_SHEET_NAME = 'Test Sheet'
TEST_RANGE = 'Test Sheet!A2:AA2'  # Just row 2 (one asset group)

# Target configuration
CUSTOMER_ID = '8573235780'  # UK account
MANAGER_ID = '2569949686'
EXPECTED_CAMPAIGN = 'SMY | UK | P Max | Test'
EXPECTED_ASSET_GROUP = 'Test Asset Group'

print("=" * 80)
print("SMYTHSON ASSET SWAP TEST")
print("=" * 80)
print(f"Test Spreadsheet: {TEST_SPREADSHEET_ID}")
print(f"Sheet: {TEST_SHEET_NAME}")
print(f"Target: {EXPECTED_CAMPAIGN} / {EXPECTED_ASSET_GROUP}")
print(f"Account: UK ({CUSTOMER_ID})")
print("=" * 80)
print()

# Instructions for running
print("MANUAL EXECUTION REQUIRED:")
print()
print("Since this is a test, please use the existing script with modified config:")
print()
print("1. Temporarily edit apply-text-assets-from-sheet.py line 34:")
print(f"   SPREADSHEET_ID = '{TEST_SPREADSHEET_ID}'")
print()
print("2. Temporarily edit line 40 (UK sheet_name):")
print(f"   'sheet_name': '{TEST_SHEET_NAME}',")
print()
print("3. Temporarily edit line 41 (UK data_range):")
print(f"   'data_range': '{TEST_RANGE}',")
print()
print("4. Run dry-run:")
print("   cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts")
print("   python3 apply-text-assets-from-sheet.py --region uk --dry-run")
print()
print("5. If dry-run looks good, run live:")
print("   python3 apply-text-assets-from-sheet.py --region uk")
print()
print("6. REMEMBER TO REVERT THE CHANGES after testing!")
print()
print("=" * 80)
