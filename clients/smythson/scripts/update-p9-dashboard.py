#!/usr/bin/env python3
"""
Smythson P9 Dashboard Daily Update (December 2025)

Fetches latest performance data from Google Ads and updates the P9 Strategy Control Dashboard.
Focused on December-only tracking with £171,128 budget constraint.

Runs: Daily at 7:00 AM

IMPORTANT: This replaces the Q4 dashboard script. P9 is December only (Dec 1-31, 2025).
Budget: £171,128 (hard constraint)
Revenue Target: £1,121,694 (fixed, cannot change)
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add shared scripts to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "shared" / "scripts"))

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    import gspread
except ImportError:
    print("Error: Required packages not installed")
    print("Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread")
    sys.exit(1)

# Configuration
SPREADSHEET_ID = "10vRzZJuUQMX0l86plKcuZfdoiidoexI1LPYnhr6gJlU"
ACCOUNTS = {
    "UK": "8573235780",
    "USA": "7808690871",
    "EUR": "7679616761",
    "ROW": "5556710725"
}
MANAGER_ID = "2569949686"

# P9 Period (December 2025 only)
P9_START = datetime(2025, 12, 1)
P9_END = datetime(2025, 12, 31)
P9_DAYS = (P9_END - P9_START).days + 1  # 31 days

# P9 Budget - HARD CONSTRAINT
# Source: clients/smythson/documents/P9-REVENUE-STRATEGY-FINAL.html
P9_TOTAL_BUDGET = 171128  # £171,128 (confirmed Dec 4, 2025)

# P9 Revenue Target - FIXED (cannot change)
# Source: clients/smythson/documents/P9-REVENUE-STRATEGY-FINAL.html
P9_REVENUE_TARGET = 1121694  # £1,121,694 (requires 6.55x ROAS - stretch goal)

# Regional allocation (based on historical performance distribution)
# UK: 51.56%, USA: 31.64%, EUR: 10.94%, ROW: 5.86%
REGIONAL_BUDGET = {
    "UK": round(P9_TOTAL_BUDGET * 0.5156),    # £88,238
    "USA": round(P9_TOTAL_BUDGET * 0.3164),   # £54,145
    "EUR": round(P9_TOTAL_BUDGET * 0.1094),   # £18,721
    "ROW": round(P9_TOTAL_BUDGET * 0.0586)    # £10,024
}

REGIONAL_REVENUE_TARGET = {
    "UK": round(P9_REVENUE_TARGET * 0.5156),   # £578,370
    "USA": round(P9_REVENUE_TARGET * 0.3164),  # £354,904
    "EUR": round(P9_REVENUE_TARGET * 0.1094),  # £122,689
    "ROW": round(P9_REVENUE_TARGET * 0.0586)   # £65,731
}

# Target ROAS by region (calculated from targets)
TARGET_ROAS = {
    "UK": REGIONAL_REVENUE_TARGET["UK"] / REGIONAL_BUDGET["UK"],      # ~6.55x
    "USA": REGIONAL_REVENUE_TARGET["USA"] / REGIONAL_BUDGET["USA"],   # ~6.55x
    "EUR": REGIONAL_REVENUE_TARGET["EUR"] / REGIONAL_BUDGET["EUR"],   # ~6.55x
    "ROW": REGIONAL_REVENUE_TARGET["ROW"] / REGIONAL_BUDGET["ROW"]    # ~6.55x
}

# P9 Phases (internal tracking, not displayed on dashboard)
P9_PHASES = {
    "PHASE_1": {"start": datetime(2025, 12, 1), "end": datetime(2025, 12, 7), "name": "Cyber Week"},
    "PHASE_2A": {"start": datetime(2025, 12, 8), "end": datetime(2025, 12, 16), "name": "Last Order Dates"},
    "PHASE_2B": {"start": datetime(2025, 12, 17), "end": datetime(2025, 12, 23), "name": "Post-Last Orders"},
    "PHASE_3": {"start": datetime(2025, 12, 24), "end": datetime(2025, 12, 26), "name": "Christmas Day"},
    "PHASE_4": {"start": datetime(2025, 12, 27), "end": datetime(2025, 12, 31), "name": "Sale Launch"}
}

def get_current_phase(date):
    """Determine which P9 phase we're in based on date"""
    for phase_key, phase_info in P9_PHASES.items():
        if phase_info["start"] <= date <= phase_info["end"]:
            return phase_key, phase_info["name"]
    return "PHASE_4", "Sale Launch"  # Default to last phase if outside ranges

