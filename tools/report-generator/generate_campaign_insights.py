#!/usr/bin/env python3
"""
Generate Campaign Insights Report for Any Client

Universal script that fetches real data via MCP and generates
comprehensive campaign + product analysis with HTML browser output.

Usage:
    python3 generate_campaign_insights.py <client-slug> --start-date YYYY-MM-DD --end-date YYYY-MM-DD
    python3 generate_campaign_insights.py tree2mydoor --start-date 2025-12-09 --end-date 2025-12-15
    python3 generate_campaign_insights.py smythson --days 7
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer
from report_html_generator import HTMLReportGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate Campaign Insights Report')
    parser.add_argument('client_slug', help='Client slug (e.g., tree2mydoor, smythson)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--days', type=int, default=7, help='Days back from today (default: 7)')

    args = parser.parse_args()

    # Calculate date range
    # CRITICAL: Use 3-day lookback for conversion lag (not yesterday)
    # Conversions take 24-48 hours to settle in Google Ads
    if args.start_date and args.end_date:
        start_date = args.start_date
        end_date = args.end_date
    else:
        end_date_obj = datetime.now() - timedelta(days=3)  # 3 days ago (conversion lag)
        start_date_obj = end_date_obj - timedelta(days=args.days - 1)
        start_date = start_date_obj.strftime('%Y-%m-%d')
        end_date = end_date_obj.strftime('%Y-%m-%d')

    print("=" * 100)
    print(f"{args.client_slug.upper().replace('-', ' ')} CAMPAIGN INSIGHTS REPORT")
    print("=" * 100)
    print(f"Date Range: {start_date} to {end_date}")
    print()

    # This script is designed to be called from Claude Code where MCP tools are available
    # The MCP data fetching happens in the skill, which then passes the data to the analyzer

    print("⚠️  This script should be called from the Claude Code skill 'campaign-insights-report'")
    print("The skill handles MCP data fetching and passes it to the analyzer.")
    print()
    print("To generate a report, use:")
    print(f"  Skill: campaign-insights-report")
    print(f"  Client: {args.client_slug}")
    print(f"  Dates: {start_date} to {end_date}")
    print()
    print("=" * 100)

    return 0


if __name__ == '__main__':
    sys.exit(main())
