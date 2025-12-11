#!/usr/local/bin/python3
"""
WheatyBags Search Campaign Monitoring Script

Monitors WheatyBags Search campaign performance after Target ROAS change from 120% to 110%.
Sends email alerts twice daily (10am and 5pm) with performance metrics.

Change Date: 2025-11-10
Campaign ID: 60035097
Customer ID: 6281395727
Previous Target ROAS: 120%
Current Target ROAS: 110%
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Ads API setup
from google.ads.googleads.client import GoogleAdsClient

PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
CUSTOMER_ID = "6281395727"
CAMPAIGN_ID = "60035097"
CHANGE_DATE = "2025-11-10"
TARGET_ROAS = 1.10  # 110%
BASELINE_DAILY_CONVERSIONS = 3.4
BASELINE_DAILY_SPEND = 29.80

# Email configuration
GMAIL_USER = os.environ.get("GMAIL_USER", "petere@roksys.co.uk")
GMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
EMAIL_TO = "petere@roksys.co.uk"


def get_campaign_performance(days_back=3):
    """Query Google Ads API for campaign performance"""

    # Initialize client
    google_ads_yaml = Path.home() / "google-ads.yaml"
    client = GoogleAdsClient.load_from_storage(str(google_ads_yaml))
    ga_service = client.get_service("GoogleAdsService")

    # Calculate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.clicks,
            metrics.impressions,
            metrics.search_impression_share,
            metrics.search_budget_lost_impression_share,
            metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE
            campaign.id = {CAMPAIGN_ID}
            AND segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    # Aggregate results
    total_cost = 0
    total_conversions = 0
    total_conv_value = 0
    total_clicks = 0
    total_impressions = 0
    impression_share = 0
    budget_lost_is = 0
    rank_lost_is = 0

    for row in response:
        total_cost += row.metrics.cost_micros
        total_conversions += row.metrics.conversions
        total_conv_value += row.metrics.conversions_value
        total_clicks += row.metrics.clicks
        total_impressions += row.metrics.impressions

        # Use latest impression share data
        if row.metrics.impressions > 0:
            impression_share = row.metrics.search_impression_share
            budget_lost_is = row.metrics.search_budget_lost_impression_share
            rank_lost_is = row.metrics.search_rank_lost_impression_share

    # Calculate metrics
    cost_gbp = total_cost / 1_000_000
    roas = (total_conv_value / cost_gbp) if cost_gbp > 0 else 0
    cpa = (cost_gbp / total_conversions) if total_conversions > 0 else 0
    daily_conversions = total_conversions / days_back
    daily_spend = cost_gbp / days_back

    return {
        'days': days_back,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'cost': cost_gbp,
        'conversions': total_conversions,
        'conv_value': total_conv_value,
        'clicks': total_clicks,
        'impressions': total_impressions,
        'roas': roas,
        'cpa': cpa,
        'impression_share': impression_share,
        'budget_lost_is': budget_lost_is,
        'rank_lost_is': rank_lost_is,
        'daily_conversions': daily_conversions,
        'daily_spend': daily_spend
    }


def get_status_emoji(roas, target=TARGET_ROAS):
    """Determine status emoji based on ROAS"""
    if roas >= target + 0.05:  # 5% above target
        return "✅"
    elif roas >= target:
        return "✅"
    elif roas >= 1.00:  # Still profitable
        return "⚠️"
    else:  # Losing money
        return "❌"


def format_html_report(data_3day, data_7day, time_label):
    """Format performance data as HTML email"""

    status = get_status_emoji(data_3day['roas'])

    # Determine overall status
    if data_3day['roas'] < 1.00:
        status_text = "❌ URGENT: LOSING MONEY"
        status_color = "#dc3545"
        action = "IMMEDIATE ACTION REQUIRED: Revert Target ROAS to 120%"
    elif data_3day['roas'] < TARGET_ROAS:
        status_text = "⚠️ BELOW TARGET"
        status_color = "#ffc107"
        action = "Monitor closely. Consider increasing Target ROAS to 115% if trend continues."
    elif data_3day['roas'] >= TARGET_ROAS and data_3day['daily_conversions'] > BASELINE_DAILY_CONVERSIONS * 2:
        status_text = "✅ PERFORMING WELL"
        status_color = "#28a745"
        action = "Continue monitoring. Change is working as expected."
    elif data_3day['roas'] >= TARGET_ROAS:
        status_text = "✅ PROFITABLE"
        status_color = "#28a745"
        action = "ROAS good but volume increase minimal. Monitor for 3 more days."
    else:
        status_text = "⚠️ MONITORING"
        status_color = "#17a2b8"
        action = "Continue monitoring."

    # Calculate changes vs baseline
    conv_change_pct = ((data_3day['daily_conversions'] / BASELINE_DAILY_CONVERSIONS) - 1) * 100
    spend_change_pct = ((data_3day['daily_spend'] / BASELINE_DAILY_SPEND) - 1) * 100

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            .header {{ background-color: {status_color}; color: white; padding: 15px; border-radius: 5px; }}
            .metric-box {{ background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; }}
            .alert {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }}
            .good {{ color: #28a745; font-weight: bold; }}
            .warning {{ color: #ffc107; font-weight: bold; }}
            .danger {{ color: #dc3545; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; font-weight: bold; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; color: #666; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>{status} WheatyBags Search Campaign - {time_label} Report</h2>
            <p style="margin: 5px 0;">Target ROAS: 110% | Change Date: {CHANGE_DATE}</p>
        </div>

        <div class="metric-box">
            <h3 style="margin-top: 0;">Overall Status: <span style="color: {status_color};">{status_text}</span></h3>
            <p><strong>Action:</strong> {action}</p>
        </div>

        <h3>Last 3 Days Performance ({data_3day['start_date']} to {data_3day['end_date']})</h3>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Status</th>
            </tr>
            <tr>
                <td><strong>ROAS</strong></td>
                <td class="{'good' if data_3day['roas'] >= TARGET_ROAS else 'danger' if data_3day['roas'] < 1.00 else 'warning'}">{data_3day['roas']:.0%}</td>
                <td>{'✅ Above target' if data_3day['roas'] >= TARGET_ROAS else '❌ LOSING MONEY' if data_3day['roas'] < 1.00 else '⚠️ Below target'}</td>
            </tr>
            <tr>
                <td><strong>Conversions</strong></td>
                <td>{data_3day['conversions']:.1f} ({data_3day['daily_conversions']:.1f}/day)</td>
                <td class="{'good' if conv_change_pct > 50 else 'warning'}">{'✅' if conv_change_pct > 50 else '⚠️'} {conv_change_pct:+.0f}% vs baseline</td>
            </tr>
            <tr>
                <td><strong>Spend</strong></td>
                <td>£{data_3day['cost']:.2f} (£{data_3day['daily_spend']:.2f}/day)</td>
                <td>{spend_change_pct:+.0f}% vs baseline</td>
            </tr>
            <tr>
                <td><strong>CPA</strong></td>
                <td>£{data_3day['cpa']:.2f}</td>
                <td class="{'good' if data_3day['cpa'] < 12 else 'warning'}">{'✅ Good' if data_3day['cpa'] < 12 else '⚠️ High'}</td>
            </tr>
            <tr>
                <td><strong>Impression Share</strong></td>
                <td>{data_3day['impression_share']:.1%}</td>
                <td class="{'good' if data_3day['impression_share'] > 0.30 else 'warning'}">{'✅ Improved' if data_3day['impression_share'] > 0.30 else '⚠️ Still low'}</td>
            </tr>
            <tr>
                <td><strong>Rank Lost IS</strong></td>
                <td>{data_3day['rank_lost_is']:.1%}</td>
                <td class="{'good' if data_3day['rank_lost_is'] < 0.50 else 'warning'}">{'✅ Better' if data_3day['rank_lost_is'] < 0.50 else '⚠️ Still losing auctions'}</td>
            </tr>
        </table>

        <h3>Last 7 Days Performance ({data_7day['start_date']} to {data_7day['end_date']})</h3>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td><strong>ROAS</strong></td>
                <td class="{'good' if data_7day['roas'] >= TARGET_ROAS else 'danger' if data_7day['roas'] < 1.00 else 'warning'}">{data_7day['roas']:.0%}</td>
            </tr>
            <tr>
                <td><strong>Conversions</strong></td>
                <td>{data_7day['conversions']:.1f} ({data_7day['daily_conversions']:.1f}/day avg)</td>
            </tr>
            <tr>
                <td><strong>Spend</strong></td>
                <td>£{data_7day['cost']:.2f} (£{data_7day['daily_spend']:.2f}/day avg)</td>
            </tr>
            <tr>
                <td><strong>CPA</strong></td>
                <td>£{data_7day['cpa']:.2f}</td>
            </tr>
        </table>

        <div class="alert" style="margin-top: 30px;">
            <h4 style="margin-top: 0;">⚠️ Critical Thresholds</h4>
            <ul>
                <li><strong>ROAS below 100%:</strong> Client loses money - REVERT IMMEDIATELY</li>
                <li><strong>ROAS 100-110%:</strong> Below target - Consider increasing to 115%</li>
                <li><strong>ROAS 110%+:</strong> On target - Continue monitoring</li>
                <li><strong>No volume increase after 7 days:</strong> Change not working - Reassess strategy</li>
            </ul>
        </div>

        <div class="footer">
            <p><strong>Campaign:</strong> CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 (ID: {CAMPAIGN_ID})</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Monitoring Period:</strong> 14 days from {CHANGE_DATE}</p>
        </div>
    </body>
    </html>
    """

    return html, status_text


