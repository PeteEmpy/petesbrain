#!/usr/bin/env python3
"""
Upload US search terms data to destination spreadsheet.
"""
import csv
import json

# Read CSV file
us_data = []
with open('product-feeds/us/us-data-new.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:  # Skip empty rows
            us_data.append(row)

print(f"Read {len(us_data)} rows (including header)")

# Print row count for verification
print(f"Total rows to upload: {len(us_data)}")
print(f"First row (header): {us_data[0]}")
print(f"Second row (sample): {us_data[1] if len(us_data) > 1 else 'N/A'}")
print(f"Last row (sample): {us_data[-1]}")

# Save to JSON for easy inspection
with open('us-data-for-upload.json', 'w') as f:
    json.dump(us_data, f, indent=2)

print("\nData prepared. Ready for upload to Google Sheets.")
print(f"Data saved to: us-data-for-upload.json")
