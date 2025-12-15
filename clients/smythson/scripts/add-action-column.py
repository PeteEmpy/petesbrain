#!/usr/bin/env python3
"""Add Action column to force Google Ads Editor to update instead of create"""

import csv

def add_action_column(input_file, output_file):
    """Add Action column set to 'Edit' to force updates"""

    rows = []

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Add Action column after Customer ID
        new_header = [header[0], 'Action'] + header[1:]
        rows.append(new_header)

        # Process data rows
        for row in reader:
            # Add 'Edit' action for all rows
            new_row = [row[0], 'Edit'] + row[1:]
            rows.append(new_row)

    # Write updated file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Created {output_file} with Action column")
    return output_file

# Process all files
files = [
    ('rsa-uk-editor-format-20251215.csv', 'rsa-uk-editor-with-action-20251215.csv'),
    ('rsa-usa-editor-format-20251215.csv', 'rsa-usa-editor-with-action-20251215.csv'),
    ('rsa-eur-editor-format-20251215.csv', 'rsa-eur-editor-with-action-20251215.csv'),
    ('rsa-row-editor-format-20251215.csv', 'rsa-row-editor-with-action-20251215.csv')
]

print("Adding Action column to force updates...")
print("=" * 50)

for input_file, output_file in files:
    add_action_column(input_file, output_file)

print("\n" + "=" * 50)
print("🎯 Files created with Action='Edit' column!")
print("\nUse these if download doesn't fix the issue:")
for _, output in files:
    print(f"  - {output}")