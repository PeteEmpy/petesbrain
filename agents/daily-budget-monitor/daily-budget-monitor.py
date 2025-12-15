#!/usr/bin/env python3
"""
Daily Budget Monitor
Monitors client budgets and sends alerts if spending deviates from target pacing.

Currently monitors:
- Devonshire Hotels (£11,000/month November 2025)

Usage:
    ANTHROPIC_API_KEY="key" shared/email-sync/.venv/bin/python3 shared/scripts/daily-budget-monitor.py

Automated: Runs daily at 9:00 AM via LaunchAgent
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
LOG_DIR = Path.home() / '.petesbrain-logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'daily-budget-monitor_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler()  # Also output to console for LaunchAgent logs
    ]
)

logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Add project root to path for centralized imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import centralized path discovery
from shared.paths import get_project_root as get_project_root_paths

# Verify project root can be discovered
try:
    PROJECT_ROOT = get_project_root_paths()
    logger.debug(f"Project root: {PROJECT_ROOT}")
except RuntimeError as e:
    logger.critical("=" * 60)
    logger.critical("❌ Failed to discover project root")
    logger.critical(f"Error: {e}")
    logger.critical("Action required: Set PETESBRAIN_ROOT environment variable or run from project directory")
    logger.critical("=" * 60)
    sys.exit(1)

# Gmail API imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Google Ads MCP would be called via subprocess or API
# For now, we'll structure it to be called externally

def authenticate_gmail():
    """Authenticate with Gmail API."""
    logger.info("🔐 Authenticating with Gmail API...")

    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    email_sync_dir = Path(__file__).parent.parent / 'email-sync'
    token_file = email_sync_dir / 'token.json'

    logger.debug(f"Token file path: {token_file}")

    if token_file.exists():
        logger.debug("Loading credentials from token file")
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired OAuth token...")
            creds.refresh(Request())
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            logger.info("✅ OAuth token refreshed successfully")
        else:
            logger.error("=" * 60)
            logger.error("❌ Gmail Authentication Failed")
            logger.error(f"Token file: {token_file}")
            logger.error(f"Token exists: {token_file.exists()}")
            logger.error(f"Credentials valid: {creds.valid if creds else 'N/A'}")
            logger.error("Action required: Run oauth-refresh skill")
            logger.error("=" * 60)
            raise Exception(f"No valid Gmail credentials at {token_file}")

    logger.info("✅ Gmail authentication successful")
    return creds

def get_devonshire_spend():
    """
    Get current month spend for Devonshire campaigns.
    Returns dict with main properties and The Hide breakdown.

    NOTE: This needs to be called with Google Ads MCP access.
    For now, returns structure that will be populated.
    """
    # This will be populated by calling Google Ads MCP
    # In actual implementation, we'd query:
    # - All "DEV | Properties" campaigns (excluding The Hide)
    # - The Hide campaign separately
    # - MTD spend for current month

    return {
        'main_properties': {
            'spend': 0.0,
            'campaign_count': 11
        },
        'the_hide': {
            'spend': 0.0
        },
        'total_spend': 0.0,
        'data_date': datetime.now().strftime('%Y-%m-%d')
    }

def calculate_expected_spend(monthly_budget, days_in_month, days_elapsed):
    """Calculate expected spend based on days elapsed."""
    daily_budget = monthly_budget / days_in_month
    expected_spend = daily_budget * days_elapsed

    logger.debug(f"Expected spend calculation:")
    logger.debug(f"  - Monthly budget: £{monthly_budget:,.2f}")
    logger.debug(f"  - Days in month: {days_in_month}")
    logger.debug(f"  - Days elapsed: {days_elapsed}")
    logger.debug(f"  - Daily budget: £{daily_budget:,.2f}")
    logger.debug(f"  - Expected spend: £{expected_spend:,.2f} ({expected_spend/monthly_budget*100:.1f}%)")

    return expected_spend

def calculate_deviation(actual, expected):
    """Calculate deviation amount and percentage."""
    deviation_amount = actual - expected
    deviation_percent = (deviation_amount / expected * 100) if expected > 0 else 0

    logger.info(f"📊 Deviation calculation:")
    logger.info(f"  - Actual spend: £{actual:,.2f}")
    logger.info(f"  - Expected spend: £{expected:,.2f}")
    logger.info(f"  - Deviation amount: {'+' if deviation_amount > 0 else ''}£{deviation_amount:,.2f}")
    logger.info(f"  - Deviation percent: {'+' if deviation_percent > 0 else ''}{deviation_percent:.1f}%")

    return deviation_amount, deviation_percent

def should_send_alert(deviation_percent, threshold=5.0):
    """Determine if alert should be sent based on deviation threshold."""
    send_alert = abs(deviation_percent) >= threshold

    logger.info(f"🎯 Alert decision:")
    logger.info(f"  - Absolute deviation: {abs(deviation_percent):.1f}%")
    logger.info(f"  - Threshold: {threshold}%")
    logger.info(f"  - Send alert: {'YES' if send_alert else 'NO'}")

    return send_alert

def generate_alert_email(client_data, deviation_data, today):
    """Generate HTML email for budget alert."""

    deviation_amount = deviation_data['deviation_amount']
    deviation_percent = deviation_data['deviation_percent']

    # Determine alert level
    if abs(deviation_percent) >= 15:
        alert_level = "critical"
        alert_color = "#d32f2f"
        alert_icon = "🚨"
    elif abs(deviation_percent) >= 10:
        alert_level = "warning"
        alert_color = "#ff9800"
        alert_icon = "⚠️"
    else:
        alert_level = "notice"
        alert_color = "#2196f3"
        alert_icon = "ℹ️"

    status = "OVERPACING" if deviation_amount > 0 else "UNDERPACING"

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: {alert_color}; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .alert-box {{ background: #fff3cd; border-left: 4px solid {alert_color}; padding: 15px; margin: 20px 0; }}
            .metrics {{ background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            .metric-row {{ display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: white; border-radius: 3px; }}
            .metric-label {{ font-weight: bold; }}
            .metric-value {{ font-size: 1.1em; }}
            .over {{ color: #d32f2f; font-weight: bold; }}
            .under {{ color: #1976d2; font-weight: bold; }}
            .breakdown {{ margin: 20px 0; }}
            .breakdown table {{ width: 100%; border-collapse: collapse; }}
            .breakdown th {{ background: #2196f3; color: white; padding: 10px; text-align: left; }}
            .breakdown td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            .recommendation {{ background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0; }}
            .footer {{ background: #f5f5f5; padding: 15px; margin-top: 20px; font-size: 0.9em; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{alert_icon} Budget Alert: {client_data['client_name']}</h1>
            <p style="margin: 0; font-size: 1.1em;">{status} - {today.strftime('%B %d, %Y')}</p>
        </div>

        <div class="content">
            <div class="alert-box">
                <h2 style="margin-top: 0;">Budget is {abs(deviation_percent):.1f}% {'over' if deviation_amount > 0 else 'under'} pace</h2>
                <p>Your Devonshire Hotels campaigns are {'spending faster' if deviation_amount > 0 else 'spending slower'} than the target budget pacing.</p>
            </div>

            <div class="metrics">
                <div class="metric-row">
                    <span class="metric-label">Days Elapsed:</span>
                    <span class="metric-value">{client_data['days_elapsed']} of {client_data['days_in_month']} days</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Expected Spend:</span>
                    <span class="metric-value">£{client_data['expected_spend']:,.2f} ({client_data['days_elapsed']/client_data['days_in_month']*100:.1f}%)</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Actual Spend:</span>
                    <span class="metric-value {'over' if deviation_amount > 0 else 'under'}">£{client_data['actual_spend']:,.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Deviation:</span>
                    <span class="metric-value {'over' if deviation_amount > 0 else 'under'}">
                        {'+' if deviation_amount > 0 else ''}£{deviation_amount:,.2f} ({'+' if deviation_percent > 0 else ''}{deviation_percent:.1f}%)
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Remaining Budget:</span>
                    <span class="metric-value">£{client_data['remaining_budget']:,.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Days Remaining:</span>
                    <span class="metric-value">{client_data['days_remaining']} days</span>
                </div>
            </div>

            <div class="breakdown">
                <h2>Campaign Breakdown</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>MTD Spend</th>
                            <th>Monthly Budget</th>
                            <th>% Used</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Main Properties</strong></td>
                            <td>£{client_data['main_spend']:,.2f}</td>
                            <td>£{client_data['main_budget']:,.2f}</td>
                            <td>{client_data['main_spend']/client_data['main_budget']*100:.1f}%</td>
                        </tr>
                        <tr>
                            <td><strong>The Hide</strong></td>
                            <td>£{client_data['hide_spend']:,.2f}</td>
                            <td>£{client_data['hide_budget']:,.2f}</td>
                            <td>{client_data['hide_spend']/client_data['hide_budget']*100:.1f}%</td>
                        </tr>
                        <tr style="background: #f5f5f5; font-weight: bold;">
                            <td><strong>TOTAL</strong></td>
                            <td>£{client_data['actual_spend']:,.2f}</td>
                            <td>£{client_data['monthly_budget']:,.2f}</td>
                            <td>{client_data['actual_spend']/client_data['monthly_budget']*100:.1f}%</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="recommendation">
                <h2 style="margin-top: 0;">💡 Recommendation</h2>
                {generate_recommendation(deviation_amount, deviation_percent, client_data)}
            </div>

            <h2>📊 Budget Tracker</h2>
            <p>View full details in the automated budget tracker:</p>
            <p><a href="https://docs.google.com/spreadsheets/d/1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc/">Devonshire Budget Tracker Spreadsheet</a></p>
        </div>

        <div class="footer">
            <p><strong>Automated Budget Monitor</strong> | Pete's Brain</p>
            <p>This alert was automatically generated because budget deviation exceeded {abs(deviation_percent):.1f}% threshold.</p>
            <p>Monitor runs daily at 9:00 AM | Next check: {(today + timedelta(days=1)).strftime('%B %d, %Y')}</p>
        </div>
    </body>
    </html>
    """

    return html

