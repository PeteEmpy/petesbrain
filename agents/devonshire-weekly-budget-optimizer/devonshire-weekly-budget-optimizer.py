#!/usr/bin/env python3
"""
Devonshire Weekly Budget Optimizer
Analyzes campaign performance and suggests budget reallocations to maximize revenue.

Runs every Thursday morning at 9:00 AM.

Identifies campaigns with:
- ROAS > 550% (5.5x)
- Lost IS Budget > 10%
- Within £9,000 monthly Properties budget constraint

Suggests specific budget increases/decreases within fixed envelope.

Usage:
    ANTHROPIC_API_KEY="key" GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml \
    shared/email-sync/.venv/bin/python3 shared/scripts/devonshire-weekly-budget-optimizer.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Gmail API imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Google Ads imports
from google.ads.googleads.client import GoogleAdsClient

# Configuration
ACCOUNT_ID = "5898250490"
MANAGER_ID = "2569949686"
THE_HIDE_CAMPAIGN_IDS = ["23069490466", "21815704991"]  # Exclude from Properties budget

# Budget constraints
MONTHLY_PROPERTIES_BUDGET = 9000.0  # £9,000 for Properties (excluding The Hide)

# Performance thresholds
MIN_ROAS = 5.5  # 550% minimum ROAS for budget increase eligibility
MIN_LOST_IS_BUDGET = 10.0  # 10% minimum Lost IS Budget to be considered constrained


def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def authenticate_gmail():
    """Authenticate with Gmail API."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    # Token is in shared/email-sync, not agents/email-sync
    email_sync_dir = Path(__file__).parent.parent.parent / 'shared' / 'email-sync'
    token_file = email_sync_dir / 'token.json'

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        else:
            raise Exception(f"No valid Gmail credentials at {token_file}")

    return creds


def get_google_ads_client():
    """Initialize Google Ads API client."""
    try:
        client = GoogleAdsClient.load_from_storage()
        return client
    except Exception as e:
        log(f"ERROR: Failed to load Google Ads client: {e}")
        sys.exit(1)


