#!/usr/bin/env python3
"""
Devonshire Budget Tracker - Daily Update Script

Fetches current spend data from Google Ads API and updates the automated
budget tracking sheets in Google Sheets.

Updates:
- Dev Properties Auto sheet (main campaigns excluding The Hide)
- The Hide Properties Auto sheet (The Hide campaign only)

Schedule: Daily at 9:00 AM via LaunchAgent
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add Google Ads MCP server path for imports
google_ads_path = Path(__file__).parent.parent.parent / "infrastructure" / "mcp-servers" / "google-ads-mcp-server"
google_sheets_path = Path(__file__).parent.parent.parent / "infrastructure" / "mcp-servers" / "google-sheets-mcp-server"
sys.path.insert(0, str(google_ads_path))
sys.path.insert(0, str(google_sheets_path))

# Import Google services
from oauth.google_auth import execute_gaql
from gsheet_service import gsheet_service

# Configuration
ACCOUNT_ID = "5898250490"
# The Hide campaigns (current + old paused Highwayman before rename)
THE_HIDE_CAMPAIGN_IDS = ["23069490466", "21815704991"]
SPREADSHEET_ID = "1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc"

# Sheets
DEV_PROPERTIES_SHEET = "Dev Properties Auto"
THE_HIDE_SHEET = "The Hide Properties Auto"

# Budget data (update monthly at the start of each new month)
MONTHLY_BUDGETS = {
    "2025-10": {"dev": 11730.00, "hide": 2000.00},
    "2025-11": {"dev": 9000.00, "hide": 2000.00},
    "2025-12": {"dev": 7750.00, "hide": 2000.00},
    "2026-01": {"dev": 6750.00, "hide": 2000.00},
    "2026-02": {"dev": 6500.00, "hide": 2000.00},
    "2026-03": {"dev": 8000.00, "hide": 2000.00},
}


def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_current_month_data():
    """Fetch current month spend for DEV | Properties campaigns (including paused)"""
    log("Fetching current month spend data for DEV | Properties campaigns...")

    query = """
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.name LIKE '%DEV | Properties%'
    """

    return execute_gaql(ACCOUNT_ID, query)


def get_yesterday_spend():
    """Fetch yesterday's spend for DEV | Properties campaigns (including paused)"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    log(f"Fetching yesterday's spend ({yesterday}) for DEV | Properties campaigns...")

    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.name LIKE '%DEV | Properties%'
    """

    return execute_gaql(ACCOUNT_ID, query)


def micros_to_pounds(micros):
    """Convert Google Ads micros to pounds"""
    return float(micros) / 1_000_000


def calculate_budget_metrics(spend, budget, total_days, days_elapsed):
    """Calculate pacing metrics"""
    days_remaining = total_days - days_elapsed
    expected_spend = (budget / total_days) * days_elapsed
    remaining_budget = budget - spend
    req_daily_budget = remaining_budget / days_remaining if days_remaining > 0 else 0
    pacing_pct = (spend / expected_spend * 100) if expected_spend > 0 else 0
    predicted_spend = (spend / days_elapsed * total_days) if days_elapsed > 0 else 0

    return {
        "days_remaining": days_remaining,
        "expected_spend": expected_spend,
        "remaining_budget": remaining_budget,
        "req_daily_budget": req_daily_budget,
        "pacing_pct": pacing_pct,
        "predicted_spend": predicted_spend
    }


def update_google_sheet(service, sheet_name, range_spec, values):
    """Update Google Sheets"""
    log(f"Updating {sheet_name} - {range_spec}...")

    try:
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet_name}!{range_spec}",
            valueInputOption="USER_ENTERED",
            body={"values": values}
        ).execute()
        log(f"✓ Updated {sheet_name}")
    except Exception as e:
        log(f"ERROR: Failed to update sheet: {e}")
        raise


def main():
    """Main update workflow"""
    log("=" * 60)
    log("DEVONSHIRE BUDGET TRACKER - DAILY UPDATE")
    log("=" * 60)

    # Initialize Google Sheets service
    try:
        sheets_service = gsheet_service()
        log("✓ Connected to Google Sheets API")
    except Exception as e:
        log(f"✗ Failed to connect to Google Sheets API: {e}")
        return 1

    # Get current date info
    now = datetime.now()
    month_key = now.strftime("%Y-%m")
    day_of_month = now.day

    # Get total days in month
    if now.month == 12:
        next_month = now.replace(year=now.year + 1, month=1, day=1)
    else:
        next_month = now.replace(month=now.month + 1, day=1)
    total_days = (next_month - timedelta(days=1)).day

    log(f"Month: {month_key}")
    log(f"Day: {day_of_month} of {total_days}")

    # Get budget for current month
    if month_key not in MONTHLY_BUDGETS:
        log(f"WARNING: No budget defined for {month_key}")
        log("Please update MONTHLY_BUDGETS in script")
        return 1

    budgets = MONTHLY_BUDGETS[month_key]
    log(f"Dev Properties Budget: £{budgets['dev']:,.2f}")
    log(f"The Hide Budget: £{budgets['hide']:,.2f}")

    # Fetch data from Google Ads
    try:
        month_data = get_current_month_data()
        yesterday_data = get_yesterday_spend()
        log("✓ Fetched Google Ads data")
    except Exception as e:
        log(f"✗ Failed to fetch Google Ads data: {e}")
        return 1

    # Process campaign data
    dev_spend = 0
    hide_spend = 0
    dev_yesterday = 0
    hide_yesterday = 0

    for result in month_data.get("results", []):
        campaign_id = result["campaign"]["id"]
        cost_micros = int(result["metrics"]["costMicros"])
        cost_pounds = micros_to_pounds(cost_micros)

        # The Hide includes both current campaign and old paused Highwayman
        if campaign_id in THE_HIDE_CAMPAIGN_IDS:
            hide_spend += cost_pounds
        else:
            dev_spend += cost_pounds

    for result in yesterday_data.get("results", []):
        campaign_id = result["campaign"]["id"]
        cost_micros = int(result["metrics"]["costMicros"])
        cost_pounds = micros_to_pounds(cost_micros)

        # The Hide includes both current campaign and old paused Highwayman
        if campaign_id in THE_HIDE_CAMPAIGN_IDS:
            hide_yesterday += cost_pounds
        else:
            dev_yesterday += cost_pounds

    log(f"Dev Properties Spend MTD: £{dev_spend:,.2f}")
    log(f"The Hide Spend MTD: £{hide_spend:,.2f}")
    log(f"Dev Yesterday: £{dev_yesterday:,.2f}")
    log(f"Hide Yesterday: £{hide_yesterday:,.2f}")

    # Calculate metrics for Dev Properties
    dev_metrics = calculate_budget_metrics(
        dev_spend, budgets["dev"], total_days, day_of_month
    )

    # Calculate metrics for The Hide
    hide_metrics = calculate_budget_metrics(
        hide_spend, budgets["hide"], total_days, day_of_month
    )

    # Update timestamp
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    update_google_sheet(sheets_service, DEV_PROPERTIES_SHEET, "B2", [[timestamp]])
    update_google_sheet(sheets_service, THE_HIDE_SHEET, "B2", [[timestamp]])

    # Update Dev Properties (row 6, columns E-M)
    # E: Days Elapsed, F: Days Remaining, G: Spend, H: Expected Spend,
    # I: Remaining Budget, J: Req Daily Budget, K: Pacing %,
    # L: Predicted Spend, M: Yesterday Spend
    dev_row = [[
        str(day_of_month),
        str(dev_metrics["days_remaining"]),
        f"{dev_spend:.2f}",
        f"{dev_metrics['expected_spend']:.2f}",
        f"{dev_metrics['remaining_budget']:.2f}",
        f"{dev_metrics['req_daily_budget']:.2f}",
        f"{dev_metrics['pacing_pct']:.2f}",
        f"{dev_metrics['predicted_spend']:.2f}",
        f"{dev_yesterday:.2f}"
    ]]
    update_google_sheet(sheets_service, DEV_PROPERTIES_SHEET, "E6:M6", dev_row)

    # Update The Hide (row 7, columns E-M)
    hide_row = [[
        str(day_of_month),
        str(hide_metrics["days_remaining"]),
        f"{hide_spend:.2f}",
        f"{hide_metrics['expected_spend']:.2f}",
        f"{hide_metrics['remaining_budget']:.2f}",
        f"{hide_metrics['req_daily_budget']:.2f}",
        f"{hide_metrics['pacing_pct']:.2f}",
        f"{hide_metrics['predicted_spend']:.2f}",
        f"{hide_yesterday:.2f}"
    ]]
    update_google_sheet(sheets_service, THE_HIDE_SHEET, "E7:M7", hide_row)

    # Summary
    log("=" * 60)
    log("UPDATE COMPLETE")
    log("=" * 60)
    log(f"Dev Properties: £{dev_spend:,.2f} / £{budgets['dev']:,.2f} ({dev_metrics['pacing_pct']:.1f}% pacing)")
    log(f"The Hide: £{hide_spend:,.2f} / £{budgets['hide']:,.2f} ({hide_metrics['pacing_pct']:.1f}% pacing)")
    log(f"Combined Total: £{dev_spend + hide_spend:,.2f}")

    # Alert if significantly off-pace
    combined_pacing = ((dev_spend + hide_spend) / (budgets['dev'] + budgets['hide']) * total_days / day_of_month) * 100
    if combined_pacing > 110:
        log(f"⚠️  WARNING: Combined pacing {combined_pacing:.1f}% - running significantly over!")
    elif combined_pacing < 90:
        log(f"⚠️  WARNING: Combined pacing {combined_pacing:.1f}% - running significantly under!")

    log("=" * 60)
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
