#!/usr/bin/env python3
"""
Fetch product data for Clear Prospects using MCP Google Ads tool
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def fetch_shopping_data():
    """Fetch shopping performance data for Clear Prospects"""
    print("Fetching Shopping data for Clear Prospects...")

    customer_id = "6281395727"
    merchant_id = "7481296"  # HSG merchant ID

    query = """
    SELECT
        segments.date,
        segments.product_item_id,
        segments.product_title,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions_value
    FROM shopping_performance_view
    WHERE segments.date DURING LAST_7_DAYS
    """

    # Use subprocess to run MCP command and capture output
    cmd = [
        'python3', '-c',
        f"""
import json
from mcp_client import MCPClient

client = MCPClient()
result = client.google_ads.run_gaql(
    customer_id='{customer_id}',
    query='''{query}'''
)
print(json.dumps(result))
"""
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # Save to file
        output_file = Path(__file__).parent / "data" / "shopping_clear_prospects.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Saved {len(data.get('results', []))} rows to {output_file}")
        return True

    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        return False

def fetch_ads_data():
    """Fetch Google Ads performance data for Clear Prospects"""
    print("Fetching Google Ads data for Clear Prospects...")

    customer_id = "6281395727"

    query = """
    SELECT
        campaign.name,
        segments.date,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM campaign
    WHERE segments.date DURING LAST_7_DAYS
      AND campaign.status = 'ENABLED'
    """

    try:
        # Direct MCP call would go here, but for now just note what's needed
        print("  Note: Run this query via Claude Code MCP:")
        print(f"  Customer ID: {customer_id}")
        print(f"  Query: {query}")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Clear Prospects Data Fetcher")
    print("=" * 60)

    # This script shows what data we need
    # Actual fetching happens via Claude Code MCP tools

    print("\nTo fetch data for Clear Prospects, run these MCP commands:\n")

    print("1. Shopping Performance Data:")
    print("   mcp__google-ads__run_gaql(")
    print("       customer_id='6281395727',")
    print("       query='SELECT segments.date, segments.product_item_id,")
    print("              segments.product_title, metrics.clicks,")
    print("              metrics.cost_micros, metrics.conversions_value")
    print("              FROM shopping_performance_view")
    print("              WHERE segments.date DURING LAST_7_DAYS'")
    print("   )")
    print("   Save to: data/shopping_clear_prospects.json\n")

    print("2. Campaign Performance Data:")
    print("   mcp__google-ads__run_gaql(")
    print("       customer_id='6281395727',")
    print("       query='SELECT campaign.name, segments.date,")
    print("              metrics.clicks, metrics.cost_micros,")
    print("              metrics.conversions, metrics.conversions_value")
    print("              FROM campaign")
    print("              WHERE segments.date DURING LAST_7_DAYS")
    print("              AND campaign.status = \"ENABLED\"'")
    print("   )")
    print("   Save to: data/ads_clear_prospects.json\n")

    print("=" * 60)