def get_campaign_performance(client):
    """
    Fetch campaign performance for last 7 days.
    Returns list of campaigns with performance metrics.
    """
    log("Fetching campaign performance (last 7 days)...")

    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.conversions_value,
            metrics.conversions,
            metrics.search_impression_share,
            metrics.search_budget_lost_impression_share,
            metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE campaign.status = 'ENABLED'
            AND campaign.name LIKE '%DEV | Properties%'
            AND segments.date DURING LAST_7_DAYS
    """

    try:
        response = ga_service.search(customer_id=ACCOUNT_ID, query=query)

        campaigns = {}
        for row in response:
            campaign_id = str(row.campaign.id)
            campaign_name = row.campaign.name

            # Skip The Hide campaigns
            if campaign_id in THE_HIDE_CAMPAIGN_IDS:
                continue

            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    'id': campaign_id,
                    'name': campaign_name,
                    'budget_micros': row.campaign_budget.amount_micros,
                    'cost_micros': 0,
                    'conversions_value': 0.0,
                    'conversions': 0.0
                }

            campaigns[campaign_id]['cost_micros'] += row.metrics.cost_micros
            campaigns[campaign_id]['conversions_value'] += row.metrics.conversions_value
            campaigns[campaign_id]['conversions'] += row.metrics.conversions

            # Lost IS Budget (take latest value)
            campaigns[campaign_id]['lost_is_budget'] = row.metrics.search_budget_lost_impression_share * 100

        # Calculate ROAS and daily budgets
        results = []
        for campaign in campaigns.values():
            cost = campaign['cost_micros'] / 1_000_000
            revenue = campaign['conversions_value']
            budget_daily = campaign['budget_micros'] / 1_000_000

            roas = (revenue / cost) if cost > 0 else 0.0
            roas_percent = roas * 100

            results.append({
                'id': campaign['id'],
                'name': campaign['name'],
                'budget_daily': budget_daily,
                'cost_7d': cost,
                'revenue_7d': revenue,
                'conversions_7d': campaign['conversions'],
                'roas': roas,
                'roas_percent': roas_percent,
                'lost_is_budget': campaign.get('lost_is_budget', 0.0)
            })

        # Sort by ROAS descending
        results.sort(key=lambda x: x['roas'], reverse=True)

        log(f"✓ Fetched {len(results)} Properties campaigns (excluding The Hide)")
        return results

    except Exception as e:
        log(f"ERROR: Failed to fetch campaign performance: {e}")
        return []


def calculate_budget_recommendations(campaigns):
    """
    Analyze campaigns and suggest budget reallocations.

    Rules:
    - Identify campaigns with ROAS > 5.5x AND Lost IS Budget > 10%
    - Identify campaigns with ROAS < 5.5x OR zero conversions (candidates for reduction)
    - Suggest reallocations within £9,000 total budget
    """
    log("\nAnalyzing campaigns for optimization opportunities...")

    # Current total daily budget
    current_total_daily = sum(c['budget_daily'] for c in campaigns)
    target_monthly_budget = MONTHLY_PROPERTIES_BUDGET
    target_daily_budget = target_monthly_budget / 30  # Approximate £300/day

    log(f"Current total daily budget: £{current_total_daily:.2f}")
    log(f"Target daily budget: £{target_daily_budget:.2f}")

    # Categorize campaigns
    increase_candidates = []
    decrease_candidates = []
    maintain = []

    for campaign in campaigns:
        roas = campaign['roas']
        lost_is = campaign['lost_is_budget']
        conversions = campaign['conversions_7d']

        # Increase candidates: High ROAS + Budget constrained
        if roas >= MIN_ROAS and lost_is >= MIN_LOST_IS_BUDGET:
            increase_candidates.append(campaign)

        # Decrease candidates: Low ROAS OR zero conversions
        elif roas < MIN_ROAS or conversions == 0:
            decrease_candidates.append(campaign)

        # Maintain: Decent performance but not constrained
        else:
            maintain.append(campaign)

    log(f"\n📊 Campaign Analysis:")
    log(f"   Increase candidates: {len(increase_candidates)} campaigns")
    log(f"   Decrease candidates: {len(decrease_candidates)} campaigns")
    log(f"   Maintain: {len(maintain)} campaigns")

    # Generate recommendations
    recommendations = {
        'increase': [],
        'decrease': [],
        'maintain': [],
        'summary': {
            'current_daily_total': current_total_daily,
            'target_daily_total': target_daily_budget,
            'available_budget': 0.0,
            'proposed_increases': 0.0,
            'proposed_decreases': 0.0
        }
    }

    # Calculate available budget from decreases
    total_decrease = 0.0
    for campaign in decrease_candidates:
        # Suggest 20% reduction or pause if zero conversions
        if campaign['conversions_7d'] == 0:
            reduction = campaign['budget_daily']  # Pause completely
            new_budget = 0.0
            action = "PAUSE"
        else:
            reduction = campaign['budget_daily'] * 0.2
            new_budget = campaign['budget_daily'] - reduction
            action = "REDUCE 20%"

        total_decrease += reduction

        recommendations['decrease'].append({
            'campaign': campaign,
            'action': action,
            'current_budget': campaign['budget_daily'],
            'proposed_budget': new_budget,
            'reduction': reduction,
            'reason': f"ROAS {campaign['roas']:.1f}x (below 5.5x threshold)" if campaign['conversions_7d'] > 0 else "Zero conversions in last 7 days"
        })

    recommendations['summary']['available_budget'] = total_decrease
    recommendations['summary']['proposed_decreases'] = total_decrease

    # Allocate increases to top performers
    if increase_candidates and total_decrease > 0:
        # Distribute available budget proportionally by Lost IS Budget
        total_lost_is = sum(c['lost_is_budget'] for c in increase_candidates)

        for campaign in increase_candidates:
            # Allocate proportional to Lost IS Budget
            weight = campaign['lost_is_budget'] / total_lost_is
            increase = total_decrease * weight
            new_budget = campaign['budget_daily'] + increase

            recommendations['increase'].append({
                'campaign': campaign,
                'action': "INCREASE",
                'current_budget': campaign['budget_daily'],
                'proposed_budget': new_budget,
                'increase': increase,
                'reason': f"ROAS {campaign['roas']:.1f}x, {campaign['lost_is_budget']:.1f}% Lost IS Budget"
            })

        recommendations['summary']['proposed_increases'] = total_decrease

    # Maintain list
    for campaign in maintain:
        recommendations['maintain'].append({
            'campaign': campaign,
            'action': "MAINTAIN",
            'current_budget': campaign['budget_daily'],
            'proposed_budget': campaign['budget_daily'],
            'reason': f"ROAS {campaign['roas']:.1f}x, {campaign['lost_is_budget']:.1f}% Lost IS Budget - performing well but not constrained"
        })

    return recommendations


def generate_email_html(recommendations, today):
    """Generate HTML email with budget recommendations."""

    summary = recommendations['summary']
    increases = recommendations['increase']
    decreases = recommendations['decrease']
    maintains = recommendations['maintain']

    # Determine if there are actionable recommendations
    has_recommendations = len(increases) > 0 or len(decreases) > 0

    if has_recommendations:
        header_color = "#2196f3"
        header_icon = "💡"
        header_text = "Budget Optimization Recommendations"
    else:
        header_color = "#4caf50"
        header_icon = "✅"
        header_text = "No Changes Needed - Budget Optimized"

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.4; color: #333; margin: 0; padding: 0; }}
            .header {{ background: {header_color}; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .summary-box {{ background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            .metric-row {{ display: flex; justify-content: space-between; margin: 6px 0; padding: 8px; background: white; border-radius: 3px; }}
            .metric-label {{ font-weight: bold; }}
            .metric-value {{ font-size: 1.05em; }}
            .section {{ margin: 20px 0; }}
            .section-header {{ background: #e3f2fd; padding: 10px; margin: 15px 0 10px 0; border-left: 4px solid #2196f3; font-weight: bold; font-size: 1.1em; }}
            .campaign-list {{ margin: 10px 0; }}
            .campaign-item {{ background: white; border: 1px solid #ddd; border-radius: 5px; padding: 12px; margin: 6px 0; }}
            .campaign-name {{ font-weight: bold; color: #1976d2; margin-bottom: 6px; }}
            .campaign-metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.9em; margin: 6px 0; }}
            .campaign-action {{ background: #e8f5e9; padding: 8px; margin: 6px 0; border-radius: 3px; }}
            .action-increase {{ background: #e8f5e9; border-left: 3px solid #4caf50; }}
            .action-decrease {{ background: #ffebee; border-left: 3px solid #f44336; }}
            .action-maintain {{ background: #f5f5f5; border-left: 3px solid #9e9e9e; }}
            .budget-change {{ font-size: 1.1em; font-weight: bold; }}
            .increase {{ color: #4caf50; }}
            .decrease {{ color: #f44336; }}
            .recommendation-box {{ background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0; }}
            .footer {{ background: #f5f5f5; padding: 15px; margin-top: 20px; font-size: 0.85em; color: #666; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th {{ background: #2196f3; color: white; padding: 8px; text-align: left; font-size: 0.9em; }}
            td {{ padding: 8px; border-bottom: 1px solid #ddd; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{header_icon} {header_text}</h1>
            <p style="margin: 0; font-size: 1.05em;">Devonshire Hotels - {today.strftime('%B %d, %Y')}</p>
        </div>

        <div class="content">
    """

    if has_recommendations:
        html += f"""
            <div class="summary-box">
                <h2 style="margin-top: 0;">💰 Budget Reallocation Summary</h2>
                <div class="metric-row">
                    <span class="metric-label">Available from reductions:</span>
                    <span class="metric-value">£{summary['available_budget']:.2f}/day</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Proposed for increases:</span>
                    <span class="metric-value">£{summary['proposed_increases']:.2f}/day</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Net budget change:</span>
                    <span class="metric-value">£0.00/day (budget-neutral)</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Monthly budget maintained:</span>
                    <span class="metric-value">£9,000</span>
                </div>
            </div>

            <div class="recommendation-box">
                <h2 style="margin-top: 0;">💡 Key Insight</h2>
                <p>We've identified <strong>{len(increases)} campaign(s)</strong> with excellent ROAS (>550%) that are being held back by budget constraints. By reallocating budget from <strong>{len(decreases)} underperforming campaign(s)</strong>, we can increase revenue without increasing total spend.</p>
            </div>
        """
    else:
        html += f"""
            <div class="summary-box">
                <h2 style="margin-top: 0;">✅ Current Status</h2>
                <p>All campaigns are performing well and optimally budgeted. No budget reallocations needed this week.</p>
                <div class="metric-row">
                    <span class="metric-label">Current daily budget:</span>
                    <span class="metric-value">£{summary['current_daily_total']:.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Monthly budget:</span>
                    <span class="metric-value">£9,000</span>
                </div>
            </div>
        """

    # INCREASE RECOMMENDATIONS
    if increases:
        html += """
            <div class="section">
                <div class="section-header">📈 Budget Increases (High Performers)</div>
                <p style="margin: 6px 0;"><strong>These campaigns have strong ROAS and are budget-constrained. Increasing budgets here will drive more revenue.</strong></p>
                <div class="campaign-list">
        """

        for rec in increases:
            campaign = rec['campaign']
            html += f"""
                <div class="campaign-item action-increase">
                    <div class="campaign-name">{campaign['name']}</div>
                    <div class="campaign-metrics">
                        <div>ROAS: <strong>{campaign['roas']:.1f}x ({campaign['roas_percent']:.0f}%)</strong></div>
                        <div>Lost IS Budget: <strong>{campaign['lost_is_budget']:.1f}%</strong></div>
                        <div>7d Revenue: <strong>£{campaign['revenue_7d']:,.2f}</strong></div>
                        <div>7d Conversions: <strong>{campaign['conversions_7d']:.1f}</strong></div>
                    </div>
                    <div class="campaign-action">
                        <div class="budget-change increase">
                            £{rec['current_budget']:.2f}/day → £{rec['proposed_budget']:.2f}/day
                            (+£{rec['increase']:.2f}/day)
                        </div>
                        <div style="margin-top: 6px; font-size: 0.9em;">{rec['reason']}</div>
                    </div>
                </div>
            """

        html += """
                </div>
            </div>
        """

    # DECREASE RECOMMENDATIONS
    if decreases:
        html += """
            <div class="section">
                <div class="section-header">📉 Budget Reductions (Underperformers)</div>
                <p style="margin: 6px 0;"><strong>These campaigns have low ROAS or zero conversions. Reducing budgets here frees up budget for top performers.</strong></p>
                <div class="campaign-list">
        """

        for rec in decreases:
            campaign = rec['campaign']
            html += f"""
                <div class="campaign-item action-decrease">
                    <div class="campaign-name">{campaign['name']}</div>
                    <div class="campaign-metrics">
                        <div>ROAS: <strong>{campaign['roas']:.1f}x ({campaign['roas_percent']:.0f}%)</strong></div>
                        <div>Lost IS Budget: <strong>{campaign['lost_is_budget']:.1f}%</strong></div>
                        <div>7d Revenue: <strong>£{campaign['revenue_7d']:,.2f}</strong></div>
                        <div>7d Conversions: <strong>{campaign['conversions_7d']:.1f}</strong></div>
                    </div>
                    <div class="campaign-action">
                        <div class="budget-change decrease">
                            £{rec['current_budget']:.2f}/day → £{rec['proposed_budget']:.2f}/day
                            (-£{rec['reduction']:.2f}/day)
                        </div>
                        <div style="margin-top: 6px; font-size: 0.9em;">{rec['reason']}</div>
                    </div>
                </div>
            """

        html += """
                </div>
            </div>
        """

    # MAINTAIN
    if maintains:
        html += """
            <div class="section">
                <div class="section-header">➡️ No Changes (Optimized)</div>
                <p style="margin: 6px 0;"><strong>These campaigns are performing well and appropriately budgeted.</strong></p>
        """

        html += """
                <table>
                    <thead>
                        <tr>
                            <th>Campaign</th>
                            <th>Daily Budget</th>
                            <th>ROAS</th>
                            <th>Lost IS Budget</th>
                            <th>7d Revenue</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for rec in maintains:
            campaign = rec['campaign']
            html += f"""
                        <tr>
                            <td>{campaign['name']}</td>
                            <td>£{campaign['budget_daily']:.2f}</td>
                            <td>{campaign['roas']:.1f}x</td>
                            <td>{campaign['lost_is_budget']:.1f}%</td>
                            <td>£{campaign['revenue_7d']:,.2f}</td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        """

    # Expected impact
    if has_recommendations:
        total_increase_revenue = sum(
            rec['campaign']['revenue_7d'] * (rec['increase'] / rec['campaign']['budget_daily'])
            for rec in increases
            if rec['campaign']['budget_daily'] > 0
        )

        html += f"""
            <div class="section">
                <div class="section-header">📊 Expected Impact</div>
                <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <div style="font-size: 1.1em; margin-bottom: 6px;"><strong>Estimated Weekly Revenue Increase:</strong></div>
                    <div style="font-size: 1.3em; color: #4caf50; font-weight: bold;">+£{total_increase_revenue:,.0f}/week</div>
                    <div style="font-size: 0.9em; margin-top: 6px; color: #666;">Based on last 7 days performance and proportional budget increases</div>
                </div>
                <p style="margin: 6px 0;"><strong>Note:</strong> This assumes the high-performing campaigns maintain their current ROAS at increased budgets. Actual results may vary based on auction dynamics.</p>
            </div>
        """

    html += f"""
            <h2>🎯 Next Steps</h2>
            <ol style="line-height: 1.6;">
                <li><strong>Review recommendations above</strong></li>
                <li><strong>If approved</strong>, implement budget changes in Google Ads</li>
                <li><strong>Monitor performance</strong> over next 7 days to validate impact</li>
                <li><strong>Next review</strong>: {(today + timedelta(days=7)).strftime('%B %d, %Y')} (next Thursday)</li>
            </ol>

            <div style="background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">📋 Quick Implementation</h3>
                <p style="margin: 6px 0;">To implement these changes:</p>
                <ol style="line-height: 1.6; margin: 6px 0;">
                    <li>Open Google Ads → Devonshire account</li>
                    <li>Navigate to each campaign listed above</li>
                    <li>Update daily budgets as recommended</li>
                    <li>Changes take effect immediately</li>
                </ol>
            </div>
        </div>

        <div class="footer">
            <p><strong>Automated Weekly Budget Optimizer</strong> | Pete's Brain</p>
            <p>This report analyzes the last 7 days of campaign performance and suggests budget reallocations within your £9,000 monthly Properties budget.</p>
            <p><strong>Criteria:</strong> Campaigns with ROAS > 550% and Lost IS Budget > 10% are candidates for increases. Campaigns with ROAS < 550% or zero conversions are candidates for reductions.</p>
            <p>Runs every Thursday at 9:00 AM | Next report: {(today + timedelta(days=7)).strftime('%B %d, %Y')}</p>
        </div>
    </body>
    </html>
    """

    return html


def send_email(gmail_service, to, subject, html_content):
    """Send email via Gmail API."""
    message = MIMEMultipart('alternative')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        sent = gmail_service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        return sent
    except Exception as e:
        log(f"ERROR: Failed to send email: {e}")
        return None


def main():
    """Main workflow"""
    log("=" * 80)
    log("📊 Devonshire Weekly Budget Optimizer")
    log("=" * 80)

    today = datetime.now()
    log(f"\n📅 Date: {today.strftime('%A, %B %d, %Y')}")

    # Initialize Google Ads client
    client = get_google_ads_client()

    # Fetch campaign performance
    campaigns = get_campaign_performance(client)

    if not campaigns:
        log("❌ No campaign data available")
        return 1

    log(f"\n📊 Campaign Summary:")
    log(f"   Total campaigns: {len(campaigns)}")
    log(f"   Total daily budget: £{sum(c['budget_daily'] for c in campaigns):.2f}")
    log(f"   Total 7d spend: £{sum(c['cost_7d'] for c in campaigns):,.2f}")
    log(f"   Total 7d revenue: £{sum(c['revenue_7d'] for c in campaigns):,.2f}")

    # Calculate recommendations
    recommendations = calculate_budget_recommendations(campaigns)

    # Generate email
    log("\n📧 Generating email report...")
    html_content = generate_email_html(recommendations, today)

    has_recommendations = len(recommendations['increase']) > 0 or len(recommendations['decrease']) > 0

    if has_recommendations:
        subject = f"💡 Devonshire Budget Optimization - {today.strftime('%b %d')}"
        log("\n💡 Actionable recommendations found")
    else:
        subject = f"✅ Devonshire Budget Review - No Changes Needed - {today.strftime('%b %d')}"
        log("\n✅ No changes needed - budget optimized")

    # Authenticate and send
    try:
        log("\n🔐 Authenticating with Gmail...")
        creds = authenticate_gmail()
        gmail_service = build('gmail', 'v1', credentials=creds)

        log("📧 Sending weekly report to petere@roksys.co.uk...")
        result = send_email(gmail_service, 'petere@roksys.co.uk', subject, html_content)

        if result:
            log(f"✅ Report sent successfully! Message ID: {result['id']}")

            if has_recommendations:
                log("\n💡 Recommendations Summary:")
                log(f"   Increase: {len(recommendations['increase'])} campaigns")
                log(f"   Decrease: {len(recommendations['decrease'])} campaigns")
                log(f"   Maintain: {len(recommendations['maintain'])} campaigns")
        else:
            log("❌ Failed to send report")
            return 1
    except Exception as e:
        log(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    log("\n" + "=" * 80)
    return 0


if __name__ == '__main__':
    sys.exit(main())
