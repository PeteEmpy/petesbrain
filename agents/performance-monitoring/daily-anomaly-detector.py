#!/usr/bin/env python3
"""
Daily Performance Anomaly Detector

Detects unusual performance patterns across all clients and sends email alerts.
Runs every morning at 9:00 AM to analyze performance from 2 days ago (data lag adjustment).

Outputs: data/cache/daily-performance-anomalies.json
"""

import os
import sys
import json
import statistics
from pathlib import Path
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    sys.exit(1)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data/cache/daily-performance-anomalies.json"
GOOGLE_ADS_YAML = Path.home() / "google-ads.yaml"

# Gmail configuration
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Active client configuration
ACTIVE_CLIENTS = {
    'Bright Minds': '1404868570',
    'Tree2mydoor': '4941701449',
    'National Design Academy': '1994728449',
    'Accessories for the Home': '7972994730',
    'Devonshire Hotels': '5898250490',
    'Go Glean': '8492163737',
    'Godshot': '9922220205',
    'Grain Guard': '4391940141',
    'Just Bin Bags': '9697059148',
    'Smythson UK': '8573235780',
    'Superspace': '7482100090',
    'Uno Lighting': '6413338364',
    # 'Positive Bakes': 'TBD',  # TODO: Add customer ID once Google Ads account is set up
}

# Anomaly detection thresholds (based on historical data analysis)
THRESHOLDS = {
    'critical': {
        'revenue_drop_pct': 50,      # >50% drop from 7-day avg
        'roas_drop_pct': 40,          # >40% drop from baseline
        'spend_spike_pct': 50,        # >50% above average
        'conversion_drop_pct': 60,    # >60% drop
        'zero_revenue_min': 50        # Alert if zero revenue and avg >£50/day
    },
    'warning': {
        'revenue_change_pct': 30,     # 30-50% change from avg
        'roas_change_pct': 25,        # 25-40% change
        'spend_spike_pct': 30,        # 30-50% above average
        'conversion_drop_pct': 40     # 40-60% drop
    }
}

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def fetch_daily_performance(client, customer_id, target_date, baseline_start, baseline_end):
    """Fetch target date's performance vs 7-day baseline"""
    try:
        # Query for target day
        target_query = f"""
            SELECT
                segments.date,
                metrics.conversions_value,
                metrics.cost_micros,
                metrics.conversions,
                metrics.clicks,
                metrics.impressions
            FROM customer
            WHERE segments.date = '{target_date.strftime('%Y-%m-%d')}'
        """

        ga_service = client.get_service("GoogleAdsService")
        target_response = ga_service.search(customer_id=customer_id, query=target_query)

        target_data = {}
        for row in target_response:
            target_data = {
                'revenue': row.metrics.conversions_value,
                'cost': row.metrics.cost_micros / 1_000_000,
                'conversions': row.metrics.conversions,
                'clicks': row.metrics.clicks,
                'impressions': row.metrics.impressions,
                'roas': (row.metrics.conversions_value / (row.metrics.cost_micros / 1_000_000) * 100) if row.metrics.cost_micros > 0 else 0
            }

        # Query for baseline (7 days before target)
        baseline_query = f"""
            SELECT
                segments.date,
                metrics.conversions_value,
                metrics.cost_micros,
                metrics.conversions,
                metrics.clicks,
                metrics.impressions
            FROM customer
            WHERE segments.date >= '{baseline_start.strftime('%Y-%m-%d')}'
              AND segments.date <= '{baseline_end.strftime('%Y-%m-%d')}'
            ORDER BY segments.date
        """

        baseline_response = ga_service.search(customer_id=customer_id, query=baseline_query)

        baseline_data = []
        for row in baseline_response:
            baseline_data.append({
                'revenue': row.metrics.conversions_value,
                'cost': row.metrics.cost_micros / 1_000_000,
                'conversions': row.metrics.conversions,
                'roas': (row.metrics.conversions_value / (row.metrics.cost_micros / 1_000_000) * 100) if row.metrics.cost_micros > 0 else 0
            })

        return target_data, baseline_data

    except Exception as e:
        log(f"  Error fetching data for {customer_id}: {e}")
        return {}, []