def send_email(subject, html_body):
    """Send email via Gmail SMTP"""

    if not GMAIL_PASSWORD:
        print("ERROR: GMAIL_APP_PASSWORD environment variable not set")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = EMAIL_TO

        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {EMAIL_TO}")
        return True

    except Exception as e:
        print(f"ERROR sending email: {e}")
        return False


def main():
    """Main monitoring function"""

    print(f"WheatyBags Search Campaign Monitoring - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Campaign ID: {CAMPAIGN_ID}")
    print(f"Customer ID: {CUSTOMER_ID}")
    print(f"Target ROAS: {TARGET_ROAS:.0%}")
    print("-" * 60)

    # Determine time label
    hour = datetime.now().hour
    if hour < 12:
        time_label = "10am"
    else:
        time_label = "5pm"

    # Get performance data
    print("Querying 3-day performance...")
    data_3day = get_campaign_performance(days_back=3)

    print("Querying 7-day performance...")
    data_7day = get_campaign_performance(days_back=7)

    # Format report
    print("Generating report...")
    html_body, status_text = format_html_report(data_3day, data_7day, time_label)

    # Create email subject with status indicator
    subject = f"WheatyBags Monitor - {time_label} - {status_text}"

    # Send email
    print(f"Sending email to {EMAIL_TO}...")
    success = send_email(subject, html_body)

    # Print summary to console
    print("\n" + "=" * 60)
    print(f"SUMMARY - Last 3 Days:")
    print(f"  ROAS: {data_3day['roas']:.0%} (Target: {TARGET_ROAS:.0%})")
    print(f"  Conversions: {data_3day['conversions']:.1f} ({data_3day['daily_conversions']:.1f}/day)")
    print(f"  Spend: £{data_3day['cost']:.2f} (£{data_3day['daily_spend']:.2f}/day)")
    print(f"  CPA: £{data_3day['cpa']:.2f}")
    print(f"  Status: {status_text}")
    print("=" * 60)

    if success:
        print("\n✅ Monitoring complete - Email sent")
    else:
        print("\n❌ Monitoring complete - Email failed")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
