#!/usr/bin/env python3
"""Create ultra-simple test file to check if Editor works at all"""

import csv

# Create the simplest possible test file
with open('simple-test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Minimal header
    writer.writerow(['Account', 'Ad', 'Headline 1'])

    # One simple row
    writer.writerow(['8573235780', '784157361259', 'Test headline'])

print("✅ Created simple-test.csv")
print("\nThis file has:")
print("  - 3 columns only")
print("  - 1 data row")
print("  - No special characters")
print("  - Basic ASCII text only")
print("\nIf Editor still hangs on this, the problem is with Editor itself.")

# Also create a version with Windows line endings
with open('simple-test-windows.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, lineterminator='\r\n')

    writer.writerow(['Account', 'Ad', 'Headline 1'])
    writer.writerow(['8573235780', '784157361259', 'Test headline'])

print("\n✅ Created simple-test-windows.csv")
print("  - With Windows line endings")
print("  - UTF-8 with BOM")
print("  - For better Windows compatibility")