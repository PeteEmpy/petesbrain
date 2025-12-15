#!/usr/bin/env python3
"""Diagnose issues with UK RSA export problem lines"""

import csv

# Check the problem lines
problem_lines = [7, 8, 9, 10, 11, 12, 26]

with open('rsa-uk-export-final-20251215.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find indices
    h1_idx = header.index('H1')
    d1_idx = header.index('D1')
    final_url_idx = header.index('Final URL')

    print("Analyzing problem lines in UK export:\n")

    for i, row in enumerate(reader, start=2):
        if i not in problem_lines:
            continue

        # Count actual values vs #original
        headline_count = 0
        original_count = 0
        empty_count = 0

        for j in range(h1_idx, h1_idx + 15):
            if j < len(row):
                if row[j] == '#original':
                    original_count += 1
                elif row[j] == '':
                    empty_count += 1
                else:
                    headline_count += 1

        desc_count = 0
        desc_original = 0
        desc_empty = 0

        for j in range(d1_idx, d1_idx + 4):
            if j < len(row):
                if row[j] == '#original':
                    desc_original += 1
                elif row[j] == '':
                    desc_empty += 1
                else:
                    desc_count += 1

        print(f"Line {i}:")
        print(f"  Ad ID: {row[8]}")
        print(f"  Headlines: {headline_count} values, {original_count} #original, {empty_count} empty")
        print(f"  Descriptions: {desc_count} values, {desc_original} #original, {desc_empty} empty")

        # Check for issues
        issues = []

        # Issue 1: Too many #original?
        if original_count > 12:  # If more than 12 headlines are #original
            issues.append("Too many #original headlines")

        # Issue 2: Empty values (should be #original)
        if empty_count > 0:
            issues.append(f"{empty_count} empty headline fields (should be #original)")

        if desc_empty > 0:
            issues.append(f"{desc_empty} empty description fields (should be #original)")

        # Issue 3: H2 is #original on line 26
        if i == 26 and row[h1_idx + 1] == '#original':
            issues.append("H2 is #original (might need a value)")

        if issues:
            print(f"  ⚠️  Issues: {', '.join(issues)}")
        else:
            print(f"  ✅ No obvious issues found")
        print()

print("\n🔍 Possible causes of import errors:")
print("1. Google Ads Editor might not accept #original for certain fields")
print("2. Ads might need to be ENABLED to edit")
print("3. Some ads might not support all 15 headlines")
print("4. Empty fields should be removed entirely (not #original)")