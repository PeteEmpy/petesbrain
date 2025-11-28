#!/usr/bin/env python3
"""
Smythson Q4 Dashboard Daily Update

Fetches latest performance data from Google Ads and updates the Q4 Strategy Control Dashboard.
Sends email summary to petere@roksys.co.uk with current status.

Runs: Daily at 7:00 AM

IMPORTANT: All budget, revenue, and ROAS targets defined in this script are authoritative.
For reference, see: /Users/administrator/Documents/PetesBrain/clients/smythson/SMYTHSON-Q4-AUTHORITATIVE-FIGURES.md
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

# Phase dates
PHASE_1_START = datetime(2025, 11, 3)   # Initial launches
PHASE_2_START = datetime(2025, 11, 15)  # Mid-November adjustments (UK ROAS reduction)
PHASE_3_START = datetime(2025, 11, 25)  # Thanksgiving boost (USA ROAS reduction)
PHASE_4_START = datetime(2025, 12, 1)   # December peak optimization

# Budget configuration by phase
BUDGETS = {
    "PHASE_1": {"UK": 2716, "USA": 2264, "EUR": 868, "ROW": 354},  # Nov 3-14
    "PHASE_2": {"UK": 2716, "USA": 2264, "EUR": 868, "ROW": 354},  # Nov 15-24 (UK ROAS changes, budgets same)
    "PHASE_3": {"UK": 2716, "USA": 2604, "EUR": 868, "ROW": 354},  # Nov 25-30 (USA budget +15%)
    "PHASE_4": {"UK": 2557, "USA": 2131, "EUR": 817, "ROW": 333}   # Dec 1-31
}

# ROAS targets by phase
# Based on FINAL agreed Q4 2025 strategy (gomarble.ai report)
TARGET_ROAS = {
    "PHASE_1": {"UK": 4.3, "USA": 2.5, "EUR": 1.5, "ROW": 1.0},  # Oct 29 - Nov 14 (baseline launch)
    "PHASE_2": {"UK": 3.8, "USA": 2.2, "EUR": 1.3, "ROW": 1.0},  # Nov 15-24 (UK & USA reductions)
    "PHASE_3": {"UK": 3.8, "USA": 2.2, "EUR": 1.3, "ROW": 1.0},  # Nov 25-30 (USA budget +15%, ROAS maintained)
    "PHASE_4": {"UK": 3.5, "USA": 2.0, "EUR": 1.2, "ROW": 0.9}   # Dec 1-31 (peak season reductions)
}

# Q4 overall targets and dates
Q4_START = datetime(2025, 10, 29)
Q4_END = datetime(2025, 12, 31)
NOVEMBER_START = datetime(2025, 11, 3)
NOVEMBER_END = datetime(2025, 11, 30)
DECEMBER_START = datetime(2025, 12, 1)
DECEMBER_END = datetime(2025, 12, 31)

# CRITICAL: Christmas delivery cutoff
# Campaigns must pause ~Dec 22 to ensure delivery before Christmas
# This affects SPEND calculations (not revenue - orders placed earlier still convert)
CHRISTMAS_DELIVERY_CUTOFF = datetime(2025, 12, 22)
EFFECTIVE_DECEMBER_SPEND_DAYS = (CHRISTMAS_DELIVERY_CUTOFF - DECEMBER_START).days  # 21 days, not 31

# Q4 Total Budget - ACTUAL APPROVED (Nov 2025 clarification - CORRECTED Nov 17)
# P7 (Sep 29 - Nov 2): £151,072 (no underspend, fully spent)
# P8 (Nov 3-30): £186,051 (NO carryforward from P7)
# P9 (Dec 1-28): £183,929
TOTAL_BUDGET = 521052  # £521,052 total Q4 budget (P7: £151,072 + P8: £186,051 + P9: £183,929)

# Revenue Target - Based on P7 actuals + P8/P9 realistic projections
# CORRECTED Nov 28: P8 and P9 targets updated to reflect actual targets
# P7 (Oct 29 - Nov 2): £479,840 actual revenue (£151k spend @ 318% ROAS)
# P8 (Nov 3 - Nov 30): £1,119,436 target (£186,051 budget @ 602% ROAS)
# P9 (Dec 1 - Dec 28): £1,121,694 target (£183,929 budget @ 610% ROAS)
# Total Q4: £479,840 + £1,119,436 + £1,121,694 = £2,720,970 revised Q4 target
TOTAL_REVENUE_TARGET = 2720970  # £2,720,970 total Q4 revenue target (revised Nov 28)

# Regional revenue targets by month - CORRECTED Nov 28
# P8 (Nov 3-30): £1,119,436 total → regional split maintaining proportions
# UK: 51.56% × £1,119,436 = £577,208 (705% ROAS on £81,862 budget)
# USA: 31.64% × £1,119,436 = £354,194 (529% ROAS on £66,978 budget)
# EUR: 10.94% × £1,119,436 = £122,440 (470% ROAS on £26,047 budget)
# ROW: 5.86% × £1,119,436 = £65,594 (588% ROAS on £11,163 budget)
NOVEMBER_REVENUE_TARGETS = {
    "UK": 577208,
    "USA": 354194,
    "EUR": 122440,
    "ROW": 65594
}

# P9 (Dec 1-28): CORRECTED Nov 28
# Full 28-day period targets (not 21-day cutoff)
# UK: 51.56% × £1,121,694 = £578,372 (714% ROAS on £80,976 budget)
# USA: 31.64% × £1,121,694 = £354,908 (527% ROAS on £67,332 budget)
# EUR: 10.94% × £1,121,694 = £122,687 (476% ROAS on £25,750 budget)
# ROW: 5.86% × £1,121,694 = £65,726 (666% ROAS on £9,871 budget)
# Note: Previous calculations assumed 21-day Christmas cutoff, but current targets reflect full month budget allocation
DECEMBER_REVENUE_TARGETS = {
    "UK": 578372,
    "USA": 354908,
    "EUR": 122687,
    "ROW": 65726
}

# Email configuration
EMAIL_TO = "petere@roksys.co.uk"
EMAIL_FROM = "petere@roksys.co.uk"

def get_google_ads_data(account_id, start_date, end_date):
    """Fetch performance data from Google Ads via API

    IMPORTANT: All Smythson accounts report in GBP (£) natively.
    No currency conversion needed - UK, USA, EUR, ROW all use £.
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

        # GAQL query to get performance metrics
        query = f"""
            SELECT
                metrics.cost_micros,
                metrics.conversions_value,
                metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '{start_str}' AND '{end_str}'
        """

        response = ga_service.search(customer_id=account_id, query=query)

        # Aggregate metrics
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
        roas = revenue / spend if spend > 0 else 0

        return {
            "spend": spend,
            "revenue": revenue,
            "roas": roas,
            "conversions": total_conversions
        }

    except Exception as e:
        print(f"Error fetching Google Ads data for account {account_id}: {e}")
        return {
            "spend": 0,
            "revenue": 0,
            "roas": 0,
            "conversions": 0
        }

