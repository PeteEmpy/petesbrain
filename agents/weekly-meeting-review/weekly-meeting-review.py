#!/usr/bin/env python3
"""
Weekly Meeting Review Report Generator
Generates a report of recent meetings for client assignment validation.
Also includes completed Google Tasks from the past week.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENTS_DIR = Path("/Users/administrator/Documents/PetesBrain/clients")
ROKSYS_DIR = Path("/Users/administrator/Documents/PetesBrain/roksys")
TASKS_COMPLETIONS_FILE = Path("/Users/administrator/Documents/PetesBrain/data/state/tasks-completed.json")

def authenticate():
    """Authenticate with Gmail API."""
    creds = None
    email_sync_dir = Path(__file__).parent.parent / 'email-sync'
    token_file = email_sync_dir / 'token.json'
    credentials_file = email_sync_dir / 'credentials.json'

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_file.exists():
                print(f"Error: credentials.json not found at {credentials_file}")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

def find_recent_meetings(days=7):
    """Find all meetings from the last N days."""
    meetings = []
    cutoff_date = datetime.now() - timedelta(days=days)

    # Search in clients folders
    for client_dir in CLIENTS_DIR.iterdir():
        if not client_dir.is_dir():
            continue
        if client_dir.name.startswith('_'):  # Skip _templates, _unassigned
            continue

        meeting_dir = client_dir / 'meeting-notes'
        if not meeting_dir.exists():
            continue

        for meeting_file in meeting_dir.glob('*.md'):
            # Check file modification time
            mtime = datetime.fromtimestamp(meeting_file.stat().st_mtime)
            if mtime >= cutoff_date:
                meetings.append({
                    'file': meeting_file,
                    'client': client_dir.name,
                    'location': 'clients',
                    'mtime': mtime
                })

    # Search in roksys folder
    roksys_meeting_dir = ROKSYS_DIR / 'meeting-notes'
    if roksys_meeting_dir.exists():
        for meeting_file in roksys_meeting_dir.glob('*.md'):
            mtime = datetime.fromtimestamp(meeting_file.stat().st_mtime)
            if mtime >= cutoff_date:
                meetings.append({
                    'file': meeting_file,
                    'client': 'roksys',
                    'location': 'company',
                    'mtime': mtime
                })

    # Sort by modification time, newest first
    meetings.sort(key=lambda x: x['mtime'], reverse=True)
    return meetings

def find_completed_tasks(days=7):
    """Find all tasks completed in the last N days."""
    if not TASKS_COMPLETIONS_FILE.exists():
        return []

    try:
        with open(TASKS_COMPLETIONS_FILE, 'r', encoding='utf-8') as f:
            all_completions = json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load tasks completions: {e}")
        return []

    cutoff_date = datetime.now() - timedelta(days=days)
    recent_completions = []

    for task in all_completions:
        # Use detected_at as primary timestamp (when we detected completion)
        detected_at_str = task.get('detected_at')
        if detected_at_str:
            try:
                detected_at = datetime.fromisoformat(detected_at_str.replace('Z', '+00:00'))
                # Convert to naive datetime for comparison
                if detected_at.tzinfo:
                    detected_at = detected_at.replace(tzinfo=None)

                if detected_at >= cutoff_date:
                    recent_completions.append(task)
            except Exception as e:
                print(f"Warning: Failed to parse date for task '{task.get('title')}': {e}")

    # Sort by detected_at, newest first
    recent_completions.sort(
        key=lambda x: x.get('detected_at', ''),
        reverse=True
    )

    return recent_completions

def extract_meeting_preview(filepath, lines=15):
    """Extract first N lines of meeting for preview."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content_lines = []
            in_frontmatter = False
            frontmatter_count = 0

            for line in f:
                # Skip YAML frontmatter
                if line.strip() == '---':
                    frontmatter_count += 1
                    if frontmatter_count == 2:
                        in_frontmatter = False
                    else:
                        in_frontmatter = True
                    continue

                if not in_frontmatter and line.strip():
                    content_lines.append(line.rstrip())
                    if len(content_lines) >= lines:
                        break

            return '\n'.join(content_lines)
    except Exception as e:
        return f"[Error reading file: {e}]"

