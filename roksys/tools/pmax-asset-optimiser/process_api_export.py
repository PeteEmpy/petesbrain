#!/usr/bin/env python3
"""
Process Bright Minds API Export to CSV

Converts the Google Ads API GAQL response into the CSV format expected by the analysis scripts.
"""

import csv
import json

# API response data (97 text assets)
api_results = """PASTE_API_RESULTS_HERE"""

def convert_to_csv(results, output_file):
    """Convert API results to CSV format matching manual export"""

    # CSV headers (double header row like manual export)
    header_row_1 = ["Performance Max campaigns"]
    header_row_2 = [
        "Campaign",
        "Asset group",
        "Asset",
        "Asset type",
        "Performance label",  # Not available in API
        "Impressions",
        "Clicks",
        "CTR",
        "Conversions",
        "Conv. rate",
        "Cost / conv."
    ]

    rows = []

    for result in results:
        campaign_name = result['campaign']['name']
        asset_group_name = result['assetGroup']['name']
        asset_text = result['asset']['textAsset']['text']
        field_type = result['assetGroupAsset']['fieldType']

        # Map field type to readable format
        asset_type_map = {
            'HEADLINE': 'Headline',
            'LONG_HEADLINE': 'Long headline',
            'DESCRIPTION': 'Description'
        }
        asset_type = asset_type_map.get(field_type, field_type)

        # Metrics
        impressions = int(result['metrics']['impressions'])
        clicks = int(result['metrics']['clicks'])
        ctr = float(result['metrics']['ctr']) * 100  # Convert to percentage
        conversions = float(result['metrics']['conversions'])
        cost_micros = int(result['metrics']['costMicros'])
        cost = cost_micros / 1_000_000  # Convert to currency

        # Calculate conv rate and cost/conv
        conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
        cost_per_conv = (cost / conversions) if conversions > 0 else 0

        row = [
            campaign_name,
            asset_group_name,
            asset_text,
            asset_type,
            "",  # Performance label not available in API
            impressions,
            clicks,
            f"{ctr:.2f}%",
            f"{conversions:.2f}",
            f"{conv_rate:.2f}%",
            f"£{cost_per_conv:.2f}" if conversions > 0 else "£0.00"
        ]

        rows.append(row)

    # Write CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header_row_1)
        writer.writerow(header_row_2)
        writer.writerows(rows)

    print(f"✅ Converted {len(rows)} assets to CSV")
    print(f"   Output: {output_file}")
    print()
    print("Summary by asset type:")

    # Count by type
    type_counts = {}
    for row in rows:
        asset_type = row[3]
        type_counts[asset_type] = type_counts.get(asset_type, 0) + 1

    for asset_type, count in sorted(type_counts.items()):
        print(f"   {asset_type}: {count}")

if __name__ == "__main__":
    print("This script needs to be updated with the actual API results")
    print("The API returned 97 text assets for Bright Minds")