def generate_recommendation(deviation_amount, deviation_percent, client_data):
    """Generate recommendation based on deviation."""
    if abs(deviation_percent) < 5:
        return "<p>✅ Budget is on pace. No action needed at this time.</p>"

    if deviation_amount > 0:  # Overpacing
        if deviation_percent >= 15:
            return f"""
            <p><strong>⚠️ URGENT: Significant overpacing detected</strong></p>
            <ul>
                <li>You're spending £{abs(deviation_amount):,.2f} more than expected at this point in the month</li>
                <li>At current pace, you'll exceed budget by approximately £{abs(deviation_amount) / (client_data['days_elapsed']/client_data['days_in_month']):.0f}</li>
                <li><strong>Action:</strong> Consider reducing daily budgets immediately or pausing lower-performing campaigns</li>
                <li>Review campaign performance to identify high spenders</li>
            </ul>
            """
        elif deviation_percent >= 10:
            return f"""
            <p><strong>⚠️ Overpacing detected</strong></p>
            <ul>
                <li>You're spending £{abs(deviation_amount):,.2f} more than expected</li>
                <li>Monitor closely over next 2-3 days</li>
                <li>If trend continues, consider reducing budgets by 10-15%</li>
            </ul>
            """
        else:
            return f"""
            <p><strong>ℹ️ Slight overpacing</strong></p>
            <ul>
                <li>You're spending £{abs(deviation_amount):,.2f} more than expected</li>
                <li>This is within normal variance</li>
                <li>Monitor for next few days to see if it stabilizes</li>
            </ul>
            """
    else:  # Underpacing
        if abs(deviation_percent) >= 15:
            return f"""
            <p><strong>⚠️ URGENT: Significant underpacing detected</strong></p>
            <ul>
                <li>You're spending £{abs(deviation_amount):,.2f} less than expected</li>
                <li>At current pace, you'll underspend by approximately £{abs(deviation_amount) / (client_data['days_elapsed']/client_data['days_in_month']):.0f}</li>
                <li><strong>Action:</strong> Consider increasing daily budgets or lowering ROAS targets to capture more volume</li>
                <li>Check if campaigns are limited by budget</li>
            </ul>
            """
        elif abs(deviation_percent) >= 10:
            return f"""
            <p><strong>ℹ️ Underpacing detected</strong></p>
            <ul>
                <li>You're spending £{abs(deviation_amount):,.2f} less than expected</li>
                <li>Monitor closely to ensure you hit monthly target</li>
                <li>Consider increasing budgets by 10-15% if you want to hit target</li>
            </ul>
            """
        else:
            return f"""
            <p><strong>ℹ️ Slight underpacing</strong></p>
            <ul>
                <li>You're spending £{abs(deviation_amount):,.2f} less than expected</li>
                <li>This is within normal variance</li>
                <li>Monitor for next few days to see if it picks up</li>
            </ul>
            """

