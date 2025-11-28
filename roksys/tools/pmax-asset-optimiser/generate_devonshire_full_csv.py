#!/usr/bin/env python3
"""
Generate COMPLETE Devonshire Hotels CSV from API data
All 80 assets with campaign names and asset groups
"""

import json
import csv

def convert_devonshire_api_to_csv(api_results, output_file):
    """Convert Devonshire API results to CSV with campaign name and asset group"""
    
    print(f"Converting {len(api_results)} assets to CSV...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["Performance Max campaigns"])
        writer.writerow([
            "Campaign",
            "Asset group",
            "Asset",
            "Asset type",
            "Performance label",
            "Impr.",
            "Clicks",
            "CTR",
            "Conversions",
            "Conv. rate",
            "Cost / conv."
        ])
        
        # Write data rows
        for result in api_results:
            campaign_name = result['campaign']['name']
            asset_group_name = result['assetGroup']['name']
            asset_text = result['asset']['textAsset']['text']
            
            # Map field type to human-readable format
            field_type_map = {
                'HEADLINE': 'Headline',
                'LONG_HEADLINE': 'Long headline',
                'DESCRIPTION': 'Description',
                'BUSINESS_NAME': 'Business Name'
            }
            field_type = field_type_map.get(result['assetGroupAsset']['fieldType'], result['assetGroupAsset']['fieldType'])
            
            metrics = result['metrics']
            impressions = int(metrics['impressions'])
            clicks = int(metrics['clicks'])
            ctr = float(metrics['ctr']) * 100  # Convert to percentage
            conversions = float(metrics.get('conversions', 0))
            cost_micros = int(metrics['costMicros'])
            cost = cost_micros / 1_000_000  # Convert micros to pounds
            
            # Calculate conversion rate and cost per conversion
            conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
            cost_per_conv = (cost / conversions) if conversions > 0 else 0
            
            writer.writerow([
                campaign_name,
                asset_group_name,
                asset_text,
                field_type,
                "",  # Performance label (not available in API)
                f"{impressions}",
                f"{clicks}",
                f"{ctr:.2f}%",
                f"{conversions:.2f}",
                f"{conv_rate:.2f}%",
                f"£{cost_per_conv:.2f}" if conversions > 0 else "£0.00"
            ])
    
    print(f"✅ CSV created: {output_file}")
    print(f"✅ {len(api_results)} assets processed")
    print()
    print("CSV includes:")
    print("  ✓ Campaign name column")
    print("  ✓ Asset group column")
    print("  ✓ All performance metrics")
    
    return output_file

# This script will be called with the actual API data
print("Devonshire CSV Generator Ready")
print("Waiting for API data...")
