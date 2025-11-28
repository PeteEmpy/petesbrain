#!/usr/bin/env python3
"""
Devonshire Hotels Budget Tracker Updater
Automatically updates Google Sheets budget tracker with live data from Google Ads MCP

Usage:
    python3 update_budget_tracker.py [spreadsheet_id]

    If no spreadsheet_id provided, uses the existing budget tracker:
    1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc

Requirements:
    - Google Ads MCP server configured
    - Google Sheets MCP server configured
    - Access to Devonshire Hotels Google Ads account (5898250490)
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import MCP modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared" / "mcp-servers"))

# Default spreadsheet ID (existing budget tracker)
DEFAULT_SPREADSHEET_ID = "1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc"

# Google Ads account details
GOOGLE_ADS_CUSTOMER_ID = "5898250490"
DEV_PROPERTIES_FILTER = "%DEV | Properties%"
THE_HIDE_CAMPAIGN_ID = "23069490466"
THE_HIDE_CAMPAIGN_NAME = "DEV | Properties | The Hide"

def get_current_month_date_range():
    """Get start and end date for current month"""
    today = datetime.now()
    start_date = today.replace(day=1).strftime("%Y-%m-%d")
    # Get last day of month
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    end_date = (next_month - timedelta(days=1)).strftime("%Y-%m-%d")

    return start_date, end_date, today.strftime("%Y-%m-%d")

def calculate_days_in_month(year, month):
    """Calculate total days in a given month"""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    return (next_month - datetime(year, month, 1)).days

def fetch_google_ads_data():
    """
    Fetch campaign spend data from Google Ads using MCP

    Returns:
        dict: Campaign spend data
    """
    print("🔍 Fetching data from Google Ads...")

    # This is a placeholder - in production, this would call the Google Ads MCP
    # For now, you'll need to integrate this with your MCP setup

    # Example structure of what this should return:
    return {
        "dev_properties_campaigns": [
            # List of campaigns excluding The Hide
        ],
        "the_hide_campaign": {
            "id": THE_HIDE_CAMPAIGN_ID,
            "name": THE_HIDE_CAMPAIGN_NAME,
            "spend": 0.0,
            "yesterday_spend": 0.0
        },
        "total_dev_properties_spend": 0.0,
        "total_dev_properties_yesterday": 0.0
    }

def calculate_budget_metrics(budget, total_days, days_elapsed, actual_spend):
    """
    Calculate budget pacing metrics

    Args:
        budget: Total monthly budget
        total_days: Total days in month
        days_elapsed: Days elapsed so far
        actual_spend: Actual spend to date

    Returns:
        dict: Calculated metrics
    """
    days_remaining = total_days - days_elapsed
    daily_budget = budget / total_days
    expected_spend = daily_budget * days_elapsed
    remaining_budget = budget - actual_spend
    required_daily_budget = remaining_budget / days_remaining if days_remaining > 0 else 0
    pacing_percentage = (actual_spend / expected_spend * 100) if expected_spend > 0 else 0
    predicted_spend = (actual_spend / days_elapsed * total_days) if days_elapsed > 0 else 0

    return {
        "expected_spend": expected_spend,
        "remaining_budget": remaining_budget,
        "required_daily_budget": required_daily_budget,
        "pacing_percentage": pacing_percentage,
        "predicted_spend": predicted_spend,
        "days_remaining": days_remaining
    }

def format_currency(amount):
    """Format amount as GBP currency"""
    return f"£{amount:,.2f}"

def format_percentage(percentage):
    """Format percentage"""
    return f"{percentage:.2f}%"

def update_spreadsheet(spreadsheet_id, data):
    """
    Update Google Sheet with calculated budget data

    Args:
        spreadsheet_id: Google Sheet ID
        data: Budget data to write
    """
    print(f"📊 Updating spreadsheet {spreadsheet_id}...")

    # This is a placeholder - in production, this would call the Google Sheets MCP
    # to write the data to the appropriate ranges

    print("✅ Spreadsheet updated successfully!")

def main():
    """Main execution function"""
    print("=" * 60)
    print("Devonshire Hotels - Budget Tracker Updater")
    print("=" * 60)
    print()

    # Get spreadsheet ID from args or use default
    spreadsheet_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SPREADSHEET_ID

    # Get current month date range
    start_date, end_date, today = get_current_month_date_range()
    print(f"📅 Processing period: {start_date} to {end_date}")
    print(f"📅 Today: {today}")
    print()

    # Calculate days
    now = datetime.now()
    total_days = calculate_days_in_month(now.year, now.month)
    days_elapsed = now.day

    print(f"📊 Month progress: {days_elapsed}/{total_days} days")
    print()

    # Fetch data from Google Ads
    ads_data = fetch_google_ads_data()

    # You would integrate the actual MCP calls here
    print("⚠️  This script is a template. You need to integrate it with:")
    print("   1. Google Ads MCP to fetch spend data")
    print("   2. Google Sheets MCP to write updates")
    print()
    print("   See the code comments for integration points.")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
