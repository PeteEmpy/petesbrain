#!/usr/bin/env python3
"""Verify RSA CSV files are ready for deployment"""

import csv
import os

os.chdir('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/spreadsheets')

files = {
    'UK': 'rsa-uk-proven-format-20251215.csv',
    'USA': 'rsa-usa-proven-format-20251215.csv',
    'EUR': 'rsa-eur-proven-format-20251215.csv',
    'ROW': 'rsa-row-proven-format-20251215.csv'
}

print("=" * 80)
print("RSA CSV VERIFICATION REPORT")
print("=" * 80)

all_problems = []

for region, filename in files.items():
    print(f"\n{'=' * 80}")
    print(f"REGION: {region}")
    print(f"FILE: {filename}")
    print(f"{'=' * 80}")

    if not os.path.exists(filename):
        print(f"❌ FILE NOT FOUND: {filename}")
        all_problems.append(f"{region}: File not found")
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Find column indices
        try:
            h1_idx = header.index('Headline 1')
            d1_idx = header.index('Description 1')
            account_idx = header.index('Account')
            campaign_idx = header.index('Campaign')
            ad_group_idx = header.index('Ad group')
        except ValueError as e:
            print(f"❌ HEADER ERROR: {e}")
            all_problems.append(f"{region}: Invalid header")
            continue

        rows = list(reader)
        total_ads = len(rows)

        print(f"\n📊 TOTAL ADS: {total_ads}")

        problems_this_file = []

        for i, row in enumerate(rows, start=2):
            # Count actual headlines (not --, not #original, not empty)
            headlines = []
            for j in range(h1_idx, min(h1_idx + 15, len(header))):
                if j < len(row) and row[j] and row[j] != '--' and row[j] != '#original':
                    headlines.append(row[j].strip())

            # Count actual descriptions
            descriptions = []
            for j in range(d1_idx, min(d1_idx + 4, len(header))):
                if j < len(row) and row[j] and row[j] != '--' and row[j] != '#original':
                    descriptions.append(row[j].strip())

            # Check minimums
            if len(headlines) < 3:
                problem = f"Line {i}: Only {len(headlines)} headlines (need 3+)"
                problems_this_file.append(problem)
                print(f"  ❌ {problem}")
                if row[campaign_idx]:
                    print(f"     Campaign: {row[campaign_idx]}")
                    print(f"     Ad Group: {row[ad_group_idx]}")

            if len(descriptions) < 2:
                problem = f"Line {i}: Only {len(descriptions)} descriptions (need 2+)"
                problems_this_file.append(problem)
                print(f"  ❌ {problem}")

        if not problems_this_file:
            print(f"\n✅ {region}: ALL {total_ads} ADS MEET MINIMUM REQUIREMENTS")
        else:
            print(f"\n❌ {region}: {len(problems_this_file)} PROBLEMS FOUND")
            all_problems.extend([f"{region}: {p}" for p in problems_this_file])

print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)

if not all_problems:
    print("\n✅✅✅ ALL FILES READY FOR DEPLOYMENT ✅✅✅")
    print("\nFiles can be imported into Google Ads Editor tomorrow.")
else:
    print(f"\n❌ {len(all_problems)} TOTAL PROBLEMS FOUND")
    print("\nProblems need to be fixed before deployment:")
    for problem in all_problems:
        print(f"  - {problem}")

print("\n" + "=" * 80)