def get_google_ads_data(account_id, start_date, end_date):
    """Fetch performance data from Google Ads via MCP-style GAQL query

    IMPORTANT: All Smythson accounts report in GBP (£) natively.
    No currency conversion needed - UK, USA, EUR, ROW all use £.

    Uses customer-level query to ensure all data is captured.
    """
    try:
        from google.ads.googleads.client import GoogleAdsClient

        # Initialize Google Ads client
        client = GoogleAdsClient.load_from_storage(
            path=os.path.expanduser("~/google-ads.yaml")
        )

        ga_service = client.get_service("GoogleAdsService")

        # Format dates for GAQL (YYYY-MM-DD)
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        # CRITICAL: Use customer-level query, not campaign-level
        # Campaign-level queries can miss data
        query = f"""
            SELECT
                metrics.cost_micros,
                metrics.conversions_value,
                metrics.conversions
            FROM customer
            WHERE segments.date BETWEEN '{start_str}' AND '{end_str}'
        """

        response = ga_service.search(customer_id=account_id, query=query)

        # Aggregate metrics (customer-level returns one row per day)
        total_cost_micros = 0
        total_conv_value = 0
        total_conversions = 0

        for row in response:
            total_cost_micros += row.metrics.cost_micros
            total_conv_value += row.metrics.conversions_value
            total_conversions += row.metrics.conversions

        # Convert micros to actual currency (GBP)
        spend = total_cost_micros / 1_000_000
        revenue = total_conv_value
        roas = (revenue / spend * 100) if spend > 0 else 0  # ROAS as percentage

        return {
            "spend": spend,
            "revenue": revenue,
            "roas": roas,
            "conversions": total_conversions
        }

    except Exception as e:
        print(f"Error fetching Google Ads data for account {account_id}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "spend": 0,
            "revenue": 0,
            "roas": 0,
            "conversions": 0
        }

def calculate_status(actual, target, tolerance=0.15):
    """Calculate traffic light status based on actual vs target"""
    if actual >= target * (1 - tolerance):
        return "🟢"
    elif actual >= target * (1 - tolerance * 2):
        return "🟡"
    else:
        return "🔴"

def calculate_budget_risk(total_spend, days_elapsed, days_remaining, budget):
    """Calculate budget overrun risk based on current spending rate"""
    if days_elapsed == 0:
        return 0, 0  # No data yet

    daily_avg = total_spend / days_elapsed
    projected_total = total_spend + (daily_avg * days_remaining)
    overrun = projected_total - budget
    overrun_pct = (overrun / budget * 100) if budget > 0 else 0

    return projected_total, overrun_pct

