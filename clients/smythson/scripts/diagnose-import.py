#!/usr/bin/env python3
"""Diagnose which ads are updating vs failing"""

import csv

# Let's create 3 test files to isolate the problem
def create_diagnostic_files():
    """Split the UK file into smaller test batches"""

    with open('rsa-uk-clean-20251215.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        all_rows = list(reader)

        # Test 1: First 5 ads only
        with open('test-batch-1.csv', 'w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            for row in all_rows[:5]:
                writer.writerow(row)

        print("✅ test-batch-1.csv - First 5 ads:")
        for i, row in enumerate(all_rows[:5], 1):
            print(f"   {i}. {row[3]} - {row[1][:40]}")

        # Test 2: Ads 6-10
        with open('test-batch-2.csv', 'w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            for row in all_rows[5:10]:
                writer.writerow(row)

        print("\n✅ test-batch-2.csv - Ads 6-10:")
        for i, row in enumerate(all_rows[5:10], 6):
            print(f"   {i}. {row[3]} - {row[1][:40]}")

        # Test 3: Last 5 ads
        with open('test-batch-3.csv', 'w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            for row in all_rows[-5:]:
                writer.writerow(row)

        print("\n✅ test-batch-3.csv - Last 5 ads:")
        for i, row in enumerate(all_rows[-5:], 23):
            print(f"   {i}. {row[3]} - {row[1][:40]}")

create_diagnostic_files()

print("\n" + "="*50)
print("DIAGNOSTIC APPROACH:")
print("1. Try importing test-batch-1.csv")
print("2. Note which ads show as Updated vs Added vs Skipped")
print("3. This will tell us the pattern")
print("\nThe 3 that work likely have something in common:")
print("  - Specific campaign?")
print("  - Were downloaded in Editor's cache?")
print("  - Different ad group structure?")