def send_email(gmail_service, to, subject, html_content):
    """Send email via Gmail API."""
    logger.info(f"📧 Preparing email...")
    logger.info(f"  - To: {to}")
    logger.info(f"  - Subject: {subject}")
    logger.debug(f"  - Content length: {len(html_content)} chars")

    message = MIMEMultipart('alternative')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        logger.info("Sending email via Gmail API...")
        sent = gmail_service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        logger.info(f"✅ Email sent successfully")
        logger.info(f"  - Message ID: {sent.get('id', 'N/A')}")

        return sent

    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ Email Send Failed")
        logger.error(f"  - Error type: {type(e).__name__}")
        logger.error(f"  - Error message: {str(e)}")
        logger.error(f"  - To: {to}")
        logger.error(f"  - Subject: {subject}")
        logger.error("=" * 60)
        return None

def main():
    from datetime import timedelta

    # LOG 1/5: START - Entry log with parameters
    logger.info("=" * 60)
    logger.info("🚀 Starting Daily Budget Monitor")
    logger.info(f"📅 Execution time: {datetime.now():%Y-%m-%d %H:%M:%S}")
    logger.info("=" * 60)

    try:
        today = datetime.now()
        current_month = today.strftime('%B %Y')
        days_in_month = 30 if today.month == 11 else 31  # November has 30 days

        logger.info(f"Current month: {current_month}")
        logger.info(f"Days in month: {days_in_month}")

        # For November 2025, implementation started Nov 3rd
        # So we need to account for Nov 1-2 spending at old rates
        if today.month == 11 and today.year == 2025:
            if today.day < 3:
                logger.warning("⏸️  Budget changes not yet implemented (Nov 3rd)")
                logger.warning("Skipping monitoring until implementation date")
                logger.info("=" * 60)
                return 0

            # Days elapsed includes Nov 1-2 at old rates + days since Nov 3
            days_elapsed = today.day
        else:
            days_elapsed = today.day

        days_remaining = days_in_month - days_elapsed

        logger.info(f"Days elapsed: {days_elapsed}/{days_in_month}")
        logger.info(f"Days remaining: {days_remaining}")

        # Devonshire Hotels monitoring
        logger.info("")
        logger.info("🏨 Monitoring: Devonshire Hotels")

        # Monthly budgets
        monthly_budget = 11000.0
        main_budget = 9000.0
        hide_budget = 2000.0

        logger.info(f"Monthly budget: £{monthly_budget:,.2f}")
        logger.info(f"  - Main Properties: £{main_budget:,.2f}")
        logger.info(f"  - The Hide: £{hide_budget:,.2f}")

        # LOG 2/5: DATA COLLECTION - Calculate expected spend
        logger.info("")
        logger.info("📥 Calculating expected spend...")
        expected_spend = calculate_expected_spend(monthly_budget, days_in_month, days_elapsed)
        logger.info(f"Expected spend to date: £{expected_spend:,.2f} ({expected_spend/monthly_budget*100:.1f}%)")

        # LOG 2/5: DATA COLLECTION - Get actual spend from Google Ads
        logger.info("")
        logger.info("🔍 Fetching current spend from Google Ads...")
        logger.warning("⚠️  NOTE: This requires Google Ads MCP to be called")
        logger.warning("For testing, using placeholder data")

        # PLACEHOLDER - In production, this would query Google Ads MCP
        spend_data = get_devonshire_spend()

        # For testing, let's simulate some data
        # If actual spend data is available, use it
        actual_spend = spend_data['total_spend']

        if actual_spend == 0:
            logger.warning("⚠️  No spend data available (using placeholder)")
            logger.warning("To get real data, this script needs to call Google Ads MCP")
            logger.info("")
            logger.info("💡 Skipping alert for now - will work once integrated with MCP")
            logger.info("=" * 60)
            return 0

        main_spend = spend_data['main_properties']['spend']
        hide_spend = spend_data['the_hide']['spend']

        logger.info(f"✅ Spend data retrieved:")
        logger.info(f"  - Total: £{actual_spend:,.2f}")
        logger.info(f"  - Main Properties: £{main_spend:,.2f}")
        logger.info(f"  - The Hide: £{hide_spend:,.2f}")

        # LOG 3/5: PROCESSING - Calculate deviation
        logger.info("")
        logger.info("⚙️  Processing deviation analysis...")
        deviation_amount, deviation_percent = calculate_deviation(actual_spend, expected_spend)

        # LOG 3/5: PROCESSING - Check if alert should be sent
        logger.info("")
        threshold = 5.0  # 5% threshold
        if should_send_alert(deviation_percent, threshold):
            logger.warning(f"🚨 ALERT: Deviation exceeds {threshold}% threshold")
            logger.info("Preparing to send email alert...")

            # LOG 4/5: OUTPUT - Prepare and send alert
            logger.info("")
            logger.info("📤 Generating alert output...")

            # Prepare client data
            client_data = {
                'client_name': 'Devonshire Hotels',
                'monthly_budget': monthly_budget,
                'main_budget': main_budget,
                'hide_budget': hide_budget,
                'expected_spend': expected_spend,
                'actual_spend': actual_spend,
                'main_spend': main_spend,
                'hide_spend': hide_spend,
                'remaining_budget': monthly_budget - actual_spend,
                'days_in_month': days_in_month,
                'days_elapsed': days_elapsed,
                'days_remaining': days_remaining
            }

            deviation_data = {
                'deviation_amount': deviation_amount,
                'deviation_percent': deviation_percent
            }

            logger.info("Generating HTML email content...")
            html_content = generate_alert_email(client_data, deviation_data, today)

            status = "OVERPACING" if deviation_amount > 0 else "UNDERPACING"
            subject = f"🚨 Budget Alert: Devonshire Hotels {status} - {today.strftime('%b %d')}"

            logger.info(f"Email subject: {subject}")

            # Authenticate and send
            try:
                creds = authenticate_gmail()
                gmail_service = build('gmail', 'v1', credentials=creds)

                result = send_email(gmail_service, 'petere@roksys.co.uk', subject, html_content)

                if result:
                    logger.info("")
                    logger.info("=" * 60)
                    logger.info("✅ Daily Budget Monitor Completed Successfully")
                    logger.info(f"  - Alert sent: YES")
                    logger.info(f"  - Message ID: {result['id']}")
                    logger.info(f"  - Status: {status}")
                    logger.info(f"  - Deviation: {'+' if deviation_percent > 0 else ''}{deviation_percent:.1f}%")
                    logger.info("=" * 60)
                else:
                    logger.error("=" * 60)
                    logger.error("❌ Daily Budget Monitor Failed")
                    logger.error("Alert email failed to send")
                    logger.error("=" * 60)
                    return 1

            except Exception as e:
                logger.error("=" * 60)
                logger.error("❌ Daily Budget Monitor Failed - Email Send Error")
                logger.error(f"  - Error type: {type(e).__name__}")
                logger.error(f"  - Error message: {str(e)}")
                logger.error(f"  - Context: Sending {status} alert for Devonshire Hotels")
                logger.error(f"  - Deviation: {deviation_percent:.1f}%")
                logger.error("=" * 60)
                return 1

        else:
            logger.info(f"✅ Budget is on pace (within {threshold}% threshold)")
            logger.info("No alert needed")

            # LOG 5/5: END - Success log (no alert)
            logger.info("")
            logger.info("=" * 60)
            logger.info("✅ Daily Budget Monitor Completed Successfully")
            logger.info(f"  - Alert sent: NO")
            logger.info(f"  - Deviation: {'+' if deviation_percent > 0 else ''}{deviation_percent:.1f}%")
            logger.info(f"  - Within threshold: {threshold}%")
            logger.info("=" * 60)

        return 0

    except Exception as e:
        # Error context logging - full debugging package
        logger.error("=" * 60)
        logger.error("❌ Daily Budget Monitor Failed - Unexpected Error")
        logger.error("=" * 60)
        logger.error("1. Operation Context:")
        logger.error(f"   - Function: main()")
        logger.error(f"   - Date: {datetime.now():%Y-%m-%d}")

        logger.error("2. Error Details:")
        logger.error(f"   - Type: {type(e).__name__}")
        logger.error(f"   - Message: {str(e)}")

        logger.error("3. Possible Causes:")
        if "credentials" in str(e).lower() or "auth" in str(e).lower():
            logger.error("   - OAuth token may be expired")
            logger.error("   - Action: Run oauth-refresh skill")
        elif "connection" in str(e).lower() or "network" in str(e).lower():
            logger.error("   - Network connectivity issue")
            logger.error("   - Action: Check internet connection")
        else:
            logger.error("   - Unknown error")
            logger.error("   - Action: Check error message and stack trace")

        logger.error("=" * 60)
        logger.exception("Full stack trace:")  # Logs full traceback
        logger.error("=" * 60)

        return 1

if __name__ == '__main__':
    sys.exit(main())
