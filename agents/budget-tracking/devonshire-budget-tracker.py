#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Devonshire Budget Tracker - Daily Update Script

Fetches current spend data from Google Ads and updates Google Sheets budget tracker.
Uses direct imports from MCP servers (no subprocess calls).

Schedule: Daily at 9:00 AM via LaunchAgent
"""

import os
import sys
from datetime import datetime, timedelta

# Add paths for direct imports
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server")
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server")

# Load environment variables from Google Ads MCP
env_file = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Import after environment is loaded
from oauth.google_auth import execute_gaql
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuration
ACCOUNT_ID = "5898250490"
THE_HIDE_CAMPAIGN_IDS = ["23069490466", "21815704991"]
SPREADSHEET_ID = "1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc"

# Sheets
DEV_PROPERTIES_SHEET = "Dev Properties Auto"
THE_HIDE_SHEET = "The Hide Properties Auto"

# Google Sheets credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

# Budget data (update monthly)
MONTHLY_BUDGETS = {
    "2025-10": {"dev": 11730.00, "hide": 2000.00},
    "2025-11": {"dev": 9000.00, "hide": 2000.00},
    "2025-12": {"dev": 7750.00, "hide": 2000.00},
    "2026-01": {"dev": 6750.00, "hide": 2000.00},
    "2026-02": {"dev": 6500.00, "hide": 2000.00},
    "2026-03": {"dev": 8000.00, "hide": 2000.00},
}


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_sheets_service():
    """Get Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)


def run_gaql(query):
    """Execute GAQL query via Google Ads MCP"""
    log("Executing GAQL query...")
    result = execute_gaql(ACCOUNT_ID, query)
    log("✓ Query complete")
    return result


def update_sheet(service, sheet_name, range_spec, values):
    """Update Google Sheet via Google Sheets API"""
    log(f"Updating {sheet_name} - {range_spec}...")
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!{range_spec}",
        valueInputOption="USER_ENTERED",
        body={"values": values}
    ).execute()
    log(f"✓ Updated {sheet_name}")


def micros_to_pounds(micros):
    return float(micros) / 1_000_000


def calculate_metrics(spend, budget, total_days, days_elapsed):
    days_remaining = total_days - days_elapsed
    expected_spend = (budget / total_days) * days_elapsed
    remaining_budget = budget - spend
    req_daily = remaining_budget / days_remaining if days_remaining > 0 else 0
    pacing_pct = (spend / expected_spend * 100) if expected_spend > 0 else 0
    predicted = (spend / days_elapsed * total_days) if days_elapsed > 0 else 0
    return {
        "days_remaining": days_remaining,
        "expected_spend": expected_spend,
        "remaining_budget": remaining_budget,
        "req_daily_budget": req_daily,
        "pacing_pct": pacing_pct,
        "predicted_spend": predicted
    }


def main():
    log("=" * 60)
    log("DEVONSHIRE BUDGET TRACKER - DAILY UPDATE")
    log("=" * 60)

    # Date info
    now = datetime.now()
    month_key = now.strftime("%Y-%m")
    day_of_month = now.day

    if now.month == 12:
        next_month = now.replace(year=now.year + 1, month=1, day=1)
    else:
        next_month = now.replace(month=now.month + 1, day=1)
    total_days = (next_month - timedelta(days=1)).day

    log(f"Month: {month_key}, Day: {day_of_month} of {total_days}")

    if month_key not in MONTHLY_BUDGETS:
        log(f"ERROR: No budget defined for {month_key}")
        return 1

    budgets = MONTHLY_BUDGETS[month_key]
    log(f"Dev Budget: £{budgets['dev']:,.2f}, Hide Budget: £{budgets['hide']:,.2f}")

    # Fetch data
    month_query = """
    SELECT campaign.id, campaign.name, metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.name LIKE '%DEV | Properties%'
    """

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_query = f"""
    SELECT campaign.id, metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.name LIKE '%DEV | Properties%'
    """

    month_data = run_gaql(month_query)
    yesterday_data = run_gaql(yesterday_query)
    log("✓ Fetched Google Ads data")

    # Process data
    dev_spend = hide_spend = dev_yesterday = hide_yesterday = 0

    for result in month_data.get("results", []):
        cid = result["campaign"]["id"]
        cost = micros_to_pounds(int(result["metrics"]["costMicros"]))
        if cid in THE_HIDE_CAMPAIGN_IDS:
            hide_spend += cost
        else:
            dev_spend += cost

    for result in yesterday_data.get("results", []):
        cid = result["campaign"]["id"]
        cost = micros_to_pounds(int(result["metrics"]["costMicros"]))
        if cid in THE_HIDE_CAMPAIGN_IDS:
            hide_yesterday += cost
        else:
            dev_yesterday += cost

    log(f"Dev MTD: £{dev_spend:,.2f}, Hide MTD: £{hide_spend:,.2f}")
    log(f"Dev Yesterday: £{dev_yesterday:,.2f}, Hide Yesterday: £{hide_yesterday:,.2f}")

    # Calculate metrics
    dev_metrics = calculate_metrics(dev_spend, budgets["dev"], total_days, day_of_month)
    hide_metrics = calculate_metrics(hide_spend, budgets["hide"], total_days, day_of_month)

    # Get Google Sheets service
    sheets_service = get_sheets_service()

    # Update sheets
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    update_sheet(sheets_service, DEV_PROPERTIES_SHEET, "B2", [[timestamp]])
    update_sheet(sheets_service, THE_HIDE_SHEET, "B2", [[timestamp]])

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
    update_sheet(sheets_service, DEV_PROPERTIES_SHEET, "E6:M6", dev_row)

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
    update_sheet(sheets_service, THE_HIDE_SHEET, "E7:M7", hide_row)

    # Summary
    log("=" * 60)
    log("UPDATE COMPLETE")
    log(f"Dev: £{dev_spend:,.2f} / £{budgets['dev']:,.2f} ({dev_metrics['pacing_pct']:.1f}%)")
    log(f"Hide: £{hide_spend:,.2f} / £{budgets['hide']:,.2f} ({hide_metrics['pacing_pct']:.1f}%)")
    log(f"Combined: £{dev_spend + hide_spend:,.2f}")

    combined_pacing = ((dev_spend + hide_spend) / (budgets['dev'] + budgets['hide']) * total_days / day_of_month) * 100
    if combined_pacing > 110:
        log(f"⚠️  WARNING: {combined_pacing:.1f}% pacing - OVERSPENDING!")
    elif combined_pacing < 90:
        log(f"⚠️  WARNING: {combined_pacing:.1f}% pacing - UNDERSPENDING!")
    else:
        log(f"✓ Pacing: {combined_pacing:.1f}% - ON TRACK")

    log("=" * 60)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
