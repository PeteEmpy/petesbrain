#!/usr/bin/env python3
"""
Check Daily Performance Sheet Capacity

Monitors cell usage and sends alerts when archival is needed.
Designed to run daily via LaunchAgent.
"""

import json
import os
import smtplib
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_sheet_capacity(spreadsheet_id: str, sheet_name: str) -> dict:
    """Get capacity info for a specific sheet"""
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")

    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = build('sheets', 'v4', credentials=credentials)

    # Get sheet properties
    spreadsheet = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        includeGridData=False
    ).execute()

    # Find the specific sheet
    for sheet in spreadsheet.get('sheets', []):
        if sheet['properties']['title'] == sheet_name:
            props = sheet['properties']
            grid_props = props.get('gridProperties', {})
            rows = grid_props.get('rowCount', 0)
            cols = grid_props.get('columnCount', 0)
            cells = rows * cols

            return {
                'rows': rows,
                'cols': cols,
                'cells': cells,
                'capacity_pct': cells / 10_000_000 * 100
            }

    return None


def get_total_capacity(spreadsheet_id: str) -> dict:
    """Get total spreadsheet capacity"""
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = build('sheets', 'v4', credentials=credentials)

    spreadsheet = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        includeGridData=False
    ).execute()

    total_cells = 0
    sheets_info = []

    for sheet in spreadsheet.get('sheets', []):
        props = sheet['properties']
        grid_props = props.get('gridProperties', {})
        rows = grid_props.get('rowCount', 0)
        cols = grid_props.get('columnCount', 0)
        cells = rows * cols
        total_cells += cells

        sheets_info.append({
            'name': props['title'],
            'rows': rows,
            'cols': cols,
            'cells': cells
        })

    return {
        'total_cells': total_cells,
        'capacity_pct': total_cells / 10_000_000 * 100,
        'sheets': sheets_info
    }


def send_alert(subject: str, body: str):
    """Send email alert"""
    # Email configuration from environment
    sender = os.getenv('GMAIL_USER', 'your-email@gmail.com')
    password = os.getenv('GMAIL_APP_PASSWORD', '')
    recipient = os.getenv('ALERT_EMAIL', sender)

    if not password:
        print("Warning: GMAIL_APP_PASSWORD not set, skipping email")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Plain text version
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"✅ Alert sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")


def main():
    print("\n" + "="*80)
    print("CAPACITY CHECK")
    print("="*80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load config
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    spreadsheet_id = config['spreadsheet_id']

    # Check total capacity
    total_info = get_total_capacity(spreadsheet_id)
    total_pct = total_info['capacity_pct']

    print(f"Total Spreadsheet Capacity: {total_pct:.1f}%")
    print(f"Total Cells: {total_info['total_cells']:,} / 10,000,000")
    print()

    # Check Daily Performance specifically
    daily_perf = get_sheet_capacity(spreadsheet_id, 'Daily Performance')

    if daily_perf:
        daily_pct = daily_perf['capacity_pct']
        print(f"Daily Performance Sheet:")
        print(f"  Rows: {daily_perf['rows']:,}")
        print(f"  Columns: {daily_perf['cols']}")
        print(f"  Cells: {daily_perf['cells']:,}")
        print(f"  Capacity: {daily_pct:.1f}%")
        print()

        # Calculate days until full
        # Assuming 10,500 rows/day (15 clients × 700 products)
        daily_row_accumulation = 10500
        cells_per_day = daily_row_accumulation * daily_perf['cols']
        available_cells = 10_000_000 - total_info['total_cells']
        days_remaining = available_cells / cells_per_day if cells_per_day > 0 else 999

        print(f"Estimated days until full: {days_remaining:.0f} days")
        print()

        # Determine alert level
        alert_needed = False
        alert_severity = None
        alert_message = None

        if total_pct >= 95:
            alert_needed = True
            alert_severity = "🚨 CRITICAL"
            alert_message = (
                f"URGENT: Spreadsheet at {total_pct:.1f}% capacity!\n\n"
                f"Daily Performance sheet has {daily_perf['rows']:,} rows.\n"
                f"Estimated days until full: {days_remaining:.0f}\n\n"
                f"ACTION REQUIRED IMMEDIATELY:\n"
                f"Run archival script NOW to free up space:\n\n"
                f"  cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer\n"
                f"  GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\\n"
                f"    .venv/bin/python3 archive_old_data.py --yes --keep-days 60\n\n"
                f"View spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
            )

        elif total_pct >= 85:
            alert_needed = True
            alert_severity = "⚠️  WARNING"
            alert_message = (
                f"Spreadsheet at {total_pct:.1f}% capacity.\n\n"
                f"Daily Performance sheet has {daily_perf['rows']:,} rows.\n"
                f"Estimated days until full: {days_remaining:.0f}\n\n"
                f"ACTION REQUIRED WITHIN 1 WEEK:\n"
                f"Schedule archival to free up space:\n\n"
                f"  cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer\n"
                f"  GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\\n"
                f"    .venv/bin/python3 archive_old_data.py --yes --keep-days 90\n\n"
                f"View spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
            )

        elif total_pct >= 70:
            alert_needed = True
            alert_severity = "ℹ️  INFO"
            alert_message = (
                f"Spreadsheet at {total_pct:.1f}% capacity.\n\n"
                f"Daily Performance sheet has {daily_perf['rows']:,} rows.\n"
                f"Estimated days until full: {days_remaining:.0f}\n\n"
                f"Plan archival for the next 2-4 weeks.\n\n"
                f"View spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
            )

        # Send alert if needed
        if alert_needed:
            print(f"{alert_severity}")
            print(alert_message)
            print()

            # Check if we should send email (only send once per day for same severity)
            state_file = Path(__file__).parent / "data" / "capacity_alert_state.json"
            state_file.parent.mkdir(exist_ok=True)

            should_send = True
            today = datetime.now().strftime("%Y-%m-%d")

            if state_file.exists():
                with open(state_file) as f:
                    state = json.load(f)

                # Don't re-send if same severity level sent today
                if state.get('last_alert_date') == today and state.get('last_severity') == alert_severity:
                    should_send = False
                    print("(Alert already sent today, skipping email)")

            if should_send:
                subject = f"{alert_severity} Product Impact Analyzer - Capacity Alert ({total_pct:.1f}%)"
                send_alert(subject, alert_message)

                # Save state
                with open(state_file, 'w') as f:
                    json.dump({
                        'last_alert_date': today,
                        'last_severity': alert_severity,
                        'capacity_pct': total_pct
                    }, f)

        else:
            print("✅ Capacity healthy, no action needed")
            print()

    print("="*80)


if __name__ == "__main__":
    main()