def get_current_phase(date):
    """Determine which strategy phase we're in based on date"""
    if date >= PHASE_4_START:
        return "PHASE_4"
    elif date >= PHASE_3_START:
        return "PHASE_3"
    elif date >= PHASE_2_START:
        return "PHASE_2"
    elif date >= PHASE_1_START:
        return "PHASE_1"
    else:
        return "PHASE_1"  # Default to phase 1

def calculate_status(actual, target, tolerance=0.15):
    """Calculate traffic light status based on actual vs target"""
    if actual >= target:
        return "🟢"
    elif actual >= target * (1 - tolerance):
        return "🟡"
    else:
        return "🔴"

def calculate_weighted_pacing(start_date, end_date, current_date, phase_changes=None):
    """
    Calculate expected revenue pacing with weighted factors based on Q4 2024 actual performance:
    - Actual daily revenue distribution from Q4 2024 (not assumed multipliers)
    - Phase transitions (budget/ROAS changes)
    - Peak shopping periods (Black Friday, Cyber Monday) based on real data

    Returns a value between 0 and 1 representing expected progress toward monthly target
    """
    if current_date < start_date:
        return 0.0
    if current_date >= end_date:
        return 1.0

    total_days = (end_date - start_date).days
    days_elapsed = (current_date - start_date).days

    # Load Q4 2024 actual revenue distribution
    # This replaces assumed multipliers with real historical data
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        q4_data_path = os.path.join(script_dir, 'q4-2024-revenue-distribution.json')

        with open(q4_data_path, 'r') as f:
            q4_2024_data = json.load(f)

        # Extract daily multipliers (day of month -> multiplier)
        # Convert "2024-11-23" format to day number (23)
        q4_multipliers = {}
        for date_str, multiplier in q4_2024_data['daily_multipliers'].items():
            date_parts = date_str.split('-')
            month = int(date_parts[1])
            day = int(date_parts[2])

            # Store by (month, day) tuple
            q4_multipliers[(month, day)] = multiplier

        using_real_data = True
    except Exception as e:
        print(f"Warning: Could not load Q4 2024 data, using fallback multipliers: {e}")
        # Fallback to basic multipliers if file not available
        q4_multipliers = {}
        using_real_data = False

    # Fallback multipliers (only used if Q4 2024 data unavailable)
    # December 2024 data not yet available, so keep assumptions for Dec
    # NOTE: These multipliers apply to REVENUE (orders placed/converting)
    # SPEND multipliers should account for Dec 22 delivery cutoff separately
    fallback_december_multipliers = {
        # Pre-Christmas peak (Dec 15-22) - assumed 1.3x normal
        # Dec 23+ has minimal spend due to delivery cutoff, but revenue still converts
        (12, 15): 1.3, (12, 16): 1.3, (12, 17): 1.3, (12, 18): 1.3,
        (12, 19): 1.3, (12, 20): 1.3, (12, 21): 1.3, (12, 22): 1.3,

        # Post-cutoff (Dec 23+) - revenue still comes in but minimal new spend
        (12, 23): 0.3, (12, 24): 0.2, (12, 25): 0.1,

        # Post-Christmas - assumed 0.9x normal (for any campaigns that restart)
        (12, 26): 0.9, (12, 27): 0.9, (12, 28): 0.9,
    }

    # Learning period multipliers (campaigns need time to optimize)
    # November campaigns started Nov 3
    learning_start = datetime(2025, 11, 3)

    # Phase transition dates (budget/ROAS changes cause temporary performance dips)
    phase_transitions = [
        datetime(2025, 11, 15),  # Phase 2: UK ROAS reduction, ROW launch
        datetime(2025, 11, 25),  # Phase 3: USA budget increase
        datetime(2025, 12, 1),   # Phase 4: All regions ROAS reductions
    ]

    # Calculate weighted days elapsed and total weighted days
    weighted_elapsed = 0
    weighted_total = 0

    for day_offset in range(total_days):
        day = start_date + timedelta(days=day_offset)

        # Base weight: Start with Q4 2024 actual daily multiplier
        # This replaces all assumed CVR lifts and peak periods with real data
        day_key = (day.month, day.day)

        if day_key in q4_multipliers:
            # Use actual Q4 2024 revenue distribution for this day
            weight = q4_multipliers[day_key]
        elif day.month == 12 and day_key in fallback_december_multipliers:
            # December 2024 data not yet available, use fallback
            weight = fallback_december_multipliers[day_key]
        else:
            # Default to 1.0 for days without data
            weight = 1.0

        # Apply phase transition multipliers (ROAS/budget changes cause temporary dips)
        # This is still relevant as it accounts for 2025 account changes
        for transition_date in phase_transitions:
            days_since_transition = (day - transition_date).days
            if 0 <= days_since_transition <= 2:
                # Days 0-2 after transition: Re-learning period
                weight *= 0.85

        # Add to total weighted days
        weighted_total += weight

        # Add to elapsed if this day has passed
        if day_offset < days_elapsed:
            weighted_elapsed += weight

    # Return weighted pacing (what proportion of the weighted total has passed)
    return weighted_elapsed / weighted_total if weighted_total > 0 else 0.0


