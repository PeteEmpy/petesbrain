#!/usr/bin/env python3
"""Fix RSA exports to use Add for new ads and Edit for existing ones"""

import csv

def fix_action_for_file(input_file, output_file):
    """Fix Action based on Ad ID - placeholder IDs mean new ads"""

    rows = []

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        # Find column indices
        action_idx = header.index('Action')
        ad_id_idx = header.index('Ad ID')

        for row in reader:
            if not row:
                continue

            # Check if Ad ID looks like a placeholder
            ad_id = row[ad_id_idx]

            # Placeholder IDs are short (like 789012) or contain "123456"
            # Real Google Ads IDs are 12+ digits
            if len(ad_id) < 12 or ad_id in ['789012', '123456']:
                # This is a new ad - use Add
                row[action_idx] = 'Add'
                print(f"  Changed to Add: Ad ID {ad_id}")

                # For new ads, we can't use #original - need to remove them
                for i, val in enumerate(row):
                    if val == '#original':
                        row[i] = ''  # Clear #original for new ads
            else:
                # This is an existing ad - keep Edit
                row[action_idx] = 'Edit'

            rows.append(row)

    # Write the fixed file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return len(rows) - 1  # Return number of data rows

# Fix EUR and ROW files which have placeholder Ad IDs
files_to_fix = [
    ('rsa-eur-export-fixed-20251215.csv', 'rsa-eur-export-final-20251215.csv'),
    ('rsa-row-export-fixed-20251215.csv', 'rsa-row-export-final-20251215.csv')
]

print("Fixing EUR and ROW files (placeholder Ad IDs → Add action):")
for input_file, output_file in files_to_fix:
    print(f"\n{input_file}:")
    count = fix_action_for_file(input_file, output_file)
    print(f"  ✅ Created {output_file} ({count} ads)")

# Also create final versions for UK and USA (no changes needed but for consistency)
import shutil

print("\nCopying UK and USA files (already correct):")
shutil.copy('rsa-uk-export-fixed-20251215.csv', 'rsa-uk-export-final-20251215.csv')
print("  ✅ Created rsa-uk-export-final-20251215.csv")

shutil.copy('rsa-usa-export-fixed-20251215.csv', 'rsa-usa-export-final-20251215.csv')
print("  ✅ Created rsa-usa-export-final-20251215.csv")

print("\n🎯 Final files ready for import:")
print("  - rsa-uk-export-final-20251215.csv (Edit existing ads)")
print("  - rsa-usa-export-final-20251215.csv (Edit existing ads)")
print("  - rsa-eur-export-final-20251215.csv (Add new ad)")
print("  - rsa-row-export-final-20251215.csv (Add new ad)")