def extract_participants(filepath):
    """Extract participants from YAML frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            in_frontmatter = False
            for line in f:
                if line.strip() == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        break
                    continue

                if in_frontmatter and line.startswith('participants:'):
                    # Extract participants list
                    participants = line.split(':', 1)[1].strip()
                    # Clean up formatting
                    participants = participants.strip('[]').replace("'", "").replace('"', '')
                    return participants
        return "Unknown"
    except Exception as e:
        return "Unknown"

def get_smythson_budget_status():
    """
    Get Smythson budget status from Google Sheets (MICE budget tracker).

    Returns budget status dict for current active period.
    Spreadsheet: https://docs.google.com/spreadsheets/d/1BB2V2e13PbRLhTvGqYITRhcpa5U92HLQV4_Bm9zxbVI/
    """
    try:
        from googleapiclient.discovery import build

        # Authenticate using same credentials as email
        email_sync_dir = Path(__file__).parent.parent / 'email-sync'
        token_file = email_sync_dir / 'token.json'

        if not token_file.exists():
            return None

        creds = Credentials.from_authorized_user_file(str(token_file),
            ['https://www.googleapis.com/auth/spreadsheets.readonly'])

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                return None

        service = build('sheets', 'v4', credentials=creds)
        spreadsheet_id = '1BB2V2e13PbRLhTvGqYITRhcpa5U92HLQV4_Bm9zxbVI'

        # Fetch data from Sheet1 (rows 2-13 contain period data)
        range_name = 'Sheet1!A2:N13'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])

        if not values:
            return None

        # Find the active period (has "Days Left" > 0)
        # Column indices: 0=Period, 1=Start, 2=End, 3=Budget, 4=Actual, 5=Predicted, 6=VAR,
        #                 7=Days Elapsed, 8=Days Left, 9=Budget Remaining, 10=Budget Pacing %,
        #                 11=Spend Yesterday, 12=Required Spend, 13=Extra Spend Per Day

        for row in values:
            if len(row) < 9:  # Need at least through "Days Left" column
                continue

            period = row[0] if len(row) > 0 else ''
            if not period or period.startswith('P') == False:
                continue

            try:
                days_left_str = row[8] if len(row) > 8 else ''
                if not days_left_str or days_left_str == '':
                    continue

                days_left = int(days_left_str)
                if days_left <= 0:
                    continue  # Period is over

                # This is the active period
                budget_str = row[3].replace('£', '').replace(',', '') if len(row) > 3 else '0'
                actual_str = row[4].replace('£', '').replace(',', '') if len(row) > 4 else '0'
                remaining_str = row[9].replace('£', '').replace(',', '') if len(row) > 9 else '0'
                pacing_str = row[10].replace('%', '') if len(row) > 10 else '100'
                days_elapsed_str = row[7] if len(row) > 7 else '0'
                required_spend_str = row[12].replace('£', '').replace(',', '') if len(row) > 12 else '0'

                budget = float(budget_str)
                actual_spend = float(actual_str)
                remaining_budget = float(remaining_str)
                pacing_percent = float(pacing_str)
                days_elapsed = int(days_elapsed_str)
                required_spend_per_day = float(required_spend_str) if required_spend_str else 0

                # Calculate expected spend for linear pacing
                total_days = days_elapsed + days_left
                expected_spend = (budget / total_days) * days_elapsed if total_days > 0 else budget

                deviation = actual_spend - expected_spend
                deviation_percent = (deviation / expected_spend * 100) if expected_spend > 0 else 0

                # Determine status based on pacing %
                status = "on-pace"
                if pacing_percent < 85 or pacing_percent > 115:
                    status = "critical"
                elif pacing_percent < 90 or pacing_percent > 110:
                    status = "warning"

                return {
                    'client': 'Smythson',
                    'period': period,
                    'monthly_budget': budget,
                    'expected_spend': expected_spend,
                    'actual_spend': actual_spend,
                    'remaining_budget': remaining_budget,
                    'deviation_amount': deviation,
                    'deviation_percent': deviation_percent,
                    'pacing_percent': pacing_percent,
                    'days_elapsed': days_elapsed,
                    'days_remaining': days_left,
                    'required_spend_per_day': required_spend_per_day,
                    'status': status,
                    'url': 'https://docs.google.com/spreadsheets/d/1BB2V2e13PbRLhTvGqYITRhcpa5U92HLQV4_Bm9zxbVI/'
                }

            except (ValueError, IndexError) as e:
                continue  # Skip rows with parsing errors

        return None  # No active period found

    except Exception as e:
        print(f"Warning: Failed to fetch MICE budget data: {e}")
        return None

def get_bright_minds_performance(days=7):
    """
    Get Google Ads performance for Bright Minds for the last complete week.

    Returns performance dict with week-over-week comparison and YoY data.
    Includes 4-week trend and trajectory analysis.
    """
    try:
        # Import here to avoid circular dependency
        import subprocess
        from datetime import datetime, timedelta

        ACCOUNT_ID = "1404868570"
        TARGET_ROAS = 400  # 400% = £4 back for every £1 spent

        # Get last complete week (Mon-Sun)
        today = datetime.now().date()
        days_since_sunday = (today.weekday() + 1) % 7
        if days_since_sunday == 0 and datetime.now().hour < 12:
            days_since_sunday = 7

        last_sunday = today - timedelta(days=days_since_sunday)
        current_week_start = last_sunday - timedelta(days=6)
        current_week_end = last_sunday

        # TODO: Implement actual GAQL queries via MCP
        # For now, return placeholder structure
        return {
            'client': 'Bright Minds',
            'account_id': ACCOUNT_ID,
            'target_roas': TARGET_ROAS,
            'current_week': {
                'start': current_week_start.strftime('%Y-%m-%d'),
                'end': current_week_end.strftime('%Y-%m-%d'),
                'conversion_value': 0,  # Placeholder
                'cost': 0,  # Placeholder
                'roas': 0,  # Placeholder
                'conversions': 0  # Placeholder
            },
            'status': 'placeholder',  # Will be 'on-track', 'needs-attention', 'excellent'
            'note': 'Google Ads data integration pending - requires MCP query implementation'
        }

    except Exception as e:
        print(f"   ⚠️  Warning: Could not fetch Bright Minds performance: {e}")
        return None


def get_devonshire_budget_status():
    """
    Get current budget status for Devonshire Hotels from automated budget tracker.

    Reads data from the "Dev Properties Auto" sheet which is updated daily.
    Returns budget status dict or None if data unavailable.
    """
    try:
        # Authenticate using same credentials as email
        email_sync_dir = Path(__file__).parent.parent / 'email-sync'
        token_file = email_sync_dir / 'token.json'

        if not token_file.exists():
            return None

        creds = Credentials.from_authorized_user_file(str(token_file),
            ['https://www.googleapis.com/auth/spreadsheets.readonly'])

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                return None

        service = build('sheets', 'v4', credentials=creds)
        spreadsheet_id = '1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc'

        # Fetch data from Dev Properties Auto sheet (row 6 contains current month)
        range_name = 'Dev Properties Auto!A6:M6'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])
        if not values or len(values[0]) < 13:
            return None

        row = values[0]
        # Columns: A=Start Date, B=End Date, C=Budget, D=Total Days, E=Days Elapsed,
        #          F=Days Remaining, G=Spend, H=Expected Spend, I=Remaining Budget,
        #          J=Req Daily Budget, K=Pacing %, L=Predicted Spend, M=Yesterday Spend

        budget_str = row[2].replace('£', '').replace(',', '') if len(row) > 2 else '0'
        actual_str = row[6].replace('£', '').replace(',', '') if len(row) > 6 else '0'
        expected_str = row[7].replace('£', '').replace(',', '') if len(row) > 7 else '0'
        remaining_str = row[8].replace('£', '').replace(',', '') if len(row) > 8 else '0'
        pacing_str = row[10] if len(row) > 10 else '100'
        days_elapsed_str = row[4] if len(row) > 4 else '0'
        days_remaining_str = row[5] if len(row) > 5 else '0'

        budget = float(budget_str)
        actual_spend = float(actual_str)
        expected_spend = float(expected_str)
        remaining_budget = float(remaining_str)
        pacing_percent = float(pacing_str)
        days_elapsed = int(days_elapsed_str)
        days_remaining = int(days_remaining_str)

        deviation = actual_spend - expected_spend
        deviation_percent = (deviation / expected_spend * 100) if expected_spend > 0 else 0

        # Determine status based on pacing %
        status = "on-pace"
        if pacing_percent < 85 or pacing_percent > 115:
            status = "critical"
        elif pacing_percent < 90 or pacing_percent > 110:
            status = "warning"

        return {
            'client': 'Devonshire Hotels',
            'monthly_budget': budget,
            'expected_spend': expected_spend,
            'actual_spend': actual_spend,
            'remaining_budget': remaining_budget,
            'deviation_amount': deviation,
            'deviation_percent': deviation_percent,
            'pacing_percent': pacing_percent,
            'days_elapsed': days_elapsed,
            'days_remaining': days_remaining,
            'status': status,
            'url': 'https://docs.google.com/spreadsheets/d/1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc/'
        }

    except Exception as e:
        print(f"   ⚠️  Warning: Could not fetch Devonshire budget status: {e}")
        return None


def get_uno_budget_status():
    """
    Get UNO Lighting budget increase implementation status.

    Tracks £1,800/day budget increase (Nov 13 - Dec 6, 2025).
    Queries Google Ads API for actual performance.

    Returns budget status dict or None if data unavailable.
    """
    try:
        from datetime import datetime, timedelta
        import subprocess
        import json

        ACCOUNT_ID = "6413338364"
        TARGET_DAILY_BUDGET = 1800
        TARGET_ROAS = 300  # 300%
        START_DATE = "2025-11-13"
        END_DATE = "2025-12-06"

        # Calculate days elapsed and remaining
        today = datetime.now().date()
        start = datetime.strptime(START_DATE, "%Y-%m-%d").date()
        end = datetime.strptime(END_DATE, "%Y-%m-%d").date()

        # Only track if we're within the period
        if today < start:
            return None  # Not started yet

        days_elapsed = (today - start).days + 1
        days_remaining = max(0, (end - today).days)
        total_days = (end - start).days + 1

        # Query Google Ads for performance since start date
        # Get last 7 days for weekly tracking
        seven_days_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        today_str = today.strftime("%Y-%m-%d")

        query = f"""
        SELECT
            segments.date,
            metrics.cost_micros,
            metrics.conversions_value_micros,
            metrics.conversions
        FROM campaign
        WHERE segments.date BETWEEN '{seven_days_ago}' AND '{today_str}'
            AND campaign.status = 'ENABLED'
        ORDER BY segments.date DESC
        """

        # Execute GAQL query (placeholder - would use MCP in production)
        # For now, return structure with placeholder data
        # TODO: Implement MCP query when available

        # Calculate expected metrics
        expected_total_spend = TARGET_DAILY_BUDGET * days_elapsed
        expected_daily_avg = TARGET_DAILY_BUDGET

        # Placeholder actual metrics (would come from API)
        actual_total_spend = 0  # To be filled by API
        actual_daily_avg = 0  # To be filled by API
        actual_roas = 0  # To be filled by API

        # Calculate deviation
        deviation = actual_total_spend - expected_total_spend
        deviation_percent = (deviation / expected_total_spend * 100) if expected_total_spend > 0 else 0

        # Determine status
        status = "placeholder"  # Will be 'on-track', 'warning', or 'critical'

        return {
            'client': 'UNO Lighting',
            'campaign_name': 'Budget Increase Implementation',
            'period': f'{START_DATE} to {END_DATE}',
            'target_daily_budget': TARGET_DAILY_BUDGET,
            'target_total_budget': TARGET_DAILY_BUDGET * total_days,
            'target_roas': TARGET_ROAS,
            'expected_total_spend': expected_total_spend,
            'actual_total_spend': actual_total_spend,
            'actual_daily_avg': actual_daily_avg,
            'actual_roas': actual_roas,
            'deviation': deviation,
            'deviation_percent': deviation_percent,
            'days_elapsed': days_elapsed,
            'days_remaining': days_remaining,
            'total_days': total_days,
            'status': status,
            'note': 'Google Ads API integration pending - requires MCP query implementation'
        }

    except Exception as e:
        print(f"   ⚠️  Warning: Could not fetch UNO Lighting budget status: {e}")
        return None


def get_budget_status():
    """
    Get budget status for clients with active budget monitoring.

    Returns list of budget status dicts for each monitored client.
    Currently monitors: Devonshire Hotels, Smythson, UNO Lighting
    """
    budget_statuses = []

    # Devonshire Hotels (automated daily tracking)
    devonshire_budget = get_devonshire_budget_status()
    if devonshire_budget:
        budget_statuses.append(devonshire_budget)

    # Smythson Budget (period-based tracking via MICE spreadsheet)
    smythson_budget = get_smythson_budget_status()
    if smythson_budget:
        budget_statuses.append(smythson_budget)

    # UNO Lighting Budget Increase (Nov 13 - Dec 6, 2025)
    uno_budget = get_uno_budget_status()
    if uno_budget:
        budget_statuses.append(uno_budget)

    return budget_statuses

def get_shared_drive_updates(days=7):
    """
    Get shared drive updates from state file.

    Returns dict of client: [files] for files modified in last N days.
    """
    state_file = Path(__file__).parent.parent / "data" / "shared-drives-state.json"

    if not state_file.exists():
        return {}

    try:
        with open(state_file, "r") as f:
            state = json.load(f)

        # For now, return structure that would come from daily scan
        # TODO: Implement actual file tracking when script is fully built
        return state.get("recent_updates", {})
    except Exception as e:
        print(f"   ⚠️  Warning: Could not read shared drives state: {e}")
        return {}


def generate_html_report(meetings, completed_tasks, budget_status=None, shared_drive_updates=None, bright_minds_performance=None):
    """Generate HTML report of meetings, completed tasks, budget status, shared drive updates, and Bright Minds performance."""
    if budget_status is None:
        budget_status = []
    if shared_drive_updates is None:
        shared_drive_updates = {}

    if not meetings and not completed_tasks and not budget_status:
        return """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #2c3e50;">📅 Weekly Review</h1>
            <p><strong>Period:</strong> Last 7 days</p>
            <p>✅ No meetings or completed tasks found in the last 7 days.</p>
        </body>
        </html>
        """

    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            .meeting {
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }
            .meeting.company {
                border-left-color: #9b59b6;
            }
            .meeting-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            .meeting-title {
                color: #2c3e50;
                font-size: 1.1em;
                font-weight: bold;
                margin: 0;
            }
            .meeting-meta {
                color: #7f8c8d;
                font-size: 0.9em;
                margin: 5px 0;
            }
            .meeting-location {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 0.85em;
                font-weight: bold;
            }
            .location-client {
                background-color: #3498db;
                color: white;
            }
            .location-company {
                background-color: #9b59b6;
                color: white;
            }
            .meeting-preview {
                background-color: white;
                padding: 10px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                white-space: pre-wrap;
                max-height: 200px;
                overflow-y: auto;
                margin-top: 10px;
            }
            .action-required {
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .action-required h3 {
                color: #856404;
                margin-top: 0;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #7f8c8d;
                font-size: 0.9em;
            }
            .task-section {
                margin: 30px 0;
            }
            .task-item {
                background-color: #e8f5e9;
                border-left: 4px solid #4caf50;
                padding: 12px;
                margin: 10px 0;
                border-radius: 5px;
            }
            .task-title {
                color: #2e7d32;
                font-weight: bold;
                margin: 0;
            }
            .task-meta {
                color: #5d7f5f;
                font-size: 0.9em;
                margin: 5px 0 0 0;
            }
            .task-notes {
                background-color: white;
                padding: 8px;
                margin-top: 8px;
                border-radius: 3px;
                font-size: 0.9em;
                font-style: italic;
            }
            .budget-section {
                margin: 30px 0;
            }
            .budget-item {
                background-color: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }
            .budget-item.warning {
                background-color: #fff3cd;
                border-left-color: #ff9800;
            }
            .budget-item.critical {
                background-color: #ffebee;
                border-left-color: #d32f2f;
            }
            .budget-metrics {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-top: 10px;
            }
            .budget-metric {
                background-color: white;
                padding: 10px;
                border-radius: 3px;
            }
            .budget-metric-label {
                font-size: 0.85em;
                color: #666;
                margin-bottom: 5px;
            }
            .budget-metric-value {
                font-size: 1.2em;
                font-weight: bold;
                color: #2c3e50;
            }
            .budget-metric-value.over {
                color: #d32f2f;
            }
            .budget-metric-value.under {
                color: #1976d2;
            }
        </style>
    </head>
    <body>
        <h1>📅 Weekly Review</h1>
        <p><strong>Period:</strong> Last 7 days</p>
        <p><strong>Total Meetings:</strong> """ + str(len(meetings)) + """ | <strong>Completed Tasks:</strong> """ + str(len(completed_tasks)) + """</p>

        <div class="action-required">
            <h3>⚠️ Action Required</h3>
            <p>Please review the meetings below and verify that each meeting is in the correct client folder:</p>
            <ul>
                <li><strong>Client meetings</strong> should be in <code>clients/[client-name]/meeting-notes/</code></li>
                <li><strong>Company meetings</strong> should be in <code>roksys/meeting-notes/</code></li>
            </ul>
            <p>To correct assignments, run: <code>./shared/scripts/review-meeting-client.sh</code></p>
        </div>
    """

    for meeting in meetings:
        client_display = meeting['client'].replace('-', ' ').title()
        filename = meeting['file'].name
        date_str = meeting['mtime'].strftime('%Y-%m-%d %H:%M')
        participants = extract_participants(meeting['file'])
        preview = extract_meeting_preview(meeting['file'])

        location_class = "location-company" if meeting['location'] == 'company' else "location-client"
        location_text = "Company Meeting" if meeting['location'] == 'company' else f"Client: {client_display}"
        meeting_class = "meeting company" if meeting['location'] == 'company' else "meeting"

        html += f"""
        <div class="{meeting_class}">
            <div class="meeting-header">
                <div>
                    <p class="meeting-title">{filename}</p>
                    <p class="meeting-meta">
                        <span class="meeting-location {location_class}">{location_text}</span>
                        | Participants: {participants}
                    </p>
                </div>
            </div>
            <p class="meeting-meta">Modified: {date_str}</p>
            <details>
                <summary style="cursor: pointer; color: #3498db; font-weight: bold;">View Preview</summary>
                <div class="meeting-preview">{preview}</div>
            </details>
        </div>
        """

    # Add completed tasks section
    if completed_tasks:
        # Group tasks by client
        tasks_by_client = {}
        roksys_tasks = []

        for task in completed_tasks:
            client = task.get('client')
            if client:
                if client not in tasks_by_client:
                    tasks_by_client[client] = []
                tasks_by_client[client].append(task)
            else:
                roksys_tasks.append(task)

        html += """
        <div class="task-section">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #4caf50; padding-bottom: 10px;">✅ Completed Tasks</h2>
            <p>Tasks completed in the past 7 days:</p>
        """

        # Display Roksys internal tasks first
        if roksys_tasks:
            html += """
            <h3 style="color: #9b59b6; margin-top: 20px; margin-bottom: 10px;">🏢 Roksys Internal</h3>
            """

            for task in roksys_tasks:
                title = task.get('title', 'Untitled')
                tasklist_name = task.get('tasklist_name', 'Unknown List')
                notes = task.get('notes', '')
                detected_at = task.get('detected_at', '')

                # Format date
                try:
                    detected_dt = datetime.fromisoformat(detected_at.replace('Z', '+00:00'))
                    date_str = detected_dt.strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = detected_at

                html += f"""
                <div class="task-item" style="border-left-color: #9b59b6; background-color: #f3e5f5;">
                    <p class="task-title" style="color: #6a1b9a;">{title}</p>
                    <p class="task-meta">List: {tasklist_name} | Completed: {date_str}</p>
                """

                if notes:
                    html += f"""
                    <div class="task-notes">{notes}</div>
                """

                html += """
                </div>
                """

        # Display client tasks grouped by client
        for client_name in sorted(tasks_by_client.keys()):
            client_display = client_name.replace('-', ' ').title()
            client_tasks = tasks_by_client[client_name]

            html += f"""
            <h3 style="color: #3498db; margin-top: 20px; margin-bottom: 10px;">👤 {client_display} ({len(client_tasks)} task{'s' if len(client_tasks) > 1 else ''})</h3>
            """

            for task in client_tasks:
                title = task.get('title', 'Untitled')
                tasklist_name = task.get('tasklist_name', 'Unknown List')
                notes = task.get('notes', '')
                detected_at = task.get('detected_at', '')

                # Format date
                try:
                    detected_dt = datetime.fromisoformat(detected_at.replace('Z', '+00:00'))
                    date_str = detected_dt.strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = detected_at

                html += f"""
                <div class="task-item">
                    <p class="task-title">{title}</p>
                    <p class="task-meta">List: {tasklist_name} | Completed: {date_str}</p>
                """

                if notes:
                    html += f"""
                    <div class="task-notes">{notes}</div>
                """

                html += """
                </div>
                """

        html += """
        </div>
        """

    # Add budget status section
    if budget_status:
        html += """
        <div class="budget-section">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #2196f3; padding-bottom: 10px;">💰 Budget Status</h2>
            <p>Active budget monitoring for clients:</p>
        """

        for budget in budget_status:
            client = budget['client']

            # Check if this is UNO Lighting (different structure)
            is_uno = budget.get('campaign_name') == 'Budget Increase Implementation'

            if is_uno:
                # UNO-specific fields
                campaign_name = budget['campaign_name']
                period = budget.get('period', '')
                target_daily = budget['target_daily_budget']
                target_total = budget['target_total_budget']
                target_roas = budget['target_roas']
                expected_spend = budget['expected_total_spend']
                actual_spend = budget.get('actual_total_spend', 0)
                actual_daily = budget.get('actual_daily_avg', 0)
                actual_roas = budget.get('actual_roas', 0)
                deviation = budget.get('deviation', 0)
                deviation_percent = budget.get('deviation_percent', 0)
                days_elapsed = budget['days_elapsed']
                days_remaining = budget['days_remaining']
                total_days = budget['total_days']
                status = budget.get('status', 'placeholder')
                note = budget.get('note', '')

                status_icon = "ℹ️" if status == "placeholder" else ("✅" if status == "on-track" else ("⚠️" if status == "warning" else "🚨"))
                status_text = "Data Pending" if status == "placeholder" else ("On Track" if status == "on-track" else ("Warning" if status == "warning" else "Critical"))
                item_class = "budget-item"

                deviation_class = "over" if deviation > 0 else "under"
                deviation_sign = "+" if deviation > 0 else ""

                html += f"""
                <div class="{item_class}">
                    <h3 style="margin-top: 0; color: #2c3e50;">{status_icon} {client} - {campaign_name}</h3>
                    <p><strong>Period:</strong> {period}</p>
                    <p><strong>Status:</strong> {status_text}</p>
                """

                if note:
                    html += f"""
                    <div style="background-color: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 3px; margin: 15px 0;">
                        <p style="margin: 0; color: #856404;">
                            ℹ️ <strong>Note:</strong> {note}
                        </p>
                    </div>
                    """

                html += f"""
                    <div class="budget-metrics">
                        <div class="budget-metric">
                            <div class="budget-metric-label">Target Daily Budget</div>
                            <div class="budget-metric-value">£{target_daily:,.0f}/day</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Target Total (24 days)</div>
                            <div class="budget-metric-value">£{target_total:,.0f}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Target ROAS</div>
                            <div class="budget-metric-value">{target_roas}%</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Progress</div>
                            <div class="budget-metric-value">Day {days_elapsed} of {total_days}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Expected Spend (to date)</div>
                            <div class="budget-metric-value">£{expected_spend:,.0f}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Actual Spend</div>
                            <div class="budget-metric-value {deviation_class}">£{actual_spend:,.0f}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Actual Daily Avg</div>
                            <div class="budget-metric-value">£{actual_daily:,.0f}/day</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Actual ROAS</div>
                            <div class="budget-metric-value">{actual_roas}%</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Days Remaining</div>
                            <div class="budget-metric-value">{days_remaining} days</div>
                        </div>
                    </div>
                </div>
                """

            else:
                # Standard budget format (Devonshire, Smythson)
                monthly_budget = budget['monthly_budget']
                expected_spend = budget['expected_spend']
                actual_spend = budget['actual_spend']
                remaining_budget = budget['remaining_budget']
                deviation_amount = budget['deviation_amount']
                deviation_percent = budget['deviation_percent']
                days_elapsed = budget['days_elapsed']
                days_remaining = budget['days_remaining']
                status = budget['status']
                url = budget.get('url', '#')

                # Smythson-specific fields
                period = budget.get('period', '')
                pacing_percent = budget.get('pacing_percent', 0)
                required_spend_per_day = budget.get('required_spend_per_day', 0)

                status_icon = "✅" if status == "on-pace" else ("⚠️" if status == "warning" else "🚨")
                status_text = "On Pace" if status == "on-pace" else ("Warning: Off Pace" if status == "warning" else "Critical: Significant Deviation")
                item_class = f"budget-item {status}" if status != "on-pace" else "budget-item"

                deviation_class = "over" if deviation_amount > 0 else "under"
                deviation_sign = "+" if deviation_amount > 0 else ""

                # Period header for Smythson
                period_display = f" - {period}" if period else ""

                html += f"""
                <div class="{item_class}">
                    <h3 style="margin-top: 0; color: #2c3e50;">{status_icon} {client}{period_display}</h3>
                    <p><strong>Status:</strong> {status_text}</p>

                    <div class="budget-metrics">
                        <div class="budget-metric">
                            <div class="budget-metric-label">{"Period" if period else "Monthly"} Budget</div>
                            <div class="budget-metric-value">£{monthly_budget:,.0f}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Remaining Budget</div>
                            <div class="budget-metric-value">£{remaining_budget:,.2f}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Expected Spend (Day {days_elapsed})</div>
                            <div class="budget-metric-value">£{expected_spend:,.2f}</div>
                        </div>
                        <div class="budget-metric">
                            <div class="budget-metric-label">Actual Spend</div>
                            <div class="budget-metric-value {deviation_class}">£{actual_spend:,.2f}</div>
                        </div>"""

                # Add pacing % for Smythson
                if pacing_percent > 0:
                    pacing_class = "over" if pacing_percent > 100 else "under"
                    html += f"""
                        <div class="budget-metric">
                            <div class="budget-metric-label">Budget Pacing</div>
                            <div class="budget-metric-value {pacing_class}">{pacing_percent:.1f}%</div>
                        </div>"""
                else:
                    html += f"""
                        <div class="budget-metric">
                            <div class="budget-metric-label">Deviation</div>
                            <div class="budget-metric-value {deviation_class}">{deviation_sign}£{abs(deviation_amount):,.2f} ({deviation_sign}{deviation_percent:.1f}%)</div>
                        </div>"""

                # Add required spend for Smythson
                if required_spend_per_day > 0:
                    html += f"""
                        <div class="budget-metric">
                            <div class="budget-metric-label">Required Spend/Day</div>
                            <div class="budget-metric-value">£{required_spend_per_day:,.2f}</div>
                        </div>"""

                html += f"""
                        <div class="budget-metric">
                            <div class="budget-metric-label">Days Remaining</div>
                            <div class="budget-metric-value">{days_remaining} days</div>
                        </div>
                    </div>

                    <p style="margin-top: 15px;">
                        <a href="{url}" style="color: #2196f3; text-decoration: none; font-weight: bold;">📊 View Budget Tracker →</a>
                    </p>
                </div>
                """

        html += """
        </div>
        """

    # Add Bright Minds performance section
    if bright_minds_performance:
        html += """
        <div class="section">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #6CC24A; padding-bottom: 10px;">📊 Bright Minds - Google Ads Performance</h2>
        """

        week_data = bright_minds_performance.get('current_week', {})
        target_roas = bright_minds_performance.get('target_roas', 4.00)
        status = bright_minds_performance.get('status', 'unknown')
        note = bright_minds_performance.get('note', '')

        # Status styling
        if status == 'excellent':
            status_icon = "🎉"
            status_color = "#4caf50"
            status_text = "Excellent Performance"
        elif status == 'on-track':
            status_icon = "✅"
            status_color = "#2196f3"
            status_text = "On Track"
        elif status == 'needs-attention':
            status_icon = "⚠️"
            status_color = "#ff9800"
            status_text = "Needs Attention"
        else:
            status_icon = "ℹ️"
            status_color = "#666"
            status_text = "Data Pending"

        week_start = week_data.get('start', 'N/A')
        week_end = week_data.get('end', 'N/A')
        conversion_value = week_data.get('conversion_value', 0)
        cost = week_data.get('cost', 0)
        roas = week_data.get('roas', 0)
        conversions = week_data.get('conversions', 0)

        html += f"""
        <div style="background-color: #f8f9fa; border-left: 4px solid #6CC24A; padding: 15px; margin: 15px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: #2c3e50;">
                {status_icon} Week of {week_start} - {week_end}
            </h3>
            <p style="color: {status_color}; font-weight: bold; margin: 10px 0;">
                Status: {status_text}
            </p>
        """

        if note:
            html += f"""
            <div style="background-color: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 3px; margin: 15px 0;">
                <p style="margin: 0; color: #856404;">
                    ℹ️ <strong>Note:</strong> {note}
                </p>
            </div>
            """
        else:
            html += f"""
            <div class="budget-metrics" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 15px;">
                <div style="background-color: white; padding: 10px; border-radius: 3px;">
                    <div style="font-size: 0.85em; color: #666; margin-bottom: 5px;">Revenue</div>
                    <div style="font-size: 1.2em; font-weight: bold; color: #2c3e50;">£{conversion_value:,.2f}</div>
                </div>
                <div style="background-color: white; padding: 10px; border-radius: 3px;">
                    <div style="font-size: 0.85em; color: #666; margin-bottom: 5px;">Ad Spend</div>
                    <div style="font-size: 1.2em; font-weight: bold; color: #2c3e50;">£{cost:,.2f}</div>
                </div>
                <div style="background-color: white; padding: 10px; border-radius: 3px;">
                    <div style="font-size: 0.85em; color: #666; margin-bottom: 5px;">ROAS</div>
                    <div style="font-size: 1.2em; font-weight: bold; color: {'#4caf50' if roas >= target_roas else '#ff9800'};">
                        {roas:.0f}% (target: {target_roas:.0f}%)
                    </div>
                </div>
                <div style="background-color: white; padding: 10px; border-radius: 3px;">
                    <div style="font-size: 0.85em; color: #666; margin-bottom: 5px;">Conversions</div>
                    <div style="font-size: 1.2em; font-weight: bold; color: #2c3e50;">{conversions}</div>
                </div>
            </div>
            """

        html += """
        </div>
        <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
            <em>This summary is for Peter's internal review. Separate client-facing report sent to Barry and Sharon.</em>
        </p>
        </div>
        """

    # Add shared drives section
    if shared_drive_updates:
        html += """
        <div class="section">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #9c27b0; padding-bottom: 10px;">📁 Shared Drive Updates</h2>
            <p style="color: #666; margin-bottom: 20px;">New and updated documents in the last 7 days:</p>
        """

        # Group updates by client
        for client, files in sorted(shared_drive_updates.items()):
            if not files:
                continue

            client_display = client.replace('-', ' ').title()
            html += f"""
            <div style="margin-bottom: 25px; background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #9c27b0;">
                <h3 style="color: #333; margin: 0 0 15px 0; font-size: 18px;">
                    {client_display}
                </h3>
            """

            for file_info in files:
                file_name = file_info.get('name', 'Unknown')
                file_type = file_info.get('type', 'Unknown')
                modified = file_info.get('modified', 'Unknown')
                url = file_info.get('url', '#')

                # Icon based on type
                if 'spreadsheet' in file_type:
                    icon = '📊'
                elif 'document' in file_type:
                    icon = '📄'
                elif 'presentation' in file_type:
                    icon = '📊'
                elif 'pdf' in file_type:
                    icon = '📑'
                else:
                    icon = '📁'

                html += f"""
                <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 3px;">
                    <p style="margin: 0 0 5px 0;">
                        {icon} <strong><a href="{url}" style="color: #9c27b0; text-decoration: none;">{file_name}</a></strong>
                    </p>
                    <p style="margin: 0; color: #666; font-size: 13px;">
                        Last modified: {modified}
                    </p>
                </div>
                """

            html += """
            </div>
            """

        html += """
        </div>
        """

    html += """
        <div class="footer">
            <p><strong>What to Check:</strong></p>
            <ul>
                <li>Does the meeting content match the assigned client?</li>
                <li>Are company/internal meetings correctly placed in roksys/?</li>
                <li>Are client-specific meetings in the right client folder?</li>
            </ul>
            <p><em>This report was automatically generated by Pete's Brain weekly review system.</em></p>
        </div>
    </body>
    </html>
    """

    return html