def detect_anomalies(client_name, target_data, baseline_data):
    """Detect anomalies in target date's performance vs baseline"""
    if not target_data or not baseline_data:
        return []

    anomalies = []

    # Calculate baseline averages
    baseline_revenue = statistics.mean([d['revenue'] for d in baseline_data]) if baseline_data else 0
    baseline_cost = statistics.mean([d['cost'] for d in baseline_data]) if baseline_data else 0
    baseline_conversions = statistics.mean([d['conversions'] for d in baseline_data]) if baseline_data else 0
    baseline_roas = statistics.mean([d['roas'] for d in baseline_data]) if baseline_data else 0

    # Check for zero revenue (CRITICAL)
    if target_data['revenue'] == 0 and baseline_revenue > THRESHOLDS['critical']['zero_revenue_min']:
        anomalies.append({
            'severity': 'critical',
            'type': 'zero_revenue',
            'message': f"Zero revenue on target date (baseline: £{int(baseline_revenue)}/day)",
            'target_value': 0,
            'baseline_value': round(baseline_revenue, 2),
            'change_pct': -100
        })

    # Check revenue drop (CRITICAL)
    if baseline_revenue > 0:
        revenue_change_pct = ((target_data['revenue'] - baseline_revenue) / baseline_revenue * 100)

        if revenue_change_pct < -THRESHOLDS['critical']['revenue_drop_pct']:
            anomalies.append({
                'severity': 'critical',
                'type': 'revenue_drop',
                'message': f"Revenue £{int(target_data['revenue'])} ({int(abs(revenue_change_pct))}% below baseline £{int(baseline_revenue)})",
                'target_value': round(target_data['revenue'], 2),
                'baseline_value': round(baseline_revenue, 2),
                'change_pct': round(revenue_change_pct, 1)
            })
        elif abs(revenue_change_pct) > THRESHOLDS['warning']['revenue_change_pct']:
            direction = 'drop' if revenue_change_pct < 0 else 'spike'
            anomalies.append({
                'severity': 'warning',
                'type': f'revenue_{direction}',
                'message': f"Revenue £{int(target_data['revenue'])} ({int(abs(revenue_change_pct))}% {'below' if revenue_change_pct < 0 else 'above'} baseline £{int(baseline_revenue)})",
                'target_value': round(target_data['revenue'], 2),
                'baseline_value': round(baseline_revenue, 2),
                'change_pct': round(revenue_change_pct, 1)
            })

    # Check ROAS drop (CRITICAL/WARNING)
    if baseline_roas > 0:
        roas_change_pct = ((target_data['roas'] - baseline_roas) / baseline_roas * 100)

        if roas_change_pct < -THRESHOLDS['critical']['roas_drop_pct']:
            anomalies.append({
                'severity': 'critical',
                'type': 'roas_drop',
                'message': f"ROAS {int(target_data['roas'])}% ({int(abs(roas_change_pct))}% below baseline {int(baseline_roas)}%)",
                'target_value': round(target_data['roas'], 0),
                'baseline_value': round(baseline_roas, 0),
                'change_pct': round(roas_change_pct, 1)
            })
        elif abs(roas_change_pct) > THRESHOLDS['warning']['roas_change_pct']:
            anomalies.append({
                'severity': 'warning',
                'type': 'roas_change',
                'message': f"ROAS {int(target_data['roas'])}% ({int(abs(roas_change_pct))}% {'below' if roas_change_pct < 0 else 'above'} baseline {int(baseline_roas)}%)",
                'target_value': round(target_data['roas'], 0),
                'baseline_value': round(baseline_roas, 0),
                'change_pct': round(roas_change_pct, 1)
            })

    # Check spend spike (WARNING/CRITICAL)
    if baseline_cost > 0:
        cost_change_pct = ((target_data['cost'] - baseline_cost) / baseline_cost * 100)

        if cost_change_pct > THRESHOLDS['critical']['spend_spike_pct']:
            anomalies.append({
                'severity': 'critical',
                'type': 'spend_spike',
                'message': f"Spend £{int(target_data['cost'])} ({int(cost_change_pct)}% above baseline £{int(baseline_cost)})",
                'target_value': round(target_data['cost'], 2),
                'baseline_value': round(baseline_cost, 2),
                'change_pct': round(cost_change_pct, 1)
            })
        elif cost_change_pct > THRESHOLDS['warning']['spend_spike_pct']:
            anomalies.append({
                'severity': 'warning',
                'type': 'spend_spike',
                'message': f"Spend £{int(target_data['cost'])} ({int(cost_change_pct)}% above baseline £{int(baseline_cost)})",
                'target_value': round(target_data['cost'], 2),
                'baseline_value': round(baseline_cost, 2),
                'change_pct': round(cost_change_pct, 1)
            })

    # Check conversion drop (CRITICAL/WARNING)
    if baseline_conversions > 0:
        conv_change_pct = ((target_data['conversions'] - baseline_conversions) / baseline_conversions * 100)

        if conv_change_pct < -THRESHOLDS['critical']['conversion_drop_pct']:
            anomalies.append({
                'severity': 'critical',
                'type': 'conversion_drop',
                'message': f"Conversions {round(target_data['conversions'], 1)} ({int(abs(conv_change_pct))}% below baseline {round(baseline_conversions, 1)})",
                'target_value': round(target_data['conversions'], 1),
                'baseline_value': round(baseline_conversions, 1),
                'change_pct': round(conv_change_pct, 1)
            })
        elif conv_change_pct < -THRESHOLDS['warning']['conversion_drop_pct']:
            anomalies.append({
                'severity': 'warning',
                'type': 'conversion_drop',
                'message': f"Conversions {round(target_data['conversions'], 1)} ({int(abs(conv_change_pct))}% below baseline {round(baseline_conversions, 1)})",
                'target_value': round(target_data['conversions'], 1),
                'baseline_value': round(baseline_conversions, 1),
                'change_pct': round(conv_change_pct, 1)
            })

    return anomalies

