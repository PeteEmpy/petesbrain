#!/usr/bin/env python3
"""
Devonshire Budget Tracker - Daily Update Script

Fetches current spend data from Google Ads via MCP and updates
the automated budget tracking sheets in Google Sheets.

NOTE: This script must be run via Claude Code which provides MCP access.
"""

import json
import sys
from datetime import datetime, timedelta

# This script requires Claude Code MCP tools to be available
print("Note: This script requires Claude Code with MCP servers enabled.")
print("Please run via: Ask Claude Code to run the budget tracker script")

# Configuration
ACCOUNT_ID = "5898250490"
THE_HIDE_CAMPAIGN_ID = "23069490466"
SPREADSHEET_ID = "1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc"

# Sheets
DEV_PROPERTIES_SHEET = "Dev Properties Auto"
THE_HIDE_SHEET = "The Hide Properties Auto"

# Budget data (update monthly at the start of each new month)
# Historical note: The Hide launched Oct 10, 2025
MONTHLY_BUDGETS = {
    "2025-05": {"dev": 12000.00, "hide": 0.00},      # Historical estimate (pre-Hide)
    "2025-06": {"dev": 11500.00, "hide": 0.00},      # Historical estimate (pre-Hide)
    "2025-07": {"dev": 11500.00, "hide": 0.00},      # Historical estimate (pre-Hide)
    "2025-08": {"dev": 12000.00, "hide": 0.00},      # Historical estimate (pre-Hide)
    "2025-09": {"dev": 11500.00, "hide": 0.00},      # Historical estimate (pre-Hide)
    "2025-10": {"dev": 11730.00, "hide": 2000.00},   # The Hide launched Oct 10
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


def call_google_ads_mcp(query):
    """Call Google Ads MCP via npx"""
    try:
        # Use npx to call the Google Ads MCP server
        cmd = [
            "npx",
            "-y",
            "@heilmansights/google-ads-mcp@latest",
            "run_gaql",
            "--customer_id", ACCOUNT_ID,
            "--query", query
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        log("ERROR: Google Ads MCP call timed out")
        return None
    except subprocess.CalledProcessError as e:
        log(f"ERROR: Google Ads MCP call failed: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        log(f"ERROR: Failed to parse Google Ads response: {e}")
        return None


def call_google_sheets_mcp(action, **kwargs):
    """Call Google Sheets MCP via npx"""
    try:
        cmd = ["npx", "-y", "@modelcontextprotocol/server-google-sheets@latest", action]

        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        return json.loads(result.stdout) if result.stdout else None
    except Exception as e:
        log(f"ERROR: Google Sheets MCP call failed: {e}")
        return None


def get_current_month_data():
    """Fetch current month spend for DEV | Properties campaigns (excluding The Hide)"""
    log("Fetching current month spend data for DEV | Properties campaigns (excluding The Hide)...")

    query = """
    SELECT
      campaign.id,
      campaign.name,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING THIS_MONTH
      AND campaign.status = 'ENABLED'
      AND campaign.name LIKE '%DEV | Properties%'
      AND campaign.name NOT LIKE '%The Hide%'
      AND campaign.name NOT LIKE '%Highwayman%'
    """

    return call_google_ads_mcp(query)


def get_yesterday_spend():
    """Fetch yesterday's spend for DEV | Properties campaigns (excluding The Hide)"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    log(f"Fetching yesterday's spend ({yesterday}) for DEV | Properties campaigns (excluding The Hide)...")

    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date = '{yesterday}'
      AND campaign.status = 'ENABLED'
      AND campaign.name LIKE '%DEV | Properties%'
      AND campaign.name NOT LIKE '%The Hide%'
      AND campaign.name NOT LIKE '%Highwayman%'
    """

    return call_google_ads_mcp(query)


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


def update_google_sheet(sheet_name, range_spec, values):
    """Update Google Sheets using write_cells MCP tool"""
    log(f"Updating {sheet_name} - {range_spec}...")

    # Convert values to JSON string for command line
    values_json = json.dumps(values)

    try:
        result = call_google_sheets_mcp(
            "write_cells",
            spreadsheet_id=SPREADSHEET_ID,
            range_name=f"{sheet_name}!{range_spec}",
            values=values_json
        )

        if result:
            log(f"✓ Updated {sheet_name}")
        else:
            log(f"⚠️  Warning: Update may have failed for {sheet_name}")

    except Exception as e:
        log(f"ERROR: Failed to update {sheet_name}: {e}")
        raise


def get_month_spend(year, month):
    """Fetch spend for a specific month"""
    # Format dates for the month
    first_day = f"{year}-{month:02d}-01"

    # Get last day of month
    if month == 12:
        last_day = f"{year}-12-31"
    else:
        next_month = datetime(year, month + 1, 1)
        last_day = (next_month - timedelta(days=1)).strftime("%Y-%m-%d")

    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      metrics.cost_micros
    FROM campaign
    WHERE segments.date BETWEEN '{first_day}' AND '{last_day}'
      AND campaign.status = 'ENABLED'
      AND campaign.name LIKE '%DEV | Properties%'
      AND campaign.name NOT LIKE '%The Hide%'
      AND campaign.name NOT LIKE '%Highwayman%'
    """

    return call_google_ads_mcp(query)


def update_budget_history():
    """Update past budgets section showing last 6 months with actual spend vs budget"""
    log("Updating past budgets section...")

    now = datetime.now()

    # Create header matching main tracking format
    history_rows = [
        ["PAST BUDGETS (Last 6 Months)"],
        ["Start Date", "End Date", "Budget", "Total Days", "Days Elapsed", "Days Remaining",
         "Spend", "Expected Spend", "Remaining Budget", "Req Daily Budget", "Pacing %",
         "Predicted Spend", "Yesterday Spend", "Notes"]
    ]

    # Get last 6 complete months (excluding current month)
    for i in range(6, 0, -1):
        # Go back i months
        month_date = now - timedelta(days=i*30)
        year = month_date.year
        month = month_date.month
        month_key = month_date.strftime("%Y-%m")

        if month_key in MONTHLY_BUDGETS:
            budgets = MONTHLY_BUDGETS[month_key]

            # Get first and last day of month
            first_day = datetime(year, month, 1)
            if month == 12:
                last_day = datetime(year, 12, 31)
            else:
                next_month = datetime(year, month + 1, 1)
                last_day = next_month - timedelta(days=1)

            total_days = last_day.day

            # Fetch actual spend for this month
            log(f"Fetching spend for {month_key}...")
            month_data = get_month_spend(year, month)

            actual_spend = 0
            if month_data:
                for result in month_data.get("results", []):
                    cost_micros = int(result["metrics"]["costMicros"])
                    actual_spend += micros_to_pounds(cost_micros)

            # Calculate metrics (all days elapsed for past months)
            expected_spend = budgets["dev"]  # Full budget
            remaining_budget = budgets["dev"] - actual_spend
            pacing_pct = (actual_spend / expected_spend * 100) if expected_spend > 0 else 0

            # Format row matching main tracking structure
            history_rows.append([
                first_day.strftime("%Y-%m-%d"),
                last_day.strftime("%Y-%m-%d"),
                f"£{budgets['dev']:,.2f}",
                str(total_days),
                str(total_days),  # All days elapsed
                "0",  # No days remaining
                f"{actual_spend:.2f}",
                f"{expected_spend:.2f}",
                f"{remaining_budget:.2f}",
                "0",  # No daily budget needed
                f"{pacing_pct:.2f}",
                f"{actual_spend:.2f}",  # Predicted = actual for past months
                "0",  # No yesterday data for past months
                f"Completed - {month_date.strftime('%B %Y')}"
            ])

    # Write to both sheets starting at row 20 (below Future Budgets)
    try:
        # Calculate range based on number of rows (header + 6 months)
        end_row = 20 + len(history_rows) - 1
        update_google_sheet(DEV_PROPERTIES_SHEET, f"A20:N{end_row}", history_rows)
        update_google_sheet(THE_HIDE_SHEET, f"A20:N{end_row}", history_rows)
        log("✓ Past budgets updated")
    except Exception as e:
        log(f"⚠️ Warning: Failed to update past budgets: {e}")


def main():
    """Main update workflow"""
    log("=" * 60)
    log("DEVONSHIRE BUDGET TRACKER - DAILY UPDATE")
    log("=" * 60)

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
    month_data = get_current_month_data()
    if not month_data:
        log("✗ Failed to fetch month data")
        return 1

    yesterday_data = get_yesterday_spend()
    if not yesterday_data:
        log("✗ Failed to fetch yesterday data")
        return 1

    log("✓ Fetched Google Ads data")

    # Process campaign data
    dev_spend = 0
    hide_spend = 0
    dev_yesterday = 0
    hide_yesterday = 0

    for result in month_data.get("results", []):
        campaign_id = result["campaign"]["id"]
        cost_micros = int(result["metrics"]["costMicros"])
        cost_pounds = micros_to_pounds(cost_micros)

        if campaign_id == THE_HIDE_CAMPAIGN_ID:
            hide_spend += cost_pounds
        else:
            dev_spend += cost_pounds

    for result in yesterday_data.get("results", []):
        campaign_id = result["campaign"]["id"]
        cost_micros = int(result["metrics"]["costMicros"])
        cost_pounds = micros_to_pounds(cost_micros)

        if campaign_id == THE_HIDE_CAMPAIGN_ID:
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
    update_google_sheet(DEV_PROPERTIES_SHEET, "B2", [[timestamp]])
    update_google_sheet(THE_HIDE_SHEET, "B2", [[timestamp]])

    # Update Dev Properties (row 6, columns E-M)
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
    update_google_sheet(DEV_PROPERTIES_SHEET, "E6:M6", dev_row)

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
    update_google_sheet(THE_HIDE_SHEET, "E7:M7", hide_row)

    # Update budget history section
    update_budget_history()

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
        sys.exit(main())
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