def create_message(to, subject, html_content):
    """Create email message."""
    message = MIMEMultipart('alternative')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, message):
    """Send email message."""
    try:
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()
        return sent_message
    except Exception as e:
        print(f'Error sending message: {e}')
        return None

def main():
    print("📅 Weekly Review Report Generator")
    print("=" * 50)

    # Find recent meetings
    print("\n🔍 Finding meetings from last 7 days...")
    meetings = find_recent_meetings(days=7)
    print(f"   Found {len(meetings)} meeting(s)")

    if meetings:
        print("\n📋 Meetings found:")
        for meeting in meetings:
            location = "company" if meeting['location'] == 'company' else meeting['client']
            print(f"   - {meeting['file'].name} ({location})")

    # Find completed tasks
    print("\n✅ Finding completed tasks from last 7 days...")
    completed_tasks = find_completed_tasks(days=7)
    print(f"   Found {len(completed_tasks)} completed task(s)")

    if completed_tasks:
        # Group for display
        client_count = len(set(t.get('client') for t in completed_tasks if t.get('client')))
        roksys_count = len([t for t in completed_tasks if not t.get('client')])

        print("\n📋 Completed tasks breakdown:")
        print(f"   - Roksys internal: {roksys_count}")
        if client_count > 0:
            print(f"   - Client tasks: {len(completed_tasks) - roksys_count} across {client_count} client(s)")

        for task in completed_tasks:
            client = task.get('client')
            client_display = client.replace('-', ' ').title() if client else "Roksys"
            print(f"   - [{client_display}] {task.get('title')}")

    # Get budget status
    print("\n💰 Checking budget status...")
    budget_status = get_budget_status()
    if budget_status:
        print(f"   Found {len(budget_status)} client(s) with active budget monitoring")
        for budget in budget_status:
            print(f"   - {budget['client']}: {budget['status']}")
    else:
        print("   No active budget monitoring")

    # Get Bright Minds performance
    print("\n📊 Checking Bright Minds Google Ads performance...")
    bright_minds_performance = get_bright_minds_performance(days=7)
    if bright_minds_performance:
        print(f"   Week: {bright_minds_performance['current_week']['start']} to {bright_minds_performance['current_week']['end']}")
    else:
        print("   Could not fetch Bright Minds performance")

    # Get shared drive updates
    print("\n📁 Checking shared drive updates...")
    shared_drive_updates = get_shared_drive_updates(days=7)
    if shared_drive_updates:
        total_files = sum(len(files) for files in shared_drive_updates.values())
        print(f"   Found {total_files} updated file(s) across {len(shared_drive_updates)} client(s)")
        for client, files in shared_drive_updates.items():
            print(f"   - {client.replace('-', ' ').title()}: {len(files)} file(s)")
    else:
        print("   No shared drive updates found")

    # Generate report
    print("\n📄 Generating HTML report...")
    html_content = generate_html_report(meetings, completed_tasks, budget_status, shared_drive_updates, bright_minds_performance)

    # Authenticate and send
    print("\n🔐 Authenticating with Gmail...")
    creds = authenticate()

    if not creds:
        print("❌ Authentication failed")
        return 1

    try:
        service = build('gmail', 'v1', credentials=creds)

        today = datetime.now().strftime('%B %d, %Y')
        subject = f"📅 Weekly Review: Meetings & Tasks - {today}"

        print("📧 Composing email...")
        message = create_message(
            to='petere@roksys.co.uk',
            subject=subject,
            html_content=html_content
        )

        print("📤 Sending email to petere@roksys.co.uk...")
        result = send_message(service, message)

        if result:
            print(f"✅ Email sent successfully! Message ID: {result['id']}")
            return 0
        else:
            print("❌ Failed to send email")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
