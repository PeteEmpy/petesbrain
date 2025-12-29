#!/usr/bin/env python3
"""
Weekly Revenue Attribution Report

Generates comprehensive revenue-based classification report for all clients,
identifying high-value products that may be misclassified by external systems.

Runs weekly on Sundays to analyze last 30 days of performance.

Usage:
    # Automated (via LaunchAgent)
    python3 revenue_attribution_report.py

    # Manual test
    python3 revenue_attribution_report.py --test

    # Specific client only
    python3 revenue_attribution_report.py --client "Smythson"
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))
from revenue_classifier import RevenueClassifier
from monitor import ProductMonitor

# Add project root to path for centralized imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.petesbrain_secrets import get_secret


class RevenueAttributionReporter:
    """Generates weekly revenue attribution reports"""

    def __init__(self, config_path: Path):
        """Initialize reporter"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

        # Initialize classifier and monitor
        self.classifier = RevenueClassifier()
        self.monitor = ProductMonitor(config_path)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def generate_report(self, client_filter: Optional[str] = None) -> str:
        """
        Generate comprehensive revenue attribution report.

        Args:
            client_filter: Optional client name to filter

        Returns:
            HTML report content
        """
        self.log("="*80)
        self.log("REVENUE ATTRIBUTION REPORT")
        self.log("="*80)

        # Analysis period: last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        period_str = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Revenue Attribution Report - {period_str}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 40px 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                h1 {{ color: #10B981; border-bottom: 3px solid #10B981; padding-bottom: 10px; }}
                h2 {{ color: #059669; border-bottom: 2px solid #D1FAE5; padding-bottom: 8px; margin-top: 40px; }}
                h3 {{ color: #047857; margin-top: 30px; }}
                h4 {{ color: #065F46; margin-top: 20px; }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th {{
                    background-color: #10B981;
                    color: white;
                    padding: 12px;
                    font-weight: 600;
                    text-align: left;
                }}
                td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background-color: #D1FAE5;
                }}
                .summary-box {{
                    background: #F0FDF4;
                    border-left: 4px solid #10B981;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .warning-box {{
                    background: #FEF3C7;
                    border-left: 4px solid #F59E0B;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .stat {{
                    font-size: 1.1em;
                    font-weight: 600;
                    color: #059669;
                }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>🟢 Revenue Attribution Report</h1>
            <p><strong>Period:</strong> {period_str} (30 days)</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """

        # Process each client
        for client_config in self.config['clients']:
            if not client_config.get('enabled'):
                continue

            client_name = client_config['name']

            if client_filter and client_name != client_filter:
                continue

            self.log(f"\nAnalysing {client_name}...")

            # Load 30-day ads data
            ads_data = self.monitor.load_current_ads_data(client_name)

            if not ads_data:
                self.log(f"  No ads data for {client_name}")
                continue

            # Aggregate 30-day metrics
            metrics = self.monitor.aggregate_product_metrics(ads_data, client_name, days_back=30)

            # Load external labels
            labels = self.monitor.load_current_labels(client_name)

            # Run revenue classification
            classifications, stats = self.classifier.classify_products(metrics, external_labels=labels)

            if not classifications:
                self.log(f"  No revenue data for {client_name}")
                html += f"""
                <h2>{client_name}</h2>
                <p><em>No revenue data in the last 30 days</em></p>
                """
                continue

            self.log(f"  Classified {stats['total_products']} products")
            self.log(f"  Top 20% generate {stats['hero_revenue_pct']:.1f}% of revenue")

            # Generate client section
            html += self.generate_client_section(client_name, classifications, stats)

        html += """
        </div>
        </body>
        </html>
        """

        return html

    def generate_client_section(
        self,
        client: str,
        classifications: List,
        stats: Dict
    ) -> str:
        """Generate HTML section for one client"""

        html = f"""
        <h2>{client}</h2>

        <div class="summary-box">
            <h4>Revenue Concentration</h4>
            <p>
                Top 20% of products (<span class="stat">{stats['hero_count']} products</span>) generate
                <span class="stat">£{stats['hero_revenue']:.2f}</span>
                (<span class="stat">{stats['hero_revenue_pct']:.1f}%</span> of total revenue)
            </p>
            <p>
                Total revenue: <span class="stat">£{stats['total_revenue']:.2f}</span>
                from <span class="stat">{stats['total_products']} products</span>
            </p>
        </div>

        <h3>Revenue Classification Distribution</h3>
        <table>
            <tr>
                <th>Classification</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
            <tr>
                <td>Revenue Heroes (Top 20%)</td>
                <td>{stats['hero_count']}</td>
                <td>{stats['hero_count'] / stats['total_products'] * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Revenue Sidekicks (60-80%)</td>
                <td>{stats['sidekick_count']}</td>
                <td>{stats['sidekick_count'] / stats['total_products'] * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Revenue Villains (20-60%)</td>
                <td>{stats['villain_count']}</td>
                <td>{stats['villain_count'] / stats['total_products'] * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Revenue Zombies (Bottom 20%)</td>
                <td>{stats['zombie_count']}</td>
                <td>{stats['zombie_count'] / stats['total_products'] * 100:.1f}%</td>
            </tr>
        </table>
        """

        # High-value mismatches
        high_value_mismatches = self.classifier.find_high_value_mismatches(classifications, min_revenue=100)

        if high_value_mismatches:
            html += f"""
            <div class="warning-box">
                <h4>⚠️ High-Value Mismatches ({len(high_value_mismatches)} products)</h4>
                <p>These products generate significant revenue but are classified as Villains/Zombies by Product Hero:</p>
            </div>

            <table>
                <tr>
                    <th>Product</th>
                    <th>30-Day Revenue</th>
                    <th>Revenue Rank</th>
                    <th>Revenue Label</th>
                    <th>External Label</th>
                </tr>
            """

            for m in high_value_mismatches[:15]:  # Top 15
                html += f"""
                <tr>
                    <td>{m.product_title[:60]}</td>
                    <td>£{m.revenue:.2f}</td>
                    <td>{m.revenue_rank_pct:.0f}th percentile</td>
                    <td><strong>{m.revenue_label.replace('revenue_', '').replace('_', ' ').title()}</strong></td>
                    <td>{m.external_label.title()}</td>
                </tr>
                """

            html += """
            </table>
            <p><em>Recommendation: Review these products in Product Hero. Consider reclassifying as Heroes/Sidekicks.</em></p>
            """
        else:
            html += """
            <div class="summary-box">
                <p>✅ No significant label mismatches detected. Revenue classification aligns with Product Hero labels.</p>
            </div>
            """

        return html

    def send_email(self, html_content: str):
        """Send report via email"""
        try:
            from_email = get_secret("GMAIL_USERNAME")
            to_email = get_secret("GMAIL_USERNAME")  # Send to self
            password = get_secret("GMAIL_PASSWORD")

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Revenue Attribution Report - {datetime.now().strftime('%b %d, %Y')}"
            msg['From'] = from_email
            msg['To'] = to_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(from_email, password)
                server.send_message(msg)

            self.log("✅ Email sent successfully")

        except Exception as e:
            self.log(f"ERROR sending email: {e}")


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description='Generate weekly revenue attribution report')
    parser.add_argument('--test', action='store_true', help='Test mode')
    parser.add_argument('--client', type=str, help='Filter to specific client')
    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.json"
    reporter = RevenueAttributionReporter(config_path)

    # Generate report
    html = reporter.generate_report(client_filter=args.client)

    # Save to file
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = reporter.output_dir / f"revenue-attribution-{timestamp}.html"

    with open(output_file, 'w') as f:
        f.write(html)

    reporter.log(f"\n✅ Report saved: {output_file}")

    # Open in browser for review
    import subprocess
    subprocess.run(['open', str(output_file)])

    # Send email (unless test mode)
    if not args.test:
        reporter.send_email(html)

    reporter.log("="*80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