def calculate_predicted_revenue(actual_revenue, actual_spend, remaining_budget, target_roas,
                                 start_date, end_date, current_date):
    """
    Calculate spending-capacity-constrained predicted revenue using historical weighting.

    This replaces the naive "actual / pacing" calculation with a realistic projection
    that accounts for:
    1. Actual spending capacity (based on current daily spend rate, not theoretical budget)
    2. Current ROAS performance vs target (trending)
    3. Historical revenue distribution of remaining days (Q4 2024 data)

    Formula:
    Predicted = Actual Revenue + (Realistic Remaining Spend × Adjusted ROAS)

    Where:
    - Realistic Remaining Spend = min(remaining_budget, projected_spend_at_current_rate)
    - Adjusted ROAS is the current ROAS, conservatively blended toward target
    """
    if current_date >= end_date:
        return actual_revenue  # Month complete, actual is final

    if actual_spend <= 0 or remaining_budget <= 0:
        # No spend yet or no budget left - return actual + (remaining × target)
        return actual_revenue + (remaining_budget * target_roas) if remaining_budget > 0 else actual_revenue

    # Calculate current ROAS
    current_roas = actual_revenue / actual_spend

    # Load Q4 2024 daily percentages to understand remaining days' potential
    try:
        # Get script directory - handle both direct execution and import scenarios
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv[0] else '.'
        q4_data_path = os.path.join(script_dir, 'q4-2024-revenue-distribution.json')

        with open(q4_data_path, 'r') as f:
            q4_2024_data = json.load(f)

        daily_percentages = q4_2024_data.get('daily_percentages', {})

        # Calculate what % of month's revenue potential has passed vs remains
        elapsed_weight = 0
        remaining_weight = 0

        current_day = start_date
        while current_day <= end_date:
            day_key = current_day.strftime('%Y-%m-%d').replace('2025', '2024')  # Map 2025 to 2024 data
            day_pct = daily_percentages.get(day_key, 3.33)  # Default ~3.33% if no data (1/30 days)

            if current_day < current_date:
                elapsed_weight += day_pct
            else:
                remaining_weight += day_pct

            current_day += timedelta(days=1)

        # Are peak days (Black Friday week) ahead or behind?
        # If remaining_weight > elapsed_weight proportionally, peak days are ahead
        days_elapsed = (current_date - start_date).days
        days_remaining = (end_date - current_date).days + 1

        if days_elapsed > 0 and days_remaining > 0:
            # Expected weight ratio if days were equal
            expected_remaining_ratio = days_remaining / (days_elapsed + days_remaining)
            actual_remaining_ratio = remaining_weight / (elapsed_weight + remaining_weight) if (elapsed_weight + remaining_weight) > 0 else 0.5

            # Peak factor: >1 if peak days ahead, <1 if peak days behind
            peak_factor = actual_remaining_ratio / expected_remaining_ratio if expected_remaining_ratio > 0 else 1.0
        else:
            peak_factor = 1.0

    except Exception as e:
        print(f"Warning: Could not load Q4 2024 data for prediction: {e}")
        peak_factor = 1.0

    # Calculate adjusted ROAS for remaining budget
    # Be conservative: blend current ROAS toward target, don't assume current performance continues perfectly
    #
    # Logic:
    # - If current ROAS > target: Don't assume we'll maintain outperformance
    #   Use weighted average: 60% current + 40% target (regress toward mean)
    # - If current ROAS < target: Be realistic, don't assume we'll catch up
    #   Use weighted average: 70% current + 30% target (slight optimism for remaining peak days)
    # - Apply peak factor to account for Black Friday week potential

    if current_roas > target_roas:
        # Outperforming - be conservative, expect some regression
        # Cap the outperformance at 20% above target for predictions
        capped_current_roas = min(current_roas, target_roas * 1.20)
        adjusted_roas = (capped_current_roas * 0.6) + (target_roas * 0.4)
    else:
        # Underperforming - slight optimism if peak days ahead, but mostly realistic
        base_blend = (current_roas * 0.7) + (target_roas * 0.3)
        # If peak days ahead (peak_factor > 1), allow modest uplift (max 10%)
        peak_uplift = min(peak_factor, 1.10) if peak_factor > 1 else 1.0
        adjusted_roas = base_blend * peak_uplift

    # Calculate predicted remaining revenue using full remaining budget
    predicted_remaining = remaining_budget * adjusted_roas

    # Final prediction
    predicted_revenue = actual_revenue + predicted_remaining

    return predicted_revenue


