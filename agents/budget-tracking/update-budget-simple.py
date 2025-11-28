#!/usr/bin/env python3
"""
Simple budget updater - manually updates Google Sheets
No MCP dependencies, uses Google Sheets API directly
"""

import os
import sys
from datetime import datetime, timedelta

# Add path for direct Google Sheets access
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server")
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server")

# Load environment variables
env_file = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from oauth.google_auth import execute_gaql

# Use googleapiclient directly
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

def get_sheets_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)

# Configuration
ACCOUNT_ID = "5898250490"
THE_HIDE_IDS = ["23069490466", "21815704991"]
SPREADSHEET_ID = "1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc"
BUDGETS = {"2025-11": {"dev": 9000.00, "hide": 2000.00}}

def main():
    now = datetime.now()
    month_key = now.strftime("%Y-%m")
    day = now.day

    # Get total days in month
    if now.month == 12:
        next_month = now.replace(year=now.year + 1, month=1, day=1)
    else:
        next_month = now.replace(month=now.month + 1, day=1)
    total_days = (next_month - timedelta(days=1)).day

    budgets = BUDGETS.get(month_key, {"dev": 9000, "hide": 2000})

    # Fetch data
    month_query = """
    SELECT campaign.id, metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.name LIKE '%DEV | Properties%'
    """

    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_query = f"""
    SELECT campaign.id, metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.name LIKE '%DEV | Properties%'
    """

    month_data = execute_gaql(ACCOUNT_ID, month_query)
    yesterday_data = execute_gaql(ACCOUNT_ID, yesterday_query)

    # Process
    dev_spend = hide_spend = dev_yesterday = hide_yesterday = 0

    for r in month_data.get("results", []):
        cost = float(r["metrics"]["costMicros"]) / 1_000_000
        if r["campaign"]["id"] in THE_HIDE_IDS:
            hide_spend += cost
        else:
            dev_spend += cost

    for r in yesterday_data.get("results", []):
        cost = float(r["metrics"]["costMicros"]) / 1_000_000
        if r["campaign"]["id"] in THE_HIDE_IDS:
            hide_yesterday += cost
        else:
            dev_yesterday += cost

    # Calculate
    def calc(spend, budget, total, elapsed):
        remaining = total - elapsed
        expected = (budget / total) * elapsed
        rem_budget = budget - spend
        req_daily = rem_budget / remaining if remaining > 0 else 0
        pacing = (spend / expected * 100) if expected > 0 else 0
        predicted = (spend / elapsed * total) if elapsed > 0 else 0
        return [elapsed, remaining, spend, expected, rem_budget, req_daily, pacing, predicted]

    dev_metrics = calc(dev_spend, budgets["dev"], total_days, day)
    hide_metrics = calc(hide_spend, budgets["hide"], total_days, day)

    # Update sheet
    service = get_sheets_service()
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    dev_row = [[str(day), str(dev_metrics[1]), f"{dev_spend:.2f}",
                f"{dev_metrics[3]:.2f}", f"{dev_metrics[4]:.2f}",
                f"{dev_metrics[5]:.2f}", f"{dev_metrics[6]:.2f}",
                f"{dev_metrics[7]:.2f}", f"{dev_yesterday:.2f}"]]

    hide_row = [[str(day), str(hide_metrics[1]), f"{hide_spend:.2f}",
                 f"{hide_metrics[3]:.2f}", f"{hide_metrics[4]:.2f}",
                 f"{hide_metrics[5]:.2f}", f"{hide_metrics[6]:.2f}",
                 f"{hide_metrics[7]:.2f}", f"{hide_yesterday:.2f}"]]

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Dev Properties Auto!B2",
        valueInputOption="USER_ENTERED",
        body={"values": [[timestamp]]}
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Dev Properties Auto!E6:M6",
        valueInputOption="USER_ENTERED",
        body={"values": dev_row}
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="The Hide Properties Auto!B2",
        valueInputOption="USER_ENTERED",
        body={"values": [[timestamp]]}
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="The Hide Properties Auto!E7:M7",
        valueInputOption="USER_ENTERED",
        body={"values": hide_row}
    ).execute()

    print(f"✓ Updated: Dev £{dev_spend:,.2f}, Hide £{hide_spend:,.2f}, Pacing {dev_metrics[6]:.1f}%")

if __name__ == "__main__":
    main()
