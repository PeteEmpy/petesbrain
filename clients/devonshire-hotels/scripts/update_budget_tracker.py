#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
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
google_ads_path = Path(__file__).parent.parent.parent.parent / "infrastructure" / "mcp-servers" / "google-ads-mcp-server"
google_sheets_path = Path(__file__).parent.parent.parent.parent / "infrastructure" / "mcp-servers" / "google-sheets-mcp-server"
sys.path.insert(0, str(google_ads_path))
sys.path.insert(0, str(google_sheets_path))

# Load environment variables from Google Ads MCP
env_file = str(google_ads_path / ".env")
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Import Google services
from oauth.google_auth import execute_gaql
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuration
ACCOUNT_ID = "5898250490"
# The Hide campaigns (current + old paused Highwayman before rename)
THE_HIDE_CAMPAIGN_IDS = ["23069490466", "21815704991"]
SPREADSHEET_ID = "1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc"

# Sheets
DEV_PROPERTIES_SHEET = "Dev Properties Auto"
THE_HIDE_SHEET = "The Hide Properties Auto"

# Google Sheets credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

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
    """Fetch current month spend for Core Properties and Self Catering campaigns"""
    log("Fetching current month spend data for Core Properties and Self Catering campaigns...")

    # Query for Core Properties campaigns
    query_core = """
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.name LIKE '%Core Properties%'
    """

    # Query for Self Catering campaigns
    query_self_catering = """
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.name LIKE '%Self Catering%'
    """

    # Query for The Hide campaign (tracked separately but needs to be fetched)
    query_hide = """
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.name LIKE '%The Hide%'
    """

    # Combine results from all queries
    core_results = execute_gaql(ACCOUNT_ID, query_core)
    self_catering_results = execute_gaql(ACCOUNT_ID, query_self_catering)
    hide_results = execute_gaql(ACCOUNT_ID, query_hide)

    # Merge results, avoiding duplicates by campaign ID
    seen_ids = set()
    combined_results = []

    for result in core_results.get("results", []):
        cid = result["campaign"]["id"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            combined_results.append(result)

    for result in self_catering_results.get("results", []):
        cid = result["campaign"]["id"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            combined_results.append(result)

    for result in hide_results.get("results", []):
        cid = result["campaign"]["id"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            combined_results.append(result)

    return {"results": combined_results}


def get_yesterday_spend():
    """Fetch yesterday's spend for Core Properties and Self Catering campaigns"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    log(f"Fetching yesterday's spend ({yesterday}) for Core Properties and Self Catering campaigns...")

    # Query for Core Properties campaigns
    query_core = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.name LIKE '%Core Properties%'
    """

    # Query for Self Catering campaigns
    query_self_catering = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.name LIKE '%Self Catering%'
    """

    # Query for The Hide campaign (tracked separately but needs to be fetched)
    query_hide = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.name LIKE '%The Hide%'
    """

    # Combine results from all queries
    core_results = execute_gaql(ACCOUNT_ID, query_core)
    self_catering_results = execute_gaql(ACCOUNT_ID, query_self_catering)
    hide_results = execute_gaql(ACCOUNT_ID, query_hide)

    # Merge results, avoiding duplicates by campaign ID
    seen_ids = set()
    combined_results = []

    for result in core_results.get("results", []):
        cid = result["campaign"]["id"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            combined_results.append(result)

    for result in self_catering_results.get("results", []):
        cid = result["campaign"]["id"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            combined_results.append(result)

    for result in hide_results.get("results", []):
        cid = result["campaign"]["id"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            combined_results.append(result)

    return {"results": combined_results}


def micros_to_pounds(micros):
    """Convert Google Ads micros to pounds"""
    return float(micros) / 1_000_000


def calculate_budget_metrics(spend, budget, total_days, days_elapsed):
    """Calculate pacing metrics"""
    days_remaining = total_days - days_elapsed
    expected_spend = (budget / total_days) * days_elapsed
    remaining_budget = budget - spend
    req_daily_budget = remaining_budget / days_remaining if days_remaining > 0 else 0
    predicted_spend = (spend / days_elapsed * total_days) if days_elapsed > 0 else 0
    # Pacing % = Predicted Spend / Budget (are we on track to hit budget?)
    pacing_pct = (predicted_spend / budget * 100) if budget > 0 else 0

    return {
        "days_remaining": days_remaining,
        "expected_spend": expected_spend,
        "remaining_budget": remaining_budget,
        "req_daily_budget": req_daily_budget,
        "pacing_pct": pacing_pct,
        "predicted_spend": predicted_spend
    }


def read_budget_from_sheet(service, sheet_name, cell):
    """Read budget value from spreadsheet (source of truth)"""
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet_name}!{cell}"
        ).execute()
        values = result.get('values', [[]])
        if values and values[0]:
            # Parse the value, removing currency symbols and commas
            raw_value = str(values[0][0]).replace('£', '').replace(',', '').strip()
            return float(raw_value)
        return 0.0
    except Exception as e:
        log(f"ERROR: Failed to read budget from {sheet_name}!{cell}: {e}")
        return 0.0


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
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        sheets_service = build('sheets', 'v4', credentials=creds)
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

    # Read budgets from spreadsheet (source of truth) - Column C, Row 6 for each sheet
    log("Reading budgets from spreadsheet...")
    dev_budget = read_budget_from_sheet(sheets_service, DEV_PROPERTIES_SHEET, "C6")
    hide_budget = read_budget_from_sheet(sheets_service, THE_HIDE_SHEET, "C7")

    if dev_budget == 0 or hide_budget == 0:
        log("WARNING: Could not read budgets from spreadsheet, using fallback values")
        budgets = MONTHLY_BUDGETS.get(month_key, {"dev": 9000.00, "hide": 2000.00})
        dev_budget = dev_budget or budgets["dev"]
        hide_budget = hide_budget or budgets["hide"]

    log(f"Dev Properties Budget: £{dev_budget:,.2f}")
    log(f"The Hide Budget: £{hide_budget:,.2f}")

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
        dev_spend, dev_budget, total_days, day_of_month
    )

    # Calculate metrics for The Hide
    hide_metrics = calculate_budget_metrics(
        hide_spend, hide_budget, total_days, day_of_month
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
    log(f"Dev Properties: £{dev_spend:,.2f} / £{dev_budget:,.2f} ({dev_metrics['pacing_pct']:.1f}% pacing)")
    log(f"The Hide: £{hide_spend:,.2f} / £{hide_budget:,.2f} ({hide_metrics['pacing_pct']:.1f}% pacing)")
    log(f"Combined Total: £{dev_spend + hide_spend:,.2f}")

    # Alert if significantly off-pace (using predicted spend vs budget)
    combined_predicted = dev_metrics['predicted_spend'] + hide_metrics['predicted_spend']
    combined_budget = dev_budget + hide_budget
    combined_pacing = (combined_predicted / combined_budget * 100) if combined_budget > 0 else 0
    if combined_pacing > 110:
        log(f"⚠️  WARNING: Combined pacing {combined_pacing:.1f}% - predicted to exceed budget!")
    elif combined_pacing < 90:
        log(f"⚠️  WARNING: Combined pacing {combined_pacing:.1f}% - predicted to underspend!")

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