def update_dashboard():
    """Update Google Sheet with latest performance data using BATCH UPDATES to avoid quota limits"""

    print(f"Starting Smythson Q4 Dashboard update - {datetime.now()}")

    # Initialize Google Sheets
    gc = gspread.service_account(
        filename=os.path.expanduser("~/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json")
    )
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

    # Calculate date ranges
    today = datetime.now()
    days_elapsed = (today - Q4_START).days
    days_remaining = (Q4_END - today).days
    weeks_elapsed = days_elapsed / 7

    # Fetch data for each region - Q4 total
    regional_data = {}
    total_spend = 0
    total_revenue = 0

    for region, account_id in ACCOUNTS.items():
        data = get_google_ads_data(account_id, Q4_START, today)
        regional_data[region] = data
        total_spend += data["spend"]
        total_revenue += data["revenue"]

    # Fetch November data
    november_data = {}
    for region, account_id in ACCOUNTS.items():
        nov_data = get_google_ads_data(account_id, NOVEMBER_START, min(today, NOVEMBER_END))
        november_data[region] = nov_data

    # Fetch December data (if in December)
    december_data = {}
    if today >= DECEMBER_START:
        for region, account_id in ACCOUNTS.items():
            dec_data = get_google_ads_data(account_id, DECEMBER_START, today)
            december_data[region] = dec_data

    # Calculate overall metrics
    overall_roas = total_revenue / total_spend if total_spend > 0 else 0
    budget_pacing = (total_spend / TOTAL_BUDGET) * 100
    revenue_progress = (total_revenue / TOTAL_REVENUE_TARGET) * 100

    # Calculate expected budget pacing at this point in Q4
    # Use weighted pacing (same as revenue) because spend should follow revenue patterns
    # Black Friday week gets more spend, learning periods get less, etc.
    expected_budget_pacing = calculate_weighted_pacing(Q4_START, Q4_END, today) * 100

    # BATCH UPDATE: Collect all updates into a single list
    # This reduces API calls from 80+ to 1, avoiding quota limits
    batch_updates = []

    # Update "Current Status at a Glance" section (rows 41-46)
    batch_updates.append({
        'range': 'C41',
        'values': [[f"£{total_revenue:,.0f}"]]  # Total Revenue
    })
    batch_updates.append({
        'range': 'C42',
        'values': [[f"£{total_spend:,.0f}"]]  # Total Spend
    })
    batch_updates.append({
        'range': 'C43',
        'values': [[f"{overall_roas:.2f}"]]  # Overall ROAS
    })
    batch_updates.append({
        'range': 'C44',
        'values': [[f"{budget_pacing:.1f}%"]]  # Budget Pacing (Actual)
    })
    batch_updates.append({
        'range': 'B44',
        'values': [[f"{expected_budget_pacing:.1f}%"]]  # Budget Pacing (Expected Target)
    })

    # Update status indicators
    revenue_status = calculate_status(revenue_progress, weeks_elapsed * 11.1)  # ~11.1% per week
    spend_status = calculate_status(budget_pacing, weeks_elapsed * 11.1)
    roas_status = calculate_status(overall_roas, 2.13)

    batch_updates.append({
        'range': 'D41',
        'values': [[revenue_status]]
    })
    batch_updates.append({
        'range': 'D42',
        'values': [[spend_status if spend_status == "🟢" else "🟡" if budget_pacing < 100 else "🔴"]]
    })
    batch_updates.append({
        'range': 'D43',
        'values': [[roas_status]]
    })

    # Update November Regional Overview (rows 19-22)
    # Determine current phase for November (could be PHASE_1, 2, or 3)
    november_phase = get_current_phase(min(today, NOVEMBER_END))

    # Calculate November pacing with weighted factors (peak periods, phase changes)
    november_pacing = calculate_weighted_pacing(NOVEMBER_START, NOVEMBER_END, today)

    # Calculate November expected spend by region (budget weighted by pacing)
    november_days_in_month = (NOVEMBER_END - NOVEMBER_START).days

    for i, region in enumerate(["UK", "USA", "EUR", "ROW"]):
        row = 19 + i
        data = november_data.get(region, {"roas": 0, "revenue": 0, "spend": 0})
        actual_roas = data["roas"]

        # Use the current phase's target ROAS for November
        target_roas = TARGET_ROAS[november_phase][region]
        roas_status = calculate_status(actual_roas, target_roas) if actual_roas > 0 else "🔴"

        # Calculate expected revenue based on weighted pacing
        monthly_revenue_target = NOVEMBER_REVENUE_TARGETS[region]
        expected_revenue = monthly_revenue_target * november_pacing
        actual_revenue = data["revenue"]

        # Calculate expected spend based on weighted pacing
        # November uses weighted average budget accounting for phase transitions
        if region == "USA":
            # USA budget increases Nov 25 (PHASE_3)
            days_phase_2 = (PHASE_3_START - NOVEMBER_START).days  # Nov 3-24: 22 days
            days_phase_3 = (NOVEMBER_END - PHASE_3_START).days + 1  # Nov 25-30: 6 days
            november_monthly_budget = (BUDGETS["PHASE_2"]["USA"] * days_phase_2 + BUDGETS["PHASE_3"]["USA"] * days_phase_3)
        else:
            # Other regions maintain same budget throughout November
            november_monthly_budget = BUDGETS["PHASE_2"][region] * november_days_in_month

        expected_spend = november_monthly_budget * november_pacing

        # Revenue traffic lighting (more lenient: 85% threshold for green, 70% for amber)
        if actual_revenue >= expected_revenue * 0.85:
            revenue_status = "🟢"
        elif actual_revenue >= expected_revenue * 0.70:
            revenue_status = "🟡"
        else:
            revenue_status = "🔴"

        # Spend traffic lighting (tighter range: 85-115% for green)
        actual_spend = data["spend"]
        if expected_spend > 0:
            spend_pacing_pct = (actual_spend / expected_spend) * 100
            if 85 <= spend_pacing_pct <= 115:
                spend_status = "🟢"  # On track
            elif (70 <= spend_pacing_pct < 85) or (115 < spend_pacing_pct <= 130):
                spend_status = "🟡"  # Moderate variance
            else:
                spend_status = "🔴"  # Significant variance (under or overspending)
        else:
            spend_status = "⚪"  # No expected spend yet

        # All Smythson reporting in GBP (£) - no currency conversions
        revenue_str = f"£{actual_revenue:,.0f}" if actual_revenue > 0 else "£0"
        expected_revenue_str = f"£{expected_revenue:,.0f}" if expected_revenue > 0 else "£0"
        spend_str = f"£{actual_spend:,.0f}" if actual_spend > 0 else "£0"
        expected_spend_str = f"£{expected_spend:,.0f}" if expected_spend > 0 else "£0"
        target_revenue_str = f"£{monthly_revenue_target:,.0f}"

        # Calculate predicted revenue using budget-constrained method
        # Uses: remaining budget, current ROAS trending, historical peak day weighting
        remaining_budget = november_monthly_budget - actual_spend
        # Use blended target ROAS for the region (from NOVEMBER_REVENUE_TARGETS / budget allocation)
        region_target_roas = monthly_revenue_target / november_monthly_budget if november_monthly_budget > 0 else 5.0
        predicted_revenue = calculate_predicted_revenue(
            actual_revenue=actual_revenue,
            actual_spend=actual_spend,
            remaining_budget=remaining_budget,
            target_roas=region_target_roas,
            start_date=NOVEMBER_START,
            end_date=NOVEMBER_END,
            current_date=today
        )
        predicted_revenue_str = f"£{predicted_revenue:,.0f}" if predicted_revenue > 0 else "£0"

        # Add to batch updates instead of individual sheet.update() calls
        batch_updates.append({'range': f"D{row}", 'values': [[f"{actual_roas:.2f}" if actual_roas > 0 else "—"]]})
        batch_updates.append({'range': f"E{row}", 'values': [[roas_status]]})
        batch_updates.append({'range': f"F{row}", 'values': [[revenue_str]]})
        batch_updates.append({'range': f"G{row}", 'values': [[expected_revenue_str]]})
        batch_updates.append({'range': f"H{row}", 'values': [[revenue_status]]})
        batch_updates.append({'range': f"I{row}", 'values': [[spend_str]]})  # Actual Spend
        batch_updates.append({'range': f"J{row}", 'values': [[expected_spend_str]]})  # Expected Spend
        batch_updates.append({'range': f"K{row}", 'values': [[spend_status]]})  # Spend Status
        batch_updates.append({'range': f"L{row}", 'values': [[target_revenue_str]]})  # Target Revenue
        batch_updates.append({'range': f"M{row}", 'values': [[predicted_revenue_str]]})  # Predicted Revenue

    # Update November TOTALS row (row 23)
    november_total_revenue = sum(november_data[r]["revenue"] for r in ["UK", "USA", "EUR", "ROW"])
    november_total_spend = sum(november_data[r]["spend"] for r in ["UK", "USA", "EUR", "ROW"])
    november_total_roas = november_total_revenue / november_total_spend if november_total_spend > 0 else 0

    # Calculate expected totals
    november_expected_revenue = sum(NOVEMBER_REVENUE_TARGETS[r] * november_pacing for r in ["UK", "USA", "EUR", "ROW"])
    november_expected_spend = sum([
        (BUDGETS["PHASE_2"]["UK"] * november_days_in_month) * november_pacing,
        ((BUDGETS["PHASE_2"]["USA"] * 22 + BUDGETS["PHASE_3"]["USA"] * 6)) * november_pacing,  # USA weighted
        (BUDGETS["PHASE_2"]["EUR"] * november_days_in_month) * november_pacing,
        (BUDGETS["PHASE_2"]["ROW"] * november_days_in_month) * november_pacing
    ])

    # Calculate blended target ROAS for November (weighted by spend allocation)
    # UK 44%, USA 36%, EUR 14%, ROW 6% based on budget allocation
    november_target_roas = (0.44 * 6.0) + (0.36 * 4.5) + (0.14 * 4.0) + (0.06 * 5.0)  # ~5.12 blended

    # Traffic lights for totals
    # ROAS Status: Compare to blended target
    if november_total_roas >= november_target_roas * 0.85:
        november_roas_status = "🟢"
    elif november_total_roas >= november_target_roas * 0.70:
        november_roas_status = "🟡"
    else:
        november_roas_status = "🔴"

    # Revenue Status
    revenue_pct = (november_total_revenue / november_expected_revenue * 100) if november_expected_revenue > 0 else 0
    if revenue_pct >= 85:
        november_revenue_status = "🟢"
    elif revenue_pct >= 70:
        november_revenue_status = "🟡"
    else:
        november_revenue_status = "🔴"

    # Spend Status
    spend_pct = (november_total_spend / november_expected_spend * 100) if november_expected_spend > 0 else 0
    if 85 <= spend_pct <= 115:
        november_spend_status = "🟢"
    elif (70 <= spend_pct < 85) or (115 < spend_pct <= 130):
        november_spend_status = "🟡"
    else:
        november_spend_status = "🔴"

    # Calculate November predicted revenue total using budget-constrained method
    # Total remaining budget for November
    november_total_budget = sum([
        BUDGETS["PHASE_2"]["UK"] * november_days_in_month,
        (BUDGETS["PHASE_2"]["USA"] * 22 + BUDGETS["PHASE_3"]["USA"] * 6),  # USA weighted
        BUDGETS["PHASE_2"]["EUR"] * november_days_in_month,
        BUDGETS["PHASE_2"]["ROW"] * november_days_in_month
    ])
    november_remaining_budget = november_total_budget - november_total_spend
    november_total_target = sum(NOVEMBER_REVENUE_TARGETS.values())
    november_blended_target_roas = november_total_target / november_total_budget if november_total_budget > 0 else 5.0

    november_predicted_revenue = calculate_predicted_revenue(
        actual_revenue=november_total_revenue,
        actual_spend=november_total_spend,
        remaining_budget=november_remaining_budget,
        target_roas=november_blended_target_roas,
        start_date=NOVEMBER_START,
        end_date=NOVEMBER_END,
        current_date=today
    )

    # Update November totals row
    batch_updates.append({'range': 'D23', 'values': [[f"{november_total_roas:.2f}" if november_total_roas > 0 else "—"]]})
    batch_updates.append({'range': 'E23', 'values': [[november_roas_status]]})
    batch_updates.append({'range': 'F23', 'values': [[f"£{november_total_revenue:,.0f}"]]})
    batch_updates.append({'range': 'G23', 'values': [[f"£{november_expected_revenue:,.0f}"]]})
    batch_updates.append({'range': 'H23', 'values': [[november_revenue_status]]})
    batch_updates.append({'range': 'I23', 'values': [[f"£{november_total_spend:,.0f}"]]})
    batch_updates.append({'range': 'J23', 'values': [[f"£{november_expected_spend:,.0f}"]]})
    batch_updates.append({'range': 'K23', 'values': [[november_spend_status]]})
    batch_updates.append({'range': 'M23', 'values': [[f"£{november_predicted_revenue:,.0f}"]]})  # Predicted Revenue Total

    # Add November header for Predicted Revenue column
    batch_updates.append({'range': 'M18', 'values': [['Predicted Revenue']]})

    # Update December Regional Overview (rows 31-34)
    # December is always PHASE_4

    # Calculate December pacing with weighted factors (peak periods, phase changes)
    december_pacing = calculate_weighted_pacing(DECEMBER_START, DECEMBER_END, today)

    # Calculate December expected spend by region (budget weighted by pacing)
    december_days_in_month = (DECEMBER_END - DECEMBER_START).days

    for i, region in enumerate(["UK", "USA", "EUR", "ROW"]):
        row = 31 + i

        if today < DECEMBER_START:
            # December hasn't started yet - show targets with white status
            monthly_revenue_target = DECEMBER_REVENUE_TARGETS[region]
            target_revenue_str = f"£{monthly_revenue_target:,.0f}"

            batch_updates.append({'range': f"D{row}", 'values': [["—"]]})
            batch_updates.append({'range': f"E{row}", 'values': [["⚪"]]})
            batch_updates.append({'range': f"F{row}", 'values': [["£0"]]})
            batch_updates.append({'range': f"G{row}", 'values': [["£0"]]})
            batch_updates.append({'range': f"H{row}", 'values': [["⚪"]]})
            batch_updates.append({'range': f"I{row}", 'values': [["£0"]]})  # Actual Spend
            batch_updates.append({'range': f"J{row}", 'values': [["£0"]]})  # Expected Spend
            batch_updates.append({'range': f"K{row}", 'values': [["⚪"]]})  # Spend Status
            batch_updates.append({'range': f"L{row}", 'values': [[target_revenue_str]]})  # Target Revenue
            batch_updates.append({'range': f"M{row}", 'values': [["£0"]]})  # Predicted Revenue (not started)
        else:
            data = december_data.get(region, {"roas": 0, "revenue": 0, "spend": 0})
            actual_roas = data["roas"]

            # December uses PHASE_4 targets
            target_roas = TARGET_ROAS["PHASE_4"][region]
            roas_status = calculate_status(actual_roas, target_roas) if actual_roas > 0 else "🔴"

            # Calculate expected revenue based on weighted pacing
            monthly_revenue_target = DECEMBER_REVENUE_TARGETS[region]
            expected_revenue = monthly_revenue_target * december_pacing
            actual_revenue = data["revenue"]

            # Calculate expected spend based on weighted pacing
            # CRITICAL: December spend limited by Christmas delivery cutoff (Dec 22)
            # Use EFFECTIVE_DECEMBER_SPEND_DAYS (21 days) not full month (31 days)
            # Revenue pacing uses full month (orders placed earlier still convert)
            december_monthly_budget = BUDGETS["PHASE_4"][region] * EFFECTIVE_DECEMBER_SPEND_DAYS
            expected_spend = december_monthly_budget * december_pacing

            # Revenue traffic lighting (more lenient: 85% threshold for green, 70% for amber)
            if actual_revenue >= expected_revenue * 0.85:
                revenue_status = "🟢"
            elif actual_revenue >= expected_revenue * 0.70:
                revenue_status = "🟡"
            else:
                revenue_status = "🔴"

            # Spend traffic lighting (tighter range: 85-115% for green)
            actual_spend = data["spend"]
            if expected_spend > 0:
                spend_pacing_pct = (actual_spend / expected_spend) * 100
                if 85 <= spend_pacing_pct <= 115:
                    spend_status = "🟢"  # On track
                elif (70 <= spend_pacing_pct < 85) or (115 < spend_pacing_pct <= 130):
                    spend_status = "🟡"  # Moderate variance
                else:
                    spend_status = "🔴"  # Significant variance (under or overspending)
            else:
                spend_status = "⚪"  # No expected spend yet

            # All Smythson reporting in GBP (£) - no currency conversions
            revenue_str = f"£{actual_revenue:,.0f}" if actual_revenue > 0 else "£0"
            expected_revenue_str = f"£{expected_revenue:,.0f}" if expected_revenue > 0 else "£0"
            spend_str = f"£{actual_spend:,.0f}" if actual_spend > 0 else "£0"
            expected_spend_str = f"£{expected_spend:,.0f}" if expected_spend > 0 else "£0"
            target_revenue_str = f"£{monthly_revenue_target:,.0f}"

            # Calculate predicted revenue using budget-constrained method
            # Uses: remaining budget, current ROAS trending, historical peak day weighting
            remaining_budget = december_monthly_budget - actual_spend
            # Use blended target ROAS for the region (from DECEMBER_REVENUE_TARGETS / budget allocation)
            region_target_roas = monthly_revenue_target / december_monthly_budget if december_monthly_budget > 0 else 5.0
            predicted_revenue = calculate_predicted_revenue(
                actual_revenue=actual_revenue,
                actual_spend=actual_spend,
                remaining_budget=remaining_budget,
                target_roas=region_target_roas,
                start_date=DECEMBER_START,
                end_date=DECEMBER_END,
                current_date=today
            )
            predicted_revenue_str = f"£{predicted_revenue:,.0f}" if predicted_revenue > 0 else "£0"

            # Add to batch updates
            batch_updates.append({'range': f"D{row}", 'values': [[f"{actual_roas:.2f}" if actual_roas > 0 else "—"]]})
            batch_updates.append({'range': f"E{row}", 'values': [[roas_status]]})
            batch_updates.append({'range': f"F{row}", 'values': [[revenue_str]]})
            batch_updates.append({'range': f"G{row}", 'values': [[expected_revenue_str]]})
            batch_updates.append({'range': f"H{row}", 'values': [[revenue_status]]})
            batch_updates.append({'range': f"I{row}", 'values': [[spend_str]]})  # Actual Spend
            batch_updates.append({'range': f"J{row}", 'values': [[expected_spend_str]]})  # Expected Spend
            batch_updates.append({'range': f"K{row}", 'values': [[spend_status]]})  # Spend Status
            batch_updates.append({'range': f"L{row}", 'values': [[target_revenue_str]]})  # Target Revenue
            batch_updates.append({'range': f"M{row}", 'values': [[predicted_revenue_str]]})  # Predicted Revenue

    # Update December TOTALS row (row 35)
    if today < DECEMBER_START:
        # December hasn't started - show white status
        batch_updates.append({'range': 'D35', 'values': [["—"]]})
        batch_updates.append({'range': 'E35', 'values': [["⚪"]]})
        batch_updates.append({'range': 'F35', 'values': [["£0"]]})
        batch_updates.append({'range': 'G35', 'values': [["£0"]]})
        batch_updates.append({'range': 'H35', 'values': [["⚪"]]})
        batch_updates.append({'range': 'I35', 'values': [["£0"]]})
        batch_updates.append({'range': 'J35', 'values': [["£0"]]})
        batch_updates.append({'range': 'K35', 'values': [["⚪"]]})
        batch_updates.append({'range': 'M35', 'values': [["£0"]]})  # Predicted Revenue (not started)
    else:
        # December has started - calculate totals
        december_total_revenue = sum(december_data[r]["revenue"] for r in ["UK", "USA", "EUR", "ROW"])
        december_total_spend = sum(december_data[r]["spend"] for r in ["UK", "USA", "EUR", "ROW"])
        december_total_roas = december_total_revenue / december_total_spend if december_total_spend > 0 else 0

        # Calculate expected totals
        # Revenue uses full month (orders placed earlier still convert)
        december_expected_revenue = sum(DECEMBER_REVENUE_TARGETS[r] * december_pacing for r in ["UK", "USA", "EUR", "ROW"])

        # Spend uses EFFECTIVE_DECEMBER_SPEND_DAYS (21 days) due to Christmas delivery cutoff
        december_expected_spend = sum([
            (BUDGETS["PHASE_4"]["UK"] * EFFECTIVE_DECEMBER_SPEND_DAYS) * december_pacing,
            (BUDGETS["PHASE_4"]["USA"] * EFFECTIVE_DECEMBER_SPEND_DAYS) * december_pacing,
            (BUDGETS["PHASE_4"]["EUR"] * EFFECTIVE_DECEMBER_SPEND_DAYS) * december_pacing,
            (BUDGETS["PHASE_4"]["ROW"] * EFFECTIVE_DECEMBER_SPEND_DAYS) * december_pacing
        ])

        # Calculate blended target ROAS for December (same allocations as November)
        december_target_roas = (0.44 * 6.0) + (0.36 * 4.5) + (0.14 * 4.0) + (0.06 * 5.0)  # ~5.12 blended

        # Traffic lights for totals
        # ROAS Status
        if december_total_roas >= december_target_roas * 0.85:
            december_roas_status = "🟢"
        elif december_total_roas >= december_target_roas * 0.70:
            december_roas_status = "🟡"
        else:
            december_roas_status = "🔴"

        # Revenue Status
        dec_revenue_pct = (december_total_revenue / december_expected_revenue * 100) if december_expected_revenue > 0 else 0
        if dec_revenue_pct >= 85:
            december_revenue_status = "🟢"
        elif dec_revenue_pct >= 70:
            december_revenue_status = "🟡"
        else:
            december_revenue_status = "🔴"

        # Spend Status
        dec_spend_pct = (december_total_spend / december_expected_spend * 100) if december_expected_spend > 0 else 0
        if 85 <= dec_spend_pct <= 115:
            december_spend_status = "🟢"
        elif (70 <= dec_spend_pct < 85) or (115 < dec_spend_pct <= 130):
            december_spend_status = "🟡"
        else:
            december_spend_status = "🔴"

        # Calculate December predicted revenue total using budget-constrained method
        # Total remaining budget for December (using effective 21-day spend period)
        december_total_budget = sum([
            BUDGETS["PHASE_4"]["UK"] * EFFECTIVE_DECEMBER_SPEND_DAYS,
            BUDGETS["PHASE_4"]["USA"] * EFFECTIVE_DECEMBER_SPEND_DAYS,
            BUDGETS["PHASE_4"]["EUR"] * EFFECTIVE_DECEMBER_SPEND_DAYS,
            BUDGETS["PHASE_4"]["ROW"] * EFFECTIVE_DECEMBER_SPEND_DAYS
        ])
        december_remaining_budget = december_total_budget - december_total_spend
        december_total_target = sum(DECEMBER_REVENUE_TARGETS.values())
        december_blended_target_roas = december_total_target / december_total_budget if december_total_budget > 0 else 5.0

        december_predicted_revenue = calculate_predicted_revenue(
            actual_revenue=december_total_revenue,
            actual_spend=december_total_spend,
            remaining_budget=december_remaining_budget,
            target_roas=december_blended_target_roas,
            start_date=DECEMBER_START,
            end_date=DECEMBER_END,
            current_date=today
        )

        # Update December totals row
        batch_updates.append({'range': 'D35', 'values': [[f"{december_total_roas:.2f}" if december_total_roas > 0 else "—"]]})
        batch_updates.append({'range': 'E35', 'values': [[december_roas_status]]})
        batch_updates.append({'range': 'F35', 'values': [[f"£{december_total_revenue:,.0f}"]]})
        batch_updates.append({'range': 'G35', 'values': [[f"£{december_expected_revenue:,.0f}"]]})
        batch_updates.append({'range': 'H35', 'values': [[december_revenue_status]]})
        batch_updates.append({'range': 'I35', 'values': [[f"£{december_total_spend:,.0f}"]]})
        batch_updates.append({'range': 'J35', 'values': [[f"£{december_expected_spend:,.0f}"]]})
        batch_updates.append({'range': 'K35', 'values': [[december_spend_status]]})
        batch_updates.append({'range': 'M35', 'values': [[f"£{december_predicted_revenue:,.0f}"]]})  # Predicted Revenue Total

    # Add December header for Predicted Revenue column
    batch_updates.append({'range': 'M30', 'values': [['Predicted Revenue']]})

    # Update Initiative Status based on current phase
    current_phase = get_current_phase(today)

    # Define initiative rows and their phase requirements
    initiatives = [
        # Phase 1 (rows 53-55) - Always complete
        (53, "1", "PHASE_1"),  # UK Launch
        (54, "1", "PHASE_1"),  # EUR Launch
        (55, "1", "PHASE_1"),  # USA Launch
        # Phase 2 (rows 56-58)
        (56, "2", "PHASE_2"),  # UK ROAS Reduction
        (57, "2", "PHASE_2"),  # ROW Launch
        (58, "2", "PHASE_2"),  # Mid-Quarter Review
        # Phase 3 (rows 59-60)
        (59, "3", "PHASE_3"),  # USA Budget Increase
        (60, "3", "PHASE_3"),  # USA ROAS Reduction
        # Phase 4 (rows 61-66)
        (61, "4", "PHASE_4"),  # UK ROAS Reduction
        (62, "4", "PHASE_4"),  # USA ROAS Reduction
        (63, "4", "PHASE_4"),  # EUR ROAS Reduction
        (64, "4", "PHASE_4"),  # ROW ROAS Reduction
        (65, "4", "PHASE_4"),  # EUR Budget Adjustment
        (66, "4", "PHASE_4"),  # ROW Budget Adjustment
    ]

    # Phase priority (for determining if initiative should be complete)
    phase_order = ["PHASE_1", "PHASE_2", "PHASE_3", "PHASE_4"]
    current_phase_index = phase_order.index(current_phase)

    for row, phase_num, required_phase in initiatives:
        required_phase_index = phase_order.index(required_phase)

        if required_phase_index <= current_phase_index:
            # This phase has started or completed
            batch_updates.append({'range': f"D{row}", 'values': [["🟢 Complete"]]})
        else:
            # This phase is still scheduled
            batch_updates.append({'range': f"D{row}", 'values': [["📋 Scheduled"]]})

    # Update "Last Updated" timestamp
    batch_updates.append({'range': 'B12', 'values': [[today.strftime("%Y-%m-%d %H:%M")]]})

    # Update Column B reference/target cells with corrected Q4 figures
    # These are the static reference values that actual performance is compared against

    # B11: Target ROAS (blended Q4 target)
    target_roas_blended = TOTAL_REVENUE_TARGET / TOTAL_BUDGET  # 2,380,000 / 521,052 = 4.57
    batch_updates.append({'range': 'B11', 'values': [[f"{target_roas_blended:.2f}"]]})

    # B23: November Budget (P8 total with no carryforward)
    november_total_budget = 186051
    batch_updates.append({'range': 'B23', 'values': [[f"£{november_total_budget:,}"]]})

    # B35: December Budget (P9 with note about 21-day effective period)
    december_total_budget = 183929
    batch_updates.append({'range': 'B35', 'values': [[f"£{december_total_budget:,} (21 days effective)"]]})

    # B41: Revenue Target (Client target)
    batch_updates.append({'range': 'B41', 'values': [[f"£{TOTAL_REVENUE_TARGET:,}"]]})

    # B42: Total Q4 Budget (corrected with no P7 carryforward)
    batch_updates.append({'range': 'B42', 'values': [[f"£{TOTAL_BUDGET:,}"]]})

    # B43: ROAS Target (same as B11)
    batch_updates.append({'range': 'B43', 'values': [[f"{target_roas_blended:.2f}"]]})

    # EXECUTE BATCH UPDATE - Single API call instead of 80+
    # This avoids Google Sheets API quota limits (60 writes/minute)
    print(f"Executing batch update with {len(batch_updates)} cell updates...")
    sheet.batch_update(batch_updates)

    print("Dashboard updated successfully")
    print(f"Current phase: {current_phase}")
    print(f"Total API calls: 1 (batch update with {len(batch_updates)} cells)")

    return {
        "total_revenue": total_revenue,
        "total_spend": total_spend,
        "overall_roas": overall_roas,
        "budget_pacing": budget_pacing,
        "revenue_progress": revenue_progress,
        "regional_data": regional_data,
        "november_data": november_data,
        "december_data": december_data
    }