def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    token_file = PROJECT_ROOT / 'shared/email-sync/token-weekly-summary.json'
    credentials_file = PROJECT_ROOT / 'shared/email-sync/credentials.json'

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), GMAIL_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        else:
            return None

    return creds

def create_anomaly_email(anomalies_by_client, target_date):
    """Create HTML email with anomaly alerts"""

    critical_clients = {client: anomalies for client, anomalies in anomalies_by_client.items()
                        if any(a['severity'] == 'critical' for a in anomalies)}
    warning_clients = {client: anomalies for client, anomalies in anomalies_by_client.items()
                       if client not in critical_clients and any(a['severity'] == 'warning' for a in anomalies)}

    if not critical_clients and not warning_clients:
        return None  # No anomalies, don't send email

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #c0392b; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
            h2 {{ color: #e74c3c; margin-top: 30px; }}
            h3 {{ color: #e67e22; margin-top: 20px; }}
            .critical {{ background-color: #fadbd8; border-left: 4px solid #c0392b; padding: 15px; margin: 15px 0; }}
            .warning {{ background-color: #fdeaa8; border-left: 4px solid #f39c12; padding: 15px; margin: 15px 0; }}
            .client-name {{ font-weight: bold; font-size: 1.1em; color: #2c3e50; }}
            .anomaly {{ margin: 8px 0; padding-left: 10px; }}
            .metric {{ font-weight: bold; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #bdc3c7; color: #7f8c8d; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>🚨 Daily Performance Alerts - {target_date.strftime('%B %d, %Y')}</h1>
        <p>Unusual performance patterns detected (2-day lag for data accuracy).</p>
    """

    if critical_clients:
        html += f"""
        <h2>🚨 CRITICAL ISSUES ({len(critical_clients)} clients)</h2>
        """
        for client, anomalies in critical_clients.items():
            critical_anomalies = [a for a in anomalies if a['severity'] == 'critical']
            html += f"""
            <div class="critical">
                <div class="client-name">{client}</div>
            """
            for anomaly in critical_anomalies:
                html += f"""
                <div class="anomaly">• {anomaly['message']}</div>
                """
            html += "</div>"

    if warning_clients:
        html += f"""
        <h2>⚠️ WARNINGS ({len(warning_clients)} clients)</h2>
        """
        for client, anomalies in warning_clients.items():
            warning_anomalies = [a for a in anomalies if a['severity'] == 'warning']
            html += f"""
            <div class="warning">
                <div class="client-name">{client}</div>
            """
            for anomaly in warning_anomalies:
                html += f"""
                <div class="anomaly">• {anomaly['message']}</div>
                """
            html += "</div>"

    html += f"""
        <div class="footer">
            <p><strong>Detection Thresholds:</strong></p>
            <ul>
                <li>Critical: Revenue drop >50%, ROAS drop >40%, Spend spike >50%, Zero revenue days</li>
                <li>Warning: Revenue change 30-50%, ROAS change 25-40%, Spend spike 30-50%</li>
            </ul>
            <p>Baseline: 7-day average (prior to target date)</p>
        </div>
    </body>
    </html>
    """

    return html

def send_email(html_content, target_date):
    """Send anomaly alert email via Gmail API"""
    try:
        creds = authenticate_gmail()
        if not creds:
            log("ERROR: Gmail authentication failed")
            return False

        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart('alternative')
        message['to'] = 'petere@roksys.co.uk'
        message['subject'] = f"🚨 Performance Alerts - {target_date.strftime('%b %d, %Y')}"

        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)

        raw_message = {'raw': __import__('base64').urlsafe_b64encode(message.as_bytes()).decode()}
        sent_message = service.users().messages().send(userId='me', body=raw_message).execute()

        log(f"✅ Email sent successfully! Message ID: {sent_message['id']}")
        return True

    except Exception as e:
        log(f"ERROR: Failed to send email: {e}")
        return False

def main():
    log("=" * 60)
    log("Daily Performance Anomaly Detection Started")
    log("=" * 60)

    # Check for Google Ads config
    if not GOOGLE_ADS_YAML.exists():
        log(f"ERROR: Google Ads config not found at {GOOGLE_ADS_YAML}")
        return 1

    # Initialize Google Ads client
    try:
        ads_client = GoogleAdsClient.load_from_storage(str(GOOGLE_ADS_YAML))
    except Exception as e:
        log(f"ERROR: Failed to initialize Google Ads client: {e}")
        return 1

    # Calculate date ranges
    # Note: Google Ads data takes 24-48 hours to fully populate
    # So we look at 2 days ago instead of yesterday for accurate data
    today = datetime.now().date()
    target_date = today - timedelta(days=2)  # 2 days ago (data lag adjustment)
    baseline_end = target_date - timedelta(days=1)  # Day before target
    baseline_start = baseline_end - timedelta(days=6)  # 7 days baseline

    log(f"Target date: {target_date}")
    log(f"Baseline: {baseline_start} to {baseline_end}")

    # Detect anomalies for all clients
    all_anomalies = {}

    for client_name, customer_id in ACTIVE_CLIENTS.items():
        log(f"Analyzing {client_name} ({customer_id})...")

        try:
            target_data, baseline_data = fetch_daily_performance(
                ads_client, customer_id, target_date, baseline_start, baseline_end
            )

            if target_data:
                anomalies = detect_anomalies(client_name, target_data, baseline_data)

                if anomalies:
                    all_anomalies[client_name] = anomalies
                    critical_count = sum(1 for a in anomalies if a['severity'] == 'critical')
                    warning_count = sum(1 for a in anomalies if a['severity'] == 'warning')
                    log(f"  🚨 {critical_count} critical, ⚠️  {warning_count} warnings")
                else:
                    log(f"  ✓ No anomalies detected")

        except Exception as e:
            log(f"  ✗ Error: {e}")

    # Save results to JSON
    output = {
        'generated_at': datetime.now().isoformat(),
        'target_date': target_date.isoformat(),
        'baseline': {
            'start': baseline_start.isoformat(),
            'end': baseline_end.isoformat()
        },
        'anomalies': all_anomalies,
        'summary': {
            'total_clients_checked': len(ACTIVE_CLIENTS),
            'clients_with_anomalies': len(all_anomalies),
            'critical_count': sum(sum(1 for a in anomalies if a['severity'] == 'critical') for anomalies in all_anomalies.values()),
            'warning_count': sum(sum(1 for a in anomalies if a['severity'] == 'warning') for anomalies in all_anomalies.values())
        }
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    log(f"\n✅ Anomaly detection complete")
    log(f"   Saved to: {OUTPUT_FILE}")
    log(f"   Clients with anomalies: {output['summary']['clients_with_anomalies']}/{output['summary']['total_clients_checked']}")
    log(f"   Critical: {output['summary']['critical_count']}, Warnings: {output['summary']['warning_count']}")

    # Send email if anomalies detected
    if all_anomalies:
        log("\n📧 Generating and sending anomaly alert email...")
        html_content = create_anomaly_email(all_anomalies, target_date)
        if html_content:
            send_email(html_content, target_date)
    else:
        log("\n✓ No anomalies detected - no email sent")

    log("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
