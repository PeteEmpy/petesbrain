#!/usr/bin/env python3
"""
Convert Bright Minds API Export to CSV Format

Takes the Google Ads API GAQL response and converts it to the CSV format
expected by the analysis scripts.
"""

import csv
import json

def convert_api_to_csv(api_results, output_file):
    """Convert API results to CSV format"""
    
    print("=" * 80)
    print("BRIGHT MINDS - API TO CSV CONVERSION")
    print("=" * 80)
    print()
    print(f"Input: {len(api_results)} text assets from API")
    print(f"Output: {output_file}")
    print()
    
    # CSV headers (double header row like manual export)
    header_row_1 = ["Performance Max campaigns"]
    header_row_2 = [
        "Campaign",
        "Asset group", 
        "Asset",
        "Asset type",
        "Performance label",  # Not available in API
        "Impr.",
        "Clicks",
        "CTR",
        "Conversions",
        "Conv. rate",
        "Cost / conv."
    ]
    
    rows = []
    
    # Map field types to readable format
    asset_type_map = {
        'HEADLINE': 'Headline',
        'LONG_HEADLINE': 'Long headline',
        'DESCRIPTION': 'Description'
    }
    
    for result in api_results:
        campaign_name = result['campaign']['name']
        asset_group_name = result['assetGroup']['name']
        asset_text = result['asset']['textAsset']['text']
        field_type = result['assetGroupAsset']['fieldType']
        asset_type = asset_type_map.get(field_type, field_type)
        
        # Metrics
        impressions = int(result['metrics']['impressions'])
        clicks = int(result['metrics']['clicks'])
        ctr = float(result['metrics']['ctr']) * 100  # Convert to percentage
        conversions = float(result['metrics']['conversions'])
        cost_micros = int(result['metrics']['costMicros'])
        cost = cost_micros / 1_000_000  # Convert to GBP
        
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
    print()
    
    # Summary by asset type
    print("Summary by asset type:")
    type_counts = {}
    for row in rows:
        asset_type = row[3]
        type_counts[asset_type] = type_counts.get(asset_type, 0) + 1
    
    for asset_type, count in sorted(type_counts.items()):
        print(f"   {asset_type}: {count}")
    
    print()
    
    # Summary by asset group
    print("Summary by asset group:")
    group_counts = {}
    for row in rows:
        asset_group = row[1]
        group_counts[asset_group] = group_counts.get(asset_group, 0) + 1
    
    for group, count in sorted(group_counts.items()):
        print(f"   {group}: {count}")
    
    print()
    print("=" * 80)
    
    return len(rows)


if __name__ == "__main__":
    print("This script will be called with actual API data")
    print("Preparing to convert 97 Bright Minds assets...")