def save_to_json(data):
    """Save dashboard data to JSON for weekly summary integration

    NOTE: Email notifications disabled - data is now included in weekly summary email
    """
    import json

    # Save to shared/data for weekly summary to pick up
    output_file = Path(__file__).parent.parent.parent / "data/cache/smythson-q4-dashboard.json"

    # Calculate current phase
    current_phase = get_current_phase(datetime.now())

    # Prepare data structure
    dashboard_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "q4_period": {
            "start": Q4_START.strftime("%Y-%m-%d"),
            "end": Q4_END.strftime("%Y-%m-%d"),
            "current_phase": current_phase,
            "days_elapsed": (datetime.now() - Q4_START).days,
            "days_remaining": (Q4_END - datetime.now()).days
        },
        "overall": {
            "revenue": round(data["total_revenue"], 2),
            "revenue_target": TOTAL_REVENUE_TARGET,
            "revenue_progress_pct": round(data["revenue_progress"], 1),
            "spend": round(data["total_spend"], 2),
            "budget": TOTAL_BUDGET,
            "budget_pacing_pct": round(data["budget_pacing"], 1),
            "roas": round(data["overall_roas"], 2),
            "roas_target": 5.47  # Blended target
        },
        "regional": {}
    }

    # Add regional data
    for region in ["UK", "USA", "EUR", "ROW"]:
        regional_entry = data["regional_data"][region]
        dashboard_data["regional"][region] = {
            "revenue": round(regional_entry["revenue"], 2),
            "spend": round(regional_entry["spend"], 2),
            "roas": round(regional_entry["roas"], 2),
            "conversions": round(regional_entry["conversions"], 1)
        }

    # Save to JSON
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        print(f"Dashboard data saved to {output_file} for weekly summary integration")
    except Exception as e:
        print(f"Warning: Could not save dashboard data to JSON: {e}")

if __name__ == "__main__":
    try:
        data = update_dashboard()
        save_to_json(data)
        print("Smythson Q4 Dashboard update complete")
        print("Data saved for weekly summary email integration")
    except Exception as e:
        print(f"Error updating dashboard: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
