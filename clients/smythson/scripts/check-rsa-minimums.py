#!/usr/bin/env python3
"""Check if RSA exports meet minimum requirements"""

import csv

def check_minimums(filename):
    print(f"\n=== Checking {filename} ===")

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Find column indices
        h1_idx = header.index('H1')
        d1_idx = header.index('D1')

        problems = []

        for i, row in enumerate(reader, start=2):
            # Count actual headlines (not #original or empty)
            headlines = []
            for j in range(h1_idx, h1_idx + 15):
                if j < len(row) and row[j] != '#original' and row[j].strip():
                    headlines.append(row[j])

            # Count actual descriptions (not #original or empty)
            descriptions = []
            for j in range(d1_idx, d1_idx + 4):
                if j < len(row) and row[j] != '#original' and row[j].strip():
                    descriptions.append(row[j])

            # Check minimums
            if len(headlines) < 3:
                problems.append(f"Line {i}: Only {len(headlines)} headlines (need 3+)")
                print(f"  ❌ Line {i}: {len(headlines)} headlines - {headlines[:3]}")

            if len(descriptions) < 2:
                problems.append(f"Line {i}: Only {len(descriptions)} descriptions (need 2+)")
                print(f"  ❌ Line {i}: {len(descriptions)} descriptions")

            # Show problem lines in detail
            if i in [7, 8, 9, 10, 11, 12, 26]:
                print(f"  Line {i}: {len(headlines)} headlines, {len(descriptions)} descriptions")

    if problems:
        print(f"\n❌ {filename}: {len(problems)} lines don't meet minimums")
    else:
        print(f"✅ {filename}: All lines meet minimums")

    return problems

# Check all fixed files
files = [
    'rsa-uk-export-fixed-20251215.csv',
    'rsa-usa-export-fixed-20251215.csv',
    'rsa-eur-export-fixed-20251215.csv',
    'rsa-row-export-fixed-20251215.csv'
]

all_problems = {}
for file in files:
    try:
        problems = check_minimums(file)
        if problems:
            all_problems[file] = problems
    except Exception as e:
        print(f"Error checking {file}: {e}")

if all_problems:
    print("\n❌ SUMMARY: Some files have lines that don't meet RSA minimums")
    print("RSAs require at least 3 headlines and 2 descriptions with actual values")
else:
    print("\n✅ All files meet RSA minimum requirements")