def update_dashboard():
    """Update Google Sheet with latest P9 performance data"""

    print(f"Starting Smythson P9 Dashboard update - {datetime.now()}")

    # Initialize Google Sheets
    gc = gspread.service_account(
        filename=os.path.expanduser("~/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json")
    )
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

    # Calculate date ranges
    today = datetime.now()

    # If today is before P9 start or after P9 end, adjust
    if today < P9_START:
        print(f"P9 hasn't started yet (starts {P9_START.strftime('%Y-%m-%d')})")
        return None

    query_end = min(today, P9_END)
    days_elapsed = (query_end - P9_START).days + 1
    days_remaining = max(0, (P9_END - today).days)

    # Get current phase
    current_phase_key, current_phase_name = get_current_phase(today)

    # Fetch data for each region - P9 total (Dec 1 to today)
    regional_data = {}
    total_spend = 0
    total_revenue = 0
    total_conversions = 0

    print("Fetching regional data...")
    for region, account_id in ACCOUNTS.items():
        print(f"  Querying {region} account {account_id}...")
        data = get_google_ads_data(account_id, P9_START, query_end)
        regional_data[region] = data
        total_spend += data["spend"]
        total_revenue += data["revenue"]
        total_conversions += data["conversions"]

    # Calculate overall metrics
    overall_roas = (total_revenue / total_spend * 100) if total_spend > 0 else 0
    budget_used_pct = (total_spend / P9_TOTAL_BUDGET) * 100
    revenue_progress_pct = (total_revenue / P9_REVENUE_TARGET) * 100

    # Calculate budget risk
    projected_spend, overrun_pct = calculate_budget_risk(
        total_spend, days_elapsed, days_remaining, P9_TOTAL_BUDGET
    )

    # Calculate required daily spend to stay on budget
    budget_remaining = P9_TOTAL_BUDGET - total_spend
    required_daily_avg = budget_remaining / days_remaining if days_remaining > 0 else 0
    actual_daily_avg = total_spend / days_elapsed if days_elapsed > 0 else 0

    print(f"\nP9 Status Summary:")
    print(f"  Days elapsed: {days_elapsed}/{P9_DAYS}")
    print(f"  Total spend: £{total_spend:,.2f} / £{P9_TOTAL_BUDGET:,} ({budget_used_pct:.1f}%)")
    print(f"  Total revenue: £{total_revenue:,.2f} / £{P9_REVENUE_TARGET:,} ({revenue_progress_pct:.1f}%)")
    print(f"  Overall ROAS: {overall_roas:.0f}%")
    print(f"  Current daily avg: £{actual_daily_avg:,.2f}/day")
    print(f"  Required daily avg: £{required_daily_avg:,.2f}/day")
    print(f"  Projected spend: £{projected_spend:,.2f} ({'+' if overrun_pct > 0 else ''}{overrun_pct:.1f}%)")
    print(f"  Current phase: {current_phase_name}")

    # BATCH UPDATE: Collect all updates into a single list
    batch_updates = []

    # Update header with P9 period and last updated
    batch_updates.append({
        'range': 'B5',
        'values': [['P9 Strategy Control Dashboard - December 2025']]
    })
    batch_updates.append({
        'range': 'B6',
        'values': [[f'Period: {P9_START.strftime("%d %b")} - {P9_END.strftime("%d %b %Y")} | Last Updated: {today.strftime("%Y-%m-%d %H:%M")}']]
    })
    batch_updates.append({
        'range': 'B7',
        'values': [[f'Current Phase: {current_phase_name} | Day {days_elapsed} of {P9_DAYS}']]
    })

    # Update Budget Status section
    batch_updates.append({'range': 'B10', 'values': [['💰 BUDGET STATUS']]})
    batch_updates.append({'range': 'B11', 'values': [['P9 Budget (Hard Constraint)']]})
    batch_updates.append({'range': 'C11', 'values': [[f'£{P9_TOTAL_BUDGET:,}']]})

    batch_updates.append({'range': 'B12', 'values': [['Budget Used']]})
    batch_updates.append({'range': 'C12', 'values': [[f'£{total_spend:,.0f}']]})
    batch_updates.append({'range': 'D12', 'values': [[f'{budget_used_pct:.1f}%']]})

    batch_updates.append({'range': 'B13', 'values': [['Budget Remaining']]})
    batch_updates.append({'range': 'C13', 'values': [[f'£{budget_remaining:,.0f}']]})
    batch_updates.append({'range': 'D13', 'values': [[f'{days_remaining} days']]})

    batch_updates.append({'range': 'B14', 'values': [['Daily Burn Rate']]})
    batch_updates.append({'range': 'C14', 'values': [[f'£{actual_daily_avg:,.0f}/day']]})
    daily_status = "🔴" if actual_daily_avg > required_daily_avg * 1.1 else ("🟡" if actual_daily_avg > required_daily_avg else "🟢")
    batch_updates.append({'range': 'D14', 'values': [[daily_status]]})

    batch_updates.append({'range': 'B15', 'values': [['Required Daily Avg']]})
    batch_updates.append({'range': 'C15', 'values': [[f'£{required_daily_avg:,.0f}/day']]})

    batch_updates.append({'range': 'B16', 'values': [['Projected Total Spend']]})
    batch_updates.append({'range': 'C16', 'values': [[f'£{projected_spend:,.0f}']]})
    projection_status = "🔴" if overrun_pct > 5 else ("🟡" if overrun_pct > 0 else "🟢")
    batch_updates.append({'range': 'D16', 'values': [[projection_status]]})

    if overrun_pct > 0:
        batch_updates.append({'range': 'E16', 'values': [[f'+£{projected_spend - P9_TOTAL_BUDGET:,.0f} ({overrun_pct:.1f}% over)']]})

    # Update Revenue Status section
    batch_updates.append({'range': 'B19', 'values': [['📊 REVENUE STATUS']]})
    batch_updates.append({'range': 'B20', 'values': [['Revenue Target (Fixed)']]})
    batch_updates.append({'range': 'C20', 'values': [[f'£{P9_REVENUE_TARGET:,}']]})

    batch_updates.append({'range': 'B21', 'values': [['Revenue Achieved']]})
    batch_updates.append({'range': 'C21', 'values': [[f'£{total_revenue:,.0f}']]})
    batch_updates.append({'range': 'D21', 'values': [[f'{revenue_progress_pct:.1f}%']]})

    batch_updates.append({'range': 'B22', 'values': [['Overall ROAS']]})
    batch_updates.append({'range': 'C22', 'values': [[f'{overall_roas:.0f}%']]})
    target_blended_roas = (P9_REVENUE_TARGET / P9_TOTAL_BUDGET * 100)
    roas_status = "🟢" if overall_roas >= target_blended_roas * 0.85 else ("🟡" if overall_roas >= target_blended_roas * 0.70 else "🔴")
    batch_updates.append({'range': 'D22', 'values': [[roas_status]]})

    batch_updates.append({'range': 'B23', 'values': [['Required ROAS']]})
    batch_updates.append({'range': 'C23', 'values': [[f'{target_blended_roas:.0f}%']]})

    # Update Regional Performance section
    batch_updates.append({'range': 'B26', 'values': [['🌍 REGIONAL PERFORMANCE (Dec 1 - Today)']]})

    # Regional table header (row 27)
    batch_updates.append({'range': 'B27', 'values': [['Region']]})
    batch_updates.append({'range': 'C27', 'values': [['Spend']]})
    batch_updates.append({'range': 'D27', 'values': [['Revenue']]})
    batch_updates.append({'range': 'E27', 'values': [['ROAS']]})
    batch_updates.append({'range': 'F27', 'values': [['Target ROAS']]})
    batch_updates.append({'range': 'G27', 'values': [['Status']]})
    batch_updates.append({'range': 'H27', 'values': [['Budget']]})
    batch_updates.append({'range': 'I27', 'values': [['% Used']]})

    # Regional data rows (28-31: UK, USA, EUR, ROW)
    for i, region in enumerate(["UK", "USA", "EUR", "ROW"]):
        row = 28 + i
        data = regional_data[region]

        region_spend = data["spend"]
        region_revenue = data["revenue"]
        region_roas = data["roas"]
        region_budget = REGIONAL_BUDGET[region]
        region_target = REGIONAL_REVENUE_TARGET[region]
        region_target_roas = TARGET_ROAS[region] * 100  # Convert to percentage
        region_budget_used = (region_spend / region_budget * 100) if region_budget > 0 else 0

        # ROAS status
        roas_status = calculate_status(region_roas, region_target_roas, tolerance=0.15)

        # Region emoji
        region_emoji = {"UK": "🇬🇧", "USA": "🇺🇸", "EUR": "🇪🇺", "ROW": "🌏"}

        batch_updates.append({'range': f"B{row}", 'values': [[f"{region_emoji[region]} {region}"]]})
        batch_updates.append({'range': f"C{row}", 'values': [[f"£{region_spend:,.0f}"]]})
        batch_updates.append({'range': f"D{row}", 'values': [[f"£{region_revenue:,.0f}"]]})
        batch_updates.append({'range': f"E{row}", 'values': [[f"{region_roas:.0f}%"]]})
        batch_updates.append({'range': f"F{row}", 'values': [[f"{region_target_roas:.0f}%"]]})
        batch_updates.append({'range': f"G{row}", 'values': [[roas_status]]})
        batch_updates.append({'range': f"H{row}", 'values': [[f"£{region_budget:,}"]]})
        batch_updates.append({'range': f"I{row}", 'values': [[f"{region_budget_used:.1f}%"]]})

    # Regional totals row (32)
    batch_updates.append({'range': 'B32', 'values': [['TOTAL']]})
    batch_updates.append({'range': 'C32', 'values': [[f"£{total_spend:,.0f}"]]})
    batch_updates.append({'range': 'D32', 'values': [[f"£{total_revenue:,.0f}"]]})
    batch_updates.append({'range': 'E32', 'values': [[f"{overall_roas:.0f}%"]]})
    batch_updates.append({'range': 'F32', 'values': [[f"{target_blended_roas:.0f}%"]]})
    batch_updates.append({'range': 'G32', 'values': [[roas_status]]})
    batch_updates.append({'range': 'H32', 'values': [[f"£{P9_TOTAL_BUDGET:,}"]]})
    batch_updates.append({'range': 'I32', 'values': [[f"{budget_used_pct:.1f}%"]]})

    # EXECUTE BATCH UPDATE
    print(f"\nExecuting batch update with {len(batch_updates)} cell updates...")
    try:
        sheet.batch_update(batch_updates)
        print("✅ Dashboard updated successfully")
    except Exception as e:
        print(f"❌ Error during batch update: {e}")
        import traceback
        traceback.print_exc()
        return None

    return {
        "total_revenue": total_revenue,
        "total_spend": total_spend,
        "overall_roas": overall_roas,
        "budget_used_pct": budget_used_pct,
        "revenue_progress_pct": revenue_progress_pct,
        "regional_data": regional_data,
        "projected_spend": projected_spend,
        "overrun_pct": overrun_pct
    }

