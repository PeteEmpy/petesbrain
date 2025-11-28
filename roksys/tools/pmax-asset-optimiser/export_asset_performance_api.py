#!/usr/bin/env python3
"""
Export Asset Performance Data via Google Ads API

Uses GAQL to fetch asset performance metrics for Performance Max campaigns.
"""

import sys
import csv
from datetime import datetime, timedelta

# Customer ID and campaign ID
CUSTOMER_ID = "1404868570"  # Bright Minds
CAMPAIGN_ID = "21064167535"  # BMI | P Max | Generic

def export_asset_performance():
    """Export asset performance using MCP Google Ads tool"""
    
    # Calculate date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    date_filter = f"segments.date >= '{start_date.strftime('%Y-%m-%d')}' AND segments.date <= '{end_date.strftime('%Y-%m-%d')}'"
    
    # Build GAQL query for asset performance
    query = f"""
        SELECT
            campaign.name,
            campaign.id,
            asset_group.name,
            asset_group.id,
            asset_group_asset.field_type,
            asset.text_asset.text,
            asset.id,
            asset.type,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros,
            segments.date
        FROM asset_group_asset
        WHERE campaign.id = {CAMPAIGN_ID}
        AND {date_filter}
        AND asset_group_asset.status = 'ENABLED'
        AND asset.type IN ('TEXT', 'IMAGE', 'YOUTUBE_VIDEO')
        ORDER BY metrics.impressions DESC
    """
    
    print("=" * 80)
    print("BRIGHT MINDS - ASSET PERFORMANCE EXPORT (API)")
    print("=" * 80)
    print(f"Customer ID: {CUSTOMER_ID}")
    print(f"Campaign ID: {CAMPAIGN_ID}")
    print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print("=" * 80)
    print()
    print("Query:")
    print(query)
    print()
    print("⚠️  NOTE: This script outputs the query for use with MCP tools")
    print("    Run via Claude Code with mcp__google-ads__run_gaql")
    print()

if __name__ == "__main__":
    export_asset_performance()