def save_to_json(data):
    """Save dashboard data to JSON for weekly summary integration"""
    if data is None:
        return

    import json

    # Save to shared/data for weekly summary to pick up
    output_file = Path(__file__).parent.parent.parent / "data/cache/smythson-p9-dashboard.json"

    # Get current phase
    current_phase_key, current_phase_name = get_current_phase(datetime.now())

    # Prepare data structure
    dashboard_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "p9_period": {
            "start": P9_START.strftime("%Y-%m-%d"),
            "end": P9_END.strftime("%Y-%m-%d"),
            "current_phase": current_phase_name,
            "days_elapsed": (datetime.now() - P9_START).days + 1,
            "days_remaining": max(0, (P9_END - datetime.now()).days)
        },
        "overall": {
            "revenue": round(data["total_revenue"], 2),
            "revenue_target": P9_REVENUE_TARGET,
            "revenue_progress_pct": round(data["revenue_progress_pct"], 1),
            "spend": round(data["total_spend"], 2),
            "budget": P9_TOTAL_BUDGET,
            "budget_used_pct": round(data["budget_used_pct"], 1),
            "roas": round(data["overall_roas"], 1),
            "roas_target": round((P9_REVENUE_TARGET / P9_TOTAL_BUDGET * 100), 1),
            "projected_spend": round(data["projected_spend"], 2),
            "overrun_pct": round(data["overrun_pct"], 1)
        },
        "regional": {}
    }

    # Add regional data
    for region in ["UK", "USA", "EUR", "ROW"]:
        regional_entry = data["regional_data"][region]
        dashboard_data["regional"][region] = {
            "revenue": round(regional_entry["revenue"], 2),
            "spend": round(regional_entry["spend"], 2),
            "roas": round(regional_entry["roas"], 1),
            "conversions": round(regional_entry["conversions"], 1)
        }

    # Save to JSON
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        print(f"✅ Dashboard data saved to {output_file}")
    except Exception as e:
        print(f"⚠️  Warning: Could not save dashboard data to JSON: {e}")

if __name__ == "__main__":
    try:
        data = update_dashboard()
        save_to_json(data)
        print("\n✅ Smythson P9 Dashboard update complete")
    except Exception as e:
        print(f"\n❌ Error updating dashboard: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
